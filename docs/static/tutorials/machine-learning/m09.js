(()=>{'use strict';
const zh=document.documentElement.lang.startsWith('zh'),q=s=>document.querySelector('#M09-'+s),tr=(a,b)=>zh?a:b;
let p={w:.3,lr:.1};
const calc=w=>{const z=2*w-.1,h=Math.tanh(z),loss=.5*(h-1)**2,gradient=(h-1)*(1-h*h)*2;return {z,h,loss,gradient}};
function state(){return {...p,...calc(p.w)}}
function draw(){const v=state();q('w').value=p.w;q('lr').value=p.lr;q('w-value').textContent=p.w.toFixed(3);q('lr-value').textContent=p.lr.toFixed(2);
 q('results').innerHTML=[['w',p.w],['z',v.z],['h',v.h],['L',v.loss],['dL/dw',v.gradient]].map(([a,b])=>'<tr><th>'+a+'</th><td>'+b.toFixed(6)+'</td></tr>').join('');
 const X=w=>65+(w+1)*165,Y=l=>260-l*105;let path='';for(let i=0;i<=180;i++){const w=-1+i/60;path+=(i?'L':'M')+X(w).toFixed(2)+','+Y(calc(w).loss).toFixed(2)}
 q('curve').setAttribute('d',path);q('point').setAttribute('cx',X(p.w));q('point').setAttribute('cy',Y(v.loss));
 q('tangent').setAttribute('x1',X(p.w-.22));q('tangent').setAttribute('y1',Y(v.loss-v.gradient*.22));q('tangent').setAttribute('x2',X(p.w+.22));q('tangent').setAttribute('y2',Y(v.loss+v.gradient*.22));
 q('interpretation').textContent=tr('当前梯度为 '+v.gradient.toFixed(4)+'；沿负梯度方向更新后，权重将为 '+(p.w-p.lr*v.gradient).toFixed(4)+'。橙线是当前位置的切线。','The current gradient is '+v.gradient.toFixed(4)+'. A negative-gradient update proposes weight '+(p.w-p.lr*v.gradient).toFixed(4)+'. The orange segment is the local tangent.');}
function set(a){if(Number.isFinite(a.w))p.w=Math.max(-1,Math.min(2,a.w));if(Number.isFinite(a.lr))p.lr=Math.max(.01,Math.min(1,a.lr));draw();return state()}
q('w').addEventListener('input',e=>set({w:+e.target.value}));q('lr').addEventListener('input',e=>set({lr:+e.target.value}));
q('step').addEventListener('click',()=>set({w:p.w-p.lr*calc(p.w).gradient}));q('reset').addEventListener('click',()=>set({w:.3,lr:.1}));
window.CourseLab={state,set,reset:()=>set({w:.3,lr:.1})};draw();
})();

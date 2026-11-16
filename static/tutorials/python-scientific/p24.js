(function(){
 'use strict';
 const root=document.getElementById('P24-lab');if(!root)return;
 const zh=document.documentElement.lang.startsWith('zh'),tr=(z,e)=>zh?z:e;
 const el=s=>root.querySelector('#P24-'+s), defaults={alpha:.5,position:1,exponent:-1};let params={...defaults};
 const U=(x,a)=>x*x+a*x**4/4,F=(x,a)=>2*x+a*x**3;
 const fmt=x=>x===0?'0':Math.abs(x)<.0001?x.toExponential(3):Number(x.toFixed(5)).toString();
 const txt=(x,y,t,size=16,anchor='start',color='#203642')=>`<text x="${x}" y="${y}" font-size="${size}" text-anchor="${anchor}" fill="${color}" font-family="Arial,Microsoft YaHei,sans-serif">${t}</text>`;
 function frame(id,w,h,title,xmin,xmax,ymin,ymax,xticks,yticks,xlabel,ylabel,xfmt=fmt,yfmt=fmt){
  const svg=el(id),m={l:74,r:24,t:55,b:64},x=v=>m.l+(v-xmin)/(xmax-xmin)*(w-m.l-m.r),y=v=>h-m.b-(v-ymin)/(ymax-ymin)*(h-m.t-m.b);
  let s=txt(m.l,27,title,18);
  for(const v of yticks)s+=`<path d="M${m.l},${y(v)}H${w-m.r}" stroke="#dce5e9"/>`+txt(m.l-10,y(v)+5,yfmt(v),16,'end');
  for(const v of xticks)s+=txt(x(v),h-m.b+25,xfmt(v),16,'middle');
  s+=`<path d="M${m.l},${m.t}V${h-m.b}H${w-m.r}" stroke="#617680" fill="none"/>`+txt((m.l+w-m.r)/2,h-12,xlabel,16,'middle');
  s+=`<text x="19" y="${(m.t+h-m.b)/2}" transform="rotate(-90 19 ${(m.t+h-m.b)/2})" font-size="16" text-anchor="middle" fill="#203642" font-family="Arial,Microsoft YaHei,sans-serif">${ylabel}</text>`;
  svg.setAttribute('viewBox',`0 0 ${w} ${h}`);
  return {x,y,s,svg};
 }
 const path=(pts,p,color,width=2,dash='')=>`<path d="${pts.map((v,i)=>(i?'L':'M')+p.x(v[0]).toFixed(3)+','+p.y(v[1]).toFixed(3)).join(' ')}" fill="none" stroke="${color}" stroke-width="${width}" ${dash?`stroke-dasharray="${dash}"`:''}/>`;
 const dot=(p,x,y,color,r=5)=>`<circle cx="${p.x(x)}" cy="${p.y(y)}" r="${r}" fill="${color}" stroke="white" stroke-width="1.5"/>`;
 function state(){const {alpha:a,position:x,exponent}=params,h=10**exponent,energy=U(x,a),force=F(x,a),difference=(U(x+h,a)-U(x-h,a))/(2*h);return {...params,h,energy,force,stiffness:2+3*a*x*x,difference,error:Math.abs(difference-force),exactError:a*x*h*h};}
 function render(){
  const s=state(),a=s.alpha,x=s.position,h=s.h,grid=Array.from({length:201},(_,i)=>i/100);
  for(const key of Object.keys(defaults))el(key).value=params[key];
  el('readout').textContent=tr(`α=${fmt(a)} N/mm³；x=${fmt(x)} mm；h=${fmt(h)} mm。储能 ${fmt(s.energy)} mJ，外力 ${fmt(s.force)} N，切线刚度 ${fmt(s.stiffness)} N/mm。差分 ${fmt(s.difference)} N，实际误差 ${fmt(s.error)} N，精确算术误差 ${fmt(s.exactError)} N。`,`α = ${fmt(a)} N/mm³; x = ${fmt(x)} mm; h = ${fmt(h)} mm. Energy ${fmt(s.energy)} mJ; force ${fmt(s.force)} N; tangent stiffness ${fmt(s.stiffness)} N/mm. Difference ${fmt(s.difference)} N; actual error ${fmt(s.error)} N; exact-arithmetic error ${fmt(s.exactError)} N.`);
  let p=frame('energy-view',900,360,tr('储能与当前位置的斜率','Energy and slope at the current position'),0,2,0,14,[0,.5,1,1.5,2],[0,2,4,6,8,10,12,14],tr('位移 / mm','Displacement / mm'),tr('储能 / mJ','Energy / mJ'));
  p.s+=path(grid.map(v=>[v,U(v,a)]),p,'#28658c',2.6);
  const ends=[Math.max(0,x-.2,x-s.energy/s.force),Math.min(2,x+.2)],tangent=ends.map(v=>[v,Math.max(0,s.energy+s.force*(v-x))]);
  if(tangent.length===2)p.s+=path(tangent,p,'#2b8a74',2,'7 4');
  p.s+=path([[x-h,U(x-h,a)],[x+h,U(x+h,a)]],p,'#c26835',2.5)+dot(p,x-h,U(x-h,a),'#c26835',5)+dot(p,x+h,U(x+h,a),'#c26835',5)+dot(p,x,s.energy,'#28658c',6);
  p.s+=txt(570,28,tr('切线斜率 = 外力','Tangent slope = applied force'),16,'start','#2b8a74');p.svg.innerHTML=p.s;
  p=frame('force-view',540,350,tr('同一位置的外力','Force at the same position'),0,2,0,20,[0,.5,1,1.5,2],[0,5,10,15,20],tr('位移 / mm','Displacement / mm'),tr('外力 / N','Force / N'));
  p.s+=path(grid.map(v=>[v,F(v,a)]),p,'#28658c',2.6)+path([[x,0],[x,s.force]],p,'#71838d',1.5,'5 4')+dot(p,x,s.force,'#28658c',6);p.svg.innerHTML=p.s;
  p=frame('error-view',540,350,tr('差分误差随步长变化','Difference error versus step'),-14,-1,-17,0,[-14,-10,-6,-2],[-16,-12,-8,-4,0],tr('半间距 h / mm','Half-spacing h / mm'),tr('绝对误差 / N','Absolute error / N'),v=>'10'+sup(v),v=>'10'+sup(v));
  const actual=[],theory=[];for(let i=0;i<=169;i++){const e=-14+13*i/169,q=10**e,err=Math.abs((U(x+q,a)-U(x-q,a))/(2*q)-s.force),ideal=a*x*q*q;if(err>=1e-17&&err<=1)actual.push([e,Math.log10(err)]);if(ideal>0&&Math.log10(ideal)>=-17)theory.push([e,Math.log10(ideal)]);}
  p.s+=path(actual,p,'#28658c',1.6);if(theory.length)p.s+=path(theory,p,'#c26835',2,'6 4');
  if(s.error>=1e-17&&s.error<=1)p.s+=dot(p,s.exponent,Math.log10(s.error),'#172b36',6);
  p.s+=path([[s.exponent,-17],[s.exponent,0]],p,'#71838d',1,'3 4');p.svg.innerHTML=p.s;
  return s;
 }
 function sup(v){return String(v).split('').map(c=>({'-':'⁻','0':'⁰','1':'¹','2':'²','3':'³','4':'⁴','5':'⁵','6':'⁶','7':'⁷','8':'⁸','9':'⁹'}[c])).join('');}
 function set(values={}){for(const key of Object.keys(defaults))if(values[key]!==undefined){const num=Number(values[key]);if(Number.isFinite(num))params[key]=num;}params.alpha=Math.max(0,Math.min(2,params.alpha));params.position=Math.max(.2,Math.min(1.8,params.position));params.exponent=Math.max(-10,Math.min(-1,params.exponent));return render();}
 for(const key of Object.keys(defaults))el(key).addEventListener('input',event=>set({[key]:event.target.value}));
 el('reset').addEventListener('click',()=>{params={...defaults};render();});
 window.CourseLab={state,set,reset(){params={...defaults};return render();},destroy(){}};render();
})();

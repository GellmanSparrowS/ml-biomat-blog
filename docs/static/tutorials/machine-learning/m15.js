(function(){
 'use strict'; const zh=document.documentElement.lang.startsWith('zh');
 const defaults={f:.9,i:.2,o:.7,steps:20,writeStep:8};let p={...defaults},timer=null;
 const el=k=>document.getElementById('M15-'+k),tr=(a,b)=>zh?a:b;
 if(!el('plot'))return;
 function values(){let c=.8;const rows=[{t:0,c,h:p.o*Math.tanh(c)}];for(let t=1;t<=p.steps;t++){c=p.f*c+(t===p.writeStep?p.i*(-.5):0);rows.push({t,c,h:p.o*Math.tanh(c)});}return rows;}
 function state(){const row=values().at(-1);return {...p,lastC:row.c,lastH:row.h,directRetention:p.f**p.steps};}
 function draw(){const rows=values(),s=state(),X=t=>65+t/40*795,Y=v=>300-(v+.6)/1.5*260;
  for(const k of Object.keys(p)){el(k).value=p[k];el(k+'-value').textContent=['steps','writeStep'].includes(k)?p[k]:p[k].toFixed(2);}
  let svg='';for(const v of [-.5,0,.5,.8])svg+=`<line x1="65" y1="${Y(v)}" x2="860" y2="${Y(v)}" stroke="#d9e0e4"/><text x="53" y="${Y(v)+5}" text-anchor="end" fill="currentColor">${v}</text>`;
  for(const t of [0,8,16,24,32,40])svg+=`<text x="${X(t)}" y="328" text-anchor="middle" fill="currentColor">${t}</text>`;
  svg+=`<line x1="${X(p.writeStep)}" y1="40" x2="${X(p.writeStep)}" y2="300" stroke="#8a9097" stroke-dasharray="5 5"/>`;
  for(const [key,color] of [['c','#0072B2'],['h','#D58500']]){svg+=`<path d="${rows.map((r,j)=>(j?'L':'M')+X(r.t)+','+Y(r[key])).join(' ')}" fill="none" stroke="${color}" stroke-width="3"/>`;for(const r of rows)svg+=`<circle cx="${X(r.t)}" cy="${Y(r[key])}" r="3" fill="${color}"/>`;}
  svg+=`<text x="65" y="23" fill="currentColor">${tr('状态（无量纲）','State (dimensionless)')}</text><text x="460" y="358" text-anchor="middle" fill="currentColor">${tr('时间步','Time step')}</text>`;el('plot').innerHTML=svg;
  el('result').textContent=tr(`第${p.steps}步：细胞状态 ${s.lastC.toFixed(5)}；隐藏读出 ${s.lastH.toFixed(5)}；初始内容沿直接通路保留 ${(s.directRetention*100).toFixed(2)}%。`,`Step ${p.steps}: cell state ${s.lastC.toFixed(5)}; hidden readout ${s.lastH.toFixed(5)}; direct retention of initial content ${(s.directRetention*100).toFixed(2)}%.`);
 }
 function stop(){if(timer){clearInterval(timer);timer=null;}el('play').textContent=tr('播放','Play');}
 function set(v){for(const k of ['f','i','o'])if(Number.isFinite(Number(v[k])))p[k]=Math.max(0,Math.min(1,Number(v[k])));for(const k of ['steps','writeStep'])if(Number.isFinite(Number(v[k])))p[k]=Math.max(1,Math.min(40,Math.round(Number(v[k]))));draw();return state();}
 function reset(){stop();p={...defaults};draw();return state();}
 for(const k of Object.keys(p))el(k).addEventListener('input',()=>{stop();set({[k]:+el(k).value});});
 el('step').addEventListener('click',()=>{stop();set({steps:Math.min(40,p.steps+1)});});
 el('play').addEventListener('click',()=>{if(timer){stop();return;}if(p.steps>=40)p.steps=1;el('play').textContent=tr('暂停','Pause');timer=setInterval(()=>{set({steps:p.steps+1});if(p.steps>=40)stop();},400);});
 el('reset').addEventListener('click',reset);window.CourseLab={state,set,reset,destroy:stop};draw();
})();

(()=>{
const zh=document.documentElement.lang.startsWith('zh');
const defaults={position:1.5,velocity:0,horizon:4,limit:1,step:0,disturbance:.6};
let parameters={...defaults},output={};
const el=id=>document.getElementById('M38-'+id);
const advance=(x,u)=>[x[0]+.5*x[1]+.125*u,x[1]+.5*u];
function plan(x){
 const options=[-parameters.limit,0,parameters.limit],candidates=[];
 function visit(state,actions,path,cost){
  if(actions.length===parameters.horizon){candidates.push({actions,path,cost});return;}
  for(const u of options){
   const next=advance(state,u),last=actions.length===parameters.horizon-1;
   const stage=(last?2:1)*next[0]**2+(last?.5:.1)*next[1]**2+.1*u*u;
   visit(next,[...actions,u],[...path,next],cost+stage);
  }
 }
 visit(x,[],[x],0);candidates.sort((a,b)=>a.cost-b.cost);
 return candidates;
}
function render(){
 let x=[parameters.position,parameters.velocity],history=[x],applied=[];
 for(let k=0;k<parameters.step;k++){
  const u=plan(x)[0].actions[0];x=advance(x,u);
  if(k===2)x=[x[0],x[1]+parameters.disturbance];
  history.push(x);applied.push(u);
 }
 const candidates=plan(x),best=candidates[0];
 output={...parameters,currentPosition:x[0],currentVelocity:x[1],firstAction:best.actions[0],plannedCost:best.cost,candidates:candidates.length,plan:best.actions,history,applied};
 for(const key of ['position','velocity','horizon','limit','disturbance'])if(el(key))el(key).value=parameters[key];
 const svg=el('plot');let s='<rect width="900" height="410" fill="white"/>';
 const text=(x,y,t,anchor='start',color='#243a49')=>`<text x="${x}" y="${y}" text-anchor="${anchor}" font-family="sans-serif" font-size="14" fill="${color}">${t}</text>`;
 const bounds=Math.max(1.5,...history.map(z=>Math.abs(z[0])),...candidates.slice(0,6).flatMap(c=>c.path.map(z=>Math.abs(z[0]))))*1.15;
 const line=(path,x0,width,steps,color,stroke=2,opacity=1)=>`<polyline points="${path.map((p,i)=>`${x0+i*width/Math.max(steps,1)},${195-p[0]*130/bounds}`).join(' ')}" fill="none" stroke="${color}" stroke-width="${stroke}" opacity="${opacity}"/>`;
 s+=text(62,28,zh?'已执行的真实轨迹':'Executed trajectory');s+=text(510,28,zh?'从当前测量重新规划':'Replan from current measurement');
 for(const [x0,width,steps]of [[65,335,12],[510,335,parameters.horizon]]){
  s+=`<path d="M${x0},55 V330 H${x0+width}" fill="none" stroke="#8da1ad"/><path d="M${x0},195 H${x0+width}" stroke="#b9c6cd" stroke-dasharray="4 5"/>`;
  for(const v of [-bounds,0,bounds])s+=text(x0-8,200-v*130/bounds,v.toFixed(1),'end');
  for(let k=0;k<=steps;k++)s+=text(x0+k*width/steps,350,String(k),'middle');
  s+=text(x0+width/2,380,zh?'相对步数（每步 0.5 s）':'Steps (0.5 s each)','middle');
 }
 s+=text(18,48,zh?'位置 / m':'Position / m');
 if(parameters.step>=3){const xd=65+3*335/12;s+=`<path d="M${xd},55 V330" stroke="#c7524c" stroke-dasharray="5 4"/>`;}
 s+=line(history,65,335,12,'#246e85',3);
 for(const c of candidates.slice(1,6))s+=line(c.path,510,335,parameters.horizon,'#b8c3cb',1.6,.7);
 s+=line(best.path,510,335,parameters.horizon,'#dd8a33',3);
 s+=`<circle cx="${65+parameters.step*335/12}" cy="${195-x[0]*130/bounds}" r="5" fill="#246e85"/>`;
 s+=text(510,403,zh?'橙色：最小代价；灰色：其后五条候选':'Orange: minimum cost; gray: next five candidates');
 if(svg)svg.innerHTML=s;
 el('status').textContent=zh?`已执行 ${parameters.step} 步；位置 ${x[0].toFixed(3)} m，速度 ${x[1].toFixed(3)} m/s。比较 ${candidates.length} 条计划，下一动作 ${best.actions[0].toFixed(2)} m/s²，预测代价 ${best.cost.toFixed(5)}。`:`Executed ${parameters.step} steps; position ${x[0].toFixed(3)} m, velocity ${x[1].toFixed(3)} m/s. Compared ${candidates.length} plans; next action ${best.actions[0].toFixed(2)} m/s²; predicted cost ${best.cost.toFixed(5)}.`;
 el('actions').textContent=(zh?'当前最优计划：':'Current best plan: ')+best.actions.map(u=>u.toFixed(2)).join(' → ')+' m/s²';
 el('next').disabled=parameters.step>=12;
}
function set(values){
 const numeric={};for(const k of Object.keys(defaults))if(k in values&&Number.isFinite(Number(values[k])))numeric[k]=Number(values[k]);
 parameters={...parameters,...numeric};parameters.horizon=Math.max(1,Math.min(6,Math.round(parameters.horizon)));parameters.step=Math.max(0,Math.min(12,Math.round(parameters.step)));parameters.limit=Math.max(.25,Math.min(2,parameters.limit));parameters.position=Math.max(-3,Math.min(3,parameters.position));parameters.velocity=Math.max(-2,Math.min(2,parameters.velocity));parameters.disturbance=Math.max(-1,Math.min(1,parameters.disturbance));render();return output;
}
for(const key of ['position','velocity','horizon','limit','disturbance'])el(key).addEventListener('input',()=>set({[key]:el(key).value,step:0}));
el('next').addEventListener('click',()=>set({step:parameters.step+1}));el('reset').addEventListener('click',()=>{parameters={...defaults};render();});
window.CourseLab={set,state:()=>JSON.parse(JSON.stringify(output)),reset:()=>{parameters={...defaults};render();return output;}};
render();
})();

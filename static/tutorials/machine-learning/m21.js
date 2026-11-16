(()=>{
 const get=id=>document.getElementById('M21-'+id);if(!get('lab'))return;
 const zh=document.documentElement.lang.startsWith('zh');let p={origin:28,horizon:7,trend:0,shift:6,method:'seasonal',reveal:false},result;
 const season=[0,2,4,3,1,-1,-2],value=t=>20+p.trend*t+season[t%7]+(t>=42?p.shift:0);
 function compute(){
  const history=Array.from({length:p.origin},(_,i)=>value(i)),days=Array.from({length:p.horizon},(_,i)=>p.origin+i);
  const forecasts=days.map((t,i)=>p.method==='seasonal'?history[p.origin-7+i]:p.method==='naive'?history[p.origin-1]:history[p.origin-1]+(i+1)*(history[p.origin-1]-history[p.origin-14])/13);
  const truth=days.map(value),errors=truth.map((v,i)=>Math.abs(v-forecasts[i])),mae=errors.reduce((a,b)=>a+b,0)/p.horizon;
  result={...p,days,forecasts,truth,errors,mae,latestInput:p.origin-1};
  const shown=history.concat(forecasts,p.reveal?truth:[]),lo=Math.floor((Math.min(...shown)-3)/5)*5,hi=Math.ceil((Math.max(...shown)+3)/5)*5;
  const X=t=>65+t/63*830,Y=v=>335-(v-lo)/(hi-lo)*265;
  let s='<rect width="940" height="420" fill="#f7f9fb" rx="12"/>';
  s+=`<rect x="${X(Math.max(0,p.origin-14))}" y="70" width="${X(p.origin)-X(Math.max(0,p.origin-14))}" height="265" fill="#e4edf4"/><rect x="${X(p.origin)}" y="70" width="${895-X(p.origin)}" height="265" fill="#fff2dc"/>`;
  for(let k=0;k<=5;k++){const v=lo+k*(hi-lo)/5;s+=`<line x1="65" x2="895" y1="${Y(v)}" y2="${Y(v)}" stroke="#d5dfe5"/><text x="55" y="${Y(v)+5}" text-anchor="end" font-size="14">${v.toFixed(0)}</text>`;}
  for(let t=0;t<=63;t+=7)s+=`<text x="${X(t)}" y="360" text-anchor="middle" font-size="14">${t}</text>`;
  const path=(ys,ts)=>ys.map((v,i)=>(i?'L':'M')+X(ts[i])+','+Y(v)).join(' ');
  s+=`<path d="${path(history,history.map((_,i)=>i))}" fill="none" stroke="#526575" stroke-width="2.5"/><line x1="${X(p.origin)}" x2="${X(p.origin)}" y1="65" y2="340" stroke="#b1711c" stroke-dasharray="6 4"/><path d="${path(forecasts,days)}" fill="none" stroke="#be6320" stroke-width="3"/>`;
  if(p.reveal)s+=`<path d="${path(truth,days)}" fill="none" stroke="#157c79" stroke-width="2.5"/>`;
  forecasts.forEach((v,i)=>{s+=`<circle cx="${X(days[i])}" cy="${Y(v)}" r="4" fill="#be6320"/>`;if(p.reveal)s+=`<line x1="${X(days[i])}" x2="${X(days[i])}" y1="${Y(v)}" y2="${Y(truth[i])}" stroke="#889da7" stroke-dasharray="3 3"/><circle cx="${X(days[i])}" cy="${Y(truth[i])}" r="3.5" fill="#157c79"/>`;});
  s+=`<text x="65" y="28" font-size="16">${zh?'需求量（统一单位）':'Demand (common units)'}</text><text x="500" y="395" text-anchor="middle" font-size="15">${zh?'日索引':'Day index'}</text><text x="895" y="28" text-anchor="end" font-size="15" fill="#b1711c">${zh?'预测起点':'Origin'} ${p.origin}</text>`;
  const labels=zh?['灰：已知历史','橙：预测','青：未来真值','蓝底：最近14天']:['Gray: observed history','Orange: forecast','Teal: future outcomes','Blue: latest 14 days'];
  labels.forEach((t,i)=>{s+=`<text x="${65+i*205}" y="52" font-size="13">${t}</text>`;});get('svg').innerHTML=s;
  get('status').textContent=zh?`最新输入为第 ${p.origin-1} 天；预测第 ${p.origin} 至 ${p.origin+p.horizon-1} 天。${p.reveal?'平均绝对误差 '+mae.toFixed(3)+'。':'未来真值已隐藏。'}`:`Latest input: day ${p.origin-1}. Forecast days ${p.origin}–${p.origin+p.horizon-1}. ${p.reveal?'MAE '+mae.toFixed(3)+'.':'Future outcomes are hidden.'}`;
  get('table').innerHTML='<table><thead><tr>'+ (zh?['日索引','预测','真值','绝对误差']:['Day','Forecast','Outcome','Absolute error']).map(v=>'<th>'+v+'</th>').join('')+'</tr></thead><tbody>'+days.map((t,i)=>`<tr><td>${t}</td><td>${forecasts[i].toFixed(2)}</td><td>${p.reveal?truth[i].toFixed(2):'—'}</td><td>${p.reveal?errors[i].toFixed(2):'—'}</td></tr>`).join('')+'</tbody></table>';
  ['origin','horizon','trend','shift','method'].forEach(k=>get(k).value=p[k]);get('reveal').checked=p.reveal;
 }
 function state(){return JSON.parse(JSON.stringify(result));}
 function set(v={}){for(const [k,l,h]of[['origin',14,56],['horizon',1,7],['trend',0,1],['shift',0,10]])if(v[k]!==undefined)p[k]=Math.max(l,Math.min(h,Number(v[k])));p.origin=Math.round(p.origin);p.horizon=Math.round(p.horizon);if(['seasonal','naive','drift'].includes(v.method))p.method=v.method;if(v.reveal!==undefined)p.reveal=Boolean(v.reveal);compute();return state();}
 function reset(){p={origin:28,horizon:7,trend:0,shift:6,method:'seasonal',reveal:false};compute();return state();}
 ['origin','horizon','trend','shift'].forEach(k=>get(k).addEventListener('input',e=>set({[k]:e.target.value})));
 get('method').addEventListener('change',e=>set({method:e.target.value}));get('reveal').addEventListener('change',e=>set({reveal:e.target.checked}));get('next').addEventListener('click',()=>set({origin:p.origin+7}));get('reset').addEventListener('click',reset);window.CourseLab={set,state,reset};compute();
})();

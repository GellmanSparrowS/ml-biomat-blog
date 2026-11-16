(() => {
 const root=document.getElementById('P16-lab');if(!root)return;
 const zh=document.documentElement.lang.startsWith('zh'),tr=(a,b)=>zh?a:b,el=x=>root.querySelector('#P16-'+x);
 const defaults={tau:4,time:4,vmax:4},taus=[1,2,4,8],times=Array.from({length:25},(_,i)=>i/2);let p={...defaults},result={};
 const mass=(tau,t)=>4*Math.exp(-t/tau), text=(x,y,s,anchor='start',size=14)=>`<text x="${x}" y="${y}" text-anchor="${anchor}" font-size="${size}" fill="#20313e">${s}</text>`;
 const stops=[[68,1,84],[59,82,139],[33,145,140],[94,201,98],[253,231,37]];
 function color(x){const k=Math.max(0,Math.min(1,x))*4,i=Math.min(3,Math.floor(k)),f=k-i;return`rgb(${stops[i].map((c,j)=>Math.round(c*(1-f)+stops[i+1][j]*f)).join(',')})`}
 function draw(){
  const wide=root.getBoundingClientRect().width>720,width=wide?860:430,L=68,W=width-L-25,H=160,T=59,X=t=>L+t/12*W;
  const svg=el('map');svg.setAttribute('viewBox',`0 0 ${width} 340`);
  let s=text(L,23,tr('质量总览 · 4 个离散条件','Mass overview · 4 discrete conditions'),'start',17)+text(L,46,tr('行标签：时间常数 / min','Row labels: time constant / min'));
  taus.forEach((tau,j)=>{times.forEach((t,i)=>{const left=i===0?0:t-.25,right=i===24?12:t+.25;s+=`<rect x="${X(left)}" y="${T+j*40}" width="${(right-left)/12*W+.2}" height="40" fill="${color(mass(tau,t)/p.vmax)}"/>`});s+=text(L-12,T+j*40+25,tau,'end')});
  s+=`<line x1="${X(p.time)}" x2="${X(p.time)}" y1="${T}" y2="${T+H}" stroke="#fff" stroke-width="2" stroke-dasharray="4 3"/><circle cx="${X(p.time)}" cy="${T+taus.indexOf(p.tau)*40+20}" r="8" fill="none" stroke="#111" stroke-width="3"/><circle cx="${X(p.time)}" cy="${T+taus.indexOf(p.tau)*40+20}" r="10" fill="none" stroke="#fff" stroke-width="2"/>`;
  [0,3,6,9,12].forEach(t=>{s+=text(X(t),T+H+22,t,'middle')});s+=text(L+W/2,265,tr('时间 / min','Time / min'),'middle');
  for(let i=0;i<100;i++)s+=`<rect x="${L+i*W/100}" y="285" width="${W/100+.5}" height="13" fill="${color(i/99)}"/>`;
  s+=text(L,321,'0 mg')+text(L+W/2,321,tr('线性质量颜色尺度','Linear mass color scale'),'middle')+text(L+W,321,`${p.vmax} mg`,'end');svg.innerHTML=s;
  for(const mode of ['linear','log']){
   const a=el(mode),left=68,top=58,w=332,h=223,xx=t=>left+t/12*w;
   const yy=v=>top+h-(mode==='log'?(Math.log10(v)+5)/6:v/4)*h;
   a.setAttribute('viewBox','0 0 430 350');let c=text(left,23,tr(mode==='log'?'倍数差异':'绝对量差异',mode==='log'?'Ratio differences':'Absolute differences'),'start',17)+text(left,46,tr('剩余质量 / mg','Remaining mass / mg'));
   const ticks=mode==='log'?[.00001,.001,.1,1,10]:[0,1,2,3,4];
   ticks.forEach(v=>{c+=`<line x1="${left}" x2="${left+w}" y1="${yy(v)}" y2="${yy(v)}" stroke="#dce3e8"/>`+text(left-8,yy(v)+5,mode==='log'&&v<.001?v.toExponential(0):v,'end')});
   const pts=Array.from({length:121},(_,i)=>[i/10,mass(p.tau,i/10)]);c+=`<path d="${pts.map(([t,v],i)=>`${i?'L':'M'}${xx(t)},${yy(v)}`).join(' ')}" fill="none" stroke="#28658c" stroke-width="2.5"/><line x1="${xx(p.time)}" x2="${xx(p.time)}" y1="${top}" y2="${top+h}" stroke="#b64a35" stroke-dasharray="4 4"/><circle cx="${xx(p.time)}" cy="${yy(mass(p.tau,p.time))}" r="6" fill="#b64a35" stroke="#fff"/>`;
   [0,3,6,9,12].forEach(t=>{c+=text(xx(t),top+h+22,t,'middle')});c+=text(left+w/2,335,tr('时间 / min','Time / min'),'middle');a.innerHTML=c;
  }
  const m=mass(p.tau,p.time),above=taus.flatMap(tau=>times.map(t=>mass(tau,t))).filter(v=>v>p.vmax).length;
  result={...p,mass:m,above,color_fraction:Math.min(1,m/p.vmax),grid_points:100,half_time:p.tau*Math.log(2)};
  el('readout').textContent=tr(`t = ${p.time} min，τ = ${p.tau} min：${m.toPrecision(6)} mg；半衰时间 ${result.half_time.toFixed(3)} min。100个网格点中，${above} 个超过颜色上限。`,`t = ${p.time} min, τ = ${p.tau} min: ${m.toPrecision(6)} mg; half-time ${result.half_time.toFixed(3)} min. ${above} of 100 grid points exceed the color limit.`);
  el('time-value').textContent=p.time;
 }
 function set(q){p={...p,...q};p.tau=taus.includes(+p.tau)?+p.tau:4;p.time=Math.max(0,Math.min(12,+p.time));p.vmax=+p.vmax===2?2:4;for(const key of ['tau','time','vmax'])el(key).value=p[key];draw();return result}
 for(const key of ['tau','time','vmax'])el(key).addEventListener('input',()=>set({[key]:+el(key).value}));el('reset').addEventListener('click',()=>set(defaults));
 let observer=null,lastWidth=0;if(typeof ResizeObserver!=='undefined'){observer=new ResizeObserver(()=>{const w=root.getBoundingClientRect().width;if(Math.abs(w-lastWidth)>1){lastWidth=w;draw()}});observer.observe(root)}
 window.CourseLab={set,state:()=>structuredClone(result),reset:()=>set(defaults),destroy:()=>observer?.disconnect()};set(defaults);
})();

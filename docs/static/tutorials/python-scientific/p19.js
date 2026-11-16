(() => {
  const root=document.getElementById('P19-lab'); if(!root)return;
  const zh=document.documentElement.lang.startsWith('zh'), tr=(a,b)=>zh?a:b;
  const noise=[.04,-.03,.02,-.05,.01,.03,-.02,.04,-.01,-.03,.02,-.04,.03,0,-.02,.01,.03,-.01,-.03,.02,-.01,.03,-.02,.01,-.02];
  const data=noise.map((e,i)=>({t:i/2,y:2.4*Math.exp(-i/6)+.4+e}));
  const defaults={tau:3,tmax:12}; let settings={...defaults}, result={};
  const el=id=>root.querySelector('#P19-'+id), fmt=x=>Number(x).toFixed(5);
  function fit(tau,tmax){
    const d=data.filter(p=>p.t<=tmax), z=d.map(p=>Math.exp(-p.t/tau));
    const mz=z.reduce((a,b)=>a+b,0)/d.length,my=d.reduce((a,p)=>a+p.y,0)/d.length;
    const A=z.reduce((s,v,i)=>s+(v-mz)*(d[i].y-my),0)/z.reduce((s,v)=>s+(v-mz)**2,0);
    const b=my-A*mz, residual=d.map((p,i)=>p.y-(A*z[i]+b));
    return {A,b,Q:residual.reduce((s,v)=>s+v*v,0),n:d.length,residual};
  }
  const text=(x,y,s,anchor='start',size=14,color='#202e39')=>`<text x="${x}" y="${y}" text-anchor="${anchor}" font-size="${size}" fill="${color}">${s}</text>`;
  function chart(svg,title,xmin,xmax,ymin,ymax,xlabel,ylabel){
    const rawStep=(ymax-ymin)/4, magnitude=10**Math.floor(Math.log10(rawStep));
    const step=[1,2,2.5,5,10].find(v=>v*magnitude>=rawStep-1e-12)*magnitude;
    ymin=Math.floor(ymin/step)*step; ymax=Math.ceil(ymax/step)*step;
    const tickLabel=value=>Math.abs(value)<step*1e-8?'0':String(Number(value.toPrecision(10)));
    const wide=svg.id==='P19-curve' && root.getBoundingClientRect().width>720;
    if(svg.setAttribute)svg.setAttribute('viewBox',wide?'0 0 860 350':'0 0 430 350');
    const L=68,T=57,W=wide?760:330,H=225, X=x=>L+(x-xmin)/(xmax-xmin)*W,Y=y=>T+H-(y-ymin)/(ymax-ymin)*H;
    let s=text(L,22,title,'start',17)+text(L,43,ylabel,'start',14,'#596b78');
    for(let i=0;i<=Math.round((ymax-ymin)/step);i++){const y=ymin+step*i; s+=`<line x1="${L}" x2="${L+W}" y1="${Y(y)}" y2="${Y(y)}" stroke="#dce3e8"/>`+text(L-8,Y(y)+4,tickLabel(y),'end');}
    for(let i=0;i<5;i++){const x=xmin+(xmax-xmin)*i/4;s+=text(X(x),T+H+20,x.toFixed(xmax<=7?1:0),'middle');}
    s+=`<path d="M${L},${T}V${T+H}H${L+W}" fill="none" stroke="#202e39"/>`+text(L+W/2,330,xlabel,'middle',14);
    return {s,X,Y,L,T,W,H,svg};
  }
  function draw(){
    const {tau,tmax}=settings,f=fit(tau,tmax), pred=t=>f.A*Math.exp(-t/tau)+f.b;
    const curve=Array.from({length:161},(_,i)=>({x:12*i/160,y:pred(12*i/160)}));
    const profile=Array.from({length:301},(_,i)=>{const q=1+i/50;return{x:q,y:fit(q,tmax).Q}});
    const low=profile.reduce((a,b)=>a.y<b.y?a:b);
    result={...settings,A:f.A,b:f.b,Q:f.Q,n:f.n,first_observed:data[0].y,last_prediction:pred(12),grid_best_tau:low.x};
    const ylo=Math.min(0,Math.floor(Math.min(...curve.map(p=>p.y))*2)/2), yhi=3.2;
    let c=chart(el('curve'),tr('曲线与纳入范围','Curve and included interval'),0,12,ylo,yhi,tr('时间 / s','Time / s'),tr('应力 / kPa','Stress / kPa'));
    c.s+=`<rect x="${c.X(0)}" y="${c.T}" width="${c.X(tmax)-c.X(0)}" height="${c.H}" fill="#28658c" opacity=".07"/>`;
    c.s+=`<path d="${curve.map((p,i)=>(i?'L':'M')+c.X(p.x)+','+c.Y(p.y)).join('')}" fill="none" stroke="#28658c" stroke-width="2.3"/>`;
    for(const p of data)c.s+=`<circle cx="${c.X(p.t)}" cy="${c.Y(p.y)}" r="3.6" stroke="#202e39" stroke-width="1.1" fill="${p.t<=tmax?'#202e39':'white'}"/>`;
    c.svg.innerHTML=c.s;
    const rmax=Math.max(.06,...f.residual.map(Math.abs))*1.25;
    c=chart(el('residual'),tr('同一组记录的残差','Residuals of the same records'),0,12,-rmax,rmax,tr('时间 / s','Time / s'),tr('观测 − 模型 / kPa','Observed − model / kPa'));
    c.s+=`<line x1="${c.L}" x2="${c.L+c.W}" y1="${c.Y(0)}" y2="${c.Y(0)}" stroke="#71808b"/>`;
    f.residual.forEach((r,i)=>{c.s+=`<line x1="${c.X(data[i].t)}" x2="${c.X(data[i].t)}" y1="${c.Y(0)}" y2="${c.Y(r)}" stroke="#b64a35" stroke-width="1.5"/><circle cx="${c.X(data[i].t)}" cy="${c.Y(r)}" r="3" fill="#b64a35"/>`});
    c.svg.innerHTML=c.s;
    c=chart(el('profile'),tr('重新拟合A、b后的误差','Error after refitting A and b'),1,7,0,Math.max(...profile.map(p=>p.y)) * 1.05,tr('固定的 τ / s','Fixed τ / s'),'SSE / kPa²');
    c.s+=`<path d="${profile.map((p,i)=>(i?'L':'M')+c.X(p.x)+','+c.Y(p.y)).join('')}" fill="none" stroke="#28658c" stroke-width="2.1"/>`;
    c.s+=`<line x1="${c.X(tau)}" x2="${c.X(tau)}" y1="${c.Y(0)}" y2="${c.Y(f.Q)}" stroke="#b64a35" stroke-dasharray="3 3"/><circle cx="${c.X(tau)}" cy="${c.Y(f.Q)}" r="5.4" fill="#b64a35" stroke="white" stroke-width="1.5"/>`;
    c.svg.innerHTML=c.s;
    el('tau').value=tau;el('tmax').value=tmax;
    el('tau-value').textContent=tau.toFixed(2)+' s';
    el('numbers').textContent=`n=${f.n} · A=${fmt(f.A)} kPa · b=${fmt(f.b)} kPa · SSE=${fmt(f.Q)} kPa²`;
    el('interpret').textContent=tr(`当前固定τ=${tau.toFixed(2)} s，使用0–${tmax} s的${f.n}个记录重新拟合A和b。网格中最低点位于τ≈${low.x.toFixed(2)} s（网格间隔0.02 s）。空心点保留在图中，未参与当前拟合。`,
      `At fixed τ=${tau.toFixed(2)} s, A and b are refitted to ${f.n} records from 0–${tmax} s. The lowest sampled profile point is at τ≈${low.x.toFixed(2)} s (0.02 s grid). Hollow points remain visible and are excluded from this fit.`);
  }
  function set(p={}){if(Number.isFinite(+p.tau))settings.tau=Math.max(1,Math.min(7,+p.tau));if([3,6,12].includes(+p.tmax))settings.tmax=+p.tmax;draw();return {...result}}
  el('tau').addEventListener('input',e=>set({tau:+e.target.value}));el('tmax').addEventListener('change',e=>set({tmax:+e.target.value}));
  const reset=()=>{settings={...defaults};draw();return{...result}};el('reset').addEventListener('click',reset);
  let observer=null,lastWidth=0;
  if(typeof ResizeObserver!=='undefined'){observer=new ResizeObserver(entries=>{const width=entries[0].contentRect.width;if(Math.abs(width-lastWidth)>1){lastWidth=width;draw()}});observer.observe(root)}
  window.CourseLab={set,state:()=>({...result}),reset,destroy:()=>observer?.disconnect()};draw();
})();

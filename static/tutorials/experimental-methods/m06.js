(() => {
  const zh=document.documentElement.lang.startsWith('zh');
  const defaults={stress:500,hold:180,tau:40};let p={...defaults};
  const el=k=>document.getElementById('M06-'+k);
  const compliance=t=>2e-5+4e-5*(1-Math.exp(-t/p.tau))+t/2e7;
  const strain=t=>p.stress*(compliance(t)-(t>=p.hold?compliance(t-p.hold):0));
  function state(){return {...p,peakPercent:100*p.stress*compliance(p.hold),residualPercent:100*p.stress*p.hold/2e7};}
  function render(){
    ['stress','hold','tau'].forEach(k=>{el(k).value=p[k];el(k+'-value').textContent=p[k];});
    const s=state(), xmax=p.hold+Math.max(240,5*p.tau), ymax=Math.max(1,s.peakPercent*1.2);
    const x=t=>70+680*t/xmax,y=v=>335-280*v/ymax;
    let svg='<rect x="0" y="0" width="800" height="400" fill="#faf9f5"/>';
    for(let i=0;i<=4;i++){
      const vy=ymax*i/4,tx=xmax*i/4;
      svg+=`<path d="M70 ${y(vy)}H750" stroke="#dce3e4"/><text x="59" y="${y(vy)+5}" text-anchor="end" font-size="14">${vy.toFixed(1)}</text><text x="${x(tx)}" y="359" text-anchor="middle" font-size="14">${Math.round(tx)}</text>`;
    }
    svg+=`<path d="M70 55V335H750" fill="none" stroke="#435964"/><text x="410" y="390" text-anchor="middle" font-size="16">${zh?'时间 / s':'Time / s'}</text><text x="20" y="195" transform="rotate(-90 20 195)" text-anchor="middle" font-size="16">${zh?'应变 / %':'Strain / %'}</text>`;
    const ts=[...Array(151)].map((_,i)=>p.hold*i/151).concat([p.hold-1e-7,p.hold], [...Array(151)].map((_,i)=>p.hold+(xmax-p.hold)*(i+1)/151));
    const d=ts.map((t,i)=>(i?'L':'M')+x(t).toFixed(2)+' '+y(strain(t)*100).toFixed(2)).join('');
    svg+=`<path d="${d}" fill="none" stroke="#176c83" stroke-width="3"/><path d="M${x(p.hold)} 55V335" stroke="#84969d" stroke-dasharray="4 5"/><path d="M70 ${y(s.residualPercent)}H750" stroke="#cc7d36" stroke-width="2" stroke-dasharray="6 5"/><text x="78" y="25" font-size="15" fill="#176c83">${zh?'蓝线：应变响应；橙虚线：长期残余':'Blue: strain response; orange dashed: long-time residual'}</text>`;
    el('plot').innerHTML=svg;
    el('readout').textContent=zh?`卸载前峰值 ${s.peakPercent.toFixed(3)}%；长期残余 ${s.residualPercent.toFixed(3)}%。保持 ${p.hold} s 后卸载。`:`Peak before unloading: ${s.peakPercent.toFixed(3)}%; long-time residual: ${s.residualPercent.toFixed(3)}%. Unload after ${p.hold} s.`;
  }
  function set(v){for(const k of ['stress','hold','tau'])if(k in v){const e=el(k);p[k]=Math.max(+e.min,Math.min(+e.max,+v[k]));}render();}
  function reset(){p={...defaults};render();}
  for(const k of ['stress','hold','tau'])el(k).addEventListener('input',()=>set({[k]:+el(k).value}));
  el('double').addEventListener('click',()=>set({stress:Math.min(1000,p.stress*2)}));
  el('reset').addEventListener('click',reset);
  window.CourseLab={set,state,reset};render();
})();

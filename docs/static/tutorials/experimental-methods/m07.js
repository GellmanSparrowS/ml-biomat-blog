(() => {
 const zh=document.documentElement.lang.startsWith('zh'),el=k=>document.getElementById('M07-'+k);
 const defaults={omega:10,amplitude:.2,tau:.1};let p={...defaults};
 function state(){const x=p.omega*p.tau,storageMPa=2+8*x*x/(1+x*x),lossMPa=8*x/(1+x*x);return {...p,storageMPa,lossMPa,tanDelta:lossMPa/storageMPa,energy:Math.PI*lossMPa*1e6*(p.amplitude/100)**2,phaseDegrees:Math.atan2(lossMPa,storageMPa)*180/Math.PI};}
 function render(){
  for(const k of ['omega','amplitude','tau']){el(k).value=p[k];el(k+'-value').textContent=p[k];}
  const s=state(),maxStrain=.55,maxStress=55,xx=v=>75+660*(v+maxStrain)/(2*maxStrain),yy=v=>345-285*(v+maxStress)/(2*maxStress);
  let svg='<rect width="800" height="420" fill="#faf9f5"/>';
  for(let i=-2;i<=2;i++){let strain=i*.25,stress=i*25;svg+=`<path d="M${xx(strain)} 60V345M75 ${yy(stress)}H735" stroke="#dce3e4"/><text x="${xx(strain)}" y="370" text-anchor="middle" font-size="14">${strain.toFixed(2)}</text><text x="64" y="${yy(stress)+5}" text-anchor="end" font-size="14">${stress}</text>`;}
  const path=[...Array(301)].map((_,i)=>{let q=2*Math.PI*i/300,strain=p.amplitude*Math.sin(q),stress=p.amplitude/100*(s.storageMPa*Math.sin(q)+s.lossMPa*Math.cos(q))*1000;return (i?'L':'M')+xx(strain).toFixed(3)+' '+yy(stress).toFixed(3);}).join('')+'Z';
  svg+=`<path d="${path}" fill="#186e83" fill-opacity=".16" stroke="#186e83" stroke-width="3"/><path d="M75 60V345H735" stroke="#435964" fill="none"/><text x="400" y="405" text-anchor="middle" font-size="16">${zh?'应变 / %':'Strain / %'}</text><text x="20" y="205" transform="rotate(-90 20 205)" text-anchor="middle" font-size="16">${zh?'应力 / kPa':'Stress / kPa'}</text><text x="75" y="27" font-size="15">${zh?'固定坐标范围便于比较回线面积':'Fixed axes make loop areas directly comparable'}</text>`;
  el('plot').innerHTML=svg;
  el('readout').textContent=zh?`E′ = ${s.storageMPa.toFixed(3)} MPa；E″ = ${s.lossMPa.toFixed(3)} MPa；相位 ${s.phaseDegrees.toFixed(2)}°；每周期耗散 ${s.energy.toFixed(2)} J/m³；频率 ${(p.omega/(2*Math.PI)).toFixed(3)} Hz。`:`E′ = ${s.storageMPa.toFixed(3)} MPa; E″ = ${s.lossMPa.toFixed(3)} MPa; phase ${s.phaseDegrees.toFixed(2)}°; dissipation ${s.energy.toFixed(2)} J/m³ per cycle; frequency ${(p.omega/(2*Math.PI)).toFixed(3)} Hz.`;
 }
 function set(v){for(const k of ['omega','amplitude','tau'])if(k in v){const e=el(k);p[k]=Math.max(+e.min,Math.min(+e.max,+v[k]));}render();}
 function reset(){p={...defaults};render();}
 for(const k of ['omega','amplitude','tau'])el(k).addEventListener('input',()=>set({[k]:+el(k).value}));
 el('double').addEventListener('click',()=>set({amplitude:Math.min(.5,2*p.amplitude)}));el('reset').addEventListener('click',reset);
 window.CourseLab={set,state,reset};render();
})();

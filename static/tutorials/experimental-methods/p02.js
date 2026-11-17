(() => {
 const zh=document.documentElement.lang.startsWith('zh'), keys=['logI','delta','surface'];
 const controls=Object.fromEntries(keys.map(k=>[k,document.getElementById('P02-'+k)]));
 const plot=document.getElementById('P02-plot'), result=document.getElementById('P02-result');
 let current={}; const L=(z,e)=>zh?z:e;
 function render(){
  const v=Object.fromEntries(keys.map(k=>[k,Number(controls[k].value)]));
  const ionic=10**v.logI,eps=8.8541878128e-12*78.4;
  const lam=Math.sqrt(eps*1.380649e-23*298.15/(2*(1.602176634e-19)**2*6.02214076e23*ionic))*1e9;
  const attenuation=Math.exp(-v.delta/lam),zeta=v.surface*attenuation;
  current={ionic_strength_mM:ionic,Debye_length_nm:lam,zeta_mV:zeta,attenuation,kappa_a_for100nm:100/lam};
  keys.forEach(k=>document.getElementById('P02-'+k+'-value').textContent=v[k].toFixed(k==='surface'?0:2));
  result.textContent=L('离子强度','Ionic strength')+` ${ionic.toFixed(3)} mmol/L · `+L('Debye长度','Debye length')+` ${lam.toFixed(3)} nm · ζ = ${zeta.toFixed(3)} mV · κa = ${(100/lam).toFixed(2)}`;
  const X=x=>75+x/40*640,Y=y=>340-(y+22)/44*290;
  let svg='<rect x="0" y="0" width="760" height="400" fill="#fcfbf7"/>';
  for(const y of [-20,-10,0,10,20])svg+=`<path d="M75 ${Y(y)}H715" stroke="${y===0?'#85949b':'#dfe5e5'}" fill="none"/><text x="61" y="${Y(y)+5}" text-anchor="end" font-size="14">${y}</text>`;
  for(const x of [0,10,20,30,40])svg+=`<text x="${X(x)}" y="364" text-anchor="middle" font-size="14">${x}</text>`;
  svg+='<text x="75" y="26" font-size="15">'+L('电位 / mV','Potential / mV')+'</text><text x="405" y="390" text-anchor="middle" font-size="15">'+L('距表面距离 / nm','Distance from surface / nm')+'</text>';
  let d='';for(let j=0;j<=400;j++){const x=j/10;d+=(j?'L':'M')+X(x).toFixed(2)+' '+Y(v.surface*Math.exp(-x/lam)).toFixed(2)+' ';}
  svg+=`<path d="${d}" fill="none" stroke="#167d9a" stroke-width="3"/><path d="M${X(v.delta)} 50V340" stroke="#d35f47" stroke-dasharray="6 5"/><circle cx="${X(v.delta)}" cy="${Y(zeta)}" r="6" fill="#d35f47"/>`;
  svg+=`<text x="350" y="65" font-size="15" fill="#d35f47">`+L('滑移面距表面','Slipping plane:')+` ${v.delta.toFixed(2)} nm</text><text x="350" y="91" font-size="15">`+L('表面电位固定为','Surface potential:')+` ${v.surface.toFixed(0)} mV</text>`;
  plot.innerHTML=svg;
 }
 function set(p){for(const k of keys)if(Object.prototype.hasOwnProperty.call(p,k)){const n=Number(p[k]);if(Number.isFinite(n))controls[k].value=String(Math.min(Number(controls[k].max),Math.max(Number(controls[k].min),n)));}render();}
 function reset(){set({logI:0,delta:1,surface:-15});}
 keys.forEach(k=>controls[k].addEventListener('input',render));document.getElementById('P02-reset').addEventListener('click',reset);
 window.CourseLab={set,state:()=>({...current}),reset};reset();
})();

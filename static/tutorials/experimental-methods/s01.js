(()=>{
 const en=document.documentElement.lang==='en', t=(zh,english)=>en?english:zh;
 const by=id=>document.getElementById('S01-'+id);
 let values={wavenumber:1000,angle:45};
 function depth(wn,angle){return 10000/wn/(2*Math.PI*2.4*Math.sqrt(Math.sin(angle*Math.PI/180)**2-(1.5/2.4)**2));}
 function text(x,y,label,anchor='middle',fill='#243c47',size=14){return `<text x="${x}" y="${y}" text-anchor="${anchor}" fill="${fill}" font-size="${size}">${label}</text>`;}
 function path(points,color){return `<path d="${points.map((p,i)=>(i?'L':'M')+p[0].toFixed(2)+','+p[1].toFixed(2)).join(' ')}" fill="none" stroke="${color}" stroke-width="3"/>`;}
 function render(){
  for(const key of ['wavenumber','angle']){by(key).value=values[key];by(key+'-value').value=values[key];}
  const d=depth(values.wavenumber,values.angle);let svg='';
  for(const x0 of [70,540]){
   svg+=`<path d="M${x0},55V330H${x0+330}" stroke="#aebfc6" fill="none"/>`;
   for(let j=0;j<=4;j++){const yy=330-j*65;svg+=`<path d="M${x0},${yy}H${x0+330}" stroke="#e0e8eb"/>`;svg+=text(x0-12,yy+5,(x0===70?j/4:j).toString(),'end');}
  }
  for(let j=0;j<=4;j++)svg+=text(70+j*82.5,354,(j*2).toString());
  for(const wn of [1000,2000,3000])svg+=text(540+(wn-800)/2700*330,354,wn.toString());
  svg+=text(235,25,t('距界面越远，强度逐渐减弱','Intensity decays away from the interface'));
  svg+=text(705,25,t('波数与衰减深度','Wavenumber and decay depth'));
  svg+=text(70,47,t('归一化强度','Normalized intensity'),'start','#50636c',12);
  svg+=text(540,47,t('振幅衰减长度 / μm','Amplitude decay length / μm'),'start','#50636c',12);
  svg+=text(235,390,t('距晶体表面的距离 / μm','Distance from crystal / μm'));
  svg+=text(705,390,t('波数 / cm⁻¹','Wavenumber / cm⁻¹'));
  const profile=Array.from({length:161},(_,i)=>[70+i/160*330,330-260*Math.exp(-2*(i/160*8)/d)]);
  const curve=Array.from({length:161},(_,i)=>{const wn=800+i/160*2700;return [540+i/160*330,330-depth(wn,values.angle)*65];});
  svg+=path(profile,'#12687b')+path(curve,'#12687b');
  svg+=`<path d="M${70+d/8*330},330V${330-260*Math.exp(-2)}" stroke="#be6047" stroke-dasharray="5 4"/>`;
  svg+=`<circle cx="${70+d/8*330}" cy="${330-260*Math.exp(-2)}" r="5" fill="#be6047"/>`;
  svg+=`<circle cx="${540+(values.wavenumber-800)/2700*330}" cy="${330-d*65}" r="6" fill="#be6047"/>`;
  svg+=text(390,92,`dₚ = ${d.toFixed(3)} μm`,'end','#be6047');
  by('plot').innerHTML=svg;
  by('readout').textContent=t(`当前振幅衰减长度为 ${d.toFixed(3)} μm；在这一深度，强度为界面值的 ${(Math.exp(-2)*100).toFixed(2)}%。入射角均高于本模型的临界角38.68°。`,`The amplitude decay length is ${d.toFixed(3)} μm. At that depth, intensity is ${(Math.exp(-2)*100).toFixed(2)}% of its interface value. All selectable angles exceed the model critical angle of 38.68°.`);
 }
 function set(parameters){if(parameters.wavenumber!==undefined)values.wavenumber=Math.max(800,Math.min(3500,Number(parameters.wavenumber)));if(parameters.angle!==undefined)values.angle=Math.max(42,Math.min(75,Number(parameters.angle)));render();}
 function reset(){values={wavenumber:1000,angle:45};render();}
 for(const key of ['wavenumber','angle'])by(key).addEventListener('input',()=>set({[key]:Number(by(key).value)}));
 by('double').addEventListener('click',()=>set({wavenumber:2000}));by('reset').addEventListener('click',reset);
 window.CourseLab={set,reset,state:()=>({...values,depth:depth(values.wavenumber,values.angle),intensity_at_depth:Math.exp(-2)})};render();
})();

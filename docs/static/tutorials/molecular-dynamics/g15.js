document.querySelectorAll('[data-lab="G15-I1"]').forEach(root=>{
 if(root.dataset.ready)return;root.dataset.ready='1';
 const angle=root.querySelector('[data-angle]'), mode=root.querySelector('[data-mode]');
 const readout=root.querySelector('[data-readout]'), result=root.querySelector('[data-result]');
 const picture=root.querySelector('[data-picture]'), zh=root.dataset.language==='zh';
 function update(){
  const theta=Number(angle.value), opposing=mode.value==='opposing';
  const angles=opposing?[theta,theta,180-theta,180-theta]:[theta,theta,theta,theta];
  const p2=angles.reduce((sum,x)=>sum+(3*Math.cos(x*Math.PI/180)**2-1)/2,0)/4;
  const mean=angles.reduce((a,b)=>a+b,0)/4;
  const fromMean=(3*Math.cos(mean*Math.PI/180)**2-1)/2;
  readout.textContent=theta.toFixed(0)+'°';
  result.textContent=(zh?'逐根计算后平均 P₂ = ':'Mean of individual P₂ = ')+p2.toFixed(3)+
   (zh?'；平均角 θ̄ = ':'; mean angle θ̄ = ')+mean.toFixed(1)+'°'+
   (zh?'；先平均角度再计算 = ':'; evaluating the mean angle first = ')+fromMean.toFixed(3);
  let drawing='<rect width="800" height="300" fill="#f4f2e9"/>';
  drawing+='<path d="M40 160H760" stroke="#c5d4cf" stroke-width="2" stroke-dasharray="7 7"/>';
  angles.forEach((x,i)=>{const cx=115+190*i,dx=70*Math.sin(x*Math.PI/180),dy=-70*Math.cos(x*Math.PI/180);
   drawing+='<path d="M'+cx+' 245V65" stroke="#c5d4cf" stroke-width="2"/>';
   drawing+='<path d="M'+cx+' 160L'+(cx+dx)+' '+(160+dy)+'" stroke="#147d92" stroke-width="6"/>';
   drawing+='<circle cx="'+(cx+dx)+'" cy="'+(160+dy)+'" r="8" fill="#147d92"/>';
   drawing+='<text x="'+cx+'" y="280" text-anchor="middle" fill="#193844" font-size="22">'+x.toFixed(0)+'°</text>';
  });picture.innerHTML=drawing;
 }
 angle.addEventListener('input',update);mode.addEventListener('change',update);
 root.querySelector('[data-reset]').addEventListener('click',()=>{angle.value='30';mode.value='opposing';update();});
 update();
});
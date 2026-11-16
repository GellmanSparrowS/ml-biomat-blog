(() => {
 const root=document.getElementById('P01-lab'); if(!root)return;
 const zh=document.documentElement.lang.startsWith('zh'), tr=(a,b)=>zh?a:b;
 const $=s=>document.getElementById('P01-'+s), c={tare:.4,dry:1.6,wet:5.2,compare:true}; let state={};
 const text=(x,y,s,size=17,extra='')=>`<text x="${x}" y="${y}" font-size="${size}" fill="#172b36" ${extra}>${s}</text>`;
 const line=(x,y,X,Y,color='#ccd3d1',width=1,extra='')=>`<line x1="${x}" y1="${y}" x2="${X}" y2="${Y}" stroke="${color}" stroke-width="${width}" ${extra}/>`;
 const niceMax=(value,intervals)=>{const raw=value/intervals,base=10**Math.floor(Math.log10(raw));return [1,2,2.5,5,10].find(v=>v*base>=raw-1e-12)*base*intervals;};
 const tick=value=>String(Number(value.toPrecision(6)));
 function render(){
  const d=c.dry-c.tare,w=c.wet-c.tare,a=w-d,valid=c.tare>=0&&d>0&&a>=-1e-10;
  state={...c,valid,dry_g:d,wet_g:w,water_g:a,uptake:valid?a/d:null,fraction:valid?a/w:null};
  $('error').textContent=valid?'':tr('检查读数：容器质量应非负，干态总读数应大于容器，湿态总读数应不小于干态。','Check readings: container mass must be nonnegative, dry total must exceed container mass, and wet total must be at least dry total.');
  if(!valid){$('mass').innerHTML=text(25,50,tr('先调整称量关系，再查看质量图。','Correct the weighing relationships to view the mass account.'));$('curves').innerHTML='';$('result').textContent='';return;}
  const max=niceMax(Math.max(6,c.wet*1.16),4),sx=v=>150+v/max*670;
  let m=text(24,30,tr('称量组成 / g','Weighing contributions / g'),21);
  for(let i=0;i<3;i++){const y=76+i*70,labels=[tr('空容器','Container'),tr('干态总读数','Dry total'),tr('湿态总读数','Wet total')];m+=text(135,y+24,labels[i],17,'text-anchor="end"'); const seg=[c.tare,i>0?d:0,i>1?a:0],colors=['#bfc6c5','#b85336','#28648a'];let start=0;seg.forEach((v,j)=>{m+=`<rect x="${sx(start)}" y="${y}" width="${v/max*670}" height="36" fill="${colors[j]}"/>`;start+=v;});m+=text(sx(start)+9,y+24,start.toFixed(2),17);}
  for(let k=0;k<=4;k++){const v=max*k/4;m+=line(sx(v),271,sx(v),277,'#172b36')+text(sx(v),300,tick(v),15,'text-anchor="middle"');}
  m+=line(150,271,820,271,'#172b36')+text(150,334,tr('灰：容器　橙：干材料　蓝：留存水','Gray: container   Orange: dry material   Blue: retained water'),17);
  $('mass').innerHTML=m;
  const xmax=niceMax(Math.max(6,a*1.2),3),qmax=niceMax(Math.max(5,xmax/d,c.compare?xmax/1.2:0),4), X=(v,p)=>p+v/xmax*320,Yq=v=>255-v/qmax*185,Yw=v=>255-v*185;
  let g=text(25,28,tr('干质量作分母 / g·g⁻¹','Dry-mass denominator / g·g⁻¹'),18)+text(485,28,tr('湿质量作分母 / %','Wet-mass denominator / %'),18);
  [65,525].forEach((p,j)=>{for(let k=0;k<=4;k++){let val=(j?1:qmax)*k/4,y=j?Yw(val):Yq(val);g+=line(p,y,p+320,y,'#e0e4df')+text(p-12,y+5,j?(val*100).toFixed(0):tick(val),15,'text-anchor="end"');}g+=line(p,70,p,255,'#172b36')+line(p,255,p+320,255,'#172b36');for(let k=0;k<=3;k++){let v=xmax*k/3;g+=text(X(v,p),281,tick(v),15,'text-anchor="middle"');}g+=text(p+160,310,tr('留存水质量 / g','Retained water mass / g'),17,'text-anchor="middle"');});
  const path=(den,p,Y)=>Array.from({length:101},(_,i)=>{const v=xmax*i/100;return `${i?'L':'M'}${X(v,p)},${Y(den(v))}`}).join(' ');
  if(c.compare){g+=`<path d="${path(v=>v/1.2,65,Yq)}" stroke="#8b9699" fill="none" stroke-width="2" stroke-dasharray="6 4"/><path d="${path(v=>v/(1.2+v),525,Yw)}" stroke="#8b9699" fill="none" stroke-width="2" stroke-dasharray="6 4"/>`;}
  g+=`<path d="${path(v=>v/d,65,Yq)}" stroke="#b85336" fill="none" stroke-width="3"/><path d="${path(v=>v/(d+v),525,Yw)}" stroke="#28648a" fill="none" stroke-width="3"/>`;
  [[65,Yq(state.uptake)],[525,Yw(state.fraction)]].forEach(([p,y])=>g+=line(X(a,p),y,X(a,p),255,'#a08432',1.5,'stroke-dasharray="4 3"')+`<circle cx="${X(a,p)}" cy="${y}" r="7" fill="#172b36" stroke="#fbfaf6" stroke-width="2"/>`);
  g+=text(25,347,tr('实线：当前干质量；灰虚线：原始1.20 g干质量','Solid: current dry mass; dashed: original 1.20 g dry mass'),16);
  $('curves').innerHTML=g;
  $('result').textContent=`${tr('净干质量','Net dry mass')}: ${c.dry.toFixed(2)} − ${c.tare.toFixed(2)} = ${d.toFixed(3)} g\n${tr('留存水','Retained water')}: ${w.toFixed(3)} − ${d.toFixed(3)} = ${a.toFixed(3)} g\n${tr('按干质量','Dry basis')}: ${a.toFixed(3)} / ${d.toFixed(3)} = ${state.uptake.toFixed(3)} g/g\n${tr('湿样水分数','Wet-specimen water fraction')}: ${a.toFixed(3)} / ${w.toFixed(3)} = ${(state.fraction*100).toFixed(2)}%`;
 }
 function set(v){Object.assign(c,v);['tare','dry','wet'].forEach(k=>{c[k]=Math.max(0,Number(c[k])||0);$(k).value=c[k];});$('compare').checked=c.compare;render();}
 ['tare','dry','wet'].forEach(k=>$(k).addEventListener('input',()=>set({[k]:Number($(k).value)})));
 $('compare').addEventListener('input',()=>set({compare:$('compare').checked}));
 const reset=()=>set({tare:.4,dry:1.6,wet:5.2,compare:true});$('reset').addEventListener('click',reset);
 window.CourseLab={set,reset,state:()=>JSON.parse(JSON.stringify(state))};render();
})();

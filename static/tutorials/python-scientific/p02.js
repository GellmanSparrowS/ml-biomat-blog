(() => {
 const root=document.getElementById('P02-lab');if(!root)return;
 const zh=document.documentElement.lang.startsWith('zh'),tr=(a,b)=>zh?a:b,$=id=>document.getElementById('P02-'+id);
 const p={force:5,width:2,thickness:.1,unit:'mm',rel:.01,abs:.01};let result={};
 const tx=(x,y,s,z=17,extra='')=>`<text x="${x}" y="${y}" font-size="${z}" fill="#172b36" ${extra}>${s}</text>`;
 const ln=(x,y,X,Y,c='#c4ccca',w=1,extra='')=>`<line x1="${x}" y1="${y}" x2="${X}" y2="${Y}" stroke="${c}" stroke-width="${w}" ${extra}/>`;
 const niceMax=value=>{const raw=value/4,base=10**Math.floor(Math.log10(raw));return [1,2,2.5,5,10].find(v=>v*base>=raw-1e-12)*base*4;};
 function render(){
  const A=p.width*p.thickness,s=p.force/A,ref=p.force/(p.width*.1),diff=Math.abs(s-ref),threshold=Math.max(p.rel*Math.max(Math.abs(s),Math.abs(ref)),p.abs),close=diff<=threshold;
  result={...p,area_mm2:A,area_m2:A*1e-6,stress_MPa:s,reference_MPa:ref,relative_change:ref?s/ref-1:null,difference_MPa:diff,threshold_MPa:threshold,close};
  const format=v=>p.unit==='m'?(v/1000).toPrecision(4)+' m':v.toPrecision(4)+' mm';
  const width=200+p.width/10*150,height=45+p.thickness/.4*110,x=80,y=100;
  let g=tx(22,28,tr('初始矩形截面','Initial rectangular section'),21);
  g+=`<rect x="${x}" y="${y}" width="${width}" height="${height}" fill="#28648a" fill-opacity=".14" stroke="#28648a" stroke-width="2"/>`;
  g+=ln(x,y-20,x+width,y-20,'#172b36',1.5)+ln(x,y-26,x,y-14,'#172b36')+ln(x+width,y-26,x+width,y-14,'#172b36')+tx(x+width/2,y-35,format(p.width),18,'text-anchor="middle"');
  g+=ln(x+width+20,y,x+width+20,y+height,'#172b36',1.5)+ln(x+width+14,y,x+width+26,y,'#172b36')+ln(x+width+14,y+height,x+width+26,y+height,'#172b36')+tx(x+width+32,y+height/2+6,format(p.thickness),16);
  g+=tx(x+width/2,y+height/2+6,`A = ${A.toFixed(4)} mm²`,18,'text-anchor="middle"');
  g+=tx(22,300,tr('方向分别缩放；实际尺寸以标注为准。','Directions use separate drawing scales; labels give actual sizes.'),15);
  $('geometry').innerHTML=g;
  const tmax=(p.thickness<=.2?.25:.5),tmin=.025,ymax=niceMax(Math.max(p.force/(p.width*tmin),1)*1.05),X=t=>65+(t-tmin)/(tmax-tmin)*430,Y=v=>260-v/ymax*200;
  let q=tx(20,28,tr('同一力与宽度下的厚度变化','Thickness at the same force and width'),20);
  for(let i=0;i<=4;i++){const v=ymax*i/4;q+=ln(65,Y(v),495,Y(v),'#e0e4df')+tx(55,Y(v)+5,String(Number(v.toPrecision(6))),15,'text-anchor="end"');}
  q+=ln(65,60,65,260,'#172b36')+ln(65,260,495,260,'#172b36');
  for(const t of (tmax===.25?[.025,.05,.1,.15,.2,.25]:[.025,.1,.2,.3,.4,.5])){q+=tx(X(t),284,p.unit==='m'?(t*.001).toExponential(1):String(t),14,'text-anchor="middle"');}
  let path='';for(let i=0;i<=160;i++){const t=tmin+(tmax-tmin)*i/160;path+=(i?' L':'M')+X(t)+','+Y(p.force/(p.width*t));}
  q+=`<path d="${path}" fill="none" stroke="#28648a" stroke-width="3"/>`;
  q+=ln(X(.1),Y(ref),X(.1),260,'#8a9698',1.4,'stroke-dasharray="4 4"')+`<circle cx="${X(.1)}" cy="${Y(ref)}" r="6" fill="#fbfaf6" stroke="#172b36" stroke-width="2"/>`;
  q+=ln(X(p.thickness),Y(s),X(p.thickness),260,'#b85336',1.5,'stroke-dasharray="4 3"')+`<circle cx="${X(p.thickness)}" cy="${Y(s)}" r="7" fill="#b85336"/>`;
  q+=tx(310,310,tr('厚度 / ','Thickness / ')+p.unit,17,'text-anchor="middle"')+tx(20,52,tr('名义应力 / MPa','Nominal stress / MPa'),15)+tx(20,343,tr('空心：0.10 mm基准；实心：当前厚度','Open: 0.10 mm reference; filled: current thickness'),15);
  $('curve').innerHTML=q;
  const ratio=ref?((s/ref-1)*100).toFixed(2)+'%':tr('零载荷：相对变化不定义','Zero load: relative change undefined');
  $('result').textContent=`${tr('面积','Area')}: ${A.toFixed(6)} mm² = ${(A*1e-6).toExponential(6)} m²\n${tr('毫米路线','Millimetre route')}: ${p.force.toFixed(3)} / ${A.toFixed(6)} = ${s.toFixed(6)} MPa\n${tr('米路线','Metre route')}: ${p.force.toFixed(3)} / ${(A*1e-6).toExponential(6)} / 10⁶ = ${s.toFixed(6)} MPa\n${tr('相对基准变化','Change from reference')}: ${ratio}\n${tr('结果差值','Result difference')}: ${diff.toFixed(6)} MPa\n${tr('比较阈值','Comparison threshold')}: ${threshold.toFixed(6)} MPa\nmath.isclose → ${close?'True':'False'}`;
 }
 function set(v){Object.assign(p,v);p.force=Math.max(0,Math.min(30,Number(p.force)||0));p.width=Math.max(.5,Math.min(10,Number(p.width)||.5));p.thickness=Math.max(.025,Math.min(.4,Number(p.thickness)||.025));p.rel=Math.max(0,Math.min(.5,Number(p.rel)||0));p.abs=Math.max(0,Math.min(50,Number(p.abs)||0));p.unit=p.unit==='m'?'m':'mm';Object.keys(p).forEach(k=>$(k).value=p[k]);render();}
 Object.keys(p).forEach(k=>$(k).addEventListener('input',()=>set({[k]:k==='unit'?$(k).value:Number($(k).value)})));
 const reset=()=>set({force:5,width:2,thickness:.1,unit:'mm',rel:.01,abs:.01});$('reset').addEventListener('click',reset);
 window.CourseLab={set,reset,state:()=>JSON.parse(JSON.stringify(result))};render();
})();

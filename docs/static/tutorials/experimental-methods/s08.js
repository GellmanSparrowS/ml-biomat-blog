(()=>{
 'use strict';
 const en=document.documentElement.lang==='en',t=(zh,english)=>en?english:zh;
 const by=id=>document.getElementById('S08-'+id);
 const defaults={separation:.018,width:.014,interference:.6,matrix:.8};
 const bounds={separation:[0,.04],width:[.006,.03],interference:[0,1.5],matrix:[.4,1.2]};
 const colors={target:'#18877d',fit:'#236d96',interference:'#d57b39',background:'#8863a4',ink:'#293c49'};
 let parameters={...defaults},current;
 const dot=(a,b)=>a.reduce((s,v,i)=>s+v*b[i],0),mean=a=>a.reduce((s,v)=>s+v,0)/a.length;
 function fixedNoise(n,seed=804){const a=[];while(a.length<n){seed=(Math.imul(1664525,seed)+1013904223)>>>0;const u=(seed+.5)/4294967296;seed=(Math.imul(1664525,seed)+1013904223)>>>0;const v=(seed+.5)/4294967296,r=Math.sqrt(-2*Math.log(u));a.push(r*Math.cos(2*Math.PI*v),r*Math.sin(2*Math.PI*v));}return a.slice(0,n);}
 const noise=fixedNoise(241),x=Array.from({length:241},(_,i)=>-.06+.12*i/240),xc=x.map(v=>v-mean(x)),xx=dot(xc,xc);
 function removeBackground(a){const m=mean(a),b=dot(xc,a)/xx;return a.map((v,i)=>v-m-b*xc[i]);}
 function calculate(){
  const p=parameters,sigma=p.width/Math.sqrt(8*Math.log(2));
  const g=x.map(v=>Math.exp(-.5*(v/sigma)**2)),h=x.map(v=>Math.exp(-.5*((v-p.separation)/sigma)**2));
  const baseline=x.map(v=>250+800*v),y=x.map((_,i)=>baseline[i]+p.matrix*12000*.8*(g[i]+p.interference*h[i])+20*noise[i]);
  const gp=removeBackground(g),hp=removeBackground(h),yp=removeBackground(y),gg=dot(gp,gp),hh=dot(hp,hp),gh=dot(gp,hp),yg=dot(yp,gp),yh=dot(yp,hp);
  const rho=Math.max(-1,Math.min(1,gh/Math.sqrt(gg*hh))),identifiable=Math.abs(rho)<1-1e-12;
  const condition=identifiable?Math.sqrt((1+Math.abs(rho))/(1-Math.abs(rho))):null;
  let a,b,external=null,corrected=null,se=null;
  if(identifiable){const determinant=gg*hh-gh*gh;a=(yg*hh-yh*gh)/determinant;b=(yh*gg-yg*gh)/determinant;external=a/12000;corrected=external/p.matrix;se=20/Math.sqrt(gg*(1-rho*rho))/(12000*p.matrix);}
  else{a=yg/gg;b=0;}
  const rest=y.map((v,i)=>v-a*g[i]-b*h[i]),bgSlope=dot(xc,rest)/xx,bgMean=mean(rest);
  const bg=x.map((_,i)=>bgMean+bgSlope*xc[i]),fit=x.map((_,i)=>a*g[i]+b*h[i]+bg[i]),residual=y.map((v,i)=>v-fit[i]);
  return {x,y,g,h,bg,fit,residual,a,b,identifiable,condition,
   external_mg_L:external,corrected_mg_L:corrected,standard_error_mg_L:se,
   center_naive_mg_L:(y[120]-baseline[120])/12000,residual_rms:Math.sqrt(dot(residual,residual)/residual.length)};
 }
 function text(px,py,label,size=14,anchor='middle',fill=colors.ink){return `<text x="${px}" y="${py}" font-size="${size}" text-anchor="${anchor}" fill="${fill}">${label}</text>`;}
 function line(points,color,width=2,dash=''){return `<path d="${points.map((p,i)=>(i?'L':'M')+p[0].toFixed(3)+','+p[1].toFixed(3)).join(' ')}" fill="none" stroke="${color}" stroke-width="${width}" ${dash?`stroke-dasharray="${dash}"`:''}/>`;}
 function render(){
  current=calculate();const s=current,p=parameters;
  for(const key of Object.keys(defaults)){by(key).value=p[key];by(key+'-value').value=p[key].toFixed(key==='separation'||key==='width'?3:key==='matrix'?2:1);}
  const maxY=Math.ceil(Math.max(...s.y)/4000)*4000,minY=Math.min(-300,Math.min(...s.bg)-100);
  const X=v=>80+(v+.06)/.12*880,Y=v=>345-(v-minY)/(maxY-minY)*260;
  let svg=`<rect width="1040" height="690" fill="#fffdf9"/>`;
  svg+=text(80,27,t('光谱：观测、分峰与背景','Spectrum: observations, components and background'),19,'start');
  const legends=[[80,'#7f8c95',t('构造观测','Constructed data')],[280,colors.fit,t('总拟合','Total fit')],[440,colors.target,t('钙峰','Calcium peak')],[605,colors.interference,t('模拟邻峰','Modelled neighbour')],[815,colors.background,t('背景','Background')]];
  for(const [px,col,label] of legends){svg+=`<path d="M${px},50h20" stroke="${col}" stroke-width="3"/>`+text(px+27,55,label,13,'start');}
  svg+=text(80,78,t('信号 / a.u.','Signal / a.u.'),13,'start');
  for(let j=0;j<=4;j++){const v=j*maxY/4,yy=Y(v);svg+=`<path d="M80,${yy}H960" stroke="#e1e8eb"/>`+text(70,yy+4,v.toFixed(0),12,'end');}
  for(let j=0;j<=6;j++){const v=-.06+j*.02,px=X(v);svg+=`<path d="M${px},345v5" stroke="#8799a1"/>`+text(px,367,(317.9332+v).toFixed(3),12);}
  svg+=`<path d="M80,85V345H960" fill="none" stroke="#8799a1"/>`;
  svg+=line(s.y.map((v,i)=>[X(x[i]),Y(v)]),'#9ba8af',1);
  svg+=line(s.fit.map((v,i)=>[X(x[i]),Y(v)]),colors.fit,2.2);
  if(s.identifiable){svg+=line(s.g.map((v,i)=>[X(x[i]),Y(s.a*v)]),colors.target,2,'6 4');svg+=line(s.h.map((v,i)=>[X(x[i]),Y(s.b*v)]),colors.interference,2,'6 4');}
  svg+=line(s.bg.map((v,i)=>[X(x[i]),Y(v)]),colors.background,1.5,'3 3');
  for(let i=0;i<x.length;i+=8)svg+=`<circle cx="${X(x[i])}" cy="${Y(s.y[i])}" r="2" fill="#7f8c95"><title>${(317.9332+x[i]).toFixed(4)} nm; ${s.y[i].toFixed(1)} a.u.</title></circle>`;
  svg+=text(520,393,t('空气波长 / nm；分峰曲线不含背景','Air wavelength / nm; component curves exclude background'),13);
  if(!s.identifiable)svg+=text(950,115,t('两条谱线完全重合：只确定总贡献','Coincident lines: only the combined contribution is identified'),14,'end',colors.interference);
  const rmax=Math.max(60,Math.ceil(Math.max(...s.residual.map(Math.abs))/20)*20),RX=v=>80+(v+.06)/.12*380,RY=v=>535-v/rmax*66;
  svg+=text(80,435,t('残差：小残差能保证分峰正确吗？','Residuals: does a small residual settle the split?'),15,'start');
  svg+=`<rect x="80" y="${RY(40)}" width="380" height="${RY(-40)-RY(40)}" fill="#edf3f7"/>`;
  for(const v of [-rmax,0,rmax])svg+=`<path d="M80,${RY(v)}H460" stroke="#d9e3e7"/>`+text(71,RY(v)+4,v.toFixed(0),12,'end');
  svg+=line(s.residual.map((v,i)=>[RX(x[i]),RY(v)]),colors.fit,1.3);
  svg+=`<path d="M80,469V601H460" fill="none" stroke="#8799a1"/>`;
  for(const v of [-.06,0,.06])svg+=text(RX(v),624,v.toFixed(2),12);
  svg+=text(270,650,t('距目标线中心 / nm；残差单位 a.u.','Offset from target / nm; residual units: a.u.'),13);
  svg+=text(80,674,t('浅色区：±2 × 已知噪声标准差','Shaded region: ±2 × known noise standard deviation'),12,'start','#647780');
  const values=[s.center_naive_mg_L,s.external_mg_L,s.corrected_mg_L],errors=[40/12000,s.standard_error_mg_L===null?null:2*s.standard_error_mg_L*p.matrix,s.standard_error_mg_L===null?null:2*s.standard_error_mg_L];
  let low=0,high=1.2;for(let i=0;i<3;i++)if(values[i]!==null){low=Math.min(low,values[i]-errors[i]-.05);high=Math.max(high,values[i]+errors[i]+.05);}
  const CX=v=>640+(v-low)/(high-low)*330;
  svg+=text(640,435,t('浓度：共同响应校正前后','Concentration estimates'),15,'start');
  svg+=`<path d="M${CX(.8)},455V597" stroke="${colors.target}" stroke-dasharray="5 4"/>`+text(CX(.8),454,'0.800',12,'middle',colors.target);
  const labels=[t('峰中心','Peak centre'),t('分峰 + 外标','Fit + external'),t('分峰 + 内标','Fit + internal')],cols=[colors.interference,colors.fit,colors.target];
  for(let i=0;i<3;i++){const yy=485+i*48;svg+=text(628,yy+5,labels[i],13,'end');if(values[i]===null){svg+=text(805,yy+5,t('无法分别估计','Not separately identifiable'),13,'middle',colors.interference);continue;}
   const lo=CX(values[i]-errors[i]),hi=CX(values[i]+errors[i]);svg+=`<path d="M${lo},${yy}H${hi}M${lo},${yy-5}v10M${hi},${yy-5}v10" stroke="${cols[i]}" stroke-width="2"/><circle cx="${CX(values[i])}" cy="${yy}" r="5" fill="${cols[i]}"><title>${values[i].toFixed(6)} ± ${errors[i].toFixed(6)} mg/L</title></circle>`;
  }
  svg+=`<path d="M640,601H970" stroke="#8799a1"/>`;
  for(let j=0;j<=4;j++)svg+=text(640+j/4*330,624,(low+(high-low)*j/4).toFixed(2),12);
  svg+=text(805,650,t('浓度 / mg L⁻¹','Concentration / mg L⁻¹'),13);
  svg+=text(640,674,t('误差线：±2 × 模型标准误差','Error bars: ±2 × model standard error'),12,'start','#647780');
  by('plot').innerHTML=svg;
  const fmt=v=>v===null?t('无法分别估计','Not separately identifiable'):v.toFixed(5);
  by('naive').textContent=fmt(s.center_naive_mg_L);by('external').textContent=fmt(s.external_mg_L);by('corrected').textContent=fmt(s.corrected_mg_L);
  by('status').textContent=s.identifiable?t(`峰间距为峰宽的 ${(p.separation/p.width).toFixed(2)} 倍；投影后条件数 κ = ${s.condition.toFixed(2)}；残差均方根为 ${s.residual_rms.toFixed(2)} a.u.。`,`Separation is ${(p.separation/p.width).toFixed(2)} times the FWHM; projected condition number κ = ${s.condition.toFixed(2)}; residual RMS = ${s.residual_rms.toFixed(2)} a.u.`):t(`完全重合时条件数趋于无穷，钙与邻峰贡献无法分别确定。总曲线的残差均方根仍为 ${s.residual_rms.toFixed(2)} a.u.，小残差并没有消除这个歧义。`,`At exact coincidence the condition number diverges and calcium cannot be separated from its neighbour. The total-curve residual RMS is still ${s.residual_rms.toFixed(2)} a.u.; a small residual has not removed the ambiguity.`);
 }
 function set(next){for(const key of Object.keys(defaults))if(Object.prototype.hasOwnProperty.call(next,key)){const v=Number(next[key]);if(Number.isFinite(v))parameters[key]=Math.max(bounds[key][0],Math.min(bounds[key][1],v));}render();}
 function reset(){parameters={...defaults};render();}
 for(const key of Object.keys(defaults))by(key).addEventListener('input',()=>set({[key]:by(key).value}));
 by('reset').addEventListener('click',reset);by('separated').addEventListener('click',()=>set({separation:.03,width:.01,interference:.6,matrix:1}));by('coincident').addEventListener('click',()=>set({separation:0}));by('suppressed').addEventListener('click',()=>set({...defaults,matrix:.65}));
 window.CourseLab={set,reset,state:()=>({...parameters,identifiable:current.identifiable,condition:current.condition,external_mg_L:current.external_mg_L,corrected_mg_L:current.corrected_mg_L,standard_error_mg_L:current.standard_error_mg_L,center_naive_mg_L:current.center_naive_mg_L,residual_rms:current.residual_rms})};
 render();
})();

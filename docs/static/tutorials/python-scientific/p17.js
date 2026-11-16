(() => {
 const root=document.getElementById('P17-lab');if(!root)return;
 const zh=document.documentElement.lang.startsWith('zh'),tr=(a,b)=>zh?a:b,el=x=>root.querySelector('#P17-'+x);
 const data={A:[8,8,9,9,10,10,10,10,11,11,12,12],B:[6,6,7,8,9,10,10,11,12,13,14,14]};
 const defaults={group:'A',width:1,interval:'sd',threshold:10};let p={...defaults},result={};
 const text=(x,y,s,anchor='start',size=14)=>`<text x="${x}" y="${y}" text-anchor="${anchor}" font-size="${size}" fill="#20313e">${s}</text>`;
 function draw(){
  const v=data[p.group],mean=v.reduce((a,b)=>a+b,0)/v.length,sd=Math.sqrt(v.reduce((s,x)=>s+(x-mean)**2,0)/(v.length-1)),sem=sd/Math.sqrt(v.length),half=p.interval==='sd'?sd:p.interval==='sem'?sem:2.200985160091639*sem;
  const below=v.filter(x=>x<=p.threshold).length,color=p.group==='A'?'#28658c':'#b64a35',wide=root.getBoundingClientRect().width>720,width=wide?860:430,L=63,W=width-L-25,X=x=>L+(x-5)/10*W;
  const raw=el('points');raw.setAttribute('viewBox',`0 0 ${width} 310`);
  let s=text(L,23,tr('12 个样品与均值区间','12 specimens and mean interval'),'start',17)+text(L,48,tr('每个圆点 = 一个独立样品','Each circle = one independent specimen'));
  s+=`<rect x="${L}" y="57" width="${X(p.threshold)-L}" height="153" fill="#edf2f5"/>`;
  const repeats={};v.forEach(x=>{const k=repeats[x]||0;repeats[x]=k+1;s+=`<circle cx="${X(x)}" cy="${73+k*17}" r="6" stroke="${color}" stroke-width="2" fill="${x<=p.threshold?color:'#fff'}"/>`});
  s+=text(L,156,p.interval==='ci'?'95% t CI':`mean ± ${p.interval.toUpperCase()}`)+`<line x1="${X(mean-half)}" x2="${X(mean+half)}" y1="183" y2="183" stroke="${color}" stroke-width="3"/><path d="M${X(mean-half)},175v16M${X(mean+half)},175v16" stroke="${color}" stroke-width="2"/><circle cx="${X(mean)}" cy="183" r="6" fill="${color}"/><line x1="${X(p.threshold)}" x2="${X(p.threshold)}" y1="57" y2="225" stroke="#71808b" stroke-dasharray="4 4"/>`;
  [6,8,10,12,14].forEach(x=>{s+=text(X(x),248,x,'middle')});s+=text(L+W/2,283,tr('样品平均模量 / kPa','Specimen-mean modulus / kPa'),'middle');raw.innerHTML=s;
  function chart(svg,title,ymax,ytitle){const l=63,w=339,t=56,h=225,x=x=>l+(x-5)/13*w,y=y=>t+h-y/ymax*h;svg.setAttribute('viewBox','0 0 430 350');let s=text(l,23,title,'start',17)+text(l,46,ytitle);for(const yy of (ymax===1?[0,.25,.5,.75,1]:[0,3,6,9,12]))s+=`<line x1="${l}" x2="${l+w}" y1="${y(yy)}" y2="${y(yy)}" stroke="#dce3e8"/>`+text(l-7,y(yy)+5,yy,'end');for(const xx of [6,9,12,15,18])s+=text(x(xx),303,xx,'middle');s+=text(l+w/2,335,tr('模量 / kPa','Modulus / kPa'),'middle');return{svg,s,x,y}}
  let c=chart(el('hist'),tr('分箱计数','Binned counts'),12,tr('样品数','Specimen count'));const bins=[];
  for(let left=5.5;left<17.5;left+=p.width){const n=v.filter(x=>x>=left&&x<left+p.width).length;bins.push({left,right:left+p.width,count:n});c.s+=`<rect x="${c.x(left)}" y="${c.y(n)}" width="${c.x(left+p.width)-c.x(left)-1}" height="${c.y(0)-c.y(n)}" fill="${color}" opacity=".8"/>`;if(n)c.s+=text((c.x(left)+c.x(left+p.width))/2,c.y(n)-7,n,'middle')};c.svg.innerHTML=c.s;
  c=chart(el('cdf'),tr('经验累积分布','Empirical cumulative distribution'),1,tr('不超过横轴值的比例','Fraction at or below x'));
  let path=`M${c.x(5.5)},${c.y(0)}`,count=0;for(const value of [...new Set(v)]){path+=`H${c.x(value)}`;count+=v.filter(x=>x===value).length;path+=`V${c.y(count/v.length)}`};path+=`H${c.x(17.5)}`;c.s+=`<path d="${path}" fill="none" stroke="${color}" stroke-width="2.5"/><circle cx="${c.x(p.threshold)}" cy="${c.y(below/v.length)}" r="6" fill="#20313e"/><line x1="${c.x(p.threshold)}" x2="${c.x(p.threshold)}" y1="${c.y(0)}" y2="${c.y(below/v.length)}" stroke="#71808b" stroke-dasharray="4 4"/>`;c.svg.innerHTML=c.s;
  result={...p,n:v.length,mean,sd,sem,half_width:half,count_below:below,fraction:below/v.length,bins};el('threshold-value').textContent=p.threshold;
  el('readout').textContent=tr(`组${p.group}：n=12，均值 ${mean.toFixed(3)} kPa，SD ${sd.toFixed(4)} kPa，SEM ${sem.toFixed(5)} kPa。所选区间 [${(mean-half).toFixed(4)}, ${(mean+half).toFixed(4)}] kPa；≤${p.threshold} kPa 有${below}/12（${(below/12*100).toFixed(1)}%）。`,`Group ${p.group}: n=12, mean ${mean.toFixed(3)} kPa, SD ${sd.toFixed(4)} kPa, SEM ${sem.toFixed(5)} kPa. Selected interval [${(mean-half).toFixed(4)}, ${(mean+half).toFixed(4)}] kPa; ${below}/12 (${(below/12*100).toFixed(1)}%) at or below ${p.threshold} kPa.`);
 }
 function set(q){p={...p,...q};p.group=p.group==='B'?'B':'A';p.width=[1,2,4].includes(+p.width)?+p.width:1;p.interval=['sd','sem','ci'].includes(p.interval)?p.interval:'sd';p.threshold=Math.max(5,Math.min(15,+p.threshold));for(const k of ['group','width','interval','threshold'])el(k).value=p[k];draw();return result}
 for(const k of ['group','width','interval','threshold'])el(k).addEventListener('input',()=>set({[k]:el(k).value}));el('reset').addEventListener('click',()=>set(defaults));
 let observer=null,lastWidth=0;if(typeof ResizeObserver!=='undefined'){observer=new ResizeObserver(()=>{const w=root.getBoundingClientRect().width;if(Math.abs(w-lastWidth)>1){lastWidth=w;draw()}});observer.observe(root)}
 window.CourseLab={set,state:()=>structuredClone(result),reset:()=>set(defaults),destroy:()=>observer?.disconnect()};set(defaults);
})();

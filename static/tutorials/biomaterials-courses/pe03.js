document.querySelectorAll('[data-lab="PE03-I1"]').forEach(root=>{
 const zh=root.closest('[data-lang]').dataset.lang==='zh',f=k=>root.querySelector('[data-field="'+k+'"]');
 function draw(){const n=Number(f('tanks').value),tau=Number(f('mean').value);let logfac=0;for(let j=1;j<n;j++)logfac+=Math.log(j);
 function density(theta){if(theta===0)return n===1?1:0;return Math.exp(n*Math.log(n)+(n-1)*Math.log(theta)-n*theta-logfac);}
 function cdf(theta){let x=n*theta,sum=1,term=1;for(let j=1;j<n;j++){term*=x/j;sum+=term;}return Math.max(0,Math.min(1,1-Math.exp(-x)*sum));}
 f('n-value').textContent=String(n);f('mean-value').textContent=tau.toFixed(0)+' min';
 let s='<rect width="600" height="470" fill="#faf9f5"/><text x="65" y="35" font-size="22" fill="#19383f">'+(zh?'停留时间密度 / min⁻¹':'Residence-time density / min⁻¹')+'</text>';
 for(let j=0;j<=4;j++){const y=350-260*j/4,v=1.6*j/4/tau;s+='<line x1="65" y1="'+y+'" x2="550" y2="'+y+'" stroke="#d7dfdb"/><text x="53" y="'+(y+7)+'" text-anchor="end" font-size="19" fill="#63757b">'+v.toFixed(2)+'</text>';}
 for(let j=0;j<=4;j++)s+='<text x="'+(65+485*j/4)+'" y="382" text-anchor="middle" font-size="20" fill="#63757b">'+tau*j+'</text>';
 s+='<line x1="65" y1="90" x2="65" y2="350" stroke="#63757b"/>';
 let pts=[];for(let i=0;i<=240;i++)pts.push((65+485*i/240).toFixed(2)+','+(350-260*density(4*i/240)/1.6).toFixed(2));
 s+='<polyline points="'+pts.join(' ')+'" stroke="#087d80" stroke-width="3" fill="none"/><line x1="186.25" y1="90" x2="186.25" y2="350" stroke="#bd582a" stroke-dasharray="5 5"/><text x="310" y="425" text-anchor="middle" font-size="22" fill="#19383f">'+(zh?'停留时间 / min':'Residence time / min')+'</text><text x="300" y="462" text-anchor="middle" font-size="20" fill="#63757b">'+(zh?'橙色虚线：平均时间':'Orange dashed line: mean time')+'</text>';f('plot').innerHTML=s;
 const early=cdf(.5),late=1-cdf(2),sd=tau/Math.sqrt(n);
 f('result').textContent=zh?n+'只等容釜串联，总平均时间'+tau.toFixed(0)+' min，标准差'+sd.toFixed(2)+' min。在半个平均时间前离开'+(100*early).toFixed(2)+'%，超过两个平均时间才离开'+(100*late).toFixed(2)+'%。图中画到四个平均时间，此后仍有'+(100*(1-cdf(4))).toFixed(3)+'%的尾部。':n+' equal tanks in series have total mean '+tau.toFixed(0)+' min and standard deviation '+sd.toFixed(2)+' min. '+(100*early).toFixed(2)+'% leaves before half the mean; '+(100*late).toFixed(2)+'% leaves after twice the mean. The plot ends at four means, leaving '+(100*(1-cdf(4))).toFixed(3)+'% in the later tail.';
 root.dataset.mean=String(tau);root.dataset.variance=String(tau*tau/n);root.dataset.early=String(early);
 }
 root.querySelectorAll('input').forEach(e=>e.addEventListener('input',draw));root.querySelector('[data-reset]').addEventListener('click',()=>{f('tanks').value=2;f('mean').value=10;draw()});draw();
});


document.querySelectorAll('[data-lab="PE03-I2"]').forEach(root=>{
 const zh=root.closest('[data-lang]').dataset.lang==='zh',f=k=>root.querySelector('[data-field="'+k+'"]');
 function draw(){const n=Number(f('tanks').value),h=Number(f('growth').value),v0=.004,tau=10,mean=v0+h*tau,variance=h*h*tau*tau/n,sd=Math.sqrt(variance),radius=Math.cbrt(3*mean/(4*Math.PI));
 function cdf(v){if(h===0)return v>=v0?1:0;if(v<=v0)return 0;let x=n*(v-v0)/(h*tau),sum=1,term=1;for(let j=1;j<n;j++){term*=x/j;sum+=term;}return Math.max(0,Math.min(1,1-Math.exp(-x)*sum));}
 f('n-value').textContent=String(n);f('growth-value').textContent=h.toFixed(5)+' μm³/min';
 let s='<rect width="600" height="470" fill="#faf9f5"/><text x="65" y="35" font-size="22" fill="#19383f">'+(zh?'体积不超过横轴值的累计比例':'Fraction at or below the indicated volume')+'</text>';
 for(let j=0;j<=4;j++){const y=350-260*j/4;s+='<line x1="65" y1="'+y+'" x2="550" y2="'+y+'" stroke="#d7dfdb"/><text x="53" y="'+(y+7)+'" text-anchor="end" font-size="20" fill="#63757b">'+(j/4).toFixed(2)+'</text>';}
 for(let j=0;j<=5;j++)s+='<text x="'+(65+485*j/5)+'" y="382" text-anchor="middle" font-size="19" fill="#63757b">'+(.01*j).toFixed(2)+'</text>';
 s+='<line x1="65" y1="90" x2="65" y2="350" stroke="#63757b"/>';
 let pts=[];if(h===0){const x=65+485*v0/.05;pts=['65,350',x+',350',x+',90','550,90'];}else{for(let i=0;i<=250;i++)pts.push((65+485*i/250).toFixed(2)+','+(350-260*cdf(.05*i/250)).toFixed(2));}
 const x=65+485*mean/.05;s+='<polyline points="'+pts.join(' ')+'" fill="none" stroke="#087d80" stroke-width="3"/><line x1="'+x+'" y1="90" x2="'+x+'" y2="350" stroke="#bd582a" stroke-dasharray="5 5"/><text x="310" y="425" text-anchor="middle" font-size="22" fill="#19383f">'+(zh?'聚合物体积 / μm³':'Polymer volume / μm³')+'</text><text x="300" y="462" text-anchor="middle" font-size="20" fill="#63757b">'+(zh?'橙色虚线：按数量平均的体积':'Orange dashed line: number-average volume')+'</text>';f('plot').innerHTML=s;
 f('result').textContent=zh?'平均体积'+mean.toFixed(5)+' μm³，体积标准差'+sd.toFixed(5)+' μm³，体积方差'+variance.toFixed(8)+' μm⁶。具有平均体积的等效球半径为'+(radius*1000).toFixed(1)+' nm。'+(h===0?'增长速率为零，所有种子保持原体积，分布集中为一步跳变。':'增加串联级数不改变这里的平均体积，会缩小由停留差异产生的体积离散。'):'Mean volume is '+mean.toFixed(5)+' μm³, volume standard deviation '+sd.toFixed(5)+' μm³ and volume variance '+variance.toFixed(8)+' μm⁶. A sphere with the mean volume has radius '+(radius*1000).toFixed(1)+' nm. '+(h===0?'With zero growth, all seeds retain their initial volume and the cumulative curve is a single step.':'More stages preserve this mean volume while reducing variation caused by different residence times.');
 root.dataset.meanVolume=String(mean);root.dataset.variance=String(variance);root.dataset.radius=String(radius);
 }
 root.querySelectorAll('input').forEach(e=>e.addEventListener('input',draw));root.querySelector('[data-reset]').addEventListener('click',()=>{f('tanks').value=1;f('growth').value=.0004;draw()});draw();
});

document.querySelectorAll('[data-lab="PE02-I1"]').forEach(root=>{
 const zh=root.closest('[data-lang]').dataset.lang==='zh',f=k=>root.querySelector('[data-field="'+k+'"]');
 function draw(){const da=Number(f('da').value),n=Number(f('tanks').value),xp=1-Math.exp(-da),xc=da/(1+da),xn=1-(1+da/n)**(-n);
 f('da-value').textContent=da.toFixed(2);f('n-value').textContent=String(n);
 const values=[xc,xn,xp],names=zh?['一只全混釜',n+'只等容釜串联','理想平推流']:['One stirred tank',n+' equal tanks in series','Ideal plug flow'];
 let s='<rect width="600" height="420" fill="#faf9f5"/>';
 values.forEach((x,i)=>{const y=55+105*i,c=['#bd582a','#3c64a0','#087d80'][i];s+='<text x="30" y="'+y+'" font-size="23" fill="#19383f">'+names[i]+'</text><text x="570" y="'+y+'" text-anchor="end" font-size="24" fill="'+c+'">'+(100*x).toFixed(1)+'%</text><rect x="30" y="'+(y+17)+'" width="540" height="30" fill="#e1e8e3"/><rect x="30" y="'+(y+17)+'" width="'+(540*x)+'" height="30" fill="'+c+'"/>';});
 s+='<text x="300" y="390" text-anchor="middle" font-size="21" fill="#63757b">'+(zh?'比较时总有效体积、流量和温度相同':'Same total volume, flow and temperature')+'</text>';f('plot').innerHTML=s;
 f('result').textContent=zh?'反应强度kτ为'+da.toFixed(2)+'时，单釜、'+n+'釜串联、平推流的转化率分别为'+(xc*100).toFixed(1)+'%、'+(xn*100).toFixed(1)+'%和'+(xp*100).toFixed(1)+'%。增加级数分配了原有体积，各级都按自己的出口浓度反应。':'At kτ='+da.toFixed(2)+', conversion is '+(xc*100).toFixed(1)+'% in one tank, '+(xn*100).toFixed(1)+'% in '+n+' tanks and '+(xp*100).toFixed(1)+'% in plug flow. Adding stages redistributes the existing volume; each tank reacts at its own outlet concentration.';
 root.dataset.single=String(xc);root.dataset.cascade=String(xn);root.dataset.plug=String(xp);
 }
 root.querySelectorAll('input').forEach(e=>e.addEventListener('input',draw));root.querySelector('[data-reset]').addEventListener('click',()=>{f('da').value=2;f('tanks').value=3;draw()});draw();
});


document.querySelectorAll('[data-lab="PE02-I2"]').forEach(root=>{
 const zh=root.closest('[data-lang]').dataset.lang==='zh',f=k=>root.querySelector('[data-field="'+k+'"]');
 function draw(){const ratio=Number(f('ratio').value),t=Number(f('time').value),k1=.1,k2=k1*ratio;
 function composition(time){const a=Math.exp(-k1*time),p=Math.abs(ratio-1)<1e-7?k1*time*a:(Math.exp(-k1*time)-Math.exp(-k2*time))/(ratio-1);return [a,Math.max(0,p),Math.max(0,1-a-p)];}
 const peak=Math.abs(ratio-1)<1e-7?1/k1:Math.log(ratio)/(k2-k1),peakP=composition(peak)[1],values=composition(t),colors=['#087d80','#bd582a','#3c64a0'];
 f('ratio-value').textContent=ratio.toFixed(2);f('time-value').textContent=t.toFixed(1)+' min';
 let s='<rect width="600" height="480" fill="#faf9f5"/><text x="65" y="37" font-size="22" fill="#19383f">'+(zh?'浓度 / 初始A浓度':'Concentration / initial A')+'</text>';
 for(let j=0;j<=4;j++){const v=j/4,y=360-270*v;s+='<line x1="65" y1="'+y+'" x2="550" y2="'+y+'" stroke="#d5dfda"/><text x="53" y="'+(y+7)+'" text-anchor="end" font-size="19" fill="#63757b">'+v+'</text>';}
 for(let j=0;j<=4;j++){const x=65+485*j/4;s+='<text x="'+x+'" y="390" text-anchor="middle" font-size="19" fill="#63757b">'+15*j+'</text>';}
 s+='<line x1="65" y1="90" x2="65" y2="360" stroke="#63757b"/><text x="305" y="433" text-anchor="middle" font-size="22" fill="#19383f">'+(zh?'时间 / min':'Time / min')+'</text>';
 for(let j=0;j<3;j++){let pts=[];for(let i=0;i<=150;i++)pts.push((65+485*i/150).toFixed(2)+','+(360-270*composition(60*i/150)[j]).toFixed(2));s+='<polyline points="'+pts.join(' ')+'" fill="none" stroke="'+colors[j]+'" stroke-width="3"/>';s+='<text x="'+(160+140*j)+'" y="472" font-size="23" fill="'+colors[j]+'">'+['A','P','S'][j]+'</text>';}
 const x=65+485*t/60;s+='<line x1="'+x+'" y1="90" x2="'+x+'" y2="360" stroke="#19383f" stroke-dasharray="5 5"/>';
 values.forEach((v,j)=>s+='<circle cx="'+x+'" cy="'+(360-270*v)+'" r="5" fill="'+colors[j]+'"/>');f('plot').innerHTML=s;
 f('result').textContent=zh?'在'+t.toFixed(1)+' min时，A、P、S相对初始A的比例分别为'+values.map(v=>(100*v).toFixed(1)+'%').join('、')+'。P的峰值出现在'+peak.toFixed(2)+' min，最大比例为'+(peakP*100).toFixed(1)+'%。':'At '+t.toFixed(1)+' min, A, P and S are '+values.map(v=>(100*v).toFixed(1)+'%').join(', ')+' of initial A. P peaks at '+peak.toFixed(2)+' min, reaching '+(100*peakP).toFixed(1)+'%.';
 root.dataset.total=String(values.reduce((a,b)=>a+b,0));root.dataset.peakTime=String(peak);root.dataset.peakYield=String(peakP);root.dataset.product=String(values[1]);
 }
 root.querySelectorAll('input').forEach(e=>e.addEventListener('input',draw));root.querySelector('[data-reset]').addEventListener('click',()=>{f('ratio').value=.5;f('time').value=14;draw()});draw();
});

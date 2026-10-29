document.querySelectorAll('[data-lab="CP04-I1"]').forEach(root=>{
 const zh=root.dataset.lang==='zh', nInput=root.querySelector('[data-field="n"]'), choice=root.querySelector('[data-field="state"]'), plot=root.querySelector('[data-field="plot"]');
 const modes=[{id:'good',nu:.6,color:'#167c82',name:zh?'良溶剂':'Good solvent'},{id:'theta',nu:.5,color:'#c17c2d',name:zh?'理想链':'Ideal chain'},{id:'compact',nu:1/3,color:'#765794',name:zh?'紧密球团':'Compact globule'}];
 const X=n=>75+(Math.log10(n)-2)/2*455,Y=r=>345-Math.log10(r)/Math.log10(400)*270;
 function update(){const n=Math.round(10**Number(nInput.value));root.querySelector('[data-field="nvalue"]').textContent=n.toLocaleString();let s='<rect width="600" height="430" fill="#f4f3ed"/><g font-family="Arial,sans-serif" font-size="21" fill="#173e45"><path d="M75 65V345H545" fill="none" stroke="#526a70" stroke-width="2"/>';
 [100,1000,10000].forEach(v=>s+=`<text x="${X(v)}" y="376" text-anchor="middle">${v}</text>`);[1,10,100].forEach(v=>s+=`<path d="M75 ${Y(v)}H545" stroke="#d2dfdb"/><text x="63" y="${Y(v)+7}" text-anchor="end">${v}</text>`);
 s+=`<text x="75" y="35">${zh?'尺寸 / nm':'Size / nm'}</text><text x="310" y="417" text-anchor="middle">${zh?'链段数 N（对数刻度）':'Segment count N (log scale)'}</text>`;
 modes.forEach(m=>{let d='';for(let i=0;i<=100;i++){const x=10**(2+2*i/100);d+=(i?'L':'M')+X(x).toFixed(2)+','+Y(x**m.nu).toFixed(2)+' ';}s+=`<path d="${d}" fill="none" stroke="${m.color}" stroke-width="${m.id===choice.value?5:2}" opacity="${m.id===choice.value?1:.42}"/>`;if(m.id===choice.value)s+=`<circle cx="${X(n)}" cy="${Y(n**m.nu)}" r="7" fill="${m.color}"/>`;});plot.innerHTML=s+'</g>';
 const m=modes.find(m=>m.id===choice.value),r=n**m.nu,ratio=10**m.nu;
 root.querySelector('[data-field="feedback"]').textContent=zh?`${m.name}标度：N = ${n}，尺寸约 ${r.toFixed(1)} nm。链段数增加10倍，尺寸增加约 ${ratio.toFixed(2)} 倍。图中取链段长度1 nm和单位比例系数，比较的是指数造成的差别。`:`${m.name} scaling: N = ${n}, size ≈ ${r.toFixed(1)} nm. A tenfold increase in segment count increases size by about ${ratio.toFixed(2)}. The plot uses a 1 nm segment length and unit prefactor to compare exponents.`;
 }
 nInput.addEventListener('input',update);choice.addEventListener('change',update);update();
});
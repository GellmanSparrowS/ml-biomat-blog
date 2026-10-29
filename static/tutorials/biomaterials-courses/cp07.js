document.querySelectorAll('[data-lab="CP07-I1"]').forEach(root=>{
 const zh=root.dataset.lang==='zh',q=k=>root.querySelector('[data-field="'+k+'"]'),p2=u=>(3*u*u-1)/2;
 function update(){const k=+q('k').value;q('kv').textContent=k.toFixed(1);const count=800,du=2/count;let z=0,s=0,u2=0;
  for(let i=0;i<=count;i++){const u=-1+i*du,w=Math.exp(k*p2(u)),coef=(i===0||i===count)?1:(i%2?4:2);z+=coef*w;s+=coef*w*p2(u);u2+=coef*w*u*u;}z*=du/3;s=s*du/3/z;u2=u2*du/3/z;
  const density=u=>Math.exp(k*p2(u))/z,max=Math.max(density(-1),density(0),density(1))*1.12,X=u=>80+(u+1)/2*465,Y=p=>340-p/max*245;
  let str='<rect width="600" height="450" fill="#f4f3ed"/><g font-family="Arial,sans-serif" font-size="21" fill="#173e45"><path d="M80 85V340H545" stroke="#53686d" stroke-width="2" fill="none"/>';
  for(let i=0;i<=4;i++){let v=max*i/4;str+=`<path d="M80 ${Y(v)}H545" stroke="#d4dfda"/><text x="70" y="${Y(v)+7}" text-anchor="end" font-size="18">${v.toFixed(2)}</text>`;}
  for(const u of [-1,-.5,0,.5,1])str+=`<text x="${X(u)}" y="374" text-anchor="middle">${u}</text>`;
  let d='';for(let i=0;i<=300;i++){let u=-1+2*i/300;d+=(i?'L':'M')+X(u).toFixed(2)+','+Y(density(u)).toFixed(2)+' ';}str+=`<path d="${d}" fill="none" stroke="#207d80" stroke-width="4"/><text x="30" y="37">${zh?'概率密度 p(u)':'Probability density p(u)'}</text><text x="310" y="418" text-anchor="middle">u = cos θ</text></g>`;q('plot').innerHTML=str;
  const interpretation=k>0?(zh?'平行与反平行方向共同增强。':'Parallel and antiparallel orientations are both favoured.'):(k<0?(zh?'偏向垂直于参考轴的方向。':'Orientations perpendicular to the reference axis are favoured.'):(zh?'三维各向同性：平方投影平均为1/3。':'Three-dimensional isotropy: mean squared projection is 1/3.'));
  q('feedback').textContent=zh?`κ=${k.toFixed(1)}，归一化因子Z=${z.toFixed(4)}，平均u²=${u2.toFixed(4)}，S=${s.toFixed(4)}。${interpretation} 概率密度积分为1；密度峰值可以大于1。`:`κ=${k.toFixed(1)}, normalization Z=${z.toFixed(4)}, mean u²=${u2.toFixed(4)}, S=${s.toFixed(4)}. ${interpretation} The density integrates to one; its peak may exceed one.`;
 }
 q('k').addEventListener('input',update);q('reset').addEventListener('click',()=>{q('k').value=0;update();});update();
});

document.querySelectorAll('[data-lab="CP06-I1"]').forEach(root=>{
 const zh=root.dataset.lang==='zh',q=k=>root.querySelector('[data-field="'+k+'"]');
 function update(){const r=+q('r').value,u=+q('u').value;q('rv').textContent=r.toFixed(4);
  const f=m=>r*m*m/2+u*m**4/4+m**6/6,curv=m=>r+3*u*m*m+5*m**4;
  let points=[0],disc=u*u-4*r;
  if(disc>=0)for(const y of [(-u+Math.sqrt(disc))/2,(-u-Math.sqrt(disc))/2])if(y>1e-12)points.push(-Math.sqrt(y),Math.sqrt(y));
  points=[...new Set(points.map(v=>+v.toFixed(10)))].sort((a,b)=>a-b);
  const mins=points.filter(m=>curv(m)>1e-8||(Math.abs(m)<1e-8&&Math.abs(r)<1e-8&&u>0)),best=Math.min(...mins.map(f));
  const vals=Array.from({length:281},(_,i)=>({m:-1.4+i*.01,g:f(-1.4+i*.01)}));let ymin=Math.min(...vals.map(p=>p.g))-.025,ymax=Math.max(.2,...mins.map(f))+.05;
  const X=m=>80+(m+1.4)/2.8*465,Y=g=>340-(g-ymin)/(ymax-ymin)*245;
  let s='<rect width="600" height="450" fill="#f4f3ed"/><g font-family="Arial,sans-serif" font-size="21" fill="#173e45"><path d="M80 85V340H545" stroke="#526a70" stroke-width="2" fill="none"/>';
  for(let i=0;i<=4;i++){let g=ymin+(ymax-ymin)*i/4;s+=`<path d="M80 ${Y(g)}H545" stroke="#d3dfda"/><text x="70" y="${Y(g)+6}" text-anchor="end" font-size="18">${g.toFixed(2)}</text>`;}
  for(const m of [-1,0,1])s+=`<text x="${X(m)}" y="374" text-anchor="middle">${m}</text>`;
  s+=`<text x="30" y="37">${zh?'无量纲自由能 f':'Dimensionless free energy f'}</text><text x="310" y="418" text-anchor="middle">${zh?'序参量 m':'Order parameter m'}</text>`;
  let d='',pen=false;vals.forEach(p=>{if(p.g<=ymax&&p.g>=ymin){d+=(pen?'L':'M')+X(p.m).toFixed(2)+','+Y(p.g).toFixed(2)+' ';pen=true;}else pen=false;});s+=`<path d="${d}" fill="none" stroke="#435d72" stroke-width="4"/>`;
  mins.forEach(m=>s+=`<circle cx="${X(m)}" cy="${Y(f(m))}" r="7" fill="${Math.abs(f(m)-best)<1e-8?'#207d80':'#b96635'}"/>`);q('plot').innerHTML=s+'</g>';
  const mintext=mins.map(m=>`${m.toFixed(3)} (${Math.abs(f(m)-best)<1e-8?(zh?'全局':'global'):(zh?'亚稳':'metastable')})`).join(zh?'；':'; ');
  const transition=u>0?0:3/16;
  q('feedback').textContent=zh?`r=${r.toFixed(4)}，u=${u}。平衡转变在r=${transition.toFixed(4)}。最低点m：${mintext}。${u>0?'最低点连续从0出现。':'等深时m从0跳到约±0.866；原点到r=0才失稳。'}`:`r=${r.toFixed(4)}, u=${u}. Equilibrium transition at r=${transition.toFixed(4)}. Minima m: ${mintext}. ${u>0?'The minima emerge continuously from zero.':'At equal depth m jumps from zero to about ±0.866; the origin loses stability only at r=0.'}`;
 }
 q('r').addEventListener('input',update);q('u').addEventListener('change',update);q('transition').addEventListener('click',()=>{q('r').value=+q('u').value>0?0:3/16;update();});update();
});

document.querySelectorAll('[data-lab="CP05-I1"]').forEach(root=>{
 const zh=root.dataset.lang==='zh',get=k=>root.querySelector('[data-field="'+k+'"]'),plot=get('plot');
 function update(){
  const n=+get('n').value,chi=+get('chi').value,phi=+get('phi').value,crit=2/n;
  get('nv').textContent=n;get('cv').textContent=chi.toFixed(3);get('pv').textContent=phi.toFixed(2);
  const f=p=>(p===0||p===1)?0:(p*Math.log(p)+(1-p)*Math.log(1-p))/n+chi*p*(1-p);
  const fp=p=>Math.log(p/(1-p))/n+chi*(1-2*p),curv=1/(n*phi)+1/(n*(1-phi))-2*chi;
  let bin=null,spin=null;
  if(chi>crit+1e-12){let lo=1e-16,hi=.5-1e-8;for(let k=0;k<90;k++){const mid=(lo+hi)/2;if(fp(mid)>0)hi=mid;else lo=mid;}bin=(lo+hi)/2;spin=(1-Math.sqrt(1-2/(n*chi)))/2;}
  const vals=Array.from({length:241},(_,i)=>f(i/240));let mn=Math.min(...vals),mx=Math.max(...vals),span=mx-mn;if(span<.001)span=.001;mn-=span*.12;mx+=span*.20;
  const X=p=>80+465*p,Y=g=>340-(g-mn)/(mx-mn)*250;
  let s='<rect width="600" height="450" fill="#f4f3ed"/><g font-family="Arial,sans-serif" font-size="21" fill="#173e45">';
  if(spin!==null)s+=`<rect x="${X(spin)}" y="90" width="${X(1-spin)-X(spin)}" height="250" fill="#f1ddd0"/>`;
  s+='<path d="M80 90V340H545" stroke="#53686d" stroke-width="2" fill="none"/>';
  for(let i=0;i<=4;i++){const g=mn+(mx-mn)*i/4;s+=`<path d="M80 ${Y(g)}H545" stroke="#d2ddda"/><text x="70" y="${Y(g)+6}" text-anchor="end" font-size="18">${g.toFixed(Math.max(3, Math.min(7, 2 - Math.floor(Math.log10(mx-mn)))))}</text>`;}
  for(const p of [0,.25,.5,.75,1])s+=`<text x="${X(p)}" y="371" text-anchor="middle">${p.toFixed(2)}</text>`;
  s+=`<text x="30" y="39">${zh?'自由能 g（每格 / kBT）':'Free energy g (per site / kBT)'}</text><text x="305" y="415" text-anchor="middle">${zh?'A体积分数 φ':'A volume fraction φ'}</text>`;
  let d='';vals.forEach((g,i)=>d+=(i?'L':'M')+X(i/240).toFixed(2)+','+Y(g).toFixed(2)+' ');s+=`<path d="${d}" fill="none" stroke="#207d80" stroke-width="4"/>`;
  if(bin!==null){s+=`<path d="M${X(bin)} ${Y(f(bin))}H${X(1-bin)}" stroke="#715791" stroke-width="3" stroke-dasharray="7 5"/><circle cx="${X(bin)}" cy="${Y(f(bin))}" r="5" fill="#715791"/><circle cx="${X(1-bin)}" cy="${Y(f(bin))}" r="5" fill="#715791"/>`;}
  s+=`<circle cx="${X(phi)}" cy="${Y(f(phi))}" r="7" fill="#b56334"/></g>`;plot.innerHTML=s;
  let state;
  if(Math.abs(curv)<1e-7)state=zh?'局部曲率为零，位于局部稳定性边界。':'Local curvature is zero: a local-stability boundary.';
  else if(curv<0)state=zh?'局部不稳定：很小的组成起伏降低自由能。':'Locally unstable: very small composition fluctuations lower free energy.';
  else if(bin!==null&&phi>bin&&phi<1-bin)state=zh?'亚稳：小起伏受抑制，但公切线所示两相的自由能更低。':'Metastable: small fluctuations are opposed, but the common-tangent two-phase state is lower in free energy.';
  else state=zh?'在此模型中是稳定的均匀组成。':'A stable uniform composition in this model.';
  get('feedback').textContent=(zh?`N=${n}，χ=${chi.toFixed(3)}，临界χ=${crit.toFixed(4)}。φ=${phi.toFixed(2)}，g=${f(phi).toFixed(5)}，g″=${curv.toFixed(5)}。`:`N=${n}, χ=${chi.toFixed(3)}, critical χ=${crit.toFixed(4)}. φ=${phi.toFixed(2)}, g=${f(phi).toFixed(5)}, g″=${curv.toFixed(5)}. `)+state;
  get('coexist').textContent=bin===null?(zh?'当前没有两相公切线。曲线的最低点与选定总组成是不同概念；总组成由加入的两种物质量决定。':'There is no two-phase common tangent at these settings. The curve minimum and the chosen overall composition are different concepts; the amounts added determine overall composition.'):(zh?`紫色虚线为公切线；共存组成约为${bin.toFixed(3)}和${(1-bin).toFixed(3)}。浅橙区域为负曲率区；处于共存组成之间时，两相数量由杠杆规则确定。`:`The purple dashed common tangent joins coexistence compositions of about ${bin.toFixed(3)} and ${(1-bin).toFixed(3)}. Pale orange marks negative curvature. Within the coexistence interval, the lever rule sets phase amounts.`);
 }
 ['n','chi','phi'].forEach(k=>get(k).addEventListener('input',update));update();
});

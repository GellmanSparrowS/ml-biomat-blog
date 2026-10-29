document.querySelectorAll('[data-lab="CP08-I1"]').forEach(root=>{
 const zh=root.dataset.lang==='zh',q=k=>root.querySelector('[data-field="'+k+'"]');
 function update(){const n=+q('n').value,sigma=10**(+q('sigma').value),a=.5,R=a*n**.6,D=sigma**(-.5),cross=1/(R*R),h=n*a*(sigma*a*a)**(1/3),contour=n*a,overlap=sigma*R*R;
  q('nv').textContent=n;q('sv').textContent=sigma.toFixed(4);const maxh=n*a*(10**(-.4)*a*a)**(1/3),ymax=Math.max(10,maxh*1.15),X=s=>80+(Math.log10(s)+3)/2.6*465,Y=v=>340-v/ymax*245;
  let st='<rect width="600" height="450" fill="#f4f3ed"/><g font-family="Arial,sans-serif" font-size="21" fill="#173e45">';const bound=Math.max(80,Math.min(545,X(cross)));st+=`<rect x="80" y="95" width="${bound-80}" height="245" fill="#e3e6e1"/><path d="M80 95V340H545" stroke="#526a70" stroke-width="2" fill="none"/>`;
  for(let i=0;i<=4;i++){const v=ymax*i/4;st+=`<path d="M80 ${Y(v)}H545" stroke="#d0dcd6"/><text x="70" y="${Y(v)+7}" text-anchor="end" font-size="18">${v.toFixed(0)}</text>`;}for(const v of [.001,.01,.1])st+=`<text x="${X(v)}" y="374" text-anchor="middle">${v}</text>`;
  let d='',start=false;for(let i=0;i<=250;i++){const s=10**(-3+2.6*i/250);if(s>=cross){d+=(start?'L':'M')+X(s).toFixed(2)+','+Y(n*a*(s*a*a)**(1/3)).toFixed(2)+' ';start=true;}}st+=`<path d="${d}" fill="none" stroke="#207d80" stroke-width="4"/>`;
  if(overlap>=1)st+=`<circle cx="${X(sigma)}" cy="${Y(h)}" r="7" fill="#b66838"/>`;else st+=`<path d="M${X(sigma)} 95V340" stroke="#b66838" stroke-width="3" stroke-dasharray="5 4"/>`;
  st+=`<text x="30" y="37">${zh?'刷高 h / nm':'Brush height h / nm'}</text><text x="310" y="419" text-anchor="middle">${zh?'接枝密度 σ / nm⁻²（对数）':'Graft density σ / nm⁻² (log)'}</text></g>`;q('plot').innerHTML=st;
  const desc=overlap<1?(zh?'蘑菇区：线团尚未明显交叠，不用刷高公式。':'Mushroom regime: coils do not appreciably overlap; brush height is not applied.'):(zh?`交叠刷层估算h≈${h.toFixed(2)} nm，约为轮廓长度的${(100*h/contour).toFixed(1)}%。`:`Overlapping-brush estimate h≈${h.toFixed(2)} nm, ${(100*h/contour).toFixed(1)}% of contour length.`);
  q('feedback').textContent=zh?`N=${n}，σ=${sigma.toFixed(4)} nm⁻²，间距D≈${D.toFixed(2)} nm，自由线团尺度R≈${R.toFixed(2)} nm。σR²=${overlap.toFixed(2)}，轮廓长度${contour.toFixed(1)} nm。${desc}`:`N=${n}, σ=${sigma.toFixed(4)} nm⁻², spacing D≈${D.toFixed(2)} nm, free-coil scale R≈${R.toFixed(2)} nm. σR²=${overlap.toFixed(2)}; contour length ${contour.toFixed(1)} nm. ${desc}`;
 }
 ['n','sigma'].forEach(k=>q(k).addEventListener('input',update));update();
});

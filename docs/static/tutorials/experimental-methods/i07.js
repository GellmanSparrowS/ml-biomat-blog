(function(){
  const root=document.getElementById('I07-lab');
  if(!root)return;
  const zh=document.documentElement.lang.startsWith('zh');
  const tr=(a,b)=>zh?a:b;
  const lo=root.querySelector('#I07-lo'),hi=root.querySelector('#I07-hi');
  const svg=root.querySelector('#I07-plot'),result=root.querySelector('#I07-result');
  const data=JSON.parse(root.querySelector('#I07-data').textContent);
  let current={};
  function draw(){
    let qmin=Number(lo.value),qmax=Number(hi.value);
    const chosen=data.filter(d=>d[0]>=qmin&&d[0]<=qmax&&d[1]>0&&d[2]>0);
    let sw=0,sx=0,sy=0,sxx=0,sxy=0;
    for(const [q,i,e] of chosen){const w=(i/e)**2,x=q*q,y=Math.log(i);sw+=w;sx+=w*x;sy+=w*y;sxx+=w*x*x;sxy+=w*x*y;}
    const slope=(sw*sxy-sx*sy)/(sw*sxx-sx*sx),intercept=(sy-slope*sx)/sw;
    const rg=Math.sqrt(-3*slope),i0=Math.exp(intercept);
    current={qmin:qmin,qmax:qmax,points:chosen.length,rg_nm:rg,i0:i0,qmax_rg:qmax*rg};
    const X=x=>65+x/1.44*690,Y=y=>310-(y-1.6)/1.15*270;
    let html='<rect width="800" height="370" fill="#fbfcfc"/>';
    for(let x=0;x<=1.4001;x+=.2){html+=`<path d="M${X(x)},40V310" stroke="#dce3e8"/><text x="${X(x)}" y="333" text-anchor="middle" font-size="13">${x.toFixed(1)}</text>`;}
    for(let y=1.6;y<2.751;y+=.2){html+=`<text x="55" y="${Y(y)+4}" text-anchor="end" font-size="13">${y.toFixed(1)}</text>`;}
    html+='<defs><clipPath id="I07-clip"><rect x="65" y="40" width="690" height="270"/></clipPath></defs><g clip-path="url(#I07-clip)">';
    for(const [q,i,e] of data){if(i<=0)continue;const included=q>=qmin&&q<=qmax,x=X(q*q),y=Y(Math.log(i));html+=`<circle cx="${x}" cy="${y}" r="2.3" fill="${included?'#186c94':'white'}" stroke="${included?'#186c94':'#a1abb2'}"/>`;}
    html+=`<path d="M${X(qmin*qmin)},${Y(intercept+slope*qmin*qmin)}L${X(qmax*qmax)},${Y(intercept+slope*qmax*qmax)}" fill="none" stroke="#d27839" stroke-width="3"/></g><text x="400" y="361" text-anchor="middle">q² / nm⁻²</text><text x="19" y="185" transform="rotate(-90 19 185)" text-anchor="middle">ln I</text>`;
    svg.innerHTML=html;
    result.textContent=tr('拟合范围','Fit interval')+` ${qmin.toFixed(3)}–${qmax.toFixed(3)} nm⁻¹ · n=${chosen.length} · Rg=${rg.toFixed(4)} nm · I(0)=${i0.toFixed(4)} · qmax Rg=${(qmax*rg).toFixed(3)}`;
    return {...current};
  }
  const reset=()=>{lo.value=.087;hi.value=.8;return draw();};
  const set=p=>{if(p.qmin!==undefined)lo.value=p.qmin;if(p.qmax!==undefined)hi.value=p.qmax;return draw();};
  lo.addEventListener('input',draw);hi.addEventListener('input',draw);
  const btn=root.querySelector('#I07-reset');btn.addEventListener('click',reset);
  window.CourseLab={set,state:()=>({...current}),reset,destroy:()=>{lo.removeEventListener('input',draw);hi.removeEventListener('input',draw);btn.removeEventListener('click',reset);}};reset();
})();

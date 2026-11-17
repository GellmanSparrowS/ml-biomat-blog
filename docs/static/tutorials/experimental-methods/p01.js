(()=>{
 const zh=document.documentElement.lang.startsWith('zh'),L=(a,b)=>zh?a:b,get=k=>document.getElementById('P01-'+k),keys=['large','actual','entered'];let current={};
 const defaults={large:.1,actual:.89,entered:.89};
 function update(){const p=+get('large').value/100,eta=+get('actual').value,entered=+get('entered').value,w=p*729/(1-p+p*729),mean=(1-w)/10+w/30,z=1/mean;
 current={large_intensity_percent:100*w,true_z_nm:z,reported_z_nm:z*eta/entered,PDI:((1-w)*(1/10-mean)**2+w*(1/30-mean)**2)/mean**2,number_mean_nm:10+20*p};
 keys.forEach(k=>get(k+'-value').textContent=(+get(k).value).toFixed(k==='large'?3:2));
 get('result').textContent=L(`大颗粒光强占比 ${current.large_intensity_percent.toFixed(2)}%；真实 z 平均 ${z.toFixed(2)} nm；按输入黏度报告 ${current.reported_z_nm.toFixed(2)} nm；PDI ${current.PDI.toFixed(3)}。`,`Large-particle intensity ${current.large_intensity_percent.toFixed(2)}%; true z-average ${z.toFixed(2)} nm; reported with entered viscosity ${current.reported_z_nm.toFixed(2)} nm; PDI ${current.PDI.toFixed(3)}.`);
 const q=4*Math.PI*1.333/(633e-9)*Math.sin(Math.PI/4),rate=d=>1.380649e-23*298.15/(3*Math.PI*eta*.001*d*1e-9)*q*q;
 const X=x=>70+(Math.log10(x)+1)/5*650,Y=y=>315-(y-1)/.5*250;
 let h='<rect width="760" height="390" fill="#fcfbf7"/><path d="M70 40V315H725" fill="none" stroke="#566b77"/>';
 [1,1.1,1.2,1.3,1.4,1.5].forEach(v=>h+=`<path d="M70 ${Y(v)}H725" stroke="#dce3e4"/><text x="60" y="${Y(v)+4}" text-anchor="end" fill="#20333e">${v.toFixed(1)}</text>`);
 [.1,1,10,100,1000,10000].forEach(x=>h+=`<text x="${X(x)}" y="338" text-anchor="middle" fill="#20333e">${x}</text>`);
 for(const [mix,c] of [[false,'#d35f47'],[true,'#167d9a']]){let d='';for(let j=0;j<=260;j++){const us=10**(-1+j/260*5),t=us*1e-6,g=mix?(1-w)*Math.exp(-rate(10)*t)+w*Math.exp(-rate(30)*t):Math.exp(-rate(10)*t);d+=(j?'L':'M')+X(us).toFixed(2)+' '+Y(1+.5*g*g).toFixed(2)+' ';}h+=`<path d="${d}" fill="none" stroke="${c}" stroke-width="2.5"/>`;}
 h+=`<text x="70" y="24" fill="#20333e">g₂(τ)</text><text x="395" y="373" text-anchor="middle" fill="#20333e">${L('延迟时间 / μs（对数轴）','Delay time / μs (logarithmic axis)')}</text><text x="485" y="80" fill="#167d9a">${L('蓝：混合物','Blue: mixture')}</text><text x="485" y="105" fill="#d35f47">${L('红：仅10 nm','Red:10 nm only')}</text>`;get('plot').innerHTML=h;
 }
 function set(p){keys.forEach(k=>{if(p[k]!==undefined)get(k).value=Math.min(+get(k).max,Math.max(+get(k).min,+p[k]));});update();return {...current};}
 keys.forEach(k=>get(k).addEventListener('input',update));get('reset').addEventListener('click',()=>set(defaults));window.CourseLab={set,state:()=>({...current}),reset:()=>set(defaults)};set(defaults);
})();

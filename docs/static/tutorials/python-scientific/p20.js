(() => {
 const root=document.getElementById('P20-lab');if(!root)return;
 const zh=document.documentElement.lang.startsWith('zh'),tr=(a,b)=>zh?a:b,el=x=>root.querySelector('#P20-'+x);
 const dt=.02,t=Array.from({length:501},(_,i)=>i*dt),clean=t.map(t=>.1+.02*t+1.2*Math.exp(-.5*((t-3)/.25)**2)+.8*Math.exp(-.5*((t-7)/.5)**2)),raw=t.map((t,i)=>clean[i]+.12*Math.sin(2*Math.PI*9*t)+.035*Math.cos(2*Math.PI*17*t));
 const defaults={method:'savgol',window:21,focus:150};let p={...defaults},result={};
 const text=(x,y,s,anchor='start',size=14)=>`<text x="${x}" y="${y}" text-anchor="${anchor}" font-size="${size}" fill="#20313e">${s}</text>`;
 const reflected=j=>j<0?-j:j>500?1000-j:j;
 function draw(){
  const m=(p.window-1)/2,k=Array.from({length:p.window},(_,i)=>i-m),S2=k.reduce((s,x)=>s+x*x,0),S4=k.reduce((s,x)=>s+x**4,0),c=k.map(x=>p.method==='mean'?1/p.window:(S4-S2*x*x)/(p.window*S4-S2*S2));
  const smoothed=raw.map((_,i)=>k.reduce((s,x,j)=>s+c[j]*raw[reflected(i+x)],0)),gain=f=>Math.abs(k.reduce((s,x,j)=>s+c[j]*Math.cos(2*Math.PI*f*dt*x),0)),rmse=Math.sqrt(smoothed.reduce((s,x,i)=>s+(x-clean[i])**2,0)/501),nref=k.filter(x=>p.focus+x<0||p.focus+x>500).length;
  const wide=root.getBoundingClientRect().width>720,width=wide?860:430,L=64,W=width-90,T=57,H=232,X=x=>L+x/10*W,Y=y=>T+H-(y+.1)/1.7*H,svg=el('signal');svg.setAttribute('viewBox',`0 0 ${width} 355`);
  let s=text(L,23,tr('原始信号、模型与平滑结果','Input, model, and smoothed output'),'start',17)+text(L,46,tr('电压 / mV','Voltage / mV'));
  for(const y of [0,.4,.8,1.2,1.6])s+=`<line x1="${L}" x2="${L+W}" y1="${Y(y)}" y2="${Y(y)}" stroke="#e1e7eb"/>`+text(L-8,Y(y)+5,y.toFixed(1),'end');
  const left=Math.max(0,(p.focus-m)*dt),right=Math.min(10,(p.focus+m)*dt);s+=`<rect x="${X(left)}" y="${T}" width="${X(right)-X(left)}" height="${H}" fill="#f2e7cf" opacity=".7"/>`;
  for(const [values,color,dash,line] of [[raw,'#b9c6ce','',1],[clean,'#20313e','5 4',1.5],[smoothed,'#28658c','',2]])s+=`<path d="${values.map((v,i)=>`${i?'L':'M'}${X(t[i])},${Y(v)}`).join(' ')}" fill="none" stroke="${color}" stroke-width="${line}" stroke-dasharray="${dash}"/>`;
  s+=`<circle cx="${X(t[p.focus])}" cy="${Y(smoothed[p.focus])}" r="5" fill="#b64a35"/>`;for(const x of [0,2,4,6,8,10])s+=text(X(x),313,x,'middle');s+=text(L+W/2,342,tr('时间 / s','Time / s'),'middle');svg.innerHTML=s;
  const weights=el('weights');weights.setAttribute('viewBox','0 0 430 400');const l=64,w=339,xx=x=>l+(x+m+.5)/p.window*w,yw=y=>160-(y+.12)/.67*100,yr=y=>335-(y+.1)/1.7*120;
  s=text(l,23,tr('窗口权重与取入的样本','Weights and input neighborhood'),'start',17)+text(l,47,tr('权重（无量纲）','Weights (dimensionless)'));
  s+=`<line x1="${l}" x2="${l+w}" y1="${yw(0)}" y2="${yw(0)}" stroke="#8798a3"/>`;
  for(const y of [0,.25,.5])s+=text(l-8,yw(y)+5,y,'end');
  k.forEach((x,j)=>{const yy=c[j],zero=yw(0);s+=`<rect x="${xx(x)-w/p.window*.38}" y="${Math.min(zero,yw(yy))}" width="${w/p.window*.76}" height="${Math.abs(zero-yw(yy))}" fill="#28658c"/>`});
  s+=text(l,195,tr('取入的电压 / mV','Input voltage / mV'));for(const y of [0,.8,1.6])s+=`<line x1="${l}" x2="${l+w}" y1="${yr(y)}" y2="${yr(y)}" stroke="#e1e7eb"/>`+text(l-8,yr(y)+5,y.toFixed(1),'end');
  k.forEach(x=>{const source=reflected(p.focus+x);s+=`<circle cx="${xx(x)}" cy="${yr(raw[source])}" r="${p.window>21?2.7:4}" fill="${source===p.focus+x?'#20313e':'#b64a35'}"/>`});for(const x of [-m,0,m])s+=text(xx(x),362,x,'middle');s+=text(l+w/2,391,tr('相对中心的样本偏移 k','Sample offset k from center'),'middle');weights.innerHTML=s;
  const freq=el('gain');freq.setAttribute('viewBox','0 0 430 400');const xf=f=>l+f/25*w,yf=a=>335-a/1.05*278;
  s=text(l,23,tr('正弦幅值增益','Sinusoidal amplitude gain'),'start',17)+text(l,47,tr('增益，无量纲','Gain, dimensionless'));
  for(const a of [0,.25,.5,.75,1])s+=`<line x1="${l}" x2="${l+w}" y1="${yf(a)}" y2="${yf(a)}" stroke="#e1e7eb"/>`+text(l-8,yf(a)+5,a,'end');
  s+=`<path d="${Array.from({length:201},(_,i)=>`${i?'L':'M'}${xf(i/8)},${yf(gain(i/8))}`).join(' ')}" fill="none" stroke="#28658c" stroke-width="2.2"/><line x1="${xf(9)}" x2="${xf(9)}" y1="57" y2="335" stroke="#b64a35" stroke-dasharray="4 4"/><circle cx="${xf(9)}" cy="${yf(gain(9))}" r="5" fill="#b64a35"/>`;for(const f of [0,5,10,15,20,25])s+=text(xf(f),362,f,'middle');s+=text(l+w/2,391,tr('频率 / Hz','Frequency / Hz'),'middle');freq.innerHTML=s;
  result={...p,rmse,at3:smoothed[150],gain9:gain(9),reflected:nref,span_s:2*m*dt,coefficient_sum:c.reduce((a,b)=>a+b,0),focus_output:smoothed[p.focus]};el('focus-value').textContent=p.focus;
  el('readout').textContent=tr(`${p.window}点，首末跨度${result.span_s.toFixed(2)} s；3 s读数${result.at3.toFixed(6)} mV，RMSE ${rmse.toFixed(6)} mV，9 Hz幅值增益${result.gain9.toFixed(6)}。焦点t=${t[p.focus].toFixed(2)} s，镜像输入${nref}个。`,`${p.window} points span ${result.span_s.toFixed(2)} s; value at 3 s: ${result.at3.toFixed(6)} mV, RMSE ${rmse.toFixed(6)} mV, amplitude gain at 9 Hz: ${result.gain9.toFixed(6)}. Focus t = ${t[p.focus].toFixed(2)} s; ${nref} mirrored inputs.`);
 }
 function set(q){p={...p,...q};p.method=p.method==='mean'?'mean':'savgol';p.window=[5,11,21,41].includes(+p.window)?+p.window:21;p.focus=Math.round(Math.max(0,Math.min(500,+p.focus)));for(const key of ['method','window','focus'])el(key).value=p[key];draw();return result}
 for(const key of ['method','window','focus'])el(key).addEventListener('input',()=>set({[key]:el(key).value}));el('reset').addEventListener('click',()=>set(defaults));
 let observer=null,lastWidth=0;if(typeof ResizeObserver!=='undefined'){observer=new ResizeObserver(()=>{const w=root.getBoundingClientRect().width;if(Math.abs(w-lastWidth)>1){lastWidth=w;draw()}});observer.observe(root)}
 window.CourseLab={set,state:()=>structuredClone(result),reset:()=>set(defaults),destroy:()=>observer?.disconnect()};set(defaults);
})();

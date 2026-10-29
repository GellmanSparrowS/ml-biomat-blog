document.querySelectorAll('[data-lab="PE04-I1"]').forEach(root=>{
 const zh=root.closest('[data-lang]').dataset.lang==='zh', f=k=>root.querySelector('[data-field="'+k+'"]');
 const text=(x,y,s,size=21,color='#627780',anchor='start')=>'<text x="'+x+'" y="'+y+'" font-size="'+size+'" fill="'+color+'" text-anchor="'+anchor+'">'+s+'</text>';
 function draw(){
  const delta=Number(f('delta').value),initial=Number(f('initial').value),crit=1/Math.E;
  f('delta-value').textContent=delta.toFixed(3);f('initial-value').textContent=initial.toFixed(2);
  const rate=t=>delta*Math.exp(t)-t,roots=[];
  if(delta<crit){for(const interval of [[0,1],[1,10]]){let [a,b]=interval;for(let n=0;n<55;n++){const m=(a+b)/2;if(rate(a)*rate(m)<=0)b=m;else a=m;}roots.push((a+b)/2);}}
  let trajectory=[[0,initial]],t=0,v=initial;const dt=.002;
  while(t<10&&v<4){let h=Math.min(dt,.02/Math.max(1,Math.abs(rate(v))),10-t),a=rate(v),b=rate(v+h*a/2),c=rate(v+h*b/2),d=rate(v+h*c);let next=v+h*(a+2*b+2*c+d)/6;if(next>=4){const hlast=h*(4-v)/(next-v);t+=hlast;v=4;trajectory.push([t,v]);break;}t+=h;v=next;if(trajectory.length===1||t-trajectory.at(-1)[0]>=.025||t>=10)trajectory.push([t,v]);}
  let s='<rect width="640" height="840" fill="#faf9f5"/>';
  const x=q=>75+515*q/3,y=q=>330-250*q/11;
  s+=text(75,36,zh?'产热与散热 / 无量纲':'Generation and removal / scaled power',21,'#19383f');
  for(let q=0;q<=10;q+=2){s+='<line x1="75" x2="590" y1="'+y(q)+'" y2="'+y(q)+'" stroke="#d7dfdb"/>'+text(61,y(q)+6,String(q),18,'#627780','end');}
  for(let q=0;q<=3;q++)s+=text(x(q),360,String(q),20,'#627780','middle');
  s+='<line x1="75" x2="75" y1="80" y2="330" stroke="#627780"/>';
  const pts=[];for(let i=0;i<=160;i++){const q=3*i/160;pts.push(x(q).toFixed(2)+','+y(delta*Math.exp(q)).toFixed(2));}
  s+='<polyline points="'+pts.join(' ')+'" fill="none" stroke="#bc592c" stroke-width="3"/><line x1="'+x(0)+'" y1="'+y(0)+'" x2="'+x(3)+'" y2="'+y(3)+'" stroke="#087b83" stroke-width="3"/>';
  roots.filter(r=>r<=3).forEach((r,i)=>{s+='<circle cx="'+x(r)+'" cy="'+y(r)+'" r="6" fill="'+(i===0?'#087b83':'#bc592c')+'" stroke="#faf9f5" stroke-width="2"/>';});
  s+=text(330,397,zh?'θ：无量纲温升':'θ: dimensionless temperature rise',21,'#19383f','middle');
  s+=text(75,435,zh?'橙线：产热　青线：散热':'Orange: generation · teal: removal',20);
  const xx=q=>75+515*q/10,yy=q=>730-235*q/4;
  s+=text(75,477,zh?'温度轨迹 / 无量纲温升':'Trajectory / scaled temperature rise',21,'#19383f');
  for(let q=0;q<=4;q++){s+='<line x1="75" x2="590" y1="'+yy(q)+'" y2="'+yy(q)+'" stroke="#d7dfdb"/>'+text(61,yy(q)+6,String(q),18,'#627780','end');}
  for(let q=0;q<=10;q+=2)s+=text(xx(q),765,String(q),20,'#627780','middle');
  s+='<polyline points="'+trajectory.map(p=>xx(p[0]).toFixed(2)+','+yy(p[1]).toFixed(2)).join(' ')+'" stroke="#17313b" stroke-width="3" fill="none"/>';
  s+=text(330,811,zh?'s：无量纲时间':'s: dimensionless time',21,'#19383f','middle');f('plot').innerHTML=s;
  const desc=roots.length?(zh?'两个交点为 θ = '+roots[0].toFixed(4)+' 和 '+roots[1].toFixed(4)+'。较低交点局部稳定，较高交点不稳定。':'Intersections occur at θ = '+roots[0].toFixed(4)+' and '+roots[1].toFixed(4)+'. The lower state is locally stable and the upper one unstable.'):(zh?'δ 超过 1/e ≈ 0.3679，图中模型没有平衡交点。':'δ exceeds 1/e ≈ 0.3679, so this model has no equilibrium intersection.');
  f('result').textContent=desc+' '+(v>=4?(zh?'轨迹在 s = '+t.toFixed(2)+' 达到 θ = 4，图线在此结束；后续应加入消耗、相变等过程。':'The trajectory reaches θ = 4 at s = '+t.toFixed(2)+', where this plot ends. Later evolution requires depletion, phase changes and other relevant processes.'):(zh?'到 s = 10，θ = '+v.toFixed(4)+'。轨迹按单温度近似的能量方程计算。':'At s = 10, θ = '+v.toFixed(4)+'. The trajectory follows the one-temperature energy model.'));
  root.dataset.lower=roots.length?String(roots[0]):'';root.dataset.upper=roots.length?String(roots[1]):'';root.dataset.final=String(v);
 }
 root.querySelectorAll('input').forEach(e=>e.addEventListener('input',draw));root.querySelector('[data-reset]').addEventListener('click',()=>{f('delta').value=.3;f('initial').value=0;draw();});draw();
});


document.querySelectorAll('[data-lab="PE04-I2"]').forEach(root=>{
 const zh=root.closest('[data-lang]').dataset.lang==='zh',f=k=>root.querySelector('[data-field="'+k+'"]');
 const k=T=>.01*Math.exp(10000*(1/350-1/T));
 const text=(x,y,s,size=20,color='#627780',anchor='start')=>'<text x="'+x+'" y="'+y+'" font-size="'+size+'" fill="'+color+'" text-anchor="'+anchor+'">'+s+'</text>';
 function draw(){
  const coolant=Number(f('coolant').value),T0=Number(f('initialT').value),C0=Number(f('initialC').value);
  f('coolant-value').textContent=coolant.toFixed(0)+' K';f('T-value').textContent=T0.toFixed(0)+' K';f('C-value').textContent=C0.toFixed(2)+' mol/L';
  const generation=T=>2000*k(T)/(1+100*k(T)),removal=T=>.1*(T-300)+.1*(T-coolant),balance=T=>generation(T)-removal(T);
  const roots=[];function keep(T){if(!roots.some(x=>Math.abs(x.T-T)<1e-5)){let rate=k(T),C=1/(1+100*rate),kp=rate*10000/T**2,a=-.01-rate,b=-kp*C,c=200*rate,d=-.02+200*kp*C;roots.push({T,C,stable:a+d<0&&a*d-b*c>0,trace:a+d,det:a*d-b*c});}}
  for(let a=250;a<470;a+=.25){let b=a+.25;if(Math.abs(balance(a))<1e-10)keep(a);if(balance(a)*balance(b)<0){let lo=a,hi=b;for(let j=0;j<45;j++){let m=(lo+hi)/2;if(balance(lo)*balance(m)<=0)hi=m;else lo=m;}keep((lo+hi)/2);}}
  roots.sort((a,b)=>a.T-b.T);
  const rhs=(C,T)=>[.01*(1-C)-k(T)*C,.01*(300-T)+200*k(T)*C-.01*(T-coolant)];
  function step(C,T,h){let a=rhs(C,T),b=rhs(C+h*a[0]/2,T+h*a[1]/2),c=rhs(C+h*b[0]/2,T+h*b[1]/2),d=rhs(C+h*c[0],T+h*c[1]);return [C+h*(a[0]+2*b[0]+2*c[0]+d[0])/6,T+h*(a[1]+2*b[1]+2*c[1]+d[1])/6];}
  let t=0,C=C0,T=T0,peak=T0,history=[[0,C,T]],steps=0;
  while(t<1200){let h=Math.min(.2,.02/(.01+k(T)),1200-t),next=step(C,T,h);for(let tries=0;tries<15&&(!Number.isFinite(next[1])||next[0]<0||next[0]>1.000001||next[1]<200||next[1]>650);tries++){h/=2;next=step(C,T,h);}C=next[0];T=next[1];t+=h;peak=Math.max(peak,T);steps++;if(t-history.at(-1)[0]>=1.5||t>=1200)history.push([t,C,T]);}
  let s='<rect width="680" height="1125" fill="#faf9f5"/>';
  const x=q=>85+535*(q-280)/150,y=q=>340-250*(q+8)/36;
  s+=text(85,35,zh?'稳态热功率 / kW':'Steady heat power / kW',22,'#19383f');
  for(let q=-5;q<=25;q+=5){s+='<line x1="85" x2="620" y1="'+y(q)+'" y2="'+y(q)+'" stroke="#d7dfdb"/>'+text(68,y(q)+6,String(q),18,'#627780','end');}
  for(let q=280;q<=430;q+=30)s+=text(x(q),374,String(q),19,'#627780','middle');
  for(const [fn,color] of [[generation,'#bc592c'],[removal,'#087b83']]){let pts=[];for(let i=0;i<=180;i++){let q=280+150*i/180;pts.push(x(q).toFixed(2)+','+y(fn(q)).toFixed(2));}s+='<polyline points="'+pts.join(' ')+'" fill="none" stroke="'+color+'" stroke-width="3"/>';}
  roots.forEach(r=>{s+='<circle cx="'+x(r.T)+'" cy="'+y(generation(r.T))+'" r="6" fill="'+(r.stable?'#087b83':'#bc592c')+'" stroke="#faf9f5" stroke-width="2"/>';});
  s+=text(350,409,zh?'温度 / K':'Temperature / K',21,'#19383f','middle')+text(85,447,zh?'橙线：产热；青线：移热':'Orange: generation; teal: removal',20);
  const xx=q=>85+535*q/1200;const minT=Math.floor(Math.min(...history.map(p=>p[2]))/20)*20-10,maxT=Math.ceil(Math.max(...history.map(p=>p[2]))/20)*20+10;
  const yy=q=>731-230*(q-minT)/(maxT-minT);
  s+=text(85,486,zh?'瞬态温度 / K':'Transient temperature / K',22,'#19383f');
  for(let j=0;j<=4;j++){let q=minT+(maxT-minT)*j/4;s+='<line x1="85" x2="620" y1="'+yy(q)+'" y2="'+yy(q)+'" stroke="#d7dfdb"/>'+text(68,yy(q)+6,q.toFixed(0),18,'#627780','end');}
  s+='<polyline points="'+history.map(p=>xx(p[0]).toFixed(2)+','+yy(p[2]).toFixed(2)).join(' ')+'" fill="none" stroke="#bc592c" stroke-width="3"/>';
  for(let q=0;q<=20;q+=5)s+=text(xx(q*60),764,String(q),19,'#627780','middle');
  s+=text(85,811,zh?'瞬态浓度 / mol·L⁻¹':'Transient concentration / mol·L⁻¹',22,'#19383f');
  const yc=q=>1035-200*q;
  for(let j=0;j<=4;j++){let q=j/4;s+='<line x1="85" x2="620" y1="'+yc(q)+'" y2="'+yc(q)+'" stroke="#d7dfdb"/>'+text(68,yc(q)+6,q.toFixed(2),18,'#627780','end');}
  s+='<polyline points="'+history.map(p=>xx(p[0]).toFixed(2)+','+yc(p[1]).toFixed(2)).join(' ')+'" fill="none" stroke="#087b83" stroke-width="3"/>';
  for(let q=0;q<=20;q+=5)s+=text(xx(q*60),1068,String(q),19,'#627780','middle');
  s+=text(350,1110,zh?'两幅轨迹的横轴：时间 / min':'Both trajectories: time / min',21,'#19383f','middle');f('plot').innerHTML=s;
  const states=roots.map(r=>r.T.toFixed(2)+' K '+(zh?(r.stable?'局部稳定':'不稳定'):(r.stable?'locally stable':'unstable'))).join(zh?'；':'; ');
  f('result').textContent=(zh?'稳态：':'Steady states: ')+states+'. '+(zh?'初始浓度 '+C0.toFixed(2)+' mol/L、温度 '+T0.toFixed(0)+' K；20 min 后温度 '+T.toFixed(2)+' K、浓度 '+C.toFixed(4)+' mol/L。计算轨迹中的最高温度约 '+peak.toFixed(2)+' K。温度轴随当前轨迹调整；负移热表示外部在供热。':'Starting from '+C0.toFixed(2)+' mol/L and '+T0.toFixed(0)+' K, at 20 min the temperature is '+T.toFixed(2)+' K and concentration '+C.toFixed(4)+' mol/L. The calculated peak is about '+peak.toFixed(2)+' K. The temperature axis adapts to the trajectory; negative removal means external heat input.');
  root.dataset.states=JSON.stringify(roots);root.dataset.peak=String(peak);root.dataset.finalTemperature=String(T);root.dataset.finalConcentration=String(C);root.dataset.steps=String(steps);
 }
 root.querySelectorAll('input').forEach(e=>e.addEventListener('input',draw));root.querySelector('[data-reset]').addEventListener('click',()=>{f('coolant').value=300;f('initialT').value=320;f('initialC').value=1;draw();});draw();
});

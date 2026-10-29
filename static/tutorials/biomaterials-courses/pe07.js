

document.querySelectorAll('[data-lab^="PE07-"]').forEach(root=>{
 const z=root.closest('[data-lang]').dataset.lang==='zh',which=root.dataset.lab,pick=n=>root.querySelector('[data-field="'+n+'"]'),f=(v,n=2)=>Number(v).toFixed(n),esc=s=>String(s).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
 const text=(x,y,s,size=22,color='#17313b',anchor='start')=>`<text x="${x}" y="${y}" font-size="${size}" fill="${color}" text-anchor="${anchor}">${esc(s)}</text>`;
 const line=(x,y,u,v,c='#d6e0df',width=1)=>`<line x1="${x}" y1="${y}" x2="${u}" y2="${v}" stroke="${c}" stroke-width="${width}"/>`;
 const path=(pts,c)=>`<path d="${pts.map((p,i)=>(i?'L':'M')+p.map(v=>v.toFixed(3)).join(',')).join(' ')}" stroke="${c}" stroke-width="4" fill="none"/>`;
 const dot=(x,y,c)=>`<circle cx="${x}" cy="${y}" r="7" fill="${c}" stroke="#fff" stroke-width="2"/>`;
 function bulk(factor,transfer){const I=.01*factor,cR=Math.sqrt(.6*1e-5*I/1e7),Rp=500*5*cR,Ri=2*.6*1e-5*I,nu=Rp/Ri,dp=1/(1/(2*nu)+transfer);return{factor,transfer,I,cR,Rp,Ri,nu,dp};}
 function occupation(a,b,t){const eq=a/(2*a+b),p=eq*(1-Math.exp(-(2*a+b)*t)),rate=500*5*p*1e17/6.02214076e23;return{a,b,t,eq,p,empty:1-p,rate};}
 function drawBulk(){const v=bulk(+pick('initiator').value,+pick('transfer').value);root.dataset.values=JSON.stringify(v);pick('initiator-value').textContent=f(v.factor)+' ×';pick('transfer-value').textContent=f(v.transfer,4);let s=text(30,35,z?'引发更多活性链，怎样改变速率与链长？':'More initiated chains: rate and molecular length',23);const xx=a=>95+(a-.25)/3.75*540;
 for(const panel of [{top:105,base:355,max:4,label:z?'单体消耗速率 / 10⁻⁴ mol L⁻¹ s⁻¹':'Monomer consumption / 10⁻⁴ mol L⁻¹ s⁻¹',key:'Rp',scale:1e4,color:'#bc592c',ticks:[0,1,2,3,4]},{top:500,base:750,max:6500,label:z?'数均聚合度 / 单体单元数':'Number-average degree of polymerization',key:'dp',scale:1,color:'#087b83',ticks:[0,2000,4000,6000]}]){
  s+=text(30,panel.top-27,panel.label,21);const yy=y=>panel.base-y/panel.max*250;
  panel.ticks.forEach(n=>{s+=line(95,yy(n),635,yy(n))+text(80,yy(n)+7,n,20,'#627780','end')});
  [1,2,3,4].forEach(n=>{s+=line(xx(n),panel.top,xx(n),panel.base)+text(xx(n),panel.base+32,n,20,'#627780','middle')});
  s+=path(Array.from({length:121},(_,i)=>{const a=.25+3.75*i/120;return[xx(a),yy(bulk(a,v.transfer)[panel.key]*panel.scale)]}),panel.color)+line(xx(v.factor),panel.top,xx(v.factor),panel.base,'#627780',2)+dot(xx(v.factor),yy(v[panel.key]*panel.scale),panel.color);
 }
 s+=text(635,815,z?'引发剂浓度相对于初值的倍数':'Initiator concentration relative to reference',21,'#627780','end');pick('plot').innerHTML=s;
 pick('result').textContent=z?`引发剂浓度 ${f(v.I,4)} mol/L，活性链浓度 ${v.cR.toExponential(3)} mol/L。单体消耗速率 ${f(v.Rp*1e4,3)} ×10⁻⁴ mol/(L·s)，动力学链长 ${f(v.nu,1)}，最终理想数均聚合度 ${f(v.dp,1)}。引发剂改变速率与终止机会；此处可快速重新引发的转移项改变分子数，保持自由基总量的稳态关系。`:`Initiator concentration is ${f(v.I,4)} mol/L and active-chain concentration ${v.cR.toExponential(3)} mol/L. Monomer consumption is ${f(v.Rp*1e4,3)} ×10⁻⁴ mol/(L·s), kinetic chain length ${f(v.nu,1)} and ideal number-average degree of polymerization ${f(v.dp,1)}. Initiator changes rate and termination opportunities. Transfer followed by rapid reinitiation changes molecular count while preserving the steady radical balance used here.`;
 }
 function drawOccupation(){const v=occupation(+pick('entry').value,+pick('exit').value,+pick('time').value);root.dataset.values=JSON.stringify(v);pick('entry-value').textContent=f(v.a)+' s⁻¹';pick('exit-value').textContent=f(v.b)+' s⁻¹';pick('time-value').textContent=f(v.t,0)+' s';let s=text(30,38,z?'粒子在两种活性状态之间如何分配？':'How particles populate two activity states',23),xx=t=>90+t/60*550,yy=p=>390-p*270;
 for(let p=0;p<=1.001;p+=.25)s+=line(90,yy(p),640,yy(p))+text(75,yy(p)+7,f(p,2),20,'#627780','end');for(let t=0;t<=60;t+=10)s+=line(xx(t),120,xx(t),390)+text(xx(t),425,t,20,'#627780','middle');s+=text(30,88,z?'粒子比例':'Particle fraction',21)+text(640,467,z?'时间 / s':'Time / s',21,'#627780','end');
 const occupied=Array.from({length:121},(_,i)=>[xx(i/2),yy(occupation(v.a,v.b,i/2).p)]),empty=Array.from({length:121},(_,i)=>[xx(i/2),yy(occupation(v.a,v.b,i/2).empty)]);s+=path(empty,'#627780')+path(occupied,'#087b83')+line(xx(v.t),120,xx(v.t),390,'#bc592c',2)+dot(xx(v.t),yy(v.p),'#087b83')+dot(xx(v.t),yy(v.empty),'#627780');
 s+=line(35,515,75,515,'#087b83',4)+text(90,522,z?'一个活性自由基':'One active radical',22)+line(35,563,75,563,'#627780',4)+text(90,570,z?'没有活性自由基':'No active radical',22);
 s+=text(35,635,(z?'观察时刻的平均活性数 ':'Mean activity at the selected time: ')+f(v.p,4),22,'#087b83');s+=text(35,684,(z?'长期平均活性数 ':'Stationary mean activity: ')+f(v.eq,4),22,'#627780');pick('plot').innerHTML=s;
 pick('result').textContent=z?`${f(v.t,0)} s 时，约 ${f(v.p*100,2)}% 的粒子含一个活性自由基，其余 ${f(v.empty*100,2)}% 不含活性自由基；每个粒子仍可含许多已停止增长的聚合物链。按给定粒子数与粒内单体浓度，此时增长速率约 ${f(v.rate*1e4,3)} ×10⁻⁴ mol/(L·s)。长期平均值为 ${f(v.eq,4)}，由进入与离开的竞争决定。`:`At ${f(v.t,0)} s, approximately ${f(v.p*100,2)}% of particles contain one active radical and ${f(v.empty*100,2)}% contain none. Each particle can still hold many inactive polymer chains. At the stated particle count and internal monomer concentration, the current propagation rate is approximately ${f(v.rate*1e4,3)} ×10⁻⁴ mol/(L·s). The stationary mean of ${f(v.eq,4)} follows from competing entry and exit.`;
 }
 const first=which==='PE07-I1',fields=first?['initiator','transfer']:['entry','exit','time'],draw=first?drawBulk:drawOccupation;fields.forEach(n=>pick(n).addEventListener('input',draw));root.querySelector('[data-reset]').addEventListener('click',()=>{const values=first?[1,.001]:[.1,0,20];fields.forEach((n,i)=>pick(n).value=values[i]);draw()});draw();
});

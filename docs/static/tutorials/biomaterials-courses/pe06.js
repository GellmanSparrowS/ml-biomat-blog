document.querySelectorAll('[data-lab="PE06-I1"]').forEach(root=>{
const z=root.closest('[data-lang]').dataset.lang==='zh',pick=n=>root.querySelector('[data-field="'+n+'"]');
const f=(v,n=2)=>Number(v).toFixed(n),esc=s=>String(s).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
function calculate(X,S){const E=1000/28,A=E/X,W=A*S,Aout=A-E,nin=A+W,nout=nin+E,qr=E*150000/3600,qs=A*(115+40*S)*200/3600,Q=qr+qs,q=(nin+nout)/2/3600*8.314*900/200,V=q*.3,area=Q/75,d=4*V/area,L=area/(Math.PI*d);return{X,S,E,A,W,Aout,nin,nout,qr,qs,Q,q,V,area,d,L};}
const text=(x,y,s,size=22,c='#17313b',anchor='start')=>`<text x="${x}" y="${y}" font-size="${size}" fill="${c}" text-anchor="${anchor}">${esc(s)}</text>`;
function draw(){const v=calculate(+pick('conversion').value,+pick('steam').value);root.dataset.values=JSON.stringify(v);pick('conversion-value').textContent=f(v.X*100,0)+'%';pick('steam-value').textContent=f(v.S,2);let s=text(25,38,z?'同一乙烯产量下，出口有哪些气体？':'Outlet gas at a fixed ethylene output',23);s+=text(25,77,z?'摩尔流量 / kmol h⁻¹':'Molar flow / kmol h⁻¹',21,'#627780');const x0=200,w=430;
for(let n=0;n<=750;n+=150){const x=x0+n/750*w;s+=`<line x1="${x}" y1="100" x2="${x}" y2="392" stroke="#d6e0df"/>`+text(x,420,n,20,'#627780','middle');}
const rows=[[z?'未反应乙烷':'Unreacted ethane',v.Aout,'#627780'],[z?'乙烯产品':'Ethylene',v.E,'#087b83'],[z?'氢气':'Hydrogen',v.E,'#bc592c'],[z?'水蒸气':'Steam',v.W,'#528eae']];
rows.forEach((r,i)=>{const y=115+i*70;s+=text(25,y+24,r[0],20)+`<rect x="${x0}" y="${y}" width="${r[1]/750*w}" height="34" rx="4" fill="${r[2]}"/>`+text(680,y+23,f(r[1],1),20,'#17313b','end');});
s+=text(25,485,z?'反应吸热保持不变，升温负荷随进料改变':'Reaction heat stays fixed; feed heating changes',22);
s+=`<rect x="75" y="540" width="${v.qr/5000*550}" height="50" fill="#bc592c"/><rect x="${75+v.qr/5000*550}" y="540" width="${v.qs/5000*550}" height="50" fill="#087b83"/>`;
for(let n=0;n<=5;n++)s+=text(75+n*110,625,String(n),21,'#627780','middle');s+=text(650,662,'MW',21,'#627780','end');
s+=`<rect x="35" y="696" width="19" height="19" fill="#bc592c"/>`+text(66,713,(z?'反应吸热 ':'Reaction ')+f(v.qr/1000,3)+' MW',21);
s+=`<rect x="35" y="742" width="19" height="19" fill="#087b83"/>`+text(66,759,(z?'进料升温 ':'Feed heating ')+f(v.qs/1000,3)+' MW',21);
s+=text(35,813,(z?'总热负荷 ':'Total duty ')+f(v.Q/1000,3)+' MW',24,'#087b83');pick('plot').innerHTML=s;
pick('result').textContent=z?`乙烯产量固定为 1000 kg/h。乙烷进入反应段 ${f(v.A)} kmol/h，其中 ${f(v.Aout)} kmol/h 未反应；蒸汽为 ${f(v.W)} kmol/h。按 900 K、200 kPa 与中点摩尔流量估算，气体体积流量为 ${f(v.q,3)} m³/s，0.30 s 对应体积 ${f(v.V,3)} m³。所需换热面积约 ${f(v.area)} m²；单管几何估算给出内径 ${f(v.d*1000,1)} mm、长度 ${f(v.L,1)} m。转化率降低或蒸汽增加，会扩大加热与流动负担；这里保持目标反应选择性为 100%，未把转化率当作动力学计算结果。`:`Ethylene output stays at 1000 kg/h. Ethane enters the reaction section at ${f(v.A)} kmol/h, of which ${f(v.Aout)} kmol/h remains unreacted; steam flow is ${f(v.W)} kmol/h. At 900 K and 200 kPa with midpoint molar flow, gas volume flow is ${f(v.q,3)} m³/s, giving ${f(v.V,3)} m³ for 0.30 s. Heat-transfer area is approximately ${f(v.area)} m²; the single-tube estimate gives an internal diameter of ${f(v.d*1000,1)} mm and a length of ${f(v.L,1)} m. Lower conversion or more steam increases heating and flow demands. Selectivity is fixed at 100%, and conversion is a specified input to this balance.`;
}
['conversion','steam'].forEach(n=>pick(n).addEventListener('input',draw));root.querySelector('[data-reset]').addEventListener('click',()=>{pick('conversion').value=.3;pick('steam').value=1.5;draw();});draw();
});

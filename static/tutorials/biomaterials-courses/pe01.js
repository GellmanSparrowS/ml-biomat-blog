document.querySelectorAll('[data-lab="PE01-I1"]').forEach(root=>{
const zh=root.closest('[data-lang]').dataset.lang==='zh';const field=n=>root.querySelector('[data-field="'+n+'"]');
function q(fo){if(fo<=0)return 1;let total=0;for(let j=0;j<100;j++){const k=2*j+1;total+=Math.exp(-k*k*Math.PI*Math.PI*fo/4)/(k*k)}return Math.min(1,8/Math.PI**2*total)}
function crossing(target){let lo=0,hi=4;for(let k=0;k<55;k++){const mid=(lo+hi)/2;if(q(mid)>target)lo=mid;else hi=mid}return (lo+hi)/2}
const at10=crossing(.1);const fmt=x=>x>=100?x.toFixed(0):x.toFixed(2);
function draw(){const L=Number(field('L').value)*1e-3,D=10**Number(field('D').value),hours=Number(field('t').value),scale=L*L/D;
field('Lout').textContent=(L*1000).toFixed(2)+' mm';field('Dout').textContent=D.toExponential(2)+' m²/s';field('tout').textContent=hours.toFixed(1)+' h';
const remaining=q(hours*3600/scale),t10=at10*scale/3600;
field('remaining').textContent=(remaining*100).toFixed(1)+'%';field('t10').textContent=fmt(t10)+' h';field('result').textContent=zh?'在所选时刻，超过表面平衡值的水分还剩 '+(remaining*100).toFixed(1)+'%。达到10%约需 '+fmt(t10)+' 小时。':'At the selected time, '+(remaining*100).toFixed(1)+'% of the moisture above surface equilibrium remains. Reaching 10% takes about '+fmt(t10)+' hours.';
const points=Array.from({length:241},(_,i)=>{const h=i/10;return (75+h/24*475).toFixed(2)+','+(345-q(h*3600/scale)*255).toFixed(2)}).join(' ');
let s='<rect width="600" height="450" fill="#f6f3ed"/><text x="35" y="35" font-size="23" fill="#19383f">'+(zh?'平均剩余比例 / %':'Average remaining fraction / %')+'</text>';
for(let y=0;y<=100;y+=25){const p=345-y/100*255;s+='<line x1="75" y1="'+p+'" x2="550" y2="'+p+'" stroke="#ccd6d2"/><text x="62" y="'+(p+7)+'" text-anchor="end" font-size="20" fill="#19383f">'+y+'</text>'}
for(let h=0;h<=24;h+=6){const x=75+h/24*475;s+='<text x="'+x+'" y="382" text-anchor="middle" font-size="21" fill="#19383f">'+h+'</text>'}
s+='<polyline points="'+points+'" fill="none" stroke="#087d80" stroke-width="4"/><line x1="75" y1="319.5" x2="550" y2="319.5" stroke="#b85b31" stroke-dasharray="7 5"/><circle cx="'+(75+hours/24*475)+'" cy="'+(345-remaining*255)+'" r="7" fill="#b85b31"/><text x="320" y="425" text-anchor="middle" font-size="23" fill="#19383f">'+(zh?'干燥时间 / h':'Drying time / h')+'</text>';
field('plot').innerHTML=s;root.dataset.remaining=String(remaining);root.dataset.hoursTo10=String(t10)}
root.querySelectorAll('input').forEach(e=>e.addEventListener('input',draw));root.querySelector('[data-reset]').addEventListener('click',()=>{field('L').value=.5;field('D').value=-11;field('t').value=2;draw()});draw();
});


document.querySelectorAll('[data-lab="PE01-I2"]').forEach(root=>{
const zh=root.closest('[data-lang]').dataset.lang==='zh';const f=n=>root.querySelector('[data-field="'+n+'"]');
function draw(){const radius=Number(f('radius').value)*1e-6,dp=Number(f('pressure').value)*1000,gamma=Number(f('tension').value)/1000,eta=10**Number(f('viscosity').value),critical=2*gamma/dp,velocity=(dp*radius-2*gamma)/(4*eta),growth=velocity>1e-12,shrink=velocity< -1e-12;
f('rout').textContent=(radius*1e6).toFixed(0)+' μm';f('pout').textContent=(dp/1000).toFixed(1)+' kPa';f('gout').textContent=(gamma*1000).toFixed(0)+' mN/m';f('eout').textContent=eta.toFixed(0)+' Pa·s';
f('rate').textContent=(velocity*1e6).toPrecision(3)+' μm/s';f('critical').textContent=(critical*1e6).toPrecision(3)+' μm';
f('result').textContent=zh?'当前状态下，半径变化率为 '+(velocity*1e6).toPrecision(3)+' μm/s，气泡'+(growth?'趋于增长':shrink?'趋于收缩':'恰处于静态门槛')+'。临界半径约为 '+(critical*1e6).toPrecision(3)+' μm。':'At the current state, the radius changes at '+(velocity*1e6).toPrecision(3)+' μm/s: '+(growth?'the bubble tends to grow':shrink?'the bubble tends to shrink':'the bubble is at the static threshold')+'. The critical radius is approximately '+(critical*1e6).toPrecision(3)+' μm.';
const R=25+radius*1e6*1.05,cx=180,cy=200,color=growth?'#087d80':shrink?'#b85b31':'#627780';
let s='<rect width="600" height="400" fill="#f6f3ed"/><text x="30" y="37" font-size="24" fill="#19383f">'+(zh?'球泡的当前力学状态':'Current mechanical state of the bubble')+'</text><circle cx="180" cy="200" r="155" fill="#d7e8e5"/><circle cx="180" cy="200" r="'+R+'" fill="white" stroke="'+color+'" stroke-width="4"/><line x1="180" y1="200" x2="'+(180+R)+'" y2="200" stroke="#19383f" stroke-width="3"/><text x="'+(180+R/2)+'" y="188" font-size="24" text-anchor="middle" fill="#19383f">R</text>';
if(growth||shrink){const a=growth?cx+R+10:cx+R+45,b=growth?cx+R+45:cx+R+10;s+='<line x1="'+a+'" y1="235" x2="'+b+'" y2="235" stroke="'+color+'" stroke-width="4"/><path d="M '+(b+(growth?-10:10))+' 227 L '+b+' 235 L '+(b+(growth?-10:10))+' 243" fill="none" stroke="'+color+'" stroke-width="3"/>';}
s+='<text x="365" y="140" font-size="23" fill="#19383f">'+(zh?'半径变化率':'Radius-change rate')+'</text><text x="365" y="181" font-size="24" fill="'+color+'">'+(velocity*1e6).toPrecision(3)+' μm/s</text><text x="365" y="247" font-size="23" fill="#19383f">'+(zh?'临界半径':'Critical radius')+'</text><text x="365" y="288" font-size="24" fill="#19383f">'+(critical*1e6).toPrecision(3)+' μm</text><text x="300" y="375" font-size="21" text-anchor="middle" fill="#19383f">'+(zh?'黏度改变速度，压力与张力决定门槛':'Viscosity changes rate; pressure and tension set the threshold')+'</text>';
f('plot').innerHTML=s;root.dataset.velocity=String(velocity);root.dataset.critical=String(critical)}
root.querySelectorAll('input').forEach(e=>e.addEventListener('input',draw));root.querySelector('[data-reset]').addEventListener('click',()=>{f('radius').value=10;f('pressure').value=10;f('tension').value=30;f('viscosity').value=3;draw()});draw();
});

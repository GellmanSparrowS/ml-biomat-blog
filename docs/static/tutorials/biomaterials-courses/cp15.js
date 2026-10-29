document.querySelectorAll('[data-lab="CP15-I1"]').forEach(root=>{
const z=root.dataset.lang==='zh',f=k=>root.querySelector('[data-field="'+k+'"]');
const txt=(x,y,s,size=22)=>'<text x="'+x+'" y="'+y+'" font-size="'+size+'">'+s+'</text>';
const line=(x,y,X,Y,c='#8ba1a3')=>'<line x1="'+x+'" y1="'+y+'" x2="'+X+'" y2="'+Y+'" stroke="'+c+'" stroke-width="2"/>';
const path=(p,c,w=3)=>'<path d="'+p.map((v,i)=>(i?'L':'M')+v[0].toFixed(2)+','+v[1].toFixed(2)).join(' ')+'" fill="none" stroke="'+c+'" stroke-width="'+w+'"/>';
function draw(){let r=+f('rate').value,x0=+f('initial').value,n=+f('step').value,a=[x0],b=[x0+.000001];for(let i=0;i<81;i++){a.push(r*a[i]*(1-a[i]));b.push(r*b[i]*(1-b[i]));}f('rv').textContent=r.toFixed(3);f('iv').textContent=x0.toFixed(2);f('nv').textContent=n;
let sum=0,singular=false;for(let i=0;i<n;i++){let d=Math.abs(r*(1-2*a[i]));if(d===0)singular=true;else sum+=Math.log(d);}let s='<g font-family="Arial,sans-serif" fill="#173e45">'+txt(30,38,z?'同一规则，两条近邻轨迹':'One rule, two nearby trajectories',24);let X=i=>65+i*6,Y=v=>325-220*v;
s+=line(65,325,555,325)+line(65,325,65,100)+txt(20,80,'x')+txt(515,390,'n');for(let i of [0,20,40,60,80])s+=txt(X(i)-8,360,''+i,21);for(let v of [0,.5,1])s+=txt(15,Y(v)+7,''+v,21);s+=path(a.slice(0,81).map((v,i)=>[X(i),Y(v)]),'#207d80')+path(b.slice(0,81).map((v,i)=>[X(i),Y(v)]),'#bb6a38',2)+line(X(n),100,X(n),325,'#667c85');s+='<circle cx="'+X(n)+'" cy="'+Y(a[n])+'" r="6" fill="#207d80"/><circle cx="'+X(n)+'" cy="'+Y(b[n])+'" r="5" fill="#bb6a38"/>';
let U=v=>95+390*v,V=v=>825-390*v;s+=txt(30,410,z?'返回图：xₙ 与 xₙ₊₁':'Return plot: xₙ and xₙ₊₁',24)+line(95,825,495,825)+line(95,825,95,430)+txt(495,870,'xₙ')+txt(120,465,'xₙ₊₁',21)+line(95,825,485,435,'#a9b7b6')+path(Array.from({length:161},(_,i)=>{let x=i/160;return[U(x),V(r*x*(1-x))];}),'#207d80',3);for(let i=0;i<=n;i++)s+='<circle cx="'+U(a[i])+'" cy="'+V(a[i+1])+'" r="'+(i===n?6:2.5)+'" fill="'+(i===n?'#bb6a38':'#527e85')+'"/>';for(let v of [0,.5,1])s+=txt(U(v)-8,860,''+v,21)+txt(45,V(v)+7,''+v,21);s+='</g>';f('plot').innerHTML=s;
let distance=Math.abs(a[n]-b[n]),text=z?'第 '+n+' 步：x='+a[n].toFixed(8)+'，近邻='+b[n].toFixed(8)+'，差值='+distance.toExponential(3)+'。':'Step '+n+': x='+a[n].toFixed(8)+', neighbor='+b[n].toFixed(8)+', separation='+distance.toExponential(3)+'. ';
if(n===0)text+=z?'尚未更新，有限步指数未定义。':'No update yet; the finite-step exponent is undefined.';
else if(singular)text+=z?'轨迹经过零导数，线性对数和为−∞；需考虑高阶误差。':'A zero derivative occurs: the linear logarithmic sum is −∞; higher-order errors matter.';
else text+=z?'前 '+n+' 步平均对数放大率='+ (sum/n).toFixed(5)+' 每步，包含暂态。':'Mean logarithmic growth over '+n+' updates='+ (sum/n).toFixed(5)+' per step, including transients.';
if(r===4&&x0===.5)text+=z?'该精确初值进入1→0→0的特殊轨道。':'This exact initial state enters the exceptional 1→0→0 orbit.';f('feedback').textContent=text;}
['rate','initial','step'].forEach(k=>f(k).addEventListener('input',draw));draw();
});

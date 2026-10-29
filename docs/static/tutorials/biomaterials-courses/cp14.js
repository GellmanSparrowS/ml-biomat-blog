document.querySelectorAll('[data-lab="CP14-I1"]').forEach(root=>{
const z=root.dataset.lang==='zh',f=k=>root.querySelector('[data-field="'+k+'"]');
const txt=(x,y,s,size=22)=>'<text x="'+x+'" y="'+y+'" font-size="'+size+'">'+s+'</text>';
const line=(x,y,X,Y,c='#8ba1a3')=>'<line x1="'+x+'" y1="'+y+'" x2="'+X+'" y2="'+Y+'" stroke="'+c+'" stroke-width="2"/>';
const path=(pts,c,w=4)=>'<path d="'+pts.map((p,i)=>(i?'L':'M')+p[0].toFixed(2)+','+p[1].toFixed(2)).join(' ')+'" fill="none" stroke="'+c+'" stroke-width="'+w+'"/>';
function draw(){const a=+f('curvature').value,k=+f('kappa').value,n=+f('mode').value,t=+f('time').value,q=2*Math.PI*n/20,w=-q*q*(a+k*q*q),amp=.005*Math.exp(w*t),unstable=a<0,qstar=unstable?Math.sqrt(-a/(2*k)):0;
f('av').textContent=a.toFixed(1);f('kv').textContent=k.toFixed(1);f('nv').textContent=n;f('tv').textContent=t.toFixed(2);
let best=1,bw=-Infinity;for(let j=1;j<=6;j++){let Q=2*Math.PI*j/20,W=-Q*Q*(a+k*Q*Q);if(W>bw){best=j;bw=W;}}
const X=Q=>65+Q*245,Y=W=>325-(W+1)*100,id='CP14-I1-'+(z?'zh':'en')+'-clip';let s='<defs><clipPath id="'+id+'"><rect x="65" y="95" width="490" height="230"/></clipPath></defs><g font-family="Arial,sans-serif" fill="#173e45">';
s+=txt(30,38,z?'早期增长率谱':'Early growth-rate spectrum',25)+line(65,95,65,325)+line(65,Y(0),555,Y(0))+txt(22,100,'ω')+txt(525,380,'q');
[-1,0,1].forEach(v=>{s+=txt(14,Y(v)+7,v.toFixed(0),21);});[0,1,2].forEach(v=>{s+=txt(X(v)-7,355,''+v,21);});
s+='<g clip-path="url(#'+id+')">';if(unstable)s+='<rect x="65" y="95" width="'+(Math.sqrt(-a/k)*245)+'" height="230" fill="#dcebe4"/>';
s+=line(65,Y(0),555,Y(0))+path(Array.from({length:241},(_,i)=>{const Q=2*i/240;return[X(Q),Y(-Q*Q*(a+k*Q*Q))];}),'#207d80');
if(unstable)s+=line(X(qstar),95,X(qstar),325,'#ba793e');s+='<circle cx="'+X(q)+'" cy="'+Y(w)+'" r="7" fill="#bf653a"/></g>';
s+=txt(30,405,z?'所选波：初始与当前':'Selected wave: initial and current',24)+line(65,480,65,710)+line(65,595,555,595)+txt(22,465,'φ')+txt(525,783,'x');
const XX=x=>65+x*24.5,YY=v=>595-(v-.5)*2000;[.45,.5,.55].forEach(v=>s+=txt(5,YY(v)+7,v.toFixed(2),21));[0,10,20].forEach(v=>s+=txt(XX(v)-8,745,''+v,21));
s+=path(Array.from({length:241},(_,i)=>{let x=20*i/240;return[XX(x),YY(.5+.005*Math.cos(q*x))];}),'#9ba9a8',3)+path(Array.from({length:241},(_,i)=>{let x=20*i/240;return[XX(x),YY(.5+amp*Math.cos(q*x))];}),'#207d80',4)+'</g>';f('plot').innerHTML=s;
let info=z?'所选 q='+q.toFixed(3)+'，增长率 ω='+w.toFixed(4)+'；幅度 '+amp.toFixed(6)+'，平均组成保持0.5。':'Selected q='+q.toFixed(3)+', growth rate ω='+w.toFixed(4)+'; amplitude '+amp.toFixed(6)+', with mean composition fixed at 0.5. ';
if(unstable){info+=z?'连续模型 q*='+qstar.toFixed(3)+'，最快波长 '+(2*Math.PI/qstar).toFixed(3)+'。允许模式中 n='+best+' 的增长率最高'+(bw>0?'，波长 '+(20/best).toFixed(3)+'。':'，但全部允许模式均衰减。'):'Continuum q*='+qstar.toFixed(3)+', fastest wavelength '+(2*Math.PI/qstar).toFixed(3)+'. Allowed mode n='+best+' has the highest rate'+(bw>0?', with wavelength '+(20/best).toFixed(3)+'.':', but all allowed modes decay.');}
else info+=z?'曲率非负，所有非零波数都衰减，没有增长的优选波长。':'Nonnegative curvature: all nonzero wavenumbers decay, with no preferred growing wavelength.';
f('feedback').textContent=info;}
['curvature','kappa','mode','time'].forEach(k=>f(k).addEventListener('input',draw));draw();
});

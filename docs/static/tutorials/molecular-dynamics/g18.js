document.querySelectorAll('[data-lab="G18-I1"]').forEach(root=>{
if(root.dataset.ready)return;root.dataset.ready='1';
const q=s=>root.querySelector('[data-'+s+']'),n=q('n'),nu=q('nu'),mode=q('mode'),chart=q('chart'),zh=root.dataset.lang==='zh';
const create=(name,attrs,text)=>{const el=document.createElementNS('http://www.w3.org/2000/svg',name);Object.entries(attrs).forEach(([k,v])=>el.setAttribute(k,v));if(text!==undefined)el.textContent=text;chart.append(el);return el;};
function render(){const N=Number(n.value),v=Number(nu.value),a=mode.value==='half'?.5:mode.value==='one'?1:0,D=.5*Math.pow(N/8,v),Q=D/Math.pow(N,a);q('n-value').textContent=N;q('nu-value').textContent=v.toFixed(2);chart.replaceChildren();
const data=Array.from({length:121},(_,i)=>{const k=i+8;return[k,.5*Math.pow(k/8,v)/Math.pow(k,a)];}),top=Math.max(...data.map(p=>p[1]))*1.12,scale=Math.pow(10,Math.floor(Math.log10(top))),maxY=Math.ceil(top/scale)*scale,x=k=>90+(k-8)/120*735,y=d=>350-d/maxY*285;
create('rect',{x:0,y:0,width:900,height:450,fill:'#f8f7f2'});create('line',{x1:90,y1:350,x2:825,y2:350,stroke:'#163840','stroke-width':2});create('line',{x1:90,y1:350,x2:90,y2:55,stroke:'#163840','stroke-width':2});
for(const k of [8,32,64,96,128]){create('line',{x1:x(k),y1:350,x2:x(k),y2:357,stroke:'#163840'});create('text',{x:x(k),y:385,'text-anchor':'middle','font-size':21,fill:'#163840'},k);}
for(const f of [0,.25,.5,.75,1]){const t=f*maxY;create('text',{x:78,y:y(t)+6,'text-anchor':'end','font-size':18,fill:'#163840'},t.toFixed(t<.1?3:2));}
create('text',{x:90,y:30,'font-size':22,fill:'#163840'},mode.value==='raw'?'D / nm':mode.value==='half'?'D / √n / nm':'D / n / nm');create('text',{x:450,y:425,'text-anchor':'middle','font-size':22,fill:'#163840'},zh?'化学重复数 n':'Chemical repeat count n');
create('polyline',{points:data.map(p=>x(p[0])+','+y(p[1])).join(' '),fill:'none',stroke:'#167d84','stroke-width':4});create('circle',{cx:x(N),cy:y(Q),r:7,fill:'#c16b3d'});
q('answer').textContent=(zh?'所选解析模型：':'Selected analytical model: ')+`n = ${N}; ν = ${v.toFixed(2)}; D = ${D.toFixed(6)} nm; Q = ${Q.toFixed(6)} nm; D/D(8) = ${(D/.5).toFixed(6)}.`;
}
n.addEventListener('input',render);nu.addEventListener('input',render);mode.addEventListener('change',render);q('reset').addEventListener('click',()=>{n.value='32';nu.value='0.5';mode.value='half';render();});render();
});
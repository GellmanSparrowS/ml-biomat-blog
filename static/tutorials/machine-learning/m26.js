(()=>{
const zh=document.documentElement.lang.startsWith('zh'),el=x=>document.getElementById('M26-'+x);
const initial={parametersM:100,replicas:4,microbatch:8,accumulation:3,method:'DDP',stage:0,parameterIndex:0};let p={...initial},result={};
const methods=['DDP','ZeRO-1','ZeRO-2','ZeRO-3'];
const names=zh?['保存训练状态','计算局部梯度','聚合梯度','更新参数','形成下一步状态']:['Store training state','Compute local gradients','Aggregate gradients','Update parameters','Prepare next-step state'];
function draw(){
 const sharding=methods.indexOf(p.method),R=p.replicas,P=p.parametersM*1e6,j=p.parameterIndex;
 const bytes=[2/(sharding===3?R:1),2/(sharding>=2?R:1),12/(sharding>=1?R:1)];
 const components=bytes.map(b=>b*P/1e9),persistentGB=components.reduce((x,y)=>x+y,0);
 const gradients=Array.from({length:R},(_,rank)=>Array.from({length:2*R},(_,index)=>(rank+1)*(index+1)/10));
 const mean=gradients[0].map((_,index)=>gradients.reduce((sum,g)=>sum+g[index],0)/R),updated=mean.map(g=>1-.1*g);
 result={...p,persistentGB,effectiveBatch:R*p.microbatch*p.accumulation,firstMeanGradient:mean[0],firstUpdatedWeight:updated[0],selectedMeanGradient:mean[j],selectedUpdatedWeight:updated[j],owner:Math.floor(j/2),componentsGB:components,localGradients:gradients,meanGradient:mean,updatedWeights:updated};
 for(const key of ['parametersM','replicas','microbatch','accumulation','method','parameterIndex'])el(key).value=p[key];
 el('parameterIndex').max=2*R-1;
 const tx=(x,y,t,color='#24384a',anchor='start',size=14)=>`<text x="${x}" y="${y}" fill="${color}" font-family="sans-serif" font-size="${size}" text-anchor="${anchor}">${t}</text>`;
 let s='<rect width="960" height="590" fill="white"/>';
 s+=tx(24,32,(zh?'阶段 ':'Stage ')+p.stage+'/4 — '+names[p.stage],'#183b52','start',20);
 s+=tx(24,65,zh?`检查参数 ${j}（0起编号），每个分片负责2个示意参数`:`Inspect parameter ${j} (zero-based); each shard owns two illustrative parameters`);
 const heads=zh?['进程','局部梯度','平均梯度','更新后权重','持久状态归属']:['Process','Local gradient','Mean gradient','Updated weight','Persistent ownership'];
 const xs=[25,155,290,435,595];heads.forEach((h,i)=>s+=tx(xs[i],103,h));
 s+='<path d="M24,116 H930" stroke="#bccbd3"/>';
 for(let rank=0;rank<R;rank++){
  const y=145+rank*30;
  if(rank===Math.floor(j/2)&&sharding>0)s+=`<rect x="20" y="${y-20}" width="915" height="28" fill="#eef4e7"/>`;
  const frac=(condition)=>condition?(zh?`本进程1/${R}`:`local 1/${R}`):(zh?'完整':'full');
  const ownership=`W: ${frac(sharding===3)} · G: ${frac(sharding>=2)} · O: ${frac(sharding>=1)}`;
  const values=[String(rank),p.stage>=1?gradients[rank][j].toFixed(3):'—',p.stage>=2?mean[j].toFixed(3):'—',p.stage>=3?updated[j].toFixed(3):'1.000',ownership];
  values.forEach((v,i)=>s+=tx(xs[i],y,v,i===2?'#256e87':'#24384a','start',i===4?12:14));
 }
 s+=tx(24,420,zh?'每设备持久状态预算 / GB（十进制）':'Persistent state per device / GB (decimal)','#183b52','start',17);
 const colors=['#266d86','#dd8b38','#8a63a2'],labels=zh?['W 参数','G 梯度','O 主权重 + Adam矩']:['W weights','G gradients','O master weights + Adam moments'];
 let x=25;const scale=870/(16*P/1e9);
 for(let i=0;i<3;i++){const w=components[i]*scale;s+=`<rect x="${x}" y="440" width="${w}" height="36" fill="${colors[i]}"/>`;if(w>45)s+=tx(x+w/2,464,components[i].toFixed(3),'white','middle',13);x+=w;}
 s+=tx(930,420,(zh?'合计 ':'Total ')+persistentGB.toFixed(3)+' GB','#183b52','end',16);
 labels.forEach((label,i)=>{s+=`<rect x="${25+i*290}" y="495" width="12" height="12" fill="${colors[i]}"/>`;s+=tx(44+i*290,506,label,'#24384a','start',13);});
 s+=tx(25,540,zh?'浅绿色行：当前参数对应的优化器分片拥有者。':'Pale green: optimizer-shard owner for the selected parameter.');
 s+=tx(25,567,zh?'预算不计激活、参数暂存和通信缓冲；表格展示数学值，归属列说明实际保存位置。':'Budget excludes activations and buffers; values illustrate arithmetic, ownership describes storage.','#526c7b','start',13);
 el('plot').innerHTML=s;
 const note=zh?`有效批次 ${result.effectiveBatch} = ${R} 副本 × ${p.microbatch} 样本 × ${p.accumulation} 次累积。参数 ${j} 的平均梯度为 ${mean[j].toFixed(3)}，学习率0.1时权重1更新为 ${updated[j].toFixed(3)}。`:`Effective batch ${result.effectiveBatch} = ${R} replicas × ${p.microbatch} examples × ${p.accumulation} accumulation steps. Parameter ${j} has mean gradient ${mean[j].toFixed(3)}; learning rate 0.1 updates weight 1 to ${updated[j].toFixed(3)}.`;
 el('status').textContent=note;el('back').disabled=p.stage===0;el('next').disabled=p.stage===4;
}
function set(values){
 for(const key of Object.keys(initial)){
  if(key==='method'){if(methods.includes(values[key]))p[key]=values[key];}
  else if(key in values&&Number.isFinite(Number(values[key])))p[key]=Number(values[key]);
 }
 p.replicas=[2,4,8].includes(p.replicas)?p.replicas:4;p.stage=Math.max(0,Math.min(4,Math.round(p.stage)));p.parametersM=Math.max(1,Math.min(1000,p.parametersM));p.microbatch=Math.max(1,Math.min(128,Math.round(p.microbatch)));p.accumulation=Math.max(1,Math.min(16,Math.round(p.accumulation)));p.parameterIndex=Math.max(0,Math.min(2*p.replicas-1,Math.round(p.parameterIndex)));draw();return result;
}
for(const key of ['parametersM','replicas','microbatch','accumulation','method','parameterIndex'])el(key).addEventListener('input',()=>set({[key]:el(key).value}));
el('back').addEventListener('click',()=>set({stage:p.stage-1}));el('next').addEventListener('click',()=>set({stage:p.stage+1}));el('reset').addEventListener('click',()=>{p={...initial};draw();});
window.CourseLab={set,state:()=>JSON.parse(JSON.stringify(result)),reset:()=>{p={...initial};draw();return result;}};draw();
})();


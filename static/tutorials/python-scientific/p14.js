(() => {
 const root=document.getElementById('P14-lab');if(!root)return;
 const zh=document.documentElement.lang.startsWith('zh'),tr=(a,b)=>zh?a:b,el=id=>root.querySelector('#P14-'+id);
 const data={A:{t:[0,1,2.5,5,6,9,15,16,19],y:[22,26,35,47,51,58,67,69,71]},B:{t:[0,2,3,5,8,9,15,17,19],y:[21,29,35,44,53,55,65,68,70]}};
 const defaults={batch:'A',width:5,offset:0,selected:0};let p={...defaults},result={};
 const text=(x,y,s,anchor='start',size=14,color='#202e39')=>`<text x="${x}" y="${y}" text-anchor="${anchor}" font-size="${size}" fill="${color}">${s}</text>`;
 function draw(){
  const d=data[p.batch],low=Math.floor((Math.min(...d.t)-p.offset)/p.width),high=Math.floor((Math.max(...d.t)-p.offset)/p.width);
  const bins=Array.from({length:high-low+1},(_,i)=>{const k=low+i,left=p.offset+k*p.width,members=d.t.map((t,j)=>({t,y:d.y[j]})).filter(r=>r.t>=left&&r.t<left+p.width);return{left,right:left+p.width,count:members.length,mean:members.length?members.reduce((s,r)=>s+r.y,0)/members.length:null,members}});
  p.selected=Math.min(p.selected,bins.length-1);const selected=bins[p.selected],xmin=bins[0].left,xmax=bins.at(-1).right;
  function chart(svg,title,ymin,ymax,unit,wide=false){
   const actualWide=wide&&root.getBoundingClientRect().width>720,L=65,T=56,W=actualWide?760:330,H=225,X=x=>L+(x-xmin)/(xmax-xmin)*W,Y=y=>T+H-(y-ymin)/(ymax-ymin)*H;
   svg.setAttribute('viewBox',`0 0 ${actualWide?860:430} 350`);
   let s=text(L,22,title,'start',17)+text(L,44,unit,'start',14,'#596b78');
   const yticks=ymin===15?[20,40,60,80]:Array.from({length:Math.floor(ymax)+1},(_,i)=>i);
   for(const yy of yticks){s+=`<line x1="${L}" x2="${L+W}" y1="${Y(yy)}" y2="${Y(yy)}" stroke="#dce3e8"/>`+text(L-8,Y(yy)+5,String(yy),'end')}
   for(let i=0;i<=4;i++){const xx=xmin+(xmax-xmin)*i/4;s+=text(X(xx),T+H+21,Number(xx.toFixed(1)).toString(),'middle')}
   s+=`<path d="M${L},${T}V${T+H}H${L+W}" fill="none" stroke="#202e39"/>`+text(L+W/2,330,tr('经过时间 / min','Elapsed time / min'),'middle',14);
   return {svg,s,X,Y,L,T,W,H};
  }
  let c=chart(el('records'),tr('每条记录进入哪个时间箱','Which bin receives each record'),15,80,tr('温度 / °C','Temperature / °C'),true);
  bins.forEach((b,i)=>{c.s+=`<rect x="${c.X(b.left)}" y="${c.T}" width="${c.X(b.right)-c.X(b.left)}" height="${c.H}" fill="${i===p.selected?'#b64a35':'#28658c'}" opacity="${i===p.selected?.1:(i%2?.04:.075)}"/>`;c.s+=`<line x1="${c.X(b.left)}" x2="${c.X(b.left)}" y1="${c.T}" y2="${c.T+c.H}" stroke="#becdd6" stroke-dasharray="3 3"/>`;b.members.forEach(r=>c.s+=`<circle cx="${c.X(r.t)}" cy="${c.Y(r.y)}" r="${i===p.selected?5.4:4.1}" fill="${i===p.selected?'#b64a35':'#28658c'}" stroke="white"/>`)});c.svg.innerHTML=c.s;
  c=chart(el('means'),tr('箱内观测均值','Means within bins'),15,80,tr('平均温度 / °C','Mean temperature / °C'));
  bins.forEach((b,i)=>{if(b.mean===null)return;const x=(b.left+b.right)/2;c.s+=`<line x1="${c.X(b.left)}" x2="${c.X(b.right)}" y1="${c.Y(b.mean)}" y2="${c.Y(b.mean)}" stroke="${i===p.selected?'#b64a35':'#28658c'}" stroke-width="2"/><circle cx="${c.X(x)}" cy="${c.Y(b.mean)}" r="4.5" fill="${i===p.selected?'#b64a35':'#28658c'}"/>`});c.svg.innerHTML=c.s;
  c=chart(el('counts'),tr('同时保留记录覆盖情况','Retain observation coverage'),0,8,tr('记录数 / 条','Observation count'));
  bins.forEach((b,i)=>{const x=(b.left+b.right)/2,w=(c.X(b.right)-c.X(b.left))*.76;c.s+=`<rect x="${c.X(x)-w/2}" y="${c.Y(b.count)}" width="${w}" height="${c.Y(0)-c.Y(b.count)}" fill="${i===p.selected?'#b64a35':'#28658c'}"/>`+text(c.X(x),c.Y(b.count)-8,String(b.count),'middle',14,b.count?'#202e39':'#b64a35')});c.svg.innerHTML=c.s;
  el('batch').value=p.batch;el('width').value=p.width;el('offset').max=p.width-1;el('offset').value=p.offset;el('offset-value').textContent=p.offset+' min';
  el('selected').innerHTML=bins.map((b,i)=>`<option value="${i}"${i===p.selected?' selected':''}>[${b.left}, ${b.right}) min</option>`).join('');
  el('members').textContent=selected.count?tr(`选中区间 [${selected.left}, ${selected.right}) min：${selected.members.map(r=>`${r.t} min → ${r.y} °C`).join('；')}。均值 ${selected.mean.toFixed(4)} °C。`,`Selected [${selected.left}, ${selected.right}) min: ${selected.members.map(r=>`${r.t} min → ${r.y} °C`).join('; ')}. Mean ${selected.mean.toFixed(4)} °C.`):tr(`选中区间 [${selected.left}, ${selected.right}) min 没有记录，均值保留为空。`,`Selected [${selected.left}, ${selected.right}) min contains no records; its mean remains missing.`);
  result={...p,n_bins:bins.length,empty_bins:bins.filter(b=>!b.count).length,total_observations:d.t.length,first_mean:bins[0].mean,first_left:bins[0].left,bins};
  el('numbers').textContent=tr(`${bins.length}个时间箱 · ${result.empty_bins}个空箱 · 原始${d.t.length}条记录 · 左闭右开`,`${bins.length} bins · ${result.empty_bins} empty bins · ${d.t.length} original observations · left endpoint included`);
 }
 function set(q={}){if(['A','B'].includes(q.batch))p.batch=q.batch;if([2,5,10].includes(+q.width))p.width=+q.width;if(Number.isFinite(+q.offset))p.offset=Math.round(+q.offset);p.offset=Math.max(0,Math.min(p.width-1,p.offset));if(Number.isFinite(+q.selected))p.selected=Math.max(0,Math.floor(+q.selected));draw();return{...result}}
 const reset=()=>{p={...defaults};draw();return{...result}};
 for(const id of ['batch','width','selected'])el(id).addEventListener('change',e=>set({[id]:id==='batch'?e.target.value:+e.target.value}));el('offset').addEventListener('input',e=>set({offset:+e.target.value}));el('reset').addEventListener('click',reset);
 let observer=null,lastWidth=0;if(typeof ResizeObserver!=='undefined'){observer=new ResizeObserver(entries=>{const width=entries[0].contentRect.width;if(Math.abs(width-lastWidth)>1){lastWidth=width;draw()}});observer.observe(root)}
 window.CourseLab={set,state:()=>JSON.parse(JSON.stringify(result)),reset,destroy:()=>observer?.disconnect()};draw();
})();

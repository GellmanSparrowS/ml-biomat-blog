(() => {
 const root=document.getElementById('P13-lab');if(!root)return;
 const zh=document.documentElement.lang.startsWith('zh'),tr=(a,b)=>zh?a:b,el=id=>root.querySelector('#P13-'+id);
 const observations=[['R01','S01',12],['R02','S01',14],['R03','S02',18],['R04','S03',21],['R05','S03',23],['R06','S04',16]];
 const samples=[['S03','A'],['S01','A'],['S05','B'],['S02','B']];
 const defaults={how:'left',duplicate:false,focus:'R04'};let p={...defaults},result={};
 const colors={S01:'#28658c',S02:'#886a29',S03:'#b64a35',S04:'#71808b',S05:'#71808b'};
 const text=(x,y,s,anchor='start',size=14,c='#202e39')=>`<text x="${x}" y="${y}" text-anchor="${anchor}" font-size="${size}" fill="${c}">${s}</text>`;
 function draw(){
  const meta=p.duplicate?[...samples,['S03','A']]:[...samples],rows=[];
  observations.forEach((o,i)=>{const match=meta.map((m,j)=>({m,j})).filter(x=>x.m[0]===o[1]);
   if(match.length)match.forEach(({m,j})=>rows.push({record:o[0],sample:o[1],y:o[2],group:m[1],status:'both',i,j}));
   else if(p.how!=='inner')rows.push({record:o[0],sample:o[1],y:o[2],group:null,status:'left_only',i,j:-1});
  });
  if(p.how==='outer')meta.forEach((m,j)=>{if(!observations.some(o=>o[1]===m[0]))rows.push({record:null,sample:m[0],y:null,group:m[1],status:'right_only',i:-1,j})});
  const A=rows.filter(r=>r.group==='A'&&r.y!==null),mean=A.reduce((s,r)=>s+r.y,0)/A.length;
  const counts={};['both','left_only','right_only'].forEach(k=>counts[k]=rows.filter(r=>r.status===k).length);
  result={...p,rows:rows.length,matched:counts.both,left_only:counts.left_only,right_only:counts.right_only,A_mean:mean,A_count:A.length,unique_observations:new Set(rows.filter(r=>r.record).map(r=>r.record)).size,contract_ok:!p.duplicate};
  let s=text(30,27,tr('测量记录 → 样品信息','Observation records → sample metadata'),'start',17);
  rows.filter(r=>r.status==='both').forEach(r=>{const focus=r.record===p.focus;s+=`<path d="M245,${66+r.i*43} C370,${66+r.i*43} 445,${82+r.j*47} 565,${82+r.j*47}" fill="none" stroke="${colors[r.sample]}" opacity="${focus?1:.24}" stroke-width="${focus?3:1.4}"/>`});
  observations.forEach((o,i)=>{const y=66+i*43,focus=o[0]===p.focus; s+=`<rect x="24" y="${y-17}" width="216" height="34" rx="2" fill="${focus?'#e8eef3':'#f5f7f8'}" stroke="${focus?colors[o[1]]:'none'}"/>`+text(34,y+5,`${o[0]} · ${o[1]} · ${o[2]} kPa`,'start',14,colors[o[1]])});
  meta.forEach((m,j)=>{const y=82+j*47;s+=`<rect x="570" y="${y-17}" width="190" height="34" rx="2" fill="#f5f7f8"/>`+text(582,y+5,`${m[0]} → ${m[1]}${j===4?tr('（重复）',' (duplicate)'):''}`,'start',14,colors[m[0]])});
  s+=text(30,333,tr('加粗线追踪选中记录；每条线生成一条匹配结果。','Bold links trace the selected record; each link generates one matched row.'),'start',12,'#596b78');el('links').innerHTML=s;
  el('output').innerHTML=rows.map(r=>`<tr${r.record===p.focus?' class="selected"':''}><td>${r.record??'—'}</td><td>${r.sample}</td><td>${r.y??'—'}</td><td>${r.group??'—'}</td><td>${r.status}</td></tr>`).join('');
  s=text(55,28,tr('结果行数与统计权重','Output size and statistical weight'),'start',16);
  const plot={left:65,top:60,width:610,height:108},X=v=>plot.left+v/10*plot.width;
  s+=text(55,48,tr('合并后的行数 / 行','Merged output / rows'),'start',12,'#596b78');let start=0;
  for(const [k,c,label]of [['both','#28658c',tr('匹配','matched')],['left_only','#b64a35',tr('仅左','left only')],['right_only','#71808b',tr('仅右','right only')]]){
   const n=counts[k];if(n){s+=`<rect x="${X(start)}" y="65" width="${X(n)-X(0)}" height="39" fill="${c}"/>`+text(X(start+n/2),90,`${n}`,'middle',14,'white');start+=n;}
  }
  for(let i=0;i<=10;i+=2)s+=text(X(i),124,String(i),'middle',12);
  s+=text(55,156,tr('蓝：匹配；红：只有测量；灰：只有样品信息','Blue: matched; red: measurements only; gray: metadata only'),'start',12,'#596b78');
  s+=text(55,191,tr('配方A均值 / kPa','Formulation A mean / kPa'),'start',13);
  for(const [j,v,name,c]of [[0,17.5,tr('原始4次测量','4 original observations'),'#71808b'],[1,mean,tr('当前结果行','Current result rows'),'#28658c']]){
   const yy=218+j*53;s+=text(55,yy+15,name,'start',12)+`<rect x="270" y="${yy}" width="${v/25*390}" height="27" fill="${c}"/>`+text(278+v/25*390,yy+18,v.toFixed(2),'start',14);
  }
  el('summary-plot').innerHTML=s;
  el('how').value=p.how;el('duplicate').checked=p.duplicate;el('focus').value=p.focus;
  el('numbers').textContent=tr(`${rows.length}条结果行 · ${result.unique_observations}条不同测量 · 配方A均值 ${mean.toFixed(2)} kPa`,`${rows.length} output rows · ${result.unique_observations} distinct observations · formulation A mean ${mean.toFixed(2)} kPa`);
  el('contract').textContent=p.duplicate?tr('S03在右表有2条记录。validate="m:1"会报告键不唯一；上方展开其配对结果，以观察重复匹配如何改变计数。','S03 has 2 metadata rows. validate="m:1" reports a nonunique key; the expanded pairing above shows how repeated matches change counts.'):tr('右表样品键唯一，validate="m:1"通过。一个样品的多次测量分别匹配同一条样品信息。','Right-table sample keys are unique, so validate="m:1" succeeds. Multiple observations of a sample each match its single metadata record.');
 }
 function set(q={}){if(['left','inner','outer'].includes(q.how))p.how=q.how;if(typeof q.duplicate==='boolean')p.duplicate=q.duplicate;if(observations.some(o=>o[0]===q.focus))p.focus=q.focus;draw();return{...result}}
 const reset=()=>{p={...defaults};draw();return{...result}};
 el('how').addEventListener('change',e=>set({how:e.target.value}));el('duplicate').addEventListener('change',e=>set({duplicate:e.target.checked}));el('focus').addEventListener('change',e=>set({focus:e.target.value}));el('reset').addEventListener('click',reset);
 window.CourseLab={set,state:()=>({...result}),reset};draw();
})();

(() => {
 const root=document.getElementById('P03-lab');if(!root)return;
 const zh=document.documentElement.lang.startsWith('zh'),tr=(a,b)=>zh?a:b,$=s=>document.getElementById('P03-'+s);
 const base=[['A01','water',1.2,4.8],['A02','water',1,3.4],['A03','water',.8,2.8],['B01','saline',1.2,3.6],['B02','saline',1,null],['B03','saline',.8,2.32]];
 let records=[],saved={},p={selected:'A01',order:'id',mismatch:false},state={};
 const t=(x,y,s,z=17,e='')=>`<text x="${x}" y="${y}" font-size="${z}" fill="#172b36" ${e}>${s}</text>`;
 const line=(x,y,X,Y,c='#c6cecb',w=1,e='')=>`<line x1="${x}" y1="${y}" x2="${X}" y2="${Y}" stroke="${c}" stroke-width="${w}" ${e}/>`;
 const uptake=r=>r.wet!==null&&r.wet>=r.dry&&r.dry>0?(r.wet-r.dry)/r.dry:null;
 const niceStep=span=>{const raw=span/5,power=10**Math.floor(Math.log10(raw));return [1,2,2.5,5,10].find(v=>v*power>=raw)*power;};
 function render(){
  const selected=records.find(r=>r.id===p.selected),order=records.slice().sort((a,b)=>p.order==='id'?a.id.localeCompare(b.id):p.order==='dry'?a.dry-b.dry:(a.wet===null?Infinity:a.wet)-(b.wet===null?Infinity:b.wet));
  const valid=records.filter(r=>uptake(r)!==null),groups={};
  ['water','saline'].forEach(b=>{const vals=valid.filter(r=>r.bath===b).map(uptake);groups[b]={count:vals.length,mean:vals.length?vals.reduce((a,b)=>a+b,0)/vals.length:null};});
  let wrong=null;if(p.mismatch&&records.slice(0,3).every(r=>r.wet!==null)){const ws=records.slice(0,3).map(r=>r.wet).sort((a,b)=>a-b);wrong=records.slice(0,3).map((r,i)=>(ws[i]-r.dry)/r.dry);}
  $('rows').innerHTML=order.map((r,i)=>`<tr${r.id===p.selected?' class="selected"':''}><td>${i}</td><th scope="row">${r.id}</th><td>${tr(r.bath==='water'?'水浴':'盐水浴',r.bath)}</td><td>${r.dry.toFixed(2)}</td><td>${r.wet===null?'None':r.wet.toFixed(2)}</td><td>${uptake(r)===null?'—':uptake(r).toFixed(4)}</td></tr>`).join('');
  const invalid=records.filter(r=>r.wet!==null&&r.wet<r.dry).map(r=>r.id);
  $('note').textContent=invalid.length?tr('检查湿质量低于干质量的记录：','Check records with wet mass below dry mass: ')+invalid.join(', '):p.mismatch&&wrong===null?tr('水浴组含缺失称量，错配对照暂不计算。','Water-bath weighings include missing values; the mismatching comparison is not calculated.'):' ';
  let g=t(20,27,tr('称量对：高亮始终追踪ID','Paired masses: highlight follows the ID'),20)+t(535,27,tr('每个样品的吸液量','Uptake of each specimen'),20);
  const wetExtent=Math.max(6,...records.map(r=>r.wet||0))*1.1,wetStep=Math.max(1,niceStep(wetExtent)),maxWet=Math.ceil(wetExtent/wetStep)*wetStep,dryStep=.5,maxDry=Math.ceil(Math.max(1.5,...records.map(r=>r.dry))*1.15/dryStep)*dryStep,X=v=>70+v/maxDry*340,Y=v=>295-v/maxWet*220;
  for(let v=0;v<=maxWet+1e-9;v+=wetStep)g+=line(70,Y(v),410,Y(v),'#e1e5df')+t(59,Y(v)+5,String(v),15,'text-anchor="end"');
  for(let u=0;u<=maxDry+1e-9;u+=dryStep)g+=t(X(u),320,u.toFixed(1),15,'text-anchor="middle"');
  g+=line(70,75,70,295,'#172b36')+line(70,295,410,295,'#172b36')+t(18,55,tr('湿质量 / g','Wet mass / g'),16)+t(240,350,tr('干质量 / g','Dry mass / g'),17,'text-anchor="middle"');
  for(const r of records){if(r.wet===null)continue;const color=r.bath==='water'?'#28648a':'#b85336';g+=`<circle cx="${X(r.dry)}" cy="${Y(r.wet)}" r="6" fill="${color}"/>`+t(X(r.dry)+10,Y(r.wet)-7,r.id,15);if(r.id===p.selected)g+=`<circle cx="${X(r.dry)}" cy="${Y(r.wet)}" r="12" fill="none" stroke="#ad7a1a" stroke-width="3"/>`;}
  const values=valid.map(uptake).concat(wrong||[]),lo=Math.min(0,...values),hi=Math.max(4,...values)*1.12,qStep=Math.max(1,niceStep(hi-lo)),minQ=Math.floor(lo/qStep)*qStep,maxQ=Math.ceil(hi/qStep)*qStep,Q=v=>615+(v-minQ)/(maxQ-minQ)*275;
  for(let v=minQ;v<=maxQ+1e-9;v+=qStep)g+=line(Q(v),61,Q(v),305,'#e1e5df')+t(Q(v),328,String(v),15,'text-anchor="middle"');
  order.forEach((r,i)=>{const y=80+i*39,q=uptake(r),color=r.bath==='water'?'#28648a':'#b85336';g+=t(598,y+5,r.id,17,`text-anchor="end" ${r.id===p.selected?'font-weight="bold"':''}`);if(q!==null){g+=line(Q(0),y,Q(q),y,color,2)+`<circle cx="${Q(q)}" cy="${y}" r="6" fill="${color}"/>`;if(r.id===p.selected)g+=`<circle cx="${Q(q)}" cy="${y}" r="11" fill="none" stroke="#ad7a1a" stroke-width="2.5"/>`;}else g+=t(Q(0)+7,y+5,r.wet===null?'None':tr('检查','Check'),15);if(wrong&&r.bath==='water'){const v=wrong[records.findIndex(x=>x.id===r.id)];g+=line(Q(v)-5,y-5,Q(v)+5,y+5,'#8b3f8f',2)+line(Q(v)-5,y+5,Q(v)+5,y-5,'#8b3f8f',2);}});
  g+=t(750,358,tr('吸液量 / g·g⁻¹','Uptake / g·g⁻¹'),17,'text-anchor="middle"')+t(535,390,tr('紫色×：故意单独排序湿质量的结果','Purple ×: wet masses deliberately sorted separately'),15);
  $('plot').innerHTML=g;
  const q=uptake(selected),show=x=>x===null?'None':x.toFixed(6);
  $('result').textContent=`${tr('选择','Selected')}: ${p.selected} | records[${order.findIndex(r=>r.id===p.selected)}]\n${tr('按ID查找的湿质量','Wet mass found by ID')}: ${selected.wet===null?'None':selected.wet.toFixed(2)+' g'}\n${tr('吸液量','Uptake')}: ${show(q)} g/g\n${tr('有效数 / 总数','Valid / total')}: ${valid.length} / 6\n${tr('水浴均值','Water mean')}: ${show(groups.water.mean)} g/g (n=${groups.water.count})\n${tr('盐水浴均值','Saline mean')}: ${show(groups.saline.mean)} g/g (n=${groups.saline.count})`;
  state={...p,records:records.map(r=>({...r,uptake:uptake(r)})),ordered_ids:order.map(r=>r.id),selected_uptake:q,valid_count:valid.length,water_mean:groups.water.mean,saline_mean:groups.saline.mean,wrong_uptake:wrong};
 }
 function set(v){if(v.selected&&records.some(r=>r.id===v.selected))p.selected=v.selected;if(v.order)p.order=['id','dry','wet'].includes(v.order)?v.order:'id';if('mismatch'in v)p.mismatch=!!v.mismatch;const r=records.find(x=>x.id===p.selected);if('dry'in v)r.dry=Math.max(.1,Math.min(2,Number(v.dry)||.1));if('wet'in v){saved[r.id]=Math.max(0,Math.min(10,Number(v.wet)||0));if(r.wet!==null)r.wet=saved[r.id];}if('missing'in v)r.wet=v.missing?null:saved[r.id];$('selected').value=p.selected;$('order').value=p.order;$('mismatch').checked=p.mismatch;$('dry').value=r.dry;$('wet').value=r.wet===null?saved[r.id]:r.wet;$('missing').checked=r.wet===null;render();}
 const reset=()=>{records=base.map(([id,bath,dry,wet])=>({id,bath,dry,wet}));saved=Object.fromEntries(records.map(r=>[r.id,r.wet===null?2.8:r.wet]));p={selected:'A01',order:'id',mismatch:false};set({});};
 ['selected','order'].forEach(k=>$(k).addEventListener('input',()=>set({[k]:$(k).value})));['dry','wet'].forEach(k=>$(k).addEventListener('input',()=>set({[k]:Number($(k).value)})));['missing','mismatch'].forEach(k=>$(k).addEventListener('input',()=>set({[k]:$(k).checked})));$('reset').addEventListener('click',reset);
 window.CourseLab={set,reset,state:()=>JSON.parse(JSON.stringify(state))};reset();
})();

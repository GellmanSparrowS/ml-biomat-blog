(()=>{'use strict';
const root=document.getElementById('P12-lab');if(!root)return;
const zh=document.documentElement.lang.startsWith('zh'),tr=(z,e)=>zh?z:e,$=id=>root.querySelector('#P12-'+id);
const data={A01:[2,2.2],A02:[2.8],A03:[3,3.2,3.4],B01:[2,2.2],B02:[2.5,2.7],B03:[2.9]},ids=Object.keys(data),blue='#235f83',orange='#bd5838',ink='#1e303c';
let settings={copies:1,missing:false,specimen:'A03'},snapshot={};
const avg=a=>a.length?a.reduce((s,v)=>s+v,0)/a.length:null;
const text=(x,y,s,size=16,anchor='start',color=ink)=>`<text x="${x}" y="${y}" font-size="${size}" text-anchor="${anchor}" fill="${color}">${s}</text>`;
const line=(x1,y1,x2,y2,c='#dae3e7',w=1)=>`<path d="M${x1},${y1}L${x2},${y2}" stroke="${c}" stroke-width="${w}" fill="none"/>`;
function calculate(k,missing){
 const rows=ids.map(id=>{const values=(id==='A01'?Array.from({length:k},()=>data[id]).flat():data[id]).slice();return{id,form:id[0],rows:values.length,values:missing&&id==='A02'?[]:values}});
 rows.forEach(r=>{r.valid=r.values.length;r.mean=avg(r.values)});
 const groups={};for(const form of ['A','B']){const s=rows.filter(r=>r.form===form),valid=s.filter(r=>r.mean!==null);groups[form]={rows:s.reduce((n,r)=>n+r.rows,0),valid:s.reduce((n,r)=>n+r.valid,0),specimens:s.length,validSpecimens:valid.length,rowMean:avg(s.flatMap(r=>r.values)),equalMean:avg(valid.map(r=>r.mean))};}
 rows.forEach(r=>{r.rowWeight=r.valid/groups[r.form].valid;r.equalWeight=r.mean===null?0:1/groups[r.form].validSpecimens});return{rows,groups};
}
function render(){
 const result=calculate(settings.copies,settings.missing),chosen=result.rows.find(r=>r.id===settings.specimen),a=result.groups.A;
 $('copies').value=settings.copies;$('copies-value').textContent=settings.copies;$('missing').checked=settings.missing;$('specimen').value=settings.specimen;
 const X=q=>100+(q-1.8)/1.8*510,Y=i=>85+i*55;
 let s=text(24,27,tr('读数与所属试样的均值','Readings and their specimen means'),20);
 for(let v=2;v<=3.6;v+=.4){s+=line(X(v),55,X(v),395)+text(X(v),422,v.toFixed(1),15,'middle')}
 result.rows.forEach((r,i)=>{if(r.id===chosen.id)s+=`<rect x="20" y="${Y(i)-23}" width="610" height="46" fill="#eaf1f4"/>`;s+=text(76,Y(i)+5,r.id,17,'end');
  if(r.valid){r.values.forEach((v,j)=>{const y=Y(i)+(r.valid>1?(j/(r.valid-1)-.5)*28:0);s+=`<circle cx="${X(v)}" cy="${y}" r="4.5" fill="${blue}"/>`});const x=X(r.mean),y=Y(i);s+=`<path d="M${x},${y-7}l7,7l-7,7l-7,-7Z" fill="${orange}"/>`}else s+=text(X(2),Y(i)+5,tr('q缺失；记录仍保留','q missing; row retained'),16);
 });s+=text(355,453,'q / g g⁻¹',17,'middle')+`<circle cx="105" cy="487" r="5" fill="${blue}"/>`+text(118,492,tr('技术读数','Technical reading'),15)+`<path d="M350,480l7,7l-7,7l-7,-7Z" fill="${orange}"/>`+text(365,492,tr('试样均值','Specimen mean'),15);$('readings').innerHTML=s;
 const W=w=>100+w*510;s=text(24,27,tr('每块试样在本配方内的权重','Specimen weights within its formulation'),20);
 for(const v of [0,.25,.5,.75,1])s+=line(W(v),55,W(v),400)+text(W(v),426,`${Math.round(v*100)}%`,15,'middle');
 result.rows.forEach((r,i)=>{s+=text(76,Y(i)+5,r.id,17,'end');s+=`<rect x="100" y="${Y(i)-15}" width="${r.rowWeight*510}" height="12" fill="${blue}"/><rect x="100" y="${Y(i)+3}" width="${r.equalWeight*510}" height="12" fill="${orange}"/>`;if(r.id===chosen.id)s+=`<rect x="92" y="${Y(i)-22}" width="526" height="45" fill="none" stroke="${ink}" stroke-width="2"/>`;});
 s+=`<rect x="105" y="482" width="19" height="9" fill="${blue}"/>`+text(133,492,tr('读数等权','Equal readings'),15)+`<rect x="350" y="482" width="19" height="9" fill="${orange}"/>`+text(378,492,tr('试样等权','Equal specimens'),15);$('weights').innerHTML=s;
 const cx=k=>105+(k-1)*150,cy=q=>345-(q-2.1)/.8*260;s=text(30,28,tr('复制A01的已有记录：沿同一个计算追踪','Copy existing A01 records and trace the same calculation'),22);
 for(let q=2.1;q<2.91;q+=.2)s+=line(105,cy(q),855,cy(q))+text(90,cy(q)+5,q.toFixed(1),16,'end');
 for(let k=1;k<=6;k++)s+=text(cx(k),377,k,17,'middle');
 for(const [key,c] of [['rowMean',blue],['equalMean',orange]]){const points=[];for(let k=1;k<=6;k++){const v=calculate(k,settings.missing).groups.A[key];points.push([cx(k),cy(v)]);s+=`<circle cx="${cx(k)}" cy="${cy(v)}" r="4" fill="${c}"/>`;}s+=`<path d="M${points.map(p=>p.join(',')).join('L')}" stroke="${c}" stroke-width="3" fill="none"/>`;const q=a[key];s+=`<circle cx="${cx(settings.copies)}" cy="${cy(q)}" r="8" stroke="${c}" stroke-width="3" fill="white"/>`;}
 s+=text(480,414,tr('A01两条记录的保留份数 k','Copies k of the two A01 records'),19,'middle')+text(105,60,'A: q / g g⁻¹',18);
 s+=line(105,448,135,448,blue,3)+text(145,454,tr('逐读数平均','Mean over readings'),17)+line(470,448,500,448,orange,3)+text(510,454,tr('有效试样等权平均','Mean over valid specimens'),17);$('curve').innerHTML=s;
 let table=`<thead><tr><th>${tr('配方','Formulation')}</th><th>${tr('行数 / 有效读数','Rows / valid readings')}</th><th>${tr('登记 / 有效试样','Registered / valid specimens')}</th><th>${tr('逐读数 q','Reading mean q')} / g g⁻¹</th><th>${tr('试样等权 q','Equal-specimen q')} / g g⁻¹</th></tr></thead><tbody>`;
 for(const id of ['A','B']){const g=result.groups[id];table+=`<tr><td>${id}</td><td>${g.rows} / ${g.valid}</td><td>${g.specimens} / ${g.validSpecimens}</td><td>${g.rowMean.toFixed(4)}</td><td>${g.equalMean.toFixed(4)}</td></tr>`;}$('summary').innerHTML=table+'</tbody>';
 $('readout').textContent=tr(`${chosen.id}：${chosen.rows}行，${chosen.valid}个有效读数；试样均值 ${chosen.mean===null?'缺失':chosen.mean.toFixed(4)+' g/g'}。逐读数权重 ${(100*chosen.rowWeight).toFixed(2)}%，试样等权权重 ${(100*chosen.equalWeight).toFixed(2)}%。`,`${chosen.id}: ${chosen.rows} rows, ${chosen.valid} valid readings; specimen mean ${chosen.mean===null?'missing':chosen.mean.toFixed(4)+' g/g'}. Reading weight ${(100*chosen.rowWeight).toFixed(2)}%; equal-specimen weight ${(100*chosen.equalWeight).toFixed(2)}%.`);
 snapshot={...settings,A_rows:a.rows,A_valid:a.valid,A_specimens:a.specimens,A_valid_specimens:a.validSpecimens,A_row_mean:a.rowMean,A_equal_mean:a.equalMean,B_row_mean:result.groups.B.rowMean,B_equal_mean:result.groups.B.equalMean,selected_mean:chosen.mean,selected_row_weight:chosen.rowWeight,selected_equal_weight:chosen.equalWeight};return snapshot;
}
function set(p={}){if(Number.isFinite(Number(p.copies)))settings.copies=Math.max(1,Math.min(6,Math.round(Number(p.copies))));if('missing'in p)settings.missing=Boolean(p.missing);if(ids.includes(p.specimen))settings.specimen=p.specimen;return render()}
function reset(){settings={copies:1,missing:false,specimen:'A03'};return render()}
for(const name of ['copies','specimen'])$(name).addEventListener('input',()=>set({[name]:$(name).value}));$('missing').addEventListener('change',()=>set({missing:$('missing').checked}));$('reset').addEventListener('click',reset);
window.CourseLab={set,reset,state:()=>({...snapshot}),destroy:()=>{}};render();
})();

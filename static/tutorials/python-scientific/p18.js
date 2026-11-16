(() => {
 const root=document.getElementById('P18-lab');if(!root)return;
 const zh=document.documentElement.lang.startsWith('zh'),tr=(a,b)=>zh?a:b,el=x=>root.querySelector('#P18-'+x);
 const defaults={eta:4,frequency:.25,phase:45};let p={...defaults},result={},resetCount=0,destroyed=false;const mounted=new Set();
 function draw(){
  const omega=2*Math.PI*p.frequency,period=1/p.frequency,rows=Array.from({length:361},(_,i)=>{const angle=i*Math.PI/180,t=i/360*period,eps=.05*Math.sin(angle),rate=.05*omega*Math.cos(angle);return[i,t,eps,20*eps+p.eta*rate]});
  const current=rows[p.phase],work=Math.PI*p.eta*omega*.05**2*1000;
  let polygon=0;for(let i=1;i<rows.length;i++)polygon+=(rows[i][3]+rows[i-1][3])/2*(rows[i][2]-rows[i-1][2])*1000;
  result={...p,time_s:current[1],strain:current[2],stress_kPa:current[3],period_s:period,work_J_m3:work,polygon_J_m3:polygon,record:p.phase,n:rows.length};
  el('phase-value').textContent=p.phase;
  el('readout').textContent=tr(`记录${p.phase}：t=${current[1].toFixed(4)} s，应变${(current[2]*100).toFixed(4)}%，应力${current[3].toFixed(6)} kPa。周期${period.toFixed(2)} s；每周期耗散${work.toFixed(4)} J/m³，采样积分${polygon.toFixed(4)} J/m³。`,`Record ${p.phase}: t=${current[1].toFixed(4)} s, strain ${(current[2]*100).toFixed(4)}%, stress ${current[3].toFixed(6)} kPa. Period ${period.toFixed(2)} s; dissipated energy ${work.toFixed(4)} J/m³ per cycle; sampled integral ${polygon.toFixed(4)} J/m³.`);
  if(!window.Plotly)return;
  const custom=rows.map(r=>[r[0],r[1],r[2]*100,r[3]]),revision=`${p.eta}|${p.frequency}|${resetCount}`;
  const hover=tr('记录%{customdata[0]}<br>t=%{customdata[1]:.3f} s<br>应变%{customdata[2]:.3f}%<br>应力%{customdata[3]:.4f} kPa<extra></extra>','Record %{customdata[0]}<br>t=%{customdata[1]:.3f} s<br>strain%{customdata[2]:.3f}%<br>stress%{customdata[3]:.4f} kPa<extra></extra>');
  const definitions=[['loop',2,3,100,1,tr('应力—应变轨迹','Stress–strain trajectory'),tr('应变 / %','Strain / %'),tr('应力 / kPa','Stress / kPa'),[-5.8,5.8],[-1.8,1.8]],['strain',1,2,1,100,tr('应变随时间变化','Strain over time'),tr('时间 / s','Time / s'),tr('应变 / %','Strain / %'),[0,period],[-5.8,5.8]],['stress',1,3,1,1,tr('应力随时间变化','Stress over time'),tr('时间 / s','Time / s'),tr('应力 / kPa','Stress / kPa'),[0,period],[-1.8,1.8]]];
  const promises=definitions.map(([id,xi,yi,xf,yf,title,xlabel,ylabel,xrange,yrange])=>{
   const div=el(id),x=rows.map(r=>r[xi]*xf),y=rows.map(r=>r[yi]*yf),traces=[{x,y,customdata:custom,type:'scatter',mode:'lines',line:{color:'#28658c',width:2.7},hovertemplate:hover},{x:[current[xi]*xf],y:[current[yi]*yf],customdata:[custom[p.phase]],type:'scatter',mode:'markers',marker:{color:'#b64a35',size:12,line:{color:'#fff',width:1}},hovertemplate:hover}];
   const layout={title:{text:title,font:{size:18}},showlegend:false,margin:{l:65,r:20,t:55,b:60},font:{size:14,color:'#20313e'},paper_bgcolor:'#fff',plot_bgcolor:'#fff',uirevision:revision,
    xaxis:{title:{text:xlabel,font:{size:15}},range:xrange,gridcolor:'#e4eaee',zerolinecolor:'#b7c4cb'},yaxis:{title:{text:ylabel,font:{size:15}},range:yrange,gridcolor:'#e4eaee',zerolinecolor:'#b7c4cb'}};
   return window.Plotly.react(div,traces,layout,{displaylogo:false,responsive:true,scrollZoom:false,modeBarButtonsToRemove:['lasso2d','select2d']}).then(()=>{if(destroyed)return;if(!mounted.has(id)){div.on('plotly_click',event=>{const r=event.points[0].customdata;if(r)set({phase:r[0]})});mounted.add(id)}});
  });window.CourseLab.ready=Promise.all(promises);
 }
 function set(q){p={...p,...q};p.eta=[0,2,4,8].includes(+p.eta)?+p.eta:4;p.frequency=[.125,.25,.5].includes(+p.frequency)?+p.frequency:.25;p.phase=Math.round(Math.max(0,Math.min(360,+p.phase)));for(const k of ['eta','frequency','phase'])el(k).value=p[k];draw();return result}
 for(const k of ['eta','frequency','phase'])el(k).addEventListener('input',()=>set({[k]:el(k).value}));
 const reset=()=>{resetCount++;return set(defaults)};el('reset').addEventListener('click',reset);
 window.CourseLab={set,state:()=>structuredClone(result),reset,ready:Promise.resolve(),destroy:()=>{destroyed=true;if(window.Plotly)for(const id of ['loop','strain','stress'])window.Plotly.purge(el(id))}};set(defaults);
})();

(() => {
  if(!document.getElementById('P05-lab'))return;
  const zh=document.documentElement.lang.startsWith('zh'),tr=(z,e)=>zh?z:e,get=n=>document.getElementById('P05-'+n);
  const base={R01:{raw:[0,60,120,180,240,300],unit:'s',temp:[80,61,48,39,33,30]},R02:{raw:[0,1,2,3,4,5],unit:'min',temp:[80,65,null,46,40,35]},R03:{raw:[0,60,120,180,240,300],unit:'s',temp:[80,70,60,52,45,40]}};
  let p;
  function values(){const r=base[p.selected],temp=[...r.temp];if(p.selected==='R02'){if(p.mode==='supplied')temp[2]=p.middle;if(p.mode==='zero')temp[2]=0;}if(p.missing_last)temp[5]=null;const factor=r.unit==='min'&&!p.ignore_units?60:1,times=r.raw.map(x=>x*factor),valid=temp.map((x,i)=>x===null?null:i).filter(x=>x!==null),a=valid[0],b=valid[valid.length-1];const duration=times[b]-times[a],change=temp[b]-temp[a],trueDuration=(r.raw[b]-r.raw[a])*(r.unit==='min'?60:1);return{raw:r.raw,unit:r.unit,temp,times,valid_count:valid.length,duration_s:duration,change,rate:change/duration,reference_rate:change/trueDuration,first:a,last:b,middle_temperature:temp[2]};}
  function state(){return {...p,...values()};}
  function render(){const s=state();get('selected').value=p.selected;get('ignore').checked=p.ignore_units;get('mode').value=p.mode;get('middle').value=p.middle;get('last').checked=p.missing_last;get('mode').disabled=p.selected!=='R02';get('middle').disabled=p.selected!=='R02'||p.mode!=='supplied';
    get('output').textContent=tr(`${p.selected}：有效 ${s.valid_count}/6；窗口 ${s.times[s.first]}–${s.times[s.last]} s；温差 ${s.change.toFixed(1)} °C；平均速率 ${s.rate.toFixed(4)} °C/s。`,`${p.selected}: ${s.valid_count}/6 valid; interval ${s.times[s.first]}–${s.times[s.last]} s; change ${s.change.toFixed(1)} °C; mean rate ${s.rate.toFixed(4)} °C/s.`)+' '+(p.ignore_units&&s.unit==='min'?tr('当前故意把分钟误读为秒。','Minutes are deliberately being misread as seconds.'):tr('时间单位按清单换算。','Time units follow the manifest.'));
    get('rows').innerHTML=s.raw.map((raw,i)=>`<tr><th scope="row">${i+1}</th><td>${raw}</td><td>${s.unit}</td><td>${s.times[i]}</td><td>${s.temp[i]===null?'None':s.temp[i].toFixed(1)}</td><td>${i===s.first?tr('起点','First'):i===s.last?tr('终点','Last'):s.temp[i]===null?tr('缺失','Missing'):'—'}</td></tr>`).join('');
    const blue='#28648a',red='#b85336',gray='#829291';let svg=[];
    const text=(x,y,t,size=14,c='#172b36',anchor='start')=>`<text x="${x}" y="${y}" font-size="${size}" fill="${c}" text-anchor="${anchor}">${t}</text>`;
    const x0=55,y0=315,w=535,h=255,X=x=>x0+x*w/300,Y=t=>y0-t*h/90;
    svg.push(text(x0,25,tr('温度 / °C','Temperature / °C'),17),`<path d="M${x0} 55V${y0}H${x0+w}" fill="none" stroke="#172b36"/>`);
    for(let t=0;t<=80;t+=20){svg.push(`<path d="M${x0} ${Y(t)}H${x0+w}" stroke="#dce2df"/>`,text(x0-10,Y(t)+5,t,12,gray,'end'));}
    for(let t=0;t<=300;t+=60)svg.push(text(X(t),338,t,12,gray,'middle'));
    svg.push(text(x0+w/2,365,tr('按当前规则解释的时间 / s','Time interpreted by the current rule / s'),14,'#172b36','middle'));
    function curve(times,temp,color,width,dash){let d='',active=false;for(let i=0;i<times.length;i++){if(temp[i]===null){active=false;continue;}d+=(active?'L':'M')+X(times[i])+','+Y(temp[i])+' ';active=true;}return `<path d="${d}" stroke="${color}" stroke-width="${width}" fill="none" ${dash?'stroke-dasharray="7 4"':''}/>`;}
    for(const [rid,r]of Object.entries(base))if(rid!==p.selected)svg.push(curve(r.raw.map(t=>t*(r.unit==='min'?60:1)),r.temp,'#b8c5c2',1.5,false));
    const trueTimes=s.raw.map(t=>t*(s.unit==='min'?60:1));svg.push(curve(trueTimes,s.temp,gray,2,true),curve(s.times,s.temp,blue,2.8,false));
    for(let i=0;i<6;i++)if(s.temp[i]!==null)svg.push(`<circle cx="${X(s.times[i])}" cy="${Y(s.temp[i])}" r="5" fill="${p.mode==='zero'&&i===2&&p.selected==='R02'?red:blue}"/>`);
    svg.push(`<path d="M${X(s.times[s.first])} ${Y(s.temp[s.first])}L${X(s.times[s.last])} ${Y(s.temp[s.last])}" stroke="${red}" stroke-width="1.5" stroke-dasharray="3 4"/>`);
    svg.push(text(655,25,tr('端点平均速率 / °C·s⁻¹','Endpoint rate / °C·s⁻¹'),17));
    const vmax=Math.max(Math.abs(s.rate),Math.abs(s.reference_rate)),tick=vmax>.5?2:.05,max=Math.ceil(vmax/tick)*tick+tick,rx=650,rw=280,R=r=>rx+rw+r/max*rw;
    svg.push(`<path d="M${rx+rw} 65V265M${rx} 265H${rx+rw}" stroke="#172b36" fill="none"/>`);
    for(let q=0;q<=max+1e-9;q+=tick)svg.push(text(R(-q),286,tick<1?(-q).toFixed(2):String(-q),11,gray,'middle'));
    for(const [i,v,label,col]of [[0,s.reference_rate,tr('正确单位','Correct units'),gray],[1,s.rate,tr('当前解释','Current rule'),blue]]){const y=105+i*100;svg.push(text(rx,y-20,label,14,col),`<rect x="${R(v)}" y="${y-8}" width="${-v/max*rw}" height="26" fill="${col}" fill-opacity=".8"/>`,text(rx,y+43,v.toFixed(4),16,col));}
    svg.push(text(650,333,tr('温差','Change')+` = ${s.change.toFixed(1)} °C`,15),text(650,360,tr('历时','Duration')+` = ${s.duration_s} s`,15),text(650,387,tr('速率大小比','Magnitude ratio')+` = ${(Math.abs(s.rate/s.reference_rate)).toFixed(1)}`,15));
    svg.push(text(55,404,tr('蓝：当前记录  灰虚线：正确单位  红点线：端点连线','Blue: current; gray dashed: correct units; red dotted: endpoints'),13));get('plot').innerHTML=svg.join('');
  }
  function set(q){for(const k of ['selected','ignore_units','missing_last','middle','mode'])if(k in q)p[k]=q[k];if('fill_middle'in q)p.mode=q.fill_middle?'supplied':'original';if('zero_missing'in q)p.mode=q.zero_missing?'zero':'original';p.middle=Math.max(0,Math.min(90,Number(p.middle)));if(!base[p.selected])throw Error('Unknown run');render();return state();}
  function reset(){p={selected:'R02',ignore_units:false,missing_last:false,middle:55,mode:'original'};render();return state();}
  get('selected').addEventListener('change',()=>set({selected:get('selected').value}));get('ignore').addEventListener('change',()=>set({ignore_units:get('ignore').checked}));get('mode').addEventListener('change',()=>set({mode:get('mode').value}));get('middle').addEventListener('input',()=>set({middle:Number(get('middle').value)}));get('last').addEventListener('change',()=>set({missing_last:get('last').checked}));get('reset').addEventListener('click',reset);window.CourseLab={set,state,reset};reset();
})();

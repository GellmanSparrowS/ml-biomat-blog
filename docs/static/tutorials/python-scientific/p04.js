(() => {
  const root=document.getElementById('P04-lab'); if(!root)return;
  const zh=document.documentElement.lang.startsWith('zh'),tr=(a,b)=>zh?a:b;
  const get=n=>document.getElementById('P04-'+n);
  let records,selected,step;
  const base=()=>[{id:'A01',dry:1.2,wet:4.8},{id:'A02',dry:1,wet:3.4},{id:'A03',dry:.8,wet:2.8},{id:'B01',dry:1.2,wet:3.6},{id:'B02',dry:1,wet:null},{id:'B03',dry:.8,wet:2.32}];
  function evaluate(r){if(!Number.isFinite(r.dry)||r.dry<=0)return{status:'invalid',value:null,reason:tr('干质量应为有限正数','Dry mass must be finite and positive'),branch:0};if(r.wet===null)return{status:'missing',value:null,reason:tr('湿质量缺失，返回 None','Wet mass absent: return None'),branch:1};if(!Number.isFinite(r.wet)||r.wet<r.dry)return{status:'invalid',value:null,reason:tr('核对湿质量与干质量的关系','Check wet mass against dry mass'),branch:2};return{status:'valid',value:(r.wet-r.dry)/r.dry,reason:tr('完成相减和归一化，返回数值','Subtract and normalize: return a value'),branch:3};}
  function trace(){let sum=0,n=0;return records.map((r,i)=>{const v=evaluate(r);if(v.value!==null){sum+=v.value;n++;}return{...v,id:r.id,step:i+1,sum,valid_count:n,mean:n?sum/n:null};});}
  function state(){const all=trace(),now=step?all[step-1]:null;return{selected,step,valid_count:now?.valid_count??0,sum:now?.sum??0,mean:now?.mean??null,current_status:now?.status??'unprocessed',results:all.map((t,i)=>({id:t.id,status:i<step?t.status:'unprocessed',value:i<step?t.value:null}))};}
  function sync(){const r=records.find(x=>x.id===selected);get('selected').value=selected;get('dry').value=r.dry;get('wet').value=r.wet??2.8;get('missing').checked=r.wet===null;get('wet').disabled=r.wet===null;}
  const fmt=x=>x===null?'None':x.toFixed(3);
  const niceMax=value=>{const raw=value/4,base=10**Math.floor(Math.log10(raw));return [1,2,2.5,5,10].find(v=>v*base>=raw-1e-12)*base*4;};
  function render(){sync();const all=trace(),s=state(),cur=step?all[step-1]:null;
    get('output').textContent=tr(`已处理 ${step}/6；有效 ${s.valid_count}；总和 ${fmt(s.sum)} g/g；均值 ${fmt(s.mean)} g/g。`,`${step}/6 processed; ${s.valid_count} valid; sum ${fmt(s.sum)} g/g; mean ${fmt(s.mean)} g/g.`)+' '+(cur?`${cur.id}: ${cur.reason}`:tr('按“下一条”进入 A01。','Choose Next record to enter A01.'));
    get('next').disabled=step>=6;
    get('rows').innerHTML=records.map((r,i)=>{const t=all[i],done=i<step;const label=done?({valid:tr('有效','Valid'),missing:tr('缺失','Missing'),invalid:tr('需核对','Invalid')}[t.status]):tr('尚未处理','Unprocessed');return `<tr${i===step-1?' class="current"':''}><td>${i+1}</td><th scope="row">${r.id}</th><td>${r.dry.toFixed(2)}</td><td>${r.wet===null?'None':r.wet.toFixed(2)}</td><td>${label}</td><td>${done?fmt(t.value):'—'}</td><td>${done?t.valid_count:'—'}</td><td>${done?fmt(t.mean):'—'}</td></tr>`;}).join('');
    const blue='#28648a',red='#b85336',gray='#819093',green='#467a62';let parts=[];
    const text=(x,y,str,size=15,color='#172b36',anchor='start')=>`<text x="${x}" y="${y}" font-size="${size}" fill="${color}" text-anchor="${anchor}">${str}</text>`;
    parts.push(text(24,27,tr('当前调用经过的判断','Decisions in the current call'),18));
    const labels=[tr('干质量有限且 > 0？','Finite dry mass > 0?'),tr('湿质量存在？','Wet mass supplied?'),tr('湿质量 ≥ 干质量？','Wet mass ≥ dry mass?'),tr('返回 (湿−干)/干','Return (wet−dry)/dry')];
    labels.forEach((label,i)=>{const active=cur&&cur.branch===i,passed=cur&&cur.branch>i,color=active?(i===3?blue:red):(passed?green:gray),y=54+i*79;parts.push(`<rect x="24" y="${y}" width="310" height="48" rx="3" fill="${color}" fill-opacity="${active?.18:.06}" stroke="${color}"/>`,text(39,y+30,label,16,color));if(i<3)parts.push(`<path d="M179 ${y+49}v28" stroke="${passed?green:gray}" stroke-width="2"/>`,text(189,y+69,tr('是','Yes'),12,passed?green:gray));});
    parts.push(text(24,410,cur?cur.id+' → '+(cur.status==='valid'?fmt(cur.value)+' g/g':cur.status==='missing'?'None':'ValueError'):tr('等待第一次调用','Waiting for the first call'),18,cur?.status==='valid'?blue:red));
    const x0=430,y0=355,w=480,h=275,max=niceMax(Math.max(3.5,...all.map(t=>t.mean??0))*1.12),X=k=>x0+(k-1)*w/5,Y=q=>y0-q/max*h;
    parts.push(text(x0,27,tr('累计均值 / g·g⁻¹','Running mean / g·g⁻¹'),18),`<path d="M${x0} ${y0-h}V${y0}H${x0+w}" stroke="#172b36" fill="none"/>`);
    for(let i=0;i<=4;i++){let q=max*i/4;parts.push(`<path d="M${x0} ${Y(q)}H${x0+w}" stroke="#dde2df"/>`,text(x0-8,Y(q)+5,String(Number(q.toPrecision(6))),12,'#56676c','end'));}
    for(let i=1;i<=6;i++){parts.push(text(X(i),379,String(i),13,'#56676c','middle'));if(i>step)parts.push(`<circle cx="${X(i)}" cy="${y0+2}" r="4" fill="#bec6c4"/>`);}
    parts.push(text(x0+w/2,412,tr('已处理的记录数（不是时间）','Records processed (not time)'),14,'#172b36','middle'));
    const visible=all.slice(0,step).filter(t=>t.mean!==null);if(visible.length)parts.push(`<polyline points="${visible.map(t=>X(t.step)+','+Y(t.mean)).join(' ')}" stroke="${blue}" stroke-width="2.5" fill="none"/>`);
    visible.forEach(t=>{parts.push(`<circle cx="${X(t.step)}" cy="${Y(t.mean)}" r="${t.step===step?7:4.5}" fill="${t.status==='valid'?blue:red}"/>`);if(t.step===step)parts.push(text(X(t.step)-5,Y(t.mean)-15,fmt(t.mean),14,blue,t.step===6?'end':'middle'));});
    get('plot').innerHTML=parts.join('');
  }
  function set(p){if(p.selected)selected=p.selected;const r=records.find(x=>x.id===selected);if(!r)throw new Error('Unknown specimen');let changed=false;if('dry'in p){r.dry=Number(p.dry);changed=true;}if('wet'in p){r.wet=Number(p.wet);changed=true;}if('missing'in p){r.wet=p.missing?null:(r.wet??2.8);changed=true;}if(changed)step=0;if('step'in p)step=Math.max(0,Math.min(6,Math.floor(p.step)));render();return state();}
  function reset(){records=base();selected='A01';step=0;render();return state();}
  get('selected').addEventListener('change',()=>set({selected:get('selected').value}));get('dry').addEventListener('change',()=>set({dry:Number(get('dry').value)}));get('wet').addEventListener('change',()=>set({wet:Number(get('wet').value)}));get('missing').addEventListener('change',()=>set({missing:get('missing').checked}));get('next').addEventListener('click',()=>set({step:step+1}));get('all').addEventListener('click',()=>set({step:6}));get('restart').addEventListener('click',()=>set({step:0}));get('reset').addEventListener('click',reset);
  window.CourseLab={reset,set,state};reset();
})();

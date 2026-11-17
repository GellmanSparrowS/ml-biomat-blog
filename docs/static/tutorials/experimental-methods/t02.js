(()=>{
 const zh=document.documentElement.lang.startsWith('zh');const L=(a,b)=>zh?a:b;
 const ids=['char','burn','mass'];const get=k=>document.getElementById('T02-'+k);
 let current={};const defaults={char:.1,burn:1,mass:10};
 function update(){const y=+get('char').value,b=+get('burn').value,m=+get('mass').value;
  current={pyrolysis_loss_percent:60*(1-y),air_loss_percent:b*(12+60*y),final_residue_percent:20+(1-b)*(12+60*y),inert_mass_mg:m*(.32+.6*y),final_mass_mg:m*(.2+(1-b)*(.12+.6*y)),original_carbon_percent:12};
  ids.forEach(k=>get(k+'-value').textContent=(+get(k).value).toFixed(k==='mass'?1:2));
  get('result').textContent=L(`氮气热解失重 ${current.pyrolysis_loss_percent.toFixed(1)}%；空气阶段失重 ${current.air_loss_percent.toFixed(1)}%；最终残余 ${current.final_residue_percent.toFixed(1)}%。原有炭黑始终12%，无机组分始终20%。`,`Nitrogen-stage loss ${current.pyrolysis_loss_percent.toFixed(1)}%; air-stage loss ${current.air_loss_percent.toFixed(1)}%; final residue ${current.final_residue_percent.toFixed(1)}%. Original carbon remains 12% and the inorganic component remains 20%.`);
  const values=[100,92,32+60*y,current.final_residue_percent],labels=L(['初始','脱水后','氮气热解后','空气阶段后'],['Initial','After drying','After pyrolysis','After air stage']);
  let h='<rect width="760" height="390" fill="#fcfbf7"/><path d="M65 32V315H730" fill="none" stroke="#566b77"/>';
  const X=i=>135+i*175,Y=v=>315-v*2.5;
  [0,20,40,60,80,100].forEach(v=>h+=`<path d="M65 ${Y(v)}H730" stroke="#dce3e4"/><text x="55" y="${Y(v)+4}" text-anchor="end" fill="#20333e">${v}</text>`);
  values.forEach((v,i)=>{h+=`<rect x="${X(i)-35}" y="${Y(v)}" width="70" height="${315-Y(v)}" fill="${['#167d9a','#37967d','#20333e','#c49b35'][i]}"/><text x="${X(i)}" y="${Y(v)-9}" text-anchor="middle" fill="#20333e">${v.toFixed(1)}% · ${(m*v/100).toFixed(2)} mg</text><text x="${X(i)}" y="340" text-anchor="middle" fill="#20333e">${labels[i]}</text>`;});
  h+=`<text x="65" y="20" fill="#20333e">${L('初始质量的百分比 / %','Percent of initial mass / %')}</text><text x="397" y="374" text-anchor="middle" fill="#20333e">${L('四个阶段的质量；不是连续时间曲线','Mass at four stages; not a continuous time trace')}</text>`;get('plot').innerHTML=h;
 }
 function set(p){ids.forEach(k=>{if(p[k]!==undefined)get(k).value=Math.min(+get(k).max,Math.max(+get(k).min,+p[k]));});update();return {...current};}
 ids.forEach(k=>get(k).addEventListener('input',update));get('reset').addEventListener('click',()=>set(defaults));
 window.CourseLab={set,state:()=>({...current}),reset:()=>set(defaults)};set(defaults);
})();

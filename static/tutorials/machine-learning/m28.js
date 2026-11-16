(()=>{
 const root=document.getElementById('M28-lab');if(!root)return;
 const zh=document.documentElement.lang.startsWith('zh'), $=id=>document.getElementById('M28-'+id);
 let p={n11:229,n10:0,n01:210,n00:11};let result;
 const colors=['#dceaf0','#e8cdb9','#acd0d7','#e4e8eb'];
 function draw(){
  const n=p.n11+p.n10+p.n01+p.n00;
  result={...p,n,valid:n>0,accuracyA:n?(p.n11+p.n10)/n:null,accuracyB:n?(p.n11+p.n01)/n:null,delta:n?(p.n01-p.n10)/n:null};
  for(const k of ['n11','n10','n01','n00'])$(k).value=p[k];
  const headings=zh?['两者正确','仅基线正确','仅增广正确','两者错误']:['Both correct','Baseline only correct','Augmented only correct','Both wrong'];
  const nums=[p.n11,p.n10,p.n01,p.n00];
  let svg='';nums.forEach((v,i)=>{const x=22+(i%2)*255,y=40+Math.floor(i/2)*140;svg+=`<rect x="${x}" y="${y}" width="238" height="124" rx="5" fill="${colors[i]}"/><text x="${x+119}" y="${y+35}" text-anchor="middle" font-size="15">${headings[i]}</text><text x="${x+119}" y="${y+85}" text-anchor="middle" font-size="29">${v}</text>`});
  svg+=`<text x="273" y="23" text-anchor="middle" font-size="16">${zh?'同一批样本的成对结果':'Paired outcomes on the same observations'}</text>`;
  if(n){
   const values=[result.accuracyA,result.accuracyB],names=zh?['基线','增广']:['Baseline','Augmented'];
   values.forEach((v,i)=>{const y=352+i*50;svg+=`<text x="90" y="${y+18}" text-anchor="end" font-size="15">${names[i]}</text><rect x="105" y="${y}" width="350" height="24" fill="#edf2f4"/><rect x="105" y="${y}" width="${v*350}" height="24" fill="${i?'#b76b39':'#326f8b'}"/><text x="463" y="${y+18}" font-size="14">${(v*100).toFixed(2)}%</text>`});
   [0,25,50,75,100].forEach(t=>svg+=`<text x="${105+t*3.5}" y="454" text-anchor="middle" font-size="12">${t}</text>`);
   svg+=`<text x="280" y="478" text-anchor="middle" font-size="13">${zh?'正确率 / %':'Accuracy / %'}</text>`;
  }
  $('plot').innerHTML=svg;
  $('readout').textContent=n?(zh?`样本总数 ${n}；增广 − 基线 = (${p.n01} − ${p.n10}) / ${n} = ${(100*result.delta).toFixed(2)} 个百分点。`:`Total ${n}; augmented − baseline = (${p.n01} − ${p.n10}) / ${n} = ${(100*result.delta).toFixed(2)} percentage points.`):(zh?'先加入至少一条观测，再计算正确率。':'Add at least one observation to calculate accuracy.');
 }
 function state(){return JSON.parse(JSON.stringify(result))}
 function set(v={}){for(const k of ['n11','n10','n01','n00'])if(v[k]!==undefined)p[k]=Math.max(0,Math.min(500,Math.round(Number(v[k])||0)));draw();return state()}
 function reset(){p={n11:229,n10:0,n01:210,n00:11};draw();return state()}
 ['n11','n10','n01','n00'].forEach(k=>$(k).addEventListener('input',e=>set({[k]:e.target.value})));
 $('reset').onclick=reset;$('small').onclick=()=>set({n11:6,n10:1,n01:3,n00:0});$('same').onclick=()=>set({n11:6,n10:2,n01:2,n00:0});
 window.CourseLab={set,state,reset};draw();
})();

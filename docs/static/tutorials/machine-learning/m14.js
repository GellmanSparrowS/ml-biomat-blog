(() => {
 const root=document.getElementById('M14-lab');if(!root)return;
 const zh=document.documentElement.lang.startsWith('zh'),get=id=>document.getElementById('M14-'+id);
 let p={a0:.5,a1:.5,a2:0,reverse:false,steps:3},result;
 const colors=[[1,0,0],[0,0,1],[0,1,0]],paint=['#c84a42','#176baf','#3a9764'];
 const names=zh?['红','蓝','绿']:['Red','Blue','Green'];
 function compute(){
  const order=p.reverse?[2,1,0]:[0,1,2],alpha=[p.a0,p.a1,p.a2];
  let transmission=1,color=[0,0,0],weights=[],incoming=[];
  order.forEach((id,k)=>{incoming.push(transmission);const weight=k<p.steps?transmission*alpha[id]:0;weights.push(weight);for(let j=0;j<3;j++)color[j]+=weight*colors[id][j];if(k<p.steps)transmission*=1-alpha[id];});
  color=color.map(v=>v+transmission);result={...p,order,weights,incoming,remaining:transmission,color,weightSum:weights.reduce((a,b)=>a+b,transmission)};
  let s='<rect width="940" height="380" rx="12" fill="#f7f9fb"/>';
  s+='<line x1="35" y1="100" x2="620" y2="100" stroke="#667887" stroke-width="3"/>';
  order.forEach((id,k)=>{const x=90+k*180;const active=k<p.steps;s+=`<rect x="${x}" y="50" width="65" height="125" fill="${paint[id]}" opacity="${.15+.7*alpha[id]}" stroke="${paint[id]}" stroke-dasharray="${active?'none':'5 4'}"/><text x="${x+32}" y="35" text-anchor="middle" font-size="16">${names[id]} α=${alpha[id].toFixed(2)}</text><text x="${x+32}" y="205" text-anchor="middle" font-size="14">T=${incoming[k].toFixed(3)}</text><text x="${x+32}" y="230" text-anchor="middle" font-size="14">w=${weights[k].toFixed(3)}</text>`;
    s+=`<rect x="${x}" y="${335-weights[k]*85}" width="65" height="${weights[k]*85}" fill="${paint[id]}"/>`;
  });
  const rgb=color.map(v=>Math.round(v*255)).join(',');
  s+=`<rect x="700" y="55" width="175" height="150" fill="rgb(${rgb})" stroke="#bcc6ce"/><text x="787" y="35" text-anchor="middle" font-size="16">${zh?'合成像素':'Composited pixel'}</text><text x="787" y="235" text-anchor="middle" font-size="14">RGB (${color.map(v=>v.toFixed(3)).join(', ')})</text><text x="787" y="270" text-anchor="middle" font-size="14">${zh?'白背景权重':'White background'} ${transmission.toFixed(3)}</text><text x="787" y="300" text-anchor="middle" font-size="14">Σw + T = ${result.weightSum.toFixed(6)}</text>`;
  s+=`<text x="90" y="365" font-size="14">${zh?'颜色权重（无量纲，柱高0至1）':'Contribution weights (dimensionless, bar heights 0–1)'}</text>`;
  get('svg').innerHTML=s;
  for(const key of ['a0','a1','a2'])get(key).value=p[key];get('reverse').checked=p.reverse;
  get('status').textContent=zh?`完成 ${p.steps}/3 层，剩余透射率 ${transmission.toFixed(4)}。下一层只使用尚未被前层截获的权重。`:`Processed ${p.steps}/3 layers; remaining transmittance ${transmission.toFixed(4)}. Each next layer uses only the weight surviving earlier layers.`;
 }
 function set(v={}){for(const k of ['a0','a1','a2'])if(v[k]!==undefined)p[k]=Math.max(0,Math.min(1,Number(v[k])));if(v.reverse!==undefined)p.reverse=Boolean(v.reverse);if(v.steps!==undefined)p.steps=Math.max(0,Math.min(3,Math.floor(Number(v.steps))));compute();return state();}
 function state(){return JSON.parse(JSON.stringify(result));}
 function reset(){p={a0:.5,a1:.5,a2:0,reverse:false,steps:3};compute();return state();}
 for(const k of ['a0','a1','a2'])get(k).addEventListener('input',e=>set({[k]:e.target.value}));
 get('reverse').addEventListener('change',e=>set({reverse:e.target.checked}));
 get('step').addEventListener('click',()=>set({steps:p.steps+1}));get('restart').addEventListener('click',()=>set({steps:0}));get('reset').addEventListener('click',reset);
 window.CourseLab={set,state,reset};compute();
})();

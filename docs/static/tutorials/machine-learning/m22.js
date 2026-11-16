(() => {
  const root = document.getElementById('M22-lab'); if (!root) return;
  const zh = document.documentElement.lang.startsWith('zh');
  const get = id => document.getElementById('M22-' + id);
  let parameters = {mode:'mean', first:1, extra:false, steps:0};
  let values, matrix;
  const positions = [[70,105],[170,55],[280,65],[365,145],[215,170]];
  function calculate() {
    const a = Array.from({length:5},(_,i)=>Array.from({length:5},(_,j)=>i===j?1:0));
    for (let i=0;i<4;i++) a[i][i+1]=a[i+1][i]=1;
    if(parameters.extra) a[0][4]=a[4][0]=1;
    const degree=a.map(row=>row.reduce((s,v)=>s+v,0));
    matrix=a.map((row,i)=>row.map((v,j)=>parameters.mode==='sum'?v:parameters.mode==='gcn'?v/Math.sqrt(degree[i]*degree[j]):v/degree[i]));
    values=[parameters.first,3,5,2,4];
    for(let t=0;t<parameters.steps;t++) values=matrix.map(row=>row.reduce((s,v,j)=>s+v*values[j],0));
    let content='<rect width="940" height="390" fill="#f7f9fb" rx="12"/>';
    for(let i=0;i<5;i++)for(let j=i+1;j<5;j++)if(a[i][j])content+=`<line x1="${positions[i][0]}" y1="${positions[i][1]}" x2="${positions[j][0]}" y2="${positions[j][1]}" stroke="#9cabb7" stroke-width="3"/>`;
    positions.forEach(([x,y],i)=>{content+=`<circle cx="${x}" cy="${y}" r="27" fill="#176b91"/><text x="${x}" y="${y-4}" text-anchor="middle" fill="white" font-size="13">${i+1}</text><text x="${x}" y="${y+13}" text-anchor="middle" fill="white" font-size="13">${values[i].toFixed(2)}</text>`;});
    content+=`<text x="650" y="25" text-anchor="middle" font-size="15">${zh?'传播矩阵：行接收，列发送':'Propagation matrix: row receives, column sends'}</text>`;
    matrix.forEach((row,i)=>row.forEach((v,j)=>{const x=510+j*58,y=45+i*33;content+=`<rect x="${x}" y="${y}" width="54" height="30" fill="${v?'#d5e6ed':'#eef0f2'}"/><text x="${x+27}" y="${y+20}" text-anchor="middle" font-size="13">${v.toFixed(2)}</text>`;}));
    const high=Math.max(...values,1), baseline=345;
    values.forEach((v,i)=>{const x=130+i*155,h=v/high*100;content+=`<rect x="${x}" y="${baseline-h}" width="65" height="${h}" fill="#bb554d"/><text x="${x+32}" y="${baseline-h-8}" text-anchor="middle" font-size="14">${v.toFixed(3)}</text><text x="${x+32}" y="370" text-anchor="middle" font-size="13">${zh?'节点':'Node'} ${i+1}</text>`;});
    content+=`<text x="30" y="220" font-size="14">${zh?'信号（无量纲）；柱高按当前最大值缩放':'Signal (dimensionless); bar heights scale to the current maximum'}</text>`;
    get('svg').innerHTML=content;
    get('status').textContent=zh?`已传播 ${parameters.steps} 步；初始信号 [${parameters.first}, 3, 5, 2, 4]。当前节点1 = ${values[0].toFixed(6)}。`:`${parameters.steps} propagation steps; initial signal [${parameters.first}, 3, 5, 2, 4]. Current node 1 = ${values[0].toFixed(6)}.`;
    get('mode').value=parameters.mode;get('first').value=parameters.first;get('extra').checked=parameters.extra;
  }
  function set(p={}) {
    if(['mean','sum','gcn'].includes(p.mode))parameters.mode=p.mode;
    if(p.first!==undefined)parameters.first=Math.max(0,Math.min(8,Number(p.first)));
    if(p.extra!==undefined)parameters.extra=Boolean(p.extra);
    if(p.steps!==undefined)parameters.steps=Math.max(0,Math.min(20,Math.floor(Number(p.steps))));
    calculate();return state();
  }
  function state(){return {...parameters,values:[...values],matrix:matrix.map(row=>[...row])};}
  function reset(){parameters={mode:'mean',first:1,extra:false,steps:0};calculate();return state();}
  get('mode').addEventListener('change',e=>set({mode:e.target.value}));
  get('first').addEventListener('input',e=>set({first:e.target.value}));
  get('extra').addEventListener('change',e=>set({extra:e.target.checked}));
  get('step').addEventListener('click',()=>set({steps:parameters.steps+1}));
  get('reset').addEventListener('click',reset);
  window.CourseLab={set,state,reset};calculate();
})();

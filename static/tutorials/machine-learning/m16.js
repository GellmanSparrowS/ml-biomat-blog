(()=>{
 const get=id=>document.getElementById('M16-'+id);if(!get('lab'))return;const zh=document.documentElement.lang.startsWith('zh');let p={rank:1,alpha:1,x0:1,x1:2},result;
 const multiply=(a,b)=>a.map(row=>b[0].map((_,j)=>row.reduce((s,v,k)=>s+v*b[k][j],0)));
 function compute(){
  const A=[[1,1],[1,-1]].slice(0,p.rank),B=[[.5,.25],[-.25,.5]].map(row=>row.slice(0,p.rank)),base=[[1,0],[0,1]],x=[[p.x0],[p.x1]],delta=multiply(B,A).map(row=>row.map(v=>v*p.alpha/p.rank)),merged=base.map((row,i)=>row.map((v,j)=>v+delta[i][j]));
  const hidden=multiply(A,x).map(row=>row[0]),deltaOutput=multiply(delta,x).map(row=>row[0]),output=deltaOutput.map((v,i)=>v+x[i][0]),mergedOutput=multiply(merged,x).map(row=>row[0]);
  result={...p,A,B,delta,merged,hidden,deltaOutput,output,mergedOutput,error:Math.max(...output.map((v,i)=>Math.abs(v-mergedOutput[i])))};
  let s='<rect width="940" height="500" rx="12" fill="#f7f9fb"/>';
  function matrix(mat,x,y,title){s+=`<text x="${x}" y="${y-22}" font-size="17">${title}</text>`;mat.forEach((row,i)=>row.forEach((v,j)=>{const color=v>=0?'#e3edf3':'#f2e2d7';s+=`<rect x="${x+j*64}" y="${y+i*44}" width="60" height="40" rx="4" fill="${color}" stroke="#b7c7d0"/><text x="${x+j*64+30}" y="${y+i*44+26}" text-anchor="middle" font-size="16">${v.toFixed(2)}</text>`;}));}
  matrix(A,40,80,`A (${p.rank}×2)`);matrix(B,245,80,`B (2×${p.rank})`);matrix(delta,460,80,'ΔW = (α/r)BA');matrix(merged,720,80,'W₀ + ΔW');
  s+=`<text x="40" y="205" font-size="16">α/r = ${(p.alpha/p.rank).toFixed(3)}</text><text x="40" y="260" font-size="17">x = (${p.x0.toFixed(2)}, ${p.x1.toFixed(2)})</text><text x="40" y="305" font-size="17">Ax = (${hidden.map(v=>v.toFixed(3)).join(', ')})</text>`;
  s+=`<text x="460" y="250" font-size="17">${zh?'原输出 W₀x':'Base W₀x'} = (${p.x0.toFixed(3)}, ${p.x1.toFixed(3)})</text><text x="460" y="290" font-size="17">ΔWx = (${deltaOutput.map(v=>v.toFixed(3)).join(', ')})</text><text x="460" y="340" font-size="18" fill="#176b91">${zh?'两支路相加':'Add branches'}: (${output.map(v=>v.toFixed(3)).join(', ')})</text><text x="460" y="385" font-size="18" fill="#277d68">${zh?'合并矩阵计算':'Merged computation'}: (${mergedOutput.map(v=>v.toFixed(3)).join(', ')})</text>`;
  s+=`<text x="40" y="450" font-size="14">${zh?'矩阵格子显示真实数值；蓝底为非负，暖底为负。':'Cells display numerical values; blue is nonnegative and warm is negative.'}</text>`;get('svg').innerHTML=s;
  get('status').textContent=zh?`秩至多为 ${p.rank}，两条计算路径的最大差为 ${result.error.toExponential(2)}。原单位矩阵始终冻结。`:`Update rank is at most ${p.rank}; maximum difference between computation paths is ${result.error.toExponential(2)}. The original identity matrix remains frozen.`;
  Object.keys(p).forEach(k=>get(k).value=p[k]);
 }
 function state(){return JSON.parse(JSON.stringify(result));}function set(v={}){if(v.rank!==undefined)p.rank=Number(v.rank)>=2?2:1;for(const[k,lo,hi]of[['alpha',0,4],['x0',-3,3],['x1',-3,3]])if(v[k]!==undefined)p[k]=Math.max(lo,Math.min(hi,Number(v[k])));compute();return state();}function reset(){p={rank:1,alpha:1,x0:1,x1:2};compute();return state();}
 ['rank','alpha','x0','x1'].forEach(k=>get(k).addEventListener(k==='rank'?'change':'input',e=>set({[k]:e.target.value})));get('reset').addEventListener('click',reset);window.CourseLab={set,state,reset};compute();
})();

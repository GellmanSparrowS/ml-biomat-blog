(()=>{
 const get=id=>document.getElementById('M20-'+id);if(!get('lab'))return;const zh=document.documentElement.lang.startsWith('zh');let p={p0:.6,p1:.5,p2:.7},result;
 const collapse=path=>path.filter((s,i)=>s==='A'&&(i===0||s!==path[i-1])).join('')||'empty';
 function compute(){
  const probs=[p.p0,p.p1,p.p2],totals={empty:0,A:0,AA:0},paths=[];
  for(let n=0;n<8;n++){const path=[(n>>2)&1,(n>>1)&1,n&1].map(v=>v?'A':'_');const probability=path.reduce((v,s,i)=>v*(s==='A'?probs[i]:1-probs[i]),1);const output=collapse(path);totals[output]+=probability;paths.push({path,output,probability});}
  const greedy=collapse(probs.map(v=>v>.5?'A':'_')),best=Object.keys(totals).reduce((a,b)=>totals[b]>totals[a]?b:a);result={...p,probabilities:totals,greedy,best,total:Object.values(totals).reduce((a,b)=>a+b,0),paths};
  const name=v=>v==='empty'?(zh?'空序列':'Empty'):v,color={empty:'#8b9da6',A:'#176b91',AA:'#b96b35'};
  let s='<rect width="940" height="480" rx="12" fill="#f7f9fb"/>';
  s+=`<text x="30" y="30" font-size="17">${zh?'逐帧路径':'Frame path'}</text><text x="240" y="30" font-size="17">${zh?'折叠结果':'Collapsed'}</text><text x="410" y="30" font-size="17">${zh?'路径概率':'Path probability'}</text>`;
  paths.forEach((v,i)=>{const y=65+46*i;v.path.forEach((c,j)=>{s+=`<rect x="${30+j*55}" y="${y-19}" width="40" height="28" rx="4" fill="${c==='A'?'#d7e8ef':'#e5e9eb'}"/><text x="${50+j*55}" y="${y+1}" text-anchor="middle" font-size="17">${c==='_'?'∅':c}</text>`;});s+=`<text x="205" y="${y+1}" font-size="18">→</text><text x="260" y="${y+1}" font-size="16" fill="${color[v.output]}">${name(v.output)}</text><rect x="400" y="${y-15}" width="${130*v.probability}" height="20" fill="${color[v.output]}"/><text x="545" y="${y+1}" font-size="14">${v.probability.toFixed(4)}</text>`;});
  s+=`<text x="760" y="40" text-anchor="middle" font-size="17">${zh?'转写概率（0–1）':'Transcript probability (0–1)'}</text>`;
  Object.entries(totals).forEach(([k,v],i)=>{const y=115+i*110;s+=`<text x="650" y="${y-18}" font-size="16">${name(k)} ${v.toFixed(4)}</text><rect x="650" y="${y}" width="235" height="30" fill="#e1e7eb"/><rect x="650" y="${y}" width="${235*v}" height="30" fill="${color[k]}"/>`;});
  s+=`<text x="650" y="420" font-size="15">Σp = ${result.total.toFixed(6)}</text><text x="30" y="460" font-size="14">${zh?'∅ 表示空白；条宽与概率成正比。':'∅ denotes blank; bar widths are proportional to probability.'}</text>`;
  get('svg').innerHTML=s;get('status').textContent=zh?`贪心输出：${name(greedy)}；总概率最大的转写：${name(best)}。A—空白—A 保留为两个 A。`:`Greedy output: ${name(greedy)}; highest-probability transcript: ${name(best)}. A–blank–A retains two As.`;
  Object.keys(p).forEach(k=>get(k).value=p[k]);
 }
 function state(){return JSON.parse(JSON.stringify(result));}function set(v={}){for(const k of ['p0','p1','p2'])if(v[k]!==undefined)p[k]=Math.max(0,Math.min(1,Number(v[k])));compute();return state();}function reset(){p={p0:.6,p1:.5,p2:.7};compute();return state();}
 for(const k of ['p0','p1','p2'])get(k).addEventListener('input',e=>set({[k]:e.target.value}));get('reset').addEventListener('click',reset);window.CourseLab={set,state,reset};compute();
})();

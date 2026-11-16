(()=>{
 const get=id=>document.getElementById('M19-'+id);if(!get('lab'))return;const zh=document.documentElement.lang.startsWith('zh');let p={angle:0,temperature:1,includeThird:true},result;
 function compute(){
  const rad=p.angle*Math.PI/180,count=p.includeThird?3:2,angles=[0,Math.PI/2,Math.PI].slice(0,count),scores=angles.map(v=>Math.cos(rad-v));const logits=scores.map(v=>v/p.temperature),mx=Math.max(...logits),exp=logits.map(v=>Math.exp(v-mx)),sum=exp.reduce((a,b)=>a+b,0),probabilities=exp.map(v=>v/sum);
  result={...p,scores,probabilities,lossForA:-Math.log(probabilities[0]),normalizationSum:probabilities.reduce((a,b)=>a+b,0)};
  const X=v=>235+150*v,Y=v=>220-150*v;let s='<rect width="940" height="430" rx="12" fill="#f7f9fb"/>';
  s+=`<circle cx="235" cy="220" r="150" fill="white" stroke="#b8c8d3"/><line x1="65" y1="220" x2="405" y2="220" stroke="#b8c8d3"/><line x1="235" y1="50" x2="235" y2="390" stroke="#b8c8d3"/>`;
  const colors=['#69899b','#8b739c','#839c71'];angles.forEach((a,i)=>{s+=`<line x1="235" y1="220" x2="${X(Math.cos(a))}" y2="${Y(Math.sin(a))}" stroke="${colors[i]}" stroke-width="4"/><circle cx="${X(Math.cos(a))}" cy="${Y(Math.sin(a))}" r="5" fill="${colors[i]}"/><text x="${X(1.14*Math.cos(a))}" y="${Y(1.14*Math.sin(a))+5}" text-anchor="middle" font-size="17">${'ABC'[i]}</text>`;});
  s+=`<line x1="235" y1="220" x2="${X(Math.cos(rad))}" y2="${Y(Math.sin(rad))}" stroke="#bd632f" stroke-width="3" stroke-dasharray="8 4"/><circle cx="${X(Math.cos(rad))}" cy="${Y(Math.sin(rad))}" r="7" fill="none" stroke="#bd632f" stroke-width="3"/><text x="235" y="25" text-anchor="middle" font-size="17">${zh?'单位向量：橙色为图像':'Unit vectors: image in orange'}</text>`;
  s+=`<text x="500" y="45" font-size="16">${zh?'候选 / 余弦 / 归一化分数':'Candidate / cosine / normalized score'}</text>`;
  probabilities.forEach((v,i)=>{const y=115+100*i;s+=`<text x="500" y="${y-15}" font-size="17">${'ABC'[i]}   cos=${scores[i].toFixed(3)}   p=${v.toFixed(4)}</text><rect x="500" y="${y}" width="350" height="25" fill="#e0e8ed"/><rect x="500" y="${y}" width="${350*v}" height="25" fill="${colors[i]}"/>`;});
  s+=`<text x="500" y="405" font-size="14">${zh?'条宽表示 0 到 1，概率和':'Bar widths span 0–1; probability sum'} ${result.normalizationSum.toFixed(6)}</text>`;get('svg').innerHTML=s;
  get('status').textContent=zh?`方向 ${p.angle}°，温度 ${p.temperature.toFixed(2)}，候选 ${count} 个。若 A 是正确项，交叉熵为 ${result.lossForA.toFixed(4)}。`:`Direction ${p.angle}°, temperature ${p.temperature.toFixed(2)}, ${count} candidates. If A is the target, cross entropy is ${result.lossForA.toFixed(4)}.`;
  get('angle').value=p.angle;get('temperature').value=p.temperature;get('includeThird').checked=p.includeThird;
 }
 function state(){return JSON.parse(JSON.stringify(result));}function set(v={}){if(v.angle!==undefined)p.angle=Math.max(0,Math.min(180,Number(v.angle)));if(v.temperature!==undefined)p.temperature=Math.max(.1,Math.min(2,Number(v.temperature)));if(v.includeThird!==undefined)p.includeThird=Boolean(v.includeThird);compute();return state();}function reset(){p={angle:0,temperature:1,includeThird:true};compute();return state();}
 get('angle').addEventListener('input',e=>set({angle:e.target.value}));get('temperature').addEventListener('input',e=>set({temperature:e.target.value}));get('includeThird').addEventListener('change',e=>set({includeThird:e.target.checked}));get('reset').addEventListener('click',reset);window.CourseLab={set,state,reset};compute();
})();

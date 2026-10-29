document.querySelectorAll('[data-lab="CP09-I1"]').forEach(root=>{
 const z=root.dataset.lang==='zh',q=s=>root.querySelector('[data-field="'+s+'"]'),W=20,H=16,N=W*H;
 let seed=9071,edges=[];
 function prepare(){let state=seed>>>0;const rnd=()=>{state=(1664525*state+1013904223)>>>0;return state/4294967296};edges=[];for(let y=0;y<H;y++)for(let x=0;x<W;x++){const i=y*W+x;if(x<W-1)edges.push([i,i+1,rnd()]);if(y<H-1)edges.push([i,i+W,rnd()]);}}
 function draw(){const p=+q('p').value;q('pv').textContent=p.toFixed(2);const adj=Array.from({length:N},()=>[]),active=edges.filter(e=>e[2]<p);active.forEach(e=>{adj[e[0]].push(e[1]);adj[e[1]].push(e[0]);});const ids=Array(N).fill(-1),groups=[];
 for(let i=0;i<N;i++)if(ids[i]<0){const id=groups.length,stack=[i],members=[];let left=false,right=false;ids[i]=id;while(stack.length){const k=stack.pop();members.push(k);left=left||k%W===0;right=right||k%W===W-1;adj[k].forEach(j=>{if(ids[j]<0){ids[j]=id;stack.push(j);}});}groups.push({members,span:left&&right});}
 let largest=0;groups.forEach((g,i)=>{if(g.members.length>groups[largest].members.length)largest=i;});const spans=groups.some(g=>g.span),point=i=>[45+(i%W)*26.8,60+Math.floor(i/W)*26.8];let out='<rect width="600" height="510" fill="#f4f3ed"/><g font-family="Arial,sans-serif" font-size="22">';out+='<text x="35" y="30" fill="#173e45">'+(z?'寻找从左到右的连接':'Find a connection from left to right')+'</text><path d="M32 50 V472 M567 50 V472" stroke="#516970" stroke-width="4"/>';
 const colour=i=>groups[ids[i]].span?'#207d80':(!spans&&ids[i]===largest?'#ba6e3e':'#b9c5c5');
 active.forEach(e=>{const a=point(e[0]),b=point(e[1]);out+='<line x1="'+a[0]+'" y1="'+a[1]+'" x2="'+b[0]+'" y2="'+b[1]+'" stroke="'+colour(e[0])+'" stroke-width="4"/>';});for(let i=0;i<N;i++){const a=point(i);out+='<circle cx="'+a[0]+'" cy="'+a[1]+'" r="3.8" fill="'+colour(i)+'"/>';}
 out+='<text x="35" y="502" fill="#173e45">'+(z?'左右贯穿：':'Left-to-right spanning: ')+(spans?(z?'是':'yes'):(z?'否':'no'))+'</text></g>';q('plot').innerHTML=out;
 const frac=(100*active.length/edges.length).toFixed(1),big=groups[largest].members.length,bigpc=(100*big/N).toFixed(1);
 q('feedback').textContent=z?'p = '+p.toFixed(2)+'；实际保留 '+active.length+'/'+edges.length+' 条边（'+frac+'%）；'+groups.length+' 个集群；最大集群 '+big+'/'+N+' 个节点（'+bigpc+'%）。'+(spans?'存在左右贯穿集群。':'当前实现未形成左右贯穿。')+' 同一 p 更换实现可改变结果。':'p = '+p.toFixed(2)+'; retained '+active.length+'/'+edges.length+' edges ('+frac+'%); '+groups.length+' clusters; largest '+big+'/'+N+' nodes ('+bigpc+'%). '+(spans?'A left-to-right spanning cluster exists.':'This realization does not span left to right.')+' A new realization at the same p can change the outcome.';
 }
 q('p').addEventListener('input',draw);q('renew').addEventListener('click',()=>{seed=(seed+104729)>>>0;prepare();draw();});q('reset').addEventListener('click',()=>{seed=9071;q('p').value='0.5';prepare();draw();});prepare();draw();
});

(function(){
  const root=document.getElementById('I08-lab');if(!root)return;
  const zh=document.documentElement.lang.startsWith('zh'),tr=(a,b)=>zh?a:b;
  const N=48,total=N**3,plane=N*N;
  const encoded=JSON.parse(root.querySelector('#I08-data').textContent),volumes={};
  for(const [k,v] of Object.entries(encoded)){const binary=atob(v);volumes[k]=Uint8Array.from(binary,c=>c.charCodeAt(0));}
  const sig=root.querySelector('#I08-sigma'),th=root.querySelector('#I08-threshold'),slice=root.querySelector('#I08-slice');
  const canvas=root.querySelector('#I08-plot'),ctx=canvas.getContext('2d'),out=root.querySelector('#I08-result');
  let current={};
  function draw(){
    const sigma=Number(sig.value),threshold=Number(th.value),zslice=Number(slice.value),g=volumes[String(sigma)];
    const labels=new Uint32Array(total),queue=new Int32Array(total),spanning=[false];
    let count=0,components=0,spancount=0;
    for(let start=0;start<total;start++){
      if(g[start]>=threshold||labels[start])continue;
      components++;let head=0,tail=1,touches0=false,touches1=false;queue[0]=start;labels[start]=components;
      while(head<tail){
        const j=queue[head++],x=j%N,y=Math.floor(j/N)%N,z=Math.floor(j/plane);
        if(z===0)touches0=true;if(z===N-1)touches1=true;
        const near=[];if(x>0)near.push(j-1);if(x<N-1)near.push(j+1);if(y>0)near.push(j-N);if(y<N-1)near.push(j+N);if(z>0)near.push(j-plane);if(z<N-1)near.push(j+plane);
        for(const k of near)if(g[k]<threshold&&!labels[k]){labels[k]=components;queue[tail++]=k;}
      }
      count+=tail;spanning[components]=touches0&&touches1;if(spanning[components])spancount+=tail;
    }
    current={sigma,threshold,slice:zslice,pore_voxels:count,porosity:count/total,components,spanning_fraction:count?spancount/count:0,pore_volume_mm3:count*.01**3};
    ctx.fillStyle='#fbfcfc';ctx.fillRect(0,0,760,420);ctx.font='16px sans-serif';ctx.textAlign='center';ctx.fillStyle='#18344a';
    ctx.fillText(tr('灰度截面','Gray section'),200,25);ctx.fillText(tr('绿色：连接z两端的孔隙','Green: pores spanning both z faces'),570,25);
    const scale=6;
    for(let y=0;y<N;y++)for(let x=0;x<N;x++){
      const j=zslice*plane+y*N+x,v=g[j],label=labels[j];ctx.fillStyle=`rgb(${v},${v},${v})`;ctx.fillRect(55+x*scale,50+(N-1-y)*scale,scale,scale);
      ctx.fillStyle=!label?'#182c38':spanning[label]?'#188777':'#d27839';ctx.fillRect(425+x*scale,50+(N-1-y)*scale,scale,scale);
    }
    ctx.fillStyle='#18344a';ctx.fillText('x: 0–0.48 mm',200,365);ctx.fillText('x: 0–0.48 mm',570,365);
    ctx.fillText(tr('y方向向上 · 当前z切片','y increases upward · z section')+` ${zslice} / 47`,380,398);
    out.textContent=tr('三维孔隙率','3D porosity')+` ${(100*current.porosity).toFixed(3)}% · `+tr('贯通孔隙比例','Spanning pore fraction')+` ${(100*current.spanning_fraction).toFixed(2)}% · `+tr('孔隙体素','Pore voxels')+` ${count} · `+tr('独立团簇','Components')+` ${components} · σ=${sigma} voxel · T=${threshold}`;
    return {...current};
  }
  const reset=()=>{sig.value='1';th.value=128;slice.value=24;return draw();};
  const set=p=>{if(p.sigma!==undefined)sig.value=String(p.sigma);if(p.threshold!==undefined)th.value=p.threshold;if(p.slice!==undefined)slice.value=p.slice;return draw();};
  const button=root.querySelector('#I08-reset');for(const c of [sig,th,slice])c.addEventListener('input',draw);button.addEventListener('click',reset);
  window.CourseLab={set,state:()=>({...current}),reset,destroy:()=>{for(const c of [sig,th,slice])c.removeEventListener('input',draw);button.removeEventListener('click',reset);}};reset();
})();

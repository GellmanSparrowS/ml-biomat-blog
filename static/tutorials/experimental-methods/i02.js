(() => {
  const zh=document.documentElement.lang.startsWith('zh'),data=JSON.parse(document.getElementById('I02-data').textContent);
  const slider=document.getElementById('I02-slice'),select=document.getElementById('I02-mode'),img=document.getElementById('I02-image'),out=document.getElementById('I02-result');
  const value={slice:0,mode:'slice'};
  function draw(){img.src=value.mode==='slice'?data.slices[value.slice]:data[value.mode];const z=value.slice*1.25;out.textContent=value.mode==='slice'?(zh?`第${value.slice}层；z=${z.toFixed(2)} μm；原始平面平均数字量=${data.means[value.slice].toFixed(2)}。`:`Slice ${value.slice}; z=${z.toFixed(2)} μm; original plane-mean digital number=${data.means[value.slice].toFixed(2)}.`):(zh?`${value.mode==='max'?'最大':'平均'}投影：由16层组成，首末中心间距18.75 μm。回到单层查看深度位置。`:`${value.mode==='max'?'Maximum':'Mean'} projection of 16 planes; first-to-last center distance 18.75 μm. Return to a section to inspect depth.`);slider.disabled=value.mode!=='slice';}
  function set(p){if('slice' in p)value.slice=Math.max(0,Math.min(15,Math.round(Number(p.slice)||0)));if(['slice','max','mean'].includes(p.mode))value.mode=p.mode;slider.value=value.slice;select.value=value.mode;draw();}
  const sf=()=>set({slice:slider.value}),mf=()=>set({mode:select.value}),reset=()=>set({slice:0,mode:'slice'}),button=document.getElementById('I02-reset');slider.addEventListener('input',sf);select.addEventListener('change',mf);button.addEventListener('click',reset);
  window.CourseLab={set,state:()=>({...value,z_um:value.slice*1.25,plane_mean:data.means[value.slice]}),reset,destroy(){slider.removeEventListener('input',sf);select.removeEventListener('change',mf);button.removeEventListener('click',reset);}};draw();
})();

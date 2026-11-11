(()=>{'use strict';
const language=root=>root.closest('[data-lang]')?.dataset.lang||document.documentElement.lang.slice(0,2);
document.querySelectorAll('.code-example').forEach(root=>{
 const code=root.querySelector('code'),copy=root.querySelector('[data-copy-code]'),download=root.querySelector('[data-download-code]');
 copy.addEventListener('click',async()=>{
  let ok=false;
  try{await navigator.clipboard.writeText(code.textContent);ok=true}catch{
   const text=document.createElement('textarea');text.value=code.textContent;text.setAttribute('aria-hidden','true');text.style.position='fixed';text.style.left='-10000px';document.body.append(text);text.select();ok=document.execCommand('copy');text.remove();copy.focus();
  }
  copy.textContent=language(root)==='zh'?(ok?'已复制':'请选择代码复制'):(ok?'Copied':'Select code to copy');
  copy.dataset.copySuccess=String(ok);
  setTimeout(()=>copy.textContent=language(root)==='zh'?'复制':'Copy',1800);
 });
 download.addEventListener('click',()=>{
  const blob=new Blob([code.textContent],{type:'text/plain;charset=utf-8'}),url=URL.createObjectURL(blob),a=document.createElement('a');
  a.href=url;a.download=download.dataset.filename;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);
 });
});
function initializeTrajectory(root){
 const data=root.trajectoryPayload,canvas=root.querySelector('canvas'),ctx=canvas.getContext('2d'),slider=root.querySelector('[data-frame]'),play=root.querySelector('[data-play]'),reset=root.querySelector('[data-reset]'),out=root.querySelector('[data-time]'),zh=language(root)==='zh';
 const frames=data.frames,times=data.times,atoms=data.atoms||[],bonds=data.bonds||[],unit=data.time_unit||'ps',hasBox=data.box?.length===3||(data.boxes||[]).some(b=>b.length===3);
 let index=0,playing=false,raf=0,last=0,yaw=.55,pitch=.28,drag=null,zoom=1;
 let solventVisible=data.solvent_visible!==false;
 let viewMode=solventVisible&&hasBox?'box':'selection';
 const controls=root.querySelector('.trajectory-controls'),camera=document.createElement('div');camera.className='trajectory-camera';
 const zoomLabel=document.createElement('label'),zoomInput=document.createElement('input'),zoomValue=document.createElement('output');zoomInput.type='range';zoomInput.min='.5';zoomInput.max='4';zoomInput.step='.05';zoomInput.value='1';zoomInput.dataset.zoom='';zoomLabel.append(document.createTextNode(zh?'缩放':'Zoom'),zoomInput,zoomValue);
 const fitSelection=document.createElement('button'),fitBox=document.createElement('button');fitSelection.type=fitBox.type='button';fitSelection.dataset.fitSelection='';fitBox.dataset.fitBox='';fitSelection.textContent=zh?'查看粒子':'Fit particles';fitBox.textContent=zh?'查看盒子':'Fit box';camera.append(zoomLabel,fitSelection,fitBox);controls.after(camera);
 fitBox.hidden=!hasBox;
 const status=document.createElement('p'),hint=document.createElement('p');status.className='trajectory-status';status.dataset.particleCount='';hint.className='trajectory-hint';hint.textContent=zh?'拖动旋转；聚焦图形后用方向键旋转，用 + / − 缩放。':'Drag to rotate. With the figure focused, arrow keys rotate and + / − zoom.';canvas.before(status);camera.after(hint);
 const hasSolvent=atoms.some(a=>a.role==='solvent')||(data.atom_frames||[]).some(frame=>frame.some(a=>a.role==='solvent'));
 if(hasSolvent){const label=document.createElement('label'),input=document.createElement('input');label.className='solvent-toggle';input.type='checkbox';input.checked=solventVisible;input.dataset.showSolvent='';label.append(input,document.createTextNode(zh?'显示溶剂':'Show solvent'));controls.append(label);input.addEventListener('change',()=>{solventVisible=input.checked;viewMode=solventVisible&&hasBox?'box':'selection';zoom=1;updateCamera();draw();});}
 if(data.legend?.length){const legend=document.createElement('div');legend.className='trajectory-legend';for(const item of data.legend){const label=document.createElement('span'),swatch=document.createElement('i');swatch.style.background=item.color;swatch.setAttribute('aria-hidden','true');label.append(swatch,document.createTextNode(item.label[zh?'zh':'en']));legend.append(label);}root.querySelector('.trajectory-controls').after(legend);}
 const fullBounds=[[Infinity,-Infinity],[Infinity,-Infinity],[Infinity,-Infinity]],soluteBounds=[[Infinity,-Infinity],[Infinity,-Infinity],[Infinity,-Infinity]],boxBounds=[[Infinity,-Infinity],[Infinity,-Infinity],[Infinity,-Infinity]];
 for(let f=0;f<frames.length;f++){const a=data.atom_frames?.[f]||atoms;for(let i=0;i<frames[f].length;i++)for(let k=0;k<3;k++){const v=frames[f][i][k];fullBounds[k][0]=Math.min(fullBounds[k][0],v);fullBounds[k][1]=Math.max(fullBounds[k][1],v);if(a[i]?.role!=='solvent'){soluteBounds[k][0]=Math.min(soluteBounds[k][0],v);soluteBounds[k][1]=Math.max(soluteBounds[k][1],v);}}const box=data.boxes?.[f]||data.box;if(box?.length===3)for(let k=0;k<3;k++){boxBounds[k][0]=Math.min(boxBounds[k][0],0);boxBounds[k][1]=Math.max(boxBounds[k][1],box[k]);}}
 let center=[0,0,0],scale=1;
 const colors={H:'#b8d5df',C:'#4d5b60',N:'#2e63bf',O:'#c94b42',S:'#cba62a',P:'#ac7139'};
 function updateCamera(){
  const bounds=viewMode==='box'&&Number.isFinite(boxBounds[0][0])?boxBounds:!solventVisible&&Number.isFinite(soluteBounds[0][0])?soluteBounds:fullBounds;center=bounds.map(b=>(b[0]+b[1])/2);
  const corners=[];for(let a=0;a<2;a++)for(let b=0;b<2;b++)for(let c=0;c<2;c++)corners.push([bounds[0][a],bounds[1][b],bounds[2][c]]);
  scale=1;const projected=corners.map(project),width=Math.max(...projected.map(p=>p[0]))-Math.min(...projected.map(p=>p[0])),height=Math.max(...projected.map(p=>p[1]))-Math.min(...projected.map(p=>p[1]));scale=Math.min(760/Math.max(width,1e-6),470/Math.max(height,1e-6))*zoom;
  zoomInput.value=String(zoom);zoomValue.textContent=zoom.toFixed(2)+'×';fitSelection.setAttribute('aria-pressed',String(viewMode==='selection'));fitBox.setAttribute('aria-pressed',String(viewMode==='box'));root.dataset.zoom=String(zoom);root.dataset.viewMode=viewMode;
 }
 function project(p){const x=p[0]-center[0],y=p[1]-center[1],z=p[2]-center[2],x1=x*Math.cos(yaw)+z*Math.sin(yaw),z1=-x*Math.sin(yaw)+z*Math.cos(yaw);return [450+x1*scale,285-(y*Math.cos(pitch)-z1*Math.sin(pitch))*scale,y*Math.sin(pitch)+z1*Math.cos(pitch)];}
 function draw(){
  ctx.fillStyle='#f5f7f6';ctx.fillRect(0,0,900,600);const points=frames[index].map(project),frameAtoms=data.atom_frames?.[index]||atoms,frameBonds=data.bond_frames?.[index]||bonds,n=points.length,visible=points.map((p,i)=>solventVisible||frameAtoms[i]?.role!=='solvent'),visibleCount=visible.filter(Boolean).length;
  const box=data.boxes?.[index]||data.box;
  if(box?.length===3){const corners=[];for(let a=0;a<2;a++)for(let b=0;b<2;b++)for(let c=0;c<2;c++)corners.push(project([a*box[0],b*box[1],c*box[2]]));ctx.strokeStyle='#aebbb6';ctx.lineWidth=1.5;for(let a=0;a<8;a++)for(const mask of [1,2,4]){const b=a^mask;if(b>a){ctx.beginPath();ctx.moveTo(...corners[a].slice(0,2));ctx.lineTo(...corners[b].slice(0,2));ctx.stroke();}}}
  ctx.strokeStyle='#7b8985';ctx.lineWidth=3;
  for(const [a,b] of frameBonds){if(!points[a]||!points[b]||!visible[a]||!visible[b])continue;if(box&&frames[index][a].some((v,k)=>Math.abs(v-frames[index][b][k])>box[k]*.5))continue;ctx.beginPath();ctx.moveTo(points[a][0],points[a][1]);ctx.lineTo(points[b][0],points[b][1]);ctx.stroke();}
  const order=points.map((p,i)=>({p,i})).filter(({i})=>visible[i]).sort((a,b)=>a.p[2]-b.p[2]);
  for(const {p,i} of order){const atom=frameAtoms[i]||{},r=Math.max(2.4,Math.min(13,(atom.radius||.09)*scale));ctx.beginPath();ctx.arc(p[0],p[1],r,0,Math.PI*2);ctx.fillStyle=atom.color||colors[atom.element]||'#147b69';ctx.fill();}
  const t=times?times[index]:index,phase=(data.stages||[]).find((v,i,a)=>t>=v.start&&(t<v.end||(i===a.length-1&&t<=v.end)));
  status.textContent=(zh?'显示粒子数：':'Displayed particles: ')+visibleCount+(visibleCount<n?' / '+n:'');
  if(data.coordinate_unit){const ideal=150/scale,power=10**Math.floor(Math.log10(ideal)),bar=[1,2,5,10].map(v=>v*power).filter(v=>v<=ideal).at(-1)||power,px=bar*scale;ctx.strokeStyle='#223c35';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(28,548);ctx.lineTo(28+px,548);ctx.stroke();ctx.fillStyle='#223c35';const font=Math.max(17,Math.min(43,13*900/Math.max(canvas.clientWidth,270)));ctx.font=font+'px Segoe UI, Microsoft YaHei, sans-serif';ctx.fillText(Number(bar.toPrecision(3))+' '+data.coordinate_unit,28,548+font+5);}
  slider.value=String(index);out.textContent=(zh?'第 ':'Frame ')+(index+1)+' / '+frames.length+' · '+Number(t).toPrecision(5)+' '+unit+(phase?' · '+phase.label[zh?'zh':'en']:'');root.dataset.currentFrame=String(index);root.dataset.visibleAtoms=String(visibleCount);root.dataset.frameAtoms=String(n);
 }
 function stop(){playing=false;cancelAnimationFrame(raf);play.textContent=zh?'播放':'Play';play.setAttribute('aria-pressed','false');}
 function tick(t){if(!playing)return;if(t-last>160){index=(index+1)%frames.length;draw();last=t;}raf=requestAnimationFrame(tick);}
 play.setAttribute('aria-pressed','false');play.addEventListener('click',()=>{if(playing){stop();return;}playing=true;play.textContent=zh?'暂停':'Pause';play.setAttribute('aria-pressed','true');last=performance.now();raf=requestAnimationFrame(tick);});
 reset.addEventListener('click',()=>{stop();index=0;yaw=.55;pitch=.28;zoom=1;solventVisible=data.solvent_visible!==false;viewMode=solventVisible&&hasBox?'box':'selection';const toggle=root.querySelector('[data-show-solvent]');if(toggle)toggle.checked=solventVisible;updateCamera();draw();});slider.addEventListener('input',()=>{stop();index=Number(slider.value);draw();});
 zoomInput.addEventListener('input',()=>{zoom=Number(zoomInput.value);updateCamera();draw();});fitSelection.addEventListener('click',()=>{viewMode='selection';zoom=1;updateCamera();draw();});fitBox.addEventListener('click',()=>{viewMode='box';zoom=1;updateCamera();draw();});
 canvas.tabIndex=0;canvas.addEventListener('pointerdown',e=>{drag=[e.clientX,e.clientY];canvas.setPointerCapture(e.pointerId);});canvas.addEventListener('pointermove',e=>{if(!drag)return;yaw+=(e.clientX-drag[0])*.008;pitch=Math.max(-1.5,Math.min(1.5,pitch+(e.clientY-drag[1])*.008));drag=[e.clientX,e.clientY];updateCamera();draw();});canvas.addEventListener('pointerup',()=>drag=null);canvas.addEventListener('pointercancel',()=>drag=null);
 canvas.addEventListener('keydown',e=>{if(!['ArrowLeft','ArrowRight','ArrowUp','ArrowDown','+','=','-'].includes(e.key))return;e.preventDefault();if(['+','=','-'].includes(e.key))zoom=Math.max(.5,Math.min(4,zoom*(e.key==='-'?1/1.25:1.25)));else{yaw+=(e.key==='ArrowRight'?.08:e.key==='ArrowLeft'?-.08:0);pitch=Math.max(-1.5,Math.min(1.5,pitch+(e.key==='ArrowDown'?.08:e.key==='ArrowUp'?-.08:0)));}updateCamera();draw();});
 document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});document.addEventListener('course:language',()=>{stop();draw();});matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change',()=>stop());new ResizeObserver(()=>draw()).observe(canvas);updateCamera();draw();
}
async function loadTrajectory(root){
 if(root.dataset.loading||root.dataset.loaded)return;root.dataset.loading='true';root.setAttribute('aria-busy','true');
 const controls=[...root.querySelectorAll('button,input')];controls.forEach(el=>el.disabled=true);
 try{
  const script=root.querySelector('.trajectory-data');
  if(script.dataset.src){const response=await fetch(script.dataset.src);if(!response.ok)throw new Error('Trajectory load');root.trajectoryPayload=await response.json();}
  else{root.trajectoryPayload=JSON.parse(script.textContent);}initializeTrajectory(root);root.dataset.loaded='true';observer?.unobserve(root);
  root.querySelector('[data-retry-trajectory]')?.remove();
 }catch(error){
  if(!root.querySelector('[data-retry-trajectory]')){const retry=document.createElement('button');retry.type='button';retry.dataset.retryTrajectory='';retry.textContent=language(root)==='zh'?'重新加载轨迹':'Reload trajectory';retry.onclick=()=>loadTrajectory(root);root.append(retry);}
 }finally{delete root.dataset.loading;root.removeAttribute('aria-busy');controls.forEach(el=>el.disabled=false);}
}
const observer='IntersectionObserver' in window?new IntersectionObserver(entries=>{for(const entry of entries)if(entry.isIntersecting)loadTrajectory(entry.target);},{rootMargin:'600px'}):null;
document.querySelectorAll('.trajectory-player').forEach(root=>{root.querySelectorAll('button,input').forEach(el=>el.disabled=true);if(observer)observer.observe(root);else loadTrajectory(root);});
})();

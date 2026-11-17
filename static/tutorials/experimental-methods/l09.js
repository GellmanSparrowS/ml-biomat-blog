(() => {
  if(window.CourseLab&&window.CourseLab.destroy)window.CourseLab.destroy();
  const root=document.getElementById('L09-lab');if(!root)return;
  const zh=document.documentElement.lang.startsWith('zh');
  const T=(z,e)=>zh?z:e;const svg=root.querySelector('svg');
  const ns='http://www.w3.org/2000/svg';const defaults={spill:.25,threshold:150,cofactor:50};
  const controls=Object.fromEntries(Object.keys(defaults).map(k=>[k,root.querySelector('#L09-'+k)]));
  const events=Array.from({length:240},(_,i)=>{
    const group=Math.floor(i/60),j=i%60;
    const x=(group%2?1000:20)+(group%2?120:12)*Math.sin(j*2.399);
    const y=(group>=2?300:20)+(group>=2?35:10)*Math.cos(j*1.73);
    return [x+.05*y+3*Math.cos(j*.47),.25*x+y+4*Math.sin(j*.81)];
  });let result={};const listeners=[];
  function node(tag,attrs,text,parent=svg){const e=document.createElementNS(ns,tag);Object.entries(attrs).forEach(([k,v])=>e.setAttribute(k,v));if(text!==undefined)e.textContent=text;parent.appendChild(e);return e;}
  function update(){
    const p=Object.fromEntries(Object.entries(controls).map(([k,e])=>[k,Number(e.value)]));
    const den=1-.05*p.spill;const comp=events.map(([a,b])=>[(a-.05*b)/den,(b-p.spill*a)/den]);
    const yPositive=comp.filter(e=>e[1]>p.threshold).length;
    const doublePositive=comp.filter(e=>e[0]>400&&e[1]>p.threshold).length;
    result={...p,events:240,yPositive,doublePositive,yPercent:100*yPositive/240,doublePercent:100*doublePositive/240,negativeY:comp.filter(e=>e[1]<0).length};
    Object.entries(p).forEach(([k,v])=>root.querySelector('#L09-'+k+'-value').textContent=k==='spill'?(100*v).toFixed(0)+'%':v.toFixed(0));
    root.querySelector('#L09-result').textContent=T(`Y阳性 ${yPositive}/240（${result.yPercent.toFixed(1)}%）；X/Y双阳性 ${doublePositive}/240（${result.doublePercent.toFixed(1)}%）。补偿Y小于零：${result.negativeY}个事件。`,`Y-positive ${yPositive}/240 (${result.yPercent.toFixed(1)}%); X/Y double-positive ${doublePositive}/240 (${result.doublePercent.toFixed(1)}%). Negative compensated Y: ${result.negativeY} events.`);
    svg.replaceChildren();node('title',{},T('同一事件集的混合信号和补偿结果','Mixed signals and compensated values for the same events'));
    const w=282,h=285,top=66,origins=[55,415],tr=x=>Math.asinh(x/p.cofactor);
    const px=(v,o)=>o+(v+4)/9*w,py=v=>top+h-(v+4)/9*h;
    [events,comp].forEach((data,panel)=>{
      const o=origins[panel];node('text',{x:o+w/2,y:28,'text-anchor':'middle',fill:'#23434b','font-size':15},panel?T('补偿后：紫色为双阳性','Compensated: purple is double-positive'):T('扣基线的混合信号','Background-corrected mixture'));
      node('rect',{x:o,y:top,width:w,height:h,fill:'#fffdf7',stroke:'#b5c8cd'});
      [-4,-2,0,2,4].forEach(t=>{
        node('line',{x1:px(t,o),x2:px(t,o),y1:top,y2:top+h,stroke:'#dae4e5','stroke-width':.6});
        node('line',{x1:o,x2:o+w,y1:py(t),y2:py(t),stroke:'#dae4e5','stroke-width':.6});
        node('text',{x:px(t,o),y:top+h+19,'text-anchor':'middle','font-size':12,fill:'#36545d'},t);
        node('text',{x:o-9,y:py(t)+4,'text-anchor':'end','font-size':12,fill:'#36545d'},t);
      });
      const xGate=tr(400),yGate=tr(p.threshold);
      if(panel){node('rect',{x:px(xGate,o),y:top,width:o+w-px(xGate,o),height:py(yGate)-top,fill:'#8160a1',opacity:.08});}
      data.forEach((e,i)=>{
        const selected=panel&&comp[i][0]>400&&comp[i][1]>p.threshold;
        const dot=node('circle',{cx:px(tr(e[0]),o),cy:py(tr(e[1])),r:2.6,fill:selected?'#8160a1':'#186e83',opacity:.42});
        node('title',{},panel?`${i+1}: X=${e[0].toFixed(1)}, Y=${e[1].toFixed(1)}`:`${i+1}: detector 1=${e[0].toFixed(1)}, detector 2=${e[1].toFixed(1)}`,dot);
      });
      if(panel){node('line',{x1:px(xGate,o),x2:px(xGate,o),y1:top,y2:top+h,stroke:'#cd803f','stroke-dasharray':'5 3'});node('line',{x1:o,x2:o+w,y1:py(yGate),y2:py(yGate),stroke:'#cd803f','stroke-dasharray':'5 3'});}
      node('text',{x:o+w/2,y:top+h+46,'text-anchor':'middle','font-size':13,fill:'#23434b'},panel?'asinh(X / c)':'asinh(detector 1 / c)');
      node('text',{transform:`translate(${o-39},${top+h/2}) rotate(-90)`,'text-anchor':'middle','font-size':13,fill:'#23434b'},panel?'asinh(Y / c)':'asinh(detector 2 / c)');
    });
    node('text',{x:380,y:433,'text-anchor':'middle','font-size':13,fill:'#36545d'},T('同一240事件；阈值在原信号尺度定义，随显示坐标一起变换。','Same 240 events; signal-scale thresholds transform with the display.'));
  }
  function set(p={}){Object.entries(p).forEach(([k,v])=>{if(controls[k])controls[k].value=String(v);});update();return {...result};}
  function on(e,type,fn){e.addEventListener(type,fn);listeners.push([e,type,fn]);}
  Object.values(controls).forEach(e=>on(e,'input',update));
  on(root.querySelector('#L09-skip'),'click',()=>set({spill:0}));
  on(root.querySelector('#L09-reset'),'click',()=>set(defaults));
  window.CourseLab={set,state:()=>({...result}),reset:()=>set(defaults),destroy:()=>listeners.forEach(([e,t,f])=>e.removeEventListener(t,f))};
  set(defaults);
})();

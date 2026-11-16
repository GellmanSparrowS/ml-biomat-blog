(() => {
  'use strict';
  const zh=document.documentElement.lang.startsWith('zh');
  const get=id=>document.getElementById('M29-'+id);
  const svg=get('board'), ns='http://www.w3.org/2000/svg';
  let k=.35,h=1,method='euler',answer={};
  function element(tag,attributes,text){
    const node=document.createElementNS(ns,tag);
    Object.entries(attributes).forEach(([name,value])=>node.setAttribute(name,value));
    if(text!==undefined)node.textContent=text;
    svg.append(node);return node;
  }
  function factor(z){return method==='euler'?1-z:1-z+z*z/2-z*z*z/6+z*z*z*z/24;}
  function render(){
    const points=[[0,80]];
    while(points.at(-1)[0]<12-1e-10){
      const [t,T]=points.at(-1),dt=Math.min(h,12-t);
      points.push([t+dt,20+(T-20)*factor(k*dt)]);
    }
    const exact=20+60*Math.exp(-12*k), final=points.at(-1)[1];
    const maxError=Math.max(...points.map(([t,T])=>Math.abs(T-(20+60*Math.exp(-k*t)))));
    answer={k,h,method,multiplier:factor(k*h),final,exact,maxError,steps:points.length-1};
    const low=Math.min(0,...points.map(p=>p[1])),high=Math.max(85,...points.map(p=>p[1]));
    const padding=.08*(high-low),ymin=low-padding,ymax=high+padding;
    const X=t=>70+t/12*560,Y=T=>355-(T-ymin)/(ymax-ymin)*280;
    svg.replaceChildren();
    element('path',{d:'M70 65V355H640',fill:'none',stroke:'#71858e'});
    for(let i=0;i<6;i++){
      const value=ymin+(ymax-ymin)*i/5;
      element('text',{x:58,y:Y(value)+4,'text-anchor':'end','font-size':12},value.toFixed(1));
    }
    for(let t=0;t<=12;t+=2)element('text',{x:X(t),y:378,'text-anchor':'middle','font-size':13},t);
    element('text',{x:350,y:412,'text-anchor':'middle'},zh?'时间 / min':'Time / min');
    element('text',{x:70,y:38},zh?'温度 / °C':'Temperature / °C');
    element('path',{d:`M70 ${Y(20)}H640`,stroke:'#9aa5aa','stroke-dasharray':'4 4'});
    const truth=Array.from({length:121},(_,i)=>[i/10,20+60*Math.exp(-k*i/10)]);
    function curve(values,color,width){element('path',{d:values.map(([t,T],i)=>(i?'L':'M')+X(t)+','+Y(T)).join(' '),fill:'none',stroke:color,'stroke-width':width});}
    curve(truth,'#183a4c',2);curve(points,'#bd653f',2.5);
    points.forEach(([t,T])=>element('circle',{cx:X(t),cy:Y(T),r:3,fill:'#bd653f'}));
    element('text',{x:690,y:70,'font-size':22},method.toUpperCase());
    const lines=[
      (zh?'当前 k = ':'Current k = ')+k.toFixed(2)+' /min',
      'h = '+h.toFixed(1)+' min',
      (zh?'一步放大因子：':'One-step multiplier: ')+answer.multiplier.toFixed(5),
      (zh?'12min数值温度：':'Numerical at 12 min: ')+final.toFixed(3)+' °C',
      (zh?'12min精确温度：':'Exact at 12 min: ')+exact.toFixed(3)+' °C',
      (zh?'网格点最大误差：':'Maximum grid error: ')+maxError.toFixed(3)+' °C',
      (zh?'橙：数值更新':'Orange: discrete updates'),
      (zh?'深蓝：精确指数曲线':'Navy: exact exponential'),
    ];
    lines.forEach((text,i)=>element('text',{x:690,y:110+i*31,'font-size':14},text));
    get('k').value=k;get('h').value=h;get('method').value=method;
    get('status').textContent=(zh?'本次计算 ':'Computed ')+answer.steps+(zh?' 步。真实温度始终从80°C趋向20°C；比较的是求解器的离散行为。':' steps. Physical temperature approaches 20°C from 80°C; the comparison concerns discrete integration.');
  }
  function set(values){
    if(values.k!==undefined)k=Math.max(.1,Math.min(.8,Number(values.k)));
    if(values.h!==undefined)h=Math.max(.1,Math.min(4,Number(values.h)));
    if(['euler','rk4'].includes(values.method))method=values.method;
    render();return {...answer};
  }
  function reset(){return set({k:.35,h:1,method:'euler'});}
  get('k').oninput=()=>set({k:get('k').value});
  get('h').oninput=()=>set({h:get('h').value});
  get('method').onchange=()=>set({method:get('method').value});
  get('reset').onclick=reset;
  window.CourseLab={state:()=>({...answer}),set,reset};reset();
})();

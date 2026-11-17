(function(){
const root=document.getElementById('P03-lab');if(!root)return;
const zh=document.documentElement.lang.startsWith('zh'),tr=(a,b)=>zh?a:b;
const angle=root.querySelector('#P03-angle'),volume=root.querySelector('#P03-volume'),baseline=root.querySelector('#P03-baseline');
const svg=root.querySelector('#P03-plot'),out=root.querySelector('#P03-result');let current={};
function draw(){
 const theta=Number(angle.value),v=Number(volume.value),offset=Number(baseline.value),t=theta*Math.PI/180;
 const R=(3*v/(Math.PI*(1-Math.cos(t))**2*(2+Math.cos(t))))**(1/3),a=R*Math.sin(t),h=R*(1-Math.cos(t)),cy=-R*Math.cos(t),b=offset/1000;
 const estimate=Math.acos(Math.max(-1,Math.min(1,(b-cy)/R)))*180/Math.PI;
 current={angle_deg:theta,volume_ul:v,baseline_um:offset,radius_mm:R,base_radius_mm:a,height_mm:h,estimated_angle_deg:estimate,error_deg:estimate-theta};
 const extent=Math.max(1.2*a,1.1*R,1.25*h),scale=Math.min(285/extent,250/Math.max(h,.2));
 const X=x=>400+x*scale,Y=y=>320-y*scale;
 let d='';for(let k=0;k<=160;k++){const u=-t+2*t*k/160,x=R*Math.sin(u),y=R*Math.cos(u)+cy;d+=(k?'L':'M')+X(x)+','+Y(y);}
 let html=`<rect width="800" height="390" fill="#fbfcfc"/><path d="${d}L${X(-a)},320Z" fill="#c8e4e7"/><path d="${d}" fill="none" stroke="#186c94" stroke-width="3"/><path d="M30,320H770" stroke="#188777" stroke-width="2"/><path d="M30,${Y(b)}H770" stroke="#a14e6d" stroke-width="2" stroke-dasharray="7,5"/>`;
 const cut=Math.sqrt(Math.max(0,R*R-(b-cy)**2));
 html+=`<circle cx="${X(cut)}" cy="${Y(b)}" r="5" fill="#a14e6d"/><circle cx="${X(-cut)}" cy="${Y(b)}" r="5" fill="#a14e6d"/>`;
 html+=`<text x="35" y="25" fill="#18344a" font-size="17">${tr('真实球冠；分析线改变交点','True spherical cap; analysis line changes the intersection')}</text><text x="400" y="353" text-anchor="middle" fill="#188777">${tr('绿色：真实表面','Green: actual substrate')}</text><text x="400" y="378" text-anchor="middle" fill="#a14e6d">${tr('紫色虚线：分析基线','Purple dashed line: analysis baseline')} · ${offset} μm</text>`;
 svg.innerHTML=html;out.textContent=`θ=${theta.toFixed(1)}° · `+tr('估计角度','Estimated angle')+` ${estimate.toFixed(3)}° · `+tr('偏差','Error')+` ${(estimate-theta).toFixed(3)}° · a=${a.toFixed(4)} mm · h=${h.toFixed(4)} mm · V=${v.toFixed(2)} μL`;return {...current};
}
const reset=()=>{angle.value=70;volume.value=.5;baseline.value=0;return draw();};
const set=p=>{if(p.angle_deg!==undefined)angle.value=p.angle_deg;if(p.volume_ul!==undefined)volume.value=p.volume_ul;if(p.baseline_um!==undefined)baseline.value=p.baseline_um;return draw();};
const button=root.querySelector('#P03-reset');for(const c of [angle,volume,baseline])c.addEventListener('input',draw);button.addEventListener('click',reset);
window.CourseLab={set,state:()=>({...current}),reset,destroy:()=>{for(const c of [angle,volume,baseline])c.removeEventListener('input',draw);button.removeEventListener('click',reset);}};reset();
})();

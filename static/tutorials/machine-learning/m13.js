(() => {
 const root=document.getElementById('M13-lab');if(!root)return;
 const zh=document.documentElement.lang.startsWith('zh'),get=id=>document.getElementById('M13-'+id);
 let p={shift:20,nms:.5,confidence:0},result;
 const scores=[.9,.8,.7],colors=['#176b91','#bb554d','#96771d'];
 function iou(a,b){const w=Math.max(0,Math.min(a[2],b[2])-Math.max(a[0],b[0])),h=Math.max(0,Math.min(a[3],b[3])-Math.max(a[1],b[1]));const inter=w*h;return inter/((a[2]-a[0])*(a[3]-a[1])+(b[2]-b[0])*(b[3]-b[1])-inter);}
 function draw(){
  const truth=[[60,70,180,190],[260,85,340,190]],boxes=[truth[0],[60+p.shift,70,180+p.shift,190],truth[1]];
  let remaining=[0,1,2].filter(i=>scores[i]>=p.confidence),kept=[];
  while(remaining.length){let k=remaining.shift();kept.push(k);remaining=remaining.filter(j=>iou(boxes[k],boxes[j])<=p.nms);}
  const matched=new Set();let tp=0;
  for(const k of kept){let index=-1,best=0;truth.forEach((g,j)=>{const overlap=iou(boxes[k],g);if(!matched.has(j)&&overlap>best){best=overlap;index=j;}});if(best>=.5){tp++;matched.add(index);}}
  const fp=kept.length-tp,fn=truth.length-tp,precision=kept.length?tp/kept.length:0,recall=tp/truth.length;
  result={...p,kept,tp,fp,fn,precision,recall,iou01:iou(boxes[0],boxes[1])};
  let s='<rect width="940" height="350" rx="12" fill="#f7f9fb"/>';
  truth.forEach(b=>s+=`<rect x="${b[0]}" y="${b[1]}" width="${b[2]-b[0]}" height="${b[3]-b[1]}" fill="#d8dde2"/>`);
  boxes.forEach((b,i)=>{s+=`<rect x="${b[0]}" y="${b[1]}" width="${b[2]-b[0]}" height="${b[3]-b[1]}" fill="none" stroke="${colors[i]}" stroke-width="3" stroke-dasharray="${kept.includes(i)?'none':'7 5'}"/><text x="${b[0]+5}" y="${45+i*9}" fill="${colors[i]}" font-size="14">${i}: ${scores[i].toFixed(1)}</text>`;});
  s+=`<text x="60" y="225" font-size="15">${zh?'框0与1的IoU':'IoU of boxes 0 and 1'} = ${result.iou01.toFixed(4)}</text>`;
  const labels=zh?['保留候选','真阳性 TP','假阳性 FP','漏检 FN','精确率','召回率']:['Retained candidates','True positives','False positives','Missed objects','Precision','Recall'];
  const values=[kept.join(', ')||'—',tp,fp,fn,precision.toFixed(3),recall.toFixed(3)];
  labels.forEach((name,i)=>{s+=`<text x="535" y="55+i*42" font-size="16">${name}</text><text x="855" y="55+i*42" text-anchor="end" font-size="18" fill="#176b91">${values[i]}</text>`;});
  s+=`<text x="60" y="275" font-size="14">${zh?'坐标单位：px；NMS阈值与评价阈值分别使用':'Coordinates: pixels; NMS and evaluation thresholds are distinct'}</text>`;
  get('svg').innerHTML=s;
  get('shift').value=p.shift;get('nms').value=p.nms;get('confidence').value=p.confidence;
  get('status').textContent=zh?`偏移 ${p.shift} px；NMS ${p.nms.toFixed(2)}；最低置信 ${p.confidence.toFixed(2)}。无输出时本实验将精确率显示为0。`:`Shift ${p.shift} px; NMS ${p.nms.toFixed(2)}; minimum confidence ${p.confidence.toFixed(2)}. With no predictions this lab displays precision as zero.`;
 }
 function set(v={}){for(const key of ['shift','nms','confidence'])if(v[key]!==undefined)p[key]=Math.max(0,Math.min(key==='shift'?140:1,Number(v[key])));draw();return state();}
 function state(){return {...result,kept:[...result.kept]};}
 function reset(){p={shift:20,nms:.5,confidence:0};draw();return state();}
 for(const key of ['shift','nms','confidence'])get(key).addEventListener('input',e=>set({[key]:e.target.value}));
 get('reset').addEventListener('click',reset);window.CourseLab={set,state,reset};draw();
})();

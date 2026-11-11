document.querySelectorAll('[data-lab="G12-I1"]').forEach(root=>{
 if(root.dataset.ready)return;root.dataset.ready='1';const zh=root.dataset.lang==='zh';
 const a=root.querySelector('[data-a]'),b=root.querySelector('[data-b]'),canvas=root.querySelector('canvas'),ctx=canvas.getContext('2d');
 function draw(){const aa=+a.value,bb=+b.value,ra=aa*Math.PI/180,rb=bb*Math.PI/180,c=(Math.cos(ra)+Math.cos(rb))/2,s=(Math.sin(ra)+Math.sin(rb))/2,R=Math.hypot(c,s),mean=Math.atan2(s,c)*180/Math.PI,arith=(aa+bb)/2;
 root.querySelector('[data-readout]').textContent=`A ${aa}° · B ${bb}° · ${zh?'算术平均':'Arithmetic mean'} ${arith.toFixed(1)}° · ${zh?'圆均值':'Circular mean'} ${R<1e-8?(zh?'无定义':'undefined'):mean.toFixed(1)+'°'} · R ${R.toFixed(4)}`;
 ctx.clearRect(0,0,900,420);ctx.fillStyle='#f8f7f2';ctx.fillRect(0,0,900,420);const x=240,y=210,r=145;
 ctx.strokeStyle='#a8bfba';ctx.lineWidth=2;ctx.beginPath();ctx.arc(x,y,r,0,2*Math.PI);ctx.stroke();
 function arrow(angle,length,color){const ex=x+length*Math.cos(angle),ey=y-length*Math.sin(angle);ctx.strokeStyle=color;ctx.fillStyle=color;ctx.lineWidth=4;ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(ex,ey);ctx.stroke();const q=Math.atan2(ey-y,ex-x);ctx.beginPath();ctx.moveTo(ex,ey);ctx.lineTo(ex-12*Math.cos(q-.45),ey-12*Math.sin(q-.45));ctx.lineTo(ex-12*Math.cos(q+.45),ey-12*Math.sin(q+.45));ctx.closePath();ctx.fill();}
 arrow(ra,r,'#176d83');arrow(rb,r,'#b28a35');if(R>=1e-8)arrow(Math.atan2(s,c),r*R,'#b44e3f');
 ctx.font='22px sans-serif';ctx.fillStyle='#173f46';ctx.fillText('0°',x+r+12,y+8);ctx.fillText('180°',x-r-72,y+8);ctx.fillText('90°',x-18,y-r-16);ctx.fillText('−90°',x-28,y+r+32);
 const lines=zh?['蓝：角度 A；金：角度 B','红：平均箭头，长度为 R','179° 和 −179° 在圆周上相邻。','相反的两根箭头恰好相互抵消，','此时平均方向没有定义。']:['Blue: A; gold: B','Red: mean arrow, length R','179° and −179° are neighbours.','Opposite arrows cancel exactly;','their mean direction is undefined.'];
 lines.forEach((s,i)=>ctx.fillText(s,455,110+i*48));}
 [a,b].forEach(e=>e.addEventListener('input',draw));root.querySelector('[data-reset]').addEventListener('click',()=>{a.value=179;b.value=-179;draw();});draw();});
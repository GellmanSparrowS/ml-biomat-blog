

document.querySelectorAll('[data-lab="PE08-I1"],[data-lab="PE08-I2"]').forEach(root=>{
 const zh=root.closest('[data-lang]').dataset.lang==='zh',first=root.dataset.lab.endsWith('I1'),q=k=>root.querySelector('[data-field="'+k+'"]');
 const text=(x,y,s,size=21,color='#17313b',anchor='start')=>`<text x="${x}" y="${y}" font-size="${size}" fill="${color}" text-anchor="${anchor}">${s}</text>`;
 const line=(x,y,a,b,color='#d6e0df',w=1,dash='')=>`<line x1="${x}" y1="${y}" x2="${a}" y2="${b}" stroke="${color}" stroke-width="${w}" stroke-dasharray="${dash}"/>`;
 const path=(pts,color,w=3)=>`<path d="${pts.map((p,i)=>(i?'L':'M')+p[0].toFixed(3)+','+p[1].toFixed(3)).join(' ')}" fill="none" stroke="${color}" stroke-width="${w}"/>`;
 const dot=(x,y,c)=>`<circle cx="${x}" cy="${y}" r="6" fill="${c}"/>`;
 const fmt=v=>v.toLocaleString('en-US',{maximumFractionDigits:3}),Teal='#087b83',Orange='#bc592c';
 const names=first?['ratio','conversion']:['diffusion','reaction','shell'];
 const defaults=first?[.98,.99]:[-11,300,3];
 function draw(){
  let s='';
  if(first){
   const r=+q('ratio').value,p=+q('conversion').value,dp=(1+r)/(1+r-2*r*p),balanced=1/(1-p),remaining=(1+r-2*r*p)/(1+r);
   q('ratio-value').textContent=r.toFixed(3);q('conversion-value').textContent=(100*p).toFixed(1)+'%';
   const X=a=>90+(a-.9)/.099*550,Y=v=>485-Math.log10(v)/3*360;
   s+=text(35,43,zh?'同一反应程度下的两种配比':'Two group balances at the same conversion',23);
   for(const d of [1,10,100,1000])s+=line(90,Y(d),640,Y(d))+text(76,Y(d)+7,String(d),20,'#627780','end');
   for(const a of [.9,.92,.94,.96,.98,.999])s+=line(X(a),125,X(a),485)+text(X(a),520,(100*a).toFixed(a===.999?1:0),20,'#627780','middle');
   s+=line(90,125,90,485,'#17313b',2)+line(90,485,640,485,'#17313b',2)+text(35,88,zh?'平均构件数（纵轴每级相差10倍）':'Mean components (each vertical step is tenfold)',21)+text(640,563,zh?'A端基反应程度 / %':'A-group conversion / %',21,'#17313b','end');
   const a=[],b=[];for(let i=0;i<=180;i++){const pp=.9+.099*i/180;a.push([X(pp),Y(1/(1-pp))]);b.push([X(pp),Y((1+r)/(1+r-2*r*pp))]);}
   s+=path(a,Orange,4)+path(b,Teal,4)+line(X(p),125,X(p),485,'#627780',1,'6 5')+dot(X(p),Y(balanced),Orange)+dot(X(p),Y(dp),Teal);
   s+=line(40,613,82,613,Teal,4)+text(95,620,(zh?'所选配比 r = ':'Selected ratio r = ')+r.toFixed(3),22,Teal);
   s+=line(40,658,82,658,Orange,4)+text(95,665,zh?'等量接口 r = 1':'Balanced groups r = 1',22,Orange);
   s+=text(35,720,(zh?'当前平均链长：':'Current mean length: ')+fmt(dp),25,Teal)+text(35,768,(zh?'相同转化率、等量时：':'Balanced at the same conversion: ')+fmt(balanced),22,Orange);
   q('result').textContent=zh?`A端基反应程度 ${(p*100).toFixed(1)}%，接口比 ${r.toFixed(3)}：平均每个分子含 ${fmt(dp)} 个原始构件；剩余分子数为初始构件数的 ${(100*remaining).toFixed(3)}%。${r===1?'等量的理想模型在转化率趋近100%时没有有限链长上限。':`即使A端基全部反应，平均链长上限仍为 ${fmt((1+r)/(1-r))}。`} 图轴保持不变；纵轴按10倍间隔排列。`:`At ${(100*p).toFixed(1)}% A-group conversion and ratio ${r.toFixed(3)}, each molecule contains ${fmt(dp)} original components on average. Remaining molecular count is ${(100*remaining).toFixed(3)}% of the initial component count. ${r===1?'The balanced ideal model has no finite chain-length ceiling as conversion approaches 100%.':`Even complete A-group conversion gives a ceiling of ${fmt((1+r)/(1-r))}.`} Axes stay fixed, with tenfold vertical intervals.`;
   root.dataset.values=JSON.stringify({r,p,dp,balanced,remaining});
  }else{
   const D=10**(+q('diffusion').value),k=+q('reaction').value,shell=+q('shell').value,rc=1e-6,rp=rc*shell,cl=100,da=k*rc*rc/(3*D)*(1-rc/rp),cc=cl/(1+da),rate=4*Math.PI*rc**3/3*k*cc,unlimited=4*Math.PI*rc**3/3*k*cl;
   q('diffusion-value').textContent=D.toExponential(2)+' m²/s';q('reaction-value').textContent=k+' s⁻¹';q('shell-value').textContent=shell.toFixed(1)+' μm';
   const X=a=>90+(a-1)/9*550,Y=c=>460-c/100*325;
   s+=text(35,43,zh?'单体从外表面扩散到催化剂核':'Monomer diffuses inward to the catalyst core',23)+text(35,90,zh?'单体浓度 / (mol/m³)':'Monomer concentration / (mol/m³)',21);
   for(const c of [0,25,50,75,100])s+=line(90,Y(c),640,Y(c))+text(76,Y(c)+7,String(c),20,'#627780','end');
   for(const a of [1,3,5,7,10])s+=line(X(a),135,X(a),460)+text(X(a),496,String(a),20,'#627780','middle');
   s+=line(90,135,90,460,'#17313b',2)+line(90,460,640,460,'#17313b',2)+text(640,540,zh?'距球心半径 / μm':'Radius from centre / μm',21,'#17313b','end');
   const pts=[];for(let i=0;i<=160;i++){const rr=rc+(rp-rc)*i/160,c=cc+rate/(4*Math.PI*D)*(1/rc-1/rr);pts.push([X(rr/rc),Y(c)]);}
   s+=path(pts,Teal,4)+dot(X(1),Y(cc),Orange)+dot(X(shell),Y(cl),Teal)+line(X(shell),135,X(shell),460,Teal,1,'6 5');
   s+=text(35,593,(zh?'核表面：':'Core surface: ')+fmt(cc)+' mol/m³',23,Orange)+text(35,638,(zh?'外表面：':'Outer surface: ')+cl+' mol/m³',23,Teal);
   s+=text(35,691,'Da = '+fmt(da)+(zh?'；局部浓度比 ':'; local concentration ratio ')+(cc/cl).toFixed(4),22)+text(35,742,(zh?'实际总消耗：':'Total consumption: ')+rate.toExponential(3)+' mol/s',22);
   q('result').textContent=zh?`固定核半径1 μm，壳层外半径 ${shell.toFixed(1)} μm；局部浓度保留外部值的 ${(100*cc/cl).toFixed(2)}%。实际消耗 ${rate.toExponential(3)} mol/s，无壳层限制时为 ${unlimited.toExponential(3)} mol/s。扩散供给与反应消耗相等。这里只计算固定几何的等温准稳态；图上由右向左供给单体。`:`The core radius is fixed at 1 μm and the outer radius is ${shell.toFixed(1)} μm. Local concentration is ${(100*cc/cl).toFixed(2)}% of the external value. Consumption is ${rate.toExponential(3)} mol/s, compared with ${unlimited.toExponential(3)} mol/s without shell limitation. Supply equals consumption in this fixed-geometry, isothermal quasi-steady model. Monomer travels from right to left on the plot.`;
   root.dataset.values=JSON.stringify({D,k,shell,rc,rp,cl,da,cc,rate,unlimited});
  }
  q('plot').innerHTML=s;
 }
 names.forEach(n=>q(n).addEventListener('input',draw));
 root.querySelector('[data-reset]').addEventListener('click',()=>{names.forEach((n,i)=>q(n).value=defaults[i]);draw();});draw();
});

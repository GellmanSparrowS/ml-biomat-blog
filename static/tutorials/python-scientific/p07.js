(() => {
  const root = document.getElementById('P07-lab');
  if (!root) return;
  const zh = document.documentElement.lang.startsWith('zh');
  const say = (a,b) => zh ? a : b;
  const base = [[1,1.08,1.14,1.18,1.20],[1.02,1.09,1.16,1.21,1.24],[.98,1.05,1.11,1.15,1.18]];
  const times = [0,10,20,40,60], colors=['#28648a','#b85336','#467a62'], names=['A','B','C'];
  const byId = name => document.getElementById('P07-'+name);
  const fields=['row','col','axis','delta','missing','baseline'];
  const current={row:1,col:2,axis:0,delta:0,missing:false,baseline:true};
  let last={};
  const text=(x,y,value,size=17,extra='')=>`<text x="${x}" y="${y}" font-size="${size}" fill="#172b36" ${extra}>${value}</text>`;
  const line=(x1,y1,x2,y2,color='#bac4c6',width=1,extra='')=>`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${color}" stroke-width="${width}" ${extra}/>`;
  const summarize=values=>{const valid=values.filter(Number.isFinite),n=valid.length,mean=n?valid.reduce((a,b)=>a+b,0)/n:null;return{n,mean,sd:n>1?Math.sqrt(valid.reduce((s,v)=>s+(v-mean)**2,0)/(n-1)):null};};
  function render(){
    const h=base.map(row=>row.slice());
    h[current.row][current.col]=current.missing?null:base[current.row][current.col]+current.delta;
    const columns=times.map((_,j)=>summarize(h.map(row=>row[j])));
    const rows=h.map(summarize);
    const groups=current.axis===0?columns:rows;
    const baselineGroups=current.axis===0?times.map((_,j)=>summarize(base.map(r=>r[j]))):base.map(summarize);
    let matrix=text(12,24,'h.shape = (3, 5)',19)+text(89,64,say('时间 / min（axis 1）','Time / min (axis 1)'),17);
    times.forEach((v,j)=>matrix+=text(119+j*74,93,String(v),17,'text-anchor="middle"'));
    h.forEach((row,i)=>{
      matrix+=text(37,137+i*54,names[i],19,'font-weight="bold"');
      row.forEach((v,j)=>{
        const selected=i===current.row&&j===current.col,x=84+j*74,y=106+i*54;
        const opacity=v===null?.05:Math.min(.88,Math.max(.10,(v-.7)/.85));
        matrix+=`<rect x="${x}" y="${y}" width="70" height="48" fill="${colors[i]}" fill-opacity="${opacity}" stroke="${selected?'#b37c12':'#dbe1df'}" stroke-width="${selected?3:1}"/>`;
        matrix+=text(x+35,y+31,v===null?'NaN':v.toFixed(2),18,'text-anchor="middle"');
      });
    });
    matrix+=text(22,293,say('行：样品（axis 0）；格内数值单位 mm','Rows: specimens (axis 0); cell values in mm'),15);
    byId('matrix').innerHTML=matrix;
    const x=t=>65+t/60*460,y=v=>290-(v-.6)/1.1*230;
    let curves='';
    [.6,.8,1,1.2,1.4,1.6].forEach(v=>{curves+=line(65,y(v),535,y(v),'#e4e5df')+text(54,y(v)+6,v.toFixed(1),16,'text-anchor="end"');});
    times.forEach(t=>{curves+=line(x(t),290,x(t),296,'#172b36')+text(x(t),319,String(t),16,'text-anchor="middle"');});
    curves+=line(65,60,65,290,'#172b36')+line(65,290,535,290,'#172b36')+text(16,28,say('厚度 / mm','Thickness / mm'),17)+text(295,349,say('时间 / min','Time / min'),17,'text-anchor="middle"');
    h.forEach((row,i)=>{
      let path='',active=false;
      row.forEach((v,j)=>{if(v===null){active=false;return;}path+=(active?' L':' M')+x(times[j])+','+y(v);active=true;});
      curves+=`<path d="${path}" fill="none" stroke="${colors[i]}" stroke-width="2"/>`;
      row.forEach((v,j)=>{if(v!==null)curves+=`<circle cx="${x(times[j])}" cy="${y(v)}" r="4" fill="${colors[i]}"/>`;});
      curves+=line(235+i*75,20,257+i*75,20,colors[i],3)+text(262+i*75,26,names[i],16);
    });
    if(current.baseline){const pts=times.map((t,j)=>`${x(t)},${y(summarize(base.map(r=>r[j])).mean)}`).join(' ');curves+=`<polyline points="${pts}" fill="none" stroke="#899496" stroke-width="2" stroke-dasharray="5 5"/>`;}
    curves+=`<polyline points="${columns.map((v,j)=>`${x(times[j])},${y(v.mean)}`).join(' ')}" fill="none" stroke="#172b36" stroke-width="3"/>`;
    if(!current.missing)curves+=`<circle cx="${x(times[current.col])}" cy="${y(h[current.row][current.col])}" r="10" fill="none" stroke="#b37c12" stroke-width="3"/>`;
    curves+=text(234,48,say('黑：当前均值；灰虚线：原始均值','Black: current mean; dashed: original'),14);
    byId('curves').innerHTML=curves;
    const selected=current.axis===0?current.col:current.row;
    const xg=i=>80+i*(420/Math.max(1,groups.length-1)),yg=v=>205-(v-.6)/1.1*145;
    let result=text(18,25,`axis=${current.axis}  →  shape (${groups.length},)`,20);
    [.8,1,1.2,1.4,1.6].forEach(v=>result+=line(60,yg(v),535,yg(v),'#e4e5df')+text(49,yg(v)+5,v.toFixed(1),15,'text-anchor="end"'));
    groups.forEach((g,i)=>{
      if(current.baseline)result+=line(xg(i)-13,yg(baselineGroups[i].mean),xg(i)+13,yg(baselineGroups[i].mean),'#899496',2,'stroke-dasharray="4 3"');
      const c=i===selected?'#b85336':'#172b36';
      if(g.sd!==null)result+=line(xg(i),yg(g.mean-g.sd),xg(i),yg(g.mean+g.sd),c,2)+line(xg(i)-6,yg(g.mean-g.sd),xg(i)+6,yg(g.mean-g.sd),c,2)+line(xg(i)-6,yg(g.mean+g.sd),xg(i)+6,yg(g.mean+g.sd),c,2);
      result+=`<circle cx="${xg(i)}" cy="${yg(g.mean)}" r="5.5" fill="${c}"/>`;
      result+=text(xg(i),227,current.axis===0?`${times[i]} min`:names[i],16,'text-anchor="middle"')+text(xg(i),250,`n=${g.n}`,16,'text-anchor="middle"');
    });
    result+=text(18,50,say('均值 ± 样本标准差 / mm','Mean ± sample SD / mm'),15);
    byId('result').innerHTML=result;
    const selectedValues=current.axis===0?h.map(row=>row[current.col]):h[current.row];
    const valid=selectedValues.filter(Number.isFinite),g=groups[selected];
    const calculation=valid.map(v=>v.toFixed(2)).join(' + ');
    byId('output').textContent=`${say('所选格子','Selected cell')}: h[${current.row}, ${current.col}]\n${say('高亮结果','Highlighted result')}: (${calculation}) / ${g.n}\n= ${g.mean.toFixed(6)} mm\n${say('原始均值','Original mean')}: ${baselineGroups[selected].mean.toFixed(6)} mm\n${say('均值变化','Mean change')}: ${(g.mean-baselineGroups[selected].mean).toFixed(6)} mm\n${say('有效计数','Valid count')}: ${g.n}`;
    last={...current,matrix:h,output_shape:[groups.length],means:groups.map(g=>g.mean),counts:groups.map(g=>g.n),sd:groups.map(g=>g.sd),selected_mean:g.mean,selected_change:g.mean-baselineGroups[selected].mean};
  }
  function set(values){
    Object.assign(current,values);
    current.row=Math.max(0,Math.min(2,Number(current.row)));current.col=Math.max(0,Math.min(4,Number(current.col)));
    current.axis=Number(current.axis)===1?1:0;current.delta=Math.max(-.3,Math.min(.3,Number(current.delta)||0));
    fields.forEach(name=>{if(typeof current[name]==='boolean')byId(name).checked=current[name];else byId(name).value=current[name];});render();
  }
  fields.forEach(name=>byId(name).addEventListener('input',()=>set({[name]:['missing','baseline'].includes(name)?byId(name).checked:Number(byId(name).value)})));
  const reset=()=>set({row:1,col:2,axis:0,delta:0,missing:false,baseline:true});
  byId('reset').addEventListener('click',reset);
  window.CourseLab={set,state:()=>JSON.parse(JSON.stringify(last)),reset};render();
})();

(()=>{const en=document.documentElement.lang==='en',t=(z,e)=>en?e:z,by=id=>document.getElementById('L02-'+id);let v={number:100,activity:1,background:0};
const text=(x,y,label,anchor='middle',size=14,color='#243c47')=>`<text x="${x}" y="${y}" text-anchor="${anchor}" font-size="${size}" fill="${color}">${label}</text>`;
function state(){const corrected=v.number*v.activity;return {...v,corrected,naive:corrected+125*v.background,sample_absorbance:.04+v.background+.008*corrected};}
function render(){for(const k of ['number','activity','background']){by(k).value=v[k];by(k+'-value').value=k==='number'?v[k]:v[k].toFixed(2);}const s=state();let svg='';
svg+=text(235,26,t('三个百分数，三种含义','Three percentages, three meanings'));svg+=text(720,26,t('数量与活性共同决定信号','Number and activity jointly set signal'));
svg+='<path d="M70,60V340H420" fill="none" stroke="#acc1c9"/>';
for(const value of [0,50,100,150,200,250]){const y=340-value;svg+=`<path d="M70,${y}H420" stroke="${value===100?'#b18a35':'#e1e9ed'}" ${value===100?'stroke-dasharray="4 4"':''}/>`+text(57,y+5,value,'end',13);}
const bars=[{value:v.number,label:t('细胞数量','Cell number'),color:'#758893'},{value:s.corrected,label:t('匹配空白校正','Matched blank'),color:'#12687b'},{value:s.naive,label:t('只减共同空白','Common blank'),color:'#be6047'}];
bars.forEach((b,i)=>{const x=100+i*112;svg+=`<rect x="${x}" y="${340-b.value}" width="58" height="${b.value}" fill="${b.color}"/>`+text(x+29,330-b.value,b.value.toFixed(1)+'%', 'middle',14,b.color)+text(x+29,366,b.label,'middle',12);});
svg+=text(70,49,t('相对参照 / %','Relative to reference / %'),'start',12);
const x0=560,y0=340,w=340,h=250;
for(let i=0;i<20;i++)for(let j=0;j<20;j++){const n=20+(i+.5)*5,q=.5+(j+.5)*.05,signal=n*q;svg+=`<rect x="${x0+i*w/20}" y="${y0-(j+1)*h/20}" width="${w/20+.3}" height="${h/20+.3}" fill="#12687b" opacity="${.08+.85*signal/180}"/>`;}
svg+=`<path d="M${x0},90V${y0}H900" stroke="#acc1c9" fill="none"/>`;
for(const n of [20,40,60,80,100,120])svg+=text(x0+(n-20)/100*w,363,n.toString(),'middle',12);
for(const q of [.5,.75,1,1.25,1.5])svg+=text(x0-12,y0-(q-.5)*h+4,q.toFixed(2),'end',12);
const pts=[];for(let n=100/1.5;n<=120;n+=.5)pts.push([x0+(n-20)/100*w,y0-(100/n-.5)*h]);svg+=`<path d="${pts.map((p,i)=>(i?'L':'M')+p.join(',')).join(' ')}" fill="none" stroke="#fff" stroke-width="3" stroke-dasharray="6 4"/>`;
svg+=`<circle cx="${x0+(v.number-20)/100*w}" cy="${y0-(v.activity-.5)*h}" r="7" fill="#be6047" stroke="white" stroke-width="2"/>`;
svg+=text(730,395,t('细胞数量 / 参照的%','Cell number / % of reference'))+text(560,65,t('单细胞相对活性 ↑','Per-cell activity ↑'),'start',12);
svg+=text(900,65,t('浅 → 深：10% → 180%','Light → dark: 10% → 180%'),'end',11);
by('plot').innerHTML=svg;by('readout').textContent=t(`含细胞孔吸光度 ${s.sample_absorbance.toFixed(3)}；匹配空白 ${(.04+v.background).toFixed(3)}。校正响应 ${s.corrected.toFixed(1)}%，只减共同空白得到 ${s.naive.toFixed(1)}%。`,`Cell-well absorbance ${s.sample_absorbance.toFixed(3)}; matched blank ${(.04+v.background).toFixed(3)}. Corrected response ${s.corrected.toFixed(1)}%; common-blank-only response ${s.naive.toFixed(1)}%.`);}
function set(p){for(const k of ['number','activity','background'])if(p[k]!==undefined){const [lo,hi]=k==='number'?[20,120]:k==='activity'?[.5,1.5]:[0,.4];v[k]=Math.max(lo,Math.min(hi,Number(p[k])));}render();}
function reset(){v={number:100,activity:1,background:0};render();}
for(const k of ['number','activity','background'])by(k).oninput=()=>set({[k]:Number(by(k).value)});by('background-case').onclick=()=>set({number:50,activity:1,background:.2});by('reset').onclick=reset;window.CourseLab={set,state,reset};render();})();

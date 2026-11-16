(function(){
const zh=document.documentElement.lang.startsWith('zh'),tr=(z,e)=>zh?z:e,$=id=>document.getElementById('P06-'+id);
const initial={interpreter:'A',installed:'A',mass:.2,thickness:2,unit:'mm',skip_units:false};let p={...initial},result;
const f=v=>v===null?'—':Number(v.toPrecision(6)).toString();
function text(x,y,t,extra=''){return `<text x="${x}" y="${y}" fill="#172b36" font-size="16" ${extra}>${t}</text>`;}
function render(){
['interpreter','installed','mass','thickness','unit'].forEach(k=>$(k).value=p[k]);$('skip').checked=p.skip_units;$('mass-label').textContent=f(p.mass);$('thickness-label').textContent=f(p.thickness);
const visible=p.installed==='both'||p.installed===p.interpreter,correctVolume=.08*p.thickness,correctDensity=p.thickness>0?p.mass/correctVolume:null;
const wrong=p.skip_units&&p.unit==='mm',volume=wrong?80*p.thickness:correctVolume,status=!visible?'ModuleNotFoundError':p.thickness===0?'ValueError':'ready',density=status==='ready'?p.mass/volume:null;
result={...p,status,density,volume:status==='ready'?volume:null,correct_density:correctDensity,factor:density===null?null:correctDensity/density};
$('result').textContent=status==='ready'?tr(`密度 ${f(density)} g/cm³；计算使用体积 ${f(volume)} cm³；正确体积 ${f(correctVolume)} cm³。`,`Density ${f(density)} g/cm³; calculated volume ${f(volume)} cm³; correct volume ${f(correctVolume)} cm³.`):status==='ValueError'?tr('ValueError：厚度必须为有限正数。改变厚度后重新计算。','ValueError: thickness must be finite and positive. Change thickness to calculate again.'):tr(`ModuleNotFoundError：环境 ${p.interpreter} 没有绘图库。把安装目标与运行入口接到同一环境。`,`ModuleNotFoundError: environment ${p.interpreter} has no plotting package. Match the installation target to the interpreter.`);
let route=text(25,30,tr('当前执行路线（教学模型）','Current execution route (teaching model)'),'font-weight="700"');
for(let i=0;i<2;i++){let label=i?'B':'A',x=25+i*450,active=p.interpreter===label,installed=p.installed===label||p.installed==='both';route+=`<rect x="${x}" y="55" width="400" height="100" rx="8" fill="${active?'#e3edf2':'#f1f1ed'}" stroke="${active?'#28648a':'#bcc7c6'}" stroke-width="2"/>`+text(x+18,85,tr('环境 ','Environment ')+label)+text(x+18,115,active?tr('正在执行 main.py','Executing main.py'):tr('未选择的入口','Inactive interpreter'))+text(x+18,145,installed?tr('matplotlib 可导入','matplotlib available'):tr('matplotlib 未安装','matplotlib absent'));}
$('route').innerHTML=route;
const ymax=Math.ceil((p.mass/.04)/5)*5,xx=h=>475+h/4*365,yy=d=>375-d/ymax*290;let svg=text(35,24,tr('样品外形尺寸','Specimen dimensions'),'font-weight="700"')+text(35,46,tr('长10 mm · 宽8 mm','Length 10 mm · width 8 mm'))+text(475,24,tr('密度随厚度变化','Density vs thickness'),'font-weight="700"')+text(475,46,tr('质量保持固定','Mass held constant'));
svg+=`<rect x="45" y="65" width="300" height="240" fill="#dce7ec" stroke="#28648a" stroke-width="2"/>`+text(195,185,tr('上视图','Top view'),'text-anchor="middle"');
svg+=`<rect x="45" y="${435-p.thickness*30}" width="300" height="${p.thickness*30}" fill="#dce8df" stroke="#467a62" stroke-width="2"/>`+text(45,458,tr(`侧视：厚 ${f(p.thickness)} mm`,`Side view: thickness ${f(p.thickness)} mm`));
for(let h=0;h<=4;h++){svg+=`<line x1="${xx(h)}" x2="${xx(h)}" y1="85" y2="375" stroke="#dce1df"/>`+text(xx(h),400,h.toString(),'text-anchor="middle"');}
for(let d=0;d<=ymax;d+=ymax/5){svg+=`<line x1="475" x2="840" y1="${yy(d)}" y2="${yy(d)}" stroke="#dce1df"/>`+text(465,yy(d)+5,f(d),'text-anchor="end"');}
let pts=[];for(let h=.5;h<=4.00001;h+=.025)pts.push(`${xx(h)},${yy(p.mass/(.08*h))}`);svg+=`<polyline points="${pts.join(' ')}" fill="none" stroke="#28648a" stroke-width="3"/>`;
if(correctDensity!==null&&p.thickness>=.5)svg+=`<circle cx="${xx(p.thickness)}" cy="${yy(correctDensity)}" r="7" fill="#fbfaf6" stroke="#28648a" stroke-width="3"/>`;
if(density!==null&&density<=ymax)svg+=`<circle cx="${xx(p.thickness)}" cy="${yy(density)}" r="5" fill="#b85336"/>`;
if(p.thickness>0&&p.thickness<.5)svg+=text(485,60,tr('当前正确密度高于曲线显示范围','Current correct density exceeds curve range'));
svg+=text(650,435,tr('厚度 / mm','Thickness / mm'),'text-anchor="middle"')+text(475,65,tr('密度 / g·cm⁻³','Density / g·cm⁻³'))+text(475,463,tr('蓝线/空心点：正确关系；红点：报告值','Blue/open marker: correct; red marker: reported'));
$('plot').innerHTML=svg;
const lengths=p.unit==='mm'?[10,8,p.thickness]:[1,.8,p.thickness*.1];$('table').innerHTML=`<table><thead><tr><th>${tr('输入长度','Entered lengths')}</th><th>${tr('正确体积 / cm³','Correct volume / cm³')}</th><th>${tr('正确密度 / g·cm⁻³','Correct density / g·cm⁻³')}</th><th>${tr('正确值÷报告值','Correct / reported')}</th></tr></thead><tbody><tr><td>${lengths.map(f).join(' × ')} ${p.unit}</td><td>${f(correctVolume)}</td><td>${f(correctDensity)}</td><td>${f(result.factor)}</td></tr></tbody></table>`;
}
function set(q){p={...p,...q};p.mass=Math.min(1,Math.max(.1,Number(p.mass)));p.thickness=Math.min(4,Math.max(0,Number(p.thickness)));render();return result;}
for(const k of ['interpreter','installed','unit'])$(k).addEventListener('change',()=>set({[k]:$(k).value}));for(const k of ['mass','thickness'])$(k).addEventListener('input',()=>set({[k]:Number($(k).value)}));$('skip').addEventListener('change',()=>set({skip_units:$('skip').checked}));function reset(){p={...initial};render();return result;}$('reset').addEventListener('click',reset);window.CourseLab={set,reset,state:()=>JSON.parse(JSON.stringify(result))};reset();
})();

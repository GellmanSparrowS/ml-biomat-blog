(() => {
const zh=document.documentElement.lang.startsWith('zh'),el=k=>document.getElementById('E01-'+k),defaults={surface:20,salt:0};let p={...defaults};
function state(){return {...p,trueRatio:10,apparentRatio:(1+p.surface/1000)/(.1+p.salt/1000),wetMass:1+p.surface/1000,dryMass:.1+p.salt/1000};}
function render(){for(const k of ['surface','salt']){el(k).value=p[k];el(k+'-value').textContent=p[k];}const s=state(),x=v=>185+540*v/12;let g='<rect width="800" height="360" fill="#faf9f5"/>';
for(let i=0;i<=12;i+=2){g+=`<path d="M${x(i)} 55V270" stroke="#dce4e7"/><text x="${x(i)}" y="300" text-anchor="middle" font-size="16">${i}</text>`;}
for(const [v,y,label,color] of [[10,90,zh?'真实质量比':'True ratio','#186e83'],[s.apparentRatio,200,zh?'表观质量比':'Apparent ratio','#cc803f']]){g+=`<rect x="185" y="${y-22}" width="${x(v)-185}" height="44" fill="${color}"/><text x="170" y="${y+6}" text-anchor="end" font-size="18">${label}</text><text x="${x(v)+7}" y="${y+6}" font-size="17">${v.toFixed(3)}</text>`;}
g+=`<text x="440" y="342" text-anchor="middle" font-size="17">${zh?'湿质量 / 干质量（无量纲）':'Wet mass / dry mass (dimensionless)'}</text>`;el('plot').innerHTML=g;
el('readout').textContent=zh?`湿称量 ${s.wetMass.toFixed(3)} g；干称量 ${s.dryMass.toFixed(3)} g；真实质量比 10.000；表观质量比 ${s.apparentRatio.toFixed(3)}；相对偏差 ${((s.apparentRatio/10-1)*100).toFixed(2)}%。`:`Wet weighing ${s.wetMass.toFixed(3)} g; dry weighing ${s.dryMass.toFixed(3)} g; true ratio 10.000; apparent ratio ${s.apparentRatio.toFixed(3)}; relative bias ${((s.apparentRatio/10-1)*100).toFixed(2)}%.`;
}
function set(next){for(const k of ['surface','salt'])if(k in next)p[k]=Math.min(k==='surface'?50:20,Math.max(0,Number(next[k])));render();return state();}
for(const k of ['surface','salt'])el(k).addEventListener('input',()=>set({[k]:+el(k).value}));el('clear').addEventListener('click',()=>set({surface:0,salt:0}));el('reset').addEventListener('click',()=>{p={...defaults};render();});window.CourseLab={set,state,reset(){p={...defaults};render();return state();}};render();
})();

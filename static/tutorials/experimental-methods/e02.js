(() => {
const zh=document.documentElement.lang.startsWith('zh'),el=k=>document.getElementById('E02-'+k),defaults={cycles:1,removal:.7,filler:20};let p={...defaults};
function calc(n){const corrected=80+20*(1-p.removal)**n;return {correctedPercent:corrected,rawPercent:p.filler+(100-p.filler)*corrected/100};}
function state(){return {...p,...calc(p.cycles),truePolymerPercent:80};}
function render(){for(const k of ['cycles','removal','filler']){el(k).value=p[k];el(k+'-value').textContent=p[k];}const s=state(),x=v=>85+63*v,y=v=>335-12*(v-78);let g='<rect width="800" height="420" fill="#faf9f5"/>';
for(let n=0;n<=10;n+=2)g+=`<text x="${x(n)}" y="362" text-anchor="middle" font-size="15">${n}</text>`;
for(let v=80;v<=100;v+=5)g+=`<path d="M85 ${y(v)}H715" stroke="#dce4e7"/><text x="73" y="${y(v)+5}" text-anchor="end" font-size="15">${v}</text>`;
for(const [key,color] of [['rawPercent','#8160a1'],['correctedPercent','#186e83']]){let d='';for(let n=0;n<=10;n++)d+=`${n?'L':'M'}${x(n)} ${y(calc(n)[key])}`;g+=`<path d="${d}" fill="none" stroke="${color}" stroke-width="3"/><circle cx="${x(p.cycles)}" cy="${y(s[key])}" r="6" fill="${color}"/>`;}
g+=`<path d="M85 ${y(80)}H715" stroke="#cd803f" stroke-dasharray="6 5"/><text x="85" y="26" font-size="15">${zh?'紫：总残留；蓝：聚合物校正；虚线：真实网络比例':'Purple: total residue; blue: polymer-corrected; dashed: true network fraction'}</text><text x="400" y="406" text-anchor="middle" font-size="17">${zh?'提取循环次数':'Extraction cycle'}</text><text x="23" y="215" transform="rotate(-90 23 215)" text-anchor="middle" font-size="17">${zh?'残留质量分数 / %':'Remaining mass fraction / %'}</text>`;el('plot').innerHTML=g;
el('readout').textContent=zh?`第 ${p.cycles} 轮：总残留 ${s.rawPercent.toFixed(3)}%；扣填料后的聚合物残留 ${s.correctedPercent.toFixed(3)}%；真实聚合物网络比例 80%。`:`Cycle ${p.cycles}: total residue ${s.rawPercent.toFixed(3)}%; polymer-corrected residue ${s.correctedPercent.toFixed(3)}%; true polymer network fraction 80%.`;
}
function set(next){if('cycles'in next)p.cycles=Math.round(Math.min(10,Math.max(0,+next.cycles)));if('removal'in next)p.removal=Math.min(.9,Math.max(.1,+next.removal));if('filler'in next)p.filler=Math.min(50,Math.max(0,+next.filler));render();return state();}
for(const k of ['cycles','removal','filler'])el(k).addEventListener('input',()=>set({[k]:+el(k).value}));el('next').addEventListener('click',()=>set({cycles:p.cycles+1}));el('reset').addEventListener('click',()=>{p={...defaults};render();});window.CourseLab={set,state,reset(){p={...defaults};render();return state();}};render();
})();

(() => {
const zh=document.documentElement.lang.startsWith('zh'),el=k=>document.getElementById('M08-'+k),defaults={gap:1,slip:.2,speed:1};let p={...defaults};
function state(){return {...p,apparentViscosity:2*p.gap/(p.gap+2*p.slip),bulkRate:p.speed/(p.gap+2*p.slip),apparentRate:p.speed/p.gap,stress:2*p.speed/(p.gap+2*p.slip)};}
function render(){
 for(const k of ['gap','slip','speed']){el(k).value=p[k];el(k+'-value').textContent=p[k];}
 const s=state(),x=v=>90+620*v/p.speed,y=v=>340-270*v;
 let g='<rect width="800" height="420" fill="#faf9f5"/>';
 for(let i=0;i<=4;i++){let q=i/4;g+=`<path d="M90 ${y(q)}H710M${x(p.speed*q)} 70V340" stroke="#dbe2e4"/><text x="77" y="${y(q)+5}" text-anchor="end" font-size="14">${(p.gap*q).toFixed(2)}</text><text x="${x(p.speed*q)}" y="365" text-anchor="middle" font-size="14">${(p.speed*q).toFixed(2)}</text>`;}
 const u0=p.speed*p.slip/(p.gap+2*p.slip),u1=p.speed*(p.gap+p.slip)/(p.gap+2*p.slip);
 g+=`<path d="M90 340L710 70" fill="none" stroke="#99aab1" stroke-width="2" stroke-dasharray="6 6"/><path d="M${x(u0)} 340L${x(u1)} 70" fill="none" stroke="#186e83" stroke-width="4"/><path d="M90 340H${x(u0)}M${x(u1)} 70H710" stroke="#cc803f" stroke-width="5"/><text x="400" y="402" text-anchor="middle" font-size="16">${zh?'流体速度 / mm·s⁻¹':'Fluid velocity / mm·s⁻¹'}</text><text x="22" y="205" transform="rotate(-90 22 205)" text-anchor="middle" font-size="16">${zh?'距离下壁高度 / mm':'Height above lower wall / mm'}</text><text x="90" y="26" font-size="14">${zh?'蓝线：体相速度；橙线：壁面滑移；虚线：无滑移参照':'Blue: bulk velocity; orange: wall slip; dashed: no-slip reference'}</text>`;
 el('plot').innerHTML=g;el('readout').textContent=zh?`真实黏度 2.000 Pa·s；表观黏度 ${s.apparentViscosity.toFixed(3)} Pa·s；内部剪切速率 ${s.bulkRate.toFixed(3)} s⁻¹；表观剪切速率 ${s.apparentRate.toFixed(3)} s⁻¹；应力 ${s.stress.toFixed(3)} Pa。`:`Bulk viscosity 2.000 Pa·s; apparent viscosity ${s.apparentViscosity.toFixed(3)} Pa·s; bulk shear rate ${s.bulkRate.toFixed(3)} s⁻¹; apparent shear rate ${s.apparentRate.toFixed(3)} s⁻¹; stress ${s.stress.toFixed(3)} Pa.`;
}
function set(v){for(const k of ['gap','slip','speed'])if(k in v){const e=el(k);p[k]=Math.max(+e.min,Math.min(+e.max,+v[k]));}render();}
function reset(){p={...defaults};render();}
for(const k of ['gap','slip','speed'])el(k).addEventListener('input',()=>set({[k]:+el(k).value}));el('noslip').addEventListener('click',()=>set({slip:0}));el('reset').addEventListener('click',reset);window.CourseLab={set,state,reset};render();
})();

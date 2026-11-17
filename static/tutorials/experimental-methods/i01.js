(() => {
  const zh = document.documentElement.lang.startsWith('zh');
  const state = {na: 1.3, separation: 0.3, pixel: 0.1};
  const defaults = {...state};
  const plot = document.getElementById('I01-plot');
  const result = document.getElementById('I01-result');
  const controls = Object.fromEntries(Object.keys(state).map(k => [k, document.getElementById('I01-'+k)]));
  const text = (a,b) => zh ? a : b;
  function draw() {
    const sigma = 0.21*0.520/state.na;
    const profile = x => Math.exp(-0.5*((x-state.separation/2)/sigma)**2)+Math.exp(-0.5*((x+state.separation/2)/sigma)**2);
    const sx = x => 70+(x+1)*340, sy = y => 320-y*130;
    let d='';for(let i=0;i<=400;i++){const x=-1+i/200;d+=(i?' L':'M')+sx(x).toFixed(2)+' '+sy(profile(x)).toFixed(2);}
    let dots='';for(let x=-1;x<=1.00001;x+=state.pixel)dots+=`<circle cx="${sx(x)}" cy="${sy(profile(x))}" r="4" fill="#bd624b"/>`;
    let ticks='';for(const x of [-1,-.5,0,.5,1])ticks+=`<text x="${sx(x)}" y="344" text-anchor="middle">${x.toFixed(1)}</text>`;
    plot.innerHTML=`<rect width="800" height="390" fill="#faf9f5"/><g font-family="Arial,Microsoft YaHei,sans-serif" font-size="15" fill="#243b45"><path d="M70 35V320H750" fill="none" stroke="#789099"/><text x="70" y="22">${text('相对强度','Relative intensity')}</text><path d="${d}" fill="none" stroke="#168477" stroke-width="3"/>${dots}${ticks}<text x="410" y="375" text-anchor="middle">${text('横向位置 / μm','Lateral position / μm')}</text><text x="52" y="325" text-anchor="end">0</text><text x="52" y="195" text-anchor="end">1</text><text x="52" y="65" text-anchor="end">2</text></g>`;
    const r=.61*.520/state.na;
    result.textContent=text(`NA=${state.na.toFixed(2)}；间距=${state.separation.toFixed(2)} μm；像素=${state.pixel.toFixed(2)} μm。瑞利尺度=${r.toFixed(3)} μm；每个分辨尺度约${(r/state.pixel).toFixed(2)}个像素。`,`NA=${state.na.toFixed(2)}; separation=${state.separation.toFixed(2)} μm; pixel=${state.pixel.toFixed(2)} μm. Rayleigh scale=${r.toFixed(3)} μm; ${(r/state.pixel).toFixed(2)} pixels per resolution scale.`);
  }
  function set(p){for(const k of Object.keys(state))if(k in p){const v=Number(p[k]);if(Number.isFinite(v)){state[k]=Math.min(Number(controls[k].max),Math.max(Number(controls[k].min),v));controls[k].value=state[k];}}draw();}
  const listeners=[];
  for(const [k,c] of Object.entries(controls)){const f=()=>set({[k]:c.value});c.addEventListener('input',f);listeners.push([c,'input',f]);}
  const reset=()=>set(defaults),button=document.getElementById('I01-reset');button.addEventListener('click',reset);listeners.push([button,'click',reset]);
  window.CourseLab={set,state:()=>({...state,rayleigh_um:.61*.520/state.na,samples_per_resolution:.61*.520/state.na/state.pixel}),reset,destroy(){for(const [e,t,f] of listeners)e.removeEventListener(t,f);}};
  draw();
})();

(()=>{'use strict';
const root=document.querySelector('#M24-lab');if(!root)return;
const zh=document.documentElement.lang.startsWith('zh'),svg=root.querySelector('svg');
const settings={gamma:.9,slip:0,iterations:0};let values=Array(48).fill(0),best=Array(48).fill(0);
const moves=[[-1,0],[0,1],[1,0],[0,-1]],arrows=['↑','→','↓','←'];
function step(s,a){const r=Math.floor(s/12),c=s%12;const nr=Math.max(0,Math.min(3,r+moves[a][0])),nc=Math.max(0,Math.min(11,c+moves[a][1]));if(nr===3&&nc>0&&nc<11)return[36,-100,false];return[nr*12+nc,-1,nr*12+nc===47]}
function target(s,a,old){let total=0;for(const [b,p] of [[a,1-settings.slip],[(a+1)%4,settings.slip/2],[(a+3)%4,settings.slip/2]]){const [n,r,end]=step(s,b);total+=p*(r+(end?0:settings.gamma*old[n]))}return total}
function sweep(){const next=values.slice();for(let s=0;s<48;s++){if(s===47||(s>=37&&s<=46))continue;const scores=moves.map((_,a)=>target(s,a,values));next[s]=Math.max(...scores);best[s]=scores.indexOf(next[s])}values=next;settings.iterations++}
function draw(){let content='';for(let s=0;s<48;s++){const row=Math.floor(s/12),col=s%12,x=35+col*72,y=35+row*66,cliff=row===3&&col>0&&col<11;const depth=Math.min(1,Math.abs(values[s])/35),fill=cliff?'#b04743':s===47?'#c8dfd4':`rgb(${Math.round(241-depth*100)},${Math.round(246-depth*50)},${Math.round(249-depth*20)})`;content+=`<rect x="${x}" y="${y}" width="69" height="63" rx="4" fill="${fill}"/><text x="${x+34}" y="${y+23}" text-anchor="middle" font-size="17" fill="${cliff?'white':'#173540'}">${cliff?'×':s===47?'G':s===36?'S '+arrows[best[s]]:arrows[best[s]]}</text><text x="${x+34}" y="${y+46}" text-anchor="middle" font-size="12" fill="${cliff?'white':'#173540'}">${cliff?'−100':values[s].toFixed(2)}</text>`}
content+=`<text x="35" y="326" font-size="14" fill="#253b45">${zh?'颜色与数字：期望折扣回报；箭头：当前最优动作。':'Colour and numbers: expected discounted return; arrows: greedy action.'}</text><text x="35" y="352" font-size="13" fill="#4d626a">${zh?'红色悬崖：回到 S；绿色 G：终止。每个普通动作的即时奖励为 −1。':'Red cliff: return to S. Green G: terminal. Each ordinary step gives reward −1.'}</text>`;svg.innerHTML=content;
root.querySelector('[data-report]').textContent=zh?`已更新 ${settings.iterations} 轮；起点价值 ${values[36].toFixed(6)}。`:`${settings.iterations} sweeps; start value ${values[36].toFixed(6)}.`;
for(const key of ['gamma','slip']){root.querySelector(`[data-control="${key}"]`).value=settings[key];root.querySelector(`[data-value="${key}"]`).textContent=settings[key].toFixed(2)}}
function set(params={}){if(params.gamma!==undefined)settings.gamma=Math.max(0,Math.min(.99,Number(params.gamma)));if(params.slip!==undefined)settings.slip=Math.max(0,Math.min(.4,Number(params.slip)));const n=Math.max(0,Math.min(200,Math.round(params.iterations??settings.iterations)));values=Array(48).fill(0);best=Array(48).fill(0);settings.iterations=0;for(let k=0;k<n;k++)sweep();draw();return state()}
function state(){return{...settings,startValue:values[36],goalValue:values[47],values:values.slice(),actions:best.slice()}}
function reset(){return set({gamma:.9,slip:0,iterations:0})}
root.querySelectorAll('[data-control]').forEach(el=>el.addEventListener('input',()=>set({[el.dataset.control]:Number(el.value),iterations:settings.iterations})));
root.querySelector('[data-one]').addEventListener('click',()=>{sweep();draw()});root.querySelector('[data-many]').addEventListener('click',()=>{for(let k=0;k<30;k++)sweep();draw()});root.querySelector('[data-reset]').addEventListener('click',reset);
window.CourseLab={set,state,reset};reset();
})();

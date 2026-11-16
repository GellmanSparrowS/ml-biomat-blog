(function () {
  'use strict';
  const root = document.getElementById('P15-lab');
  if (!root) return;
  const zh = document.documentElement.lang.startsWith('zh');
  const tr = (a, b) => zh ? a : b;
  const data = [[0, .032], [.1, .111], [.2, .205], [.3, .296], [.4, .389], [.5, .481]];
  const el = name => root.querySelector('#P15-' + name);
  let current = {index: 3, xmax: .6, ymax: .55};
  const clean = n => Number(n.toFixed(10));
  function draw(svg, xmax, ymax, title) {
    const left = 69, top = 43, width = 385, height = 254;
    const X = x => left + x / xmax * width;
    const Y = y => top + height - y / ymax * height;
    let out = '<title>' + title + '</title><rect width="480" height="370" fill="white"/>';
    out += '<g font-family="inherit" font-size="14" fill="#202e39"><text x="69" y="24" font-size="17" font-weight="600">' + title + '</text>';
    for (let i = 0; i <= 5; i++) {
      const y = ymax * i / 5, x = xmax * i / 5;
      out += `<line x1="${left}" y1="${Y(y)}" x2="${left+width}" y2="${Y(y)}" stroke="#dce3e8"/><text x="${left-10}" y="${Y(y)+5}" text-anchor="end">${y.toFixed(2)}</text>`;
      out += `<line x1="${X(x)}" y1="${top+height}" x2="${X(x)}" y2="${top+height+5}" stroke="#202e39"/><text x="${X(x)}" y="${top+height+23}" text-anchor="middle">${x.toFixed(2)}</text>`;
    }
    out += `<path d="M ${left} ${top} V ${top+height} H ${left+width}" fill="none" stroke="#202e39" stroke-width="1.5"/>`;
    data.forEach(([x,y]) => {out += `<circle cx="${X(x)}" cy="${Y(y)}" r="5.5" fill="#28658c"/>`;});
    const [x,y] = data[current.index];
    out += `<path d="M ${X(x)} ${top+height} V ${Y(y)} H ${left}" stroke="#b64a35" fill="none" stroke-dasharray="5 4"/>`;
    out += `<circle cx="${X(x)}" cy="${Y(y)}" r="9" fill="none" stroke="#b64a35" stroke-width="2"/>`;
    out += `<text x="${left+width/2}" y="350" text-anchor="middle">${tr('浓度 / mmol L⁻¹','Concentration / mmol L⁻¹')}</text>`;
    out += `<text x="19" y="${top+height/2}" text-anchor="middle" transform="rotate(-90 19 ${top+height/2})">${tr('吸光度 / 无量纲','Absorbance / dimensionless')}</text></g>`;
    svg.innerHTML = out;
  }
  function state() {
    const [c,a] = data[current.index];
    return {...current,c,a,u:c/current.xmax,v:a/current.ymax,reference_u:c/.6,reference_v:a/.55};
  }
  function render() {
    const s = state();
    ['index','xmax','ymax'].forEach(k => {el(k).value=current[k];});
    el('index-label').textContent = current.index + 1;
    el('xmax-label').textContent = current.xmax.toFixed(2);
    el('ymax-label').textContent = current.ymax.toFixed(2);
    ['c','a','u','v'].forEach(k => {el(k).textContent = s[k].toFixed(k==='c'||k==='a'?3:4);});
    draw(el('reference'),.6,.55,tr('原范围：固定对照','Original limits: fixed reference'));
    draw(el('current'),current.xmax,current.ymax,tr('当前范围：相同数据','Current limits: identical data'));
    el('command').textContent = `ax.set(xlim=(0, ${current.xmax.toFixed(2)}), ylim=(0, ${current.ymax.toFixed(2)}))`;
    el('explanation').textContent = tr(`第${s.index+1}条记录的数值保持不变。它在右图位于全宽的${(100*s.u).toFixed(2)}%、全高的${(100*s.v).toFixed(2)}%处；比例从左下角起算。`, `Record ${s.index+1} retains its original values. In the right panel it lies at ${(100*s.u).toFixed(2)}% of the width and ${(100*s.v).toFixed(2)}% of the height, measured from the lower-left corner.`);
  }
  function set(p) {
    if ('index' in p) current.index = Math.max(0,Math.min(5,Math.round(Number(p.index))));
    if ('xmax' in p) current.xmax = clean(Math.max(.6,Math.min(1.2,Number(p.xmax))));
    if ('ymax' in p) current.ymax = clean(Math.max(.55,Math.min(1.1,Number(p.ymax))));
    render(); return state();
  }
  function reset() {current={index:3,xmax:.6,ymax:.55};render();return state();}
  ['index','xmax','ymax'].forEach(k => el(k).addEventListener('input',()=>set({[k]:Number(el(k).value)})));
  el('reset').addEventListener('click',reset);
  window.CourseLab={set,state,reset};render();
})();

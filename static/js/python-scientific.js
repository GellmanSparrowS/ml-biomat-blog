(()=>{'use strict';
const root=document.querySelector('.python-course');if(!root)return;
const article=root.querySelector('.python-article'),zh=root.dataset.lang==='zh';
for(const link of document.querySelectorAll('.lang-switch a[href]'))link.addEventListener('click',()=>{if(location.hash)link.hash=location.hash;});
article.querySelectorAll('pre').forEach(pre=>pre.tabIndex=0);
article.addEventListener('click',async event=>{
 const copy=event.target.closest('[data-copy]'),download=event.target.closest('[data-download-code]');
 if(copy){const code=copy.closest('.code-example').querySelector('pre code');let ok=false;try{await navigator.clipboard.writeText(code.textContent);ok=true;}catch{const area=document.createElement('textarea');area.value=code.textContent;area.style.position='fixed';area.style.left='-9999px';document.body.append(area);area.select();ok=document.execCommand('copy');area.remove();copy.focus();}copy.textContent=zh?(ok?'已复制':'请选择代码复制'):(ok?'Copied':'Select code to copy');copy.dataset.copySuccess=String(ok);setTimeout(()=>copy.textContent=zh?'复制':'Copy',1800);}
 if(download){const card=download.closest('.code-example'),url=URL.createObjectURL(new Blob([card.querySelector('pre code').textContent],{type:'text/plain;charset=utf-8'})),a=document.createElement('a');a.href=url;a.download=card.dataset.filename||'example.py';document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),2000);}
});
for(const svg of article.querySelectorAll('.science-lab svg')){
 if(svg.closest('.js-plotly-plot')||svg.parentElement.closest('svg'))continue;
 const view=svg.viewBox?.baseVal;if(!view||view.width<450)continue;
 const placement=getComputedStyle(svg),frame=document.createElement('div');frame.className='lab-plot-scroll';
 if(placement.gridColumn!=='auto')frame.style.gridColumn=placement.gridColumn;if(placement.gridRow!=='auto')frame.style.gridRow=placement.gridRow;
 for(let parent=svg.parentElement;parent&&!parent.classList.contains('science-lab');parent=parent.parentElement)if(getComputedStyle(parent).display==='grid')parent.classList.add('lab-plot-grid');
 frame.tabIndex=0;frame.setAttribute('role','region');frame.setAttribute('aria-label',zh?'科学图形，可横向滚动查看':'Scientific plot; scroll horizontally to inspect');frame.style.setProperty('--plot-reading-width',Math.max(520,view.width)+'px');svg.before(frame);frame.append(svg);
}
})();

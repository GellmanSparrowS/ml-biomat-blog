/* Shared article navigation and direct scientific-figure enlargement. */
(()=>{'use strict';
const root=document.querySelector('.biomat-course');if(!root)return;
const en=root.dataset.lang==='en',toc=root.querySelector('.bc-toc details');
const mobile=matchMedia('(max-width:760px)');
function sizeToc(){if(toc)toc.open=!mobile.matches;}
sizeToc();mobile.addEventListener('change',sizeToc);
const sections=[...root.querySelectorAll('.language-pane>section[id]')];
const links=[...root.querySelectorAll('.bc-toc a')];let queued=false;
function activeSection(){queued=false;const s=sections.find(el=>el.getBoundingClientRect().bottom>145)||sections.at(-1);for(const link of links)link.classList.toggle('active',link.hash==='#'+s?.id);}
addEventListener('scroll',()=>{if(!queued){queued=true;requestAnimationFrame(activeSection)}},{passive:true});activeSection();
// Map stable section anchors when following the site's real translated URL.
for(const link of document.querySelectorAll('.lang-switch a[href]')){
 link.addEventListener('click',()=>{if(!location.hash)return;const match=location.hash.match(/^#(?:zh|en)-(.*)$/);if(match){const target=link.dataset.language;link.hash=target+'-'+match[1]}});
}
const viewer=document.createElement('dialog');viewer.className='bc-figure-dialog';viewer.setAttribute('aria-label',en?'Scientific figure':'科学图示');viewer.lang=en?'en':'zh-CN';
viewer.innerHTML='<div class="bc-figure-toolbar"><button type="button" data-zoom-out aria-label="'+(en?'Zoom out':'缩小')+'">−</button><button type="button" data-zoom-in aria-label="'+(en?'Zoom in':'放大')+'">+</button><button type="button" data-zoom-fit>'+(en?'Fit':'适应窗口')+'</button><button type="button" data-close aria-label="'+(en?'Close':'关闭')+'">×</button></div><div class="bc-figure-stage" tabindex="0"></div><p class="bc-figure-caption"></p>';
document.body.append(viewer);const stage=viewer.querySelector('.bc-figure-stage');let zoom=1,width=720,source=null,serial=0;
function setZoom(value){zoom=Math.max(.1,Math.min(5,value));const svg=stage.firstElementChild;if(svg){svg.style.width=(width*zoom)+'px';svg.style.height='auto'}viewer.dataset.zoom=String(zoom);}
function fit(){setZoom(Math.min(1,stage.clientWidth/width));}
function open(graphic){
 source=graphic;const clone=graphic.cloneNode(true),prefix='bc-view-'+(++serial)+'-',ids=new Map();
 clone.querySelectorAll('[id]').forEach(el=>{ids.set(el.id,prefix+el.id);el.id=prefix+el.id});
 clone.querySelectorAll('*').forEach(el=>[...el.attributes].forEach(attr=>{let value=attr.value;ids.forEach((next,old)=>{value=value.split('url(#'+old+')').join('url(#'+next+')');if(value==='#'+old)value='#'+next;if(attr.name==='aria-labelledby'||attr.name==='aria-describedby')value=value.split(' ').map(k=>k===old?next:k).join(' ')});if(value!==attr.value)el.setAttribute(attr.name,value)}));
 clone.removeAttribute('id');clone.removeAttribute('tabindex');clone.setAttribute('role','img');clone.style.cursor='default';
 width=graphic.viewBox.baseVal.width||graphic.getBoundingClientRect().width||720;stage.replaceChildren(clone);
 const caption=graphic.closest('figure')?.querySelector('figcaption')?.textContent||graphic.closest('.lab')?.querySelector('.lab-caption')?.textContent||'';
 viewer.querySelector('.bc-figure-caption').textContent=caption;viewer.querySelector('.bc-figure-caption').hidden=!caption;
 viewer.showModal();fit();stage.scrollTop=stage.scrollLeft=0;viewer.querySelector('[data-close]').focus();
}
viewer.querySelector('[data-zoom-out]').addEventListener('click',()=>setZoom(zoom/1.25));viewer.querySelector('[data-zoom-in]').addEventListener('click',()=>setZoom(zoom*1.25));viewer.querySelector('[data-zoom-fit]').addEventListener('click',fit);viewer.querySelector('[data-close]').addEventListener('click',()=>viewer.close());
viewer.addEventListener('click',event=>{if(event.target!==viewer)return;const rect=viewer.getBoundingClientRect();if(event.clientX<rect.left||event.clientX>rect.right||event.clientY<rect.top||event.clientY>rect.bottom)viewer.close()});
viewer.addEventListener('close',()=>{stage.replaceChildren();source?.focus({preventScroll:true})});
stage.addEventListener('keydown',event=>{if(event.key==='+'||event.key==='='){event.preventDefault();setZoom(zoom*1.25)}else if(event.key==='-'){event.preventDefault();setZoom(zoom/1.25)}});
root.querySelectorAll('.science-figure>.figure-wrap>svg,.lab svg').forEach(graphic=>{
 if(graphic.closest('.math'))return;
 const existing=graphic.getAttribute('aria-label')||graphic.querySelector('title')?.textContent;
 graphic.setAttribute('role','button');graphic.setAttribute('tabindex','0');graphic.setAttribute('aria-haspopup','dialog');graphic.setAttribute('aria-label',existing||(en?'Open scientific figure':'打开科学图示'));
 graphic.addEventListener('click',()=>open(graphic));graphic.addEventListener('keydown',event=>{if(event.key==='Enter'||event.key===' '){event.preventDefault();open(graphic)}});
});
})();

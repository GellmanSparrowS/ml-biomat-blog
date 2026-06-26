// ml-biomat.com — enhanced: code copy (always visible), search, TOC, back-to-top
(function(){
document.addEventListener('DOMContentLoaded',function(){
    // === CODE COPY: always visible, clipboard icon ===
    document.querySelectorAll('pre').forEach(function(block){
        block.style.position='relative';
        var b=document.createElement('button');
        b.className='copy-btn';
        b.innerHTML='<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>';
        b.title='Copy code';
        b.onclick=function(){navigator.clipboard.writeText(block.textContent.trim()).then(function(){b.innerHTML='&#10003;';setTimeout(function(){b.innerHTML='<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>';},2000);});};
        block.appendChild(b);
    });

    // === BACK TO TOP ===
    var btt=document.createElement('button');
    btt.id='back-to-top';
    btt.innerHTML='&#8593;';
    btt.title='Back to top';
    btt.onclick=function(){window.scrollTo({top:0,behavior:'smooth'});};
    document.body.appendChild(btt);
    window.addEventListener('scroll',function(){var v=window.scrollY>400?'1':'0';btt.style.opacity=v;btt.style.pointerEvents=v==='1'?'auto':'none';});

    // === TABLE OF CONTENTS ===
    var content=document.querySelector('.content');
    var hs=document.querySelectorAll('.content h2,.content h3');
    if(content&&hs.length>2){
        var toc=document.createElement('details');
        toc.className='toc';
        toc.innerHTML='<summary>Table of Contents</summary><ul></ul>';
        var ul=toc.querySelector('ul');
        hs.forEach(function(h,i){var id='h-'+i;h.id=id;ul.innerHTML+='<li style="'+(h.tagName==='H3'?'padding-left:1rem':'')+'"><a href="#'+id+'">'+h.textContent+'</a></li>';});
        content.insertBefore(toc,content.firstChild);
    }
});

// === SEARCH ===
var searchData=null,loaded=false;
function loadSD(cb){if(loaded){cb();return;}fetch('/search.json').then(function(r){return r.json();}).then(function(d){searchData=d;loaded=true;cb();});}
function doSearch(q){if(!q||q.length<2){hideRes();return;}q=q.toLowerCase();var r=searchData.filter(function(p){return p.title.toLowerCase().indexOf(q)>=0||(p.description||'').toLowerCase().indexOf(q)>=0||(p.tags||[]).some(function(t){return t.toLowerCase().indexOf(q)>=0;});});showRes(r.slice(0,8),q);}
function showRes(r,q){var dd=document.getElementById('search-dd');if(!dd){dd=document.createElement('div');dd.id='search-dd';dd.className='search-dd';document.body.appendChild(dd);}if(r.length===0){dd.innerHTML='<div class="search-item" style="color:var(--c-muted)">No results</div>';}else{dd.innerHTML=r.map(function(p){return '<a class="search-item" href="/posts/'+p.slug+'/"><strong>'+p.title+'</strong><span style="font-size:.75rem;color:var(--c-muted);display:block">'+(p.description||'')+'</span></a>';}).join('');}dd.style.display='block';}
function hideRes(){var dd=document.getElementById('search-dd');if(dd)dd.style.display='none';}
document.addEventListener('DOMContentLoaded',function(){var inp=document.getElementById('search-input');if(!inp)return;var timer;inp.addEventListener('input',function(){clearTimeout(timer);var q=inp.value.trim();if(q.length<2){hideRes();return;}timer=setTimeout(function(){loadSD(function(){doSearch(q);});},200);});inp.addEventListener('focus',function(){if(inp.value.trim().length>=2)loadSD(function(){doSearch(inp.value.trim());});});document.addEventListener('click',function(e){if(!e.target.closest('#search-input')&&!e.target.closest('#search-dd'))hideRes();});});
})();

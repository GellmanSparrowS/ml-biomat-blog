// ml-biomat.com — enhanced code copy + search
(function(){
// === CODE COPY (always visible, icon-style) ===
document.addEventListener('DOMContentLoaded', function(){
    document.querySelectorAll('pre').forEach(function(block){
        var wrapper = document.createElement('div');
        wrapper.style.position = 'relative';
        block.parentNode.insertBefore(wrapper, block);
        wrapper.appendChild(block);

        var btn = document.createElement('button');
        btn.className = 'copy-btn';
        btn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>';
        btn.title = 'Copy code';
        btn.onclick = function(){
            var code = block.textContent.trim();
            navigator.clipboard.writeText(code).then(function(){
                btn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"></polyline></svg>';
                btn.classList.add('copied');
                setTimeout(function(){
                    btn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>';
                    btn.classList.remove('copied');
                }, 2000);
            });
        };
        wrapper.appendChild(btn);
    });
});

// === SEARCH (improved) ===
var searchData = null, searchLoaded = false;

function loadSearchData(cb){
    if(searchLoaded){ cb(); return; }
    fetch('/search.json').then(function(r){ return r.json(); }).then(function(d){
        searchData = d; searchLoaded = true; cb();
    }).catch(function(){ console.log('Search data not loaded'); });
}

function doSearch(q){
    var resultsEl = document.getElementById('search-results');
    var inputEl = document.getElementById('search-input-big');
    if(!q || q.length < 2){
        if(resultsEl) resultsEl.innerHTML = '';
        return;
    }
    q = q.toLowerCase();
    var results = searchData.filter(function(p){
        return p.title.toLowerCase().indexOf(q) >= 0 ||
               (p.description||'').toLowerCase().indexOf(q) >= 0 ||
               (p.tags||[]).some(function(t){ return t.toLowerCase().indexOf(q) >= 0; });
    });
    if(resultsEl){
        if(results.length === 0){
            resultsEl.innerHTML = '<p style="color:var(--c-muted);text-align:center;padding:2rem">No results found.</p>';
        } else {
            resultsEl.innerHTML = results.map(function(p){
                var tags = (p.tags||[]).slice(0,3).map(function(t){ return '<span class="tag-pill">'+t+'</span>'; }).join('');
                return '<a class="post-card" href="/posts/'+p.slug+'/" style="text-decoration:none;display:block"><span class="card-lang '+p.lang+'">'+(p.lang==='en'?'EN':'\u4e2d\u6587')+'</span><h3>'+p.title+'</h3><p class="card-desc">'+(p.description||'')+'</p><div class="card-tags">'+tags+'</div></a>';
            }).join('');
        }
    }
}

// Init search on DOM ready
document.addEventListener('DOMContentLoaded', function(){
    var input = document.getElementById('search-input');
    if(!input) return;
    var timer;
    input.addEventListener('input', function(){
        clearTimeout(timer); var q = input.value.trim();
        if(q.length < 2){ hideResults(); return; }
        timer = setTimeout(function(){ loadSearchData(function(){ doSearchDropdown(q); }); }, 200);
    });
    input.addEventListener('focus', function(){
        if(input.value.trim().length >= 2) loadSearchData(function(){ doSearchDropdown(input.value.trim()); });
    });
    document.addEventListener('click', function(e){
        if(!e.target.closest('#search-input') && !e.target.closest('#search-dropdown')) hideResults();
    });

    // Big search on /search/ page
    var bigInput = document.getElementById('search-input-big');
    if(bigInput){
        bigInput.addEventListener('input', function(){
            clearTimeout(timer);
            timer = setTimeout(function(){
                loadSearchData(function(){ doSearch(bigInput.value.trim()); });
            }, 200);
        });
        // Handle URL param ?q=...
        var params = new URLSearchParams(window.location.search);
        var q = params.get('q');
        if(q){
            bigInput.value = q;
            loadSearchData(function(){ doSearch(q); });
        }
    }
});

function doSearchDropdown(q){
    var results = searchData.filter(function(p){
        return p.title.toLowerCase().indexOf(q) >= 0 ||
               (p.description||'').toLowerCase().indexOf(q) >= 0 ||
               (p.tags||[]).some(function(t){ return t.toLowerCase().indexOf(q) >= 0; });
    });
    showDropdown(results.slice(0, 8), q);
}

function showDropdown(results, q){
    var dd = document.getElementById('search-dropdown');
    if(!dd){
        dd = document.createElement('div'); dd.id = 'search-dropdown'; dd.className = 'search-dropdown';
        document.body.appendChild(dd);
    }
    if(results.length === 0){
        dd.innerHTML = '<div class="search-item" style="color:var(--c-muted)">No results</div>';
    } else {
        dd.innerHTML = results.map(function(p){
            return '<a class="search-item" href="/posts/'+p.slug+'/"><strong>'+p.title+'</strong><span style="font-size:.75rem;color:var(--c-muted);display:block">'+(p.description||'')+'</span></a>';
        }).join('');
    }
    dd.style.display = 'block';
}

function hideResults(){
    var dd = document.getElementById('search-dropdown');
    if(dd) dd.style.display = 'none';
}

// === Progress bar + Back to top ===

// Back to top click handler
document.addEventListener('DOMContentLoaded', function(){
    var btn = document.getElementById('back-to-top');
    if(btn){
        btn.addEventListener('click', function(){
            window.scrollTo({top: 0, behavior: 'smooth'});
        });
    }
});

window.addEventListener('scroll', function(){
    var winH = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    var scrolled = (window.scrollY / winH) * 100;
    var bar = document.getElementById('progress-bar');
    if(bar) bar.style.width = scrolled + '%';
    var btn = document.getElementById('back-to-top');
    if(btn) btn.style.display = window.scrollY > 400 ? 'block' : 'none';
});
})();
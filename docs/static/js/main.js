// ml-biomat.com — search + code copy
(function(){
// === CODE COPY ===
document.addEventListener('DOMContentLoaded', function(){
    document.querySelectorAll('pre').forEach(function(block){
        var btn = document.createElement('button');
        btn.className = 'copy-btn';
        btn.textContent = 'Copy';
        btn.onclick = function(){
            navigator.clipboard.writeText(block.textContent.trim()).then(function(){
                btn.textContent = 'Copied!';
                setTimeout(function(){ btn.textContent = 'Copy'; }, 2000);
            });
        };
        block.style.position = 'relative';
        block.appendChild(btn);
    });
});

// === SEARCH ===
var searchData = null;
var searchLoaded = false;

function loadSearchData(cb){
    if(searchLoaded){ cb(); return; }
    fetch('/search.json').then(function(r){ return r.json(); }).then(function(d){
        searchData = d;
        searchLoaded = true;
        cb();
    });
}

function doSearch(q){
    if(!q || q.length < 2){ hideResults(); return; }
    q = q.toLowerCase();
    var results = searchData.filter(function(p){
        return p.title.toLowerCase().indexOf(q) >= 0 ||
               (p.description||'').toLowerCase().indexOf(q) >= 0 ||
               (p.tags||[]).some(function(t){ return t.toLowerCase().indexOf(q) >= 0; });
    });
    showResults(results.slice(0, 8), q);
}

function showResults(results, q){
    var dd = document.getElementById('search-dropdown');
    if(!dd){
        dd = document.createElement('div');
        dd.id = 'search-dropdown';
        dd.className = 'search-dropdown';
        document.body.appendChild(dd);
    }
    if(results.length === 0){
        dd.innerHTML = '<div class="search-item" style="color:var(--c-muted)">No results for "' + q + '"</div>';
    } else {
        dd.innerHTML = results.map(function(p){
            return '<a class="search-item" href="/posts/' + p.slug + '/"><strong>' + p.title + '</strong><span style="font-size:.75rem;color:var(--c-muted);display:block">' + (p.description||'') + '</span></a>';
        }).join('');
    }
    dd.style.display = 'block';
}

function hideResults(){
    var dd = document.getElementById('search-dropdown');
    if(dd) dd.style.display = 'none';
}

// Init search on DOM ready
document.addEventListener('DOMContentLoaded', function(){
    var input = document.getElementById('search-input');
    if(!input) return;
    var timer;
    input.addEventListener('input', function(){
        clearTimeout(timer);
        var q = input.value.trim();
        if(q.length < 2){ hideResults(); return; }
        timer = setTimeout(function(){
            loadSearchData(function(){ doSearch(q); });
        }, 200);
    });
    input.addEventListener('focus', function(){
        if(input.value.trim().length >= 2){
            loadSearchData(function(){ doSearch(input.value.trim()); });
        }
    });
    document.addEventListener('click', function(e){
        if(!e.target.closest('#search-input') && !e.target.closest('#search-dropdown')){
            hideResults();
        }
    });
});
})();
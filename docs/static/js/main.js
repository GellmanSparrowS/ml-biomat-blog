// ml-biomat.com — enhanced code copy + search
(function(){
// === CODE COPY (always visible, icon-style) ===
document.addEventListener('DOMContentLoaded', function(){
    if(window.hljs){window.hljs.highlightAll();}
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


// === HEADING ANCHORS ===
document.addEventListener('DOMContentLoaded',function(){
    document.querySelectorAll('.content h2, .content h3, article h2, article h3').forEach(function(h){
        if(!h.id) h.id = h.textContent.toLowerCase().replace(/[^a-z0-9\u4e00-\u9fff]+/g,'-').replace(/^-|-$/g,'');
        var a = document.createElement('a');
        a.href = '#' + h.id;
        a.className = 'anchor-link';
        a.innerHTML = '#';
        a.title = 'Link to this section';
        a.onclick = function(e){
            e.preventDefault();
            history.pushState(null,null,'#'+h.id);
            h.scrollIntoView({behavior:'smooth'});
            navigator.clipboard.writeText(location.href).catch(function(){});
        };
        h.appendChild(a);
    });
});

// === IMAGE LOADED CLASS ===
document.addEventListener('DOMContentLoaded',function(){
    document.querySelectorAll('img[loading="lazy"]').forEach(function(img){
        if(img.complete) img.classList.add('loaded');
        else img.addEventListener('load',function(){img.classList.add('loaded');});
    });
});

// === IMAGE ZOOM (medium-zoom) ===
(function(){
    var script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/medium-zoom@1/dist/medium-zoom.min.js';
    script.onload = function(){
        mediumZoom('article img, .img-full, .about-card img', {
            margin: 24,
            background: 'rgba(0,0,0,.9)',
            scrollOffset: 0,
        });
    };
    document.head.appendChild(script);
})();

// ===== THEME TOGGLE =====
(function(){
    var KEY = 'ml-biomat-theme';
    function currentTheme(){ return document.documentElement.getAttribute('data-theme'); }
    function render(){
        var btn = document.getElementById('theme-toggle');
        if(btn) btn.textContent = currentTheme() === 'dark' ? '\u2600' : '\u263e';
    }
    function apply(){
        try {
            var saved = localStorage.getItem(KEY);
            if(saved === 'dark' || saved === 'light') document.documentElement.setAttribute('data-theme', saved);
        } catch(e) {}
        render();
    }
    document.addEventListener('DOMContentLoaded', function(){
        apply();
        var btn = document.getElementById('theme-toggle');
        if(btn) btn.addEventListener('click', function(){
            var next = currentTheme() === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', next);
            try { localStorage.setItem(KEY, next); } catch(e) {}
            render();
        });
    });
})();

// ===== TOC SCROLL SPY =====
(function(){
    if(!('IntersectionObserver' in window)) return;
    document.addEventListener('DOMContentLoaded', function(){
        var links = Array.prototype.slice.call(document.querySelectorAll('.toc a[href^="#"]'));
        if(!links.length) return;
        var map = {};
        links.forEach(function(a){
            var h = document.querySelector(a.getAttribute('href'));
            if(h) map[h.id] = a;
        });
        var obs = new IntersectionObserver(function(entries){
            entries.forEach(function(e){
                if(e.isIntersecting){
                    links.forEach(function(a){ a.classList.remove('active'); });
                    var link = map[e.target.id];
                    if(link) link.classList.add('active');
                }
            });
        }, {rootMargin:'-20% 0px -70% 0px', threshold:0});
        Object.keys(map).forEach(function(id){
            var h = document.getElementById(id);
            if(h) obs.observe(h);
        });
    });
})();

// ===== SUBTLE REACTIVE BACKGROUND NETWORK =====
(function(){
    var canvas = document.getElementById('bg-canvas');
    if(!canvas) return;
    if(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    var ctx = canvas.getContext('2d');
    var W = 0, H = 0, nodes = [];
    var mouse = {x:-9999, y:-9999};
    function resize(){
        W = canvas.width = window.innerWidth;
        H = canvas.height = window.innerHeight;
        var n = Math.min(90, Math.max(28, Math.floor(W * H / 25000)));
        nodes = [];
        for(var i = 0; i < n; i++){
            nodes.push({x:Math.random()*W, y:Math.random()*H, vx:(Math.random()-0.5)*0.2, vy:(Math.random()-0.5)*0.2});
        }
    }
    function isDark(){
        var t = document.documentElement.getAttribute('data-theme');
        if(t === 'dark') return true;
        if(t === 'light') return false;
        return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    }
    function step(){
        ctx.clearRect(0, 0, W, H);
        var dark = isDark();
        for(var i = 0; i < nodes.length; i++){
            var a = nodes[i];
            var dx = a.x - mouse.x, dy = a.y - mouse.y, d2 = dx*dx + dy*dy;
            if(d2 < 26000){
                var f = (160 - d2/160) * 0.008;
                a.vx += dx * f || 0.02;
                a.vy += dy * f || 0.02;
            }
            a.vx *= 0.995; a.vy *= 0.995;
            if(Math.abs(a.vx) < 0.02) a.vx += (Math.random()-0.5)*0.04;
            if(Math.abs(a.vy) < 0.02) a.vy += (Math.random()-0.5)*0.04;
            a.x += a.vx; a.y += a.vy;
            if(a.x < -30) a.x = W + 30; if(a.x > W + 30) a.x = -30;
            if(a.y < -30) a.y = H + 30; if(a.y > H + 30) a.y = -30;
        }
        for(var i = 0; i < nodes.length; i++){
            for(var k = i + 1; k < nodes.length; k++){
                var p = nodes[i], q = nodes[k];
                var dd = (p.x-q.x)*(p.x-q.x) + (p.y-q.y)*(p.y-q.y);
                if(dd < 42000){
                    var alpha = (1 - dd/42000) * (dark ? 0.16 : 0.11);
                    ctx.strokeStyle = 'rgba(59,130,246,' + alpha.toFixed(3) + ')';
                    ctx.lineWidth = 1;
                    ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(q.x, q.y); ctx.stroke();
                }
            }
        }
        for(var m = 0; m < nodes.length; m++){
            ctx.beginPath();
            ctx.arc(nodes[m].x, nodes[m].y, dark ? 1.9 : 1.6, 0, 6.2832);
            ctx.fillStyle = 'rgba(59,130,246,' + (dark ? 0.42 : 0.34) + ')';
            ctx.fill();
        }
        requestAnimationFrame(step);
    }
    window.addEventListener('resize', resize);
    window.addEventListener('mousemove', function(e){ mouse.x = e.clientX; mouse.y = e.clientY; });
    window.addEventListener('touchmove', function(e){ if(e.touches.length){ mouse.x = e.touches[0].clientX; mouse.y = e.touches[0].clientY; } }, {passive:true});
    window.addEventListener('mouseleave', function(){ mouse.x = -9999; mouse.y = -9999; });
    resize();
    requestAnimationFrame(step);
})();

// ===== SUBTLE PARTICLE NETWORK BACKGROUND =====
(function(){
    var cv = document.getElementById('bg-network');
    if(!cv || !window.matchMedia || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    var ctx = cv.getContext('2d');
    var W, H, nodes = [], mouse = {x:-9999, y:-9999};
    var N = Math.min(60, Math.max(28, Math.floor(window.innerWidth / 28)));
    function resize(){
        W = cv.width = window.innerWidth; H = cv.height = window.innerHeight;
        nodes = [];
        for(var i=0;i<N;i++){
            nodes.push({x:Math.random()*W, y:Math.random()*H, vx:(Math.random()-.5)*.22, vy:(Math.random()-.5)*.22});
        }
    }
    function colors(){
        var s=getComputedStyle(document.documentElement);
        return [s.getPropertyValue('--c-primary').trim()||'#2f6bff', s.getPropertyValue('--c-accent').trim()||'#0eb7a6'];
    }
    function frame(){
        ctx.clearRect(0,0,W,H);
        var c=colors();
        for(var i=0;i<nodes.length;i++){
            var n=nodes[i];
            n.x+=n.vx; n.y+=n.vy;
            if(n.x<0||n.x>W) n.vx*=-1;
            if(n.y<0||n.y>H) n.vy*=-1;
            var dx=mouse.x-n.x, dy=mouse.y-n.y, d=Math.hypot(dx,dy);
            if(d<140){ n.x-=dx/d*.6; n.y-=dy/d*.6; }
        }
        ctx.lineWidth=1;
        for(var a=0;a<nodes.length;a++){
            for(var b=a+1;b<nodes.length;b++){
                var dx=nodes[a].x-nodes[b].x, dy=nodes[a].y-nodes[b].y, d=dx*dx+dy*dy;
                var lim=130;
                if(d<lim*lim){
                    var alpha=(1-Math.sqrt(d)/lim)*.16;
                    ctx.strokeStyle='rgba(90,130,200,'+alpha.toFixed(3)+')';
                    ctx.beginPath();ctx.moveTo(nodes[a].x,nodes[a].y);ctx.lineTo(nodes[b].x,nodes[b].y);ctx.stroke();
                }
            }
        }
        for(var k=0;k<nodes.length;k++){
            var p=nodes[k];
            ctx.fillStyle='rgba(120,160,230,.5)';
            ctx.beginPath();ctx.arc(p.x,p.y,1.6,0,6.2832);ctx.fill();
        }
        requestAnimationFrame(frame);
    }
    window.addEventListener('resize', resize);
    window.addEventListener('mousemove', function(e){mouse.x=e.clientX;mouse.y=e.clientY;});
    window.addEventListener('mouseout', function(){mouse.x=-9999;mouse.y=-9999;});
    resize(); frame();
})();

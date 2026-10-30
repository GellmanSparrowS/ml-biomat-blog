// ml-biomat.com — enhanced code copy + search
(function(){
var isChinese = document.documentElement.lang !== 'en';
// === CODE COPY (always visible, icon-style) ===
document.addEventListener('DOMContentLoaded', function(){
    if(document.querySelector('.tutorial-reader')) return;
    document.querySelectorAll('pre').forEach(function(block){
        var wrapper = document.createElement('div');
        wrapper.style.position = 'relative';
        block.parentNode.insertBefore(wrapper, block);
        wrapper.appendChild(block);

        var btn = document.createElement('button');
        btn.className = 'copy-btn';
        btn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>';
        btn.title = isChinese ? '复制代码' : 'Copy code';
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
var searchData = null, searchLoaded = false, searchPending = null;

function loadSearchData(cb){
    if(searchLoaded){ cb(); return; }
    if(!searchPending) searchPending=fetch('/search.json').then(function(r){if(!r.ok)throw Error('Search unavailable');return r.json();}).then(function(d){searchData=d;searchLoaded=true;}).finally(function(){searchPending=null;});
    searchPending.then(cb).catch(function(){});
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
                return '<a class="post-card" href="'+(p.url||('/posts/'+p.slug+'/'))+'" style="text-decoration:none;display:block"><span class="card-lang '+p.lang+'">'+(p.lang==='en'?'EN':'\u4e2d\u6587')+'</span><h3>'+p.title+'</h3><p class="card-desc">'+(p.description||'')+'</p><div class="card-tags">'+tags+'</div></a>';
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
    q = q.toLowerCase();
    var results = searchData.filter(function(p){
        return p.title.toLowerCase().indexOf(q) >= 0 ||
               (p.description||'').toLowerCase().indexOf(q) >= 0 ||
               (p.tags||[]).some(function(t){ return t.toLowerCase().indexOf(q) >= 0; });
    });
    results.sort(function(a,b){var lang=isChinese?'zh':'en';return Number(b.lang===lang)-Number(a.lang===lang);});
    showDropdown(results.slice(0, 8), q);
}

function showDropdown(results, q){
    var dd = document.getElementById('search-dropdown');
    if(!dd){
        dd = document.createElement('div'); dd.id = 'search-dropdown'; dd.className = 'search-dropdown';
        document.body.appendChild(dd);
    }
    if(results.length === 0){
        dd.innerHTML = '<div class="search-item" style="color:var(--c-muted)">'+(isChinese?'未找到匹配内容':'No results')+'</div>';
    } else {
        dd.innerHTML = results.map(function(p){
            return '<a class="search-item" href="'+(p.url||('/posts/'+p.slug+'/'))+'"><strong>'+p.title+'</strong><span style="font-size:.75rem;color:var(--c-muted);display:block">'+(p.description||'')+'</span></a>';
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
            window.scrollTo({top:0,behavior:window.siteMotion&&window.siteMotion.matches?'auto':'smooth'});
        });
    }
});

document.addEventListener('DOMContentLoaded',function(){
    var bar=document.getElementById('progress-bar'),btn=document.getElementById('back-to-top'),queued=false;
    function update(){
        queued=false;
        var height=document.documentElement.scrollHeight-document.documentElement.clientHeight,y=window.scrollY;
        if(bar)bar.style.width=(height>0?Math.max(0,Math.min(100,y/height*100)):0)+'%';
        if(btn)btn.style.display=y>400?'block':'none';
    }
    window.addEventListener('scroll',function(){if(!queued){queued=true;requestAnimationFrame(update);}},{passive:true});update();
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
        a.title = document.documentElement.lang === 'en' ? 'Link to this section' : '复制本节链接';
        a.onclick = function(e){
            e.preventDefault();
            history.pushState(null,null,'#'+h.id);
            h.scrollIntoView({behavior:window.siteMotion&&window.siteMotion.matches?'auto':'smooth'});
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

// ===== SHARED THEME STATE =====
(function(){
    var KEY = 'ml-biomat-theme';
    var english=document.documentElement.lang==='en';
    function currentTheme(){return document.documentElement.dataset.theme||'dark';}
    function commentsTheme(){
        var frame=document.querySelector('iframe.giscus-frame');
        if(frame && frame.contentWindow) frame.contentWindow.postMessage({giscus:{setConfig:{theme:currentTheme()}}},'https://giscus.app');
        document.querySelectorAll('script[src*="giscus.app/client.js"]').forEach(function(node){node.dataset.theme=currentTheme();});
    }
    function render(){
        var btn=document.getElementById('theme-toggle');
        if(btn){
            var dark=currentTheme()==='dark';
            var label=english?(dark?'Switch to light mode':'Switch to dark mode'):(dark?'切换到亮色':'切换到暗色');
            btn.textContent=dark?'☀':'☾';btn.title=label;btn.setAttribute('aria-label',label);
        }
        commentsTheme();
    }
    document.addEventListener('DOMContentLoaded',function(){
        var selected='dark';
        try{var saved=localStorage.getItem(KEY);if(saved==='light'||saved==='dark')selected=saved;}catch(e){}
        document.documentElement.dataset.theme=selected;render();
        var btn=document.getElementById('theme-toggle');
        if(btn) btn.addEventListener('click',function(){
            var next=currentTheme()==='dark'?'light':'dark';document.documentElement.dataset.theme=next;
            try{localStorage.setItem(KEY,next);}catch(e){}render();
        });
        var observer=new MutationObserver(function(){
            var frame=document.querySelector('iframe.giscus-frame');
            if(frame){frame.addEventListener('load',commentsTheme);commentsTheme();observer.disconnect();}
        });
        observer.observe(document.body,{childList:true,subtree:true});
        if(!document.querySelector('script[src*="giscus.app/client.js"]'))observer.disconnect();
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
            var h = document.getElementById(decodeURIComponent(a.getAttribute('href').slice(1)));
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

// ===== CONTINUOUS FIBER NETWORK BACKGROUND =====
// Decorative shared-node geometry: an illustration of connected fibers, not a solver output.
(function(){
    'use strict';
    function initFiberBackground(){
        var canvas = document.getElementById('bg-canvas');
        var legacy = document.getElementById('bg-network');
        if(legacy){ legacy.hidden = true; legacy.style.display = 'none'; }
        if(!canvas || canvas.dataset.ambient === 'fiber-network') return;
        var ctx = canvas.getContext('2d', {alpha:true});
        if(!ctx) return;
        canvas.dataset.ambient = 'fiber-network';
        canvas.setAttribute('aria-hidden', 'true');
        canvas.style.opacity = '1';
        canvas.style.pointerEvents = 'none';
        canvas.style.position = 'fixed';
        canvas.style.inset = '0';
        canvas.style.zIndex = '0';
        canvas.style.contain = 'strict';

        var motionQuery = window.siteMotion || window.matchMedia('(prefers-reduced-motion: reduce)');
        var darkQuery = window.matchMedia('(prefers-color-scheme: dark)');
        var coarseQuery = window.matchMedia('(pointer: coarse)');
        var fineQuery = window.matchMedia('(hover: hover) and (pointer: fine)');
        var printQuery = window.matchMedia('print');
        var connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
        var main = document.querySelector('main');
        var width = 0, height = 0, dpr = 1, columns = 0, rows = 0;
        var nodes = [], rowFibers = [], columnFibers = [], diagonalFibers = [];
        var mask = null, palette = null, mobile = false, lowPower = false;
        var animation = 0, resizeFrame = 0, elapsed = 0, previousTime = 0, lastPaint = 0, paintedFrames = 0;
        var slowFrames = 0, performanceLimited = false, pendingResize = false;
        var frameInterval = 1000 / 28;
        var pointer = {x:0, y:0, targetX:0, targetY:0, amount:0, targetAmount:0, updated:0, positioned:false};

        function listen(query, callback){
            if(query.addEventListener) query.addEventListener('change', callback);
            else query.addListener(callback);
        }
        function noise(seed){
            var value = Math.sin(seed * 127.1 + 311.7) * 43758.5453;
            return value - Math.floor(value);
        }
        function isDark(){
            var selected = document.documentElement.getAttribute('data-theme');
            return selected === 'dark' || (selected !== 'light' && darkQuery.matches);
        }
        function readPalette(){
            palette = isDark()
                ? {fiber:'113,153,194', accent:'93,179,173', line:.43, highlight:.58, joint:.64}
                : {fiber:'71,103,143', accent:'40,125,128', line:.37, highlight:.49, joint:.53};
        }
        function staticMode(){
            return motionQuery.matches;
        }
        function updateFrameInterval(){
            // Small screens and slower devices retain motion at a lower drawing rate.
            frameInterval = 1000 / (performanceLimited ? 10 : lowPower ? 12 : mobile ? 18 : 28);
        }
        function pixelRatio(){
            return Math.min(window.devicePixelRatio || 1, (mobile || lowPower) ? 1.5 : 2, Math.sqrt(8400000/Math.max(1,width*height)));
        }
        function stop(){
            if(animation){ cancelAnimationFrame(animation); animation = 0; }
            previousTime = 0;
        }
        function setMask(){
            var rect = main ? main.getBoundingClientRect() : {left:width*.15, right:width*.85};
            var left = Math.max(18, Math.min(width*.42, rect.left + 14));
            var right = Math.min(width - 18, Math.max(width*.58, rect.right - 14));
            var feather = mobile ? 30 : 80;
            mask = ctx.createLinearGradient(0, 0, width, 0);
            mask.addColorStop(0, 'rgba(0,0,0,.96)');
            mask.addColorStop(Math.max(0, left - feather)/width, 'rgba(0,0,0,.9)');
            mask.addColorStop(left/width, 'rgba(0,0,0,.055)');
            mask.addColorStop(right/width, 'rgba(0,0,0,.055)');
            mask.addColorStop(Math.min(width, right + feather)/width, 'rgba(0,0,0,.9)');
            mask.addColorStop(1, 'rgba(0,0,0,.96)');
        }
        function createGeometry(){
            nodes = []; rowFibers = []; columnFibers = []; diagonalFibers = [];
            columns = mobile ? 6 : Math.max(8, Math.min(16, Math.ceil(width / 125) + 1));
            rows = mobile ? 7 : Math.max(7, Math.min(12, Math.ceil(height / 115) + 1));
            var stepX = (width + 150) / (columns - 1);
            var stepY = (height + 140) / (rows - 1);
            for(var row = 0; row < rows; row++){
                var rowPath = [];
                for(var col = 0; col < columns; col++){
                    var seed = row * 31 + col * 7;
                    var node = {
                        baseX:col * stepX - 75 + (noise(seed)-.5)*stepX*.5,
                        baseY:row * stepY - 70 + (noise(seed+21)-.5)*stepY*.5,
                        u:col/(columns-1), v:row/(rows-1), phase:noise(seed+7)*Math.PI*2,
                        x:0, y:0
                    };
                    nodes.push(node); rowPath.push(node);
                }
                rowFibers.push(rowPath);
            }
            for(var c = 0; c < columns; c++){
                var columnPath = [];
                for(var r = 0; r < rows; r++) columnPath.push(nodes[r * columns + c]);
                columnFibers.push(columnPath);
            }
            // A few continuous diagonal fibers connect the same junctions at a larger scale.
            if(!mobile){
                for(var start = -rows + 2; start < columns - 1; start += 3){
                    var diagonal = [];
                    for(var rr = 0; rr < rows; rr++){
                        var cc = start + rr;
                        if(cc >= 0 && cc < columns) diagonal.push(nodes[rr*columns+cc]);
                    }
                    if(diagonal.length > 2) diagonalFibers.push(diagonal);
                }
            }
        }
        function clearPointer(){ pointer.targetAmount = 0; }
        function updatePointer(time){
            if(!fineQuery.matches || staticMode()){
                pointer.amount = 0; pointer.targetAmount = 0; pointer.positioned = false;
                pointer.updated = time;
                return;
            }
            var delta = Math.max(0, Math.min(.1, time-pointer.updated));
            pointer.updated = time;
            var positionBlend = 1-Math.exp(-delta*12);
            var strengthBlend = 1-Math.exp(-delta*5);
            pointer.x += (pointer.targetX-pointer.x)*positionBlend;
            pointer.y += (pointer.targetY-pointer.y)*positionBlend;
            pointer.amount += (pointer.targetAmount-pointer.amount)*strengthBlend;
            if(pointer.targetAmount === 0 && pointer.amount < .0001) pointer.amount = 0;
        }
        function trackPointer(event){
            if(!fineQuery.matches || staticMode() || document.hidden ||
                (event.pointerType && event.pointerType !== 'mouse' && event.pointerType !== 'pen')) return;
            if(!Number.isFinite(event.clientX) || !Number.isFinite(event.clientY)) return;
            if(!pointer.positioned){
                pointer.x = event.clientX; pointer.y = event.clientY; pointer.positioned = true;
            }
            pointer.targetX = event.clientX; pointer.targetY = event.clientY;
            pointer.targetAmount = 1;
        }
        function updateGeometry(time){
            updatePointer(time);
            var amplitude = mobile ? 9 : 15;
            for(var i = 0; i < nodes.length; i++){
                var node = nodes[i];
                node.x = node.baseX + Math.sin(time*.19 + node.v*5.1 + node.u*2)*amplitude
                    + Math.sin(time*.12 + node.phase)*4;
                node.y = node.baseY + Math.cos(time*.16 + node.u*4.3 - node.v*1.7)*amplitude
                    + Math.cos(time*.11 + node.phase)*4;
                // Shared junctions bend gently near a fine pointer; the 20px core avoids a singular force.
                if(pointer.amount > 0){
                    var dx = node.x-pointer.x, dy = node.y-pointer.y;
                    var distance = Math.sqrt(dx*dx+dy*dy);
                    if(distance < 180){
                        var falloff = 1-distance/180;
                        var scale = 6.5*falloff*falloff*pointer.amount/Math.max(distance,20);
                        node.x += dx*scale; node.y += dy*scale;
                    }
                }
            }
        }
        function trace(fiber){
            ctx.beginPath(); ctx.moveTo(fiber[0].x, fiber[0].y);
            // Interpolating cubic curves meet at the shared junctions, preserving connectivity.
            for(var i = 0; i < fiber.length-1; i++){
                var before = fiber[Math.max(0, i-1)];
                var a = fiber[i], b = fiber[i+1];
                var after = fiber[Math.min(fiber.length-1, i+2)];
                ctx.bezierCurveTo(a.x+(b.x-before.x)/6, a.y+(b.y-before.y)/6,
                    b.x-(after.x-a.x)/6, b.y-(after.y-a.y)/6, b.x, b.y);
            }
        }
        function drawFibers(fibers, color, alpha, lineWidth){
            ctx.strokeStyle = 'rgba('+color+','+alpha+')';
            ctx.lineWidth = lineWidth;
            for(var i = 0; i < fibers.length; i++){ trace(fibers[i]); ctx.stroke(); }
        }
        function paint(){
            ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
            ctx.clearRect(0, 0, width, height);
            ctx.lineCap = 'round'; ctx.lineJoin = 'round';
            updateGeometry(elapsed);
            var strength = mobile ? .68 : 1;
            drawFibers(rowFibers, palette.fiber, palette.line*.78*strength, .9);
            drawFibers(columnFibers, palette.fiber, palette.line*strength, 1.05);
            drawFibers(diagonalFibers, palette.accent, palette.line*.56, .8);
            // A pair of accent fibers gives the field a clear continuous visual route.
            var accents = [columnFibers[1], columnFibers[columns-2]];
            drawFibers(accents, palette.accent, palette.highlight*strength, 1.35);
            ctx.fillStyle = 'rgba('+palette.fiber+','+(palette.joint*strength)+')';
            for(var j = 0; j < nodes.length; j++){
                var point = nodes[j];
                ctx.beginPath(); ctx.arc(point.x, point.y, mobile ? 1.15 : 1.45, 0, Math.PI*2); ctx.fill();
            }
            // Protect the reading column while retaining visible fibers along both page edges.
            ctx.globalCompositeOperation = 'destination-in';
            ctx.fillStyle = mask; ctx.fillRect(0, 0, width, height);
            ctx.globalCompositeOperation = 'source-over';
            paintedFrames++;
        }
        function frame(timestamp){
            animation = 0;
            if(document.hidden || printQuery.matches){ stop(); canvas.dataset.motion = 'paused'; return; }
            if(staticMode()){ previousTime = 0; canvas.dataset.motion = 'static'; return; }
            if(pixelRatio() !== dpr){ resize(); return; }
            if(!previousTime) previousTime = timestamp;
            elapsed += Math.min((timestamp - previousTime)/1000, .08);
            previousTime = timestamp;
            if(timestamp-lastPaint >= frameInterval){
                var started = performance.now();
                paint(); lastPaint = timestamp;
                slowFrames = performance.now()-started > 12 ? slowFrames+1 : Math.max(0,slowFrames-1);
                if(slowFrames >= 18){
                    performanceLimited = true;
                    updateFrameInterval();
                    slowFrames = 0;
                }
            }
            animation = requestAnimationFrame(frame);
        }
        function synchronize(){
            stop();
            if(document.hidden || printQuery.matches){ canvas.dataset.motion = 'paused'; return; }
            if(pendingResize){ resize(); return; }
            readPalette(); paint();
            if(staticMode()){ canvas.dataset.motion = 'static'; return; }
            canvas.dataset.motion = 'animated';
            lastPaint = 0;
            animation = requestAnimationFrame(frame);
        }
        function resize(){
            pendingResize = false; stop();
            var oldWidth=width,oldHeight=height,oldMobile=mobile;
            width = Math.max(1, window.innerWidth); height = Math.max(1, window.innerHeight);
            mobile = width <= 640 || coarseQuery.matches;
            lowPower = !!((connection && connection.saveData) ||
                (navigator.hardwareConcurrency && navigator.hardwareConcurrency <= 2) ||
                (navigator.deviceMemory && navigator.deviceMemory < 4));
            updateFrameInterval();
            dpr = pixelRatio();
            var backingWidth=Math.round(width*dpr),backingHeight=Math.round(height*dpr);
            if(canvas.width!==backingWidth||canvas.height!==backingHeight){canvas.width=backingWidth;canvas.height=backingHeight;}
            if(oldWidth!==width||oldHeight!==height){canvas.style.width=width+'px';canvas.style.height=height+'px';}
            ctx.setTransform(canvas.width/width,0,0,canvas.height/height,0,0);
            if(oldWidth!==width||oldHeight!==height||oldMobile!==mobile||!nodes.length)createGeometry();
            setMask();synchronize();
        }
        function scheduleResize(){
            pendingResize = true;
            if(document.hidden || resizeFrame) return;
            resizeFrame = requestAnimationFrame(function(){ resizeFrame = 0; resize(); });
        }
        window.addEventListener('pointermove', trackPointer, {passive:true});
        window.addEventListener('pointerout', function(event){ if(!event.relatedTarget) clearPointer(); }, {passive:true});
        window.addEventListener('blur', clearPointer, {passive:true});
        document.documentElement.addEventListener('pointerleave', clearPointer, {passive:true});
        document.addEventListener('visibilitychange', function(){
            if(document.hidden) clearPointer();
            if(document.hidden && resizeFrame){ cancelAnimationFrame(resizeFrame); resizeFrame = 0; }
            synchronize();
        });
        window.addEventListener('pagehide', function(){
            clearPointer(); stop();
            if(resizeFrame){ cancelAnimationFrame(resizeFrame); resizeFrame = 0; }
            canvas.dataset.motion = 'paused';
        });
        window.addEventListener('pageshow', scheduleResize);
        window.addEventListener('focus', function(){ if(!document.hidden) synchronize(); });
        window.addEventListener('resize', scheduleResize, {passive:true});
        listen(motionQuery, synchronize); listen(darkQuery, synchronize);
        listen(coarseQuery, scheduleResize); listen(printQuery, synchronize);
        listen(fineQuery, function(){ clearPointer(); synchronize(); });
        if(connection && connection.addEventListener) connection.addEventListener('change', scheduleResize);
        new MutationObserver(synchronize).observe(document.documentElement, {attributes:true, attributeFilter:['data-theme']});
        if(main && window.ResizeObserver) new ResizeObserver(scheduleResize).observe(main);
        // Read-only animation state for release checks; no extra visible controls.
        canvas.fiberBackground = {snapshot:function(){
            return {elapsed:elapsed, frames:paintedFrames, running:!!animation,
                reduced:motionQuery.matches, mobile:mobile, lowPower:lowPower,
                performanceLimited:performanceLimited, fps:1000/frameInterval,
                width:width, height:height, pixelRatio:dpr, backingWidth:canvas.width, backingHeight:canvas.height, nodes:nodes.length};
        }};
        resize();
    }
    if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initFiberBackground);
    else initFiberBackground();
})();

// Keep the first mobile screen focused on the article; contents remain one tap away.
document.addEventListener('DOMContentLoaded', function(){
    var mobileContents = window.matchMedia('(max-width:760px)');
    if(mobileContents.matches){
        document.querySelectorAll('details.toc, details.lesson-toc').forEach(function(toc){toc.open=false;});
    }
    function revealDesktopContents(event){
        if(!event.matches) document.querySelectorAll('details.lesson-toc').forEach(function(toc){toc.open=true;});
    }
    if(mobileContents.addEventListener) mobileContents.addEventListener('change', revealDesktopContents);
    else if(mobileContents.addListener) mobileContents.addListener(revealDesktopContents);
});


// Local, keyboard-accessible figure viewer: fit, original size, and scrollable zoom.
document.addEventListener('DOMContentLoaded', function(){
    var figures = Array.from(document.querySelectorAll('.content img, .tutorial-reader img, .fibernet-page img, img[data-full-src]')).filter(function(image){
        if(image.closest('[data-pr-image], [hidden], .pr-viewer, dialog'))return false;
        var link=image.closest('a[href]');
        return !link||/\.(?:png|jpe?g|webp|avif|svg)(?:[?#]|$)/i.test(link.href);
    });
    if(!figures.length) return;
    var chinese = /^zh/i.test(document.documentElement.lang);
    var text = chinese ? {
        view:'查看图解', close:'关闭', fit:'适应窗口', original:'原始大小',
        out:'缩小', inside:'放大', source:'打开原图', region:'图解，可滚动查看',
        loading:'正在载入图解…', error:'图解载入失败，请打开原图查看。', title:'图解'
    } : {
        view:'View figure', close:'Close', fit:'Fit', original:'Original size',
        out:'Zoom out', inside:'Zoom in', source:'Open original', region:'Figure; scroll to explore',
        loading:'Loading figure…', error:'The figure could not be loaded. Open the original to view it.', title:'Figure'
    };
    var dialog, stage, canvas, picture, heading, message, percentage, sourceLink;
    var fitButton, originalButton, plusButton, minusButton, closeButton;
    var trigger = null, zoom = 1, fitMode = true, naturalWidth = 1, naturalHeight = 1;
    var loaded = false, bodyOverflow = '', loadVersion = 0, fullRequest = null;

    function element(tag, className, value){
        var node = document.createElement(tag);
        if(className) node.className = className;
        if(value !== undefined) node.textContent = value;
        return node;
    }
    function button(label, className, callback){
        var node = element('button', className, label);
        node.type = 'button'; node.addEventListener('click', callback);
        return node;
    }
    function fitScale(){
        return Math.min(1, Math.max(1, stage.clientWidth - 28)/naturalWidth,
            Math.max(1, stage.clientHeight - 28)/naturalHeight);
    }
    function draw(scale, preserveCenter){
        if(!loaded) return;
        var x = .5, y = .5;
        if(preserveCenter && picture.offsetWidth){
            x = (stage.scrollLeft + stage.clientWidth/2 - picture.offsetLeft)/picture.offsetWidth;
            y = (stage.scrollTop + stage.clientHeight/2 - picture.offsetTop)/picture.offsetHeight;
            x = Math.max(0, Math.min(1, x)); y = Math.max(0, Math.min(1, y));
        }
        zoom = Math.max(.05, Math.min(4, scale));
        picture.style.width = (naturalWidth*zoom)+'px';
        picture.style.height = (naturalHeight*zoom)+'px';
        percentage.textContent = Math.round(zoom*100)+'%';
        fitButton.setAttribute('aria-pressed', String(fitMode));
        originalButton.setAttribute('aria-pressed', String(!fitMode && Math.abs(zoom-1)<.001));
        minusButton.disabled = zoom <= .0501;
        plusButton.disabled = zoom >= 3.999;
        stage.scrollLeft = picture.offsetLeft + x*picture.offsetWidth - stage.clientWidth/2;
        stage.scrollTop = picture.offsetTop + y*picture.offsetHeight - stage.clientHeight/2;
    }
    function fit(){fitMode=true;draw(fitScale(),false);}
    function original(){fitMode=false;draw(1,true);}
    function changeZoom(factor){fitMode=false;draw(zoom*factor,true);}
    function controlsEnabled(enabled){
        [fitButton,originalButton,plusButton,minusButton].forEach(function(node){node.disabled=!enabled;});
    }
    function close(){if(dialog.open) dialog.close();}
    function createViewer(){
        dialog = element('dialog','figure-viewer'); dialog.id='article-figure-viewer';
        dialog.setAttribute('aria-labelledby','figure-viewer-title');
        var header = element('header','figure-viewer-header');
        heading = element('h2','',text.title); heading.id='figure-viewer-title';
        closeButton=button(text.close,'figure-viewer-close',close);
        header.append(heading,closeButton);
        var toolbar=element('div','figure-viewer-toolbar');
        toolbar.setAttribute('role','group');toolbar.setAttribute('aria-label',text.view);
        fitButton=button(text.fit,'',fit);
        originalButton=button(text.original,'',original);
        minusButton=button('−','figure-viewer-step',function(){changeZoom(1/1.25);});
        plusButton=button('+','figure-viewer-step',function(){changeZoom(1.25);});
        minusButton.setAttribute('aria-label',text.out);minusButton.title=text.out;
        plusButton.setAttribute('aria-label',text.inside);plusButton.title=text.inside;
        percentage=element('output','figure-viewer-percent','');
        percentage.setAttribute('aria-live','polite');percentage.setAttribute('aria-atomic','true');
        sourceLink=element('a','figure-viewer-source',text.source);
        sourceLink.target='_blank';sourceLink.rel='noopener';
        toolbar.append(fitButton,originalButton,minusButton,percentage,plusButton,sourceLink);
        stage=element('div','figure-viewer-stage');stage.tabIndex=0;
        stage.setAttribute('role','region');stage.setAttribute('aria-label',text.region);
        canvas=element('div','figure-viewer-canvas');
        picture=element('img','figure-viewer-image');picture.draggable=false;
        message=element('p','figure-viewer-message',text.loading);message.setAttribute('role','status');
        canvas.append(picture,message);stage.append(canvas);
        dialog.append(header,toolbar,stage);document.body.append(dialog);
        dialog.addEventListener('close',function(){
            loadVersion++;loaded=false;
            if(fullRequest){fullRequest.onload=null;fullRequest.onerror=null;fullRequest.removeAttribute('src');fullRequest=null;}
            picture.onload=null;picture.onerror=null;picture.removeAttribute('src');picture.hidden=true;
            document.body.style.overflow=bodyOverflow;
            if(trigger && trigger.isConnected) trigger.focus({preventScroll:true});
        });
        dialog.addEventListener('click',function(event){
            if(event.target!==dialog) return;
            var r=dialog.getBoundingClientRect();
            if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom) close();
        });
        dialog.addEventListener('keydown',function(event){
            if(!loaded) return;
            if(event.key==='+'||event.key==='='){event.preventDefault();changeZoom(1.25);}
            else if(event.key==='-'){event.preventDefault();changeZoom(1/1.25);}
            else if(event.key==='0'){event.preventDefault();fit();}
            else if(event.key==='1'){event.preventDefault();original();}
        });
        window.addEventListener('resize',function(){if(dialog.open&&loaded) draw(fitMode?fitScale():zoom,true);},{passive:true});
    }
    function openFigure(image){
        if(!dialog) createViewer();
        var preview=image.currentSrc||image.src,url=image.dataset.fullSrc||preview;
        if(typeof dialog.showModal!=='function'){window.open(url,'_blank','noopener');return;}
        trigger=image;heading.textContent=image.alt||text.title;picture.alt=image.alt||text.title;
        sourceLink.href=url;loaded=false;fitMode=true;percentage.textContent='';
        controlsEnabled(false);picture.hidden=true;message.hidden=false;message.textContent=text.loading;
        stage.setAttribute('aria-busy','true');
        bodyOverflow=document.body.style.overflow;document.body.style.overflow='hidden';
        dialog.showModal();closeButton.focus({preventScroll:true});
        var version=++loadVersion;
        function reveal(width,height,src,complete){
            if(version!==loadVersion||!dialog.open||!width||!height)return;
            var oldWidth=naturalWidth,wasLoaded=loaded;
            naturalWidth=width;naturalHeight=height;loaded=true;
            if(src){picture.onload=null;picture.src=src;}
            picture.hidden=false;message.hidden=true;controlsEnabled(true);
            if(complete)stage.removeAttribute('aria-busy');
            if(fitMode)fit();else draw(wasLoaded?zoom*oldWidth/width:fitScale(),true);
        }
        picture.onload=function(){reveal(picture.naturalWidth,picture.naturalHeight,null,preview===url);};
        picture.onerror=function(){if(version===loadVersion&&!loaded){message.textContent=text.error;message.hidden=false;stage.removeAttribute('aria-busy');}};
        picture.decoding='async';picture.src=preview;
        if(image.complete&&image.naturalWidth)reveal(image.naturalWidth,image.naturalHeight,null,preview===url);
        if(preview!==url){
            var high=new Image();fullRequest=high;high.decoding='async';
            high.onload=function(){
                var decoded=high.decode?high.decode().catch(function(){}):Promise.resolve();
                decoded.then(function(){reveal(high.naturalWidth,high.naturalHeight,url,true);if(fullRequest===high)fullRequest=null;});
            };
            high.onerror=function(){if(version!==loadVersion||!dialog.open)return;stage.removeAttribute('aria-busy');if(!loaded){message.hidden=false;message.textContent=text.error;}if(fullRequest===high)fullRequest=null;};
            high.src=url;
        }
    }
    figures.forEach(function(image){
        image.tabIndex=0;image.setAttribute('role','button');image.setAttribute('aria-haspopup','dialog');
        image.setAttribute('aria-label',(image.alt?image.alt+' — ':'')+text.view);
        image.classList.add('article-figure-trigger');
        image.addEventListener('click',function(event){event.preventDefault();openFigure(image);});
        image.addEventListener('keydown',function(event){
            if(event.key==='Enter'||event.key===' '){event.preventDefault();openFigure(image);}
        });
    });
});

// Lesson scripts already toggle the size; keep the button wording in sync.
document.addEventListener('DOMContentLoaded',function(){
    var toggle=document.getElementById('font-toggle');
    var reader=document.querySelector('.tutorial-reader');
    if(!toggle||!reader) return;
    function label(){toggle.textContent=reader.classList.contains('large')?'恢复字号':'放大正文';}
    toggle.addEventListener('click',function(){queueMicrotask(label);});
    label();
});

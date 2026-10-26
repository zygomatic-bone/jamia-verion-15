/* Motion layer: scroll reveals, counters, dropdown/drawer polish, photograph lightbox, link prefetch, slow-device check.
   Shared by the root pages (portal-assets/motion.js) and the Residential School pages (assets/js/motion.js).
   Written in the style of the original site: ES5, "function(){", 4 spaces, single quotes, semicolons.
   Rules: one IntersectionObserver for all reveals, no scroll or touchmove listeners, nothing runs while the tab is hidden,
   and a failure anywhere leaves the page fully visible (hidden "before" states exist only after this script has started). */
(function(){
    'use strict';
    var root = document.documentElement;
    var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
    var hasIO = 'IntersectionObserver' in window;
    var conn = navigator.connection || {};
    var saveData = !!conn.saveData;
    var fineHover = window.matchMedia && matchMedia('(hover: hover) and (pointer: fine)').matches;

    /* ---- iOS only shows :active (pressed state) when some touchstart listener exists ---- */
    document.addEventListener('touchstart', function(){}, {passive: true});

    /* ---- stop endless CSS animations while the tab is hidden ---- */
    document.addEventListener('visibilitychange', function(){
        root.classList.toggle('mo-away', document.hidden);
    });

    /* ---- slow-device check: after the page has loaded, time 30 frames; a slow median switches the decorative extras off (html.mo-lite) ---- */
    function probe(){
        var lite = false;
        try{
            lite = sessionStorage.getItem('jame-lite') === '1';
        }catch(e){}
        if(lite){
            root.classList.add('mo-lite');
            return;
        }
        if(reduce || !window.requestAnimationFrame){
            return;
        }
        var weak = (navigator.deviceMemory && navigator.deviceMemory <= 2) || (navigator.hardwareConcurrency && navigator.hardwareConcurrency <= 2);
        var last = 0;
        var gaps = [];
        function frame(t){
            if(document.hidden){
                last = 0;
                gaps = [];
                return requestAnimationFrame(frame);
            }
            if(last){
                gaps.push(t - last);
            }
            last = t;
            if(gaps.length < 30){
                return requestAnimationFrame(frame);
            }
            gaps.sort(function(a, b){ return a - b; });
            var median = gaps[15];
            if(median > 30 || (weak && median > 22)){
                root.classList.add('mo-lite');
                try{
                    sessionStorage.setItem('jame-lite', '1');
                }catch(e){}
            }
        }
        setTimeout(function(){ requestAnimationFrame(frame); }, 700);
    }
    if(document.readyState === 'complete'){
        probe();
    }else{
        window.addEventListener('load', probe, {once: true});
    }

    /* ---- headings: a short gold line under section headings (drawn in when the heading appears) ---- */
    var headings = [].slice.call(document.querySelectorAll('.portal-content h2, .mp-head h2'));
    headings.forEach(function(h){
        if(!h.closest('.rc-letter, .pf-card, .pf-tile, .reveal, .stagger')){
            h.classList.add('mo-heading');
        }
    });

    /* ---- scroll reveals ---- */
    var pending = [];
    var observer = null;
    function clean(el){
        el.classList.remove('mo-pre', 'mo-left', 'mo-right', 'mo-scale', 'mo-group');
        if(!el.classList.contains('mo-heading')){
            el.classList.remove('mo-in');
        }
        el.style.removeProperty('--mo-d');
    }
    function show(el, step){
        if(step){
            el.style.setProperty('--mo-d', (Math.min(step, 4) * 0.07).toFixed(2) + 's');
        }
        el.classList.add('mo-in');
        var i = pending.indexOf(el);
        if(i > -1){
            pending.splice(i, 1);
        }
        setTimeout(function(){ clean(el); }, 1500 + (step ? 300 : 0));
    }
    function setupReveals(){
        var skip = '.reveal, .stagger, .pf-reveal, .pf-stagger, .rg-item, [data-no-motion], .page-hero, .hero, .mo-lb';
        var groupSel = '.rc-gallery, .rc-people, .rc-docs, .rc-letters, .rc-vision, .rc-twocol, .mp-lead, .mp-gallery, .mp-videos, .footer-grid, .cx-grid, .cx-accs';
        var singleSel = '.portal-content p, .portal-content blockquote, .rc-table-wrap, .rc-quote-plain, .rc-single, .rc-logo, .mp-head, .rc-info, .cx-head, .cx-find, .cx-status, .cx-aside, .cx-side';
        var splitSel = '.rc-split > :first-child, .rc-split > :last-child';
        var h = window.innerHeight || 800;
        var plan = [];
        var groups = [].filter.call(document.querySelectorAll(groupSel), function(el){
            return el.children.length > 1 && !el.closest(skip);
        });
        function inGroup(el){
            return groups.some(function(g){ return g.contains(el); });
        }
        /* first read every position (one layout pass), then write the classes */
        groups.forEach(function(el){
            plan.push({el: el, kind: 'group', top: el.getBoundingClientRect().top});
        });
        [].forEach.call(document.querySelectorAll(singleSel), function(el){
            if(!el.closest(skip) && !inGroup(el)){
                plan.push({el: el, kind: 'up', top: el.getBoundingClientRect().top});
            }
        });
        [].forEach.call(document.querySelectorAll(splitSel), function(el){
            var parent = el.parentNode;
            if(parent.children.length === 2 && !el.closest(skip) && !inGroup(el)){
                plan.push({el: el, kind: el === parent.firstElementChild ? 'left' : 'right', top: el.getBoundingClientRect().top});
            }
        });
        [].forEach.call(document.querySelectorAll('.mo-heading'), function(el){
            plan.push({el: el, kind: 'heading', top: el.getBoundingClientRect().top});
        });
        root.classList.add('mo-on');
        observer = new IntersectionObserver(function(entries){
            var step = 0;
            entries.forEach(function(entry){
                if(entry.isIntersecting){
                    observer.unobserve(entry.target);
                    show(entry.target, step++);
                }
            });
        }, {threshold: 0, rootMargin: '0px 0px -6% 0px'});
        var seen = [];
        plan.forEach(function(p){
            var el = p.el;
            if(seen.indexOf(el) > -1){
                return;
            }
            seen.push(el);
            if(p.kind === 'heading'){
                if(p.top < h){
                    setTimeout(function(){ el.classList.add('mo-in'); }, 350);
                    return;
                }
            }else{
                if(p.top < h * 0.95){
                    return;
                }
                if(p.kind === 'group'){
                    el.classList.add('mo-group');
                }else{
                    el.classList.add('mo-pre');
                    if(p.kind === 'left' || p.kind === 'right'){
                        el.classList.add('mo-' + p.kind);
                    }else if(el.matches('.rc-single, .rc-logo, .rc-table-wrap')){
                        el.classList.add('mo-scale');
                    }
                }
            }
            observer.observe(el);
            pending.push(el);
        });
        /* safety nets: whatever is on screen shows after 2.5 s; whatever is still waiting shows after 9 s, so nothing can stay hidden */
        setTimeout(function(){
            pending.slice().forEach(function(el){
                var r = el.getBoundingClientRect();
                if(r.top < h && r.bottom > 0){
                    observer.unobserve(el);
                    show(el, 0);
                }
            });
        }, 2500);
        setTimeout(function(){
            pending.slice().forEach(function(el){
                observer.unobserve(el);
                show(el, 0);
            });
        }, 9000);
    }
    if(!reduce && hasIO){
        try{
            setupReveals();
        }catch(e){
            root.classList.remove('mo-on');
            [].forEach.call(document.querySelectorAll('.mo-pre, .mo-group'), clean);
        }
    }else{
        [].forEach.call(document.querySelectorAll('.mo-heading'), function(el){ el.classList.add('mo-in'); });
    }
    window.addEventListener('pagehide', function(){
        if(observer){
            observer.disconnect();
        }
    });

    /* ---- counters: only elements marked data-count (a real figure); the final value is already in the page ---- */
    var counters = [].slice.call(document.querySelectorAll('[data-count]'));
    function format(n, decimals){
        return decimals ? n.toFixed(decimals) : Math.round(n).toLocaleString('en-IN');
    }
    function countUp(el){
        var end = parseFloat(el.getAttribute('data-count'));
        if(isNaN(end)){
            return;
        }
        var final = el.textContent;
        var decimals = (String(end).split('.')[1] || '').length;
        var start = null;
        function step(t){
            if(start === null){
                start = t;
            }
            var p = Math.min(1, (t - start) / 1000);
            var eased = 1 - Math.pow(1 - p, 3);
            el.textContent = format(end * eased, decimals);
            if(p < 1){
                requestAnimationFrame(step);
            }else{
                el.textContent = final;
            }
        }
        requestAnimationFrame(step);
        setTimeout(function(){ el.textContent = final; }, 2500);
    }
    if(counters.length && !reduce && hasIO){
        var cio = new IntersectionObserver(function(entries){
            entries.forEach(function(entry){
                if(entry.isIntersecting){
                    cio.unobserve(entry.target);
                    countUp(entry.target);
                }
            });
        }, {threshold: 0.6});
        counters.forEach(function(el){ cio.observe(el); });
    }

    /* ---- desktop dropdowns fade out as well as in ---- */
    document.addEventListener('click', function(e){
        var summary = e.target.closest && e.target.closest('.nav-group > summary');
        if(!summary || reduce){
            return;
        }
        var group = summary.parentNode;
        if(!group.open){
            return;
        }
        e.preventDefault();
        group.classList.add('is-closing');
        setTimeout(function(){
            group.open = false;
            group.classList.remove('is-closing');
        }, 160);
    }, true);

    /* ---- mobile drawer: a link to the same page (or an anchor) closes it ---- */
    var drawer = document.getElementById('mobile-drawer');
    if(drawer && drawer.close){
        drawer.addEventListener('click', function(e){
            var a = e.target.closest && e.target.closest('a[href]');
            if(a && a.origin === location.origin && a.pathname === location.pathname){
                drawer.close();
            }
        });
    }

    /* ---- photograph lightbox for pictures that are plain links to an image file ---- */
    var IMG = /\.(?:jpe?g|png|webp|gif)(?:[?#].*)?$/i;
    var lb = null;
    var lbImg = null;
    var lbCap = null;
    var lbCount = null;
    var items = [];
    var index = 0;
    var busy = false;
    function isPhotoLink(a){
        return a && a.getAttribute('href') && IMG.test(a.getAttribute('href')) && !a.hasAttribute('download') && !a.hasAttribute('data-lightbox') && a.querySelector('img') && a.origin === location.origin;
    }
    function build(){
        lb = document.createElement('dialog');
        lb.className = 'mo-lb';
        lb.setAttribute('aria-label', 'Photograph viewer');
        lb.innerHTML = '<div class="mo-lb-stage"><img class="mo-lb-img" alt=""></div><p class="mo-lb-cap" aria-live="polite"></p><span class="mo-lb-count" aria-hidden="true"></span>' +
            '<button class="mo-lb-btn mo-lb-close" type="button" aria-label="Close photograph">×</button>' +
            '<button class="mo-lb-btn mo-lb-prev" type="button" aria-label="Previous photograph">‹</button>' +
            '<button class="mo-lb-btn mo-lb-next" type="button" aria-label="Next photograph">›</button>';
        document.body.appendChild(lb);
        lbImg = lb.querySelector('.mo-lb-img');
        lbCap = lb.querySelector('.mo-lb-cap');
        lbCount = lb.querySelector('.mo-lb-count');
        var stage = lb.querySelector('.mo-lb-stage');
        lb.querySelector('.mo-lb-close').addEventListener('click', function(){ lb.close(); });
        lb.querySelector('.mo-lb-prev').addEventListener('click', function(){ go(-1); });
        lb.querySelector('.mo-lb-next').addEventListener('click', function(){ go(1); });
        var swiped = 0;
        stage.addEventListener('click', function(e){
            if(e.target === stage && Date.now() - swiped > 400){
                lb.close();
            }
        });
        lb.addEventListener('keydown', function(e){
            if(e.key === 'ArrowLeft'){
                go(-1);
            }else if(e.key === 'ArrowRight'){
                go(1);
            }
        });
        lb.addEventListener('wheel', function(e){ e.preventDefault(); }, {passive: false});
        lb.addEventListener('close', function(){
            setTimeout(function(){ lbImg.classList.remove('is-ready'); }, 300);
        });
        /* touch and pen: a quick horizontal swipe moves to the next or previous photograph */
        var x0 = 0, y0 = 0, down = false;
        stage.addEventListener('pointerdown', function(e){
            down = true;
            x0 = e.clientX;
            y0 = e.clientY;
        });
        stage.addEventListener('pointerup', function(e){
            if(!down){
                return;
            }
            down = false;
            var dx = e.clientX - x0;
            var dy = e.clientY - y0;
            if(Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.5){
                swiped = Date.now();
                go(dx < 0 ? 1 : -1);
            }
        });
        stage.addEventListener('pointercancel', function(){ down = false; });
    }
    function caption(a){
        var fig = a.closest('figure');
        var c = fig && fig.querySelector('figcaption');
        var img = a.querySelector('img');
        return (c && c.textContent.trim()) || (img && img.alt) || '';
    }
    function load(i, dir){
        var a = items[i];
        var url = a.href;
        busy = true;
        lbImg.classList.remove('is-ready');
        var next = new Image();
        next.onload = next.onerror = function(){
            lbImg.src = url;
            lbImg.alt = (a.querySelector('img') || {}).alt || '';
            lbImg.classList.remove('is-out-left', 'is-out-right');
            lbCap.textContent = caption(a);
            lbCount.textContent = items.length > 1 ? (i + 1) + ' / ' + items.length : '';
            requestAnimationFrame(function(){
                lbImg.classList.add('is-ready');
                busy = false;
            });
            [i - 1, i + 1].forEach(function(n){
                if(items[n]){
                    new Image().src = items[n].href;
                }
            });
        };
        if(dir){
            lbImg.classList.add(dir > 0 ? 'is-out-left' : 'is-out-right');
        }
        setTimeout(function(){ next.src = url; }, dir ? 120 : 0);
    }
    function go(dir){
        if(busy || items.length < 2){
            return;
        }
        index = (index + dir + items.length) % items.length;
        load(index, dir);
    }
    function open(a){
        if(!lb){
            build();
        }
        var scope = a.closest('.mp-sec, .rc-gallery, .rc-letters, .rc-split, .portal-content, main') || document;
        var seen = {};
        items = [].filter.call(scope.querySelectorAll('a[href]'), function(link){
            if(!isPhotoLink(link) || seen[link.href]){
                return false;
            }
            seen[link.href] = 1;
            return true;
        });
        index = Math.max(0, items.map(function(l){ return l.href; }).indexOf(a.href));
        lb.querySelector('.mo-lb-prev').hidden = lb.querySelector('.mo-lb-next').hidden = items.length < 2;
        lb.showModal();
        load(index, 0);
    }
    document.addEventListener('click', function(e){
        if(e.defaultPrevented || e.button || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey){
            return;
        }
        var a = e.target.closest && e.target.closest('a[href]');
        if(isPhotoLink(a) && a.closest('main') && typeof HTMLDialogElement === 'function'){
            e.preventDefault();
            open(a);
        }
    });

    /* ---- instant page loads: a link is fetched ahead as soon as a pointer rests on it (or a finger touches it) ---- */
    var prefetched = {};
    var prefetchCount = 0;
    var hoverTimer = 0;
    function prefetch(a){
        if(saveData || prefetchCount > 8 || !a || !a.href || a.origin !== location.origin || a.target === '_blank' || a.hasAttribute('download')){
            return;
        }
        var url = a.href.split('#')[0];
        if(url === location.href.split('#')[0] || prefetched[url] || /\.(?:pdf|jpe?g|png|gif|webp|mp4|mp3|zip)$/i.test(url)){
            return;
        }
        prefetched[url] = 1;
        prefetchCount++;
        var l = document.createElement('link');
        l.rel = 'prefetch';
        l.href = url;
        l.as = 'document';
        document.head.appendChild(l);
    }
    if(!saveData && 'relList' in document.createElement('link') && document.createElement('link').relList.supports && document.createElement('link').relList.supports('prefetch')){
        if(fineHover){
            document.addEventListener('mouseover', function(e){
                var a = e.target.closest && e.target.closest('a[href]');
                clearTimeout(hoverTimer);
                if(a){
                    hoverTimer = setTimeout(function(){ prefetch(a); }, 80);
                }
            }, {passive: true});
        }
        document.addEventListener('touchstart', function(e){
            prefetch(e.target.closest && e.target.closest('a[href]'));
        }, {passive: true});
    }
})();

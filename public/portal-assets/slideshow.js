/* Bayanath page: the Photo Slideshow under the video grid.
   Whole photographs on a quiet backdrop, a short cross-fade, previous / next (buttons, side arrows, keyboard, swipe), one dot per photograph,
   and a pause / play button. It advances by itself every data-interval seconds, and holds while the pointer rests on it, focus is inside it,
   it is scrolled out of view or the tab is hidden. With prefers-reduced-motion it starts paused and changes photographs without a fade.
   The next photograph is requested one step ahead (the others stay lazy). A photograph that fails to load is skipped, and if none loads the
   frame shows a short plain message. Without JavaScript the photographs are a swipeable row (see slideshow.css) and nothing here is needed.
   ES5, no libraries, no HTML injection. */
(function(){
    'use strict';
    var root = document.querySelector('[data-slideshow]');
    if(!root){ return; }
    var show = root.querySelector('.ph-show');
    var stage = root.querySelector('.ph-stage');
    var slides = Array.prototype.slice.call(stage.querySelectorAll('.ph-slide'));
    var dots = Array.prototype.slice.call(root.querySelectorAll('.ph-dot'));
    var reduce = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
    var hasIO = 'IntersectionObserver' in window;
    var live = root.querySelector('.ph-live');
    var pp = root.querySelector('.ph-pp');
    var arrows = root.querySelector('.ph-arrows');
    var bar = root.querySelector('.ph-bar');
    var side = Array.prototype.slice.call(root.querySelectorAll('.ph-side'));
    var interval = (parseInt(root.getAttribute('data-interval'), 10) || 10) * 1000;
    var FADE = reduce ? 0 : 700;
    var cur = 0, timer = 0, startedAt = 0, remaining = interval, userPaused = false, leaveTimer = 0;
    var hold = { hover: false, focus: false, off: hasIO, hidden: document.hidden };
    var broken = [];

    var usable = function(i){ return !broken[i]; };
    var anyUsable = function(){ for(var i = 0; i < slides.length; i++){ if(usable(i)){ return true; } } return false; };
    var step = function(from, dir){
        var n = from;
        for(var k = 0; k < slides.length; k++){
            n = (n + dir + slides.length) % slides.length;
            if(usable(n)){ return n; }
        }
        return from;
    };
    var imgOf = function(i){ return slides[i].querySelector('.ph-img'); };
    var warm = function(i){
        // ask for the picture one step ahead; the rest stay lazy
        [slides[i].querySelector('.ph-img'), slides[i].querySelector('.ph-bg')].forEach(function(im){ if(im && im.getAttribute('loading') === 'lazy'){ im.setAttribute('loading', 'eager'); } });
    };

    show.classList.add('is-js');
    stage.scrollLeft = 0;
    arrows.hidden = false; bar.hidden = false;
    side.forEach(function(b){ b.hidden = false; });
    root.style.setProperty('--ph-ms', (interval / 1000) + 's');
    root.style.setProperty('--ph-fade', (FADE / 1000) + 's');

    var anyHold = function(){ return hold.hover || hold.focus || hold.off || hold.hidden; };
    var syncHeld = function(){ show.classList.toggle('is-held', anyHold() || userPaused); };
    var stop = function(){
        if(timer){ window.clearTimeout(timer); timer = 0; remaining -= (Date.now() - startedAt); if(remaining < 400){ remaining = 400; } }
    };
    var start = function(){
        if(timer || userPaused || anyHold() || !anyUsable()){ return; }
        startedAt = Date.now();
        timer = window.setTimeout(function(){ timer = 0; go(step(cur, 1), true); }, remaining);
    };
    var refresh = function(){ syncHeld(); if(anyHold() || userPaused){ stop(); } else { start(); } };

    var go = function(n, auto){
        if(n === cur || !usable(n)){ return; }
        var old = slides[cur], nu = slides[n];
        window.clearTimeout(leaveTimer);
        slides.forEach(function(s){ if(s !== old && s !== nu){ s.classList.remove('is-active', 'is-leaving'); } });
        old.classList.remove('is-active'); old.classList.add('is-leaving');
        nu.classList.remove('is-leaving'); nu.classList.add('is-active');
        leaveTimer = window.setTimeout(function(){ old.classList.remove('is-leaving'); }, FADE);
        dots[cur].classList.remove('is-active'); dots[cur].removeAttribute('aria-current');
        dots[n].classList.add('is-active'); dots[n].setAttribute('aria-current', 'true');
        cur = n;
        warm(step(cur, 1));
        if(!auto){ live.textContent = 'Photograph ' + (n + 1) + ' of ' + slides.length; }
        stop(); timer = 0; remaining = interval;
        refresh();
    };
    var prev = function(){ go(step(cur, -1), false); };
    var next = function(){ go(step(cur, 1), false); };

    root.querySelector('.ph-prev').addEventListener('click', prev);
    root.querySelector('.ph-next').addEventListener('click', next);
    root.querySelector('.ph-side-prev').addEventListener('click', prev);
    root.querySelector('.ph-side-next').addEventListener('click', next);
    dots.forEach(function(d, i){ d.addEventListener('click', function(){ go(i, false); }); });

    var setPaused = function(p){
        userPaused = p;
        pp.classList.toggle('is-paused', p);
        pp.setAttribute('aria-pressed', p ? 'true' : 'false');
        pp.setAttribute('aria-label', p ? 'Play the slideshow' : 'Pause the slideshow');
        show.classList.toggle('is-still', p);
        if(p){ stop(); }
        refresh();
    };
    pp.addEventListener('click', function(){ setPaused(!userPaused); });

    show.addEventListener('keydown', function(e){
        if(e.key === 'ArrowLeft'){ e.preventDefault(); prev(); }
        else if(e.key === 'ArrowRight'){ e.preventDefault(); next(); }
    });
    show.addEventListener('mouseenter', function(){ hold.hover = true; refresh(); });
    show.addEventListener('mouseleave', function(){ hold.hover = false; refresh(); });
    root.addEventListener('focusin', function(){ hold.focus = true; refresh(); });
    root.addEventListener('focusout', function(){ hold.focus = false; refresh(); });
    document.addEventListener('visibilitychange', function(){ hold.hidden = document.hidden; refresh(); });
    if(hasIO){
        new IntersectionObserver(function(entries){
            hold.off = !entries[entries.length - 1].isIntersecting;
            refresh();
        }, { threshold: 0.2 }).observe(root);
    }

    // swipe (and mouse drag): a horizontal flick changes the photograph, a vertical one still scrolls the page
    var sx = 0, sy = 0, sid = null;
    stage.addEventListener('pointerdown', function(e){
        if(e.pointerType === 'mouse' && e.button !== 0){ return; }
        sx = e.clientX; sy = e.clientY; sid = e.pointerId;
    });
    var end = function(e){
        if(sid === null || e.pointerId !== sid){ return; }
        var dx = e.clientX - sx, dy = e.clientY - sy;
        sid = null;
        if(e.type === 'pointerup' && Math.abs(dx) > 40 && Math.abs(dx) > Math.abs(dy) * 1.4){ if(dx < 0){ next(); } else { prev(); } }
    };
    stage.addEventListener('pointerup', end);
    stage.addEventListener('pointercancel', end);
    stage.addEventListener('dragstart', function(e){ e.preventDefault(); });

    // a photograph that cannot be loaded is skipped; if none can be, the frame says so
    slides.forEach(function(s, i){
        var im = imgOf(i);
        var failed = function(){
            if(broken[i]){ return; }
            broken[i] = true;
            s.classList.add('is-broken');
            dots[i].hidden = true;
            if(i === cur){
                var n = step(cur, 1);
                if(n !== cur){ go(n, true); } else { show.classList.add('is-empty'); }
            }
            refresh();
        };
        im.addEventListener('error', failed);
        if(im.complete && im.naturalWidth === 0 && im.getAttribute('src')){ failed(); }
    });

    if(slides.length < 2){
        arrows.hidden = true; bar.hidden = true;
        side.forEach(function(b){ b.hidden = true; });
    } else {
        warm(step(cur, 1));
        if(reduce){ setPaused(true); } else { refresh(); }
    }
})();

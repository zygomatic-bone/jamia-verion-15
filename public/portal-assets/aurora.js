/* Bayanath page: makes the Live Aurora Glow answer the pointer, a touch and the scroll position.
   The CSS (bayanath.css) already drifts the four bands slowly; this file only sets four numbers on the one .bz-bg element:
   --ax and --ay (-1 to 1, the eased shift of the bands) and --sx and --sy (the spot that follows the pointer or the finger).
   Written in the style of the original site: ES5, "function(){", 4 spaces, single quotes, semicolons.
   Design rules:
   - passive listeners only, no touchmove listener, so scrolling and taps are never delayed;
   - one requestAnimationFrame loop that runs only while something is still moving, then stops by itself;
   - eased (interpolated) positions with time-based smoothing, so the gradients glide instead of jumping;
   - one element updated per frame (custom properties), never the whole page;
   - if frames take too long, or motion.js marks the device as slow, the effect simplifies itself and removes its listeners;
   - nothing runs while the tab is hidden, and every listener is removed when the page is left;
   - the aurora layer has pointer-events: none, so video thumbnails, menus and buttons are never blocked. */
(function(){
    'use strict';
    var bg = document.querySelector('.bz-bg');
    var root = document.documentElement;
    if(!bg || (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches)){
        return;
    }
    var w = window.innerWidth || 1;
    var h = window.innerHeight || 1;
    var px = 0;           /* pointer, -1 to 1 */
    var py = 0;
    var scrollN = 0;      /* scroll position, 0 to 1 */
    var ax = 0;           /* eased shift of the bands */
    var ay = 0;
    var sx = w / 2;       /* eased spot position in pixels */
    var sy = h * 0.36;
    var spotX = sx;       /* spot target in pixels */
    var spotY = sy;
    var raf = 0;
    var last = 0;
    var slow = 0;
    var off = false;
    var fadeTimer = 0;

    function target(){
        return {x: px, y: Math.max(-1, Math.min(1, py * 0.7 + (scrollN - 0.5) * 1.6))};
    }
    function ease(dt, rate){
        /* frame-rate independent smoothing: rate is the share of the remaining distance covered per 16.7 ms */
        return 1 - Math.pow(1 - rate, Math.min(dt, 64) / 16.7);
    }
    function frame(now){
        raf = 0;
        if(off){
            return;
        }
        if(root.classList.contains('mo-lite')){
            return simplify();
        }
        var dt = last ? now - last : 16.7;
        last = now;
        /* a long run of slow frames means this device cannot keep up: simplify instead of lagging */
        slow = dt > 45 ? slow + 1 : Math.max(0, slow - 1);
        if(slow > 12){
            return simplify();
        }
        var t = target();
        var kb = ease(dt, 0.2);
        var ks = ease(dt, 0.3);
        ax += (t.x - ax) * kb;
        ay += (t.y - ay) * kb;
        sx += (spotX - sx) * ks;
        sy += (spotY - sy) * ks;
        bg.style.setProperty('--ax', ax.toFixed(3));
        bg.style.setProperty('--ay', ay.toFixed(3));
        bg.style.setProperty('--sx', sx.toFixed(1) + 'px');
        bg.style.setProperty('--sy', sy.toFixed(1) + 'px');
        if(Math.abs(t.x - ax) > 0.002 || Math.abs(t.y - ay) > 0.002 || Math.abs(spotX - sx) > 0.4 || Math.abs(spotY - sy) > 0.4){
            raf = requestAnimationFrame(frame);
        }else{
            last = 0;
        }
    }
    function kick(){
        if(!raf && !off && !document.hidden){
            raf = requestAnimationFrame(frame);
        }
    }
    function glow(on){
        clearTimeout(fadeTimer);
        bg.classList.toggle('is-on', on);
    }
    function onMove(e){
        px = (e.clientX / w - 0.5) * 2;
        py = (e.clientY / h - 0.5) * 2;
        spotX = e.clientX;
        spotY = e.clientY;
        if(!bg.classList.contains('is-on')){
            sx = spotX;
            sy = spotY;
            glow(true);
        }
        kick();
    }
    function onDown(e){
        if(e.pointerType === 'mouse'){
            return;
        }
        /* a finger: the spot appears under it at once and fades shortly after it lifts */
        spotX = sx = e.clientX;
        spotY = sy = e.clientY;
        px = (e.clientX / w - 0.5) * 2;
        py = (e.clientY / h - 0.5) * 2;
        glow(true);
        kick();
    }
    function onUp(e){
        if(e.pointerType === 'mouse'){
            return;
        }
        clearTimeout(fadeTimer);
        fadeTimer = setTimeout(function(){ glow(false); }, 700);
    }
    function onLeave(e){
        if(e && e.pointerType && e.pointerType !== 'mouse'){
            return;   /* a finger leaving the screen is handled by onUp (a short fade) */
        }
        glow(false);
        px = 0;
        py = 0;
        kick();
    }
    function onScroll(){
        var max = Math.max(1, document.documentElement.scrollHeight - h);
        scrollN = Math.min(1, Math.max(0, window.pageYOffset / max));
        kick();
    }
    function onResize(){
        w = window.innerWidth || 1;
        h = window.innerHeight || 1;
        onScroll();
    }
    function onVisibility(){
        if(document.hidden){
            cancelAnimationFrame(raf);
            raf = 0;
            last = 0;
        }else{
            kick();
        }
    }
    function teardown(){
        off = true;
        cancelAnimationFrame(raf);
        clearTimeout(fadeTimer);
        window.removeEventListener('pointermove', onMove);
        window.removeEventListener('pointerdown', onDown);
        window.removeEventListener('pointerup', onUp);
        window.removeEventListener('pointercancel', onUp);
        root.removeEventListener('pointerleave', onLeave);
        window.removeEventListener('scroll', onScroll);
        window.removeEventListener('resize', onResize);
        document.removeEventListener('visibilitychange', onVisibility);
    }
    function simplify(){
        teardown();
        bg.classList.remove('is-on');
        bg.classList.add('bz-lite');
        bg.style.removeProperty('--ax');
        bg.style.removeProperty('--ay');
    }

    window.addEventListener('pointermove', onMove, {passive: true});
    window.addEventListener('pointerdown', onDown, {passive: true});
    window.addEventListener('pointerup', onUp, {passive: true});
    window.addEventListener('pointercancel', onUp, {passive: true});
    root.addEventListener('pointerleave', onLeave, {passive: true});
    window.addEventListener('scroll', onScroll, {passive: true});
    window.addEventListener('resize', onResize, {passive: true});
    document.addEventListener('visibilitychange', onVisibility);
    window.addEventListener('pagehide', teardown);
    onScroll();
})();

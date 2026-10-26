/* About Us, "Support Our Mission": copy buttons for the published bank details, and a soft entrance.
   Without JavaScript the details are plain text on the page and nothing is hidden. Nothing is sent anywhere. */
(function(){
    'use strict';
    var root = document.querySelector('[data-support]');
    if(!root){ return; }
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // entrance
    var shown = false;
    var reveal = function(){ if(!shown){ shown = true; root.classList.add('is-in'); } };
    if(!reduce){
        root.classList.add('is-armed');
        if('IntersectionObserver' in window){
            var io = new IntersectionObserver(function(es){ if(es[0].isIntersecting){ io.disconnect(); reveal(); } }, { threshold: 0.1 });
            io.observe(root);
        } else { reveal(); }
        window.setTimeout(reveal, 3000);   // safety net: never left hidden
    }

    var status = root.querySelector('.sup-status');
    var say = function(t){ if(status){ status.textContent = t; } };
    var done = function(btn, label){
        var span = btn.querySelector('span'), was = span.textContent;
        btn.classList.add('is-done'); span.textContent = label; say(label === 'Copied' ? 'Copied to your clipboard.' : label);
        window.setTimeout(function(){ btn.classList.remove('is-done'); span.textContent = was; }, 2200);
    };
    var copy = function(text){
        if(navigator.clipboard && window.isSecureContext){ return navigator.clipboard.writeText(text); }
        return new Promise(function(resolve, reject){   // older browsers and plain-http previews
            var t = document.createElement('textarea');
            t.value = text; t.setAttribute('readonly', ''); t.style.position = 'fixed'; t.style.top = '0'; t.style.opacity = '0';
            document.body.appendChild(t); t.select();
            var ok = false;
            try { ok = document.execCommand('copy'); } catch(e) {}
            document.body.removeChild(t);
            return ok ? resolve() : reject(new Error('copy failed'));
        });
    };
    var attempt = function(btn, text){
        copy(text).then(function(){ done(btn, 'Copied'); }, function(){ say('Your browser would not copy. Please select the details and copy them by hand.'); });
    };

    var rows = Array.prototype.slice.call(root.querySelectorAll('.sup-row'));
    rows.forEach(function(row){
        var b = row.querySelector('.sup-copy'), v = row.querySelector('.sup-val');
        if(!b || !v){ return; }
        b.hidden = false;
        b.addEventListener('click', function(){ attempt(b, v.getAttribute('data-copy')); });
    });
    var all = root.querySelector('.sup-all');
    if(all && rows.length){
        all.hidden = false;
        all.addEventListener('click', function(){
            var text = rows.map(function(r){ return r.querySelector('dt').textContent + ': ' + r.querySelector('.sup-val').getAttribute('data-copy'); }).join('\n');
            attempt(all, text);
        });
    }
})();

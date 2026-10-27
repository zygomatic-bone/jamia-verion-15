/* Contact, Feedback, Admissions and Careers pages: progressive enhancement.
   Written in the style of the original site: ES5, "function(){", 4 spaces, single quotes, semicolons.
   Everything on these pages works without this file: the forms are ordinary forms. When the form service is set up
   (the form's action address) they post to it and it answers with a small page; until then they are mail links and carry
   data-cx-offline (invisible to visitors). This file adds: copy buttons, the department search, the feedback journey (stars, face, steps), the
   checklist counters, the role cards and the fetch() submit with honest success and error states.
   Rules:
   - success is shown only when the form service answers 200 with {"ok": true}; anything else keeps the form and the text;
   - a form marked data-cx-offline (no service set up) never contacts anything and never shows success: it opens the visitor's email program with the message ready and says only that;
   - the request carries no cookies (credentials: 'omit'): the service lives on another origin and needs none;
   - nothing a visitor types is ever put into the page as HTML (textContent only);
   - listeners are passive where they can be, and the pointer glow runs from one requestAnimationFrame at a time;
   - html.cx-js is set first, so the CSS may start hidden states only when this script is really running. */
(function(){
    'use strict';
    var root = document.documentElement;
    var reduce = !!(window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches);
    var t0 = Date.now();
    var toastTimer = 0;
    root.classList.add('cx-js');

    function $(sel, ctx){ return (ctx || document).querySelector(sel); }
    function $$(sel, ctx){ return [].slice.call((ctx || document).querySelectorAll(sel)); }

    /* ---------- toast + copy buttons ---------- */
    var toast = $('.cx-toast');
    function say(text){
        if(!toast){
            return;
        }
        toast.textContent = text;
        toast.classList.add('is-on');
        clearTimeout(toastTimer);
        toastTimer = setTimeout(function(){ toast.classList.remove('is-on'); }, 2400);
    }
    function copyText(text, done, fail){
        if(navigator.clipboard && navigator.clipboard.writeText){
            navigator.clipboard.writeText(text).then(done, fail);
            return;
        }
        var ta = document.createElement('textarea');
        ta.value = text;
        ta.setAttribute('readonly', '');
        ta.className = 'cx-sr';
        document.body.appendChild(ta);
        ta.select();
        var ok = false;
        try{
            ok = document.execCommand('copy');
        }catch(e){
            ok = false;
        }
        document.body.removeChild(ta);
        if(ok){
            done();
        }else{
            fail();
        }
    }
    $$('[data-cx-copy]').forEach(function(btn){
        btn.hidden = false;
        btn.addEventListener('click', function(){
            var what = btn.getAttribute('data-cx-what') || 'Text';
            copyText(btn.getAttribute('data-cx-copy'), function(){ say(what + ' copied'); }, function(){ say('Could not copy. Please select the text and copy it.'); });
        });
    });

    /* ---------- department search ---------- */
    var q = $('[data-cx-filter]');
    if(q){
        var list = $(q.getAttribute('data-cx-filter'));
        var items = $$('.cx-dept', list);
        var count = $('.cx-count');
        q.parentNode.hidden = false;
        q.addEventListener('input', function(){
            var term = q.value.toLowerCase().replace(/\s+/g, ' ').trim();
            var plain = term.replace(/\s/g, '');
            var shown = 0;
            items.forEach(function(li){
                var hay = li.getAttribute('data-dept');
                var hit = !term || hay.indexOf(term) > -1 || hay.replace(/\s/g, '').indexOf(plain) > -1;
                li.hidden = !hit;
                if(hit){
                    shown++;
                }
            });
            if(count){
                count.hidden = !term;
                count.textContent = shown ? ('Showing ' + shown + ' of ' + items.length + ' departments') : 'No department matches that search. Please call the Administrative Office.';
            }
        });
    }

    /* ---------- pointer glow on cards (fine pointers only) ---------- */
    if(!reduce && window.matchMedia && matchMedia('(hover: hover) and (pointer: fine)').matches){
        var glowRaf = 0;
        var gx = 0;
        var gy = 0;
        var gel = null;
        document.addEventListener('pointermove', function(e){
            var card = e.target.closest ? e.target.closest('.cx-card') : null;
            if(!card){
                return;
            }
            gel = card;
            var r = card.getBoundingClientRect();
            gx = e.clientX - r.left;
            gy = e.clientY - r.top;
            if(!glowRaf){
                glowRaf = requestAnimationFrame(function(){
                    glowRaf = 0;
                    gel.style.setProperty('--mx', gx + 'px');
                    gel.style.setProperty('--my', gy + 'px');
                });
            }
        }, {passive: true});
    }

    /* ---------- admissions: the journey line and number badges light up when they come into view ---------- */
    var journey = $('.cx-journey');
    if(journey){
        if('IntersectionObserver' in window){
            var jo = new IntersectionObserver(function(entries){
                entries.forEach(function(en){
                    if(en.isIntersecting){
                        journey.classList.add('is-on');
                        jo.disconnect();
                    }
                });
            }, {threshold: 0.25});
            jo.observe(journey);
            setTimeout(function(){ journey.classList.add('is-on'); }, 6000);
        }else{
            journey.classList.add('is-on');
        }
    }

    /* ---------- admissions: document checklists (for the visitor's own use; nothing is sent) ---------- */
    $$('[data-cx-list]').forEach(function(box){
        var ticks = $$('[data-cx-tick]', box);
        var meter = $('.cx-meter', box);
        var bar = $('.cx-meter-bar i', box);
        var txt = $('.cx-meter-t', box);
        meter.hidden = false;
        function update(){
            var n = ticks.filter(function(t){ return t.checked; }).length;
            bar.style.setProperty('--p', String(n / ticks.length));
            txt.textContent = n === ticks.length ? 'All ready' : (n + ' of ' + ticks.length + ' ready');
        }
        ticks.forEach(function(t){ t.addEventListener('change', update); });
        update();
    });

    /* ---------- careers: role cards fill in the area of interest ---------- */
    var areaSel = $('#careers-area');
    var roleBtns = $$('[data-cx-area]');
    function markRole(){
        roleBtns.forEach(function(b){
            var on = areaSel && areaSel.value === b.getAttribute('data-cx-area');
            b.classList.toggle('is-picked', on);
            b.setAttribute('aria-pressed', on ? 'true' : 'false');
        });
    }
    if(areaSel && roleBtns.length){
        roleBtns.forEach(function(b){
            b.setAttribute('aria-pressed', 'false');
            b.addEventListener('click', function(){
                areaSel.value = b.getAttribute('data-cx-area');
                markRole();
                var target = $('#interest');
                if(target && target.scrollIntoView){
                    target.scrollIntoView({behavior: reduce ? 'auto' : 'smooth', block: 'start'});
                }
                setTimeout(function(){ areaSel.focus({preventScroll: true}); }, reduce ? 0 : 450);
                say('Area chosen: ' + areaSel.options[areaSel.selectedIndex].text);
            });
        });
        areaSel.addEventListener('change', markRole);
    }

    /* ---------- links such as Admissions.html?programme=pu or Careers.html?area=computer pre-select a choice ---------- */
    (function(){
        var s = location.search.replace(/^\?/, '').split('&');
        s.forEach(function(pair){
            var kv = pair.split('=');
            var name = kv[0];
            var val = kv[1] ? decodeURIComponent(kv[1]) : '';
            if(['programme', 'area', 'category'].indexOf(name) < 0 || !val){
                return;
            }
            var radio = $$('input[type="radio"][name="' + name + '"]').filter(function(r){ return r.value === val; })[0];
            if(radio){
                radio.checked = true;
                return;
            }
            var sel = $('select[name="' + name + '"]');
            if(sel){
                sel.value = val;
                if(sel.value !== val){
                    sel.value = '';
                }
                markRole();
            }
        });
    })();

    /* ---------- forms ---------- */
    var RULES = {feedback: {message: 5}};
    var WORDS = ['Not good', 'Could be better', 'Good', 'Very good', 'Wonderful'];
    var MOUTHS = ['M15 33 Q24 26 33 33', 'M16 31 Q24 28 32 31', 'M16 30 Q24 30 32 30', 'M15 29 Q24 35 33 29', 'M14 28 Q24 39 34 28'];

    function initForm(form){
        var kind = form.getAttribute('data-cx-form');
        var banner = $('.cx-banner', form);
        var fallback = $('.cx-fallback', form);
        var steps = $$('.cx-step', form);
        var wrap = form.parentNode;
        var success = $('[data-cx-success="' + kind + '"]', wrap);
        var cur = 0;
        var busy = false;

        function ctl(name){ return form.elements[name]; }
        function errBox(name){ return document.getElementById(kind + '-' + name + '-e'); }
        function setErr(name, msg){
            var box = errBox(name);
            var c = ctl(name);
            var first = c && (c.length && !c.tagName ? c[0] : c);
            var holder = first && first.closest ? first.closest('.cx-field') : null;
            if(box){
                box.hidden = !msg;
                box.textContent = msg || '';
            }
            if(holder){
                holder.classList.toggle('is-bad', !!msg);
            }
            if(first && first.setAttribute){
                if(msg){
                    first.setAttribute('aria-invalid', 'true');
                }else{
                    first.removeAttribute('aria-invalid');
                }
            }
        }
        function clearErrors(){
            $$('.cx-err', form).forEach(function(b){ b.hidden = true; b.textContent = ''; });
            $$('.is-bad', form).forEach(function(h){ h.classList.remove('is-bad'); });
            $$('[aria-invalid]', form).forEach(function(c){ c.removeAttribute('aria-invalid'); });
            banner.hidden = true;
            fallback.hidden = true;
            $$('.cx-handoff', form).forEach(function(n){ n.hidden = true; });
        }
        function value(name){
            var c = ctl(name);
            if(!c){
                return '';
            }
            if(c.length && !c.tagName){
                var on = [].filter.call(c, function(r){ return r.checked; })[0];
                return on ? on.value : '';
            }
            if(c.type === 'checkbox'){
                return c.checked ? c.value : '';
            }
            return String(c.value || '').replace(/^\s+|\s+$/g, '');
        }
        /* mirrors the server rules; the server stays the authority */
        function check(name, label){
            var c = ctl(name);
            if(!c){
                return '';
            }
            var first = c.length && !c.tagName ? c[0] : c;
            var req = first.hasAttribute('required');
            var v = value(name);
            if(!v){
                if(!req){
                    return '';
                }
                if(name === 'consent'){
                    return 'Please tick this box so that we may contact you.';
                }
                if(name === 'rating'){
                    return 'Please tap a star to rate your experience.';
                }
                if(first.type === 'radio' || first.tagName === 'SELECT'){
                    return 'Please choose one of the options.';
                }
                return 'Please fill this in.';
            }
            if(name === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)){
                return 'Please enter an email address such as name@example.com.';
            }
            if(name === 'phone'){
                var digits = v.replace(/\D/g, '');
                if(!/^[0-9 +()\-]{7,20}$/.test(v) || digits.length < 7 || digits.length > 15){
                    return 'Please enter a phone number we can call.';
                }
            }
            if(RULES[kind] && RULES[kind][name] && v.length < RULES[kind][name]){
                return 'Please write a little more (at least ' + RULES[kind][name] + ' characters).';
            }
            return '';
        }
        function names(scope){
            var seen = {};
            var out = [];
            $$('input[name], select[name], textarea[name]', scope).forEach(function(c){
                if(c.type === 'hidden' || c.name === 'website' || seen[c.name]){
                    return;
                }
                seen[c.name] = 1;
                out.push(c.name);
            });
            return out;
        }
        function validate(scope){
            var firstBad = null;
            names(scope).forEach(function(n){
                var msg = check(n);
                setErr(n, msg);
                if(msg && !firstBad){
                    firstBad = n;
                }
            });
            return firstBad;
        }
        function focusField(name){
            var c = ctl(name);
            var el = c && c.length && !c.tagName ? c[0] : c;
            if(el && el.focus){
                el.focus();
            }
        }

        /* -- the journey (feedback) -- */
        var prog = $('.cx-progress', form);
        var back = $('.cx-back', form);
        var next = $('.cx-next', form);
        var finalBtn = $('.cx-submit', form);
        function showStep(i, focus){
            cur = i;
            steps.forEach(function(s, n){
                s.hidden = n !== i;
                s.classList.remove('is-in');
            });
            steps[i].classList.add('is-in');
            if(prog){
                $$('li', prog).forEach(function(li, n){
                    li.classList.toggle('is-done', n < i);
                    li.classList.toggle('is-now', n === i);
                    if(n === i){
                        li.setAttribute('aria-current', 'step');
                    }else{
                        li.removeAttribute('aria-current');
                    }
                });
            }
            back.hidden = i === 0;
            next.hidden = i === steps.length - 1;
            finalBtn.hidden = i !== steps.length - 1;
            if(focus){
                var lg = $('legend', steps[i]);
                if(lg){
                    lg.setAttribute('tabindex', '-1');
                    lg.focus({preventScroll: false});
                }
            }
        }
        if(steps.length){
            form.classList.add('is-steps');
            prog.hidden = false;
            showStep(0, false);
            next.addEventListener('click', function(){ goNext(); });
            back.addEventListener('click', function(){ showStep(cur - 1, true); });
        }
        function goNext(){
            var bad = validate(steps[cur]);
            if(bad){
                focusField(bad);
                return;
            }
            showStep(cur + 1, true);
        }

        /* -- stars, face, counter -- */
        var stars = $('.cx-stars', form);
        if(stars){
            var word = $('[data-cx-word]', form);
            var mouth = $('.cx-mouth', form);
            var radios = $$('input[name="rating"]', form);
            var fillTo = function(n){ stars.setAttribute('data-fill', String(n || 0)); };
            var chosen = function(){
                var r = radios.filter(function(x){ return x.checked; })[0];
                return r ? parseInt(r.value, 10) : 0;
            };
            var describe = function(n){
                word.textContent = n ? WORDS[n - 1] : 'Tap a star to rate';
                mouth.setAttribute('d', n ? MOUTHS[n - 1] : 'M15 30 Q24 30 33 30');
            };
            radios.forEach(function(r){
                r.addEventListener('change', function(){
                    var n = chosen();
                    fillTo(n);
                    describe(n);
                    setErr('rating', '');
                    var lab = r.nextElementSibling;
                    if(lab && !reduce){
                        lab.classList.remove('is-pop');
                        void lab.offsetWidth;
                        lab.classList.add('is-pop');
                    }
                });
            });
            $$('.cx-star', stars).forEach(function(lab){
                lab.addEventListener('mouseenter', function(){
                    if(window.matchMedia && matchMedia('(hover: hover)').matches){
                        var n = parseInt(lab.getAttribute('data-v'), 10);
                        fillTo(n);
                        describe(n);
                    }
                });
            });
            stars.addEventListener('mouseleave', function(){ fillTo(chosen()); describe(chosen()); });
            fillTo(0);
        }
        var msg = ctl('message');
        var counter = $('[data-cx-count]', form);
        if(msg && counter){
            msg.addEventListener('input', function(){ counter.textContent = String(msg.value.length); });
        }
        $$('input, select, textarea', form).forEach(function(c){
            c.addEventListener('input', function(){
                if(c.name && errBox(c.name) && !errBox(c.name).hidden){
                    setErr(c.name, '');
                }
            });
            c.addEventListener('change', function(){
                if(c.name && errBox(c.name) && !errBox(c.name).hidden){
                    setErr(c.name, '');
                }
            });
        });

        /* -- sending -- */
        function mailtoFor(target){
            var parts = [];
            names(form).forEach(function(n){
                var v = value(n);
                if(v && n !== 'consent'){
                    parts.push(n + ': ' + v);
                }
            });
            var a = $('a', target || fallback);
            if(a){
                var base = a.getAttribute('href').split('&body=')[0];
                a.setAttribute('href', base + '&body=' + encodeURIComponent(parts.join('\n').slice(0, 1400)));
            }
        }
        function fail(message, withFallback){
            banner.textContent = message;
            banner.hidden = false;
            if(withFallback){
                mailtoFor();
                fallback.hidden = false;
            }
            banner.scrollIntoView && banner.scrollIntoView({behavior: reduce ? 'auto' : 'smooth', block: 'nearest'});
        }
        function finish(ref){
            form.hidden = true;
            success.hidden = false;
            var refLine = $('.cx-ref-line', success);
            if(ref && refLine){
                $('[data-cx-ref]', success).textContent = ref;
                refLine.hidden = false;
            }
            void success.offsetWidth;
            success.classList.add('is-on');
            var h = $('[data-cx-focus]', success);
            if(h){
                h.setAttribute('tabindex', '-1');
                h.focus();
            }
            if(success.scrollIntoView){
                success.scrollIntoView({behavior: reduce ? 'auto' : 'smooth', block: 'center'});
            }
        }
        function stepOf(name){
            var c = ctl(name);
            var el = c && c.length && !c.tagName ? c[0] : c;
            var s = el && el.closest ? el.closest('.cx-step') : null;
            return s ? steps.indexOf(s) : -1;
        }
        function handle(res){
            var j = res.json;
            if(res.status === 200 && j && j.ok === true){
                finish(j.ref || '');
                return;
            }
            if(j && res.status === 422 && j.errors){
                var firstName = '';
                Object.keys(j.errors).forEach(function(n){
                    setErr(n, String(j.errors[n]));
                    if(!firstName){
                        firstName = n;
                    }
                });
                banner.textContent = String(j.message || 'Please check the highlighted fields.');
                banner.hidden = false;
                if(firstName){
                    var si = stepOf(firstName);
                    if(si > -1 && steps.length){
                        showStep(si, false);
                    }
                    focusField(firstName);
                }
                return;
            }
            if(j && j.message){
                fail(String(j.message) + ' Your text is still here.', true);
                return;
            }
            fail('We could not send your message just now. Please try again in a few minutes. Your text is still here.', true);
        }
        var sendLabel = $('.cx-submit-label', form);
        var sendText = sendLabel ? sendLabel.textContent : '';
        function sending(on){
            if(sendLabel){
                sendLabel.textContent = on ? 'Sending\u2026' : sendText;
            }
        }
        function send(){
            if(busy){
                return;
            }
            clearErrors();
            var bad = validate(form);
            if(bad){
                var si = stepOf(bad);
                if(si > -1 && steps.length){
                    showStep(si, false);
                }
                focusField(bad);
                return;
            }
            busy = true;
            form.classList.add('is-busy');
            form.setAttribute('aria-busy', 'true');
            sending(true);
            if(form.hasAttribute('data-cx-offline')){
                /* no form service yet: hand the answers to the visitor's own email program, and claim nothing more than that */
                setTimeout(function(){
                    var note = $('.cx-handoff', form);
                    mailtoFor(note);
                    busy = false;
                    form.classList.remove('is-busy');
                    form.removeAttribute('aria-busy');
                    sending(false);
                    note.hidden = false;
                    location.href = $('a', note).getAttribute('href');
                }, reduce ? 0 : 600);
                return;
            }
            var fd = new FormData(form);
            fd.set('opened', String(Date.now() - t0));
            fetch(form.action, {method: 'POST', body: fd, headers: {'Accept': 'application/json'}, credentials: 'omit', mode: 'cors', redirect: 'error', referrerPolicy: 'strict-origin-when-cross-origin'}).then(function(r){
                return r.text().then(function(t){
                    var j = null;
                    try{
                        j = JSON.parse(t);
                    }catch(e){
                        j = null;
                    }
                    return {status: r.status, json: (j && typeof j === 'object') ? j : null};
                });
            }).then(handle, function(){
                fail('We could not send your message just now. Please check your connection and try again. Your text is still here.', true);
            }).then(function(){
                busy = false;
                form.classList.remove('is-busy');
                form.removeAttribute('aria-busy');
                sending(false);
            });
        }
        if(window.fetch && window.FormData){
            form.addEventListener('submit', function(e){
                e.preventDefault();
                if(steps.length && cur < steps.length - 1){
                    goNext();
                    return;
                }
                send();
            });
        }else{
            /* very old browsers: the plain post still works (to the service, or a mail link while it is not set up); just fill in the timer */
            form.addEventListener('submit', function(){
                $('[data-cx-opened]', form).value = String(Date.now() - t0);
            });
        }
        var again = $('.cx-again', wrap);
        if(again){
            again.addEventListener('click', function(){
                form.reset();
                clearErrors();
                if(stars){
                    stars.setAttribute('data-fill', '0');
                    $('[data-cx-word]', form).textContent = 'Tap a star to rate';
                    $('.cx-mouth', form).setAttribute('d', 'M15 30 Q24 30 33 30');
                }
                if(counter){
                    counter.textContent = '0';
                }
                success.hidden = true;
                success.classList.remove('is-on');
                form.hidden = false;
                if(steps.length){
                    showStep(0, true);
                }
            });
        }
    }
    $$('[data-cx-form]').forEach(initForm);
})();

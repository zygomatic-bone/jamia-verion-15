/* Scholar-profile-only title reveals. Independent of the shared motion layer. */
(function(){
    'use strict';
    var page = document.querySelector('.page-scholar');
    if(!page){
        return;
    }
    var titles = [].slice.call(page.querySelectorAll('.bz-head h1, .sh-sec h2, .sh-role-body h3'));
    if(!titles.length){
        return;
    }
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if(reduce){
        return;
    }
    var directions = ['left', 'right', 'up'];
    titles.forEach(function(el, index){
        el.classList.add('sh-title-reveal', 'sh-from-' + directions[index % directions.length]);
    });
    function reveal(el, index){
        el.style.setProperty('--sh-title-delay', (index % 4 * 0.09).toFixed(2) + 's');
        requestAnimationFrame(function(){
            requestAnimationFrame(function(){
                el.classList.add('sh-title-visible');
            });
        });
    }
    if(!('IntersectionObserver' in window)){
        titles.forEach(function(el, index){
            reveal(el, index);
        });
        return;
    }
    var observer = new IntersectionObserver(function(entries){
        entries.forEach(function(entry){
            if(entry.isIntersecting){
                observer.unobserve(entry.target);
                reveal(entry.target, titles.indexOf(entry.target));
            }
        });
    }, {
        threshold: 0.05,
        rootMargin: '0px 0px -5% 0px'
    });
    titles.forEach(function(el){
        observer.observe(el);
    });
    window.addEventListener('pagehide', function(){
        observer.disconnect();
    }, {once: true});
})();
/* Jamia Masjid page: muted, looping videos start when they scroll into view and pause when they leave.
   Respects reduced-motion and data-saver settings (the video then waits for the visitor to press play). */
(function () {
  var vids = [].slice.call(document.querySelectorAll('video[data-autoplay]'));
  if (!vids.length) return;
  // Poster frames are attached only when a clip is within about one screen of the viewport, so ten of them do not compete
  // with the stylesheet and the first photograph on a slow phone connection.
  function setPoster(v) { if (v.getAttribute('data-poster')) { v.poster = v.getAttribute('data-poster'); v.removeAttribute('data-poster'); } }
  if ('IntersectionObserver' in window) {
    var pio = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { setPoster(e.target); pio.unobserve(e.target); } }); }, { rootMargin: '900px 0px' });
    vids.forEach(function (v) { pio.observe(v); });
  } else { vids.forEach(setPoster); }
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var save = navigator.connection && navigator.connection.saveData;
  if (reduce || save || !('IntersectionObserver' in window)) return; // controls stay visible; nothing starts by itself
  var userPaused = new WeakSet();
  vids.forEach(function (v) {
    v.controls = false; v.muted = true;
    var b = document.createElement('button');
    b.type = 'button'; b.className = 'mp-vbtn'; b.setAttribute('aria-label', 'Pause video'); b.setAttribute('aria-pressed', 'false');
    b.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path class="p" d="M8 5v14M16 5v14"></path><path class="q" d="M8 5l11 7-11 7Z"></path></svg>';
    v.parentNode.appendChild(b);
    b.addEventListener('click', function () {
      if (v.paused) { userPaused.delete(v); v.play().catch(function () {}); } else { userPaused.add(v); v.pause(); }
    });
    function sync() { var p = v.paused; b.setAttribute('aria-pressed', p ? 'true' : 'false'); b.setAttribute('aria-label', p ? 'Play video' : 'Pause video'); b.classList.toggle('is-paused', p); }
    v.addEventListener('play', sync); v.addEventListener('pause', sync); sync();
  });
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      var v = e.target;
      if (e.isIntersecting && !userPaused.has(v) && !document.hidden) v.play().catch(function () { v.controls = true; });
      else v.pause();
    });
  }, { threshold: 0.4 });
  vids.forEach(function (v) { io.observe(v); });
  document.addEventListener('visibilitychange', function () {
    if (document.hidden) vids.forEach(function (v) { v.pause(); });
    else vids.forEach(function (v) { io.unobserve(v); io.observe(v); }); // re-check which clips are on screen
  });
})();

/* Applies the saved (or system) colour theme before first paint.
   Kept as an external file so the site can use a strict Content-Security-Policy without inline scripts. */
(function () {
  document.documentElement.classList.add('js'); // lets CSS hide reveal-on-scroll items only when scripting works
  try {
    var saved = localStorage.getItem('jame-theme');
    document.documentElement.dataset.theme = saved || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  } catch (e) {
    document.documentElement.dataset.theme = 'light';
  }
})();

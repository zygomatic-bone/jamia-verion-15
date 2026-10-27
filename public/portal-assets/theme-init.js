/* Applies the saved colour theme before first paint. First-time visitors (nothing saved) get the light theme; a visitor who has chosen
   light or dark keeps that choice on every page and every visit (localStorage key "jame-theme", written by the toggle in app.js).
   Kept as an external file so the site can use a strict Content-Security-Policy without inline scripts. */
(function () {
  document.documentElement.classList.add('js'); // lets CSS hide reveal-on-scroll items only when scripting works
  var theme = 'light';
  try {
    var saved = localStorage.getItem('jame-theme');
    if (saved === 'dark' || saved === 'light') theme = saved;
  } catch (e) {}
  document.documentElement.dataset.theme = theme;
})();

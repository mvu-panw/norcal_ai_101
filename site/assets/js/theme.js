// Dark mode toggle. Dark is the default look; a visitor's choice is remembered.
// Loaded in <head> without defer so the saved theme applies before first paint (no flash).
(function () {
  var KEY = 'ai101-theme';
  var root = document.documentElement;
  var saved = null;
  try { saved = localStorage.getItem(KEY); } catch (e) {}
  root.setAttribute('data-theme', saved === 'light' ? 'light' : 'dark');

  function sync(btn) {
    var dark = root.getAttribute('data-theme') !== 'light';
    btn.setAttribute('aria-pressed', dark ? 'true' : 'false');
    btn.title = dark ? 'Switch to light mode' : 'Switch to dark mode';
    btn.textContent = dark ? '☀︎' : '☾';  // sun in dark mode, moon in light mode
  }

  document.addEventListener('DOMContentLoaded', function () {
    var btn = document.querySelector('.theme-toggle');
    if (!btn) return;
    sync(btn);
    btn.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem(KEY, next); } catch (e) {}
      sync(btn);
    });
  });
})();

// Naviga Law — small progressive enhancements. Everything works without JS.
(function () {
  // Mobile menu
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!open));
      nav.classList.toggle('open', !open);
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) { toggle.setAttribute('aria-expanded', 'false'); nav.classList.remove('open'); }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('open')) { toggle.click(); toggle.focus(); }
    });
  }

  // Services carousel arrows (phones only — grid on larger screens)
  var grid = document.querySelector('.svc-grid');
  function step(dir) { if (grid) grid.scrollBy({ left: dir * (grid.clientWidth + 16), behavior: 'smooth' }); }
  var prev = document.querySelector('.svc-prev'), next = document.querySelector('.svc-next');
  if (prev) prev.addEventListener('click', function () { step(-1); });
  if (next) next.addEventListener('click', function () { step(1); });

  // Jumping to the consultation form on a phone: scroll the carousel to it
  function revealForm() {
    if (location.hash === '#schedule-consultation' && grid) {
      var f = document.getElementById('schedule-consultation');
      if (f && getComputedStyle(grid).display === 'flex') grid.scrollLeft = f.offsetLeft - grid.offsetLeft;
    }
  }
  window.addEventListener('hashchange', revealForm); revealForm();

  // Forms: submit in place, fall back to normal POST (which redirects to /thanks/)
  document.querySelectorAll('form.js-form').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      if (!window.fetch) return;
      e.preventDefault();
      var btn = form.querySelector('button[type=submit]');
      var status = form.querySelector('.form-status');
      var label = btn.textContent;
      btn.disabled = true; btn.textContent = 'Sending…';
      status.className = 'form-status'; status.textContent = '';
      fetch(form.action, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } })
        .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok, j: j }; }); })
        .then(function (res) {
          if (!res.ok) throw new Error((res.j && res.j.error) || '');
          form.reset();
          status.textContent = form.querySelector('[name=form]').value === 'consultation'
            ? 'Thank you — Meredith will email you within one business day to set a time.'
            : 'Thank you — your message is on its way. We usually reply within one business day.';
        })
        .catch(function (err) {
          status.className = 'form-status err';
          status.textContent = (err && err.message) || 'Something went wrong. Please email info@navigalaw.com or call (207) 805-2182.';
        })
        .finally(function () { btn.disabled = false; btn.textContent = label; });
    });
  });
})();

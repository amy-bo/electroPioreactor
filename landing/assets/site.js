// electropioreactor.org: shared behaviour (theme switch, mobile menu, table-of-contents highlight).
(() => {
  // theme: dark | light | auto, stored per browser; the <head> script applies it before first paint
  const sel = document.getElementById('themeSel');
  const OS_LIGHT = matchMedia('(prefers-color-scheme: light)');
  const read = () => { try { return localStorage.getItem('theme') || 'auto'; } catch (e) { return 'auto'; } };
  const apply = (t) => {
    const d = document.documentElement;
    if (t === 'auto') delete d.dataset.theme; else d.dataset.theme = t;
    const light = t === 'light' || (t === 'auto' && OS_LIGHT.matches);
    window.dispatchEvent(new CustomEvent('themechange', { detail: { theme: t, light } }));
  };
  if (sel) {
    sel.value = read();
    sel.addEventListener('change', () => { try { localStorage.setItem('theme', sel.value); } catch (e) {} apply(sel.value); });
  }
  OS_LIGHT.addEventListener('change', () => { if (read() === 'auto') apply('auto'); });
  window.__themeLight = () => { const t = read(); return t === 'light' || (t === 'auto' && OS_LIGHT.matches); };

  const btn = document.querySelector('.menu-btn');
  const nav = document.getElementById('site-nav');
  if (btn && nav) {
    const set = (open) => {
      btn.setAttribute('aria-expanded', String(open));
      nav.classList.toggle('open', open);
      btn.querySelector('.menu-label').textContent = open ? 'Close' : 'Menu';
    };
    btn.addEventListener('click', () => set(btn.getAttribute('aria-expanded') !== 'true'));
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && nav.classList.contains('open')) { set(false); btn.focus(); }
    });
    document.addEventListener('click', (e) => {
      if (nav.classList.contains('open') && !nav.contains(e.target) && !btn.contains(e.target)) set(false);
    });
    matchMedia('(min-width: 881px)').addEventListener('change', (m) => { if (m.matches) set(false); });
  }

  // highlight the current heading in the side table of contents
  const links = [...document.querySelectorAll('.toc-side .toc a')];
  if (links.length && 'IntersectionObserver' in window) {
    const byId = new Map(links.map((a) => [decodeURIComponent(a.hash.slice(1)), a]));
    const heads = [...byId.keys()].map((id) => document.getElementById(id)).filter(Boolean);
    const seen = new Set();
    const io = new IntersectionObserver((entries) => {
      for (const e of entries) e.isIntersecting ? seen.add(e.target) : seen.delete(e.target);
      const first = heads.find((h) => seen.has(h));
      if (!first) return;
      links.forEach((a) => a.classList.toggle('active', a === byId.get(first.id)));
    }, { rootMargin: '-70px 0px -65% 0px' });
    heads.forEach((h) => io.observe(h));
  }
})();

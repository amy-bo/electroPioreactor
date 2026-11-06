// electropioreactor.org: shared behaviour (mobile menu, table-of-contents highlight).
(() => {
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

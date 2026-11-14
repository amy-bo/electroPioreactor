// Site-wide constants. Change the branch here when the default branch moves (repo: links follow it).
export const BRANCH = 'main';
export const SITE = {
  name: 'electroPioreactor',
  longName: 'Aseptic electroPioreactor AEP0.2',
  tagline: 'Open hardware for hydrogen-oxidising bacteria',
  origin: 'https://electropioreactor.org',
  guide: 'https://docs.electropioreactor.org/AEP/',
  github: 'https://github.com/amy-bo/electroPioreactor',
  repoBlob: `https://github.com/amy-bo/electroPioreactor/blob/${BRANCH}/`,
  repoTree: `https://github.com/amy-bo/electroPioreactor/tree/${BRANCH}/`,
  radicle: 'https://app.radicle.xyz/nodes/iris.radicle.xyz/rad%3AzY4GuyErQo91xGYdLi4r2bea9QDJ',
  forum: 'https://forum.amybo.org',
  bibliography: 'https://bibbase.org/show?bib=https://raw.githubusercontent.com/amy-bo/electroPioreactor/main/Literature/HOB%20ferm.%20in-culture%20electrolysis.bib',
  amybo: 'https://amybo.org',
  email: 'hello@amybo.org',
  carma: 'https://carmahub.co.uk/about-us/pump-priming-projects/',
  imperial: 'https://profiles.imperial.ac.uk/s.billerbeck',
  edinburgh: 'https://biology.ed.ac.uk/chris-french-laboratory',
  labcrafter: 'https://labcrafter.co.uk',
  pioreactor: 'https://pioreactor.com',
  // filled in by build.mjs from landing/content/*.md, in `order`: [{ slug, href, label }]
  nav: [],
};

// Site-wide constants. Change the branch here when the default branch moves (repo: links follow it).
export const BRANCH = 'AEP02';
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
  // filled in by build.mjs (a section index, or a content page whose slug is the section name)
  sectionHref: { learn: '/learn/', build: '/build/', research: '/research/', about: '/about/' },
};
export const SECTIONS = {
  learn: { title: 'Learn', blurb: 'What the electroPioreactor is, why hydrogen-oxidising bacteria matter, and how the parts work together. No background needed.' },
  build: { title: 'Build', blurb: 'Specifications, variants, software, media and how to get or build one. Links into the assembly video guide.' },
  research: { title: 'Research', blurb: 'The gas and electrolysis model, results, past projects and the literature behind the design.' },
  about: { title: 'About', blurb: 'Who makes the electroPioreactor, who funds it, and how the project is shared.' },
};
export const AUDIENCE = {
  newcomer: { label: 'Start here', long: 'Written for newcomers' },
  expert: { label: 'In depth', long: 'For researchers and builders' },
  everyone: { label: 'For everyone', long: 'For everyone' },
};

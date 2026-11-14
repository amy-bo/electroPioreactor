# electropioreactor.org

The source of the home site at <https://electropioreactor.org>: the interactive 3D vial on the
home page, plus plain-language and in-depth pages about the electroPioreactor. The assembly
instructions are a separate site, the [Assembly Video Guide](https://docs.electropioreactor.org/AEP/)
(built from `site/` and `docs/`); this site links into it and never copies it.

## Build

```sh
cd landing && npm install && cd ..   # once: marked + gray-matter
node landing/build.mjs               # writes landing/dist/
npx serve landing/dist               # preview at http://localhost:3000
```

Options: `--viewer <file>` (another viewer build), `--no-strict` (report broken links and missing
`repo:` paths as warnings instead of failing), `--examples` (also build `content/_*.md`).

The home page wraps `Components/Vial Cap/render/renders/Vial Cap viewer.html` (made by
`Components/Vial Cap/render/build-viewer.mjs`). Rebuild the viewer first if the 3D model changed.
The 14 numbered hotspots and the "How it works" panel take their wording from
`Components/Vial Cap/render/callouts.mjs`, the same file the A4 vial poster uses; their 3D anchor
points are worked out in the browser from the part meshes (`assets/home.js`, `anchorPoints`).

## Deploy

Cloudflare Pages, Direct Upload, project `electropioreactor-home`. From the repo root on a machine
logged in to Wrangler:

```sh
node landing/build.mjs
npx wrangler pages deploy landing/dist --project-name electropioreactor-home --branch main --commit-dirty=true
```

`landing/dist/` and `landing/node_modules/` are not committed.

## Content pages

Each `landing/content/<slug>.md` becomes `/<slug>/`. Files starting with `_` are skipped.

```markdown
---
title: Short page title
description: One sentence, used for <meta description> and the cards on the home page.
section: learn | build | research | about
audience: newcomer | expert | everyone
order: 10
---
Markdown body (GitHub-flavoured). Start at `##`; the title is the page's only h1.
```

- **Sections.** `/learn/`, `/build/`, `/research/` and `/about/` list their pages by `order`.
  A content page whose slug is a section name (`research.md`, `about.md`) is that section's page,
  and gets the list of the section's other pages added at the end.
- **Home page cards.** `learn` pages appear under "New to this?"; `build` and `research` pages under
  "For researchers and builders".
- **Links.** Other pages: `/slug/` (the build fails on a link to a page that does not exist).
  Repository files: `repo:Media/MediaFormulation.md` or `repo:Components/Vial%20Cap/`, rewritten to
  GitHub on the branch set in `templates/site.mjs` (`BRANCH`); the build fails if the path does not
  exist. The assembly guide: full `https://docs.electropioreactor.org/AEP/...` URLs.
- **Callouts.** A blockquote whose first words are `**Note:**`, `**Tip:**`, `**Safety:**` or
  `**Expert:**` becomes a coloured box.
- **Images.** Put them in `landing/content/img/` and write `![Alt text](/img/name.png)`. Keep each
  under about 300 KB.
- **Notes for editors.** HTML comments (`<!-- source: ... -->`) are removed from the output.
- Pages with three or more `##` headings get a table of contents; every page gets previous/next
  links within its section.

## Files

| Path | What |
|---|---|
| `build.mjs` | the generator |
| `templates/site.mjs` | site constants: URLs, branch, sections, audiences |
| `templates/layout.mjs` | `<head>`, header, footer |
| `templates/page.mjs` | content, section and 404 pages |
| `templates/home.mjs` | home hero overlay, hotspots panel, sections below the hero |
| `assets/` | CSS, JS and the AMYBO logo, copied to `dist/assets/` |
| `static/` | copied to the site root as is (`og.jpg`, the share image) |
| `content/` | the pages (owned by their authors) |

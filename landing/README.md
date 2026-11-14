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

All the wording is Markdown in `landing/content/`. There are five files, one per page:

| File | Page |
|---|---|
| `home.md` | `/`: the title, strapline, button and intro beside the 3D model, and the text below the page cards |
| `what-it-is.md` | `/what-it-is/` |
| `get-one.md` | `/get-one/` |
| `research.md` | `/research/` |
| `about.md` | `/about/` |

To edit with a live preview, run `node landing/build.mjs --watch` from the repo root and open
<http://localhost:4321>. Save a file and the page reloads.

```markdown
---
title: Short page title (also its name in the menu)
description: One sentence, used under the title, for <meta description> and on the home page card.
order: 10
---
Markdown body (GitHub-flavoured). Start at `##`; the title is the page's only h1.
```

- **Menu.** Every page except `home.md` is in the menu, sorted by `order`. A new `<slug>.md` becomes
  `/<slug>/` and appears there. Files starting with `_` are skipped.
- **Home.** `home.md` also takes `strapline`, `button` and `pages_heading`. Its first paragraph is the
  intro beside the 3D model; anything after it is shown below the page cards.
- **Old addresses.** The site had 17 pages until November 2026. Their addresses redirect to the page
  that replaced them (`MOVED` in `build.mjs`).
- **Links.** Other pages: `/slug/` (the build fails on a link to a page that does not exist).
  Repository files: `repo:Media/MediaFormulation.md` or `repo:Components/Vial%20Cap/`, rewritten to
  GitHub on the branch set in `templates/site.mjs` (`BRANCH`); the build fails if the path does not
  exist. The assembly guide: full `https://docs.electropioreactor.org/AEP/...` URLs.
- **Callouts.** A blockquote whose first words are `**Note:**`, `**Tip:**`, `**Safety:**` or
  `**Expert:**` becomes a coloured box.
- **Images.** Put them in `landing/content/img/` and write `![Alt text](/img/name.png)`. Keep each
  under about 300 KB.
- **Notes for editors.** HTML comments (`<!-- source: ... -->`) are removed from the output.
- Every page gets previous/next links to its neighbours in the menu.

## Files

| Path | What |
|---|---|
| `build.mjs` | the generator |
| `watch.mjs` | `--watch`: rebuild on save, local preview server, browser reload |
| `templates/site.mjs` | site constants: URLs, branch |
| `templates/layout.mjs` | `<head>`, header, footer |
| `templates/page.mjs` | content and 404 pages |
| `templates/home.mjs` | home hero overlay, hotspots panel, sections below the hero |
| `assets/` | CSS, JS and the AMYBO logo, copied to `dist/assets/` |
| `static/` | copied to the site root as is (`og.jpg`, the share image) |
| `content/` | the pages (owned by their authors) |

# AEP0.2 presentation

One offline HTML file, `AEP0.2 presentation.html`: the amybo.org opening pages, then the 3D build of MEP, AEP0.1, AEP0.1.1 and AEP0.2. Open it in a browser; no internet needed.

**Keys:** ← / → step, PageUp / PageDown jump between pages (each reactor version lands on its finished state), Home front page, M or the AMYBO logo for the page menu, F full screen, B black screen. Click the version tag to toggle the turntable. On a phone, tap right for next, left for back.

**Cameras:** E enters camera edit; S saves this step's view (Shift+S its second view), X clears it, C copies all as JSON. Paste the JSON into `cams.json` and rebuild to bake them in.

**Build:** `npm ci && node build.mjs`. It reads the AEP0.2 parts from `../Components/Vial Cap/render/renders/Vial Cap viewer.html` and the template next to it, the earlier-version parts from `stl/`, and the logo and forest image from `assets/`.

`shot.sh <step> [WxH]` screenshots one step with vibe-shot (test mode: no shadows or bloom).

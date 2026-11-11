# AEP0.2 presentation

One offline HTML file, `AEP0.2 presentation.html`: the amybo.org opening pages, then the 3D build of MEP, AEP0.1, AEP0.1.1 and AEP0.2. Open it in a browser; no internet needed.

**Keys:** ← / → step, PageUp / PageDown jump between pages (each reactor version lands on its finished state), Home front page, M or the AMYBO logo for the page menu, F full screen, B black screen. Click the version tag to toggle the turntable. On a phone, tap right for next, left for back.

**Cameras:** E enters camera edit; S saves this step's view (Shift+S its second view), X clears it, C copies all as JSON. Paste the JSON into `cams.json` and rebuild to bake them in.

**Build:** `npm ci && node build.mjs`. It reads the AEP0.2 parts from `../Components/Vial Cap/render/renders/Vial Cap viewer.html` and the template next to it, the earlier-version parts from `stl/`, and the logo and forest image from `assets/`.

`shot.sh <step> [WxH]` screenshots one step with vibe-shot (test mode: no shadows or bloom).

## Photo steps

Images in `assets/photos/` are shown full screen over the paused 3D scene.

- After the AEP0.2 CO₂ step: `cylinder-valve`, `blanking-plug` and `thread-sealant` (from the AMYBO Pitch 033 deck).
- Before the final run: `pi-zero2w` grows into `pi5` at true relative size (65 mm to 87.5 mm wide, top-left aligned), then `plugin` (the electroPioreactor job settings) and `plugins-offline` (the plugins installed from the card bundle on a unit without internet).
- A key with no file has no step.

Pi photos from Wikimedia Commons, CC BY 4.0, credited on the slide: [Raspberry Pi Zero 2 W](https://commons.wikimedia.org/wiki/File:Raspberry_Pi_Zero_2_W_--_2024_--_0008.jpg) by Anil Öztas, [Raspberry Pi 5](https://commons.wikimedia.org/wiki/File:Raspberry_Pi_5.jpg) by Simon Waldherr. Both are cropped to the board.

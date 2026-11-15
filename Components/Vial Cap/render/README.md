# Vial Cap render

`viewer.template.html` is an interactive, self-contained 3D viewer for the vial cap assembly. `build-viewer.mjs` embeds one gzipped STL per material group into it, producing a single HTML file you can open or share.

On the Mac (needs OpenSCAD and BOSL2 installed; Node 18 or newer):

```
./export-parts.sh ./parts                       # one binary STL per component (parallel; fails loudly)
node build-viewer.mjs ./parts vial-cap.html     # optional 3rd arg: template path
```

STL files in `extra-parts/` (the Pioreactor XR optics boards, which are not in the OpenSCAD model) are embedded as well; the viewer places one at each photodiode position. The CO₂ line, luer fittings and gas filters are drawn by the viewer itself (`setupFittings` in the template).

`OPENSCAD=/path/to/binary` overrides the binary (the macOS app path is tried automatically if `openscad` is not on PATH). `JOBS=n` sets parallelism. The build warns if the HTML exceeds 15 MB.

You can also open `../Vial Cap render.scad` directly in OpenSCAD and press F5 for a coloured preview.

# Vial Cap render

`viewer.template.html` is an interactive, self-contained 3D viewer for the vial cap assembly. `build-viewer.mjs` embeds one gzipped STL per material group into it, producing a single HTML file you can open or share.

On the Mac (needs OpenSCAD and BOSL2 installed; Node 18 or newer):

```
./export-parts.sh ./parts                       # one binary STL per component (parallel; fails loudly)
node build-viewer.mjs ./parts vial-cap.html     # optional 3rd arg: template path
```

`OPENSCAD=/path/to/binary` overrides the binary (the macOS app path is tried automatically if `openscad` is not on PATH). `JOBS=n` sets parallelism. The build warns if the HTML exceeds 15 MB.

You can also open `../Vial Cap render.scad` directly in OpenSCAD and press F5 for a coloured preview.

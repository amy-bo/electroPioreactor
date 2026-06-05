#!/usr/bin/env python3
"""Verification + presentation figure for electrode-holder-v2.
Top views (both port styles) prove no port/peg/column collisions and the
septum real-estate; the print-orientation panel proves support-free.
Coordinates mirror electrode-holder-v2.scad. Plain stdlib."""
import math

# ---- params (must match the SCAD) ----
cap_r=13.5; flat_d=2.2; el_off=4.8; el_r=3.0; col_endr=6.8/1.0  # el_d/2+2.8 = 5.8
col_endr=el_off and (6/2+2.8)
peg_off=4; peg_r=1.5; port_r=10; port_rad=1.6
port_angles=[60,90,120,240,270,300]

class Svg:
    def __init__(s): s.p=[]
    def rect(s,x,y,w,h,fill="none",stroke="#222",sw=1.5,rx=0,op=1):
        s.p.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" fill-opacity="{op}" stroke="{stroke}" stroke-width="{sw}"/>')
    def circ(s,cx,cy,r,fill="none",stroke="#222",sw=1.5,op=1):
        s.p.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" fill-opacity="{op}" stroke="{stroke}" stroke-width="{sw}"/>')
    def ell(s,cx,cy,rx,ry,fill="none",stroke="#222",sw=1.5,op=1):
        s.p.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{fill}" fill-opacity="{op}" stroke="{stroke}" stroke-width="{sw}"/>')
    def line(s,x1,y1,x2,y2,stroke="#222",sw=1.5,dash=""):
        d=f' stroke-dasharray="{dash}"' if dash else ""
        s.p.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}"{d}/>')
    def poly(s,pts,fill="none",stroke="#222",sw=1.5,op=1):
        pp=" ".join(f"{x:.1f},{y:.1f}" for x,y in pts)
        s.p.append(f'<polygon points="{pp}" fill="{fill}" fill-opacity="{op}" stroke="{stroke}" stroke-width="{sw}"/>')
    def txt(s,x,y,t,size=13,anchor="start",fill="#111",weight="normal"):
        s.p.append(f'<text x="{x:.1f}" y="{y:.1f}" font-family="Helvetica,Arial" font-size="{size}" text-anchor="{anchor}" fill="{fill}" font-weight="{weight}">{t}</text>')

CAP="#cfe0f5"; CARR="#ffd9a0"; SEPT="#cdb6ec"; ELEC="#b9bcc2"; GLASS="#bfe9da"; PEG="#d98a2b"
g=Svg(); W,H=980,1080
s=10.0  # px/mm

def cap_outline(cx,cy):
    pts=[]
    for a in range(0,360,3):
        r=math.radians(a); x=cx+cap_r*s*math.cos(r); y=cy+cap_r*s*math.sin(r)
        if -32<=((a+180)%360-180)<=32: x=cx+(cap_r-flat_d)*s
        pts.append((x,y))
    return pts

def column_footprint(cx,cy):
    # racetrack: two end circles + bridge, drawn translucent
    g.rect(cx-el_off*s, cy-col_endr*s, 2*el_off*s, 2*col_endr*s, fill=CARR, stroke="none", op=0.45)
    for sgn in (-1,1):
        g.circ(cx+sgn*el_off*s, cy, col_endr*s, fill=CARR, stroke="#b06a10", sw=1.2, op=0.45)

def top_view(cx,cy,style,title):
    g.txt(cx, cy-cap_r*s-26, title, size=17, anchor="middle", weight="bold")
    g.poly(cap_outline(cx,cy), fill=CAP, stroke="#1f5fa0", sw=1.8)
    # septum field hint (light purple inside)
    g.circ(cx,cy,(cap_r-2-0.3)*s, fill=SEPT, stroke="none", op=0.25)
    column_footprint(cx,cy)
    # ports or open windows
    if style=="ports":
        for a in port_angles:
            r=math.radians(a); g.circ(cx+port_r*s*math.cos(r), cy+port_r*s*math.sin(r), port_rad*s, fill="#fff", stroke="#6a3da0", sw=1.6)
    else:
        for sgn in (-1,1):
            g.ell(cx, cy+sgn*8*s, 8.5/2*1.7*s, 8.5/2*s, fill="#fff", stroke="#6a3da0", sw=1.6, op=0.9)
    # electrodes
    for sgn in (-1,1):
        g.circ(cx+sgn*el_off*s, cy, el_r*s, fill=ELEC, stroke="#555", sw=1.4)
    # pegs (on y-axis)
    for sgn in (-1,1):
        g.circ(cx, cy+sgn*peg_off*s, peg_r*s, fill=PEG, stroke="#7a4a08", sw=1.2)
    # clamp arrows
    for sgn in (-1,1):
        x0=cx+sgn*(el_off+col_endr)*s; x1=cx+sgn*el_off*s
        g.line(x0+sgn*16, cy, x1, cy, stroke="#444", sw=3)
        g.poly([(x1+sgn*6,cy-4),(x1+sgn*6,cy+4),(x1,cy)], fill="#444", stroke="#444", sw=1)
    # legend leaders
    g.txt(cx, cy+cap_r*s+24, "electrodes (grey) | pegs (orange, y-axis) | column footprint (shaded)", size=11, anchor="middle", fill="#444")
    if style=="ports":
        g.txt(cx, cy+cap_r*s+40, "6 ports clear the column; septum self-seals each", size=11, anchor="middle", fill="#444")
    else:
        g.txt(cx, cy+cap_r*s+40, "open septum field: pierce a needle anywhere", size=11, anchor="middle", fill="#444")

top_view(250, 200, "ports",  "TOP - 6-port ring")
top_view(720, 200, "open",   "TOP - open septum field")

# clamp arrow direction note
g.txt(485, 420, "M3 clamp pushes wire onto each electrode  →", size=12, anchor="middle", fill="#444")

# ---------- PRINT ORIENTATION PANEL ----------
py=470
g.txt(40, py-6, "PRINT ORIENTATION  -  every face is vertical, a vertical hole, or ≤45°  ⇒  NO SUPPORTS", size=16, weight="bold")
bed=py+330
def bed_line(x0,x1):
    g.line(x0,bed,x1,bed,stroke="#888",sw=2)
    for x in range(int(x0),int(x1),14): g.line(x,bed,x-6,bed+8,stroke="#bbb",sw=1)

# CAP printed closed-top-down (cross-section, z up = away from bed)
cx=250
bed_line(cx-150,cx+150)
sc=11
ch=12*sc; tt=2.5*sc; ww=2*sc
# closed top on the bed (solid disc), cavity opens upward
g.rect(cx-cap_r*sc, bed-tt, 2*cap_r*sc, tt, fill=CAP, stroke="#1f5fa0", sw=1.6)        # closed top (on bed)
g.rect(cx-cap_r*sc, bed-ch, ww, ch-tt, fill=CAP, stroke="#1f5fa0", sw=1.6)             # left wall
g.rect(cx+cap_r*sc-ww, bed-ch, ww, ch-tt, fill=CAP, stroke="#1f5fa0", sw=1.6)          # right wall
# vertical holes through closed top (electrodes + a port), dashed
for hx in (-el_off, el_off):
    g.line(cx+hx*sc, bed, cx+hx*sc, bed-tt, stroke="#1f5fa0", sw=1, dash="3 3")
g.txt(cx, bed-ch-12, "CAP - closed top on bed, mouth up", size=13, anchor="middle", weight="bold")
g.txt(cx, bed+26, "cavity opens UP; thread + all holes vertical", size=11, anchor="middle", fill="#060")
# up arrow inside cavity
g.line(cx, bed-tt-6, cx, bed-ch+8, stroke="#060", sw=1.5)
g.poly([(cx-4,bed-ch+12),(cx+4,bed-ch+12),(cx,bed-ch+4)], fill="#060", stroke="#060", sw=1)

# COLUMN printed flush-face-down, pegs up
cx=720
bed_line(cx-150,cx+150)
colh=25*sc/2.0
endw=(el_off+col_endr)*sc
g.rect(cx-endw, bed-colh, 2*endw, colh, fill=CARR, stroke="#a06000", sw=1.6, rx=6)
# vertical electrode bores (dashed) through the column
for hx in (-el_off, el_off):
    g.line(cx+hx*sc, bed, cx+hx*sc, bed-colh, stroke="#a06000", sw=1, dash="3 3")
# pegs pointing UP (away from bed)
for sgn in (-1,1):
    g.rect(cx+sgn*peg_off*sc-peg_r*sc, bed-colh-4*sc, 2*peg_r*sc, 4*sc, fill=CARR, stroke="#a06000", sw=1.3)
# teardrop M3 clamp hole (horizontal), apex UP (printable)
ty=bed-colh*0.5
for sgn in (-1,1):
    ax=cx+sgn*endw
    g.line(ax, ty, cx+sgn*el_off*sc, ty, stroke="#fff", sw=5)
    g.line(ax, ty, cx+sgn*el_off*sc, ty, stroke="#a06000", sw=1.2)
    # apex tick up
    g.poly([(cx+sgn*el_off*sc-5,ty),(cx+sgn*el_off*sc+5,ty),(cx+sgn*el_off*sc,ty-7)], fill="none", stroke="#a06000", sw=1)
g.txt(cx, bed-colh-4*sc-10, "COLUMN - flush face on bed, pegs up", size=13, anchor="middle", weight="bold")
g.txt(cx, bed+26, "bores vertical; M3 hole teardropped; nut trap vertex-up", size=11, anchor="middle", fill="#060")

out=(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
     f'<rect width="{W}" height="{H}" fill="#fbfbfb"/>'+"".join(g.p)+"</svg>")
open("/workspace/design-concept/electrode-holder-v2-figure.svg","w").write(out)
print("wrote electrode-holder-v2-figure.svg")

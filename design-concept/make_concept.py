#!/usr/bin/env python3
"""Throwaway concept drawing for the electrode-holder redesign.
Generates a labelled SVG so Martin can SEE the constraint scheme.
Not the real part - schematic, roughly to scale. Plain stdlib only.
"""

S = 7.0  # px per mm

def mm(v): return v * S

# ---- tiny SVG helpers -------------------------------------------------
class Svg:
    def __init__(self):
        self.parts = []
    def rect(self, x, y, w, h, fill="none", stroke="#222", sw=1.5, rx=0, op=1.0):
        self.parts.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'rx="{rx}" fill="{fill}" fill-opacity="{op}" stroke="{stroke}" stroke-width="{sw}"/>')
    def circ(self, cx, cy, r, fill="none", stroke="#222", sw=1.5):
        self.parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" '
                          f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    def ell(self, cx, cy, rx, ry, fill="none", stroke="#222", sw=1.5, op=1.0):
        self.parts.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" '
                          f'fill="{fill}" fill-opacity="{op}" stroke="{stroke}" stroke-width="{sw}"/>')
    def line(self, x1, y1, x2, y2, stroke="#222", sw=1.5, dash=""):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                          f'stroke="{stroke}" stroke-width="{sw}"{d}/>')
    def poly(self, pts, fill="none", stroke="#222", sw=1.5, op=1.0):
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        self.parts.append(f'<polygon points="{p}" fill="{fill}" fill-opacity="{op}" '
                          f'stroke="{stroke}" stroke-width="{sw}"/>')
    def text(self, x, y, s, size=13, anchor="start", fill="#111", weight="normal"):
        self.parts.append(f'<text x="{x:.1f}" y="{y:.1f}" font-family="Helvetica,Arial" '
                          f'font-size="{size}" text-anchor="{anchor}" fill="{fill}" '
                          f'font-weight="{weight}">{s}</text>')
    def leader(self, x, y, tx, ty, s, size=13, anchor="start", color="#b00"):
        # dot at feature, line to label
        self.circ(x, y, 2.0, fill=color, stroke=color, sw=1)
        self.line(x, y, tx, ty, stroke=color, sw=1.0)
        ax = tx + (4 if anchor == "start" else -4)
        self.text(ax, ty + 4, s, size=size, anchor=anchor, fill="#111")

# colours
CAP   = "#cfe3f7"
CARR  = "#ffe2b8"
SEPT  = "#d9c2ef"
ELEC  = "#b9bcc2"
GLASS = "#cdeee4"

svg = Svg()
W, H = 1180, 1180

# ============================================================
# PANEL 1  -  SECTION (cut through both electrodes), in-use (mouth down)
# ============================================================
ox, oy = 70, 70
svg.text(ox, oy-18, "1 - SECTION through both electrodes  (in use, vial below)", size=18, weight="bold")

cx = ox + mm(60)                 # centre line x
off = mm(4.8)                    # electrode offset
er  = mm(3.0)                    # electrode radius (6mm dia)
bore_gap = mm(0.4)               # clearance shown

# vertical datums (z, measured downward on screen)
y_eltop   = oy + mm(2)           # top of electrodes (wires)
y_ts_top  = oy + mm(16)          # top stop top face  = "push flush to here"
y_ts_bot  = y_ts_top + mm(12)    # top stop bottom
y_cap_top = y_ts_bot + mm(13)    # standoff = 13mm
y_cap_bot = y_cap_top + mm(12)   # cap height 12
y_tip     = y_cap_bot + mm(34)   # electrode protrudes g into vial

# centre line
svg.line(cx, oy, cx, y_tip+mm(8), stroke="#999", sw=0.8, dash="6 5")

# --- electrodes (drawn first, behind) ---
for sgn in (-1, 1):
    ex = cx + sgn*off
    svg.rect(ex-er, y_eltop, 2*er, y_tip-y_eltop, fill=ELEC, stroke="#555", sw=1.2)
# wires
svg.line(cx-off, y_eltop, cx-off-mm(5), y_eltop-mm(8), stroke="#111", sw=3)
svg.line(cx+off, y_eltop, cx+off+mm(5), y_eltop-mm(8), stroke="#c00", sw=3)

# --- TOP STOP block ---
ts_halfw = off + er + mm(5)
svg.rect(cx-ts_halfw, y_ts_top, 2*ts_halfw, y_ts_bot-y_ts_top, fill=CARR, stroke="#a06000", sw=1.6)
# upper bores (snug) shown as clearance slots around electrodes
for sgn in (-1, 1):
    ex = cx + sgn*off
    svg.rect(ex-er-bore_gap, y_ts_top, 2*(er+bore_gap), y_ts_bot-y_ts_top, fill="none", stroke="#a06000", sw=0.8, op=1)
# M3 clamp bolts (horizontal) - pinch wire+electrode
for sgn in (-1, 1):
    ex = cx + sgn*off
    bx0 = cx - ts_halfw if sgn < 0 else cx + ts_halfw
    bx1 = ex - sgn*er
    svg.line(bx0, (y_ts_top+y_ts_bot)/2, bx1, (y_ts_top+y_ts_bot)/2, stroke="#444", sw=4)
    # bolt head
    hx = cx - ts_halfw - mm(2) if sgn < 0 else cx + ts_halfw + mm(2)
    svg.circ(hx, (y_ts_top+y_ts_bot)/2, mm(1.8), fill="#777", stroke="#333", sw=1)

# --- STANDOFF posts (vertical) ---
for sgn in (-1, 1):
    px = cx + sgn*(ts_halfw - mm(2))
    svg.rect(px-mm(1.5), y_ts_bot, mm(3), y_cap_top-y_ts_bot, fill=CARR, stroke="#a06000", sw=1.2)

# --- CAP ---
cap_halfw = mm(13.5)
svg.rect(cx-cap_halfw, y_cap_top, 2*cap_halfw, y_cap_bot-y_cap_top, fill=CAP, stroke="#1f5fa0", sw=1.6)
# thread hint (sawtooth on inner walls)
for i in range(4):
    yy = y_cap_top+mm(3)+i*mm(2)
    svg.line(cx-cap_halfw+mm(1), yy, cx-cap_halfw+mm(3), yy+mm(1), stroke="#1f5fa0", sw=1)
    svg.line(cx+cap_halfw-mm(1), yy, cx+cap_halfw-mm(3), yy+mm(1), stroke="#1f5fa0", sw=1)
# registration BOSSES (raised tubes around electrode exits, sticking UP from cap)
for sgn in (-1, 1):
    ex = cx + sgn*off
    svg.rect(ex-er-mm(1.6), y_cap_top-mm(5), 2*(er+mm(1.6)), mm(5), fill="#9fc6ee", stroke="#1f5fa0", sw=1.2)
    # cap guide bore (BEARING 1) through cap ceiling
    svg.rect(ex-er-bore_gap, y_cap_top-mm(5), 2*(er+bore_gap), mm(7), fill="none", stroke="#1f5fa0", sw=0.8)
# carriage lower bore slips OVER boss -> registration (show collar)
for sgn in (-1, 1):
    ex = cx + sgn*off
    svg.rect(ex-er-mm(2.4), y_cap_top-mm(5), 2*(er+mm(2.4)), mm(5), fill="none", stroke="#a06000", sw=1.4)

# --- SEPTUM disc inside cap, against ceiling ---
sept_y = y_cap_bot-mm(2)-mm(2)
svg.rect(cx-cap_halfw+mm(2.5), sept_y, 2*(cap_halfw-mm(2.5)), mm(2), fill=SEPT, stroke="#6a3da0", sw=1.4)

# --- glass vial rim pushing up ---
svg.rect(cx-cap_halfw+mm(2), y_cap_bot, 2*(cap_halfw-mm(2)), mm(7), fill=GLASS, stroke="#2a8f72", sw=1.4)
svg.line(cx-cap_halfw+mm(2), y_cap_bot+mm(7), cx-cap_halfw+mm(2), y_tip+mm(8), stroke="#2a8f72", sw=1.4)
svg.line(cx+cap_halfw-mm(2), y_cap_bot+mm(7), cx+cap_halfw-mm(2), y_tip+mm(8), stroke="#2a8f72", sw=1.4)
svg.text(cx, y_tip+mm(7), "glass vial", size=12, anchor="middle", fill="#2a8f72")

# --- labels (right side) ---
LX = cx + cap_halfw + mm(16)
svg.leader(cx+off+er, (y_ts_top+y_ts_bot)/2, LX, y_ts_top+mm(2),
           "M3 clamp: bolt pushes wire onto electrode", size=13)
svg.leader(cx+off+er+bore_gap, y_ts_top+mm(3), LX, y_ts_top-mm(6),
           "BEARING 2  (upper snug bore)", size=13)
svg.leader(cx+off+er+mm(2.4), y_cap_top-mm(3), LX, y_cap_top-mm(6),
           "registration BOSS + carriage collar (slip-fit, keyed)", size=13)
svg.leader(cx+off+er+bore_gap, y_cap_top-mm(1), LX, y_cap_top+mm(8),
           "BEARING 1  (cap guide bore)", size=13)
svg.leader(cx+cap_halfw-mm(4), sept_y+mm(1), LX, sept_y+mm(2),
           "SEPTUM - seals only, grips nothing", size=13)
svg.leader(cx+cap_halfw-mm(6), y_cap_bot+mm(3), LX, y_cap_bot+mm(8),
           "vial rim crushes septum to cap ceiling = seal", size=13)

# --- left side: the two key annotations ---
LXL = cx - cap_halfw - mm(16)
# standoff dimension
svg.line(cx-ts_halfw-mm(6), y_ts_bot, cx-ts_halfw-mm(6), y_cap_top, stroke="#06c", sw=1.2)
svg.line(cx-ts_halfw-mm(8), y_ts_bot, cx-ts_halfw-mm(4), y_ts_bot, stroke="#06c", sw=1.2)
svg.line(cx-ts_halfw-mm(8), y_cap_top, cx-ts_halfw-mm(4), y_cap_top, stroke="#06c", sw=1.2)
svg.text(cx-ts_halfw-mm(9), (y_ts_bot+y_cap_top)/2, "standoff =", size=12, anchor="end", fill="#06c")
svg.text(cx-ts_halfw-mm(9), (y_ts_bot+y_cap_top)/2+14, "L - cap_h - g", size=12, anchor="end", fill="#06c")
# flush face
svg.line(cx-off, y_ts_top, cx-ts_halfw-mm(2), y_ts_top, stroke="#b00", sw=1.0)
svg.text(cx-ts_halfw-mm(3), y_ts_top+3, "push electrode flush to this face", size=12, anchor="end", fill="#111")
# the punchline
svg.text(LXL-mm(2), y_cap_bot+mm(20),
         "Both bores tied to the cap", size=14, anchor="end", weight="bold", fill="#060")
svg.text(LXL-mm(2), y_cap_bot+mm(20)+18,
         "through the posts:", size=14, anchor="end", weight="bold", fill="#060")
svg.text(LXL-mm(2), y_cap_bot+mm(20)+40,
         "no tilt, no slide. Clamp", size=14, anchor="end", fill="#060")
svg.text(LXL-mm(2), y_cap_bot+mm(20)+58,
         "kills the last DOF.", size=14, anchor="end", fill="#060")

# ============================================================
# PANEL 2  -  TOP PLAN  (looking down on the cap)
# ============================================================
p2x, p2y = 70, 760
svg.text(p2x, p2y-14, "2 - TOP VIEW of cap (poka-yoke + layout)", size=18, weight="bold")
pcx, pcy = p2x + mm(20), p2y + mm(20)
R = mm(13.5)
# cap circle with a flat (poka-yoke) on one side
import math
pts = []
for a in range(0, 360, 4):
    rad = math.radians(a)
    x = pcx + R*math.cos(rad)
    y = pcy + R*math.sin(rad)
    # flatten the right side between -35 and +35 deg
    if -35 <= ((a+180)%360-180) <= 35:
        x = pcx + (R-mm(2.2))
    pts.append((x, y))
svg.poly(pts, fill=CAP, stroke="#1f5fa0", sw=1.6)
# electrodes
for sgn in (-1, 1):
    svg.circ(pcx, pcy + sgn*off, er, fill=ELEC, stroke="#555", sw=1.4)
# sample/needle zone (centre)
svg.circ(pcx, pcy, mm(2.2), fill=SEPT, stroke="#6a3da0", sw=1.0)
svg.text(pcx, pcy+4, "needle", size=9, anchor="middle", fill="#6a3da0")
# bolt directions
for sgn in (-1, 1):
    svg.line(pcx+sgn*(R+mm(6)), pcy+sgn*off, pcx+sgn*er, pcy+sgn*off, stroke="#444", sw=3)
svg.leader(pcx+R-mm(1), pcy, pcx+R+mm(10), pcy-mm(8), "poka-yoke flat keys rotation", size=12)
svg.leader(pcx, pcy-off, pcx+R+mm(10), pcy+mm(10), "electrode ports (x2)", size=12)

# ============================================================
# PANEL 3  -  EXPLODED  (how the parts stack)
# ============================================================
p3x, p3y = 560, 720
svg.text(p3x, p3y-14, "3 - EXPLODED (assembly order)", size=18, weight="bold")
ecx = p3x + mm(28)
def disc(cy, rx, ry, fill, label, sw=1.6, stroke="#333", body=0):
    svg.ell(ecx, cy, rx, ry, fill=fill, stroke=stroke, sw=sw)
    if body:
        svg.rect(ecx-rx, cy, 2*rx, body, fill=fill, stroke=stroke, sw=sw)
        svg.ell(ecx, cy+body, rx, ry, fill=fill, stroke=stroke, sw=sw)
    svg.text(ecx+rx+12, cy+4, label, size=13)

# carriage on top
cy = p3y + mm(6)
svg.rect(ecx-mm(13), cy, mm(26), mm(10), fill=CARR, stroke="#a06000", sw=1.6, rx=6)
for sgn in (-1, 1):
    svg.circ(ecx+sgn*off, cy+mm(5), er+1, fill="#fff", stroke="#a06000", sw=1.2)
svg.text(ecx+mm(13)+12, cy+mm(6), "CARRIAGE  (top stop + posts + clamp)", size=13)
# posts hanging down (drawn as two legs)
for sgn in (-1,1):
    svg.rect(ecx+sgn*(mm(11))-mm(1.5), cy+mm(10), mm(3), mm(8), fill=CARR, stroke="#a06000", sw=1.0)

# electrodes
ey = cy + mm(26)
for sgn in (-1, 1):
    svg.rect(ecx+sgn*off-er, ey, 2*er, mm(34), fill=ELEC, stroke="#555", sw=1.2)
svg.text(ecx+off+er+14, ey+mm(10), "electrodes", size=13)
svg.line(ecx, cy+mm(19), ecx, ey-2, stroke="#888", sw=1.0, dash="4 4")

# septum disc
sy = ey + mm(40)
disc(sy, mm(11), mm(3.2), SEPT, "SEPTUM disc (1-3mm silicone)")
svg.line(ecx, ey+mm(34)+2, ecx, sy-mm(3.2), stroke="#888", sw=1.0, dash="4 4")

# cap (cylinder)
capy = sy + mm(12)
svg.ell(ecx, capy, mm(13.5), mm(4), fill=CAP, stroke="#1f5fa0", sw=1.6)
svg.rect(ecx-mm(13.5), capy, mm(27), mm(12), fill=CAP, stroke="#1f5fa0", sw=1.6)
svg.ell(ecx, capy+mm(12), mm(13.5), mm(4), fill="#bcd8f4", stroke="#1f5fa0", sw=1.6)
# bosses on cap top
for sgn in (-1, 1):
    svg.ell(ecx+sgn*off, capy, er+mm(1.6), mm(1.6), fill="#9fc6ee", stroke="#1f5fa0", sw=1.2)
svg.text(ecx+mm(13.5)+12, capy+mm(6), "CAP (thread + septum seat + bosses)", size=13)
svg.line(ecx, sy+mm(3.2), ecx, capy-mm(4), stroke="#888", sw=1.0, dash="4 4")

# big down arrows
for yy in (cy+mm(21), ey+mm(36), sy+mm(6)):
    svg.line(ecx-mm(20), yy, ecx-mm(20), yy+mm(8), stroke="#060", sw=2)
    svg.poly([(ecx-mm(20)-4, yy+mm(8)-1),(ecx-mm(20)+4, yy+mm(8)-1),(ecx-mm(20), yy+mm(8)+5)],
             fill="#060", stroke="#060", sw=1)

out = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
       f'viewBox="0 0 {W} {H}"><rect width="{W}" height="{H}" fill="#fbfbfb"/>'
       + "".join(svg.parts) + "</svg>")
with open("/workspace/design-concept/electrode-holder-concept.svg", "w") as f:
    f.write(out)
print("wrote electrode-holder-concept.svg", len(out), "bytes")

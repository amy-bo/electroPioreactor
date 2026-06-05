#!/usr/bin/env python3
"""Cross-sections of the 1-piece OPEN holder, to confirm the shape.
USE orientation (z up): cap at the bottom, top stop (racetrack) at the top.
Plain stdlib SVG."""
cap_R=13.5; cap_h=12.3; rt_x=14.5; rt_y=5.0; H_top=37.0; el_off=4.8; el_d=6
join_z=cap_h+(cap_R-rt_y)        # 45 deg ramp from cap rim meets racetrack here (~20.8)

class Svg:
    def __init__(s): s.p=[]
    def rect(s,x,y,w,h,fill="none",stroke="#222",sw=1.5,rx=0,op=1):
        s.p.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" fill-opacity="{op}" stroke="{stroke}" stroke-width="{sw}"/>')
    def line(s,x1,y1,x2,y2,stroke="#222",sw=1.5,dash=""):
        d=f' stroke-dasharray="{dash}"' if dash else ""
        s.p.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}"{d}/>')
    def poly(s,pts,fill="none",stroke="#222",sw=1.5,op=1):
        pp=" ".join(f"{x:.1f},{y:.1f}" for x,y in pts)
        s.p.append(f'<polygon points="{pp}" fill="{fill}" fill-opacity="{op}" stroke="{stroke}" stroke-width="{sw}"/>')
    def txt(s,x,y,t,size=13,anchor="start",fill="#111",weight="normal"):
        s.p.append(f'<text x="{x:.1f}" y="{y:.1f}" font-family="Helvetica,Arial" font-size="{size}" text-anchor="{anchor}" fill="{fill}" font-weight="{weight}">{t}</text>')

CAP="#cfe0f5"; CARR="#ffd9a0"; ELEC="#b9bcc2"; SEPT="#cdb6ec"; GLASS="#bfe9da"
g=Svg(); W,H=1000,640; s=11.0

def Z(base,z): return base - z*s          # use z up -> screen

# ---------- FRONT view (Y-Z, looking along the electrode axis) ----------
cx=255; base=560
g.txt(cx, 70, "FRONT view  (the 45° rise)", size=16, anchor="middle", weight="bold")
g.line(cx-160,base,cx+170,base,stroke="#ccc",sw=1)
# cap walls + septum
g.rect(cx-cap_R*s, Z(base,cap_h), 2*cap_R*s, cap_h*s, fill=CAP, stroke="#1f5fa0", sw=1.5)
g.rect(cx-(cap_R-2)*s, Z(base,cap_h-2), 2*(cap_R-2)*s, 2*s, fill=SEPT, stroke="#6a3da0", sw=1.2)  # septum band
g.txt(cx, Z(base,cap_h-1)+4, "septum across the open neck", size=9.5, anchor="middle", fill="#6a3da0")
# poka-yoke tab (front, -Y = left)
g.rect(cx-(cap_R+3)*s, Z(base,cap_h), 3*s, cap_h*s, fill=CAP, stroke="#1f5fa0", sw=1.2)
# racetrack (narrow in Y) up to H_top
g.rect(cx-rt_y*s, Z(base,H_top), 2*rt_y*s, (H_top-cap_h)*s, fill=CARR, stroke="#a06000", sw=1.5)
# 45 deg ramps cap-rim -> racetrack (connector)
for sgn in (-1,1):
    g.poly([(cx+sgn*cap_R*s, Z(base,cap_h)),
            (cx+sgn*rt_y*s,  Z(base,join_z)),
            (cx+sgn*rt_y*s,  Z(base,cap_h))], fill=CARR, stroke="#a06000", sw=1.4)
    g.txt(cx+sgn*9.5*s, Z(base,cap_h+4.2), "45°", size=11, anchor="middle", fill="#a06000")
# electrodes project to centre
g.line(cx, Z(base,H_top), cx, Z(base,-23), stroke="#8a9099", sw=4)
g.txt(cx, Z(base,-23)-6, "electrodes", size=10, anchor="middle", fill="#555")
# needle entering at 45 deg through the open front
g.line(cx-21*s, Z(base,cap_h+8.5)-0, cx-(cap_R-3)*s, Z(base,cap_h-1), stroke="#c00", sw=2)
g.txt(cx-15*s, Z(base,cap_h+10), "needle (45° in)", size=10, anchor="middle", fill="#c00")
g.txt(cx, base+26, "low at front/back, rises at 45° to meet the racetrack part-way up", size=11, anchor="middle", fill="#444")

# ---------- SIDE view (X-Z, looking at the poka-yoke) ----------
cx=730; base=560
g.txt(cx, 70, "SIDE view  (cap meets racetrack here)", size=16, anchor="middle", weight="bold")
g.line(cx-170,base,cx+170,base,stroke="#ccc",sw=1)
# vial below
g.rect(cx-(cap_R-2)*s, Z(base,0), 2*(cap_R-2)*s, 23*s, fill=GLASS, stroke="#2a8f72", sw=1.2, op=0.5)
g.txt(cx, Z(base,-20)+4, "vial", size=10, anchor="middle", fill="#2a8f72")
# cap
g.rect(cx-cap_R*s, Z(base,cap_h), 2*cap_R*s, cap_h*s, fill=CAP, stroke="#1f5fa0", sw=1.5)
# racetrack (wide in X, slightly wider than cap) up to H_top
g.rect(cx-rt_x*s, Z(base,H_top), 2*rt_x*s, (H_top-cap_h)*s, fill=CARR, stroke="#a06000", sw=1.5)
# electrode bores / rods
for sgn in (-1,1):
    g.rect(cx+sgn*el_off*s-el_d/2*s, Z(base,H_top), el_d*s, (H_top+23)*s, fill=ELEC, stroke="#555", sw=1.2)
# clamp bolt (horizontal) near one end
g.line(cx+rt_x*s, Z(base,H_top-5), cx+el_off*s, Z(base,H_top-5), stroke="#444", sw=3)
g.txt(cx, Z(base,H_top)-8, "top stop / racetrack (bores + clamp)", size=10, anchor="middle", fill="#a06000")
g.txt(cx, base+26, "racetrack spans the cap width here, so the sides meet ~vertically", size=11, anchor="middle", fill="#444")

out=(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
     f'<rect width="{W}" height="{H}" fill="#fbfbfb"/>'+"".join(g.p)+"</svg>")
open("/workspace/design-concept/electrode-holder-1piece.svg","w").write(out)
print("wrote electrode-holder-1piece.svg")

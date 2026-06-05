#!/usr/bin/env python3
"""Verification + presentation figure for electrode-holder-v3.
Panel A: top view - poka-yoke tab + ports at the current cap's radius (in the neck).
Panel B: clamp cross-section - the corrected outside-in captive-nut stack.
Panel C: print orientation. Plain stdlib."""
import math
el_off=4.8; el_d=6; clear=0.3; cap_r=13.5
port_r=(18.7706-3.2)/2; port_rad=1.6; port_angles=[60,90,120,240,270,300]
bearing_r=el_d/2+1.8; peg_off=4; peg_r=1.5
xe=el_off+(el_d+clear)/2; t_inner=2.2; nut_t=2.7; t_outer=2.6
x_nut0=xe+t_inner; x_nut1=x_nut0+nut_t; x_out=x_nut1+t_outer; nut_af=5.7

class Svg:
    def __init__(s): s.p=[]
    def rect(s,x,y,w,h,fill="none",stroke="#222",sw=1.5,rx=0,op=1):
        s.p.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" fill-opacity="{op}" stroke="{stroke}" stroke-width="{sw}"/>')
    def circ(s,cx,cy,r,fill="none",stroke="#222",sw=1.5,op=1,dash=""):
        d=f' stroke-dasharray="{dash}"' if dash else ""
        s.p.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" fill-opacity="{op}" stroke="{stroke}" stroke-width="{sw}"{d}/>')
    def line(s,x1,y1,x2,y2,stroke="#222",sw=1.5,dash=""):
        d=f' stroke-dasharray="{dash}"' if dash else ""
        s.p.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}"{d}/>')
    def poly(s,pts,fill="none",stroke="#222",sw=1.5,op=1):
        pp=" ".join(f"{x:.1f},{y:.1f}" for x,y in pts)
        s.p.append(f'<polygon points="{pp}" fill="{fill}" fill-opacity="{op}" stroke="{stroke}" stroke-width="{sw}"/>')
    def txt(s,x,y,t,size=13,anchor="start",fill="#111",weight="normal"):
        s.p.append(f'<text x="{x:.1f}" y="{y:.1f}" font-family="Helvetica,Arial" font-size="{size}" text-anchor="{anchor}" fill="{fill}" font-weight="{weight}">{t}</text>')
    def hexagon(s,cx,cy,af,fill,stroke,sw=1.5):
        ac=af/math.cos(math.radians(30)); pts=[]
        for k in range(6):
            a=math.radians(60*k+90)  # vertex up
            pts.append((cx+ac/2*math.cos(a), cy-ac/2*math.sin(a)))
        s.poly(pts,fill=fill,stroke=stroke,sw=sw)

CAP="#cfe0f5"; CARR="#ffd9a0"; SEPT="#cdb6ec"; ELEC="#b9bcc2"; PEG="#d98a2b"; WIRE="#c0622a"; STEEL="#9aa0a8"
g=Svg(); W,H=1000,1120; s=10.0

# ---------- Panel A: TOP VIEW ----------
ax,ay=250,230
g.txt(ax,ay-cap_r*s-22,"TOP - poka-yoke tab + ports inside the neck",size=16,anchor="middle",weight="bold")
g.circ(ax,ay,cap_r*s,fill=CAP,stroke="#1f5fa0",sw=1.8)
g.circ(ax,ay+(cap_r-1)*s,4*s,fill=CAP,stroke="#1f5fa0",sw=1.8)   # poka-yoke tab (-Y is down on screen)
g.circ(ax,ay,(cap_r-2)*s,fill=SEPT,stroke="none",op=0.22)
# neck circle (where ports must stay inside)
g.circ(ax,ay,(18.7706/2)*s,fill="none",stroke="#2a8f72",sw=1.2,dash="5 4")
# column bearing + ears
g.rect(ax-el_off*s,ay-bearing_r*s,2*el_off*s,2*bearing_r*s,fill=CARR,stroke="none",op=0.5)
for sgn in (-1,1):
    g.circ(ax+sgn*el_off*s,ay,bearing_r*s,fill=CARR,stroke="#b06a10",sw=1,op=0.5)
    g.rect(ax+(sgn>0 and xe*s or -x_out*s),ay-(nut_af/2+1.6)*s,(x_out-xe)*s,(nut_af+3.2)*s,fill=CARR,stroke="#b06a10",sw=1,op=0.5)
for a in port_angles:
    r=math.radians(a); g.circ(ax+port_r*s*math.cos(r),ay-port_r*s*math.sin(r),port_rad*s,fill="#fff",stroke="#6a3da0",sw=1.5)
for sgn in (-1,1): g.circ(ax+sgn*el_off*s,ay,el_d/2*s,fill=ELEC,stroke="#555",sw=1.3)
for sgn in (-1,1): g.circ(ax,ay+sgn*peg_off*s,peg_r*s,fill=PEG,stroke="#7a4a08",sw=1.1)
g.txt(ax,ay+cap_r*s+30,"green = vial neck; ports at r=7.785 sit inside it",size=11,anchor="middle",fill="#2a8f72")
g.txt(ax,ay+cap_r*s+46,"tab keys rotation (from vial-cap-s.3mf)",size=11,anchor="middle",fill="#444")

# ---------- Panel B: CLAMP CROSS-SECTION ----------
bx,by=590,210; sc=15.5
g.txt(bx+ (el_off+x_out)/2*sc, by-70,"CLAMP - cross-section (outside  →  in)",size=16,anchor="middle",weight="bold")
axis=by
def X(xx): return bx+xx*sc
# electrode
g.circ(X(el_off),axis,el_d/2*sc,fill=ELEC,stroke="#555",sw=1.4)
# wire (between electrode and bolt)
g.circ(X(el_off+el_d/2+0.45),axis,0.9*sc,fill=WIRE,stroke="#7a3a12",sw=1.2)
# inner wall
g.rect(X(xe),axis-9*sc/2/2.0*0+ -3.2*sc, (t_inner)*sc, 6.4*sc, fill=CARR,stroke="#a06000",sw=1.5)
# outer wall
g.rect(X(x_nut1),axis-3.2*sc,(t_outer)*sc,6.4*sc,fill=CARR,stroke="#a06000",sw=1.5)
# nut pocket walls (top/bottom) + nut
g.rect(X(x_nut0),axis-3.2*sc,(nut_t)*sc,6.4*sc,fill="#fff",stroke="none")
g.hexagon(X((x_nut0+x_nut1)/2),axis,nut_af*sc,STEEL,"#444",sw=1.4)
# bolt through everything
g.line(X(el_off+el_d/2),axis,X(x_out+3),axis,stroke="#333",sw=3)
g.rect(X(x_out),axis-2.0*sc,1.6*sc,4.0*sc,fill="#777",stroke="#333",sw=1.2)  # allen head
# top insertion slot (dashed) above nut
g.line(X(x_nut0),axis-3.2*sc,X(x_nut0),axis-7*sc,stroke="#a06000",sw=1,dash="4 3")
g.line(X(x_nut1),axis-3.2*sc,X(x_nut1),axis-7*sc,stroke="#a06000",sw=1,dash="4 3")
g.txt(X((x_nut0+x_nut1)/2),axis-7.4*sc,"nut drops in here (top slot)",size=10,anchor="middle",fill="#a06000")
# labels
def lab(xx,t,dy):
    g.line(X(xx),axis+3.2*sc,X(xx),axis+3.2*sc+dy,stroke="#999",sw=0.8)
    g.txt(X(xx),axis+3.2*sc+dy+12,t,size=10.5,anchor="middle")
lab(el_off,"electrode",95)
lab(el_off+el_d/2+0.45,"wire",70)
lab(xe+t_inner/2,"inner wall (retains nut)",45)
lab((x_nut0+x_nut1)/2,"captive nut (can't rotate)",20)
lab(x_nut1+t_outer/2,"outer wall (head bears)",120)
g.txt(X(x_out+2),axis-2.4*sc,"M3 Allen bolt",size=11,anchor="start",fill="#111")
g.txt(bx+(el_off+x_out)/2*sc, by+170,"thicker PC-CF walls than the current part (Grace-proof)",size=11,anchor="middle",fill="#060")

# ---------- Panel C: PRINT ORIENTATION ----------
py=470
g.txt(40,py-6,"PRINT ORIENTATION  -  vertical faces / vertical holes / teardrop+nut-slot  =>  NO SUPPORTS",size=15,weight="bold")
bed=py+330
def bedline(x0,x1):
    g.line(x0,bed,x1,bed,stroke="#888",sw=2)
    for x in range(int(x0),int(x1),14): g.line(x,bed,x-6,bed+8,stroke="#bbb",sw=1)
# cap closed-top down
cx=250; bedline(cx-150,cx+150); ch=12*11; tt=2.5*11; ww=2*11
g.rect(cx-cap_r*11,bed-tt,2*cap_r*11,tt,fill=CAP,stroke="#1f5fa0",sw=1.6)
g.rect(cx-cap_r*11,bed-ch,ww,ch-tt,fill=CAP,stroke="#1f5fa0",sw=1.6)
g.rect(cx+cap_r*11-ww,bed-ch,ww,ch-tt,fill=CAP,stroke="#1f5fa0",sw=1.6)
g.txt(cx,bed-ch-12,"CAP - closed top on bed, mouth up",size=13,anchor="middle",weight="bold")
g.txt(cx,bed+26,"cavity opens UP; thread + holes vertical; tab is a vertical lobe",size=11,anchor="middle",fill="#060")
g.line(cx,bed-tt-6,cx,bed-ch+8,stroke="#060",sw=1.4)
g.poly([(cx-4,bed-ch+12),(cx+4,bed-ch+12),(cx,bed-ch+4)],fill="#060",stroke="#060",sw=1)
# column flush-face down, pegs up
cx=720; bedline(cx-150,cx+150); colh=25*11/2.0; endw=(el_off+5)*11
g.rect(cx-endw,bed-colh,2*endw,colh,fill=CARR,stroke="#a06000",sw=1.6,rx=6)
for hx in (-el_off,el_off): g.line(cx+hx*11,bed,cx+hx*11,bed-colh,stroke="#a06000",sw=1,dash="3 3")
for sgn in (-1,1): g.rect(cx+sgn*peg_off*11-peg_r*11,bed-colh-4*11,2*peg_r*11,4*11,fill=CARR,stroke="#a06000",sw=1.3)
g.txt(cx,bed-colh-4*11-10,"COLUMN - flush face on bed, pegs up",size=13,anchor="middle",weight="bold")
g.txt(cx,bed+26,"bores vertical; M3 teardropped; nut drops from top",size=11,anchor="middle",fill="#060")

out=(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
     f'<rect width="{W}" height="{H}" fill="#fbfbfb"/>'+"".join(g.p)+"</svg>")
open("/workspace/design-concept/electrode-holder-v3-figure.svg","w").write(out)
print("wrote electrode-holder-v3-figure.svg")

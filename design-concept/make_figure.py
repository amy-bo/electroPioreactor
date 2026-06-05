#!/usr/bin/env python3
"""Figure for electrode-holder.scad. Plain stdlib SVG.
A: top (ports, real tab)  B: clamp cross-section (corrected nut)  C: top (open)  D: print."""
import math
el_off=4.8; el_d=6; fit=0.3; bore_d=el_d+fit; cap_R=13.5
port_R=(18.7706-3.2)/2; port_rad=1.6; port_angles=[60,90,120,240,270,300]
bearing_r=el_d/2+1.8; peg_off=3; peg_r=1.5
xe=el_off+bore_d/2; clamp_in=1.8; nut_th=2.6; clamp_out=2.2
x_nut0=xe+clamp_in; x_nut1=x_nut0+nut_th; x_out=x_nut1+clamp_out
nut_af=5.7; nut_ac=nut_af/math.cos(math.radians(30))
tab_R=17; tab_half=26

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
    def poly(s,pts,fill="none",stroke="#222",sw=1.5,op=1,close=True):
        pp=" ".join(f"{x:.1f},{y:.1f}" for x,y in pts)
        tag="polygon" if close else "polyline"
        s.p.append(f'<{tag} points="{pp}" fill="{fill}" fill-opacity="{op}" stroke="{stroke}" stroke-width="{sw}"/>')
    def txt(s,x,y,t,size=13,anchor="start",fill="#111",weight="normal"):
        s.p.append(f'<text x="{x:.1f}" y="{y:.1f}" font-family="Helvetica,Arial" font-size="{size}" text-anchor="{anchor}" fill="{fill}" font-weight="{weight}">{t}</text>')
    def hexagon(s,cx,cy,af,fill,stroke,sw=1.5,rot=90):
        ac=af/math.cos(math.radians(30)); pts=[]
        for k in range(6):
            a=math.radians(60*k+rot); pts.append((cx+ac/2*math.cos(a), cy-ac/2*math.sin(a)))
        s.poly(pts,fill=fill,stroke=stroke,sw=sw)

CAP="#cfe0f5"; CARR="#ffd9a0"; SEPT="#cdb6ec"; ELEC="#b9bcc2"; PEG="#d98a2b"; WIRE="#c0622a"; STEEL="#9aa0a8"
g=Svg(); W,H=1000,1230; s=10.0

def tab_radius(adeg):
    # constant-radius plateau at -90 with fillet shoulders
    d=abs(((adeg+90+180)%360)-180)
    if d<=tab_half-4: return tab_R
    if d>=tab_half+5: return cap_R
    t=(tab_half+5-d)/9.0; return cap_R+(tab_R-cap_R)*(t*t*(3-2*t))

def cap_outline(cx,cy):
    pts=[]
    for a in range(0,360,2):
        r=tab_radius(a); pts.append((cx+r*s*math.cos(math.radians(a)), cy-r*s*math.sin(math.radians(a))))
    return pts

def topview(cx,cy,style,title):
    g.txt(cx,cy-tab_R*s-14,title,size=15,anchor="middle",weight="bold")
    g.poly(cap_outline(cx,cy),fill=CAP,stroke="#1f5fa0",sw=1.7)
    g.circ(cx,cy,(18.7706/2)*s,stroke="#2a8f72",sw=1,dash="5 4")          # neck
    if style=="open":
        g.circ(cx,cy,(cap_R-2-1.5)*s,fill=SEPT,stroke="none",op=0.30)     # exposed septum field
        g.rect(cx-cap_R*s,cy-5*s,2*cap_R*s,2*5*s,fill=CAP,stroke="#1f5fa0",sw=1.2,rx=6) # full-width x-spine
    else:
        g.circ(cx,cy,(cap_R-2)*s,fill=SEPT,stroke="none",op=0.18)
    # column bearing + rounded ears
    g.rect(cx-el_off*s,cy-bearing_r*s,2*el_off*s,2*bearing_r*s,fill=CARR,stroke="none",op=0.5)
    for sgn in (-1,1):
        g.circ(cx+sgn*el_off*s,cy,bearing_r*s,fill=CARR,stroke="#b06a10",sw=1,op=0.5)
        g.rect(cx+(sgn>0 and xe*s or -x_out*s),cy-(nut_af/2+1.6)*s,(x_out-xe)*s,(nut_af+3.2)*s,
               fill=CARR,stroke="#b06a10",sw=1,op=0.5,rx=6)
    if style=="ports":
        for a in port_angles:
            r=math.radians(a); g.circ(cx+port_R*s*math.cos(r),cy-port_R*s*math.sin(r),port_rad*s,fill="#fff",stroke="#6a3da0",sw=1.4)
    for sgn in (-1,1): g.circ(cx+sgn*el_off*s,cy,el_d/2*s,fill=ELEC,stroke="#555",sw=1.3)
    for sgn in (-1,1): g.circ(cx,cy+sgn*peg_off*s,peg_r*s,fill=PEG,stroke="#7a4a08",sw=1.1)
    note = "6 ports inside the neck (green)" if style=="ports" else "full-width spine surrounds pegs; two large rounded windows"
    g.txt(cx,cy+tab_R*s+22,note,size=10.5,anchor="middle",fill="#444")
    g.txt(cx,cy+tab_R*s+38,"poka-yoke = constant-radius tab (from vial-cap-s.3mf)",size=10.5,anchor="middle",fill="#444")

topview(245,200,"ports","TOP - ports")
topview(245,650,"open","TOP - open septum field")

# ----- Panel B: CLAMP cross-section (corrected) -----
bx,by=560,150; sc=15
g.txt(bx+ (el_off+x_out)/2*sc, by-44,"CLAMP cross-section (outside  →  in)",size=15,anchor="middle",weight="bold")
ax=by+40
def X(xx): return bx+xx*sc
g.circ(X(el_off),ax,el_d/2*sc,fill=ELEC,stroke="#555",sw=1.4)
g.circ(X(el_off+el_d/2+0.45),ax,0.9*sc,fill=WIRE,stroke="#7a3a12",sw=1.2)
g.rect(X(xe),ax-3.0*sc,clamp_in*sc,6.0*sc,fill=CARR,stroke="#a06000",sw=1.4)         # inner wall
g.rect(X(x_nut1),ax-3.0*sc,clamp_out*sc,6.0*sc,fill=CARR,stroke="#a06000",sw=1.4)    # outer wall
# nut = RECTANGLE here (thin dimension along the bolt), not a hexagon
g.rect(X(x_nut0),ax-nut_ac/2*sc,nut_th*sc,nut_ac*sc,fill=STEEL,stroke="#444",sw=1.4)
g.line(X(el_off+el_d/2),ax,X(x_out+3),ax,stroke="#333",sw=3)                         # bolt
g.rect(X(x_out),ax-2.0*sc,1.5*sc,4.0*sc,fill="#777",stroke="#333",sw=1.2)            # allen head
def lab(xx,t,dy,anc="middle"):
    g.line(X(xx),ax+3.0*sc,X(xx),ax+3.0*sc+dy,stroke="#999",sw=0.7); g.txt(X(xx),ax+3.0*sc+dy+12,t,size=10,anchor=anc)
lab(el_off,"electrode",92); lab(el_off+el_d/2+0.45,"wire",68)
lab(xe+clamp_in/2,"inner wall",44); lab((x_nut0+x_nut1)/2,"nut (thin side along bolt)",20)
lab(x_nut1+clamp_out/2,"outer wall (head bears)",116)
g.txt(X(x_out+2.2),ax-2.4*sc,"M3 Allen bolt",size=10.5,anchor="start")

# end view of the nut (looking along the bolt): hex flats against the slot walls
ex,ey=720,485
g.txt(ex,ey-4.6*sc,"nut end-view (down the bolt)",size=12,anchor="middle",weight="bold")
g.hexagon(ex,ey,nut_af*sc,STEEL,"#444",sw=1.5,rot=90)         # vertex up/down, flats left/right
g.line(ex-nut_af/2*sc,ey-4*sc,ex-nut_af/2*sc,ey+4*sc,stroke="#a06000",sw=2)   # slot wall
g.line(ex+nut_af/2*sc,ey-4*sc,ex+nut_af/2*sc,ey+4*sc,stroke="#a06000",sw=2)   # slot wall
g.circ(ex,ey,1.7*sc,fill="#fff",stroke="#333",sw=1)
g.line(ex-2.2*sc,ey-4*sc,ex+2.2*sc,ey-4*sc,stroke="#060",sw=1.5)
g.poly([(ex-3,ey-4*sc+5),(ex+3,ey-4*sc+5),(ex,ey-4*sc-3)],fill="#060",stroke="#060")
g.txt(ex,ey+5.4*sc,"flats vs slot walls = can't rotate;",size=10,anchor="middle",fill="#060")
g.txt(ex,ey+5.4*sc+13,"open top = drops in, no bridge",size=10,anchor="middle",fill="#060")

# ----- Panel D: PRINT orientation -----
py=905
g.txt(470,py-2,"PRINT ORIENTATION  -  no supports (clamp at top => nut pocket opens at the bed)",size=14,weight="bold",anchor="middle")
bed=py+200
def bedline(x0,x1):
    g.line(x0,bed,x1,bed,stroke="#888",sw=2)
    for x in range(int(x0),int(x1),14): g.line(x,bed,x-6,bed+8,stroke="#bbb",sw=1)
cx=250; bedline(cx-150,cx+150); ch=12.3*11; tt=2.5*11; ww=2*11
g.rect(cx-cap_R*11,bed-tt,2*cap_R*11,tt,fill=CAP,stroke="#1f5fa0",sw=1.5)
g.rect(cx-cap_R*11,bed-ch,ww,ch-tt,fill=CAP,stroke="#1f5fa0",sw=1.5)
g.rect(cx+cap_R*11-ww,bed-ch,ww,ch-tt,fill=CAP,stroke="#1f5fa0",sw=1.5)
g.txt(cx,bed-ch-10,"CAP - closed top on bed",size=12,anchor="middle",weight="bold")
g.txt(cx,bed+24,"cavity opens up; tab is a vertical lobe",size=10,anchor="middle",fill="#060")
cx=720; bedline(cx-150,cx+150); colh=24.7*11/2.2; endw=(el_off+5)*11
g.rect(cx-endw,bed-colh,2*endw,colh,fill=CARR,stroke="#a06000",sw=1.5,rx=8)
for hx in (-el_off,el_off): g.line(cx+hx*11,bed,cx+hx*11,bed-colh,stroke="#a06000",sw=1,dash="3 3")
for sgn in (-1,1):  # pegs (short cylinders) pointing up, flush-depth = cap top thickness
    bxp=cx+sgn*peg_off*11
    g.rect(bxp-peg_r*11,bed-colh-2.5*11,2*peg_r*11,2.5*11,fill=CARR,stroke="#a06000",sw=1.2)
g.txt(cx,bed-colh-2.5*11-8,"COLUMN - flush face on bed, pegs up",size=12,anchor="middle",weight="bold")
g.txt(cx,bed+24,"bores vertical; teardrop holes; nut pocket opens at the bed (no bridge)",size=10,anchor="middle",fill="#060")

out=(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
     f'<rect width="{W}" height="{H}" fill="#fbfbfb"/>'+"".join(g.p)+"</svg>")
open("/workspace/design-concept/electrode-holder-figure.svg","w").write(out)
print("wrote electrode-holder-figure.svg")

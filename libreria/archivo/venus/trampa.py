import sys, math, random
sys.path.insert(0, '/tmp/claude-0/-home-user-automatizacion-contenidos/039df981-7a17-5355-b711-18510fb209db/scratchpad/venus')
from trap import *

HX, HY, AO, S = 250, 372, 26, 1.0
PRE = sys.argv[1] if len(sys.argv) > 1 else ""

def lw(cx, cy, lower):
    """punto canónico del lóbulo -> mundo (abierto)"""
    sg = -1 if lower else 1
    y = -sg * cy
    a = math.radians(AO if lower else -AO)
    return (HX + S * (cx * math.cos(a) - y * math.sin(a)), HY + S * (cx * math.sin(a) + y * math.cos(a)))

def hairbase(x, lower):
    top = 60 * math.sin(math.pi * (x - 12) / 406)
    return lw(x, top * 0.55, lower), lw(x + 6, top * 0.55 - 30, lower)

defs = DEFS + '''
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#EAF6E2"/><stop offset="1" stop-color="#CFE8C4"/></linearGradient>
<radialGradient id="bok" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0.7"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient>
<linearGradient id="moss" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9CCB6A"/><stop offset="1" stop-color="#5E8F3E"/></linearGradient>
<radialGradient id="dropG" cx="0.35" cy="0.3" r="0.8"><stop offset="0" stop-color="#FFFFFF"/><stop offset="0.4" stop-color="#BFE6FF"/><stop offset="1" stop-color="#4FA3E6"/></radialGradient>
'''
o = [svg_open(defs)]
o.append('<rect width="1000" height="700" fill="url(#sky)"/>')
random.seed(3)
for _ in range(14):
    x, y, r = random.uniform(0, 1000), random.uniform(40, 420), random.uniform(30, 80)
    o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="url(#bok)"/>')
# hojas lejanas desenfocadas (sin contorno)
for (x, y, a, c) in ((860, 520, -40, "#B5D9A0"), (720, 600, -20, "#A8D190"), (960, 300, -70, "#BFE0AA"), (110, 600, 30, "#A8D190")):
    o.append(f'<g transform="translate({x} {y}) rotate({a})"><path d="M -150 0 C -80 -60, 80 -60, 150 0 C 80 60, -80 60, -150 0 Z" fill="{c}"/></g>')
# musgo (esfagno) abajo
o.append('<path d="M 0 610 C 120 590, 260 612, 400 598 C 560 584, 720 610, 860 596 C 930 590, 970 600, 1000 596 L 1000 700 L 0 700 Z" fill="url(#moss)" stroke="#0B0B14" stroke-width="6" stroke-linejoin="round"/>')
mo = []
for _ in range(90):
    x = random.uniform(10, 990); y = random.uniform(615, 690)
    mo.append(f'<path d="M {x:.0f} {y:.0f} l -6 -8 M {x:.0f} {y:.0f} l 6 -8 M {x:.0f} {y:.0f} l 0 -10" />')
o.append('<g stroke="#3F6E2A" stroke-width="2.5" stroke-linecap="round" opacity="0.7">' + "".join(mo) + '</g>')
# peciolo desde abajo a la izquierda
o.append(petiole(60, 690, HX, HY, w=40))
# lóbulos
o.append(lobe("lobebot", HX, HY, AO, S, lower=True, hair_id={1: "hair1", 2: "hair2"}))
# mosca: posición inicial (revoloteando arriba a la derecha)
FX0, FY0 = 820, 170
h1b, h1t = hairbase(235, True)
h2b, h2t = hairbase(315, True)
# punto donde se posa la mosca: un poco por encima del pelito
L1 = (h1t[0] + 34, h1t[1] - 18)
L2 = (h2t[0] + 30, h2t[1] - 22)
print(f"fly moves: to hair1 {L1[0]-FX0:.0f},{L1[1]-FY0:.0f}  to hair2 {L2[0]-L1[0]:.0f},{L2[1]-L1[1]:.0f}", file=sys.stderr)
fx, fy = (FX0, FY0)
if PRE == "h1": fx, fy = L1
if PRE == "h2": fx, fy = L2
o.append(fly("fly", fx, fy, 1.15, -10, wings_id="wings"))
o.append(lobe("lobetop", HX, HY, -AO, S, lower=False))
# señal eléctrica: desde el pelito hasta la bisagra
def bolt(p, q, n=7, amp=12):
    pts = [p]
    for k in range(1, n):
        t = k / n
        x = p[0] + (q[0] - p[0]) * t; y = p[1] + (q[1] - p[1]) * t
        dx, dy = q[0] - p[0], q[1] - p[1]; ln = math.hypot(dx, dy)
        sgn = 1 if k % 2 else -1
        pts.append((x - dy / ln * amp * sgn, y + dx / ln * amp * sgn))
    pts.append(q)
    return P(pts)
o.append('<g id="zap">' + stroke2(bolt(h1b, (HX + 14, HY + 6)), 6, "#FFE14D", extra=7) + stroke2(bolt(h2b, (HX + 14, HY + 6), 9), 6, "#FFE14D", extra=7) + '</g>')
# contadores
o.append(counter("n1", h1t[0] - 10, h1t[1] - 120, "1"))
o.append(counter("n2", h2t[0] + 40, h2t[1] - 120, "2", col=CORAL))
# cronómetro 20 s
o.append(tag("t20", 840, 610, "20 s", bg="#FFFFFF", fg=INK))
# gota de lluvia (cae sobre el pelito 1)
DX0, DY0 = 830, 60
o.append(f'<g id="drop"><path d="M {DX0} {DY0-26} C {DX0+6} {DY0-12}, {DX0+18} {DY0}, {DX0+18} {DY0+10} C {DX0+18} {DY0+22}, {DX0+9} {DY0+30}, {DX0} {DY0+30} C {DX0-9} {DY0+30}, {DX0-18} {DY0+22}, {DX0-18} {DY0+10} C {DX0-18} {DY0}, {DX0-6} {DY0-12}, {DX0} {DY0-26} Z" fill="url(#dropG)" stroke="{INK}" stroke-width="5"/><ellipse cx="{DX0-7}" cy="{DY0+6}" rx="4" ry="7" fill="#FFFFFF"/></g>')
print(f"drop move: {h2t[0]-DX0:.0f},{h2t[1]-DY0-30:.0f}", file=sys.stderr)
SPX, SPY = h2t
o.append('<g id="splash">' + "".join(stroke2(f"M {SPX+12*math.cos(math.radians(a)):.0f} {SPY+12*math.sin(math.radians(a)):.0f} L {SPX+30*math.cos(math.radians(a)):.0f} {SPY+30*math.sin(math.radians(a)):.0f}", 4, "#8FD3FF", extra=5) for a in (-160, -125, -90, -55, -20)) + '</g>')
# etiquetas
o.append(counter("nr", h2t[0] + 40, h2t[1] - 120, "1"))
o.append(tag("lpel", 820, 330, "PELITOS", leader=(h2t[0] + 3, h2t[1] + 2)))
# ¡zas!
o.append(f'<g id="zas"><path d="M 720 200 L 760 150 L 772 190 L 830 150 L 812 210 L 870 214 L 806 246 L 830 290 L 770 262 L 742 300 L 736 252 L 690 250 Z" fill="#FFE14D" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
         f'<text x="780" y="236" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="34" fill="{INK}">¡ZAS!</text></g>')
if PRE == "closed":
    o.append(f'<style>#lobetop,#lobebot{{transform-box:fill-box;transform-origin:center}}#lobetop{{rotate:{AO}deg}}#lobebot{{rotate:-{AO}deg}}#fly{{opacity:0}}</style>')
o.append('</svg>')
print("\n".join(o))

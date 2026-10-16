"""Corte del embudo de la hormiga león: arena con textura, larva enterrada, hormiga resbalando."""
import math, random, sys
sys.path.insert(0, ".")
from lib import *

S = 236                      # superficie del suelo
ANG = 33                     # ángulo de reposo aprox. de la arena seca
HALF = 340
DEPTH = HALF * math.tan(math.radians(ANG))
L, R, A = (500 - HALF, S), (500 + HALF, S), (500, S + DEPTH)
ux, uy = HALF / math.hypot(HALF, DEPTH), DEPTH / math.hypot(HALF, DEPTH)   # dirección ladera izq. hacia abajo
RIMRY = 34


def onslope(t):  # punto de la ladera izquierda, t=0 borde, t=1 fondo
    return (L[0] + (A[0] - L[0]) * t, L[1] + (A[1] - L[1]) * t)


o = [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 700">
<defs>
{ANT_DEFS}
{LARVA_DEFS}
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#CFEAFF"/><stop offset="1" stop-color="#FFF1DA"/></linearGradient>
<linearGradient id="cut" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E9C98E"/><stop offset="0.5" stop-color="#D2A866"/><stop offset="1" stop-color="#A97C48"/></linearGradient>
<linearGradient id="wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F6E3B8"/><stop offset="0.7" stop-color="#E2C089"/><stop offset="1" stop-color="#C99E5E"/></linearGradient>
<linearGradient id="ground" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F3E0B2"/><stop offset="1" stop-color="#EBCF97"/></linearGradient>
<radialGradient id="pocket" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#8A6436" stop-opacity="0.55"/><stop offset="1" stop-color="#8A6436" stop-opacity="0"/></radialGradient>
</defs>
<rect width="1000" height="700" fill="url(#sky)"/>''']
# fondo lejano: dunas y pinos claros, sin contorno
o.append('<path d="M 0 170 C 120 140, 220 150, 330 160 C 470 172, 560 128, 700 138 C 820 146, 900 128, 1000 140 L 1000 210 L 0 210 Z" fill="#F1DDB4"/>')
o.append('<g fill="#B9D7B0" opacity="0.9">' + "".join(
    f'<path d="M {x} 162 L {x - 18} 162 L {x} {162 - h} L {x + 18} 162 Z"/><rect x="{x - 3}" y="160" width="6" height="12" fill="#C9B79A"/>'
    for x, h in ((70, 70), (112, 52), (880, 64), (930, 82), (965, 56))) + '</g>')
o.append(f'<rect y="190" width="1000" height="{S - 190 + 2}" fill="url(#ground)"/>')
# plano del suelo: textura lejana
o.append(grains([(0, 192), (1000, 192), (1000, S), (0, S)], 120, ["#E2C48C", "#D9B77C", "#FFF3D6"], 1.2, 2.6, seed=3, op=0.8))
# pared trasera del embudo (vista dentro del corte)
back = f"M {L[0]} {S} A {HALF} {RIMRY} 0 0 1 {R[0]} {S} L {A[0]} {A[1]:.1f} Z"
o.append(f'<path d="{back}" fill="url(#wall)"/>')
# curvas de nivel del cono
for f in (0.2, 0.4, 0.6, 0.8):
    rx, cy = HALF * (1 - f), S + DEPTH * f
    o.append(f'<path d="M {500 - rx:.1f} {cy:.1f} A {rx:.1f} {RIMRY * (1 - f):.1f} 0 0 1 {500 + rx:.1f} {cy:.1f}" fill="none" stroke="#C49A5C" stroke-width="3" opacity="0.45"/>')
wallpoly = [(L[0] + 20, S - 4), (500, S - RIMRY + 6), (R[0] - 20, S - 4), (A[0], A[1] - 10)]
o.append(grains(wallpoly, 160, ["#D6B072", "#C99E5E", "#FFF6E0"], 1.5, 3.2, seed=5, op=0.75))
o.append(f'<path d="M {L[0]} {S} A {HALF} {RIMRY} 0 0 1 {R[0]} {S}" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>')
o.append(f'<path d="M {L[0] + 30} {S - 6} A {HALF - 30} {RIMRY - 6} 0 0 1 {R[0] - 30} {S - 6}" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.55"/>')

# cara de corte (primer plano)
cutpoly = [(-10, S), L, A, R, (1010, S), (1010, 710), (-10, 710)]
o.append(f'<path d="{P(cutpoly)} Z" fill="url(#cut)"/>')
# estratos
random.seed(11)
for k, y0 in enumerate((330, 420, 520, 610)):
    pts = []
    for x in range(-10, 1011, 40):
        y = y0 + 8 * math.sin(x / 90 + k) + 4 * math.sin(x / 37)
        pts.append((x, y))
    o.append(f'<path d="{P(pts)}" fill="none" stroke="#B68852" stroke-width="5" opacity="0.35"/>')
LV = (506, 478)      # cabeza de la larva
avoid = [(LV[0] + 86, LV[1] + 108, 120, 100)]
o.append(grains(cutpoly, 900, ["#C99A5C", "#B5864A", "#E9CC95", "#F7E6BF", "#9C7040"], 2, 5.5, seed=7, avoid=avoid))
# piedrecitas
for x, y, rx, ry, c in ((90, 560, 26, 15, "#A9A39A"), (940, 470, 30, 17, "#B8AFA2"), (300, 640, 20, 11, "#9E968B"), (760, 400, 16, 10, "#B0A698")):
    o.append(f'<g><ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{c}" stroke="{INK}" stroke-width="4"/><ellipse cx="{x - rx * 0.3:.0f}" cy="{y - ry * 0.4:.0f}" rx="{rx * 0.35:.0f}" ry="{ry * 0.25:.0f}" fill="#FFFFFF" opacity="0.6"/></g>')

# borde del corte (tinta)
o.append(f'<path d="M -10 {S} L {L[0]} {S} L {A[0]} {A[1]:.1f} L {R[0]} {S} L 1010 {S}" fill="none" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>')
o.append(f'<path d="M -10 {S + 7} L {L[0] - 4} {S + 7}  M {L[0] + 10} {S + 12} L {A[0] - 6} {A[1] + 2:.1f} M {A[0] + 6} {A[1] + 2:.1f} L {R[0] - 10} {S + 12} M {R[0] + 4} {S + 7} L 1010 {S + 7}" fill="none" stroke="#FFF2D2" stroke-width="3" opacity="0.7"/>')

# larva enterrada (en su hueco), cabeza en el fondo del embudo
o.append(f'<ellipse cx="{LV[0] + 80}" cy="{LV[1] + 104}" rx="105" ry="150" fill="url(#pocket)" transform="rotate(-40 {LV[0] + 80} {LV[1] + 104})"/>')
o.append(f'<g id="larva"><g transform="translate({LV[0]} {LV[1]}) rotate(-28) scale(0.86)">')
o.append(larva(0.8))
o.append('</g></g>')
# algo de arena sobre el cuerpo (está enterrada)
o.append(grains([(LV[0] + 60, LV[1] + 60), (LV[0] + 170, LV[1] + 90), (LV[0] + 130, LV[1] + 170), (LV[0] + 30, LV[1] + 140)], 18, ["#E9CC95", "#C99A5C"], 2, 4.5, seed=9, op=0.9))

# matas de hierba seca en los bordes
def tuft(x, y, sc=1, col="#8FAF4E"):
    s = []
    for a, h in ((-30, 46), (-12, 64), (6, 58), (24, 44), (40, 32)):
        ex, ey = x + math.sin(math.radians(a)) * h * sc, y - math.cos(math.radians(a)) * h * sc
        s.append(dstroke(f"M {x} {y} Q {x + (ex - x) * 0.3:.1f} {y - h * sc * 0.6:.1f} {ex:.1f} {ey:.1f}", 4, col, 5))
    return "".join(s)
o.append(f'<g id="grass">{tuft(70, S + 2)}{tuft(930, S + 2, 1.1, "#9DB85A")}</g>')

# ángulo de reposo (en la ladera derecha)
r = 120
ax2, ay2 = R[0] - r * math.cos(math.radians(ANG)), S + r * math.sin(math.radians(ANG))
o.append(f'<g id="angulo"><line x1="{R[0]}" y1="{S}" x2="{R[0] - 190}" y2="{S}" stroke="{INK}" stroke-width="4" stroke-dasharray="10 9"/>'
         f'<path d="M {R[0] - r} {S} A {r} {r} 0 0 0 {ax2:.1f} {ay2:.1f}" fill="none" stroke="{INK}" stroke-width="12" stroke-linecap="round"/>'
         f'<path d="M {R[0] - r} {S} A {r} {r} 0 0 0 {ax2:.1f} {ay2:.1f}" fill="none" stroke="{LIME}" stroke-width="6" stroke-linecap="round"/>'
         f'<g><rect x="{R[0] - 250}" y="{S + 22}" width="100" height="40" rx="10" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/>'
         f'<text x="{R[0] - 200}" y="{S + 52}" text-anchor="middle" font-family="{FONT}" font-weight="800" font-size="24" fill="{INK}">≈33°</text></g></g>')
am = math.radians(ANG / 2)
o.append(tag("langulo", 790, 160, "ÁNGULO DE REPOSO", R[0] - r * math.cos(am), S + r * math.sin(am)))

# avalancha bajo la hormiga
t0, t1 = 0.36, 0.86
streaks = []
for k, (a, b, off) in enumerate(((0.40, 0.66, 10), (0.50, 0.80, 20), (0.58, 0.88, 6), (0.45, 0.72, 30))):
    p, q = onslope(a), onslope(b)
    nx, ny = uy, -ux   # normal hacia el aire (arriba-derecha)
    streaks.append(f'<line x1="{p[0] + nx * off:.1f}" y1="{p[1] + ny * off:.1f}" x2="{q[0] + nx * off:.1f}" y2="{q[1] + ny * off:.1f}" stroke="#FFF6E0" stroke-width="4" stroke-linecap="round" stroke-dasharray="16 12" opacity="0.9"/>')
gr = []
random.seed(21)
for k in range(46):
    t = random.uniform(0.42, 0.86)
    off = random.uniform(4, 30)
    p = onslope(t)
    x, y = p[0] + uy * off, p[1] - ux * off
    rr = random.uniform(3, 6.5)
    gr.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rr:.1f}" fill="{random.choice(["#E2BC7E", "#C99A5C", "#F3DDAE"])}" stroke="{INK}" stroke-width="1.6"/>')
o.append(f'<g id="aval">{"".join(streaks)}{"".join(gr)}</g>')
pa, pb = onslope(0.56), onslope(0.84)
off = 44
o.append(arrow("avarrow", [(pa[0] + uy * off, pa[1] - ux * off), (pb[0] + uy * off, pb[1] - ux * off)], CORAL, 10, 30))
o.append(tag("laval", 196, 470, "AVALANCHA", onslope(0.66)[0] - 4, onslope(0.66)[1] + 6))

# chorros de arena lanzados por la larva hacia la hormiga
head = (LV[0] - 6, LV[1] - 46)
arcs, gr = [], []
for k, (tx, ty, cy_) in enumerate(((300, 236, 120), (350, 214, 150), (260, 270, 170))):
    d = f"M {head[0]} {head[1]} Q {(head[0] + tx) / 2 - 10:.0f} {cy_} {tx} {ty}"
    arcs.append(f'<path d="{d}" fill="none" stroke="#B5864A" stroke-width="4" stroke-linecap="round" stroke-dasharray="3 12" opacity="0.9"/>')
random.seed(31)
for k in range(40):
    tt = random.uniform(0.25, 1.0)
    tx, ty, cy_ = random.choice(((300, 236, 120), (350, 214, 150), (260, 270, 170)))
    cx_ = (head[0] + tx) / 2 - 10
    x = (1 - tt) ** 2 * head[0] + 2 * (1 - tt) * tt * cx_ + tt * tt * tx + random.uniform(-14, 14)
    y = (1 - tt) ** 2 * head[1] + 2 * (1 - tt) * tt * cy_ + tt * tt * ty + random.uniform(-14, 14)
    rr = random.uniform(3, 6)
    gr.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rr:.1f}" fill="{random.choice(["#E2BC7E", "#C99A5C", "#F3DDAE"])}" stroke="{INK}" stroke-width="1.6"/>')
o.append(f'<g id="tossarc">{"".join(arcs)}</g>')
o.append(f'<g id="toss">{"".join(gr)}</g>')

# hormiga en la ladera (resbalando, mirando cuesta arriba)
ANT_T = 0.34
ap = onslope(ANT_T)
o.append(f'<g id="ant"><g transform="translate({ap[0]:.1f} {ap[1]:.1f}) rotate({ANG}) scale(0.85)">{ant("slip")}</g></g>')
o.append(f'<g id="sweat"><path d="M {ap[0] - 70:.0f} {ap[1] - 120:.0f} q -6 12 0 18 q 6 -6 0 -18 Z" fill="#8FD3FF" stroke="{INK}" stroke-width="3"/>'
         f'<path d="M {ap[0] - 40:.0f} {ap[1] - 136:.0f} l -6 -16 M {ap[0] - 22:.0f} {ap[1] - 134:.0f} l 2 -18" stroke="{INK}" stroke-width="4" stroke-linecap="round"/></g>')
o.append(tag("lant", 150, 156, "HORMIGA", ap[0] - 60, ap[1] - 70))
o.append(tag("llarva", 850, 560, "LARVA", LV[0] + 140, LV[1] + 96))

# cadáver vacío lanzado fuera (oculto salvo en su escena)
o.append(f'<g id="husk"><g transform="translate(610 180) rotate(-160) scale(0.8)">{ant("walk", husk=True)}</g>'
         f'<path d="M 540 260 q 10 -30 40 -46 M 512 266 q 14 -40 44 -60" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round" opacity="0.7"/></g>')
o.append('</svg>')
print("\n".join(o))

"""Fig. 1 · Pez arquero en el manglar disparando a una mosca."""
import math, random
from lib import *
from parts import fish, fish_defs, fly, FLY_DEFS, MOUTH

S = 330  # superficie
ANG, SC = -47, 0.85
MW = (556, 337)  # boca en el mundo
mx, my = xf(MOUTH, 0, 0, ANG, SC)
TX, TY = MW[0] - mx, MW[1] - my
P = lambda p: xf(p, TX, TY, ANG, SC)

# hoja diana y mosca
LEAF0, LEAFC, LEAF1 = (664, 240), (772, 200), (884, 228)   # borde superior de la hoja (bezier cuadrática)
leaf_top = lambda t: qbez(LEAF0, LEAFC, LEAF1, t)
BUG = (776, 0)  # x del centro; y se calcula
bug_y = y_at_x(leaf_top, BUG[0])
BUGS = 1.45
foot = lambda xl: (y_at_x(leaf_top, BUG[0] + xl * BUGS) - bug_y) / BUGS
TARGET = (BUG[0] + 6, bug_y - 36 * BUGS)  # tórax de la mosca

defs = fish_defs("f") + FLY_DEFS + """
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#D6EEFF"/><stop offset="1" stop-color="#FFF3E0"/></linearGradient>
<linearGradient id="water" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8FD3FF"/><stop offset="0.5" stop-color="#4FA3E6"/><stop offset="1" stop-color="#2F7FD6"/></linearGradient>
<linearGradient id="bark" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8A6243"/><stop offset="0.5" stop-color="#6B4A33"/><stop offset="1" stop-color="#4A3222"/></linearGradient>
<linearGradient id="leafg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5FCB8C"/><stop offset="1" stop-color="#1F7F52"/></linearGradient>
<linearGradient id="leafd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#46B37A"/><stop offset="1" stop-color="#176943"/></linearGradient>
<linearGradient id="sand" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E7C487"/><stop offset="1" stop-color="#B98F5A"/></linearGradient>
<radialGradient id="dropg" cx="0.35" cy="0.3" r="0.8"><stop offset="0" stop-color="#FFFFFF"/><stop offset="0.5" stop-color="#9FDBFF"/><stop offset="1" stop-color="#2F7FD6"/></radialGradient>
"""
o = [svg_open(defs)]
o.append('<rect width="1000" height="700" fill="url(#sky)"/>')
# fondo lejano: manglar desaturado sin contorno
def canopy(y0, col, seed, r0, r1):
    random.seed(seed)
    c = []
    x = -40
    while x < 1060:
        r = random.uniform(r0, r1)
        c.append(f'<circle cx="{f(x)}" cy="{f(y0 - r * 0.5)}" r="{f(r)}"/>')
        x += r * 1.2
    return f'<g fill="{col}">{"".join(c)}<rect x="0" y="{y0 - 10}" width="1000" height="{S - y0 + 10}"/></g>'
o.append(canopy(270, "#D3EAD8", 3, 40, 70))
o.append(canopy(300, "#B5DDC1", 7, 30, 52))
# raíces lejanas
o.append('<g fill="none" stroke="#8FBF9C" stroke-width="6" opacity="0.8">' + "".join(
    f'<path d="M {x} 290 C {x - 20} 300, {x - 34} 318, {x - 40} {S}"/><path d="M {x} 290 C {x + 18} 302, {x + 28} 318, {x + 34} {S}"/>' for x in (420, 560, 880)) + '</g>')

# agua
o.append(f'<rect y="{S}" width="1000" height="{700 - S}" fill="url(#water)"/>')
# raíces sumergidas (desdibujadas)
o.append(f'<g fill="none" stroke="#2C6FA8" stroke-width="16" opacity="0.35" stroke-linecap="round">'
         f'<path d="M 40 {S} C 36 420, 30 540, 24 700"/><path d="M 150 {S} C 168 430, 190 560, 196 700"/><path d="M 250 {S} C 280 420, 300 520, 330 640"/></g>')
o.append('<g id="rays"><g fill="#FFFFFF" opacity="0.13">'
         f'<path d="M 330 {S} L 400 {S} L 300 700 L 190 700 Z"/><path d="M 640 {S} L 690 {S} L 640 700 L 560 700 Z"/><path d="M 860 {S} L 930 {S} L 920 700 L 810 700 Z"/></g></g>')
# peces lejanos
far = '<path d="M 0 0 C 14 -10, 34 -10, 44 0 C 34 10, 14 10, 0 0 Z M 0 0 L -12 -8 L -12 8 Z"/>'
o.append(f'<g id="school"><g fill="#2A6EAF" opacity="0.4"><g transform="translate(760 430)">{far}</g><g transform="translate(830 452) scale(0.8)">{far}</g><g transform="translate(700 470) scale(0.7)">{far}</g></g></g>')
# fondo de arena
o.append(f'<path d="M 0 650 C 160 636, 330 658, 520 644 C 700 632, 860 652, 1000 640 L 1000 700 L 0 700 Z" fill="url(#sand)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
o.append(f'<g fill="#9C7A4C" stroke="{INK}" stroke-width="4"><ellipse cx="120" cy="664" rx="24" ry="10"/><ellipse cx="640" cy="662" rx="16" ry="8"/><ellipse cx="890" cy="660" rx="28" ry="11"/></g>')
# hierbas del fondo
o.append('<g id="grass">' + "".join(dbl(f"M {x} 652 C {x - 6} 610, {x + 10} 590, {x + 4} {560 + (x % 3) * 12}", 6, "#2E9C6A", 6) for x in (560, 578, 940, 958, 976)) + '</g>')
# sombra del pez en el fondo
o.append(f'<ellipse cx="{f(P((0, 0))[0] + 30)}" cy="660" rx="150" ry="9" fill="#1D5FA8" opacity="0.45"/>')

# mangle cercano (izquierda): tronco + raíces zancudas
o.append(f'<g id="tree"><path d="M 70 -10 L 66 236 L 124 236 L 120 -10 Z" fill="url(#bark)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
         f'<path d="M 82 0 L 80 220" stroke="#A47A55" stroke-width="5" opacity="0.7"/>'
         f'<path d="M 100 30 q 6 10 0 20 M 92 120 q 6 10 0 20 M 106 180 q -6 10 0 20" fill="none" stroke="{INK}" stroke-width="3" opacity="0.4"/>')
for (x0, y0, x1, c1, c2) in [(80, 226, 18, (50, 236), (26, 290)), (96, 232, 120, (100, 270), (114, 300)),
                             (112, 228, 214, (150, 230), (200, 280)), (118, 214, 296, (190, 196), (270, 260))]:
    d = f"M {x0} {y0} C {c1[0]} {c1[1]}, {c2[0]} {c2[1]}, {x1} {S + 4}"
    o.append(dbl(d, 14, "#6B4A33", 8, cap="butt"))
    o.append(f'<path d="{d}" fill="none" stroke="#A47A55" stroke-width="3" opacity="0.7" transform="translate(-3 -3)"/>')
o.append('</g>')

# superficie

o.append(f'<line x1="0" y1="{S + 8}" x2="1000" y2="{S + 8}" stroke="#FFFFFF" stroke-width="3" opacity="0.55"/>')
o.append(f'<g fill="#FFFFFF" opacity="0.5"><rect x="300" y="{S + 18}" width="60" height="4" rx="2"/><rect x="700" y="{S + 22}" width="80" height="4" rx="2"/><rect x="880" y="{S + 16}" width="40" height="4" rx="2"/></g>')

# rama con hojas (desde la derecha)
BR = "M 1010 64 C 920 80, 820 92, 720 104 C 670 110, 630 116, 600 128"
o.append(dbl(BR, 20, "#6B4A33", 8))
o.append(f'<path d="M 1000 62 C 920 76, 820 88, 720 99 C 670 105, 640 110, 610 120" fill="none" stroke="#A47A55" stroke-width="4" opacity="0.8"/>')
def mleaf(cx, cy, ang, L=70, Wd=24, grad="leafg"):
    return (f'<g transform="translate({cx} {cy}) rotate({ang})"><path d="M 0 0 C {L*0.3} {-Wd}, {L*0.75} {-Wd}, {L} 0 C {L*0.75} {Wd}, {L*0.3} {Wd}, 0 0 Z" fill="url(#{grad})" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
            f'<path d="M 4 0 L {L - 8} 0" stroke="#B9F0C9" stroke-width="3" stroke-linecap="round"/></g>')
o.append('<g id="leaves">' + "".join([
    mleaf(940, 72, -150, 80, 24, "leafd"), mleaf(900, 78, 70, 76, 22), mleaf(860, 84, 115, 70, 22, "leafd"),
    mleaf(812, 90, -20, 74, 22), mleaf(700, 110, -35, 66, 20), mleaf(612, 126, 150, 64, 20, "leafd"),
    mleaf(980, 66, 95, 70, 22)]) + '</g>')
# hoja diana: pecíolo desde la rama
o.append(dbl("M 652 120 C 672 160, 648 204, 664 240", 6, "#3E7A4F", 6))
lb = (f"M {LEAF0[0]} {LEAF0[1]} Q {LEAFC[0]} {LEAFC[1]} {LEAF1[0]} {LEAF1[1]} "
      f"Q 790 282 {LEAF0[0]} {LEAF0[1]} Z")
o.append(f'<g id="leaf"><path d="{lb}" fill="url(#leafg)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
         f'<path d="M 676 240 Q 780 226 870 230" fill="none" stroke="#B9F0C9" stroke-width="3" stroke-linecap="round"/>'
         f'<path d="M 706 226 Q 768 208 830 212" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.6" stroke-linecap="round"/></g>')
# mosca
o.append(f'<g id="bug"><g transform="translate({f(BUG[0])} {f(bug_y)}) scale({BUGS})">{fly(foot)}</g></g>')
# golpe del chorro en la mosca
def burst(cx, cy, r1, r2, n=10, col=LIME):
    pts = []
    for k in range(2 * n):
        r = r2 if k % 2 == 0 else r1
        a = math.pi * k / n
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return f'<path d="{pts_d(pts, True)}" fill="{col}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
o.append(f'<g id="impact">{burst(TARGET[0], TARGET[1], 30, 62, 9, "#FFFFFF")}'
         + "".join(f'<circle cx="{f(TARGET[0] + 70 * math.cos(a))}" cy="{f(TARGET[1] + 60 * math.sin(a))}" r="{r}" fill="url(#dropg)" stroke="{INK}" stroke-width="3"/>'
                   for a, r in [(-2.6, 9), (-1.9, 7), (-0.6, 10), (0.2, 7), (-1.2, 6)]) + '</g>')

# pez (debajo del agua) + burbujas
o.append(f'<g id="fish"><g id="fishbody"><g transform="translate({f(TX)} {f(TY)}) rotate({ANG}) scale({SC})">{fish("f")}</g></g></g>')
gx, gy = P((40, -80))
o.append('<g id="bubbles" fill="#FFFFFF" fill-opacity="0.35" stroke="#FFFFFF" stroke-width="3">' + "".join(
    f'<circle cx="{f(gx + dx)}" cy="{f(gy + dy)}" r="{r}"/>' for dx, dy, r in [(-10, -20, 7), (6, -52, 5), (-4, -84, 9), (14, -112, 4)]) + '</g>')

o.append(f'<path d="M {MW[0]-44} {S} L {MW[0]+30} {S}" stroke="#FFFFFF" stroke-width="3" opacity="0.7"/>')
# ondas en la boca
o.append('<g fill="none" stroke="#FFFFFF" stroke-width="4">')
for k in (1, 2):
    o.append(f'<g id="rip{k}"><ellipse cx="{MW[0]}" cy="{S + 2}" rx="56" ry="10"/></g>')
LAND = (TARGET[0] + 40, S)
for k in (1, 2):
    o.append(f'<g id="rs{k}"><ellipse cx="{f(LAND[0])}" cy="{S + 2}" rx="60" ry="11"/></g>')
o.append('</g>')

# chorro: parábola desde la boca hasta la mosca (sale en la dirección del pez)
d_dir = (math.cos(math.radians(ANG)), math.sin(math.radians(ANG)))
C = (MW[0] + d_dir[0] * 150, MW[1] + d_dir[1] * 150)
end = (TARGET[0] - 4, TARGET[1] + 16)
jd = f"M {MW[0]} {MW[1] - 2} Q {f(C[0])} {f(C[1])} {f(end[0])} {f(end[1])}"
o.append(f'<g id="jet"><path d="{jd}" fill="none" stroke="{INK}" stroke-width="17" stroke-linecap="round"/>'
         f'<path d="{jd}" fill="none" stroke="#8FD3FF" stroke-width="9" stroke-linecap="round"/>'
         f'<path d="{jd}" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" opacity="0.9" transform="translate(-3 0)"/></g>')
pts = [qbez(MW, C, end, t) for t in (0.25, 0.5, 0.75)]
o.append('<g id="drops">' + "".join(
    f'<circle cx="{f(x + dx)}" cy="{f(y + dy)}" r="{r}" fill="url(#dropg)" stroke="{INK}" stroke-width="3"/>'
    for (x, y), (dx, dy, r) in zip(pts, [(-22, 6, 6), (24, -4, 7), (-20, 4, 5)])) + '</g>')
# salpicadura al caer
sx = LAND[0]
o.append(f'<g id="splash">' + "".join(
    f'<path d="M {f(sx + a)} {S} Q {f(sx + a * 1.4)} {S - h} {f(sx + a * 2)} {S - h * 0.6}" fill="none" stroke="{INK}" stroke-width="12" stroke-linecap="round"/>'
    f'<path d="M {f(sx + a)} {S} Q {f(sx + a * 1.4)} {S - h} {f(sx + a * 2)} {S - h * 0.6}" fill="none" stroke="#8FD3FF" stroke-width="6" stroke-linecap="round"/>'
    for a, h in [(-14, 56), (14, 56), (-26, 34), (26, 34)])
    + "".join(f'<circle cx="{f(sx + dx)}" cy="{f(S - dy)}" r="{r}" fill="url(#dropg)" stroke="{INK}" stroke-width="3"/>' for dx, dy, r in [(-50, 70, 6), (52, 76, 7), (0, 92, 8)]) + '</g>')

o.append(f'<line x1="{0}" y1="{S}" x2="1000" y2="{S}" stroke="{INK}" stroke-width="6"/>')
# etiquetas
lp, bp = label("lpresa", 470, 176, "PRESA", line_to=(TARGET[0] - 30, TARGET[1] + 6))
o.append(lp)
fc = P((20, 10))
lf, bf = label("lpez", 800, 560, "PEZ ARQUERO", line_to=(fc[0] + 40, fc[1] + 20))
o.append(lf)
o.append('</svg>')
open("escena.svg", "w").write("\n".join(o))
print("mouth", MW, "target", TARGET, "fish center", P((0, 0)), "tail", P((-252, 0)), "lp", bp, "lf", bf)

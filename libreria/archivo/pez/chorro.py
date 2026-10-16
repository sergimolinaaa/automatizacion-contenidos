"""Fig. · El chorro: la cola sale más rápida que la punta y el agua se junta en una gota."""
import math, random
from lib import *
from parts import fish, fish_defs, fly, FLY_DEFS, MOUTH

S = 540
ANG, SC = -45, 0.8
MW = (196, S + 4)
mx, my = xf(MOUTH, 0, 0, ANG, SC)
TX, TY = MW[0] - mx, MW[1] - my
P0, C, P2 = (MW[0] + 2, MW[1] - 4), (440, 300), (800, 172)
B = lambda t: qbez(P0, C, P2, t)
def tang(t):
    a, b = B(max(0, t - 0.01)), B(min(1, t + 0.01))
    L = math.hypot(b[0] - a[0], b[1] - a[1])
    return ((b[0] - a[0]) / L, (b[1] - a[1]) / L)

FS = 1.35
F = (806, 150)       # cuerpo de la mosca
FO = (F[0], F[1] + 38 * FS)
LEAF0, LEAFC, LEAF1 = (FO[0] - 120, FO[1] + 8), (FO[0] - 6, FO[1] - 30), (FO[0] + 116, FO[1] + 4)
leaf_top = lambda t: qbez(LEAF0, LEAFC, LEAF1, t)
fy0 = y_at_x(leaf_top, FO[0])
FO = (FO[0], fy0)
foot = lambda xl: (y_at_x(leaf_top, FO[0] + xl * FS) - fy0) / FS

defs = fish_defs("f") + FLY_DEFS + """
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#D6EEFF"/><stop offset="1" stop-color="#FFF3E0"/></linearGradient>
<linearGradient id="water" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8FD3FF"/><stop offset="1" stop-color="#3D8FE0"/></linearGradient>
<linearGradient id="leafg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5FCB8C"/><stop offset="1" stop-color="#1F7F52"/></linearGradient>
<linearGradient id="jetg" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#5FB4F0"/><stop offset="1" stop-color="#A9E0FF"/></linearGradient>
<radialGradient id="blobg" cx="0.36" cy="0.3" r="0.8"><stop offset="0" stop-color="#FFFFFF"/><stop offset="0.45" stop-color="#A9E0FF"/><stop offset="1" stop-color="#2F7FD6"/></radialGradient>
<radialGradient id="dropg" cx="0.35" cy="0.3" r="0.8"><stop offset="0" stop-color="#FFFFFF"/><stop offset="0.5" stop-color="#9FDBFF"/><stop offset="1" stop-color="#2F7FD6"/></radialGradient>
"""
o = [svg_open(defs)]
o.append('<rect width="1000" height="700" fill="url(#sky)"/>')
random.seed(11)
for y0, col, r0, r1 in [(470, "#D9EDDD", 50, 84), (520, "#BFE2C9", 36, 60)]:
    c, x = [], -40
    while x < 1060:
        r = random.uniform(r0, r1)
        c.append(f'<circle cx="{f(x)}" cy="{f(y0 - r * 0.45)}" r="{f(r)}"/>')
        x += r * 1.2
    o.append(f'<g fill="{col}">{"".join(c)}<rect x="0" y="{y0 - 6}" width="1000" height="{S - y0 + 6}"/></g>')
# cuadrícula de medida tenue (como una foto de laboratorio)
o.append('<g stroke="#9CC3DE" stroke-width="2" opacity="0.45">' + "".join(f'<line x1="{x}" y1="40" x2="{x}" y2="{S}"/>' for x in range(100, 1000, 100))
         + "".join(f'<line x1="0" y1="{y}" x2="1000" y2="{y}"/>' for y in range(100, S, 100)) + '</g>')
o.append(f'<rect y="{S}" width="1000" height="{700 - S}" fill="url(#water)"/>')

# rama + hoja + mosca
o.append(dbl("M 1010 60 C 960 66, 930 72, 900 80", 18, "#6B4A33", 8))
o.append(dbl(f"M 950 70 C 962 110, 950 {f(FO[1] - 20)}, {f(LEAF1[0] - 6)} {f(LEAF1[1] - 2)}", 6, "#3E7A4F", 6))
lb = f"M {f(LEAF0[0])} {f(LEAF0[1])} Q {f(LEAFC[0])} {f(LEAFC[1])} {f(LEAF1[0])} {f(LEAF1[1])} Q {f(FO[0])} {f(FO[1] + 48)} {f(LEAF0[0])} {f(LEAF0[1])} Z"
o.append(f'<g id="leaf"><path d="{lb}" fill="url(#leafg)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
         f'<path d="M {f(LEAF0[0] + 14)} {f(LEAF0[1] + 2)} Q {f(FO[0])} {f(FO[1] + 8)} {f(LEAF1[0] - 12)} {f(LEAF1[1] + 2)}" fill="none" stroke="#B9F0C9" stroke-width="3"/></g>')
o.append(f'<g id="bug"><g transform="translate({f(FO[0])} {f(FO[1])}) scale({FS})">{fly(foot)}</g></g>')

# chorro con grosor variable: más grueso cerca de la boca (cola) que en el tramo medio
def ribbon(t0, t1, w0, w1, n=40):
    left, right = [], []
    for k in range(n + 1):
        t = t0 + (t1 - t0) * k / n
        w = w0 + (w1 - w0) * k / n
        (x, y), (tx, ty) = B(t), tang(t)
        nx, ny = -ty, tx
        left.append((x + nx * w / 2, y + ny * w / 2))
        right.append((x - nx * w / 2, y - ny * w / 2))
    return pts_d(left + right[::-1], True)
TB = 0.87  # posición de la gota
o.append('<g id="stream">')
o.append(f'<path d="{ribbon(0.0, TB, 26, 12)}" fill="url(#jetg)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
hl = "M " + " L ".join(f"{f(B(t)[0] - tang(t)[1] * -4)} {f(B(t)[1] + tang(t)[0] * -4)}" for t in [i / 30 * (TB - 0.05) + 0.03 for i in range(31)])
o.append(f'<path d="{hl}" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" opacity="0.85"/>')
o.append('</g>')
bx, by = B(TB)
o.append(f'<g id="blob"><circle cx="{f(bx)}" cy="{f(by)}" r="32" fill="url(#blobg)" stroke="{INK}" stroke-width="6"/>'
         f'<ellipse cx="{f(bx - 10)}" cy="{f(by - 12)}" rx="10" ry="6" fill="#FFFFFF" transform="rotate(-30 {f(bx - 10)} {f(by - 12)})"/></g>')

# flechas de velocidad (paralelas al chorro, por debajo)
def speed_arrow(id_, t, length, col, off=46, w=10):
    (x, y), (tx, ty) = B(t), tang(t)
    nx, ny = ty, -tx  # lado inferior-derecho
    cx, cy = x - nx * off, y - ny * off
    return arrow(id_, cx - tx * length / 2, cy - ty * length / 2, cx + tx * length / 2, cy + ty * length / 2, col, w=w)
o.append(speed_arrow("fast", 0.26, 170, CORAL, w=12))
o.append(speed_arrow("slow", 0.7, 64, LIME, w=10))

# superficie, ondas y pez
o.append(f'<g id="fish"><g id="fishbody"><g transform="translate({f(TX)} {f(TY)}) rotate({ANG}) scale({SC})">{fish("f")}</g></g></g>')
o.append(f'<line x1="0" y1="{S}" x2="1000" y2="{S}" stroke="{INK}" stroke-width="6"/>')
o.append(f'<line x1="0" y1="{S + 8}" x2="1000" y2="{S + 8}" stroke="#FFFFFF" stroke-width="3" opacity="0.55"/>')
o.append('<g fill="none" stroke="#FFFFFF" stroke-width="4">' + "".join(
    f'<g id="rip{k}"><ellipse cx="{MW[0]}" cy="{S + 3}" rx="60" ry="10"/></g>' for k in (1, 2)) + '</g>')

# impacto
def burst(cx, cy, r1, r2, n=9):
    pts = [(cx + (r2 if k % 2 == 0 else r1) * math.cos(math.pi * k / n), cy + (r2 if k % 2 == 0 else r1) * math.sin(math.pi * k / n)) for k in range(2 * n)]
    return f'<path d="{pts_d(pts, True)}" fill="#FFFFFF" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
o.append(f'<g id="impact">{burst(F[0] - 10, F[1], 30, 64)}' + "".join(
    f'<circle cx="{f(F[0] - 10 + 76 * math.cos(a))}" cy="{f(F[1] + 64 * math.sin(a))}" r="{r}" fill="url(#dropg)" stroke="{INK}" stroke-width="3"/>'
    for a, r in [(-2.6, 9), (-1.8, 7), (-0.7, 10), (0.4, 7), (2.4, 8)]) + '</g>')

# etiquetas
def side(t, off):
    (x, y), (tx, ty) = B(t), tang(t)
    return (x - ty * off, y + tx * off)
fa, sa = side(0.26, 46), side(0.7, 46)
L = [label("lfast", fa[0] + 110, fa[1] + 70, "COLA RÁPIDA", bg=CORAL, fg=INK),
     label("lslow", sa[0] + 90, sa[1] + 70, "PUNTA LENTA", bg=LIME, fg=INK),
     label("lgota", bx - 190, by - 50, "GOTA", line_to=(bx - 32, by - 6))]
for s_, b in L:
    o.append(s_)
o.append('</svg>')
open("chorro.svg", "w").write("\n".join(o))
print("blob", (bx, by), "fast", B(0.22), "slow", B(0.72), [b for _, b in L])

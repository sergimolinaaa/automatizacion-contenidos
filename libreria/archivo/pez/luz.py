"""Fig. · Refracción: la mosca real y la que «ve» el pez."""
import math, random
from lib import *
from parts import fish, fish_defs, fly, FLY_DEFS, EYE, MOUTH

S = 300
F = (806, 212)      # centro del cuerpo de la mosca real
E = (346, 436)      # ojo del pez
N1, N2 = 1.0, 1.33
FS = 1.2


def solve():
    def g(xp):
        s1 = (F[0] - xp) / math.hypot(F[0] - xp, F[1] - S)
        s2 = (xp - E[0]) / math.hypot(xp - E[0], E[1] - S)
        return N1 * s1 - N2 * s2
    lo, hi = E[0], F[0]
    for _ in range(80):
        m = (lo + hi) / 2
        if g(m) > 0:
            lo = m
        else:
            hi = m
    return (m, S)


P = solve()
dF = math.hypot(F[0] - P[0], F[1] - S)
u = ((P[0] - E[0]), (P[1] - E[1]))
n = math.hypot(*u)
u = (u[0] / n, u[1] / n)
G = (P[0] + u[0] * dF * 1.0, P[1] + u[1] * dF * 0.94)   # posición aparente
ANG = math.degrees(math.atan2(u[1], u[0]))
SC = 0.66
ex, ey = xf(EYE, 0, 0, ANG, SC)
TX, TY = E[0] - ex, E[1] - ey
MW = xf(MOUTH, TX, TY, ANG, SC)

# hoja bajo la mosca real
FO = (F[0], F[1] + 38 * FS)  # pies
LEAF0, LEAFC, LEAF1 = (FO[0] - 112, FO[1] + 6), (FO[0] - 4, FO[1] - 30), (FO[0] + 108, FO[1] + 2)
leaf_top = lambda t: qbez(LEAF0, LEAFC, LEAF1, t)
fy0 = y_at_x(leaf_top, FO[0])
FO = (FO[0], fy0)
foot = lambda xl: (y_at_x(leaf_top, FO[0] + xl * FS) - fy0) / FS

defs = fish_defs("f") + FLY_DEFS + """
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#D6EEFF"/><stop offset="1" stop-color="#FFF3E0"/></linearGradient>
<linearGradient id="water" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8FD3FF"/><stop offset="0.6" stop-color="#4FA3E6"/><stop offset="1" stop-color="#2F7FD6"/></linearGradient>
<linearGradient id="leafg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5FCB8C"/><stop offset="1" stop-color="#1F7F52"/></linearGradient>
<linearGradient id="sand" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E7C487"/><stop offset="1" stop-color="#B98F5A"/></linearGradient>
"""
o = [svg_open(defs)]
o.append('<rect width="1000" height="700" fill="url(#sky)"/>')
random.seed(5)
c = []
x = -30
while x < 1050:
    r = random.uniform(34, 60)
    c.append(f'<circle cx="{f(x)}" cy="{f(268 - r * 0.4)}" r="{f(r)}"/>')
    x += r * 1.25
o.append(f'<g fill="#CFE8D6">{"".join(c)}<rect x="0" y="262" width="1000" height="40"/></g>')
o.append(f'<rect y="{S}" width="1000" height="{700 - S}" fill="url(#water)"/>')
o.append('<g id="rays"><g fill="#FFFFFF" opacity="0.12">'
         f'<path d="M 600 {S} L 660 {S} L 600 700 L 510 700 Z"/><path d="M 860 {S} L 930 {S} L 930 700 L 820 700 Z"/></g></g>')
o.append(f'<path d="M 0 652 C 200 640, 380 660, 560 646 C 740 634, 880 656, 1000 644 L 1000 700 L 0 700 Z" fill="url(#sand)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
o.append(f'<g fill="#9C7A4C" stroke="{INK}" stroke-width="4"><ellipse cx="560" cy="664" rx="22" ry="9"/><ellipse cx="860" cy="662" rx="16" ry="8"/></g>')

# rama + ramita hasta la hoja
o.append(dbl("M 1010 70 C 960 78, 920 84, 880 96", 18, "#6B4A33", 8))
o.append(dbl(f"M 940 82 C 950 140, 930 {FO[1] - 30}, {f(LEAF1[0] - 6)} {f(LEAF1[1] - 2)}", 6, "#3E7A4F", 6))
o.append(f'<g transform="translate(900 92) rotate(-150)"><path d="M 0 0 C 21 -22, 52 -22, 70 0 C 52 22, 21 22, 0 0 Z" fill="url(#leafg)" stroke="{INK}" stroke-width="5"/><path d="M 4 0 L 62 0" stroke="#B9F0C9" stroke-width="3"/></g>')
lb = f"M {f(LEAF0[0])} {f(LEAF0[1])} Q {f(LEAFC[0])} {f(LEAFC[1])} {f(LEAF1[0])} {f(LEAF1[1])} Q {f(FO[0])} {f(FO[1] + 46)} {f(LEAF0[0])} {f(LEAF0[1])} Z"
o.append(f'<path d="{lb}" fill="url(#leafg)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
o.append(f'<path d="M {f(LEAF0[0] + 14)} {f(LEAF0[1] + 2)} Q {f(FO[0])} {f(FO[1] + 8)} {f(LEAF1[0] - 12)} {f(LEAF1[1] + 2)}" fill="none" stroke="#B9F0C9" stroke-width="3"/>')

# normal y rayos
o.append(f'<g id="normal"><path d="{dash_d([(P[0], S - 120), (P[0], S + 150)], 12, 9)}" stroke="{INK}" stroke-width="3" opacity="0.55"/></g>')
o.append(f'<g id="fake"><path d="{dash_d([P, (G[0] - 30 * u[0], G[1] - 30 * u[1])], 16, 12)}" fill="none" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round"/></g>')
ray = f"M {f(F[0])} {f(F[1])} L {f(P[0])} {f(P[1])} L {f(E[0])} {f(E[1])}"
o.append(f'<g id="ray"><path d="{ray}" fill="none" stroke="{INK}" stroke-width="15" stroke-linecap="round" stroke-linejoin="round"/>'
         f'<path d="{ray}" fill="none" stroke="#FFE15A" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></g>')
# punto de quiebre
o.append(f'<g id="bend"><circle cx="{f(P[0])}" cy="{f(P[1])}" r="22" fill="none" stroke="{LIME}" stroke-width="6"/><circle cx="{f(P[0])}" cy="{f(P[1])}" r="22" fill="none" stroke="{INK}" stroke-width="2"/></g>')
# superficie
o.append(f'<line x1="0" y1="{S}" x2="1000" y2="{S}" stroke="{INK}" stroke-width="6"/>')
o.append(f'<line x1="0" y1="{S + 8}" x2="1000" y2="{S + 8}" stroke="#FFFFFF" stroke-width="3" opacity="0.55"/>')


# mosca aparente (fantasma)
GO = (G[0], G[1] + 38 * FS)
o.append(f'<g id="ghost"><g opacity="0.45"><g transform="translate({f(GO[0])} {f(GO[1])}) scale({FS})">{fly(ids=False)}</g></g></g>')
# mosca real
o.append(f'<g id="bug"><g transform="translate({f(FO[0])} {f(FO[1])}) scale({FS})">{fly(foot)}</g></g>')
# diana sobre la real
o.append(f'<g id="reticle" fill="none"><circle cx="{f(F[0] + 10)}" cy="{f(F[1] - 6)}" r="70" stroke="{INK}" stroke-width="11"/>'
         f'<circle cx="{f(F[0] + 10)}" cy="{f(F[1] - 6)}" r="70" stroke="{CORAL}" stroke-width="5"/>'
         + "".join(f'<path d="M {f(F[0] + 10 + dx * 54)} {f(F[1] - 6 + dy * 54)} L {f(F[0] + 10 + dx * 88)} {f(F[1] - 6 + dy * 88)}" stroke="{INK}" stroke-width="11" stroke-linecap="round"/>'
                   f'<path d="M {f(F[0] + 10 + dx * 54)} {f(F[1] - 6 + dy * 54)} L {f(F[0] + 10 + dx * 88)} {f(F[1] - 6 + dy * 88)}" stroke="{CORAL}" stroke-width="5" stroke-linecap="round"/>'
                   for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]) + '</g>')

# pez
o.append(f'<g id="fish"><g id="fishbody"><g transform="translate({f(TX)} {f(TY)}) rotate({f(ANG)}) scale({SC})">{fish("f")}</g></g></g>')
# línea de puntería corregida: de la boca a la mosca real
A0, A1 = MW, (F[0] - 6, F[1] + 10)
nd = int(math.hypot(A1[0] - A0[0], A1[1] - A0[1]) // 24)
o.append('<g id="aim">' + "".join(f'<circle cx="{f(A0[0] + (A1[0] - A0[0]) * k / nd)}" cy="{f(A0[1] + (A1[1] - A0[1]) * k / nd)}" r="6" fill="{CORAL}" stroke="{INK}" stroke-width="3"/>' for k in range(1, nd + 1)) + '</g>')

L = [label("lparece", 560, 96, "PARECE", line_to=(G[0] - 46, G[1])),
     label("lreal", 600, 200, "REAL", line_to=(F[0] - 40, F[1] - 6)),
     label("ltuerce", 250, 236, "SE TUERCE", line_to=(P[0] - 22, P[1] - 4))]
for s_, b in L:
    o.append(s_)
o.append('</svg>')
open("luz.svg", "w").write("\n".join(o))
print("P", P, "G", G, "ANG", ANG, "MW", MW, "boxes", [b for _, b in L], "tail", xf((-252, 0), TX, TY, ANG, SC))

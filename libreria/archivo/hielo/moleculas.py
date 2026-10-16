import math, random, sys
sys.path.insert(0, "/tmp/claude-0/-home-user-automatizacion-contenidos/039df981-7a17-5355-b711-18510fb209db/scratchpad/dedos")
from common import *

random.seed(21)
BY0, BY1 = 160, 560
LX0, LX1 = 40, 440
IX0, IX1 = 520, 960
o = [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 700">
<defs>
<radialGradient id="bg" cx="0.5" cy="0.45" r="0.8"><stop offset="0" stop-color="#F4FAFF"/><stop offset="1" stop-color="#D8EAF6"/></radialGradient>
<linearGradient id="liq" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9ED8FF"/><stop offset="1" stop-color="#3F8FDB"/></linearGradient>
<linearGradient id="ice" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F3FBFF"/><stop offset="1" stop-color="#BFE3F7"/></linearGradient>
<radialGradient id="ox" cx="0.35" cy="0.3" r="0.75"><stop offset="0" stop-color="#FF9A7E"/><stop offset="0.6" stop-color="#F0472B"/><stop offset="1" stop-color="#B92A16"/></radialGradient>
<radialGradient id="hy" cx="0.35" cy="0.3" r="0.75"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#D6E2EC"/></radialGradient>
<clipPath id="box"><rect x="520" y="160" width="440" height="400" rx="26"/></clipPath>
</defs>
<rect width="1000" height="700" fill="url(#bg)"/>
<g fill="none" stroke="#C9DDEB" stroke-width="2"><circle cx="500" cy="350" r="320"/><circle cx="500" cy="350" r="460"/></g>''']


def mol(x, y, ang, s=1.0):
    """molecula de agua: O rojo + 2 H blancos a 104,5 grados"""
    g = [f'<g transform="translate({x:.1f} {y:.1f}) rotate({ang:.0f}) scale({s})">']
    for side in (-1, 1):
        a = math.radians(90 + side * 52.25)
        hx, hy = 25 * math.cos(a), 25 * math.sin(a)
        g.append(f'<line x1="0" y1="0" x2="{hx:.1f}" y2="{hy:.1f}" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>')
        g.append(f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="10" fill="url(#hy)" stroke="{INK}" stroke-width="3.5"/>')
    g.append(f'<circle cx="0" cy="0" r="17" fill="url(#ox)" stroke="{INK}" stroke-width="4"/>')
    g.append('<circle cx="-6" cy="-6" r="4.5" fill="#FFFFFF" opacity="0.75"/></g>')
    return "".join(g)


# ---------- caja liquido ----------
o.append(f'<rect x="{LX0 + 8}" y="{BY0 + 10}" width="{LX1 - LX0}" height="{BY1 - BY0}" rx="26" fill="{INK}" opacity="0.15"/>')
o.append(f'<rect x="{LX0}" y="{BY0}" width="{LX1 - LX0}" height="{BY1 - BY0}" rx="26" fill="url(#liq)" stroke="{INK}" stroke-width="7"/>')
o.append(f'<path d="M {LX0 + 24} {BY0 + 14} L {LX1 - 24} {BY0 + 14}" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity="0.7"/>')
pts = []
tries = 0
while len(pts) < 40 and tries < 20000:
    tries += 1
    x = random.uniform(LX0 + 34, LX1 - 34); y = random.uniform(BY0 + 36, BY1 - 34)
    if all(math.hypot(x - a, y - b) > 58 for a, b in pts):
        pts.append((x, y))
groups = [[], [], []]
for i, (x, y) in enumerate(pts):
    groups[i % 3].append(mol(x, y, random.uniform(0, 360)))
for k, gr in enumerate(groups):
    o.append(f'<g id="liq{k + 1}">' + "".join(gr) + '</g>')
# flechitas de movimiento (agitacion)
o.append('<g id="jitter" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" opacity="0.85">')
for x, y in random.sample(pts, 7):
    a = random.uniform(0, 6.28)
    o.append(f'<path d="M {x + 26 * math.cos(a):.0f} {y + 26 * math.sin(a):.0f} l {12 * math.cos(a):.0f} {12 * math.sin(a):.0f}"/>')
o.append('</g>')

# ---------- caja hielo ----------
o.append(f'<rect x="{IX0 + 8}" y="{BY0 + 10}" width="{IX1 - IX0}" height="{BY1 - BY0}" rx="26" fill="{INK}" opacity="0.15"/>')
o.append(f'<rect x="{IX0}" y="{BY0}" width="{IX1 - IX0}" height="{BY1 - BY0}" rx="26" fill="url(#ice)" stroke="{INK}" stroke-width="7"/>')
o.append(f'<path d="M {IX0 + 24} {BY0 + 14} L {IX1 - 24} {BY0 + 14}" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>')
A = 64
s3 = math.sqrt(3)
verts = {}
centers = []
for j in range(-1, 8):
    for i in range(-1, 8):
        cx = IX0 + 40 + i * s3 * A + (j % 2) * s3 * A / 2
        cy = BY0 + 30 + j * 1.5 * A
        centers.append((cx, cy))
        for k in range(6):
            a = math.radians(90 + 60 * k)
            vx, vy = round(cx + A * math.cos(a), 1), round(cy + A * math.sin(a), 1)
            verts[(round(vx), round(vy))] = (vx, vy)
M = -40
V = [v for v in verts.values() if IX0 + M < v[0] < IX1 - M and BY0 + M < v[1] < BY1 - M]
E = []
for i in range(len(V)):
    for j in range(i + 1, len(V)):
        if abs(math.hypot(V[i][0] - V[j][0], V[i][1] - V[j][1]) - A) < 2:
            E.append((i, j))
random.shuffle(E)
nh = [0] * len(V)
hbonds, cov = [], []
for i, j in E:
    if nh[i] > nh[j]:
        i, j = j, i
    if nh[i] < 2:
        nh[i] += 1
        cov.append((i, j))
    else:
        hbonds.append((i, j))
# enlaces de hidrogeno: puntitos
o.append('<g clip-path="url(#box)">')
o.append('<g id="hb" fill="#3F8FDB">')
for i, j in cov:
    (x1, y1), (x2, y2) = V[i], V[j]
    for t in [0.5, 0.6, 0.7, 0.8]:
        o.append(f'<circle cx="{x1 + (x2 - x1) * t:.1f}" cy="{y1 + (y2 - y1) * t:.1f}" r="3.2"/>')
for i, j in hbonds:
    (x1, y1), (x2, y2) = V[i], V[j]
    for t in [0.3, 0.42, 0.54, 0.66]:
        o.append(f'<circle cx="{x1 + (x2 - x1) * t:.1f}" cy="{y1 + (y2 - y1) * t:.1f}" r="3.2"/>')
o.append('</g>')
# huecos (centros de hexagonos dentro de la caja)
gaps = [(x, y) for x, y in centers if IX0 - 10 < x < IX1 + 10 and BY0 - 10 < y < BY1 + 10]
o.append('<g id="gaps">')
for x, y in gaps:
    o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="26" fill="{LIME}" opacity="0.55" stroke="{INK}" stroke-width="3"/>')
o.append('</g>')
# hexagonos remarcados
o.append('<g id="hexes" fill="none" stroke-linejoin="round">')
for x, y in gaps:
    d = "M " + " L ".join(f"{x + A * math.cos(math.radians(90 + 60 * k)):.1f} {y + A * math.sin(math.radians(90 + 60 * k)):.1f}" for k in range(6)) + " Z"
    o.append(f'<path d="{d}" stroke="{INK}" stroke-width="12"/><path d="{d}" stroke="{LIME}" stroke-width="6"/>')
o.append('</g>')
# moleculas de la red: H hacia sus vecinos
o.append('<g id="lattice">')
for vi, (x, y) in enumerate(V):
    hs = [V[j] for i, j in cov if i == vi]
    g = [f'<g>']
    for hx, hy in hs:
        a = math.atan2(hy - y, hx - x)
        px, py = x + 25 * math.cos(a), y + 25 * math.sin(a)
        g.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{px:.1f}" y2="{py:.1f}" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>')
        g.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="10" fill="url(#hy)" stroke="{INK}" stroke-width="3.5"/>')
    g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="17" fill="url(#ox)" stroke="{INK}" stroke-width="4"/><circle cx="{x - 6:.1f}" cy="{y - 6:.1f}" r="4.5" fill="#FFFFFF" opacity="0.75"/></g>')
    o.append("".join(g))
o.append('</g>')
o.append('</g>')
o.append(f'<rect x="{IX0}" y="{BY0}" width="{IX1 - IX0}" height="{BY1 - BY0}" rx="26" fill="none" stroke="{INK}" stroke-width="7"/>')
# +9 %: franja extra del hielo respecto al mismo numero de moleculas en liquido
GW = (IX1 - IX0) / 1.09
o.append(f'<g id="more"><rect x="{IX0 + GW:.1f}" y="{BY0 + 4}" width="{IX1 - IX0 - GW - 4:.1f}" height="{BY1 - BY0 - 8}" rx="18" fill="{CORAL}" opacity="0.35"/>'
         f'<path d="M {IX0 + GW:.1f} {BY0 - 6} L {IX0 + GW:.1f} {BY1 + 6}" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>'
         f'<path d="M {IX0 + GW:.1f} {BY0 - 6} L {IX0 + GW:.1f} {BY1 + 6}" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/></g>')
o.append(tag("lmas", 830, 580, "+9 %", bg=CORAL, fg=INK, lead=(890, 580, IX0 + GW + 18, 520)))
# etiquetas
o.append(tag("la", 155, 576, "LÍQUIDO", lead=None))
o.append(tag("lb", 680, 92, "HIELO", lead=None))
gx, gy = min(gaps, key=lambda p: (abs(p[1] - 480) + abs(p[0] - 640)))
o.append(tag("lc", 560, 580, "HUECOS", lead=(640, 580, round(gx), round(gy))))
o.append('</svg>')
print("\n".join(o))

import math, random, sys
sys.path.insert(0, sys.path[0])
from common import *

random.seed(21)
HZ = 330          # horizonte
F = 420           # focal


def P(X, Z):
    return (500 + F * X / Z, HZ + F / Z)


defs = '''
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8EC2EC"/><stop offset="0.7" stop-color="#DCE9F2"/><stop offset="1" stop-color="#FBE6C8"/></linearGradient>
<linearGradient id="playa" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E9DCC0"/><stop offset="1" stop-color="#E2D0AE"/></linearGradient>
<linearGradient id="mtn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#A9826A"/><stop offset="1" stop-color="#7C5B49"/></linearGradient>
<linearGradient id="rock" x1="0" y1="0" x2="0.3" y2="1"><stop offset="0" stop-color="#8A7C70"/><stop offset="0.5" stop-color="#5E534B"/><stop offset="1" stop-color="#352E29"/></linearGradient>
<linearGradient id="metal" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#9AA3AD"/><stop offset="0.5" stop-color="#E6EBF0"/><stop offset="1" stop-color="#7D8790"/></linearGradient>
<radialGradient id="sun" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#FFF6D0"/><stop offset="0.6" stop-color="#FFE48A" stop-opacity="0.9"/><stop offset="1" stop-color="#FFE48A" stop-opacity="0"/></radialGradient>
'''
FULL = len(sys.argv) > 1 and sys.argv[1] == "full"
if FULL:
    o = [head(defs).replace('viewBox="0 0 1000 700"', 'viewBox="0 0 1080 1920"'), '<g transform="translate(-85 430) scale(1.25)">']
    o.append('<rect x="-100" y="-360" width="1200" height="1060" fill="url(#sky)"/>')
    o.append('<g fill="#FFFFFF" opacity="0.8"><ellipse cx="260" cy="-120" rx="110" ry="24"/><ellipse cx="320" cy="-138" rx="60" ry="26"/><ellipse cx="760" cy="-40" rx="80" ry="18"/></g>')
else:
    o = [head(defs)]
    o.append('<rect width="1000" height="700" fill="url(#sky)"/>')
o.append('<g id="sun"><circle cx="830" cy="120" r="90" fill="url(#sun)"/><circle cx="830" cy="120" r="38" fill="#FFF3C2"/></g>')
o.append('<g id="clouds" fill="#FFFFFF" opacity="0.85"><ellipse cx="520" cy="110" rx="90" ry="20"/><ellipse cx="575" cy="96" rx="50" ry="22"/><ellipse cx="200" cy="170" rx="70" ry="14"/></g>')
# montañas lejanas (sin contorno)
o.append(f'<path d="M 0 {HZ-70} L 90 {HZ-120} L 170 {HZ-90} L 260 {HZ-150} L 360 {HZ-100} L 450 {HZ-130} L 540 {HZ-85} L 640 {HZ-140} L 720 {HZ-105} L 820 {HZ-160} L 900 {HZ-120} L 1000 {HZ-135} L 1000 {HZ} L 0 {HZ} Z" fill="#CDB9C4"/>')
o.append(f'<path d="M 0 {HZ-35} L 120 {HZ-70} L 230 {HZ-45} L 330 {HZ-80} L 430 {HZ-50} L 560 {HZ-60} L 680 {HZ-40} L 780 {HZ-75} L 880 {HZ-50} L 1000 {HZ-65} L 1000 {HZ} L 0 {HZ} Z" fill="#B99A8C"/>')
# sierra cercana con contorno (derecha)
o.append(f'<path d="M 620 {HZ+2} L 690 {HZ-55} L 740 {HZ-40} L 800 {HZ-95} L 860 {HZ-70} L 930 {HZ-110} L 1010 {HZ-80} L 1010 {HZ+2} Z" fill="url(#mtn)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
o.append(f'<path d="M 800 {HZ-95} L 790 {HZ-40} M 930 {HZ-110} L 915 {HZ-50} M 690 {HZ-55} L 700 {HZ-20}" stroke="#5E4434" stroke-width="5" stroke-linecap="round"/>')
o.append(f'<path d="M 690 {HZ-55} L 740 {HZ-40} L 800 {HZ-95}" fill="none" stroke="#C9A58A" stroke-width="4" opacity="0.8"/>')
# playa
YB = 1200 if FULL else 700
o.append(f'<rect x="-100" y="{HZ}" width="1200" height="{YB-HZ}" fill="url(#playa)"/>')
# grietas de barro en perspectiva (rejilla en ángulo / log Z)
rows = []
w0, w1, dw = (math.log(0.46) if FULL else math.log(1.05)), math.log(28), 0.13
a0, da = -1.6, 0.115
na = int(3.2 / da) + 1
nw = int((w1 - w0) / dw) + 1
grid = [[None] * (na + 1) for _ in range(nw + 1)]
for i in range(nw + 1):
    for j in range(na + 1):
        jw = random.uniform(-0.3, 0.3) * dw if 0 < i < nw else 0
        ja = random.uniform(-0.3, 0.3) * da
        Z = math.exp(w0 + i * dw + jw)
        a = a0 + j * da + ja
        grid[i][j] = P(a * Z, Z)
cells = []
for i in range(nw):
    for j in range(na):
        q = [grid[i][j], grid[i][j + 1], grid[i + 1][j + 1], grid[i + 1][j]]
        Z = math.exp(w0 + i * dw)
        shade = random.choice(["#EFE5D0", "#EADDC3", "#E6D7BA", "#F1E8D6"])
        sw = max(0.6, 5.5 / Z)
        cells.append(f'<path d="{poly(q)} Z" fill="{shade}" stroke="#B9A584" stroke-width="{sw:.2f}" stroke-linejoin="round"/>')
o.append('<g>' + "".join(reversed(cells)) + '</g>')
o.append(f'<rect y="{HZ}" width="1000" height="14" fill="#E9DCC0" opacity="0.8"/>')
# The Grandstand (afloramiento oscuro al fondo)
o.append(f'<path d="M 250 {HZ+6} L 262 {HZ-10} L 280 {HZ-16} L 300 {HZ-24} L 318 {HZ-18} L 335 {HZ-20} L 352 {HZ-6} L 360 {HZ+6} Z" fill="#4E433B" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')
o.append(f'<path d="M 280 {HZ-14} L 300 {HZ-22} L 318 {HZ-16}" fill="none" stroke="#7D6E62" stroke-width="3"/>')

# surcos y piedras
def trail(pts, wg):
    """pts en suelo (X,Z); devuelve surco: banda oscura + bordes claros"""
    left, right, center = [], [], []
    for k in range(len(pts)):
        X, Z = pts[k]
        if k < len(pts) - 1:
            dX, dZ = pts[k + 1][0] - X, pts[k + 1][1] - Z
        else:
            dX, dZ = X - pts[k - 1][0], Z - pts[k - 1][1]
        ln = math.hypot(dX, dZ); nX, nZ = -dZ / ln, dX / ln
        left.append(P(X + nX * wg, Z + nZ * wg)); right.append(P(X - nX * wg, Z - nZ * wg)); center.append(P(X, Z))
    band = poly(left) + " L " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in reversed(right)) + " Z"
    return band, left, right, center


def smooth(ctrl, n=40):
    """Catmull-Rom en el suelo"""
    out = []
    for i in range(len(ctrl) - 1):
        p0 = ctrl[max(0, i - 1)]; p1 = ctrl[i]; p2 = ctrl[i + 1]; p3 = ctrl[min(len(ctrl) - 1, i + 2)]
        for k in range(n):
            t = k / n
            out.append(tuple(0.5 * ((2 * p1[c]) + (-p0[c] + p2[c]) * t + (2 * p0[c] - 5 * p1[c] + 4 * p2[c] - p3[c]) * t * t + (-p0[c] + 3 * p1[c] - 3 * p2[c] + p3[c]) * t ** 3) for c in (0, 1)))
    out.append(ctrl[-1])
    return out


rocks = [
    # (X, Z, tamaño en suelo, ruta del surco desde la piedra hacia atrás)
    ("r1", 0.42, 2.25, 0.5, [(0.42, 2.45), (0.15, 3.6), (-0.35, 6), (-0.1, 10), (0.6, 17)]),
    ("r2", -1.45, 3.3, 0.36, [(-1.45, 3.5), (-1.7, 5), (-1.5, 7.5), (-2.4, 12)]),
    ("r3", 1.7, 5.4, 0.36, [(1.7, 5.6), (1.95, 7.5), (1.6, 10), (2.2, 15)]),
    ("r4", -0.75, 9, 0.26, [(-0.75, 9.25), (-0.95, 12), (-0.6, 16)]),
    ("r5", 1.0, 13, 0.26, [(1.0, 13.3), (1.3, 17), (1.0, 22)]),
]
if FULL:
    rocks.append(("r0", -0.5, 1.65, 0.42, [(-0.5, 1.8), (-0.25, 2.4), (0.05, 4), (-0.3, 7), (0.2, 11)]))
info = {}
for rid, X, Z, sz, path in rocks:
    pts = smooth(path, 30)
    band, left, right, center = trail(pts, sz * 0.42)
    g = f'<g id="t{rid}"><path d="{band}" fill="#C9B590"/>'
    g += f'<path d="{poly(center)}" fill="none" stroke="#A8916B" stroke-width="{max(1.2, 0.18*F*sz/Z):.1f}" stroke-linecap="round" opacity="0.7"/>'
    g += f'<path d="{poly(left)}" fill="none" stroke="#F7F0E2" stroke-width="{max(1, 0.1*F*sz/Z):.1f}" stroke-linecap="round"/>'
    g += f'<path d="{poly(right)}" fill="none" stroke="#9C8460" stroke-width="{max(1, 0.08*F*sz/Z):.1f}" stroke-linecap="round"/></g>'
    o.append(g)
    info[rid] = (X, Z, sz, center)
o.append('<g id="trailglow">' + f'<path d="{poly(info["r0" if FULL else "r1"][3])}" fill="none" stroke="{LIME}" stroke-width="7" stroke-linecap="round" stroke-dasharray="1 0"/></g>')


def rock(rid, X, Z, sz):
    cx, cy = P(X, Z)
    s = F * sz / Z  # semi-ancho en pantalla
    random.seed(sum(map(ord, rid)) * 7)
    pts = []
    for k in range(9):
        a = math.pi + k * math.pi / 8
        r = s * random.uniform(0.82, 1.05)
        pts.append((cx + r * math.cos(a), cy + r * 0.95 * math.sin(a) * (1.0 if k not in (0, 8) else 0)))
    base = [(cx + s * 0.95, cy + s * 0.08), (cx + s * 0.4, cy + s * 0.2), (cx - s * 0.4, cy + s * 0.2), (cx - s * 0.97, cy + s * 0.06)]
    d = poly(pts + base) + " Z"
    sw = max(2.5, min(7, s * 0.12))
    g = f'<g id="{rid}"><ellipse cx="{cx+s*0.25:.1f}" cy="{cy+s*0.2:.1f}" rx="{s*1.25:.1f}" ry="{s*0.22:.1f}" fill="#6B5A44" opacity="0.35"/>'
    g += f'<path d="{d}" fill="url(#rock)" stroke="{INK}" stroke-width="{sw:.1f}" stroke-linejoin="round"/>'
    g += f'<path d="M {cx-s*0.6:.1f} {cy-s*0.55:.1f} Q {cx-s*0.1:.1f} {cy-s*0.95:.1f} {cx+s*0.45:.1f} {cy-s*0.6:.1f}" fill="none" stroke="#B5AA9E" stroke-width="{max(1.5, s*0.08):.1f}" stroke-linecap="round" opacity="0.9"/>'
    if s > 30:
        g += f'<path d="M {cx-s*0.2:.1f} {cy-s*0.3:.1f} l {s*0.25:.1f} {s*0.25:.1f} M {cx+s*0.3:.1f} {cy-s*0.2:.1f} l {-s*0.1:.1f} {s*0.3:.1f}" stroke="#2A2420" stroke-width="3" stroke-linecap="round" opacity="0.6"/>'
    g += '</g>'
    return g, (cx, cy, s)


rk = {}
for rid, X, Z, sz, _ in sorted(rocks, key=lambda r: -r[2]):
    g, geo = rock(rid, X, Z, sz)
    o.append(g)
    rk[rid] = geo

# instrumentos
cx, cy, s = rk["r1"]
gx, gy = cx + s * 0.05, cy - s * 0.82
o.append(f'<g id="gps"><rect x="{gx-20:.0f}" y="{gy-16:.0f}" width="40" height="24" rx="6" fill="#FFD23F" stroke="{INK}" stroke-width="5"/>'
         f'<line x1="{gx+8:.0f}" y1="{gy-16:.0f}" x2="{gx+14:.0f}" y2="{gy-60:.0f}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
         f'<circle cx="{gx+14:.0f}" cy="{gy-62:.0f}" r="7" fill="{CORAL}" stroke="{INK}" stroke-width="4"/>'
         f'<circle cx="{gx-9:.0f}" cy="{gy-4:.0f}" r="4" fill="#3BD16F"/></g>')
for k in (1, 2):
    o.append(f'<g id="gw{k}"><circle cx="{gx+14:.0f}" cy="{gy-62:.0f}" r="34" fill="none" stroke="{CORAL}" stroke-width="5"/></g>')
# cámara de lapso de tiempo en trípode (izquierda)
o.append(f'<g id="camara">' + stroke2("M 150 470 L 105 640", 7, "#6B6F75", 6) + stroke2("M 150 470 L 150 650", 7, "#6B6F75", 6) + stroke2("M 150 470 L 200 640", 7, "#6B6F75", 6)
         + f'<rect x="102" y="410" width="104" height="66" rx="12" fill="#3C4148" stroke="{INK}" stroke-width="6"/>'
         + f'<rect x="114" y="420" width="44" height="12" rx="4" fill="#6E757E"/>'
         + f'<circle cx="190" cy="443" r="22" fill="#20242A" stroke="{INK}" stroke-width="5"/><circle cx="190" cy="443" r="11" fill="#4F7CC9"/><circle cx="185" cy="438" r="4" fill="#FFFFFF"/>'
         + f'<circle cx="122" cy="458" r="5" fill="{CORAL}"/></g>')
# estación meteorológica (derecha)
o.append(f'<g id="meteo">' + stroke2("M 880 650 L 880 395", 8, "url(#metal)", 6)
         + stroke2("M 880 640 L 838 660 M 880 640 L 922 660", 6, "#8A939C", 6)
         + f'<rect x="840" y="470" width="80" height="50" rx="4" fill="#2F5C9E" stroke="{INK}" stroke-width="5" transform="rotate(-12 880 495)"/>'
         + f'<path d="M 852 485 L 906 474 M 852 500 L 908 489" stroke="#9CC3F5" stroke-width="3" transform="rotate(0)"/>'
         + f'<rect x="868" y="540" width="24" height="32" rx="4" fill="#F2F2F2" stroke="{INK}" stroke-width="5"/></g>')
o.append('<g id="cups">' + stroke2("M 840 392 L 920 392 M 880 372 L 880 412", 4, "#8A939C", 5)
         + "".join(f'<circle cx="{x}" cy="{y}" r="11" fill="#F2F2F2" stroke="{INK}" stroke-width="4"/>' for x, y in ((840, 392), (920, 392), (880, 372), (880, 412)))
         + f'<circle cx="880" cy="392" r="6" fill="{INK}"/></g>')

# etiquetas
mid = info["r1"][3][62]
o.append(tag("lsurco", 330, 215, tw("SURCO"), "SURCO", 400, 273, f"{mid[0]:.0f}", f"{mid[1]:.0f}"))
o.append(tag("lgps", 690, 300, tw("GPS"), "GPS", 700, 352, gx + 20, gy - 66))
o.append(tag("lcamara", 60, 330, tw("CÁMARA"), "CÁMARA", 130, 388, 140, 410))
o.append(tag("lmeteo", 700, 230, tw("VIENTO"), "VIENTO", 840, 288, 862, 380))
if FULL:
    o.append('</g>')
o.append('</svg>')
print("\n".join(o))

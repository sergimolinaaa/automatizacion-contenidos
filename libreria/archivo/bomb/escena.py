import sys, random, math
sys.path.insert(0, '/tmp/claude-0/-home-user-automatizacion-contenidos/039df981-7a17-5355-b711-18510fb209db/scratchpad/bomb')
from lib import *
import beetle as B
import ant as A

BX, BY, BS = 405, 445, 1.05
AX, AY, AS = 735, 489, 1.1
GROUND = 470

defs = B.DEFS + A.DEFS + '''
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFF3DA"/><stop offset="1" stop-color="#E9F1D2"/></linearGradient>
<linearGradient id="soil" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E2BF86"/><stop offset="1" stop-color="#B98A55"/></linearGradient>
<linearGradient id="jet" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFFFFF"/><stop offset="0.5" stop-color="#FFE7B0"/><stop offset="1" stop-color="#FFC27A"/></linearGradient>
<radialGradient id="steamG" cx="0.4" cy="0.35" r="0.7"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#E6ECF2"/></radialGradient>
<linearGradient id="leafG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#D99A45"/><stop offset="1" stop-color="#9C5E22"/></linearGradient>
'''
o = [svg_open(defs)]
o.append('<rect width="1000" height="700" fill="url(#sky)"/>')
# troncos lejanos
for x, w in ((120, 46), (300, 30), (760, 54), (900, 34)):
    o.append(f'<rect x="{x}" y="0" width="{w}" height="{GROUND}" fill="#D9D8C0" opacity="0.8"/>')
    o.append(f'<rect x="{x+6}" y="0" width="{w*0.25:.0f}" height="{GROUND}" fill="#E8E7D2" opacity="0.8"/>')
o.append('<path d="M 0 360 C 120 330, 220 352, 340 336 C 470 318, 600 346, 720 330 C 840 316, 930 336, 1000 326 L 1000 480 L 0 480 Z" fill="#D2E4B8"/>')
o.append('<path d="M 0 410 C 150 392, 260 414, 420 400 C 580 386, 720 412, 860 398 C 930 392, 970 400, 1000 396 L 1000 480 L 0 480 Z" fill="#B9D59C"/>')
# suelo
o.append(f'<path d="M 0 {GROUND} C 200 462, 420 476, 620 466 C 780 460, 900 470, 1000 464 L 1000 700 L 0 700 Z" fill="url(#soil)"/>')
o.append(f'<path d="M 0 {GROUND} C 200 462, 420 476, 620 466 C 780 460, 900 470, 1000 464" fill="none" stroke="#A4794A" stroke-width="4" opacity="0.6"/>')
random.seed(7)
spk = []
for _ in range(140):
    x = random.uniform(10, 990); y = random.uniform(485, 690)
    r = 1.5 + (y - 470) / 220 * 3
    spk.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}"/>')
o.append('<g fill="#8E6236" opacity="0.45">' + "".join(spk) + '</g>')
# piedrecitas lejanas (sin contorno) y cercanas (con contorno)
for x, y, rx, ry in ((90, 500, 16, 7), (610, 492, 12, 5), (930, 498, 18, 7)):
    o.append(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#C9A57A"/>')
# hojas secas cercanas
def leaf(cx, cy, L, ang, col="url(#leafG)"):
    g = f'<g transform="translate({cx} {cy}) rotate({ang})">'
    g += f'<path d="M {-L} 0 C {-L*0.5} {-L*0.42}, {L*0.5} {-L*0.42}, {L} 0 C {L*0.5} {L*0.42}, {-L*0.5} {L*0.42}, {-L} 0 Z" fill="{col}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    g += f'<path d="M {-L*0.95} 0 L {L*0.9} 0" stroke="#7A4614" stroke-width="3"/>'
    for t in (-0.5, -0.1, 0.3):
        g += f'<path d="M {L*t:.0f} 0 L {L*(t+0.25):.0f} {-L*0.25:.0f} M {L*t:.0f} 0 L {L*(t+0.25):.0f} {L*0.25:.0f}" stroke="#7A4614" stroke-width="2.5"/>'
    g += f'<path d="M {-L*0.6:.0f} {-L*0.2:.0f} C {-L*0.2:.0f} {-L*0.32:.0f}, {L*0.2:.0f} {-L*0.32:.0f}, {L*0.5:.0f} {-L*0.22:.0f}" fill="none" stroke="#F3C27A" stroke-width="3" stroke-linecap="round" opacity="0.8"/>'
    return g + '</g>'
o.append(leaf(140, 640, 70, -12))
o.append(leaf(870, 650, 60, 18, "#C7873A"))
o.append(leaf(520, 668, 50, 4, "#B9772E"))
for x, y, rx, ry, c in ((300, 620, 22, 12, "#B7A58F"), (690, 640, 16, 9, "#A8957C"), (980, 560, 20, 10, "#B7A58F"), (40, 560, 18, 9, "#A8957C")):
    o.append(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{c}" stroke="{INK}" stroke-width="4"/>'
             f'<ellipse cx="{x-rx*0.3:.0f}" cy="{y-ry*0.35:.0f}" rx="{rx*0.4:.0f}" ry="{ry*0.25:.0f}" fill="#FFFFFF" opacity="0.5"/>')
# hierbas
def blade(x0, y0, x1, y1, cx, cy, col):
    d = f"M {x0} {y0} Q {cx} {cy} {x1} {y1}"
    return stroke2(d, 7, col, extra=7)
o.append('<g id="grassl">' + blade(30, 560, 60, 360, 20, 450, "#5DAA4E") + blade(60, 560, 110, 400, 90, 470, "#79C463") + blade(48, 562, 6, 420, 30, 480, "#4E9944") + '</g>')
o.append('<g id="grassr">' + blade(972, 640, 985, 470, 995, 560, "#5DAA4E") + blade(958, 642, 930, 520, 940, 590, "#79C463") + '</g>')

# escarabajo
o.append(f'<g transform="translate({BX} {BY}) scale({BS})">' + B.shadow() + B.beetle() + '</g>')

# hormiga (se acerca 60 unidades en "molestas")
PRE = len(sys.argv) > 1
o.append(f'<g transform="translate({AX+(0 if PRE else 60)} {AY}) scale({AS})">' + A.ant() + '</g>')


# chorro: desde la boquilla girada 25° hacia la cabeza de la hormiga
def W(lx, ly):
    return (BX + lx * BS, BY + ly * BS)
nz = rot(214, -2, 156, 0, 25)
N = W(*nz)
H = (AX + 6 * AS, AY + 8 * AS)  # cabeza hormiga (posición final)
mid = ((N[0] + H[0]) / 2, (N[1] + H[1]) / 2 - 18)
o.append('<g id="spray">')
def qp(t):
    return ((1 - t) ** 2 * N[0] + 2 * (1 - t) * t * mid[0] + t * t * H[0], (1 - t) ** 2 * N[1] + 2 * (1 - t) * t * mid[1] + t * t * H[1])
L_, R_ = [], []
for k in range(21):
    t = 0.04 + 0.92 * k / 20
    x, y = qp(t); x2, y2 = qp(t + 0.01)
    dx, dy = x2 - x, y2 - y; ln = math.hypot(dx, dy); nx, ny = -dy / ln, dx / ln
    w = 4 + 16 * t
    L_.append((x + nx * w, y + ny * w)); R_.append((x - nx * w, y - ny * w))
poly = P(L_ + R_[::-1]) + " Z"
o.append(f'<path d="{poly}" fill="url(#jet)" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
core = "M " + " L ".join(f"{qp(0.06+0.85*k/12)[0]:.1f} {qp(0.06+0.85*k/12)[1]-3:.1f}" for k in range(13))
o.append(f'<path d="{core}" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" opacity="0.9"/>')
o.append('</g>')
# gotitas
random.seed(3)
o.append('<g id="mist">')
for i in range(14):
    t = random.uniform(0.25, 1.0)
    x = (1 - t) ** 2 * N[0] + 2 * (1 - t) * t * mid[0] + t * t * H[0]
    y = (1 - t) ** 2 * N[1] + 2 * (1 - t) * t * mid[1] + t * t * H[1]
    x += random.uniform(-10, 10) * (0.5 + t); y += random.uniform(-26, 26) * t
    r = random.uniform(3.5, 6.5)
    o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="#FFE2A6" stroke="{INK}" stroke-width="2.5"/>')
o.append('</g>')
# nube de vapor alrededor de la cabeza de la hormiga
o.append('<g id="steam">')
for (dx, dy, r) in ((-30, -34, 22), (-6, -52, 24), (-44, -60, 16), (20, -70, 18), (-58, -30, 14)):
    o.append(f'<circle cx="{H[0]+dx:.1f}" cy="{H[1]+dy:.1f}" r="{r}" fill="url(#steamG)" stroke="#8B97A6" stroke-width="3.5"/>')
o.append('</g>')
# rayitas de calor
o.append('<g id="heat">')
for k, x in enumerate((H[0] - 34, H[0] + 4, H[0] + 42)):
    yb = H[1] - 92 - (k % 2) * 10
    dd = f"M {x:.0f} {yb:.0f} c -10 -12, 10 -22, 0 -34 c -10 -12, 10 -22, 0 -34"
    o.append(stroke2(dd, 5, CORAL, extra=6))
o.append('</g>')
# etiqueta 100 ºC (arriba a la derecha, sin tapar a nadie)
o.append(tag("hot", 870, 230, "100 °C", bg=CORAL, fg=INK, leader=(H[0] + 20, H[1] - 150)))
# signos de alarma de la hormiga
o.append('<g id="alarm">' + stroke2(f"M {AX+150*AS:.0f} {AY-70:.0f} l 10 -26", 5, INK, extra=0) + stroke2(f"M {AX+170*AS:.0f} {AY-60:.0f} l 20 -18", 5, INK, extra=0) + '</g>')
if PRE:
    o.append('<style>#abdtip{transform-box:fill-box;transform-origin:0% 50%;rotate:25deg}</style>')
o.append('</svg>')
print("\n".join(o))

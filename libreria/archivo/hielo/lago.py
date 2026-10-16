import math, random, sys
sys.path.insert(0, "/tmp/claude-0/-home-user-automatizacion-contenidos/039df981-7a17-5355-b711-18510fb209db/scratchpad/dedos")
from common import *

random.seed(4)
IT, IB = 262, 302  # hielo arriba / abajo
basin = "M 0 252 L 60 256 C 104 300, 140 420, 220 520 C 320 640, 680 646, 780 540 C 860 452, 896 320, 940 256 L 1000 252 L 1000 720 L 0 720 Z"


def bez(p0, p1, p2, p3, t):
    return tuple((1 - t) ** 3 * a + 3 * (1 - t) ** 2 * t * b + 3 * (1 - t) * t ** 2 * c + t ** 3 * d for a, b, c, d in zip(p0, p1, p2, p3))


segs = [((60, 256), (104, 300), (140, 420), (220, 520)), ((220, 520), (320, 640), (680, 646), (780, 540)), ((780, 540), (860, 452), (896, 320), (940, 256))]
floor = [bez(*s, t / 40) for s in segs for t in range(41)]


def floor_y(x):
    best = min(floor, key=lambda p: abs(p[0] - x) + (0 if p[1] > 400 else 1000))
    return best[1]


o = [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 700">
<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#CFE3F2"/><stop offset="1" stop-color="#EEF5FA"/></linearGradient>
<linearGradient id="water" gradientUnits="userSpaceOnUse" x1="0" y1="{IB}" x2="0" y2="640"><stop offset="0" stop-color="#A9DDF8"/><stop offset="1" stop-color="#2A6FB8"/></linearGradient>
<linearGradient id="ice" gradientUnits="userSpaceOnUse" x1="0" y1="{IT}" x2="0" y2="{IB}"><stop offset="0" stop-color="#FFFFFF"/><stop offset="0.4" stop-color="#DDF4FF"/><stop offset="1" stop-color="#A8DCF5"/></linearGradient>
<linearGradient id="earth" gradientUnits="userSpaceOnUse" x1="0" y1="250" x2="0" y2="700"><stop offset="0" stop-color="#9C7650"/><stop offset="1" stop-color="#5E4330"/></linearGradient>
<radialGradient id="snowb" cx="0.35" cy="0.3" r="0.8"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#D5E6F2"/></radialGradient>
</defs>
<rect width="1000" height="700" fill="url(#sky)"/>
<path d="M 0 200 C 140 150, 260 190, 400 160 C 540 130, 700 180, 820 150 C 900 132, 960 150, 1000 140 L 1000 260 L 0 260 Z" fill="#E1ECF4"/>
<path d="M 0 236 C 160 210, 300 232, 460 214 C 620 198, 800 228, 1000 206 L 1000 260 L 0 260 Z" fill="#D2E2EC"/>''']
# pinos lejanos (sin contorno)
for x, h in [(40, 90), (80, 70), (900, 96), (950, 74), (860, 60)]:
    o.append(f'<path d="M {x} {250 - h} L {x + h * 0.3:.0f} 250 L {x - h * 0.3:.0f} 250 Z" fill="#9DBFB0"/>')
# copos (bucle)
o.append('<g id="snow" fill="#FFFFFF">' + "".join(f'<circle cx="{random.randint(360, 980)}" cy="{random.randint(80, 230)}" r="{random.choice([3, 4, 5])}"/>' for _ in range(22)) + '</g>')
# agua (detras del terreno)
o.append(f'<rect x="0" y="{IB}" width="1000" height="{700 - IB}" fill="url(#water)"/>')
o.append(f'<g fill="#FFFFFF" opacity="0.13"><path d="M 300 {IB} L 380 {IB} L 300 640 L 220 640 Z"/><path d="M 600 {IB} L 650 {IB} L 610 640 L 550 640 Z"/></g>')
# burbujas atrapadas bajo el hielo
o.append('<g id="bubs" fill="#FFFFFF" stroke="#7FB9DD" stroke-width="2">' + "".join(f'<ellipse cx="{x}" cy="{IB + 6}" rx="{r * 1.6:.0f}" ry="{r}"/>' for x, r in [(200, 5), (232, 3), (520, 6), (560, 4), (720, 5)]) + '</g>')


def fish(id_, x, y, s, col, flip=False):
    t = f'translate({x} {y}) scale({-s if flip else s} {s})'
    return (f'<g id="{id_}"><g transform="{t}">'
            f'<path d="M 30 0 L 54 -18 L 50 0 L 54 18 Z" fill="{col}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
            f'<path d="M -40 0 C -20 -22, 20 -22, 34 0 C 20 22, -20 22, -40 0 Z" fill="{col}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
            f'<path d="M 0 -15 L 12 -26 L 18 -13" fill="{col}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
            f'<circle cx="-22" cy="-4" r="5" fill="{INK}"/><circle cx="-23.5" cy="-5.5" r="1.8" fill="#FFFFFF"/>'
            f'<path d="M -6 -12 C 0 -4, 0 4, -6 12" fill="none" stroke="{INK}" stroke-width="3" opacity="0.6"/>'
            f'<path d="M -30 -8 C -16 -16, 6 -16, 20 -10" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.7"/></g></g>')


# algas
o.append('<g id="weed">')
for x, h, col in [(300, 120, "#36B37E"), (330, 80, "#2E9C6A"), (690, 110, "#36B37E"), (660, 70, "#5CCB8A")]:
    y0 = floor_y(x) + 6
    d = f"M {x} {y0} C {x - 20} {y0 - h * 0.35:.0f}, {x + 20} {y0 - h * 0.65:.0f}, {x - 4} {y0 - h}"
    o.append(dbl(d, 9, col, 7))
o.append('</g>')
o.append(fish("fish1", 360, 430, 1.05, "#FF9F43", flip=True))
o.append(fish("fish2", 640, 500, 0.9, "#FFD23F"))
o.append(fish("fish3", 520, 380, 0.6, "#FF7A6A", flip=True))
# TAPA DE HIELO (+ muñeco de nieve encima)
o.append('<g id="icesheet">')
o.append(f'<path d="M 20 {IT} L 980 {IT} L 980 {IB} L 20 {IB} Z" fill="url(#ice)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
o.append(f'<path d="M 70 {IT + 7} L 930 {IT + 7}" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>')
o.append(f'<g fill="none" stroke="#7FB9DD" stroke-width="3" stroke-linecap="round"><path d="M 260 {IT + 4} L 276 {IT + 20} L 268 {IB - 6}"/><path d="M 610 {IT + 6} L 596 {IT + 22} L 612 {IB - 4}"/><path d="M 820 {IT + 4} L 832 {IB - 10}"/></g>')
o.append(f'<g fill="#FFFFFF" stroke="{INK}" stroke-width="4"><path d="M 140 {IT} C 160 {IT - 10}, 220 {IT - 10}, 240 {IT} Z"/><path d="M 470 {IT} C 490 {IT - 8}, 540 {IT - 8}, 560 {IT} Z"/></g>')
SX = 760
o.append(f'''<g id="snowman"><ellipse cx="{SX}" cy="{IT}" rx="46" ry="6" fill="#7FB9DD" opacity="0.6"/>
<circle cx="{SX}" cy="{IT - 34}" r="36" fill="url(#snowb)" stroke="{INK}" stroke-width="6"/>
<circle cx="{SX}" cy="{IT - 88}" r="26" fill="url(#snowb)" stroke="{INK}" stroke-width="6"/>
<path d="M {SX - 24} {IT - 70} C {SX - 10} {IT - 62}, {SX + 10} {IT - 62}, {SX + 24} {IT - 70} L {SX + 26} {IT - 58} C {SX + 8} {IT - 52}, {SX - 8} {IT - 52}, {SX - 26} {IT - 58} Z" fill="{CORAL}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>
<path d="M {SX + 14} {IT - 62} L {SX + 22} {IT - 36} L {SX + 34} {IT - 40} L {SX + 26} {IT - 62} Z" fill="{CORAL}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>
<circle cx="{SX}" cy="{IT - 132}" r="20" fill="url(#snowb)" stroke="{INK}" stroke-width="6"/>
<circle cx="{SX - 7}" cy="{IT - 136}" r="3.5" fill="{INK}"/><circle cx="{SX + 7}" cy="{IT - 136}" r="3.5" fill="{INK}"/>
<path d="M {SX} {IT - 130} L {SX + 22} {IT - 126} L {SX} {IT - 124} Z" fill="#FF8A1F" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>
<path d="M {SX - 18} {IT - 148} L {SX + 18} {IT - 148} L {SX + 14} {IT - 176} L {SX - 14} {IT - 176} Z" fill="#2B2D3A" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>
<path d="M {SX - 26} {IT - 148} L {SX + 26} {IT - 148}" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>
<g fill="{INK}"><circle cx="{SX}" cy="{IT - 92}" r="3.5"/><circle cx="{SX}" cy="{IT - 40}" r="4"/><circle cx="{SX}" cy="{IT - 24}" r="4"/></g>
<path d="M {SX - 24} {IT - 92} L {SX - 60} {IT - 118} M {SX - 48} {IT - 110} L {SX - 54} {IT - 124}" stroke="#6E4A2E" stroke-width="5" stroke-linecap="round"/>
<path d="M {SX + 24} {IT - 92} L {SX + 58} {IT - 108}" stroke="#6E4A2E" stroke-width="5" stroke-linecap="round"/></g>''')
o.append('</g>')
# terreno
o.append(f'<path d="{basin}" fill="url(#earth)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
o.append('<g fill="#7A5A3C" opacity="0.8">' + "".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}"/>' for x, y, rx, ry in [(120, 560, 30, 12), (880, 600, 26, 10), (60, 420, 18, 8), (950, 420, 20, 8)]) + '</g>')
# piedras del fondo
for x, rx in [(400, 26), (460, 16), (600, 22)]:
    y = floor_y(x)
    o.append(f'<ellipse cx="{x}" cy="{y - 4:.0f}" rx="{rx}" ry="{rx * 0.55:.0f}" fill="#9AA5AE" stroke="{INK}" stroke-width="5"/>'
             f'<ellipse cx="{x - rx * 0.3:.0f}" cy="{y - 4 - rx * 0.2:.0f}" rx="{rx * 0.35:.0f}" ry="{rx * 0.15:.0f}" fill="#FFFFFF" opacity="0.6"/>')
# nieve en las orillas
o.append(f'<path d="M 0 252 L 60 256 C 70 266, 78 276, 84 286 C 60 276, 30 270, 0 268 Z" fill="#FFFFFF" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
o.append(f'<path d="M 1000 252 L 940 256 C 930 266, 924 276, 918 286 C 942 276, 972 270, 1000 268 Z" fill="#FFFFFF" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')

# etiquetas
o.append(tag("ltapa", 300, 120, "TAPA DE HIELO", lead=(420, 178, 430, 282)))
o.append(tag("l0", 776, 318, "0 °C", fs=28, w=104, lead=(776, 347, 700, 330)))
o.append(tag("l4", 560, 566, "4 °C", fs=28, w=104, lead=(560, 595, 470, 560)))
o.append('</svg>')
print("\n".join(o))

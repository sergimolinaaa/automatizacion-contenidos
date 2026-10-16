import math, random
from lib import *
import octo
defs = (octo.defs("rojo") + lg("bgw", [(0, "#7FC6E8"), (1, "#2A6FB0")]) +
        rg("iris", [(0, "#FFF0B0"), (0.7, "#E9C86A"), (1, "#B8902E")], 0.45, 0.4, 0.7) +
        f'<clipPath id="burb"><circle cx="725" cy="320" r="205"/></clipPath>')
o = [header(defs)]
o.append('<rect width="1000" height="700" fill="url(#bgw)"/>')
o.append('<g fill="#FFFFFF" opacity="0.18">' + "".join(f'<path d="M {x} 0 L {x + 50} 0 L {x + 200} 700 L {x + 120} 700 Z"/>' for x in (420, 760)) + '</g>')
# ---- cabeza del pulpo (primer plano, izquierda) ----
H = ['<g id="cabeza">']
H.append(f'<path d="M -20 120 C 120 60, 300 70, 400 170 C 480 250, 500 390, 450 500 C 410 590, 300 640, 160 650 L -20 660 Z" fill="url(#rojo_mant)" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>')
H.append('<path d="M 40 150 C 140 110, 260 116, 340 170" fill="none" stroke="#FFB59C" stroke-width="9" stroke-linecap="round" opacity="0.85"/>')
random.seed(8)
for _ in range(60):
    x, y = random.uniform(10, 440), random.uniform(150, 630)
    if ((x - 230) ** 2 / 210 ** 2 + (y - 390) ** 2 / 250 ** 2) > 0.9 or (x - 250) ** 2 + (y - 380) ** 2 < 125 ** 2:
        continue
    r = random.uniform(5, 15)
    H.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r:.0f}" ry="{r * 0.7:.0f}" fill="#B52A18" opacity="0.55"/>')
    if random.random() < 0.5:
        H.append(f'<circle cx="{x + 8:.0f}" cy="{y - 6:.0f}" r="3" fill="#FFC2AE"/>')
# brazo en primer plano abajo
d, c, norms, ws = tentacle([(-20, 600), (120, 600), (260, 640), (340, 690)], 110, 50)
H.append(f'<path d="{d}" fill="url(#rojo_arm)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
for i in range(6, len(c) - 4, 4):
    x, y = c[i]; nx, ny = norms[i]
    sx, sy = x + nx * ws[i] * 0.9, y + ny * ws[i] * 0.9
    if ny < 0:
        sx, sy = x - nx * ws[i] * 0.9, y - ny * ws[i] * 0.9
    H.append(f'<circle cx="{sx:.0f}" cy="{sy:.0f}" r="{ws[i] * 0.35:.0f}" fill="#FFD9CC" stroke="{INK}" stroke-width="3"/>')
# cuenca y ojo
H.append(f'<ellipse cx="250" cy="380" rx="128" ry="108" fill="#E2412A" stroke="{INK}" stroke-width="7"/>')
H.append(f'<path d="M 140 330 C 180 270, 320 262, 366 330" fill="none" stroke="#FFB59C" stroke-width="7" stroke-linecap="round" opacity="0.8"/>')
for a in range(-160, -10, 22):
    r = math.radians(a)
    x, y = 250 + 136 * math.cos(r), 380 + 116 * math.sin(r)
    H.append(f'<path d="M {x - 8 * math.sin(r):.0f} {y + 8 * math.cos(r):.0f} L {x + 16 * math.cos(r):.0f} {y + 16 * math.sin(r):.0f} L {x + 8 * math.sin(r):.0f} {y - 8 * math.cos(r):.0f}" fill="#E2412A" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')
H.append('</g>')
o.append("".join(H))
o.append(f'<g id="ojo"><ellipse cx="250" cy="384" rx="100" ry="82" fill="url(#iris)" stroke="{INK}" stroke-width="7"/>'
         f'<rect x="170" y="364" width="160" height="40" rx="20" fill="{INK}"/>'
         f'<path d="M 182 384 L 318 384" stroke="#2A2A3A" stroke-width="6" stroke-linecap="round"/>'
         f'<ellipse cx="208" cy="342" rx="20" ry="11" fill="#FFFFFF" opacity="0.9"/><circle cx="292" cy="420" r="6" fill="#FFFFFF" opacity="0.6"/>'
         '<path d="M 160 350 C 170 330, 190 318, 214 312" stroke="#C9A040" stroke-width="3" fill="none" opacity="0.6"/></g>')
o.append(f'<path d="M 146 380 C 160 300, 340 300, 354 380" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>')
# ---- bocadillo de visión ----
for x, y, r in ((396, 300, 14), (440, 284, 22)):
    o.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/>')
o.append(f'<circle cx="732" cy="330" r="214" fill="#000" opacity="0.2"/>')


def scene(cmap):
    s = []
    s.append(f'<rect x="510" y="110" width="440" height="420" fill="{cmap("#4FB3E8")}"/>')
    s.append(f'<path d="M 510 300 C 600 280, 700 300, 950 280 L 950 530 L 510 530 Z" fill="{cmap("#2F7FD6")}"/>')
    s.append(f'<path d="M 510 450 C 620 430, 760 460, 950 440 L 950 530 L 510 530 Z" fill="{cmap("#E7C487")}" stroke="{INK}" stroke-width="5"/>')
    # coral
    for (x0, y0, x1, y1) in ((600, 460, 570, 360), (600, 460, 630, 350), (600, 420, 650, 400), (590, 400, 560, 390)):
        s.append(dbl(f"M {x0} {y0} L {x1} {y1}", 12, cmap("#FF6A4E"), 7))
    for x, y in ((570, 360), (630, 350), (650, 400), (560, 390)):
        s.append(f'<circle cx="{x}" cy="{y}" r="11" fill="{cmap("#FFB0C8")}" stroke="{INK}" stroke-width="4"/>')
    # alga
    s.append(dbl("M 880 460 C 860 400, 900 360, 870 300 C 860 270, 880 240, 870 220", 11, cmap("#36B37E"), 7))
    s.append(dbl("M 900 460 C 920 410, 890 370, 912 330", 9, cmap("#7BE07B"), 7))
    # peces
    for x, y, col, sc in ((740, 220, "#FFD23F", 1.0), (800, 300, "#B06BFF", 0.8), (690, 330, "#FF8A3D", 0.7)):
        s.append(f'<g transform="translate({x} {y}) scale({sc})"><path d="M -44 0 C -20 -30, 34 -28, 50 0 C 34 28, -20 30, -44 0 Z" fill="{cmap(col)}" stroke="{INK}" stroke-width="5"/>'
                 f'<path d="M -42 0 L -72 -22 L -64 0 L -72 22 Z" fill="{cmap(col)}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
                 f'<path d="M -6 -24 Q 6 0 -6 24" fill="none" stroke="{cmap("#2347FF")}" stroke-width="8"/>'
                 f'<circle cx="28" cy="-6" r="7" fill="#FFFFFF" stroke="{INK}" stroke-width="3"/><circle cx="30" cy="-6" r="3.5" fill="{INK}"/></g>')
    # anémona
    s.append(f'<ellipse cx="760" cy="470" rx="40" ry="14" fill="{cmap("#E85A9A")}" stroke="{INK}" stroke-width="5"/>')
    return "".join(s)


def grey(hexc):
    r, g, b = (int(hexc[i:i + 2], 16) for i in (1, 3, 5))
    l = int(0.3 * r + 0.59 * g + 0.11 * b)
    return f"#{l:02X}{l:02X}{l:02X}"


o.append(f'<g id="vista_gris"><g clip-path="url(#burb)">{scene(grey)}</g></g>')
o.append(f'<g id="vista_color"><g clip-path="url(#burb)">{scene(lambda c: c)}</g></g>')
o.append(f'<circle cx="725" cy="320" r="205" fill="none" stroke="#FFFFFF" stroke-width="16"/><circle cx="725" cy="320" r="214" fill="none" stroke="{INK}" stroke-width="6"/><circle cx="725" cy="320" r="198" fill="none" stroke="{INK}" stroke-width="4"/>')
s_, _ = tag("l_bn", 725, 590, "¿EN BLANCO Y NEGRO?", size=26)
o.append(s_)
o.append(f'<g id="interroga"><circle cx="905" cy="150" r="54" fill="{CORAL}" stroke="{INK}" stroke-width="6"/>' + txt(905, 176, "?", 76, "#FFFFFF") + '</g>')
o.append('</svg>')
open("ojo.svg", "w").write("\n".join(o))

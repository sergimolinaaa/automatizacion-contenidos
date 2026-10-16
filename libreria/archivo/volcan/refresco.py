import sys, math, random
sys.path.insert(0, "/tmp/claude-0/-home-user-automatizacion-contenidos/039df981-7a17-5355-b711-18510fb209db/scratchpad/volcan")
from vlib import *
random.seed(11)
X = 380  # eje de la botella

def half(sg):
    s = lambda dx: X + sg * dx
    return [("M", s(26), 158), ("L", s(26), 204), ("C", s(26), 246, s(100), 252, s(100), 302), ("L", s(100), 372),
            ("Q", s(90), 384, s(100), 396), ("L", s(100), 520), ("Q", s(90), 532, s(100), 544), ("L", s(100), 578),
            ("C", s(100), 608, s(82), 626, s(52), 628)]

def path_bottle():
    L = half(-1); R = half(1)
    d = f"M {L[0][1]} {L[0][2]}"
    for c in L[1:]:
        d += " " + c[0] + " " + " ".join(f"{v:.1f}" for v in c[1:])
    d += f" L {R[-1][-2]:.1f} {R[-1][-1]}"
    # recorrer la mitad derecha al revés
    pts_r = R[::-1]
    prev = pts_r[0]
    for k in range(len(pts_r) - 1):
        c = pts_r[k]; nxt = pts_r[k + 1]
        end = (nxt[-2], nxt[-1])
        if c[0] == "L" or c[0] == "M":
            d += f" L {end[0]:.1f} {end[1]}"
        elif c[0] == "Q":
            d += f" Q {c[1]:.1f} {c[2]} {end[0]:.1f} {end[1]}"
        elif c[0] == "C":
            d += f" C {c[3]:.1f} {c[4]}, {c[1]:.1f} {c[2]}, {end[0]:.1f} {end[1]}"
    return d + " Z"

bottle = path_bottle()
LIQ = 238
defs = "\n".join([
    lg("wall", [(0, "#FFF6EA"), (1, "#F6DDBF")]),
    lg("table", [(0, "#D9A46A"), (1, "#A8703E")]),
    lg("cola", [(0, "#2A1006"), (0.3, "#7A3410"), (0.55, "#6A2C0E"), (1, "#1E0A04")], 0, 0, 1, 0),
    lg("plastic", [(0, "#CFE8F7", 0.3), (0.4, "#FFFFFF", 0.08), (1, "#A9CDE6", 0.3)], 0, 0, 1, 0),
    lg("cap", [(0, "#FF7A5C"), (0.5, "#E8412C"), (1, "#9E2414")], 0, 0, 1, 0),
    lg("label", [(0, "#F2F2F2"), (0.4, "#FFFFFF"), (1, "#CFCFCF")], 0, 0, 1, 0),
    rg("bub", [(0, "#FFFFFF"), (0.6, "#FFF0DC"), (1, "#E7B98F")], 0.38, 0.32, 0.7),
    rg("lens", [(0, "#9A5228"), (1, "#4A220E")], 0.45, 0.4, 0.65),
    f'<clipPath id="botc"><path d="{bottle}"/></clipPath>',
    '<clipPath id="lensc"><circle cx="760" cy="300" r="112"/></clipPath>',
])
o = [head(defs)]
o.append('<rect width="1000" height="700" fill="url(#wall)"/>')
# azulejos
o.append('<g stroke="#E9CFAF" stroke-width="3">' + "".join(f'<path d="M 0 {y} L 1000 {y}"/>' for y in range(100, 600, 100))
         + "".join(f'<path d="M {x + (50 if (y // 100) % 2 else 0)} {y} L {x + (50 if (y // 100) % 2 else 0)} {y + 100}"/>' for y in range(0, 600, 100) for x in range(100, 1000, 100)) + '</g>')
# mesa
o.append(f'<path d="M 0 600 L 1000 600 L 1000 700 L 0 700 Z" fill="url(#table)"/>')
o.append(f'<path d="M 0 600 L 1000 600" stroke="{INK}" stroke-width="6"/><path d="M 0 610 L 1000 610" stroke="#F0C48E" stroke-width="3" opacity="0.8"/>')
o.append('<g stroke="#8A5A30" stroke-width="3" opacity="0.5" fill="none"><path d="M 40 640 C 200 632, 360 650, 520 640"/><path d="M 560 668 C 700 660, 840 676, 980 664"/></g>')
o.append(f'<ellipse cx="{X + 30}" cy="632" rx="140" ry="16" fill="#5A3417" opacity="0.4"/>')
# líquido
o.append('<g clip-path="url(#botc)">')
o.append(f'<rect x="{X - 110}" y="{LIQ}" width="220" height="400" fill="url(#cola)"/>')
o.append(f'<path d="M {X - 110} {LIQ} L {X + 110} {LIQ}" stroke="#B8642E" stroke-width="5"/>')
# gas disuelto: casi invisible
o.append('<g id="disuelto" fill="#FFFFFF" opacity="0.18">' + "".join(
    f'<circle cx="{random.uniform(X - 90, X + 90):.0f}" cy="{random.uniform(LIQ + 20, 600):.0f}" r="2.2"/>' for _ in range(60)) + '</g>')
# burbujas subiendo (ocultas al principio en la escena cerrada)
bb = []
for col in range(7):
    x0 = X - 75 + col * 25
    y = random.uniform(560, 600)
    while y > LIQ + 18:
        r = 3.5 + (600 - y) / 360 * 6 * random.uniform(0.7, 1.1)
        bb.append((x0 + random.uniform(-6, 6), y, r))
        y -= r * 2 + random.uniform(22, 50)
o.append('<g id="burbujas">' + "".join(bubble(x, y, r) for x, y, r in bb) + '</g>')
o.append('</g>')
# etiqueta de la botella
o.append('<g clip-path="url(#botc)">')
o.append(f'<rect x="{X - 110}" y="410" width="220" height="96" fill="url(#label)"/>')
o.append(f'<path d="M {X - 110} 470 C {X - 60} 440, {X - 10} 492, {X + 40} 456 C {X + 70} 436, {X + 95} 450, {X + 110} 444 L {X + 110} 506 L {X - 110} 506 Z" fill="{CORAL}"/>')
o.append(f'<path d="M {X - 110} 410 L {X + 110} 410 M {X - 110} 506 L {X + 110} 506" stroke="{INK}" stroke-width="4"/>')
o.append('</g>')
# plástico + brillos
o.append(f'<path d="{bottle}" fill="url(#plastic)"/>')
o.append(f'<path d="M {X - 68} 320 L {X - 68} 590" stroke="#FFFFFF" stroke-width="12" stroke-linecap="round" opacity="0.55"/>')
o.append(f'<path d="M {X - 46} 262 Q {X - 30} 246, {X - 16} 212" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round" opacity="0.6" fill="none"/>')
o.append(f'<path d="M {X + 70} 330 L {X + 70} 570" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" opacity="0.35"/>')
# pétalos del fondo
o.append('<g fill="none" stroke="#0B0B14" stroke-width="3" opacity="0.5">' + "".join(
    f'<path d="M {X + dx - 18} 626 Q {X + dx} 600, {X + dx + 18} 626"/>' for dx in (-56, 0, 56)) + '</g>')
o.append(f'<path d="{bottle}" fill="none" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
# anillo del cuello
o.append(f'<rect x="{X - 36}" y="182" width="72" height="10" rx="5" fill="#E8E8EE" stroke="{INK}" stroke-width="4"/>')
# presión dentro (cerrada)
o.append('<g id="presion">' + arrow(None, X - 12, 222, X - 52, 206, "#FFFFFF", w=6, head=16) + arrow(None, X + 12, 222, X + 52, 206, "#FFFFFF", w=6, head=16)
         + arrow(None, X, 214, X, 172, "#FFFFFF", w=6, head=16) + '</g>')
# espuma en la boca
fo = [(X - 22, 150, 12), (X - 4, 140, 15), (X + 16, 146, 13), (X + 28, 160, 10), (X - 30, 166, 9), (X + 6, 128, 11), (X - 16, 128, 9), (X + 30, 176, 8), (X - 31, 184, 7)]
o.append('<g id="foam">' + "".join(f'<circle cx="{x}" cy="{y}" r="{r + 4}" fill="{INK}"/>' for x, y, r in fo)
         + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFF6EA"/>' for x, y, r in fo)
         + "".join(f'<circle cx="{x - r * 0.3:.0f}" cy="{y - r * 0.3:.0f}" r="{r * 0.3:.1f}" fill="#FFFFFF"/>' for x, y, r in fo) + '</g>')
# chorros de gas (fsss)
sp = []
for ang, ln in [(-124, 40), (-103, 50), (-77, 50), (-56, 40)]:
    a = math.radians(ang)
    x1, y1 = X + 26 * math.cos(a), 128 + 20 * math.sin(a)
    x2, y2 = X + (26 + ln) * math.cos(a), 128 + (20 + ln * 0.8) * math.sin(a)
    sp.append(f'<path d="M {x1:.1f} {y1:.1f} L {x2:.1f} {y2:.1f}" stroke="{INK}" stroke-width="13" stroke-linecap="round"/>'
              f'<path d="M {x1:.1f} {y1:.1f} L {x2:.1f} {y2:.1f}" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round"/>')
o.append('<g id="spray">' + "".join(sp) + '</g>')
o.append('<g id="drops">' + "".join(bubble(x, y, r, fill="url(#bub)") for x, y, r in [(X - 84, 92, 7), (X + 88, 86, 8), (X - 50, 76, 6), (X + 54, 72, 6)]) + '</g>')
# tapón
o.append(f'<g id="cap"><rect x="{X - 32}" y="112" width="64" height="44" rx="7" fill="url(#cap)" stroke="{INK}" stroke-width="6"/>'
         + "".join(f'<path d="M {X - 24 + k * 8} 120 L {X - 24 + k * 8} 150" stroke="#7A1A0E" stroke-width="3" opacity="0.6"/>' for k in range(7))
         + f'<path d="M {X - 26} 118 L {X + 26} 118" stroke="#FFB4A2" stroke-width="4" stroke-linecap="round"/></g>')
# lupa: CO2 disuelto
o.append('<g id="lupa">')
o.append(f'<path d="M {X + 66} 330 L 657 252 M {X + 66} 380 L 664 360" stroke="{INK}" stroke-width="4" opacity="0.6"/>')
o.append(f'<circle cx="{X + 50}" cy="356" r="24" fill="none" stroke="{INK}" stroke-width="9"/><circle cx="{X + 50}" cy="356" r="24" fill="none" stroke="{LIME}" stroke-width="4"/>')
o.append('<circle cx="760" cy="300" r="112" fill="url(#lens)"/>')
o.append('<g clip-path="url(#lensc)">')
for x, y, a in [(705, 245, 20), (790, 228, -35), (760, 300, 70), (690, 330, -15), (835, 300, 10), (765, 375, 40), (840, 375, -60), (680, 270, 80)]:
    o.append(f'<g transform="translate({x} {y}) rotate({a})"><circle cx="-24" cy="0" r="12" fill="#FF4B3E" stroke="{INK}" stroke-width="3.5"/><circle cx="24" cy="0" r="12" fill="#FF4B3E" stroke="{INK}" stroke-width="3.5"/><circle cx="0" cy="0" r="13" fill="#3A3A44" stroke="{INK}" stroke-width="3.5"/><circle cx="-28" cy="-4" r="3.5" fill="#FFFFFF" opacity="0.7"/><circle cx="20" cy="-4" r="3.5" fill="#FFFFFF" opacity="0.7"/></g>')
o.append('</g>')
o.append(f'<circle cx="760" cy="300" r="112" fill="none" stroke="{INK}" stroke-width="10"/><circle cx="760" cy="300" r="105" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.5"/>')
o.append('</g>')
o.append(label("lgas", 760, 100, "GAS DISUELTO", 760, 188, anchor="center"))
o.append(label("lburb", 610, 480, "BURBUJAS", X + 60, 500))
t, _ = tag("lfsss", 500, 96, "¡FSSS!", bg=LIME, fg=INK)
o.append(t)
o.append(label("lpresion", 560, 180, "PRESIÓN", X + 40, 204))
o.append('</svg>')
open(sys.argv[1], "w").write("\n".join(o))

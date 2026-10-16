import sys, math, random
sys.path.insert(0, "/tmp/claude-0/-home-user-automatizacion-contenidos/039df981-7a17-5355-b711-18510fb209db/scratchpad/volcan")
from vlib import *
random.seed(7)
G = 420          # nivel del suelo
CX = 460         # eje del conducto
cone = (f"M 120 {G} C 250 {G - 18}, 370 300, 420 194 L 440 188 Q {CX} 198 480 188 L 500 194 "
        f"C 550 300, 670 {G - 18}, 800 {G} Z")

def hw(y):  # semiancho del conducto
    return 24 + (556 - y) / (556 - 192) * 16 + 2.5 * math.sin(y / 23)

ys_ = list(range(556, 191, -12)) + [192]
left = [(CX - hw(y), y) for y in ys_]
right = [(CX + hw(y), y) for y in reversed(ys_)]
conduit = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in left + right) + " Z"
wl = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in left if y <= 541)
wr = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in right if y <= 541)

ch = [(CX + 232 * math.cos(a) * (1 + 0.05 * math.sin(3 * a)), 588 + 54 * math.sin(a) * (1 + 0.08 * math.cos(2 * a))) for a in [k * 2 * math.pi / 18 for k in range(18)]]
chd = [(CX + 232 * math.cos(a) * (1 + 0.05 * math.sin(3 * a)), 588 + 54 * math.sin(a) * (1 + 0.08 * math.cos(2 * a))) for a in [k * 2 * math.pi / 240 for k in range(240)]]
chamber = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in chd) + " Z"
MOUTH = 24 + (556 - 540) / (556 - 192) * 16
# contorno sin la boca del conducto: empieza justo a la derecha de la boca y da la vuelta
i0 = max(i for i, (x, y) in enumerate(chd) if y < 560 and x <= CX + MOUTH + 1 and x >= CX)
seq = chd[i0:] + chd[:i0]
seq = [p for p in seq if not (p[1] < 560 and abs(p[0] - CX) < MOUTH - 1)]
chamber_line = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in seq)

defs = "\n".join([
    lg("sky", [(0, "#9ACDF2"), (1, "#E6F4FF")]),
    lg("crust", [(0, "#9C7B62"), (1, "#4B372C")]),
    rg("magma", [(0, "#FFE27A"), (0.45, "#FF9A3C"), (0.85, "#E5432A"), (1, "#B32A1A")], 0.5, 0.4, 0.6),
    rg("halo", [(0, "#FF7A3A", 0.55), (1, "#FF7A3A", 0)]),
    lg("lavav", [(0, "#FFD34D"), (0.5, "#FF8A3D"), (1, "#FF7A36")]),
    rg("bub", [(0, "#FFFFFF"), (0.6, "#FFF1C9"), (1, "#FFD08A")], 0.38, 0.32, 0.7),
    rg("lump", [(0, "#F4F1EC"), (0.55, "#B9B3B2"), (1, "#6E6870")], 0.4, 0.34, 0.66),
    rg("burst", [(0, "#FFF59A"), (0.6, "#FFB03A"), (1, "#FF5A36")]),
    lg("gauge", [(0, "#FFFFFF"), (1, "#FF5A36")]),
    rg("lens", [(0, "#FFC15A"), (1, "#F05A2C")], 0.45, 0.4, 0.65),
    f'<clipPath id="conec"><path d="{cone}"/></clipPath>',
    '<clipPath id="lensc"><circle cx="790" cy="250" r="92"/></clipPath>',
])
o = [head(defs)]
o.append('<rect width="1000" height="700" fill="url(#sky)"/>')
o.append('<g fill="#FFFFFF" opacity="0.8"><ellipse cx="620" cy="110" rx="70" ry="16"/><ellipse cx="655" cy="98" rx="40" ry="16"/></g>')
# montañas lejanas
o.append(f'<path d="M 0 {G} L 0 360 L 70 330 L 140 370 Z M 760 {G} L 870 350 L 940 380 L 1000 360 L 1000 {G} Z" fill="#C7D7E6"/>')
# subsuelo en bandas
bands = [("#A98A6E", G), ("#94765D", 470), ("#7E634F", 530), ("#664F40", 600), ("#523F34", 660)]
for k, (col, y0) in enumerate(bands):
    d = f"M 0 {y0} " + " ".join(f"L {x} {y0 + 6 * math.sin(x / 70 + k):.1f}" for x in range(0, 1001, 50)) + " L 1000 700 L 0 700 Z"
    o.append(f'<path d="{d}" fill="{col}"/>')
    if k:
        o.append(f'<path d="{d.split(" L 1000 700")[0]}" fill="none" stroke="#3B2C24" stroke-width="3" opacity="0.5"/>')
# piedrecitas en el subsuelo
for _ in range(45):
    x, y = random.uniform(20, 980), random.uniform(440, 690)
    if ((x - CX) / 260) ** 2 + ((y - 588) / 80) ** 2 < 1 or abs(x - CX) < 50:
        continue
    r = random.uniform(4, 9)
    o.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r:.1f}" ry="{r * 0.6:.1f}" fill="#3B2C24" opacity="0.35"/>')
# volcán cortado: estratos
o.append(f'<g clip-path="url(#conec)">')
cols = ["#8E715D", "#B39478", "#7A604F", "#A88B71", "#6F5646", "#9D8068", "#644D40", "#8E715D"]
for k, c in enumerate(cols):
    o.append(f'<path d="{cone}" fill="{c}" transform="translate(0 {k * 30})"/>')
o.append('</g>')
o.append(f'<path d="M 0 {G} L 1000 {G}" stroke="{INK}" stroke-width="6"/>')
o.append(f'<path d="{cone}" fill="none" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
# hierba en superficie
o.append(f'<path d="M 0 {G - 3} L 128 {G - 3}" stroke="#5BBF6A" stroke-width="7"/><path d="M 792 {G - 3} L 1000 {G - 3}" stroke="#5BBF6A" stroke-width="7"/>')
o.append(f'<path d="M 0 {G} L 1000 {G}" stroke="{INK}" stroke-width="3" transform="translate(0 -8)" opacity="0"/>')
# conducto
o.append(f'<g id="conduit"><path d="{conduit}" fill="url(#lavav)"/><path d="{wl}" fill="none" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/><path d="{wr}" fill="none" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
         f'<path d="M {CX - 12} 520 L {CX - 18} 210" stroke="#FFF2B0" stroke-width="4" stroke-linecap="round" opacity="0.6"/></g>')
# tapa la unión conducto-cámara
# halo de calor y cámara magmática
o.append(f'<ellipse cx="{CX}" cy="588" rx="300" ry="110" fill="url(#halo)"/>')
o.append(f'<g id="chamber"><path d="{chamber}" fill="url(#magma)"/><path d="{chamber_line}" fill="none" stroke="{INK}" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"/>'
         f'<path d="M {CX - 170} 556 C {CX - 90} 542, {CX + 60} 540, {CX + 160} 552" fill="none" stroke="#FFF2B0" stroke-width="5" stroke-linecap="round" opacity="0.7"/></g>')
# lava en el cráter
o.append(f'<path d="M 436 190 Q {CX} 200 484 190" fill="none" stroke="#FFD34D" stroke-width="8" stroke-linecap="round"/>')
# gas disuelto (puntitos)
dots = []
for _ in range(70):
    a, rr = random.uniform(0, 2 * math.pi), math.sqrt(random.uniform(0, 1))
    x, y = CX + 205 * rr * math.cos(a), 590 + 40 * rr * math.sin(a)
    dots.append((x, y))
for y in range(520, 440, -16):
    dots.append((CX + random.uniform(-12, 12), y))
o.append('<g id="disuelto">' + "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.2" fill="#FFFFFF" stroke="#B32A1A" stroke-width="1.2"/>' for x, y in dots) + '</g>')
# capa "espesa" (magma viscoso)
vpath = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in left if y <= 541) + " L " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in right if y <= 541) + " Z"
o.append(f'<g id="viscoso"><path d="{vpath}" fill="#8A2A1A" opacity="0.45"/>'
         + "".join(f'<path d="M {CX - 14} {y} Q {CX} {y + 10} {CX + 14} {y}" fill="none" stroke="#5A1A10" stroke-width="3" opacity="0.5"/>' for y in range(250, 520, 34)) + '</g>')
# burbujas creciendo hacia arriba
bub = []
y, k = 490, 0
while y > 225:
    t = (490 - y) / (490 - 225)
    r = 4 + 19 * t ** 1.3
    xoff = (9 if k % 2 else -9) * (1 - t * 0.6)
    bub.append((CX + xoff, y, r))
    y -= r * 2 + 6
    k += 1
thirds = [bub[: len(bub) // 3], bub[len(bub) // 3: 2 * len(bub) // 3], bub[2 * len(bub) // 3:]]
o.append('<g id="burbujas">' + "".join(f'<g id="bb{i + 1}">' + "".join(bubble(x, y, r) for x, y, r in th) + '</g>' for i, th in enumerate(thirds)) + '</g>')
# presión (flechas blancas)
o.append('<g id="presion">' + arrow(None, 330, 600, 290, 560, "#FFFFFF", w=8, head=22) + arrow(None, 590, 600, 630, 560, "#FFFFFF", w=8, head=22)
         + arrow(None, CX, 330, CX, 262, "#FFFFFF", w=8, head=22) + '</g>')
# flecha de subida
o.append(arrow("sube", 545, 500, 545, 250, LIME, w=10, head=28))
# explosión: destello, penacho y bombas
sb = []
for k in range(16):
    a = math.pi + k * math.pi / 15
    r = 120 if k % 2 == 0 else 60
    sb.append((CX + r * math.cos(a), 190 + r * math.sin(a) * 0.95))
o.append(f'<g id="burst"><path d="M {CX - 70} 196 L ' + " L ".join(f"{x:.1f} {y:.1f}" for x, y in sb) + f' L {CX + 70} 196 Z" fill="url(#burst)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/></g>')
lumps = [(460, 168, 30), (472, 142, 38), (448, 122, 40), (420, 112, 36), (500, 112, 40), (380, 130, 32), (548, 128, 34), (590, 146, 26), (342, 150, 24), (462, 100, 30)]
order = sorted(lumps, key=lambda l: l[1])
o.append('<g id="plume">' + "".join(f'<circle cx="{x}" cy="{y}" r="{r + 6}" fill="{INK}"/>' for x, y, r in lumps)
         + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#lump)"/>' for x, y, r in order) + '</g>')
def rock(x, y, r, rot):
    p = [(x + r * (1 + 0.2 * math.sin(k * 2.3 + rot)) * math.cos(k * math.pi / 4 + rot), y + r * (1 + 0.2 * math.sin(k * 2.3 + rot)) * math.sin(k * math.pi / 4 + rot)) for k in range(8)]
    return f'<path d="{smooth(p, True)}" fill="#3A2C28" stroke="{INK}" stroke-width="5"/><circle cx="{x - r * 0.3:.1f}" cy="{y - r * 0.3:.1f}" r="{r * 0.25:.1f}" fill="#FF8A3D"/>'
o.append('<g id="bombs">' + rock(300, 190, 13, 0.2) + rock(625, 175, 14, 1.0) + rock(655, 240, 10, 2.2) + rock(270, 250, 10, 0.6) + '</g>')
# manómetro de presión (izquierda)
o.append('<g id="gauge">')
o.append(f'<rect x="64" y="160" width="40" height="370" rx="20" fill="url(#gauge)" stroke="{INK}" stroke-width="6"/>')
o.append(f'<path d="M 74 180 L 74 500" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity="0.6"/>')
t1, _ = tag("_", 44, 88, "PRESIÓN", bg="#FFFFFF", fg=INK)
o.append(t1.replace('<g id="_">', '').replace('</g>', ''))
t2, _ = tag("_", 118, 168, "BAJA", bg="#FFFFFF", fg=INK, size=24, h=46)
t3, _ = tag("_", 118, 478, "ALTA", bg=CORAL, fg=INK, size=24, h=46)
o.append((t2 + t3).replace('<g id="_">', '').replace('</g>', ''))
o.append('</g>')
# lupa: vapor de agua disuelto en el magma
o.append('<g id="lupa">')
o.append(f'<path d="M 726 316 L 590 562 M 868 290 L 620 566" stroke="{INK}" stroke-width="4" opacity="0.7"/>')
o.append(f'<circle cx="605" cy="572" r="22" fill="none" stroke="{INK}" stroke-width="9"/><circle cx="605" cy="572" r="22" fill="none" stroke="{LIME}" stroke-width="4"/>')
o.append('<circle cx="790" cy="250" r="92" fill="url(#lens)"/>')
o.append('<g clip-path="url(#lensc)">')
for k, (x, y, a) in enumerate([(745, 205, 20), (820, 190, -30), (790, 262, 60), (735, 290, -10), (850, 270, 15), (790, 330, 40), (700, 250, 0), (875, 215, 70)]):
    o.append(f'<g transform="translate({x} {y}) rotate({a})"><circle cx="-14" cy="11" r="8" fill="#FFFFFF" stroke="{INK}" stroke-width="3"/><circle cx="14" cy="11" r="8" fill="#FFFFFF" stroke="{INK}" stroke-width="3"/><circle cx="0" cy="0" r="14" fill="#2F7FD6" stroke="{INK}" stroke-width="3.5"/><circle cx="-5" cy="-5" r="4" fill="#FFFFFF" opacity="0.7"/></g>')
o.append('</g>')
o.append(f'<circle cx="790" cy="250" r="92" fill="none" stroke="{INK}" stroke-width="10"/><circle cx="790" cy="250" r="86" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.6"/>')
o.append('</g>')
o.append(label("lvapor", 790, 98, "VAPOR DE AGUA", 790, 158, anchor="center"))
# etiquetas
o.append(label("lmagma", 40, 592, "MAGMA", 262, 600))
o.append(label("lgas", 700, 592, "GAS DISUELTO", 632, 612))
o.append(label("lburb", 590, 360, "BURBUJAS", 476, 320))
o.append(label("lespeso", 222, 296, "ESPESO", 438, 340))
o.append('</svg>')
open(sys.argv[1], "w").write("\n".join(o))

import sys, math
sys.path.insert(0, "/tmp/claude-0/-home-user-automatizacion-contenidos/039df981-7a17-5355-b711-18510fb209db/scratchpad/volcan")
from vlib import *

def bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u**3*p0[0]+3*u*u*t*p1[0]+3*u*t*t*p2[0]+t**3*p3[0], u**3*p0[1]+3*u*u*t*p1[1]+3*u*t*t*p2[1]+t**3*p3[1])

L = [(110, 620), (260, 575), (390, 430), (448, 238)]
R = [(552, 238), (610, 430), (740, 575), (890, 620)]
cone = (f"M {L[0][0]} {L[0][1]} C {L[1][0]} {L[1][1]}, {L[2][0]} {L[2][1]}, {L[3][0]} {L[3][1]} "
        f"L 472 228 Q 500 240 528 228 L 552 238 "
        f"C {R[1][0]} {R[1][1]}, {R[2][0]} {R[2][1]}, {R[3][0]} {R[3][1]} Z")

defs = "\n".join([
    lg("sky", [(0, "#8EC5F0"), (0.55, "#CFE6F7"), (1, "#FFE4C4")]),
    lg("cone", [(0, "#A08572"), (0.5, "#7A6253"), (1, "#4A3A33")], 0, 0, 1, 0),
    lg("ground", [(0, "#8CCB6A"), (1, "#4E8F45")]),
    lg("far1", [(0, "#BCCBDB"), (1, "#D7E1EA")]),
    lg("far2", [(0, "#A9C3A2"), (1, "#C2D6B9")]),
    '<linearGradient id="ash" gradientUnits="userSpaceOnUse" x1="0" y1="50" x2="0" y2="240"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/><stop offset="0.5" stop-color="#8C8690" stop-opacity="0.2"/><stop offset="1" stop-color="#3E3842"/></linearGradient>',
    rg("lump", [(0, "#F4F1EC"), (0.55, "#B9B3B2"), (1, "#7A7379")], 0.4, 0.34, 0.66),
    rg("glow", [(0, "#FFF2A8"), (0.45, "#FFB03A"), (1, "#FF5A36", 0)]),
    lg("lava", [(0, "#FFD34D"), (1, "#FF5A36")]),
    rg("rock", [(0, "#6B5B55"), (1, "#2A2224")], 0.35, 0.3, 0.75),
    f'<clipPath id="conec"><path d="{cone}"/></clipPath>',
])
o = [head(defs)]
o.append('<rect width="1000" height="700" fill="url(#sky)"/>')
# nubes lejanas
o.append('<g id="clouds" fill="#FFFFFF" opacity="0.75">'
         '<ellipse cx="150" cy="150" rx="90" ry="20"/><ellipse cx="200" cy="136" rx="60" ry="22"/>'
         '<ellipse cx="860" cy="250" rx="80" ry="16"/><ellipse cx="900" cy="238" rx="48" ry="18"/></g>')
# montañas lejanas (sin contorno)
o.append('<path d="M 0 520 L 90 455 L 170 500 L 260 430 L 340 490 L 420 470 L 560 480 L 660 440 L 760 485 L 860 420 L 1000 480 L 1000 700 L 0 700 Z" fill="url(#far1)"/>')
o.append('<path d="M 0 560 C 120 520, 220 548, 330 530 C 450 512, 560 540, 680 525 C 800 510, 900 535, 1000 520 L 1000 700 L 0 700 Z" fill="url(#far2)"/>')
# lava (flujo por el flanco derecho) — se dibuja antes del contorno del cono para que quede sobre la ladera
flow = [(536, 236), (552, 262), (566, 300), (574, 340), (590, 380), (606, 420), (626, 462), (646, 505), (664, 548), (676, 590)]
fd = smooth(flow)
# volcán
o.append(f'<path d="{cone}" fill="url(#cone)"/>')
o.append('<g clip-path="url(#conec)">')
# sombra lado derecho
o.append('<path d="M 500 230 C 520 330, 560 470, 610 640 L 900 640 L 900 200 Z" fill="#2A1F1C" opacity="0.28"/>')
# estratos/cárcavas
for k, (sx, ex) in enumerate([(458, 170), (468, 250), (480, 330), (490, 410), (510, 560), (522, 650), (534, 740), (545, 820)]):
    o.append(f'<path d="M {sx} 245 Q {(sx + ex) / 2 + (8 if ex > 500 else -8)} 430 {ex} 640" fill="none" stroke="#2E2420" stroke-width="4" opacity="0.35"/>')
import random
random.seed(3)
for _ in range(38):
    y = random.uniform(270, 520); 
    t = (y - 238) / (620 - 238)
    xl = 448 - (448 - 110) * t ** 1.6; xr = 552 + (890 - 552) * t ** 1.6
    x = random.uniform(xl + 20, xr - 20)
    if abs(x - (552 + (676 - 552) * t)) < 30: continue
    rx = random.uniform(5, 11)
    o.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rx:.1f}" ry="{rx * 0.45:.1f}" fill="#3A2C26" opacity="0.35"/>')
    o.append(f'<ellipse cx="{x - 1:.0f}" cy="{y - 2:.0f}" rx="{rx * 0.6:.1f}" ry="{rx * 0.2:.1f}" fill="#C9AE97" opacity="0.5"/>')
# bandas de vegetación en la base
o.append('<path d="M 100 560 C 250 540, 380 520, 500 530 C 640 520, 760 545, 900 560 L 900 700 L 100 700 Z" fill="#5E8F4E" opacity="0.85"/>')
o.append('<path d="M 100 545 C 250 528, 380 508, 500 518 C 640 508, 760 530, 900 545" fill="none" stroke="#7FB069" stroke-width="5" opacity="0.8"/>')
o.append('</g>')
o.append(f'<path d="{cone}" fill="none" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
o.append('<path d="M 160 600 C 280 560, 395 420, 452 250" fill="none" stroke="#C9AE97" stroke-width="5" stroke-linecap="round" opacity="0.7"/>')
# brillo del cráter
o.append('<g id="glow"><ellipse cx="500" cy="232" rx="78" ry="30" fill="url(#glow)"/>'
         f'<path d="M 472 228 Q 500 240 528 228" fill="none" stroke="#FFD34D" stroke-width="7" stroke-linecap="round"/></g>')
# colada de lava
o.append('<g id="lavaflow">'
         f'<path d="{fd}" fill="none" stroke="{INK}" stroke-width="30" stroke-linecap="round" stroke-linejoin="round"/>'
         f'<path d="{fd}" fill="none" stroke="#FF5A36" stroke-width="19" stroke-linecap="round" stroke-linejoin="round"/>'
         '<ellipse cx="680" cy="596" rx="30" ry="11" fill="#FF5A36" stroke="#0B0B14" stroke-width="6"/>'
         '</g>')
o.append(f'<g id="lavacore"><path d="{fd}" fill="none" stroke="#FFD34D" stroke-width="7" stroke-linecap="round"/></g>')
# penacho de ceniza
lumps = [(500, 214, 32), (514, 190, 40), (492, 168, 46), (516, 152, 50),
         (360, 174, 36), (690, 176, 38), (430, 172, 46), (612, 170, 48), (472, 158, 50), (560, 158, 52),
         (404, 142, 46), (454, 126, 56), (522, 124, 58), (592, 128, 56), (648, 146, 46)]
o.append('<g id="plume">')
o.append('<g>' + "".join(f'<circle cx="{x}" cy="{y}" r="{r + 6}" fill="{INK}"/>' for x, y, r in lumps) + '</g>')
order = sorted(lumps, key=lambda l: l[1])
o.append('<g>' + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#lump)"/>' for x, y, r in order) + '</g>')
o.append('<g opacity="0.55">' + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#ash)"/>' for x, y, r in order) + '</g>')
# base incandescente del penacho
o.append('<ellipse cx="500" cy="222" rx="26" ry="12" fill="#FF8A3D" opacity="0.8"/>')
o.append('</g>')
# rayo volcánico
zz = [(560, 108), (540, 142), (562, 146), (534, 190)]
zd = "M " + " L ".join(f"{x} {y}" for x, y in zz)
o.append(f'<g id="rayo"><path d="{zd}" fill="none" stroke="{INK}" stroke-width="15" stroke-linejoin="round" stroke-linecap="round"/>'
         f'<path d="{zd}" fill="none" stroke="#FFF59A" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"/></g>')
# bombas volcánicas
def rock(x, y, r, rot):
    pts_ = [(x + r * (1 + 0.18 * math.sin(k * 2.3 + rot)) * math.cos(k * math.pi / 4 + rot), y + r * (1 + 0.18 * math.sin(k * 2.3 + rot)) * math.sin(k * math.pi / 4 + rot)) for k in range(8)]
    return (f'<path d="{smooth(pts_, True)}" fill="url(#rock)" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
            f'<path d="M {x - r * 0.4:.1f} {y + r * 0.1:.1f} L {x + r * 0.05:.1f} {y - r * 0.15:.1f} L {x + r * 0.4:.1f} {y + r * 0.25:.1f}" fill="none" stroke="#FF8A3D" stroke-width="3" stroke-linecap="round"/>')
def trail(x, y):
    return f'<path d="M 500 226 Q {(500 + x) / 2:.0f} {min(y, 226) - 60:.0f} {x} {y}" fill="none" stroke="#7A6A62" stroke-width="5" stroke-linecap="round" opacity="0.45"/>'
o.append('<g id="bombsl">' + trail(330, 252) + trail(270, 318) + rock(330, 252, 15, 0.3) + rock(270, 318, 12, 1.1) + '</g>')
o.append('<g id="bombsr">' + trail(720, 236) + trail(770, 300) + rock(720, 236, 16, 0.7) + rock(770, 300, 12, 2.0) + '</g>')
# ceniza que cae
o.append('<g id="ashfall" fill="#6E6870" opacity="0.6">' + "".join(
    f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x, y, r in [(700, 220, 3), (730, 260, 2.5), (690, 280, 3), (750, 230, 2), (720, 320, 2.5), (660, 245, 2), (770, 270, 3)]) + '</g>')
# suelo en primer plano
o.append('<path d="M 0 612 C 150 596, 300 618, 470 606 C 640 594, 820 616, 1000 600 L 1000 700 L 0 700 Z" fill="url(#ground)"/>')
o.append(f'<path d="M 0 612 C 150 596, 300 618, 470 606 C 640 594, 820 616, 1000 600" fill="none" stroke="{INK}" stroke-width="6"/>')
o.append('<path d="M 0 622 C 150 606, 300 628, 470 616 C 640 604, 820 626, 1000 610" fill="none" stroke="#B5E08E" stroke-width="3" opacity="0.7"/>')
# pinos
def pine(x, y, h, col="#2F7A4A"):
    w = h * 0.42
    s = f'<rect x="{x - 5}" y="{y - h * 0.18:.0f}" width="10" height="{h * 0.2:.0f}" fill="#6B4A2E" stroke="{INK}" stroke-width="4"/>'
    for k, f in enumerate([0, 0.28, 0.52]):
        top = y - h + f * h * 0.55
        bot = y - h * 0.15 - (2 - k) * h * 0.18
        ww = w * (1 - f * 0.55)
        s += f'<path d="M {x} {top:.0f} L {x + ww:.0f} {bot:.0f} L {x - ww:.0f} {bot:.0f} Z" fill="{col}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
        s += f'<path d="M {x} {top + 6:.0f} L {x - ww * 0.7:.0f} {bot - 4:.0f}" stroke="#6FC27E" stroke-width="3" opacity="0.8"/>'
    return s
o.append('<g id="trees">' + "".join(pine(x, y, h) for x, y, h in [(48, 640, 96), (110, 650, 120), (178, 642, 84), (250, 654, 70)]) + '</g>')
# pueblo
def house(x, y, w, h, roof="#D9553B"):
    return (f'<rect x="{x}" y="{y - h}" width="{w}" height="{h}" fill="#FFF6E6" stroke="{INK}" stroke-width="4"/>'
            f'<path d="M {x - 6} {y - h} L {x + w / 2} {y - h - h * 0.75:.0f} L {x + w + 6} {y - h} Z" fill="{roof}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
            f'<rect x="{x + w * 0.3:.0f}" y="{y - h * 0.62:.0f}" width="{w * 0.4:.0f}" height="{h * 0.35:.0f}" fill="#7FC3F0" stroke="{INK}" stroke-width="3"/>')
o.append('<g id="town">' + house(840, 648, 50, 34) + house(900, 652, 44, 30, "#B8462F") + house(790, 652, 38, 26) + '</g>')
# regla de altura (Pinatubo)
o.append('<g id="altura">')
o.append(arrow(None, 805, 560, 805, 96, "#FFFFFF", w=8, head=26))
for y in range(520, 120, -80):
    o.append(f'<path d="M 790 {y} L 820 {y}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>')
o.append('</g>')
t35, _ = tag("l35", 832, 96, "35 KM", bg=LIME, fg=INK)
o.append(t35)
o.append(label("lceniza", 110, 232, "CENIZA", 372, 196))
o.append('</svg>')
open(sys.argv[1], "w").write("\n".join(o))

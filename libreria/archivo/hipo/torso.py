import sys, math, random
sys.path.insert(0, "/tmp/claude-0/-home-user-automatizacion-contenidos/039df981-7a17-5355-b711-18510fb209db/scratchpad/volcan")
from vlib import *
random.seed(2)

# --- curva superior del diafragma (dos cúpulas) ---
DP = [(318, 590), (340, 540), (372, 500), (420, 476), (468, 486), (500, 498), (532, 488), (580, 480), (628, 504), (660, 542), (682, 592)]
def D(x):
    for (x0, y0), (x1, y1) in zip(DP, DP[1:]):
        if x0 <= x <= x1:
            t = (x - x0) / (x1 - x0)
            # interpolación suave (coseno)
            t = (1 - math.cos(t * math.pi)) / 2
            return y0 + (y1 - y0) * t
    return DP[-1][1]
dtop = smooth(DP)
TH = 18
dbot_pts = [(x, y + TH) for x, y in DP]
dband = dtop + " L " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in [(DP[-1][0], DP[-1][1] + TH)]) + " " + smooth(dbot_pts[::-1]).replace("M", "L", 1) + " Z"
EXT = 40  # extensión oculta de los pulmones bajo el diafragma

def lung(side):
    s = side  # -1 = pulmón derecho (a la izquierda del dibujo), +1 = izquierdo
    if s < 0:
        up = [(474, D(474) + 4), (481, 430), (484, 370), (480, 318), (468, 284), (450, 264), (428, 268), (398, 290), (372, 330), (354, 390), (344, 450), (338, D(338) + 2)]
        xs = list(range(338, 475, 6))
    else:
        up = [(586, D(586) + 2), (566, 470), (548, 438), (528, 408), (520, 360), (520, 318), (532, 284), (550, 264), (572, 268), (602, 290), (628, 330), (646, 390), (656, 450), (662, D(662) + 2)]
        up = up[::-1]
        xs = list(range(586, 663, 6))
    top = smooth(up)
    if s < 0:
        bottom = [(x, D(x) + EXT) for x in xs]
        d = top + " L " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in bottom) + " Z"
    else:
        bottom = [(x, D(x) + EXT) for x in xs]
        d = top + " L " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in bottom) + " Z"
    return d

L1, L2 = lung(-1), lung(1)
body = ("M 472 158 L 472 214 C 440 232, 380 236, 330 250 C 296 260, 276 286, 268 330 L 248 655 L 752 655 L 732 330 "
        "C 724 286, 704 260, 670 250 C 620 236, 560 232, 528 214 L 528 158 Z")
torso_in = "M 336 300 C 360 262, 430 246, 500 244 C 570 246, 640 262, 664 300 L 690 655 L 310 655 Z"

defs = "\n".join([
    lg("bg", [(0, "#EAF4FF"), (1, "#CFE3F7")]),
    lg("skin", [(0, "#F6CDB0"), (1, "#E3A884")], 0, 0, 1, 0),
    rg("face", [(0, "#FBD9C0"), (1, "#E4A783")], 0.4, 0.35, 0.7),
    lg("cav", [(0, "#F9E3D3"), (1, "#F1CBB4")]),
    rg("lungR", [(0, "#FF9DB0"), (0.5, "#E9637E"), (1, "#A8344E")], 0.35, 0.3, 0.75),
    rg("lungL", [(0, "#FF9DB0"), (0.5, "#E9637E"), (1, "#A8344E")], 0.65, 0.3, 0.75),
    lg("dia", [(0, "#E2585A"), (1, "#A8323C")]),
    rg("liver", [(0, "#C2604E"), (1, "#7E2E26")], 0.4, 0.3, 0.8),
    rg("stom", [(0, "#FFD0C2"), (1, "#E58C7C")], 0.4, 0.3, 0.8),
    rg("heart", [(0, "#F05A5A"), (1, "#9E1E2A")], 0.4, 0.35, 0.75),
    lg("cart", [(0, "#F4F8FB"), (1, "#BCD0DE")], 0, 0, 1, 0),
    lg("lumen", [(0, "#8A2F45"), (1, "#5A1A2C")]),
    lg("muc", [(0, "#F7A8B0"), (1, "#E07A88")], 0, 0, 1, 0),
    lg("fold", [(0, "#FFFFFF"), (1, "#EADFD4")]),
    f'<clipPath id="bodyc"><path d="{body}"/></clipPath>',
    '<clipPath id="lensc"><circle cx="812" cy="250" r="140"/></clipPath>',
])
o = [head(defs)]
o.append('<rect width="1000" height="700" fill="url(#bg)"/>')
o.append('<g fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.6"><circle cx="500" cy="400" r="300"/><circle cx="500" cy="400" r="420"/></g>')
# cuerpo
o.append(f'<path d="{body}" fill="url(#skin)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
# brazos (línea interna)
o.append(f'<path d="M 318 340 C 312 420, 306 540, 302 655 M 682 340 C 688 420, 694 540, 698 655" fill="none" stroke="#B9785A" stroke-width="5" stroke-linecap="round"/>')
# cavidad torácica/abdominal (piel transparente)
o.append(f'<path d="{torso_in}" fill="url(#cav)" stroke="#D49A7C" stroke-width="4"/>')
# costillas tenues detrás
o.append('<g fill="none" stroke="#E7B9A0" stroke-width="8" stroke-linecap="round" opacity="0.7">' + "".join(
    f'<path d="M 494 {y} C {440 - k * 6} {y - 10}, {372 - k * 5} {y + 4}, {350 - k * 3} {y + 40 + k * 4}"/><path d="M 506 {y} C {560 + k * 6} {y - 10}, {628 + k * 5} {y + 4}, {650 + k * 3} {y + 40 + k * 4}"/>'
    for k, y in enumerate(range(290, 470, 34))) + '</g>')
# corazón (detrás de los pulmones, en la escotadura)
o.append(f'<g id="heart"><path d="M 486 410 C 476 372, 520 352, 548 372 C 576 368, 600 400, 584 440 C 572 470, 560 486, 548 498 C 520 494, 494 470, 486 440 Z" fill="url(#heart)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
         f'<path d="M 500 394 C 512 378, 532 374, 546 380" fill="none" stroke="#FF9A9A" stroke-width="5" stroke-linecap="round"/></g>')
# pulmones
def lobes(side):
    if side < 0:
        return ('<path d="M 352 420 C 390 400, 430 390, 474 360" fill="none" stroke="#B2475E" stroke-width="4" stroke-linecap="round"/>'
                '<path d="M 346 470 C 390 450, 430 440, 470 430" fill="none" stroke="#B2475E" stroke-width="4" stroke-linecap="round"/>')
    return '<path d="M 650 440 C 610 410, 570 380, 528 330" fill="none" stroke="#B2475E" stroke-width="4" stroke-linecap="round"/>'
def bronchi(side):
    s = side
    hx = 474 if s < 0 else 526
    out = ""
    for (ox, dy, l) in [(0.8, -0.7, 70), (1, -0.1, 90), (0.9, 0.5, 95), (0.45, 0.9, 100), (0.7, 0.9, 80)]:
        x1, y1 = hx + s * ox * l, 352 + dy * l
        if s > 0 and y1 > 400 and x1 < 575:  # escotadura cardiaca
            x1 += 30
        segs = [(hx, 352, x1, y1), (x1, y1, x1 + s * ox * 30 + s * 8, y1 + dy * 30 + 10), (x1, y1, x1 + s * ox * 26 - s * 6, y1 + dy * 26 - 14)]
        for x0, y0, xa, ya in segs:
            out += f'<path d="M {x0:.0f} {y0:.0f} L {xa:.0f} {ya:.0f}" stroke="#FFE0E5" stroke-width="5" stroke-linecap="round" opacity="0.85"/>'
    return out
o.append('<g id="lungs">')
for d, g, s in [(L1, "lungR", -1), (L2, "lungL", 1)]:
    o.append(f'<path d="{d}" fill="url(#{g})" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
    o.append(lobes(s))
    o.append(bronchi(s))
o.append('<path d="M 380 312 C 396 288, 418 274, 440 270" fill="none" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round" opacity="0.7"/>')
o.append('<path d="M 560 270 C 584 274, 604 288, 620 312" fill="none" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round" opacity="0.7"/>')
o.append('</g>')
# tráquea y bronquios principales
tr = []
o.append('<g id="trachea">')
o.append(f'<path d="M 500 232 L 500 318 M 500 318 L 474 352 M 500 318 L 526 352" fill="none" stroke="{INK}" stroke-width="34" stroke-linecap="round" stroke-linejoin="round"/>')
o.append('<path d="M 500 232 L 500 318 M 500 318 L 474 352 M 500 318 L 526 352" fill="none" stroke="#DDEAF2" stroke-width="22" stroke-linecap="round" stroke-linejoin="round"/>')
o.append('<g stroke="#9DB6C8" stroke-width="4">' + "".join(f'<path d="M 490 {y} L 510 {y}"/>' for y in range(240, 312, 10)) + '</g>')
o.append('<path d="M 494 236 L 494 312" stroke="#FFFFFF" stroke-width="4" opacity="0.8"/>')
o.append('</g>')
# aire que entra
o.append('<g id="airin">' + arrow(None, 500, 238, 500, 300, LIME, w=8, head=20) + arrow(None, 470, 360, 420, 410, LIME, w=8, head=20) + arrow(None, 530, 360, 580, 410, LIME, w=8, head=20) + '</g>')
# nervios frénicos (desde el cuello hasta el diafragma)
nl = smooth([(474, 214), (466, 262), (468, 320), (480, 380), (480, 440), (462, 482)])
nr = smooth([(526, 214), (536, 262), (534, 320), (548, 366), (590, 410), (598, 478)])
o.append('<g id="nerves">' + "".join(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="12" stroke-linecap="round"/><path d="{d}" fill="none" stroke="#FFD84A" stroke-width="5" stroke-linecap="round"/>' for d in (nl, nr)) + '</g>')
# abdomen (se mueve con el diafragma)
abd_fill = dtop + " L 700 700 L 300 700 Z"
o.append('<g id="abdomen">')
o.append(f'<g clip-path="url(#bodyc)"><path d="{abd_fill}" fill="url(#cav)"/></g>')
liver = smooth([(330, 600), (342, 548), (372, 512), (420, 494), (468, 504), (500, 516), (526, 530), (520, 556), (480, 580), (420, 610), (360, 632)], True)
o.append(f'<path d="{liver}" fill="url(#liver)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
o.append('<path d="M 360 540 C 390 516, 430 506, 470 512" fill="none" stroke="#E08A76" stroke-width="5" stroke-linecap="round" opacity="0.8"/>')
o.append('<g id="stomach">')
stom = smooth([(560, 512), (600, 500), (640, 516), (662, 556), (658, 604), (628, 640), (580, 648), (540, 632), (530, 602), (556, 592), (590, 600), (612, 584), (606, 548), (574, 532)], True)
o.append(f'<path d="{stom}" fill="url(#stom)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
o.append('<path d="M 580 512 C 606 506, 630 516, 644 534" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity="0.7"/>')
o.append('<g id="gasbub">' + "".join(bubble(x, y, r, fill="#FFFFFF") for x, y, r in [(600, 530, 9), (626, 548, 12), (640, 580, 8), (618, 572, 6)]) + '</g>')
o.append('</g>')
# diafragma
o.append(f'<g id="diaphragm"><path d="{dband}" fill="url(#dia)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
fib = []
for x in range(334, 670, 14):
    if abs(x - 500) < 6:
        continue
    y = D(x)
    fib.append(f'<path d="M {x} {y + 4:.1f} L {x + 3} {y + TH - 4:.1f}" stroke="#7E1E28" stroke-width="2.5" opacity="0.55"/>')
o.append("".join(fib))
o.append(f'<path d="{dtop}" fill="none" stroke="#FFB2B0" stroke-width="3" opacity="0.8" transform="translate(0 4)"/>')
o.append('</g>')
o.append('</g>')
# cuello y cabeza
o.append(f'<path d="M 472 150 L 472 214 L 528 214 L 528 150" fill="url(#skin)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
# laringe
o.append(f'<g id="larynx"><path d="M 482 176 L 518 176 L 512 210 Q 500 218 488 210 Z" fill="url(#cart)" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
         f'<path d="M 492 182 L 500 196 L 508 182" fill="none" stroke="#9DB6C8" stroke-width="3"/><rect x="486" y="214" width="28" height="12" rx="5" fill="url(#cart)" stroke="{INK}" stroke-width="4"/></g>')
# cabeza
o.append(f'<g id="headg">')
o.append(f'<ellipse cx="436" cy="110" rx="12" ry="18" fill="#E9AE8A" stroke="{INK}" stroke-width="6"/><ellipse cx="564" cy="110" rx="12" ry="18" fill="#E9AE8A" stroke="{INK}" stroke-width="6"/>')
o.append(f'<ellipse cx="500" cy="104" rx="64" ry="72" fill="url(#face)" stroke="{INK}" stroke-width="7"/>')
o.append(f'<path d="M 438 92 C 430 50, 470 30, 504 34 C 548 36, 574 60, 564 96 C 548 72, 520 64, 496 70 C 470 64, 450 76, 438 92 Z" fill="#4A2E22" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
o.append('<path d="M 470 50 C 490 42, 520 42, 540 52" fill="none" stroke="#7A5040" stroke-width="5" stroke-linecap="round"/>')
o.append(f'<g id="eyes"><ellipse cx="476" cy="104" rx="10" ry="12" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/><ellipse cx="524" cy="104" rx="10" ry="12" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/>'
         f'<circle cx="478" cy="106" r="5" fill="{INK}"/><circle cx="522" cy="106" r="5" fill="{INK}"/><circle cx="476" cy="103" r="1.8" fill="#FFFFFF"/><circle cx="520" cy="103" r="1.8" fill="#FFFFFF"/></g>')
o.append(f'<path d="M 462 86 Q 476 80 488 86 M 512 86 Q 524 80 538 86" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>')
o.append('<ellipse cx="462" cy="128" rx="10" ry="6" fill="#F49A8A" opacity="0.6"/><ellipse cx="538" cy="128" rx="10" ry="6" fill="#F49A8A" opacity="0.6"/>')
o.append(f'<path d="M 500 112 Q 494 124 502 126" fill="none" stroke="#B9785A" stroke-width="3.5" stroke-linecap="round"/>')
o.append(f'<g id="mouth"><ellipse cx="500" cy="146" rx="9" ry="11" fill="#7A2030" stroke="{INK}" stroke-width="4"/></g>')
o.append('</g>')
# bocadillo ¡HIC!
o.append(f'<g id="hic"><path d="M 240 158 L 404 150 L 408 166 L 468 150 L 410 192 L 412 208 L 248 216 Z" fill="{LIME}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
         f'<text x="324" y="199" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="42" fill="{INK}" transform="rotate(-3 324 186)">¡HIC!</text></g>')
# lupa: corte frontal (coronal) de la laringe
LX, LY, LR = 812, 250, 140
GAP = 30
def half(y):
    # semiancho de la luz (aire) según la altura relativa a la glotis (y=0)
    pts_ = [(-160, 50), (-90, 46), (-58, 44), (-40, 38), (-26, 48), (-12, 58), (36, 58), (50, 40), (90, 42), (160, 44)]
    for (y0, h0), (y1, h1) in zip(pts_, pts_[1:]):
        if y0 <= y <= y1:
            t = (1 - math.cos((y - y0) / (y1 - y0) * math.pi)) / 2
            return h0 + (h1 - h0) * t
    return 44
ys = list(range(-160, 161, 2))
o.append('<g id="lupa">')
o.append(f'<path d="M 516 192 L {LX - LR * 0.95:.0f} {LY - LR * 0.3:.0f} M 514 212 L {LX - LR * 0.86:.0f} {LY + LR * 0.5:.0f}" stroke="{INK}" stroke-width="4" opacity="0.6"/>')
o.append(f'<circle cx="500" cy="200" r="26" fill="none" stroke="{INK}" stroke-width="8"/><circle cx="500" cy="200" r="26" fill="none" stroke="{LIME}" stroke-width="3.5"/>')
o.append(f'<circle cx="{LX}" cy="{LY}" r="{LR}" fill="#FBE3D2"/>')
o.append('<g clip-path="url(#lensc)">')
o.append(f'<rect x="{LX - 150}" y="{LY - 150}" width="300" height="300" fill="#DDF1FF"/>')
# cuerdas vocales (debajo de las paredes, para que su base quede siempre tapada)
def fold(s):
    tip = LX + s * GAP
    base = LX + s * 100
    d = (f"M {base} {LY - 12} C {LX + s * 46} {LY - 10}, {tip + s * 14} {LY - 4}, {tip} {LY + 6} "
         f"C {tip + s * 10} {LY + 18}, {LX + s * 44} {LY + 34}, {base} {LY + 40} Z")
    return (f'<path d="{d}" fill="url(#fold)" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
            f'<path d="M {LX + s * 56} {LY + 6} C {LX + s * 44} {LY + 12}, {LX + s * 34} {LY + 18}, {LX + s * 30} {LY + 24}" fill="none" stroke="#D8607A" stroke-width="10" stroke-linecap="round" opacity="0.5"/>'
            f'<path d="M {LX + s * 60} {LY - 6} C {LX + s * 40} {LY - 6}, {tip + s * 14} {LY - 2}, {tip + s * 5} {LY + 3}" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/>')
o.append('<g id="foldl">' + fold(-1) + '</g>')
o.append('<g id="foldr">' + fold(1) + '</g>')
for s_ in (-1, 1):
    inner = [(LX + s_ * half(y), LY + y) for y in ys]
    muc = [(LX + s_ * (half(y) + (22 if -36 < y < 46 else 16)), LY + y) for y in ys]
    # mucosa (rosa) entre la luz y el cartílago
    d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in inner) + f" L {LX + s_ * 160} {LY + 160} L {LX + s_ * 160} {LY - 160} Z"
    o.append(f'<path d="{d}" fill="url(#muc)"/>')
    # cartílagos: tiroides (arriba) y cricoides (abajo)
    o.append(f'<path d="M {LX + s_ * 92} {LY - 150} L {LX + s_ * 84} {LY + 50} L {LX + s_ * 120} {LY + 50} L {LX + s_ * 128} {LY - 150} Z" fill="url(#cart)" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')
    o.append(f'<path d="M {LX + s_ * 70} {LY + 62} L {LX + s_ * 70} {LY + 100} L {LX + s_ * 104} {LY + 100} L {LX + s_ * 104} {LY + 62} Z" fill="url(#cart)" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')
    for yy in (LY + 116, LY + 140):
        o.append(f'<rect x="{min(LX + s_ * 66, LX + s_ * 98)}" y="{yy}" width="32" height="14" rx="6" fill="url(#cart)" stroke="{INK}" stroke-width="3.5"/>')
    o.append(f'<path d="M {inner[0][0]:.1f} {inner[0][1]:.1f} ' + " ".join(f"L {x:.1f} {y:.1f}" for x, y in inner[1:]) + f'" fill="none" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    o.append(f'<path d="M {LX + s_ * 136} {LY - 160} L {LX + s_ * 136} {LY + 160}" stroke="#E7B9A0" stroke-width="6"/>')
o.append('</g>')
o.append('<g id="airlupa">' + arrow(None, LX, LY - 112, LX, LY + 104, LIME, w=8, head=22) + '</g>')
sb = []
for k in range(14):
    a = k * 2 * math.pi / 14
    r = 36 if k % 2 == 0 else 18
    sb.append((LX + r * math.cos(a), LY + 6 + r * math.sin(a) * 0.8))
o.append(f'<g id="golpe"><path d="M ' + " L ".join(f"{x:.1f} {y:.1f}" for x, y in sb) + f' Z" fill="{CORAL}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/></g>')
o.append(f'<circle cx="{LX}" cy="{LY}" r="{LR}" fill="none" stroke="{INK}" stroke-width="10"/><circle cx="{LX}" cy="{LY}" r="{LR - 7}" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.5"/>')
o.append('</g>')
o.append(label("lglotis", 836, 412, "GLOTIS", LX + 8, LY + 10))
# etiquetas
o.append(label("lpul", 40, 330, "PULMONES", 362, 380))
o.append(label("ltra", 40, 220, "TRÁQUEA", 486, 276))
o.append(label("ldia", 52, 546, "DIAFRAGMA", 352, 530))
o.append('<g id="bajar">' + arrow(None, 420, 520, 420, 590, CORAL, w=9, head=22) + arrow(None, 590, 524, 590, 594, CORAL, w=9, head=22) + '</g>')
o.append(label("lest", 772, 580, "ESTÓMAGO", 640, 600))
o.append(label("lner", 790, 494, "NERVIOS", 588, 440))
o.append('</svg>')
open(sys.argv[1], "w").write("\n".join(o))

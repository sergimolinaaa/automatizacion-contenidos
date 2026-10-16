"""Fig. 1 · Géiser en erupción (cuenca tipo Yellowstone)."""
import math, random
from lib import *

G = 548          # base del cono
VX, VY = 520, 470  # boca del géiser
TOPY = 78        # techo del chorro (≈ 55 m)

defs = """
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9FD3FF"/><stop offset="0.7" stop-color="#DDF0FF"/><stop offset="1" stop-color="#F4F8FF"/></linearGradient>
<linearGradient id="ground" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#EFE8D8"/><stop offset="1" stop-color="#CBBE9F"/></linearGradient>
<linearGradient id="cone" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FBF8EF"/><stop offset="0.5" stop-color="#DCD3BE"/><stop offset="1" stop-color="#B5A684"/></linearGradient>
<linearGradient id="jetg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#CFEAFF"/><stop offset="0.45" stop-color="#FFFFFF"/><stop offset="1" stop-color="#A9D8FA"/></linearGradient>
<radialGradient id="pool" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#1E8FB8"/><stop offset="0.45" stop-color="#3DBFD0"/><stop offset="0.62" stop-color="#9BE0C8"/><stop offset="0.75" stop-color="#F2D14E"/><stop offset="0.9" stop-color="#E8833A"/><stop offset="1" stop-color="#B85A2A"/></radialGradient>
<linearGradient id="bison" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7A5638"/><stop offset="1" stop-color="#3A2618"/></linearGradient>
<linearGradient id="cape" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#A57A4E"/><stop offset="1" stop-color="#5E3F28"/></linearGradient>
<linearGradient id="wood" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#C79A64"/><stop offset="1" stop-color="#8A6238"/></linearGradient>
<radialGradient id="dropg" cx="0.35" cy="0.3" r="0.8"><stop offset="0" stop-color="#FFFFFF"/><stop offset="0.5" stop-color="#BFE6FF"/><stop offset="1" stop-color="#5FAEE8"/></radialGradient>
"""
o = [svg_open(defs)]
o.append('<rect width="1000" height="700" fill="url(#sky)"/>')
# montañas lejanas
o.append('<path d="M 0 360 L 90 300 L 170 330 L 270 270 L 380 320 L 470 290 L 560 330 L 680 280 L 790 320 L 880 290 L 1000 330 L 1000 450 L 0 450 Z" fill="#C3D3E2"/>')
o.append('<path d="M 0 400 L 120 360 L 230 385 L 340 350 L 470 390 L 600 365 L 730 392 L 860 362 L 1000 388 L 1000 450 L 0 450 Z" fill="#AFC4D6"/>')
# pinos lejanos (sin contorno)
random.seed(2)
def pine(x, base, h, col):
    w = h * 0.22
    return f'<path d="M {f(x)} {f(base - h)} L {f(x + w)} {f(base - h * 0.35)} L {f(x + w * 0.6)} {f(base - h * 0.38)} L {f(x + w * 1.2)} {f(base)} L {f(x - w * 1.2)} {f(base)} L {f(x - w * 0.6)} {f(base - h * 0.38)} L {f(x - w)} {f(base - h * 0.35)} Z" fill="{col}"/>'
row = []
x = -10
while x < 1020:
    row.append(pine(x, 446, random.uniform(50, 80), "#9DBFA8"))
    x += random.uniform(16, 26)
o.append("".join(row))
row = []
x = -6
while x < 1020:
    if not 400 < x < 640:
        row.append(pine(x, 462, random.uniform(60, 96), "#6F9C80"))
    x += random.uniform(20, 32)
o.append("".join(row))
# suelo de sínter
o.append(f'<path d="M 0 452 C 200 444, 400 458, 600 448 C 760 442, 880 452, 1000 446 L 1000 700 L 0 700 Z" fill="url(#ground)"/>')
o.append(f'<path d="M 0 452 C 200 444, 400 458, 600 448 C 760 442, 880 452, 1000 446" fill="none" stroke="#B7AA8C" stroke-width="3"/>')
# tapetes de bacterias en los regueros (sin contorno, capas)
for col, wd in [("#B85A2A", 46), ("#E8833A", 34), ("#F2C14E", 20), ("#E9F3E8", 6)]:
    o.append(f'<path d="M 470 540 C 420 580, 330 590, 250 640 C 200 670, 120 690, 60 720" fill="none" stroke="{col}" stroke-width="{wd}" stroke-linecap="round" opacity="0.9"/>')
    o.append(f'<path d="M 580 542 C 640 570, 700 600, 760 660 C 790 690, 820 700, 840 720" fill="none" stroke="{col}" stroke-width="{wd * 0.8}" stroke-linecap="round" opacity="0.9"/>')
# terrazas de sínter
o.append('<g fill="none" stroke="#C9BC9C" stroke-width="3">' + "".join(
    f'<path d="M {x} {y} q 30 -8 60 0 q 30 8 60 0"/>' for x, y in [(60, 500), (300, 492), (720, 500), (840, 530), (130, 600), (900, 610)]) + '</g>')
# poza caliente (estilo Grand Prismatic)
o.append(f'<ellipse cx="820" cy="512" rx="120" ry="26" fill="url(#pool)" stroke="{INK}" stroke-width="6"/>')
o.append('<ellipse cx="800" cy="505" rx="50" ry="7" fill="#FFFFFF" opacity="0.35"/>')
o.append('<g id="poolfog"><g fill="#FFFFFF" opacity="0.6"><ellipse cx="800" cy="486" rx="56" ry="13"/><ellipse cx="860" cy="472" rx="38" ry="10"/></g></g>')

# cono del géiser
cone = f"M 380 {G} C 420 528, 460 486, 498 {VY} L 542 {VY} C 580 486, 620 528, 662 {G} C 600 {G + 10}, 440 {G + 10}, 380 {G} Z"
o.append(f'<ellipse cx="{VX}" cy="{G + 8}" rx="170" ry="14" fill="#8C7B5C" opacity="0.4"/>')
o.append(f'<path d="{cone}" fill="url(#cone)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
o.append('<g fill="none" stroke="#A8987A" stroke-width="3" stroke-linecap="round">' + "".join(
    f'<path d="M {VX - w} {y} q {w / 2} 6 {w} 0 q {w / 2} -6 {w} 0"/>' for w, y in [(40, 488), (64, 506), (88, 524), (110, 540)]) + '</g>')
o.append(f'<path d="M 420 530 C 446 506, 470 484, 500 476" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" opacity="0.8"/>')
o.append(f'<ellipse cx="{VX}" cy="{VY}" rx="24" ry="7" fill="#3E7FB8" stroke="{INK}" stroke-width="5"/>')
# agua que escurre por el cono
o.append(f'<g id="runoff"><path d="M 504 476 C 480 500, 440 520, 400 546 M 540 478 C 570 500, 610 524, 646 546" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/></g>')
# vapor tranquilo (antes de la erupción)
o.append(f'<g id="puff"><g fill="#FFFFFF" opacity="0.85"><ellipse cx="{VX - 6}" cy="{VY - 22}" rx="26" ry="16"/><ellipse cx="{VX + 14}" cy="{VY - 48}" rx="22" ry="14"/><ellipse cx="{VX - 4}" cy="{VY - 76}" rx="16" ry="11"/></g></g>')

# chorro de la erupción: columna «nube» hecha de círculos (contorno común)
random.seed(9)
circ = []
n = 26
for k in range(n + 1):
    t = k / n
    y = VY - 6 - (VY - 6 - TOPY - 40) * t
    cx = VX + 26 * t ** 2
    r = 16 + 40 * t ** 1.5
    circ.append((cx, y, r * 1.0))
    if t > 0.25:
        circ.append((cx - r * 0.55, y + random.uniform(-6, 6), r * random.uniform(0.5, 0.7)))
        circ.append((cx + r * 0.55, y + random.uniform(-6, 6), r * random.uniform(0.5, 0.7)))
for dx, dy, r in [(-70, 30, 46), (-20, 6, 56), (40, 4, 58), (96, 26, 48), (10, 40, 50), (-40, 50, 40), (70, 52, 42)]:
    circ.append((VX + 26 + dx, TOPY + dy + 30, r))
o.append('<g id="jet">')
o.append('<g fill="#0B0B14">' + "".join(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r + 6)}"/>' for x, y, r in circ) + '</g>')
o.append('<g fill="#FFFFFF">' + "".join(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}"/>' for x, y, r in circ) + '</g>')
o.append('<g fill="#D6ECFB">' + "".join(f'<circle cx="{f(x + r * 0.35)}" cy="{f(y + r * 0.3)}" r="{f(r * 0.55)}"/>' for x, y, r in circ[::2]) + '</g>')
o.append('<g fill="none" stroke="#9FD2F5" stroke-width="5" stroke-linecap="round">' + "".join(
    f'<path d="M {f(VX + dx)} {VY - 24} C {f(VX + dx * 1.3)} 360, {f(VX + dx * 2 + 10)} 250, {f(VX + dx * 3 + 24)} {TOPY + 70}"/>' for dx in (-8, 0, 8)) + '</g>')
o.append(f'<path d="M {VX - 10} {VY - 24} C {VX - 16} 360, {VX - 26} 250, {VX - 40} {TOPY + 80}" fill="none" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round"/>')
o.append("".join(f'<circle cx="{f(VX + dx)}" cy="{f(y)}" r="{r}" fill="url(#dropg)" stroke="{INK}" stroke-width="3"/>'
                 for dx, y, r in [(-118, 190, 8), (-104, 262, 6), (-82, 340, 7), (150, 200, 7), (128, 280, 8), (100, 350, 6), (-60, 410, 5), (70, 420, 5)]))
o.append('</g>')
# nubes de vapor arrastradas por el viento (a la derecha)
def cloud(cx, cy, s):
    cs = [(cx - 40 * s, cy, 30 * s), (cx, cy - 18 * s, 40 * s), (cx + 44 * s, cy, 32 * s), (cx + 5 * s, cy + 12 * s, 34 * s)]
    return ('<g fill="#C9DCEA">' + "".join(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r + 4)}"/>' for x, y, r in cs) + '</g>'
            '<g fill="#FFFFFF">' + "".join(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}"/>' for x, y, r in cs) + '</g>')
o.append('<g id="steam"><g opacity="0.9">' + cloud(VX + 200, 110, 1.0) + cloud(VX + 300, 170, 0.75) + cloud(VX + 380, 110, 0.6) + '</g></g>')

# bisonte (primer plano, izquierda), mirando a la derecha; patas hasta el suelo y=640
BY = 640
def bleg(x0, y0, x1, w, col):
    d = f"M {x0} {y0} C {x0 + 2} {y0 + 30}, {x1 - 2} {BY - 30}, {x1} {BY - 6}"
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w + 7}" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>'
            f'<path d="M {x1 - w / 2 - 1} {BY - 10} L {x1 + w / 2 + 3} {BY - 10} L {x1 + w / 2 + 5} {BY} L {x1 - w / 2 - 2} {BY} Z" fill="#1A120C" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')
o.append('<g id="bison">')
o.append(f'<ellipse cx="190" cy="{BY + 2}" rx="125" ry="9" fill="#6E5F44" opacity="0.4"/>')
def leg2(pts, w, col):
    d = pts_d(pts)
    x1 = pts[-1][0]
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w + 7}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="M {x1 - w / 2} {BY - 10} L {x1 + w / 2 + 2} {BY - 10} L {x1 + w / 2 + 4} {BY} L {x1 - w / 2 - 2} {BY} Z" fill="#1A120C" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')
o.append(leg2([(148, 590), (140, 616), (146, BY - 8)], 13, "#24170F") + leg2([(222, 590), (218, 616), (222, BY - 8)], 14, "#24170F"))
body = ("M 84 566 C 84 540, 100 528, 130 524 C 160 516, 178 490, 206 484 C 236 480, 256 494, 266 512 "
        "C 270 540, 268 580, 252 600 L 120 602 C 96 600, 84 588, 84 566 Z")
o.append(f'<path d="{body}" fill="url(#bison)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
o.append('<path d="M 176 494 C 200 480, 240 482, 262 504 C 272 530, 270 570, 258 598 L 248 588 L 240 600 L 230 588 L 220 598 L 210 584 C 196 560, 186 530, 176 494 Z" fill="url(#cape)"/>')
o.append('<path d="M 186 492 C 206 482, 236 484, 254 498" fill="none" stroke="#D2AE84" stroke-width="4" stroke-linecap="round" opacity="0.8"/>')
o.append('<path d="M 112 530 C 130 524, 150 518, 168 504" fill="none" stroke="#9C7652" stroke-width="3" stroke-linecap="round" opacity="0.7"/>')
o.append(f'<path d="M 86 552 C 74 562, 72 578, 76 590" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/><ellipse cx="76" cy="594" rx="5" ry="9" fill="#24170F" stroke="{INK}" stroke-width="3"/>')
o.append(leg2([(124, 592), (114, 616), (122, BY - 8)], 15, "#3A2618") + leg2([(240, 588), (236, 616), (242, BY - 8)], 17, "#5E3F28"))
o.append('<path d="M 230 594 L 228 612 M 238 596 L 238 614 M 246 594 L 248 612" stroke="#3A2618" stroke-width="3" stroke-linecap="round"/>')
head = "M 256 516 C 280 506, 306 516, 314 540 C 320 562, 318 584, 306 594 C 296 602, 280 604, 270 596 C 258 584, 250 548, 256 516 Z"
o.append(f'<path d="M 272 594 C 266 612, 276 628, 288 618 C 294 610, 296 600, 294 594 Z" fill="#24170F" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')
o.append(f'<path d="{head}" fill="#33221A" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
o.append('<path d="M 262 522 C 278 512, 296 516, 306 528" fill="none" stroke="#6B4A33" stroke-width="5" stroke-linecap="round"/>')
o.append(f'<path d="M 272 520 C 272 502, 284 494, 296 498" fill="none" stroke="{INK}" stroke-width="10" stroke-linecap="round"/><path d="M 272 520 C 272 502, 284 494, 296 498" fill="none" stroke="#EDE5D3" stroke-width="5" stroke-linecap="round"/>')
o.append(f'<ellipse cx="260" cy="530" rx="7" ry="5" fill="#33221A" stroke="{INK}" stroke-width="3"/>')
o.append(f'<circle cx="296" cy="548" r="5" fill="{INK}"/><circle cx="294.5" cy="546.5" r="1.8" fill="#FFFFFF"/>')
o.append(f'<path d="M 312 572 C 316 578, 314 586, 308 588" fill="none" stroke="{INK}" stroke-width="3"/><circle cx="311" cy="578" r="2" fill="{INK}"/>')
o.append('</g>')

# pasarela de madera con visitantes (derecha, primer plano)
o.append(f'<path d="M 690 628 L 1000 618 L 1000 646 L 690 656 Z" fill="url(#wood)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
o.append('<g stroke="#7A532C" stroke-width="2">' + "".join(f'<line x1="{x}" y1="{f(628 - (x - 690) * 10 / 310)}" x2="{x}" y2="{f(656 - (x - 690) * 10 / 310)}"/>' for x in range(720, 1000, 30)) + '</g>')
def person(x, base, col, h=64, arm=None):
    head = base - h
    o2 = [f'<g>']
    o2.append(dbl(f"M {x - 6} {base - h * 0.42} L {x - 8} {base - 4}", 7, "#2E3442", 6))
    o2.append(dbl(f"M {x + 6} {base - h * 0.42} L {x + 9} {base - 4}", 7, "#3A4152", 6))
    o2.append(f'<path d="M {x - 14} {base - h * 0.78} C {x - 14} {base - h * 0.9}, {x + 14} {base - h * 0.9}, {x + 14} {base - h * 0.78} L {x + 13} {base - h * 0.38} L {x - 13} {base - h * 0.38} Z" fill="{col}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    if arm:
        o2.append(dbl(f"M {x + 8} {base - h * 0.8} L {arm[0]} {arm[1]}", 6, col, 6))
    o2.append(f'<circle cx="{x}" cy="{head + 8}" r="10" fill="#F2C7A5" stroke="{INK}" stroke-width="5"/>')
    o2.append(f'<path d="M {x - 10} {head + 6} C {x - 8} {head - 4}, {x + 8} {head - 4}, {x + 10} {head + 4}" fill="#5A3A22" stroke="{INK}" stroke-width="3"/>')
    o2.append('</g>')
    return "".join(o2)
o.append('<g id="people">' + person(770, 636, "#FF5A36", 66, arm=(746, 556)) + person(830, 634, "#F2C14E", 58) + person(900, 632, "#2FB5A0", 70) + '</g>')
o.append(dbl("M 700 600 L 1000 590", 5, "#A57A4E", 6))
o.append("".join(dbl(f"M {x} {f(628 - (x - 690) * 10 / 310)} L {x} {f(600 - (x - 700) * 10 / 300)}", 5, "#8A6238", 6) for x in (710, 860, 990)))

# regla de altura (escena «+»)
RX = 690
o.append('<g id="ruler">')
o.append(f'<path d="M {RX} {VY} L {RX} {TOPY}" stroke="{INK}" stroke-width="12" stroke-linecap="round"/><path d="M {RX} {VY} L {RX} {TOPY}" stroke="{LIME}" stroke-width="5" stroke-linecap="round"/>')
for k in range(0, 12):
    y = VY - (VY - TOPY) * k / 11
    w = 22 if k % 5 == 0 else 12
    o.append(f'<path d="M {RX - w} {f(y)} L {RX + w} {f(y)}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>')
o.append('</g>')
la, ba = label("lalt", RX + 90, TOPY + 20, "55 M", bg=LIME, fg=INK)
o.append(la)
lh, bh = label("lhot", 230, 200, "AGUA HIRVIENDO", line_to=(VX - 40, 250))
o.append(lh)
li, bi = label("linterval", 236, 152, "CADA 60-110 MIN", bg="#FFFFFF", fg=INK)
o.append(li)
ly, by_ = label("lyellow", 236, 152, "YELLOWSTONE", bg=LIME, fg=INK)
o.append(ly)
o.append('</svg>')
open("escena.svg", "w").write("\n".join(o))
print(ba, bh)

"""Fig. · Corte de un géiser: cono, tubo estrecho, cámara de agua, grietas con lluvia y roca caliente."""
import math, random
from lib import *

SG = 172            # superficie del suelo
VX, VY = 520, 134   # boca
defs = """
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#A9D8FF"/><stop offset="1" stop-color="#E6F3FF"/></linearGradient>
<linearGradient id="soil" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E2CDA4"/><stop offset="1" stop-color="#BFA071"/></linearGradient>
<linearGradient id="rock" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#A49482"/><stop offset="1" stop-color="#7D6A5A"/></linearGradient>
<linearGradient id="hot" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8E5A44"/><stop offset="0.5" stop-color="#C2482E"/><stop offset="1" stop-color="#FF5A36"/></linearGradient>
<radialGradient id="magma" cx="0.5" cy="0.4" r="0.6"><stop offset="0" stop-color="#FFE27A"/><stop offset="0.5" stop-color="#FFA23A"/><stop offset="1" stop-color="#E5482A"/></radialGradient>
<linearGradient id="water" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8FD3FF"/><stop offset="1" stop-color="#2F7FD6"/></linearGradient>
<linearGradient id="cone" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FBF8EF"/><stop offset="1" stop-color="#C9BC9C"/></linearGradient>
<radialGradient id="bub" cx="0.35" cy="0.3" r="0.8"><stop offset="0" stop-color="#FFFFFF"/><stop offset="0.6" stop-color="#E4F4FF"/><stop offset="1" stop-color="#A9D8FA"/></radialGradient>
<radialGradient id="dropg" cx="0.35" cy="0.3" r="0.8"><stop offset="0" stop-color="#FFFFFF"/><stop offset="0.5" stop-color="#BFE6FF"/><stop offset="1" stop-color="#5FAEE8"/></radialGradient>
"""
o = [svg_open(defs)]
o.append('<rect width="1000" height="700" fill="url(#sky)"/>')
random.seed(4)
def pine(x, base, h, col):
    w = h * 0.22
    return f'<path d="M {f(x)} {f(base - h)} L {f(x + w)} {f(base - h * 0.35)} L {f(x + w * 0.6)} {f(base - h * 0.38)} L {f(x + w * 1.2)} {f(base)} L {f(x - w * 1.2)} {f(base)} L {f(x - w * 0.6)} {f(base - h * 0.38)} L {f(x - w)} {f(base - h * 0.35)} Z" fill="{col}"/>'
x = 0
while x < 1010:
    if not 380 < x < 660:
        o.append(pine(x, SG + 2, random.uniform(44, 70), "#8DB79A"))
    x += random.uniform(22, 34)

# capas del subsuelo
o.append(f'<rect y="{SG}" width="1000" height="140" fill="url(#soil)"/>')
o.append(f'<path d="M 0 310 C 200 300, 380 322, 560 306 C 740 292, 880 312, 1000 300 L 1000 600 L 0 600 Z" fill="url(#rock)"/>')
o.append(f'<path d="M 0 576 C 160 566, 340 590, 520 572 C 700 556, 860 584, 1000 570 L 1000 700 L 0 700 Z" fill="url(#hot)"/>')
o.append('<g transform="translate(0 -34)"><g fill="url(#magma)" stroke="#0B0B14" stroke-width="5">'
         '<path d="M 120 760 L 120 700 C 140 650, 220 630, 300 646 C 360 630, 440 640, 470 760 L 120 760 Z"/>'
         '<path d="M 560 760 L 560 700 C 600 652, 700 640, 760 656 C 820 640, 900 650, 930 760 L 560 760 Z"/></g>')
o.append('<g fill="#FFF3B0" opacity="0.8"><ellipse cx="260" cy="672" rx="40" ry="8"/><ellipse cx="720" cy="676" rx="50" ry="9"/></g></g>')
# textura: piedrecitas en el suelo y grietas en la roca
o.append('<g fill="#A88A5E" opacity="0.7">' + "".join(f'<ellipse cx="{random.randint(20, 980)}" cy="{random.randint(SG + 20, 296)}" rx="{random.randint(4, 9)}" ry="{random.randint(3, 5)}"/>' for _ in range(40)) + '</g>')
o.append('<g fill="none" stroke="#5E4F42" stroke-width="3" opacity="0.55" stroke-linecap="round">'
         '<path d="M 60 360 l 30 20 l -10 30 l 24 18"/><path d="M 900 340 l -20 26 l 14 22 l -18 30"/><path d="M 180 500 l 26 -10 l 20 16"/><path d="M 780 520 l 30 8 l 12 -20"/></g>')
o.append(f'<path d="M 0 310 C 200 300, 380 322, 560 306 C 740 292, 880 312, 1000 300" fill="none" stroke="#6E5A48" stroke-width="3" opacity="0.6"/>')

# grietas por donde baja el agua de lluvia
crackL = "M 150 176 C 170 240, 240 300, 280 360 C 310 404, 340 430, 372 446"
crackR = "M 860 176 C 840 240, 780 300, 740 350 C 712 390, 690 420, 668 440"
o.append(f'<g fill="none" stroke="#3E3228" stroke-width="10" stroke-linecap="round"><path d="{crackL}"/><path d="{crackR}"/></g>')
o.append(f'<g fill="none" stroke="#7FC4F0" stroke-width="4" stroke-linecap="round"><path d="{crackL}"/><path d="{crackR}"/></g>')

# cámara + tubo (agua)
cav = ("M 506 150 C 500 190, 512 230, 506 270 C 500 300, 510 330, 500 368 "
       "C 440 366, 380 384, 362 426 C 344 470, 372 528, 430 540 C 490 552, 580 552, 640 532 "
       "C 690 514, 700 466, 676 430 C 656 398, 600 372, 540 368 "
       "C 532 330, 540 300, 534 270 C 528 230, 540 190, 534 150 Z")
o.append(f'<g id="chamber"><path d="{cav}" fill="#3E3228" stroke="#3E3228" stroke-width="22" stroke-linejoin="round"/>')
o.append(f'<path d="{cav}" fill="url(#water)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
o.append('<path d="M 390 420 C 420 392, 470 380, 520 382" fill="none" stroke="#FFFFFF" stroke-width="4" opacity="0.6" stroke-linecap="round"/>')
o.append('<path d="M 512 160 C 508 200, 516 240, 512 270" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.6" stroke-linecap="round"/></g>')
# burbujitas de fondo
o.append('<g id="bubbles" fill="url(#bub)" stroke="#0B0B14" stroke-width="2.5">' + "".join(
    f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x, y, r in [(450, 500, 6), (600, 490, 5), (520, 470, 4), (410, 460, 4), (640, 460, 5)]) + '</g>')

# cono de sínter en la superficie
cone = f"M 420 {SG} C 450 160, 480 140, 506 {VY} L 534 {VY} C 560 140, 590 160, 620 {SG} Z"
o.append(f'<path d="{cone}" fill="url(#cone)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
o.append(f'<path d="M 0 {SG} L 420 {SG} M 620 {SG} L 1000 {SG}" stroke="{INK}" stroke-width="6"/>')
o.append(f'<ellipse cx="{VX}" cy="{VY}" rx="15" ry="5" fill="#3E7FB8" stroke="{INK}" stroke-width="4"/>')

# lluvia (dos zonas)
o.append('<g id="rain" stroke="#2F7FD6" stroke-width="5" stroke-linecap="round">' + "".join(
    f'<path d="M {x} {y} l -6 16"/>' for x, y in [(80, 90), (120, 120), (160, 86), (200, 116), (100, 150), (180, 150), (800, 92), (840, 122), (880, 88), (920, 118), (820, 150), (900, 150)]) + '</g>')
# flechas de infiltración y de calor
def inner(g):
    return g[g.index(">") + 1:-4]
o.append('<g id="infil">' + inner(curved_arrow("a", "M 130 196 C 160 260, 230 320, 270 372", (270, 372), (250, 344), "#8FD3FF", w=9, head=24))
         + inner(curved_arrow("b", "M 880 196 C 850 260, 790 320, 750 366", (750, 366), (772, 340), "#8FD3FF", w=9, head=24)) + '</g>')
def wavy(x, y0, y1):
    pts = [(x + 10 * math.sin((y0 - y) / 18), y) for y in range(y0, y1 - 1, -4)]
    return pts
heat = []
for x in (420, 520, 620):
    pts = wavy(x, 640, 566)
    d = pts_d(pts)
    heat.append(inner(curved_arrow("h", d, pts[-1], pts[-3], CORAL, w=8, head=20)))
o.append('<g id="heat">' + "".join(heat) + '</g>')

# burbuja grande de vapor subiendo por el tubo
o.append(f'<g id="vapor"><circle cx="520" cy="356" r="15" fill="url(#bub)" stroke="{INK}" stroke-width="4"/><circle cx="515" cy="351" r="4" fill="#FFFFFF"/></g>')
# agua que rebosa por la boca
o.append(f'<g id="spill"><path d="M 508 136 C 490 140, 470 150, 452 168 M 532 136 C 550 140, 570 150, 588 168" fill="none" stroke="{INK}" stroke-width="11" stroke-linecap="round"/>'
         f'<path d="M 508 136 C 490 140, 470 150, 452 168 M 532 136 C 550 140, 570 150, 588 168" fill="none" stroke="#8FD3FF" stroke-width="5" stroke-linecap="round"/>'
         f'<circle cx="500" cy="118" r="6" fill="url(#dropg)" stroke="{INK}" stroke-width="3"/><circle cx="544" cy="114" r="5" fill="url(#dropg)" stroke="{INK}" stroke-width="3"/></g>')
# ebullición repentina: burbujas por toda la cámara y el tubo
random.seed(21)
bo = []
for _ in range(34):
    x, y = random.uniform(380, 660), random.uniform(392, 530)
    bo.append((x, y, random.uniform(6, 14)))
for y in range(170, 360, 26):
    bo.append((520 + random.uniform(-4, 4), y, random.uniform(6, 9)))
o.append('<g id="boil" fill="url(#bub)" stroke="#0B0B14" stroke-width="3">' + "".join(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}"/>' for x, y, r in bo) + '</g>')
# chorro saliendo por arriba
circ = []
for k in range(10):
    t = k / 9
    y = VY - 6 - (VY - 6 - 30) * t
    r = 12 + 22 * t
    circ.append((VX + 4 * t, y, r))
    circ.append((VX - r * 0.5, y + 4, r * 0.6))
    circ.append((VX + r * 0.5, y - 2, r * 0.6))
o.append('<g id="jet"><g fill="#0B0B14">' + "".join(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r + 6)}"/>' for x, y, r in circ) + '</g>'
         '<g fill="#FFFFFF">' + "".join(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}"/>' for x, y, r in circ) + '</g>'
         '<g fill="#D6ECFB">' + "".join(f'<circle cx="{f(x + r * 0.35)}" cy="{f(y + r * 0.3)}" r="{f(r * 0.5)}"/>' for x, y, r in circ[::3]) + '</g>'
         f'<path d="M {VX} {VY - 8} L {VX + 4} 40" stroke="#9FD2F5" stroke-width="5" stroke-linecap="round"/></g>')

L = [label("lcam", 236, 486, "CÁMARA", line_to=(366, 476)),
     label("ltubo", 690, 250, "TUBO ESTRECHO", line_to=(538, 250)),
     label("llluvia", 664, 100, "LLUVIA", line_to=(796, 112)),
     label("lmagma", 200, 560, "MAGMA", line_to=(300, 616)),
     label("lvapor", 660, 320, "VAPOR", line_to=(538, 352))]
for s_, b in L:
    o.append(s_)
o.append('</svg>')
open("corte.svg", "w").write("\n".join(o))
print([b for _, b in L])

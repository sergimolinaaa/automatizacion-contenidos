import math, random, sys
sys.path.insert(0, sys.path[0])
from common import *

random.seed(7)
SKIN_D = "#C97B5C"
o = [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 700">
<defs>
<linearGradient id="wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#EAF4F7"/><stop offset="1" stop-color="#D3E5EC"/></linearGradient>
<linearGradient id="water" gradientUnits="userSpaceOnUse" x1="0" y1="350" x2="0" y2="486"><stop offset="0" stop-color="#CFEEFF"/><stop offset="0.5" stop-color="#8FD3FF"/><stop offset="1" stop-color="#4E9FE0"/></linearGradient>
<linearGradient id="tub" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="0.55" stop-color="#EEF2F6"/><stop offset="1" stop-color="#C5D0DC"/></linearGradient>
<linearGradient id="rim" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#DCE4EC"/></linearGradient>
<linearGradient id="skin" gradientUnits="userSpaceOnUse" x1="300" y1="0" x2="560" y2="0"><stop offset="0" stop-color="#E9A27F"/><stop offset="0.35" stop-color="#FBD3B8"/><stop offset="1" stop-color="#F0B391"/></linearGradient>
<linearGradient id="skinf" gradientUnits="userSpaceOnUse" x1="720" y1="0" x2="900" y2="0"><stop offset="0" stop-color="#F7C9AC"/><stop offset="0.5" stop-color="#FCDCC7"/><stop offset="1" stop-color="#E8A887"/></linearGradient>
<radialGradient id="duck" cx="0.35" cy="0.3" r="0.8"><stop offset="0" stop-color="#FFF08A"/><stop offset="0.6" stop-color="#FFD23F"/><stop offset="1" stop-color="#E9A800"/></radialGradient>
<radialGradient id="bub" cx="0.35" cy="0.3" r="0.8"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#DDF0FF"/></radialGradient>
</defs>
<rect width="1000" height="700" fill="url(#wall)"/>''']
# azulejos (lejos, sin contorno)
g = ['<g stroke="#C4D8E1" stroke-width="4">']
for x in range(0, 1001, 110):
    g.append(f'<line x1="{x}" y1="0" x2="{x}" y2="380"/>')
for y in range(40, 380, 110):
    g.append(f'<line x1="0" y1="{y}" x2="1000" y2="{y}"/>')
g.append('</g>')
o += g
o.append('<g fill="#FFFFFF" opacity="0.45"><path d="M 560 0 L 640 0 L 520 380 L 440 380 Z"/><path d="M 680 0 L 710 0 L 590 380 L 560 380 Z"/></g>')
# estante con botes (lejos, desaturado)
o.append('<g opacity="0.9"><rect x="70" y="300" width="170" height="14" rx="5" fill="#B9C9D3"/>'
         '<rect x="88" y="232" width="40" height="68" rx="10" fill="#9FD6C4"/><rect x="98" y="218" width="20" height="16" rx="4" fill="#7FBFAA"/>'
         '<rect x="140" y="250" width="34" height="50" rx="9" fill="#F4B7C5"/><rect x="150" y="238" width="14" height="13" rx="3" fill="#E39AAC"/>'
         '<rect x="184" y="262" width="44" height="38" rx="12" fill="#C9D9F5"/>'
         '<rect x="94" y="244" width="6" height="40" rx="3" fill="#FFFFFF" opacity="0.6"/></g>')
# bañera: borde superior + hueco con agua
o.append(f'<rect x="20" y="326" width="960" height="190" rx="95" fill="url(#rim)" stroke="{INK}" stroke-width="7"/>')
o.append(f'<rect x="62" y="350" width="876" height="136" rx="68" fill="url(#water)" stroke="{INK}" stroke-width="5"/>')
o.append('<path d="M 120 360 C 300 352, 700 352, 880 360" fill="none" stroke="#FFFFFF" stroke-width="6" opacity="0.6"/>')
# reflejos en el agua
o.append('<g id="waves" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" opacity="0.75">'
         + "".join(f'<path d="{wavy(x, y, x + l, y, 3, 2)}"/>' for x, y, l in [(120, 400, 90), (520, 392, 70), (640, 440, 110), (180, 452, 70), (900 - 120, 465, 60)])
         + '</g>')
# sombra del pie y de la mano en el agua
o.append('<g fill="#2F7FD6" opacity="0.35"><ellipse cx="385" cy="462" rx="80" ry="12"/><ellipse cx="800" cy="440" rx="70" ry="11"/></g>')

# ---------- PIE (al fondo, a la derecha, planta hacia nosotros) ----------
foot = 'M 770 448 C 752 420, 742 370, 744 318 C 746 286, 758 262, 790 258 C 830 254, 878 258, 892 280 C 904 302, 884 338, 862 372 C 848 396, 840 420, 842 448 Z'
toes = [(758, 232, 26, 31), (800, 222, 17, 21), (834, 226, 15, 18), (862, 238, 13, 16), (886, 256, 11, 13)]
o.append('<g id="foot">')
o.append(f'<path d="{foot}" fill="none" stroke="{INK}" stroke-width="15" stroke-linejoin="round"/>')
o.append("".join(f'<ellipse cx="{x}" cy="{y}" rx="{a}" ry="{b}" fill="none" stroke="{INK}" stroke-width="15"/>' for x, y, a, b in toes))
o.append(f'<path d="{foot}" fill="url(#skinf)"/>')
o.append("".join(f'<ellipse cx="{x}" cy="{y}" rx="{a}" ry="{b}" fill="url(#skinf)"/>' for x, y, a, b in toes))
# pliegue bajo los dedos + talon y arco
o.append(f'<path d="M 748 270 C 790 262, 850 262, 890 282" fill="none" stroke="{SKIN_D}" stroke-width="4" stroke-linecap="round" opacity="0.8"/>')
o.append('<ellipse cx="808" cy="300" rx="44" ry="20" fill="#F9B9A0" opacity="0.6"/><ellipse cx="800" cy="420" rx="26" ry="18" fill="#F9B9A0" opacity="0.5"/>')
o.append('<path d="M 760 300 C 756 340, 764 380, 776 420" fill="none" stroke="#FFF1E6" stroke-width="5" stroke-linecap="round" opacity="0.8"/>')
o.append('<g id="toewr" fill="none" stroke="#B5644A" stroke-width="3" stroke-linecap="round">')
for x, y, a, b in toes:
    for k in ((-1, 0, 1) if a > 16 else (-1, 1)):
        dx = k * a * (0.38 if a > 16 else 0.3)
        o.append(f'<path d="{wavy(x + dx, y - b * 0.55, x + dx * 1.1, y + b * 0.45, 1.6, 2, 12)}"/>')
o.append('</g></g>')
# agua delante del tobillo + onda
o.append('<path d="M 740 446 C 770 440, 840 440, 870 446 L 870 470 L 740 470 Z" fill="url(#water)" opacity="0.93"/>')
o.append(f'<ellipse cx="806" cy="446" rx="64" ry="9" fill="none" stroke="#FFFFFF" stroke-width="5"/>')
for k in (1, 2):
    o.append(f'<g id="ripf{k}"><ellipse cx="806" cy="446" rx="78" ry="12" fill="none" stroke="#FFFFFF" stroke-width="4"/></g>')

# ---------- PATITO ----------
o.append(f'''<g id="duck"><ellipse cx="610" cy="430" rx="52" ry="7" fill="#2F7FD6" opacity="0.35"/>
<path d="M 560 420 C 556 392, 590 384, 618 392 C 640 398, 664 392, 668 380 C 676 404, 662 432, 612 432 C 582 432, 562 428, 560 420 Z" fill="url(#duck)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>
<circle cx="590" cy="372" r="27" fill="url(#duck)" stroke="{INK}" stroke-width="6"/>
<path d="M 566 374 C 548 370, 540 378, 548 384 C 556 388, 566 384, 570 382 Z" fill="#FF8A1F" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>
<circle cx="584" cy="366" r="5" fill="{INK}"/><circle cx="582" cy="364" r="1.8" fill="#FFFFFF"/>
<path d="M 600 404 C 616 398, 636 402, 644 412" fill="none" stroke="#E9A800" stroke-width="5" stroke-linecap="round"/>
<path d="M 576 352 C 586 346, 598 348, 604 354" fill="none" stroke="#FFF7C2" stroke-width="4" stroke-linecap="round"/></g>''')

# ---------- MANO (palma hacia nosotros, mano derecha: pulgar a la derecha) ----------
fingers = [  # base, angulo, largo, ancho
    ((334, 292), -14, 118, 36),
    ((374, 270), -5, 150, 40),
    ((416, 266), 2, 164, 42),
    ((456, 274), 10, 148, 40),
]
thumb = ((470, 400), 42, 120, 46)
palm = 'M 330 470 C 326 430, 312 380, 314 330 C 315 300, 324 282, 344 272 C 380 256, 440 254, 470 266 C 488 276, 494 300, 492 330 C 490 372, 470 420, 452 470 Z'
def caps(b, a, L, w, fill, stroke=None, sw=0):
    r = w / 2
    x0, y0 = rot(0, 40 - r, a, *b)
    x1, y1 = rot(0, -L + r, a, *b)
    return f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="{fill}" stroke-width="{w + sw}" stroke-linecap="round"/>'
o.append('<g id="hand">')
# contorno unido: primero todo en tinta gruesa, luego los rellenos
o.append(f'<path d="{palm}" fill="{INK}" stroke="{INK}" stroke-width="16" stroke-linejoin="round"/>')
for b, a, L, w in fingers + [thumb]:
    o.append(caps(b, a, L, w, INK, INK, 16))
o.append(f'<path d="{palm}" fill="url(#skin)"/>')
for b, a, L, w in [thumb] + fingers:
    o.append(caps(b, a, L, w, "url(#skin)"))
# separacion entre dedos (hendidura) y pliegues
for (b1, a1, L1, w1), (b2, a2, L2, w2) in zip(fingers, fingers[1:]):
    mx, my = (b1[0] + b2[0]) / 2, (b1[1] + b2[1]) / 2
    o.append(f'<path d="M {mx:.0f} {my - 6:.0f} L {mx + (a1 + a2) * 0.6:.0f} {my - 40:.0f}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>')
for b, a, L, w in fingers:
    for f in (0.36, 0.68):
        y = -L * f
        o.append(f'<path d="M {-w * 0.32:.1f} {y:.1f} Q 0 {y + 5:.1f} {w * 0.32:.1f} {y:.1f}" fill="none" stroke="{SKIN_D}" stroke-width="3.5" stroke-linecap="round" transform="translate({b[0]} {b[1]}) rotate({a})"/>')
    # brillo en el lado izquierdo
    o.append(f'<path d="M {-w / 2 + 7} {-L * 0.15:.0f} L {-w / 2 + 7} {-L + w * 0.55:.0f}" stroke="#FFEADB" stroke-width="4" stroke-linecap="round" opacity="0.9" transform="translate({b[0]} {b[1]}) rotate({a})"/>')
b, a, L, w = thumb
o.append(f'<path d="M {-w * 0.32:.1f} {-L * 0.45:.1f} Q 0 {-L * 0.45 + 5:.1f} {w * 0.32:.1f} {-L * 0.45:.1f}" fill="none" stroke="{SKIN_D}" stroke-width="3.5" stroke-linecap="round" transform="translate({b[0]} {b[1]}) rotate({a})"/>')
# lineas de la palma
o.append(f'<g fill="none" stroke="{SKIN_D}" stroke-width="4" stroke-linecap="round" opacity="0.85">'
         '<path d="M 330 318 C 370 312, 420 318, 470 300"/>'
         '<path d="M 326 350 C 370 340, 410 334, 444 316"/>'
         '<path d="M 452 320 C 420 360, 418 410, 432 452"/></g>')
o.append('<path d="M 326 330 C 322 380, 330 420, 336 452" fill="none" stroke="#FFEADB" stroke-width="5" stroke-linecap="round" opacity="0.8"/>')
# ARRUGAS de las yemas
o.append('<g id="wrinkles" fill="none" stroke="#A9573F" stroke-width="3.6" stroke-linecap="round">')
for b, a, L, w in fingers + [thumb]:
    tr = f'transform="translate({b[0]} {b[1]}) rotate({a})"'
    top = -L + 8
    for k in (-0.28, 0, 0.28):
        x = k * w
        o.append(f'<path d="{wavy(x, top + 4 + abs(k) * 20, x * 1.15, top + w * 0.95, 2.2, 2, 14)}" {tr}/>')
    o.append(f'<path d="M {-w * 0.3:.1f} {top + w * 1.1:.1f} Q 0 {top + w * 1.0:.1f} {w * 0.3:.1f} {top + w * 1.1:.1f}" {tr}/>')
o.append('</g>')
o.append('</g>')
# agua delante de la muñeca + onda
o.append('<path d="M 300 452 C 340 446, 440 446, 476 452 L 476 480 L 300 480 Z" fill="url(#water)" opacity="0.93"/>')
o.append(f'<ellipse cx="390" cy="456" rx="82" ry="10" fill="none" stroke="#FFFFFF" stroke-width="5"/>')
for k in (1, 2):
    o.append(f'<g id="riph{k}"><ellipse cx="390" cy="456" rx="96" ry="14" fill="none" stroke="#FFFFFF" stroke-width="4"/></g>')
# gotas que caen del meñique
o.append('<g id="drops">')
for x, y, r in [(352, 380, 7), (430, 214, 6), (800, 330, 7)]:
    o.append(f'<path d="M {x} {y - r * 1.8} C {x + r} {y - r * 0.4}, {x + r} {y + r}, {x} {y + r} C {x - r} {y + r}, {x - r} {y - r * 0.4}, {x} {y - r * 1.8} Z" fill="#8FD3FF" stroke="{INK}" stroke-width="3.5"/>'
             f'<circle cx="{x - r * 0.35:.1f}" cy="{y:.1f}" r="{r * 0.28:.1f}" fill="#FFFFFF"/>')
o.append('</g>')
# espuma
o.append('<g id="foam">')
for cx, cy, n, sp in [(140, 380, 9, 50), (250, 468, 7, 40), (520, 466, 8, 40), (690, 372, 6, 36), (900, 400, 7, 30)]:
    for _ in range(n):
        x = cx + random.uniform(-sp, sp); y = cy + random.uniform(-10, 10); r = random.uniform(7, 15)
        o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="url(#bub)" stroke="{INK}" stroke-width="3"/>'
                 f'<circle cx="{x - r * 0.35:.0f}" cy="{y - r * 0.35:.0f}" r="{r * 0.22:.1f}" fill="#FFFFFF"/>')
o.append('</g>')
# vapor
o.append('<g id="steam" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round" opacity="0.8">'
         '<path d="M 620 330 C 600 300, 640 280, 620 250 C 604 226, 630 206, 620 186"/>'
         '<path d="M 680 336 C 662 310, 700 290, 682 262"/>'
         '<path d="M 200 340 C 184 314, 214 296, 200 270"/></g>')
# frente de la bañera
o.append(f'<path d="M 20 421 L 20 760 L 980 760 L 980 421 C 980 470, 940 516, 885 516 L 115 516 C 60 516, 20 470, 20 421 Z" fill="url(#tub)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
o.append('<path d="M 70 540 C 70 600, 80 640, 90 700" fill="none" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round" opacity="0.9"/>')
o.append('<path d="M 130 506 L 870 506" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity="0.9"/>')
TW = 'M 604 476 C 640 468, 700 468, 736 476 L 748 628 C 736 640, 724 632, 712 642 C 698 650, 684 638, 670 646 C 656 652, 640 640, 626 646 C 614 650, 602 642, 594 632 Z'
o.append(f'<path d="{TW}" fill="#FF8C7A" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
o.append('<path d="M 600 590 C 650 598, 700 598, 744 590 L 745 606 C 700 614, 650 614, 599 606 Z" fill="#FFFFFF" opacity="0.85"/>')
o.append('<g fill="none" stroke="#E0604E" stroke-width="5" stroke-linecap="round"><path d="M 640 500 C 636 540, 640 580, 636 630"/><path d="M 700 500 C 704 540, 700 580, 706 630"/></g>')
o.append('<path d="M 618 492 L 612 580" stroke="#FFC2B8" stroke-width="6" stroke-linecap="round"/>')
o.append(f'<path d="M 600 478 C 640 462, 700 462, 740 478 C 742 494, 738 506, 736 512 C 700 500, 640 500, 604 512 C 600 504, 598 492, 600 478 Z" fill="#E86F5E" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
# etiquetas
o.append(tag("lmanos", 40, 150, "MANOS", lead=(200, 179, 300, 182)))
o.append(tag("lpies", 820, 92, "PIES", lead=(890, 150, 862, 220)))
o.append(tag("larrugas", 536, 96, "ARRUGAS", lead=(536, 125, 492, 140)))
o.append('</svg>')
print("\n".join(o))

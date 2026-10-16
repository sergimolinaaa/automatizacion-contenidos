import math
from lib import *
defs = (lg("tilebg", [(0, "#EAF4F8"), (1, "#D5E6EE")]) + lg("counter", [(0, "#F4EEE6"), (1, "#D9CFC2")]) +
        lg("cab", [(0, "#7FA7C9"), (1, "#5A84AA")]) + lg("boxf", [(0, "#FF7A5C"), (1, "#E0482A")]) + lg("boxs", [(0, "#C9391E"), (1, "#9E2A14")]) +
        lg("bowl", [(0, "#FFFFFF"), (0.6, "#E6EEF5"), (1, "#B9C8D6")]) + rg("batter", [(0, "#FFE7B0"), (1, "#E9C27A")]) +
        lg("shell", [(0, "#FFF8EC"), (1, "#E8D6BC")]) + rg("yolk", [(0, "#FFD36A", 1), (0.6, "#FFB020"), (1, "#F08A00")], 0.4, 0.35, 0.7) +
        lg("cake", [(0, "#F7C98B"), (1, "#C98A45")]))
o = [header(defs)]
o.append('<rect width="1000" height="700" fill="url(#tilebg)"/>')
# azulejos metro
for r, y in enumerate(range(0, 470, 44)):
    off = 0 if r % 2 == 0 else 45
    o.append(f'<path d="M 0 {y} L 1000 {y}" stroke="#BFD3DE" stroke-width="3"/>')
    for x in range(-off, 1000, 90):
        o.append(f'<path d="M {x} {y} L {x} {y + 44}" stroke="#BFD3DE" stroke-width="3"/>')
o.append('<g fill="#FFFFFF" opacity="0.5">' + "".join(f'<rect x="{x + 8}" y="{y + 6}" width="30" height="6" rx="3"/>' for y in range(0, 440, 88) for x in range(0, 1000, 180)) + '</g>')
# encimera
o.append(f'<rect x="-10" y="462" width="1020" height="40" fill="url(#counter)" stroke="{INK}" stroke-width="6"/>')
o.append('<path d="M 60 476 C 160 470, 220 486, 320 478 M 520 490 C 600 484, 700 494, 820 486" stroke="#C7BBAE" stroke-width="3" fill="none" opacity="0.7"/>')
o.append(f'<path d="M 0 468 L 1000 468" stroke="#FFFFFF" stroke-width="4" opacity="0.8"/>')
o.append(f'<rect x="-10" y="502" width="1020" height="220" fill="url(#cab)" stroke="{INK}" stroke-width="6"/>')
for x in (20, 345, 670):
    o.append(f'<rect x="{x}" y="522" width="310" height="200" rx="8" fill="none" stroke="{INK}" stroke-width="5" opacity="0.8"/><rect x="{x + 125}" y="540" width="60" height="12" rx="6" fill="#D9E2EA" stroke="{INK}" stroke-width="4"/>')
o.append('<rect x="-10" y="502" width="1020" height="18" fill="#000" opacity="0.15"/>')

# caja de preparado (genérica)
bx0, by0, bw, bh, d = 90, 196, 190, 272, 34
C = ['<g id="caja">', f'<ellipse cx="{bx0 + bw / 2 + 14}" cy="466" rx="{bw / 2 + 30}" ry="10" fill="#000" opacity="0.2"/>']
C.append(f'<path d="{poly([(bx0 + bw, by0), (bx0 + bw + d, by0 - 22), (bx0 + bw + d, by0 + bh - 22), (bx0 + bw, by0 + bh)], True)}" fill="url(#boxs)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
C.append(f'<path d="{poly([(bx0, by0), (bx0 + d, by0 - 22), (bx0 + bw + d, by0 - 22), (bx0 + bw, by0)], True)}" fill="#FF9C80" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
C.append(f'<rect x="{bx0}" y="{by0}" width="{bw}" height="{bh}" fill="url(#boxf)" stroke="{INK}" stroke-width="7"/>')
C.append(f'<rect x="{bx0 + 14}" y="{by0 + 16}" width="{bw - 28}" height="50" rx="8" fill="#FFF4E0" stroke="{INK}" stroke-width="4"/>')
C.append(txt(bx0 + bw / 2, by0 + 50, "BIZCOCHO", 24, "#C9391E"))
# pastel dibujado en la caja
cx, cy = bx0 + bw / 2, by0 + 170
C.append(f'<ellipse cx="{cx}" cy="{cy + 50}" rx="72" ry="12" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/>')
C.append(f'<path d="M {cx - 60} {cy - 10} L {cx - 60} {cy + 40} Q {cx} {cy + 58} {cx + 60} {cy + 40} L {cx + 60} {cy - 10} Z" fill="url(#cake)" stroke="{INK}" stroke-width="5"/>')
C.append(f'<ellipse cx="{cx}" cy="{cy - 10}" rx="60" ry="16" fill="#FFF0F4" stroke="{INK}" stroke-width="5"/>')
C.append(f'<path d="M {cx - 58} {cy - 4} q 10 18 20 4 q 10 16 20 2 q 10 18 20 2 q 10 16 20 2 q 10 16 18 0" fill="#FFF0F4" stroke="{INK}" stroke-width="4"/>')
C.append(f'<circle cx="{cx}" cy="{cy - 26}" r="11" fill="#E5484D" stroke="{INK}" stroke-width="4"/><path d="M {cx} {cy - 37} q 6 -12 14 -14" stroke="{INK}" stroke-width="3" fill="none"/>')
C.append(f'<path d="M {bx0 + 10} {by0 + 8} L {bx0 + 10} {by0 + bh - 10}" stroke="#FFB6A4" stroke-width="5" stroke-linecap="round"/>')
C.append('</g>')
o.append("".join(C))
# sello en la caja: añade 1 huevo
o.append(f'<g id="sello"><path d="{star(312, 150, 62, 50, 16)}" fill="{LIME}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>' + txt(312, 142, "AÑADE", 18) + txt(312, 166, "1 HUEVO", 18) + '</g>')

# bol con masa
bcx, bty = 545, 352
o.append(f'<ellipse cx="{bcx}" cy="468" rx="150" ry="12" fill="#000" opacity="0.2"/>')
o.append(f'<path d="M {bcx - 170} {bty} C {bcx - 168} {bty + 90}, {bcx - 100} {bty + 116}, {bcx} {bty + 116} C {bcx + 100} {bty + 116}, {bcx + 168} {bty + 90}, {bcx + 170} {bty} Z" fill="url(#bowl)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
o.append(f'<ellipse cx="{bcx}" cy="{bty}" rx="170" ry="34" fill="#F4F8FB" stroke="{INK}" stroke-width="7"/>')
o.append(f'<g id="masa"><ellipse cx="{bcx}" cy="{bty + 6}" rx="146" ry="24" fill="url(#batter)"/>'
         f'<path d="M {bcx - 90} {bty + 4} q 30 -10 60 0 q 30 10 60 0 q 30 -10 50 2" fill="none" stroke="#D9AE62" stroke-width="4" stroke-linecap="round"/></g>')
o.append(f'<path d="M {bcx - 140} {bty + 40} Q {bcx - 130} {bty + 80} {bcx - 90} {bty + 98}" stroke="#FFFFFF" stroke-width="8" fill="none" stroke-linecap="round"/>')
o.append(f'<rect x="{bcx - 70}" y="{bty + 116}" width="140" height="10" rx="4" fill="#B9C8D6" stroke="{INK}" stroke-width="5"/>')
# varillas apoyadas en el bol
W_ = ['<g id="varillas">']
W_.append(dbl(f"M {bcx + 140} {bty - 6} L {bcx + 250} {bty - 150}", 12, "#3A3A44"))
for k in (-1, 0, 1):
    W_.append(f'<path d="M {bcx + 140} {bty - 6} C {bcx + 90 + 20 * k} {bty - 10 + 18 * k}, {bcx + 70 + 16 * k} {bty + 26 + 10 * k}, {bcx + 110} {bty + 30}" fill="none" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>'
              f'<path d="M {bcx + 140} {bty - 6} C {bcx + 90 + 20 * k} {bty - 10 + 18 * k}, {bcx + 70 + 16 * k} {bty + 26 + 10 * k}, {bcx + 110} {bty + 30}" fill="none" stroke="#C7CFD8" stroke-width="4" stroke-linecap="round"/>')
W_.append('</g>')
# (las varillas van detrás del borde del bol: se dibujan antes del borde) -> simplificamos: encima
o.append("".join(W_))

# huevo que se casca sobre el bol
ex, ey = 520, 150
# cáscaras dibujadas como dos cuencos girados
o.append(f'<g id="cascaras">'
         f'<path d="M 420 120 C 420 70, 470 52, 500 70 C 512 78, 516 92, 512 104 L 500 98 L 492 112 L 480 102 L 470 116 L 458 104 L 448 118 L 436 108 Z" fill="url(#shell)" stroke="{INK}" stroke-width="6" stroke-linejoin="round" transform="rotate(-24 470 100)"/>'
         f'<path d="M 670 120 C 670 70, 620 52, 590 70 C 578 78, 574 92, 578 104 L 590 98 L 598 112 L 610 102 L 620 116 L 632 104 L 642 118 L 654 108 Z" fill="url(#shell)" stroke="{INK}" stroke-width="6" stroke-linejoin="round" transform="rotate(24 620 100)"/>'
         f'<path d="M 440 92 q 6 -16 22 -22 M 650 92 q -6 -16 -22 -22" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" fill="none"/></g>')
o.append(f'<g id="yema"><path d="M 545 150 C 520 150, 512 176, 520 196 C 528 214, 562 214, 570 196 C 578 176, 570 150, 545 150 Z" fill="#FFFFFF" opacity="0.75" stroke="#C9D6E0" stroke-width="3"/>'
         f'<circle cx="545" cy="186" r="22" fill="url(#yolk)" stroke="{INK}" stroke-width="5"/><circle cx="538" cy="179" r="6" fill="#FFFFFF" opacity="0.85"/></g>')
# salpicadura en la masa
o.append(f'<g id="salpica"><ellipse cx="545" cy="356" rx="34" ry="9" fill="#FFB020" stroke="{INK}" stroke-width="4"/>'
         + "".join(f'<circle cx="{545 + 60 * math.cos(a):.0f}" cy="{340 - 30 * abs(math.sin(a)):.0f}" r="6" fill="#FFE7B0" stroke="{INK}" stroke-width="3"/>' for a in (0.3, 1.0, 2.1, 2.8)) + '</g>')
# cartón de huevos a la derecha
E = ['<g id="huevera">', '<ellipse cx="850" cy="466" rx="120" ry="10" fill="#000" opacity="0.2"/>']
for k in range(3):
    E.append(f'<ellipse cx="{780 + 70 * k}" cy="418" rx="26" ry="34" fill="url(#shell)" stroke="{INK}" stroke-width="5"/><path d="M {770 + 70 * k} 400 q 4 -10 12 -14" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" fill="none"/>')
E.append(f'<path d="M 734 432 L 966 432 L 952 466 L 748 466 Z" fill="#C9B79A" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
E.append('<path d="M 790 440 L 790 462 M 850 440 L 850 462 M 910 440 L 910 462" stroke="#A8957A" stroke-width="4"/>')
E.append('</g>')
o.append("".join(E))
o.append('</svg>')
open("bizcocho.svg", "w").write("\n".join(o))

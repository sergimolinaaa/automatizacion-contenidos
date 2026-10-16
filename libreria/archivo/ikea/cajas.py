from lib import *
defs = WOOD_DEFS + lg("wall", [(0, "#F6F1E9"), (1, "#E4DCCF")]) + lg("table", [(0, "#EED6B0"), (1, "#D7B27E")]) + \
    lg("apron", [(0, "#B98A55"), (1, "#8C6237")]) + lg("floor", [(0, "#6E5A48"), (1, "#4E3F33")]) + \
    lg("card", [(0, "#FFFFFF"), (1, "#EEF2F7")])
o = [header(defs)]
o.append('<rect width="1000" height="700" fill="url(#wall)"/>')
# fondo lejano: estantería del laboratorio con cajas (sin contorno, desaturado)
o.append('<g opacity="0.55">')
o.append('<rect x="560" y="70" width="400" height="12" fill="#CDBFAA"/><rect x="560" y="190" width="400" height="12" fill="#CDBFAA"/>')
for k, (x, w, h, c) in enumerate(((590, 80, 70, "#D9C4A2"), (680, 60, 90, "#C9D6E2"), (750, 110, 60, "#E2CFA8"), (870, 70, 80, "#D3C0DA"))):
    o.append(f'<rect x="{x}" y="{190 - h}" width="{w}" height="{h}" rx="4" fill="{c}"/>')
o.append('<rect x="370" y="96" width="150" height="110" rx="8" fill="#DCE7EE"/><rect x="384" y="110" width="122" height="14" rx="4" fill="#B9CAD6"/><rect x="384" y="134" width="90" height="10" rx="4" fill="#C9D6E0"/><rect x="384" y="152" width="104" height="10" rx="4" fill="#C9D6E0"/><rect x="384" y="170" width="70" height="10" rx="4" fill="#C9D6E0"/>')
o.append('</g>')
# ventana con luz de día
o.append(f'<path d="M 250 300 L 470 430 L 160 430 L 40 300 Z" fill="#FFFFFF" opacity="0.35"/>')
o.append(f'<rect x="40" y="96" width="210" height="204" rx="6" fill="#F0E6D6" stroke="{INK}" stroke-width="6"/>')
o.append('<rect x="56" y="112" width="178" height="172" fill="#BFE6FF"/>')
o.append('<path d="M 56 230 C 100 210, 150 222, 234 200 L 234 284 L 56 284 Z" fill="#9FD39A"/><path d="M 56 252 C 120 238, 180 250, 234 236 L 234 284 L 56 284 Z" fill="#7CC27A"/>')
o.append('<g fill="#FFFFFF" opacity="0.9"><ellipse cx="110" cy="150" rx="30" ry="11"/><ellipse cx="132" cy="142" rx="20" ry="12"/></g>')
o.append(f'<path d="M 145 112 L 145 284 M 56 198 L 234 198" stroke="#F0E6D6" stroke-width="10"/><path d="M 145 112 L 145 284 M 56 198 L 234 198" stroke="{INK}" stroke-width="3" opacity="0.5"/>')
o.append(f'<rect x="56" y="112" width="178" height="172" fill="none" stroke="{INK}" stroke-width="4"/>')
o.append('<path d="M 70 270 L 120 126" stroke="#FFFFFF" stroke-width="8" opacity="0.5" stroke-linecap="round"/>')
o.append(f'<rect x="30" y="298" width="230" height="16" rx="4" fill="#E2D3BC" stroke="{INK}" stroke-width="5"/>')
# reloj de pared
o.append(f'<g id="reloj"><circle cx="935" cy="300" r="38" fill="#FFFFFF" stroke="{INK}" stroke-width="6"/><circle cx="935" cy="300" r="30" fill="none" stroke="#D6DCE3" stroke-width="3"/></g>')
o.append(f'<g id="aguja"><path d="M 935 312 L 935 276 M 935 300 L 935 324" stroke="{INK}" stroke-width="5" stroke-linecap="round"/><circle cx="935" cy="300" r="4" fill="{INK}"/></g>')
o.append(f'<path d="M 935 300 L 952 306" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>')
# rodapié y suelo
o.append('<rect y="560" width="1000" height="140" fill="url(#floor)"/>')
o.append('<g stroke="#7E6A57" stroke-width="3" opacity="0.6">' + "".join(f'<path d="M {x} 600 L {x - 30 + (x - 500) * 0.25:.0f} 700"/>' for x in range(-40, 1100, 120)) + '<path d="M 0 610 L 1000 610 M 0 650 L 1000 650"/></g>')
# mesa: tablero en perspectiva + canto
o.append(f'<path d="M -10 430 L 1010 430 L 1010 528 L -10 528 Z" fill="url(#table)" stroke="{INK}" stroke-width="6"/>')
o.append('<g stroke="#C69E6B" stroke-width="2.5" opacity="0.5" fill="none"><path d="M 0 452 C 200 446, 420 458, 640 450 S 900 456, 1000 450"/><path d="M 0 480 C 240 486, 460 474, 700 482 S 920 476, 1000 482"/><path d="M 0 508 C 180 502, 520 512, 760 504 S 940 510, 1000 506"/></g>')
o.append(f'<path d="M -10 436 L 1010 436" stroke="#FFF3DC" stroke-width="4" opacity="0.8"/>')
o.append(f'<rect x="-10" y="528" width="1020" height="34" fill="url(#apron)" stroke="{INK}" stroke-width="6"/>')
o.append(f'<path d="M 0 538 L 1000 538" stroke="#D2A672" stroke-width="3" opacity="0.7"/>')
# patas de la mesa
for x in (60, 920):
    o.append(f'<rect x="{x}" y="562" width="30" height="140" fill="#8C6237" stroke="{INK}" stroke-width="6"/>')
o.append('<rect x="-10" y="562" width="1020" height="26" fill="#000" opacity="0.18"/>')

# caja izquierda (montada por el participante) y piezas planas
o.append('<g id="cajal">' + storage_box(150, 495, grain_seed=1) + '</g>')
pz = ['<g id="piezas">', '<ellipse cx="300" cy="497" rx="170" ry="14" fill="#3A2A1A" opacity="0.2"/>']
for k in range(5):
    y = 492 - k * 13
    xo = (k % 2) * 14 - 6
    pz.append(f'<path d="M {150 + xo} {y} L {200 + xo} {y - 20} L {440 + xo} {y - 20} L {390 + xo} {y} Z" fill="url(#wtop)" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    pz.append(f'<rect x="{150 + xo}" y="{y}" width="240" height="7" fill="#C99A63" stroke="{INK}" stroke-width="4"/>')
# hoja de instrucciones sobre la pila
pz.append(f'<g transform="rotate(-4 300 420)"><path d="M 240 418 L 268 404 L 372 404 L 344 418 Z" fill="#FFFFFF" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
          f'<path d="M 270 412 L 300 412 M 306 412 L 330 412" stroke="#8A97A6" stroke-width="3"/></g>')
pz.append('</g>')
o.append("".join(pz))
# caja derecha (ya montada)
o.append('<g id="cajar">' + storage_box(575, 495, grain_seed=2) + '</g>')
# herramientas sobre la mesa
o.append('<g id="llave">' + allen_key(120, 515, 1.0, -8) + '</g>')
o.append(screw(60, 470, 0.9, 20) + screw(470, 518, 0.8, -150))

# rótulos
s1, b1 = tag("lmontas", 298, 618, "LA MONTAS TÚ", size=28)
s2, b2 = tag("lmontada", 722, 618, "YA MONTADA", size=28)
o += [s1, s2]
# etiquetas de precio con cordel
for gid, cx, cy, ang, txt_, anchor in (("pl", 300, 150, -6, "0,78 $", (178, 290)), ("pr", 724, 150, 5, "0,48 $", (603, 290))):
    t, (hx, hy) = price_tag(cx, cy, txt_, ang)
    cord = f'<path d="M {f(hx)} {f(hy)} Q {f((hx + anchor[0]) / 2 - 20)} {f((hy + anchor[1]) / 2 + 10)} {f(anchor[0])} {f(anchor[1])}" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/><path d="M {f(hx)} {f(hy)} Q {f((hx + anchor[0]) / 2 - 20)} {f((hy + anchor[1]) / 2 + 10)} {f(anchor[0])} {f(anchor[1])}" fill="none" stroke="#E9DCC3" stroke-width="3" stroke-linecap="round"/>'
    o.append(f'<g id="{gid}">{cord}{t}</g>')
# insignia +63 %
o.append(f'<g id="badge"><path d="{star(512, 160, 84, 66, 18)}" fill="#C8FF2E" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
         + txt(512, 166, "+63 %", 36) + txt(512, 196, "MÁS", 20) + '</g>')
# pregunta
o.append(f'<g id="pregunta"><path d="M 300 70 L 700 70 Q 716 70 716 86 L 716 172 Q 716 188 700 188 L 560 188 L 520 226 L 524 188 L 300 188 Q 284 188 284 172 L 284 86 Q 284 70 300 70 Z" fill="url(#card)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
         + txt(500, 122, "¿CUÁNTO", 36) + txt(500, 166, "PAGARÍAS?", 36, fill="#2347FF") + '</g>')
o.append('</svg>')
open("cajas.svg", "w").write("\n".join(o))

from lib import *
src = open("cajas.py").read()
pre = src[:src.index("# caja izquierda")]
pre = pre.replace('lg("card"', 'lg("grey", [(0, "#C9CED6"), (1, "#8E96A3")]) + lg("card"')
import re
pre = re.sub(r"\n# reloj de pared.*?(?=\n# rodapié)", "", pre, flags=re.S)
g = {}
exec(pre, g)
o = g["o"]
x0, yb, w, h, dx, dy = 330, 495, 250, 190, 46, -38
B = ['<g id="caja">']
B.append(f'<ellipse cx="{x0 + w / 2 + dx / 2}" cy="{yb + 2}" rx="{w / 2 + 50}" ry="16" fill="#3A2A1A" opacity="0.22"/>')
# base
B.append(f'<path d="{poly([(x0, yb), (x0 + dx, yb + dy), (x0 + w + dx, yb + dy), (x0 + w, yb)], True)}" fill="url(#wtop)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
B.append(f'<path d="M {x0} {yb} L {x0 + w} {yb} L {x0 + w} {yb + 9} L {x0} {yb + 9} Z" fill="#C99A63" stroke="{INK}" stroke-width="4"/>')
# pared trasera (cara interior)
B.append(f'<rect x="{x0 + dx}" y="{yb + dy - h}" width="{w}" height="{h}" fill="url(#winner)" stroke="{INK}" stroke-width="6"/>')
B.append(f'<rect x="{x0 + dx + w / 2 - 42}" y="{yb + dy - h + 34}" width="84" height="26" rx="13" fill="#4A3018" stroke="{INK}" stroke-width="5"/>')
B.append(f'<path d="M {x0 + dx + 8} {yb + dy - h + 7} L {x0 + dx + w - 8} {yb + dy - h + 7}" stroke="#E7C79A" stroke-width="4" stroke-linecap="round"/>')
# pared izquierda (de pie)
B.append(f'<path d="{poly([(x0, yb), (x0 + dx, yb + dy), (x0 + dx, yb + dy - h), (x0, yb - h)], True)}" fill="url(#wside)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
B.append(f'<path d="M {x0 + 5} {yb - h + 8} L {x0 + dx - 4} {yb + dy - h + 6}" stroke="#FFF1D6" stroke-width="3.5" stroke-linecap="round"/>')
# tornillo a medio meter en la esquina
B.append(f'<circle cx="{x0 + dx + 14}" cy="{yb + dy - 20}" r="6" fill="#9AA3AD" stroke="{INK}" stroke-width="3"/>')
B.append('</g>')
o.append("".join(B))
# paneles sueltos sobre la mesa (frontal y lateral)
P = ['<g id="paneles">']
P.append(f'<path d="M 640 500 L 690 470 L 930 470 L 880 500 Z" fill="url(#wtop)" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/><rect x="640" y="500" width="240" height="8" fill="#C99A63" stroke="{INK}" stroke-width="4"/>')
P.append(f'<path d="M 740 482 Q 760 476 790 482" stroke="#4A3018" stroke-width="9" stroke-linecap="round"/>')
P.append(f'<path d="M 668 486 L 708 462 L 900 462 L 862 486 Z" fill="url(#wfront)" stroke="{INK}" stroke-width="5" stroke-linejoin="round" transform="translate(0 -18)"/>')
P.append('</g>')
o.append("".join(P))
o.append(screw(140, 500, 0.9, 10) + screw(250, 515, 0.85, 160) + screw(960, 520, 0.8, 200))
o.append('<g id="llave">' + allen_key(210, 470, 1.0, -20) + '</g>')
# flecha circular de "desmontar"
o.append(f'<g id="flecha">{arrow(None, 560, 230, 790, 430, CORAL, 10, 30, curve=(740, 210))}</g>')
# corazones
o.append(f'<g id="corazon">{heart(860, 170, 1.6)}</g>')
cr = heart(860, 170, 1.6, "#B8BEC8", "#E3E7EC")
cr += f'<path d="M 860 122 L 846 150 L 870 172 L 852 198 L 860 216" fill="none" stroke="{INK}" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"/>'
o.append(f'<g id="roto">{cr}</g>')
s, _ = tag("lsin", 200, 170, "SIN TERMINAR", size=28)
s = s.replace('<g id="lsin">', f'<g id="lsin"><line x1="270" y1="199" x2="352" y2="300" stroke="{INK}" stroke-width="5" stroke-linecap="round"/><circle cx="352" cy="300" r="9" fill="{LIME}" stroke="{INK}" stroke-width="4"/>')
o.append(s)
o.append("</svg>")
open("inacabada.svg", "w").write("\n".join(o))

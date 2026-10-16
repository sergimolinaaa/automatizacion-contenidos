from dib import *
o = [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 700">
<defs>{DEFS}
<linearGradient id="fl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E2BE8C"/><stop offset="1" stop-color="#C99A62"/></linearGradient>
</defs>
<rect width="500" height="700" fill="#FFE6DE"/><rect x="500" width="500" height="700" fill="#F0FFD6"/>
<rect y="470" width="1000" height="230" fill="url(#fl)"/>
<g stroke="#B8895A" stroke-width="2.5" opacity="0.5"><line x1="0" y1="530" x2="1000" y2="530"/><line x1="0" y1="600" x2="1000" y2="600"/><line x1="200" y1="470" x2="200" y2="530"/><line x1="760" y1="470" x2="760" y2="530"/><line x1="420" y1="530" x2="420" y2="600"/><line x1="900" y1="530" x2="900" y2="600"/></g>
<rect x="0" y="456" width="1000" height="16" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/>
''']
def scene(uid, ox, oy, s, off=False, shift=0):
    k = 1.15 / s
    g = [f'<g transform="translate({ox} {oy}) scale({s})">']
    g.append(f'<g id="{uid}conv">')
    g.append(mat((-150 + shift, -22), (148 + shift, -22), (140 + shift, 20), (-162 + shift, 20), cols=9, rows=3, k=k))
    g.append(capd(f"M {144+shift} -16 C {150+shift} -40 {156+shift} -36 {158+shift} -18", 7, "#FFFFFF", k))
    g.append(cart(100 + shift, -198, k=k, uid=uid))
    if off:
        g.append(f'<g id="{uid}bebe"><g transform="translate({-16+shift} 50)">{baby(k=k, uid=uid, hand=(118, -246))}</g></g>')
    else:
        g.append(f'<g id="{uid}bebe">{baby(k=k, uid=uid)}</g>')
    g.append('</g></g>')
    return "".join(g)
o.append('<clipPath id="cl"><rect x="0" y="0" width="497" height="700"/></clipPath><clipPath id="cr"><rect x="503" y="0" width="497" height="700"/></clipPath>')
o.append('<g clip-path="url(#cl)">' + scene("e15", 120, 630, 0.8) + '</g>')
o.append('<g clip-path="url(#cr)">' + scene("e21", 590, 586, 0.86, off=True, shift=20) + '</g>')
o.append(f'<line x1="500" y1="0" x2="500" y2="700" stroke="{INK}" stroke-width="7"/>')
# frenado (izq) y velocidad (der)
wx, wy = 120 + 158 * 0.8, 630 - 18 * 0.8
o.append(f'<g id="frena" stroke="{CORAL}" stroke-width="7" stroke-linecap="round">' + "".join(
    f'<path d="M {wx+dx:.0f} {wy+dy:.0f} L {wx+dx*1.5:.0f} {wy+dy*1.5:.0f}" stroke="{INK}" stroke-width="15"/><path d="M {wx+dx:.0f} {wy+dy:.0f} L {wx+dx*1.5:.0f} {wy+dy*1.5:.0f}"/>'
    for dx, dy in [(0, -34), (26, -26), (-26, -26), (36, 0)]) + '</g>')
o.append('<g id="vel" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round">' + "".join(
    f'<path d="M {x} {y} L {x+60} {y}" stroke="{INK}" stroke-width="15"/><path d="M {x} {y} L {x+60} {y}"/>' for x, y in [(518, 330), (530, 400), (516, 470)]) + '</g>')
# duda y acierto
o.append(f'<g id="duda"><circle cx="200" cy="272" r="40" fill="#FFFFFF" stroke="{INK}" stroke-width="6"/><circle cx="160" cy="322" r="9" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/>'
         f'<text x="200" y="296" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="68" fill="{CORAL}">?</text></g>')
o.append(f'<g id="ok"><circle cx="560" cy="250" r="40" fill="{LIME}" stroke="{INK}" stroke-width="6"/>'
         f'<path d="M 540 252 L 554 268 L 582 232" fill="none" stroke="{INK}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/></g>')
o.append(tag("t15", 300, 108, 190, "15 MESES", bg="#FFFFFF", fg=INK))
o.append(tag("t21", 640, 108, 200, "21 MESES", bg=INK, fg=LIME))
o.append(tag("lsigue", 240, 178, 240, "SIGUE ENCIMA", bg=CORAL, fg=INK, fs=26))
o.append(tag("lbaja", 700, 178, 230, "¡SE BAJA!", bg=LIME, fg=INK))
o.append('</svg>')
open("edades.svg", "w").write("\n".join(o))

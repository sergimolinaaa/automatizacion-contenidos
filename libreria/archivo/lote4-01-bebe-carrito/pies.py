from dib import *
S = 2.7
OX, OY = 300, 640
K = 1.3 / S
def g(x, y): return OX + x * S, OY + y * S
o = [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 700">
<defs>{DEFS}
<linearGradient id="wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFF4E2"/><stop offset="1" stop-color="#FBE2C2"/></linearGradient>
<linearGradient id="floor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E2BE8C"/><stop offset="1" stop-color="#C99A62"/></linearGradient>
</defs>
<rect width="1000" height="700" fill="url(#wall)"/>
<rect x="0" y="380" width="1000" height="320" fill="url(#floor)"/>
<g stroke="#B8895A" stroke-width="3" opacity="0.5"><line x1="0" y1="440" x2="1000" y2="440"/><line x1="0" y1="520" x2="1000" y2="520"/><line x1="0" y1="610" x2="1000" y2="610"/><line x1="380" y1="380" x2="380" y2="440"/><line x1="820" y1="440" x2="820" y2="520"/><line x1="160" y1="520" x2="160" y2="610"/></g>
<rect x="0" y="362" width="1000" height="22" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/>
''']
o.append(f'<g transform="translate({OX} {OY}) scale({S})">')
o.append(f'<g id="manta">{mat((-200,-24),(140,-24),(132,12),(-210,12),cols=8,rows=2,k=K)}</g>')
o.append('</g>')
# halo del obstáculo (detrás del bebé): silueta en lima
halo = (capd("M -18 -100 L -16 -24", 38 + 34 * K, LIME, K, ow=38 + 34 * K) + capd("M 16 -96 L 22 -24", 40 + 34 * K, LIME, K, ow=40 + 34 * K)
        + f'<path d="M -40 -252 C -60 -232 -66 -172 -58 -126 C -72 -110 -66 -84 -40 -78 C -10 -72 32 -74 52 -84 C 68 -96 68 -118 61 -134 C 68 -168 64 -228 42 -252 Z" fill="{LIME}" stroke="{LIME}" stroke-width="{34*K}" stroke-linejoin="round"/>'
        + f'<ellipse cx="20" cy="-10" rx="62" ry="22" fill="{LIME}"/>' + capd("M 20 -230 Q 60 -205 98 -198", 30 + 34 * K, LIME, K, ow=30 + 34 * K))
o.append(f'<g id="glow"><g transform="translate({OX} {OY}) scale({S})" opacity="0.85">{halo}</g></g>')
o.append(f'<g transform="translate({OX} {OY}) scale({S})">')
o.append(f'<g id="cuerda">' + capd("M 128 -10 C 136 -44 150 -40 158 -18", 7, "#FFFFFF", K) + capd("M 112 -14 C 124 -36 146 -34 156 -16", 7, "#FFFFFF", K) + f'<circle cx="157" cy="-18" r="4" fill="#FFFFFF" stroke="{INK}" stroke-width="{4*K}"/>' + '</g>')
o.append(f'<g id="carrito">{cart(100,-198,k=K,items=False)}</g>')
o.append(f'<g id="bebe">{baby(k=K, uid="pb", hand=(100,-196))}</g>')
o.append('</g>')
# marcas de frenado en la rueda
wx, wy = g(158, -18)
o.append(f'<g id="frena" stroke="{CORAL}" stroke-width="9" stroke-linecap="round">' + "".join(
    f'<path d="M {wx+dx*1.0:.0f} {wy+dy*1.0:.0f} L {wx+dx*1.45:.0f} {wy+dy*1.45:.0f}" stroke="{INK}" stroke-width="19"/><path d="M {wx+dx*1.0:.0f} {wy+dy*1.0:.0f} L {wx+dx*1.45:.0f} {wy+dy*1.45:.0f}"/>'
    for dx, dy in [(0,-62),(44,-44),(62,0),(-44,-44)]) + '</g>')
# peso: flecha + chevrones bajo los pies
o.append(arrow("peso", 95, 380, 95, 600, CORAL, w=14, head=34))
o.append(f'<g id="presion" stroke="{CORAL}" stroke-width="7" stroke-linecap="round" fill="none">' + "".join(
    f'<path d="M {x-14} {y} L {x} {y+12} L {x+14} {y}" stroke="{INK}" stroke-width="15"/><path d="M {x-14} {y} L {x} {y+12} L {x+14} {y}"/>'
    for x, y in [(g(-6,0)[0], 652), (g(44,0)[0], 652)]) + '</g>')
o.append(arrow("empuje", 640, 100, 840, 100, LIME, w=14, head=34))
o.append(tag("lpeso", 30, 300, 130, "PESO", bg=CORAL, fg=INK))
o.append(tag("latada", 470, 430, 160, "ATADA", 550, 488, g(136,-36)[0], g(136,-36)[1]))
o.append(tag("lobst", 30, 170, 300, "EL OBSTÁCULO", bg=LIME, fg=INK))
o.append(tag("lnada", 790, 200, 170, "¡NADA!", bg=CORAL, fg=INK))
o.append('</svg>')
open("pies.svg", "w").write("\n".join(o))

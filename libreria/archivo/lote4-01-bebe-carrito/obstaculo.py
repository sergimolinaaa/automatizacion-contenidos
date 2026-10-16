from dib import *
S = 1.55
OX, OY = 300, 800
K = 1.2 / S
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 860">\n<defs>{DEFS}</defs>']
# sombra suave en el "suelo" (sin fondo: flota sobre el azul de la marca)
o.append(f'<ellipse cx="520" cy="{OY+28}" rx="430" ry="34" fill="{INK}" opacity="0.25"/>')
o.append(f'<g transform="translate({OX} {OY}) scale({S})">')
o.append(f'<g id="manta">{mat((-170,-24),(150,-24),(140,22),(-180,22),cols=9,rows=3,k=K)}</g>')
o.append('</g>')
halo = (capd("M -18 -100 L -16 -24", 38 + 30 * K, LIME, K, ow=38 + 30 * K) + capd("M 16 -96 L 22 -24", 40 + 30 * K, LIME, K, ow=40 + 30 * K)
        + f'<path d="M -40 -252 C -60 -232 -66 -172 -58 -126 C -72 -110 -66 -84 -40 -78 C -10 -72 32 -74 52 -84 C 68 -96 68 -118 61 -134 C 68 -168 64 -228 42 -252 Z" fill="{LIME}" stroke="{LIME}" stroke-width="{30*K}" stroke-linejoin="round"/>'
        + f'<circle cx="16" cy="-310" r="{63+14*K:.0f}" fill="{LIME}"/><ellipse cx="-14" cy="-304" rx="22" ry="26" fill="{LIME}"/>'
        + f'<ellipse cx="20" cy="-10" rx="62" ry="22" fill="{LIME}"/>' + capd("M 20 -230 Q 60 -205 98 -198", 30 + 30 * K, LIME, K, ow=30 + 30 * K))
o.append(f'<g id="glow"><g transform="translate({OX} {OY}) scale({S})" opacity="0.9">{halo}</g></g>')
o.append(f'<g transform="translate({OX} {OY}) scale({S})">')
o.append(f'<g id="cuerda">' + capd("M 144 -16 C 150 -40 156 -36 158 -18", 7, "#FFFFFF", K) + '</g>')
o.append(f'<g id="carrito">{cart(100,-198,k=K,uid="oc")}</g>')
o.append(f'<g id="bebe">{baby(k=K, uid="ob")}</g>')
o.append('</g>')
o.append(arrow("peso", 120, 470, 120, 700, CORAL, w=14, head=34))
o.append(tag("lpeso", 55, 400, 130, "PESO", bg=CORAL, fg=INK))
o.append(tag("lobst", 520, 120, 330, "EL OBSTÁCULO", 520, 178, 400, 260, bg=LIME, fg=INK))
o.append(f'<g id="duda"><circle cx="150" cy="170" r="50" fill="#FFFFFF" stroke="{INK}" stroke-width="6"/><circle cx="206" cy="232" r="11" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/>'
         f'<text x="150" y="198" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="78" fill="{CORAL}">?</text></g>')
o.append('</svg>')
open("obstaculo.svg", "w").write("\n".join(o))

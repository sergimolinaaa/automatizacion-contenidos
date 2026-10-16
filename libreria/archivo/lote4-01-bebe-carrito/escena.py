from dib import *

BX, BY = 225, 596          # pies del bebé (sobre la manta)
HX, HY = BX + 100, BY - 192  # asa
FL, FR, NR, NL = (66, 574), (372, 574), (360, 620), (44, 620)

o = [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 700">
<defs>{DEFS}
<linearGradient id="wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFF4E2"/><stop offset="1" stop-color="#FBE2C2"/></linearGradient>
<linearGradient id="floor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E2BE8C"/><stop offset="1" stop-color="#C99A62"/></linearGradient>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#CDEBFF"/><stop offset="1" stop-color="#EAF6FF"/></linearGradient>
<linearGradient id="can" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8C96A8"/><stop offset="0.35" stop-color="#F1F4F8"/><stop offset="1" stop-color="#7D879A"/></linearGradient>
</defs>
<rect width="1000" height="700" fill="url(#wall)"/>
''']
# fondo lejano (sin contorno, desaturado)
o.append('<g opacity="0.9">')
o.append('<rect x="440" y="70" width="230" height="200" rx="10" fill="#E9D3B4"/><rect x="455" y="85" width="200" height="170" rx="6" fill="url(#sky)"/>'
         '<rect x="551" y="85" width="8" height="170" fill="#E9D3B4"/><rect x="455" y="166" width="200" height="8" fill="#E9D3B4"/>'
         '<ellipse cx="510" cy="130" rx="34" ry="12" fill="#FFFFFF" opacity="0.8"/><ellipse cx="610" cy="210" rx="26" ry="9" fill="#FFFFFF" opacity="0.7"/>')
# estantería con juguetes
o.append('<rect x="40" y="250" width="150" height="205" rx="6" fill="#E8CFAE"/><rect x="40" y="320" width="150" height="8" fill="#D9BC96"/><rect x="40" y="390" width="150" height="8" fill="#D9BC96"/>'
         '<rect x="56" y="282" width="34" height="38" rx="4" fill="#F7B5B5"/><rect x="96" y="290" width="30" height="30" rx="4" fill="#B5D8F7"/><circle cx="152" cy="300" r="20" fill="#F7DFA0"/>'
         '<rect x="60" y="352" width="22" height="38" rx="3" fill="#B9E3C6"/><rect x="86" y="346" width="22" height="44" rx="3" fill="#F2C4A0"/><rect x="112" y="356" width="22" height="34" rx="3" fill="#C9B9E8"/>'
         '<circle cx="160" cy="430" r="22" fill="#F7C3D6"/><rect x="62" y="418" width="44" height="34" rx="6" fill="#B5D8F7"/>')
# cámara del laboratorio en trípode
o.append('<g fill="#C7B9A6"><rect x="760" y="150" width="80" height="50" rx="8"/><circle cx="752" cy="175" r="18"/><rect x="796" y="200" width="8" height="150"/>'
         '<path d="M 800 340 L 770 455 L 778 455 L 800 360 L 822 455 L 830 455 Z"/></g>'
         '<circle cx="752" cy="175" r="9" fill="#AFA08C"/><circle cx="828" cy="162" r="4" fill="#F08A7A"/>')
# metro de altura en la pared
o.append('<rect x="250" y="120" width="34" height="300" rx="6" fill="#F3E3A6"/>' + "".join(
    f'<rect x="250" y="{y}" width="{16 if (y//30)%2 else 24}" height="3" fill="#D9C27C"/>' for y in range(135, 420, 15)))
o.append('</g>')
# rodapié y suelo
o.append('<rect x="0" y="455" width="1000" height="700" fill="url(#floor)"/>')
o.append('<g stroke="#B8895A" stroke-width="2.5" opacity="0.55">' + "".join(
    f'<line x1="0" y1="{y}" x2="1000" y2="{y}"/>' for y in (492, 536, 588, 648)) + "".join(
    f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{y1}"/>' for x, y0, y1 in [(120, 455, 492), (520, 455, 492), (860, 455, 492), (300, 492, 536), (700, 492, 536), (90, 536, 588), (480, 536, 588), (900, 536, 588), (260, 588, 648), (640, 588, 648)]) + '</g>')
o.append(f'<rect x="0" y="440" width="1000" height="18" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/>')

# mamá (más atrás)
o.append(f'<g id="mama"><g transform="translate(838 548) scale(1.6)">{mom(k=1/1.6*1.15)}</g></g>')
# corazón/brillos de éxito
o.append('<g id="yay">' + "".join(
    f'<path d="M {x} {y-16} L {x+5} {y-5} L {x+16} {y} L {x+5} {y+5} L {x} {y+16} L {x-5} {y+5} L {x-16} {y} L {x-5} {y-5} Z" fill="{LIME}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
    for x, y in [(700, 250), (760, 120), (650, 170)]) +
    f'<path d="M 905 150 C 905 130 935 130 935 150 C 935 130 965 130 965 150 C 965 172 935 186 935 196 C 935 186 905 172 905 150 Z" fill="{CORAL}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/></g>')

o.append('<g id="convoy">')
o.append(f'<g id="manta">{mat(FL, FR, NR, NL, cols=10, rows=3)}</g>')
# cordón que ata la manta al eje trasero
o.append(f'<g id="cuerda">' + capd(f"M {FR[0]-4} {FR[1]+6} Q {FR[0]+8} {FR[1]+2} {HX+58} {BY-22}", 5, "#F2F2F2") +
         capd(f"M {NR[0]-4} {NR[1]-8} Q {NR[0]+16} {NR[1]-14} {HX+58} {BY-16}", 5, "#F2F2F2") + '</g>')
o.append(f'<g id="carrito">{cart(HX, HY)}</g>')
# bote con arena (condición de control)
cx, cy = 92, 604
o.append(f'<g id="bote"><ellipse cx="{cx}" cy="{cy}" rx="48" ry="10" fill="{INK}" opacity="0.25"/>'
         f'<path d="M {cx-44} {cy-110} L {cx-44} {cy-6} A 44 12 0 0 0 {cx+44} {cy-6} L {cx+44} {cy-110} Z" fill="url(#can)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
         f'<rect x="{cx-44}" y="{cy-82}" width="88" height="46" fill="#FF8A3D" stroke="{INK}" stroke-width="4"/>'
         f'<text x="{cx}" y="{cy-50}" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="22" fill="{INK}">ARENA</text>'
         f'<ellipse cx="{cx}" cy="{cy-110}" rx="44" ry="12" fill="#C9CFD9" stroke="{INK}" stroke-width="6"/>'
         f'<ellipse cx="{cx}" cy="{cy-110}" rx="32" ry="7" fill="#E7C487"/>'
         f'<path d="M {cx-40} {cy-104} Q {cx} {cy-150} {cx+40} {cy-104}" fill="none" stroke="{INK}" stroke-width="5"/>'
         f'<rect x="{cx-30}" y="{cy-100}" width="8" height="86" rx="4" fill="#FFFFFF" opacity="0.6"/></g>')
o.append(f'<g id="bebe"><g transform="translate({BX} {BY})">{baby(uid="b1")}</g></g>')
# bebé fuera de la manta (más cerca de la cámara, junto a ella)
o.append(f'<g id="bebe2"><g transform="translate({BX-16} {BY+48})">{baby(uid="b2", hand=(116, -240))}</g></g>')
o.append('</g>')

# líneas de velocidad
o.append('<g id="vel" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round">' + "".join(
    f'<path d="M {x} {y} L {x+70} {y}" stroke="{INK}" stroke-width="15"/><path d="M {x} {y} L {x+70} {y}"/>' for x, y in [(10, 360), (30, 430), (0, 500)]) + '</g>')
# pregunta
o.append(f'<g id="duda"><circle cx="400" cy="170" r="46" fill="#FFFFFF" stroke="{INK}" stroke-width="6"/>'
         f'<circle cx="352" cy="226" r="10" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/><circle cx="334" cy="250" r="6" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/>'
         f'<text x="400" y="196" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="74" fill="{CORAL}">?</text></g>')
o.append(arrow("empuje", 470, 290, 620, 290, LIME, w=12))
o.append(tag("lmanta", 20, 470, 130, "MANTA", 85, 528, 120, 592))
o.append(tag("lbote", 24, 214, 290, "BOTE DE ARENA", 80, 272, 84, 470))
o.append(tag("lmama", 840, 74, 120, "MAMÁ", 900, 132, 892, 190))
o.append('</svg>')
open("escena.svg", "w").write("\n".join(o))

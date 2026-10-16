from vc import *

OUT = "oficina.svg"
defs = BASE_DEFS + EXTRA_DEFS + lg("wallO", [(0, "#FFF4D6"), (1, "#F3DFAE")]) + lg("cntTop", [(0, "#F7F7FA"), (1, "#C9CDD8")]) \
    + lg("cntFront", [(0, "#3E63C9"), (1, "#28449A")]) + lg("glassO", [(0, "#E8F6FF", 0.55), (1, "#BFE0F5", 0.35)]) + lg("formG", [(0, "#FFFFFF"), (1, "#EEF0F5")])
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 700">\n<defs>{defs}</defs>']
o.append('<rect width="1000" height="700" fill="url(#wallO)"/>')
o.append('<g fill="#EFD9A2" opacity="0.6">' + "".join(f'<rect x="{x}" y="0" width="26" height="430"/>' for x in range(30, 1000, 80)) + "</g>")
# rótulo genérico
o.append(f'<g id="rotulo"><rect x="415" y="62" width="320" height="78" rx="14" fill="{YEL}" stroke="{INK}" stroke-width="6"/>'
         + sobre(472, 101, 62, 42, 0, fill="#FFFFFF", sw=4) + T(624, 113, "CORREOS", 32, INK, font=DISP) + "</g>")

# caja fuerte (fondo derecha)
CX0, CY0, CW, CH = 700, 150, 250, 280
o.append(f'<g id="caja"><rect x="{CX0+12}" y="{CY0+14}" width="{CW}" height="{CH}" rx="16" fill="{INK}" opacity="0.25"/>'
         f'<rect x="{CX0}" y="{CY0}" width="{CW}" height="{CH}" rx="16" fill="url(#steelD)" stroke="{INK}" stroke-width="7"/>'
         f'<rect x="{CX0+22}" y="{CY0+22}" width="{CW-44}" height="{CH-44}" rx="10" fill="url(#steelG)" stroke="{INK}" stroke-width="5"/>'
         f'<path d="M {CX0+34} {CY0+40} L {CX0+34} {CY0+CH-60}" stroke="#D5DCE8" stroke-width="7" stroke-linecap="round" opacity="0.8"/>')
DX, DY = CX0 + CW / 2, CY0 + CH / 2 - 34
o.append(f'<circle cx="{DX}" cy="{DY}" r="52" fill="#C9D1DF" stroke="{INK}" stroke-width="6"/><circle cx="{DX}" cy="{DY}" r="34" fill="url(#steelD)" stroke="{INK}" stroke-width="5"/>')
o.append(f'<g id="rueda">' + "".join(f'<line x1="{f(DX+30*math.cos(a))}" y1="{f(DY+30*math.sin(a))}" x2="{f(DX+50*math.cos(a))}" y2="{f(DY+50*math.sin(a))}" stroke="{INK}" stroke-width="5"/>' for a in [i * math.pi / 6 for i in range(12)])
         + f'<path d="M {DX} {DY} L {DX} {DY-28}" stroke="{CORAL}" stroke-width="7" stroke-linecap="round"/></g>')
o.append(f'<rect x="{CX0+CW-46}" y="{CY0+110}" width="18" height="70" rx="9" fill="#C9D1DF" stroke="{INK}" stroke-width="5"/>')
for yy in (CY0 + 50, CY0 + CH - 70):
    o.append(f'<rect x="{CX0-8}" y="{yy}" width="18" height="40" rx="5" fill="#3C465C" stroke="{INK}" stroke-width="4"/>')
o.append("</g>")
# candado (sobre la caja)
LX, LY = DX, CY0 + CH - 46
o.append(f'<g id="candado"><path d="M {LX-24} {LY-10} L {LX-24} {LY-34} C {LX-24} {LY-66}, {LX+24} {LY-66}, {LX+24} {LY-34} L {LX+24} {LY-10}" fill="none" stroke="{INK}" stroke-width="16"/>'
         f'<path d="M {LX-24} {LY-10} L {LX-24} {LY-34} C {LX-24} {LY-66}, {LX+24} {LY-66}, {LX+24} {LY-34} L {LX+24} {LY-10}" fill="none" stroke="#C9D1DF" stroke-width="8"/>'
         f'<rect x="{LX-40}" y="{LY-14}" width="80" height="64" rx="12" fill="url(#yelG)" stroke="{INK}" stroke-width="6"/>'
         f'<circle cx="{LX}" cy="{LY+12}" r="8" fill="{INK}"/><path d="M {LX} {LY+14} L {LX} {LY+32}" stroke="{INK}" stroke-width="7" stroke-linecap="round"/></g>')
# saca junto a la caja
o.append(saca(625, 448, 120, 150, id_="saca"))

# ventanilla: mampara de cristal (izquierda)
o.append(f'<rect x="40" y="170" width="510" height="270" rx="10" fill="#C7B489" opacity="0.35"/>')
o.append(f'<g id="mampara"><rect x="40" y="170" width="510" height="270" rx="10" fill="url(#glassO)" stroke="{INK}" stroke-width="6"/>'
         f'<path d="M 295 170 L 295 440" stroke="{INK}" stroke-width="6"/>'
         f'<path d="M 80 200 L 140 200 L 80 290 Z M 335 200 L 385 200 L 335 270 Z" fill="#FFFFFF" opacity="0.6"/>'
         f'<rect x="140" y="395" width="310" height="45" rx="6" fill="#E9E2CC" stroke="{INK}" stroke-width="5"/></g>')

# mostrador
o.append(f'<path d="M 0 440 L 1000 440 L 1000 500 L 0 500 Z" fill="url(#cntTop)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
o.append(f'<rect x="0" y="500" width="1000" height="200" fill="url(#cntFront)" stroke="{INK}" stroke-width="7"/>')
o.append(f'<path d="M 10 452 L 990 452" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity="0.9"/>')
o.append('<g stroke="#1F3780" stroke-width="5" opacity="0.6">' + "".join(f'<line x1="{x}" y1="520" x2="{x}" y2="700"/>' for x in (250, 500, 750)) + "</g>")

# objetos sobre el mostrador
# formulario de solicitud
FX, FY = 300, 462
o.append(f'<g id="form"><g transform="rotate(-6 {FX} {FY})"><rect x="{FX-95}" y="{FY-150}" width="190" height="170" rx="6" fill="{INK}" opacity="0.2" transform="translate(8 8)"/>'
         f'<rect x="{FX-95}" y="{FY-150}" width="190" height="170" rx="6" fill="url(#formG)" stroke="{INK}" stroke-width="5"/>'
         f'<rect x="{FX-95}" y="{FY-150}" width="190" height="34" rx="6" fill="{YEL}" stroke="{INK}" stroke-width="4"/>'
         + T(FX, FY - 126, "SOLICITUD", 18, INK, font=DISP)
         + "".join(f'<path d="M {FX-75} {FY-92+i*24} L {FX+(60 if i%2 else 75)} {FY-92+i*24}" stroke="#9AA3B5" stroke-width="6" stroke-linecap="round"/>' for i in range(4))
         + f'<rect x="{FX-75}" y="{FY-24}" width="18" height="18" rx="3" fill="#FFFFFF" stroke="{INK}" stroke-width="3"/>'
         + f'<path d="M {FX-72} {FY-16} L {FX-66} {FY-9} L {FX-54} {FY-26}" fill="none" stroke="{CORAL}" stroke-width="5" stroke-linecap="round"/>'
         + "</g></g>")
o.append(dni(130, 455, 170, -10, id_="dni"))
# sobre a entregar
o.append(cert_envelope(480, 430, 190, 124, 5, id_="sobreE", text="VOTO", franq=False))
# sello CERTIFICADO
o.append(stamp(480, 420, "CERTIFICADO", 22, rot=-10, id_="sello"))

# etiquetas de plazos
s, _ = label("l19", 295, 250, "PIDE: HASTA 19 NOV", bg=INK, fg=LIME, size=30); o.append(s.replace('id="l19"', 'id="l19"'))
s, _ = label("l25", 295, 250, "ENTREGA: HASTA 25 NOV", bg=INK, fg=LIME, size=28); o.append(s)
s, _ = label("lgratis", 480, 330, "GRATIS", bg=LIME, fg=INK, size=30); o.append(s)
s, _ = label("lcust", 825, 105, "CUSTODIA", bg=CORAL, fg="#FFFFFF", size=30); o.append(s)
o.append("</svg>")
save(OUT, "\n".join(o))

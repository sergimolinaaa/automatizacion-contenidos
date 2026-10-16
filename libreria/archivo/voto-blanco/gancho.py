from vb import *

OUT = "gancho_full.svg"
extra = lg("wallG", [(0, "#E9EEF7"), (1, "#CBD5E6")]) + lg("floorG", [(0, "#C98B55"), (1, "#8A5A31")]) + rg("burstY", [(0, "#FFF2A8"), (1, YEL)])
o = [header(1080, 1920, extra)]
o.append('<rect width="1080" height="1920" fill="url(#wallG)"/>')
# friso de pared y zócalo
o.append(f'<rect x="0" y="380" width="1080" height="24" fill="#B9C4D8"/>')
o.append('<g stroke="#D5DDEA" stroke-width="3">' + "".join(f'<line x1="{x}" y1="404" x2="{x}" y2="1180"/>' for x in range(60, 1080, 120)) + "</g>")
o.append(f'<path d="M 0 1180 L 1080 1180 L 1080 1920 L 0 1920 Z" fill="url(#floorG)"/>')
o.append(f'<path d="M 0 1180 L 1080 1180" stroke="{INK}" stroke-width="7"/>')
o.append('<g fill="none" stroke="#7A4E2A" stroke-width="3" opacity="0.5">' + "".join(
    f'<path d="M 0 {y} L 1080 {y}"/>' for y in (1260, 1360, 1480, 1620, 1780)) + "</g>")
# mesa electoral
o.append(f'<rect x="150" y="1100" width="780" height="40" rx="8" fill="url(#woodG)" stroke="{INK}" stroke-width="7"/>')
o.append(f'<rect x="190" y="1140" width="30" height="110" fill="#6E4524" stroke="{INK}" stroke-width="6"/>')
o.append(f'<rect x="860" y="1140" width="30" height="110" fill="#6E4524" stroke="{INK}" stroke-width="6"/>')
o.append(f'<path d="M 170 1108 L 900 1108" stroke="#E6B98A" stroke-width="5" stroke-linecap="round"/>')

# urna sobre la mesa
u, slot = urna(520, 1100, 330, 290, "VOTO", n_sobres=7, seed=7)
o.append(g("urna", u))
print("slot", slot)

# partidos ficticios (fila superior)
xs = [170, 355, 540, 725, 910]
row = ""
for x, p in zip(xs, PARTIES):
    row += f'<g id="p{p[2]}"><circle cx="{x}" cy="508" r="44" fill="#FFFFFF" stroke="{INK}" stroke-width="6"/>' + icon(p[2], x, 510, 26, p[1]) + "</g>"
o.append(g("partidos", row))

# sobre vacío flotando sobre la ranura
SX, SY = slot[0], 714
o.append(g("sobre", envelope(SX, SY, 230, 148)))
# rayitas de movimiento


# etiquetas del gancho
s, _ = label("t29", 185, 640, "29-N", bg=CORAL, fg="#FFFFFF", size=34); o.append(s)
s, _ = label("tcast", 870, 668, "¿CASTIGO?", bg=INK, fg=LIME, size=30); o.append(s)
s, _ = label("tblanco", 185, 735, "EN BLANCO", bg="#FFFFFF", fg=INK, size=28); o.append(s)
# interrogante grande
o.append(f'<g id="duda"><circle cx="880" cy="900" r="62" fill="url(#burstY)" stroke="{INK}" stroke-width="6"/>' + T(880, 930, "?", 84, INK, font=DISP) + "</g>")

# escena 2: sin papeleta / válido / ley
s, _ = label("tsinpap", 185, 900, "SIN PAPELETA", bg="#FFFFFF", fg=INK, size=26); o.append(s)
o.append(check(890, 900, 64, id_="valido"))
s, _ = label("tvalido", 890, 1010, "VÁLIDO", bg=LIME, fg=INK, size=30); o.append(s)
s, _ = label("tley", 540, 1215, "LOREG · ART. 96.5", bg=INK, fg=LIME, size=28); o.append(s)
o.append("</svg>")
save(OUT, "\n".join(o))

from pn import *

OUT = "gancho_full.svg"
o = [header(1080, 1920, SEPIA + lg("wallG", [(0, "#E9EEF7"), (1, "#CBD5E6")]) + lg("floorG", [(0, "#C98B55"), (1, "#8A5A31")]) + rg("burstY", [(0, "#FFF2A8"), (1, YEL)]))]
o.append('<rect width="1080" height="1920" fill="url(#wallG)"/>')
o.append('<g stroke="#D5DDEA" stroke-width="3">' + "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="1300"/>' for x in range(60, 1080, 120)) + "</g>")
o.append('<rect x="0" y="1300" width="1080" height="620" fill="url(#woodG)"/>')
o.append(f'<path d="M 0 1300 L 1080 1300" stroke="{INK}" stroke-width="7"/>')
o.append('<g fill="none" stroke="#7A4E2A" stroke-width="3" opacity="0.5">' + "".join(f'<path d="M 0 {y} L 1080 {y}"/>' for y in (1380, 1480, 1600, 1740)) + "</g>")

BX, BY, BW, BH = 540, 925, 450, 590
b, ys = ballot(BX, BY, BW, BH, "star", rows=6)
ROT = -3
o.append(f'<g id="papeleta"><g transform="rotate({ROT} {BX} {BY})">{b}'
         # tachón sobre el nombre nº 2
         + scribble(BX - BW * 0.32, BX + BW * 0.3, ys[1], 16, 9, sw=12, id_="tachon")
         + "</g></g>")
# números resaltados (orden fijo) en escena 1
x0 = BX - BW / 2
nums = "".join(f'<circle cx="{f(x0+BW*0.12)}" cy="{f(y+2)}" r="22" fill="none" stroke="{CORAL}" stroke-width="6"/>' for y in ys[:3])
o.append(f'<g id="nums"><g transform="rotate({ROT} {BX} {BY})">{nums}</g></g>')
# bolígrafo (punta al final del tachón)
o.append(pen(BX + BW * 0.3 + 6, ys[1] + 18, 330, rot=-38, id_="boli"))
# sello NULO
o.append(stamp2(BX + 40, BY + 170, "NULO", 92, rot=-12, id_="nulo"))
# etiquetas gancho
s, _ = label("t29", 160, 590, "29-N", bg=CORAL, fg="#FFFFFF", size=36); o.append(s)
s, _ = label("tcong", 910, 590, "CONGRESO", bg=INK, fg=LIME, size=30); o.append(s)
s, _ = label("tunvoto", 175, 1268, "1 TACHÓN", bg="#FFFFFF", fg=INK, size=30); o.append(s)
s, _ = label("tcero", 905, 1268, "0 VOTOS", bg=CORAL, fg="#FFFFFF", size=30); o.append(s)
# escena 1: lista cerrada
o.append(lock(880, 760, 92, id_="candado"))
s, _ = label("torden", 150, ys[0]+80, "ORDEN", bg="#FFFFFF", fg=INK, size=28, target=(x0 + 22, ys[0]), src=(150, ys[0]+80)); o.append(s)
s, _ = label("tpartido", 540, 1268, "LO DECIDE EL PARTIDO", bg=LIME, fg=INK, size=30); o.append(s)
o.append("</svg>")
save(OUT, "\n".join(o))

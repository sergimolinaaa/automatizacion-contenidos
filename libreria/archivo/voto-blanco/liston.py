from vb import *

OUT = "liston.svg"
PX = 0.5          # px por voto (zona ampliada del eje)
GROUND = 640
Y3000 = 450
y_of = lambda v: Y3000 - (v - 3000) * PX
YR = y_of(3100)   # 400
YB2 = y_of(3270)  # 315
print("y 3100", YR, "y 3270", YB2)
extra = lg("skyL", [(0, "#DDEBFF"), (1, "#F4F8FF")]) + lg("trackG", [(0, "#E2603F"), (1, "#B9432A")]) + lg("matG", [(0, "#4F7BE0"), (1, "#2D50A8")])
o = [header(1000, 700, extra)]
o.append('<rect width="1000" height="700" fill="url(#skyL)"/>')
# gradas difuminadas al fondo
o.append('<g opacity="0.35">' + "".join(f'<rect x="0" y="{y}" width="1000" height="16" fill="#B7C6DE"/>' for y in (520, 560, 600)) + "</g>")
# pista
o.append(f'<rect x="0" y="{GROUND}" width="1000" height="60" fill="url(#trackG)"/>')
o.append(f'<path d="M 0 {GROUND} L 1000 {GROUND}" stroke="{INK}" stroke-width="6"/>')
o.append(f'<path d="M 0 {GROUND+30} L 1000 {GROUND+30}" stroke="#FFFFFF" stroke-width="4" stroke-dasharray="30 20" opacity="0.7"/>')

# postes
for x in (110, 890):
    o.append(f'<rect x="{x-14}" y="140" width="28" height="{GROUND-140}" rx="8" fill="url(#poleG)" stroke="{INK}" stroke-width="6"/>')
    o.append(f'<rect x="{x-40}" y="{GROUND-16}" width="80" height="22" rx="6" fill="#5E6A82" stroke="{INK}" stroke-width="5"/>')
    o.append('<g stroke="#6F7B93" stroke-width="3">' + "".join(f'<line x1="{x-10}" y1="{y}" x2="{x+10}" y2="{y}"/>' for y in range(170, GROUND - 20, 30)) + "</g>")

# columna de Rombo (3.100 votos)
CX, CW = 360, 170
col = f'<rect x="{CX-CW/2+8}" y="{YR+10}" width="{CW}" height="{GROUND-YR}" rx="10" fill="{INK}" opacity="0.2"/>'
col += f'<rect x="{CX-CW/2}" y="{YR}" width="{CW}" height="{GROUND-YR+4}" rx="10" fill="url(#colG)" stroke="{INK}" stroke-width="7"/>'
col += f'<path d="M {CX-CW/2+18} {YR+16} L {CX-CW/2+18} {GROUND-14}" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round" opacity="0.7"/>'
col += f'<circle cx="{CX}" cy="{YR+75}" r="46" fill="#FFFFFF" stroke="{INK}" stroke-width="6"/>' + icon("diamond", CX, YR + 75, 30, COL["ROMBO"])
col += T(CX, YR + 168, "ROMBO", 28, INK)
o.append(g("rombo", col))
s, _ = label("t3100", CX, YR + 215, "3.100", bg=INK, fg=LIME, size=30); o.append(s)

# montón de votos en blanco
pile = ""
for i in range(4):
    pile += sobre(660 + (i % 2) * 14 - 7, GROUND - 22 - i * 26, 150, 44, (-4, 3, -2, 5)[i], sw=4.5)
o.append(g("monton", pile))

# listón (barra de salto) con sus etiquetas
bar = f'<rect x="96" y="{Y3000-10}" width="808" height="20" rx="10" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/>'
bar += "".join(f'<rect x="{x}" y="{Y3000-7}" width="40" height="14" fill="{CORAL}"/>' for x in range(120, 880, 80))
bar += f'<path d="M 110 {Y3000-4} L 890 {Y3000-4}" stroke="#FFFFFF" stroke-width="3" opacity="0.6"/>'
inner = g("barra", bar)
s, _ = label("t3", 700, Y3000 - 48, "LISTÓN: 3 %", bg=CORAL, fg="#FFFFFF", size=28); inner += s
s, _ = label("t3000", 700, Y3000 - 48, "3 % = 3.000", bg=CORAL, fg="#FFFFFF", size=28); inner += s
s, _ = label("t3270", 700, Y3000 - 48, "3 % = 3.270", bg=CORAL, fg="#FFFFFF", size=28); inner += s
o.append(g("liston", inner))

# contador de votos válidos
s, _ = label("v100", 690, 100, "100.000 VÁLIDOS", bg=INK, fg=LIME, size=30); o.append(s)
s, _ = label("v109", 690, 100, "109.000 VÁLIDOS", bg=INK, fg=LIME, size=30); o.append(s)
s, _ = label("tmas", 690, 172, "+9.000 EN BLANCO", bg="#FFFFFF", fg=INK, size=28); o.append(s)
s, _ = label("tley", 690, 172, "LOREG · ART. 163.1", bg="#FFFFFF", fg=INK, size=28); o.append(s)
# sellos
o.append(stamp2(330, 250, "ENTRA", 40, rot=-6, col="#3E8E1E", id_="entra"))
o.append(stamp2(330, 215, "NO LLEGA", 38, rot=-6, col=CORAL, id_="nollega"))
o.append("</svg>")
save(OUT, "\n".join(o))

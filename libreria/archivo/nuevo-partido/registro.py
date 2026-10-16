from np import *

OUT = "registro_free.svg"
defs = BASE_DEFS + NP_DEFS + lg("carnetG", [(0, "#F4FBFA"), (1, "#D5ECE9")])
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000">\n<defs>{defs}</defs>']

# ---------- A: inscrito en el Registro ----------
s, _ = label("tinterior", 500, 120, "MINISTERIO DEL INTERIOR", bg=INK, fg=LIME, size=30); o.append(s)
CX, CY, W, H = 500, 440, 680, 420
x, y = CX - W / 2, CY - H / 2
c = f'<g transform="rotate(-3 {CX} {CY})">'
c += f'<rect x="{x+12}" y="{y+16}" width="{W}" height="{H}" rx="30" fill="{INK}" opacity="0.25"/>'
c += f'<rect x="{x}" y="{y}" width="{W}" height="{H}" rx="30" fill="url(#carnetG)" stroke="{INK}" stroke-width="8"/>'
c += f'<path d="M {x} {y+96} L {x} {y+30} Q {x} {y} {x+30} {y} L {x+W-30} {y} Q {x+W} {y} {x+W} {y+30} L {x+W} {y+96} Z" fill="url(#tealS)" stroke="{INK}" stroke-width="8"/>'
c += T(CX, y + 46, "REGISTRO DE", 30, "#FFFFFF", font=DISP) + T(CX, y + 82, "PARTIDOS POLÍTICOS", 30, "#FFFFFF", font=DISP)
# «foto»: el logo genérico
c += f'<rect x="{x+36}" y="{y+128}" width="200" height="240" rx="16" fill="#FFFFFF" stroke="{INK}" stroke-width="6"/>'
c += logo(x + 136, y + 248, 76)
# datos
c += T(x + 270, y + 165, "NOMBRE", 22, "#5A6170", anchor="start")
c += T(x + 270, y + 210, "DEMOCRACIA 21", 38, INK, anchor="start", font=DISP)
c += T(x + 270, y + 262, "INSCRIPCIÓN", 22, "#5A6170", anchor="start")
c += "".join(f'<path d="M {x+270} {y+300+k*34} L {x+W-(60 if k else 150)} {y+300+k*34}" stroke="#9AB7B3" stroke-width="12" stroke-linecap="round"/>' for k in range(2))
c += f'<rect x="{x+W-120}" y="{y+120}" width="70" height="56" rx="8" fill="#E2B84C" stroke="{INK}" stroke-width="5"/>'
c += f'<path d="M {x+22} {y+120} L {x+22} {y+H-30}" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round" opacity="0.8"/>'
c += "</g>"
o.append(G("carnet", c))
s, _ = label("tjunio", 560, 538, "JUNIO 2026", bg=CORAL, fg="#FFFFFF", size=34); o.append(s)
o.append(stamp(680, 650, "INSCRITO", 50, rot=-10, col=TEAL_D, id_="sello"))
o.append(check(880, 560, 46, id_="chk"))
s, _ = label("tdni", 500, 760, "= SU «DNI» DE PARTIDO", bg=INK, fg=LIME, size=32); o.append(s)

# ---------- B: firmas ----------
s, _ = label("tesc", 500, 110, "0 ESCAÑOS PREVIOS", bg=CORAL, fg="#FFFFFF", size=32); o.append(s)
s, _ = label("tdefesc", 500, 175, "ESCAÑO = ASIENTO EN LAS CORTES", bg=INK, fg=LIME, size=22); o.append(s)
# portapapeles con firmas
KX, KY, KW, KH = 290, 520, 340, 430
rnd = random.Random(5)
k = f'<g transform="rotate(-5 {KX} {KY})">'
k += f'<rect x="{KX-KW/2+10}" y="{KY-KH/2+14}" width="{KW}" height="{KH}" rx="18" fill="{INK}" opacity="0.25"/>'
k += f'<rect x="{KX-KW/2}" y="{KY-KH/2}" width="{KW}" height="{KH}" rx="18" fill="url(#clipG)" stroke="{INK}" stroke-width="7"/>'
k += f'<rect x="{KX-KW/2+22}" y="{KY-KH/2+34}" width="{KW-44}" height="{KH-56}" rx="6" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/>'
k += f'<rect x="{KX-50}" y="{KY-KH/2-16}" width="100" height="40" rx="10" fill="#9AA3B5" stroke="{INK}" stroke-width="6"/>'
k += T(KX, KY - KH / 2 + 76, "FIRMAS DE APOYO", 22, INK, font=DISP)
for i in range(7):
    yy = KY - KH / 2 + 118 + i * 44
    k += f'<path d="M {KX-KW/2+44} {yy+12} L {KX+KW/2-44} {yy+12}" stroke="#C9CFDA" stroke-width="3"/>'
    if i < 6:
        x0 = KX - KW / 2 + 54 + rnd.uniform(0, 30)
        pts_ = [(x0 + j * 26, yy + rnd.uniform(-10, 8)) for j in range(int(rnd.uniform(6, 9)))]
        k += f'<path d="{smooth(pts_)}" fill="none" stroke="#2F4BD6" stroke-width="4" stroke-linecap="round"/>'
k += "</g>"
o.append(G("firmas", k))
# bolígrafo
o.append(G("boli", f'<g transform="rotate(35 400 640)"><rect x="380" y="540" width="34" height="170" rx="10" fill="{VIO}" stroke="{INK}" stroke-width="6"/>'
           f'<path d="M 380 710 L 397 750 L 414 710 Z" fill="#F1D3A8" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
           f'<rect x="388" y="550" width="7" height="140" rx="3" fill="#FFFFFF" opacity="0.5"/></g>'))
# multitud: 1 de cada 1.000
gx0, gy0, st = 590, 330, 64
g = ""
for r in range(5):
    for cc in range(5):
        px, py = gx0 + cc * st, gy0 + r * (st + 8)
        if (r, cc) != (2, 2):
            g += person_icon(px, py, 46, sw=4)
o.append(G("gente", g))
o.append(G("uno", f'<circle cx="{gx0+2*st}" cy="{gy0+2*(st+8)}" r="44" fill="{LIME}" stroke="{INK}" stroke-width="5"/>' + person_icon(gx0 + 2 * st, gy0 + 2 * (st + 8), 50, col="url(#tealG)", sw=5)))
s, _ = label("t1000", 720, 700, "1 DE CADA 1.000", bg=INK, fg=LIME, size=32); o.append(s)
s, _ = label("t01", 720, 770, "= 0,1 % DEL CENSO", bg=CORAL, fg="#FFFFFF", size=28); o.append(s)
s, _ = label("tprov", 500, 870, "EN CADA PROVINCIA", bg=INK, fg=LIME, size=30); o.append(s)
o.append("</svg>")
save(OUT, "\n".join(o))

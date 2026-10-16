from vx import *

OUT = "carteles.svg"
defs = BASE_DEFS + VX_DEFS + lg("bgP", [(0, "#EEF1F7"), (1, "#D3DAE8")]) + lg("floorP", [(0, "#BFA27E"), (1, "#8E6F4C")])
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 700">\n<defs>{defs}</defs>']
o.append('<rect width="1000" height="700" fill="url(#bgP)"/>')
o.append('<g stroke="#C3CCDD" stroke-width="3">' + "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="610"/>' for x in range(50, 1000, 100)) + "</g>")
o.append(f'<rect x="0" y="610" width="1000" height="90" fill="url(#floorP)"/><path d="M 0 610 L 1000 610" stroke="{INK}" stroke-width="6"/>')

# rótulo
o.append(G("nombre", plate(560, 112, 400, 70, "VOX · PROGRAMA 2023", 26)))
s, _ = label("tsegun", 560, 178, "SEGÚN SU PROGRAMA", bg=INK, fg=LIME, size=22); o.append(s)

# iconos
def ic_imp(cx, cy):
    o = ""
    for k in range(4):
        o += f'<ellipse cx="{f(cx-38)}" cy="{f(cy+30-k*12)}" rx="30" ry="10" fill="url(#coinG)" stroke="{INK}" stroke-width="4"/>'
    o += T(cx - 38, cy - 10, "€", 22, "#8A5A00", font=DISP)
    o += dbl(f"M {f(cx+34)} {f(cy-40)} L {f(cx+34)} {f(cy+22)}", 14, CORAL, 8)
    o += dbl(f"M {f(cx+12)} {f(cy+2)} L {f(cx+34)} {f(cy+30)} L {f(cx+56)} {f(cy+2)}", 14, CORAL, 8)
    return o

def ic_viv(cx, cy):
    return house(cx - 22, cy + 42, 96) + clock(cx + 52, cy - 14, 30)

def ic_inm(cx, cy):
    # barrera de paso fronterizo y flecha de vuelta
    o = f'<rect x="{f(cx-62)}" y="{f(cy-30)}" width="14" height="74" rx="4" fill="url(#steelG)" stroke="{INK}" stroke-width="4"/>'
    o += f'<g transform="rotate(-4 {f(cx-55)} {f(cy-22)})"><rect x="{f(cx-60)}" y="{f(cy-30)}" width="128" height="18" rx="6" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/>'
    o += "".join(f'<rect x="{f(cx-40+k*30)}" y="{f(cy-30)}" width="14" height="18" fill="{CORAL}"/>' for k in range(4)) + "</g>"
    o += dbl(f"M {f(cx+50)} {f(cy+30)} Q {f(cx)} {f(cy+60)} {f(cx-30)} {f(cy+30)}", 10, "#5C78E8", 7)
    o += dbl(f"M {f(cx-12)} {f(cy+20)} L {f(cx-32)} {f(cy+30)} L {f(cx-18)} {f(cy+48)}", 10, "#5C78E8", 7)
    return o

CW, CH = 290, 250
specs = [("c1", 180, 360, "IMPUESTOS", "↓ IRPF · ✕ HERENCIAS", ic_imp, CORAL, -3),
         ("c2", 500, 370, "VIVIENDA", "DESALOJO EN 48 H", ic_viv, YEL, 2),
         ("c3", 820, 360, "INMIGRACIÓN", "EXPULSAR SI ENTRA ILEGAL", ic_inm, "#5C78E8", 3)]
for id_, cx, cy, t, sub, ic, acc, rot in specs:
    o.append(G(id_, card(cx, cy, CW, CH, t, sub, ic(cx, cy - 40), accent=acc, rot=rot, tsize=30 if len(t) < 10 else 26, ssize=17 if len(sub) > 18 else 20)))

# definiciones por escena (banda inferior, y 520-650)
s, _ = label("tirpf", 330, 548, "IRPF = IMPUESTO DE LO QUE GANAS", bg=INK, fg=LIME, size=24); o.append(s)
s, _ = label("tsuc", 330, 612, "SUCESIONES = HERENCIAS", bg=CORAL, fg="#FFFFFF", size=24); o.append(s)
s, _ = label("tokupa", 640, 548, "CASA OCUPADA SIN PERMISO", bg=INK, fg=LIME, size=24); o.append(s)
s, _ = label("t48", 640, 612, "48 HORAS = 2 DÍAS", bg=CORAL, fg="#FFFFFF", size=24); o.append(s)
s, _ = label("tileg", 660, 560, "ILEGAL = SIN PERMISO PARA ENTRAR", bg=INK, fg=LIME, size=24); o.append(s)
o.append("</svg>")
save(OUT, "\n".join(o))

from hc import *

OUT = "corte_free.svg"
W, H = 1000, 900
o = [header(W, H)]
CX, CY, S = 430, 480, 440
h = S / 2
d = S * 0.34
X0, Y0, X1, Y1 = CX - h, CY - h, CX + h, CY + h
TH = 62  # grosor de la capa exterior

P = lambda pts: "M " + " L ".join(f"{f(x)} {f(y)}" for x, y in pts) + " Z"
cube_g = []
cube_g.append(f'<ellipse cx="{CX+90}" cy="{Y1+40}" rx="{S*0.62}" ry="26" fill="{INK}" opacity="0.25"/>')
Tp = [(X0, Y0), (X0 + d, Y0 - d * 0.8), (X1 + d, Y0 - d * 0.8), (X1, Y0)]
Sd = [(X1, Y0), (X1 + d, Y0 - d * 0.8), (X1 + d, Y1 - d * 0.8), (X1, Y1)]
cube_g.append(f'<path d="{P(Sd)}" fill="url(#iceS)" stroke="{ICE_EDGE}" stroke-width="9" stroke-linejoin="round"/>')
cube_g.append(f'<path d="{P(Tp)}" fill="url(#iceT)" stroke="{ICE_EDGE}" stroke-width="9" stroke-linejoin="round"/>')
cube_g.append(f'<rect x="{X0}" y="{Y0}" width="{S}" height="{S}" fill="url(#iceF)" stroke="{ICE_EDGE}" stroke-width="9"/>')
cube_g.append(f'<ellipse cx="{CX}" cy="{CY}" rx="{S*0.26}" ry="{S*0.22}" fill="url(#cloudR)"/>')
rnd = random.Random(11)
for _ in range(7):
    cube_g.append(f'<circle cx="{f(rnd.uniform(X0+90, X1-90))}" cy="{f(rnd.uniform(Y0+90, Y1-90))}" r="{f(rnd.uniform(6, 11))}" fill="#FFFFFF" stroke="#9CCFEA" stroke-width="3"/>')
cube_g.append(f'<path d="M {X0+30} {Y0+34} L {X0+30} {Y1-120}" stroke="#FFFFFF" stroke-width="16" stroke-linecap="round"/>')
cube_g.append(f'<path d="M {X1+14} {Y0-6} L {X1+d-16} {Y0-d*0.8+14}" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round" opacity="0.8"/>')
# refresco mojando la cara de arriba
cube_g.append(f'<path d="M {X0+40} {Y0-12} Q {X0+120} {Y0-40} {X0+200} {Y0-30} Q {X0+260} {Y0-24} {X0+250} {Y0-60} Q {X0+330} {Y0-90} {X1+40} {Y0-70}" fill="none" stroke="#F5A52A" stroke-width="16" stroke-linecap="round" opacity="0.85"/>')
o.append(g("cubo", "".join(cube_g)))

# capa exterior templada (anillo) y núcleo frío
ring = (f"M {X0+5} {Y0+5} L {X1-5} {Y0+5} L {X1-5} {Y1-5} L {X0+5} {Y1-5} Z "
        f"M {X0+TH} {Y0+TH} L {X0+TH} {Y1-TH} L {X1-TH} {Y1-TH} L {X1-TH} {Y0+TH} Z")
o.append(g("capa", f'<path d="{ring}" fill="url(#warmG)" fill-rule="evenodd" opacity="0.92"/>'
           f'<path d="M {X0+18} {Y0+18} L {X1-18} {Y0+18}" stroke="#FFE3D2" stroke-width="7" stroke-linecap="round"/>'))
o.append(g("nucleo", f'<rect x="{X0+TH}" y="{Y0+TH}" width="{S-2*TH}" height="{S-2*TH}" rx="6" fill="url(#coldG)" stroke="#2B6E9E" stroke-width="6" stroke-dasharray="14 10"/>'
           + "".join(f'<path d="M {f(x-12)} {f(y)} L {f(x+12)} {f(y)} M {f(x)} {f(y-12)} L {f(x)} {f(y+12)} M {f(x-8)} {f(y-8)} L {f(x+8)} {f(y+8)} M {f(x+8)} {f(y-8)} L {f(x-8)} {f(y+8)}" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>'
                     for x, y in ((CX - 80, CY - 70), (CX + 70, CY - 30), (CX - 20, CY + 80), (CX + 90, CY + 90), (CX - 100, CY + 40)))))
o.append(f'<rect x="{X0}" y="{Y0}" width="{S}" height="{S}" fill="none" stroke="{ICE_EDGE}" stroke-width="9"/>')

# gotas de bebida cayendo encima
drops = ""
for x, y, r in ((CX - 120, Y0 - 150, 16), (CX + 10, Y0 - 190, 13), (CX + 150, Y0 - 160, 15), (CX + 260, Y0 - 210, 12)):
    drops += f'<path d="M {x} {y-r*1.9} Q {x+r} {y-r*0.4} {x+r} {y} A {r} {r} 0 0 1 {x-r} {y} Q {x-r} {y-r*0.4} {x} {y-r*1.9} Z" fill="#F5A52A" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    drops += f'<circle cx="{f(x-r*0.35)}" cy="{f(y-r*0.2)}" r="{f(r*0.28)}" fill="#FFFFFF" opacity="0.8"/>'
o.append(g("gotas", drops))

# flechas de calor (entran poco)
heat = ""
for (x1, y1, x2, y2) in ((X0 - 95, CY - 90, X0 + 40, CY - 90), (X0 - 95, CY + 80, X0 + 40, CY + 80), (X1 + d + 110, CY - 40, X1 + d - 30, CY - 40), (X1 + d + 110, CY + 110, X1 + d - 30, CY + 110)):
    heat += arrow(None, ((x1, y1), (x2, y2)), col=CORAL, w=12, head=26)
o.append(g("calor", heat))

# caracol «despacio»
o.append(snail(830, 800, 120, id_="caracol"))

# escena 4: la capa quiere crecer
outs = ""
for (x1, y1, x2, y2) in ((X0 + 20, CY, X0 - 120, CY), (X1 + d / 2, CY - 60, X1 + d / 2 + 120, CY - 60), (CX - 100, Y0 - 20, CX - 100, Y0 - 150)):
    outs += arrow(None, ((x1, y1), (x2, y2)), col=CORAL, w=14, head=30)
o.append(g("crecer", outs))
# tensión entre capa y núcleo
ten = ""
for side in range(4):
    pts = []
    n = 14
    for i in range(n + 1):
        t = i / n
        k = 9 if i % 2 else -9
        if side == 0:
            pts.append((X0 + TH + t * (S - 2 * TH), Y0 + TH + k))
        elif side == 1:
            pts.append((X1 - TH + k, Y0 + TH + t * (S - 2 * TH)))
        elif side == 2:
            pts.append((X0 + TH + t * (S - 2 * TH), Y1 - TH + k))
        else:
            pts.append((X0 + TH + k, Y0 + TH + t * (S - 2 * TH)))
    dd = "M " + " L ".join(f"{f(x)} {f(y)}" for x, y in pts)
    ten += f'<path d="{dd}" fill="none" stroke="{INK}" stroke-width="12" stroke-linejoin="round"/><path d="{dd}" fill="none" stroke="{YEL}" stroke-width="6" stroke-linejoin="round"/>'
o.append(g("tension", ten))

# escena 5: grietas
cr = [zig(X0 + 120, Y0, CX + 10, CY + 40, n=6, amp=16, seed=21),
      zig(X1, Y0 + 130, CX + 30, CY + 10, n=6, amp=14, seed=22),
      zig(X0 + 60, Y1, CX - 20, CY + 30, n=6, amp=15, seed=23),
      zig(X1 + d, Y0 - d * 0.8 + 60, X1 + 30, CY + 60, n=5, amp=12, seed=24)]
for i, pts in enumerate(cr):
    o.append(crack(pts, 9, col=INK, id_=f"g{i+1}"))
o.append(burst(850, 200, 120, "¡CRAC!", 34, rot=10, id_="crac1"))
o.append(burst(120, 250, 105, "¡CRIC!", 30, rot=-12, id_="crac2", col="#FFFFFF"))

# etiquetas
for id_, x, y, t, bg, fg in (("lfuera", 300, 790, "FUERA: SE CALIENTA", CORAL, "#FFFFFF"),
                             ("ldentro", 300, 856, "DENTRO: SIGUE HELADO", "#3E95E0", "#FFFFFF"),
                             ("lcrecer", 300, 790, "FUERA QUIERE CRECER", CORAL, "#FFFFFF"),
                             ("lnodeja", 300, 856, "EL CENTRO NO LA DEJA", "#3E95E0", "#FFFFFF"),
                             ("lchoque", 300, 790, "CHOQUE TÉRMICO", INK, LIME),
                             ("lfragil", 340, 856, "FRÁGIL COMO EL CRISTAL", INK, LIME)):
    s, _ = label(id_, x, y, t, bg=bg, fg=fg, size=32); o.append(s)
o.append("</svg>")
save(OUT, "\n".join(o))

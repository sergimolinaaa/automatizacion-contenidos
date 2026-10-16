import math, random
from lib import *
W, H = 1080, 1920
FY = 1190  # suelo
ANG = -4.0
SC = 1.12
PX, PY = 540, 1188  # pivote de la inclinación (pie de la estantería)


def rot(x, y, a=ANG, cx=PX, cy=PY):
    r = math.radians(a)
    x, y = (x - cx) * SC, (y - cy) * SC
    return (cx + x * math.cos(r) - y * math.sin(r), cy + x * math.sin(r) + y * math.cos(r))


defs = WOOD_DEFS + lg("wallg", [(0, "#EFE3CF"), (1, "#DCCBB0")]) + lg("floorg", [(0, "#B9875A"), (1, "#7A5232")]) + \
    lg("birch", [(0, "#F6E2C0"), (1, "#DDB988")]) + lg("birchd", [(0, "#D9B585"), (1, "#B98E5C")]) + \
    lg("back", [(0, "#CFA877"), (1, "#B48A5A")]) + lg("cardb", [(0, "#D8A86A"), (1, "#B9864A")]) + \
    lg("level", [(0, "#FFE36A"), (1, "#F2B807")]) + lg("vial", [(0, "#E9FFB0"), (1, "#B6E35A")]) + \
    lg("shade", [(0, "#FFF4DC"), (1, "#F4D9A6")], 0, 0, 1, 0) + \
    rg("glow", [(0, "#FFE9B0", 0.9), (0.5, "#FFE2A0", 0.35), (1, "#FFE2A0", 0)]) + \
    lg("mug", [(0, "#4F7BFF"), (1, "#2347D8")], 0, 0, 1, 0) + lg("pot", [(0, "#F08A5D"), (1, "#C65A33")], 0, 0, 1, 0) + \
    rg("rug", [(0, "#5E7FA8"), (1, "#3F5D84")])
o = [header(defs, W, H)]
# ---------- pared ----------
o.append('<g transform="translate(0 70)">')
o.append(f'<rect y="-80" width="{W}" height="{FY + 80}" fill="url(#wallg)"/>')
o.append('<g fill="#FFFFFF" opacity="0.16">' + "".join(f'<rect x="{x}" y="-80" width="22" height="{FY + 80}"/>' for x in range(20, W, 70)) + '</g>')
# cuadro en la pared (decorado)
o.append(f'<rect x="96" y="470" width="190" height="150" rx="6" fill="#FFFFFF" stroke="{INK}" stroke-width="6"/><rect x="114" y="488" width="154" height="114" fill="#BFE0F2"/>'
         '<path d="M 114 602 L 160 540 L 196 580 L 226 548 L 268 602 Z" fill="#7CC27A"/><circle cx="236" cy="516" r="14" fill="#FFD23F"/>')
o.append(f'<path d="M 190 470 L 190 440" stroke="{INK}" stroke-width="4"/><circle cx="190" cy="438" r="5" fill="{INK}"/>')
# lámpara de pie (derecha)
o.append('<g id="luz"><circle cx="950" cy="700" r="300" fill="url(#glow)"/></g>')
o.append(f'<ellipse cx="950" cy="{FY - 6}" rx="74" ry="16" fill="#000" opacity="0.25"/>')
o.append(dbl(f"M 950 {FY - 12} L 950 690", 9, "#3A3A44"))
o.append(f'<ellipse cx="950" cy="{FY - 14}" rx="58" ry="14" fill="#3A3A44" stroke="{INK}" stroke-width="6"/>')
o.append(f'<path d="M 880 700 L 1020 700 L 990 590 L 910 590 Z" fill="url(#shade)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
o.append('<path d="M 918 600 L 896 690" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round" opacity="0.8"/>')
o.append('<ellipse cx="950" cy="704" rx="66" ry="9" fill="#FFF3C4" opacity="0.9"/>')
# rodapié
o.append(f'<rect x="-10" y="{FY - 30}" width="{W + 20}" height="30" fill="#F7F0E4" stroke="{INK}" stroke-width="5"/>')
# ---------- suelo de parqué ----------
o.append(f'<rect y="{FY}" width="{W}" height="{H - FY}" fill="url(#floorg)"/>')
random.seed(3)
for k, y in enumerate(range(FY, H, 64)):
    o.append(f'<path d="M 0 {y} L {W} {y}" stroke="#6A4528" stroke-width="3" opacity="0.55"/>')
    off = (k * 137) % 260
    for x in range(-off, W, 260):
        o.append(f'<path d="M {x} {y} L {x} {y + 64}" stroke="#6A4528" stroke-width="3" opacity="0.5"/>')
    o.append(f'<path d="M 0 {y + 22} C 300 {y + 18}, 700 {y + 30}, {W} {y + 20}" stroke="#D6A46E" stroke-width="3" opacity="0.25" fill="none"/>')
# alfombra
o.append(f'<ellipse cx="540" cy="{FY + 34}" rx="400" ry="52" fill="url(#rug)" stroke="{INK}" stroke-width="6"/>')
o.append(f'<ellipse cx="540" cy="{FY + 34}" rx="352" ry="38" fill="none" stroke="#9FB8D8" stroke-width="5" stroke-dasharray="18 12"/>')
# ---------- caja de cartón plana apoyada en la pared (izquierda) ----------
o.append('<g id="carton">')
o.append(f'<ellipse cx="170" cy="{FY + 4}" rx="130" ry="14" fill="#000" opacity="0.25"/>')
o.append(f'<path d="M 50 {FY + 4} L 104 860 L 312 872 L 292 {FY + 6} Z" fill="url(#cardb)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
o.append(f'<path d="M 104 860 L 118 852 L 324 864 L 312 872 Z" fill="#E9C08A" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
o.append(f'<path d="M 312 872 L 324 864 L 304 {FY - 2} L 292 {FY + 6} Z" fill="#9C6E3A" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
o.append('<path d="M 170 866 L 150 1192" stroke="#E8D9B8" stroke-width="22" opacity="0.8"/>')
o.append(f'<rect x="140" y="940" width="90" height="28" rx="14" fill="#5A3C20" stroke="{INK}" stroke-width="5" transform="rotate(3 185 954)"/>')
o.append('<g opacity="0.75"><path d="M 112 1040 l 60 4 l -2 40 l -60 -4 Z" fill="none" stroke="#5A3C20" stroke-width="4"/><path d="M 124 1052 l 34 2 M 122 1066 l 30 2" stroke="#5A3C20" stroke-width="4"/></g>')
o.append('</g>')
# ---------- estantería torcida ----------
S = ['<g id="estanteria">', f'<ellipse cx="540" cy="{FY}" rx="260" ry="20" fill="#000" opacity="0.3"/>', f'<g transform="translate({PX} {PY}) rotate({ANG}) scale({SC}) translate({-PX} {-PY})">']
X0, X1, YT, YB = 340, 740, 600, 1186
T = 24
# fondo
S.append(f'<rect x="{X0 + T}" y="{YT + 26}" width="{X1 - X0 - 2 * T}" height="{YB - YT - 60}" fill="url(#back)"/>')
S.append('<g stroke="#A47C4E" stroke-width="3" opacity="0.5">' + "".join(f'<path d="M {x} {YT + 30} L {x} {YB - 40}"/>' for x in range(420, 700, 70)) + '</g>')
# baldas: 1 recta, 2 torcida
B1 = 800
S.append(f'<rect x="{X0 + T - 2}" y="{B1}" width="{X1 - X0 - 2 * T + 4}" height="20" fill="url(#birch)" stroke="{INK}" stroke-width="6"/>')
S.append(f'<path d="M {X0 + T} {B1 + 4} L {X1 - T} {B1 + 4}" stroke="#FFF6E4" stroke-width="3"/>')
b2l, b2r = 990, 1022
S.append(f'<path d="M {X0 + T - 2} {b2l} L {X1 - T + 2} {b2r} L {X1 - T + 2} {b2r + 20} L {X0 + T - 2} {b2l + 20} Z" fill="url(#birch)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
S.append(f'<path d="M {X0 + T} {b2l + 4} L {X1 - T} {b2r + 4}" stroke="#FFF6E4" stroke-width="3"/>')
# libros en la balda 1
x = X0 + T + 6
cols = ["#E5484D", "#2E8BFF", "#F2B807", "#36B37E", "#7C5CFF", "#FF8A3D", "#1F2937"]
random.seed(5)
for k in range(8):
    w = random.choice((26, 30, 34, 38))
    h = random.choice((128, 140, 150, 158))
    c = cols[k % len(cols)]
    if k == 7:  # libro inclinado
        S.append(f'<g transform="rotate(18 {x} {B1})"><rect x="{x}" y="{B1 - h}" width="{w}" height="{h}" rx="3" fill="{c}" stroke="{INK}" stroke-width="5"/><rect x="{x + 5}" y="{B1 - h + 20}" width="{w - 10}" height="8" fill="#FFFFFF" opacity="0.7"/></g>')
        x += w + 40
        break
    S.append(f'<rect x="{x}" y="{B1 - h}" width="{w}" height="{h}" rx="3" fill="{c}" stroke="{INK}" stroke-width="5"/>')
    S.append(f'<rect x="{x + 5}" y="{B1 - h + 18}" width="{w - 10}" height="8" fill="#FFFFFF" opacity="0.7"/><rect x="{x + 5}" y="{B1 - 30}" width="{w - 10}" height="5" fill="#FFFFFF" opacity="0.5"/>')
    S.append(f'<path d="M {x + 4} {B1 - h + 6} L {x + 4} {B1 - 6}" stroke="#FFFFFF" stroke-width="3" opacity="0.35"/>')
    x += w
# maceta pequeña con planta (balda 1, derecha)
S.append(f'<path d="M 640 {B1} L 632 {B1 - 56} L 700 {B1 - 56} L 692 {B1} Z" fill="url(#pot)" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
S.append(f'<rect x="626" y="{B1 - 66}" width="80" height="14" rx="4" fill="#E2774B" stroke="{INK}" stroke-width="5"/>')
for a, l in ((-60, 70), (-90, 92), (-120, 74), (-30, 56), (-150, 52)):
    r = math.radians(a)
    ex, ey = 666 + l * math.cos(r), B1 - 66 + l * math.sin(r)
    S.append(f'<path d="M 666 {B1 - 66} Q {666 + l * 0.6 * math.cos(r) - 14:.0f} {B1 - 66 + l * 0.5 * math.sin(r):.0f} {ex:.0f} {ey:.0f} Q {666 + l * 0.6 * math.cos(r) + 14:.0f} {B1 - 66 + l * 0.6 * math.sin(r):.0f} 666 {B1 - 66} Z" fill="#36B37E" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')
# balda 2 (torcida): taza y pelota resbaladas hacia la derecha
slope = math.degrees(math.atan2(b2r - b2l, X1 - X0 - 2 * T))
def on_b2(xx):
    return b2l + (b2r - b2l) * (xx - X0 - T) / (X1 - X0 - 2 * T)
# portafotos inclinado (izquierda)
yb = on_b2(400)
S.append(f'<g transform="rotate({slope - 8:.1f} 400 {yb:.0f})"><rect x="380" y="{yb - 110:.0f}" width="96" height="110" rx="5" fill="#F7F0E4" stroke="{INK}" stroke-width="5"/><rect x="392" y="{yb - 98:.0f}" width="72" height="80" fill="#FFC9A8"/><circle cx="428" cy="{yb - 70:.0f}" r="14" fill="#C47B55"/><path d="M 404 {yb - 18:.0f} Q 428 {yb - 54:.0f} 452 {yb - 18:.0f} Z" fill="#2E8BFF"/></g>')
xm = 640
ym = on_b2(xm + 30)
S.append(f'<g transform="rotate({slope:.1f} {xm + 30} {ym:.0f})"><path d="M {xm + 58} {ym - 64:.0f} q 26 4 22 26 q -4 18 -22 16" fill="none" stroke="{INK}" stroke-width="13"/><path d="M {xm + 58} {ym - 64:.0f} q 26 4 22 26 q -4 18 -22 16" fill="none" stroke="#2E5BEA" stroke-width="6"/>'
         f'<rect x="{xm}" y="{ym - 78:.0f}" width="62" height="78" rx="8" fill="url(#mug)" stroke="{INK}" stroke-width="5"/><path d="M {xm + 10} {ym - 66:.0f} L {xm + 10} {ym - 14:.0f}" stroke="#9FB6FF" stroke-width="5" stroke-linecap="round"/></g>')
yb2 = on_b2(696)
S.append(f'<circle cx="696" cy="{yb2 - 20:.0f}" r="20" fill="#FF8A3D" stroke="{INK}" stroke-width="5"/><path d="M 684 {yb2 - 30:.0f} q 8 -6 16 -4" stroke="#FFD0A8" stroke-width="4" stroke-linecap="round" fill="none"/>')
# compartimento bajo: caja de almacenaje y revistas
S.append(storage_box(382, 1150, w=200, h=104, dx=28, dy=-22, screws=False, grain_seed=4))
for k, c in enumerate(("#F2B807", "#E5484D", "#2E8BFF", "#36B37E")):
    S.append(f'<rect x="620" y="{1150 - 16 * (k + 1)}" width="92" height="16" rx="3" fill="{c}" stroke="{INK}" stroke-width="4"/>')
# laterales, tapa y zócalo
S.append(f'<rect x="{X0}" y="{YT}" width="{T}" height="{YB - YT}" fill="url(#birchd)" stroke="{INK}" stroke-width="7"/>')
S.append(f'<rect x="{X1 - T}" y="{YT}" width="{T}" height="{YB - YT}" fill="url(#birchd)" stroke="{INK}" stroke-width="7"/>')
S.append(f'<path d="M {X0 + 6} {YT + 30} L {X0 + 6} {YB - 10} M {X1 - T + 6} {YT + 30} L {X1 - T + 6} {YB - 10}" stroke="#FFF1D6" stroke-width="3" opacity="0.8"/>')
S.append(f'<rect x="{X0 - 8}" y="{YT - 4}" width="{X1 - X0 + 16}" height="30" fill="url(#birch)" stroke="{INK}" stroke-width="7"/>')
S.append(f'<path d="M {X0} {YT + 3} L {X1} {YT + 3}" stroke="#FFF6E4" stroke-width="4"/>')
S.append(f'<rect x="{X0 + T - 2}" y="{YB - 36}" width="{X1 - X0 - 2 * T + 4}" height="36" fill="url(#birchd)" stroke="{INK}" stroke-width="6"/>')
# tornillos vistos y un tornillo sin apretar
for sx, sy in ((X0 + 12, YT + 12), (X1 - 12, YT + 12), (X0 + 12, B1 + 10), (X1 - 12, B1 + 10), (X0 + 12, YB - 18), (X1 - 12, YB - 18)):
    S.append(f'<circle cx="{sx}" cy="{sy}" r="5.5" fill="#9AA3AD" stroke="{INK}" stroke-width="3"/>')
# nivel de burbuja encima (dentro del giro, para que vaya inclinado)
S.append('<g id="nivel">')
S.append(f'<rect x="420" y="{YT - 40}" width="240" height="36" rx="6" fill="url(#level)" stroke="{INK}" stroke-width="6"/>')
S.append(f'<rect x="500" y="{YT - 33}" width="80" height="22" rx="11" fill="url(#vial)" stroke="{INK}" stroke-width="4"/>')
S.append(f'<path d="M 532 {YT - 33} L 532 {YT - 11} M 548 {YT - 33} L 548 {YT - 11}" stroke="{INK}" stroke-width="2.5"/>')
S.append(f'<g id="burbuja"><ellipse cx="540" cy="{YT - 22}" rx="10" ry="6" fill="#FFFFFF" stroke="#7FA83A" stroke-width="2"/></g>')
S.append(f'<path d="M 430 {YT - 33} L 490 {YT - 33}" stroke="#FFF6B0" stroke-width="4" stroke-linecap="round"/>')
S.append('</g>')
S.append('</g></g>')
o.append("".join(S))
# plomada: referencia vertical desde la esquina inferior derecha
bx, by = rot(X1, YB)
tx, ty = rot(X1, YT)
o.append(f'<g id="plomada"><path d="M {bx:.0f} {by:.0f} L {bx:.0f} {ty - 30:.0f}" stroke="{INK}" stroke-width="9" stroke-dasharray="20 14" stroke-linecap="round"/>'
         f'<path d="M {bx:.0f} {by:.0f} L {bx:.0f} {ty - 30:.0f}" stroke="{LIME}" stroke-width="4" stroke-dasharray="20 14" stroke-linecap="round"/>'
         f'<path d="M {bx - 4:.0f} {ty + 30:.0f} L {tx + 6:.0f} {ty + 30:.0f}" stroke="{INK}" stroke-width="11" stroke-linecap="round"/><path d="M {bx - 4:.0f} {ty + 30:.0f} L {tx + 6:.0f} {ty + 30:.0f}" stroke="{CORAL}" stroke-width="5" stroke-linecap="round"/>'
         f'<rect x="{bx + 16:.0f}" y="{ty + 52:.0f}" width="70" height="44" rx="10" fill="{INK}"/>' + txt(bx + 51, ty + 84, "4°", 28, LIME) + '</g>')
# ---------- en el suelo: llave Allen, instrucciones y el tornillo que sobra ----------
o.append(f'<g id="instr"><g transform="translate(-80 -58) rotate(-8 230 1300) scale(0.8) translate(46 260)"><path d="M 140 1262 L 330 1262 L 330 1352 L 140 1352 Z" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/>'
         '<circle cx="176" cy="1290" r="10" fill="none" stroke="#8A97A6" stroke-width="3"/><path d="M 176 1300 L 176 1326 M 162 1310 L 190 1310 M 210 1286 L 300 1286 M 210 1304 L 280 1304 M 210 1322 L 296 1322" stroke="#8A97A6" stroke-width="4"/></g></g>')
o.append('<g id="llave">' + allen_key(450, 1228, 1.1, -14) + '</g>')
o.append('<g id="tornillo">' + screw(690, 1218, 1.3, -24) + '</g>')
ls, _ = tag("lsobra", 862, 1218, "¡SOBRA UNO!", size=28)
o.append(ls.replace('<g id="lsobra">', '<g id="lsobra"><line x1="745" y1="1218" x2="722" y2="1212" stroke="#0B0B14" stroke-width="5" stroke-linecap="round"/>'))
# ---------- corazones y medalla ----------
o.append('<g id="corazones">' + heart(98, 800, 0.85) + heart(840, 900, 1.05) + heart(880, 515, 0.75) + '</g>')
med = ['<g id="medalla">']
mx, my = 205, 712
med.append(f'<path d="M {mx - 26} {my + 20} L {mx - 46} {my + 104} L {mx - 22} {my + 90} L {mx - 6} {my + 112} L {mx + 4} {my + 24} Z" fill="#2347FF" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
med.append(f'<path d="M {mx + 26} {my + 20} L {mx + 46} {my + 104} L {mx + 22} {my + 90} L {mx + 6} {my + 112} L {mx - 4} {my + 24} Z" fill="#2347FF" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
med.append(f'<path d="{star(mx, my, 62, 52, 22)}" fill="#C8FF2E" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
med.append(f'<circle cx="{mx}" cy="{my}" r="42" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/>')
med.append(txt(mx, my - 4, "HECHO", 17) + txt(mx, my + 18, "POR MÍ", 17))
med.append('</g>')
o.append("".join(med))
o.append('</g>')
o.append('</svg>')
open("montaje_full.svg", "w").write("\n".join(o))

import math, random, sys
sys.path.insert(0, sys.path[0])
from common import *

random.seed(4)
Y0 = 235          # superficie de la piel
YB = 288          # unión epidermis-dermis
YH = 560          # comienzo de la hipodermis (grasa)
LEAN = 33         # inclinación del pelo en reposo (grados, horario)
ROT = -24         # giro al contraerse el músculo

defs = f'''
<linearGradient id="air" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#D7ECFF"/><stop offset="1" stop-color="#F1F8FF"/></linearGradient>
<linearGradient id="epi" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F2C2A2"/><stop offset="1" stop-color="#D99470"/></linearGradient>
<linearGradient id="derm" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F9D3C8"/><stop offset="1" stop-color="#F1B7AA"/></linearGradient>
<linearGradient id="hypo" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FBE7A6"/><stop offset="1" stop-color="#F0CD72"/></linearGradient>
<radialGradient id="fat" cx="0.38" cy="0.32" r="0.8"><stop offset="0" stop-color="#FFF6C9"/><stop offset="1" stop-color="#F4CF62"/></radialGradient>
<linearGradient id="sheath" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#E9C2A8"/><stop offset="0.45" stop-color="#FBE3D2"/><stop offset="1" stop-color="#D9A88A"/></linearGradient>
<linearGradient id="shaft" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2A1C14"/><stop offset="0.4" stop-color="#6B4A35"/><stop offset="1" stop-color="#22160F"/></linearGradient>
<radialGradient id="bulb" cx="0.5" cy="0.4" r="0.7"><stop offset="0" stop-color="#C68A66"/><stop offset="1" stop-color="#8A5638"/></radialGradient>
<radialGradient id="papilla" cx="0.4" cy="0.35" r="0.7"><stop offset="0" stop-color="#FF9B8F"/><stop offset="1" stop-color="#D9504A"/></radialGradient>
<radialGradient id="seb" cx="0.35" cy="0.3" r="0.8"><stop offset="0" stop-color="#FFF4B8"/><stop offset="1" stop-color="#E8C35A"/></radialGradient>
<linearGradient id="muscle" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FF8A70"/><stop offset="1" stop-color="#C9382A"/></linearGradient>
<radialGradient id="stem" cx="0.35" cy="0.3" r="0.8"><stop offset="0" stop-color="#EFFFB0"/><stop offset="1" stop-color="#7FCB2E"/></radialGradient>
'''
o = [head(defs)]
o.append(f'<rect width="1000" height="700" fill="url(#air)"/>')
# copos lejanos en el aire frío
o.append('<g id="snow" fill="#FFFFFF" stroke="#9CC6EA" stroke-width="2">')
for x, y, r in [(380, 120, 7), (640, 70, 6), (700, 170, 8), (935, 95, 7), (240, 175, 6), (585, 150, 5)]:
    o.append(f'<circle cx="{x}" cy="{y}" r="{r}"/>')
o.append('</g>')
# hipodermis
o.append(f'<rect y="{YH}" width="1000" height="{700-YH}" fill="url(#hypo)"/>')
o.append('<g stroke="#C79A3A" stroke-width="3">')
xs = 10
row = 0
for yy in (590, 640, 690):
    x = -20 + (row % 2) * 40
    while x < 1040:
        r = 34 + random.randint(-5, 6)
        o.append(f'<ellipse cx="{x}" cy="{yy+random.randint(-4,4)}" rx="{r}" ry="{r*0.8:.0f}" fill="url(#fat)"/>')
        x += 78 + random.randint(-6, 6)
    row += 1
o.append('</g>')
# dermis (borde inferior ondulado sobre la grasa)
o.append(f'<path d="M 0 {YB-20} L 1000 {YB-20} L 1000 {YH} C 900 {YH+14}, 820 {YH-10}, 700 {YH+6} C 580 {YH+18}, 480 {YH-8}, 360 {YH+6} C 240 {YH+18}, 120 {YH-6}, 0 {YH+8} Z" fill="url(#derm)" stroke="#D88C7E" stroke-width="4"/>')
# fibras de colágeno
o.append('<g fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.45" stroke-linecap="round">')
for i in range(14):
    x = random.randint(20, 940); y = random.randint(330, 530)
    o.append(f'<path d="M {x} {y} c 15 -8, 30 8, 45 0 s 30 8, 45 0"/>')
o.append('</g>')
# vasos sanguíneos
o.append(stroke2(f"M -10 470 C 60 455, 90 420, 120 380 C 140 352, 175 352, 185 380 C 196 412, 230 430, 300 440", 10, "#E5484D", 6))
o.append(stroke2(f"M -10 498 C 70 488, 110 452, 140 410 C 152 392, 166 394, 170 412 C 178 448, 230 462, 300 470", 9, "#5B7FD6", 6))
# epidermis con crestas
ridge = " ".join(f"Q {x+25} {YB+18 if (x//50)%2==0 else YB-6} {x+50} {YB}" for x in range(0, 1000, 50))
o.append(f'<path d="M 0 {Y0} L 1000 {Y0} L 1000 {YB} L 0 {YB} Z" fill="url(#epi)"/>')
o.append(f'<path d="M 0 {YB} {ridge} L 1000 {YB-20} L 0 {YB-20} Z" fill="url(#epi)"/>')
o.append(f'<path d="M 0 {YB} {ridge}" fill="none" stroke="#B5694A" stroke-width="5" stroke-dasharray="2 9" stroke-linecap="round"/>')
o.append(f'<line x1="0" y1="{Y0+9}" x2="1000" y2="{Y0+9}" stroke="#FBE0CF" stroke-width="5" opacity="0.8"/>')
o.append(f'<line x1="0" y1="{Y0}" x2="1000" y2="{Y0}" stroke="{INK}" stroke-width="7"/>')


def hair_local(sc, sid):
    """pelo en marco local: superficie en (0,0), el folículo baja por +y; +x = lado del músculo"""
    L, Ls = 330 * sc, 165 * sc
    w = 27 * sc
    g = []
    # glándula sebácea (lado +x)
    g.append(f'<g stroke="{INK}" stroke-width="{5*sc:.1f}" fill="url(#seb)">'
             f'<ellipse cx="{w+22*sc:.1f}" cy="{70*sc:.1f}" rx="{26*sc:.1f}" ry="{20*sc:.1f}"/>'
             f'<ellipse cx="{w+30*sc:.1f}" cy="{102*sc:.1f}" rx="{24*sc:.1f}" ry="{19*sc:.1f}"/>'
             f'<ellipse cx="{w+14*sc:.1f}" cy="{92*sc:.1f}" rx="{18*sc:.1f}" ry="{16*sc:.1f}"/></g>')
    # vaina del folículo
    bw = 42 * sc
    d = (f"M {-w:.1f} {-4*sc:.1f} L {-w:.1f} {L-70*sc:.1f} C {-w:.1f} {L-40*sc:.1f}, {-bw:.1f} {L-40*sc:.1f}, {-bw:.1f} {L-8*sc:.1f} "
         f"C {-bw:.1f} {L+30*sc:.1f}, {bw:.1f} {L+30*sc:.1f}, {bw:.1f} {L-8*sc:.1f} C {bw:.1f} {L-40*sc:.1f}, {w:.1f} {L-40*sc:.1f}, {w:.1f} {L-70*sc:.1f} L {w:.1f} {-4*sc:.1f} Z")
    g.append(f'<path d="{d}" fill="url(#sheath)" stroke="{INK}" stroke-width="{6*sc:.1f}" stroke-linejoin="round"/>')
    g.append(f'<line x1="{-w+7*sc:.1f}" y1="{10*sc:.1f}" x2="{-w+7*sc:.1f}" y2="{L-80*sc:.1f}" stroke="#FFFFFF" stroke-width="{4*sc:.1f}" opacity="0.6" stroke-linecap="round"/>')
    # bulbo y papila
    g.append(f'<ellipse cx="0" cy="{L-10*sc:.1f}" rx="{33*sc:.1f}" ry="{26*sc:.1f}" fill="url(#bulb)" stroke="{INK}" stroke-width="{4*sc:.1f}"/>')
    g.append(f'<path d="M {-15*sc:.1f} {L+14*sc:.1f} C {-16*sc:.1f} {L-6*sc:.1f}, {-8*sc:.1f} {L-16*sc:.1f}, 0 {L-16*sc:.1f} C {8*sc:.1f} {L-16*sc:.1f}, {16*sc:.1f} {L-6*sc:.1f}, {15*sc:.1f} {L+14*sc:.1f} Z" fill="url(#papilla)" stroke="{INK}" stroke-width="{4*sc:.1f}"/>')
    # raíz y tallo del pelo
    g.append(f'<path d="M {-6*sc:.1f} {L-28*sc:.1f} L {-5*sc:.1f} 0 L {-3*sc:.1f} {-Ls:.1f} L {3*sc:.1f} {-Ls:.1f} L {5*sc:.1f} 0 L {6*sc:.1f} {L-28*sc:.1f} Z" fill="url(#shaft)" stroke="{INK}" stroke-width="{4*sc:.1f}" stroke-linejoin="round"/>')
    g.append(f'<line x1="{-1.5*sc:.1f}" y1="{-10*sc:.1f}" x2="{-1*sc:.1f}" y2="{-Ls+12*sc:.1f}" stroke="#B88A66" stroke-width="{2*sc:.1f}" stroke-linecap="round"/>')
    # células madre del abultamiento (bulge)
    cells = []
    for side in (-1, 1):
        for k, yy in enumerate((128, 150, 172)):
            cells.append(f'<circle cx="{side*(w-3*sc):.1f}" cy="{yy*sc:.1f}" r="{10*sc:.1f}"/>')
    g.append(f'<g id="{sid}" fill="url(#stem)" stroke="{INK}" stroke-width="{3.5*sc:.1f}">' + "".join(cells) + '</g>')
    return "".join(g), L, Ls, w


def spindle(p, q, wid, cid):
    """músculo en huso de p a q con estrías"""
    dx, dy = q[0] - p[0], q[1] - p[1]
    ln = math.hypot(dx, dy); ux, uy = dx / ln, dy / ln; nx, ny = -uy, ux
    m = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
    a = (m[0] + nx * wid / 2, m[1] + ny * wid / 2); b = (m[0] - nx * wid / 2, m[1] - ny * wid / 2)
    d = (f"M {p[0]:.1f} {p[1]:.1f} Q {a[0]-ux*ln*0.25:.1f} {a[1]-uy*ln*0.25:.1f} {a[0]:.1f} {a[1]:.1f} Q {a[0]+ux*ln*0.25:.1f} {a[1]+uy*ln*0.25:.1f} {q[0]:.1f} {q[1]:.1f} "
         f"Q {b[0]+ux*ln*0.25:.1f} {b[1]+uy*ln*0.25:.1f} {b[0]:.1f} {b[1]:.1f} Q {b[0]-ux*ln*0.25:.1f} {b[1]-uy*ln*0.25:.1f} {p[0]:.1f} {p[1]:.1f} Z")
    s = f'<g id="{cid}"><path d="{d}" fill="url(#muscle)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
    for t in (-0.22, 0, 0.22):
        c0 = (m[0] + nx * wid * t - ux * ln * 0.3, m[1] + ny * wid * t - uy * ln * 0.3)
        c1 = (m[0] + nx * wid * t + ux * ln * 0.3, m[1] + ny * wid * t + uy * ln * 0.3)
        s += f'<line x1="{c0[0]:.1f}" y1="{c0[1]:.1f}" x2="{c1[0]:.1f}" y2="{c1[1]:.1f}" stroke="#FFC2B2" stroke-width="3" stroke-linecap="round" opacity="0.8"/>'
    s += '</g>'
    return s, m


def world(S, lean, pt):
    c, s = math.cos(math.radians(lean)), math.sin(math.radians(lean))
    return (S[0] + pt[0] * c - pt[1] * s, S[1] + pt[0] * s + pt[1] * c)


hairs = [((420, Y0), 1.0, "1"), ((848, Y0), 0.72, "2")]
info = {}
bumps, hairsvg, muscles = [], [], []
for S, sc, n in hairs:
    body, L, Ls, w = hair_local(sc, f"stem{n}" if n == "1" else f"stemb{n}")
    # bounding box simétrica respecto a S para que el origen "center" del grupo sea S
    E = L + 40 * sc
    inv = f'<rect x="{S[0]-E:.1f}" y="{S[1]-E:.1f}" width="{2*E:.1f}" height="{2*E:.1f}" fill="none" stroke="none" opacity="0"/>'
    hairsvg.append(f'<g id="hair{n}">{inv}<g transform="translate({S[0]} {S[1]}) rotate({LEAN})">{body}</g></g>')
    A_loc = (w, 185 * sc)
    A = world(S, LEAN, A_loc)
    A2 = rot(A, S, ROT)
    D = (S[0] + 175 * sc, Y0 + 72 * sc)
    D2 = (D[0] - 4, D[1] + 4)
    mr, m1 = spindle(A, D, 34 * sc, f"musr{n}")
    mc, m2 = spindle(A2, D2, 48 * sc, f"musc{n}")
    muscles.append((mr, mc))
    # bulto de la piel de gallina
    bx0, bx1, h = S[0] - 150 * sc, S[0] + 170 * sc, 30 * sc
    bd = f"M {bx0:.1f} {Y0} C {bx0+60*sc:.1f} {Y0}, {S[0]-50*sc:.1f} {Y0-h:.1f}, {S[0]+10*sc:.1f} {Y0-h:.1f} C {S[0]+80*sc:.1f} {Y0-h:.1f}, {bx1-60*sc:.1f} {Y0}, {bx1:.1f} {Y0}"
    bumps.append(f'<g id="bump{n}"><path d="{bd} L {bx1:.1f} {Y0+12} L {bx0:.1f} {Y0+12} Z" fill="#F2C2A2"/>'
                 f'<path d="{bd}" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
                 f'<path d="{bd}" fill="none" stroke="#FBE0CF" stroke-width="4" opacity="0.8" transform="translate(0 9)"/></g>')
    info[n] = dict(S=S, A=A, A2=A2, D=D, m1=m1, m2=m2, L=L, Ls=Ls, w=w, sc=sc)

o.extend(bumps)
o.append('<g id="musrelax">' + "".join(m[0] for m in muscles) + '</g>')
o.append('<g id="muscontract">' + "".join(m[1] for m in muscles) + '</g>')
o.extend(hairsvg)

# nervio simpático: entra por la derecha y se ramifica hacia los dos músculos
i1, i2 = info["1"], info["2"]
E1 = ((i1["m1"][0] + i1["m2"][0]) / 2 + 6, (i1["m1"][1] + i1["m2"][1]) / 2 + 4)
E2 = ((i2["m1"][0] + i2["m2"][0]) / 2 + 4, (i2["m1"][1] + i2["m2"][1]) / 2 + 3)
trunk = f"M 1010 505 C 900 500, 780 492, 690 470"
br1 = f"M 690 470 C 610 450, {E1[0]+60:.0f} {E1[1]+70:.0f}, {E1[0]:.1f} {E1[1]:.1f}"
br2 = f"M 960 503 C 975 450, {E2[0]+50:.0f} {E2[1]+60:.0f}, {E2[0]:.1f} {E2[1]:.1f}"
SC = world(i1["S"], LEAN, (i1["w"] + 2, 196))
brs = f"M 690 470 C 600 480, {SC[0]+90:.0f} {SC[1]+60:.0f}, {SC[0]:.1f} {SC[1]:.1f}"
o.append('<g id="nerve">' + stroke2(trunk, 13, "#FFD34D", 7) + stroke2(br1, 9, "#FFD34D", 7) + stroke2(br2, 8, "#FFD34D", 7) +
         f'<path d="{trunk}" fill="none" stroke="#FFF3B8" stroke-width="3" opacity="0.8" transform="translate(0 -3)"/>' +
         f'<g fill="#FFD34D" stroke="{INK}" stroke-width="4"><circle cx="{E1[0]:.1f}" cy="{E1[1]:.1f}" r="9"/><circle cx="{E2[0]:.1f}" cy="{E2[1]:.1f}" r="8"/></g></g>')
o.append('<g id="nervesc">' + stroke2(brs, 8, "#FFD34D", 7) + f'<circle cx="{SC[0]:.1f}" cy="{SC[1]:.1f}" r="9" fill="#FFD34D" stroke="{INK}" stroke-width="4"/></g>')
o.append(f'<g id="signal" fill="none" stroke="{LIME}" stroke-width="6" stroke-linecap="round"><path d="{trunk}"/><path d="{br1}"/><path d="{br2}"/></g>')
o.append(f'<g id="signalsc" fill="none" stroke="{LIME}" stroke-width="6" stroke-linecap="round"><path d="{trunk}"/><path d="{brs}"/></g>')

# etiquetas
S1 = i1["S"]
tipP = world(S1, LEAN, (0, -110))
o.append(tag("lpelo", 560, 62, tw("PELO"), "PELO", 560, 91, f"{tipP[0]:.0f}", f"{tipP[1]:.0f}"))
tipU = rot(tipP, S1, ROT)
o.append(tag("lpunta", 560, 70, tw("¡DE PUNTA!"), "¡DE PUNTA!", 560, 99, f"{tipU[0]+4:.0f}", f"{tipU[1]:.0f}"))
o.append(tag("lbulto", 120, 112, tw("BULTITO"), "BULTITO", 290, 170, f"{S1[0]-60:.0f}", f"{Y0-22}"))
mm = i1["m1"]
o.append(tag("lmusculo", 520, 132, tw("MÚSCULO ERECTOR"), "MÚSCULO ERECTOR", 620, 190, f"{mm[0]+50:.0f}", f"{mm[1]-22:.0f}"))
o.append(tag("lnervio", 720, 590, tw("NERVIO"), "NERVIO", 860, 590, 870, 508))
o.append(tag("lsimpatico", 560, 590, tw("SISTEMA SIMPÁTICO"), "SISTEMA SIMPÁTICO", 860, 590, 870, 508))
stp = world(S1, LEAN, (-i1["w"], 150))
o.append(tag("lcelulas", 80, 150, tw("CÉLULAS MADRE"), "CÉLULAS MADRE", 250, 208, f"{stp[0]-8:.0f}", f"{stp[1]+6:.0f}"))
bulbP = world(S1, LEAN, (-30, i1["L"] - 10))
o.append(tag("lfoliculo", 40, 588, tw("FOLÍCULO"), "FOLÍCULO", 160, 588, f"{bulbP[0]-6:.0f}", f"{bulbP[1]+4:.0f}"))
o.append('</svg>')
print("\n".join(o))

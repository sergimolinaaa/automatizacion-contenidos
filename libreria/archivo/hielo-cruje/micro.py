from hc import *

OUT = "micro.svg"
LX, RX, CY, R = 240, 720, 360, 195
extra = (lg("bgM", [(0, "#EAF2FF"), (1, "#D3E2F6")])
         + f'<clipPath id="clipF"><circle cx="{LX}" cy="{CY}" r="{R-8}"/></clipPath><clipPath id="clipC"><circle cx="{RX}" cy="{CY}" r="{R-8}"/></clipPath>'
         + rg("lensF", [(0, "#F2FBFF"), (1, "#BFE6FA")]) + rg("lensC", [(0, "#FFF4EA"), (1, "#FFD2B5")]))
o = [header(1000, 700, extra)]
o.append('<rect width="1000" height="700" fill="url(#bgM)"/>')
o.append('<g fill="#C9D9EE">' + "".join(f'<circle cx="{x}" cy="{y}" r="4"/>' for x in range(40, 1000, 60) for y in range(40, 700, 60)) + "</g>")


def lattice(cx, cy, a, warm, seed):
    rnd = random.Random(seed)
    pts = []
    s3 = math.sqrt(3)
    for i in range(-8, 9):
        for j in range(-8, 9):
            bx = cx + i * a * s3 + j * a * s3 / 2
            by = cy + j * a * 1.5
            pts.append((bx, by))
            pts.append((bx, by + a))
    pts = [p for p in pts if math.hypot(p[0] - cx, p[1] - cy) < R + a]
    bonds, mols = "", ""
    for k, (x, y) in enumerate(pts):
        nb = [(x2, y2) for (x2, y2) in pts if abs(math.hypot(x2 - x, y2 - y) - a) < 1]
        for (x2, y2) in nb:
            if (x2, y2) > (x, y):
                bonds += f'<path d="M {f(x)} {f(y)} L {f(x2)} {f(y2)}" stroke="#7D8FB0" stroke-width="5" stroke-linecap="round"/>'
        if len(nb) >= 2:
            a1 = math.atan2(nb[0][1] - y, nb[0][0] - x)
            a2 = math.atan2(nb[1][1] - y, nb[1][0] - x)
            bis = math.degrees(math.atan2(math.sin(a1) + math.sin(a2), math.cos(a1) + math.cos(a2)))
        else:
            bis = rnd.uniform(0, 360)
        jx = rnd.uniform(-3, 3) if warm else 0
        jy = rnd.uniform(-3, 3) if warm else 0
        mols += water_mol(x + jx, y + jy, a * 0.3, bis + (rnd.uniform(-14, 14) if warm else 0), warm)
        if warm and k % 3 == 0:
            mols += (f'<path d="M {f(x-a*0.62)} {f(y-a*0.2)} Q {f(x-a*0.75)} {f(y)} {f(x-a*0.62)} {f(y+a*0.2)}" fill="none" stroke="{CORAL}" stroke-width="4" stroke-linecap="round"/>'
                     f'<path d="M {f(x+a*0.62)} {f(y-a*0.2)} Q {f(x+a*0.75)} {f(y)} {f(x+a*0.62)} {f(y+a*0.2)}" fill="none" stroke="{CORAL}" stroke-width="4" stroke-linecap="round"/>')
    return bonds, mols


def lupa(cx, id_, lens, clip, inner):
    s = f'<g id="{id_}">'
    s += f'<path d="M {cx+R*0.7} {CY+R*0.7} L {cx+R*0.7+78} {CY+R*0.7+78}" stroke="{INK}" stroke-width="52" stroke-linecap="round"/>'
    s += f'<path d="M {cx+R*0.7+4} {CY+R*0.7+4} L {cx+R*0.7+74} {CY+R*0.7+74}" stroke="#6A4A2E" stroke-width="36" stroke-linecap="round"/>'
    s += f'<circle cx="{cx+8}" cy="{CY+10}" r="{R+14}" fill="{INK}" opacity="0.2"/>'
    s += f'<circle cx="{cx}" cy="{CY}" r="{R}" fill="url(#{lens})"/>'
    s += f'<g clip-path="url(#{clip})">{inner}</g>'
    s += f'<circle cx="{cx}" cy="{CY}" r="{R}" fill="none" stroke="{INK}" stroke-width="22"/>'
    s += f'<circle cx="{cx}" cy="{CY}" r="{R}" fill="none" stroke="url(#metalG)" stroke-width="12"/>'
    s += f'<path d="M {cx-R*0.62} {CY-R*0.35} A {R*0.72} {R*0.72} 0 0 1 {cx-R*0.2} {CY-R*0.68}" fill="none" stroke="#FFFFFF" stroke-width="12" stroke-linecap="round" opacity="0.8"/>'
    return s + "</g>"


bF, mF = lattice(LX, CY - 20, 50, False, 1)
bC, mC = lattice(RX, CY - 20, 60, True, 2)
o.append(lupa(LX, "lupaF", "lensF", "clipF", bF + f'<g id="molsF">{mF}</g>'))
o.append(lupa(RX, "lupaC", "lensC", "clipC", bC + f'<g id="molsC">{mC}</g>'))
# flechas: se separan
outs = ""
for ang in (205, 335):
    a = math.radians(ang)
    x1, y1 = RX + (R + 22) * math.cos(a), CY + (R + 22) * math.sin(a)
    x2, y2 = RX + (R + 66) * math.cos(a), CY + (R + 66) * math.sin(a)
    outs += arrow(None, ((x1, y1), (x2, y2)), col=CORAL, w=11, head=24)
o.append(g("separan", outs))
o.append(g("notas", note(480, 175, 48, LIME, -10) + note(950, 455, 44, YEL, 12)))
for id_, x, y, t, bg, fg in (("lfrio", LX, 110, "CENTRO FRÍO", "#3E95E0", "#FFFFFF"),
                             ("ltemp", RX, 110, "CAPA TEMPLADA", CORAL, "#FFFFFF"),
                             ("lquietas", LX - 20, 615, "QUIETAS", INK, LIME),
                             ("lseparan", RX - 40, 615, "SE SEPARAN", INK, LIME)):
    s, _ = label(id_, x, y, t, bg=bg, fg=fg, size=30); o.append(s)
s, _ = label("lexag", RX, CY + R - 50, "EXAGERADO", bg="#FFFFFF", fg=INK, size=20); o.append(s)
o.append("</svg>")
save(OUT, "\n".join(o))

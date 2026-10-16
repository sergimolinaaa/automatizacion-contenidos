from vb import *

OUT = "hemi_free.svg"
W, H = 1000, 900
CX, CY = 500, 500
R0, R1, SR, ROWS = 200, 370, 30, 3
o = [header(W, H)]
names = []
for p in PARTIES:
    names += [p[0]] * ANTES[p[0]]
assert len(names) == SEATS
# suelo del hemiciclo
A0, A1 = R0 - SR - 26, R1 + SR + 24
ring = f'M {CX-A1} {CY} A {A1} {A1} 0 0 1 {CX+A1} {CY} L {CX+A0} {CY} A {A0} {A0} 0 0 0 {CX-A0} {CY} Z'
o.append(f'<path d="{ring}" fill="{INK}" opacity="0.25" transform="translate(8 10)"/>')
o.append(f'<path d="{ring}" fill="url(#woodH)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
for k in range(1, ROWS):
    rr = R0 + (R1 - R0) * (k - 0.5) / (ROWS - 1)
    o.append(f'<path d="M {f(CX-rr)} {CY} A {f(rr)} {f(rr)} 0 0 1 {f(CX+rr)} {CY}" fill="none" stroke="#7E4E28" stroke-width="3" opacity="0.6"/>')
o.append(f'<path d="M {CX-A0} {CY} A {A0} {A0} 0 0 1 {CX+A0} {CY} Z" fill="url(#carpet)" stroke="{INK}" stroke-width="5"/>')
o.append(f'<rect x="{CX-A0*0.42}" y="{CY-A0*0.36}" width="{A0*0.84}" height="{A0*0.3}" rx="6" fill="#E9D3A8" stroke="{INK}" stroke-width="4"/>')
seats = hemiciclo(CX, CY, SEATS, ROWS, R0, R1, [COL[n] for n in names], SR, sw=4)
by = {}
for (s, x, y), n in zip(seats, names):
    by.setdefault(n, []).append((s, x, y))
body = ""
for n, lst in by.items():
    body += f'<g id="h{SHAPE[n]}">' + "".join(s + icon(SHAPE[n], x, y + 1, SR * 0.4, "#FFFFFF", sw=2.5) for s, x, y in lst) + "</g>"
o.append(g("asientos", body))
_, rx, ry = by["ROMBO"][0]
print("rombo seat", rx, ry)
# escaño que pasa a Círculo (encima del de Rombo)
o.append(g("nuevo", f'<circle cx="{f(rx)}" cy="{f(ry)}" r="{SR}" fill="{COL["CÍRCULO"]}" stroke="{INK}" stroke-width="4"/>'
           + f'<circle cx="{f(rx-SR*0.3)}" cy="{f(ry-SR*0.35)}" r="{f(SR*0.28)}" fill="#FFFFFF" opacity="0.55"/>'
           + icon("circle", rx, ry + 1, SR * 0.4, "#FFFFFF", sw=2.5)))
o.append(g("anillo", f'<circle cx="{f(rx)}" cy="{f(ry)}" r="{SR+12}" fill="none" stroke="{LIME}" stroke-width="8"/>'
           f'<circle cx="{f(rx)}" cy="{f(ry)}" r="{SR+18}" fill="none" stroke="{INK}" stroke-width="3"/>'))


def chip(id_, x, y, shape, num, hot=False, w=172):
    s = f'<g id="{id_}">'
    s += f'<rect x="{x-w/2+6}" y="{y-36+8}" width="{w}" height="72" rx="36" fill="{INK}" opacity="0.25"/>'
    s += f'<rect x="{x-w/2}" y="{y-36}" width="{w}" height="72" rx="36" fill="#FFFFFF" stroke="{CORAL if hot else INK}" stroke-width="{8 if hot else 5}"/>'
    s += icon(shape, x - w / 2 + 42, y, 21, COL[[p[0] for p in PARTIES if p[2] == shape][0]])
    s += T(x + 26, y + 17, str(num), 46, CORAL if hot else INK, font=DISP)
    return s + "</g>"


XS = [105, 302, 500, 698, 895]
CHY = 600
chips = ""
for x, p in zip(XS, PARTIES):
    chips += chip(f"c{p[2]}", x, CHY, p[2], ANTES[p[0]])
o.append(g("chips", chips))
# chips tras el aumento del voto en blanco
o.append(chip("c2circle", XS[1], CHY, "circle", DESPUES["CÍRCULO"]))
o.append(chip("c2diamond", XS[4], CHY, "diamond", DESPUES["ROMBO"], hot=True))
# etiquetas
s, _ = label("t30", 500, 720, "30 ESCAÑOS · 30 OCUPADOS", bg=INK, fg=LIME, size=30); o.append(s)
o.append(stamp2(500, 820, "0 VACÍOS", 40, rot=-4, col="#3E8E1E", id_="cero"))
o.append(stamp2(800, 820, "FUERA", 40, rot=-6, col=CORAL, id_="fuera"))
s, _ = label("tpasa", 330, 820, "+1 PARA CÍRCULO", bg="#FFFFFF", fg=INK, size=28); o.append(s)
o.append("</svg>")
save(OUT, "\n".join(o))

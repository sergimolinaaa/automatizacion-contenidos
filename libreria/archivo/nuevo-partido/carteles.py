from np import *

OUT = "carteles.svg"
defs = BASE_DEFS + NP_DEFS + lg("bgP", [(0, "#EAF3F7"), (1, "#CFE2EA")]) + lg("floorP", [(0, "#BFA27E"), (1, "#8E6F4C")])
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 700">\n<defs>{defs}</defs>']
o.append('<rect width="1000" height="700" fill="url(#bgP)"/>')
o.append('<g stroke="#B9D0DA" stroke-width="3">' + "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="600"/>' for x in range(50, 1000, 100)) + "</g>")
o.append(f'<rect x="0" y="600" width="1000" height="100" fill="url(#floorP)"/><path d="M 0 600 L 1000 600" stroke="{INK}" stroke-width="6"/>')
o.append('<path d="M 430 0 L 570 0 L 650 640 L 350 640 Z" fill="#FFFFFF" opacity="0.35"/>')

# rótulo con el nombre
o.append(G("nombre", f'<rect x="318" y="88" width="372" height="78" rx="14" fill="{INK}" opacity="0.25" transform="translate(6 8)"/>'
           f'<rect x="318" y="88" width="372" height="78" rx="14" fill="url(#tealG)" stroke="{INK}" stroke-width="6"/>'
           + T(504, 140, "DEMOCRACIA 21", 34, "#FFFFFF", font=DISP)))
s, _ = label("tsegun", 504, 205, "SEGÚN SU PRESENTACIÓN", bg=INK, fg=LIME, size=22); o.append(s)
o.append(G("atril", lectern(500, 640, 190, 220)))

# iconos de los carteles
def ic_reforma(cx, cy):
    r = 40
    d = f"M {f(cx+r)} {f(cy)} A {r} {r} 0 1 1 {f(cx+r*0.3)} {f(cy-r*0.95)}"
    return (dbl(d, 12, TEAL, 7) + dbl(f"M {f(cx+r*0.05)} {f(cy-r*1.25)} L {f(cx+r*0.38)} {f(cy-r*0.95)} L {f(cx+r*0.02)} {f(cy-r*0.62)}", 12, TEAL, 7)
            + f'<rect x="{f(cx-16)}" y="{f(cy-20)}" width="32" height="40" rx="4" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/>'
            + "".join(f'<path d="M {f(cx-9)} {f(cy-8+k*10)} L {f(cx+9)} {f(cy-8+k*10)}" stroke="#9AA3B5" stroke-width="4" stroke-linecap="round"/>' for k in range(3)))

def ic_consenso(cx, cy):
    def bub(x, y, col, flip):
        s = -1 if flip else 1
        return (f'<path d="M {f(x-38)} {f(y-26)} Q {f(x-38)} {f(y-40)} {f(x-24)} {f(y-40)} L {f(x+24)} {f(y-40)} Q {f(x+38)} {f(y-40)} {f(x+38)} {f(y-26)} L {f(x+38)} {f(y+8)} Q {f(x+38)} {f(y+22)} {f(x+24)} {f(y+22)} L {f(x+s*10)} {f(y+22)} L {f(x-s*14)} {f(y+40)} L {f(x-s*12)} {f(y+22)} L {f(x-24)} {f(y+22)} Q {f(x-38)} {f(y+22)} {f(x-38)} {f(y+8)} Z" '
                f'fill="{col}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    return bub(cx - 28, cy - 4, CORAL, False) + bub(cx + 28, cy + 6, VIO, True) + check(cx, cy + 2, 20)

def ic_modern(cx, cy):
    u, _ = urna(cx - 6, cy + 42, 76, 70, None, n_sobres=3, seed=3)
    sp = lambda x, y, r: f'<path d="M {f(x)} {f(y-r)} Q {f(x)} {f(y)} {f(x+r)} {f(y)} Q {f(x)} {f(y)} {f(x)} {f(y+r)} Q {f(x)} {f(y)} {f(x-r)} {f(y)} Q {f(x)} {f(y)} {f(x)} {f(y-r)} Z" fill="{YEL}" stroke="{INK}" stroke-width="3"/>'
    return u + sp(cx + 52, cy - 34, 16) + sp(cx - 54, cy - 24, 12) + sp(cx + 60, cy + 14, 10)

def ic_centro(cx, cy):
    o = ""
    for r, c in ((50, "#FFFFFF"), (36, "#CDEFEA"), (22, TEAL)):
        o += f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{r}" fill="{c}" stroke="{INK}" stroke-width="4"/>'
    return o + person_icon(cx, cy - 2, 34, col="#FFFFFF", sw=4)

CW, CH = 300, 205
specs = [("c1", 190, 300, "REFORMISTA", "QUIERE REFORMAS", ic_reforma, TEAL, -3),
         ("c2", 190, 530, "CONSENSOS", "= ACUERDOS ENTRE DISTINTOS", ic_consenso, CORAL, 2),
         ("c3", 810, 300, "MODERNIZAR", "LA DEMOCRACIA", ic_modern, VIO, 3),
         ("c4", 810, 530, "EL CIUDADANO", "«EN EL CENTRO»", ic_centro, YEL, -2)]
for id_, cx, cy, t, sub, ic, acc, rot in specs:
    o.append(G(id_, card(cx, cy, CW, CH, t, sub, ic(cx, cy - 36), accent=acc, rot=rot, tsize=30 if len(t) < 11 else 26, ssize=17 if len(sub) > 18 else 20)))
o.append("</svg>")
save(OUT, "\n".join(o))

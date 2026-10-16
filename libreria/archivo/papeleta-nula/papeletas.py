from pn import *

OUT = "papeletas.svg"
o = [header(1000, 700, SEPIA + lg("bgP", [(0, "#DDEBFF"), (1, "#F4F8FF")]) + lg("deskG", [(0, "#D9A46C"), (1, "#9C6334")]))]
o.append('<rect width="1000" height="700" fill="url(#bgP)"/>')
o.append('<rect x="0" y="560" width="1000" height="140" fill="url(#deskG)"/>')
o.append(f'<path d="M 0 560 L 1000 560" stroke="{INK}" stroke-width="6"/>')
o.append('<path d="M 0 600 L 1000 600 M 0 650 L 1000 650" stroke="#7A4E2A" stroke-width="3" opacity="0.45"/>')
W, H, CY = 250, 340, 375
cols = [(185, "star", -4, "tachar"), (500, "circle", 2, "añadir"), (815, "tri", -2, "escribir")]
for i, (cx, sh, rot, kind) in enumerate(cols):
    b, ys = ballot(cx, CY, W, H, sh, rows=5)
    extra = ""
    x0 = cx - W / 2
    if kind == "tachar":
        extra = scribble(x0 + W * 0.18, x0 + W * 0.84, ys[1], 9, 8, sw=8, id_="m1")
    elif kind == "añadir":
        extra = (f'<g id="m2"><path d="M {f(x0+W*0.2)} {f(ys[-1]+38)} L {f(x0+W*0.32)} {f(ys[-1]+38)} M {f(x0+W*0.26)} {f(ys[-1]+32)} L {f(x0+W*0.26)} {f(ys[-1]+44)}" stroke="{BLUE}" stroke-width="5" stroke-linecap="round"/>'
                 f'<path d="M {f(x0+W*0.38)} {f(ys[-1]+44)} q 10 -26 20 -6 q 8 16 18 -8 q 10 -18 18 4 q 10 18 20 -6 q 10 -16 18 2 q 8 14 22 -4" fill="none" stroke="{BLUE}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></g>')
    else:
        extra = (f'<g id="m3"><g transform="rotate(-18 {cx} {CY+60})">' + T(cx, CY + 70, "¡HOLA!", 44, BLUE, font=DISP, extra='font-style="italic"')
                 + f'<path d="M {f(cx-95)} {f(CY+88)} q 95 18 190 -4" fill="none" stroke="{BLUE}" stroke-width="5" stroke-linecap="round"/></g></g>')
    o.append(f'<g id="b{i+1}"><g transform="rotate({rot} {cx} {CY})">{b}{extra}</g></g>')
    o.append(cross(cx + W / 2 - 10, CY - H / 2 + 6, 34, id_=f"x{i+1}"))
s, _ = label("l1", 185, 140, "TACHAR", bg=INK, fg=LIME, size=30); o.append(s)
s, _ = label("l2", 500, 140, "AÑADIR", bg=INK, fg=LIME, size=30); o.append(s)
s, _ = label("l3", 815, 140, "ESCRIBIR", bg=INK, fg=LIME, size=30); o.append(s)
o.append(stamp2(500, 598, "NULO = NO CUENTA", 34, rot=-3, id_="nulo"))
o.append("</svg>")
save(OUT, "\n".join(o))

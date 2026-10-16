import sys, math, random
sys.path.insert(0, sys.path[0])
from rb import *

H = 468                     # horizonte
O = (500, 522)              # punto antisolar (sombra de la cabeza): centro del arcoíris
R1 = 300                    # borde exterior (rojo) del arco principal, ~42°
W1 = 6.2
R2 = round(R1 * 50.4 / 42.3)   # borde interior (rojo) del secundario, ~50,4°
W2 = 7.0
r1_in = R1 - 6 * W1
r2_out = R2 + 6 * W2
print("R2", R2, "r2_out", r2_out, file=sys.stderr)

defs = "\n".join([
    lg("sky", [(0, "#4C5D77"), (0.55, "#8193AB"), (1, "#C9D5E0")]),
    lg("field", [(0, "#8FD27A"), (1, "#3E9A4A")]),
    lg("field2", [(0, "#A9DB8F"), (1, "#79C06B")]),
    rg("shadow", [(0, "#1F4D27", 0.6), (1, "#1F4D27", 0.25)]),
    DEFS_P,
])
o = [header(defs)]
o.append('<rect width="1000" height="700" fill="url(#sky)"/>')
# cortina de lluvia lejana
rnd = random.Random(11)
st = []
for _ in range(90):
    x, y = rnd.uniform(0, 1000), rnd.uniform(40, H - 30)
    st.append(f"M {x:.0f} {y:.0f} L {x - 6:.0f} {y + 34:.0f}")
o.append(f'<g id="lluvia"><path d="{" ".join(st)}" stroke="#DDE6F0" stroke-width="2.5" opacity="0.28" stroke-linecap="round"/></g>')
# cielo más claro dentro del arco principal, más oscuro entre los dos arcos (banda de Alejandro)
o.append(f'<g id="dentro"><path d="{disc_above(O[0], O[1], r1_in, H)}" fill="#FFFFFF" opacity="0.22"/></g>')
o.append(f'<g id="banda"><path d="{annulus_above(O[0], O[1], R1, R2, H)}" fill="#1A2235" opacity="0.33"/></g>')
# arcos
o.append('<g id="prim">' + band(O[0], O[1], R1, W1, H, SPEC, 1.0) + '</g>')
o.append('<g id="sec">' + band(O[0], O[1], r2_out, W2, H, list(reversed(SPEC)), 0.62) + '</g>')

# paisaje
o.append(f'<path d="M 0 {H} C 120 {H - 26}, 260 {H - 18}, 360 {H - 30} C 470 {H - 42}, 600 {H - 22}, 700 {H - 30} C 820 {H - 40}, 920 {H - 22}, 1000 {H - 28} L 1000 {H + 10} L 0 {H + 10} Z" fill="#8DB89A"/>')
o.append('<g>' + tree(110, H - 12, 0.55, "#6E9F80", far=True) + tree(860, H - 14, 0.6, "#6E9F80", far=True) + tree(905, H - 10, 0.45, "#6E9F80", far=True) + '</g>')
o.append(f'<path d="M 0 {H} L 1000 {H} L 1000 700 L 0 700 Z" fill="url(#field)" stroke="{INK}" stroke-width="6"/>')
# surcos del campo en perspectiva hacia el punto de fuga
fur = []
for k in range(-8, 9):
    fur.append(f"M {500 + k * 18} {H + 4} L {500 + k * 150} 700")
o.append(f'<path d="{" ".join(fur)}" stroke="#2F7F3B" stroke-width="3" opacity="0.35"/>')
o.append(f'<path d="M 0 {H + 4} L 1000 {H + 4}" stroke="#C7F0B0" stroke-width="3" opacity="0.7"/>')
o.append('<g id="arboles">' + tree(70, H + 40, 1.0, "#2E8B57") + tree(150, H + 28, 0.8, "#3FA066") + tree(930, H + 44, 1.05, "#2E8B57") + '</g>')

# círculo completo: lo que el suelo "tapa"
o.append(f'<g id="circ"><path d="{arc_below(O[0], O[1], R1 - 3 * W1, H)}" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-dasharray="16 12" opacity="0.95"/></g>')

# sombra del observador hacia el punto antisolar (perspectiva)
o.append(f'<g id="sombra"><path d="M 470 700 L 492 {O[1] + 12} C 494 {O[1] - 4}, 506 {O[1] - 4}, 508 {O[1] + 12} L 530 700 Z" fill="url(#shadow)"/>'
         f'<ellipse cx="{O[0]}" cy="{O[1] + 2}" rx="12" ry="8" fill="#1F4D27" opacity="0.7"/></g>')
o.append(person_back(500, 760, 1.0))

labels = []
t, b = tag("lsombra", 660, 600, "TU SOMBRA", target=(O[0] + 10, O[1] + 2), anchor_from=(600, 580)); o.append(t); labels.append(b)
# rojo fuera en el principal, dentro en el secundario
def on(r, deg):
    a = math.radians(deg)
    return (O[0] + r * math.cos(a), O[1] + r * math.sin(a))
p1 = on(R1 - W1 / 2, -148)
p2 = on(R2 + W2 / 2, -128)
t, b = tag("lrojo1", 104, 330, "ROJO", bg="#FF3B30", fg=INK, target=p1, anchor_from=(140, 340)); o.append(t); labels.append(b)
t, b = tag("lrojo2", 150, 168, "ROJO", bg="#FF3B30", fg=INK, target=p2, anchor_from=(180, 180)); o.append(t); labels.append(b)
p3 = on(r2_out - 10, -52)
t, b = tag("lsec", 850, 110, "2.º ARCO", target=p3, anchor_from=(820, 130)); o.append(t); labels.append(b)
p4 = on((R1 + R2) / 2, -90)
t, b = tag("lbanda", 500, 372, "BANDA DE ALEJANDRO", target=p4, anchor_from=(500, 344)); o.append(t); labels.append(b)
for i in range(len(labels)):
    for j in range(i + 1, len(labels)):
        if boxes_overlap(labels[i], labels[j]):
            print("SOLAPE", i, j, file=sys.stderr)
print("p", p1, p2, p3, p4, file=sys.stderr)
o.append('</svg>')
open(sys.argv[1], "w").write("\n".join(o))

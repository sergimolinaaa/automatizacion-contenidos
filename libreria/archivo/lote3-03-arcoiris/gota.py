import sys, math, random
sys.path.insert(0, sys.path[0])
from dl import *

CX, CY, R = 640, 298, 172
# índices de refracción: rojo real (1,331); el resto exagerado para que se vea la separación
COLS = [("#FF3B30", 1.331), ("#FF9500", 1.336), ("#FFE11A", 1.341), ("#34C759", 1.346), ("#2D7BFF", 1.351), ("#9B4DFF", 1.357)]
N_MEAN = 1.335

def inter(p, d):
    """Segunda intersección del rayo p + t d (p sobre el círculo) con el círculo."""
    ox, oy = p[0] - CX, p[1] - CY
    b = ox * d[0] + oy * d[1]
    t = -2 * b
    return (p[0] + d[0] * t, p[1] + d[1] * t)

def refract(d, nrm, eta):
    cosi = -(nrm[0] * d[0] + nrm[1] * d[1])
    k = 1 - eta * eta * (1 - cosi * cosi)
    c = eta * cosi - math.sqrt(k)
    return (eta * d[0] + c * nrm[0], eta * d[1] + c * nrm[1])

def unit(v):
    l = math.hypot(*v); return (v[0] / l, v[1] / l)

def path_for(n):
    # rayo de Descartes (desviación mínima) para el índice amarillo
    cosi = math.sqrt((N_MEAN ** 2 - 1) / 3)
    i = math.acos(cosi)
    A = (CX - R * math.cos(i), CY - R * math.sin(i))
    d0 = (1.0, 0.0)
    nA = unit((A[0] - CX, A[1] - CY))
    d1 = refract(d0, nA, 1 / n)
    B = inter(A, d1)
    nB = unit((B[0] - CX, B[1] - CY))
    dot = d1[0] * nB[0] + d1[1] * nB[1]
    d2 = (d1[0] - 2 * dot * nB[0], d1[1] - 2 * dot * nB[1])
    C = inter(B, d2)
    nC = unit((C[0] - CX, C[1] - CY))
    d3 = refract(d2, (-nC[0], -nC[1]) if (d2[0] * nC[0] + d2[1] * nC[1]) < 0 else nC, n)
    # el vector normal debe apuntar contra el rayo: hacia dentro no; recalculamos bien
    d3 = refract(d2, (-nC[0], -nC[1]), n)
    dev = math.degrees(math.atan2(d3[1], -d3[0]))  # ángulo bajo la horizontal (hacia la izquierda)
    return A, B, C, d3, dev

paths = [(c, n) + path_for(n) for c, n in COLS]
for c, n, A, B, C, d3, dev in paths:
    print(c, n, "A", [round(v) for v in A], "B", [round(v) for v in B], "C", [round(v) for v in C], "ang", round(dev, 2), file=sys.stderr)

defs = "\n".join([
    lg("sky", [(0, "#30465F"), (0.6, "#22344C"), (1, "#141F30")]),
    rg("drop", [(0, "#F2FBFF", 0.95), (0.55, "#A9DBFA", 0.85), (0.9, "#5BA6DE", 0.9), (1, "#3D86C4", 0.95)], 0.42, 0.38, 0.62),
    rg("sun", [(0, "#FFFFFF"), (0.4, "#FFF3B0"), (1, "#FFD34D")], 0.4, 0.4, 0.6),
    rg("sunglow", [(0, "#FFE680", 0.6), (1, "#FFE680", 0)]),
    rg("fdrop", [(0, "#BFE6FF", 0.35), (1, "#BFE6FF", 0)]),
])
o = [header(defs)]
o.append('<rect width="1000" height="700" fill="url(#sky)"/>')
# gotas lejanas desenfocadas y lluvia de fondo (sin contorno)
rnd = random.Random(3)
far = []
for _ in range(18):
    x, y, r = rnd.uniform(0, 1000), rnd.uniform(40, 680), rnd.uniform(10, 34)
    if math.hypot(x - CX, y - CY) < R + 40:
        continue
    far.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="url(#fdrop)"/>')
o.append('<g id="gotas">' + "".join(far) + '</g>')
streaks = []
for _ in range(30):
    x, y = rnd.uniform(0, 1000), rnd.uniform(0, 660)
    streaks.append(f"M {x:.0f} {y:.0f} L {x - 6:.0f} {y + 36:.0f}")
o.append(f'<g id="lluvia"><path d="{" ".join(streaks)}" stroke="#9FC6E8" stroke-width="2.5" opacity="0.25" stroke-linecap="round"/></g>')

A = paths[0][2]
# sol a la izquierda
SX, SY = 64, A[1]
o.append(f'<g id="sol"><circle cx="{SX}" cy="{SY:.0f}" r="105" fill="url(#sunglow)"/>'
         f'<circle cx="{SX}" cy="{SY:.0f}" r="46" fill="url(#sun)" stroke="{INK}" stroke-width="6"/>'
         f'<ellipse cx="{SX - 14}" cy="{SY - 16:.0f}" rx="13" ry="8" fill="#FFFFFF" opacity="0.8"/></g>')

def ray(d, col, w=6, glow=18, op=1.0, ink=False):
    pre = f'<path d="{d}" stroke="{INK}" stroke-width="{w + 6}" stroke-linecap="round" fill="none"/>' if ink else ""
    return pre + (f'<path d="{d}" stroke="{col}" stroke-width="{glow}" opacity="{0.22 * op:.2f}" stroke-linecap="round" fill="none"/>'
            f'<path d="{d}" stroke="{col}" stroke-width="{w}" opacity="{op:.2f}" stroke-linecap="round" fill="none"/>')

# rayo de luz blanca (con borde de tinta para que sea pegatina)
bd = f"M {SX + 50} {A[1]:.1f} L {A[0]:.1f} {A[1]:.1f}"
o.append(f'<g id="beam"><path d="{bd}" stroke="#FFF6C8" stroke-width="34" opacity="0.18" stroke-linecap="round"/>'
         f'<path d="{bd}" stroke="{INK}" stroke-width="17" stroke-linecap="round"/><path d="{bd}" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round"/></g>')

# gota (esfera: las gotas de lluvia pequeñas son redondas, no con forma de lágrima)
o.append(f'<ellipse cx="{CX + 20}" cy="{CY + R + 40}" rx="0" ry="0"/>')
o.append(f'<g id="gota"><circle cx="{CX}" cy="{CY}" r="{R}" fill="url(#drop)" stroke="{INK}" stroke-width="8"/>'
         f'<path d="M {CX - R * 0.78:.0f} {CY - R * 0.2:.0f} A {R * 0.82:.0f} {R * 0.82:.0f} 0 0 1 {CX - R * 0.2:.0f} {CY - R * 0.78:.0f}" fill="none" stroke="#FFFFFF" stroke-width="12" stroke-linecap="round" opacity="0.75"/>'
         f'<ellipse cx="{CX + R * 0.45:.0f}" cy="{CY + R * 0.55:.0f}" rx="{R * 0.16:.0f}" ry="{R * 0.07:.0f}" transform="rotate(-40 {CX + R * 0.45:.0f} {CY + R * 0.55:.0f})" fill="#FFFFFF" opacity="0.45"/></g>')

# luz blanca dentro (antes de separarse)
c0 = path_for(N_MEAN)
o.append('<g id="inwhite">' + ray(f"M {c0[0][0]:.1f} {c0[0][1]:.1f} L {c0[1][0]:.1f} {c0[1][1]:.1f}", "#FFFFFF", 6, 18, ink=True) + '</g>')
o.append('<g id="whiteback">' + ray(f"M {c0[1][0]:.1f} {c0[1][1]:.1f} L {c0[2][0]:.1f} {c0[2][1]:.1f}", "#FFFFFF", 6, 18, ink=True) + '</g>')
o.append('<g id="whiteout">' + ray(f"M {c0[2][0]:.1f} {c0[2][1]:.1f} L {c0[2][0] + c0[3][0] * 700:.1f} {c0[2][1] + c0[3][1] * 700:.1f}", "#FFFFFF", 7, 20) + '</g>')
mid = paths[len(paths) // 2]
und = lambda a, b: f'<path d="M {a[0]:.1f} {a[1]:.1f} L {b[0]:.1f} {b[1]:.1f}" stroke="{INK}" stroke-width="24" opacity="0.55" stroke-linecap="round" fill="none"/>'
fin = und(mid[2], mid[3]) + "".join(ray(f"M {A_[0]:.1f} {A_[1]:.1f} L {B[0]:.1f} {B[1]:.1f}", c, 4.5, 12) for c, n, A_, B, C, d3, dev in paths)
fback = und(mid[3], mid[4]) + "".join(ray(f"M {B[0]:.1f} {B[1]:.1f} L {C[0]:.1f} {C[1]:.1f}", c, 4.5, 12) for c, n, A_, B, C, d3, dev in paths)
L_OUT = 700
fout = "".join(ray(f"M {C[0]:.1f} {C[1]:.1f} L {C[0] + d3[0] * L_OUT:.1f} {C[1] + d3[1] * L_OUT:.1f}", c, 6, 18) for c, n, A_, B, C, d3, dev in paths)
o.append('<g id="fanin">' + fin + '</g>')
o.append('<g id="fanback">' + fback + '</g>')
o.append('<g id="fanout">' + fout + '</g>')
# punto de rebote
Bs = [p[3] for p in paths]
bx = sum(b[0] for b in Bs) / len(Bs); by = sum(b[1] for b in Bs) / len(Bs)

# ángulo de 42° entre la luz que entra (horizontal) y la que sale (rojo)
red = paths[0]
Cr, d3r = red[4], red[5]
P0 = (Cr[0] + d3r[0] * 40, Cr[1] + d3r[1] * 40)   # vértice: un poco fuera de la gota sobre el rayo rojo
# referencia: dirección de vuelta hacia el Sol (horizontal a la izquierda)
ref = f"M {P0[0]:.1f} {P0[1]:.1f} L {P0[0] - 260:.1f} {P0[1]:.1f}"
ra = 130
ang = math.atan2(d3r[1], d3r[0])
e1 = (P0[0] - ra, P0[1])
e2 = (P0[0] + math.cos(ang) * ra, P0[1] + math.sin(ang) * ra)
arc = f"M {e1[0]:.1f} {e1[1]:.1f} A {ra} {ra} 0 0 0 {e2[0]:.1f} {e2[1]:.1f}"
o.append(f'<g id="ang"><path d="{ref}" stroke="#FFFFFF" stroke-width="4" stroke-dasharray="14 10" opacity="0.9"/>'
         + dbl(arc, 6, LIME, 6) + '</g>')
mid = math.pi + (math.atan2(d3r[1], -d3r[0])) * -1  # no usado
ma = math.pi - math.radians(17)
lx, ly = P0[0] + math.cos(ma) * 196, P0[1] + math.sin(ma) * 196
o.append(f'<g id="l42"><text x="{lx:.0f}" y="{ly + 22:.0f}" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="62" fill="{LIME}" stroke="{INK}" stroke-width="10" paint-order="stroke" stroke-linejoin="round">42°</text></g>')

labels = []
t, b = tag("lluz", 250, A[1] + 86, "LUZ BLANCA", target=(300, A[1] + 4), anchor_from=(280, A[1] + 58)); o.append(t); labels.append(b)
t, b = tag("ldobla", 290, A[1] + 180, "SE DOBLA", target=(A[0] + 2, A[1] + 6), anchor_from=(330, A[1] + 152)); o.append(t); labels.append(b)
t, b = tag("lrebota", 900, by + 170, "REBOTA", target=(bx - 6, by), anchor_from=(890, by + 142)); o.append(t); labels.append(b)
# rojo y violeta a la salida
vr = paths[-1]
def on_ray(pth, t):
    C_, d_ = pth[4], pth[5]
    return (C_[0] + d_[0] * t, C_[1] + d_[1] * t)
pr = on_ray(red, 120)
pv = on_ray(vr, 205)
t, b = tag("lrojo", pr[0] + 130, pr[1] + 16, "ROJO", bg="#FF3B30", fg=INK, target=pr, anchor_from=(pr[0] + 80, pr[1] + 16)); o.append(t); labels.append(b)
t, b = tag("lvioleta", 250, pv[1] - 4, "VIOLETA", bg="#9B4DFF", fg="#FFFFFF", target=pv, anchor_from=(330, pv[1] - 4)); o.append(t); labels.append(b)
for i in range(len(labels)):
    for j in range(i + 1, len(labels)):
        if boxes_overlap(labels[i], labels[j]):
            print("SOLAPE", i, j, file=sys.stderr)
print("B", bx, by, "P0", P0, "l42", lx, ly, "pr", pr, "pv", pv, file=sys.stderr)
o.append('</svg>')
open(sys.argv[1], "w").write("\n".join(o))

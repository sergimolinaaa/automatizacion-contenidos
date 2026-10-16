import sys, math, random
sys.path.insert(0, sys.path[0])
from seeds import *

AX, AY = 500, 452        # ápice del vilano
RP = 192
BEAK_END = 578
RY = 268
RX = 134                 # semieje del anillo
RT = 50                  # radio de cada sección (remolino)

defs = "\n".join([
    lg("bg", [(0, "#0E2A47"), (0.5, "#163E63"), (1, "#0C2238")]),
    rg("ringg", [(0, "#BFF3FF", 0.55), (0.7, "#5CC8F0", 0.35), (1, "#5CC8F0", 0)]),
    rg("swirl", [(0, "#E8FBFF", 0.85), (0.6, "#7FDBFF", 0.45), (1, "#3FA9E0", 0.1)]),
    rg("low", [(0, "#2457C9", 0.75), (1, "#2457C9", 0)]),
    DEFS_SEED,
])
o = [header(defs)]
o.append('<rect width="1000" height="700" fill="url(#bg)"/>')
# lámina láser del túnel de viento (fondo, sin contorno)
o.append('<rect x="0" y="0" width="1000" height="700" fill="#FFFFFF" opacity="0.03"/>')
o.append('<g fill="#FFFFFF" opacity="0.05"><rect x="60" y="0" width="14" height="700"/><rect x="930" y="0" width="10" height="700"/></g>')

# ---- líneas de corriente (el aire sube respecto a la semilla que cae)
def outer(x0):
    sign = 1 if x0 > 500 else -1
    A = 78 * math.exp(-(abs(x0 - 500) - 190) / 170)
    p = []
    for y in range(690, -1, -30):
        b = A * math.exp(-((y - 360) / 190) ** 2)
        p.append((x0 + sign * b, y))
    return p

def inner(x0):
    sign = 1 if x0 > 500 else -1
    p = []
    for y in range(690, -1, -24):
        if y > AY - 6:
            dx = 0
        else:
            t = min(1, (AY - 6 - y) / 170)
            s = t * t * (3 - 2 * t)
            dx = (RX + RT + 36 - abs(x0 - 500)) * s
            if y < 190:
                dx *= 0.75 + 0.25 * (y / 190)
        p.append((x0 + sign * dx, y))
    return p

lines = [outer(x) for x in (95, 175, 250, 750, 825, 905)] + [inner(x) for x in (425, 575)]
d = " ".join(smooth(p) for p in lines)
o.append(f'<path d="{d}" fill="none" stroke="#9BE7FF" stroke-width="7" opacity="0.13" stroke-linecap="round"/>')
o.append(f'<g id="aire"><path d="{d}" fill="none" stroke="#A8ECFF" stroke-width="3.5" opacity="0.75" stroke-linecap="round"/></g>')
# puntas de flecha (chevrons) para indicar que el aire sube
chev = []
for p in lines:
    for yy in (610, 120):
        q = min(p, key=lambda c: abs(c[1] - yy))
        chev.append(f"M {q[0] - 9:.1f} {q[1] + 8:.1f} L {q[0]:.1f} {q[1] - 4:.1f} L {q[0] + 9:.1f} {q[1] + 8:.1f}")
o.append(f'<path d="{" ".join(chev)}" fill="none" stroke="#A8ECFF" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" opacity="0.8"/>')

# ---- anillo de aire separado (vórtice anular)
def spiral(cx, cy, r, cw, turns=1.6):
    """Espiral con flecha; cw=True gira en sentido horario."""
    p = []
    n = 60
    for i in range(n + 1):
        t = i / n
        a = (-1 if not cw else 1) * t * turns * 2 * math.pi
        rr = r * (0.18 + 0.82 * t)
        p.append((cx + math.cos(a + 1.2) * rr, cy + math.sin(a + 1.2) * rr))
    return p

def swirl(id_, cx, cy, cw):
    s = f'<g id="{id_}">'
    s += f'<circle cx="{cx}" cy="{cy}" r="{RT + 12}" fill="url(#swirl)"/>'
    p = spiral(cx, cy, RT, cw)
    dd = smooth(p)
    s += f'<path d="{dd}" fill="none" stroke="{INK}" stroke-width="11" stroke-linecap="round"/>'
    s += f'<path d="{dd}" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>'
    # flecha al final de la espiral
    (x1, y1), (x2, y2) = p[-3], p[-1]
    ang = math.atan2(y2 - y1, x2 - x1)
    h = 20
    a1 = (x2 - h * math.cos(ang - 0.6), y2 - h * math.sin(ang - 0.6))
    a2 = (x2 - h * math.cos(ang + 0.6), y2 - h * math.sin(ang + 0.6))
    hd = f"M {a1[0]:.1f} {a1[1]:.1f} L {x2:.1f} {y2:.1f} L {a2[0]:.1f} {a2[1]:.1f}"
    s += f'<path d="{hd}" fill="none" stroke="{INK}" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>'
    s += f'<path d="{hd}" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
    # círculo invisible para centrar el giro en la sección
    s += f'<circle cx="{cx}" cy="{cy}" r="{RT + 14}" fill="none" stroke="none"/>'
    return s + '</g>'

o.append('<g id="anillo">')
# zona de baja presión dentro del anillo
o.append(f'<g id="baja"><ellipse cx="500" cy="{RY}" rx="{RX - 10}" ry="58" fill="url(#low)"/></g>')
# tubo del anillo en perspectiva: mitad de atrás
o.append(f'<path d="M {500 - RX} {RY} A {RX} 34 0 0 1 {500 + RX} {RY}" fill="none" stroke="url(#ringg)" stroke-width="64" opacity="0.9"/>')
o.append(f'<path d="M {500 - RX} {RY} A {RX} 34 0 0 1 {500 + RX} {RY}" fill="none" stroke="#DFF8FF" stroke-width="3" opacity="0.5" stroke-dasharray="10 12" transform="translate(0 -18)"/>')
# secciones: izquierda gira en sentido horario (sube por fuera, baja por el eje)
o.append(swirl("swl", 500 - RX, RY, True))
o.append(swirl("swr", 500 + RX, RY, False))
# mitad de delante del tubo
o.append(f'<path d="M {500 - RX} {RY} A {RX} 34 0 0 0 {500 + RX} {RY}" fill="none" stroke="#7FDBFF" stroke-width="52" opacity="0.28"/>')
o.append(f'<path d="M {500 - RX + 30} {RY + 28} A {RX - 30} 22 0 0 0 {500 + RX - 30} {RY + 28}" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.45"/>')
o.append('</g>')

# signos de baja presión
o.append(f'<g id="menos" fill="none" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round">'
         f'<path d="M 478 {RY - 2} L 502 {RY - 2}"/><path d="M 508 {RY + 14} L 532 {RY + 14}"/><path d="M 456 {RY + 16} L 474 {RY + 16}"/></g>')

# ---- semilla (vista de lado, cayendo)
o.append('<g id="semilla">')
lines_p = pappus_lines(AX, AY, RP, n=72, theta=11, elev=17, seed=31, curl=0.18)
back, front = fil_svg(lines_p, w=2.6, edge=5.4, barbs=5, back_op=0.6, edgecol="#22384C")
o.append('<g id="vilano">' + back)
beak = f"M {AX} {AY} L {AX} {BEAK_END}"
o.append(f'<path d="{beak}" stroke="{INK}" stroke-width="12" stroke-linecap="round"/><path d="{beak}" stroke="#EDE4C4" stroke-width="6" stroke-linecap="round"/>')
o.append(achene(AX, BEAK_END - 3, 74, 24))
o.append(front + f'<circle cx="{AX}" cy="{AY}" r="5.5" fill="#F4EEDA" stroke="{INK}" stroke-width="3"/></g>')
o.append('</g>')

# flecha de freno (la baja presión tira del vilano hacia arriba = arrastre)
o.append(arrow("freno", 500, 410, 500, 336, CORAL, w=12, head=28))
# flecha de caída
o.append(arrow("cae", 700, 488, 700, 612, "#FFFFFF", w=10, head=26))
t, bc = tag("lcae", 790, 552, "CAE", bg="#FFFFFF", fg=INK); o.append(t)

t, b1 = tag("lanillo", 790, 140, "ANILLO DE AIRE", target=(500 + RX + 26, RY - 40), anchor_from=(760, 168)); o.append(t)
t, b2 = tag("lbaja", 790, 140, "BAJA PRESIÓN", target=(504, RY + 6), anchor_from=(740, 168))
t5, b5 = tag("lvel", 300, 560, "≈40 CM/S", bg="#FFFFFF", fg=INK); o.append(t5); o.append(t)
hx = min((p for z, p in lines_p if z >= 0), key=lambda p: p[-1][0])
mid = hx[2]
t, b3 = tag("lhuecos", 300, 560, "HUECOS", target=(mid[0] + 6, mid[1]), anchor_from=(320, 532)); o.append(t)
t, b4 = tag("lsep", 790, 400, "SEPARADO", bg="#FFFFFF", fg=INK, target=(600, 324), anchor_from=(700, 400)); o.append(t)
bx = [b1, b3, b4, bc, b5]
for i in range(len(bx)):
    for j in range(i + 1, len(bx)):
        if boxes_overlap(bx[i], bx[j]):
            print("SOLAPE", i, j, file=sys.stderr)
o.append('</svg>')
open(sys.argv[1], "w").write("\n".join(o))

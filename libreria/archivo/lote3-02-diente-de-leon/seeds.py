"""Piezas de diente de león: semilla con vilano en 3D proyectado."""
import math, random
from dl import *

FIL = "#FFFFFF"
FIL_EDGE = "#5E7086"


def pappus_lines(ax, ay, R, n=40, theta=14, elev=18, rot=0, seed=1, curl=0.18, jitter=True):
    """Filamentos del vilano visto de lado (con algo de elevación).
    ax, ay: ápice; theta: inclinación de los pelos sobre la horizontal; elev: elevación de la cámara;
    rot: giro de toda la semilla (grados, sentido horario en pantalla). Devuelve lista de (z, puntos)."""
    rnd = random.Random(seed)
    th, e = math.radians(theta), math.radians(elev)
    cr, sr = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    out = []
    for k in range(n):
        phi = 2 * math.pi * (k + (rnd.uniform(-0.3, 0.3) if jitter else 0)) / n
        L = R * (rnd.uniform(0.9, 1.04) if jitter else 1)
        pts_ = []
        for s in (0, 0.35, 0.7, 1.0):
            t = th + curl * s * s  # los pelos se curvan un poco hacia arriba en la punta
            X = math.cos(phi) * math.cos(t) * L * s
            Y = math.sin(t) * L * s
            Z = math.sin(phi) * math.cos(t) * L * s
            sx = X
            sy = -(Y * math.cos(e) - Z * math.sin(e))
            # giro en pantalla
            rx, ry = sx * cr - sy * sr, sx * sr + sy * cr
            pts_.append((ax + rx, ay + ry))
        out.append((math.sin(phi), pts_))
    return out


def fil_svg(lines, w=2.2, edge=4.6, back_op=0.75, col=FIL, edgecol=FIL_EDGE, barbs=0, rnd_seed=3):
    """Dibuja filamentos: los de detrás primero y más tenues. barbs = nº de pelillos laterales por filamento."""
    rnd = random.Random(rnd_seed)
    back = [p for z, p in lines if z < 0]
    front = [p for z, p in lines if z >= 0]

    def layer(group, op):
        d = " ".join(smooth(p) for p in group)
        s = (f'<path d="{d}" fill="none" stroke="{edgecol}" stroke-width="{edge}" stroke-linecap="round" opacity="{op * 0.85:.2f}"/>'
             f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" opacity="{op:.2f}"/>')
        if barbs:
            bd = []
            for p in group:
                (x0, y0), (x1, y1) = p[0], p[-1]
                L = math.hypot(x1 - x0, y1 - y0)
                if L < 20:
                    continue
                ux, uy = (x1 - x0) / L, (y1 - y0) / L
                for j in range(barbs):
                    s_ = 0.3 + 0.68 * (j + rnd.random() * 0.5) / barbs
                    # punto sobre la curva aproximado por el polígono
                    seg = s_ * (len(p) - 1)
                    i = min(int(seg), len(p) - 2)
                    fr = seg - i
                    px = p[i][0] + (p[i + 1][0] - p[i][0]) * fr
                    py = p[i][1] + (p[i + 1][1] - p[i][1]) * fr
                    side = 1 if j % 2 else -1
                    bl = 7 + 5 * s_
                    bx = px + (ux * 0.8 - uy * side * 0.6) * bl
                    by = py + (uy * 0.8 + ux * side * 0.6) * bl
                    bd.append(f"M {f(px)} {f(py)} L {f(bx)} {f(by)}")
            if bd:
                s += f'<path d="{" ".join(bd)}" fill="none" stroke="#E4F1FA" stroke-width="1.5" stroke-linecap="round" opacity="{op * 0.75:.2f}"/>'
        return s

    return layer(back, back_op), layer(front, 1.0)


def achene(x, y, L, W, rot=0, spines=True, sid=None):
    """Aquenio (semilla) con forma de huso, de (x,y) [arriba, donde nace el pico] hacia abajo L; giro rot."""
    o = []
    pts_r = []
    for i in range(0, 13):
        t = i / 12
        w = W / 2 * math.sin(math.pi * min(1, t * 1.05)) ** 0.8 * (1 - 0.35 * t)
        pts_r.append((w, t * L))
    outline = [(px, py) for px, py in pts_r] + [(-px, py) for px, py in reversed(pts_r)]
    g = f'<g transform="translate({f(x)} {f(y)}) rotate({f(rot)})">'
    g += f'<path d="{smooth(outline, True)}" fill="url(#achene)" stroke="{INK}" stroke-width="{max(2.5, W * 0.16):.1f}" stroke-linejoin="round"/>'
    # costillas
    rib = []
    for fr in (-0.45, 0, 0.45):
        rib.append("M " + " L ".join(f"{f(px * fr)} {f(py)}" for px, py in pts_r[1:-1]))
    g += f'<path d="{" ".join(rib)}" fill="none" stroke="#3B2A18" stroke-width="{max(1, W * 0.06):.1f}" opacity="0.5"/>'
    g += f'<path d="M {f(-W * 0.18)} {f(L * 0.15)} L {f(-W * 0.22)} {f(L * 0.6)}" stroke="#D9BC85" stroke-width="{max(1.2, W * 0.09):.1f}" stroke-linecap="round" opacity="0.8"/>'
    if spines:
        sp = []
        for i in range(1, 6):
            t = i / 12
            w = W / 2 * math.sin(math.pi * t * 1.05) ** 0.8 * (1 - 0.35 * t)
            for sgn in (-1, 1):
                sp.append(f"M {f(sgn * w * 0.95)} {f(t * L)} L {f(sgn * (w + W * 0.22))} {f(t * L - W * 0.3)}")
        g += f'<path d="{" ".join(sp)}" fill="none" stroke="{INK}" stroke-width="{max(1.5, W * 0.1):.1f}" stroke-linecap="round"/>'
    g += "</g>"
    return g


def side_seed(x, y, s=1.0, rot=0, n=36, theta=14, elev=20, seed=1, barbs=0, beak_col="#EDE6CC", fil_w=None):
    """Semilla entera vista de lado: ápice del vilano en (x,y), pico hacia abajo. Escala s, giro rot (grados)."""
    R = 58 * s
    lines = pappus_lines(x, y, R, n=n, theta=theta, elev=elev, rot=rot, seed=seed)
    w = fil_w or max(1.3, 1.6 * s)
    back, front = fil_svg(lines, w=w, edge=w + 2.4 * min(1.4, s ** 0.5), barbs=barbs)
    cr, sr = math.cos(math.radians(rot)), math.sin(math.radians(rot))

    def P(dx, dy):
        return (x + dx * cr - dy * sr, y + dx * sr + dy * cr)

    b0, b1 = P(0, 0), P(0, 62 * s)
    beak = f"M {f(b0[0])} {f(b0[1])} L {f(b1[0])} {f(b1[1])}"
    bw = max(1.6, 2.4 * s)
    o = back
    o += f'<path d="{beak}" stroke="{INK}" stroke-width="{bw + 2.6 * min(1.5, s):.1f}" stroke-linecap="round"/>'
    o += f'<path d="{beak}" stroke="{beak_col}" stroke-width="{bw:.1f}" stroke-linecap="round"/>'
    o += achene(b1[0], b1[1], 30 * s, 8.5 * s, rot=rot, spines=s > 0.7)
    o += front
    o += f'<circle cx="{f(x)}" cy="{f(y)}" r="{max(2, 2.6 * s):.1f}" fill="#F4EEDA" stroke="{INK}" stroke-width="{max(1.2, 1.4 * s):.1f}"/>'
    return o


DEFS_SEED = (lg("achene", [(0, "#B48A52"), (0.5, "#7A5A33"), (1, "#4A341C")], 0, 0, 1, 0))

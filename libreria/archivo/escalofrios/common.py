import math
INK = "#0B0B14"
LIME = "#C8FF2E"
CORAL = "#FF5A36"


def head(defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 700">\n<defs>\n{defs}\n</defs>\n')


def stroke2(d, w, col, ink_extra=7, cap="round", op=None, extra=""):
    o = f' opacity="{op}"' if op is not None else ""
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w+ink_extra}" stroke-linecap="{cap}" stroke-linejoin="round"{o}{extra}/>'
            f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="{cap}" stroke-linejoin="round"{o}{extra}/>')


def poly(pts):
    return "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)


def tag(id_, x, y, w, text, lx1=None, ly1=None, lx2=None, ly2=None, bg=INK, fg=LIME, h=58, fs=30):
    s = f'<g id="{id_}">'
    if lx1 is not None:
        s += (f'<line x1="{lx1}" y1="{ly1}" x2="{lx2}" y2="{ly2}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
              f'<circle cx="{lx2}" cy="{ly2}" r="9" fill="{LIME}" stroke="{INK}" stroke-width="4"/>')
    s += (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{bg}"/>'
          f'<text x="{x+w/2}" y="{y+h/2+fs*0.35:.0f}" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="{fs}" fill="{fg}">{text}</text></g>')
    return s


def tw(text, fs=30):
    """ancho aproximado de etiqueta (JetBrains Mono ~0.6em por carácter) + margen"""
    return int(len(text) * fs * 0.62 + 40)


def rot(p, c, deg):
    """rotación como CSS (grados positivos = horario en pantalla)"""
    a = math.radians(deg)
    x, y = p[0] - c[0], p[1] - c[1]
    return (c[0] + x * math.cos(a) - y * math.sin(a), c[1] + x * math.sin(a) + y * math.cos(a))


def arrow(id_, pts, col=LIME, w=12, head_len=34):
    """flecha con doble trazo; la punta se calcula con la dirección del último tramo"""
    d = poly(pts)
    (x0, y0), (x1, y1) = pts[-2], pts[-1]
    a = math.atan2(y1 - y0, x1 - x0)
    hl, hw = head_len, head_len * 0.75
    tip = (x1 + math.cos(a) * hl * 0.6, y1 + math.sin(a) * hl * 0.6)
    l = (x1 + math.cos(a + math.pi / 2) * hw / 1.4 - math.cos(a) * hl * 0.4, y1 + math.sin(a + math.pi / 2) * hw / 1.4 - math.sin(a) * hl * 0.4)
    r = (x1 + math.cos(a - math.pi / 2) * hw / 1.4 - math.cos(a) * hl * 0.4, y1 + math.sin(a - math.pi / 2) * hw / 1.4 - math.sin(a) * hl * 0.4)
    hd = poly([l, tip, r]) + " Z"
    return (f'<g id="{id_}">' + stroke2(d, w, col) +
            f'<path d="{hd}" fill="{col}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/></g>')


def f(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def smooth(p, closed=False, t=0.5):
    """Curva Catmull-Rom suave que pasa por los puntos p."""
    n = len(p)
    if n < 3:
        return poly(p)
    P = list(p)
    if closed:
        P = [p[-1]] + list(p) + [p[0], p[1]]
    else:
        P = [p[0]] + list(p) + [p[-1]]
    d = f"M {f(P[1][0])} {f(P[1][1])}"
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        c1 = (p1[0] + (p2[0] - p0[0]) * t / 3, p1[1] + (p2[1] - p0[1]) * t / 3)
        c2 = (p2[0] - (p3[0] - p1[0]) * t / 3, p2[1] - (p3[1] - p1[1]) * t / 3)
        d += f" C {f(c1[0])} {f(c1[1])}, {f(c2[0])} {f(c2[1])}, {f(p2[0])} {f(p2[1])}"
    if closed:
        d += " Z"
    return d


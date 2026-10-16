"""Utilidades comunes para dibujar los SVG (coordenadas calculadas)."""
import math

INK = "#0B0B14"
LIME = "#C8FF2E"
CORAL = "#FF5A36"


def f(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def pts_d(pts, close=False):
    d = "M " + " L ".join(f"{f(x)} {f(y)}" for x, y in pts)
    return d + (" Z" if close else "")


def dbl(d, w, col, ink_extra=7, cap="round", opacity=None, extra=""):
    """Trazo doble: tinta ancha debajo + color encima."""
    op = f' opacity="{opacity}"' if opacity is not None else ""
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w + ink_extra}" stroke-linecap="{cap}" stroke-linejoin="round"{op}{extra}/>'
            f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="{cap}" stroke-linejoin="round"{op}{extra}/>')


def text_w(text, size=30):
    return len(text) * size * 0.6 + 40


def label(id_, cx, cy, text, line_to=None, line_from=None, bg=INK, fg=LIME, size=30, dot=True):
    """Etiqueta centrada en (cx, cy) con línea guía opcional hasta line_to.
    La línea sale del borde de la caja más cercano (o de line_from)."""
    w = text_w(text, size)
    h = size * 1.93
    x, y = cx - w / 2, cy - h / 2
    o = [f'<g id="{id_}">']
    if line_to:
        tx, ty = line_to
        if line_from is None:
            # punto del borde de la caja en dirección al objetivo
            dx, dy = tx - cx, ty - cy
            sx = (w / 2) / abs(dx) if dx else 1e9
            sy = (h / 2) / abs(dy) if dy else 1e9
            s = min(sx, sy)
            line_from = (cx + dx * s, cy + dy * s)
        fx, fy = line_from
        o.append(f'<line x1="{f(fx)}" y1="{f(fy)}" x2="{f(tx)}" y2="{f(ty)}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>')
        if dot:
            o.append(f'<circle cx="{f(tx)}" cy="{f(ty)}" r="9" fill="{LIME}" stroke="{INK}" stroke-width="4"/>')
    o.append(f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="12" fill="{bg}" stroke="{INK}" stroke-width="4"/>')
    o.append(f'<text x="{f(cx)}" y="{f(cy + size * 0.36)}" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="{size}" fill="{fg}">{text}</text>')
    o.append('</g>')
    return "".join(o), (x, y, x + w, y + h)


def arrow(id_, x1, y1, x2, y2, col, w=10, head=30, ink=10, attrs=""):
    ang = math.atan2(y2 - y1, x2 - x1)
    p1 = (x2 - head * math.cos(ang - 0.5), y2 - head * math.sin(ang - 0.5))
    p2 = (x2 - head * math.cos(ang + 0.5), y2 - head * math.sin(ang + 0.5))
    shaft = f"M {f(x1)} {f(y1)} L {f(x2)} {f(y2)}"
    hd = f"M {f(p1[0])} {f(p1[1])} L {f(x2)} {f(y2)} L {f(p2[0])} {f(p2[1])}"
    inner = (f'<path d="{shaft}" fill="none" stroke="{INK}" stroke-width="{w + ink}" stroke-linecap="round"/>'
             f'<path d="{hd}" fill="none" stroke="{INK}" stroke-width="{w + ink}" stroke-linecap="round" stroke-linejoin="round"/>'
             f'<path d="{shaft}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>'
             f'<path d="{hd}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')
    if id_ is None:
        return inner
    return f'<g id="{id_}"{attrs}>{inner}</g>'


def curved_arrow(id_, d, end, prev, col, w=10, head=28):
    """Flecha con cuerpo curvo d; la punta se orienta de prev a end."""
    ang = math.atan2(end[1] - prev[1], end[0] - prev[0])
    x2, y2 = end
    p1 = (x2 - head * math.cos(ang - 0.5), y2 - head * math.sin(ang - 0.5))
    p2 = (x2 - head * math.cos(ang + 0.5), y2 - head * math.sin(ang + 0.5))
    hd = f"M {f(p1[0])} {f(p1[1])} L {f(x2)} {f(y2)} L {f(p2[0])} {f(p2[1])}"
    return (f'<g id="{id_}"><path d="{d}" fill="none" stroke="{INK}" stroke-width="{w + 10}" stroke-linecap="round"/>'
            f'<path d="{hd}" fill="none" stroke="{INK}" stroke-width="{w + 10}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>'
            f'<path d="{hd}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/></g>')


def rot(p, ang_deg, about=(0, 0)):
    a = math.radians(ang_deg)
    x, y = p[0] - about[0], p[1] - about[1]
    return (about[0] + x * math.cos(a) - y * math.sin(a), about[1] + x * math.sin(a) + y * math.cos(a))


def xf(p, tx, ty, ang, s=1.0):
    """Transforma un punto local: escala s, gira ang (grados), traslada (tx, ty). Igual que transform="translate rotate scale"."""
    x, y = p[0] * s, p[1] * s
    x, y = rot((x, y), ang)
    return (x + tx, y + ty)


def qbez(p0, c, p1, t):
    return ((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * c[0] + t * t * p1[0],
            (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * c[1] + t * t * p1[1])


def cbez(p0, c1, c2, p1, t):
    u = 1 - t
    return (u ** 3 * p0[0] + 3 * u * u * t * c1[0] + 3 * u * t * t * c2[0] + t ** 3 * p1[0],
            u ** 3 * p0[1] + 3 * u * u * t * c1[1] + 3 * u * t * t * c2[1] + t ** 3 * p1[1])


def y_at_x(curve, x, n=400):
    """curve(t)->(x,y); devuelve y para la x dada (búsqueda)."""
    best = min((abs(curve(i / n)[0] - x), curve(i / n)[1]) for i in range(n + 1))
    return best[1]


def svg_open(defs):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 700">\n<defs>\n{defs}\n</defs>'


def overlap(a, b, pad=0):
    return not (a[2] + pad <= b[0] or b[2] + pad <= a[0] or a[3] + pad <= b[1] or b[3] + pad <= a[1])


def dash_d(pts, dash, gap):
    """Trazo discontinuo como subtrazos sueltos (el motor añade pathLength=1, así que no vale stroke-dasharray)."""
    out, on, left = [], True, dash
    cur = [pts[0]]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        seg = math.hypot(x1 - x0, y1 - y0)
        pos = 0.0
        while seg - pos > left:
            pos += left
            t = pos / seg
            p = (x0 + (x1 - x0) * t, y0 + (y1 - y0) * t)
            if on:
                cur.append(p); out.append(cur)
            else:
                cur = [p]
            on = not on
            left = dash if on else gap
        left -= seg - pos
        if on:
            cur.append((x1, y1))
    if on and len(cur) > 1:
        out.append(cur)
    return " ".join(pts_d(c) for c in out if len(c) > 1)


def sample(fn, n=60):
    return [fn(i / n) for i in range(n + 1)]

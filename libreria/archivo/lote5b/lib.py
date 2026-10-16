"""Utilidades comunes para dibujar los SVG (estilo pegatina realista)."""
import math

INK = "#0B0B14"
LIME = "#C8FF2E"
CORAL = "#FF5A36"


def f(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def pts(p):
    return " ".join(f"{f(x)} {f(y)}" for x, y in p)


def poly(p, closed=False):
    d = "M " + " L ".join(f"{f(x)} {f(y)}" for x, y in p)
    return d + (" Z" if closed else "")


def smooth(p, closed=False, t=0.5):
    """Curva Catmull-Rom suave que pasa por los puntos p."""
    n = len(p)
    if n < 3:
        return poly(p, closed)
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


def dbl(d, w, col, ink_extra=7, cap="round", extra=""):
    """Trazo doble: tinta ancha debajo y color encima."""
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w + ink_extra}" stroke-linecap="{cap}" stroke-linejoin="round"{extra}/>'
            f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="{cap}" stroke-linejoin="round"{extra}/>')


def text_w(text, size=30):
    return int(len(text) * size * 0.6 + 44)


def tag(id_, cx, cy, text, target=None, bg=INK, fg=LIME, size=30, anchor_from=None, dot=True):
    """Etiqueta centrada en (cx, cy) con línea guía hasta target. Devuelve (svg, caja)."""
    w = text_w(text, size)
    h = 58 if size >= 28 else 48
    x, y = cx - w / 2, cy - h / 2
    s = f'<g id="{id_}">'
    if target:
        sx, sy = anchor_from or (cx, cy)
        s += (f'<line x1="{f(sx)}" y1="{f(sy)}" x2="{f(target[0])}" y2="{f(target[1])}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>')
        if dot:
            s += f'<circle cx="{f(target[0])}" cy="{f(target[1])}" r="9" fill="{LIME}" stroke="{INK}" stroke-width="4"/>'
    s += (f'<rect x="{f(x)}" y="{f(y)}" width="{w}" height="{h}" rx="12" fill="{bg}" stroke="{INK}" stroke-width="3"/>'
          f'<text x="{f(cx)}" y="{f(cy + size * 0.36)}" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="{size}" fill="{fg}">{text}</text></g>')
    return s, (x, y, x + w, y + h)


def arrow(id_, x1, y1, x2, y2, col, w=10, head=30, curve=None):
    """Flecha con contorno. curve=(cx,cy) para una flecha curva (cuadrática)."""
    if curve:
        d = f"M {f(x1)} {f(y1)} Q {f(curve[0])} {f(curve[1])} {f(x2)} {f(y2)}"
        ang = math.atan2(y2 - curve[1], x2 - curve[0])
    else:
        d = f"M {f(x1)} {f(y1)} L {f(x2)} {f(y2)}"
        ang = math.atan2(y2 - y1, x2 - x1)
    p1 = (x2 - head * math.cos(ang - 0.5), y2 - head * math.sin(ang - 0.5))
    p2 = (x2 - head * math.cos(ang + 0.5), y2 - head * math.sin(ang + 0.5))
    hd = f"M {f(p1[0])} {f(p1[1])} L {f(x2)} {f(y2)} L {f(p2[0])} {f(p2[1])}"
    s = f'<g id="{id_}">' if id_ else "<g>"
    s += dbl(d, w, col, w) + dbl(hd, w, col, w)
    return s + "</g>"


def header(defs, w=1000, h=700):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">\n<defs>\n{defs}\n</defs>'


def lg(id_, stops, x1=0, y1=0, x2=0, y2=1):
    s = f'<linearGradient id="{id_}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">'
    for o, c, *op in stops:
        s += f'<stop offset="{o}" stop-color="{c}"' + (f' stop-opacity="{op[0]}"' if op else "") + "/>"
    return s + "</linearGradient>"


def rg(id_, stops, cx=0.5, cy=0.5, r=0.5, fx=None, fy=None):
    s = f'<radialGradient id="{id_}" cx="{cx}" cy="{cy}" r="{r}"' + (f' fx="{fx}" fy="{fy}"' if fx is not None else "") + ">"
    for o, c, *op in stops:
        s += f'<stop offset="{o}" stop-color="{c}"' + (f' stop-opacity="{op[0]}"' if op else "") + "/>"
    return s + "</radialGradient>"


def boxes_overlap(a, b, pad=6):
    return not (a[2] + pad < b[0] or b[2] + pad < a[0] or a[3] + pad < b[1] or b[3] + pad < a[1])

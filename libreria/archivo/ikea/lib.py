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
          f'<text x="{f(cx)}" y="{f(cy + size * 0.36)}" text-anchor="middle" font-family="JetBrains Mono, DejaVu Sans Mono, monospace" font-weight="800" font-size="{size}" fill="{fg}">{text}</text></g>')
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

FONT = "JetBrains Mono, DejaVu Sans Mono, monospace"


def txt(x, y, s, size=30, fill=INK, anchor="middle", weight=800, extra=""):
    return f'<text x="{f(x)}" y="{f(y)}" text-anchor="{anchor}" font-family="{FONT}" font-weight="{weight}" font-size="{size}" fill="{fill}" {extra}>{s}</text>'


WOOD_DEFS = (lg("wfront", [(0, "#F4DDB8"), (0.55, "#E2BE8A"), (1, "#C99A63")]) +
             lg("wside", [(0, "#D5AE7A"), (1, "#A9794A")]) +
             lg("winner", [(0, "#8E643C"), (1, "#C49866")]) +
             lg("wtop", [(0, "#FBEBD0"), (1, "#EBCB9C")]))


def storage_box(x0, yb, w=250, h=190, dx=46, dy=-38, screws=True, grain_seed=0):
    """Caja de almacenaje abierta de contrachapado (abedul). Cara frontal de (x0,yb-h) a (x0+w,yb)."""
    yt = yb - h
    o = []
    # sombra
    o.append(f'<ellipse cx="{f(x0 + w / 2 + dx / 2)}" cy="{f(yb + 2)}" rx="{f(w / 2 + 40)}" ry="16" fill="#3A2A1A" opacity="0.22"/>')
    # cara lateral derecha
    side = [(x0 + w, yt), (x0 + w + dx, yt + dy), (x0 + w + dx, yb + dy), (x0 + w, yb)]
    o.append(f'<path d="{poly(side, True)}" fill="url(#wside)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
    # boca (interior)
    rim = [(x0, yt), (x0 + dx, yt + dy), (x0 + w + dx, yt + dy), (x0 + w, yt)]
    o.append(f'<path d="{poly(rim, True)}" fill="url(#winner)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
    # pared interior trasera (más clara arriba) y grosor del canto
    th = 9
    inner = [(x0 + th + 4, yt - 3), (x0 + dx + th, yt + dy + th * 0.6), (x0 + w + dx - th, yt + dy + th * 0.6), (x0 + w - th + 4, yt - 3)]
    o.append(f'<path d="{poly([(x0 + dx + th, yt + dy + th * 0.6), (x0 + w + dx - th, yt + dy + th * 0.6), (x0 + w + dx - th, yt + dy + 34), (x0 + dx + th, yt + dy + 34)], True)}" fill="#D9B482" opacity="0.9"/>')
    o.append(f'<path d="{poly(inner, True)}" fill="none" stroke="{INK}" stroke-width="3" stroke-linejoin="round" opacity="0.8"/>')
    # cara frontal
    o.append(f'<rect x="{f(x0)}" y="{f(yt)}" width="{f(w)}" height="{f(h)}" fill="url(#wfront)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
    # vetas
    import random
    random.seed(grain_seed + 7)
    for k in range(5):
        yy = yt + 30 + k * (h - 50) / 4 + random.uniform(-6, 6)
        a = random.uniform(-8, 8)
        o.append(f'<path d="M {f(x0 + 14)} {f(yy)} C {f(x0 + w * 0.3)} {f(yy + a)}, {f(x0 + w * 0.6)} {f(yy - a)}, {f(x0 + w - 14)} {f(yy + a / 2)}" fill="none" stroke="#B88A55" stroke-width="2.5" opacity="0.45"/>')
    o.append(f'<ellipse cx="{f(x0 + w * 0.72)}" cy="{f(yt + h * 0.7)}" rx="14" ry="6" fill="none" stroke="#B88A55" stroke-width="2.5" opacity="0.45"/>')
    # canto superior iluminado
    o.append(f'<path d="M {f(x0 + 8)} {f(yt + 7)} L {f(x0 + w - 8)} {f(yt + 7)}" stroke="#FFF6E4" stroke-width="5" stroke-linecap="round" opacity="0.9"/>')
    # asa
    hx, hy, hw, hh = x0 + w / 2 - 42, yt + 34, 84, 26
    o.append(f'<rect x="{f(hx)}" y="{f(hy)}" width="{hw}" height="{hh}" rx="13" fill="#5A3C20" stroke="{INK}" stroke-width="5"/>')
    o.append(f'<path d="M {f(hx + 12)} {f(hy + hh - 6)} L {f(hx + hw - 12)} {f(hy + hh - 6)}" stroke="#9C7448" stroke-width="3" stroke-linecap="round"/>')
    if screws:
        for sx, sy in ((x0 + 16, yt + 18), (x0 + w - 16, yt + 18), (x0 + 16, yb - 16), (x0 + w - 16, yb - 16)):
            o.append(f'<circle cx="{f(sx)}" cy="{f(sy)}" r="6.5" fill="#9AA3AD" stroke="{INK}" stroke-width="3"/><path d="M {f(sx - 3.5)} {f(sy - 3.5)} L {f(sx + 3.5)} {f(sy + 3.5)}" stroke="{INK}" stroke-width="2"/>')
    # canto lateral iluminado
    o.append(f'<path d="M {f(x0 + w + 6)} {f(yt + 2)} L {f(x0 + w + dx - 4)} {f(yt + dy + 6)}" stroke="#FFF1D6" stroke-width="3.5" stroke-linecap="round" opacity="0.8"/>')
    return "".join(o)


def price_tag(cx, cy, text, ang=0, w=210, h=86, size=42, col="#FFF8E8"):
    """Etiqueta de precio de papel con agujero a la izquierda. Devuelve svg (grupo interno rotado) y punto del agujero."""
    import math
    x, y = -w / 2, -h / 2
    shape = f"M {f(x + 34)} {f(y)} L {f(x + w)} {f(y)} L {f(x + w)} {f(y + h)} L {f(x + 34)} {f(y + h)} L {f(x)} 0 Z"
    s = f'<g transform="translate({f(cx)} {f(cy)}) rotate({ang})">'
    s += f'<path d="{shape}" fill="#000" opacity="0.18" transform="translate(6 7)"/>'
    s += f'<path d="{shape}" fill="{col}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
    s += f'<path d="M {f(x + 40)} {f(y + 9)} L {f(x + w - 10)} {f(y + 9)}" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>'
    s += f'<circle cx="{f(x + 26)}" cy="0" r="8" fill="#2347FF" stroke="{INK}" stroke-width="4"/>'
    s += txt(x + 34 + (w - 34) / 2, size * 0.36, text, size)
    s += "</g>"
    a = math.radians(ang)
    hx = cx + (x + 26) * math.cos(a)
    hy = cy + (x + 26) * math.sin(a)
    return s, (hx, hy)


def star(cx, cy, r1, r2, n=16, rot=0):
    import math
    p = []
    for k in range(2 * n):
        r = r1 if k % 2 == 0 else r2
        a = math.pi * k / n + math.radians(rot)
        p.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return poly(p, True)


def heart(cx, cy, s=1.0, col="#FF5A36", hi="#FF9C80"):
    d = (f"M {f(cx)} {f(cy + 30 * s)} C {f(cx - 46 * s)} {f(cy)}, {f(cx - 40 * s)} {f(cy - 34 * s)}, {f(cx - 18 * s)} {f(cy - 34 * s)} "
         f"C {f(cx - 6 * s)} {f(cy - 34 * s)}, {f(cx)} {f(cy - 24 * s)}, {f(cx)} {f(cy - 18 * s)} "
         f"C {f(cx)} {f(cy - 24 * s)}, {f(cx + 6 * s)} {f(cy - 34 * s)}, {f(cx + 18 * s)} {f(cy - 34 * s)} "
         f"C {f(cx + 40 * s)} {f(cy - 34 * s)}, {f(cx + 46 * s)} {f(cy)}, {f(cx)} {f(cy + 30 * s)} Z")
    return (f'<path d="{d}" fill="{col}" stroke="{INK}" stroke-width="{f(max(4, 6 * s))}" stroke-linejoin="round"/>'
            f'<path d="M {f(cx - 28 * s)} {f(cy - 14 * s)} Q {f(cx - 26 * s)} {f(cy - 26 * s)} {f(cx - 14 * s)} {f(cy - 27 * s)}" fill="none" stroke="{hi}" stroke-width="{f(5 * s)}" stroke-linecap="round"/>')


def allen_key(x, y, s=1.0, ang=0):
    """Llave Allen en L (hexagonal), esquina en (x,y)."""
    d = f"M {f(-70 * s)} 0 L 0 0 L 0 {f(-30 * s)}"
    return (f'<g transform="translate({f(x)} {f(y)}) rotate({ang})">'
            f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{f(16 * s)}" stroke-linejoin="round" stroke-linecap="butt"/>'
            f'<path d="{d}" fill="none" stroke="#5E6670" stroke-width="{f(9 * s)}" stroke-linejoin="round"/>'
            f'<path d="M {f(-64 * s)} {f(-2 * s)} L {f(-4 * s)} {f(-2 * s)}" stroke="#B9C2CC" stroke-width="{f(3 * s)}" stroke-linecap="round"/></g>')


def screw(x, y, s=1.0, ang=0):
    return (f'<g transform="translate({f(x)} {f(y)}) rotate({ang}) scale({s})">'
            f'<path d="M 0 -6 L 34 -4 L 40 0 L 34 4 L 0 6 Z" fill="#AAB3BD" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>'
            f'<path d="M 8 -5 L 11 5 M 16 -5 L 19 5 M 24 -4.5 L 27 4.5" stroke="{INK}" stroke-width="2"/>'
            f'<rect x="-8" y="-11" width="9" height="22" rx="3" fill="#C7CFD8" stroke="{INK}" stroke-width="3.5"/>'
            f'<path d="M -5 -7 L -5 7" stroke="#FFFFFF" stroke-width="2" opacity="0.8"/></g>')

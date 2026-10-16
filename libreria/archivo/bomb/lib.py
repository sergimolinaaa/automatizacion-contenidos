import math
INK = "#0B0B14"
LIME = "#C8FF2E"
CORAL = "#FF5A36"


def P(pts):
    return "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)


def stroke2(d, w, col, ink=INK, extra=7, cap="round", opacity=None, cls=""):
    op = f' opacity="{opacity}"' if opacity is not None else ""
    return (f'<path d="{d}" fill="none" stroke="{ink}" stroke-width="{w+extra}" stroke-linecap="{cap}" stroke-linejoin="round"{op}/>'
            f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="{cap}" stroke-linejoin="round"{op}/>')


def text_w(text, size=30):
    return len(text) * size * 0.6 + 40


def tag(id_, cx, cy, text, bg=INK, fg=LIME, size=30, leader=None, dot=True, lcol=None):
    """Etiqueta centrada en (cx, cy). leader = (x, y) punto señalado."""
    w = text_w(text, size)
    h = size * 1.9
    x, y = cx - w / 2, cy - h / 2
    o = [f'<g id="{id_}">']
    if leader:
        lx, ly = leader
        # sale del borde de la etiqueta más cercano
        sx = min(max(lx, x + 14), x + w - 14)
        sy = y + h if ly > cy else y
        if abs(ly - cy) < h / 2:
            sy = cy
            sx = x + w if lx > cx else x
        lc = lcol or INK
        o.append(f'<path d="M {sx:.1f} {sy:.1f} L {lx:.1f} {ly:.1f}" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>')
        o.append(f'<path d="M {sx:.1f} {sy:.1f} L {lx:.1f} {ly:.1f}" stroke="{lc if lcol else LIME}" stroke-width="4" stroke-linecap="round"/>')
        if dot:
            o.append(f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="9" fill="{LIME}" stroke="{INK}" stroke-width="4.5"/>')
    o.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="12" fill="{bg}" stroke="{INK}" stroke-width="4"/>')
    o.append(f'<text x="{cx:.1f}" y="{cy + size * 0.36:.1f}" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="{size}" fill="{fg}">{text}</text>')
    o.append('</g>')
    return "".join(o)


def arrow(id_, pts, col=LIME, w=10, head=28, curve=False):
    """Flecha por puntos (polilínea o curva Q si 3 puntos y curve)."""
    if curve and len(pts) == 3:
        (x0, y0), (cx, cy), (x1, y1) = pts
        d = f"M {x0:.1f} {y0:.1f} Q {cx:.1f} {cy:.1f} {x1:.1f} {y1:.1f}"
        ax, ay = cx, cy
    else:
        d = P(pts)
        ax, ay = pts[-2]
        x1, y1 = pts[-1]
    ang = math.atan2(y1 - ay, x1 - ax)
    p1 = (x1 - head * math.cos(ang - 0.5), y1 - head * math.sin(ang - 0.5))
    p2 = (x1 - head * math.cos(ang + 0.5), y1 - head * math.sin(ang + 0.5))
    hd = f"M {p1[0]:.1f} {p1[1]:.1f} L {x1:.1f} {y1:.1f} L {p2[0]:.1f} {p2[1]:.1f}"
    return (f'<g id="{id_}">' + stroke2(d, w, col, extra=10) + stroke2(hd, w, col, extra=10) + '</g>')


def rot(x, y, cx, cy, deg):
    a = math.radians(deg)
    dx, dy = x - cx, y - cy
    return (cx + dx * math.cos(a) - dy * math.sin(a), cy + dx * math.sin(a) + dy * math.cos(a))


def svg_open(defs=""):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 700">\n<defs>{defs}</defs>\n'

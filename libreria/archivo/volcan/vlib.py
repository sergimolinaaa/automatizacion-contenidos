import math
INK = "#0B0B14"
LIME = "#C8FF2E"
CORAL = "#FF5A36"


def head(defs=""):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 700">\n<defs>\n{defs}\n</defs>\n'


def _stops(stops):
    out = ""
    for st in stops:
        o, c = st[0], st[1]
        op = st[2] if len(st) > 2 else None
        out += f'<stop offset="{o}" stop-color="{c}"' + (f' stop-opacity="{op}"' if op is not None else "") + '/>'
    return out


def lg(id_, stops, x1=0, y1=0, x2=0, y2=1):
    return f'<linearGradient id="{id_}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">{_stops(stops)}</linearGradient>'


def rg(id_, stops, cx=0.5, cy=0.5, r=0.5):
    return f'<radialGradient id="{id_}" cx="{cx}" cy="{cy}" r="{r}">{_stops(stops)}</radialGradient>'


def tw(text, size=30):
    return len(text) * size * 0.6 + 44


def tag(id_, x, y, text, bg=INK, fg=LIME, w=None, h=58, size=30, anchor="left"):
    w = w or tw(text, size)
    if anchor == "center":
        x = x - w / 2
    stroke = f' stroke="{INK}" stroke-width="5"' if bg != INK else ""
    return (f'<g id="{id_}"><rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h}" rx="12" fill="{bg}"{stroke}/>'
            f'<text x="{x + w / 2:.1f}" y="{y + h / 2 + size * 0.36:.1f}" text-anchor="middle" font-family="JetBrains Mono" '
            f'font-weight="800" font-size="{size}" fill="{fg}">{text}</text></g>'), (x, y, w, h)


def leader(x1, y1, x2, y2, dot=True):
    s = f'<path d="M {x1:.1f} {y1:.1f} L {x2:.1f} {y2:.1f}" stroke="{INK}" stroke-width="5" stroke-linecap="round" fill="none"/>'
    if dot:
        s += f'<circle cx="{x2:.1f}" cy="{y2:.1f}" r="9" fill="{LIME}" stroke="{INK}" stroke-width="4"/>'
    return s


def label(id_, x, y, text, tx, ty, bg=INK, fg=LIME, anchor="left", w=None, size=30):
    t, (rx, ry, rw, rh) = tag("__", x, y, text, bg, fg, w=w, anchor=anchor, size=size)
    cx = min(max(tx, rx + 14), rx + rw - 14)
    cy = ry if ty < ry else ry + rh
    if ry <= ty <= ry + rh:
        cx = rx if tx < rx else rx + rw
        cy = ry + rh / 2
    inner = t.replace('<g id="__">', '').replace('</g>', '')
    return f'<g id="{id_}">{leader(cx, cy, tx, ty)}{inner}</g>'


def arrow(id_, x1, y1, x2, y2, col=CORAL, w=10, head=30, curve=None):
    if curve:
        cx, cy = curve
        d = f"M {x1:.1f} {y1:.1f} Q {cx:.1f} {cy:.1f} {x2:.1f} {y2:.1f}"
        ang = math.atan2(y2 - cy, x2 - cx)
    else:
        d = f"M {x1:.1f} {y1:.1f} L {x2:.1f} {y2:.1f}"
        ang = math.atan2(y2 - y1, x2 - x1)
    p1 = (x2 - head * math.cos(ang - 0.5), y2 - head * math.sin(ang - 0.5))
    p2 = (x2 - head * math.cos(ang + 0.5), y2 - head * math.sin(ang + 0.5))
    hd = f"M {p1[0]:.1f} {p1[1]:.1f} L {x2:.1f} {y2:.1f} L {p2[0]:.1f} {p2[1]:.1f}"
    o = (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w + 10}" stroke-linecap="round"/>'
         f'<path d="{hd}" fill="none" stroke="{INK}" stroke-width="{w + 10}" stroke-linecap="round" stroke-linejoin="round"/>'
         f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>'
         f'<path d="{hd}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')
    return f'<g id="{id_}">{o}</g>' if id_ else o


def bubble(x, y, r, fill="url(#bub)", sw=None):
    sw = sw or max(2.5, min(5, r * 0.28))
    s = f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}" stroke="{INK}" stroke-width="{sw:.1f}"/>'
    if r > 5:
        s += f'<circle cx="{x - r * 0.35:.1f}" cy="{y - r * 0.35:.1f}" r="{r * 0.25:.1f}" fill="#FFFFFF" opacity="0.85"/>'
    return s


def smooth(points, closed=False):
    P = list(points)
    n = len(P)
    P = ([P[-1]] + P + [P[0], P[1]]) if closed else ([P[0]] + P + [P[-1]])
    d = f"M {P[1][0]:.1f} {P[1][1]:.1f}"
    for i in (range(1, n + 1) if closed else range(1, n)):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C {c1[0]:.1f} {c1[1]:.1f}, {c2[0]:.1f} {c2[1]:.1f}, {p2[0]:.1f} {p2[1]:.1f}"
    return d + (" Z" if closed else "")

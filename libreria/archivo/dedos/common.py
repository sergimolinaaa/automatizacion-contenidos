import math
INK = "#0B0B14"
LIME = "#C8FF2E"
CORAL = "#FF5A36"
FONT = 'font-family="JetBrains Mono" font-weight="800"'


def tw(text, fs=30):
    return int(len(text) * fs * 0.62 + 40)


def tag(id_, x, y, text, lead=None, bg=INK, fg=LIME, w=None, fs=30):
    """Etiqueta: rect (x,y) arriba-izquierda. lead=(x1,y1,x2,y2) linea guia con punto en (x2,y2)."""
    w = w or tw(text, fs)
    h = 58
    s = [f'<g id="{id_}">']
    if lead:
        x1, y1, x2, y2 = lead
        s.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>')
        s.append(f'<circle cx="{x2}" cy="{y2}" r="9" fill="{LIME}" stroke="{INK}" stroke-width="4"/>')
    st = f' stroke="{INK}" stroke-width="4"' if bg != INK else ''
    s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{bg}"{st}/>')
    s.append(f'<text x="{x + w / 2:.0f}" y="{y + 40}" text-anchor="middle" {FONT} font-size="{fs}" fill="{fg}">{text}</text></g>')
    return "".join(s)


def arrow(id_, pts, col, w=10, head=30, curve=False):
    """Flecha con contorno siguiendo una polilinea (o curva cuadratica si curve y 3 puntos)."""
    if curve and len(pts) == 3:
        d = f"M {pts[0][0]} {pts[0][1]} Q {pts[1][0]} {pts[1][1]} {pts[2][0]} {pts[2][1]}"
        (ax, ay), (bx, by) = pts[1], pts[2]
    else:
        d = "M " + " L ".join(f"{x} {y}" for x, y in pts)
        (ax, ay), (bx, by) = pts[-2], pts[-1]
    ang = math.atan2(by - ay, bx - ax)
    p1 = (bx - head * math.cos(ang - 0.5), by - head * math.sin(ang - 0.5))
    p2 = (bx - head * math.cos(ang + 0.5), by - head * math.sin(ang + 0.5))
    hd = f"M {p1[0]:.1f} {p1[1]:.1f} L {bx} {by} L {p2[0]:.1f} {p2[1]:.1f}"
    return (f'<g id="{id_}"><path d="{d}" fill="none" stroke="{INK}" stroke-width="{w + 10}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{hd}" fill="none" stroke="{INK}" stroke-width="{w + 10}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{hd}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/></g>')


def dbl(d, w, col, extra=7, cap="round", op=None):
    o = f' opacity="{op}"' if op else ''
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w + extra}" stroke-linecap="{cap}" stroke-linejoin="round"{o}/>'
            f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="{cap}" stroke-linejoin="round"{o}/>')


def wavy(x0, y0, x1, y1, amp=4, n=3, steps=24):
    """Linea ondulada entre dos puntos."""
    L = math.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    nx, ny = -uy, ux
    pts = []
    for i in range(steps + 1):
        t = i / steps
        a = amp * math.sin(t * n * 2 * math.pi)
        pts.append((x0 + ux * L * t + nx * a, y0 + uy * L * t + ny * a))
    return "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)


def rot(x, y, ang, cx=0, cy=0):
    a = math.radians(ang)
    return (cx + (x * math.cos(a) - y * math.sin(a)), cy + (x * math.sin(a) + y * math.cos(a)))

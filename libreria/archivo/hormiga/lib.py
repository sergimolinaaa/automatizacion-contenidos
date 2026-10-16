import math, random
INK = "#0B0B14"
LIME = "#C8FF2E"
CORAL = "#FF5A36"
FONT = "JetBrains Mono, DejaVu Sans Mono, monospace"


def P(pts):
    return "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)


def leg(pts, w=8, col="#3A2418", ink=7, smooth=False):
    """Trazo fino con contorno: tinta ancha debajo y color encima."""
    d = P(pts)
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w + ink}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')


def dstroke(d, w=8, col="#3A2418", ink=7, extra=""):
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w + ink}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'
            f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" {extra}/>')


def text_w(text, size=30):
    return len(text) * size * 0.62 + 40


def tag(id_, cx, cy, text, lx=None, ly=None, bg=INK, fg=LIME, size=30, dot=True, w=None):
    """Etiqueta centrada en (cx, cy) con línea guía hasta (lx, ly)."""
    w = w or text_w(text, size)
    h = size + 28
    x, y = cx - w / 2, cy - h / 2
    s = f'<g id="{id_}">'
    if lx is not None:
        # la línea sale del borde de la etiqueta más cercano
        sx = min(max(lx, x + 14), x + w - 14)
        sy = y + h if ly > y + h else (y if ly < y else cy)
        if y <= ly <= y + h:
            sx = x if lx < x else x + w
        s += f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{lx:.1f}" y2="{ly:.1f}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
        if dot:
            s += f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="9" fill="{LIME}" stroke="{INK}" stroke-width="4"/>'
    s += (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h}" rx="12" fill="{bg}"/>'
          f'<text x="{cx:.1f}" y="{cy + size * 0.36:.1f}" text-anchor="middle" font-family="{FONT}" font-weight="800" font-size="{size}" fill="{fg}">{text}</text></g>')
    return s


def arrow(id_, pts, col=LIME, w=10, head=26, ink=7):
    """Flecha gruesa con contorno a lo largo de pts (polilínea); punta en el último punto."""
    (x1, y1), (x2, y2) = pts[-2], pts[-1]
    a = math.atan2(y2 - y1, x2 - x1)
    bx, by = x2 - head * 0.8 * math.cos(a), y2 - head * 0.8 * math.sin(a)
    body = pts[:-1] + [(bx, by)]
    hx1, hy1 = x2 - head * math.cos(a) + head * 0.62 * math.sin(a), y2 - head * math.sin(a) - head * 0.62 * math.cos(a)
    hx2, hy2 = x2 - head * math.cos(a) - head * 0.62 * math.sin(a), y2 - head * math.sin(a) + head * 0.62 * math.cos(a)
    tri = f"M {x2:.1f} {y2:.1f} L {hx1:.1f} {hy1:.1f} L {hx2:.1f} {hy2:.1f} Z"
    return (f'<g id="{id_}">' + leg(body, w, col, ink) +
            f'<path d="{tri}" fill="{col}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/></g>')


def inpoly(x, y, poly):
    c = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1 + 1e-9) + x1:
            c = not c
    return c


def grains(poly, n, cols, rmin=2, rmax=5, seed=1, avoid=None, op=1.0):
    random.seed(seed)
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    out = []
    k = 0
    while k < n:
        x = random.uniform(min(xs), max(xs))
        y = random.uniform(min(ys), max(ys))
        if not inpoly(x, y, poly):
            continue
        if avoid and any((x - ax) ** 2 / rx ** 2 + (y - ay) ** 2 / ry ** 2 < 1 for ax, ay, rx, ry in avoid):
            continue
        r = random.uniform(rmin, rmax)
        c = random.choice(cols)
        rot = random.uniform(0, 180)
        out.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{r:.1f}" ry="{r * 0.72:.1f}" fill="{c}" transform="rotate({rot:.0f} {x:.1f} {y:.1f})"/>')
        k += 1
    return f'<g opacity="{op}">' + "".join(out) + "</g>"


ANT_DEFS = '''<linearGradient id="antb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8A4A30"/><stop offset="0.45" stop-color="#4A2318"/><stop offset="1" stop-color="#1A0B07"/></linearGradient>
<radialGradient id="antg" cx="0.4" cy="0.3" r="0.8"><stop offset="0" stop-color="#7A3E28"/><stop offset="0.6" stop-color="#3A1A10"/><stop offset="1" stop-color="#140806"/></radialGradient>'''


def ant(legs="walk", husk=False):
    """Hormiga mirando a la izquierda; suelo en y=0, origen bajo el tórax. Largo ~150."""
    far, near = ("#B9A58C", "#D8C8B0") if husk else ("#5A3426", "#2A140C")
    body = "#E6D7BF" if husk else "url(#antb)"
    gas = "#E6D7BF" if husk else "url(#antg)"
    o = []
    # patas: (inicio en el tórax, rodilla, pie)
    if legs == "walk":
        L = [((-20, -27), (-44, -30), (-62, 0)), ((-6, -26), (16, -30), (14, 0)), ((8, -27), (42, -32), (70, 0))]
        F = [((-18, -29), (-36, -36), (-48, -2)), ((-4, -28), (22, -36), (30, -2)), ((10, -29), (52, -36), (88, -2))]
    else:  # resbalando: patas abiertas, pies arañando
        L = [((-20, -27), (-48, -38), (-74, -8)), ((-6, -26), (6, -10), (-14, 4)), ((8, -27), (44, -22), (82, 6))]
        F = [((-18, -29), (-40, -50), (-64, -30)), ((-4, -28), (24, -40), (34, -6)), ((10, -29), (56, -40), (98, -10))]
    for a, k, f in F:
        o.append(leg([a, k, f], 3.5, far, 5))
    # antena lejana
    o.append(leg([(-58, -50), (-62, -74), (-90, -78)], 3, far, 5))
    # gáster
    o.append(f'<ellipse cx="54" cy="-40" rx="30" ry="22" fill="{gas}" stroke="{INK}" stroke-width="6" transform="rotate(-12 54 -40)"/>')
    if not husk:
        o.append(f'<path d="M 34 -54 Q 52 -64 72 -56" fill="none" stroke="#C07A5A" stroke-width="4" stroke-linecap="round" opacity="0.8"/>')
    o.append(f'<g stroke="{INK}" stroke-width="2.5" opacity="0.45" fill="none"><path d="M 44 -61 Q 40 -40 46 -20"/><path d="M 60 -61 Q 56 -40 62 -20"/></g>')
    # pecíolo (nodo)
    o.append(f'<ellipse cx="22" cy="-38" rx="7" ry="10" fill="{body}" stroke="{INK}" stroke-width="5"/>')
    # mesosoma
    o.append(f'<path d="M -32 -36 C -28 -50, -10 -52, 0 -46 C 8 -42, 16 -40, 16 -33 C 8 -25, -20 -23, -32 -29 Z" fill="{body}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
    if not husk:
        o.append('<path d="M -24 -40 C -16 -46, -4 -46, 4 -42" fill="none" stroke="#C07A5A" stroke-width="3.5" stroke-linecap="round" opacity="0.8"/>')
    # cabeza
    o.append(f'<ellipse cx="-50" cy="-40" rx="21" ry="17" fill="{body}" stroke="{INK}" stroke-width="6"/>')
    if not husk:
        o.append(f'<circle cx="-54" cy="-44" r="6" fill="#0B0B14"/><circle cx="-56" cy="-46" r="2.2" fill="#FFFFFF"/>')
        o.append('<path d="M -62 -50 Q -54 -56 -42 -54" fill="none" stroke="#C07A5A" stroke-width="3" stroke-linecap="round" opacity="0.8"/>')
    else:
        o.append(f'<circle cx="-54" cy="-44" r="5" fill="none" stroke="{INK}" stroke-width="3"/>')
    # mandíbulas
    o.append(f'<path d="M -68 -32 Q -80 -30 -82 -22" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>')
    # patas cercanas
    for a, k, f in L:
        o.append(leg([a, k, f], 4.5, near, 5))
    # antena cercana (codada)
    o.append(leg([(-54, -54), (-56, -80), (-86, -92)], 3.5, near, 5))
    return "".join(o)


LARVA_DEFS = '''<radialGradient id="lvab" cx="0.38" cy="0.3" r="0.85"><stop offset="0" stop-color="#D8BE94"/><stop offset="0.5" stop-color="#A08060"/><stop offset="1" stop-color="#5A4430"/></radialGradient>
<linearGradient id="lvah" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#C4A47C"/><stop offset="1" stop-color="#6E5236"/></linearGradient>
<linearGradient id="mand" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3A1A0C"/><stop offset="0.45" stop-color="#8B4A22"/><stop offset="1" stop-color="#B8743C"/></linearGradient>'''


def bez(p0, p1, p2, p3, t):
    u = 1 - t
    return tuple(u**3 * a + 3 * u * u * t * b + 3 * u * t * t * c + t**3 * d for a, b, c, d in zip(p0, p1, p2, p3))


def _mandible(sign, open_=1.0):
    """Mandíbula en hoz (lado sign=-1 izq, +1 der), base en la cabeza, punta hacia -y."""
    s = sign
    ox = 40 * open_
    base_o, base_i = (22 * s, -12), (6 * s, -16)
    tip = ((4 + 30 * max(0, open_ - 0.6)) * s, -116)
    c1, c2 = ((26 + ox) * s, -34), ((24 + ox * 1.05) * s, -116)        # borde exterior
    c3, c4 = ((14 + ox * 0.86) * s, -96), ((10 + ox * 0.78) * s, -40)   # borde interior (punta -> base)
    d = (f"M {base_o[0]} {base_o[1]} C {c1[0]} {c1[1]}, {c2[0]} {c2[1]}, {tip[0]} {tip[1]} "
         f"C {c3[0]} {c3[1]}, {c4[0]} {c4[1]}, {base_i[0]} {base_i[1]} Z")
    o = ''
    for t, ln in ((0.28, 9), (0.46, 12), (0.64, 10)):
        px, py = bez(tip, c3, c4, base_i, t)
        o += f'<path d="M {px + 2 * s:.1f} {py - 6:.1f} L {px - ln * s:.1f} {py + 2:.1f} L {px + 2 * s:.1f} {py + 6:.1f} Z" fill="#8B4A22" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>'
    o += f'<path d="{d}" fill="url(#mand)" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    # brillo y pelillos
    hx, hy = bez(base_o, c1, c2, tip, 0.45)
    o += f'<path d="M {hx - 6 * s:.1f} {hy + 12:.1f} Q {hx - 4 * s:.1f} {hy:.1f} {hx - 10 * s:.1f} {hy - 14:.1f}" fill="none" stroke="#E0A070" stroke-width="3" stroke-linecap="round" opacity="0.8"/>'
    for t in (0.3, 0.55):
        px, py = bez(base_o, c1, c2, tip, t)
        o += f'<path d="M {px:.1f} {py:.1f} l {11 * s} -7" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>'
    return o


def larva(open_=1.0, bristles=True):
    """Larva de hormiga león vista desde arriba-lado, cabeza en (0,0) mirando a -y; abdomen hacia +y. Largo ~260."""
    o = []
    # patas (6), cortas, desde el tórax
    for y0, dx, dy in ((30, 32, -12), (52, 46, 0), (64, 50, 18)):
        for s in (-1, 1):
            o.append(leg([(14 * s, y0), (dx * s, y0 + dy - 14), ((dx + 10) * s, y0 + dy + 10)], 7, "#6E5236", 6))
    # abdomen
    o.append(f'<ellipse cx="0" cy="138" rx="58" ry="74" fill="url(#lvab)" stroke="{INK}" stroke-width="7"/>')
    if bristles:
        import math as m
        br = []
        for k in range(26):
            a = k / 26 * 2 * m.pi
            x, y = 58 * m.cos(a), 138 + 74 * m.sin(a)
            nx, ny = m.cos(a), m.sin(a)
            br.append(f'M {x:.1f} {y:.1f} l {nx * 11:.1f} {ny * 11 - 3:.1f}')
        o.append(f'<path d="{" ".join(br)}" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>')
    # segmentos y manchas
    o.append(f'<g fill="none" stroke="{INK}" stroke-width="3" opacity="0.4">' +
             "".join(f'<path d="M {-50 + abs(k) * 0:.0f} {100 + k * 26} Q 0 {112 + k * 26} 50 {100 + k * 26}"/>' for k in range(4)) + '</g>')
    o.append('<g fill="#5A4026" opacity="0.55"><ellipse cx="-22" cy="112" rx="9" ry="6"/><ellipse cx="22" cy="112" rx="9" ry="6"/><ellipse cx="-26" cy="140" rx="10" ry="6"/><ellipse cx="26" cy="140" rx="10" ry="6"/><ellipse cx="-20" cy="168" rx="8" ry="5"/><ellipse cx="20" cy="168" rx="8" ry="5"/><ellipse cx="0" cy="188" rx="9" ry="6"/></g>')
    o.append('<path d="M -34 92 Q -10 76 22 82" fill="none" stroke="#F2E2C2" stroke-width="5" stroke-linecap="round" opacity="0.8"/>')
    # tórax
    o.append(f'<ellipse cx="0" cy="58" rx="32" ry="20" fill="url(#lvah)" stroke="{INK}" stroke-width="6"/>')
    o.append(f'<ellipse cx="0" cy="30" rx="17" ry="14" fill="url(#lvah)" stroke="{INK}" stroke-width="6"/>')
    # mandíbulas
    o.append(_mandible(-1, open_) + _mandible(1, open_))
    # cabeza
    o.append(f'<path d="M -24 -16 C -26 6, -18 18, 0 18 C 18 18, 26 6, 24 -16 C 14 -22, -14 -22, -24 -16 Z" fill="url(#lvah)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
    o.append('<path d="M -8 -12 L -4 8 M 8 -12 L 4 8" stroke="#5A4026" stroke-width="4" stroke-linecap="round" opacity="0.6"/>')
    o.append('<path d="M -16 -14 Q 0 -18 16 -14" fill="none" stroke="#F2E2C2" stroke-width="3" stroke-linecap="round" opacity="0.8"/>')
    # ojos en tubérculos
    for s in (-1, 1):
        o.append(f'<circle cx="{25 * s}" cy="-10" r="7" fill="#6E5236" stroke="{INK}" stroke-width="4"/><circle cx="{25 * s}" cy="-10" r="3" fill="{INK}"/>')
    return "".join(o)


# hormiga vista desde arriba
def ant_top(husk=False):
    s = []
    for y0, ang, l1, l2 in ((-8, -50, 26, 30), (0, -95, 24, 30), (8, -135, 28, 36)):
        for sg in (-1, 1):
            a1 = math.radians(ang)
            kx, ky = sg * 10 + sg * l1 * abs(math.sin(a1)) * 1.1, y0 + l1 * math.cos(a1) * -1
            a2 = a1 + (0.6 if ang > -90 else -0.6)
            fx, fy = kx + sg * l2 * abs(math.sin(a2)), ky - l2 * math.cos(a2)
            s.append(leg([(sg * 6, y0), (kx, ky), (fx, fy)], 4, ("#D8C8B0" if husk else "#2A140C"), 5))
    s.append(f'<ellipse cx="0" cy="48" rx="18" ry="24" fill="{"#E6D7BF" if husk else "url(#antg)"}" stroke="{INK}" stroke-width="5"/>')
    s.append(f'<ellipse cx="0" cy="22" rx="6" ry="7" fill="{"#E6D7BF" if husk else "url(#antb)"}" stroke="{INK}" stroke-width="4"/>')
    s.append(f'<ellipse cx="0" cy="0" rx="10" ry="18" fill="{"#E6D7BF" if husk else "url(#antb)"}" stroke="{INK}" stroke-width="5"/>')
    s.append(f'<ellipse cx="0" cy="-30" rx="14" ry="13" fill="{"#E6D7BF" if husk else "url(#antb)"}" stroke="{INK}" stroke-width="5"/>')
    s.append('<path d="M -6 40 Q 0 32 8 38" fill="none" stroke="#C07A5A" stroke-width="3" stroke-linecap="round"/>')
    for sg in (-1, 1):
        s.append(f'<circle cx="{sg * 10}" cy="-34" r="3.5" fill="{INK}"/>')
        s.append(leg([(sg * 6, -40), (sg * 16, -62), (sg * 30, -76)], 3, ("#D8C8B0" if husk else "#2A140C"), 5))
        s.append(f'<path d="M {sg * 4} -42 l {sg * 4} -8" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>')
    return "".join(s)


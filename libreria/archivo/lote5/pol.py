"""Piezas de dibujo para los vídeos de política (urnas, sobres, hemiciclo, etiquetas)."""
import math, sys
sys.path.insert(0, "/tmp/claude-0/-home-user-automatizacion-contenidos/039df981-7a17-5355-b711-18510fb209db/scratchpad")
from lib import f, smooth, dbl, text_w, lg, rg, INK, LIME, CORAL  # noqa

MONO = 'font-family="JetBrains Mono" font-weight="800"'
DISP = 'font-family="Unbounded" font-weight="900"'

BASE_DEFS = (
    lg("urnaGlass", [(0, "#EAF8FF", 0.75), (1, "#9FD3F2", 0.55)])
    + lg("urnaSide", [(0, "#C4E6FA", 0.7), (1, "#7DB8DE", 0.6)])
    + lg("urnaLid", [(0, "#5A6B8C"), (1, "#2C3954")])
    + lg("paperG", [(0, "#FFFFFF"), (1, "#EDEFF5")])
    + lg("sobreG", [(0, "#FFFFFF"), (1, "#E3E6EE")])
    + lg("woodG", [(0, "#C98B55"), (1, "#8A5A31")])
    + rg("shadowR", [(0, INK, 0.35), (1, INK, 0)])
)


def T(x, y, s, size=30, fill=INK, anchor="middle", font=MONO, extra=""):
    return f'<text x="{f(x)}" y="{f(y)}" text-anchor="{anchor}" {font} font-size="{size}" fill="{fill}" {extra}>{s}</text>'


def label(id_, cx, cy, text, target=None, bg=INK, fg=LIME, size=30, src=None, dot=True):
    """Etiqueta (rect + texto mono MAYÚSCULAS) con línea guía opcional. Devuelve (svg, caja)."""
    w = text_w(text, size)
    h = 58 if size >= 28 else 48
    x, y = cx - w / 2, cy - h / 2
    s = f'<g id="{id_}">'
    if target:
        sx, sy = src or (cx, cy)
        s += f'<line x1="{f(sx)}" y1="{f(sy)}" x2="{f(target[0])}" y2="{f(target[1])}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
        if dot:
            s += f'<circle cx="{f(target[0])}" cy="{f(target[1])}" r="9" fill="{LIME}" stroke="{INK}" stroke-width="4"/>'
    s += (f'<rect x="{f(x)}" y="{f(y)}" width="{w}" height="{h}" rx="12" fill="{bg}" stroke="{INK}" stroke-width="3"/>'
          + T(cx, cy + size * 0.36, text, size, fg) + "</g>")
    return s, (x, y, x + w, y + h)


def arrow(id_, d_pts, col=LIME, w=12, head=30, curve=None, cubic=None):
    (x1, y1), (x2, y2) = d_pts
    if cubic:
        (a, b), (c, e) = cubic
        d = f"M {f(x1)} {f(y1)} C {f(a)} {f(b)}, {f(c)} {f(e)}, {f(x2)} {f(y2)}"
        ang = math.atan2(y2 - e, x2 - c)
    elif curve:
        d = f"M {f(x1)} {f(y1)} Q {f(curve[0])} {f(curve[1])} {f(x2)} {f(y2)}"
        ang = math.atan2(y2 - curve[1], x2 - curve[0])
    else:
        d = f"M {f(x1)} {f(y1)} L {f(x2)} {f(y2)}"
        ang = math.atan2(y2 - y1, x2 - x1)
    p1 = (x2 - head * math.cos(ang - 0.5), y2 - head * math.sin(ang - 0.5))
    p2 = (x2 - head * math.cos(ang + 0.5), y2 - head * math.sin(ang + 0.5))
    hd = f"M {f(p1[0])} {f(p1[1])} L {f(x2)} {f(y2)} L {f(p2[0])} {f(p2[1])}"
    return (f'<g id="{id_}">' if id_ else "<g>") + dbl(d, w, col, 9) + dbl(hd, w, col, 9) + "</g>"


def sobre(cx, cy, w, h, rot=0, fill="url(#sobreG)", sw=5, id_=None):
    """Sobre de votación (rectángulo con solapa)."""
    x, y = cx - w / 2, cy - h / 2
    g = f'<g{f" id={chr(34)}{id_}{chr(34)}" if id_ else ""} transform="rotate({f(rot)} {f(cx)} {f(cy)})">'
    g += f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="5" fill="{fill}" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"/>'
    g += f'<path d="M {f(x+4)} {f(y+4)} L {f(cx)} {f(y+h*0.55)} L {f(x+w-4)} {f(y+4)}" fill="none" stroke="#B9BFCC" stroke-width="{f(sw*0.7)}" stroke-linejoin="round"/>'
    return g + "</g>"


def urna(cx, base, w, h, text=None, uid="u", n_sobres=6, seed=1, plate="#FFFFFF"):
    """Urna transparente en vista 3/4. base = y del suelo de la urna (apoyo)."""
    import random
    rnd = random.Random(seed)
    d = w * 0.26
    dx, dy = d * 0.75, -d * 0.55
    x0, y0 = cx - w / 2 - dx / 2, base - h
    o = [f'<ellipse cx="{f(cx+dx/2)}" cy="{f(base+4)}" rx="{f(w*0.62)}" ry="{f(w*0.07)}" fill="{INK}" opacity="0.22"/>']
    # cara trasera/lateral (interior visible)
    side = f"M {f(x0+w)} {f(y0)} L {f(x0+w+dx)} {f(y0+dy)} L {f(x0+w+dx)} {f(base+dy)} L {f(x0+w)} {f(base)} Z"
    o.append(f'<path d="{side}" fill="url(#urnaSide)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
    # sobres dentro (apilados abajo)
    for i in range(n_sobres):
        sx = x0 + w * (0.18 + 0.68 * rnd.random()) + dx * 0.3
        sy = base - h * (0.08 + 0.22 * rnd.random()) - (i % 3) * 6
        o.append(sobre(sx, sy, w * 0.3, w * 0.2, rnd.uniform(-35, 35), sw=3.5))
    # cara frontal translúcida
    o.append(f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" fill="url(#urnaGlass)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
    # brillos
    o.append(f'<path d="M {f(x0+w*0.12)} {f(y0+h*0.15)} L {f(x0+w*0.12)} {f(y0+h*0.8)}" stroke="#FFFFFF" stroke-width="{f(w*0.05)}" stroke-linecap="round" opacity="0.8"/>')
    o.append(f'<path d="M {f(x0+w*0.22)} {f(y0+h*0.15)} L {f(x0+w*0.22)} {f(y0+h*0.45)}" stroke="#FFFFFF" stroke-width="{f(w*0.025)}" stroke-linecap="round" opacity="0.7"/>')
    # tapa (cara superior + canto)
    lt = max(14, h * 0.09)
    top = f"M {f(x0)} {f(y0)} L {f(x0+dx)} {f(y0+dy)} L {f(x0+w+dx)} {f(y0+dy)} L {f(x0+w)} {f(y0)} Z"
    o.append(f'<path d="{top}" fill="#7E8FB0" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
    o.append(f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(lt)}" fill="url(#urnaLid)" stroke="{INK}" stroke-width="6"/>')
    o.append(f'<path d="M {f(x0+w)} {f(y0)} L {f(x0+w+dx)} {f(y0+dy)} L {f(x0+w+dx)} {f(y0+dy+lt)} L {f(x0+w)} {f(y0+lt)} Z" fill="#26324A" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
    o.append(f'<path d="M {f(x0+8)} {f(y0+4)} L {f(x0+w-8)} {f(y0+4)}" stroke="#A9B8D6" stroke-width="3" stroke-linecap="round"/>')
    # ranura
    mx, my = x0 + w / 2 + dx / 2, y0 + dy / 2
    sl = w * 0.36
    o.append(f'<path d="M {f(mx-sl/2)} {f(my)} L {f(mx+sl/2)} {f(my)}" stroke="{INK}" stroke-width="{f(max(8, w*0.035))}" stroke-linecap="round"/>')
    # cantos verticales del cristal
    o.append(f'<path d="M {f(x0+w+dx)} {f(y0+dy+lt)} L {f(x0+w+dx)} {f(base+dy)}" stroke="{INK}" stroke-width="6"/>')
    if text:
        size = max(18, min(30, w * 0.085))
        tw = text_w(text, size) - 20
        o.append(f'<rect x="{f(cx-tw/2)}" y="{f(y0+h*0.42)}" width="{f(tw)}" height="{f(size*1.6)}" rx="8" fill="{plate}" stroke="{INK}" stroke-width="4"/>')
        o.append(T(cx, y0 + h * 0.42 + size * 1.13, text, size))
    return "".join(o), (mx, my)


def seats_layout(n, rows, r0, r1, sr=0):
    """Posiciones (ángulo, radio) de un hemiciclo de n escaños en 'rows' filas, ordenadas de izquierda a derecha."""
    radii = [r0 + (r1 - r0) * i / max(1, rows - 1) for i in range(rows)]
    tot = sum(radii)
    counts = [round(n * r / tot) for r in radii]
    while sum(counts) > n: counts[counts.index(max(counts))] -= 1
    while sum(counts) < n: counts[-1] += 1
    seats = []
    for r, c in zip(radii, counts):
        for k in range(c):
            m = math.asin(min(0.9, (sr + 8) / r)) if sr else 0
            a = m + (math.pi - 2 * m) * (k / (c - 1)) if c > 1 else math.pi / 2
            seats.append((a, r))
    seats.sort(key=lambda s: (-s[0], s[1]))  # de izquierda (ángulo pi) a derecha (0)
    return seats


def hemiciclo(cx, cy, n, rows, r0, r1, colors, seat_r, sw=4, ids=None):
    """colors: lista de colores por escaño (izq->dcha). Devuelve lista de (svg_escaño, x, y)."""
    out = []
    for i, (a, r) in enumerate(seats_layout(n, rows, r0, r1, seat_r)):
        x, y = cx + r * math.cos(a), cy - r * math.sin(a)
        c = colors[i]
        s = (f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(seat_r)}" fill="{c}" stroke="{INK}" stroke-width="{sw}"/>'
             f'<circle cx="{f(x-seat_r*0.3)}" cy="{f(y-seat_r*0.35)}" r="{f(seat_r*0.28)}" fill="#FFFFFF" opacity="0.55"/>')
        out.append((s, x, y))
    return out


def shade(hexc, k):
    """Aclara (k>0) u oscurece (k<0) un color hex."""
    h = hexc.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    if k >= 0:
        r, g, b = [int(v + (255 - v) * k) for v in (r, g, b)]
    else:
        r, g, b = [int(v * (1 + k)) for v in (r, g, b)]
    return f"#{r:02X}{g:02X}{b:02X}"


def save(path, svg):
    open(path, "w").write(svg)
    print("ok", path, len(svg))

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




BOTTLE_DEFS = '''<linearGradient id="glass" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#3A1A06"/><stop offset="0.18" stop-color="#7A3E0E"/><stop offset="0.42" stop-color="#B8641A"/><stop offset="0.62" stop-color="#8A4612"/><stop offset="1" stop-color="#2E1404"/></linearGradient>
<linearGradient id="glassempty" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5A2C0C"/><stop offset="0.4" stop-color="#C98A44"/><stop offset="1" stop-color="#4A2408"/></linearGradient>
<linearGradient id="cap" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8A9098"/><stop offset="0.35" stop-color="#F2F4F6"/><stop offset="0.7" stop-color="#B9C0C8"/><stop offset="1" stop-color="#6A7078"/></linearGradient>
<linearGradient id="label" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#D9CFB4"/><stop offset="0.4" stop-color="#FFF8E6"/><stop offset="1" stop-color="#CFC3A4"/></linearGradient>
<radialGradient id="foamg" cx="0.4" cy="0.3" r="0.8"><stop offset="0" stop-color="#FFFFFF"/><stop offset="0.7" stop-color="#FFF6E0"/><stop offset="1" stop-color="#EBD9B0"/></radialGradient>'''


class Bottle:
    """Perfil de botellín: cx centro, base (y del culo), H alto, W ancho."""

    def __init__(self, cx, base, H, W):
        self.cx, self.base, self.H, self.W = cx, base, H, W
        w = W / 2
        self.w = w
        self.ys = base - 0.52 * H          # empieza el hombro
        self.yn = base - 0.76 * H          # empieza el cuello
        self.yl = base - 0.93 * H          # anillo de la boca
        self.top = base - H
        self.nw = 0.36 * w

    def outline(self):
        cx, b, w, nw = self.cx, self.base, self.w, self.nw
        r = 14
        ys, yn, yl, top = self.ys, self.yn, self.yl, self.top
        lw = nw + 6
        return (f"M {cx - w + r} {b} Q {cx - w} {b} {cx - w} {b - r} L {cx - w} {ys} "
                f"C {cx - w} {ys - (ys - yn) * 0.55}, {cx - nw} {yn + (ys - yn) * 0.35}, {cx - nw} {yn} "
                f"L {cx - nw} {yl} Q {cx - lw} {yl} {cx - lw} {yl - 6} L {cx - lw} {top + 6} Q {cx - lw} {top} {cx - nw} {top} "
                f"L {cx + nw} {top} Q {cx + lw} {top} {cx + lw} {top + 6} L {cx + lw} {yl - 6} Q {cx + lw} {yl} {cx + nw} {yl} "
                f"L {cx + nw} {yn} C {cx + nw} {yn + (ys - yn) * 0.35}, {cx + w} {ys - (ys - yn) * 0.55}, {cx + w} {ys} "
                f"L {cx + w} {b - r} Q {cx + w} {b} {cx + w - r} {b} Z")

    def halfwidth(self, y):
        """Semiancho exterior a la altura y (aprox.)."""
        if y >= self.ys:
            return self.w
        if y >= self.yn:
            t = (self.ys - y) / (self.ys - self.yn)
            return self.w + (self.nw - self.w) * (3 * t * t - 2 * t ** 3)
        return self.nw

    def draw(self, cap=True, label=True, fill="url(#glass)", ink=7, liquid=None):
        cx, b, w, nw = self.cx, self.base, self.w, self.nw
        o = [f'<path d="{self.outline()}" fill="{fill}" stroke="{INK}" stroke-width="{ink}" stroke-linejoin="round"/>']
        if liquid is not None:
            # espacio de aire en el cuello (más claro) por encima del nivel
            o.append(f'<path d="M {cx - nw + 4} {liquid} L {cx + nw - 4} {liquid}" stroke="#F0B860" stroke-width="3" opacity="0.8"/>')
            o.append(f'<rect x="{cx - nw + 4}" y="{self.yl + 4}" width="{2 * nw - 8}" height="{liquid - self.yl - 4}" fill="#E8B070" opacity="0.35"/>')
        if label:
            ly0, ly1 = b - 0.42 * self.H, b - 0.12 * self.H
            o.append(f'<path d="M {cx - w + 1} {ly0} Q {cx} {ly0 + 10} {cx + w - 1} {ly0} L {cx + w - 1} {ly1} Q {cx} {ly1 + 10} {cx - w + 1} {ly1} Z" fill="url(#label)" stroke="{INK}" stroke-width="4"/>')
            my = (ly0 + ly1) / 2
            # emblema genérico: espiga
            o.append(f'<g stroke="#B5862E" stroke-width="4" fill="#E9C05A" stroke-linejoin="round">'
                     f'<line x1="{cx}" y1="{my + 22}" x2="{cx}" y2="{my - 26}" />'
                     + "".join(f'<ellipse cx="{cx + sg * 8}" cy="{my - 16 + k * 12}" rx="6" ry="9" transform="rotate({sg * 30} {cx + sg * 8} {my - 16 + k * 12})"/>' for k in range(3) for sg in (-1, 1))
                     + '</g>')
            o.append(f'<path d="M {cx - w * 0.6} {my + 34} Q {cx} {my + 40} {cx + w * 0.6} {my + 34}" fill="none" stroke="#C9302C" stroke-width="5" stroke-linecap="round"/>')
        # brillos del vidrio
        o.append(f'<path d="M {cx - w * 0.55} {b - 26} L {cx - w * 0.55} {self.ys + 6} C {cx - w * 0.55} {self.ys - 30}, {cx - nw * 0.6} {self.yn + 26}, {cx - nw * 0.55} {self.yn - 4} L {cx - nw * 0.55} {self.yl + 8}" fill="none" stroke="#FFFFFF" stroke-width="{max(5, w * 0.12):.0f}" stroke-linecap="round" opacity="0.55"/>')
        o.append(f'<path d="M {cx + w * 0.7} {b - 40} L {cx + w * 0.7} {self.ys - 4}" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" opacity="0.35"/>')
        o.append(f'<path d="M {cx - w * 0.3} {b - 8} Q {cx} {b - 2} {cx + w * 0.3} {b - 8}" fill="none" stroke="#FFD89A" stroke-width="3" opacity="0.6"/>')
        if cap:
            o.append(self.cap())
        return "".join(o)

    def cap(self):
        cx, nw, top = self.cx, self.nw, self.top
        cw = nw + 10
        teeth = []
        n = 9
        for i in range(n + 1):
            x = cx - cw + 2 * cw * i / n
            teeth.append(f"L {x:.1f} {top + 14 + (5 if i % 2 else 0)}")
        d = f"M {cx - cw} {top - 2} Q {cx - cw} {top - 12} {cx - cw + 8} {top - 12} L {cx + cw - 8} {top - 12} Q {cx + cw} {top - 12} {cx + cw} {top - 2} L {cx + cw} {top + 14} " + " ".join(reversed(teeth)) + " Z"
        return (f'<g><path d="{d}" fill="url(#cap)" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
                f'<path d="M {cx - cw + 8} {top - 6} L {cx + cw - 10} {top - 6}" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/>'
                + "".join(f'<line x1="{cx - cw + 2 * cw * (i + 0.5) / n:.1f}" y1="{top + 2}" x2="{cx - cw + 2 * cw * (i + 0.5) / n:.1f}" y2="{top + 13}" stroke="{INK}" stroke-width="2" opacity="0.5"/>' for i in range(n))
                + '</g>')


def foam_blob(pts, r, seed=1, col="url(#foamg)"):
    """Espuma con volumen: círculos solapados con contorno común (dos pasadas)."""
    random.seed(seed)
    circles = [(x + random.uniform(-4, 4), y + random.uniform(-4, 4), r * random.uniform(0.75, 1.15)) for x, y in pts]
    out = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rr + 6:.1f}" fill="{INK}"/>' for x, y, rr in circles)
    out += "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rr:.1f}" fill="{col}"/>' for x, y, rr in circles)
    out += "".join(f'<circle cx="{x - rr * 0.3:.1f}" cy="{y - rr * 0.35:.1f}" r="{rr * 0.22:.1f}" fill="#FFFFFF" opacity="0.9"/>' for x, y, rr in circles[::2])
    out += "".join(f'<circle cx="{x + rr * 0.25:.1f}" cy="{y + rr * 0.2:.1f}" r="{rr * 0.18:.1f}" fill="none" stroke="#D9C49A" stroke-width="2"/>' for x, y, rr in circles[1::3])
    return out


CUT_DEFS = '''<linearGradient id="glasscut" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5A2A08"/><stop offset="0.5" stop-color="#A65A16"/><stop offset="1" stop-color="#4A2206"/></linearGradient>
<linearGradient id="beer" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F7C04A"/><stop offset="0.5" stop-color="#E39A22"/><stop offset="1" stop-color="#B86A0C"/></linearGradient>
<linearGradient id="beerside" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#7A3E08" stop-opacity="0.45"/><stop offset="0.25" stop-color="#7A3E08" stop-opacity="0"/><stop offset="0.75" stop-color="#7A3E08" stop-opacity="0"/><stop offset="1" stop-color="#7A3E08" stop-opacity="0.5"/></linearGradient>
<radialGradient id="bub" cx="0.35" cy="0.3" r="0.75"><stop offset="0" stop-color="#FFFFFF"/><stop offset="0.6" stop-color="#FFF3D0"/><stop offset="1" stop-color="#F2C878"/></radialGradient>'''


def bubble(x, y, r, ink=True):
    s = f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="url(#bub)" fill-opacity="0.85" stroke="{INK if ink else "#B8741A"}" stroke-width="{max(1.5, min(4, r * 0.25)):.1f}"/>'
    if r > 5:
        s += f'<circle cx="{x - r * 0.35:.1f}" cy="{y - r * 0.35:.1f}" r="{r * 0.25:.1f}" fill="#FFFFFF"/>'
    return s


def cut_bottle(cx, base, H, W, level, t=16, uid="cb"):
    """Botella en corte: devuelve (fondo, borde) para meter cosas entre medias (líquido visible)."""
    out = Bottle(cx, base, H, W)
    inn = Bottle(cx, base - t, H - t, W - 2 * t)
    inn.nw = out.nw - t * 0.7
    back = [f'<path d="{out.outline()}" fill="url(#glasscut)" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>',
            f'<clipPath id="{uid}in"><path d="{inn.outline()}"/></clipPath>',
            f'<path d="{inn.outline()}" fill="#F6E7CF"/>',
            f'<g clip-path="url(#{uid}in)"><rect x="{cx - W}" y="{level}" width="{2 * W}" height="{base - level + 10}" fill="url(#beer)"/>'
            f'<rect x="{cx - W / 2}" y="{level}" width="{W}" height="{base - level + 10}" fill="url(#beerside)"/>'
            f'<path d="M {cx - W} {level} L {cx + W} {level}" stroke="#FFF2C8" stroke-width="5"/></g>']
    front = [f'<path d="{inn.outline()}" fill="none" stroke="{INK}" stroke-width="4" opacity="0.8"/>',
             f'<path d="M {cx - out.w + t * 0.45} {base - 30} L {cx - out.w + t * 0.45} {out.ys}" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity="0.6"/>']
    return "".join(back), "".join(front), out, inn

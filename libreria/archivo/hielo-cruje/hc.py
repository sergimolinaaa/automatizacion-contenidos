"""Piezas para «Por qué cruje el hielo» (reutiliza lote5/pol.py: T, label, arrow, save, shade)."""
import sys, math, random
SP = "/tmp/claude-0/-home-user-automatizacion-contenidos/039df981-7a17-5355-b711-18510fb209db/scratchpad"
for p in (SP, SP + "/lote5"):
    if p not in sys.path:
        sys.path.insert(0, p)
from pol import *  # noqa  (T, label, arrow, save, shade, MONO, DISP, f, smooth, dbl, lg, rg, INK, LIME, CORAL)

YEL = "#FFC928"
ICE_EDGE = "#2B6E9E"
DEFS = (
    lg("iceF", [(0, "#F7FDFF"), (0.55, "#D3F0FC"), (1, "#A8DDF5")], 0, 0, 1, 1)
    + lg("iceT", [(0, "#FFFFFF"), (1, "#DDF4FF")], 0, 0, 1, 1)
    + lg("iceS", [(0, "#B5E3F7"), (1, "#7FC6EA")], 0, 0, 1, 1)
    + rg("cloudR", [(0, "#FFFFFF", 0.95), (0.6, "#FFFFFF", 0.45), (1, "#FFFFFF", 0)])
    + lg("sodaG", [(0, "#FFD36B"), (0.5, "#F5A52A"), (1, "#D9741A")])
    + lg("sodaS", [(0, "#FFE7A3"), (1, "#FFC24D")])
    + lg("glassB", [(0, "#FFFFFF", 0.55), (1, "#DDEFFA", 0.35)], 0, 0, 1, 0)
    + lg("warmG", [(0, "#FFC9A3"), (1, "#FF8A5C")], 0, 0, 1, 1)
    + lg("coldG", [(0, "#BFEAFF"), (1, "#5DB7EC")], 0, 0, 1, 1)
    + lg("bottleG", [(0, "#7FD48A"), (0.45, "#C9F2C4"), (1, "#3E9D55")], 0, 0, 1, 0)
    + lg("labelG", [(0, "#FF6A45"), (1, "#E2432A")])
    + lg("woodG2", [(0, "#D9A46C"), (1, "#9C6334")])
    + lg("metalG", [(0, "#F2F4F8"), (1, "#B9C0CC")], 0, 0, 1, 0)
    + rg("burstR", [(0, "#FFF6B8"), (1, YEL)])
    + rg("skinR", [(0, "#FFD9C2"), (0.7, "#F2B08C"), (1, "#D98B66")], 0.4, 0.4, 0.7)
    + rg("shadowR", [(0, INK, 0.35), (1, INK, 0)])
)


def header(w, h, extra=""):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">\n<defs>{DEFS}{extra}</defs>'


def g(id_, body, extra=""):
    return f'<g id="{id_}"{extra}>{body}</g>'


def cube(cx, cy, s, ang=0, seed=1, bubbles=4, cloud=True, sw=None):
    """Cubito de hielo en perspectiva. (cx, cy) = centro de la cara frontal; s = lado."""
    rnd = random.Random(seed)
    h = s / 2
    d = s * 0.34
    a = math.radians(ang)
    sw = sw or max(4, s * 0.045)

    def R(x, y):
        return (cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a))
    P = lambda pts: "M " + " L ".join(f"{f(x)} {f(y)}" for x, y in pts) + " Z"
    F = [R(-h, -h), R(h, -h), R(h, h), R(-h, h)]
    Tp = [R(-h, -h), R(-h + d, -h - d * 0.8), R(h + d, -h - d * 0.8), R(h, -h)]
    S = [R(h, -h), R(h + d, -h - d * 0.8), R(h + d, h - d * 0.8), R(h, h)]
    o = f'<path d="{P(S)}" fill="url(#iceS)" stroke="{ICE_EDGE}" stroke-width="{f(sw)}" stroke-linejoin="round"/>'
    o += f'<path d="{P(Tp)}" fill="url(#iceT)" stroke="{ICE_EDGE}" stroke-width="{f(sw)}" stroke-linejoin="round"/>'
    o += f'<path d="{P(F)}" fill="url(#iceF)" stroke="{ICE_EDGE}" stroke-width="{f(sw)}" stroke-linejoin="round"/>'
    if cloud:
        c = R(0, 0)
        o += f'<ellipse cx="{f(c[0])}" cy="{f(c[1])}" rx="{f(s*0.28)}" ry="{f(s*0.24)}" fill="url(#cloudR)" transform="rotate({f(ang)} {f(c[0])} {f(c[1])})"/>'
    for _ in range(bubbles):
        bx, by = R(rnd.uniform(-h * 0.6, h * 0.6), rnd.uniform(-h * 0.6, h * 0.6))
        r = rnd.uniform(s * 0.025, s * 0.045)
        o += f'<circle cx="{f(bx)}" cy="{f(by)}" r="{f(r)}" fill="#FFFFFF" stroke="#9CCFEA" stroke-width="{f(max(1.5, s*0.01))}"/>'
    # brillos
    x1, y1 = R(-h + s * 0.12, -h + s * 0.14)
    x2, y2 = R(-h + s * 0.12, h - s * 0.3)
    o += f'<path d="M {f(x1)} {f(y1)} L {f(x2)} {f(y2)}" stroke="#FFFFFF" stroke-width="{f(s*0.07)}" stroke-linecap="round"/>'
    x1, y1 = R(-h + s * 0.28, -h + s * 0.12)
    x2, y2 = R(-h + s * 0.5, -h + s * 0.12)
    o += f'<path d="M {f(x1)} {f(y1)} L {f(x2)} {f(y2)}" stroke="#FFFFFF" stroke-width="{f(s*0.04)}" stroke-linecap="round" opacity="0.9"/>'
    return o


def crack(pts, w=6, col=ICE_EDGE, id_=None, glow=True):
    """Grieta: polilínea quebrada con brillo blanco al lado."""
    d = "M " + " L ".join(f"{f(x)} {f(y)}" for x, y in pts)
    s = f'<g id="{id_}">' if id_ else "<g>"
    if glow:
        s += f'<path d="{d}" fill="none" stroke="#FFFFFF" stroke-width="{f(w*2.2)}" stroke-linecap="round" stroke-linejoin="round" opacity="0.9"/>'
    s += f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{f(w)}" stroke-linecap="round" stroke-linejoin="round"/>'
    return s + "</g>"


def zig(x0, y0, x1, y1, n=5, amp=10, seed=3, branches=0):
    """Puntos de una grieta en zigzag de (x0,y0) a (x1,y1)."""
    rnd = random.Random(seed)
    L = math.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    nx, ny = -uy, ux
    pts = [(x0, y0)]
    for i in range(1, n):
        t = i / n
        k = amp * (1 if i % 2 else -1) * rnd.uniform(0.6, 1.2)
        pts.append((x0 + ux * L * t + nx * k, y0 + uy * L * t + ny * k))
    pts.append((x1, y1))
    return pts


def burst(cx, cy, r, text, size, rot=-8, id_=None, col="url(#burstR)", fg=INK, n=12):
    """Estrella de cómic con onomatopeya."""
    pts = []
    for i in range(n * 2):
        ang = math.pi * i / n
        rr = r if i % 2 == 0 else r * 0.72
        pts.append((cx + rr * math.cos(ang), cy + rr * 0.78 * math.sin(ang)))
    d = "M " + " L ".join(f"{f(x)} {f(y)}" for x, y in pts) + " Z"
    s = f'<g id="{id_}">' if id_ else "<g>"
    s += f'<g transform="rotate({f(rot)} {f(cx)} {f(cy)})">'
    s += f'<path d="{d}" fill="{INK}" opacity="0.25" transform="translate(8 9)"/>'
    s += f'<path d="{d}" fill="{col}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
    s += T(cx, cy + size * 0.36, text, f(size), fg, font=DISP)
    return s + "</g></g>"


def waves(cx, cy, r0, n, ang0, ang1, gap=26, w=8, col=INK, id_=None):
    """Ondas de sonido (arcos concéntricos)."""
    s = f'<g id="{id_}">' if id_ else "<g>"
    for i in range(n):
        r = r0 + i * gap
        a0, a1 = math.radians(ang0), math.radians(ang1)
        x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
        x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
        s += f'<path d="M {f(x0)} {f(y0)} A {f(r)} {f(r)} 0 0 1 {f(x1)} {f(y1)}" fill="none" stroke="{col}" stroke-width="{f(w)}" stroke-linecap="round" opacity="{f(1 - i*0.18)}"/>'
    return s + "</g>"


def thermo(cx, top, h, level, col, id_fill=None, ticks=8):
    """Termómetro: tubo de top a top+h, bulbo abajo. level 0..1 de la columna."""
    w = h * 0.13
    br = w * 1.05
    bot = top + h
    s = f'<rect x="{f(cx-w/2+6)}" y="{f(top+6)}" width="{f(w)}" height="{f(h)}" rx="{f(w/2)}" fill="{INK}" opacity="0.2"/>'
    s += f'<rect x="{f(cx-w/2)}" y="{f(top)}" width="{f(w)}" height="{f(h)}" rx="{f(w/2)}" fill="#FFFFFF" stroke="{INK}" stroke-width="6"/>'
    for i in range(ticks):
        y = top + h * 0.1 + i * h * 0.75 / ticks
        s += f'<path d="M {f(cx+w*0.5)} {f(y)} L {f(cx+w*0.5+ (16 if i%2==0 else 9))} {f(y)}" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
    ftop = bot - (h * 0.88) * level
    col_d = shade(col, -0.25)
    fill = f'<rect x="{f(cx-w*0.22)}" y="{f(ftop)}" width="{f(w*0.44)}" height="{f(bot-ftop)}" rx="{f(w*0.22)}" fill="{col}"/>'
    s += f'<g id="{id_fill}">{fill}</g>' if id_fill else fill
    s += f'<circle cx="{f(cx)}" cy="{f(bot+br*0.6)}" r="{f(br)}" fill="{col}" stroke="{INK}" stroke-width="6"/>'
    s += f'<circle cx="{f(cx-br*0.35)}" cy="{f(bot+br*0.3)}" r="{f(br*0.28)}" fill="#FFFFFF" opacity="0.7"/>'
    s += f'<path d="M {f(cx-w*0.25)} {f(top+w*0.6)} L {f(cx-w*0.25)} {f(bot-w*0.4)}" stroke="#FFFFFF" stroke-width="{f(w*0.14)}" stroke-linecap="round" opacity="0.8"/>'
    _ = col_d
    return s


def water_mol(x, y, r, a_deg, warm=False):
    """Molécula de agua: O rojo y dos H blancos a 104,5°."""
    s = ""
    for da in (-52.25, 52.25):
        a = math.radians(a_deg + da)
        hx, hy = x + r * 1.15 * math.cos(a), y + r * 1.15 * math.sin(a)
        s += f'<circle cx="{f(hx)}" cy="{f(hy)}" r="{f(r*0.55)}" fill="#FFFFFF" stroke="{INK}" stroke-width="{f(r*0.16)}"/>'
    col = "#FF6B4A" if warm else "#E2452E"
    s += f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{col}" stroke="{INK}" stroke-width="{f(r*0.18)}"/>'
    s += f'<circle cx="{f(x-r*0.35)}" cy="{f(y-r*0.35)}" r="{f(r*0.28)}" fill="#FFFFFF" opacity="0.75"/>'
    return s


def snail(cx, cy, s, id_=None):
    """Caracol simpático (para «despacio»)."""
    o = f'<g id="{id_}">' if id_ else "<g>"
    o += f'<ellipse cx="{f(cx+s*0.05)}" cy="{f(cy+s*0.42)}" rx="{f(s*0.75)}" ry="{f(s*0.08)}" fill="{INK}" opacity="0.18"/>'
    body = f"M {f(cx-s*0.7)} {f(cy+s*0.38)} Q {f(cx-s*0.2)} {f(cy+s*0.28)} {f(cx+s*0.45)} {f(cy+s*0.3)} Q {f(cx+s*0.72)} {f(cy+s*0.3)} {f(cx+s*0.72)} {f(cy)} Q {f(cx+s*0.72)} {f(cy-s*0.22)} {f(cx+s*0.55)} {f(cy-s*0.2)} L {f(cx+s*0.5)} {f(cy+s*0.1)} Q {f(cx)} {f(cy+s*0.18)} {f(cx-s*0.7)} {f(cy+s*0.38)} Z"
    o += f'<path d="{body}" fill="#B8E07A" stroke="{INK}" stroke-width="{f(s*0.06)}" stroke-linejoin="round"/>'
    for dx in (0.55, 0.7):
        o += f'<path d="M {f(cx+s*dx)} {f(cy-s*0.18)} L {f(cx+s*(dx+0.08))} {f(cy-s*0.5)}" stroke="{INK}" stroke-width="{f(s*0.05)}" stroke-linecap="round"/>'
        o += f'<circle cx="{f(cx+s*(dx+0.08))}" cy="{f(cy-s*0.52)}" r="{f(s*0.07)}" fill="#FFFFFF" stroke="{INK}" stroke-width="{f(s*0.04)}"/>'
        o += f'<circle cx="{f(cx+s*(dx+0.09))}" cy="{f(cy-s*0.52)}" r="{f(s*0.03)}" fill="{INK}"/>'
    o += f'<circle cx="{f(cx-s*0.08)}" cy="{f(cy-s*0.05)}" r="{f(s*0.42)}" fill="#E8A35C" stroke="{INK}" stroke-width="{f(s*0.06)}"/>'
    sp = []
    for i in range(40):
        t = i / 39 * 2.6 * math.pi
        rr = s * 0.34 * (1 - i / 46)
        sp.append((cx - s * 0.08 + rr * math.cos(t + 3.3), cy - s * 0.05 + rr * math.sin(t + 3.3)))
    o += f'<path d="{smooth(sp)}" fill="none" stroke="#9B5E2A" stroke-width="{f(s*0.05)}" stroke-linecap="round"/>'
    o += f'<path d="M {f(cx-s*0.36)} {f(cy-s*0.22)} Q {f(cx-s*0.2)} {f(cy-s*0.4)} {f(cx)} {f(cy-s*0.38)}" fill="none" stroke="#FFFFFF" stroke-width="{f(s*0.05)}" stroke-linecap="round" opacity="0.7"/>'
    return o + "</g>"


def note(cx, cy, s, col=LIME, rot=0):
    """Nota musical."""
    o = f'<g transform="rotate({f(rot)} {f(cx)} {f(cy)})">'
    o += f'<path d="M {f(cx+s*0.28)} {f(cy)} L {f(cx+s*0.28)} {f(cy-s)} L {f(cx+s*0.8)} {f(cy-s*0.8)}" fill="none" stroke="{INK}" stroke-width="{f(s*0.14)}" stroke-linecap="round" stroke-linejoin="round"/>'
    o += f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(s*0.32)}" ry="{f(s*0.24)}" fill="{col}" stroke="{INK}" stroke-width="{f(s*0.1)}" transform="rotate(-20 {f(cx)} {f(cy)})"/>'
    return o + "</g>"

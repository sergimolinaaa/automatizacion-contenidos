"""Piezas comunes lote5c (palomitas y gerrymandering)."""
import sys, math, random
sys.path.insert(0, "/tmp/claude-0/-home-user-automatizacion-contenidos/039df981-7a17-5355-b711-18510fb209db/scratchpad/lote5b")
from common import *  # noqa  (lib + pol + common)
from pol import arrow, label, T  # noqa

def save(path, svg):
    open(path, "w").write(svg)
    print("ok", path, len(svg))

# ---------- palomitas ----------
KDEFS = (lg("kernG", [(0, "#FFD45A"), (0.55, "#F2A81D"), (1, "#C9700C")])
         + lg("kernD", [(0, "#E59A1C"), (1, "#9C5208")])
         + rg("puffG", [(0, "#FFFFFF"), (0.6, "#FFF6DE"), (1, "#F0D9A4")], cx=0.4, cy=0.35, r=0.7)
         + lg("panG", [(0, "#4A4F5C"), (1, "#16181F")])
         + lg("panIn", [(0, "#2A2D36"), (1, "#3E4350")])
         + rg("heatR", [(0, "#FF7A3C", 0.55), (1, "#FF7A3C", 0)])
         + lg("pericG", [(0, "#F3B23A"), (1, "#B8640A")])
         + lg("vitG", [(0, "#FFE07A"), (1, "#F2B53A")])
         + lg("flourG", [(0, "#FFFBEE"), (1, "#F6E7BE")])
         + lg("germG", [(0, "#FFF0C4"), (1, "#E8C778")])
         + lg("dropG", [(0, "#BFE8FF"), (1, "#3B8FE0")])
         + lg("steamG", [(0, "#FFFFFF", 0.95), (1, "#DCEFFF", 0.8)]))

def kernel_path(cx, cy, s, rot=0):
    """Grano de maíz palomero (vista frontal): ancho y redondeado arriba, punta abajo. s = alto/2."""
    pts = [(0, -1.0), (0.5, -0.92), (0.78, -0.62), (0.82, -0.2), (0.62, 0.3), (0.34, 0.72), (0.12, 0.98),
           (-0.12, 0.98), (-0.34, 0.72), (-0.62, 0.3), (-0.82, -0.2), (-0.78, -0.62), (-0.5, -0.92)]
    a = math.radians(rot)
    P = [(cx + s * (x * math.cos(a) - y * math.sin(a)), cy + s * (x * math.sin(a) + y * math.cos(a))) for x, y in pts]
    return smooth(P, closed=True), P

def kernel(cx, cy, s, rot=0, sw=None, shadow=True):
    sw = sw or max(3.5, s * 0.12)
    d, P = kernel_path(cx, cy, s, rot)
    a = math.radians(rot)
    R = lambda x, y: (cx + s * (x * math.cos(a) - y * math.sin(a)), cy + s * (x * math.sin(a) + y * math.cos(a)))
    o = []
    if shadow:
        o.append(f'<ellipse cx="{f(cx+s*0.1)}" cy="{f(cy+s*1.02)}" rx="{f(s*0.75)}" ry="{f(s*0.16)}" fill="{INK}" opacity="0.25"/>')
    o.append(f'<path d="{d}" fill="url(#kernG)" stroke="{INK}" stroke-width="{f(sw)}" stroke-linejoin="round"/>')
    # germen (mancha clara en la cara)
    g = [R(0, -0.15), R(0.3, 0.05), R(0.22, 0.5), R(0, 0.68), R(-0.22, 0.5), R(-0.3, 0.05)]
    o.append(f'<path d="{smooth(g, True)}" fill="url(#germG)" opacity="0.55"/>')
    # punta (pedicelo)
    t = [R(-0.13, 0.86), R(0.13, 0.86), R(0.1, 1.0), R(-0.1, 1.0)]
    o.append(f'<path d="{smooth(t, True)}" fill="#8A5A2B" stroke="{INK}" stroke-width="{f(sw*0.6)}"/>')
    # brillo
    h1, h2, h3 = R(-0.55, -0.55), R(-0.3, -0.82), R(0.05, -0.88)
    o.append(f'<path d="M {f(h1[0])} {f(h1[1])} Q {f(h2[0])} {f(h2[1])} {f(h3[0])} {f(h3[1])}" fill="none" stroke="#FFFFFF" stroke-width="{f(max(2.5, s*0.09))}" stroke-linecap="round" opacity="0.85"/>')
    return "".join(o)

def puff(cx, cy, s, seed=1, hull=True, shadow=False, sw=None):
    """Palomita: nube de lóbulos blancos (espuma de almidón) + trozos de cáscara."""
    rnd = random.Random(seed)
    sw = sw or max(4, s * 0.09)
    lobes = [(0, 0, 0.62)]
    n = 7
    for i in range(n):
        ang = 2 * math.pi * i / n + rnd.uniform(-0.3, 0.3)
        d = rnd.uniform(0.45, 0.62)
        lobes.append((d * math.cos(ang), d * math.sin(ang) * 0.85, rnd.uniform(0.34, 0.46)))
    o = []
    if shadow:
        o.append(f'<ellipse cx="{f(cx)}" cy="{f(cy+s*1.0)}" rx="{f(s*0.9)}" ry="{f(s*0.16)}" fill="{INK}" opacity="0.25"/>')
    o.append("".join(f'<circle cx="{f(cx+x*s)}" cy="{f(cy+y*s)}" r="{f(r*s+sw)}" fill="{INK}"/>' for x, y, r in lobes))
    o.append("".join(f'<circle cx="{f(cx+x*s)}" cy="{f(cy+y*s)}" r="{f(r*s)}" fill="url(#puffG)"/>' for x, y, r in lobes))
    # sombreado cálido en la base de cada lóbulo y textura
    for x, y, r in lobes[1:]:
        if y > 0:
            o.append(f'<circle cx="{f(cx+x*s)}" cy="{f(cy+y*s+r*s*0.25)}" r="{f(r*s*0.7)}" fill="#EBCB86" opacity="0.35"/>')
    for i in range(14):
        a0 = rnd.uniform(0, 6.28); d0 = rnd.uniform(0, 0.75)
        o.append(f'<circle cx="{f(cx+math.cos(a0)*d0*s)}" cy="{f(cy+math.sin(a0)*d0*s*0.85)}" r="{f(s*rnd.uniform(0.012,0.025))}" fill="#E4C27C" opacity="0.7"/>')
    # brillos
    for x, y, r in lobes[:4]:
        o.append(f'<circle cx="{f(cx+(x-r*0.35)*s)}" cy="{f(cy+(y-r*0.4)*s)}" r="{f(r*s*0.18)}" fill="#FFFFFF" opacity="0.9"/>')
    if hull:
        hx, hy = cx + s * 0.1, cy + s * 0.55
        hp = [(hx - s * 0.32, hy - s * 0.05), (hx + s * 0.3, hy - s * 0.1), (hx + s * 0.22, hy + s * 0.22), (hx + s * 0.02, hy + s * 0.4), (hx - s * 0.2, hy + s * 0.22)]
        o.append(f'<path d="{smooth(hp, True)}" fill="url(#kernG)" stroke="{INK}" stroke-width="{f(sw*0.8)}" stroke-linejoin="round"/>')
        o.append(f'<path d="M {f(hx-s*0.18)} {f(hy+s*0.02)} Q {f(hx)} {f(hy-s*0.04)} {f(hx+s*0.18)} {f(hy)}" fill="none" stroke="#FFFFFF" stroke-width="{f(max(2, s*0.05))}" stroke-linecap="round" opacity="0.8"/>')
    return "".join(o)

def flame(cx, base, h, w, col1="#5BB8FF", col2="#1E5BD8"):
    d = f"M {f(cx-w/2)} {f(base)} C {f(cx-w/2)} {f(base-h*0.5)}, {f(cx-w*0.1)} {f(base-h*0.6)}, {f(cx)} {f(base-h)} C {f(cx+w*0.1)} {f(base-h*0.6)}, {f(cx+w/2)} {f(base-h*0.5)}, {f(cx+w/2)} {f(base)} Z"
    di = f"M {f(cx-w/4)} {f(base)} C {f(cx-w/4)} {f(base-h*0.3)}, {f(cx)} {f(base-h*0.4)}, {f(cx)} {f(base-h*0.6)} C {f(cx)} {f(base-h*0.4)}, {f(cx+w/4)} {f(base-h*0.3)}, {f(cx+w/4)} {f(base)} Z"
    return f'<path d="{d}" fill="{col2}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/><path d="{di}" fill="{col1}"/>'

def steam(x, y, h, k=1, w=7):
    d = f"M {f(x)} {f(y)} C {f(x-18*k)} {f(y-h*0.3)}, {f(x+18*k)} {f(y-h*0.6)}, {f(x)} {f(y-h)}"
    return f'<path d="{d}" fill="none" stroke="#FFFFFF" stroke-width="{w}" stroke-linecap="round" opacity="0.75"/>'

def gauge(cx, cy, r, needle_id, val_angle, maxlab="10", label_txt="ATM", ticks=10):
    """Manómetro: escala de -120° (0) a +120° (max). La aguja va en un grupo cuyo bbox está centrado en el eje."""
    o = [f'<ellipse cx="{f(cx+8)}" cy="{f(cy+r+12)}" rx="{f(r*0.8)}" ry="{f(r*0.12)}" fill="{INK}" opacity="0.2"/>',
         f'<rect x="{f(cx-r*0.14)}" y="{f(cy+r*0.85)}" width="{f(r*0.28)}" height="{f(r*0.3)}" fill="url(#steelG)" stroke="{INK}" stroke-width="5"/>',
         f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="url(#steelG)" stroke="{INK}" stroke-width="7"/>',
         f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r*0.84)}" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/>']
    # zona roja
    a1, a2 = math.radians(60), math.radians(120)
    rr = r * 0.7
    o.append(f'<path d="M {f(cx+rr*math.sin(a1))} {f(cy-rr*math.cos(a1))} A {f(rr)} {f(rr)} 0 0 1 {f(cx+rr*math.sin(a2))} {f(cy-rr*math.cos(a2))}" fill="none" stroke="{CORAL}" stroke-width="{f(r*0.1)}"/>')
    for k in range(ticks + 1):
        a = math.radians(-120 + 240 * k / ticks)
        r1, r2 = r * 0.78, r * (0.62 if k % 5 == 0 else 0.68)
        o.append(f'<line x1="{f(cx+r1*math.sin(a))}" y1="{f(cy-r1*math.cos(a))}" x2="{f(cx+r2*math.sin(a))}" y2="{f(cy-r2*math.cos(a))}" stroke="{INK}" stroke-width="{4 if k % 5 == 0 else 2.5}" stroke-linecap="round"/>')
    o.append(T(cx - r * 0.42, cy + r * 0.5, "0", r * 0.17, INK))
    o.append(T(cx + r * 0.42, cy + r * 0.5, maxlab, r * 0.17, INK))
    o.append(T(cx, cy + r * 0.45, label_txt, r * 0.16, "#5A6170"))
    o.append(f'<path d="M {f(cx-r*0.6)} {f(cy-r*0.4)} A {f(r*0.72)} {f(r*0.72)} 0 0 1 {f(cx+r*0.1)} {f(cy-r*0.72)}" fill="none" stroke="#FFFFFF" stroke-width="{f(r*0.06)}" stroke-linecap="round" opacity="0.8"/>')
    L = r * 0.66
    a = math.radians(val_angle)
    tx, ty = cx + L * math.sin(a), cy - L * math.cos(a)
    bx, by = cx - L * 0.2 * math.sin(a), cy + L * 0.2 * math.cos(a)
    o.append(f'<g id="{needle_id}"><circle cx="{f(cx)}" cy="{f(cy)}" r="{f(L)}" fill="none" stroke="none"/>'
             f'<line x1="{f(bx)}" y1="{f(by)}" x2="{f(tx)}" y2="{f(ty)}" stroke="{INK}" stroke-width="{f(r*0.1)}" stroke-linecap="round"/>'
             f'<line x1="{f(bx)}" y1="{f(by)}" x2="{f(tx)}" y2="{f(ty)}" stroke="{CORAL}" stroke-width="{f(r*0.045)}" stroke-linecap="round"/></g>')
    o.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r*0.09)}" fill="{INK}"/>')
    return "".join(o)

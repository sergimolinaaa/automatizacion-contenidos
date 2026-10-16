"""Piezas compartidas para lote5b (Stroop y decreto ley)."""
import math, random, sys
sys.path.insert(0, "/tmp/claude-0/-home-user-automatizacion-contenidos/039df981-7a17-5355-b711-18510fb209db/scratchpad/lote5b")
from pol import *  # noqa
from lib import *  # noqa
from pol import arrow, label, T  # noqa

RED = "#E5262B"
BLUE = "#1F5BE8"
GREEN = "#12994A"
BLACK = "#15151F"
INKC = {"rojo": RED, "azul": BLUE, "verde": GREEN, "negro": BLACK}
SKIN = "#F3C6A2"


def stopwatch(cx, cy, r, hand_id, face="#FFFFFF", case="url(#steelG)", hand_col=CORAL, tick=True, angle=0):
    """Cronómetro con aguja en un grupo propio cuyo bbox está centrado en el eje (para 'spin')."""
    o = [f'<ellipse cx="{f(cx+8)}" cy="{f(cy+r+10)}" rx="{f(r*0.9)}" ry="{f(r*0.16)}" fill="{INK}" opacity="0.2"/>']
    # corona y botones
    o.append(f'<rect x="{f(cx-r*0.16)}" y="{f(cy-r-r*0.34)}" width="{f(r*0.32)}" height="{f(r*0.28)}" rx="{f(r*0.06)}" fill="{case}" stroke="{INK}" stroke-width="6"/>')
    o.append(f'<rect x="{f(cx-r*0.26)}" y="{f(cy-r-r*0.46)}" width="{f(r*0.52)}" height="{f(r*0.16)}" rx="{f(r*0.08)}" fill="{case}" stroke="{INK}" stroke-width="6"/>')
    bx, by = cx + r * math.cos(math.radians(-45)), cy + r * math.sin(math.radians(-45))
    o.append(f'<g transform="rotate(45 {f(bx)} {f(by)})"><rect x="{f(bx-r*0.1)}" y="{f(by-r*0.2)}" width="{f(r*0.2)}" height="{f(r*0.26)}" rx="{f(r*0.05)}" fill="{case}" stroke="{INK}" stroke-width="5"/></g>')
    o.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{case}" stroke="{INK}" stroke-width="7"/>')
    o.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r*0.82)}" fill="{face}" stroke="{INK}" stroke-width="5"/>')
    o.append(f'<path d="M {f(cx-r*0.6)} {f(cy-r*0.45)} A {f(r*0.75)} {f(r*0.75)} 0 0 1 {f(cx+r*0.2)} {f(cy-r*0.72)}" fill="none" stroke="#FFFFFF" stroke-width="{f(max(3, r*0.07))}" stroke-linecap="round" opacity="0.9"/>')
    if tick:
        for k in range(12):
            a = math.radians(k * 30)
            r1, r2 = r * 0.7, r * (0.58 if k % 3 == 0 else 0.64)
            o.append(f'<line x1="{f(cx+r1*math.sin(a))}" y1="{f(cy-r1*math.cos(a))}" x2="{f(cx+r2*math.sin(a))}" y2="{f(cy-r2*math.cos(a))}" stroke="{INK}" stroke-width="{4 if k % 3 == 0 else 2.5}" stroke-linecap="round"/>')
    L = r * 0.6
    a = math.radians(angle)
    tx, ty = cx + L * math.sin(a), cy - L * math.cos(a)
    bx2, by2 = cx - L * 0.25 * math.sin(a), cy + L * 0.25 * math.cos(a)
    o.append(f'<g id="{hand_id}"><circle cx="{f(cx)}" cy="{f(cy)}" r="{f(L)}" fill="none" stroke="none"/>'
             f'<line x1="{f(bx2)}" y1="{f(by2)}" x2="{f(tx)}" y2="{f(ty)}" stroke="{INK}" stroke-width="{f(max(7, r*0.11))}" stroke-linecap="round"/>'
             f'<line x1="{f(bx2)}" y1="{f(by2)}" x2="{f(tx)}" y2="{f(ty)}" stroke="{hand_col}" stroke-width="{f(max(3, r*0.05))}" stroke-linecap="round"/></g>')
    o.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(max(5, r*0.08))}" fill="{INK}"/>')
    return "".join(o)


STEEL_DEFS = lg("steelG", [(0, "#E9EDF3"), (0.5, "#B7C0CC"), (1, "#7D8794")]) + lg("brassG", [(0, "#F6D27A"), (0.5, "#D4A23A"), (1, "#8E6516")])


def burst(cx, cy, r1, r2, n=24, fill="url(#burstG)", sw=7):
    pts = []
    for i in range(n * 2):
        r = r1 if i % 2 == 0 else r2
        a = math.pi * i / n
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return f'<path d="M {" L ".join(f"{f(x)} {f(y)}" for x, y in pts)} Z" fill="{fill}" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"/>'


BURST_DEF = rg("burstG", [(0, "#E9FF8A"), (1, LIME)])


def stamp(cx, cy, text, col, size=54, rot=-8, w=None, h=None, font=None):
    """Sello de goma (doble marco). Rotación estática en un grupo interno."""
    font = font or DISP
    w = w or len(text) * size * 0.98 + 60
    h = h or size * 2.3
    x, y = cx - w / 2, cy - h / 2
    return (f'<g transform="rotate({rot} {f(cx)} {f(cy)})">'
            f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="14" fill="#FFFFFF" fill-opacity="0.82" stroke="{col}" stroke-width="10"/>'
            f'<rect x="{f(x+12)}" y="{f(y+12)}" width="{f(w-24)}" height="{f(h-24)}" rx="8" fill="none" stroke="{col}" stroke-width="4"/>'
            + T(cx, cy + size * 0.36, text, size, col, font=font) + "</g>")

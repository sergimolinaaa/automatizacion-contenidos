"""Piezas para «Qué anula tu papeleta» (reutiliza voto-blanco/vb.py -> pol, vc, partidos)."""
import sys, math
SP = "/tmp/claude-0/-home-user-automatizacion-contenidos/039df981-7a17-5355-b711-18510fb209db/scratchpad"
for p in (SP + "/voto-blanco", SP + "/lote5", SP + "/lote5/d", SP + "/voto-correo"):
    if p not in sys.path:
        sys.path.insert(0, p)
from vb import *  # noqa

BLUE = "#2D5BD1"
SEPIA = lg("sepiaG", [(0, "#F6E7C8"), (1, "#E2C99A")]) + lg("penG", [(0, "#3F6FE8"), (1, "#1F3F9E")], 0, 0, 1, 0)
PCOL = {"star": "#FFC83D", "circle": "#2EC4B6", "tri": "#FF7EB6", "square": "#C7894B", "diamond": "#9AA3B5"}
PNAME = {"star": "ESTRELLA", "circle": "CÍRCULO", "tri": "TRIÁNGULO", "square": "CUADRADO", "diamond": "ROMBO"}


def ballot(cx, cy, w, h, shape="star", rows=6, rot=0, nums=True, row_ids=False, title=True):
    """Papeleta del Congreso: cabecera con partido ficticio y lista numerada (nombres = barras grises)."""
    x, y = cx - w / 2, cy - h / 2
    col = PCOL[shape]
    s = f'<g transform="rotate({f(rot)} {f(cx)} {f(cy)})">'
    s += f'<rect x="{f(x+w*0.03)}" y="{f(y+h*0.025)}" width="{f(w)}" height="{f(h)}" rx="{f(w*0.025)}" fill="{INK}" opacity="0.2"/>'
    s += f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{f(w*0.025)}" fill="url(#paperB)" stroke="{INK}" stroke-width="{f(max(4,w*0.014))}"/>'
    hh = h * 0.2
    s += f'<rect x="{f(x+w*0.05)}" y="{f(y+h*0.04)}" width="{f(w*0.9)}" height="{f(hh)}" rx="{f(w*0.02)}" fill="{col}" stroke="{INK}" stroke-width="{f(max(3,w*0.01))}"/>'
    s += f'<circle cx="{f(x+w*0.05+hh*0.55)}" cy="{f(y+h*0.04+hh/2)}" r="{f(hh*0.36)}" fill="#FFFFFF" stroke="{INK}" stroke-width="{f(max(3,w*0.009))}"/>'
    s += icon(shape, x + w * 0.05 + hh * 0.55, y + h * 0.04 + hh / 2 + 1, hh * 0.22, col, sw=max(2, w * 0.007))
    if title:
        fs = min(hh * 0.36, w * 0.6 / (len(PNAME[shape]) * 0.85))
        s += T(x + w * 0.05 + hh * 1.05 + (w * 0.85 - hh * 1.05) / 2, y + h * 0.04 + hh / 2 + fs * 0.36, PNAME[shape], f(fs), INK, font=DISP)
    s += f'<path d="M {f(x+w*0.07)} {f(y+h*0.055)} L {f(x+w*0.07)} {f(y+h*0.04+hh-8)}" stroke="#FFFFFF" stroke-width="{f(max(3,w*0.01))}" stroke-linecap="round" opacity="0.7"/>'
    ys = []
    for i in range(rows):
        yy = y + h * 0.33 + i * (h * 0.62 / rows)
        ys.append(yy)
        sw = h * 0.032
        if nums:
            s += T(x + w * 0.12, yy + sw * 0.6, f"{i+1}", f(h * 0.05), "#5A6170")
        s += f'<path d="M {f(x+w*0.2)} {f(yy)} L {f(x+w*(0.86-0.12*(i%3)))} {f(yy)}" stroke="#9AA2B4" stroke-width="{f(sw)}" stroke-linecap="round"/>'
    s += "</g>"
    return s, ys


def pen(cx, cy, L, rot=35, id_=None):
    """Bolígrafo con la punta en (cx, cy)."""
    s = f'<g{f" id={chr(34)}{id_}{chr(34)}" if id_ else ""}><g transform="rotate({f(rot)} {f(cx)} {f(cy)})">'
    w = L * 0.11
    s += f'<ellipse cx="{f(cx+12)}" cy="{f(cy+L*0.55)}" rx="{f(w*0.7)}" ry="{f(L*0.45)}" fill="{INK}" opacity="0.15"/>'
    s += f'<path d="M {f(cx)} {f(cy)} L {f(cx-w*0.5)} {f(cy+L*0.12)} L {f(cx+w*0.5)} {f(cy+L*0.12)} Z" fill="#C9CED8" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    s += f'<rect x="{f(cx-w*0.5)}" y="{f(cy+L*0.12)}" width="{f(w)}" height="{f(L*0.88)}" rx="{f(w*0.3)}" fill="url(#penG)" stroke="{INK}" stroke-width="6"/>'
    s += f'<rect x="{f(cx-w*0.5)}" y="{f(cy+L*0.12)}" width="{f(w)}" height="{f(L*0.14)}" rx="4" fill="#E4E7EF" stroke="{INK}" stroke-width="5"/>'
    s += f'<path d="M {f(cx+w*0.62)} {f(cy+L*0.35)} L {f(cx+w*0.62)} {f(cy+L*0.7)}" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>'
    s += f'<path d="M {f(cx-w*0.2)} {f(cy+L*0.32)} L {f(cx-w*0.2)} {f(cy+L*0.92)}" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round" opacity="0.6"/>'
    return s + "</g></g>"


def scribble(x0, x1, yc, amp, n, col=CORAL, sw=10, id_=None):
    pts = [(x0 + (x1 - x0) * i / n, yc + (amp if i % 2 else -amp) * (0.7 + 0.3 * math.sin(i * 1.7))) for i in range(n + 1)]
    d = "M " + " L ".join(f"{f(a)} {f(b)}" for a, b in pts)
    return f'<g{f" id={chr(34)}{id_}{chr(34)}" if id_ else ""}><path d="{d}" fill="none" stroke="{col}" stroke-width="{f(sw)}" stroke-linecap="round" stroke-linejoin="round"/></g>'


def xmark(cx, cy, r, col=INK, sw=8, id_=None):
    return (f'<g{f" id={chr(34)}{id_}{chr(34)}" if id_ else ""}><path d="M {f(cx-r)} {f(cy-r)} L {f(cx+r)} {f(cy+r)} M {f(cx+r)} {f(cy-r)} L {f(cx-r)} {f(cy+r)}" '
            f'fill="none" stroke="{col}" stroke-width="{f(sw)}" stroke-linecap="round"/></g>')


def lock(cx, cy, s, id_=None):
    return (f'<g{f" id={chr(34)}{id_}{chr(34)}" if id_ else ""}>'
            f'<path d="M {f(cx-s*0.32)} {f(cy)} L {f(cx-s*0.32)} {f(cy-s*0.3)} A {f(s*0.32)} {f(s*0.32)} 0 0 1 {f(cx+s*0.32)} {f(cy-s*0.3)} L {f(cx+s*0.32)} {f(cy)}" fill="none" stroke="{INK}" stroke-width="{f(s*0.16)}"/>'
            f'<path d="M {f(cx-s*0.32)} {f(cy)} L {f(cx-s*0.32)} {f(cy-s*0.3)} A {f(s*0.32)} {f(s*0.32)} 0 0 1 {f(cx+s*0.32)} {f(cy-s*0.3)} L {f(cx+s*0.32)} {f(cy)}" fill="none" stroke="#C9CED8" stroke-width="{f(s*0.07)}"/>'
            f'<rect x="{f(cx-s*0.5)}" y="{f(cy-s*0.05)}" width="{f(s)}" height="{f(s*0.75)}" rx="{f(s*0.1)}" fill="url(#yelG)" stroke="{INK}" stroke-width="{f(s*0.07)}"/>'
            f'<circle cx="{f(cx)}" cy="{f(cy+s*0.25)}" r="{f(s*0.1)}" fill="{INK}"/><path d="M {f(cx)} {f(cy+s*0.3)} L {f(cx)} {f(cy+s*0.5)}" stroke="{INK}" stroke-width="{f(s*0.08)}" stroke-linecap="round"/>'
            f'<path d="M {f(cx-s*0.38)} {f(cy+s*0.05)} L {f(cx-s*0.38)} {f(cy+s*0.55)}" stroke="#FFFFFF" stroke-width="{f(s*0.06)}" stroke-linecap="round" opacity="0.7"/></g>')


def hdr(w, h):
    return header(w, h, SEPIA)

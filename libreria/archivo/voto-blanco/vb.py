"""Piezas para el vídeo del voto en blanco (reutiliza lote5/pol.py, lote5/d/partidos.py y voto-correo/vc.py)."""
import sys, math
SP = "/tmp/claude-0/-home-user-automatizacion-contenidos/039df981-7a17-5355-b711-18510fb209db/scratchpad"
for p in (SP + "/lote5", SP + "/lote5/d", SP + "/voto-correo"):
    if p not in sys.path:
        sys.path.insert(0, p)
from vc import *  # noqa  (pol + cert_envelope, check, stamp...)
from partidos import icon, COL as _COL  # noqa

# Partidos ficticios del ejemplo (provincia imaginaria de 30 escaños)
PARTIES = [  # nombre, color, forma, votos
    ("ESTRELLA", "#FFC83D", "star", 38000),
    ("CÍRCULO", "#2EC4B6", "circle", 30000),
    ("TRIÁNGULO", "#FF7EB6", "tri", 17900),
    ("CUADRADO", "#C7894B", "square", 10000),
    ("ROMBO", "#9AA3B5", "diamond", 3100),
]
COL = {p[0]: p[1] for p in PARTIES}
SHAPE = {p[0]: p[2] for p in PARTIES}
SEATS = 30


def dhondt(votes, seats, valid):
    ok = {n: v for n, v in votes.items() if v >= 0.03 * valid}
    q = sorted(((v / k, v, n) for n, v in ok.items() for k in range(1, seats + 1)), key=lambda t: (-t[0], -t[1]))[:seats]
    r = {n: 0 for n in votes}
    for t in q:
        r[t[2]] += 1
    return r


VOTES = {p[0]: p[3] for p in PARTIES}
ANTES = dhondt(VOTES, SEATS, 100000)    # 1.000 en blanco
DESPUES = dhondt(VOTES, SEATS, 109000)  # 10.000 en blanco

DEFS = (BASE_DEFS + EXTRA_DEFS + lg("woodH", [(0, "#D9A46C"), (1, "#9C6334")]) + lg("carpet", [(0, "#D2453B"), (1, "#9E2A24")])
        + lg("envF", [(0, "#FFFFFF"), (1, "#E4E7EF")]) + lg("envIn", [(0, "#8E96A8"), (1, "#C9CEDA")])
        + lg("paperB", [(0, "#FFFFFF"), (1, "#F1F2F6")]) + lg("cardG", [(0, "#FFFFFF"), (1, "#EEF1F6")])
        + lg("poleG", [(0, "#F4F6FA"), (1, "#9AA6BC")], 0, 0, 1, 0) + lg("colG", [(0, "#D5DAE6"), (1, "#7D879C")], 0, 0, 1, 0)
        + lg("sofaG", [(0, "#7FB2FF"), (1, "#3E6FD1")]) + lg("sofaD", [(0, "#4F82DE"), (1, "#2C55A8")]))


def g(id_, body):
    return f'<g id="{id_}">{body}</g>'


def envelope(cx, cy, w, h, paper=None):
    """Sobre de votación abierto (solapa arriba). paper: None (vacío) o svg de lo que asoma."""
    x0, y0 = cx - w / 2, cy - h / 2
    s = f'<ellipse cx="{f(cx+10)}" cy="{f(y0+h+12)}" rx="{f(w*0.55)}" ry="{f(h*0.08)}" fill="{INK}" opacity="0.2"/>'
    s += f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" rx="10" fill="url(#envIn)" stroke="{INK}" stroke-width="7"/>'
    s += f'<path d="M {f(x0+4)} {f(y0+4)} L {f(cx)} {f(y0-h*0.55)} L {f(x0+w-4)} {f(y0+4)} Z" fill="url(#envF)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
    s += f'<path d="M {f(x0+w*0.1)} {f(y0-4)} L {f(cx)} {f(y0-h*0.45)}" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>'
    if paper:
        s += paper
    s += (f'<path d="M {f(x0)} {f(y0+h*0.18)} L {f(cx)} {f(y0+h*0.62)} L {f(x0+w)} {f(y0+h*0.18)} L {f(x0+w)} {f(y0+h-10)} Q {f(x0+w)} {f(y0+h)} {f(x0+w-10)} {f(y0+h)} '
          f'L {f(x0+10)} {f(y0+h)} Q {f(x0)} {f(y0+h)} {f(x0)} {f(y0+h-10)} Z" fill="url(#envF)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
    s += f'<path d="M {f(x0+14)} {f(y0+h-16)} L {f(cx)} {f(y0+h*0.72)}" stroke="#C9CED8" stroke-width="4" stroke-linecap="round"/>'
    return s


def papeleta(cx, cy, w, h, rot=0, scribble=False):
    x, y = cx - w / 2, cy - h / 2
    s = f'<g transform="rotate({f(rot)} {f(cx)} {f(cy)})">'
    s += f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="6" fill="url(#paperB)" stroke="{INK}" stroke-width="6"/>'
    s += icon("star", cx, y + h * 0.2, w * 0.12, COL["ESTRELLA"], sw=4)
    for i in range(4):
        yy = y + h * (0.42 + i * 0.13)
        s += f'<path d="M {f(x+w*0.15)} {f(yy)} L {f(x+w*(0.85-0.1*(i%2)))} {f(yy)}" stroke="#9AA2B4" stroke-width="{f(h*0.035)}" stroke-linecap="round"/>'
    if scribble:
        pts = []
        for i in range(9):
            pts.append((x + w * (0.1 + 0.8 * i / 8), y + h * (0.25 if i % 2 == 0 else 0.85)))
        s += f'<path d="M {" L ".join(f"{f(a)} {f(b)}" for a, b in pts)}" fill="none" stroke="{CORAL}" stroke-width="{f(w*0.05)}" stroke-linecap="round" stroke-linejoin="round"/>'
    return s + "</g>"


def cross(cx, cy, r, id_=None):
    return (f'<g{f" id={chr(34)}{id_}{chr(34)}" if id_ else ""}><circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{CORAL}" stroke="{INK}" stroke-width="6"/>'
            f'<path d="M {f(cx-r*0.4)} {f(cy-r*0.4)} L {f(cx+r*0.4)} {f(cy+r*0.4)} M {f(cx+r*0.4)} {f(cy-r*0.4)} L {f(cx-r*0.4)} {f(cy+r*0.4)}" stroke="#FFFFFF" stroke-width="{f(r*0.24)}" stroke-linecap="round"/></g>')


def header(w, h, extra=""):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">\n<defs>{DEFS}{extra}</defs>'


if __name__ == "__main__":
    print(ANTES, DESPUES)


def stamp2(cx, cy, text, size, rot=-8, col=CORAL, id_=None):
    """Sello con ancho calculado para la fuente Unbounded (más ancha que la mono)."""
    w = len(text) * size * 0.86 + 50
    h = size * 1.7
    return (f'<g{f" id={chr(34)}{id_}{chr(34)}" if id_ else ""}><g transform="rotate({f(rot)} {f(cx)} {f(cy)})">'
            f'<rect x="{f(cx-w/2)}" y="{f(cy-h/2)}" width="{f(w)}" height="{f(h)}" rx="10" fill="#FFFFFF" fill-opacity="0.92" stroke="{col}" stroke-width="7"/>'
            f'<rect x="{f(cx-w/2+8)}" y="{f(cy-h/2+8)}" width="{f(w-16)}" height="{f(h-16)}" rx="6" fill="none" stroke="{col}" stroke-width="3"/>'
            + T(cx, cy + size * 0.36, text, size, col, font=DISP) + "</g></g>")

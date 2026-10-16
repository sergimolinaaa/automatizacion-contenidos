"""Piezas extra para el vídeo del voto por correo (reutiliza lote5/pol.py)."""
import sys, math
sys.path.insert(0, "/tmp/claude-0/-home-user-automatizacion-contenidos/039df981-7a17-5355-b711-18510fb209db/scratchpad/lote5")
from pol import *  # noqa

YEL = "#FFC928"
EXTRA_DEFS = (lg("certG", [(0, "#FFFFFF"), (1, "#E6E9F0")]) + lg("yelG", [(0, "#FFD95A"), (1, "#E8A800")])
              + lg("yelS", [(0, "#D79B00"), (1, "#A87500")]) + lg("dniG", [(0, "#DCEBFF"), (1, "#A9C6EE")])
              + lg("steelG", [(0, "#9AA6BC"), (1, "#5E6A82")]) + lg("steelD", [(0, "#6F7B93"), (1, "#3C465C")])
              + lg("sacaG", [(0, "#E9D7A6"), (1, "#BFA36A")]) + lg("kraft", [(0, "#F4F0E6"), (1, "#DCD5C3")]))


def cert_envelope(cx, cy, w, h, rot=0, band=True, id_=None, text="CERTIFICADO", franq=True):
    """Sobre grande de correo certificado (cara frontal, cerrado) con banda y sello."""
    x, y = cx - w / 2, cy - h / 2
    g = f'<g{f" id={chr(34)}{id_}{chr(34)}" if id_ else ""} transform="rotate({f(rot)} {f(cx)} {f(cy)})">'
    g += f'<rect x="{f(x+10)}" y="{f(y+14)}" width="{f(w)}" height="{f(h)}" rx="12" fill="{INK}" opacity="0.22"/>'
    g += f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="12" fill="url(#certG)" stroke="{INK}" stroke-width="7"/>'
    g += f'<path d="M {f(x+8)} {f(y+8)} L {f(cx)} {f(y+h*0.5)} L {f(x+w-8)} {f(y+8)}" fill="none" stroke="#C3C8D4" stroke-width="5" stroke-linejoin="round"/>'
    g += f'<path d="M {f(x+18)} {f(y+h-18)} L {f(x+w*0.35)} {f(y+h*0.62)} M {f(x+w-18)} {f(y+h-18)} L {f(x+w*0.65)} {f(y+h*0.62)}" stroke="#D3D7E0" stroke-width="4" stroke-linecap="round"/>'
    # sello de franqueo (esquina)
    sx, sy, ss = x + w - w * 0.2, y + h * 0.1, w * 0.13
    if franq:
        g += f'<rect x="{f(sx)}" y="{f(sy)}" width="{f(ss)}" height="{f(ss*1.2)}" rx="4" fill="{LIME}" stroke="{INK}" stroke-width="4" stroke-dasharray="6 4"/>'
        g += f'<circle cx="{f(sx-ss*0.25)}" cy="{f(sy+ss*0.7)}" r="{f(ss*0.55)}" fill="none" stroke="#6B7280" stroke-width="3" opacity="0.8"/>'
    # líneas de dirección
    for i in range(3):
        g += f'<path d="M {f(x+w*0.38)} {f(y+h*(0.58+i*0.11))} L {f(x+w*(0.8-i*0.08))} {f(y+h*(0.58+i*0.11))}" stroke="#8A93A6" stroke-width="{f(max(4,h*0.03))}" stroke-linecap="round"/>'
    if band:
        bh = h * 0.2
        g += f'<rect x="{f(x+w*0.06)}" y="{f(y+h*0.12)}" width="{f(w*0.58)}" height="{f(bh)}" rx="6" fill="{CORAL}" stroke="{INK}" stroke-width="4"/>'
        fs = min(bh * 0.55, w * 0.52 / (len(text) * 0.82))
        g += T(x + w * 0.35, y + h * 0.12 + bh / 2 + fs * 0.36, text, f(fs), "#FFFFFF", font=DISP)
    g += f'<path d="M {f(x+14)} {f(y+16)} L {f(x+14)} {f(y+h*0.5)}" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round" opacity="0.9"/>'
    return g + "</g>"


def dni(cx, cy, w, rot=0, id_=None):
    h = w * 0.63
    x, y = cx - w / 2, cy - h / 2
    g = f'<g{f" id={chr(34)}{id_}{chr(34)}" if id_ else ""} transform="rotate({f(rot)} {f(cx)} {f(cy)})">'
    g += f'<rect x="{f(x+8)}" y="{f(y+10)}" width="{f(w)}" height="{f(h)}" rx="{f(w*0.06)}" fill="{INK}" opacity="0.22"/>'
    g += f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{f(w*0.06)}" fill="url(#dniG)" stroke="{INK}" stroke-width="6"/>'
    g += f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h*0.2)}" rx="{f(w*0.06)}" fill="#3C5FAE" stroke="{INK}" stroke-width="5"/>'
    g += T(x + w * 0.5, y + h * 0.15, "DNI", h * 0.13, "#FFFFFF", font=DISP)
    # foto
    px, py, pw, ph = x + w * 0.07, y + h * 0.3, w * 0.27, h * 0.58
    g += f'<rect x="{f(px)}" y="{f(py)}" width="{f(pw)}" height="{f(ph)}" rx="6" fill="#EEF2F8" stroke="{INK}" stroke-width="4"/>'
    g += f'<circle cx="{f(px+pw/2)}" cy="{f(py+ph*0.38)}" r="{f(pw*0.22)}" fill="#7C8AA5"/>'
    g += f'<path d="M {f(px+pw*0.12)} {f(py+ph)} Q {f(px+pw/2)} {f(py+ph*0.5)} {f(px+pw*0.88)} {f(py+ph)} Z" fill="#7C8AA5"/>'
    # chip y líneas
    g += f'<rect x="{f(x+w*0.42)}" y="{f(y+h*0.32)}" width="{f(w*0.14)}" height="{f(h*0.17)}" rx="4" fill="#E2B84C" stroke="{INK}" stroke-width="3"/>'
    for i in range(3):
        g += f'<path d="M {f(x+w*0.42)} {f(y+h*(0.62+i*0.12))} L {f(x+w*(0.9-i*0.1))} {f(y+h*(0.62+i*0.12))}" stroke="#4E5D7A" stroke-width="{f(h*0.04)}" stroke-linecap="round"/>'
    g += f'<path d="M {f(x+w*0.62)} {f(y+h*0.3)} L {f(x+w*0.9)} {f(y+h*0.3)} M {f(x+w*0.62)} {f(y+h*0.42)} L {f(x+w*0.82)} {f(y+h*0.42)}" stroke="#4E5D7A" stroke-width="{f(h*0.035)}" stroke-linecap="round"/>'
    return g + "</g>"


def check(cx, cy, r, id_=None, col=LIME):
    return (f'<g{f" id={chr(34)}{id_}{chr(34)}" if id_ else ""}><circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{col}" stroke="{INK}" stroke-width="6"/>'
            f'<path d="M {f(cx-r*0.45)} {f(cy)} L {f(cx-r*0.1)} {f(cy+r*0.38)} L {f(cx+r*0.5)} {f(cy-r*0.38)}" fill="none" stroke="{INK}" stroke-width="{f(r*0.22)}" stroke-linecap="round" stroke-linejoin="round"/></g>')


def stamp(cx, cy, text, size, rot=-8, col=CORAL, id_=None):
    w = text_w(text, size) + 10
    h = size * 1.7
    return (f'<g{f" id={chr(34)}{id_}{chr(34)}" if id_ else ""}><g transform="rotate({f(rot)} {f(cx)} {f(cy)})">'
            f'<rect x="{f(cx-w/2)}" y="{f(cy-h/2)}" width="{f(w)}" height="{f(h)}" rx="10" fill="#FFFFFF" fill-opacity="0.92" stroke="{col}" stroke-width="7"/>'
            f'<rect x="{f(cx-w/2+8)}" y="{f(cy-h/2+8)}" width="{f(w-16)}" height="{f(h-16)}" rx="6" fill="none" stroke="{col}" stroke-width="3"/>'
            + T(cx, cy + size * 0.36, text, size, col, font=DISP) + "</g></g>")


def saca(cx, base, w, h, id_=None):
    """Saca de correos (bolsa de lona) con sobres asomando."""
    x0 = cx - w / 2
    top = base - h
    g = f'<g{f" id={chr(34)}{id_}{chr(34)}" if id_ else ""}>'
    g += f'<ellipse cx="{f(cx)}" cy="{f(base+4)}" rx="{f(w*0.6)}" ry="{f(w*0.08)}" fill="{INK}" opacity="0.22"/>'
    # sobres asomando
    for k, (dx, rot) in enumerate(((-0.22, -14), (0.02, 6), (0.22, 18))):
        g += sobre(cx + dx * w, top + h * 0.06, w * 0.38, w * 0.26, rot, sw=4)
    body = (f"M {f(x0+w*0.12)} {f(top+h*0.12)} C {f(x0-w*0.08)} {f(top+h*0.5)}, {f(x0-w*0.04)} {f(base)}, {f(x0+w*0.2)} {f(base)}"
            f" L {f(x0+w*0.8)} {f(base)} C {f(x0+w*1.04)} {f(base)}, {f(x0+w*1.08)} {f(top+h*0.5)}, {f(x0+w*0.88)} {f(top+h*0.12)} Z")
    g += f'<path d="{body}" fill="url(#sacaG)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
    g += f'<path d="M {f(x0+w*0.1)} {f(top+h*0.14)} Q {f(cx)} {f(top+h*0.26)} {f(x0+w*0.9)} {f(top+h*0.14)}" fill="none" stroke="#8A6D36" stroke-width="10" stroke-linecap="round"/>'
    g += f'<path d="M {f(x0+w*0.14)} {f(top+h*0.32)} C {f(x0+w*0.04)} {f(top+h*0.6)}, {f(x0+w*0.08)} {f(base-h*0.12)}, {f(x0+w*0.2)} {f(base-h*0.06)}" fill="none" stroke="#FFF6DA" stroke-width="7" stroke-linecap="round" opacity="0.8"/>'
    # placa con sobre
    g += f'<rect x="{f(cx-w*0.22)}" y="{f(top+h*0.45)}" width="{f(w*0.44)}" height="{f(h*0.26)}" rx="8" fill="{YEL}" stroke="{INK}" stroke-width="5"/>'
    g += sobre(cx, top + h * 0.58, w * 0.26, h * 0.15, 0, fill="#FFFFFF", sw=3.5)
    return g + "</g>"

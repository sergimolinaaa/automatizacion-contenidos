"""Piezas para «¿Qué propone Vox?» (reutiliza nuevo-partido/np.py). Color neutro de marca: azul pizarra, nada de verde."""
import sys
sys.path.insert(0, "/tmp/claude-0/-home-user-automatizacion-contenidos/039df981-7a17-5355-b711-18510fb209db/scratchpad/nuevo-partido")
from np import *  # noqa

NAVY = "#2B3A5C"
VX_DEFS = NP_DEFS + lg("navyG", [(0, "#4A5D8A"), (1, "#24304D")]) + lg("docG", [(0, "#FFFFFF"), (1, "#E9ECF3")]) \
    + lg("lensG", [(0, "#EAF8FF", 0.7), (1, "#9FD3F2", 0.45)]) + lg("houseW", [(0, "#FFE3C2"), (1, "#F2BF8A")]) \
    + lg("roofG", [(0, "#E86A4A"), (1, "#B8432A")]) + lg("coinG", [(0, "#FFE27A"), (1, "#E2A400")]) \
    + lg("stoneG", [(0, "#F4F1EA"), (1, "#D6D0C2")])


def plate(cx, cy, w, h, text, size):
    """Placa de siglas en letras (sin logotipo del partido), color neutro."""
    return (f'<rect x="{f(cx-w/2+7)}" y="{f(cy-h/2+9)}" width="{f(w)}" height="{f(h)}" rx="{f(h*0.22)}" fill="{INK}" opacity="0.25"/>'
            f'<rect x="{f(cx-w/2)}" y="{f(cy-h/2)}" width="{f(w)}" height="{f(h)}" rx="{f(h*0.22)}" fill="url(#navyG)" stroke="{INK}" stroke-width="6"/>'
            f'<path d="M {f(cx-w/2+14)} {f(cy-h/2+12)} L {f(cx+w/2-14)} {f(cy-h/2+12)}" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" opacity="0.45"/>'
            + T(cx, cy + size * 0.36, text, f(size), "#FFFFFF", font=DISP))


def lectern_vx(cx, base, w, h, mic=True):
    """Atril de frente con la palabra VOX en letras sobre placa neutra."""
    top = base - h
    tw = w * 1.18
    o = f'<ellipse cx="{f(cx)}" cy="{f(base+6)}" rx="{f(w*0.75)}" ry="{f(w*0.09)}" fill="{INK}" opacity="0.28"/>'
    body = f"M {f(cx-w/2)} {f(base)} L {f(cx-w*0.42)} {f(top+h*0.12)} L {f(cx+w*0.42)} {f(top+h*0.12)} L {f(cx+w/2)} {f(base)} Z"
    o += f'<path d="{body}" fill="url(#lectG)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
    o += f'<path d="M {f(cx-w*0.36)} {f(top+h*0.2)} L {f(cx-w*0.42)} {f(base-14)}" stroke="#7F8EB0" stroke-width="8" stroke-linecap="round" opacity="0.8"/>'
    if mic:
        mx = cx + w * 0.18
        d = f"M {f(mx)} {f(top+h*0.04)} C {f(mx)} {f(top-h*0.12)}, {f(mx-w*0.08)} {f(top-h*0.2)}, {f(mx-w*0.14)} {f(top-h*0.26)}"
        o += f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="9" stroke-linecap="round"/><path d="{d}" fill="none" stroke="#9AA3B5" stroke-width="3" stroke-linecap="round"/>'
        o += f'<ellipse cx="{f(mx-w*0.16)}" cy="{f(top-h*0.3)}" rx="{f(w*0.05)}" ry="{f(w*0.07)}" transform="rotate(-40 {f(mx-w*0.16)} {f(top-h*0.3)})" fill="url(#micG)" stroke="{INK}" stroke-width="5"/>'
    o += f'<path d="M {f(cx-tw/2)} {f(top+h*0.14)} L {f(cx-tw/2+w*0.06)} {f(top)} L {f(cx+tw/2-w*0.06)} {f(top)} L {f(cx+tw/2)} {f(top+h*0.14)} Z" fill="url(#lectTop)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
    o += f'<path d="M {f(cx-tw/2+w*0.1)} {f(top+h*0.04)} L {f(cx+tw/2-w*0.1)} {f(top+h*0.04)}" stroke="#A9B7D6" stroke-width="4" stroke-linecap="round"/>'
    o += plate(cx, top + h * 0.48, w * 0.62, h * 0.24, "VOX", h * 0.14)
    return o


def doc(cx, cy, w, h, title, sub, rot=0, band="url(#navyG)", lines=6):
    """Documento grapado (programa electoral)."""
    x, y = cx - w / 2, cy - h / 2
    o = f'<g transform="rotate({f(rot)} {f(cx)} {f(cy)})">'
    o += f'<rect x="{f(x+22)}" y="{f(y+8)}" width="{f(w)}" height="{f(h)}" rx="10" fill="#DDE1EA" stroke="{INK}" stroke-width="5"/>'
    o += f'<rect x="{f(x+12)}" y="{f(y+16)}" width="{f(w)}" height="{f(h)}" rx="10" fill="{INK}" opacity="0.22"/>'
    o += f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="10" fill="url(#docG)" stroke="{INK}" stroke-width="7"/>'
    bh = h * 0.27
    o += f'<path d="M {f(x)} {f(y+bh)} L {f(x)} {f(y+10)} Q {f(x)} {f(y)} {f(x+10)} {f(y)} L {f(x+w-10)} {f(y)} Q {f(x+w)} {f(y)} {f(x+w)} {f(y+10)} L {f(x+w)} {f(y+bh)} Z" fill="{band}" stroke="{INK}" stroke-width="7"/>'
    fs = min(bh * 0.36, w * 0.86 / (len(title) * 0.82))
    o += T(cx, y + bh * 0.46, title, f(fs), "#FFFFFF", font=DISP)
    fs2 = min(bh * 0.3, w * 0.8 / (len(sub) * 0.82))
    o += T(cx, y + bh * 0.86, sub, f(fs2), LIME, font=DISP)
    for i in range(lines):
        yy = y + bh + (h - bh) * (0.14 + i * 0.8 / lines)
        o += f'<path d="M {f(x+w*0.12)} {f(yy)} L {f(x+w*(0.88 - (0.2 if i % 3 == 2 else 0)))} {f(yy)}" stroke="#AEB6C6" stroke-width="{f(max(5,h*0.025))}" stroke-linecap="round"/>'
    o += f'<rect x="{f(x+w*0.08)}" y="{f(y-8)}" width="{f(w*0.12)}" height="16" rx="4" fill="#9AA3B5" stroke="{INK}" stroke-width="4"/>'
    o += f'<path d="M {f(x+12)} {f(y+bh+14)} L {f(x+12)} {f(y+h-16)}" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round" opacity="0.9"/>'
    return o + "</g>"


def lupa(cx, cy, r, ang=40):
    import math
    a = math.radians(ang)
    hx, hy = cx + r * math.cos(a), cy + r * math.sin(a)
    ex, ey = cx + r * 2.1 * math.cos(a), cy + r * 2.1 * math.sin(a)
    return (f'<path d="M {f(hx)} {f(hy)} L {f(ex)} {f(ey)}" stroke="{INK}" stroke-width="{f(r*0.42)}" stroke-linecap="round"/>'
            f'<path d="M {f(hx+r*0.15*math.cos(a))} {f(hy+r*0.15*math.sin(a))} L {f(ex)} {f(ey)}" stroke="#7A4E28" stroke-width="{f(r*0.26)}" stroke-linecap="round"/>'
            f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="url(#lensG)" stroke="{INK}" stroke-width="{f(r*0.18)}"/>'
            f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r*0.82)}" fill="none" stroke="#9AA3B5" stroke-width="{f(r*0.08)}"/>'
            f'<path d="M {f(cx-r*0.55)} {f(cy-r*0.15)} A {f(r*0.58)} {f(r*0.58)} 0 0 1 {f(cx-r*0.1)} {f(cy-r*0.58)}" fill="none" stroke="#FFFFFF" stroke-width="{f(r*0.12)}" stroke-linecap="round"/>')


def house(cx, base, w):
    h = w * 0.62
    x = cx - w / 2
    o = f'<rect x="{f(x+6)}" y="{f(base-h+8)}" width="{f(w)}" height="{f(h)}" fill="{INK}" opacity="0.2"/>'
    o += f'<rect x="{f(x)}" y="{f(base-h)}" width="{f(w)}" height="{f(h)}" fill="url(#houseW)" stroke="{INK}" stroke-width="5"/>'
    o += f'<path d="M {f(x-w*0.12)} {f(base-h+4)} L {f(cx)} {f(base-h-w*0.42)} L {f(x+w*1.12)} {f(base-h+4)} Z" fill="url(#roofG)" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    o += f'<rect x="{f(cx-w*0.12)}" y="{f(base-h*0.62)}" width="{f(w*0.24)}" height="{f(h*0.62)}" rx="4" fill="#8A5A31" stroke="{INK}" stroke-width="4"/>'
    o += f'<circle cx="{f(cx+w*0.07)}" cy="{f(base-h*0.3)}" r="3.5" fill="{YEL}"/>'
    for k in (-1, 1):
        o += f'<rect x="{f(cx+k*w*0.32-w*0.09)}" y="{f(base-h*0.75)}" width="{f(w*0.18)}" height="{f(w*0.16)}" rx="3" fill="#BFE6FF" stroke="{INK}" stroke-width="4"/>'
    return o


def clock(cx, cy, r, txt="48 H"):
    o = f'<circle cx="{f(cx+4)}" cy="{f(cy+5)}" r="{f(r)}" fill="{INK}" opacity="0.25"/>'
    o += f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/>'
    o += f'<path d="M {f(cx)} {f(cy)} L {f(cx)} {f(cy-r*0.65)} M {f(cx)} {f(cy)} L {f(cx+r*0.5)} {f(cy+r*0.2)}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
    o += f'<circle cx="{f(cx)}" cy="{f(cy)}" r="4" fill="{CORAL}"/>'
    return o

"""Piezas para el vídeo del partido nuevo (reutiliza voto-correo/vc.py -> lote5/pol.py -> lib.py)."""
import sys, math, random
sys.path.insert(0, "/tmp/claude-0/-home-user-automatizacion-contenidos/039df981-7a17-5355-b711-18510fb209db/scratchpad/voto-correo")
from vc import *  # noqa

TEAL, TEAL_D = "#1FB5A8", "#0E7C74"
VIO = "#7B5CFF"
NP_DEFS = (EXTRA_DEFS + lg("tealG", [(0, "#38D3C4"), (1, "#0E8E84")]) + lg("tealS", [(0, "#13968B"), (1, "#0A5F58")])
           + lg("lectG", [(0, "#4A5878"), (1, "#252F47")]) + lg("lectTop", [(0, "#6D7DA0"), (1, "#3E4B69")])
           + lg("calG", [(0, "#FFFFFF"), (1, "#EEF0F5")]) + lg("calR", [(0, "#FF7A5C"), (1, "#E23C1C")])
           + lg("cardG", [(0, "#FFFFFF"), (1, "#EEF1F7")]) + lg("clipG", [(0, "#C99764"), (1, "#9B6B3D")])
           + lg("bulbG", [(0, "#FFF6B8"), (1, "#FFD23A")]) + lg("folderG", [(0, "#FFD976"), (1, "#E8AE2E")])
           + lg("micG", [(0, "#8C96AA"), (1, "#3D4558")]) + rg("spotR", [(0, "#FFF7D6", 0.55), (1, "#FFF7D6", 0)])
           + lg("personG", [(0, "#8C9BB8"), (1, "#5D6B88")]))


def G(id_, body, extra=""):
    return f'<g id="{id_}"{extra}>{body}</g>'


def logo(cx, cy, r, sw=6):
    """Logo genérico: círculo turquesa con las letras D21 (sin símbolos de partido real)."""
    return (f'<circle cx="{f(cx+r*0.08)}" cy="{f(cy+r*0.1)}" r="{f(r)}" fill="{INK}" opacity="0.22"/>'
            f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="url(#tealG)" stroke="{INK}" stroke-width="{sw}"/>'
            f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r*0.8)}" fill="none" stroke="#FFFFFF" stroke-width="{f(max(2,r*0.04))}" opacity="0.6"/>'
            + T(cx, cy + r * 0.2, "D21", f(r * 0.6), "#FFFFFF", font=DISP)
            + f'<path d="M {f(cx-r*0.62)} {f(cy-r*0.35)} A {f(r*0.72)} {f(r*0.72)} 0 0 1 {f(cx-r*0.1)} {f(cy-r*0.7)}" fill="none" stroke="#FFFFFF" stroke-width="{f(r*0.09)}" stroke-linecap="round" opacity="0.75"/>')


def lectern(cx, base, w, h, mic=True):
    """Atril de mitin visto de frente con logo D21 y micrófono."""
    top = base - h
    tw = w * 1.18
    o = f'<ellipse cx="{f(cx)}" cy="{f(base+6)}" rx="{f(w*0.75)}" ry="{f(w*0.09)}" fill="{INK}" opacity="0.28"/>'
    body = f"M {f(cx-w/2)} {f(base)} L {f(cx-w*0.42)} {f(top+h*0.12)} L {f(cx+w*0.42)} {f(top+h*0.12)} L {f(cx+w/2)} {f(base)} Z"
    o += f'<path d="{body}" fill="url(#lectG)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
    o += f'<path d="M {f(cx-w*0.36)} {f(top+h*0.2)} L {f(cx-w*0.42)} {f(base-14)}" stroke="#7F8EB0" stroke-width="8" stroke-linecap="round" opacity="0.8"/>'
    if mic:
        mx, my = cx + w * 0.18, top - h * 0.02
        o += f'<path d="M {f(mx)} {f(top+h*0.04)} C {f(mx)} {f(top-h*0.12)}, {f(mx-w*0.08)} {f(top-h*0.2)}, {f(mx-w*0.14)} {f(top-h*0.26)}" fill="none" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>'
        o += f'<path d="M {f(mx)} {f(top+h*0.04)} C {f(mx)} {f(top-h*0.12)}, {f(mx-w*0.08)} {f(top-h*0.2)}, {f(mx-w*0.14)} {f(top-h*0.26)}" fill="none" stroke="#9AA3B5" stroke-width="3" stroke-linecap="round"/>'
        o += f'<ellipse cx="{f(mx-w*0.16)}" cy="{f(top-h*0.3)}" rx="{f(w*0.05)}" ry="{f(w*0.07)}" transform="rotate(-40 {f(mx-w*0.16)} {f(top-h*0.3)})" fill="url(#micG)" stroke="{INK}" stroke-width="5"/>'
    # tablero superior inclinado
    o += f'<path d="M {f(cx-tw/2)} {f(top+h*0.14)} L {f(cx-tw/2+w*0.06)} {f(top)} L {f(cx+tw/2-w*0.06)} {f(top)} L {f(cx+tw/2)} {f(top+h*0.14)} Z" fill="url(#lectTop)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
    o += f'<path d="M {f(cx-tw/2+w*0.1)} {f(top+h*0.04)} L {f(cx+tw/2-w*0.1)} {f(top+h*0.04)}" stroke="#A9B7D6" stroke-width="4" stroke-linecap="round"/>'
    o += logo(cx, top + h * 0.5, w * 0.27)
    return o


def person_icon(cx, cy, s, col="url(#personG)", sw=5):
    """Silueta genérica (pictograma), no representa a nadie real."""
    return (f'<circle cx="{f(cx)}" cy="{f(cy-s*0.42)}" r="{f(s*0.24)}" fill="{col}" stroke="{INK}" stroke-width="{sw}"/>'
            f'<path d="M {f(cx-s*0.42)} {f(cy+s*0.5)} C {f(cx-s*0.42)} {f(cy-s*0.1)}, {f(cx+s*0.42)} {f(cy-s*0.1)}, {f(cx+s*0.42)} {f(cy+s*0.5)} Z" fill="{col}" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"/>')


def card(cx, cy, w, h, title, sub, icon, accent=TEAL, rot=0, tsize=34, ssize=20):
    x, y = cx - w / 2, cy - h / 2
    o = f'<g transform="rotate({f(rot)} {f(cx)} {f(cy)})">'
    o += f'<rect x="{f(x+9)}" y="{f(y+11)}" width="{f(w)}" height="{f(h)}" rx="18" fill="{INK}" opacity="0.25"/>'
    o += f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="18" fill="url(#cardG)" stroke="{INK}" stroke-width="6"/>'
    o += f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="16" rx="8" fill="{accent}" stroke="{INK}" stroke-width="4"/>'
    o += icon
    o += T(cx, y + h - 54, title, tsize, INK, font=DISP)
    o += T(cx, y + h - 22, sub, ssize, "#5A6170")
    # chincheta
    o += f'<circle cx="{f(cx)}" cy="{f(y+8)}" r="12" fill="{CORAL}" stroke="{INK}" stroke-width="4"/><circle cx="{f(cx-4)}" cy="{f(y+4)}" r="4" fill="#FFFFFF" opacity="0.8"/>'
    return o + "</g>"


def cal_page(cx, cy, w, h, month, day, id_=None, rot=0, col="url(#calR)"):
    """Hoja de calendario de taco con anillas."""
    x, y = cx - w / 2, cy - h / 2
    o = f'<g{f" id={chr(34)}{id_}{chr(34)}" if id_ else ""}><g transform="rotate({f(rot)} {f(cx)} {f(cy)})">'
    o += f'<rect x="{f(x+10)}" y="{f(y+12)}" width="{f(w)}" height="{f(h)}" rx="16" fill="{INK}" opacity="0.25"/>'
    o += f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="16" fill="url(#calG)" stroke="{INK}" stroke-width="7"/>'
    o += f'<path d="M {f(x)} {f(y+h*0.3)} L {f(x)} {f(y+16)} Q {f(x)} {f(y)} {f(x+16)} {f(y)} L {f(x+w-16)} {f(y)} Q {f(x+w)} {f(y)} {f(x+w)} {f(y+16)} L {f(x+w)} {f(y+h*0.3)} Z" fill="{col}" stroke="{INK}" stroke-width="7"/>'
    o += T(cx, y + h * 0.22, month, f(h * 0.13), "#FFFFFF", font=DISP)
    o += T(cx, y + h * 0.82, day, f(h * 0.44), INK, font=DISP)
    for k in (-1, 1):
        o += f'<rect x="{f(cx+k*w*0.28-9)}" y="{f(y-22)}" width="18" height="44" rx="9" fill="#9AA3B5" stroke="{INK}" stroke-width="5"/>'
    return o + "</g></g>"


def bulb(cx, cy, s):
    return (f'<path d="M {f(cx-s*0.5)} {f(cy-s*0.1)} C {f(cx-s*0.5)} {f(cy-s*0.85)}, {f(cx+s*0.5)} {f(cy-s*0.85)}, {f(cx+s*0.5)} {f(cy-s*0.1)} C {f(cx+s*0.5)} {f(cy+s*0.2)}, {f(cx+s*0.22)} {f(cy+s*0.3)}, {f(cx+s*0.22)} {f(cy+s*0.5)} L {f(cx-s*0.22)} {f(cy+s*0.5)} C {f(cx-s*0.22)} {f(cy+s*0.3)}, {f(cx-s*0.5)} {f(cy+s*0.2)}, {f(cx-s*0.5)} {f(cy-s*0.1)} Z" fill="url(#bulbG)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
            f'<rect x="{f(cx-s*0.25)}" y="{f(cy+s*0.5)}" width="{f(s*0.5)}" height="{f(s*0.3)}" rx="6" fill="#9AA3B5" stroke="{INK}" stroke-width="6"/>'
            f'<path d="M {f(cx-s*0.25)} {f(cy+s*0.62)} L {f(cx+s*0.25)} {f(cy+s*0.62)}" stroke="{INK}" stroke-width="4"/>'
            f'<path d="M {f(cx-s*0.12)} {f(cy+s*0.45)} L {f(cx-s*0.12)} {f(cy+s*0.05)} L {f(cx)} {f(cy+s*0.18)} L {f(cx+s*0.12)} {f(cy+s*0.05)} L {f(cx+s*0.12)} {f(cy+s*0.45)}" fill="none" stroke="#C08A00" stroke-width="5" stroke-linejoin="round"/>'
            f'<path d="M {f(cx-s*0.32)} {f(cy-s*0.3)} C {f(cx-s*0.3)} {f(cy-s*0.5)}, {f(cx-s*0.15)} {f(cy-s*0.6)}, {f(cx)} {f(cy-s*0.62)}" fill="none" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round" opacity="0.85"/>')


def rays(cx, cy, r1, r2, n=8, col=YEL, w=10):
    o = ""
    for i in range(n):
        a = math.radians(180 + i * 180 / (n - 1))
        o += dbl(f"M {f(cx+r1*math.cos(a))} {f(cy+r1*math.sin(a))} L {f(cx+r2*math.cos(a))} {f(cy+r2*math.sin(a))}", w, col, 7)
    return o


def folder(cx, cy, w, h, text="ESTATUTOS"):
    x, y = cx - w / 2, cy - h / 2
    o = f'<rect x="{f(x+9)}" y="{f(y+11)}" width="{f(w)}" height="{f(h)}" rx="12" fill="{INK}" opacity="0.25"/>'
    o += f'<path d="M {f(x)} {f(y+18)} L {f(x)} {f(y)} L {f(x+w*0.36)} {f(y)} L {f(x+w*0.44)} {f(y+18)} Z" fill="#E8AE2E" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
    # hojas asomando
    o += f'<rect x="{f(x+w*0.08)}" y="{f(y+4)}" width="{f(w*0.8)}" height="{f(h*0.5)}" rx="6" fill="#FFFFFF" stroke="{INK}" stroke-width="5" transform="rotate(-4 {f(cx)} {f(cy)})"/>'
    o += f'<rect x="{f(x)}" y="{f(y+18)}" width="{f(w)}" height="{f(h-18)}" rx="12" fill="url(#folderG)" stroke="{INK}" stroke-width="6"/>'
    o += f'<path d="M {f(x+14)} {f(y+34)} L {f(x+14)} {f(y+h-16)}" stroke="#FFF1B8" stroke-width="7" stroke-linecap="round"/>'
    fs = min(h * 0.17, w * 0.8 / (len(text) * 0.8))
    o += f'<rect x="{f(cx-w*0.38)}" y="{f(cy+h*0.04)}" width="{f(w*0.76)}" height="{f(fs*1.6)}" rx="6" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/>'
    o += T(cx, cy + h * 0.04 + fs * 1.15, text, f(fs), INK, font=DISP)
    return o


def confetti(seed, box, n, cols=(TEAL, CORAL, YEL, LIME, VIO, "#FFFFFF")):
    rnd = random.Random(seed)
    x0, y0, x1, y1 = box
    o = ""
    for i in range(n):
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
        c = cols[i % len(cols)]
        r = rnd.uniform(0, 180)
        if i % 3 == 0:
            o += f'<circle cx="{f(x)}" cy="{f(y)}" r="9" fill="{c}" stroke="{INK}" stroke-width="3"/>'
        else:
            o += f'<rect x="{f(x-12)}" y="{f(y-5)}" width="24" height="10" rx="3" fill="{c}" stroke="{INK}" stroke-width="3" transform="rotate({f(r)} {f(x)} {f(y)})"/>'
    return o

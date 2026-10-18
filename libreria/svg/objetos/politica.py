"""Piezas de política (ya aprobadas en los vídeos del 29-N): urna, papeletas Congreso/Senado, sobres, DNI, saca de correos,
hemiciclo con escaños, calendario de taco, atril, documento/programa, carpeta, partidos ficticios y D'Hondt.

Sale de: lote5/pol.py (urna, sobre, hemiciclo), lote5/d/partidos.py (iconos, D'Hondt), voto-correo/vc.py (sobre certificado,
DNI, saca, check), voto-blanco/vb.py (sobre abierto, papeleta simple), papeleta-nula/pn.py y senado.py (papeletas, boli,
garabato, candado), nuevo-partido/np.py (atril, calendario, carpeta, logo genérico), vox/vx.py (documento, placa de siglas).

NEUTRALIDAD: solo partidos ficticios de colores (Estrella, Círculo, Triángulo, Cuadrado, Rombo); nada de logos reales.
"""
import math
import random
from ..base import (INK, LIME, CORAL, YEL, TEAL, f, g, gt, T, MONO, DISP, shade, text_w, trazo, sombra, sombra_caja, brillo,
                    lg, rg, registrar_defs, degradado, Pieza, icono_ok)

registrar_defs(
    lg("urnaGlass", [(0, "#EAF8FF", 0.75), (1, "#9FD3F2", 0.55)])
    + lg("urnaSide", [(0, "#C4E6FA", 0.7), (1, "#7DB8DE", 0.6)])
    + lg("urnaLid", [(0, "#5A6B8C"), (1, "#2C3954")])
    + lg("sobreG", [(0, "#FFFFFF"), (1, "#E3E6EE")])
    + lg("envF", [(0, "#FFFFFF"), (1, "#E4E7EF")]) + lg("envIn", [(0, "#8E96A8"), (1, "#C9CEDA")])
    + lg("paperB", [(0, "#FFFFFF"), (1, "#F1F2F6")])
    + lg("certG", [(0, "#FFFFFF"), (1, "#E6E9F0")]) + lg("dniG", [(0, "#DCEBFF"), (1, "#A9C6EE")])
    + lg("sacaG", [(0, "#E9D7A6"), (1, "#BFA36A")])
    + lg("sepiaG", [(0, "#F6E7C8"), (1, "#E2C99A")]) + lg("penG", [(0, "#3F6FE8"), (1, "#1F3F9E")], 0, 0, 1, 0)
    + lg("tealG", [(0, "#38D3C4"), (1, "#0E8E84")])
    + lg("lectG", [(0, "#4A5878"), (1, "#252F47")]) + lg("lectTop", [(0, "#6D7DA0"), (1, "#3E4B69")])
    + lg("calG", [(0, "#FFFFFF"), (1, "#EEF0F5")]) + lg("calR", [(0, "#FF7A5C"), (1, "#E23C1C")])
    + lg("folderG", [(0, "#FFD976"), (1, "#E8AE2E")]) + lg("micG", [(0, "#8C96AA"), (1, "#3D4558")])
    + lg("navyG", [(0, "#4A5D8A"), (1, "#24304D")]) + lg("docG", [(0, "#FFFFFF"), (1, "#E9ECF3")])
    + lg("yelG", [(0, "#FFD95A"), (1, "#E8A800")])
)

# ------------------------------------------------------------------ partidos ficticios
PARTIDOS = [  # nombre, color, forma
    ("ESTRELLA", "#FFC83D", "star"),
    ("CÍRCULO", "#2EC4B6", "circle"),
    ("TRIÁNGULO", "#FF7EB6", "tri"),
    ("CUADRADO", "#C7894B", "square"),
    ("ROMBO", "#9AA3B5", "diamond"),
]
COLOR = {p[2]: p[1] for p in PARTIDOS}      # forma -> color
NOMBRE = {p[2]: p[0] for p in PARTIDOS}     # forma -> nombre
FORMA = {p[0]: p[2] for p in PARTIDOS}      # nombre -> forma


def icono_partido(forma, cx, cy, s, col=None, sw=5):
    """Icono de partido ficticio: forma ('star', 'circle', 'tri', 'square', 'diamond') con contorno y brillo. s ≈ radio."""
    col = col or COLOR[forma]
    hl = shade(col, 0.45)
    if forma == "circle":
        return (f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(s)}" fill="{col}" stroke="{INK}" stroke-width="{sw}"/>'
                f'<circle cx="{f(cx-s*0.35)}" cy="{f(cy-s*0.35)}" r="{f(s*0.25)}" fill="{hl}"/>')
    if forma == "square":
        return (f'<rect x="{f(cx-s*0.9)}" y="{f(cy-s*0.9)}" width="{f(s*1.8)}" height="{f(s*1.8)}" rx="{f(s*0.2)}" fill="{col}" stroke="{INK}" stroke-width="{sw}"/>'
                f'<rect x="{f(cx-s*0.6)}" y="{f(cy-s*0.6)}" width="{f(s*0.45)}" height="{f(s*0.3)}" rx="3" fill="{hl}"/>')
    if forma == "tri":
        P = [(cx, cy - s * 1.1), (cx + s * 1.05, cy + s * 0.8), (cx - s * 1.05, cy + s * 0.8)]
        return (f'<path d="M {" L ".join(f"{f(x)} {f(y)}" for x, y in P)} Z" fill="{col}" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"/>'
                f'<circle cx="{f(cx-s*0.15)}" cy="{f(cy-s*0.2)}" r="{f(s*0.18)}" fill="{hl}"/>')
    if forma == "diamond":
        P = [(cx, cy - s * 1.1), (cx + s * 0.95, cy), (cx, cy + s * 1.1), (cx - s * 0.95, cy)]
        return (f'<path d="M {" L ".join(f"{f(x)} {f(y)}" for x, y in P)} Z" fill="{col}" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"/>'
                f'<circle cx="{f(cx-s*0.2)}" cy="{f(cy-s*0.3)}" r="{f(s*0.14)}" fill="{hl}"/>')
    P = []
    for i in range(10):
        r = s * 1.15 if i % 2 == 0 else s * 0.5
        a = -math.pi / 2 + i * math.pi / 5
        P.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return (f'<path d="M {" L ".join(f"{f(x)} {f(y)}" for x, y in P)} Z" fill="{col}" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"/>'
            f'<circle cx="{f(cx-s*0.15)}" cy="{f(cy-s*0.25)}" r="{f(s*0.16)}" fill="{hl}"/>')


def chip_partido(id_, cx, cy, forma, texto=None, size=30):
    """Ficha redonda con el icono + nombre debajo (leyendas, repartos)."""
    s = (f'<circle cx="{f(cx+4)}" cy="{f(cy+6)}" r="{f(size*1.25)}" fill="{INK}" opacity="0.22"/>'
         f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(size*1.25)}" fill="#FFFFFF" stroke="{INK}" stroke-width="6"/>'
         + icono_partido(forma, cx, cy + 1, size * 0.72, sw=4))
    if texto is not False:
        t = texto or NOMBRE[forma]
        s += T(cx, cy + size * 2.25, t, size * 0.72, "#FFFFFF", font=DISP, extra=f'stroke="{INK}" stroke-width="5" paint-order="stroke"')
    return g(id_, s)


def dhondt(votos, escanos, umbral=0.03, validos=None):
    """Reparto D'Hondt (LOREG art. 163). votos = {nombre: votos}. validos = votos válidos (incluye blancos) para el umbral.
    Devuelve ({nombre: escaños}, lista de cocientes ganadores (cociente, votos, nombre, divisor))."""
    validos = validos or sum(votos.values())
    ok = {n: v for n, v in votos.items() if v >= umbral * validos}
    q = sorted(((v / k, v, n, k) for n, v in ok.items() for k in range(1, escanos + 1)), key=lambda t: (-t[0], -t[1]))[:escanos]
    r = {n: 0 for n in votos}
    for t in q:
        r[t[2]] += 1
    return r, q


def miles(v):
    """12345 -> '12.345' (formato español)."""
    return f"{int(round(v)):,}".replace(",", ".")


# ------------------------------------------------------------------ sobres y papeletas
def sobre(cx, cy, w, h, rot_=0, fill="url(#sobreG)", sw=5, id_=None):
    """Sobre de votación cerrado visto de frente (con solapa)."""
    x, y = cx - w / 2, cy - h / 2
    b = f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="5" fill="{fill}" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"/>'
    b += f'<path d="M {f(x+4)} {f(y+4)} L {f(cx)} {f(y+h*0.55)} L {f(x+w-4)} {f(y+4)}" fill="none" stroke="#B9BFCC" stroke-width="{f(sw*0.7)}" stroke-linejoin="round"/>'
    return gt(id_, f"rotate({f(rot_)} {f(cx)} {f(cy)})", b)


def sobre_abierto(id_, cx, cy, w, h, dentro=None):
    """Sobre de votación abierto (solapa arriba). dentro: SVG de lo que asoma (p. ej. una papeleta) o None (vacío)."""
    x0, y0 = cx - w / 2, cy - h / 2
    s = sombra(cx + 10, y0 + h + 12, w * 0.55, h * 0.08, 0.2)
    s += f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" rx="10" fill="url(#envIn)" stroke="{INK}" stroke-width="7"/>'
    s += f'<path d="M {f(x0+4)} {f(y0+4)} L {f(cx)} {f(y0-h*0.55)} L {f(x0+w-4)} {f(y0+4)} Z" fill="url(#envF)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
    s += brillo(f"M {f(x0+w*0.1)} {f(y0-4)} L {f(cx)} {f(y0-h*0.45)}", 5, 1)
    if dentro:
        s += dentro
    s += (f'<path d="M {f(x0)} {f(y0+h*0.18)} L {f(cx)} {f(y0+h*0.62)} L {f(x0+w)} {f(y0+h*0.18)} L {f(x0+w)} {f(y0+h-10)} Q {f(x0+w)} {f(y0+h)} {f(x0+w-10)} {f(y0+h)} '
          f'L {f(x0+10)} {f(y0+h)} Q {f(x0)} {f(y0+h)} {f(x0)} {f(y0+h-10)} Z" fill="url(#envF)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
    s += f'<path d="M {f(x0+14)} {f(y0+h-16)} L {f(cx)} {f(y0+h*0.72)}" stroke="#C9CED8" stroke-width="4" stroke-linecap="round"/>'
    return g(id_, s)


def papeleta(id_, cx, cy, w, h, rot_=0, forma="star", tachada=False):
    """Papeleta sencilla (icono + líneas). tachada=True: garabato coral encima (nula)."""
    x, y = cx - w / 2, cy - h / 2
    s = f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="6" fill="url(#paperB)" stroke="{INK}" stroke-width="6"/>'
    s += icono_partido(forma, cx, y + h * 0.2, w * 0.12, sw=4)
    for i in range(4):
        yy = y + h * (0.42 + i * 0.13)
        s += f'<path d="M {f(x+w*0.15)} {f(yy)} L {f(x+w*(0.85-0.1*(i%2)))} {f(yy)}" stroke="#9AA2B4" stroke-width="{f(h*0.035)}" stroke-linecap="round"/>'
    if tachada:
        P = [(x + w * (0.1 + 0.8 * i / 8), y + h * (0.25 if i % 2 == 0 else 0.85)) for i in range(9)]
        s += f'<path d="M {" L ".join(f"{f(a)} {f(b)}" for a, b in P)}" fill="none" stroke="{CORAL}" stroke-width="{f(w*0.05)}" stroke-linecap="round" stroke-linejoin="round"/>'
    return gt(id_, f"rotate({f(rot_)} {f(cx)} {f(cy)})", s)


def papeleta_congreso(id_, cx, cy, w, h, forma="star", filas=6, rot_=0, numeros=True, titulo=True):
    """Papeleta del Congreso: cabecera con partido ficticio y lista cerrada numerada (nombres = barras grises).
    Devuelve Pieza con .puntos['filas'] = y de cada fila (sin rotación)."""
    x, y = cx - w / 2, cy - h / 2
    col = COLOR[forma]
    s = f'<rect x="{f(x+w*0.03)}" y="{f(y+h*0.025)}" width="{f(w)}" height="{f(h)}" rx="{f(w*0.025)}" fill="{INK}" opacity="0.2"/>'
    s += f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{f(w*0.025)}" fill="url(#paperB)" stroke="{INK}" stroke-width="{f(max(4,w*0.014))}"/>'
    hh = h * 0.2
    s += f'<rect x="{f(x+w*0.05)}" y="{f(y+h*0.04)}" width="{f(w*0.9)}" height="{f(hh)}" rx="{f(w*0.02)}" fill="{col}" stroke="{INK}" stroke-width="{f(max(3,w*0.01))}"/>'
    s += f'<circle cx="{f(x+w*0.05+hh*0.55)}" cy="{f(y+h*0.04+hh/2)}" r="{f(hh*0.36)}" fill="#FFFFFF" stroke="{INK}" stroke-width="{f(max(3,w*0.009))}"/>'
    s += icono_partido(forma, x + w * 0.05 + hh * 0.55, y + h * 0.04 + hh / 2 + 1, hh * 0.22, col, sw=max(2, w * 0.007))
    if titulo:
        fs = min(hh * 0.36, w * 0.6 / (len(NOMBRE[forma]) * 0.85))
        s += T(x + w * 0.05 + hh * 1.05 + (w * 0.85 - hh * 1.05) / 2, y + h * 0.04 + hh / 2 + fs * 0.36, NOMBRE[forma], fs, INK, font=DISP)
    s += brillo(f"M {f(x+w*0.07)} {f(y+h*0.055)} L {f(x+w*0.07)} {f(y+h*0.04+hh-8)}", max(3, w * 0.01), 0.7)
    ys = []
    for i in range(filas):
        yy = y + h * 0.33 + i * (h * 0.62 / filas)
        ys.append(yy)
        if numeros:
            s += T(x + w * 0.12, yy + h * 0.02, f"{i+1}", h * 0.05, "#5A6170")
        s += f'<path d="M {f(x+w*0.2)} {f(yy)} L {f(x+w*(0.86-0.12*(i%3)))} {f(yy)}" stroke="#9AA2B4" stroke-width="{f(h*0.032)}" stroke-linecap="round"/>'
    return Pieza(gt(id_, f"rotate({f(rot_)} {f(cx)} {f(cy)})", s), {"filas": ys}, (x, y, x + w, y + h))


def papeleta_senado(id_, cx, cy, w=600, h=700, formas=("star", "circle", "tri", "square", "diamond", "star"), cruces=(), col_cruz="#2D5BD1"):
    """Papeleta del Senado (color sepia, lista abierta con casillas). cruces = índices de fila marcados con ✗ azul
    (cada cruz en su grupo id_+'_c<i>'). Devuelve Pieza con .puntos['casillas'] = [(x, y)…]."""
    x0, y0 = cx - w / 2, cy - h / 2
    k = w / 600
    b = f'<rect x="{f(x0+16*k)}" y="{f(y0+18*k)}" width="{f(w)}" height="{f(h)}" rx="{f(14*k)}" fill="{INK}" opacity="0.2"/>'
    b += f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" rx="{f(14*k)}" fill="url(#sepiaG)" stroke="{INK}" stroke-width="{f(8*k)}"/>'
    b += f'<rect x="{f(x0+30*k)}" y="{f(y0+28*k)}" width="{f(w-60*k)}" height="{f(92*k)}" rx="{f(10*k)}" fill="#8B5E34" stroke="{INK}" stroke-width="{f(6*k)}"/>'
    b += T(cx, y0 + 92 * k, "SENADO", 50 * k, "#FFF4DD", font=DISP)
    cas = []
    step = (h - 210 * k) / max(1, len(formas))
    for i, sh in enumerate(formas):
        yy = y0 + 180 * k + i * step
        cas.append((x0 + 78 * k, yy))
        b += f'<rect x="{f(x0+48*k)}" y="{f(yy-30*k)}" width="{f(60*k)}" height="{f(60*k)}" rx="{f(8*k)}" fill="#FFFFFF" stroke="{INK}" stroke-width="{f(6*k)}"/>'
        b += f'<circle cx="{f(x0+160*k)}" cy="{f(yy)}" r="{f(30*k)}" fill="#FFFFFF" stroke="{INK}" stroke-width="{f(5*k)}"/>' + icono_partido(sh, x0 + 160 * k, yy + 1, 18 * k, sw=3)
        b += f'<path d="M {f(x0+215*k)} {f(yy)} L {f(x0+w-(60 if i%2 else 130)*k)} {f(yy)}" stroke="#A88A5E" stroke-width="{f(22*k)}" stroke-linecap="round"/>'
    for j, i in enumerate(cruces):
        xx, yy = cas[i]
        b += g(f"{id_}_c{j+1}", f'<path d="M {f(xx-22*k)} {f(yy-22*k)} L {f(xx+22*k)} {f(yy+22*k)} M {f(xx+22*k)} {f(yy-22*k)} L {f(xx-22*k)} {f(yy+22*k)}" fill="none" stroke="{col_cruz}" stroke-width="{f(10*k)}" stroke-linecap="round"/>')
    return Pieza(g(id_, b), {"casillas": cas}, (x0, y0, x0 + w, y0 + h))


def sobre_certificado(id_, cx, cy, w, h, rot_=0, banda=True, texto="CERTIFICADO", franqueo=True):
    """Sobre grande de correo certificado (voto por correo) con banda coral y sello de franqueo."""
    x, y = cx - w / 2, cy - h / 2
    b = f'<rect x="{f(x+10)}" y="{f(y+14)}" width="{f(w)}" height="{f(h)}" rx="12" fill="{INK}" opacity="0.22"/>'
    b += f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="12" fill="url(#certG)" stroke="{INK}" stroke-width="7"/>'
    b += f'<path d="M {f(x+8)} {f(y+8)} L {f(cx)} {f(y+h*0.5)} L {f(x+w-8)} {f(y+8)}" fill="none" stroke="#C3C8D4" stroke-width="5" stroke-linejoin="round"/>'
    b += f'<path d="M {f(x+18)} {f(y+h-18)} L {f(x+w*0.35)} {f(y+h*0.62)} M {f(x+w-18)} {f(y+h-18)} L {f(x+w*0.65)} {f(y+h*0.62)}" stroke="#D3D7E0" stroke-width="4" stroke-linecap="round"/>'
    sx, sy, ss = x + w - w * 0.2, y + h * 0.1, w * 0.13
    if franqueo:
        b += f'<rect x="{f(sx)}" y="{f(sy)}" width="{f(ss)}" height="{f(ss*1.2)}" rx="4" fill="{LIME}" stroke="{INK}" stroke-width="4" stroke-dasharray="6 4"/>'
        b += f'<circle cx="{f(sx-ss*0.25)}" cy="{f(sy+ss*0.7)}" r="{f(ss*0.55)}" fill="none" stroke="#6B7280" stroke-width="3" opacity="0.8"/>'
    for i in range(3):
        b += f'<path d="M {f(x+w*0.38)} {f(y+h*(0.58+i*0.11))} L {f(x+w*(0.8-i*0.08))} {f(y+h*(0.58+i*0.11))}" stroke="#8A93A6" stroke-width="{f(max(4,h*0.03))}" stroke-linecap="round"/>'
    if banda:
        bh = h * 0.2
        b += f'<rect x="{f(x+w*0.06)}" y="{f(y+h*0.12)}" width="{f(w*0.58)}" height="{f(bh)}" rx="6" fill="{CORAL}" stroke="{INK}" stroke-width="4"/>'
        fs = min(bh * 0.55, w * 0.52 / (len(texto) * 0.82))
        b += T(x + w * 0.35, y + h * 0.12 + bh / 2 + fs * 0.36, texto, fs, "#FFFFFF", font=DISP)
    b += brillo(f"M {f(x+14)} {f(y+16)} L {f(x+14)} {f(y+h*0.5)}", 6, 0.9)
    return gt(id_, f"rotate({f(rot_)} {f(cx)} {f(cy)})", b)


def dni(id_, cx, cy, w, rot_=0):
    """DNI genérico (foto de silueta, chip, líneas)."""
    h = w * 0.63
    x, y = cx - w / 2, cy - h / 2
    b = f'<rect x="{f(x+8)}" y="{f(y+10)}" width="{f(w)}" height="{f(h)}" rx="{f(w*0.06)}" fill="{INK}" opacity="0.22"/>'
    b += f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{f(w*0.06)}" fill="url(#dniG)" stroke="{INK}" stroke-width="6"/>'
    b += f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h*0.2)}" rx="{f(w*0.06)}" fill="#3C5FAE" stroke="{INK}" stroke-width="5"/>'
    b += T(x + w * 0.5, y + h * 0.15, "DNI", h * 0.13, "#FFFFFF", font=DISP)
    px, py, pw, ph = x + w * 0.07, y + h * 0.3, w * 0.27, h * 0.58
    b += f'<rect x="{f(px)}" y="{f(py)}" width="{f(pw)}" height="{f(ph)}" rx="6" fill="#EEF2F8" stroke="{INK}" stroke-width="4"/>'
    b += f'<circle cx="{f(px+pw/2)}" cy="{f(py+ph*0.38)}" r="{f(pw*0.22)}" fill="#7C8AA5"/>'
    b += f'<path d="M {f(px+pw*0.12)} {f(py+ph)} Q {f(px+pw/2)} {f(py+ph*0.5)} {f(px+pw*0.88)} {f(py+ph)} Z" fill="#7C8AA5"/>'
    b += f'<rect x="{f(x+w*0.42)}" y="{f(y+h*0.32)}" width="{f(w*0.14)}" height="{f(h*0.17)}" rx="4" fill="#E2B84C" stroke="{INK}" stroke-width="3"/>'
    for i in range(3):
        b += f'<path d="M {f(x+w*0.42)} {f(y+h*(0.62+i*0.12))} L {f(x+w*(0.9-i*0.1))} {f(y+h*(0.62+i*0.12))}" stroke="#4E5D7A" stroke-width="{f(h*0.04)}" stroke-linecap="round"/>'
    b += f'<path d="M {f(x+w*0.62)} {f(y+h*0.3)} L {f(x+w*0.9)} {f(y+h*0.3)} M {f(x+w*0.62)} {f(y+h*0.42)} L {f(x+w*0.82)} {f(y+h*0.42)}" stroke="#4E5D7A" stroke-width="{f(h*0.035)}" stroke-linecap="round"/>'
    return gt(id_, f"rotate({f(rot_)} {f(cx)} {f(cy)})", b)


def saca(id_, cx, base, w, h):
    """Saca de Correos (bolsa de lona) con sobres asomando y placa amarilla."""
    x0, top = cx - w / 2, base - h
    s = sombra(cx, base + 4, w * 0.6, w * 0.08, 0.22)
    for dx, r_ in ((-0.22, -14), (0.02, 6), (0.22, 18)):
        s += sobre(cx + dx * w, top + h * 0.06, w * 0.38, w * 0.26, r_, sw=4)
    body = (f"M {f(x0+w*0.12)} {f(top+h*0.12)} C {f(x0-w*0.08)} {f(top+h*0.5)}, {f(x0-w*0.04)} {f(base)}, {f(x0+w*0.2)} {f(base)}"
            f" L {f(x0+w*0.8)} {f(base)} C {f(x0+w*1.04)} {f(base)}, {f(x0+w*1.08)} {f(top+h*0.5)}, {f(x0+w*0.88)} {f(top+h*0.12)} Z")
    s += f'<path d="{body}" fill="url(#sacaG)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
    s += f'<path d="M {f(x0+w*0.1)} {f(top+h*0.14)} Q {f(cx)} {f(top+h*0.26)} {f(x0+w*0.9)} {f(top+h*0.14)}" fill="none" stroke="#8A6D36" stroke-width="10" stroke-linecap="round"/>'
    s += brillo(f"M {f(x0+w*0.14)} {f(top+h*0.32)} C {f(x0+w*0.04)} {f(top+h*0.6)}, {f(x0+w*0.08)} {f(base-h*0.12)}, {f(x0+w*0.2)} {f(base-h*0.06)}", 7, 0.8, "#FFF6DA")
    s += f'<rect x="{f(cx-w*0.22)}" y="{f(top+h*0.45)}" width="{f(w*0.44)}" height="{f(h*0.26)}" rx="8" fill="{YEL}" stroke="{INK}" stroke-width="5"/>'
    s += sobre(cx, top + h * 0.58, w * 0.26, h * 0.15, 0, fill="#FFFFFF", sw=3.5)
    return g(id_, s)


# ------------------------------------------------------------------ urna y hemiciclo
def urna(id_, cx, base, w, h, texto=None, n_sobres=6, seed=1, placa="#FFFFFF"):
    """Urna transparente en vista 3/4 con sobres dentro. base = y del suelo.
    Devuelve Pieza con .puntos['ranura'] = (x, y) de la ranura (para que un sobre «entre»: move hacia ahí)."""
    rnd = random.Random(seed)
    d = w * 0.26
    dx, dy = d * 0.75, -d * 0.55
    x0, y0 = cx - w / 2 - dx / 2, base - h
    o = [sombra(cx + dx / 2, base + 4, w * 0.62, w * 0.07)]
    side = f"M {f(x0+w)} {f(y0)} L {f(x0+w+dx)} {f(y0+dy)} L {f(x0+w+dx)} {f(base+dy)} L {f(x0+w)} {f(base)} Z"
    o.append(f'<path d="{side}" fill="url(#urnaSide)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
    for i in range(n_sobres):
        sx = x0 + w * (0.18 + 0.68 * rnd.random()) + dx * 0.3
        sy = base - h * (0.08 + 0.22 * rnd.random()) - (i % 3) * 6
        o.append(sobre(sx, sy, w * 0.3, w * 0.2, rnd.uniform(-35, 35), sw=3.5))
    o.append(f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" fill="url(#urnaGlass)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
    o.append(brillo(f"M {f(x0+w*0.12)} {f(y0+h*0.15)} L {f(x0+w*0.12)} {f(y0+h*0.8)}", w * 0.05, 0.8))
    o.append(brillo(f"M {f(x0+w*0.22)} {f(y0+h*0.15)} L {f(x0+w*0.22)} {f(y0+h*0.45)}", w * 0.025, 0.7))
    lt = max(14, h * 0.09)
    top = f"M {f(x0)} {f(y0)} L {f(x0+dx)} {f(y0+dy)} L {f(x0+w+dx)} {f(y0+dy)} L {f(x0+w)} {f(y0)} Z"
    o.append(f'<path d="{top}" fill="#7E8FB0" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
    o.append(f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(lt)}" fill="url(#urnaLid)" stroke="{INK}" stroke-width="6"/>')
    o.append(f'<path d="M {f(x0+w)} {f(y0)} L {f(x0+w+dx)} {f(y0+dy)} L {f(x0+w+dx)} {f(y0+dy+lt)} L {f(x0+w)} {f(y0+lt)} Z" fill="#26324A" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
    o.append(f'<path d="M {f(x0+8)} {f(y0+4)} L {f(x0+w-8)} {f(y0+4)}" stroke="#A9B8D6" stroke-width="3" stroke-linecap="round"/>')
    mx, my = x0 + w / 2 + dx / 2, y0 + dy / 2
    sl = w * 0.36
    o.append(f'<path d="M {f(mx-sl/2)} {f(my)} L {f(mx+sl/2)} {f(my)}" stroke="{INK}" stroke-width="{f(max(8, w*0.035))}" stroke-linecap="round"/>')
    o.append(f'<path d="M {f(x0+w+dx)} {f(y0+dy+lt)} L {f(x0+w+dx)} {f(base+dy)}" stroke="{INK}" stroke-width="6"/>')
    if texto:
        size = max(18, min(30, w * 0.085))
        tw_ = text_w(texto, size) - 20
        o.append(f'<rect x="{f(cx-tw_/2)}" y="{f(y0+h*0.42)}" width="{f(tw_)}" height="{f(size*1.6)}" rx="8" fill="{placa}" stroke="{INK}" stroke-width="4"/>')
        o.append(T(cx, y0 + h * 0.42 + size * 1.13, texto, size))
    return Pieza(g(id_, "".join(o)), {"ranura": (mx, my)}, (x0, y0 + dy, x0 + w + dx, base))


def posiciones_hemiciclo(n, filas, r0, r1, sr=0):
    """Posiciones (ángulo, radio) de n escaños en `filas` arcos, ordenadas de izquierda a derecha."""
    radii = [r0 + (r1 - r0) * i / max(1, filas - 1) for i in range(filas)]
    tot = sum(radii)
    counts = [round(n * r / tot) for r in radii]
    while sum(counts) > n:
        counts[counts.index(max(counts))] -= 1
    while sum(counts) < n:
        counts[-1] += 1
    seats = []
    for r, c in zip(radii, counts):
        for k in range(c):
            m = math.asin(min(0.9, (sr + 8) / r)) if sr else 0
            a = m + (math.pi - 2 * m) * (k / (c - 1)) if c > 1 else math.pi / 2
            seats.append((a, r))
    seats.sort(key=lambda s: (-s[0], s[1]))
    return seats


def hemiciclo(id_, cx, cy, n, filas, r0, r1, colores, r_esc=None, sw=4, ids=False, suelo=True):
    """Hemiciclo (vista frontal en abanico) de n escaños. colores: lista (uno por escaño, izq→dcha) o un color.
    (cx, cy) = centro del arco (abajo). ids=True: cada escaño en su grupo id_+'_e<i>' (para animarlos de uno en uno).
    Devuelve Pieza con .puntos['escanos'] = [(x, y)…]."""
    r_esc = r_esc or max(6, (r1 - r0) / max(1, filas) * 0.42)
    if isinstance(colores, str):
        colores = [colores] * n
    out = ""
    if suelo:
        out += f'<path d="M {f(cx-r1-r_esc*2.2)} {f(cy+r_esc)} A {f(r1+r_esc*2.2)} {f(r1+r_esc*2.2)} 0 0 1 {f(cx+r1+r_esc*2.2)} {f(cy+r_esc)} Z" fill="{degradado("#D2453B", 0.15)}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
        out += f'<path d="M {f(cx-r0+r_esc*2)} {f(cy+r_esc)} A {f(r0-r_esc*2)} {f(r0-r_esc*2)} 0 0 1 {f(cx+r0-r_esc*2)} {f(cy+r_esc)} Z" fill="{degradado("#D9A46C", 0.2)}" stroke="{INK}" stroke-width="6"/>'
    pos = []
    for i, (a, r) in enumerate(posiciones_hemiciclo(n, filas, r0, r1, r_esc)):
        x, y = cx + r * math.cos(a), cy - r * math.sin(a)
        c = colores[i]
        s = (f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r_esc)}" fill="{c}" stroke="{INK}" stroke-width="{sw}"/>'
             f'<circle cx="{f(x-r_esc*0.3)}" cy="{f(y-r_esc*0.35)}" r="{f(r_esc*0.28)}" fill="#FFFFFF" opacity="0.55"/>')
        out += g(f"{id_}_e{i}", s) if ids else s
        pos.append((x, y))
    return Pieza(g(id_, out), {"escanos": pos}, (cx - r1 - r_esc, cy - r1 - r_esc, cx + r1 + r_esc, cy + r_esc))


def colores_reparto(reparto, orden=None):
    """{forma o nombre: escaños} → lista de colores izq→dcha para hemiciclo()."""
    out = []
    for k in (orden or reparto.keys()):
        forma = FORMA.get(k, k)
        out += [COLOR.get(forma, "#CCCCCC")] * reparto[k]
    return out


# ------------------------------------------------------------------ calendario, atril, documentos
def calendario(id_, cx, cy, w, h, mes, dia, rot_=0, col="url(#calR)"):
    """Hoja de calendario de taco con anillas (p. ej. ('NOV', '29'))."""
    x, y = cx - w / 2, cy - h / 2
    o = f'<rect x="{f(x+10)}" y="{f(y+12)}" width="{f(w)}" height="{f(h)}" rx="16" fill="{INK}" opacity="0.25"/>'
    o += f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="16" fill="url(#calG)" stroke="{INK}" stroke-width="7"/>'
    o += f'<path d="M {f(x)} {f(y+h*0.3)} L {f(x)} {f(y+16)} Q {f(x)} {f(y)} {f(x+16)} {f(y)} L {f(x+w-16)} {f(y)} Q {f(x+w)} {f(y)} {f(x+w)} {f(y+16)} L {f(x+w)} {f(y+h*0.3)} Z" fill="{col}" stroke="{INK}" stroke-width="7"/>'
    o += T(cx, y + h * 0.22, mes, h * 0.13, "#FFFFFF", font=DISP)
    o += T(cx, y + h * 0.82, dia, h * 0.44 * min(1, 2.4 / max(1, len(dia))), INK, font=DISP)
    for k in (-1, 1):
        o += f'<rect x="{f(cx+k*w*0.28-9)}" y="{f(y-22)}" width="18" height="44" rx="9" fill="#9AA3B5" stroke="{INK}" stroke-width="5"/>'
    return gt(id_, f"rotate({f(rot_)} {f(cx)} {f(cy)})", o)


def logo_generico(cx, cy, r, texto="D21", col="url(#tealG)", sw=6):
    """Logo inventado (círculo con siglas), sin símbolos de partidos reales."""
    return (f'<circle cx="{f(cx+r*0.08)}" cy="{f(cy+r*0.1)}" r="{f(r)}" fill="{INK}" opacity="0.22"/>'
            f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{col}" stroke="{INK}" stroke-width="{sw}"/>'
            f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r*0.8)}" fill="none" stroke="#FFFFFF" stroke-width="{f(max(2,r*0.04))}" opacity="0.6"/>'
            + T(cx, cy + r * 0.2, texto, r * 0.6 * min(1, 3 / max(1, len(texto))), "#FFFFFF", font=DISP)
            + brillo(f"M {f(cx-r*0.62)} {f(cy-r*0.35)} A {f(r*0.72)} {f(r*0.72)} 0 0 1 {f(cx-r*0.1)} {f(cy-r*0.7)}", r * 0.09, 0.75))


def placa(cx, cy, w, h, texto, size=None, col="url(#navyG)"):
    """Placa con siglas en letras (color neutro)."""
    size = size or h * 0.58
    return (f'<rect x="{f(cx-w/2+7)}" y="{f(cy-h/2+9)}" width="{f(w)}" height="{f(h)}" rx="{f(h*0.22)}" fill="{INK}" opacity="0.25"/>'
            f'<rect x="{f(cx-w/2)}" y="{f(cy-h/2)}" width="{f(w)}" height="{f(h)}" rx="{f(h*0.22)}" fill="{col}" stroke="{INK}" stroke-width="6"/>'
            + brillo(f"M {f(cx-w/2+14)} {f(cy-h/2+12)} L {f(cx+w/2-14)} {f(cy-h/2+12)}", 4, 0.45)
            + T(cx, cy + size * 0.36, texto, size, "#FFFFFF", font=DISP))


def atril(id_, cx, base, w, h, mic=True, frontal=None):
    """Atril de mitin/debate visto de frente. frontal: SVG para el frente (por defecto logo genérico D21);
    usa placa(...) para siglas en letras."""
    top = base - h
    tw_ = w * 1.18
    o = sombra(cx, base + 6, w * 0.75, w * 0.09, 0.28)
    body = f"M {f(cx-w/2)} {f(base)} L {f(cx-w*0.42)} {f(top+h*0.12)} L {f(cx+w*0.42)} {f(top+h*0.12)} L {f(cx+w/2)} {f(base)} Z"
    o += f'<path d="{body}" fill="url(#lectG)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
    o += f'<path d="M {f(cx-w*0.36)} {f(top+h*0.2)} L {f(cx-w*0.42)} {f(base-14)}" stroke="#7F8EB0" stroke-width="8" stroke-linecap="round" opacity="0.8"/>'
    if mic:
        mx = cx + w * 0.18
        d = f"M {f(mx)} {f(top+h*0.04)} C {f(mx)} {f(top-h*0.12)}, {f(mx-w*0.08)} {f(top-h*0.2)}, {f(mx-w*0.14)} {f(top-h*0.26)}"
        o += f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="9" stroke-linecap="round"/><path d="{d}" fill="none" stroke="#9AA3B5" stroke-width="3" stroke-linecap="round"/>'
        o += f'<ellipse cx="{f(mx-w*0.16)}" cy="{f(top-h*0.3)}" rx="{f(w*0.05)}" ry="{f(w*0.07)}" transform="rotate(-40 {f(mx-w*0.16)} {f(top-h*0.3)})" fill="url(#micG)" stroke="{INK}" stroke-width="5"/>'
    o += f'<path d="M {f(cx-tw_/2)} {f(top+h*0.14)} L {f(cx-tw_/2+w*0.06)} {f(top)} L {f(cx+tw_/2-w*0.06)} {f(top)} L {f(cx+tw_/2)} {f(top+h*0.14)} Z" fill="url(#lectTop)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
    o += f'<path d="M {f(cx-tw_/2+w*0.1)} {f(top+h*0.04)} L {f(cx+tw_/2-w*0.1)} {f(top+h*0.04)}" stroke="#A9B7D6" stroke-width="4" stroke-linecap="round"/>'
    o += frontal if frontal is not None else logo_generico(cx, top + h * 0.5, w * 0.27)
    return g(id_, o)


def documento(id_, cx, cy, w, h, titulo, sub="", rot_=0, banda="url(#navyG)", lineas=6):
    """Documento grapado con banda de título (programa electoral, ley, BOE ficticio…)."""
    x, y = cx - w / 2, cy - h / 2
    o = f'<rect x="{f(x+22)}" y="{f(y+8)}" width="{f(w)}" height="{f(h)}" rx="10" fill="#DDE1EA" stroke="{INK}" stroke-width="5"/>'
    o += f'<rect x="{f(x+12)}" y="{f(y+16)}" width="{f(w)}" height="{f(h)}" rx="10" fill="{INK}" opacity="0.22"/>'
    o += f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="10" fill="url(#docG)" stroke="{INK}" stroke-width="7"/>'
    bh = h * 0.27
    o += f'<path d="M {f(x)} {f(y+bh)} L {f(x)} {f(y+10)} Q {f(x)} {f(y)} {f(x+10)} {f(y)} L {f(x+w-10)} {f(y)} Q {f(x+w)} {f(y)} {f(x+w)} {f(y+10)} L {f(x+w)} {f(y+bh)} Z" fill="{banda}" stroke="{INK}" stroke-width="7"/>'
    fs = min(bh * 0.36, w * 0.86 / (len(titulo) * 0.82))
    o += T(cx, y + bh * (0.46 if sub else 0.62), titulo, fs, "#FFFFFF", font=DISP)
    if sub:
        fs2 = min(bh * 0.3, w * 0.8 / (len(sub) * 0.82))
        o += T(cx, y + bh * 0.86, sub, fs2, LIME, font=DISP)
    for i in range(lineas):
        yy = y + bh + (h - bh) * (0.14 + i * 0.8 / lineas)
        o += f'<path d="M {f(x+w*0.12)} {f(yy)} L {f(x+w*(0.88 - (0.2 if i % 3 == 2 else 0)))} {f(yy)}" stroke="#AEB6C6" stroke-width="{f(max(5,h*0.025))}" stroke-linecap="round"/>'
    o += f'<rect x="{f(x+w*0.08)}" y="{f(y-8)}" width="{f(w*0.12)}" height="16" rx="4" fill="#9AA3B5" stroke="{INK}" stroke-width="4"/>'
    o += brillo(f"M {f(x+12)} {f(y+bh+14)} L {f(x+12)} {f(y+h-16)}", 6, 0.9)
    return gt(id_, f"rotate({f(rot_)} {f(cx)} {f(cy)})", o)


def carpeta(id_, cx, cy, w, h, texto="ESTATUTOS"):
    """Carpeta amarilla con hojas asomando y etiqueta."""
    x, y = cx - w / 2, cy - h / 2
    o = f'<rect x="{f(x+9)}" y="{f(y+11)}" width="{f(w)}" height="{f(h)}" rx="12" fill="{INK}" opacity="0.25"/>'
    o += f'<path d="M {f(x)} {f(y+18)} L {f(x)} {f(y)} L {f(x+w*0.36)} {f(y)} L {f(x+w*0.44)} {f(y+18)} Z" fill="#E8AE2E" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
    o += f'<rect x="{f(x+w*0.08)}" y="{f(y+4)}" width="{f(w*0.8)}" height="{f(h*0.5)}" rx="6" fill="#FFFFFF" stroke="{INK}" stroke-width="5" transform="rotate(-4 {f(cx)} {f(cy)})"/>'
    o += f'<rect x="{f(x)}" y="{f(y+18)}" width="{f(w)}" height="{f(h-18)}" rx="12" fill="url(#folderG)" stroke="{INK}" stroke-width="6"/>'
    o += brillo(f"M {f(x+14)} {f(y+34)} L {f(x+14)} {f(y+h-16)}", 7, 1, "#FFF1B8")
    fs = min(h * 0.17, w * 0.8 / (len(texto) * 0.8))
    o += f'<rect x="{f(cx-w*0.38)}" y="{f(cy+h*0.04)}" width="{f(w*0.76)}" height="{f(fs*1.6)}" rx="6" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/>'
    o += T(cx, cy + h * 0.04 + fs * 1.15, texto, fs, INK, font=DISP)
    return g(id_, o)


# ------------------------------------------------------------------ boli, garabato, candado
def boli(id_, cx, cy, L, rot_=35):
    """Bolígrafo azul con la punta en (cx, cy). rot_ = inclinación (grados)."""
    w = L * 0.11
    s = f'<ellipse cx="{f(cx+12)}" cy="{f(cy+L*0.55)}" rx="{f(w*0.7)}" ry="{f(L*0.45)}" fill="{INK}" opacity="0.15"/>'
    s += f'<path d="M {f(cx)} {f(cy)} L {f(cx-w*0.5)} {f(cy+L*0.12)} L {f(cx+w*0.5)} {f(cy+L*0.12)} Z" fill="#C9CED8" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    s += f'<rect x="{f(cx-w*0.5)}" y="{f(cy+L*0.12)}" width="{f(w)}" height="{f(L*0.88)}" rx="{f(w*0.3)}" fill="url(#penG)" stroke="{INK}" stroke-width="6"/>'
    s += f'<rect x="{f(cx-w*0.5)}" y="{f(cy+L*0.12)}" width="{f(w)}" height="{f(L*0.14)}" rx="4" fill="#E4E7EF" stroke="{INK}" stroke-width="5"/>'
    s += f'<path d="M {f(cx+w*0.62)} {f(cy+L*0.35)} L {f(cx+w*0.62)} {f(cy+L*0.7)}" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>'
    s += brillo(f"M {f(cx-w*0.2)} {f(cy+L*0.32)} L {f(cx-w*0.2)} {f(cy+L*0.92)}", 6, 0.6)
    return gt(id_, f"rotate({f(rot_)} {f(cx)} {f(cy)})", s)


def garabato(id_, x0, x1, yc, amp, n=8, col=CORAL, sw=10):
    """Garabato en zigzag (anímalo con "draw")."""
    P = [(x0 + (x1 - x0) * i / n, yc + (amp if i % 2 else -amp) * (0.7 + 0.3 * math.sin(i * 1.7))) for i in range(n + 1)]
    d = "M " + " L ".join(f"{f(a)} {f(b)}" for a, b in P)
    return g(id_, f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{f(sw)}" stroke-linecap="round" stroke-linejoin="round"/>')


def candado(id_, cx, cy, s):
    """Candado amarillo (seguridad, «cerrado»). (cx, cy) = centro del borde superior del cuerpo."""
    return g(id_,
             f'<path d="M {f(cx-s*0.32)} {f(cy)} L {f(cx-s*0.32)} {f(cy-s*0.3)} A {f(s*0.32)} {f(s*0.32)} 0 0 1 {f(cx+s*0.32)} {f(cy-s*0.3)} L {f(cx+s*0.32)} {f(cy)}" fill="none" stroke="{INK}" stroke-width="{f(s*0.16)}"/>'
             f'<path d="M {f(cx-s*0.32)} {f(cy)} L {f(cx-s*0.32)} {f(cy-s*0.3)} A {f(s*0.32)} {f(s*0.32)} 0 0 1 {f(cx+s*0.32)} {f(cy-s*0.3)} L {f(cx+s*0.32)} {f(cy)}" fill="none" stroke="#C9CED8" stroke-width="{f(s*0.07)}"/>'
             f'<rect x="{f(cx-s*0.5)}" y="{f(cy-s*0.05)}" width="{f(s)}" height="{f(s*0.75)}" rx="{f(s*0.1)}" fill="url(#yelG)" stroke="{INK}" stroke-width="{f(s*0.07)}"/>'
             f'<circle cx="{f(cx)}" cy="{f(cy+s*0.25)}" r="{f(s*0.1)}" fill="{INK}"/><path d="M {f(cx)} {f(cy+s*0.3)} L {f(cx)} {f(cy+s*0.5)}" stroke="{INK}" stroke-width="{f(s*0.08)}" stroke-linecap="round"/>'
             + brillo(f"M {f(cx-s*0.38)} {f(cy+s*0.05)} L {f(cx-s*0.38)} {f(cy+s*0.55)}", s * 0.06, 0.7))


def sin_posicionarnos(id_, cx, cy, size=40, rot_=-6):
    """Sello obligatorio de los vídeos de política: «SIN POSICIONARNOS» (lima sobre tinta)."""
    from ..base import sello
    return sello(id_, cx, cy, "SIN POSICIONARNOS", size, rot_, col=INK, fondo=LIME)


# ------------------------------------------------------------------ mesas electorales (lote7-12-mesa-electoral)
registrar_defs(
    lg("cartaSobre", [(0, "#F3E6C4"), (1, "#D9C08A")]) + lg("cartaSobreIn", [(0, "#BFA36A"), (1, "#E2CC97")])
    + lg("bomboG", [(0, "#FFE38A"), (1, "#E0A21A")]) + lg("manteG", [(0, "#FFFFFF"), (1, "#DCE2EE")])
    + lg("bolaG", [(0, "#FFFFFF"), (1, "#D5DAE6")])
)


def carta_notificacion(id_, cx, cy, w=420, h=300, titulo="MESA ELECTORAL", cargo="VOCAL", fecha="29 NOV", remite="AYUNTAMIENTO"):
    """Carta oficial de notificación: sobre crema abierto y hoja que asoma.
    Sub-ids: {id}_hoja (para que salga del sobre: move [0, -h*0.55], está tapada abajo por el bolsillo),
    {id}_cargo (recuadro coral con el cargo: pulse/punch), {id}_sobre. .puntos: hoja (centro final tras salir), cargo, solapa.
    (cx, cy) = centro del sobre."""
    x0, y0 = cx - w / 2, cy - h / 2
    o = sombra(cx, y0 + h + 12, w * 0.52, 16, 0.25)
    back = (f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" rx="14" fill="url(#cartaSobreIn)" stroke="{INK}" stroke-width="7"/>'
            f'<path d="M {f(x0+6)} {f(y0+4)} L {f(cx)} {f(y0-h*0.42)} L {f(x0+w-6)} {f(y0+4)} Z" fill="url(#cartaSobre)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
    # hoja
    hw, hh = w * 0.84, h * 1.05
    hx, hy = cx - hw / 2, y0 + h * 0.08
    hoja = f'<rect x="{f(hx)}" y="{f(hy)}" width="{f(hw)}" height="{f(hh)}" rx="8" fill="url(#papelG)" stroke="{INK}" stroke-width="6"/>'
    bh = hh * 0.16
    hoja += f'<rect x="{f(hx)}" y="{f(hy)}" width="{f(hw)}" height="{f(bh)}" rx="8" fill="url(#navyG)" stroke="{INK}" stroke-width="6"/>'
    fs = min(bh * 0.5, hw * 0.8 / (len(remite) * 0.8))
    hoja += T(cx, hy + bh * 0.66, remite, fs, "#FFFFFF", font=DISP)
    fs2 = min(hh * 0.085, hw * 0.86 / (len(titulo) * 0.78))
    hoja += T(cx, hy + bh + hh * 0.12, titulo, fs2, INK, font=DISP)
    cw_, ch_ = hw * 0.62, hh * 0.15
    cyy = hy + bh + hh * 0.18
    cargo_g = (f'<rect x="{f(cx-cw_/2)}" y="{f(cyy)}" width="{f(cw_)}" height="{f(ch_)}" rx="10" fill="{CORAL}" stroke="{INK}" stroke-width="5"/>'
               + T(cx, cyy + ch_ * 0.7, cargo, min(ch_ * 0.6, cw_ * 0.85 / (len(cargo) * 0.8)), "#FFFFFF", font=DISP))
    hoja += g(f"{id_}_cargo", cargo_g)
    if fecha:
        hoja += T(cx, cyy + ch_ + hh * 0.1, fecha, hh * 0.07, "#5A6170", font=DISP)
    for i in range(3):
        yy = cyy + ch_ + hh * (0.17 + i * 0.075)
        hoja += f'<path d="M {f(hx+hw*0.12)} {f(yy)} L {f(hx+hw*(0.88-0.18*(i==2)))} {f(yy)}" stroke="#AEB6C6" stroke-width="{f(max(4,hh*0.02))}" stroke-linecap="round"/>'
    hoja += brillo(f"M {f(hx+10)} {f(hy+bh+12)} L {f(hx+10)} {f(hy+hh-14)}", 5, 0.8)
    front = (f'<path d="M {f(x0)} {f(y0+h*0.3)} L {f(cx)} {f(y0+h*0.62)} L {f(x0+w)} {f(y0+h*0.3)} L {f(x0+w)} {f(y0+h-14)} '
             f'Q {f(x0+w)} {f(y0+h)} {f(x0+w-14)} {f(y0+h)} L {f(x0+14)} {f(y0+h)} Q {f(x0)} {f(y0+h)} {f(x0)} {f(y0+h-14)} Z" '
             f'fill="url(#cartaSobre)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
             f'<path d="M {f(x0+16)} {f(y0+h*0.42)} L {f(x0+16)} {f(y0+h-20)}" stroke="#FFF6DC" stroke-width="7" stroke-linecap="round" opacity="0.8"/>'
             f'<rect x="{f(x0+w-w*0.22)}" y="{f(y0+h*0.66)}" width="{f(w*0.14)}" height="{f(h*0.2)}" rx="4" fill="{CORAL}" stroke="{INK}" stroke-width="4"/>'
             f'<circle cx="{f(x0+w*0.2)}" cy="{f(y0+h*0.76)}" r="{f(h*0.1)}" fill="none" stroke="#9A7A3A" stroke-width="4" stroke-dasharray="6 5"/>')
    body = o + g(f"{id_}_sobre", back) + g(f"{id_}_hoja", hoja) + front
    return Pieza(g(id_, body), {"hoja": (cx, hy + hh / 2 - h * 0.55), "cargo": (cx, cyy + ch_ / 2 - h * 0.55), "solapa": (cx, y0)},
                 (x0, y0 - h * 0.6, x0 + w, y0 + h + 20))


def calendario_plazos(id_, cx, cy, n=7, cw=110, ch=118, titulo="7 DÍAS PARA ALEGAR", inicio=1, col=LIME):
    """Tira de calendario con n casillas numeradas (plazos). Cada casilla `{id}_d<i>`; la marca de «día gastado»
    (relleno de color con ✓) en `{id}_m<i>` (oculta con hide y haz pop en cascada). Cabecera `{id}_tit` con el título.
    .puntos: casillas (centros), ultima. Ancho total ≈ n*cw + 40."""
    W = n * cw + 40
    x0, y0 = cx - W / 2, cy - (ch + 90) / 2
    o = f'<rect x="{f(x0+10)}" y="{f(y0+14)}" width="{f(W)}" height="{f(ch+90)}" rx="18" fill="{INK}" opacity="0.22"/>'
    o += f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(W)}" height="{f(ch+90)}" rx="18" fill="url(#calG)" stroke="{INK}" stroke-width="7"/>'
    o += (f'<path d="M {f(x0)} {f(y0+66)} L {f(x0)} {f(y0+18)} Q {f(x0)} {f(y0)} {f(x0+18)} {f(y0)} L {f(x0+W-18)} {f(y0)} '
          f'Q {f(x0+W)} {f(y0)} {f(x0+W)} {f(y0+18)} L {f(x0+W)} {f(y0+66)} Z" fill="url(#calR)" stroke="{INK}" stroke-width="7"/>')
    o += g(f"{id_}_tit", T(cx, y0 + 46, titulo, min(36, (W - 40) / (len(titulo) * 0.8)), "#FFFFFF", font=DISP))
    for k in range(4):
        rx_ = x0 + W * (0.15 + 0.233 * k)
        o += f'<rect x="{f(rx_-8)}" y="{f(y0-20)}" width="16" height="40" rx="8" fill="#9AA3B5" stroke="{INK}" stroke-width="5"/>'
    cs = []
    for i in range(n):
        x = x0 + 20 + i * cw
        y = y0 + 78
        cs.append((x + cw / 2, y + ch / 2))
        cel = f'<rect x="{f(x+5)}" y="{f(y)}" width="{f(cw-10)}" height="{f(ch-6)}" rx="10" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/>'
        cel += T(x + cw / 2, y + ch * 0.62, str(inicio + i), ch * 0.42, INK, font=DISP)
        o += g(f"{id_}_d{i}", cel)
        m = (f'<rect x="{f(x+5)}" y="{f(y)}" width="{f(cw-10)}" height="{f(ch-6)}" rx="10" fill="{col}" stroke="{INK}" stroke-width="5"/>'
             + T(x + cw / 2, y + ch * 0.5, str(inicio + i), ch * 0.3, INK, font=DISP)
             + f'<path d="M {f(x+cw*0.3)} {f(y+ch*0.68)} L {f(x+cw*0.45)} {f(y+ch*0.82)} L {f(x+cw*0.72)} {f(y+ch*0.58)}" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>')
        o += g(f"{id_}_m{i}", m)
    return Pieza(g(id_, o), {"casillas": cs, "ultima": cs[-1]}, (x0, y0 - 20, x0 + W, y0 + ch + 90))


def formulario(id_, cx, cy, w=520, h=700, titulo="ALEGACIÓN", sub="JUNTA ELECTORAL DE ZONA", filas=("65 AÑOS O MÁS", "EMBARAZO"),
               firma=True, rot_=0):
    """Formulario oficial con casillas: banda de título, filas con casilla + texto, firma.
    Sub-ids: ✓ de cada fila en `{id}_c<i>` (pop en cascada), fila entera `{id}_f<i>`, garabato de firma `{id}_firma` (draw),
    clip `{id}_clip`. .puntos: casillas (centros), firma."""
    x0, y0 = cx - w / 2, cy - h / 2
    o = f'<rect x="{f(x0+12)}" y="{f(y0+16)}" width="{f(w)}" height="{f(h)}" rx="12" fill="{INK}" opacity="0.22"/>'
    o += f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" rx="12" fill="url(#docG)" stroke="{INK}" stroke-width="7"/>'
    bh = h * 0.17
    o += (f'<path d="M {f(x0)} {f(y0+bh)} L {f(x0)} {f(y0+12)} Q {f(x0)} {f(y0)} {f(x0+12)} {f(y0)} L {f(x0+w-12)} {f(y0)} '
          f'Q {f(x0+w)} {f(y0)} {f(x0+w)} {f(y0+12)} L {f(x0+w)} {f(y0+bh)} Z" fill="url(#navyG)" stroke="{INK}" stroke-width="7"/>')
    o += T(cx, y0 + bh * 0.5, titulo, min(bh * 0.4, w * 0.8 / (len(titulo) * 0.8)), "#FFFFFF", font=DISP)
    o += T(cx, y0 + bh * 0.84, sub, min(bh * 0.22, w * 0.86 / (len(sub) * 0.72)), LIME, font=DISP)
    n = len(filas)
    zona = h * (0.66 if firma else 0.76)
    paso = zona / max(n, 1)
    cs = []
    s_box = min(paso * 0.62, 56)
    for i, txt in enumerate(filas):
        yy = y0 + bh + h * 0.04 + paso * (i + 0.5)
        bx = x0 + w * 0.08
        cs.append((bx + s_box / 2, yy))
        fila = f'<rect x="{f(bx)}" y="{f(yy-s_box/2)}" width="{f(s_box)}" height="{f(s_box)}" rx="8" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/>'
        tx = bx + s_box + w * 0.04
        fs = min(s_box * 0.62, (x0 + w * 0.95 - tx) / (len(txt) * 0.66))
        fila += T(tx, yy + fs * 0.36, txt, fs, INK, anchor="start", font=DISP)
        o += g(f"{id_}_f{i}", fila)
        o += g(f"{id_}_c{i}", f'<path d="M {f(bx+s_box*0.18)} {f(yy)} L {f(bx+s_box*0.42)} {f(yy+s_box*0.3)} L {f(bx+s_box*0.95)} {f(yy-s_box*0.42)}" '
                                f'fill="none" stroke="#1F9E55" stroke-width="{f(s_box*0.2)}" stroke-linecap="round" stroke-linejoin="round"/>')
    fp = (cx + w * 0.12, y0 + h * 0.9)
    if firma:
        o += f'<path d="M {f(x0+w*0.4)} {f(y0+h*0.93)} L {f(x0+w*0.92)} {f(y0+h*0.93)}" stroke="#AEB6C6" stroke-width="5" stroke-linecap="round"/>'
        o += T(x0 + w * 0.08, y0 + h * 0.93, "FIRMA", h * 0.03, "#7A8194", anchor="start", font=DISP)
        P = [(x0 + w * 0.44, y0 + h * 0.92), (x0 + w * 0.5, y0 + h * 0.86), (x0 + w * 0.54, y0 + h * 0.92), (x0 + w * 0.6, y0 + h * 0.85),
             (x0 + w * 0.64, y0 + h * 0.92), (x0 + w * 0.72, y0 + h * 0.87), (x0 + w * 0.8, y0 + h * 0.91), (x0 + w * 0.88, y0 + h * 0.88)]
        d = "M " + " L ".join(f"{f(a)} {f(b)}" for a, b in P)
        o += g(f"{id_}_firma", f'<path d="{d}" fill="none" stroke="#2D5BD1" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>')
    o += g(f"{id_}_clip", f'<rect x="{f(cx-w*0.14)}" y="{f(y0-16)}" width="{f(w*0.28)}" height="30" rx="8" fill="url(#metalG)" stroke="{INK}" stroke-width="5"/>')
    o += brillo(f"M {f(x0+12)} {f(y0+bh+14)} L {f(x0+12)} {f(y0+h-16)}", 6, 0.9)
    return Pieza(gt(id_, f"rotate({f(rot_)} {f(cx)} {f(cy)})", o), {"casillas": cs, "firma": fp}, (x0, y0 - 16, x0 + w, y0 + h + 16))


def bombo(id_, cx, cy, r=170, n_bolas=9, seed=3, texto=None, bola_txt="TÚ"):
    """Bombo de sorteo (jaula con bolas, manivela y soporte). Sub-ids: {id}_jaula (spin), {id}_manivela,
    {id}_bola (bola que sale por la boca: move hacia abajo/derecha), texto opcional en una placa del soporte.
    .puntos: boca (salida de la bola), centro."""
    rnd = random.Random(seed)
    o = sombra(cx, cy + r * 1.42, r * 1.05, r * 0.12, 0.25)
    o += (f'<path d="M {f(cx-r*0.9)} {f(cy+r*1.4)} L {f(cx-r*0.35)} {f(cy+r*0.2)} M {f(cx+r*0.9)} {f(cy+r*1.4)} L {f(cx+r*0.35)} {f(cy+r*0.2)}" '
          f'stroke="{INK}" stroke-width="22" stroke-linecap="round"/>'
          f'<path d="M {f(cx-r*0.9)} {f(cy+r*1.4)} L {f(cx-r*0.35)} {f(cy+r*0.2)} M {f(cx+r*0.9)} {f(cy+r*1.4)} L {f(cx+r*0.35)} {f(cy+r*0.2)}" '
          f'stroke="#8C96AA" stroke-width="10" stroke-linecap="round"/>')
    o += f'<rect x="{f(cx-r*1.05)}" y="{f(cy+r*1.32)}" width="{f(r*2.1)}" height="{f(r*0.18)}" rx="10" fill="url(#maderaG)" stroke="{INK}" stroke-width="6"/>'
    if texto:
        tw_ = len(texto) * r * 0.1 + 40
        o += f'<rect x="{f(cx-tw_/2)}" y="{f(cy+r*1.05)}" width="{f(tw_)}" height="{f(r*0.24)}" rx="8" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/>'
        o += T(cx, cy + r * 1.23, texto, r * 0.14, INK, font=DISP)
    jau = f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="#EAF6FF" fill-opacity="0.55" stroke="{INK}" stroke-width="8"/>'
    for i in range(n_bolas):
        a, d = rnd.uniform(0, 6.28), rnd.uniform(0.15, 0.7) * r
        bx, by = cx + d * math.cos(a), cy + abs(d * math.sin(a)) * 0.8 + r * 0.1
        col = (CORAL, YEL, TEAL, "#FFFFFF", "#7B5CFF", "#FF7EB6")[i % 6]
        jau += f'<circle cx="{f(bx)}" cy="{f(by)}" r="{f(r*0.15)}" fill="{degradado(col, 0.25)}" stroke="{INK}" stroke-width="4"/>'
        jau += f'<circle cx="{f(bx-r*0.05)}" cy="{f(by-r*0.05)}" r="{f(r*0.04)}" fill="#FFFFFF" opacity="0.8"/>'
    for k in range(-2, 3):
        jau += f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(r*abs(k)/2.6+2)}" ry="{f(r)}" fill="none" stroke="{INK}" stroke-width="4" opacity="0.75"/>'
    for k in (-0.5, 0, 0.5):
        yy = cy + k * r
        rr = math.sqrt(max(r * r - (k * r) ** 2, 1))
        jau += f'<path d="M {f(cx-rr)} {f(yy)} L {f(cx+rr)} {f(yy)}" stroke="{INK}" stroke-width="4" opacity="0.75"/>'
    jau += f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="none" stroke="{YEL}" stroke-width="5" opacity="0.7"/>'
    jau += brillo(f"M {f(cx-r*0.62)} {f(cy-r*0.5)} A {f(r*0.8)} {f(r*0.8)} 0 0 1 {f(cx-r*0.1)} {f(cy-r*0.8)}", r * 0.06, 0.8)
    o += g(f"{id_}_jaula", jau)
    o += f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r*0.12)}" fill="url(#bomboG)" stroke="{INK}" stroke-width="6"/>'
    man = (f'<path d="M {f(cx)} {f(cy)} L {f(cx+r*0.55)} {f(cy-r*0.35)}" stroke="{INK}" stroke-width="16" stroke-linecap="round"/>'
           f'<path d="M {f(cx)} {f(cy)} L {f(cx+r*0.55)} {f(cy-r*0.35)}" stroke="#C9CED8" stroke-width="6" stroke-linecap="round"/>'
           f'<rect x="{f(cx+r*0.5)}" y="{f(cy-r*0.55)}" width="{f(r*0.14)}" height="{f(r*0.3)}" rx="{f(r*0.06)}" fill="{CORAL}" stroke="{INK}" stroke-width="5"/>')
    o += g(f"{id_}_manivela", man)
    bxx, byy = cx + r * 0.7, cy + r * 0.72
    o += f'<path d="M {f(bxx-r*0.18)} {f(byy-r*0.2)} L {f(bxx+r*0.22)} {f(byy+r*0.1)}" stroke="{INK}" stroke-width="20" stroke-linecap="round"/>'
    o += f'<path d="M {f(bxx-r*0.18)} {f(byy-r*0.2)} L {f(bxx+r*0.22)} {f(byy+r*0.1)}" stroke="#8C96AA" stroke-width="9" stroke-linecap="round"/>'
    bol = (f'<circle cx="{f(bxx+r*0.3)}" cy="{f(byy+r*0.16)}" r="{f(r*0.2)}" fill="url(#limaG)" stroke="{INK}" stroke-width="6"/>'
           + T(bxx + r * 0.3, byy + r * 0.16 + r * 0.07, bola_txt, r * 0.17 * min(1, 2.2 / max(1, len(bola_txt))), INK, font=DISP)
           + f'<circle cx="{f(bxx+r*0.24)}" cy="{f(byy+r*0.08)}" r="{f(r*0.05)}" fill="#FFFFFF" opacity="0.85"/>')
    o += g(f"{id_}_bola", bol)
    return Pieza(g(id_, o), {"boca": (bxx + r * 0.3, byy + r * 0.16), "centro": (cx, cy)}, (cx - r * 1.05, cy - r, cx + r * 1.05, cy + r * 1.5))


def mesa_electoral(id_, cx, y_tablero, w=680, alto=230, cartel="MESA A", urna_=True, urna_texto="CONGRESO", urna_dx=0.0):
    """Mesa electoral de frente: tablero con mantel hasta el suelo, cartel con la letra de la mesa, urna encima y
    papeles/lista del censo. urna_dx = desplazamiento de la urna (fracción de w; 0,3 la lleva a la derecha). Pon las personas sentadas (persona(pose="busto")) ANTES en el SVG para que la mesa las tape.
    Sub-ids: {id}_urna, {id}_cartel, {id}_lista. .puntos: tablero (y), ranura, izq, der, base."""
    x0 = cx - w / 2
    base = y_tablero + alto
    o = sombra(cx, base + 6, w * 0.56, 18, 0.25)
    u = ""
    if urna_:
        u = urna(f"{id_}_urna", cx + urna_dx * w, y_tablero + 8, w * 0.27, w * 0.27, texto=urna_texto)
    o += (f'<path d="M {f(x0-10)} {f(y_tablero)} L {f(x0+w+10)} {f(y_tablero)} L {f(x0+w+26)} {f(base)} L {f(x0-26)} {f(base)} Z" '
          f'fill="url(#manteG)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
    for k in range(1, 6):
        xx = x0 - 18 + (w + 36) * k / 6
        o += f'<path d="M {f(xx)} {f(y_tablero+20)} L {f(xx + (xx-cx)*0.03)} {f(base-6)}" stroke="#C5CCDB" stroke-width="5" stroke-linecap="round"/>'
    o += f'<rect x="{f(x0-16)}" y="{f(y_tablero-14)}" width="{f(w+32)}" height="26" rx="8" fill="#F4F6FA" stroke="{INK}" stroke-width="6"/>'
    cw_ = max(150, len(cartel) * 30 + 40)
    car = (f'<rect x="{f(cx-cw_/2)}" y="{f(y_tablero+alto*0.3)}" width="{f(cw_)}" height="{f(alto*0.3)}" rx="10" fill="url(#navyG)" stroke="{INK}" stroke-width="5"/>'
           + T(cx, y_tablero + alto * 0.3 + alto * 0.21, cartel, alto * 0.16, "#FFFFFF", font=DISP))
    lista = (f'<rect x="{f(x0+w*0.06)}" y="{f(y_tablero-34)}" width="{f(w*0.18)}" height="26" rx="4" fill="#FFFFFF" stroke="{INK}" stroke-width="4" transform="rotate(-4 {f(x0+w*0.15)} {f(y_tablero-20)})"/>'
             f'<rect x="{f(x0+w*0.76)}" y="{f(y_tablero-30)}" width="{f(w*0.16)}" height="22" rx="4" fill="#FFF3C9" stroke="{INK}" stroke-width="4" transform="rotate(5 {f(x0+w*0.84)} {f(y_tablero-20)})"/>')
    body = o + g(f"{id_}_lista", lista) + g(f"{id_}_cartel", car) + u
    pr = u.puntos["ranura"] if urna_ else (cx, y_tablero)
    return Pieza(g(id_, body), {"tablero": y_tablero, "ranura": pr, "izq": (x0, y_tablero), "der": (x0 + w, y_tablero), "base": base},
                 (x0 - 26, y_tablero - w * 0.4, x0 + w + 26, base))


def colegio_electoral(W=1080, H=1920, suelo_y=None, rotulo="COLEGIO ELECTORAL"):
    """Fondo: aula de colegio convertida en colegio electoral (pared bicolor, pizarra, ventanales, reloj, cabina con cortina
    a la derecha, rótulo arriba y suelo de baldosas). Sin ids. Lo importante delante, entre y 450 y 1250."""
    sy = suelo_y or H * 0.62
    registrar_defs(lg("aulaPared", [(0, "#FFF4DE"), (1, "#F3DDB4")]), lg("aulaZoc", [(0, "#8FC9B9"), (1, "#5FA694")]),
                   lg("aulaSuelo", [(0, "#D9DEE8"), (1, "#AEB7C8")]), lg("aulaWin", [(0, "#A9DBFF"), (1, "#E6F5FF")]),
                   lg("cortinaC", [(0, "#3D6FD8"), (1, "#22409A")], 0, 0, 1, 0))
    o = f'<rect width="{W}" height="{H}" fill="url(#aulaPared)"/>'
    o += f'<rect x="0" y="{f(sy-H*0.12)}" width="{W}" height="{f(H*0.12)}" fill="url(#aulaZoc)"/><path d="M 0 {f(sy-H*0.12)} L {W} {f(sy-H*0.12)}" stroke="{INK}" stroke-width="5"/>'
    for i in range(2):
        wx = W * (0.06 + 0.3 * i)
        o += f'<rect x="{f(wx)}" y="{f(H*0.2)}" width="{f(W*0.24)}" height="{f(H*0.2)}" rx="8" fill="url(#aulaWin)" stroke="{INK}" stroke-width="7"/>'
        o += f'<path d="M {f(wx+W*0.12)} {f(H*0.2)} L {f(wx+W*0.12)} {f(H*0.4)} M {f(wx)} {f(H*0.3)} L {f(wx+W*0.24)} {f(H*0.3)}" stroke="{INK}" stroke-width="6"/>'
        o += f'<path d="M {f(wx+16)} {f(H*0.215)} L {f(wx+16)} {f(H*0.29)}" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round" opacity="0.8"/>'
    px, py, pw, ph = W * 0.66, H * 0.2, W * 0.3, H * 0.13
    o += f'<rect x="{f(px-10)}" y="{f(py-10)}" width="{f(pw+20)}" height="{f(ph+20)}" rx="8" fill="#B07A45" stroke="{INK}" stroke-width="6"/>'
    o += f'<rect x="{f(px)}" y="{f(py)}" width="{f(pw)}" height="{f(ph)}" rx="4" fill="#2C5446" stroke="{INK}" stroke-width="4"/>'
    o += (f'<path d="M {f(px+pw*0.12)} {f(py+ph*0.35)} L {f(px+pw*0.6)} {f(py+ph*0.35)} M {f(px+pw*0.12)} {f(py+ph*0.6)} L {f(px+pw*0.8)} {f(py+ph*0.6)}" '
          f'stroke="#F4F1E6" stroke-width="5" stroke-linecap="round" opacity="0.6"/>')
    o += f'<circle cx="{f(W*0.81)}" cy="{f(H*0.39)}" r="46" fill="#FFFFFF" stroke="{INK}" stroke-width="7"/>'
    o += f'<path d="M {f(W*0.81)} {f(H*0.39)} L {f(W*0.81)} {f(H*0.39-30)} M {f(W*0.81)} {f(H*0.39)} L {f(W*0.81+22)} {f(H*0.39+8)}" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
    # cabina de votación
    cx_, cw_ = W * 0.93, W * 0.2
    o += f'<rect x="{f(cx_-cw_/2)}" y="{f(sy-H*0.24)}" width="{f(cw_)}" height="16" rx="6" fill="#8C96AA" stroke="{INK}" stroke-width="5"/>'
    for k in range(5):
        xx = cx_ - cw_ / 2 + 8 + k * (cw_ - 16) / 4
        o += f'<path d="M {f(xx)} {f(sy-H*0.235)} Q {f(xx+14)} {f(sy-H*0.12)} {f(xx)} {f(sy-12)}" stroke="#1B2F70" stroke-width="5" fill="none" opacity="0.6"/>'
    o += f'<rect x="{f(cx_-cw_/2+6)}" y="{f(sy-H*0.232)}" width="{f(cw_-12)}" height="{f(H*0.22)}" rx="6" fill="url(#cortinaC)" stroke="{INK}" stroke-width="6" opacity="0.92"/>'
    if rotulo:
        rw = len(rotulo) * 32 + 80
        o += f'<rect x="{f(W/2-rw/2)}" y="{f(H*0.115)}" width="{f(rw)}" height="70" rx="14" fill="{LIME}" stroke="{INK}" stroke-width="6"/>'
        o += T(W / 2, H * 0.115 + 48, rotulo, 34, INK, font=DISP)
    o += f'<rect x="0" y="{f(sy)}" width="{W}" height="{f(H-sy)}" fill="url(#aulaSuelo)"/><path d="M 0 {f(sy)} L {W} {f(sy)}" stroke="{INK}" stroke-width="8"/>'
    o += f'<g stroke="#9AA4B8" stroke-width="4">' + "".join(
        f'<line x1="0" y1="{f(y)}" x2="{W}" y2="{f(y)}"/>' for y in [sy + (H - sy) * k for k in (0.14, 0.32, 0.55, 0.8)])
    o += "".join(f'<line x1="{f(W/2 + (x - W/2) * 0.55)}" y1="{f(sy)}" x2="{f(W/2 + (x - W/2) * 1.6)}" y2="{H}"/>' for x in range(-90, W + 200, 180)) + "</g>"
    return o

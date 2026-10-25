"""Tecnología y móviles: batería (nueva o gastada, con nivel y rayo), chip/procesador, logotipo de Apple (pegatina),
iconos de app, pantallas para `casa.movil()` (cargando, almacenamiento casi lleno, salud de la batería), barra de
almacenamiento, papelera y un armario a reventar (metáfora de la memoria llena).

Sale de: lote8-01-movil-lento (por qué tu móvil va más lento con los años).
Uso con el móvil de casa.py:
    x0, y0, x1, y1 = pantalla_movil(cx, cy, w)          # caja de la pantalla antes de dibujar el móvil
    K.movil("tel", cx, cy, w, pantalla=pantalla_cargando("tel", x0, y0, x1, y1))
"""
import math
from ..base import (INK, LIME, CORAL, YEL, TEAL, VIO, GRIS, VERDE, f, g, gt, T, MONO, DISP, shade, trazo, sombra,
                    sombra_caja, brillo, lg, rg, registrar_defs, degradado, Pieza)

registrar_defs(
    lg("bateriaCuerpo", [(0, "#F7F9FC"), (1, "#C9D1DF")], 0, 0, 1, 0)
    + lg("chipG", [(0, "#4A5470"), (1, "#1C2133")], 0, 0, 1, 1)
    + lg("appleG", [(0, "#B9C2D2"), (1, "#5A6170")])
    + lg("armarioG", [(0, "#E2A86E"), (1, "#A8693A")], 0, 0, 1, 0)
    + lg("papeleraG", [(0, "#9AA3B5"), (1, "#5A6170")], 0, 0, 1, 0)
)


def pantalla_movil(cx, cy, w=400):
    """Caja (x0, y0, x1, y1) de la pantalla de casa.movil(id_, cx, cy, w) para preparar su contenido."""
    h = w * 1.95
    PX, PY = cx - w / 2, cy - h / 2
    SX, SY, SW_, SH = PX + w * 0.055, PY + w * 0.065, w * 0.89, h - w * 0.13
    return SX, SY, SX + SW_, SY + SH


# ------------------------------------------------------------------ batería
def bateria(id_, cx, cy, w=200, h=380, nivel=1.0, col=None, rayo=True, gastada=False, texto=None):
    """Batería vertical tipo pila de litio (borne arriba). `nivel` 0-1 rellena la carga (verde > 0,5, amarilla, coral < 0,25).
    `gastada=True`: cuerpo algo hinchado y amarillento, con grietas. Sub-ids: {id}_carga (grow origin bottom), {id}_rayo (pulse).
    .puntos: borne, centro, base."""
    col = col or (VERDE if nivel > 0.5 else YEL if nivel > 0.25 else CORAL)
    x0, y0 = cx - w / 2, cy - h / 2
    bw, bh = w * 0.36, h * 0.07
    s = sombra(cx + 8, y0 + h + 10, w * 0.6, 18)
    s += f'<rect x="{f(cx-bw/2)}" y="{f(y0-bh+6)}" width="{f(bw)}" height="{f(bh)}" rx="8" fill="url(#metalG)" stroke="{INK}" stroke-width="6"/>'
    body = "url(#bateriaCuerpo)" if not gastada else degradado("#E9DFB8", 0.25, "h")
    if gastada:
        b = w * 0.07
        d = (f"M {f(x0+18)} {f(y0)} L {f(x0+w-18)} {f(y0)} Q {f(x0+w)} {f(y0)} {f(x0+w)} {f(y0+18)} "
             f"C {f(x0+w+b)} {f(y0+h*0.35)}, {f(x0+w+b)} {f(y0+h*0.65)}, {f(x0+w)} {f(y0+h-18)} Q {f(x0+w)} {f(y0+h)} {f(x0+w-18)} {f(y0+h)} "
             f"L {f(x0+18)} {f(y0+h)} Q {f(x0)} {f(y0+h)} {f(x0)} {f(y0+h-18)} C {f(x0-b)} {f(y0+h*0.65)}, {f(x0-b)} {f(y0+h*0.35)}, {f(x0)} {f(y0+18)} "
             f"Q {f(x0)} {f(y0)} {f(x0+18)} {f(y0)} Z")
        s += f'<path d="{d}" fill="{body}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'
    else:
        s += f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" rx="24" fill="{body}" stroke="{INK}" stroke-width="8"/>'
    pad = w * 0.12
    ix, iy, iw, ih = x0 + pad, y0 + pad, w - 2 * pad, h - 2 * pad
    s += f'<rect x="{f(ix)}" y="{f(iy)}" width="{f(iw)}" height="{f(ih)}" rx="12" fill="#2A3045" stroke="{INK}" stroke-width="4"/>'
    ch = max(ih * nivel, 1)
    carga = (f'<rect x="{f(ix+5)}" y="{f(iy+ih-ch+5)}" width="{f(iw-10)}" height="{f(ch-10)}" rx="8" fill="{degradado(col, 0.25, "h")}"/>'
             + brillo(f"M {f(ix+16)} {f(iy+ih-ch+18)} L {f(ix+16)} {f(iy+ih-18)}", 5, 0.55))
    s += g(f"{id_}_carga" if id_ else None, carga)
    if rayo:
        r = min(iw, ih) * 0.42
        rx_, ry_ = cx, iy + ih * 0.5
        d = (f"M {f(rx_+r*0.15)} {f(ry_-r*1.1)} L {f(rx_-r*0.55)} {f(ry_+r*0.12)} L {f(rx_-r*0.02)} {f(ry_+r*0.12)} "
             f"L {f(rx_-r*0.2)} {f(ry_+r*1.1)} L {f(rx_+r*0.55)} {f(ry_-r*0.15)} L {f(rx_+r*0.04)} {f(ry_-r*0.15)} Z")
        s += g(f"{id_}_rayo" if id_ else None, f'<path d="{d}" fill="#FFFFFF" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
    if gastada:
        s += (f'<path d="M {f(x0+w*0.78)} {f(y0+h*0.08)} l {f(-w*0.08)} {f(h*0.05)} l {f(w*0.06)} {f(h*0.04)} l {f(-w*0.07)} {f(h*0.05)}" '
              f'fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')
    s += brillo(f"M {f(x0+14)} {f(y0+30)} L {f(x0+14)} {f(y0+h*0.45)}", 6, 0.7)
    if texto:
        s += T(cx, y0 + h + 52, texto, 30, INK, font=DISP)
    return Pieza(g(id_, s), {"borne": (cx, y0 - bh), "centro": (cx, cy), "base": (cx, y0 + h)}, (x0, y0 - bh, x0 + w, y0 + h))


# ------------------------------------------------------------------ chip
def chip(id_, cx, cy, s=200, texto="CPU"):
    """Procesador visto desde arriba con patillas. Sub-id {id}_nucleo (pulse = trabajando). .puntos: centro."""
    h = s / 2
    o = sombra_caja(cx - h, cy - h, s, s, 18, 10, 12, 0.25)
    n = 5
    for k in range(n):
        t = -h * 0.7 + k * (1.4 * h / (n - 1))
        for (x1, y1, x2, y2) in ((cx + t, cy - h, cx + t, cy - h - s * 0.13), (cx + t, cy + h, cx + t, cy + h + s * 0.13),
                                 (cx - h, cy + t, cx - h - s * 0.13, cy + t), (cx + h, cy + t, cx + h + s * 0.13, cy + t)):
            o += trazo(f"M {f(x1)} {f(y1)} L {f(x2)} {f(y2)}", s * 0.045, "#D9DEE8", 5)
    o += f'<rect x="{f(cx-h)}" y="{f(cy-h)}" width="{f(s)}" height="{f(s)}" rx="{f(s*0.1)}" fill="url(#chipG)" stroke="{INK}" stroke-width="8"/>'
    nucleo = (f'<rect x="{f(cx-h*0.55)}" y="{f(cy-h*0.55)}" width="{f(s*0.55)}" height="{f(s*0.55)}" rx="{f(s*0.06)}" fill="{degradado(LIME, 0.25)}" stroke="{INK}" stroke-width="5"/>'
              + T(cx, cy + s * 0.07, texto, s * 0.17, INK, font=DISP))
    o += g(f"{id_}_nucleo" if id_ else None, nucleo)
    o += brillo(f"M {f(cx-h+16)} {f(cy-h+16)} L {f(cx+h*0.2)} {f(cy-h+16)}", 5, 0.45)
    return Pieza(g(id_, o), {"centro": (cx, cy)}, (cx - h * 1.3, cy - h * 1.3, cx + h * 1.3, cy + h * 1.3))


# ------------------------------------------------------------------ logotipo de Apple
def logo_apple(id_, cx, cy, s=200, col="url(#appleG)", contorno=True):
    """Manzana mordida de Apple (pegatina simplificada, ≈ s×s*1.2). (cx, cy) = centro del cuerpo."""
    r = s / 2
    d = (f"M {f(cx)} {f(cy-r*0.62)} "
         f"C {f(cx-r*0.35)} {f(cy-r*0.9)}, {f(cx-r*1.05)} {f(cy-r*0.85)}, {f(cx-r*1.0)} {f(cy-r*0.05)} "
         f"C {f(cx-r*0.98)} {f(cy+r*0.55)}, {f(cx-r*0.6)} {f(cy+r*1.08)}, {f(cx-r*0.3)} {f(cy+r*1.05)} "
         f"C {f(cx-r*0.12)} {f(cy+r*1.03)}, {f(cx-r*0.08)} {f(cy+r*0.95)}, {f(cx)} {f(cy+r*0.95)} "
         f"C {f(cx+r*0.08)} {f(cy+r*0.95)}, {f(cx+r*0.12)} {f(cy+r*1.03)}, {f(cx+r*0.3)} {f(cy+r*1.05)} "
         f"C {f(cx+r*0.6)} {f(cy+r*1.08)}, {f(cx+r*0.86)} {f(cy+r*0.65)}, {f(cx+r*0.98)} {f(cy+r*0.32)} "
         # mordisco a la derecha
         f"C {f(cx+r*0.62)} {f(cy+r*0.2)}, {f(cx+r*0.55)} {f(cy-r*0.4)}, {f(cx+r*0.88)} {f(cy-r*0.6)} "
         f"C {f(cx+r*0.65)} {f(cy-r*0.9)}, {f(cx+r*0.3)} {f(cy-r*0.88)}, {f(cx)} {f(cy-r*0.62)} Z")
    hoja = (f"M {f(cx+r*0.02)} {f(cy-r*0.78)} C {f(cx)} {f(cy-r*1.15)}, {f(cx+r*0.25)} {f(cy-r*1.38)}, {f(cx+r*0.52)} {f(cy-r*1.4)} "
            f"C {f(cx+r*0.54)} {f(cy-r*1.08)}, {f(cx+r*0.3)} {f(cy-r*0.82)}, {f(cx+r*0.02)} {f(cy-r*0.78)} Z")
    sw = 7 if contorno else 0
    o = sombra(cx + 8, cy + r * 1.2, r * 0.8, r * 0.12)
    o += f'<path d="{d}" fill="{col}" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"/>'
    o += f'<path d="{hoja}" fill="{col}" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"/>'
    o += brillo(f"M {f(cx-r*0.7)} {f(cy-r*0.25)} C {f(cx-r*0.68)} {f(cy-r*0.55)}, {f(cx-r*0.45)} {f(cy-r*0.68)}, {f(cx-r*0.25)} {f(cy-r*0.66)}", 7, 0.75)
    return Pieza(g(id_, o), {"centro": (cx, cy)}, (cx - r, cy - r * 1.4, cx + r, cy + r * 1.08))


# ------------------------------------------------------------------ iconos de app
def icono_app(id_, cx, cy, s=120, col=CORAL, glifo="play"):
    """Icono de app redondeado. glifo: play, chat, foto, mapa, nota, juego, camara, estrella."""
    h = s / 2
    o = f'<rect x="{f(cx-h+6)}" y="{f(cy-h+8)}" width="{f(s)}" height="{f(s)}" rx="{f(s*0.24)}" fill="{INK}" opacity="0.25"/>'
    o += f'<rect x="{f(cx-h)}" y="{f(cy-h)}" width="{f(s)}" height="{f(s)}" rx="{f(s*0.24)}" fill="{degradado(col, 0.25)}" stroke="{INK}" stroke-width="{f(max(4, s*0.05))}"/>'
    q = s * 0.26
    W = "#FFFFFF"
    if glifo == "play":
        o += f'<path d="M {f(cx-q*0.6)} {f(cy-q)} L {f(cx+q)} {f(cy)} L {f(cx-q*0.6)} {f(cy+q)} Z" fill="{W}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
    elif glifo == "chat":
        o += f'<path d="M {f(cx-q)} {f(cy-q*0.8)} L {f(cx+q)} {f(cy-q*0.8)} L {f(cx+q)} {f(cy+q*0.5)} L {f(cx-q*0.2)} {f(cy+q*0.5)} L {f(cx-q*0.7)} {f(cy+q)} L {f(cx-q*0.6)} {f(cy+q*0.5)} L {f(cx-q)} {f(cy+q*0.5)} Z" fill="{W}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
    elif glifo == "foto":
        o += f'<rect x="{f(cx-q)}" y="{f(cy-q*0.8)}" width="{f(2*q)}" height="{f(1.6*q)}" rx="6" fill="{W}" stroke="{INK}" stroke-width="3"/>'
        o += f'<path d="M {f(cx-q*0.8)} {f(cy+q*0.6)} L {f(cx-q*0.2)} {f(cy-q*0.1)} L {f(cx+q*0.2)} {f(cy+q*0.3)} L {f(cx+q*0.45)} {f(cy+q*0.05)} L {f(cx+q*0.8)} {f(cy+q*0.6)} Z" fill="{TEAL}"/>'
        o += f'<circle cx="{f(cx+q*0.45)}" cy="{f(cy-q*0.35)}" r="{f(q*0.18)}" fill="{YEL}"/>'
    elif glifo == "mapa":
        o += f'<path d="M {f(cx)} {f(cy+q)} C {f(cx-q*0.9)} {f(cy)}, {f(cx-q*0.8)} {f(cy-q)}, {f(cx)} {f(cy-q)} C {f(cx+q*0.8)} {f(cy-q)}, {f(cx+q*0.9)} {f(cy)}, {f(cx)} {f(cy+q)} Z" fill="{W}" stroke="{INK}" stroke-width="3"/>'
        o += f'<circle cx="{f(cx)}" cy="{f(cy-q*0.3)}" r="{f(q*0.3)}" fill="{col}"/>'
    elif glifo == "nota":
        o += f'<path d="M {f(cx-q*0.3)} {f(cy+q*0.6)} L {f(cx-q*0.3)} {f(cy-q*0.8)} L {f(cx+q*0.7)} {f(cy-q)} L {f(cx+q*0.7)} {f(cy+q*0.4)}" fill="none" stroke="{W}" stroke-width="{f(q*0.22)}" stroke-linejoin="round"/>'
        o += f'<circle cx="{f(cx-q*0.55)}" cy="{f(cy+q*0.65)}" r="{f(q*0.32)}" fill="{W}"/><circle cx="{f(cx+q*0.45)}" cy="{f(cy+q*0.45)}" r="{f(q*0.32)}" fill="{W}"/>'
    elif glifo == "camara":
        o += f'<rect x="{f(cx-q)}" y="{f(cy-q*0.6)}" width="{f(2*q)}" height="{f(1.4*q)}" rx="8" fill="{W}" stroke="{INK}" stroke-width="3"/>'
        o += f'<circle cx="{f(cx)}" cy="{f(cy+q*0.1)}" r="{f(q*0.45)}" fill="{INK}"/><circle cx="{f(cx)}" cy="{f(cy+q*0.1)}" r="{f(q*0.22)}" fill="{col}"/>'
    elif glifo == "juego":
        o += f'<rect x="{f(cx-q)}" y="{f(cy-q*0.5)}" width="{f(2*q)}" height="{f(q)}" rx="{f(q*0.5)}" fill="{W}" stroke="{INK}" stroke-width="3"/>'
        o += f'<path d="M {f(cx-q*0.6)} {f(cy)} L {f(cx-q*0.2)} {f(cy)} M {f(cx-q*0.4)} {f(cy-q*0.2)} L {f(cx-q*0.4)} {f(cy+q*0.2)}" stroke="{INK}" stroke-width="4"/>'
        o += f'<circle cx="{f(cx+q*0.45)}" cy="{f(cy)}" r="{f(q*0.14)}" fill="{CORAL}"/>'
    else:  # estrella
        p = []
        for k in range(10):
            rr = q if k % 2 == 0 else q * 0.45
            a = math.radians(-90 + k * 36)
            p.append(f"{f(cx+rr*math.cos(a))},{f(cy+rr*math.sin(a))}")
        o += f'<polygon points="{" ".join(p)}" fill="{W}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
    o += brillo(f"M {f(cx-h+s*0.16)} {f(cy-h+s*0.12)} L {f(cx+h*0.1)} {f(cy-h+s*0.12)}", max(3, s * 0.04), 0.55)
    return Pieza(g(id_, o), {"centro": (cx, cy)}, (cx - h, cy - h, cx + h, cy + h))


# ------------------------------------------------------------------ barra de almacenamiento
def barra_almacenamiento(id_, x, y, w, h=46, frac=0.95, col=CORAL, texto=None, size=None):
    """Barra horizontal de «almacenamiento ocupado». Sub-id {id}_lleno (grow origin left o pulse). .puntos: fin."""
    size = size or h * 0.6
    o = f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{f(h/2)}" fill="#DCE1EA" stroke="{INK}" stroke-width="5"/>'
    lw = max(w * frac, h)
    lleno = (f'<rect x="{f(x+4)}" y="{f(y+4)}" width="{f(lw-8)}" height="{f(h-8)}" rx="{f((h-8)/2)}" fill="{degradado(col, 0.25)}"/>'
             + brillo(f"M {f(x+h*0.5)} {f(y+h*0.3)} L {f(x+lw-h*0.5)} {f(y+h*0.3)}", max(3, h * 0.1), 0.5))
    o += g(f"{id_}_lleno" if id_ else None, lleno)
    if texto:
        o += T(x, y - size * 0.55, texto, size, INK, anchor="start")
    return Pieza(g(id_, o), {"fin": (x + lw, y + h / 2)}, (x, y, x + w, y + h))


# ------------------------------------------------------------------ pantallas para casa.movil
def pantalla_cargando(id_, x0, y0, x1, y1, app_col=CORAL, glifo="play"):
    """Contenido de pantalla: app que no termina de abrir (icono + rueda de carga en {id}_rueda: spin)."""
    cx, w = (x0 + x1) / 2, x1 - x0
    o = f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(y1-y0)}" fill="#F2F4F8"/>'
    o += icono_app(None, cx, y0 + (y1 - y0) * 0.33, w * 0.42, app_col, glifo)
    r = w * 0.14
    cy = y0 + (y1 - y0) * 0.66
    rueda = ""
    for k in range(8):
        a = math.radians(k * 45)
        op = 0.2 + 0.8 * k / 7
        rueda += (f'<path d="M {f(cx+r*0.5*math.cos(a))} {f(cy+r*0.5*math.sin(a))} L {f(cx+r*math.cos(a))} {f(cy+r*math.sin(a))}" '
                  f'stroke="{INK}" stroke-width="{f(r*0.22)}" stroke-linecap="round" opacity="{op:.2f}"/>')
    o += g(f"{id_}_rueda" if id_ else None, rueda)
    return o


def pantalla_almacenamiento(id_, x0, y0, x1, y1, usado="63,7", total="64 GB", frac=0.97):
    """Contenido de pantalla: Ajustes > Almacenamiento casi lleno (barra en {id}_barra, aviso en {id}_aviso)."""
    cx, w = (x0 + x1) / 2, x1 - x0
    o = f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(y1-y0)}" fill="#F2F4F8"/>'
    o += T(x0 + w * 0.08, y0 + w * 0.3, "Almacenamiento", w * 0.085, INK, anchor="start")
    o += T(x0 + w * 0.08, y0 + w * 0.45, f"{usado} de {total}", w * 0.065, "#5A6170", anchor="start")
    o += barra_almacenamiento(f"{id_}_barra" if id_ else None, x0 + w * 0.08, y0 + w * 0.55, w * 0.84, w * 0.11, frac, CORAL)
    filas = ((CORAL, "Fotos"), (VIO, "Apps"), (YEL, "Sistema"), (TEAL, "Mensajes"))
    for k, (c, t) in enumerate(filas):
        yy = y0 + w * (0.88 + k * 0.17)
        o += f'<rect x="{f(x0+w*0.08)}" y="{f(yy-w*0.05)}" width="{f(w*0.07)}" height="{f(w*0.07)}" rx="4" fill="{c}" stroke="{INK}" stroke-width="2"/>'
        o += T(x0 + w * 0.2, yy + w * 0.012, t, w * 0.06, INK, anchor="start")
    ay = y0 + w * 1.6
    aviso = (f'<rect x="{f(x0+w*0.06)}" y="{f(ay)}" width="{f(w*0.88)}" height="{f(w*0.2)}" rx="12" fill="{CORAL}" stroke="{INK}" stroke-width="3"/>'
             + T(cx, ay + w * 0.125, "CASI LLENO", w * 0.075, "#FFFFFF", font=DISP))
    o += g(f"{id_}_aviso" if id_ else None, aviso)
    return o


def pantalla_salud(id_, x0, y0, x1, y1, pct="78 %"):
    """Contenido de pantalla: Ajustes > Batería > Salud (cifra en {id}_pct)."""
    cx, w = (x0 + x1) / 2, x1 - x0
    o = f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(y1-y0)}" fill="#F2F4F8"/>'
    o += T(x0 + w * 0.08, y0 + w * 0.3, "Batería", w * 0.09, INK, anchor="start")
    o += T(x0 + w * 0.08, y0 + w * 0.46, "Salud de la batería", w * 0.065, "#5A6170", anchor="start")
    o += bateria(None, cx, y0 + w * 0.95, w * 0.3, w * 0.5, 0.78, rayo=False)
    o += g(f"{id_}_pct" if id_ else None, T(cx, y0 + w * 1.48, pct, w * 0.16, CORAL, font=DISP))
    o += T(cx, y0 + w * 1.62, "Capacidad máxima", w * 0.06, "#5A6170")
    return o


# ------------------------------------------------------------------ papelera
def papelera(id_, cx, base, w=160):
    """Papelera metálica (borrar, liberar espacio). Tapa en {id}_tapa (move rotate para abrir, origin bottom-left)."""
    h = w * 1.15
    x0 = cx - w / 2
    o = sombra(cx, base + 6, w * 0.6, 14)
    o += f'<path d="M {f(x0)} {f(base-h)} L {f(x0+w)} {f(base-h)} L {f(x0+w*0.88)} {f(base)} L {f(x0+w*0.12)} {f(base)} Z" fill="url(#papeleraG)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
    for k in (0.3, 0.5, 0.7):
        o += f'<path d="M {f(x0+w*k)} {f(base-h*0.85)} L {f(x0+w*(0.5+(k-0.5)*0.8))} {f(base-h*0.1)}" stroke="{INK}" stroke-width="4" opacity="0.5"/>'
    tapa = (f'<rect x="{f(x0-w*0.08)}" y="{f(base-h-w*0.14)}" width="{f(w*1.16)}" height="{f(w*0.14)}" rx="8" fill="{degradado(GRIS, 0.25)}" stroke="{INK}" stroke-width="6"/>'
            f'<rect x="{f(cx-w*0.15)}" y="{f(base-h-w*0.24)}" width="{f(w*0.3)}" height="{f(w*0.12)}" rx="6" fill="{GRIS}" stroke="{INK}" stroke-width="5"/>')
    o += g(f"{id_}_tapa" if id_ else None, tapa)
    return Pieza(g(id_, o), {"boca": (cx, base - h - w * 0.2)}, (x0 - w * 0.08, base - h - w * 0.24, x0 + w * 1.08, base))


# ------------------------------------------------------------------ armario a reventar
def armario(id_, cx, base, w=420, h=620, lleno=True, abierto=False):
    """Armario de madera de dos puertas. lleno=True: ropa asomando por las rendijas y una manga fuera ({id}_ropa: shake/wiggle);
    abierto=True: puertas abiertas con la ropa apretada dentro. .puntos: centro, puerta_izq, puerta_der, techo."""
    x0, y0 = cx - w / 2, base - h
    o = sombra(cx, base + 8, w * 0.6, 20)
    o += f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" rx="14" fill="url(#armarioG)" stroke="{INK}" stroke-width="8"/>'
    o += f'<rect x="{f(x0-14)}" y="{f(y0-26)}" width="{f(w+28)}" height="34" rx="8" fill="{degradado("#B87842", 0.25)}" stroke="{INK}" stroke-width="7"/>'
    cols = (CORAL, TEAL, YEL, VIO, "#FF7EB6", LIME, "#2347FF")
    ropa = ""
    if abierto:
        o += f'<rect x="{f(x0+18)}" y="{f(y0+18)}" width="{f(w-36)}" height="{f(h-60)}" rx="6" fill="#5B3A1E" stroke="{INK}" stroke-width="5"/>'
        n = 9
        for k in range(n):
            xx = x0 + 30 + k * (w - 60) / n
            c = cols[k % len(cols)]
            ropa += f'<rect x="{f(xx)}" y="{f(y0+40)}" width="{f((w-60)/n+6)}" height="{f(h*0.55 + (k%3)*18)}" rx="10" fill="{degradado(c, 0.25)}" stroke="{INK}" stroke-width="4"/>'
        for k in range(4):
            xx = x0 + 40 + k * (w - 80) / 4
            ropa += f'<rect x="{f(xx)}" y="{f(base-h*0.32)}" width="{f((w-80)/4+10)}" height="{f(h*0.24)}" rx="10" fill="{degradado(cols[(k+3)%7], 0.25)}" stroke="{INK}" stroke-width="4"/>'
    else:
        # rendija central con ropa asomando
        for k in range(5):
            yy = y0 + h * (0.15 + k * 0.16)
            c = cols[k % len(cols)]
            ropa += (f'<path d="M {f(cx-6)} {f(yy)} C {f(cx+30)} {f(yy+8)}, {f(cx+26)} {f(yy+44)}, {f(cx-4)} {f(yy+56)} Z" '
                     f'fill="{degradado(c, 0.25)}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')
        # manga colgando por abajo
        ropa += (f'<path d="M {f(cx-30)} {f(base-h*0.12)} C {f(cx-60)} {f(base+10)}, {f(cx-120)} {f(base+20)}, {f(cx-150)} {f(base+4)} '
                 f'L {f(cx-140)} {f(base-22)} C {f(cx-110)} {f(base-10)}, {f(cx-70)} {f(base-20)}, {f(cx-50)} {f(base-h*0.14)} Z" '
                 f'fill="{degradado(TEAL, 0.25)}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
        ropa += (f'<path d="M {f(x0+w*0.72)} {f(y0-6)} C {f(x0+w*0.8)} {f(y0-60)}, {f(x0+w*0.95)} {f(y0-50)}, {f(x0+w*0.9)} {f(y0-10)} Z" '
                 f'fill="{degradado(YEL, 0.25)}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    if not abierto:
        for k in (-1, 1):
            px = x0 + 14 if k < 0 else cx + 3
            o += f'<rect x="{f(px)}" y="{f(y0+14)}" width="{f(w/2-17)}" height="{f(h-56)}" rx="8" fill="{degradado("#D9985E", 0.2, "h")}" stroke="{INK}" stroke-width="5"/>'
            o += f'<rect x="{f(px+24)}" y="{f(y0+44)}" width="{f(w/2-65)}" height="{f(h*0.36)}" rx="6" fill="none" stroke="{INK}" stroke-width="3" opacity="0.35"/>'
            o += f'<rect x="{f(px+24)}" y="{f(y0+64+h*0.36)}" width="{f(w/2-65)}" height="{f(h*0.36)}" rx="6" fill="none" stroke="{INK}" stroke-width="3" opacity="0.35"/>'
            o += f'<circle cx="{f(cx + k*22)}" cy="{f(y0+h*0.5)}" r="9" fill="url(#amarilloG)" stroke="{INK}" stroke-width="4"/>'
    o += g(f"{id_}_ropa" if id_ else None, ropa)
    o += brillo(f"M {f(x0+16)} {f(y0+24)} L {f(x0+16)} {f(y0+h*0.5)}", 6, 0.5)
    return Pieza(g(id_, o), {"centro": (cx, y0 + h / 2), "puerta_izq": (x0 + w * 0.25, y0 + h / 2),
                             "puerta_der": (x0 + w * 0.75, y0 + h / 2), "techo": (cx, y0 - 26)}, (x0 - 14, y0 - 60, x0 + w + 14, base + 20))


# ------------------------------------------------------------------ brazo robótico de laboratorio (lote9-05-cosquillas)
def brazo_robot(id_, bx, base, s=1.0, hombro=-60, codo=70, herramienta="pluma", col="#FF9F2E"):
    """Brazo robótico de laboratorio sobre su peana, con una pluma (o una pinza) en la punta.
    (bx, base) = centro de la peana en la mesa; s=1 → unos 300 de alto. hombro = ángulo del brazo (0 = derecha, -90 = arriba),
    codo = giro del antebrazo respecto al brazo (positivo = hacia abajo, a la derecha de la pantalla).
    Pivotes listos para el motor (origin "center"): {id}_brazo gira en el hombro, {id}_antebrazo en el codo,
    {id}_punta (pluma o pinza) en la muñeca; {id}_led (pulse). .puntos: punta, hombro, codo, muneca."""
    from .mente import pivote, pluma
    L1, L2 = 150 * s, 135 * s
    hx, hy = bx, base - 70 * s
    a1 = math.radians(hombro)
    ex, ey = hx + L1 * math.cos(a1), hy + L1 * math.sin(a1)
    a2 = math.radians(hombro + codo)
    wx, wy = ex + L2 * math.cos(a2), ey + L2 * math.sin(a2)
    gris = "#C9D0DC"
    # peana
    o = sombra(bx, base + 4, 95 * s, 12 * s, 0.25)
    o += f'<path d="M {f(bx-85*s)} {f(base)} L {f(bx-62*s)} {f(base-40*s)} L {f(bx+62*s)} {f(base-40*s)} L {f(bx+85*s)} {f(base)} Z" fill="{degradado("#3A4258", 0.2)}" stroke="{INK}" stroke-width="{f(7*s)}" stroke-linejoin="round"/>'
    o += g(f"{id_}_led" if id_ else None, f'<circle cx="{f(bx+42*s)}" cy="{f(base-20*s)}" r="{f(7*s)}" fill="{LIME}" stroke="{INK}" stroke-width="3"/>')
    o += f'<rect x="{f(bx-34*s)}" y="{f(hy)}" width="{f(68*s)}" height="{f(base-40*s-hy+4)}" fill="url(#metalG)" stroke="{INK}" stroke-width="{f(6*s)}"/>'
    # muñeca y herramienta
    if herramienta == "pluma":
        tool = pluma(f"{id_}_pl" if id_ else None, wx, wy, 150 * s, math.degrees(a2) + 10)
        punta = tool.puntos["punta"]
    else:
        b2 = math.radians(math.degrees(a2) + 90)
        tool = "".join(trazo(f"M {f(wx)} {f(wy)} L {f(wx + 40*s*math.cos(a2) + k*16*s*math.cos(b2))} {f(wy + 40*s*math.sin(a2) + k*16*s*math.sin(b2))}", 9 * s, gris, 5) for k in (-1, 1))
        punta = (wx + 40 * s * math.cos(a2), wy + 40 * s * math.sin(a2))
    punta_g = g(f"{id_}_punta" if id_ else None, pivote(wx, wy, 170 * s) + tool)
    ante = trazo(f"M {f(ex)} {f(ey)} L {f(wx)} {f(wy)}", 30 * s, col, 7)
    ante += brillo(f"M {f(ex + 10*s*math.cos(a2))} {f(ey + 10*s*math.sin(a2) - 7*s)} L {f(wx - 16*s*math.cos(a2))} {f(wy - 16*s*math.sin(a2) - 7*s)}", 4 * s, 0.55)
    ante += f'<circle cx="{f(wx)}" cy="{f(wy)}" r="{f(17*s)}" fill="url(#metalG)" stroke="{INK}" stroke-width="{f(6*s)}"/>'
    ante_g = g(f"{id_}_antebrazo" if id_ else None, pivote(ex, ey, L2 + 175 * s) + ante + punta_g)
    brazo = trazo(f"M {f(hx)} {f(hy)} L {f(ex)} {f(ey)}", 38 * s, col, 7)
    brazo += brillo(f"M {f(hx + 12*s*math.cos(a1) - 8*s)} {f(hy + 12*s*math.sin(a1))} L {f(ex - 20*s*math.cos(a1) - 8*s)} {f(ey - 20*s*math.sin(a1))}", 5 * s, 0.55)
    codo_c = f'<circle cx="{f(ex)}" cy="{f(ey)}" r="{f(24*s)}" fill="url(#metalG)" stroke="{INK}" stroke-width="{f(6*s)}"/><circle cx="{f(ex)}" cy="{f(ey)}" r="{f(8*s)}" fill="{INK}"/>'
    hombro_c = f'<circle cx="{f(hx)}" cy="{f(hy)}" r="{f(30*s)}" fill="url(#metalG)" stroke="{INK}" stroke-width="{f(7*s)}"/><circle cx="{f(hx)}" cy="{f(hy)}" r="{f(10*s)}" fill="{INK}"/>'
    brazo_g = g(f"{id_}_brazo" if id_ else None, pivote(hx, hy, L1 + L2 + 180 * s) + brazo + ante_g + codo_c)
    o += brazo_g + hombro_c
    return Pieza(g(id_, o), {"punta": punta, "hombro": (hx, hy), "codo": (ex, ey), "muneca": (wx, wy)},
                 (min(bx - 90 * s, wx - 60 * s), min(ey, wy, punta[1]) - 60 * s, max(bx + 90 * s, wx + 60 * s, punta[0]), base + 16 * s))

"""Personaje base PARAMÉTRICO (vista de frente) en estilo pegatina realista.

    persona(id_, x, y, escala=1, edad="adulto", piel="media", pelo="corto", pelo_color="castano",
            ropa="jersey", ropa_color="#3B80CF", pantalon_color="#3E5C93", zapato_color="#2A2F3E",
            accesorios=(), expresion="neutral", pose="de_pie", brazos=("abajo", "abajo"), mira=0, silla=False)

(x, y) = punto del suelo entre los pies (de_pie / sentado) o centro del borde inferior (busto).
Altura a escala 1: adulto/joven ≈ 600, mayor ≈ 575, niño ≈ 400 (busto ≈ 330 / 220).

Ids internos (con el id_ como prefijo, p. ej. id_="ana" → "ana_cabeza"):
    {id}            todo el personaje (sin transform: anímalo con bob, breathe, shake, move…)
    {id}_cuerpo     tronco + piernas          {id}_piernas  piernas y zapatos
    {id}_cabeza     cabeza, pelo, cara y lo que lleva puesto en la cabeza (sway/wiggle con origin bottom = asentir)
    {id}_ojos       ojos (blink)              {id}_cejas    cejas     {id}_boca   boca (pulse = hablar)
    {id}_brazo_izq  brazo a la IZQUIERDA de la pantalla (wiggle/sway con origin top = saludar)
    {id}_brazo_der  brazo a la derecha de la pantalla
    {id}_mano_izq / {id}_mano_der  manos
    {id}_acc_<nombre>  cada accesorio (gafas, gorro, bufanda, pendientes, baston, barba, bigote)
Devuelve Pieza: .puntos = {"cabeza", "boca", "ojos", "mano_izq", "mano_der", "pies", "cima", "hombro_izq", "hombro_der"}
en coordenadas finales (para colocar bocadillos, objetos en la mano, etiquetas…).

Variantes:
    edad: nino, joven, adulto, mayor
    piel: clara, media, morena, oscura
    pelo: corto, largo, rizado, coleta, mono (moño), calvo, rapado, None
    pelo_color: castano, negro, rubio, pelirrojo, canoso, blanco o un hex
    ropa: camiseta, jersey, camisa, chaqueta, vestido, abrigo
    accesorios: gafas, gorro, bufanda, pendientes, baston, barba, bigote
    expresion: neutral, sorpresa, risa, duda, frio, sueno, triste, enfado
    pose: de_pie, sentado, busto
    brazos (izq, der): abajo, cintura, arriba, saluda, senala, barbilla, coge, cruzados (los dos: abrazarse de frío)
    mira: -1 izquierda, 0 frente, 1 derecha (pupilas)
Sale de: escalofrios/persona.py (gorro de lana, bufanda, cara de frío, castañeteo), lote4-01-bebe-carrito/dib.py
(bebé y mamá: degradados de piel y pelo, mejillas, brillos) y nuevo-partido/np.py (pictograma).
"""
import math
from .base import (INK, LIME, CORAL, f, g, shade, smooth, poly, trazo, sombra, brillo, lg, rg, registrar_defs,
                   degradado, Pieza)

# ------------------------------------------------------------------ paletas
PIELES = {  # claro, medio, oscuro (degradado radial de la cara), línea de detalle
    "clara": ("#FCDCC3", "#F3BE98", "#E3A07A", "#C98763"),
    "media": ("#F7CFB2", "#EDB08C", "#C98462", "#B0715A"),
    "morena": ("#E9B58C", "#C98A5E", "#A3683F", "#8A5434"),
    "oscura": ("#A9714C", "#865234", "#5E361D", "#4A2914"),
}
PELOS = {"castano": "#7A4E2B", "negro": "#2A2230", "rubio": "#E3B04B", "pelirrojo": "#C8562A",
         "canoso": "#BFC4CC", "blanco": "#EEF0F4"}

for _k, (_a, _b, _c, _l) in PIELES.items():
    registrar_defs(rg(f"piel_{_k}", [(0, _a), (0.7, _b), (1, _c)], 0.42, 0.35, 0.75),
                   lg(f"pielL_{_k}", [(0, _a), (1, _c)]))

EDADES = {
    #        cabeza (rx, ry, y)   hombros y, semiancho   cadera y, semiancho  brazo, pierna, cuello
    "nino":   dict(rx=56, ry=60, hy=-338, sy=-268, sw=50, cy=-150, cw=46, aw=24, lw=30, nw=13),
    "joven":  dict(rx=53, ry=62, hy=-536, sy=-452, sw=74, cy=-262, cw=58, aw=28, lw=34, nw=17),
    "adulto": dict(rx=56, ry=64, hy=-534, sy=-450, sw=82, cy=-262, cw=66, aw=31, lw=37, nw=19),
    "mayor":  dict(rx=56, ry=63, hy=-512, sy=-430, sw=78, cy=-250, cw=70, aw=30, lw=35, nw=18),
}
SW = 7  # contorno


def _col_pelo(c):
    return PELOS.get(c, c) if c else None


def _ik(S, H, a, b, k):
    """Codo de un brazo de dos tramos (a, b) del hombro S a la mano H; el codo sale hacia fuera (k = -1 izq, 1 der)."""
    dx, dy = H[0] - S[0], H[1] - S[1]
    d = math.hypot(dx, dy)
    d = max(1e-3, min(d, (a + b) * 0.995))
    H = (S[0] + dx / max(1e-3, math.hypot(dx, dy)) * d, S[1] + dy / max(1e-3, math.hypot(dx, dy)) * d)
    ca = max(-1, min(1, (a * a + d * d - b * b) / (2 * a * d)))
    A = math.acos(ca)
    base = math.atan2(dy, dx)
    cands = [(S[0] + a * math.cos(base + s * A), S[1] + a * math.sin(base + s * A)) for s in (1, -1)]
    E = max(cands, key=lambda p: k * p[0] + 0.3 * p[1])  # hacia fuera y algo hacia abajo
    return E, H


# ------------------------------------------------------------------ cabeza
def _ojos(e, rx, ry, hy, exp, mira, tinta=INK):
    ex, ey = rx * 0.36, hy - ry * 0.02
    px = mira * rx * 0.07
    o = ""
    for k in (-1, 1):
        x = k * ex
        if exp == "sorpresa":
            o += f'<ellipse cx="{f(x)}" cy="{f(ey)}" rx="{f(rx*0.2)}" ry="{f(ry*0.21)}" fill="#FFFFFF" stroke="{tinta}" stroke-width="4.5"/>'
            o += f'<circle cx="{f(x+px)}" cy="{f(ey+1)}" r="{f(rx*0.1)}" fill="{tinta}"/><circle cx="{f(x+px-2.5)}" cy="{f(ey-3)}" r="2.8" fill="#FFFFFF"/>'
        elif exp == "risa":
            o += f'<path d="M {f(x-rx*0.15)} {f(ey+3)} Q {f(x)} {f(ey-ry*0.17)} {f(x+rx*0.15)} {f(ey+3)}" fill="none" stroke="{tinta}" stroke-width="6" stroke-linecap="round"/>'
        elif exp == "frio":
            s = -k  # > <
            o += f'<path d="M {f(x-s*rx*0.14)} {f(ey-ry*0.09)} L {f(x+s*rx*0.12)} {f(ey)} L {f(x-s*rx*0.14)} {f(ey+ry*0.09)}" fill="none" stroke="{tinta}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>'
        elif exp == "sueno":
            o += f'<path d="M {f(x-rx*0.15)} {f(ey)} Q {f(x)} {f(ey+ry*0.1)} {f(x+rx*0.15)} {f(ey)}" fill="none" stroke="{tinta}" stroke-width="5.5" stroke-linecap="round"/>'
            o += f'<path d="M {f(x-rx*0.17)} {f(ey-ry*0.05)} L {f(x+rx*0.17)} {f(ey-ry*0.05)}" stroke="{tinta}" stroke-width="3" stroke-linecap="round" opacity="0.5"/>'
        else:
            dy = -ry * 0.04 if exp == "duda" else 0
            o += f'<ellipse cx="{f(x+px)}" cy="{f(ey+dy)}" rx="{f(rx*0.115)}" ry="{f(ry*0.15)}" fill="{tinta}"/>'
            o += f'<circle cx="{f(x+px+rx*0.04)}" cy="{f(ey+dy-ry*0.06)}" r="{f(rx*0.045)}" fill="#FFFFFF"/>'
    return o


def _cejas(rx, ry, hy, exp, col):
    by = hy - ry * 0.27
    o = ""
    for k in (-1, 1):
        x0, x1 = k * rx * 0.2, k * rx * 0.55
        if exp == "sorpresa":
            d = f"M {f(x0)} {f(by-ry*0.12)} Q {f((x0+x1)/2)} {f(by-ry*0.24)} {f(x1)} {f(by-ry*0.1)}"
        elif exp in ("frio", "triste"):
            d = f"M {f(x0)} {f(by-ry*0.06)} L {f(x1)} {f(by+ry*0.06)}"
        elif exp == "enfado":
            d = f"M {f(x0)} {f(by+ry*0.08)} L {f(x1)} {f(by-ry*0.06)}"
        elif exp == "duda":
            d = (f"M {f(x0)} {f(by-ry*0.14)} Q {f((x0+x1)/2)} {f(by-ry*0.26)} {f(x1)} {f(by-ry*0.12)}" if k < 0
                 else f"M {f(x0)} {f(by+ry*0.02)} L {f(x1)} {f(by+ry*0.02)}")
        elif exp == "sueno":
            d = f"M {f(x0)} {f(by+ry*0.05)} Q {f((x0+x1)/2)} {f(by)} {f(x1)} {f(by+ry*0.06)}"
        else:
            d = f"M {f(x0)} {f(by)} Q {f((x0+x1)/2)} {f(by-ry*0.08)} {f(x1)} {f(by+ry*0.01)}"
        o += f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{f(rx*0.13)}" stroke-linecap="round"/>'
    return o


def _boca(rx, ry, hy, exp):
    my = hy + ry * 0.5
    w = rx * 0.32
    if exp == "sorpresa":
        return (f'<ellipse cx="0" cy="{f(my+ry*0.03)}" rx="{f(rx*0.14)}" ry="{f(ry*0.15)}" fill="#7A1F2B" stroke="{INK}" stroke-width="4.5"/>'
                f'<ellipse cx="0" cy="{f(my+ry*0.1)}" rx="{f(rx*0.08)}" ry="{f(ry*0.05)}" fill="#FF8FA0"/>')
    if exp == "risa":
        d = f"M {f(-w*1.2)} {f(my-ry*0.06)} Q 0 {f(my-ry*0.1)} {f(w*1.2)} {f(my-ry*0.06)} Q {f(w*1.05)} {f(my+ry*0.32)} 0 {f(my+ry*0.32)} Q {f(-w*1.05)} {f(my+ry*0.32)} {f(-w*1.2)} {f(my-ry*0.06)} Z"
        return (f'<path d="{d}" fill="#7A1F2B" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round"/>'
                f'<path d="M {f(-w*1.0)} {f(my-ry*0.04)} Q 0 {f(my-ry*0.07)} {f(w*1.0)} {f(my-ry*0.04)} L {f(w*0.9)} {f(my+ry*0.05)} Q 0 {f(my+ry*0.03)} {f(-w*0.9)} {f(my+ry*0.05)} Z" fill="#FFFFFF"/>'
                f'<ellipse cx="0" cy="{f(my+ry*0.24)}" rx="{f(w*0.55)}" ry="{f(ry*0.07)}" fill="#FF8FA0"/>')
    if exp == "frio":
        x0, y0, ww, hh = -w * 1.1, my - ry * 0.08, w * 2.2, ry * 0.26
        return (f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(ww)}" height="{f(hh)}" rx="{f(hh*0.3)}" fill="#FFFFFF" stroke="{INK}" stroke-width="4.5"/>'
                f'<line x1="{f(x0)}" y1="{f(y0+hh/2)}" x2="{f(x0+ww)}" y2="{f(y0+hh/2)}" stroke="{INK}" stroke-width="3"/>'
                + "".join(f'<line x1="{f(x0+ww*t)}" y1="{f(y0+2)}" x2="{f(x0+ww*t)}" y2="{f(y0+hh-2)}" stroke="{INK}" stroke-width="2.5"/>' for t in (0.25, 0.5, 0.75)))
    if exp == "sueno":
        return f'<ellipse cx="{f(w*0.1)}" cy="{f(my+ry*0.03)}" rx="{f(rx*0.1)}" ry="{f(ry*0.12)}" fill="#7A1F2B" stroke="{INK}" stroke-width="4"/>'
    if exp == "duda":
        return f'<path d="M {f(-w*0.6)} {f(my+ry*0.04)} Q {f(-w*0.1)} {f(my-ry*0.04)} {f(w*0.3)} {f(my+ry*0.03)} T {f(w*1.2)} {f(my-ry*0.03)}" fill="none" stroke="{INK}" stroke-width="5.5" stroke-linecap="round"/>'
    if exp in ("triste", "enfado"):
        return f'<path d="M {f(-w)} {f(my+ry*0.08)} Q 0 {f(my-ry*0.1)} {f(w)} {f(my+ry*0.08)}" fill="none" stroke="{INK}" stroke-width="5.5" stroke-linecap="round"/>'
    return f'<path d="M {f(-w)} {f(my-ry*0.02)} Q 0 {f(my+ry*0.16)} {f(w)} {f(my-ry*0.02)}" fill="none" stroke="{INK}" stroke-width="5.5" stroke-linecap="round"/>'


def _pelo_detras(estilo, rx, ry, hy, col):
    if estilo == "largo":
        d = (f"M {f(-rx*1.08)} {f(hy-ry*0.2)} C {f(-rx*1.2)} {f(hy-ry*1.3)}, {f(rx*1.2)} {f(hy-ry*1.3)}, {f(rx*1.08)} {f(hy-ry*0.2)} "
             f"C {f(rx*1.2)} {f(hy+ry*0.6)}, {f(rx*1.3)} {f(hy+ry*1.2)}, {f(rx*1.18)} {f(hy+ry*1.45)} "
             f"Q {f(rx*0.6)} {f(hy+ry*1.6)} {f(rx*0.3)} {f(hy+ry*1.35)} L {f(-rx*0.3)} {f(hy+ry*1.35)} "
             f"Q {f(-rx*0.6)} {f(hy+ry*1.6)} {f(-rx*1.18)} {f(hy+ry*1.45)} C {f(-rx*1.3)} {f(hy+ry*1.2)}, {f(-rx*1.2)} {f(hy+ry*0.6)}, {f(-rx*1.08)} {f(hy-ry*0.2)} Z")
        return f'<path d="{d}" fill="{degradado(col, 0.22)}" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>'
    if estilo == "coleta":
        d = (f"M {f(rx*0.7)} {f(hy-ry*0.55)} C {f(rx*1.7)} {f(hy-ry*0.7)}, {f(rx*1.75)} {f(hy+ry*0.5)}, {f(rx*1.3)} {f(hy+ry*1.2)} "
             f"C {f(rx*1.25)} {f(hy+ry*0.6)}, {f(rx*1.05)} {f(hy)}, {f(rx*0.75)} {f(hy-ry*0.25)} Z")
        return (f'<path d="{d}" fill="{degradado(col, 0.22)}" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>'
                f'<path d="M {f(rx*1.2)} {f(hy-ry*0.25)} Q {f(rx*1.42)} {f(hy+ry*0.3)} {f(rx*1.33)} {f(hy+ry*0.8)}" fill="none" stroke="{shade(col, 0.35)}" stroke-width="4" stroke-linecap="round" opacity="0.8"/>'
                f'<ellipse cx="{f(rx*0.95)}" cy="{f(hy-ry*0.45)}" rx="{f(rx*0.12)}" ry="{f(ry*0.13)}" fill="{CORAL}" stroke="{INK}" stroke-width="4"/>')
    if estilo == "mono":
        return (f'<circle cx="0" cy="{f(hy-ry*1.02)}" r="{f(rx*0.42)}" fill="{degradado(col, 0.22)}" stroke="{INK}" stroke-width="{SW}"/>'
                f'<path d="M {f(-rx*0.22)} {f(hy-ry*1.15)} Q 0 {f(hy-ry*1.32)} {f(rx*0.24)} {f(hy-ry*1.12)}" fill="none" stroke="{shade(col, -0.3)}" stroke-width="4" stroke-linecap="round"/>')
    if estilo == "rizado":
        return ""
    return ""


def _pelo_delante(estilo, rx, ry, hy, col):
    hl = shade(col, 0.4)
    gr = degradado(col, 0.22)
    if estilo in ("corto", "largo", "coleta"):
        d = (f"M {f(-rx-3)} {f(hy-ry*0.05)} C {f(-rx-8)} {f(hy-ry*1.28)}, {f(rx+8)} {f(hy-ry*1.28)}, {f(rx+3)} {f(hy-ry*0.05)} "
             f"C {f(rx*0.95)} {f(hy-ry*0.42)}, {f(rx*0.55)} {f(hy-ry*0.6)}, {f(rx*0.12)} {f(hy-ry*0.52)} "
             f"C {f(-rx*0.28)} {f(hy-ry*0.72)}, {f(-rx*0.85)} {f(hy-ry*0.55)}, {f(-rx-3)} {f(hy-ry*0.05)} Z")
        s = f'<path d="{d}" fill="{gr}" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>'
        if estilo == "largo":  # mechones laterales sobre las orejas
            for k in (-1, 1):
                s += (f'<path d="M {f(k*(rx+3))} {f(hy-ry*0.2)} C {f(k*(rx+10))} {f(hy+ry*0.4)}, {f(k*(rx+4))} {f(hy+ry*0.85)}, {f(k*rx*0.86)} {f(hy+ry*1.1)} '
                      f'C {f(k*rx*0.9)} {f(hy+ry*0.6)}, {f(k*rx*0.8)} {f(hy+ry*0.1)}, {f(k*rx*0.72)} {f(hy-ry*0.35)} Z" fill="{gr}" stroke="{INK}" stroke-width="{SW-1}" stroke-linejoin="round"/>')
        s += brillo(f"M {f(-rx*0.55)} {f(hy-ry*0.88)} Q {f(-rx*0.1)} {f(hy-ry*1.08)} {f(rx*0.4)} {f(hy-ry*0.95)}", 5, 0.7, hl)
        return s
    if estilo == "rapado" or estilo == "mono":
        d = (f"M {f(-rx-2)} {f(hy-ry*0.15)} C {f(-rx-6)} {f(hy-ry*1.2)}, {f(rx+6)} {f(hy-ry*1.2)}, {f(rx+2)} {f(hy-ry*0.15)} "
             f"C {f(rx*0.8)} {f(hy-ry*0.62)}, {f(-rx*0.8)} {f(hy-ry*0.62)}, {f(-rx-2)} {f(hy-ry*0.15)} Z")
        op = ' opacity="0.9"' if estilo == "rapado" else ""
        s = f'<path d="{d}" fill="{gr}" stroke="{INK}" stroke-width="{SW-1}" stroke-linejoin="round"{op}/>'
        if estilo == "mono":
            s += "".join(f'<path d="M {f(k*rx*0.15)} {f(hy-ry*0.66)} Q {f(k*rx*0.5)} {f(hy-ry*0.9)} {f(k*rx*0.2)} {f(hy-ry*1.1)}" fill="none" stroke="{shade(col,-0.3)}" stroke-width="3.5" stroke-linecap="round"/>' for k in (-1, 1))
        s += brillo(f"M {f(-rx*0.5)} {f(hy-ry*0.85)} Q {f(-rx*0.1)} {f(hy-ry*1.02)} {f(rx*0.35)} {f(hy-ry*0.92)}", 5, 0.6, hl)
        return s
    if estilo == "calvo":  # pelo solo en los lados + brillo de calva
        s = ""
        for k in (-1, 1):
            s += (f'<path d="M {f(k*(rx+4))} {f(hy+ry*0.05)} C {f(k*(rx+10))} {f(hy-ry*0.4)}, {f(k*rx*0.9)} {f(hy-ry*0.62)}, {f(k*rx*0.6)} {f(hy-ry*0.55)} '
                  f'C {f(k*rx*0.8)} {f(hy-ry*0.35)}, {f(k*rx*0.88)} {f(hy-ry*0.1)}, {f(k*rx*0.86)} {f(hy+ry*0.08)} Z" fill="{gr}" stroke="{INK}" stroke-width="{SW-1}" stroke-linejoin="round"/>')
        s += f'<ellipse cx="{f(-rx*0.3)}" cy="{f(hy-ry*0.72)}" rx="{f(rx*0.22)}" ry="{f(ry*0.1)}" fill="#FFFFFF" opacity="0.55" transform="rotate(-20 {f(-rx*0.3)} {f(hy-ry*0.72)})"/>'
        return s
    if estilo == "rizado":
        blobs = []
        n = 11
        for i in range(n):
            a = math.radians(190 + i * 160 / (n - 1))
            blobs.append((rx * 0.98 * math.cos(a), hy - ry * 0.12 + ry * 1.0 * math.sin(a), rx * (0.3 + 0.05 * (i % 3))))
        blobs += [(-rx * 0.4, hy - ry * 0.62, rx * 0.34), (rx * 0.3, hy - ry * 0.66, rx * 0.32), (0, hy - ry * 0.85, rx * 0.4)]
        c = "".join(f'<circle cx="{f(a)}" cy="{f(b)}" r="{f(r)}"/>' for a, b, r in blobs)
        s = f'<g fill="{INK}" stroke="{INK}" stroke-width="{SW*2}">{c}</g><g fill="{gr}">{c}</g>'
        s += "".join(f'<path d="M {f(a-r*0.4)} {f(b-r*0.1)} q {f(r*0.4)} {f(-r*0.5)} {f(r*0.8)} 0" fill="none" stroke="{hl}" stroke-width="3.5" stroke-linecap="round" opacity="0.8"/>' for a, b, r in blobs[2:9:2])
        return s
    return ""


def cabeza(id_, rx, ry, hy, piel="media", pelo="corto", pelo_color="castano", expresion="neutral", mira=0, accesorios=(), edad="adulto"):
    """Cabeza en coordenadas locales (centro en (0, hy)). Úsala dentro de persona(); también sirve suelta en un <g transform>."""
    pa, pb, pc, pl = PIELES.get(piel, PIELES["media"])
    pcol = _col_pelo(pelo_color)
    exp = expresion
    o = ""
    if pelo:
        o += _pelo_detras(pelo, rx, ry, hy, pcol)
    # orejas
    for k in (-1, 1):
        o += f'<ellipse cx="{f(k*rx*0.98)}" cy="{f(hy+ry*0.08)}" rx="{f(rx*0.2)}" ry="{f(ry*0.26)}" fill="{pb}" stroke="{INK}" stroke-width="{SW-1}"/>'
        o += f'<path d="M {f(k*rx*0.98)} {f(hy-ry*0.04)} Q {f(k*rx*1.06)} {f(hy+ry*0.08)} {f(k*rx*0.98)} {f(hy+ry*0.2)}" fill="none" stroke="{pl}" stroke-width="3" stroke-linecap="round"/>'
    if "pendientes" in accesorios:
        o += g(f"{id_}_acc_pendientes", "".join(
            f'<circle cx="{f(k*rx*1.0)}" cy="{f(hy+ry*0.4)}" r="{f(rx*0.09)}" fill="{degradado("#FFC83D")}" stroke="{INK}" stroke-width="3.5"/>' for k in (-1, 1)))
    # cara
    o += f'<ellipse cx="0" cy="{f(hy)}" rx="{f(rx)}" ry="{f(ry)}" fill="url(#piel_{piel if piel in PIELES else "media"})" stroke="{INK}" stroke-width="{SW+1}"/>'
    if edad == "mayor":  # arrugas suaves
        o += "".join(f'<path d="M {f(k*rx*0.62)} {f(hy-ry*0.02)} q {f(k*rx*0.1)} {f(ry*0.06)} 0 {f(ry*0.13)}" fill="none" stroke="{pl}" stroke-width="2.5" stroke-linecap="round" opacity="0.8"/>' for k in (-1, 1))
        o += f'<path d="M {f(-rx*0.3)} {f(hy-ry*0.45)} Q 0 {f(hy-ry*0.5)} {f(rx*0.3)} {f(hy-ry*0.45)}" fill="none" stroke="{pl}" stroke-width="2.5" stroke-linecap="round" opacity="0.6"/>'
    # mejillas
    mej = "#9EC9F0" if exp == "frio" else "#FF8FA0"
    o += "".join(f'<ellipse cx="{f(k*rx*0.56)}" cy="{f(hy+ry*0.3)}" rx="{f(rx*0.2)}" ry="{f(ry*0.11)}" fill="{mej}" opacity="{0.6 if exp == "frio" else 0.4}"/>' for k in (-1, 1))
    # nariz
    if exp == "frio":
        o += f'<ellipse cx="0" cy="{f(hy+ry*0.22)}" rx="{f(rx*0.17)}" ry="{f(ry*0.12)}" fill="#F07A6A" stroke="{INK}" stroke-width="4"/><circle cx="{f(-rx*0.05)}" cy="{f(hy+ry*0.18)}" r="{f(rx*0.04)}" fill="#FFFFFF" opacity="0.8"/>'
    else:
        o += f'<path d="M {f(-rx*0.06)} {f(hy+ry*0.12)} Q {f(rx*0.12)} {f(hy+ry*0.24)} {f(-rx*0.04)} {f(hy+ry*0.3)}" fill="none" stroke="{pl}" stroke-width="4" stroke-linecap="round"/>'
    o += g(f"{id_}_ojos", _ojos(None, rx, ry, hy, exp, mira))
    ceja_col = shade(pcol, -0.35) if pcol and pelo not in ("calvo",) else "#6B4632"
    if pcol and pelo_color in ("canoso", "blanco"):
        ceja_col = "#9AA0AA"
    o += g(f"{id_}_cejas", _cejas(rx, ry, hy, exp, ceja_col))
    if "barba" in accesorios:
        bc = degradado(pcol or "#5A3A22", 0.2)
        d = (f"M {f(-rx*0.98)} {f(hy+ry*0.05)} C {f(-rx*0.95)} {f(hy+ry*0.9)}, {f(-rx*0.4)} {f(hy+ry*1.22)}, 0 {f(hy+ry*1.22)} "
             f"C {f(rx*0.4)} {f(hy+ry*1.22)}, {f(rx*0.95)} {f(hy+ry*0.9)}, {f(rx*0.98)} {f(hy+ry*0.05)} "
             f"C {f(rx*0.8)} {f(hy+ry*0.45)}, {f(rx*0.45)} {f(hy+ry*0.32)}, 0 {f(hy+ry*0.34)} C {f(-rx*0.45)} {f(hy+ry*0.32)}, {f(-rx*0.8)} {f(hy+ry*0.45)}, {f(-rx*0.98)} {f(hy+ry*0.05)} Z")
        o += g(f"{id_}_acc_barba", f'<path d="{d}" fill="{bc}" stroke="{INK}" stroke-width="{SW-1}" stroke-linejoin="round"/>')
    bo = _boca(rx, ry, hy, exp)
    if "barba" in accesorios and exp not in ("risa", "sorpresa", "frio"):
        bo = f'<ellipse cx="0" cy="{f(hy+ry*0.55)}" rx="{f(rx*0.22)}" ry="{f(ry*0.09)}" fill="#7A1F2B" stroke="{INK}" stroke-width="4"/>'
    o += g(f"{id_}_boca", bo)
    if "bigote" in accesorios or "barba" in accesorios:
        bcol = degradado(pcol or "#5A3A22", 0.2)
        d = (f"M 0 {f(hy+ry*0.36)} C {f(rx*0.2)} {f(hy+ry*0.28)}, {f(rx*0.5)} {f(hy+ry*0.34)}, {f(rx*0.52)} {f(hy+ry*0.5)} "
             f"C {f(rx*0.32)} {f(hy+ry*0.44)}, {f(rx*0.15)} {f(hy+ry*0.5)}, 0 {f(hy+ry*0.44)} C {f(-rx*0.15)} {f(hy+ry*0.5)}, {f(-rx*0.32)} {f(hy+ry*0.44)}, {f(-rx*0.52)} {f(hy+ry*0.5)} "
             f"C {f(-rx*0.5)} {f(hy+ry*0.34)}, {f(-rx*0.2)} {f(hy+ry*0.28)}, 0 {f(hy+ry*0.36)} Z")
        o += g(f"{id_}_acc_bigote", f'<path d="{d}" fill="{bcol}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')
    if pelo and "gorro" not in accesorios:
        o += _pelo_delante(pelo, rx, ry, hy, pcol)
    elif pelo == "largo" or pelo == "rizado":
        o += _pelo_delante(pelo, rx, ry, hy, pcol)
    if "gafas" in accesorios:
        ey = hy - ry * 0.02
        r = rx * 0.27
        gs = ""
        for k in (-1, 1):
            cx = k * rx * 0.36
            gs += f'<circle cx="{f(cx)}" cy="{f(ey)}" r="{f(r)}" fill="#DDF3FF" fill-opacity="0.25" stroke="{INK}" stroke-width="5.5"/>'
            gs += f'<path d="M {f(cx-r*0.55)} {f(ey-r*0.25)} Q {f(cx-r*0.35)} {f(ey-r*0.62)} {f(cx)} {f(ey-r*0.68)}" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" opacity="0.9"/>'
            gs += f'<path d="M {f(k*(rx*0.36+r))} {f(ey-r*0.2)} L {f(k*rx*0.98)} {f(ey-r*0.1)}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
        gs += f'<path d="M {f(-rx*0.36+r)} {f(ey-r*0.1)} Q 0 {f(ey-r*0.45)} {f(rx*0.36-r)} {f(ey-r*0.1)}" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
        o += g(f"{id_}_acc_gafas", gs)
    if "gorro" in accesorios:  # gorro de lana con pompón (escalofrios/persona.py)
        top = hy - ry * 1.18
        d = f"M {f(-rx*1.02)} {f(hy-ry*0.32)} C {f(-rx*1.05)} {f(top-ry*0.1)}, {f(rx*1.05)} {f(top-ry*0.1)}, {f(rx*1.02)} {f(hy-ry*0.32)} Z"
        gs = f'<path d="{d}" fill="url(#lanaR)" stroke="{INK}" stroke-width="{SW+1}" stroke-linejoin="round"/>'
        bx, by, bw, bh = -rx * 1.12, hy - ry * 0.52, rx * 2.24, ry * 0.36
        gs += f'<rect x="{f(bx)}" y="{f(by)}" width="{f(bw)}" height="{f(bh)}" rx="{f(bh*0.42)}" fill="#C83A30" stroke="{INK}" stroke-width="{SW+1}"/>'
        gs += f'<g stroke="#8E1F1A" stroke-width="4.5">' + "".join(
            f'<line x1="{f(bx+bw*t)}" y1="{f(by+5)}" x2="{f(bx+bw*t)}" y2="{f(by+bh-5)}"/>' for t in [i / 13 for i in range(1, 13)]) + "</g>"
        gs += brillo(f"M {f(-rx*0.6)} {f(top+ry*0.35)} Q {f(-rx*0.2)} {f(top+ry*0.05)} {f(rx*0.3)} {f(top+ry*0.12)}", 5, 0.5, "#FFB3A8")
        gs += f'<circle cx="0" cy="{f(top-ry*0.06)}" r="{f(rx*0.3)}" fill="#FFF3E6" stroke="{INK}" stroke-width="{SW}"/>'
        o += g(f"{id_}_acc_gorro", gs)
    return o


registrar_defs(lg("lanaR", [(0, "#F0645A"), (1, "#A82A22")]))


# ------------------------------------------------------------------ cuerpo
def _mano(x, y, r, piel, tipo="puno", k=1):
    pa, pb, pc, pl = PIELES.get(piel, PIELES["media"])
    s = ""
    if tipo == "senala":
        s += trazo(f"M {f(x)} {f(y)} L {f(x+k*r*1.7)} {f(y-r*0.1)}", r * 0.55, pb, 6)
    if tipo == "abierta":
        for i, a in enumerate((-50, -20, 8, 34)):
            aa = math.radians(-90 + a * k)
            s += trazo(f"M {f(x)} {f(y)} L {f(x+r*1.45*math.cos(aa))} {f(y+r*1.45*math.sin(aa))}", r * 0.42, pb, 5.5)
    s += f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{pb}" stroke="{INK}" stroke-width="{SW-1}"/>'
    s += f'<path d="M {f(x-r*0.45)} {f(y+r*0.45)} Q {f(x)} {f(y+r*0.75)} {f(x+r*0.45)} {f(y+r*0.4)}" fill="none" stroke="{pl}" stroke-width="3" stroke-linecap="round"/>'
    s += f'<circle cx="{f(x-r*0.3)}" cy="{f(y-r*0.35)}" r="{f(r*0.22)}" fill="#FFFFFF" opacity="0.45"/>'
    return s


def _brazo(id_, lado, S, Hm, E, aw, piel, ropa, ropa_col, mano_tipo):
    """Brazo hombro S → codo E → mano Hm. Manga según ropa."""
    pa, pb, pc, pl = PIELES.get(piel, PIELES["media"])
    k = -1 if lado == "izq" else 1
    d = f"M {f(S[0])} {f(S[1])} L {f(E[0])} {f(E[1])} L {f(Hm[0])} {f(Hm[1])}"
    s = ""
    if ropa in ("camiseta", "vestido"):
        s += trazo(f"M {f(S[0])} {f(S[1])} L {f(E[0])} {f(E[1])} L {f(Hm[0])} {f(Hm[1])}", aw * 0.82, pb, 13)
        mx, my = S[0] + (E[0] - S[0]) * 0.55, S[1] + (E[1] - S[1]) * 0.55
        s += trazo(f"M {f(S[0])} {f(S[1])} L {f(mx)} {f(my)}", aw * 1.12, ropa_col, 13, cap="butt")
        s += f'<circle cx="{f(S[0])}" cy="{f(S[1])}" r="{f(aw*0.56)}" fill="{ropa_col}"/>'
    else:
        s += trazo(d, aw, ropa_col, 13)
        # puño (rib) cerca de la mano
        cx_, cy_ = Hm[0] + (E[0] - Hm[0]) * 0.18, Hm[1] + (E[1] - Hm[1]) * 0.18
        puno = shade(ropa_col, -0.18) if ropa != "camisa" else "#FFFFFF"
        s += trazo(f"M {f(Hm[0] + (E[0]-Hm[0])*0.1)} {f(Hm[1] + (E[1]-Hm[1])*0.1)} L {f(cx_ + (E[0]-Hm[0])*0.1)} {f(cy_ + (E[1]-Hm[1])*0.1)}", aw * 0.98, puno, 8, cap="butt")
    # brillo del brazo
    s += f'<path d="M {f(S[0]-k*aw*0.15)} {f(S[1]+aw*0.2)} L {f(E[0]-k*aw*0.28)} {f(E[1])}" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity="0.35"/>'
    s += g(f"{id_}_mano_{lado}", _mano(Hm[0], Hm[1], aw * 0.62, piel, mano_tipo, k))
    return g(f"{id_}_brazo_{lado}", s)


def _torso(e, ropa, col, piel, sentado_dy=0, camisa_col="#FFFFFF"):
    sy, sw, cy, cw, nw = e["sy"], e["sw"], e["cy"] + sentado_dy, e["cw"], e["nw"]
    sy += sentado_dy
    largo = ropa == "abrigo"
    bot = cy + 14 if not largo else cy + (0 - cy) * 0.55
    wx = cw - 6 if ropa != "abrigo" else cw + 6
    P = (f"M {f(-sw)} {f(sy+24)} C {f(-sw)} {f(sy-2)}, {f(-sw*0.7)} {f(sy-14)}, {f(-nw*1.6)} {f(sy-14)} "
         f"Q 0 {f(sy+14)} {f(nw*1.6)} {f(sy-14)} C {f(sw*0.7)} {f(sy-14)}, {f(sw)} {f(sy-2)}, {f(sw)} {f(sy+24)} "
         f"C {f(sw*0.98)} {f((sy+cy)/2)}, {f(wx)} {f((sy+cy)/2+20)}, {f(wx+4 if not largo else cw+30)} {f(bot)} "
         f"L {f(-(wx+4) if not largo else -(cw+30))} {f(bot)} C {f(-wx)} {f((sy+cy)/2+20)}, {f(-sw*0.98)} {f((sy+cy)/2)}, {f(-sw)} {f(sy+24)} Z")
    s = f'<path d="{P}" fill="{degradado(col, 0.2)}" stroke="{INK}" stroke-width="{SW+1}" stroke-linejoin="round"/>'
    s += brillo(f"M {f(-sw*0.78)} {f(sy+20)} C {f(-sw*0.6)} {f(sy-2)}, {f(-sw*0.3)} {f(sy-6)}, {f(-nw*2)} {f(sy-8)}", 6, 0.55, shade(col, 0.55))
    if ropa == "jersey":
        s += f'<path d="M {f(-(wx+2))} {f(bot-16)} L {f(wx+2)} {f(bot-16)}" stroke="{shade(col,-0.25)}" stroke-width="4"/>'
        s += "".join(f'<line x1="{f(x)}" y1="{f(bot-14)}" x2="{f(x)}" y2="{f(bot-3)}" stroke="{shade(col,-0.25)}" stroke-width="3"/>' for x in range(int(-wx), int(wx), 12))
        s += f'<path d="M {f(-nw*1.6)} {f(sy-12)} Q 0 {f(sy+22)} {f(nw*1.6)} {f(sy-12)}" fill="none" stroke="{shade(col,-0.25)}" stroke-width="5"/>'
    elif ropa == "camisa":
        s += f'<path d="M {f(-nw*1.7)} {f(sy-14)} L {f(-nw*0.2)} {f(sy+26)} L {f(-nw*0.9)} {f(sy+34)} L {f(-nw*2.1)} {f(sy-4)} Z" fill="#FFFFFF" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round"/>'
        s += f'<path d="M {f(nw*1.7)} {f(sy-14)} L {f(nw*0.2)} {f(sy+26)} L {f(nw*0.9)} {f(sy+34)} L {f(nw*2.1)} {f(sy-4)} Z" fill="#FFFFFF" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round"/>'
        s += f'<path d="M 0 {f(sy+24)} L 0 {f(bot-6)}" stroke="{shade(col,-0.3)}" stroke-width="3.5"/>'
        s += "".join(f'<circle cx="5" cy="{f(sy+50+i*(bot-sy-70)/3)}" r="3.6" fill="#FFFFFF" stroke="{INK}" stroke-width="2"/>' for i in range(4))
    elif ropa in ("chaqueta", "abrigo"):
        vb = sy + (cy - sy) * (0.55 if ropa == "chaqueta" else 0.35)
        s += f'<path d="M {f(-nw*1.6)} {f(sy-12)} L 0 {f(vb)} L {f(nw*1.6)} {f(sy-12)} Q 0 {f(sy+10)} {f(-nw*1.6)} {f(sy-12)} Z" fill="{camisa_col}" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round"/>'
        if ropa == "chaqueta":
            s += f'<path d="M {f(-nw*0.5)} {f(sy+10)} L {f(nw*0.5)} {f(sy+10)} L {f(nw*0.25)} {f(vb-10)} L 0 {f(vb)} L {f(-nw*0.25)} {f(vb-10)} Z" fill="{CORAL}" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>'
        for k in (-1, 1):
            s += f'<path d="M {f(k*nw*1.6)} {f(sy-12)} L {f(k*nw*2.6)} {f(sy+40)} L {f(k*nw*1.4)} {f(sy+52)} L 0 {f(vb)}" fill="{shade(col,-0.12)}" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round"/>'
        s += f'<path d="M 0 {f(vb)} L 0 {f(bot-4)}" stroke="{INK}" stroke-width="4"/>'
        s += "".join(f'<circle cx="{f(-7)}" cy="{f(vb+18+i*28)}" r="4.5" fill="{shade(col,-0.4)}" stroke="{INK}" stroke-width="2"/>' for i in range(2 if ropa == "chaqueta" else 4))
        s += "".join(f'<path d="M {f(k*cw*0.35)} {f(cy-22)} L {f(k*cw*0.82)} {f(cy-22)}" stroke="{shade(col,-0.35)}" stroke-width="4" stroke-linecap="round"/>' for k in (-1, 1))
    elif ropa in ("camiseta", "vestido"):
        s += f'<path d="M {f(-nw*1.6)} {f(sy-12)} Q 0 {f(sy+22)} {f(nw*1.6)} {f(sy-12)}" fill="none" stroke="{shade(col,-0.25)}" stroke-width="5"/>'
    return s


def _piernas(e, ropa, pant, zap, piel, sentado=False, sdy=0):
    pa, pb, pc, pl = PIELES.get(piel, PIELES["media"])
    cy, cw, lw = e["cy"] + sdy, e["cw"], e["lw"]
    s = ""
    pierna_col = pb if ropa == "vestido" else pant
    if not sentado:
        for k in (-1, 1):
            x0, x1 = k * cw * 0.5, k * cw * 0.55
            s += trazo(f"M {f(x0)} {f(cy)} L {f(x1)} -22", lw * 1.25 if ropa != "vestido" else lw * 0.8, pierna_col, 14, cap="butt")
        if ropa != "vestido":
            # cadera del pantalón (une las dos perneras)
            s += f'<path d="M {f(-cw)} {f(cy-6)} L {f(cw)} {f(cy-6)} L {f(cw*0.55+lw*0.62)} {f(cy+90)} L {f(lw*0.15)} {f(cy+70)} L {f(-lw*0.15)} {f(cy+70)} L {f(-cw*0.55-lw*0.62)} {f(cy+90)} Z" fill="{pant}" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>'
            s += f'<path d="M 0 {f(cy+4)} L 0 {f(cy+64)}" stroke="{shade(pant,-0.3)}" stroke-width="3.5"/>'
            s += "".join(brillo(f"M {f(k*cw*0.5 - 8)} {f(cy+40)} L {f(k*cw*0.55 - 8)} -40", 5, 0.3) for k in (-1, 1))
    else:
        # sentado de frente: muslos acortados hacia el espectador + espinillas
        ky = cy + 40
        for k in (-1, 1):
            s += trazo(f"M {f(k*cw*0.5)} {f(cy)} L {f(k*cw*0.56)} {f(ky)}", lw * 1.45, pierna_col if ropa != "vestido" else pb, 14)
            s += trazo(f"M {f(k*cw*0.56)} {f(ky+6)} L {f(k*cw*0.6)} -22", lw * 1.15, pierna_col if ropa != "vestido" else pb, 14, cap="butt")
            s += f'<ellipse cx="{f(k*cw*0.56)}" cy="{f(ky-4)}" rx="{f(lw*0.5)}" ry="{f(lw*0.28)}" fill="#FFFFFF" opacity="0.25"/>'
        if ropa == "vestido":
            pass
    # zapatos
    for k in (-1, 1):
        x = k * cw * (0.6 if sentado else 0.55)
        d = (f"M {f(x - lw*0.75)} 0 C {f(x - lw*0.85)} -28, {f(x + lw*0.85)} -30, {f(x + lw*0.8 + k*10)} -6 "
             f"Q {f(x + lw*0.9 + k*12)} 0 {f(x + lw*0.6 + k*10)} 0 Z")
        s += f'<path d="{d}" fill="{degradado(zap, 0.25)}" stroke="{INK}" stroke-width="{SW-1}" stroke-linejoin="round"/>'
        s += brillo(f"M {f(x - lw*0.45)} -18 Q {f(x)} -26 {f(x + lw*0.4)} -20", 4, 0.5)
    return s


def _falda(e, col, sdy=0):
    cy, cw = e["cy"] + sdy, e["cw"]
    ky = cy + (0 - cy) * 0.48
    d = f"M {f(-cw+2)} {f(cy-6)} L {f(cw-2)} {f(cy-6)} L {f(cw*1.5)} {f(ky)} Q 0 {f(ky+18)} {f(-cw*1.5)} {f(ky)} Z"
    return (f'<path d="{d}" fill="{degradado(col, 0.2)}" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>'
            + "".join(f'<path d="M {f(k*cw*0.35)} {f(cy+10)} L {f(k*cw*0.6)} {f(ky-6)}" stroke="{shade(col,-0.25)}" stroke-width="4" stroke-linecap="round"/>' for k in (-1, 1)))


def _bufanda(e, col):
    sy, sw, nw = e["sy"], e["sw"], e["nw"]
    d = f"M {f(-nw*2.6)} {f(sy-18)} C {f(-nw*1.4)} {f(sy+18)}, {f(nw*1.4)} {f(sy+18)}, {f(nw*2.6)} {f(sy-18)} L {f(nw*2.8)} {f(sy+16)} C {f(nw*1.4)} {f(sy+46)}, {f(-nw*1.4)} {f(sy+46)}, {f(-nw*2.9)} {f(sy+16)} Z"
    tail = f"M {f(nw*0.9)} {f(sy+26)} L {f(nw*1.9)} {f(sy+150)} L {f(nw*0.1)} {f(sy+160)} L {f(-nw*0.2)} {f(sy+32)} Z"
    s = f'<path d="{tail}" fill="{degradado(col, 0.18, "h")}" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>'
    s += f'<g stroke="{shade(col,-0.35)}" stroke-width="5">' + "".join(
        f'<line x1="{f(-nw*0.1 + t*nw*0.4)}" y1="{f(sy+60+t*80)}" x2="{f(nw*1.5 + t*nw*0.3)}" y2="{f(sy+56+t*80)}"/>' for t in (0.2, 0.55)) + "</g>"
    s += "".join(f'<line x1="{f(x)}" y1="{f(sy+156)}" x2="{f(x-2)}" y2="{f(sy+174)}" stroke="{shade(col,-0.3)}" stroke-width="5" stroke-linecap="round"/>' for x in (nw*0.3, nw*0.9, nw*1.5))
    s += f'<path d="{d}" fill="{degradado(col, 0.18, "h")}" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>'
    s += brillo(f"M {f(-nw*2)} {f(sy-6)} C {f(-nw*1)} {f(sy+16)}, {f(nw)} {f(sy+16)}, {f(nw*2)} {f(sy-6)}", 4, 0.6)
    return s


def _baston(Hm, aw):
    x, y = Hm
    d = f"M {f(x - aw*0.9)} {f(y + 4)} Q {f(x - aw*0.9)} {f(y - aw*1.1)} {f(x)} {f(y - aw*1.1)} Q {f(x + aw*0.6)} {f(y - aw*1.1)} {f(x + aw*0.5)} {f(y - aw*0.2)} L {f(x + aw*0.5)} -4"
    return trazo(d, aw * 0.42, degradado("#8A5A31", 0.25, "h"), 7) + f'<rect x="{f(x + aw*0.5 - aw*0.32)}" y="-14" width="{f(aw*0.64)}" height="14" rx="4" fill="#2A2F3E" stroke="{INK}" stroke-width="4"/>'


def _silla(e, sdy, col="#C98B55"):
    cy, cw = e["cy"] + sdy, e["cw"]
    sy = e["sy"] + sdy
    seat_y = cy + 24
    s = ""
    # respaldo detrás del tronco
    s += f'<rect x="{f(-cw*1.45)}" y="{f(sy-30)}" width="{f(cw*2.9)}" height="{f(seat_y - sy + 30)}" rx="18" fill="{degradado(col, 0.2)}" stroke="{INK}" stroke-width="{SW}"/>'
    s += f'<rect x="{f(-cw*1.2)}" y="{f(sy-8)}" width="{f(cw*2.4)}" height="18" rx="8" fill="{shade(col,0.3)}" opacity="0.5"/>'
    for k in (-1, 1):
        s += f'<rect x="{f(k*cw*1.35 - 9)}" y="{f(seat_y)}" width="18" height="{f(-seat_y)}" rx="6" fill="{degradado(col, 0.2, "h")}" stroke="{INK}" stroke-width="5"/>'
    s += f'<rect x="{f(-cw*1.6)}" y="{f(seat_y-12)}" width="{f(cw*3.2)}" height="30" rx="10" fill="{degradado(col, 0.25)}" stroke="{INK}" stroke-width="{SW}"/>'
    return s


_BRAZOS = ("abajo", "cintura", "arriba", "saluda", "senala", "barbilla", "coge", "cruzados")


def persona(id_="persona", x=500, y=650, escala=1.0, edad="adulto", piel="media", pelo="corto", pelo_color="castano",
            ropa="jersey", ropa_color="#3B80CF", pantalon_color="#3E5C93", zapato_color="#2A2F3E", camisa_color="#FFFFFF",
            accesorios=(), bufanda_color="#FFC83D", expresion="neutral", pose="de_pie", brazos=("abajo", "abajo"),
            mira=0, silla=False, espejo=False):
    """Personaje completo. Ver docstring del módulo. espejo=True lo voltea en horizontal."""
    e = dict(EDADES.get(edad, EDADES["adulto"]))
    if isinstance(brazos, str):
        brazos = (brazos, brazos)
    accesorios = tuple(accesorios or ())
    if edad == "nino" and "baston" in accesorios:
        accesorios = tuple(a for a in accesorios if a != "baston")
    sentado = pose == "sentado"
    busto = pose == "busto"
    sdy = -(e["cy"]) * 0.42 if sentado else 0  # cuánto baja el tronco al sentarse
    hy = e["hy"] + sdy
    rx, ry = e["rx"], e["ry"]
    sy, sw, aw = e["sy"] + sdy, e["sw"], e["aw"]
    lu = (e["cy"] - e["sy"]) * 0.56
    lf = lu * 0.98
    o = []
    if not busto:
        o.append(sombra(0, 2, e["cw"] * 2.2, 14, 0.18))
    if silla and sentado:
        o.append(_silla(e, sdy))
    # brazos: objetivos de la mano
    def target(pose_b, k):
        if pose_b == "cintura":
            return (k * (e["cw"] + 2), e["cy"] + sdy - 40), "puno"
        if pose_b == "arriba":
            return (k * (sw + 52), hy - ry - 30), "abierta"
        if pose_b == "saluda":
            return (k * (sw + 82), hy - 20), "abierta"
        if pose_b == "senala":
            return (k * (sw + lu + lf - 16), sy + 8), "senala"
        if pose_b == "barbilla":
            return (k * rx * 0.25, hy + ry * 1.12), "puno"
        if pose_b == "coge":
            return (k * (sw + 6), e["cy"] + sdy - 70), "puno"
        if pose_b == "cruzados":
            return (-k * (sw - 14), sy + (e["cy"] - e["sy"]) * 0.42), "puno"
        if sentado:
            return (k * (e["cw"] * 0.75), e["cy"] + sdy + 20), "puno"
        L = (lu + lf) * 0.97  # brazo casi recto, un poco abierto
        return (k * (sw - 14 + L * math.sin(math.radians(9))), sy + 18 + L * math.cos(math.radians(9))), "puno"

    arms = {}
    puntos = {}
    for lado, k, pb_ in (("izq", -1, brazos[0]), ("der", 1, brazos[1])):
        S = (k * (sw - 14), sy + 18)
        Ht, mt = target(pb_, k)
        if pb_ == "cruzados":
            E = (k * (sw + 4), sy + (e["cy"] - e["sy"]) * 0.55)
            Hm = Ht
        else:
            E, Hm = _ik(S, Ht, lu, lf, k)
        arms[lado] = (S, E, Hm, mt, pb_)
        puntos[f"mano_{lado}"] = Hm
        puntos[f"hombro_{lado}"] = S
    # orden: brazos detrás del cuerpo si están abajo/cintura/arriba/saluda/señala; delante si cruzan el pecho
    front = {l for l, a in arms.items() if a[4] in ("barbilla", "cruzados", "coge")}
    cuerpo = []
    for lado in ("izq", "der"):
        if lado not in front:
            S, E, Hm, mt, _ = arms[lado]
            cuerpo.append(_brazo(id_, lado, S, Hm, E, aw, piel, ropa, ropa_color, mt))
    piernas = "" if busto else _piernas(e, ropa, pantalon_color, zapato_color, piel, sentado, sdy)
    tor = ""
    if ropa == "vestido" and not busto:
        tor += _falda(e, ropa_color, sdy)
    if ropa == "abrigo" and not busto:
        pass
    # cuello
    pa, pb, pc, pl = PIELES.get(piel, PIELES["media"])
    neck = f'<rect x="{f(-e["nw"])}" y="{f(hy+ry*0.7)}" width="{f(e["nw"]*2)}" height="{f(sy - hy - ry*0.7 + 8)}" rx="{f(e["nw"]*0.5)}" fill="url(#pielL_{piel if piel in PIELES else "media"})" stroke="{INK}" stroke-width="{SW-1}"/>'
    neck += f'<path d="M {f(-e["nw"]+3)} {f(hy+ry*0.95)} Q 0 {f(hy+ry*1.1)} {f(e["nw"]-3)} {f(hy+ry*0.95)}" fill="none" stroke="{pl}" stroke-width="4" opacity="0.6"/>'
    tor += neck + _torso(e, ropa, ropa_color, piel, sdy, camisa_color)
    if "bufanda" in accesorios:
        tor += g(f"{id_}_acc_bufanda", _bufanda(dict(e, sy=sy), bufanda_color))
    body = g(f"{id_}_piernas", piernas) + tor if not busto else tor
    cuerpo_svg = g(f"{id_}_cuerpo", body)
    o.append("".join(cuerpo))
    o.append(cuerpo_svg)
    for lado in ("izq", "der"):
        if lado in front:
            S, E, Hm, mt, _ = arms[lado]
            o.append(_brazo(id_, lado, S, Hm, E, aw, piel, ropa, ropa_color, mt))
    if "baston" in accesorios and not busto:
        Hm = arms["der"][2]
        o.append(g(f"{id_}_acc_baston", _baston(Hm, aw)))
    o.append(g(f"{id_}_cabeza", cabeza(id_, rx, ry, hy, piel, pelo, pelo_color, expresion, mira, accesorios, edad)))
    inner = "".join(o)
    cut = None
    if busto:
        cut = sy + (e["cy"] - e["sy"]) * 0.62
        cid = f"{id_}_corte"
        inner = (f'<clipPath id="{cid}"><rect x="-400" y="{f(hy - ry*2.2)}" width="800" height="{f(cut - (hy - ry*2.2))}"/></clipPath>'
                 f'<g clip-path="url(#{cid})">{inner}</g>'
                 f'<path d="M {f(-sw-30)} {f(cut)} L {f(sw+30)} {f(cut)}" stroke="{INK}" stroke-width="{SW+1}" stroke-linecap="round"/>')
    oy = -cut if busto else 0
    sx = -escala if espejo else escala
    tr = f"translate({f(x)} {f(y)}) scale({f(sx)} {f(escala)})" + (f" translate(0 {f(oy)})" if oy else "")

    def P(p):
        return (x + p[0] * sx, y + (p[1] + oy) * escala)

    pts_ = {k: P(v) for k, v in puntos.items()}
    if espejo:
        pts_["mano_izq"], pts_["mano_der"] = pts_["mano_der"], pts_["mano_izq"]
    pts_.update({"cabeza": P((0, hy)), "boca": P((0, hy + ry * 0.5)), "ojos": P((0, hy)), "cima": P((0, hy - ry * (1.35 if "gorro" in accesorios else 1.05))),
                 "pies": P((0, 0)), "alto": (hy - ry) * -escala})
    caja = (x - (sw + 100) * escala, y + (hy - ry * 1.3 + oy) * escala, x + (sw + 100) * escala, y + (oy if not busto else 0) * escala)
    return Pieza(g(id_, f'<g transform="{tr}">{inner}</g>'), pts_, caja)


def pictograma(id_, cx, cy, s=100, col="#8C9BB8", sw=5):
    """Silueta genérica de persona (icono de multitud, votantes…). s = alto aproximado."""
    fill = degradado(col, 0.15)
    return g(id_, f'<circle cx="{f(cx)}" cy="{f(cy-s*0.42)}" r="{f(s*0.24)}" fill="{fill}" stroke="{INK}" stroke-width="{sw}"/>'
             f'<path d="M {f(cx-s*0.42)} {f(cy+s*0.5)} C {f(cx-s*0.42)} {f(cy-s*0.1)}, {f(cx+s*0.42)} {f(cy-s*0.1)}, {f(cx+s*0.42)} {f(cy+s*0.5)} Z" fill="{fill}" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"/>')


def multitud(id_, x0, x1, base, n=7, s=90, seed=3, cols=("#8C9BB8", "#FF7EB6", "#2EC4B6", "#FFC83D", "#C7894B", "#7B5CFF")):
    """Fila de pictogramas (público, votantes) de x0 a x1 apoyados en `base`."""
    import random as _r
    rnd = _r.Random(seed)
    out = ""
    for i in range(n):
        cx = x0 + (x1 - x0) * (i + 0.5) / n + rnd.uniform(-8, 8)
        ss = s * rnd.uniform(0.85, 1.1)
        out += pictograma(None, cx, base - ss * 0.5, ss, cols[i % len(cols)])
    return g(id_, out)

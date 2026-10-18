"""Tienda y supermercado: cartel de precio con céntimos pequeños (estilo lineal del súper), productos genéricos
(caja, bote, botella, lata, brick), estantería llena, carrito de la compra, ticket de caja, recta numérica y el fondo
de un pasillo de supermercado.

Sale de: lote7-08-precios-99 (por qué los precios acaban en ,99).
"""
import math
import random
from ..base import (INK, LIME, CORAL, YEL, TEAL, VIO, f, g, gt, T, MONO, DISP, shade, trazo, sombra, sombra_caja, brillo,
                    lg, registrar_defs, degradado, Pieza)

registrar_defs(
    lg("superPared", [(0, "#F4F7FC"), (1, "#DCE4F1")])
    + lg("superSuelo", [(0, "#E9EDF4"), (1, "#C5CEDD")])
    + lg("baldaG", [(0, "#F4F6FA"), (1, "#B9C2D2")])
    + lg("ticketG", [(0, "#FFFFFF"), (1, "#F1F2F6")])
)

COLS_PROD = ("#FF5A36", "#2347FF", "#FFC928", "#1FB5A8", "#7B5CFF", "#FF7EB6", "#36B37E", "#FF9F1C")


# ------------------------------------------------------------------ cartel de precio
def cartel_precio(id_, cx, cy, w=300, entero="9", cent="99", moneda="€", col=YEL, cinta=None, rot_=0, fg=INK):
    """Cartel de precio del lineal: cifra entera GRANDE y céntimos pequeños arriba (como en el súper).
    Sub-ids animables: {id}_entero y {id}_cent (sin transform: pulse/punch/hide). `cinta` = texto en franja coral arriba
    (p. ej. «OFERTA»). .puntos: entero, cent (centros), centro. Con cent=None solo pinta el entero (p. ej. «10 €»)."""
    h = w * 0.62
    x0, y0 = cx - w / 2, cy - h / 2
    s = sombra_caja(x0, y0, w, h, 16, 10, 12, 0.26)
    s += f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" rx="16" fill="{degradado(col, 0.18)}" stroke="{INK}" stroke-width="7"/>'
    top = y0
    if cinta:
        s += f'<path d="M {f(x0+3.5)} {f(y0+h*0.24)} L {f(x0+3.5)} {f(y0+16)} Q {f(x0+3.5)} {f(y0+3.5)} {f(x0+16)} {f(y0+3.5)} L {f(x0+w-16)} {f(y0+3.5)} Q {f(x0+w-3.5)} {f(y0+3.5)} {f(x0+w-3.5)} {f(y0+16)} L {f(x0+w-3.5)} {f(y0+h*0.24)} Z" fill="{CORAL}"/>'
        s += f'<path d="M {f(x0)} {f(y0+h*0.24)} L {f(x0+w)} {f(y0+h*0.24)}" stroke="{INK}" stroke-width="5"/>'
        s += T(cx, y0 + h * 0.18, cinta, h * 0.14, "#FFFFFF", font=DISP)
        top = y0 + h * 0.24
    s += brillo(f"M {f(x0+16)} {f(top+14)} L {f(x0+w*0.55)} {f(top+14)}", 5, 0.7)
    zona = y0 + h - top
    big = zona * 0.78
    if cent is None:
        txt = f"{entero} {moneda}" if moneda else entero
        size = min(big, w * 0.86 / max(1, len(txt) * 0.86))
        pe = (cx, top + zona * 0.52)
        s += g(f"{id_}_entero" if id_ else None, T(cx, pe[1] + size * 0.36, txt, size, fg, font=DISP))
        return Pieza(gt(id_, f"rotate({f(rot_)} {f(cx)} {f(cy)})", s) if rot_ else g(id_, s),
                     {"entero": pe, "cent": pe, "centro": (cx, cy)}, (x0, y0, x0 + w, y0 + h))
    ew = len(entero) * big * 0.8
    cw_ = len(cent) * big * 0.42 + big * 0.18
    tot = ew + cw_
    ex = cx - tot / 2 + ew / 2
    base_y = top + zona * 0.5 + big * 0.36
    s += g(f"{id_}_entero" if id_ else None, T(ex, base_y, entero, big, fg, font=DISP))
    kx, ky, kr = ex + ew / 2 + big * 0.05, base_y - big * 0.07, big * 0.065
    s += (f'<path d="M {f(kx-kr)} {f(ky)} A {f(kr)} {f(kr)} 0 1 1 {f(kx+kr)} {f(ky)} Q {f(kx+kr)} {f(ky+kr*2.2)} {f(kx-kr*0.9)} {f(ky+kr*2.6)} '
          f'Q {f(kx)} {f(ky+kr*1.4)} {f(kx-kr*0.2)} {f(ky+kr*0.9)} A {f(kr)} {f(kr)} 0 0 1 {f(kx-kr)} {f(ky)} Z" fill="{fg}"/>')
    ccx = ex + ew / 2 + big * 0.14 + cw_ / 2
    s += g(f"{id_}_cent" if id_ else None, T(ccx, base_y - big * 0.38, cent, big * 0.48, fg, font=DISP)
           + (T(ccx, base_y, moneda, big * 0.34, fg, font=DISP) if moneda else ""))
    pts_ = {"entero": (ex, base_y - big * 0.36), "cent": (ccx, base_y - big * 0.55), "centro": (cx, cy)}
    body = gt(id_, f"rotate({f(rot_)} {f(cx)} {f(cy)})", s) if rot_ else g(id_, s)
    return Pieza(body, pts_, (x0, y0, x0 + w, y0 + h))


# ------------------------------------------------------------------ productos
def producto(tipo, cx, base, s=1.0, col=CORAL, id_=None, texto=None):
    """Producto genérico del súper apoyado en `base`. tipo: caja (cereales), bote (tarro), botella, lata, brick.
    Alto ≈ 150*s (botella 190*s)."""
    o = sombra(cx, base + 3, 46 * s, 7 * s, 0.2)
    if tipo == "caja":
        w, h = 92 * s, 150 * s
        x0, y0 = cx - w / 2, base - h
        o += f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" rx="{f(6*s)}" fill="{degradado(col, 0.2, "h")}" stroke="{INK}" stroke-width="{f(5*s)}"/>'
        o += f'<ellipse cx="{f(cx)}" cy="{f(y0+h*0.62)}" rx="{f(w*0.32)}" ry="{f(h*0.13)}" fill="#FFFFFF" stroke="{INK}" stroke-width="{f(3.5*s)}"/>'
        for k in (-1, 0, 1):
            o += f'<circle cx="{f(cx+k*w*0.13)}" cy="{f(y0+h*0.56)}" r="{f(w*0.07)}" fill="{YEL}" stroke="{INK}" stroke-width="{f(2.5*s)}"/>'
        o += f'<rect x="{f(x0+w*0.14)}" y="{f(y0+h*0.12)}" width="{f(w*0.72)}" height="{f(h*0.2)}" rx="{f(4*s)}" fill="#FFFFFF" opacity="0.9"/>'
        if texto:
            o += T(cx, y0 + h * 0.26, texto, h * 0.11, shade(col, -0.35), font=DISP)
        o += brillo(f"M {f(x0+8*s)} {f(y0+12*s)} L {f(x0+8*s)} {f(base-12*s)}", 4 * s, 0.6)
    elif tipo == "bote":
        w, h = 80 * s, 110 * s
        x0, y0 = cx - w / 2, base - h
        o += f'<rect x="{f(x0)}" y="{f(y0+16*s)}" width="{f(w)}" height="{f(h-16*s)}" rx="{f(14*s)}" fill="{degradado(col, 0.25, "h")}" stroke="{INK}" stroke-width="{f(5*s)}"/>'
        o += f'<rect x="{f(x0+4*s)}" y="{f(y0)}" width="{f(w-8*s)}" height="{f(22*s)}" rx="{f(6*s)}" fill="{degradado("#9AA3B5", 0.25)}" stroke="{INK}" stroke-width="{f(5*s)}"/>'
        o += f'<rect x="{f(x0+6*s)}" y="{f(y0+h*0.45)}" width="{f(w-12*s)}" height="{f(h*0.3)}" fill="#FFF8E8" stroke="{INK}" stroke-width="{f(3*s)}"/>'
        o += brillo(f"M {f(x0+12*s)} {f(y0+30*s)} L {f(x0+12*s)} {f(base-14*s)}", 5 * s, 0.6)
    elif tipo == "botella":
        w, h = 64 * s, 190 * s
        x0, y0 = cx - w / 2, base - h
        d = (f"M {f(cx-w*0.16)} {f(y0)} L {f(cx+w*0.16)} {f(y0)} L {f(cx+w*0.16)} {f(y0+h*0.2)} "
             f"C {f(cx+w*0.5)} {f(y0+h*0.3)}, {f(cx+w*0.5)} {f(y0+h*0.32)}, {f(cx+w*0.5)} {f(y0+h*0.42)} L {f(cx+w*0.5)} {f(base-8*s)} "
             f"Q {f(cx+w*0.5)} {f(base)} {f(cx+w*0.4)} {f(base)} L {f(cx-w*0.4)} {f(base)} Q {f(cx-w*0.5)} {f(base)} {f(cx-w*0.5)} {f(base-8*s)} "
             f"L {f(cx-w*0.5)} {f(y0+h*0.42)} C {f(cx-w*0.5)} {f(y0+h*0.32)}, {f(cx-w*0.5)} {f(y0+h*0.3)}, {f(cx-w*0.16)} {f(y0+h*0.2)} Z")
        o += f'<path d="{d}" fill="{degradado(col, 0.25, "h")}" stroke="{INK}" stroke-width="{f(5*s)}" stroke-linejoin="round"/>'
        o += f'<rect x="{f(cx-w*0.2)}" y="{f(y0-10*s)}" width="{f(w*0.4)}" height="{f(16*s)}" rx="{f(4*s)}" fill="{CORAL if col != CORAL else YEL}" stroke="{INK}" stroke-width="{f(4*s)}"/>'
        o += f'<rect x="{f(cx-w*0.5+3*s)}" y="{f(y0+h*0.55)}" width="{f(w-6*s)}" height="{f(h*0.22)}" fill="#FFFFFF" stroke="{INK}" stroke-width="{f(3*s)}"/>'
        o += brillo(f"M {f(cx-w*0.32)} {f(y0+h*0.45)} L {f(cx-w*0.32)} {f(base-14*s)}", 5 * s, 0.6)
    elif tipo == "lata":
        w, h = 70 * s, 100 * s
        x0, y0 = cx - w / 2, base - h
        o += f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" rx="{f(8*s)}" fill="{degradado(col, 0.3, "h")}" stroke="{INK}" stroke-width="{f(5*s)}"/>'
        for yy in (y0 + 8 * s, base - 8 * s):
            o += f'<path d="M {f(x0+2*s)} {f(yy)} L {f(x0+w-2*s)} {f(yy)}" stroke="{INK}" stroke-width="{f(3*s)}"/>'
        o += f'<circle cx="{f(cx)}" cy="{f(y0+h*0.5)}" r="{f(w*0.24)}" fill="#FFFFFF" stroke="{INK}" stroke-width="{f(3*s)}"/>'
        o += brillo(f"M {f(x0+10*s)} {f(y0+14*s)} L {f(x0+10*s)} {f(base-14*s)}", 5 * s, 0.6)
    else:  # brick
        w, h = 74 * s, 150 * s
        x0, y0 = cx - w / 2, base - h
        o += f'<path d="M {f(x0)} {f(y0+20*s)} L {f(cx)} {f(y0)} L {f(x0+w)} {f(y0+20*s)} Z" fill="#FFFFFF" stroke="{INK}" stroke-width="{f(5*s)}" stroke-linejoin="round"/>'
        o += f'<rect x="{f(x0)}" y="{f(y0+20*s)}" width="{f(w)}" height="{f(h-20*s)}" rx="{f(4*s)}" fill="url(#papelG)" stroke="{INK}" stroke-width="{f(5*s)}"/>'
        o += f'<path d="M {f(x0+3*s)} {f(y0+h*0.6)} Q {f(cx)} {f(y0+h*0.48)} {f(x0+w-3*s)} {f(y0+h*0.6)} L {f(x0+w-3*s)} {f(base-3*s)} L {f(x0+3*s)} {f(base-3*s)} Z" fill="{degradado(col, 0.2)}"/>'
        o += f'<rect x="{f(x0)}" y="{f(y0+20*s)}" width="{f(w)}" height="{f(h-20*s)}" rx="{f(4*s)}" fill="none" stroke="{INK}" stroke-width="{f(5*s)}"/>'
        o += brillo(f"M {f(x0+10*s)} {f(y0+32*s)} L {f(x0+10*s)} {f(y0+h*0.5)}", 5 * s, 0.7)
    return g(id_, o) if id_ else o


def estanteria(id_, x0, x1, top, baldas=3, alto=210, seed=3, col="#2347FF", tipos=("caja", "bote", "botella", "lata", "brick")):
    """Estantería de supermercado de x0 a x1 con `baldas` pisos llenos de productos aleatorios.
    .puntos['baldas'] = [y del borde frontal de cada balda] (ahí van los carteles de precio)."""
    rnd = random.Random(seed)
    w = x1 - x0
    bottom = top + baldas * alto + 30
    o = sombra_caja(x0, top - 30, w, bottom - top + 30, 10, 14, 14, 0.22)
    o += f'<rect x="{f(x0)}" y="{f(top-30)}" width="{f(w)}" height="{f(bottom-top+30)}" rx="10" fill="{degradado(col, 0.18)}" stroke="{INK}" stroke-width="7"/>'
    o += f'<rect x="{f(x0+16)}" y="{f(top-14)}" width="{f(w-32)}" height="{f(bottom-top-10)}" fill="#E7ECF5" stroke="{INK}" stroke-width="4"/>'
    ys = []
    for b in range(baldas):
        yb = top + (b + 1) * alto
        x = x0 + 30
        while x < x1 - 70:
            t = rnd.choice(tipos)
            sc = rnd.uniform(0.82, 1.0) * (0.95 if t == "botella" else 1.08)
            ww = {"caja": 92, "bote": 80, "botella": 64, "lata": 70, "brick": 74}[t] * sc
            if x + ww > x1 - 26:
                break
            o += producto(t, x + ww / 2, yb - 4, sc, COLS_PROD[rnd.randrange(len(COLS_PROD))])
            x += ww + rnd.uniform(6, 14)
        o += f'<rect x="{f(x0+10)}" y="{f(yb-4)}" width="{f(w-20)}" height="34" rx="5" fill="url(#baldaG)" stroke="{INK}" stroke-width="5"/>'
        ys.append(yb + 13)
    return Pieza(g(id_, o), {"baldas": ys}, (x0, top - 30, x1, bottom))


# ------------------------------------------------------------------ carrito
def carrito(id_, cx, base, w=380, col=CORAL, lleno=True, seed=2, espejo=False):
    """Carrito de la compra de perfil (asa a la derecha; espejo=True a la izquierda), cesta de rejilla y ruedas.
    Sub-ids: {id}_ruedas, {id}_compra (productos dentro). .puntos['asa'] = donde va la mano."""
    s = w / 380
    k = -1 if espejo else 1
    X = lambda dx: cx + k * dx * s
    Y = lambda dy: base - dy * s
    o = sombra(cx, base + 4, w * 0.5, 14, 0.25)
    cesta = [(-170, 300), (150, 300), (120, 120), (-130, 120)]
    compra = ""
    if lleno:
        rnd = random.Random(seed)
        for i, (t, dx) in enumerate((("caja", -110), ("botella", -40), ("brick", 30), ("caja", 95), ("lata", -75), ("bote", 60))):
            bb = 300 if i < 4 else 275
            compra += producto(t, X(dx), Y(bb - 40), s * (1.0 if i < 4 else 0.9), COLS_PROD[(i * 3 + seed) % len(COLS_PROD)])
    d = " ".join(("M" if i == 0 else "L") + f" {f(X(px))} {f(Y(py))}" for i, (px, py) in enumerate(cesta)) + " Z"
    o += g(f"{id_}_compra" if id_ else None, compra)
    rej = ""
    for i in range(1, 8):
        t = i / 8
        xa = -170 + (150 + 170) * t
        xb = -130 + (120 + 130) * t
        rej += f'<path d="M {f(X(xa))} {f(Y(300))} L {f(X(xb))} {f(Y(120))}" stroke="#7C879C" stroke-width="{f(5*s)}"/>'
    for i in range(1, 4):
        t = i / 4
        py = 300 - 180 * t
        xa = -170 + 40 * t
        xb = 150 - 30 * t
        rej += f'<path d="M {f(X(xa))} {f(Y(py))} L {f(X(xb))} {f(Y(py))}" stroke="#7C879C" stroke-width="{f(5*s)}"/>'
    o += f'<path d="{d}" fill="#C9D2E2" fill-opacity="0.35" stroke="none"/>' + rej
    o += f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{f(9*s)}" stroke-linejoin="round"/>'
    o += f'<path d="{d}" fill="none" stroke="#D5DBE6" stroke-width="{f(4*s)}" stroke-linejoin="round"/>'
    o += f'<rect x="{f(min(X(-170), X(150)))}" y="{f(Y(312))}" width="{f(320*s)}" height="{f(22*s)}" rx="{f(8*s)}" fill="{degradado(col, 0.22)}" stroke="{INK}" stroke-width="{f(6*s)}"/>'
    o += trazo(f"M {f(X(150))} {f(Y(300))} L {f(X(200))} {f(Y(360))}", 9 * s, "#B9C2D2", 7 * s)
    o += trazo(f"M {f(X(185))} {f(Y(375))} L {f(X(225))} {f(Y(342))}", 18 * s, col, 7 * s)
    o += trazo(f"M {f(X(-130))} {f(Y(120))} L {f(X(-150))} {f(Y(40))} L {f(X(130))} {f(Y(40))} L {f(X(120))} {f(Y(120))}", 7 * s, "#B9C2D2", 7 * s)
    ruedas = ""
    for dx in (-130, 105):
        ruedas += f'<circle cx="{f(X(dx))}" cy="{f(Y(22))}" r="{f(22*s)}" fill="{degradado("#3A4258", 0.2)}" stroke="{INK}" stroke-width="{f(6*s)}"/>'
        ruedas += f'<circle cx="{f(X(dx))}" cy="{f(Y(22))}" r="{f(7*s)}" fill="#D5DBE6"/>'
    o += g(f"{id_}_ruedas" if id_ else None, ruedas)
    o += brillo(f"M {f(X(-150))} {f(Y(290))} L {f(X(-120))} {f(Y(140))}", 4 * s, 0.6)
    xs = sorted((X(-180), X(240)))
    return Pieza(g(id_, o), {"asa": (X(205), Y(360)), "cesta": (X(-10), Y(300))}, (xs[0], Y(390), xs[1], base))


# ------------------------------------------------------------------ ticket
def ticket(id_, cx, top, w=300, lineas=(("LECHE", "0,99"), ("PAN", "1,49")), total=None, titulo="SUPER", rot_=0, size=24):
    """Ticket de caja con borde dentado abajo. lineas = [(concepto, precio)]; total = texto del total (en coral).
    Sub-ids {id}_l<i> por línea y {id}_total (para que aparezcan en cascada)."""
    lh = size * 1.7
    h = 90 + lh * len(lineas) + (lh * 1.6 if total else 0) + 30
    x0 = cx - w / 2
    n = 12
    dz = " ".join(f"L {f(x0 + w - (i + 0.5) * w / n)} {f(top + h + 14)} L {f(x0 + w - (i + 1) * w / n)} {f(top + h)}" for i in range(n))
    d = f"M {f(x0)} {f(top)} L {f(x0+w)} {f(top)} L {f(x0+w)} {f(top+h)} {dz} Z"
    s = f'<path d="{d}" transform="translate(10 12)" fill="{INK}" opacity="0.22"/>'
    s += f'<path d="{d}" fill="url(#ticketG)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
    s += T(cx, top + 50, titulo, size * 1.15, INK, font=DISP)
    s += f'<path d="M {f(x0+20)} {f(top+70)} L {f(x0+w-20)} {f(top+70)}" stroke="{INK}" stroke-width="3" stroke-dasharray="8 7"/>'
    y = top + 70 + lh
    for i, (c, p) in enumerate(lineas):
        s += g(f"{id_}_l{i}" if id_ else None, T(x0 + 22, y, c, size, INK, "start") + T(x0 + w - 22, y, p, size, INK, "end"))
        y += lh
    if total:
        s += f'<path d="M {f(x0+20)} {f(y-lh*0.55)} L {f(x0+w-20)} {f(y-lh*0.55)}" stroke="{INK}" stroke-width="4"/>'
        s += g(f"{id_}_total" if id_ else None, T(x0 + 22, y + lh * 0.35, "TOTAL", size * 1.1, INK, "start", DISP)
               + T(x0 + w - 22, y + lh * 0.35, total, size * 1.25, CORAL, "end", DISP))
    body = gt(id_, f"rotate({f(rot_)} {f(cx)} {f(top+h/2)})", s) if rot_ else g(id_, s)
    return Pieza(body, {"centro": (cx, top + h / 2)}, (x0, top, x0 + w, top + h + 14))


# ------------------------------------------------------------------ recta numérica
def recta_numerica(id_, x0, x1, y, a=0, b=10, paso=None, etiquetas=None, col="#FFFFFF", size=34):
    """Regla/recta numérica de a a b (barra con marcas). etiquetas = {valor: texto} para rotular marcas concretas.
    .puntos['x'] = función valor → x (úsala para colocar marcadores encima)."""
    paso = paso or (b - a) / 10
    X = lambda v: x0 + (x1 - x0) * (v - a) / (b - a)
    s = f'<rect x="{f(x0-24+8)}" y="{f(y-22+10)}" width="{f(x1-x0+48)}" height="44" rx="22" fill="{INK}" opacity="0.22"/>'
    s += f'<rect x="{f(x0-24)}" y="{f(y-22)}" width="{f(x1-x0+48)}" height="44" rx="22" fill="{degradado(col, 0.12)}" stroke="{INK}" stroke-width="7"/>'
    v = a
    i = 0
    while v <= b + 1e-9:
        big = abs((v - a) / paso - round((v - a) / paso)) < 1e-6 and i % 5 == 0
        hh = 30 if big else 16
        s += f'<path d="M {f(X(v))} {f(y-hh/2)} L {f(X(v))} {f(y+hh/2)}" stroke="{INK}" stroke-width="{5 if big else 3}" stroke-linecap="round"/>'
        v += paso
        i += 1
    for val, txt in (etiquetas or {a: str(a), b: str(b)}).items():
        s += T(X(val), y + 22 + size * 1.25, txt, size, "#FFFFFF", font=DISP, extra=f'stroke="{INK}" stroke-width="7" paint-order="stroke"')
    s += brillo(f"M {f(x0)} {f(y-10)} L {f(x1)} {f(y-10)}", 4, 0.6)
    return Pieza(g(id_, s), {"x": X, "a": (X(a), y), "b": (X(b), y)}, (x0 - 24, y - 22, x1 + 24, y + 22 + size * 1.6))


# ------------------------------------------------------------------ fondo: pasillo del súper
def supermercado(W=1080, H=1920, suelo_y=None, seed=5, rotulo="PASILLO 4"):
    """Fondo de supermercado: pared clara con luces de techo, estantería de fondo llena y suelo de baldosas.
    Sin ids. La estantería de fondo ocupa de y≈0.2H a suelo_y (pon delante personas, carritos y carteles)."""
    sy = suelo_y or H * 0.62
    o = f'<rect width="{W}" height="{H}" fill="url(#superPared)"/>'
    for x in range(int(W * 0.12), W, int(W * 0.38)):
        o += f'<rect x="{x}" y="{f(H*0.06)}" width="{f(W*0.24)}" height="26" rx="13" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/>'
        o += f'<ellipse cx="{f(x+W*0.12)}" cy="{f(H*0.06+60)}" rx="{f(W*0.16)}" ry="60" fill="#FFF6B8" opacity="0.35"/>'
    if rotulo:
        rw = len(rotulo) * 34 + 80
        o += f'<rect x="{f(W/2-rw/2)}" y="{f(H*0.1)}" width="{f(rw)}" height="74" rx="14" fill="{CORAL}" stroke="{INK}" stroke-width="6"/>'
        o += T(W / 2, H * 0.1 + 50, rotulo, 36, "#FFFFFF", font=DISP)
        o += f'<path d="M {f(W/2-rw/3)} {f(H*0.1)} L {f(W/2-rw/3)} {f(H*0.06+26)} M {f(W/2+rw/3)} {f(H*0.1)} L {f(W/2+rw/3)} {f(H*0.06+26)}" stroke="{INK}" stroke-width="4"/>'
    top = H * 0.2 + 30
    alto = (sy - top - 30) / 3
    o += estanteria(None, -20, W + 20, top, 3, alto, seed, col="#5A6170")
    o += f'<rect x="0" y="{f(sy)}" width="{W}" height="{f(H-sy)}" fill="url(#superSuelo)"/>'
    o += f'<path d="M 0 {f(sy)} L {W} {f(sy)}" stroke="{INK}" stroke-width="8"/>'
    o += f'<g stroke="#AEB8C9" stroke-width="4">' + "".join(
        f'<line x1="0" y1="{f(y)}" x2="{W}" y2="{f(y)}"/>' for y in [sy + (H - sy) * k for k in (0.12, 0.28, 0.48, 0.72)])
    o += "".join(f'<line x1="{f(W/2 + (x - W/2) * 0.55)}" y1="{f(sy)}" x2="{f(W/2 + (x - W/2) * 1.6)}" y2="{H}"/>' for x in range(-90, W + 200, 180)) + "</g>"
    return o


# ------------------------------------------------------------------ billetes (lote7-12-mesa-electoral)
BILLETES = {"5": "#9AA7A0", "10": "#E0525A", "20": "#4A86D9", "50": "#F29B3A", "100": "#3FAE6A", "200": "#E8C14A"}


def billete(id_, cx, cy, w=300, valor="50", rot_=0, col=None):
    """Billete de euro estilizado (no es copia del real): color por valor, cifra grande, «EURO», arco y anillo de
    estrellas. Proporción ≈ 2:1. Sub-id {id}_cifra (pulse). .puntos: centro."""
    col = col or BILLETES.get(valor, "#3FAE6A")
    h = w * 0.52
    x0, y0 = cx - w / 2, cy - h / 2
    s = sombra_caja(x0, y0, w, h, 12, 8, 10, 0.25)
    s += f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" rx="12" fill="{degradado(col, 0.22, "d")}" stroke="{INK}" stroke-width="6"/>'
    s += f'<rect x="{f(x0+w*0.04)}" y="{f(y0+h*0.08)}" width="{f(w*0.92)}" height="{f(h*0.84)}" rx="8" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.55"/>'
    ax = x0 + w * 0.62
    s += (f'<path d="M {f(ax-w*0.13)} {f(y0+h*0.86)} L {f(ax-w*0.13)} {f(y0+h*0.42)} A {f(w*0.13)} {f(w*0.13)} 0 0 1 {f(ax+w*0.13)} {f(y0+h*0.42)} '
          f'L {f(ax+w*0.13)} {f(y0+h*0.86)} Z" fill="#FFFFFF" fill-opacity="0.35" stroke="{INK}" stroke-width="4"/>')
    for k in range(12):
        a = k * math.pi / 6
        s += f'<circle cx="{f(x0+w*0.84+w*0.07*math.cos(a))}" cy="{f(y0+h*0.3+w*0.07*math.sin(a))}" r="{f(w*0.011)}" fill="#FFE15A" stroke="{INK}" stroke-width="1.5"/>'
    s += f'<rect x="{f(x0+w*0.42)}" y="{f(y0)}" width="{f(w*0.035)}" height="{f(h)}" fill="#E9EDF5" opacity="0.7"/>'
    s += g(f"{id_}_cifra", T(x0 + w * 0.22, y0 + h * 0.6, valor, h * 0.5 * min(1, 2.4 / max(1, len(valor))), "#FFFFFF", font=DISP))
    s += T(x0 + w * 0.22, y0 + h * 0.84, "EURO", h * 0.13, INK, font=DISP)
    s += T(x0 + w * 0.88, y0 + h * 0.86, valor, h * 0.16, INK, font=DISP)
    s += brillo(f"M {f(x0+12)} {f(y0+12)} L {f(x0+w*0.35)} {f(y0+12)}", 5, 0.6)
    return Pieza(gt(id_, f"rotate({f(rot_)} {f(cx)} {f(cy)})", s), {"centro": (cx, cy)}, (x0, y0, x0 + w, y0 + h))

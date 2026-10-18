"""Piezas de frío y calor en casa: congelador, cuenco (líquido o helado), escarcha, corrientes de convección,
burbujas de gas, vapor y gráfica de enfriamiento. Rescatadas de content/lote8-04-agua-caliente (efecto Mpemba)."""
import math
import random

from libreria.svg.base import (INK, LIME, CORAL, Pieza, g, f, T, DISP, MONO, degradado, sombra, sombra_caja, brillo,
                               trazo, registrar_defs, lg, rg, shade, copo)

registrar_defs(
    lg("congInt", [(0, "#F4FBFF"), (0.6, "#D6ECFA"), (1, "#B4D6EE")])
    + lg("congCuerpo", [(0, "#FFFFFF"), (1, "#D5DDE8")])
    + lg("escarchaG", [(0, "#FFFFFF"), (1, "#CFE8F8")])
    + lg("heladoLiq", [(0, "#FFF3D6"), (1, "#F2D49A")])
    + lg("heladoHielo", [(0, "#FFFFFF"), (1, "#E3E9F2")])
    + rg("vaporR", [(0, "#FFFFFF", 0.95), (1, "#FFFFFF", 0.0)])
)


# ------------------------------------------------------------------ congelador vertical con la puerta abierta
def congelador(id_, cx, base, w=380, h=760, baldas=3, puerta=True, escarcha=True, rotulo=None):
    """Congelador doméstico vertical abierto (cuerpo blanco, interior helado con baldas de rejilla y escarcha).
    La puerta abierta queda a la izquierda, en perspectiva. Sub-ids: {id}_puerta, {id}_frio (vaho frío que sale: float/drift),
    {id}_luz (pulse). .puntos: baldas = [y de cada balda, de arriba abajo], interior = (x0, y0, x1, y1), centro."""
    x0, top = cx - w / 2, base - h
    o = sombra(cx + 20, base + 6, w * 0.62, 18, 0.28)
    o += sombra_caja(x0, top, w, h, 18, 12, 14, 0.22)
    o += f'<rect x="{f(x0)}" y="{f(top)}" width="{f(w)}" height="{f(h)}" rx="18" fill="url(#congCuerpo)" stroke="{INK}" stroke-width="8"/>'
    m = w * 0.07
    ix0, iy0, ix1, iy1 = x0 + m, top + m, x0 + w - m, base - m * 1.6
    o += f'<rect x="{f(ix0)}" y="{f(iy0)}" width="{f(ix1-ix0)}" height="{f(iy1-iy0)}" rx="10" fill="url(#congInt)" stroke="{INK}" stroke-width="6"/>'
    o += g(f"{id_}_luz" if id_ else None,
           f'<ellipse cx="{f(cx)}" cy="{f(iy0+(iy1-iy0)*0.4)}" rx="{f((ix1-ix0)*0.42)}" ry="{f((iy1-iy0)*0.4)}" fill="#FFFFFF" opacity="0.35"/>'
           f'<rect x="{f(ix0+14)}" y="{f(iy0+10)}" width="{f(ix1-ix0-28)}" height="12" rx="6" fill="#FFFFFF" opacity="0.95"/>')
    ys = []
    bh = (iy1 - iy0) / (baldas + 1)
    rnd = random.Random(3)
    for b in range(baldas):
        yb = iy0 + bh * (b + 1) + bh * 0.25
        ys.append(yb)
        if escarcha:
            fr = f"M {f(ix0+6)} {f(yb)} "
            x = ix0 + 6
            while x < ix1 - 10:
                x2 = min(ix1 - 6, x + rnd.uniform(14, 26))
                fr += f"L {f((x+x2)/2)} {f(yb-rnd.uniform(6, 13))} L {f(x2)} {f(yb)} "
                x = x2
            o += f'<path d="{fr}Z" fill="url(#escarchaG)" stroke="#9CC7E6" stroke-width="2.5" stroke-linejoin="round"/>'
        o += f'<rect x="{f(ix0+2)}" y="{f(yb)}" width="{f(ix1-ix0-4)}" height="12" rx="4" fill="#C9D6E6" stroke="{INK}" stroke-width="4"/>'
        o += "".join(f'<line x1="{f(xx)}" y1="{f(yb+2)}" x2="{f(xx)}" y2="{f(yb+10)}" stroke="#8C9BB0" stroke-width="2.5"/>'
                     for xx in [ix0 + 20 + k * 26 for k in range(int((ix1 - ix0 - 30) // 26))])
    # escarcha en las esquinas del interior
    if escarcha:
        for (ex, ey, sg) in ((ix0, iy0, 1), (ix1, iy0, -1)):
            o += f'<path d="M {f(ex)} {f(ey+60)} Q {f(ex+sg*12)} {f(ey+12)} {f(ex+sg*60)} {f(ey)} L {f(ex)} {f(ey)} Z" fill="#FFFFFF" opacity="0.9"/>'
    # cajón inferior
    o += f'<rect x="{f(x0+m)}" y="{f(iy1+m*0.35)}" width="{f(w-2*m)}" height="{f(m*0.9)}" rx="6" fill="{shade("#D5DDE8", -0.1)}" stroke="{INK}" stroke-width="5"/>'
    if rotulo:
        o += T(cx, iy1 + m * 1.0, rotulo, m * 0.55, INK, font=DISP)
    o += brillo(f"M {f(x0+14)} {f(top+40)} L {f(x0+14)} {f(base-40)}", 6, 0.8)
    if puerta:
        pw = w * 0.32
        d = (f"M {f(x0)} {f(top+8)} L {f(x0-pw)} {f(top-h*0.05)} L {f(x0-pw)} {f(base+h*0.05)} L {f(x0)} {f(base-8)} Z")
        pu = f'<path d="{d}" fill="url(#congCuerpo)" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'
        di = (f"M {f(x0-pw*0.12)} {f(top+h*0.06)} L {f(x0-pw*0.86)} {f(top+h*0.0)} L {f(x0-pw*0.86)} {f(base+h*0.0)} L {f(x0-pw*0.12)} {f(base-h*0.06)} Z")
        pu += f'<path d="{di}" fill="#EEF4FA" stroke="#9AA9BE" stroke-width="4" stroke-linejoin="round"/>'
        for k in range(3):
            yy = top + h * (0.22 + k * 0.26)
            pu += f'<path d="M {f(x0-pw*0.8)} {f(yy)} L {f(x0-pw*0.18)} {f(yy+8)}" stroke="#9AA9BE" stroke-width="6" stroke-linecap="round"/>'
        pu += f'<rect x="{f(x0-pw*0.96)}" y="{f(top+h*0.4)}" width="12" height="{f(h*0.16)}" rx="6" fill="#B8C3D3" stroke="{INK}" stroke-width="4"/>'
        o += g(f"{id_}_puerta" if id_ else None, pu)
    # vaho frío que sale por abajo
    fr = ""
    for k, (dx, dy, r) in enumerate(((-0.2, 0.0, 30), (0.05, 0.03, 38), (0.3, -0.01, 28), (0.5, 0.04, 24))):
        fr += f'<circle cx="{f(cx+dx*w)}" cy="{f(base-m*1.6+dy*h)}" r="{f(r)}" fill="#FFFFFF" opacity="0.55"/>'
    o += g(f"{id_}_frio" if id_ else None, fr)
    return Pieza(g(id_, o), {"baldas": ys, "interior": (ix0, iy0, ix1, iy1), "centro": (cx, top + h / 2)},
                 (x0 - (w * 0.32 if puerta else 0), top - h * 0.05, x0 + w, base + h * 0.05))


# ------------------------------------------------------------------ cuenco con mezcla líquida o helada
def cuenco(id_, cx, base, w=220, estado="liquido", col_liq="url(#heladoLiq)", col="#FFFFFF", vapor=False):
    """Cuenco de metal visto de lado con su contenido: estado 'liquido' (mezcla con superficie brillante),
    'helado' (bola de helado con cristales). vapor=True añade vapor en {id}_vapor (float). .puntos: centro, borde."""
    h = w * 0.42
    top = base - h
    o = sombra(cx + 10, base + 6, w * 0.55, 12, 0.25)
    ry = w * 0.1
    if estado == "helado":
        cont = (f'<path d="M {f(cx-w*0.45)} {f(top+2)} C {f(cx-w*0.42)} {f(top-h*0.75)}, {f(cx+w*0.42)} {f(top-h*0.75)}, {f(cx+w*0.45)} {f(top+2)} Z" '
                f'fill="url(#heladoHielo)" stroke="{INK}" stroke-width="6"/>')
        cont += f'<ellipse cx="{f(cx-w*0.14)}" cy="{f(top-h*0.32)}" rx="{f(w*0.08)}" ry="{f(h*0.1)}" fill="#FFFFFF" opacity="0.9"/>'
        for (dx, dy, r) in ((-0.22, -0.18, 0.08), (0.12, -0.38, 0.07), (0.28, -0.1, 0.06)):
            cont += copo(cx + dx * w, top + dy * h, r * w, 15, "#6FA8D8")
    else:
        cont = f'<ellipse cx="{f(cx)}" cy="{f(top+ry*0.4)}" rx="{f(w*0.47)}" ry="{f(ry)}" fill="{col_liq}" stroke="{INK}" stroke-width="5"/>'
        cont += f'<ellipse cx="{f(cx-w*0.14)}" cy="{f(top+ry*0.2)}" rx="{f(w*0.12)}" ry="{f(ry*0.35)}" fill="#FFFFFF" opacity="0.8"/>'
    o += cont
    d = (f"M {f(cx-w/2)} {f(top)} C {f(cx-w*0.48)} {f(base-h*0.1)}, {f(cx-w*0.3)} {f(base)}, {f(cx)} {f(base)} "
         f"C {f(cx+w*0.3)} {f(base)}, {f(cx+w*0.48)} {f(base-h*0.1)}, {f(cx+w/2)} {f(top)} Z")
    o += f'<path d="{d}" fill="{degradado("#C9D3E0", 0.3, "h")}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
    o += f'<path d="M {f(cx-w/2)} {f(top)} L {f(cx+w/2)} {f(top)}" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>'
    o += brillo(f"M {f(cx-w*0.36)} {f(top+h*0.25)} Q {f(cx-w*0.3)} {f(base-h*0.2)} {f(cx-w*0.12)} {f(base-h*0.12)}", w * 0.03, 0.85)
    if vapor:
        o += g(f"{id_}_vapor" if id_ else None, vapor_subiendo(None, cx, top - 10, w * 0.6, h * 1.6))
    return Pieza(g(id_, o), {"centro": (cx, top + h / 2), "borde": (cx, top)}, (cx - w / 2, top - (h * 0.75 if estado == "helado" else ry), cx + w / 2, base + 8))


# ------------------------------------------------------------------ vapor que sube
def vapor_subiendo(id_, cx, y, w=160, alto=200, n=3, col="#FFFFFF"):
    """Hilos de vapor blancos (trazo doble azulado) que suben desde (cx, y). Para animar: float o drift."""
    o = ""
    for i in range(n):
        x = cx - w / 2 + w * (i + 0.5) / n
        q = alto / 4
        d = (f"M {f(x)} {f(y)} c {f(-q*0.5)} {f(-q*0.6)} {f(q*0.5)} {f(-q*1.3)} 0 {f(-q*2)} "
             f"c {f(-q*0.5)} {f(-q*0.6)} {f(q*0.5)} {f(-q*1.3)} 0 {f(-q*2)}")
        o += (f'<path d="{d}" fill="none" stroke="#9DB8D6" stroke-width="{f(w*0.09+6)}" stroke-linecap="round" opacity="0.8"/>'
              f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{f(w*0.09)}" stroke-linecap="round"/>')
    return g(id_, o)


# ------------------------------------------------------------------ capa de escarcha / charco
def escarcha(id_, x0, x1, y, grosor=26, seed=2, derretida=False):
    """Capa de escarcha sobre una superficie en y (picos blancos). derretida=True dibuja en su lugar un charquito de agua."""
    if derretida:
        cx, w = (x0 + x1) / 2, x1 - x0
        o = (f'<ellipse cx="{f(cx)}" cy="{f(y-3)}" rx="{f(w/2)}" ry="{f(grosor*0.35)}" fill="{degradado("#8FD3FF", 0.25)}" stroke="{INK}" stroke-width="4"/>'
             f'<ellipse cx="{f(cx-w*0.18)}" cy="{f(y-6)}" rx="{f(w*0.12)}" ry="{f(grosor*0.1)}" fill="#FFFFFF" opacity="0.85"/>')
        return g(id_, o)
    rnd = random.Random(seed)
    d = f"M {f(x0)} {f(y)} "
    x = x0
    while x < x1:
        x2 = min(x1, x + rnd.uniform(14, 28))
        d += f"L {f((x+x2)/2)} {f(y-rnd.uniform(grosor*0.5, grosor))} L {f(x2)} {f(y)} "
        x = x2
    o = f'<path d="{d}Z" fill="url(#escarchaG)" stroke="#7FB2D8" stroke-width="3.5" stroke-linejoin="round"/>'
    for k in range(4):
        o += f'<circle cx="{f(rnd.uniform(x0+10, x1-10))}" cy="{f(y-rnd.uniform(4, grosor*0.6))}" r="3" fill="#FFFFFF"/>'
    return g(id_, o)


# ------------------------------------------------------------------ corrientes de convección
def corrientes(id_, cx, cy, w=240, h=300, col=CORAL, col2="#5FB4EA"):
    """Dos bucles de convección (sube por el centro caliente, baja frío por los lados) dentro de un líquido.
    Trazos con flecha; anímalos con draw (entrada) y flow (bucle)."""
    o = ""
    for sg in (-1, 1):
        xa, xb = cx + sg * w * 0.06, cx + sg * w * 0.44
        ya, yb = cy - h / 2, cy + h / 2
        d = (f"M {f(xa)} {f(yb-h*0.1)} C {f(xa)} {f(ya)}, {f(xa)} {f(ya)}, {f((xa+xb)/2)} {f(ya)} "
             f"C {f(xb)} {f(ya)}, {f(xb)} {f(ya+h*0.1)}, {f(xb)} {f(cy)} C {f(xb)} {f(yb)}, {f(xb)} {f(yb)}, {f((xa+xb)/2)} {f(yb)}")
        o += trazo(d, 10, LIME, 7)
        ex, ey = (xa + xb) / 2, yb
        o += f'<path d="M {f(ex+sg*4)} {f(ey-16)} L {f(ex-sg*22)} {f(ey)} L {f(ex+sg*4)} {f(ey+16)} Z" fill="{LIME}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
        tx, ty = xa, ya + h * 0.12
        o += f'<path d="M {f(tx-14)} {f(ty+10)} L {f(tx)} {f(ty-14)} L {f(tx+14)} {f(ty+10)} Z" fill="{col}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
        bx, by = xb, cy + h * 0.15
        o += f'<path d="M {f(bx-14)} {f(by-10)} L {f(bx)} {f(by+14)} L {f(bx+14)} {f(by-10)} Z" fill="{col2}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    return g(id_, o)


# ------------------------------------------------------------------ burbujas de gas que escapan
def burbujas_gas(id_, cx, y0, y1, w=200, n=7, seed=4, texto=None):
    """Burbujas de gas disuelto subiendo entre y0 (abajo) e y1 (arriba). texto opcional dentro de las grandes (p. ej. 'O₂')."""
    rnd = random.Random(seed)
    o = ""
    for i in range(n):
        x = cx + rnd.uniform(-w / 2, w / 2)
        y = y0 + (y1 - y0) * (i + 0.5) / n
        r = rnd.uniform(9, 20)
        o += (f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="#FFFFFF" fill-opacity="0.75" stroke="{INK}" stroke-width="4"/>'
              f'<circle cx="{f(x-r*0.35)}" cy="{f(y-r*0.35)}" r="{f(r*0.25)}" fill="#FFFFFF"/>')
        if texto and r > 16:
            o += T(x, y + r * 0.3, texto, r * 0.8, INK, font=DISP)
    return g(id_, o)


# ------------------------------------------------------------------ gráfica temperatura frente a tiempo
def grafica_enfriamiento(id_, x0, y0, w, h, curvas, t_max=1.0, temp_max=100, cero=0, eje_x="TIEMPO", eje_y="TEMPERATURA",
                         marca_cero="0 °C", fondo="#FFFFFF"):
    """Gráfica de enfriamiento: ejes, línea de congelación discontinua y curvas.
    curvas = [(id_curva, [(t, temp), ...], color, rotulo)], t en 0..t_max y temp en °C. Cada curva va en su id (draw) y su rótulo en
    id_curva+'_r' (pop). .puntos: f(t, temp) → (x, y) en 'xy', y la y de la línea de congelación en 'cero'."""
    tmin = -20

    def xy(t, temp):
        return (x0 + 70 + (w - 100) * t / t_max, y0 + 30 + (h - 90) * (temp_max - temp) / (temp_max - tmin))
    o = f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" rx="16" fill="{fondo}" stroke="{INK}" stroke-width="6"/>'
    ax, ay = x0 + 70, y0 + h - 60
    o += f'<path d="M {f(ax)} {f(y0+24)} L {f(ax)} {f(ay)} L {f(x0+w-24)} {f(ay)}" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
    o += T(x0 + w - 30, ay + 40, eje_x, 22, INK, anchor="end", font=DISP)
    o += T(ax - 30, y0 + 40, eje_y, 20, INK, anchor="start", font=DISP, extra=f'transform="rotate(90 {f(ax-30)} {f(y0+40)})"')
    _, yc = xy(0, cero)
    o += f'<path d="M {f(ax)} {f(yc)} L {f(x0+w-24)} {f(yc)}" stroke="#5FB4EA" stroke-width="5" stroke-dasharray="14 10"/>'
    o += T(x0 + w - 30, yc - 12, marca_cero, 22, "#2F6FB0", anchor="end", font=DISP)
    for cid, pts_, col, rot in curvas:
        P = [xy(t, v) for t, v in pts_]
        d = "M " + " L ".join(f"{f(x)} {f(y)}" for x, y in P)
        cv = (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="15" stroke-linecap="round" stroke-linejoin="round"/>'
              f'<path d="{d}" fill="none" stroke="{col}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>')
        o += g(cid, cv)
        if rot:
            x, y = P[0]
            o += g(f"{cid}_r", T(x + 16, y - 14, rot, 24, shade(col, -0.25), anchor="start", font=DISP))
    return Pieza(g(id_, o), {"xy": xy, "cero": yc}, (x0, y0, x0 + w, y0 + h))

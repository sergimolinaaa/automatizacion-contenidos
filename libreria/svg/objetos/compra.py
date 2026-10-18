"""La compra: brik de leche, nevera de lácteos con puertas de cristal, ancla, caña de pescar, paquete de galletas,
tableta de chocolate, lista de la compra con tachones, barra de pan, horno de panadería, camión frigorífico,
carretilla de reparto con cajas y palé de briks.

Sale de: lote7-04-leche-fondo (por qué la leche está al fondo del súper).
"""
from ..base import (INK, LIME, CORAL, YEL, AZUL, f, g, gt, T, MONO, DISP, shade, trazo, sombra, sombra_caja, brillo,
                    lg, registrar_defs, degradado, Pieza, copo)

registrar_defs(
    lg("neveraCristal", [(0, "#E8F6FF"), (0.5, "#BFE4FA"), (1, "#9CCFEF")])
    + lg("frioG", [(0, "#DDF1FF"), (1, "#8FC7EC")])
    + lg("panG", [(0, "#F6C46A"), (1, "#C9802F")])
    + lg("chocoG", [(0, "#8A5232"), (1, "#4E2A16")])
    + lg("cartonG", [(0, "#E2B27A"), (1, "#B9844C")])
)

LECHE_AZUL = "#2F7FD6"


# ------------------------------------------------------------------ brik de leche
def brick_leche(id_, cx, base, s=1.0, col=LECHE_AZUL, texto="LECHE", rot_=0):
    """Brik de leche de 1 L: tapón, techo a dos aguas, banda de color con gota de leche y rótulo. Alto ≈ 230*s.
    .puntos: tapon, centro, base. Sub-id {id}_gota (pulse)."""
    w, h = 110 * s, 190 * s
    x0, y0 = cx - w / 2, base - h
    o = sombra(cx, base + 4 * s, w * 0.62, 9 * s, 0.22)
    # techo a dos aguas
    o += (f'<path d="M {f(x0)} {f(y0)} L {f(x0+w*0.18)} {f(y0-34*s)} L {f(x0+w*0.82)} {f(y0-34*s)} L {f(x0+w)} {f(y0)} Z" '
          f'fill="#F3F6FB" stroke="{INK}" stroke-width="{f(5.5*s)}" stroke-linejoin="round"/>')
    o += f'<rect x="{f(x0+w*0.16)}" y="{f(y0-44*s)}" width="{f(w*0.68)}" height="{f(12*s)}" rx="{f(4*s)}" fill="#E3E8F1" stroke="{INK}" stroke-width="{f(4.5*s)}"/>'
    o += f'<rect x="{f(cx+w*0.08)}" y="{f(y0-30*s)}" width="{f(26*s)}" height="{f(20*s)}" rx="{f(6*s)}" fill="{degradado(YEL, 0.3)}" stroke="{INK}" stroke-width="{f(4*s)}"/>'
    # cuerpo
    o += f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" rx="{f(6*s)}" fill="url(#papelG)" stroke="{INK}" stroke-width="{f(6*s)}"/>'
    o += (f'<path d="M {f(x0+3*s)} {f(y0+h*0.5)} Q {f(cx)} {f(y0+h*0.36)} {f(x0+w-3*s)} {f(y0+h*0.5)} L {f(x0+w-3*s)} {f(base-3*s)} '
          f'L {f(x0+3*s)} {f(base-3*s)} Z" fill="{degradado(col, 0.25)}"/>')
    gx, gy = cx, y0 + h * 0.25
    o += g(f"{id_}_gota" if id_ else None,
           f'<path d="M {f(gx)} {f(gy-24*s)} C {f(gx+20*s)} {f(gy)}, {f(gx+18*s)} {f(gy+20*s)}, {f(gx)} {f(gy+20*s)} '
           f'C {f(gx-18*s)} {f(gy+20*s)}, {f(gx-20*s)} {f(gy)}, {f(gx)} {f(gy-24*s)} Z" fill="#FFFFFF" stroke="{INK}" stroke-width="{f(4*s)}"/>')
    if texto:
        o += T(cx, y0 + h * 0.74, texto, h * 0.13 * min(1, 5 / max(1, len(texto))), "#FFFFFF", font=DISP,
               extra=f'stroke="{INK}" stroke-width="{f(3*s)}" paint-order="stroke"')
    o += f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" rx="{f(6*s)}" fill="none" stroke="{INK}" stroke-width="{f(6*s)}"/>'
    o += brillo(f"M {f(x0+12*s)} {f(y0+14*s)} L {f(x0+12*s)} {f(y0+h*0.42)}", 6 * s, 0.85)
    body = gt(id_, f"rotate({f(rot_)} {f(cx)} {f(base-h/2)})", o) if rot_ else g(id_, o)
    return Pieza(body, {"tapon": (cx + w * 0.08 + 13 * s, y0 - 30 * s), "centro": (cx, base - h / 2), "base": (cx, base)},
                 (x0, y0 - 44 * s, x0 + w, base))


# ------------------------------------------------------------------ nevera de lácteos
def nevera(id_, x0, top, w=420, h=520, puertas=2, baldas=3, rotulo="LÁCTEOS", col="#E9EEF6", seed=1, brillos=True):
    """Nevera vertical de supermercado con puertas de cristal y briks de leche en cada balda.
    Sub-ids: {id}_luz (resplandor frío interior: pulse/fade), {id}_briks, {id}_rotulo. .puntos: centro, puerta, base."""
    o = sombra_caja(x0, top, w, h, 14, 12, 14, 0.25)
    o += f'<rect x="{f(x0)}" y="{f(top)}" width="{f(w)}" height="{f(h)}" rx="14" fill="{degradado(col, 0.18)}" stroke="{INK}" stroke-width="7"/>'
    rh = h * 0.13
    o += g(f"{id_}_rotulo" if id_ else None,
           f'<rect x="{f(x0+14)}" y="{f(top+12)}" width="{f(w-28)}" height="{f(rh)}" rx="8" fill="{degradado(LECHE_AZUL, 0.25)}" stroke="{INK}" stroke-width="5"/>'
           + T(x0 + w / 2, top + 12 + rh * 0.7, rotulo, rh * 0.5, "#FFFFFF", font=DISP))
    iy0 = top + 24 + rh
    ih = h - (iy0 - top) - 26
    ix0, iw = x0 + 18, w - 36
    o += f'<rect x="{f(ix0)}" y="{f(iy0)}" width="{f(iw)}" height="{f(ih)}" rx="6" fill="url(#frioG)" stroke="{INK}" stroke-width="5"/>'
    o += g(f"{id_}_luz" if id_ else None,
           f'<rect x="{f(ix0+8)}" y="{f(iy0+6)}" width="{f(iw-16)}" height="16" rx="8" fill="#FFFFFF" opacity="0.9"/>'
           f'<ellipse cx="{f(ix0+iw/2)}" cy="{f(iy0+ih*0.45)}" rx="{f(iw*0.45)}" ry="{f(ih*0.45)}" fill="#FFFFFF" opacity="0.25"/>')
    bri = ""
    bh = ih / baldas
    for b in range(baldas):
        yb = iy0 + (b + 1) * bh - 8
        ss = min(0.5, (bh - 40) / 240)
        n = max(2, int((iw - 20) // (118 * ss)))
        for k in range(n):
            bx = ix0 + 14 + (k + 0.5) * (iw - 28) / n
            bri += brick_leche(None, bx, yb - 6, ss, (LECHE_AZUL, "#E84A3A", LECHE_AZUL, "#36B37E")[(k + b + seed) % 4], "")
        bri += f'<rect x="{f(ix0+4)}" y="{f(yb-6)}" width="{f(iw-8)}" height="14" rx="4" fill="#DDE4EF" stroke="{INK}" stroke-width="4"/>'
    o += g(f"{id_}_briks" if id_ else None, bri)
    # puertas de cristal
    pw = iw / puertas
    for p in range(puertas):
        px = ix0 + p * pw
        o += f'<rect x="{f(px)}" y="{f(iy0)}" width="{f(pw)}" height="{f(ih)}" fill="url(#neveraCristal)" fill-opacity="0.32" stroke="{INK}" stroke-width="6"/>'
        o += f'<rect x="{f(px+pw-26 if p % 2 == 0 else px+14)}" y="{f(iy0+ih*0.38)}" width="12" height="{f(ih*0.24)}" rx="6" fill="#C9D2E2" stroke="{INK}" stroke-width="4"/>'
        if brillos:
            o += brillo(f"M {f(px+18)} {f(iy0+ih*0.12)} L {f(px+pw*0.42)} {f(iy0+ih*0.02+10)}", 7, 0.7)
            o += brillo(f"M {f(px+18)} {f(iy0+ih*0.28)} L {f(px+pw*0.62)} {f(iy0+ih*0.12)}", 4, 0.5)
    o += f'<rect x="{f(x0)}" y="{f(top+h-18)}" width="{f(w)}" height="18" rx="6" fill="{shade(col, -0.35)}" stroke="{INK}" stroke-width="5"/>'
    return Pieza(g(id_, o), {"centro": (x0 + w / 2, top + h / 2), "puerta": (x0 + w / 2, iy0 + ih / 2), "base": (x0 + w / 2, top + h)},
                 (x0, top, x0 + w, top + h + 14))


# ------------------------------------------------------------------ ancla y caña
def ancla(id_, cx, cy, s=1.0, col="#3A4258"):
    """Ancla de barco (≈ 160×200 a s=1) dibujada con trazo doble."""
    d_arco = f"M {f(cx-70*s)} {f(cy+30*s)} Q {f(cx-60*s)} {f(cy+95*s)} {f(cx)} {f(cy+95*s)} Q {f(cx+60*s)} {f(cy+95*s)} {f(cx+70*s)} {f(cy+30*s)}"
    o = trazo(f"M {f(cx)} {f(cy-70*s)} L {f(cx)} {f(cy+92*s)}", 16 * s, col, 8 * s)
    o += trazo(f"M {f(cx-48*s)} {f(cy-38*s)} L {f(cx+48*s)} {f(cy-38*s)}", 14 * s, col, 8 * s)
    o += trazo(d_arco, 14 * s, col, 8 * s)
    for k in (-1, 1):
        x = cx + k * 70 * s
        o += (f'<path d="M {f(x)} {f(cy+8*s)} L {f(x-k*20*s)} {f(cy+38*s)} L {f(x+k*16*s)} {f(cy+40*s)} Z" fill="{col}" '
              f'stroke="{INK}" stroke-width="{f(5*s)}" stroke-linejoin="round"/>')
    o += f'<circle cx="{f(cx)}" cy="{f(cy-88*s)}" r="{f(20*s)}" fill="none" stroke="{INK}" stroke-width="{f(18*s)}"/>'
    o += f'<circle cx="{f(cx)}" cy="{f(cy-88*s)}" r="{f(20*s)}" fill="none" stroke="{col}" stroke-width="{f(9*s)}"/>'
    o += brillo(f"M {f(cx-3*s)} {f(cy-60*s)} L {f(cx-3*s)} {f(cy+40*s)}", 3 * s, 0.5)
    return Pieza(g(id_, o), {"centro": (cx, cy)}, (cx - 90 * s, cy - 115 * s, cx + 90 * s, cy + 110 * s))


def cana_pescar(id_, mango, punta, sedal=200, col="#2347FF"):
    """Caña de pescar desde `mango` (x, y) hasta `punta` (x, y), con carrete y sedal vertical de `sedal` px.
    Devuelve Pieza: .puntos['anzuelo'] = extremo del sedal (cuelga ahí el cebo). Sub-id {id}_sedal (draw)."""
    (x0, y0), (x1, y1) = mango, punta
    o = trazo(f"M {f(x0)} {f(y0)} Q {f((x0+x1)/2)} {f(min(y0, y1)-40)} {f(x1)} {f(y1)}", 9, "#E9EDF5", 7)
    o += trazo(f"M {f(x0)} {f(y0)} L {f(x0+(x1-x0)*0.18)} {f(y0+(y1-y0)*0.18-8)}", 20, col, 8)
    rx, ry = x0 + (x1 - x0) * 0.24, y0 + (y1 - y0) * 0.24 + 18
    o += f'<circle cx="{f(rx)}" cy="{f(ry)}" r="24" fill="{degradado("#9AA3B5", 0.25)}" stroke="{INK}" stroke-width="6"/>'
    o += f'<circle cx="{f(rx)}" cy="{f(ry)}" r="7" fill="{INK}"/>'
    o += g(f"{id_}_sedal" if id_ else None,
           f'<path d="M {f(x1)} {f(y1)} L {f(x1)} {f(y1+sedal)}" fill="none" stroke="{INK}" stroke-width="4"/>')
    o += f'<circle cx="{f(x1)}" cy="{f(y1)}" r="7" fill="{CORAL}" stroke="{INK}" stroke-width="3"/>'
    return Pieza(g(id_, o), {"anzuelo": (x1, y1 + sedal), "punta": (x1, y1)},
                 (min(x0, x1) - 30, min(y0, y1) - 60, max(x0, x1) + 30, max(y0, y1 + sedal)))


# ------------------------------------------------------------------ caprichos
def galletas(id_, cx, cy, s=1.0, col="#2347FF", texto="GALLETAS", rot_=0):
    """Paquete de galletas tumbado (≈ 240×110 a s=1) con galletas asomando por un extremo abierto."""
    w, h = 220 * s, 96 * s
    x0, y0 = cx - w / 2, cy - h / 2
    o = sombra_caja(x0, y0, w, h, 22 * s, 7 * s, 9 * s, 0.22)
    for k in range(3):
        gx = x0 + w - 6 * s + k * 9 * s
        o += f'<ellipse cx="{f(gx)}" cy="{f(cy)}" rx="{f(14*s)}" ry="{f(42*s)}" fill="{degradado("#E8B166", 0.25)}" stroke="{INK}" stroke-width="{f(4*s)}"/>'
    o += f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" rx="{f(22*s)}" fill="{degradado(col, 0.25)}" stroke="{INK}" stroke-width="{f(6*s)}"/>'
    o += f'<path d="M {f(x0+16*s)} {f(y0)} L {f(x0+16*s)} {f(y0+h)}" stroke="{INK}" stroke-width="{f(3*s)}" stroke-dasharray="{f(5*s)} {f(5*s)}"/>'
    for k in range(3):
        o += f'<circle cx="{f(x0+w*0.3+k*w*0.2)}" cy="{f(cy+h*0.18)}" r="{f(15*s)}" fill="#E8B166" stroke="{INK}" stroke-width="{f(3.5*s)}"/>'
        o += f'<circle cx="{f(x0+w*0.3+k*w*0.2-4*s)}" cy="{f(cy+h*0.14)}" r="{f(3*s)}" fill="#8A5232"/>'
    o += T(cx, y0 + h * 0.36, texto, h * 0.2, "#FFFFFF", font=DISP)
    o += brillo(f"M {f(x0+26*s)} {f(y0+10*s)} L {f(x0+w*0.7)} {f(y0+10*s)}", 5 * s, 0.7)
    body = gt(id_, f"rotate({f(rot_)} {f(cx)} {f(cy)})", o) if rot_ else g(id_, o)
    return Pieza(body, {"centro": (cx, cy)}, (x0, y0, x0 + w + 30 * s, y0 + h))


def chocolate(id_, cx, cy, s=1.0, rot_=0, col=CORAL, texto="CHOCO"):
    """Tableta de chocolate con envoltorio abierto (≈ 150×230 a s=1): onzas a la vista arriba, papel de color abajo."""
    w, h = 150 * s, 230 * s
    x0, y0 = cx - w / 2, cy - h / 2
    o = sombra_caja(x0, y0, w, h, 10 * s, 7 * s, 9 * s, 0.22)
    o += f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" rx="{f(10*s)}" fill="url(#chocoG)" stroke="{INK}" stroke-width="{f(6*s)}"/>'
    for i in range(2):
        for j in range(2):
            ox, oy = x0 + 12 * s + i * (w - 24 * s) / 2, y0 + 12 * s + j * 46 * s
            o += f'<rect x="{f(ox)}" y="{f(oy)}" width="{f((w-24*s)/2-6*s)}" height="{f(40*s)}" rx="{f(5*s)}" fill="#7A4628" stroke="{INK}" stroke-width="{f(3*s)}"/>'
            o += brillo(f"M {f(ox+6*s)} {f(oy+7*s)} L {f(ox+(w-24*s)/2-14*s)} {f(oy+7*s)}", 3 * s, 0.45)
    py = y0 + 110 * s
    o += (f'<path d="M {f(x0)} {f(py)} L {f(x0+w*0.25)} {f(py-12*s)} L {f(x0+w*0.5)} {f(py+2*s)} L {f(x0+w*0.75)} {f(py-14*s)} L {f(x0+w)} {f(py)} '
          f'L {f(x0+w)} {f(y0+h-10*s)} Q {f(x0+w)} {f(y0+h)} {f(x0+w-10*s)} {f(y0+h)} L {f(x0+10*s)} {f(y0+h)} Q {f(x0)} {f(y0+h)} {f(x0)} {f(y0+h-10*s)} Z" '
          f'fill="{degradado(col, 0.25)}" stroke="{INK}" stroke-width="{f(6*s)}" stroke-linejoin="round"/>')
    o += T(cx, y0 + h * 0.76, texto, h * 0.11, "#FFFFFF", font=DISP)
    o += brillo(f"M {f(x0+12*s)} {f(py+20*s)} L {f(x0+12*s)} {f(y0+h-16*s)}", 5 * s, 0.6)
    body = gt(id_, f"rotate({f(rot_)} {f(cx)} {f(cy)})", o) if rot_ else g(id_, o)
    return Pieza(body, {"centro": (cx, cy)}, (x0, y0, x0 + w, y0 + h))


# ------------------------------------------------------------------ lista de la compra
def lista_compra(id_, cx, cy, w=230, h=300, items=("LECHE",), tachadas=(0,), titulo="LISTA", rot_=-4, size=None):
    """Hoja de libreta con espiral, título y elementos a mano. Cada tachón está en {id}_t<i> (anímalo con draw)
    y cada línea en {id}_i<i>. .puntos['items'] = [(x, y)] del centro de cada línea."""
    x0, y0 = cx - w / 2, cy - h / 2
    size = size or w * 0.14
    o = sombra_caja(x0, y0, w, h, 10, 8, 10, 0.24)
    o += f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" rx="10" fill="url(#papelCrema)" stroke="{INK}" stroke-width="6"/>'
    for k in range(5):
        sx = x0 + w * (0.15 + k * 0.175)
        o += f'<path d="M {f(sx)} {f(y0+14)} Q {f(sx+6)} {f(y0-14)} {f(sx+14)} {f(y0+6)}" fill="none" stroke="#9AA3B5" stroke-width="6" stroke-linecap="round"/>'
    o += T(cx, y0 + size * 1.9, titulo, size * 1.05, CORAL, font=DISP)
    lh = size * 1.75
    pts_ = []
    for i, it in enumerate(items):
        y = y0 + size * 2.6 + (i + 1) * lh
        o += f'<path d="M {f(x0+16)} {f(y+8)} L {f(x0+w-16)} {f(y+8)}" stroke="#AFC3E0" stroke-width="3"/>'
        o += g(f"{id_}_i{i}" if id_ else None, T(x0 + 26, y, it, size, INK, "start", MONO))
        tw = len(it) * size * 0.62
        if i in tachadas:
            o += g(f"{id_}_t{i}" if id_ else None,
                   f'<path d="M {f(x0+18)} {f(y-size*0.32)} L {f(x0+34+tw)} {f(y-size*0.4)}" fill="none" stroke="{CORAL}" stroke-width="{f(size*0.22)}" stroke-linecap="round"/>')
        pts_.append((x0 + 26 + tw / 2, y - size * 0.35))
    body = gt(id_, f"rotate({f(rot_)} {f(cx)} {f(cy)})", o) if rot_ else g(id_, o)
    return Pieza(body, {"items": pts_, "centro": (cx, cy)}, (x0 - 10, y0 - 20, x0 + w + 10, y0 + h + 10))


# ------------------------------------------------------------------ pan
def barra_pan(id_, cx, cy, L=300, rot_=-12, grosor=None):
    """Barra de pan dorada con cortes (≈ L × 0.24L)."""
    hh = grosor or L * 0.24
    x0, x1 = cx - L / 2, cx + L / 2
    d = (f"M {f(x0+hh*0.4)} {f(cy-hh/2)} L {f(x1-hh*0.4)} {f(cy-hh/2)} Q {f(x1+hh*0.2)} {f(cy)} {f(x1-hh*0.4)} {f(cy+hh/2)} "
         f"L {f(x0+hh*0.4)} {f(cy+hh/2)} Q {f(x0-hh*0.2)} {f(cy)} {f(x0+hh*0.4)} {f(cy-hh/2)} Z")
    o = f'<path d="{d}" fill="url(#panG)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
    n = max(3, int(L // 70))
    for k in range(n):
        x = x0 + L * (k + 0.75) / (n + 0.5)
        o += f'<path d="M {f(x-hh*0.32)} {f(cy+hh*0.18)} Q {f(x)} {f(cy-hh*0.12)} {f(x+hh*0.32)} {f(cy-hh*0.26)}" fill="none" stroke="#9A5A1E" stroke-width="{f(hh*0.14)}" stroke-linecap="round"/>'
        o += f'<path d="M {f(x-hh*0.28)} {f(cy+hh*0.12)} Q {f(x)} {f(cy-hh*0.14)} {f(x+hh*0.26)} {f(cy-hh*0.26)}" fill="none" stroke="#FBE3A6" stroke-width="{f(hh*0.05)}" stroke-linecap="round"/>'
    o += brillo(f"M {f(x0+hh*0.6)} {f(cy-hh*0.32)} L {f(x1-hh*0.8)} {f(cy-hh*0.32)}", 4, 0.6)
    return Pieza(gt(id_, f"rotate({f(rot_)} {f(cx)} {f(cy)})", o) if id_ else f'<g transform="rotate({f(rot_)} {f(cx)} {f(cy)})">{o}</g>',
                 {"centro": (cx, cy)}, (x0, cy - hh, x1, cy + hh))


def horno_pan(id_, cx, base, w=380, h=430, rotulo="PANADERÍA"):
    """Mostrador de panadería con horno de ladrillo (boca encendida) y cesta de barras. Sub-ids {id}_vapor (float/drift),
    {id}_fuego (pulse), {id}_barras. .puntos: boca, cesta."""
    x0, top = cx - w / 2, base - h
    o = sombra(cx, base + 6, w * 0.55, 14, 0.25)
    o += f'<rect x="{f(x0)}" y="{f(top)}" width="{f(w)}" height="{f(h*0.62)}" rx="18" fill="{degradado("#C86B45", 0.25)}" stroke="{INK}" stroke-width="7"/>'
    for r in range(4):
        for c in range(6):
            bx = x0 + 14 + c * (w - 28) / 6 + (18 if r % 2 else 0)
            by = top + 16 + r * h * 0.14
            if bx + (w - 28) / 6 - 8 < x0 + w - 10:
                o += f'<rect x="{f(bx)}" y="{f(by)}" width="{f((w-28)/6-8)}" height="{f(h*0.14-8)}" rx="4" fill="#B65A37" opacity="0.6"/>'
    bw, bh = w * 0.52, h * 0.3
    bx0, by0 = cx - bw / 2, top + h * 0.2
    boca = f"M {f(bx0)} {f(by0+bh)} L {f(bx0)} {f(by0+bh*0.45)} A {f(bw/2)} {f(bh*0.45)} 0 0 1 {f(bx0+bw)} {f(by0+bh*0.45)} L {f(bx0+bw)} {f(by0+bh)} Z"
    o += f'<path d="{boca}" fill="#2A1A14" stroke="{INK}" stroke-width="7"/>'
    o += g(f"{id_}_fuego" if id_ else None,
           f'<ellipse cx="{f(cx)}" cy="{f(by0+bh*0.78)}" rx="{f(bw*0.38)}" ry="{f(bh*0.22)}" fill="#FF9F1C" opacity="0.9"/>'
           f'<ellipse cx="{f(cx)}" cy="{f(by0+bh*0.82)}" rx="{f(bw*0.22)}" ry="{f(bh*0.13)}" fill="#FFE15A"/>')
    o += f'<rect x="{f(x0-10)}" y="{f(top-34)}" width="{f(w+20)}" height="44" rx="10" fill="{degradado(YEL, 0.25)}" stroke="{INK}" stroke-width="6"/>'
    o += T(cx, top - 3, rotulo, 26, INK, font=DISP)
    # mostrador
    my = top + h * 0.62
    o += f'<rect x="{f(x0-20)}" y="{f(my)}" width="{f(w+40)}" height="{f(h*0.38)}" rx="12" fill="url(#maderaG)" stroke="{INK}" stroke-width="7"/>'
    o += brillo(f"M {f(x0)} {f(my+14)} L {f(x0+w)} {f(my+14)}", 5, 0.6)
    barras = ""
    for k, (dx, ang) in enumerate(((-0.28, -70), (-0.1, -82), (0.1, -98), (0.28, -110))):
        barras += barra_pan(None, cx + dx * w, my - 40, 190, ang, 38)
    o += g(f"{id_}_barras" if id_ else None, barras)
    o += (f'<path d="M {f(cx-w*0.42)} {f(my-26)} L {f(cx+w*0.42)} {f(my-26)} L {f(cx+w*0.36)} {f(my+40)} L {f(cx-w*0.36)} {f(my+40)} Z" '
          f'fill="url(#cartonG)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
    for k in range(4):
        o += f'<path d="M {f(cx-w*0.38+k*w*0.02)} {f(my-6+k*12)} L {f(cx+w*0.38-k*w*0.02)} {f(my-6+k*12)}" stroke="#9C6B38" stroke-width="3"/>'
    vap = ""
    for k, dx in enumerate((-0.18, 0.02, 0.2)):
        vx = cx + dx * w
        vy = top - 60
        vap += f'<path d="M {f(vx)} {f(vy)} C {f(vx-20)} {f(vy-30)}, {f(vx+20)} {f(vy-50)}, {f(vx)} {f(vy-84)}" fill="none" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round" opacity="0.85"/>'
    o += g(f"{id_}_vapor" if id_ else None, vap)
    return Pieza(g(id_, o), {"boca": (cx, by0 + bh * 0.7), "cesta": (cx, my - 20)}, (x0 - 20, top - 150, x0 + w + 20, base))


# ------------------------------------------------------------------ reparto
def camion_frigorifico(id_, cx, base, s=1.0, col="#F4F7FC", texto="FRÍO", espejo=False):
    """Camión frigorífico de perfil: cabina a la izquierda y caja isotérmica con equipo de frío; con espejo=True la
    cabina queda a la derecha. ≈ 620×330 a s=1. Sub-ids {id}_ruedas, {id}_frio (copos: pulse/float).
    .puntos: trasera (centro de la puerta trasera de la caja), cabina."""
    k = -1 if espejo else 1
    X = lambda dx: cx + k * dx * s
    Y = lambda dy: base - dy * s
    def R(x0_, y0_, x1_, y1_):
        xa, xb = sorted((X(x0_), X(x1_)))
        return xa, Y(y1_), xb - xa, Y(y0_) - Y(y1_)
    o = sombra(cx, base + 4, 320 * s, 16 * s, 0.25)
    # caja
    x, y, w, h = R(-120, 60, 310, 330)
    o += f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{f(10*s)}" fill="{degradado(col, 0.16)}" stroke="{INK}" stroke-width="{f(7*s)}"/>'
    xb, yb, wb, hb = R(-90, 150, 280, 230)
    o += f'<rect x="{f(xb)}" y="{f(yb)}" width="{f(wb)}" height="{f(hb)}" rx="{f(8*s)}" fill="{degradado(LECHE_AZUL, 0.25)}" stroke="{INK}" stroke-width="{f(5*s)}"/>'
    o += T(X(95), Y(172), texto, 56 * s, "#FFFFFF", font=DISP)
    fr = copo(X(-40), Y(190), 22 * s, 0, "#FFFFFF") + copo(X(230), Y(190), 22 * s, 20, "#FFFFFF")
    o += g(f"{id_}_frio" if id_ else None, fr)
    xr, yr, wr, hr = R(240, 300, 300, 345)
    o += f'<rect x="{f(xr)}" y="{f(yr)}" width="{f(wr)}" height="{f(hr)}" rx="{f(6*s)}" fill="#C9D2E2" stroke="{INK}" stroke-width="{f(5*s)}"/>'
    for i in range(4):
        o += f'<path d="M {f(X(250+i*13))} {f(Y(307))} L {f(X(250+i*13))} {f(Y(338))}" stroke="{INK}" stroke-width="{f(3*s)}"/>'
    o += brillo(f"M {f(X(-100))} {f(Y(312))} L {f(X(200))} {f(Y(312))}", 6 * s, 0.8)
    # bisagras traseras
    for dy in (110, 280):
        o += f'<rect x="{f(min(X(-122), X(-108)))}" y="{f(Y(dy+12))}" width="{f(14*s)}" height="{f(24*s)}" rx="{f(3*s)}" fill="#9AA3B5" stroke="{INK}" stroke-width="{f(3*s)}"/>'
    # cabina (al otro lado)
    # cabina: de x=-130 a x=-290 (delante de la caja, que va de -120 a 310)
    cab = [(-130, 60), (-130, 250), (-200, 250), (-250, 175), (-290, 160), (-290, 60)]
    dcab = " ".join(("M" if i == 0 else "L") + f" {f(X(px))} {f(Y(py))}" for i, (px, py) in enumerate(cab)) + " Z"
    o += f'<path d="{dcab}" fill="{degradado(CORAL, 0.22)}" stroke="{INK}" stroke-width="{f(7*s)}" stroke-linejoin="round"/>'
    vent = [(-145, 175), (-145, 235), (-195, 235), (-232, 178)]
    dv = " ".join(("M" if i == 0 else "L") + f" {f(X(px))} {f(Y(py))}" for i, (px, py) in enumerate(vent)) + " Z"
    o += f'<path d="{dv}" fill="url(#cristalG)" stroke="{INK}" stroke-width="{f(5*s)}" stroke-linejoin="round"/>'
    o += f'<rect x="{f(min(X(-290), X(-275)))}" y="{f(Y(120))}" width="{f(15*s)}" height="{f(26*s)}" rx="{f(4*s)}" fill="{YEL}" stroke="{INK}" stroke-width="{f(3*s)}"/>'
    o += f'<path d="M {f(X(-140))} {f(Y(150))} L {f(X(-170))} {f(Y(150))}" stroke="{INK}" stroke-width="{f(5*s)}" stroke-linecap="round"/>'
    o += f'<rect x="{f(min(X(-300), X(-110)))}" y="{f(Y(66))}" width="{f(190*s)}" height="{f(16*s)}" rx="{f(6*s)}" fill="#5A6170" stroke="{INK}" stroke-width="{f(4*s)}"/>'
    ruedas = ""
    for dx in (-215, 70, 200):
        ruedas += f'<circle cx="{f(X(dx))}" cy="{f(Y(42))}" r="{f(42*s)}" fill="{degradado("#3A4258", 0.2)}" stroke="{INK}" stroke-width="{f(7*s)}"/>'
        ruedas += f'<circle cx="{f(X(dx))}" cy="{f(Y(42))}" r="{f(16*s)}" fill="#D5DBE6" stroke="{INK}" stroke-width="{f(4*s)}"/>'
    o += g(f"{id_}_ruedas" if id_ else None, ruedas)
    xs = sorted((X(-300), X(312)))
    return Pieza(g(id_, o), {"trasera": (X(312), Y(195)), "cabina": (X(-210), Y(200))},
                 (xs[0], Y(345), xs[1], base))


def caja_carton(cx, base, w=90, h=70, texto="LECHE"):
    """Caja de cartón cerrada con cinta (sin id)."""
    x0, y0 = cx - w / 2, base - h
    o = f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" rx="4" fill="url(#cartonG)" stroke="{INK}" stroke-width="5"/>'
    o += f'<rect x="{f(cx-w*0.1)}" y="{f(y0)}" width="{f(w*0.2)}" height="{f(h*0.4)}" fill="#F3D7A8" stroke="{INK}" stroke-width="3"/>'
    if texto:
        o += T(cx, y0 + h * 0.78, texto, h * 0.2, "#7A4E28", font=MONO)
    return o


def carretilla(id_, x, base, s=1.0, cajas=3, espejo=False, texto="LECHE"):
    """Carretilla de mano (diablo) con `cajas` cajas apiladas. (x, base) = rueda en el suelo; el asa sube hacia
    atrás (izquierda; espejo=True a la derecha). Sub-ids {id}_cajas, {id}_rueda. .puntos: asa."""
    k = -1 if espejo else 1
    X = lambda dx: x + k * dx * s
    Y = lambda dy: base - dy * s
    o = sombra(X(40), base + 3, 90 * s, 9 * s, 0.22)
    cj = "".join(caja_carton(X(60), Y(18 + i * 72), 110 * s, 70 * s, texto) for i in range(cajas))
    o += g(f"{id_}_cajas" if id_ else None, cj)
    o += trazo(f"M {f(X(-10))} {f(Y(30+cajas*72+40))} L {f(X(0))} {f(Y(20))} L {f(X(120))} {f(Y(14))}", 10 * s, "#D04A2C", 7 * s)
    o += trazo(f"M {f(X(-24))} {f(Y(30+cajas*72+40))} L {f(X(6))} {f(Y(30+cajas*72+40))}", 14 * s, INK, 4 * s)
    rd = f'<circle cx="{f(X(10))}" cy="{f(Y(26))}" r="{f(26*s)}" fill="{degradado("#3A4258", 0.2)}" stroke="{INK}" stroke-width="{f(6*s)}"/>'
    rd += f'<circle cx="{f(X(10))}" cy="{f(Y(26))}" r="{f(8*s)}" fill="#D5DBE6"/>'
    o += g(f"{id_}_rueda" if id_ else None, rd)
    xs = sorted((X(-30), X(120)))
    return Pieza(g(id_, o), {"asa": (X(-10), Y(30 + cajas * 72 + 40))}, (xs[0], Y(30 + cajas * 72 + 50), xs[1], base))


def palet(id_, cx, base, w=240, filas=3, cols=None, texto="LECHE"):
    """Palé de madera con `filas` pisos de cajas de briks retractiladas. Sub-id opcional del grupo completo."""
    o = sombra(cx, base + 3, w * 0.55, 10, 0.22)
    x0 = cx - w / 2
    o += f'<rect x="{f(x0)}" y="{f(base-26)}" width="{f(w)}" height="26" rx="3" fill="url(#maderaG)" stroke="{INK}" stroke-width="5"/>'
    for k in range(3):
        o += f'<rect x="{f(x0+10+k*(w-50)/2)}" y="{f(base-20)}" width="30" height="20" fill="#7A4E28" stroke="{INK}" stroke-width="3"/>'
    cols = cols or max(2, int(w // 80))
    cw, ch = (w - 10) / cols, 64
    for r in range(filas):
        for c in range(cols):
            o += caja_carton(x0 + 5 + (c + 0.5) * cw, base - 26 - r * ch, cw - 4, ch - 4, texto if (r + c) % 2 == 0 else "")
    hh = filas * ch
    o += f'<rect x="{f(x0+2)}" y="{f(base-26-hh)}" width="{f(w-4)}" height="{f(hh)}" fill="#FFFFFF" opacity="0.18"/>'
    o += brillo(f"M {f(x0+12)} {f(base-26-hh+14)} L {f(x0+12)} {f(base-40)}", 5, 0.7)
    return Pieza(g(id_, o) if id_ else o, {"cima": (cx, base - 26 - hh)}, (x0, base - 26 - hh, x0 + w, base))

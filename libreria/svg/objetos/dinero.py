"""Dinero y bancos: fachada de banco, torres del Banco Central Europeo, estrellas y bandera de la UE, moneda de euro,
ficha de fórmula (piezas que se suman), carta o recibo de la hipoteca y palanca de mando (subir o bajar algo).

Sale de: lote8-05-hipoteca (por qué tu hipoteca sube o baja: Euríbor + diferencial).
"""
import math
from ..base import (INK, LIME, CORAL, YEL, f, g, gt, T, MONO, DISP, trazo, sombra, sombra_caja, brillo, brillo_arco,
                    lg, registrar_defs, degradado, Pieza)

AZUL_UE = "#003399"
ORO_UE = "#FFCC00"

registrar_defs(
    lg("bancoPiedra", [(0, "#FFFFFF"), (1, "#D9DEE8")])
    + lg("bancoColumna", [(0, "#C9D0DD"), (0.35, "#FFFFFF"), (1, "#B3BBCB")], 0, 0, 1, 0)
    + lg("bceCristal", [(0, "#BFE3FF"), (0.5, "#7FB8E6"), (1, "#4D86C2")], 0, 0, 1, 1)
    + lg("bceCristal2", [(0, "#A5D2F5"), (1, "#3F72AE")], 0, 0, 1, 1)
    + lg("monedaOro", [(0, "#FFE680"), (0.55, "#F2B705"), (1, "#C68A00")], 0, 0, 1, 1)
    + lg("reciboG", [(0, "#FFFFFF"), (1, "#EEF1F7")])
    + lg("reciboBanda", [(0, "#2B3A8C"), (1, "#16205A")])
)


def _estrella(cx, cy, r, col=ORO_UE, sw=0):
    p = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5
        rr = r if k % 2 == 0 else r * 0.42
        p.append(f"{f(cx + rr * math.cos(a))},{f(cy + rr * math.sin(a))}")
    st = f' stroke="{INK}" stroke-width="{f(sw)}" stroke-linejoin="round"' if sw else ""
    return f'<polygon points="{" ".join(p)}" fill="{col}"{st}/>'


def estrellas_ue(id_, cx, cy, r=60, s=None, col=ORO_UE, contorno=False):
    """Corona de 12 estrellas de la Unión Europea (sin fondo). s = radio de cada estrella."""
    s = s or r * 0.17
    o = "".join(_estrella(cx + r * math.cos(math.radians(k * 30 - 90)), cy + r * math.sin(math.radians(k * 30 - 90)), s, col,
                          s * 0.18 if contorno else 0) for k in range(12))
    return g(id_, o)


def bandera_ue(id_, cx, cy, w=180, h=120, rot_=0):
    """Bandera de la UE (azul con 12 estrellas doradas), tarjeta con contorno y brillo."""
    x0, y0 = cx - w / 2, cy - h / 2
    o = sombra_caja(x0, y0, w, h, 10, 8, 10, 0.25)
    o += f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" rx="10" fill="{degradado(AZUL_UE, 0.2)}" stroke="{INK}" stroke-width="6"/>'
    o += estrellas_ue(None, cx, cy, h * 0.33, h * 0.065)
    o += brillo(f"M {f(x0+12)} {f(y0+14)} L {f(x0+w*0.4)} {f(y0+14)}", 5, 0.45)
    return gt(id_, f"rotate({f(rot_)} {f(cx)} {f(cy)})", o) if rot_ else g(id_, o)


def moneda_euro(id_, cx, cy, r=50, rot_=0):
    """Moneda de euro dorada con el símbolo €."""
    o = f'<circle cx="{f(cx+r*0.12)}" cy="{f(cy+r*0.16)}" r="{f(r)}" fill="{INK}" opacity="0.25"/>'
    o += f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="url(#monedaOro)" stroke="{INK}" stroke-width="{f(max(4, r*0.12))}"/>'
    o += f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r*0.76)}" fill="none" stroke="#B07A00" stroke-width="{f(r*0.06)}" opacity="0.8"/>'
    o += T(cx, cy + r * 0.38, "€", r * 1.05, "#8A5A00", font=DISP)
    o += brillo_arco(cx, cy, r * 0.82, 200, 255, r * 0.1, 0.8)
    return gt(id_, f"rotate({f(rot_)} {f(cx)} {f(cy)})", o) if rot_ else g(id_, o)


def banco(id_, cx, base, w=360, rotulo="BANCO", col_friso=None, euro=True, ue=False):
    """Fachada clásica de banco: escalinata, 4 columnas, friso con `rotulo`, frontón con € (o estrellas UE con ue=True).
    Alto ≈ 1,05*w. .puntos: puerta, rotulo, cima, centro, izq, der. Sub-id {id}_puerta."""
    h_col = w * 0.5
    x0 = cx - w / 2
    esc_h = w * 0.09
    y_col0 = base - esc_h - h_col
    friso_h = w * 0.13
    y_fr = y_col0 - friso_h
    fr_h = w * 0.26
    o = sombra(cx, base + 4, w * 0.58, w * 0.05, 0.28)
    # escalinata
    for k in range(3):
        ww = w * (1.08 - k * 0.04)
        yy = base - (k + 1) * esc_h / 3
        o += f'<rect x="{f(cx-ww/2)}" y="{f(yy)}" width="{f(ww)}" height="{f(esc_h/3)}" fill="url(#bancoPiedra)" stroke="{INK}" stroke-width="5"/>'
    # muro de fondo + puerta
    o += f'<rect x="{f(x0+w*0.06)}" y="{f(y_col0)}" width="{f(w*0.88)}" height="{f(h_col)}" fill="#C5CCDA" stroke="{INK}" stroke-width="5"/>'
    pw, ph = w * 0.2, h_col * 0.62
    puerta = (f'<path d="M {f(cx-pw/2)} {f(base-esc_h)} L {f(cx-pw/2)} {f(base-esc_h-ph+pw/2)} A {f(pw/2)} {f(pw/2)} 0 0 1 {f(cx+pw/2)} {f(base-esc_h-ph+pw/2)} '
              f'L {f(cx+pw/2)} {f(base-esc_h)} Z" fill="{degradado("#7A4E28", 0.25)}" stroke="{INK}" stroke-width="5"/>'
              f'<line x1="{f(cx)}" y1="{f(base-esc_h-ph+pw*0.1)}" x2="{f(cx)}" y2="{f(base-esc_h)}" stroke="{INK}" stroke-width="4"/>'
              f'<circle cx="{f(cx-pw*0.12)}" cy="{f(base-esc_h-ph*0.4)}" r="{f(w*0.012)}" fill="{YEL}"/>'
              f'<circle cx="{f(cx+pw*0.12)}" cy="{f(base-esc_h-ph*0.4)}" r="{f(w*0.012)}" fill="{YEL}"/>')
    o += g(f"{id_}_puerta" if id_ else None, puerta)
    # columnas
    cw = w * 0.1
    for k in range(4):
        xc = x0 + w * 0.13 + k * (w * 0.74 - cw) / 3
        if 1 <= k <= 2 and abs(xc + cw / 2 - cx) < pw * 0.75:
            xc = cx - pw / 2 - cw - w * 0.03 if k == 1 else cx + pw / 2 + w * 0.03
        o += f'<rect x="{f(xc)}" y="{f(y_col0+8)}" width="{f(cw)}" height="{f(h_col-8)}" fill="url(#bancoColumna)" stroke="{INK}" stroke-width="5"/>'
        for j in (0.33, 0.66):
            o += f'<line x1="{f(xc+cw*j)}" y1="{f(y_col0+16)}" x2="{f(xc+cw*j)}" y2="{f(base-esc_h-10)}" stroke="#9AA3B5" stroke-width="2.5"/>'
        o += f'<rect x="{f(xc-cw*0.18)}" y="{f(y_col0)}" width="{f(cw*1.36)}" height="12" rx="3" fill="url(#bancoPiedra)" stroke="{INK}" stroke-width="4"/>'
        o += f'<rect x="{f(xc-cw*0.18)}" y="{f(base-esc_h-12)}" width="{f(cw*1.36)}" height="12" rx="3" fill="url(#bancoPiedra)" stroke="{INK}" stroke-width="4"/>'
    # friso
    fcol = col_friso or "url(#bancoPiedra)"
    o += f'<rect x="{f(x0)}" y="{f(y_fr)}" width="{f(w)}" height="{f(friso_h)}" fill="{fcol}" stroke="{INK}" stroke-width="6"/>'
    if rotulo:
        size = min(friso_h * 0.62, w * 0.78 / max(1, len(rotulo)) / 0.62)
        o += T(cx, y_fr + friso_h / 2 + size * 0.36, rotulo, size, INK if not col_friso else "#FFFFFF", font=DISP)
    # frontón
    o += (f'<path d="M {f(x0-w*0.04)} {f(y_fr)} L {f(cx)} {f(y_fr-fr_h)} L {f(x0+w*1.04)} {f(y_fr)} Z" fill="url(#bancoPiedra)" '
          f'stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
    o += brillo(f"M {f(x0+w*0.06)} {f(y_fr-8)} L {f(cx-w*0.04)} {f(y_fr-fr_h+16)}", 5, 0.9)
    if ue:
        o += f'<circle cx="{f(cx)}" cy="{f(y_fr-fr_h*0.38)}" r="{f(fr_h*0.3)}" fill="{AZUL_UE}" stroke="{INK}" stroke-width="4"/>'
        o += estrellas_ue(None, cx, y_fr - fr_h * 0.38, fr_h * 0.2, fr_h * 0.045)
    elif euro:
        o += moneda_euro(None, cx, y_fr - fr_h * 0.38, fr_h * 0.27)
    o += brillo(f"M {f(x0+8)} {f(y_fr+8)} L {f(x0+w*0.5)} {f(y_fr+8)}", 4, 0.6)
    top = y_fr - fr_h
    return Pieza(g(id_, o), {"puerta": (cx, base - esc_h - ph * 0.5), "rotulo": (cx, y_fr + friso_h / 2), "cima": (cx, top),
                             "centro": (cx, (top + base) / 2), "izq": (x0, y_col0 + h_col / 2), "der": (x0 + w, y_col0 + h_col / 2)},
                 (x0 - w * 0.04, top, x0 + w * 1.04, base))


def torre_bce(id_, cx, base, h=520, rotulo="BCE"):
    """Las dos torres de cristal del Banco Central Europeo (Fráncfort), estilizadas: dos prismas facetados unidos por
    pasarelas, con el plinto bajo y un rótulo. Ancho ≈ 0,62*h. .puntos: cima, centro, rotulo. Sub-id {id}_luces (pulse)."""
    w = h * 0.62
    x0 = cx - w / 2
    o = sombra(cx, base + 4, w * 0.62, w * 0.06, 0.3)
    # torre izquierda (más alta) y derecha
    def torre(xa, xb, top, inclina, col):
        pa = [(xa, base - h * 0.08), (xa + inclina, top), (xb, top + h * 0.04), (xb, base - h * 0.08)]
        d = "M " + " L ".join(f"{f(x)} {f(y)}" for x, y in pa) + " Z"
        s = f'<path d="{d}" fill="url(#{col})" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
        # faceta clara
        mid = (xa + xb) / 2 + inclina * 0.3
        s += f'<path d="M {f(xa+inclina)} {f(top)} L {f(mid)} {f(top+h*0.02)} L {f(mid-inclina*0.2)} {f(base-h*0.08)} L {f(xa)} {f(base-h*0.08)} Z" fill="#FFFFFF" opacity="0.18"/>'
        # plantas
        n = 16
        for k in range(1, n):
            y = top + (base - h * 0.08 - top) * k / n
            s += f'<line x1="{f(xa + inclina*(1-k/n) + 3)}" y1="{f(y)}" x2="{f(xb-3)}" y2="{f(y + h*0.04*(1-k/n))}" stroke="#2B4F86" stroke-width="2" opacity="0.55"/>'
        return s
    tl = torre(x0, cx - w * 0.04, base - h, w * 0.08, "bceCristal")
    tr = torre(cx + w * 0.04, x0 + w, base - h * 0.86, -w * 0.06, "bceCristal2")
    o += tr + tl
    # pasarelas entre torres
    for k in range(4):
        y = base - h * (0.25 + k * 0.17)
        o += f'<rect x="{f(cx-w*0.06)}" y="{f(y)}" width="{f(w*0.12)}" height="{f(h*0.035)}" fill="#DCE8F5" stroke="{INK}" stroke-width="4"/>'
    luces = "".join(f'<rect x="{f(x0 + w*(0.12 + 0.11*(k%4)))}" y="{f(base - h*(0.3 + 0.13*(k//4)))}" width="{f(w*0.05)}" height="{f(h*0.02)}" fill="{YEL}" opacity="0.9"/>'
                    for k in range(8) if k % 3 != 1)
    o += g(f"{id_}_luces" if id_ else None, luces)
    # plinto
    o += f'<rect x="{f(x0-w*0.1)}" y="{f(base-h*0.1)}" width="{f(w*1.2)}" height="{f(h*0.1)}" rx="6" fill="url(#bancoPiedra)" stroke="{INK}" stroke-width="6"/>'
    if rotulo:
        o += T(cx, base - h * 0.035, rotulo, h * 0.055, INK, font=DISP)
    o += brillo(f"M {f(x0+w*0.1)} {f(base-h*0.9)} L {f(x0+w*0.06)} {f(base-h*0.2)}", 6, 0.7)
    return Pieza(g(id_, o), {"cima": (cx, base - h), "centro": (cx, base - h / 2), "rotulo": (cx, base - h * 0.05)},
                 (x0 - w * 0.1, base - h, x0 + w * 1.1, base))


def ficha(id_, cx, cy, w=300, h=170, titulo="EURÍBOR", sub=None, col=LIME, fg=INK, rot_=0, size=None):
    """Ficha gruesa de fórmula (pieza que se suma a otra): bloque con canto 3D, título grande y subtítulo pequeño.
    Úsala con un «+» o «=» entre fichas. .puntos: centro, arriba, abajo, izq, der."""
    x0, y0 = cx - w / 2, cy - h / 2
    canto = h * 0.1
    o = sombra_caja(x0, y0, w, h + canto, 22, 10, 14, 0.28)
    o += f'<rect x="{f(x0)}" y="{f(y0+canto)}" width="{f(w)}" height="{f(h)}" rx="22" fill="{degradado(col, 0.45)}" stroke="{INK}" stroke-width="7"/>'
    o += f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" rx="22" fill="{degradado(col, 0.12)}" stroke="{INK}" stroke-width="7"/>'
    o += brillo(f"M {f(x0+22)} {f(y0+18)} L {f(x0+w*0.55)} {f(y0+18)}", 6, 0.7)
    size = size or min(h * 0.32, w * 0.86 / max(1, len(titulo)) / 0.7)
    ty = cy + size * 0.36 - (h * 0.12 if sub else 0)
    o += T(cx, ty, titulo, size, fg, font=DISP)
    if sub:
        o += T(cx, cy + h * 0.32, sub, h * 0.15, fg)
    inner = gt(None, f"rotate({f(rot_)} {f(cx)} {f(cy)})", o) if rot_ else o
    return Pieza(g(id_, inner), {"centro": (cx, cy), "arriba": (cx, y0), "abajo": (cx, y0 + h + canto),
                                 "izq": (x0, cy), "der": (x0 + w, cy)}, (x0, y0, x0 + w, y0 + h + canto))


def recibo_hipoteca(id_, cx, cy, w=360, h=470, titulo="HIPOTECA", banco_txt="TU BANCO", concepto="CUOTA MENSUAL", rot_=0):
    """Carta del banco con la cuota de la hipoteca: membrete con € , líneas de texto y una casilla vacía para la cifra
    (dibuja la cifra aparte en .puntos['cifra'] para poder cambiarla con hide/pop). .puntos: cifra, centro, membrete."""
    x0, y0 = cx - w / 2, cy - h / 2
    o = sombra_caja(x0, y0, w, h, 14, 10, 12, 0.26)
    o += f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" rx="14" fill="url(#reciboG)" stroke="{INK}" stroke-width="7"/>'
    o += f'<path d="M {f(x0)} {f(y0+h*0.2)} L {f(x0)} {f(y0+14)} Q {f(x0)} {f(y0)} {f(x0+14)} {f(y0)} L {f(x0+w-14)} {f(y0)} Q {f(x0+w)} {f(y0)} {f(x0+w)} {f(y0+14)} L {f(x0+w)} {f(y0+h*0.2)} Z" fill="url(#reciboBanda)" stroke="{INK}" stroke-width="7"/>'
    o += moneda_euro(None, x0 + h * 0.1, y0 + h * 0.1, h * 0.065)
    o += T(x0 + h * 0.19, y0 + h * 0.085, banco_txt, h * 0.045, "#FFFFFF", anchor="start")
    o += T(x0 + h * 0.19, y0 + h * 0.15, titulo, h * 0.06, LIME, anchor="start", font=DISP)
    for k in range(4):
        y = y0 + h * (0.29 + k * 0.07)
        o += f'<rect x="{f(x0+w*0.1)}" y="{f(y)}" width="{f(w*(0.8 if k % 2 == 0 else 0.6))}" height="{f(h*0.022)}" rx="4" fill="#C9D0DC"/>'
    o += T(cx, y0 + h * 0.66, concepto, h * 0.045, INK)
    bx, by, bw, bh = x0 + w * 0.1, y0 + h * 0.7, w * 0.8, h * 0.2
    o += f'<rect x="{f(bx)}" y="{f(by)}" width="{f(bw)}" height="{f(bh)}" rx="12" fill="#FFF6CC" stroke="{INK}" stroke-width="5"/>'
    o += brillo(f"M {f(x0+14)} {f(y0+h*0.25)} L {f(x0+14)} {f(y0+h-18)}", 5, 0.9)
    inner = gt(None, f"rotate({f(rot_)} {f(cx)} {f(cy)})", o) if rot_ else o
    return Pieza(g(id_, inner), {"cifra": (cx, by + bh / 2), "centro": (cx, cy), "membrete": (cx, y0 + h * 0.1)}, (x0, y0, x0 + w, y0 + h))


def palanca(id_, cx, base, h=260, texto="TIPOS", col=CORAL):
    """Palanca de mando (subir o bajar algo): caja con ranura y mango vertical en {id}_mango, que se inclina con
    {"effect":"move","rotate":±30,"origin":"bottom"}. Pon flechas de subir o bajar aparte. .puntos: pomo, caja."""
    bw, bh = h * 0.75, h * 0.32
    x0, y0 = cx - bw / 2, base - bh
    o = sombra(cx, base + 4, bw * 0.6, bh * 0.12, 0.28)
    o += f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(bw)}" height="{f(bh)}" rx="16" fill="{degradado("#3A4258", 0.18)}" stroke="{INK}" stroke-width="7"/>'
    o += f'<rect x="{f(cx-bw*0.32)}" y="{f(y0+bh*0.16)}" width="{f(bw*0.64)}" height="{f(bh*0.16)}" rx="6" fill="{INK}"/>'
    if texto:
        o += T(cx, base - bh * 0.22, texto, bh * 0.26, LIME)
    mango = trazo(f"M {f(cx)} {f(y0+bh*0.24)} L {f(cx)} {f(base-h)}", h * 0.06, "#C9D0DC", 7)
    mango += f'<circle cx="{f(cx)}" cy="{f(base-h)}" r="{f(h*0.11)}" fill="{degradado_col(col)}" stroke="{INK}" stroke-width="7"/>'
    mango += brillo_arco(cx, base - h, h * 0.08, 200, 260, h * 0.02, 0.85)
    o = o + g(f"{id_}_mango" if id_ else None, mango) + f'<rect x="{f(cx-bw*0.32)}" y="{f(y0+bh*0.16)}" width="{f(bw*0.64)}" height="{f(bh*0.08)}" rx="4" fill="{INK}"/>'
    return Pieza(g(id_, o), {"pomo": (cx, base - h), "caja": (cx, y0 + bh / 2)}, (x0, base - h - h * 0.11, x0 + bw, base))


def degradado_col(col):
    return degradado(col, 0.3)


# ------------------------------------------------------------------ gasto de campaña (lote8-09-gasto-campana)
registrar_defs(
    lg("sacoTela", [(0, "#F3DFA8"), (0.6, "#D9B76A"), (1, "#B28C45")], 0, 0, 1, 1)
    + lg("topeCinta", [(0, "#FF7A5C"), (1, "#E0391A")])
)


def saco_dinero(id_, cx, base, w=260, texto="€", col_texto="#7A5A1E"):
    """Saco de tela atado con cuerda y símbolo € (o una cifra corta), estilo pegatina. Alto ≈ 1,15·w.
    Sub-ids: {id}_nudo (sway origin bottom), {id}_texto (pulse). .puntos: boca (nudo), centro, base."""
    h = w * 1.15
    top = base - h
    o = sombra(cx + 6, base + 6, w * 0.5, 16, 0.26)
    cuerpo = (f"M {f(cx-w*0.16)} {f(top+h*0.22)} C {f(cx-w*0.62)} {f(top+h*0.36)} {f(cx-w*0.6)} {f(base)} {f(cx)} {f(base)} "
              f"C {f(cx+w*0.6)} {f(base)} {f(cx+w*0.62)} {f(top+h*0.36)} {f(cx+w*0.16)} {f(top+h*0.22)} Z")
    o += f'<path d="{cuerpo}" fill="url(#sacoTela)" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'
    o += f'<path d="M {f(cx+w*0.3)} {f(top+h*0.42)} Q {f(cx+w*0.42)} {f(top+h*0.7)} {f(cx+w*0.22)} {f(base-h*0.06)}" fill="none" stroke="#9C7838" stroke-width="5" opacity="0.6" stroke-linecap="round"/>'
    o += brillo(f"M {f(cx-w*0.3)} {f(top+h*0.45)} Q {f(cx-w*0.36)} {f(top+h*0.65)} {f(cx-w*0.26)} {f(top+h*0.82)}", 8, 0.65)
    nudo = (f'<path d="M {f(cx-w*0.16)} {f(top+h*0.22)} L {f(cx-w*0.26)} {f(top+h*0.04)} Q {f(cx)} {f(top+h*0.12)} {f(cx+w*0.26)} {f(top+h*0.04)} '
            f'L {f(cx+w*0.16)} {f(top+h*0.22)} Z" fill="url(#sacoTela)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
            f'<rect x="{f(cx-w*0.2)}" y="{f(top+h*0.18)}" width="{f(w*0.4)}" height="{f(h*0.06)}" rx="{f(h*0.03)}" fill="{CORAL}" stroke="{INK}" stroke-width="5"/>')
    o += g(f"{id_}_nudo" if id_ else None, nudo)
    fs = w * (0.42 if len(texto) <= 2 else min(0.42, 1.1 / max(1, len(texto)) * 0.95))
    o += g(f"{id_}_texto" if id_ else None, T(cx, top + h * 0.7, texto, fs, col_texto, font=DISP))
    return Pieza(g(id_, o), {"boca": (cx, top + h * 0.12), "centro": (cx, top + h * 0.62), "base": (cx, base)},
                 (cx - w * 0.6, top, cx + w * 0.6, base))


def linea_tope(id_, x0, x1, y, texto="TOPE", col=CORAL):
    """Línea roja discontinua de límite máximo con cartel a la derecha (tope de gasto, máximo legal…).
    Sub-ids: {id}_linea (draw), {id}_cartel (pop). .puntos: izq, der, cartel."""
    o = g(f"{id_}_linea" if id_ else None,
          f'<path d="M {f(x0)} {f(y)} L {f(x1)} {f(y)}" stroke="{INK}" stroke-width="14" stroke-linecap="round"/>'
          f'<path d="M {f(x0)} {f(y)} L {f(x1)} {f(y)}" stroke="{col}" stroke-width="7" stroke-dasharray="26 16" stroke-linecap="round"/>')
    tw = max(120, len(texto) * 22 + 40)
    cx = x1 - tw / 2
    cart = (sombra_caja(cx - tw / 2, y - 76, tw, 56, 12, 6, 8, 0.25)
            + f'<rect x="{f(cx-tw/2)}" y="{f(y-76)}" width="{f(tw)}" height="56" rx="12" fill="url(#topeCinta)" stroke="{INK}" stroke-width="6"/>'
            + T(cx, y - 37, texto, 30, "#FFFFFF", font=DISP))
    o += g(f"{id_}_cartel" if id_ else None, cart)
    return Pieza(g(id_, o), {"izq": (x0, y), "der": (x1, y), "cartel": (cx, y - 48)}, (x0, y - 80, x1, y + 8))

"""Objetos cotidianos: vaso con líquido, cubito de hielo, botella, taza, mesa, ventana, móvil, reloj, bombilla,
casita, etiqueta de precio, bolsa de compra, caja de madera, llave Allen y tornillo.

Sale de: hielo-cruje/hc.py y vaso.py (vaso, cubito, grieta), black-friday/bf.py (móvil, etiqueta de precio, bolsa),
vox/vx.py (reloj, casa), nuevo-partido/np.py (bombilla), ikea/lib.py (caja de madera, llave Allen, tornillo).
"""
import math
import random
from ..base import (INK, LIME, CORAL, YEL, f, g, gt, T, MONO, DISP, shade, trazo, sombra, sombra_caja, brillo, brillo_arco,
                    lg, rg, registrar_defs, degradado, Pieza, poly, smooth)

ICE_EDGE = "#2B6E9E"
registrar_defs(
    lg("iceF", [(0, "#F7FDFF"), (0.55, "#D3F0FC"), (1, "#A8DDF5")], 0, 0, 1, 1)
    + lg("iceT", [(0, "#FFFFFF"), (1, "#DDF4FF")], 0, 0, 1, 1)
    + lg("iceS", [(0, "#B5E3F7"), (1, "#7FC6EA")], 0, 0, 1, 1)
    + rg("cloudR", [(0, "#FFFFFF", 0.95), (0.6, "#FFFFFF", 0.45), (1, "#FFFFFF", 0)])
    + lg("glassB", [(0, "#FFFFFF", 0.55), (1, "#DDEFFA", 0.35)], 0, 0, 1, 0)
    + lg("phoneG", [(0, "#3A4258"), (1, "#151926")], 0, 0, 1, 1) + lg("scrG", [(0, "#FFFFFF"), (1, "#EEF2FA")])
    + lg("bulbG", [(0, "#FFF6B8"), (1, "#FFD23A")])
    + lg("houseW", [(0, "#FFE3C2"), (1, "#F2BF8A")]) + lg("roofG", [(0, "#E86A4A"), (1, "#B8432A")])
    + lg("tagG", [(0, "#FFF8E8"), (1, "#E9D9B8")])
    + lg("wfront", [(0, "#F4DDB8"), (0.55, "#E2BE8A"), (1, "#C99A63")]) + lg("wtop", [(0, "#FBEBCF"), (1, "#EBCB98")])
    + lg("wside", [(0, "#D9AE75"), (1, "#B0824C")])
    + lg("skyWin", [(0, "#9FD8FF"), (1, "#E3F4FF")])
)

LIQUIDOS = {  # superficie clara, cuerpo (3 tonos)
    "agua": ("#D8F1FF", ("#BFE6FF", "#8FD3FF", "#5FB4EA")),
    "refresco": ("#FFE7A3", ("#FFD36B", "#F5A52A", "#D9741A")),
    "cola": ("#C98B5A", ("#8A4A22", "#5A2A10", "#3A1806")),
    "leche": ("#FFFFFF", ("#FFFFFF", "#F4F1EA", "#DCD6C8")),
    "zumo": ("#FFD27A", ("#FFB547", "#FF9A1C", "#E07A00")),
    "cafe": ("#C08A5C", ("#9A5E33", "#6E3E1E", "#4A2810")),
}
for _k, (_s, (_a, _b, _c)) in LIQUIDOS.items():
    registrar_defs(lg(f"liq_{_k}", [(0, _a), (0.5, _b), (1, _c)]), lg(f"liqS_{_k}", [(0, "#FFFFFF"), (1, _s)]))


def cubito(id_, cx, cy, s, ang=0, seed=1, burbujas=4, nube_=True, sw=None):
    """Cubito de hielo en perspectiva. (cx, cy) = centro de la cara frontal; s = lado."""
    rnd = random.Random(seed)
    h = s / 2
    d = s * 0.34
    a = math.radians(ang)
    sw = sw or max(4, s * 0.045)

    def R(x, y):
        return (cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a))
    P = lambda q: "M " + " L ".join(f"{f(x)} {f(y)}" for x, y in q) + " Z"
    F = [R(-h, -h), R(h, -h), R(h, h), R(-h, h)]
    Tp = [R(-h, -h), R(-h + d, -h - d * 0.8), R(h + d, -h - d * 0.8), R(h, -h)]
    S = [R(h, -h), R(h + d, -h - d * 0.8), R(h + d, h - d * 0.8), R(h, h)]
    o = f'<path d="{P(S)}" fill="url(#iceS)" stroke="{ICE_EDGE}" stroke-width="{f(sw)}" stroke-linejoin="round"/>'
    o += f'<path d="{P(Tp)}" fill="url(#iceT)" stroke="{ICE_EDGE}" stroke-width="{f(sw)}" stroke-linejoin="round"/>'
    o += f'<path d="{P(F)}" fill="url(#iceF)" stroke="{ICE_EDGE}" stroke-width="{f(sw)}" stroke-linejoin="round"/>'
    if nube_:
        c = R(0, 0)
        o += f'<ellipse cx="{f(c[0])}" cy="{f(c[1])}" rx="{f(s*0.28)}" ry="{f(s*0.24)}" fill="url(#cloudR)" transform="rotate({f(ang)} {f(c[0])} {f(c[1])})"/>'
    for _ in range(burbujas):
        bx, by = R(rnd.uniform(-h * 0.6, h * 0.6), rnd.uniform(-h * 0.6, h * 0.6))
        o += f'<circle cx="{f(bx)}" cy="{f(by)}" r="{f(rnd.uniform(s*0.025, s*0.045))}" fill="#FFFFFF" stroke="#9CCFEA" stroke-width="{f(max(1.5, s*0.01))}"/>'
    x1, y1 = R(-h + s * 0.12, -h + s * 0.14)
    x2, y2 = R(-h + s * 0.12, h - s * 0.3)
    o += f'<path d="M {f(x1)} {f(y1)} L {f(x2)} {f(y2)}" stroke="#FFFFFF" stroke-width="{f(s*0.07)}" stroke-linecap="round"/>'
    return g(id_, o)


def grieta(id_, p0, p1, n=5, amp=10, seed=3, w=6, col=ICE_EDGE):
    """Grieta en zigzag de p0 a p1 con brillo blanco (hielo, cristal, pared). Anímala con "draw"."""
    rnd = random.Random(seed)
    (x0, y0), (x1, y1) = p0, p1
    L = math.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    nx, ny = -uy, ux
    P = [(x0, y0)]
    for i in range(1, n):
        t = i / n
        k = amp * (1 if i % 2 else -1) * rnd.uniform(0.6, 1.2)
        P.append((x0 + ux * L * t + nx * k, y0 + uy * L * t + ny * k))
    P.append((x1, y1))
    d = poly(P)
    return g(id_, f'<path d="{d}" fill="none" stroke="#FFFFFF" stroke-width="{f(w*2.2)}" stroke-linecap="round" stroke-linejoin="round" opacity="0.9"/>'
             f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{f(w)}" stroke-linecap="round" stroke-linejoin="round"/>')


def vaso(id_, cx, base, alto=420, ancho=300, nivel=0.6, liquido="agua", cubitos=0, burbujas=8, seed=5):
    """Vaso de cristal troncocónico con líquido (nivel 0-1) y cubitos opcionales flotando.
    Ids internos: id_+'_liquido', id_+'_burbujas', id_+'_cubo<i>'. Devuelve Pieza con .puntos['superficie'] y ['borde']."""
    RT, RB = ancho / 2, ancho / 2 * 0.83
    EY = RT * 0.16
    TOP, BOT = base - alto, base
    surf = BOT - alto * nivel * 0.92

    def rx(y):
        return RT + (RB - RT) * (y - TOP) / (BOT - TOP)
    rs = rx(surf)
    eys = EY * rs / RT
    o = sombra(cx + 16, BOT + 8, RB + 50, 20, 0.3)
    body = f"M {f(cx-RT)} {f(TOP)} L {f(cx-RB)} {f(BOT)} A {f(RB)} {f(EY*RB/RT)} 0 0 0 {f(cx+RB)} {f(BOT)} L {f(cx+RT)} {f(TOP)}"
    o += f'<path d="{body} A {f(RT)} {f(EY)} 0 0 0 {f(cx-RT)} {f(TOP)} Z" fill="url(#glassB)"/>'
    o += f'<ellipse cx="{f(cx)}" cy="{f(TOP)}" rx="{f(RT)}" ry="{f(EY)}" fill="#EAF6FF" fill-opacity="0.55" stroke="{INK}" stroke-width="6"/>'
    if nivel > 0:
        liq = (f"M {f(cx-rs)} {f(surf)} L {f(cx-RB+8)} {f(BOT-6)} A {f(RB-8)} {f(EY*(RB-8)/RT)} 0 0 0 {f(cx+RB-8)} {f(BOT-6)} "
               f"L {f(cx+rs)} {f(surf)} A {f(rs)} {f(eys)} 0 0 1 {f(cx-rs)} {f(surf)} Z")
        lq = f'<path d="{liq}" fill="url(#liq_{liquido})"/>'
        lq += f'<ellipse cx="{f(cx)}" cy="{f(surf)}" rx="{f(rs-4)}" ry="{f(eys)}" fill="url(#liqS_{liquido})" stroke="{INK}" stroke-width="5"/>'
        o += g(f"{id_}_liquido" if id_ else None, lq)
        rnd = random.Random(seed)
        bub = "".join(f'<circle cx="{f(cx + rnd.uniform(-RB*0.75, RB*0.75))}" cy="{f(rnd.uniform(surf + 40, BOT - 30))}" r="{f(rnd.uniform(4, 9))}" fill="#FFFFFF" fill-opacity="0.8" stroke="{shade(LIQUIDOS[liquido][1][2], -0.1)}" stroke-width="2.5"/>' for _ in range(burbujas))
        o += g(f"{id_}_burbujas" if id_ else None, bub)
        for i in range(cubitos):
            s = ancho * (0.42 - 0.06 * i)
            ccx = cx + (-0.22 + 0.44 * (i % 2)) * RT * (1 if i < 2 else 0.2)
            o += cubito(f"{id_}_cubo{i}" if id_ else None, ccx, surf - s * 0.05 - (i // 2) * s * 0.3, s, [-12, 11, 28][i % 3], seed=i + 1, burbujas=3)
        o += f'<path d="{liq}" fill="{LIQUIDOS[liquido][1][1]}" opacity="0.25"/>' if cubitos else ""
    o += f'<path d="{body}" fill="none" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'
    o += f'<path d="M {f(cx-RT)} {f(TOP)} A {f(RT)} {f(EY)} 0 0 0 {f(cx+RT)} {f(TOP)}" fill="none" stroke="{INK}" stroke-width="8"/>'
    o += brillo(f"M {f(cx-RT+RT*0.22)} {f(TOP+alto*0.1)} L {f(cx-RB+RB*0.18)} {f(BOT-alto*0.1)}", RT * 0.1, 0.75)
    o += brillo(f"M {f(cx-RT+RT*0.46)} {f(TOP+alto*0.14)} L {f(cx-RB+RB*0.38)} {f(BOT-alto*0.35)}", RT * 0.04, 0.6)
    o += brillo(f"M {f(cx+RT-RT*0.2)} {f(TOP+alto*0.12)} L {f(cx+RB-RB*0.16)} {f(BOT-alto*0.14)}", RT * 0.04, 0.45)
    return Pieza(g(id_, o), {"superficie": (cx, surf), "borde": (cx, TOP)}, (cx - RT, TOP - EY, cx + RT, BOT + EY))


def botella(id_, cx, base, alto=420, col="#7FD48A", etiqueta_col=CORAL, texto=""):
    """Botella de cristal con etiqueta y tapón."""
    w = alto * 0.3
    neck = w * 0.32
    x0 = cx - w / 2
    yb, ys, yn, yt = base, base - alto * 0.62, base - alto * 0.8, base - alto
    d = (f"M {f(x0)} {f(yb-14)} L {f(x0)} {f(ys)} C {f(x0)} {f(ys-alto*0.12)}, {f(cx-neck)} {f(yn+alto*0.04)}, {f(cx-neck)} {f(yn)} "
         f"L {f(cx-neck)} {f(yt+12)} L {f(cx+neck)} {f(yt+12)} L {f(cx+neck)} {f(yn)} C {f(cx+neck)} {f(yn+alto*0.04)}, {f(x0+w)} {f(ys-alto*0.12)}, {f(x0+w)} {f(ys)} "
         f"L {f(x0+w)} {f(yb-14)} Q {f(x0+w)} {f(yb)} {f(x0+w-14)} {f(yb)} L {f(x0+14)} {f(yb)} Q {f(x0)} {f(yb)} {f(x0)} {f(yb-14)} Z")
    o = sombra(cx + 8, base + 4, w * 0.75, 12, 0.28)
    o += f'<path d="{d}" fill="{degradado(col, 0.3, "h")}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
    o += f'<rect x="{f(x0+2)}" y="{f(ys+alto*0.08)}" width="{f(w-4)}" height="{f(alto*0.24)}" fill="{degradado(etiqueta_col, 0.15)}" stroke="{INK}" stroke-width="5"/>'
    if texto:
        o += T(cx, ys + alto * 0.2 + alto * 0.03, texto, min(alto * 0.07, w * 0.8 / max(1, len(texto) * 0.85)), "#FFFFFF", font=DISP)
    o += f'<rect x="{f(cx-neck-6)}" y="{f(yt)}" width="{f(neck*2+12)}" height="{f(alto*0.06)}" rx="5" fill="{degradado(CORAL, 0.2)}" stroke="{INK}" stroke-width="6"/>'
    o += brillo(f"M {f(x0+w*0.18)} {f(ys)} L {f(x0+w*0.18)} {f(yb-26)}", w * 0.1, 0.65)
    o += brillo(f"M {f(cx-neck*0.45)} {f(yn)} L {f(cx-neck*0.45)} {f(yt+alto*0.09)}", w * 0.06, 0.6)
    return g(id_, o)


def taza(id_, cx, base, w=200, col="#FFFFFF", liquido="cafe", vapor=True):
    """Taza con asa y líquido humeante (vapor en id_+'_vapor': anímalo con float/drift)."""
    h = w * 0.85
    x0, top = cx - w / 2, base - h
    o = sombra(cx + 10, base + 6, w * 0.65, 14, 0.25)
    o += trazo(f"M {f(x0+w-6)} {f(top+h*0.25)} C {f(x0+w+w*0.35)} {f(top+h*0.2)}, {f(x0+w+w*0.35)} {f(top+h*0.75)}, {f(x0+w-10)} {f(top+h*0.7)}", w * 0.1, shade(col, -0.06), 12)
    d = f"M {f(x0)} {f(top)} L {f(x0+w)} {f(top)} L {f(x0+w*0.92)} {f(base-18)} Q {f(x0+w*0.9)} {f(base)} {f(x0+w*0.75)} {f(base)} L {f(x0+w*0.25)} {f(base)} Q {f(x0+w*0.1)} {f(base)} {f(x0+w*0.08)} {f(base-18)} Z"
    o += f'<path d="{d}" fill="{degradado(col, 0.12, "h")}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
    o += f'<ellipse cx="{f(cx)}" cy="{f(top)}" rx="{f(w/2)}" ry="{f(w*0.1)}" fill="{shade(col,-0.1)}" stroke="{INK}" stroke-width="6"/>'
    o += f'<ellipse cx="{f(cx)}" cy="{f(top+3)}" rx="{f(w/2-12)}" ry="{f(w*0.07)}" fill="url(#liq_{liquido})"/>'
    o += brillo(f"M {f(x0+w*0.14)} {f(top+h*0.2)} L {f(x0+w*0.2)} {f(base-26)}", w * 0.06, 0.8)
    if vapor:
        v = "".join(trazo(f"M {f(cx+dx)} {f(top-14)} c -18 -22 18 -40 0 -62 c -18 -22 18 -40 0 -62", 7, "#FFFFFF", 6) for dx in (-w * 0.18, w * 0.12))
        o += g(f"{id_}_vapor" if id_ else None, f'<g opacity="0.85">{v}</g>')
    return g(id_, o)


def mesa(id_, cx, y_tablero, w=700, alto=260, grosor=34, col="#C98B55"):
    """Mesa de madera en vista frontal ligeramente cenital (tablero con canto y dos patas)."""
    x0 = cx - w / 2
    prof = grosor * 1.6
    o = sombra(cx, y_tablero + alto + 6, w * 0.55, 18, 0.25)
    for k in (0.08, 0.92):
        lx = x0 + w * k - 18
        o += f'<rect x="{f(lx)}" y="{f(y_tablero)}" width="36" height="{f(alto)}" rx="8" fill="{degradado(shade(col,-0.15), 0.2, "h")}" stroke="{INK}" stroke-width="6"/>'
    o += f'<path d="M {f(x0+30)} {f(y_tablero-prof)} L {f(x0+w-30)} {f(y_tablero-prof)} L {f(x0+w)} {f(y_tablero)} L {f(x0)} {f(y_tablero)} Z" fill="{degradado(shade(col,0.2), 0.12)}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
    o += "".join(f'<path d="M {f(x0+w*0.086+i*w*0.22)} {f(y_tablero-prof*0.6)} C {f(x0+w*0.17+i*w*0.22)} {f(y_tablero-prof*0.7)}, {f(x0+w*0.26+i*w*0.22)} {f(y_tablero-prof*0.45)}, {f(x0+w*0.34+i*w*0.22)} {f(y_tablero-prof*0.55)}" fill="none" stroke="{shade(col,-0.25)}" stroke-width="3" opacity="0.5"/>' for i in range(4))
    o += f'<rect x="{f(x0)}" y="{f(y_tablero)}" width="{f(w)}" height="{f(grosor)}" rx="6" fill="{degradado(col, 0.2)}" stroke="{INK}" stroke-width="7"/>'
    o += brillo(f"M {f(x0+40)} {f(y_tablero-prof+8)} L {f(x0+w-40)} {f(y_tablero-prof+8)}", 4, 0.6)
    return Pieza(g(id_, o), {"superficie": (cx, y_tablero - prof * 0.5)}, (x0, y_tablero - prof, x0 + w, y_tablero + alto))


def ventana(id_, cx, cy, w=320, h=380, cielo="url(#skyWin)", cortinas=True, col_marco="#FFFFFF", noche=False):
    """Ventana con marco de cuatro hojas, cielo y nubecita; cortinas opcionales."""
    x, y = cx - w / 2, cy - h / 2
    o = sombra_caja(x, y, w, h, 10, 10, 12, 0.2)
    sky = "url(#nocheWin)" if noche else cielo
    if noche:
        registrar_defs(lg("nocheWin", [(0, "#1B2550"), (1, "#3B4E8C")]))
    o += f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="8" fill="{sky}" stroke="{INK}" stroke-width="7"/>'
    if noche:
        o += f'<circle cx="{f(x+w*0.7)}" cy="{f(y+h*0.25)}" r="{f(w*0.1)}" fill="#FFF6C8" stroke="{INK}" stroke-width="4"/>'
        o += "".join(f'<circle cx="{f(x+w*a)}" cy="{f(y+h*b)}" r="3" fill="#FFFFFF"/>' for a, b in ((0.2, 0.2), (0.4, 0.35), (0.3, 0.6), (0.8, 0.6)))
    else:
        o += "".join(f'<circle cx="{f(x+w*a)}" cy="{f(y+h*b)}" r="{f(w*r)}" fill="#FFFFFF" opacity="0.9"/>' for a, b, r in ((0.3, 0.3, 0.07), (0.38, 0.27, 0.09), (0.46, 0.31, 0.06)))
    o += brillo(f"M {f(x+w*0.12)} {f(y+h*0.6)} L {f(x+w*0.32)} {f(y+h*0.4)}", 6, 0.7)
    o += f'<path d="M {f(cx)} {f(y)} L {f(cx)} {f(y+h)} M {f(x)} {f(cy)} L {f(x+w)} {f(cy)}" stroke="{INK}" stroke-width="16"/>'
    o += f'<path d="M {f(cx)} {f(y)} L {f(cx)} {f(y+h)} M {f(x)} {f(cy)} L {f(x+w)} {f(cy)}" stroke="{col_marco}" stroke-width="9"/>'
    o += f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="8" fill="none" stroke="{col_marco}" stroke-width="6"/>'
    o += f'<rect x="{f(x-4)}" y="{f(y-4)}" width="{f(w+8)}" height="{f(h+8)}" rx="10" fill="none" stroke="{INK}" stroke-width="5"/>'
    o += f'<rect x="{f(x-24)}" y="{f(y+h)}" width="{f(w+48)}" height="22" rx="6" fill="{degradado("#F4F6FA", 0.1)}" stroke="{INK}" stroke-width="6"/>'
    if cortinas:
        for k in (-1, 1):
            xx = x - 30 if k < 0 else x + w + 30
            d = f"M {f(xx)} {f(y-40)} L {f(xx - k*w*0.32)} {f(y-40)} C {f(xx - k*w*0.18)} {f(y+h*0.4)}, {f(xx - k*w*0.36)} {f(y+h*0.8)}, {f(xx - k*w*0.22)} {f(y+h+30)} L {f(xx)} {f(y+h+30)} Z"
            o += f'<path d="{d}" fill="{degradado(CORAL, 0.2, "h")}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
            o += f'<path d="M {f(xx - k*w*0.1)} {f(y-30)} C {f(xx - k*w*0.04)} {f(y+h*0.4)}, {f(xx - k*w*0.14)} {f(y+h*0.8)}, {f(xx - k*w*0.08)} {f(y+h+20)}" fill="none" stroke="{shade(CORAL,-0.3)}" stroke-width="4" opacity="0.7"/>'
        o += f'<rect x="{f(x-60)}" y="{f(y-52)}" width="{f(w+120)}" height="16" rx="8" fill="#9AA3B5" stroke="{INK}" stroke-width="5"/>'
    return g(id_, o)


def movil(id_, cx, cy, w=400, pantalla="", rot_=0):
    """Smartphone (marco oscuro, isla, botón lateral). `pantalla` = SVG que se recorta dentro de la pantalla;
    la pantalla va de .puntos['pantalla'] = (x0, y0, x1, y1)."""
    h = w * 1.95
    PX, PY = cx - w / 2, cy - h / 2
    SX, SY, SW_, SH = PX + w * 0.055, PY + w * 0.065, w * 0.89, h - w * 0.13
    cid = f"pant_{id_ or 'movil'}"
    o = f'<rect x="{f(PX+16)}" y="{f(PY+20)}" width="{f(w)}" height="{f(h)}" rx="{f(w*0.14)}" fill="{INK}" opacity="0.25"/>'
    o += f'<rect x="{f(PX)}" y="{f(PY)}" width="{f(w)}" height="{f(h)}" rx="{f(w*0.14)}" fill="url(#phoneG)" stroke="{INK}" stroke-width="8"/>'
    o += f'<rect x="{f(SX)}" y="{f(SY)}" width="{f(SW_)}" height="{f(SH)}" rx="{f(w*0.095)}" fill="url(#scrG)"/>'
    if pantalla:
        o += f'<clipPath id="{cid}"><rect x="{f(SX)}" y="{f(SY)}" width="{f(SW_)}" height="{f(SH)}" rx="{f(w*0.095)}"/></clipPath><g clip-path="url(#{cid})">{pantalla}</g>'
    o += f'<rect x="{f(cx-w*0.125)}" y="{f(SY+w*0.03)}" width="{f(w*0.25)}" height="{f(w*0.06)}" rx="{f(w*0.03)}" fill="{INK}"/>'
    o += f'<path d="M {f(PX+w+2)} {f(PY+h*0.18)} L {f(PX+w+2)} {f(PY+h*0.28)}" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>'
    o += brillo(f"M {f(PX+10)} {f(PY+h*0.1)} L {f(PX+10)} {f(PY+h*0.32)}", 5, 0.6, "#7A86A6")
    o += f'<path d="M {f(SX+SW_*0.7)} {f(SY)} L {f(SX+SW_)} {f(SY+SH*0.18)} L {f(SX+SW_)} {f(SY)} Z" fill="#FFFFFF" opacity="0.18"/>'
    return Pieza(gt(id_, f"rotate({f(rot_)} {f(cx)} {f(cy)})", o), {"pantalla": (SX, SY, SX + SW_, SY + SH)}, (PX, PY, PX + w, PY + h))


def reloj(id_, cx, cy, r=120, hora=10, minuto=10, col_marco=CORAL, texto=None):
    """Reloj de pared. Agujas en id_+'_horaria' y id_+'_minutero' (anímalas con spin, origin bottom… o move rotate)."""
    o = f'<circle cx="{f(cx+r*0.06)}" cy="{f(cy+r*0.08)}" r="{f(r*1.12)}" fill="{INK}" opacity="0.22"/>'
    o += f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r*1.12)}" fill="{degradado(col_marco, 0.25)}" stroke="{INK}" stroke-width="7"/>'
    o += f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/>'
    for i in range(12):
        a = math.radians(i * 30)
        r1 = r * (0.78 if i % 3 == 0 else 0.85)
        o += f'<path d="M {f(cx+r1*math.sin(a))} {f(cy-r1*math.cos(a))} L {f(cx+r*0.92*math.sin(a))} {f(cy-r*0.92*math.cos(a))}" stroke="{INK}" stroke-width="{6 if i % 3 == 0 else 3.5}" stroke-linecap="round"/>'
    if texto:
        o += T(cx, cy + r * 0.45, texto, r * 0.2, CORAL, font=DISP)
    ah = math.radians((hora % 12) * 30 + minuto * 0.5)
    am = math.radians(minuto * 6)
    # las agujas se dibujan verticales y se giran (así su caja tiene la base en el centro del reloj)
    o += g(f"{id_}_horaria" if id_ else None, f'<g transform="rotate({f(math.degrees(ah))} {f(cx)} {f(cy)})">' + trazo(f"M {f(cx)} {f(cy)} L {f(cx)} {f(cy-r*0.5)}", r * 0.07, INK, 0) + "</g>")
    o += g(f"{id_}_minutero" if id_ else None, f'<g transform="rotate({f(math.degrees(am))} {f(cx)} {f(cy)})">' + trazo(f"M {f(cx)} {f(cy)} L {f(cx)} {f(cy-r*0.75)}", r * 0.045, INK, 0) + "</g>")
    o += f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r*0.07)}" fill="{CORAL}" stroke="{INK}" stroke-width="3"/>'
    o += brillo_arco(cx, cy, r * 0.86, 200, 250, r * 0.05, 0.6)
    return g(id_, o)


def bombilla(id_, cx, cy, s=150, encendida=True):
    """Bombilla (idea). Con encendida=True añade halo detrás (los rayos: base.rayos)."""
    o = f'<circle cx="{f(cx)}" cy="{f(cy-s*0.15)}" r="{f(s*0.9)}" fill="url(#resplandorY)"/>' if encendida else ""
    fill = "url(#bulbG)" if encendida else "#E9EDF3"
    o += (f'<path d="M {f(cx-s*0.5)} {f(cy-s*0.1)} C {f(cx-s*0.5)} {f(cy-s*0.85)}, {f(cx+s*0.5)} {f(cy-s*0.85)}, {f(cx+s*0.5)} {f(cy-s*0.1)} C {f(cx+s*0.5)} {f(cy+s*0.2)}, {f(cx+s*0.22)} {f(cy+s*0.3)}, {f(cx+s*0.22)} {f(cy+s*0.5)} L {f(cx-s*0.22)} {f(cy+s*0.5)} C {f(cx-s*0.22)} {f(cy+s*0.3)}, {f(cx-s*0.5)} {f(cy+s*0.2)}, {f(cx-s*0.5)} {f(cy-s*0.1)} Z" fill="{fill}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
          f'<rect x="{f(cx-s*0.25)}" y="{f(cy+s*0.5)}" width="{f(s*0.5)}" height="{f(s*0.3)}" rx="6" fill="#9AA3B5" stroke="{INK}" stroke-width="6"/>'
          f'<path d="M {f(cx-s*0.25)} {f(cy+s*0.62)} L {f(cx+s*0.25)} {f(cy+s*0.62)}" stroke="{INK}" stroke-width="4"/>'
          f'<path d="M {f(cx-s*0.12)} {f(cy+s*0.45)} L {f(cx-s*0.12)} {f(cy+s*0.05)} L {f(cx)} {f(cy+s*0.18)} L {f(cx+s*0.12)} {f(cy+s*0.05)} L {f(cx+s*0.12)} {f(cy+s*0.45)}" fill="none" stroke="#C08A00" stroke-width="5" stroke-linejoin="round"/>'
          + brillo(f"M {f(cx-s*0.32)} {f(cy-s*0.3)} C {f(cx-s*0.3)} {f(cy-s*0.5)}, {f(cx-s*0.15)} {f(cy-s*0.6)}, {f(cx)} {f(cy-s*0.62)}", 8, 0.85))
    return g(id_, o)


def casita(id_, cx, base, w=200, col_pared="url(#houseW)", col_tejado="url(#roofG)"):
    """Casa sencilla (icono de vivienda, barrio, hogar)."""
    h = w * 0.62
    x = cx - w / 2
    o = f'<rect x="{f(x+6)}" y="{f(base-h+8)}" width="{f(w)}" height="{f(h)}" fill="{INK}" opacity="0.2"/>'
    o += f'<rect x="{f(x)}" y="{f(base-h)}" width="{f(w)}" height="{f(h)}" fill="{col_pared}" stroke="{INK}" stroke-width="5"/>'
    o += f'<path d="M {f(x-w*0.12)} {f(base-h+4)} L {f(cx)} {f(base-h-w*0.42)} L {f(x+w*1.12)} {f(base-h+4)} Z" fill="{col_tejado}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    o += f'<rect x="{f(cx-w*0.12)}" y="{f(base-h*0.62)}" width="{f(w*0.24)}" height="{f(h*0.62)}" rx="4" fill="#8A5A31" stroke="{INK}" stroke-width="4"/>'
    o += f'<circle cx="{f(cx+w*0.07)}" cy="{f(base-h*0.3)}" r="3.5" fill="{YEL}"/>'
    for k in (-1, 1):
        o += f'<rect x="{f(cx+k*w*0.32-w*0.09)}" y="{f(base-h*0.75)}" width="{f(w*0.18)}" height="{f(w*0.16)}" rx="3" fill="#BFE6FF" stroke="{INK}" stroke-width="4"/>'
    return g(id_, o)


def etiqueta_precio(id_, cx, cy, w=360, h=180, texto="50 €", rot_=-5, tachado=None):
    """Etiqueta de cartón con agujero (rebajas, precios). tachado = precio antiguo tachado encima."""
    x0, y0 = cx - w / 2, cy - h / 2
    n = w * 0.19
    path = (f"M {f(x0+n)} {f(y0)} L {f(x0+w-14)} {f(y0)} Q {f(x0+w)} {f(y0)} {f(x0+w)} {f(y0+14)} L {f(x0+w)} {f(y0+h-14)} "
            f"Q {f(x0+w)} {f(y0+h)} {f(x0+w-14)} {f(y0+h)} L {f(x0+n)} {f(y0+h)} L {f(x0)} {f(cy+h*0.2)} L {f(x0)} {f(cy-h*0.2)} Z")
    s = f'<path d="{path}" transform="translate(14 18)" fill="{INK}" opacity="0.28"/>'
    s += f'<path d="{path}" fill="url(#tagG)" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'
    s += brillo(f"M {f(x0+n+14)} {f(y0+14)} L {f(x0+w-24)} {f(y0+14)}", 6, 0.7)
    s += f'<circle cx="{f(x0+n*0.68)}" cy="{f(cy)}" r="{f(h*0.1)}" fill="#1A1E2C" stroke="{INK}" stroke-width="6"/>'
    tx = x0 + n + (w - n) / 2
    fs = min(h * 0.38, (w - n) * 0.9 / (len(texto) * 0.86))
    if tachado:
        s += T(tx, cy - h * 0.12, tachado, fs * 0.5, "#8A8F9E", font=DISP)
        s += f'<path d="M {f(tx-fs*len(tachado)*0.25)} {f(cy-h*0.12-fs*0.17)} L {f(tx+fs*len(tachado)*0.25)} {f(cy-h*0.12-fs*0.17)}" stroke="{CORAL}" stroke-width="6" stroke-linecap="round"/>'
        s += T(tx, cy + h * 0.3, texto, fs * 0.9, CORAL, font=DISP)
    else:
        s += T(tx, cy + fs * 0.36, texto, fs, INK, font=DISP)
    return gt(id_, f"rotate({f(rot_)} {f(cx)} {f(cy)})", s)


def bolsa(id_, cx, base, w=220, h=240, col=CORAL, texto=""):
    """Bolsa de la compra con asas."""
    x0, y0 = cx - w / 2, base - h
    s = sombra(cx + 8, base + 6, w * 0.58, 14, 0.25)
    asa = f"M {f(cx-w*0.22)} {f(y0+6)} Q {f(cx-w*0.22)} {f(y0-h*0.32)} {f(cx)} {f(y0-h*0.32)} Q {f(cx+w*0.22)} {f(y0-h*0.32)} {f(cx+w*0.22)} {f(y0+6)}"
    s += trazo(asa, 5, "#E9D9B8", 7)
    s += f'<path d="M {f(x0)} {f(y0)} L {f(x0+w)} {f(y0)} L {f(x0+w-10)} {f(base)} L {f(x0+10)} {f(base)} Z" fill="{degradado(col, 0.2)}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
    s += f'<path d="M {f(x0+w*0.7)} {f(y0+4)} L {f(x0+w-14)} {f(base-4)} L {f(x0+w-4)} {f(y0+4)} Z" fill="{shade(col,-0.3)}" opacity="0.5"/>'
    s += brillo(f"M {f(x0+16)} {f(y0+16)} L {f(x0+22)} {f(base-24)}", 6, 0.5)
    if texto:
        s += T(cx, y0 + h * 0.58, texto, min(30, w * 0.8 / max(1, len(texto) * 0.86)), "#FFFFFF", font=DISP)
    return g(id_, s)


def caja_madera(id_, x0, yb, w=250, h=190, dx=46, dy=-38, tornillos=True, seed=0):
    """Caja/mueble de madera clara en perspectiva (estilo IKEA). (x0, yb) = esquina inferior izquierda del frente."""
    rnd = random.Random(seed)
    F = [(x0, yb - h), (x0 + w, yb - h), (x0 + w, yb), (x0, yb)]
    Tp = [(x0, yb - h), (x0 + dx, yb - h + dy), (x0 + w + dx, yb - h + dy), (x0 + w, yb - h)]
    S = [(x0 + w, yb - h), (x0 + w + dx, yb - h + dy), (x0 + w + dx, yb + dy), (x0 + w, yb)]
    o = sombra(x0 + w / 2 + dx / 2, yb + 6, w * 0.62, 14, 0.25)
    o += f'<path d="{poly(S, True)}" fill="url(#wside)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
    o += f'<path d="{poly(Tp, True)}" fill="url(#wtop)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
    o += f'<path d="{poly(F, True)}" fill="url(#wfront)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
    for i in range(4):
        yy = yb - h + h * (0.2 + 0.2 * i) + rnd.uniform(-6, 6)
        o += f'<path d="M {f(x0+12)} {f(yy)} C {f(x0+w*0.3)} {f(yy-8)}, {f(x0+w*0.6)} {f(yy+8)}, {f(x0+w-12)} {f(yy)}" fill="none" stroke="#B88A55" stroke-width="2.5" opacity="0.6"/>'
    if tornillos:
        for px, py in ((x0 + 18, yb - h + 18), (x0 + w - 18, yb - h + 18), (x0 + 18, yb - 18), (x0 + w - 18, yb - 18)):
            o += f'<circle cx="{f(px)}" cy="{f(py)}" r="6" fill="#C9CED8" stroke="{INK}" stroke-width="3"/><path d="M {f(px-3.5)} {f(py)} L {f(px+3.5)} {f(py)}" stroke="{INK}" stroke-width="2"/>'
    o += brillo(f"M {f(x0+10)} {f(yb-h+10)} L {f(x0+w-10)} {f(yb-h+10)}", 4, 0.6)
    return g(id_, o)


def llave_allen(id_, x, y, s=1.0, ang=0):
    """Llave Allen (hexagonal) en L."""
    b = trazo(f"M 0 0 L 0 {f(-90*s)} Q 0 {f(-110*s)} {f(20*s)} {f(-110*s)} L {f(50*s)} {f(-110*s)}", 13 * s, degradado("#9AA6BC", 0.3, "h"), 7)
    return gt(id_, f"translate({f(x)} {f(y)}) rotate({f(ang)})", b + brillo(f"M {f(-3*s)} {f(-10*s)} L {f(-3*s)} {f(-80*s)}", 3, 0.7))


def tornillo(id_, x, y, s=1.0, ang=0):
    """Tornillo con cabeza en cruz."""
    b = f'<rect x="{f(-7*s)}" y="0" width="{f(14*s)}" height="{f(60*s)}" rx="{f(3*s)}" fill="{degradado("#C9CED8", 0.2, "h")}" stroke="{INK}" stroke-width="4"/>'
    b += "".join(f'<path d="M {f(-7*s)} {f(i*10*s+8*s)} L {f(7*s)} {f(i*10*s+14*s)}" stroke="{INK}" stroke-width="2.5"/>' for i in range(5))
    b += f'<ellipse cx="0" cy="0" rx="{f(16*s)}" ry="{f(8*s)}" fill="#E4E7EF" stroke="{INK}" stroke-width="4"/>'
    b += f'<path d="M {f(-8*s)} 0 L {f(8*s)} 0 M 0 {f(-4*s)} L 0 {f(4*s)}" stroke="{INK}" stroke-width="3"/>'
    return gt(id_, f"translate({f(x)} {f(y)}) rotate({f(ang)})", b)


# ------------------------------------------------------------------ añadidos de bostezo (lote7-03)
def sofa(id_, cx, base, w=560, asiento=150, col="#5B7FD6", respaldo=210):
    """Sofá de frente. `asiento` = altura del cojín sobre el suelo (para persona sentada a escala e: 128*e).
    Devuelve Pieza con .puntos['asiento'] = (cx, y del cojín) y ['izq'], ['der'] (centros de las dos plazas)."""
    sy = base - asiento
    o = sombra(cx, base + 2, w * 0.55, 18, 0.2)
    # respaldo
    o += f'<rect x="{f(cx-w*0.44)}" y="{f(sy-respaldo)}" width="{f(w*0.88)}" height="{f(respaldo+20)}" rx="34" fill="{degradado(col, 0.25)}" stroke="{INK}" stroke-width="7"/>'
    o += "".join(f'<rect x="{f(cx-w*0.42 + i*w*0.42 + 6)}" y="{f(sy-respaldo+14)}" width="{f(w*0.42-12)}" height="{f(respaldo-40)}" rx="26" fill="{degradado(shade(col, 0.12), 0.2)}" stroke="{INK}" stroke-width="5"/>' for i in range(2))
    o += brillo(f"M {f(cx-w*0.36)} {f(sy-respaldo+26)} L {f(cx-w*0.1)} {f(sy-respaldo+26)}", 6, 0.5)
    # base y cojines del asiento
    o += f'<rect x="{f(cx-w*0.46)}" y="{f(sy-8)}" width="{f(w*0.92)}" height="{f(asiento-22)}" rx="18" fill="{degradado(shade(col, -0.15), 0.2)}" stroke="{INK}" stroke-width="7"/>'
    o += "".join(f'<rect x="{f(cx-w*0.42 + i*w*0.42 + 4)}" y="{f(sy-24)}" width="{f(w*0.42-8)}" height="46" rx="18" fill="{degradado(shade(col, 0.2), 0.2)}" stroke="{INK}" stroke-width="5"/>' for i in range(2))
    # brazos
    for k in (-1, 1):
        x = cx + k * w * 0.46
        o += f'<rect x="{f(x-40)}" y="{f(sy-90)}" width="80" height="{f(asiento+70)}" rx="30" fill="{degradado(col, 0.25, "h")}" stroke="{INK}" stroke-width="7"/>'
        o += brillo(f"M {f(x-20)} {f(sy-74)} L {f(x-20)} {f(sy-10)}", 5, 0.45)
    # patas
    for k in (-1, 1):
        o += f'<rect x="{f(cx+k*w*0.42-9)}" y="{f(base-16)}" width="18" height="16" rx="4" fill="#5A3A22" stroke="{INK}" stroke-width="4"/>'
    return Pieza(g(id_, o), {"asiento": (cx, sy), "izq": (cx - w * 0.21, sy), "der": (cx + w * 0.21, sy)},
                 (cx - w * 0.5 - 40, sy - respaldo, cx + w * 0.5 + 40, base))


def banco(id_, cx, base, w=420, asiento=128, col="#C98B55", hierro="#3A4256"):
    """Banco de parque de listones con patas de hierro. .puntos['asiento'] = (cx, y del asiento)."""
    sy = base - asiento
    o = sombra(cx, base + 2, w * 0.55, 16, 0.2)
    for k in (-1, 1):  # patas y apoyabrazos de hierro
        x = cx + k * w * 0.42
        o += trazo(f"M {f(x)} {f(base)} L {f(x)} {f(sy-150)}", 12, hierro, 5)
        o += trazo(f"M {f(x)} {f(sy-60)} Q {f(x + k*30)} {f(sy-64)} {f(x + k*36)} {f(sy-36)} L {f(x + k*30)} {f(base)}", 10, hierro, 5)
    for i in range(3):  # respaldo
        y = sy - 150 + i * 40
        o += f'<rect x="{f(cx-w*0.5)}" y="{f(y)}" width="{f(w)}" height="28" rx="8" fill="{degradado(col, 0.25)}" stroke="{INK}" stroke-width="5"/>'
    for i in range(2):  # asiento
        y = sy - 6 + i * 22
        o += f'<rect x="{f(cx-w*0.52)}" y="{f(y)}" width="{f(w*1.04)}" height="22" rx="7" fill="{degradado(shade(col, -0.08), 0.25)}" stroke="{INK}" stroke-width="5"/>'
    o += brillo(f"M {f(cx-w*0.44)} {f(sy-142)} L {f(cx-w*0.1)} {f(sy-142)}", 4, 0.5)
    return Pieza(g(id_, o), {"asiento": (cx, sy)}, (cx - w * 0.55, sy - 150, cx + w * 0.55, base))


def cronometro(id_, cx, cy, r=80, col=CORAL, texto=None):
    """Cronómetro con botón y corona. Aguja en id_+'_aguja' dibujada a las 12: gírala con
    {"effect":"move","rotate":90,"origin":"bottom"} (o spin, origin bottom). Arco de tiempo en id_+'_arco' si texto=None."""
    o = f'<circle cx="{f(cx+r*0.06)}" cy="{f(cy+r*0.08)}" r="{f(r*1.12)}" fill="{INK}" opacity="0.22"/>'
    o += f'<rect x="{f(cx-r*0.16)}" y="{f(cy-r*1.42)}" width="{f(r*0.32)}" height="{f(r*0.36)}" rx="{f(r*0.06)}" fill="url(#metalG)" stroke="{INK}" stroke-width="5"/>'
    o += f'<rect x="{f(cx-r*0.28)}" y="{f(cy-r*1.56)}" width="{f(r*0.56)}" height="{f(r*0.18)}" rx="{f(r*0.08)}" fill="{degradado(col, 0.25)}" stroke="{INK}" stroke-width="5"/>'
    o += f'<g transform="rotate(40 {f(cx)} {f(cy)})"><rect x="{f(cx-r*0.12)}" y="{f(cy-r*1.3)}" width="{f(r*0.24)}" height="{f(r*0.26)}" rx="{f(r*0.05)}" fill="url(#metalG)" stroke="{INK}" stroke-width="4.5"/></g>'
    o += f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r*1.12)}" fill="{degradado(col, 0.25)}" stroke="{INK}" stroke-width="7"/>'
    o += f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/>'
    for i in range(12):
        a = math.radians(i * 30)
        r1 = r * (0.74 if i % 3 == 0 else 0.84)
        o += f'<path d="M {f(cx+r1*math.sin(a))} {f(cy-r1*math.cos(a))} L {f(cx+r*0.92*math.sin(a))} {f(cy-r*0.92*math.cos(a))}" stroke="{INK}" stroke-width="{6 if i % 3 == 0 else 3.5}" stroke-linecap="round"/>'
    if texto:
        o += T(cx, cy + r * 0.5, texto, r * 0.22, CORAL, font=DISP)
    o += g(f"{id_}_aguja" if id_ else None, trazo(f"M {f(cx)} {f(cy)} L {f(cx)} {f(cy-r*0.8)}", r * 0.06, CORAL, 4))
    o += f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r*0.09)}" fill="{INK}"/>'
    o += brillo_arco(cx, cy, r * 0.86, 200, 250, r * 0.05, 0.6)
    return g(id_, o)


def pizarra(id_, cx, cy, w=380, h=250, contenido="", col="#24463A", marco="#B07A45"):
    """Pizarra verde con marco de madera, bandeja y tiza. `contenido` va encima (dibújalo en coordenadas finales,
    trazos claros tipo tiza, p. ej. stroke '#F4F1E6')."""
    x0, y0 = cx - w / 2, cy - h / 2
    o = sombra_caja(x0, y0, w, h)
    o += f'<rect x="{f(x0-14)}" y="{f(y0-14)}" width="{f(w+28)}" height="{f(h+28)}" rx="12" fill="{degradado(marco, 0.25)}" stroke="{INK}" stroke-width="7"/>'
    registrar_defs(lg("pizG", [(0, shade(col, 0.15)), (1, shade(col, -0.15))], 0, 0, 1, 1))
    o += f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" rx="6" fill="url(#pizG)" stroke="{INK}" stroke-width="5"/>'
    o += f'<path d="M {f(x0+20)} {f(y0+h*0.75)} Q {f(cx)} {f(y0+h*0.68)} {f(x0+w-30)} {f(y0+h*0.8)}" fill="none" stroke="#FFFFFF" stroke-width="10" opacity="0.06" stroke-linecap="round"/>'
    o += f'<rect x="{f(x0-6)}" y="{f(y0+h+10)}" width="{f(w+12)}" height="16" rx="5" fill="{shade(marco, -0.2)}" stroke="{INK}" stroke-width="5"/>'
    o += f'<rect x="{f(x0+w*0.7)}" y="{f(y0+h+2)}" width="40" height="10" rx="4" fill="#FFFFFF" stroke="{INK}" stroke-width="3"/>'
    return g(id_, o + contenido)


def _suela(cx, cy, s, espejo=False):
    k = -1 if espejo else 1
    p = [(0, -95), (26, -86), (36, -50), (30, -6), (26, 40), (28, 74), (14, 96), (-12, 96), (-26, 72), (-24, 30), (-30, -10), (-34, -56), (-22, -88)]
    p = [(cx + k * x * s, cy + y * s) for x, y in p]
    return smooth(p, True)


def zapato_arriba(id_, cx, cy, s=1.0, col=CORAL, rot_=0, espejo=False):
    """Zapatilla vista desde arriba (puntera hacia arriba), unos 70×190 px a s=1. espejo=True: pie izquierdo."""
    d = _suela(cx, cy, s, espejo)
    o = f'<path d="{d}" fill="#FFFFFF" stroke="{INK}" stroke-width="7"/>'
    d2 = _suela(cx, cy + 4 * s, s * 0.86, espejo)
    o += f'<path d="{d2}" fill="{degradado(col, 0.25)}" stroke="{INK}" stroke-width="5"/>'
    o += f'<ellipse cx="{f(cx)}" cy="{f(cy+46*s)}" rx="{f(17*s)}" ry="{f(28*s)}" fill="{shade(col, -0.45)}" stroke="{INK}" stroke-width="4"/>'
    o += "".join(f'<path d="M {f(cx-14*s)} {f(cy+y*s)} L {f(cx+14*s)} {f(cy+(y+8)*s)} M {f(cx+14*s)} {f(cy+y*s)} L {f(cx-14*s)} {f(cy+(y+8)*s)}" stroke="#FFFFFF" stroke-width="{f(3.5*s)}" stroke-linecap="round"/>' for y in (-30, -12, 6))
    o += brillo(f"M {f(cx-14*s)} {f(cy-70*s)} Q {f(cx)} {f(cy-82*s)} {f(cx+12*s)} {f(cy-72*s)}", 4, 0.7)
    tr = f' transform="rotate({f(rot_)} {f(cx)} {f(cy)})"' if rot_ else ""
    return g(id_, f"<g{tr}>{o}</g>")


def huella(id_, cx, cy, s=1.0, col="#7C879C", espejo=False):
    """Huella (contorno discontinuo de una suela) donde encaja zapato_arriba(cx, cy, s)."""
    d = _suela(cx, cy, s * 1.06, espejo)
    return g(id_, f'<path d="{d}" fill="{col}" fill-opacity="0.18" stroke="{col}" stroke-width="6" stroke-dasharray="14 10" stroke-linecap="round"/>')


def portapapeles(id_, cx, cy, w=200, h=260, filas=4, marcadas=(0, 1, 2), col="#B07A45", titulo=None):
    """Portapapeles con hoja y casillas; las marcadas llevan ✓ en id_+'_c<i>' (para pop en cascada)."""
    x0, y0 = cx - w / 2, cy - h / 2
    o = sombra_caja(x0, y0, w, h, 14)
    o += f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" rx="14" fill="{degradado(col, 0.25)}" stroke="{INK}" stroke-width="7"/>'
    o += f'<rect x="{f(x0+w*0.08)}" y="{f(y0+h*0.1)}" width="{f(w*0.84)}" height="{f(h*0.84)}" rx="4" fill="url(#papelG)" stroke="{INK}" stroke-width="4"/>'
    o += f'<rect x="{f(cx-w*0.22)}" y="{f(y0-12)}" width="{f(w*0.44)}" height="{f(h*0.12)}" rx="8" fill="url(#metalG)" stroke="{INK}" stroke-width="5"/>'
    top = y0 + h * 0.2
    if titulo:
        o += T(cx, top + 6, titulo, w * 0.11, INK)
        top += h * 0.1
    step = (y0 + h * 0.88 - top) / filas
    for i in range(filas):
        y = top + step * (i + 0.5)
        bx = x0 + w * 0.16
        o += f'<rect x="{f(bx)}" y="{f(y-step*0.25)}" width="{f(step*0.5)}" height="{f(step*0.5)}" rx="4" fill="#FFFFFF" stroke="{INK}" stroke-width="3.5"/>'
        o += f'<path d="M {f(bx+step*0.7)} {f(y)} L {f(x0+w*0.84)} {f(y)}" stroke="#AEB6C6" stroke-width="5" stroke-linecap="round"/>'
        if i in marcadas:
            o += g(f"{id_}_c{i}", f'<path d="M {f(bx+step*0.06)} {f(y-step*0.02)} L {f(bx+step*0.22)} {f(y+step*0.18)} L {f(bx+step*0.6)} {f(y-step*0.36)}" fill="none" stroke="#1FA35A" stroke-width="{f(max(4, step*0.12))}" stroke-linecap="round" stroke-linejoin="round"/>')
    return g(id_, o)


def trofeo(id_, cx, base, h=300, texto="PREMIO", col="#FFC83D"):
    """Copa de premio dorada con asas, peana de madera y placa con `texto` (≈ 0.9h de ancho). Sub-id _brillo (destello: pulse).
    .puntos: copa (centro de la copa), placa."""
    w = h * 0.62
    top = base - h
    o = sombra(cx, base + 4, w * 0.75, h * 0.05)
    cg = degradado(col, 0.3, "h")
    # peana
    o += f'<rect x="{f(cx - w*0.55)}" y="{f(base - h*0.18)}" width="{f(w*1.1)}" height="{f(h*0.18)}" rx="10" fill="url(#maderaOsc)" stroke="{INK}" stroke-width="7"/>'
    o += f'<rect x="{f(cx - w*0.38)}" y="{f(base - h*0.145)}" width="{f(w*0.76)}" height="{f(h*0.11)}" rx="6" fill="url(#metalG)" stroke="{INK}" stroke-width="4"/>'
    o += T(cx, base - h * 0.067, texto, min(h * 0.07, w * 1.3 / max(4, len(texto))), INK, font=DISP)
    # pie y tallo
    o += f'<path d="M {f(cx - w*0.3)} {f(base - h*0.18)} L {f(cx + w*0.3)} {f(base - h*0.18)} L {f(cx + w*0.16)} {f(base - h*0.27)} L {f(cx - w*0.16)} {f(base - h*0.27)} Z" fill="{cg}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
    o += f'<rect x="{f(cx - w*0.07)}" y="{f(base - h*0.42)}" width="{f(w*0.14)}" height="{f(h*0.16)}" fill="{cg}" stroke="{INK}" stroke-width="6"/>'
    # asas
    for k in (-1, 1):
        o += trazo(f"M {f(cx + k*w*0.42)} {f(top + h*0.1)} C {f(cx + k*w*0.78)} {f(top + h*0.08)}, {f(cx + k*w*0.75)} {f(top + h*0.38)}, {f(cx + k*w*0.3)} {f(top + h*0.42)}", h * 0.035, col, 6)
    # copa
    o += (f'<path d="M {f(cx - w*0.5)} {f(top)} L {f(cx + w*0.5)} {f(top)} C {f(cx + w*0.5)} {f(top + h*0.38)}, {f(cx + w*0.2)} {f(top + h*0.56)}, {f(cx)} {f(top + h*0.58)} '
          f'C {f(cx - w*0.2)} {f(top + h*0.56)}, {f(cx - w*0.5)} {f(top + h*0.38)}, {f(cx - w*0.5)} {f(top)} Z" fill="{cg}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
    o += f'<ellipse cx="{f(cx)}" cy="{f(top)}" rx="{f(w*0.5)}" ry="{f(h*0.045)}" fill="{shade(col, -0.25)}" stroke="{INK}" stroke-width="6"/>'
    o += brillo(f"M {f(cx - w*0.32)} {f(top + h*0.08)} C {f(cx - w*0.32)} {f(top + h*0.28)}, {f(cx - w*0.18)} {f(top + h*0.42)}, {f(cx - w*0.08)} {f(top + h*0.47)}", h * 0.025, 0.75)
    o += g(f"{id_}_brillo", f'<path d="M {f(cx + w*0.22)} {f(top + h*0.1)} l 8 22 l 22 8 l -22 8 l -8 22 l -8 -22 l -22 -8 l 22 -8 Z" fill="#FFFFFF" stroke="{INK}" stroke-width="3"/>')
    return Pieza(g(id_, o), {"copa": (cx, top + h * 0.25), "placa": (cx, base - h * 0.09)}, (cx - w * 0.8, top - 10, cx + w * 0.8, base + 10))


def nivel_burbuja(id_, cx, cy, w=360, h=90, col=YEL, inclinado=0):
    """Nivel de burbuja de albañil. La burbuja va en {id}_burbuja (move horizontal: [±w*0.12, 0] = desnivel).
    inclinado: grados de giro del nivel entero. Sale de lote8-03-gatos-caen (oído interno = nivel)."""
    x, y = -w / 2, -h / 2
    o = f'<rect x="{f(x+8)}" y="{f(y+10)}" width="{f(w)}" height="{f(h)}" rx="14" fill="{INK}" opacity="0.2"/>'
    o += f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="14" fill="{degradado(col, 0.25)}" stroke="{INK}" stroke-width="7"/>'
    o += brillo(f"M {f(x+20)} {f(y+14)} L {f(x+w-20)} {f(y+14)}", 6, 0.7)
    vw, vh = w * 0.36, h * 0.48
    o += f'<rect x="{f(-vw/2)}" y="{f(-vh/2)}" width="{f(vw)}" height="{f(vh)}" rx="{f(vh/2)}" fill="#B9F06A" stroke="{INK}" stroke-width="6"/>'
    o += f'<path d="M -14 {f(-vh/2)} L -14 {f(vh/2)} M 14 {f(-vh/2)} L 14 {f(vh/2)}" stroke="{INK}" stroke-width="4"/>'
    o += g(f"{id_}_burbuja", f'<ellipse cx="0" cy="0" rx="{f(vh*0.42)}" ry="{f(vh*0.3)}" fill="#FFFFFF" stroke="{INK}" stroke-width="3" opacity="0.95"/>')
    for k in (-1, 1):
        o += f'<circle cx="{f(k*w*0.38)}" cy="0" r="{f(h*0.16)}" fill="{shade(col, -0.35)}" stroke="{INK}" stroke-width="4"/>'
    return gt(id_, f"translate({f(cx)} {f(cy)}) rotate({f(inclinado)})", o)


def red_ventana(id_, x, y, w, h, paso=34, col="#E9EEF7"):
    """Red/malla protectora para ventanas y balcones (rombos finos con marco). (x, y) = esquina superior izquierda.
    Anímala con fade o draw. Sale de lote8-03-gatos-caen."""
    o = ""
    lines = ""
    n = int((w + h) / paso) + 1
    for i in range(n):
        d = i * paso
        lines += f'<line x1="{f(x + d)}" y1="{f(y)}" x2="{f(x + d - h)}" y2="{f(y + h)}"/>'
        lines += f'<line x1="{f(x + d - h)}" y1="{f(y)}" x2="{f(x + d)}" y2="{f(y + h)}"/>'
    cid = f"clip_{id_}"
    o += f'<clipPath id="{cid}"><rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}"/></clipPath>'
    o += f'<g clip-path="url(#{cid})"><g stroke="{INK}" stroke-width="6" opacity="0.55">{lines}</g><g stroke="{col}" stroke-width="3">{lines}</g></g>'
    o += f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="6" fill="none" stroke="{INK}" stroke-width="10"/>'
    o += f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="6" fill="none" stroke="#C9D2E2" stroke-width="5"/>'
    return g(id_, o)


# --------------------------------------------------------------- lote9-04-tripa-ruge: escoba, tambor, pasta, columna y pergamino
registrar_defs(
    lg("tamborG", [(0, "#FF8A6B"), (0.5, "#FF5A36"), (1, "#B8341C")], 0, 0, 1, 0)
    + lg("parcheG", [(0, "#FFFDF4"), (1, "#EDE3C8")])
    + lg("pastaTuboG", [(0, "#FFFFFF"), (0.5, "#E9EEF6"), (1, "#B9C3D3")], 0, 0, 1, 0)
    + lg("marmolG", [(0, "#FFFFFF"), (0.55, "#ECE7DC"), (1, "#CFC6B4")], 0, 0, 1, 0)
    + lg("pergG", [(0, "#FFF4D6"), (1, "#E9CF98")])
)


def escoba(id_, p0, p1, s=1.0, col="#E3B04B", palo="#8A5A2B"):
    """Escoba de barrendero: palo de p0 (extremo de arriba) a p1 (donde empieza el cepillo), cepillo ancho de cerdas
    perpendicular al palo. Sub-ids: _palo, _cepillo (wiggle origin top para barrer). .puntos: cepillo, punta."""
    x0, y0 = p0
    x1, y1 = p1
    L = math.hypot(x1 - x0, y1 - y0)
    ang = math.degrees(math.atan2(y1 - y0, x1 - x0)) - 90
    o = g(f"{id_}_palo", trazo(f"M {f(x0)} {f(y0)} L {f(x1)} {f(y1)}", 14 * s, palo, 7))
    w, h = 210 * s, 70 * s
    cep = (f'<rect x="{f(-w/2)}" y="0" width="{f(w)}" height="{f(26*s)}" rx="{f(8*s)}" fill="{degradado("#3B4A66", 0.3)}" stroke="{INK}" stroke-width="6"/>'
           + f'<path d="M {f(-w/2+4)} {f(24*s)} L {f(-w/2-10)} {f(h+26*s)} L {f(w/2+10)} {f(h+26*s)} L {f(w/2-4)} {f(24*s)} Z" fill="{degradado(col, 0.25)}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
           + "".join(f'<path d="M {f(-w/2 + i*w/9)} {f(34*s)} L {f(-w/2 - 6 + i*w/8.4)} {f(h+20*s)}" stroke="{shade(col, -0.3)}" stroke-width="3"/>' for i in range(1, 9)))
    o += g(f"{id_}_cepillo", f'<g transform="translate({f(x1)} {f(y1)}) rotate({f(ang)})">{cep}</g>')
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    return Pieza(g(id_, o), {"cepillo": (x1, y1), "punta": (x1 + ux * (h + 26 * s), y1 + uy * (h + 26 * s))},
                 (min(x0, x1) - w / 2, min(y0, y1), max(x0, x1) + w / 2, max(y0, y1) + h + 26 * s))


def tambor(id_, cx, base, w=300, h=220, col="url(#tamborG)"):
    """Tambor de frente un poco cenital con parche, aros, tensores en zigzag y dos baquetas.
    Sub-ids: _cuerpo, _parche (pulse al golpear), _baq_izq / _baq_der (move rotate origin bottom-left / bottom-right
    para golpear). .puntos: parche (centro), golpe_izq, golpe_der."""
    rx, ry = w / 2, w * 0.17
    top = base - h
    o = sombra(cx, base + 6, rx * 1.05, 16, 0.25)
    o += g(f"{id_}_cuerpo",
           f'<path d="M {f(cx-rx)} {f(top)} L {f(cx-rx)} {f(base-ry*0.4)} A {f(rx)} {f(ry)} 0 0 0 {f(cx+rx)} {f(base-ry*0.4)} L {f(cx+rx)} {f(top)} Z" fill="{col}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'
           + "".join(f'<path d="M {f(cx-rx+i*w/6)} {f(top+ry*0.9)} L {f(cx-rx+(i+0.5)*w/6)} {f(base-ry*1.2)} L {f(cx-rx+(i+1)*w/6)} {f(top+ry*0.9)}" fill="none" stroke="#FFF4D6" stroke-width="6" stroke-linejoin="round"/>' for i in range(6))
           + f'<path d="M {f(cx-rx)} {f(base-ry*0.6)} A {f(rx)} {f(ry)} 0 0 0 {f(cx+rx)} {f(base-ry*0.6)}" fill="none" stroke="{INK}" stroke-width="16"/>'
           + f'<path d="M {f(cx-rx)} {f(base-ry*0.6)} A {f(rx)} {f(ry)} 0 0 0 {f(cx+rx)} {f(base-ry*0.6)}" fill="none" stroke="#E3B04B" stroke-width="8"/>'
           + brillo(f"M {f(cx-rx+18)} {f(top+40)} L {f(cx-rx+18)} {f(base-50)}", 8, 0.5))
    o += g(f"{id_}_parche", f'<ellipse cx="{f(cx)}" cy="{f(top)}" rx="{f(rx)}" ry="{f(ry)}" fill="url(#parcheG)" stroke="{INK}" stroke-width="8"/>'
           + f'<ellipse cx="{f(cx)}" cy="{f(top)}" rx="{f(rx-6)}" ry="{f(ry-5)}" fill="none" stroke="#E3B04B" stroke-width="6"/>')
    gi, gd = (cx - rx * 0.32, top), (cx + rx * 0.3, top - 2)
    o += g(f"{id_}_baq_izq", trazo(f"M {f(gi[0]-150)} {f(top-170)} L {f(gi[0]-6)} {f(gi[1]-14)}", 12, "#D9A066", 6)
           + f'<circle cx="{f(gi[0]-4)}" cy="{f(gi[1]-14)}" r="15" fill="#FFF4D6" stroke="{INK}" stroke-width="6"/>')
    o += g(f"{id_}_baq_der", trazo(f"M {f(gd[0]+160)} {f(top-150)} L {f(gd[0]+6)} {f(gd[1]-14)}", 12, "#D9A066", 6)
           + f'<circle cx="{f(gd[0]+4)}" cy="{f(gd[1]-14)}" r="15" fill="#FFF4D6" stroke="{INK}" stroke-width="6"/>')
    return Pieza(g(id_, o), {"parche": (cx, top), "golpe_izq": gi, "golpe_der": gd}, (cx - rx - 160, top - 180, cx + rx + 170, base + 20))


def tubo_pasta(id_, cx, cy, s=1.0, rot_=0, estrujado=False, col="#2EC4B6", texto="PASTA"):
    """Tubo de pasta de dientes de pie (tapón abajo, boca arriba). estrujado=True lo dibuja apretado por el medio.
    Sub-ids: _churro (grow origin bottom: la pasta que sale). .puntos: boca. ≈ 150×330 a s=1, (cx, cy) = centro."""
    k = 0.55 if estrujado else 1.0
    pts_tubo = [(-70, 150), (-74 * (0.8 + 0.2 * k), 40), (-60 * k, -40), (-40, -120), (-26, -150), (26, -150), (40, -120), (60 * k, -40),
                (74 * (0.8 + 0.2 * k), 40), (70, 150)]
    o = f'<path d="{poly(pts_tubo, True)}" fill="url(#pastaTuboG)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
    o += f'<rect x="-80" y="140" width="160" height="22" rx="4" fill="{col}" stroke="{INK}" stroke-width="6"/>'
    o += "".join(f'<path d="M {x} 146 L {x} 158" stroke="{INK}" stroke-width="3"/>' for x in range(-64, 70, 16))
    o += f'<path d="M -50 {f(-60 if estrujado else -30)} L 50 {f(-60 if estrujado else -30)} L 50 {f(60)} L -50 60 Z" fill="{col}" stroke="{INK}" stroke-width="5" opacity="0.95"/>'
    o += T(0, 20, texto, 24, "#FFFFFF", font=DISP, extra=f'stroke="{INK}" stroke-width="4" paint-order="stroke"')
    if estrujado:
        o += "".join(f'<path d="M {sx*74} {y} q {sx*-12} 8 {sx*-4} 18" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>' for sx in (-1, 1) for y in (-40, 0))
    o += f'<rect x="-30" y="-178" width="60" height="32" rx="6" fill="{degradado("#FFFFFF", 0.25)}" stroke="{INK}" stroke-width="6"/>'
    o += brillo("M -54 120 L -48 -20", 6, 0.8)
    churro = (f'<path d="M -20 -176 C -24 -230, -10 -270, 20 -282 C 54 -294, 64 -250, 36 -236 C 16 -226, 18 -200, 22 -176 Z" fill="#FFFFFF" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
              + f'<path d="M -8 -186 C -10 -226, 2 -256, 24 -266" fill="none" stroke="{col}" stroke-width="7" stroke-linecap="round"/>')
    o += g(f"{id_}_churro", churro)
    tr = f"translate({f(cx)} {f(cy)}) rotate({f(rot_)}) scale({f(s)})"
    return Pieza(gt(id_, tr, o), {"boca": (cx, cy - 176 * s)}, (cx - 80 * s, cy - 290 * s, cx + 80 * s, cy + 165 * s))


def columna_griega(id_, cx, base, h=520, w=120):
    """Columna griega de mármol (dórica) con capitel y basa. .puntos: capitel."""
    top = base - h
    o = sombra(cx, base + 4, w * 0.95, 14, 0.22)
    o += f'<rect x="{f(cx-w*0.78)}" y="{f(base-36)}" width="{f(w*1.56)}" height="36" rx="6" fill="url(#marmolG)" stroke="{INK}" stroke-width="7"/>'
    o += f'<path d="M {f(cx-w*0.5)} {f(base-36)} L {f(cx-w*0.44)} {f(top+46)} L {f(cx+w*0.44)} {f(top+46)} L {f(cx+w*0.5)} {f(base-36)} Z" fill="url(#marmolG)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
    o += "".join(f'<path d="M {f(cx + k*w*0.47)} {f(base-42)} L {f(cx + k*w*0.41)} {f(top+52)}" stroke="#B8AE98" stroke-width="5" stroke-linecap="round"/>'
                 for k in (-0.62, -0.25, 0.12, 0.49, 0.82))
    o += f'<path d="M {f(cx-w*0.62)} {f(top+48)} Q {f(cx)} {f(top+30)} {f(cx+w*0.62)} {f(top+48)} L {f(cx+w*0.7)} {f(top+26)} L {f(cx-w*0.7)} {f(top+26)} Z" fill="url(#marmolG)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
    o += f'<rect x="{f(cx-w*0.82)}" y="{f(top)}" width="{f(w*1.64)}" height="28" rx="5" fill="url(#marmolG)" stroke="{INK}" stroke-width="7"/>'
    o += brillo(f"M {f(cx-w*0.3)} {f(top+70)} L {f(cx-w*0.34)} {f(base-60)}", 7, 0.85)
    return Pieza(g(id_, o), {"capitel": (cx, top)}, (cx - w * 0.82, top, cx + w * 0.82, base))


def pergamino(id_, cx, cy, w=420, h=300, texto="", size=46, sub=""):
    """Pergamino desenrollado con rodillos arriba y abajo (para grow origin top: se desenrolla). Sub-ids: _texto."""
    x0, y0 = cx - w / 2, cy - h / 2
    o = f'<rect x="{f(x0+14)}" y="{f(y0+18)}" width="{f(w)}" height="{f(h)}" fill="{INK}" opacity="0.2" rx="8"/>'
    o += f'<path d="M {f(x0)} {f(y0)} L {f(x0+w)} {f(y0)} Q {f(x0+w-14)} {f(cy)} {f(x0+w)} {f(y0+h)} L {f(x0)} {f(y0+h)} Q {f(x0+14)} {f(cy)} {f(x0)} {f(y0)} Z" fill="url(#pergG)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
    for yy in (y0, y0 + h):
        o += f'<rect x="{f(x0-22)}" y="{f(yy-18)}" width="{f(w+44)}" height="36" rx="18" fill="{degradado("#D9A066", 0.3)}" stroke="{INK}" stroke-width="7"/>'
        o += brillo(f"M {f(x0-6)} {f(yy-8)} L {f(x0+w*0.4)} {f(yy-8)}", 5, 0.7)
    o += g(f"{id_}_texto", T(cx, cy + size * 0.1 + (0 if not sub else -size * 0.2), texto, size, "#7A4E28", font='font-family="Georgia, serif" font-weight="700" font-style="italic"')
           + (T(cx, cy + size * 1.05, sub, size * 0.5, "#9A7A50") if sub else ""))
    return Pieza(g(id_, o), {}, (x0 - 22, y0 - 18, x0 + w + 22, y0 + h + 18))


# ------------------------------------------------------------------ desayuno: tostada, plato, mesa de perfil, escalera, espejo roto
# (lote9-07-tostada-mantequilla)
MIGA, CORTEZA, MANTEQUILLA = "#F3D9A0", "#B9702F", "#FFD84A"


def tostada(id_, cx, cy, w=200, vista="lado", rot_=0, mantequilla=True):
    """Tostada con mantequilla. vista="lado": rebanada de canto (≈ w × 0,2w), mantequilla amarilla arriba
    (rot_=180 = boca abajo); vista="frente": rebanada de frente (≈ w × 1,05w) con la mantequilla untada
    (mantequilla=False = cara de miga tostada). (cx, cy) = centro; rot_ gira sobre el centro.
    Para animarla: grupo exterior con move + otro dentro con move rotate (origin center). .puntos: centro, mantequilla."""
    if vista == "lado":
        t = w * 0.17
        o = (f'<rect x="{f(-w/2)}" y="{f(-t/2)}" width="{f(w)}" height="{f(t)}" rx="{f(t*0.45)}" '
             f'fill="{degradado(CORTEZA, 0.18)}" stroke="{INK}" stroke-width="6"/>')
        o += f'<rect x="{f(-w/2+t*0.45)}" y="{f(-t*0.22)}" width="{f(w-t*0.9)}" height="{f(t*0.44)}" rx="{f(t*0.2)}" fill="{MIGA}"/>'
        o += "".join(f'<circle cx="{f(-w/2+w*k)}" cy="{f(t*0.02*(i%3-1))}" r="{f(t*0.07)}" fill="{shade(MIGA,-0.25)}"/>'
                     for i, k in enumerate((0.18, 0.31, 0.45, 0.58, 0.72, 0.84)))
        if mantequilla:
            bt = t * 0.42
            d = (f"M {f(-w*0.45)} {f(-t/2+3)} Q {f(-w*0.46)} {f(-t/2-bt)} {f(-w*0.32)} {f(-t/2-bt)} "
                 f"Q {f(-w*0.12)} {f(-t/2-bt*1.35)} {f(w*0.08)} {f(-t/2-bt)} Q {f(w*0.24)} {f(-t/2-bt*0.75)} {f(w*0.34)} {f(-t/2-bt)} "
                 f"Q {f(w*0.46)} {f(-t/2-bt)} {f(w*0.45)} {f(-t/2+3)} Z")
            o += f'<path d="{d}" fill="{degradado(MANTEQUILLA, 0.16)}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
            o += brillo(f"M {f(-w*0.3)} {f(-t/2-bt*0.6)} L {f(w*0.1)} {f(-t/2-bt*0.65)}", 4, 0.85)
        else:
            o += brillo(f"M {f(-w*0.35)} {f(-t*0.3)} L {f(w*0.2)} {f(-t*0.3)}", 3, 0.5)
        caja = (cx - w / 2, cy - w * 0.25, cx + w / 2, cy + w * 0.25)
    else:
        h = w * 1.05
        x0, y0 = -w / 2, -h / 2
        d = (f"M {f(x0+w*0.06)} {f(y0+h*0.98)} L {f(x0+w*0.94)} {f(y0+h*0.98)} Q {f(x0+w)} {f(y0+h*0.98)} {f(x0+w*0.98)} {f(y0+h*0.9)} "
             f"L {f(x0+w*0.95)} {f(y0+h*0.36)} C {f(x0+w*1.1)} {f(y0+h*0.2)}, {f(x0+w*0.85)} {f(y0-h*0.02)}, {f(x0+w*0.5)} {f(y0+h*0.04)} "
             f"C {f(x0+w*0.15)} {f(y0-h*0.02)}, {f(x0-w*0.1)} {f(y0+h*0.2)}, {f(x0+w*0.05)} {f(y0+h*0.36)} "
             f"L {f(x0+w*0.02)} {f(y0+h*0.9)} Q {f(x0)} {f(y0+h*0.98)} {f(x0+w*0.06)} {f(y0+h*0.98)} Z")
        o = f'<path d="{d}" fill="{degradado(CORTEZA, 0.2)}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
        o += f'<g transform="translate(0 {f(h*0.035)}) scale(0.84)"><path d="{d}" fill="{degradado("#E8B866", 0.18)}"/></g>'
        rnd = random.Random(7)
        o += "".join(f'<circle cx="{f(rnd.uniform(-w*0.32, w*0.32))}" cy="{f(rnd.uniform(-h*0.25, h*0.35))}" r="{f(w*0.012+rnd.random()*w*0.01)}" fill="#C98A3E" opacity="0.7"/>' for _ in range(16))
        if mantequilla:
            pts_ = [(-0.3, -0.2), (-0.05, -0.27), (0.27, -0.18), (0.33, 0.1), (0.22, 0.33), (-0.08, 0.3), (-0.33, 0.25), (-0.36, 0.0)]
            ub = smooth([(x * w, y * h) for x, y in pts_], True)
            o += f'<path d="{ub}" fill="{degradado(MANTEQUILLA, 0.14)}" stroke="{shade(MANTEQUILLA,-0.3)}" stroke-width="4"/>'
            o += brillo(f"M {f(-w*0.2)} {f(-h*0.12)} Q {f(0)} {f(-h*0.2)} {f(w*0.16)} {f(-h*0.1)}", 5, 0.85)
            o += f'<rect x="{f(w*0.0)}" y="{f(-h*0.02)}" width="{f(w*0.2)}" height="{f(w*0.15)}" rx="{f(w*0.03)}" fill="{degradado("#FFE680", 0.15)}" stroke="{INK}" stroke-width="4" transform="rotate(-12 {f(w*0.1)} {f(h*0.05)})"/>'
        caja = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    tr = f"translate({f(cx)} {f(cy)})" + (f" rotate({f(rot_)})" if rot_ else "")
    ang = math.radians(rot_ - 90)
    lado = (cx + math.cos(ang) * w * 0.12, cy + math.sin(ang) * w * 0.12)
    return Pieza(gt(id_, tr, o), {"centro": (cx, cy), "mantequilla": lado}, caja)


def mancha_mantequilla(id_, cx, cy, s=1.0):
    """Salpicadura de mantequilla en el suelo (≈ 260×60 a s=1): charquito aplastado y gotitas. Anímala con pop."""
    rnd = random.Random(3)
    pts_ = [(cx + math.cos(a) * 120 * s * (0.8 + rnd.random() * 0.35), cy + math.sin(a) * 22 * s * (0.8 + rnd.random() * 0.4))
            for a in [i * math.pi / 6 for i in range(12)]]
    o = f'<path d="{smooth(pts_, True)}" fill="{degradado(MANTEQUILLA, 0.14)}" stroke="{INK}" stroke-width="5"/>'
    for dx, dy, r in ((-150, -18, 11), (148, -24, 9), (-118, -42, 7), (128, -46, 6), (0, -50, 6)):
        o += f'<ellipse cx="{f(cx+dx*s)}" cy="{f(cy+dy*s)}" rx="{f(r*s*1.3)}" ry="{f(r*s)}" fill="{MANTEQUILLA}" stroke="{INK}" stroke-width="4"/>'
    o += brillo(f"M {f(cx-60*s)} {f(cy-6*s)} L {f(cx+20*s)} {f(cy-9*s)}", 4, 0.8)
    return g(id_, o)


def plato(id_, cx, cy, w=240, col="#FFFFFF"):
    """Plato llano visto un poco desde arriba (elipse con ala). (cx, cy) = centro."""
    o = sombra(cx + 6, cy + w * 0.12, w * 0.5, w * 0.08, 0.25)
    o += f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(w/2)}" ry="{f(w*0.16)}" fill="{degradado(col, 0.08)}" stroke="{INK}" stroke-width="6"/>'
    o += f'<ellipse cx="{f(cx)}" cy="{f(cy+2)}" rx="{f(w*0.33)}" ry="{f(w*0.09)}" fill="{shade(col,-0.07)}" stroke="#C9D2E2" stroke-width="3"/>'
    o += brillo(f"M {f(cx-w*0.38)} {f(cy-w*0.06)} Q {f(cx-w*0.2)} {f(cy-w*0.14)} {f(cx)} {f(cy-w*0.145)}", 4, 0.9)
    return g(id_, o)


def mesa_perfil(id_, x0, x1, y_tablero, alto=380, grosor=34, col="#C98B55", travesano=True):
    """Mesa de madera vista de perfil: tablero de x0 a x1 en y_tablero y dos patas hasta el suelo (y_tablero + alto).
    Sirve igual para una mesa normal o una gigante (alto grande). .puntos: borde (esquina de arriba a la derecha), suelo (y)."""
    suelo = y_tablero + alto
    o = sombra((x0 + x1) / 2, suelo + 4, (x1 - x0) * 0.55, 14, 0.25)
    for k in (0.1, 0.86):
        lx = x0 + (x1 - x0) * k
        o += f'<rect x="{f(lx)}" y="{f(y_tablero)}" width="34" height="{f(alto)}" rx="7" fill="{degradado(shade(col,-0.12), 0.2, "h")}" stroke="{INK}" stroke-width="6"/>'
    if travesano:
        ty = y_tablero + min(70, alto * 0.18)
        o += f'<rect x="{f(x0+(x1-x0)*0.1+20)}" y="{f(ty)}" width="{f((x1-x0)*0.76)}" height="20" rx="6" fill="{shade(col,-0.2)}" stroke="{INK}" stroke-width="5"/>'
    o += f'<rect x="{f(x0)}" y="{f(y_tablero)}" width="{f(x1-x0)}" height="{f(grosor)}" rx="7" fill="{degradado(col, 0.2)}" stroke="{INK}" stroke-width="7"/>'
    o += brillo(f"M {f(x0+16)} {f(y_tablero+9)} L {f(x1-30)} {f(y_tablero+9)}", 4, 0.6)
    return Pieza(g(id_, o), {"borde": (x1, y_tablero), "suelo": suelo}, (x0, y_tablero, x1, suelo))


def escalera(id_, p_base, p_cima, w=110, peldanos=8, col="#C7CDD8"):
    """Escalera de mano apoyada de p_base (centro de las patas en el suelo) a p_cima. .puntos["peldano"](k) = centro del peldaño k."""
    (bx, by), (tx, ty) = p_base, p_cima
    L = math.hypot(tx - bx, ty - by)
    nx, ny = -(ty - by) / L, (tx - bx) / L  # normal
    def lado(s):
        return (bx + nx * s * w / 2, by + ny * s * w / 2), (tx + nx * s * w / 2 * 0.85, ty + ny * s * w / 2 * 0.85)
    o = ""
    pts_ = []
    for k in range(1, peldanos + 1):
        u = k / (peldanos + 1)
        (a0, a1), (b0, b1) = lado(-1), lado(1)
        pa = (a0[0] + (a1[0] - a0[0]) * u, a0[1] + (a1[1] - a0[1]) * u)
        pb = (b0[0] + (b1[0] - b0[0]) * u, b0[1] + (b1[1] - b0[1]) * u)
        o += trazo(f"M {f(pa[0])} {f(pa[1])} L {f(pb[0])} {f(pb[1])}", 9, shade(col, -0.1), 6)
        pts_.append(((pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2))
    for s in (-1, 1):
        a, b = lado(s)
        o += trazo(f"M {f(a[0])} {f(a[1])} L {f(b[0])} {f(b[1])}", 14, col, 7)
    return Pieza(g(id_, o), {"peldano": lambda k: pts_[max(0, min(len(pts_) - 1, k))], "cima": p_cima},
                 (min(bx, tx) - w, min(by, ty), max(bx, tx) + w, max(by, ty)))


def espejo_roto(id_, cx, cy, w=200, h=260):
    """Espejo ovalado de marco dorado con el cristal roto (grietas desde el golpe). Mala suerte."""
    o = sombra_caja(cx - w / 2, cy - h / 2, w, h, w / 2, 8, 10, 0.2)
    o += f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(w/2)}" ry="{f(h/2)}" fill="{degradado("#E7B53C", 0.25)}" stroke="{INK}" stroke-width="7"/>'
    registrar_defs(lg("espejoG", [(0, "#EAF7FF"), (0.5, "#B8DDF2"), (1, "#7FB4D6")], 0, 0, 1, 1))
    rx, ry = w / 2 - 18, h / 2 - 18
    o += f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(rx)}" ry="{f(ry)}" fill="url(#espejoG)" stroke="{INK}" stroke-width="5"/>'
    ix, iy = cx + w * 0.08, cy - h * 0.08
    rnd = random.Random(5)
    grietas = ""
    for i in range(7):
        a = i * 2 * math.pi / 7 + rnd.uniform(-0.2, 0.2)
        mx, my = ix + math.cos(a) * rx * 0.45, iy + math.sin(a) * ry * 0.45 + rnd.uniform(-8, 8)
        ex, ey = cx + math.cos(a) * rx * 0.97, cy + math.sin(a) * ry * 0.97
        grietas += f"M {f(ix)} {f(iy)} L {f(mx)} {f(my)} L {f(ex)} {f(ey)} "
    o += f'<path d="{grietas}" fill="none" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
    o += f'<path d="M {f(ix)} {f(iy)} L {f(ix+rx*0.3)} {f(iy-ry*0.15)} L {f(ix+rx*0.22)} {f(iy+ry*0.22)} Z" fill="#5E8FB3" stroke="{INK}" stroke-width="4"/>'
    o += brillo(f"M {f(cx-rx*0.6)} {f(cy+ry*0.1)} L {f(cx-rx*0.35)} {f(cy-ry*0.45)}", 6, 0.8)
    return g(id_, o)

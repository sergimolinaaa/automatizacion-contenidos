"""Cuerpo humano: cerebro (con hipotálamo), cabeza de perfil con el cerebro al descubierto, músculo (relajado/contraído),
antebrazo con vello y piel de gallina, termómetro, gota de sudor y lupa de piel.

Sale de: escalofrios/cerebro.py (cabeza de perfil, cerebro, hipotálamo), escalofrios/persona.py (fibras del músculo),
lote3-04/brazo.py (antebrazo, vello, piel de gallina, manga de lana), hielo-cruje/hc.py (termómetro).
"""
import math
import random
from ..base import (INK, LIME, CORAL, f, g, gt, T, shade, trazo, sombra, brillo, lg, rg, registrar_defs, degradado,
                    Pieza, smooth, poly)
from ..personajes import PIELES

registrar_defs(
    rg("brainR", [(0, "#FFD3DA"), (0.65, "#F3A2AF"), (1, "#D9788A")], 0.45, 0.35, 0.75)
    + rg("cerebR", [(0, "#F7B9C3"), (1, "#C9677A")], 0.4, 0.3, 0.8)
    + rg("hglow", [(0, "#FFE15A", 0.95), (1, "#FF5A36", 0)])
    + rg("hypR", [(0, "#FFB199"), (1, "#FF5A36")], 0.4, 0.35, 0.7)
    + lg("fibG", [(0, "#F08A80"), (0.5, "#D2463E"), (1, "#8E1F1A")])
    + rg("bumpR", [(0, "#FFE3D0"), (0.6, "#F2B996"), (1, "#D9906C")], 0.4, 0.35, 0.7)
    + lg("lanaR2", [(0, "#F0645A"), (1, "#A82A22")])
)

# --------------------------------------------------------------- cerebro
_BRAIN = [(250, 300), (270, 210), (340, 150), (440, 128), (540, 150), (600, 215), (612, 290), (580, 345), (500, 370),
          (420, 368), (330, 360), (268, 340)]
_GYRI = ["M 300 230 C 330 200, 360 240, 390 210 S 440 190, 460 220", "M 280 290 C 320 270, 340 310, 380 280 S 430 260, 470 290",
         "M 480 180 C 510 200, 540 170, 570 205", "M 500 250 C 530 230, 560 270, 590 250", "M 360 160 C 380 180, 410 160, 430 175",
         "M 330 330 C 360 315, 390 345, 420 325", "M 520 310 C 545 295, 560 320, 585 300"]
_BC = (431, 250)  # centro del cerebro en las coordenadas originales


def _cerebro_local(id_, hipotalamo=True, tronco=True):
    o = ""
    if tronco:
        o += f'<path d="M 410 362 C 400 420, 410 480, 405 560 L 455 560 C 452 480, 470 420, 470 365 Z" fill="#E996A4" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
    o += f'<path d="{smooth(_BRAIN, True)}" fill="url(#brainR)" stroke="{INK}" stroke-width="7"/>'
    o += "".join(f'<path d="{d}" fill="none" stroke="#B85568" stroke-width="6" stroke-linecap="round"/>' for d in _GYRI)
    o += brillo("M 300 190 C 360 140, 460 125, 540 150", 6, 0.7)
    o += f'<path d="{smooth([(270, 352), (320, 362), (370, 380), (360, 420), (310, 428), (272, 400)], True)}" fill="url(#cerebR)" stroke="{INK}" stroke-width="6"/>'
    o += "".join(f'<path d="M {285+k*6} {378+k*13} Q 320 {372+k*14} {355-k*4} {388+k*12}" fill="none" stroke="#A84D60" stroke-width="4" stroke-linecap="round"/>' for k in range(3))
    if hipotalamo:
        o += g(f"{id_}_hipotalamo" if id_ else None, '<circle cx="482" cy="352" r="48" fill="url(#hglow)"/>'
               f'<ellipse cx="482" cy="352" rx="20" ry="16" fill="url(#hypR)" stroke="{INK}" stroke-width="5"/>'
               '<ellipse cx="476" cy="346" rx="6" ry="4" fill="#FFFFFF" opacity="0.8"/>')
    return o


def cerebro(id_, cx, cy, s=1.0, hipotalamo=True, tronco=True):
    """Cerebro de perfil (mira a la derecha) con circunvoluciones, cerebelo, tronco y el hipotálamo brillante
    (grupo id_+'_hipotalamo', «el termostato del cerebro»). s=1 → unos 360 px de ancho.
    Devuelve Pieza con .puntos['hipotalamo'], ['cerebelo'], ['frente']."""
    def P(x, y):
        return (cx + (x - _BC[0]) * s, cy + (y - _BC[1]) * s)
    body = f'<g transform="translate({f(cx)} {f(cy)}) scale({f(s)}) translate({-_BC[0]} {-_BC[1]})">{_cerebro_local(id_, hipotalamo, tronco)}</g>'
    return Pieza(g(id_, body), {"hipotalamo": P(482, 352), "cerebelo": P(315, 395), "frente": P(590, 230)},
                 (cx - 185 * s, cy - 125 * s, cx + 185 * s, cy + (310 if tronco else 180) * s))


_HEAD = [(300, 720), (292, 600), (250, 520), (208, 430), (205, 320), (240, 205), (320, 120), (430, 88), (535, 105),
         (610, 165), (648, 245), (658, 300), (668, 335), (664, 362), (676, 400), (712, 448), (700, 466), (680, 472),
         (690, 500), (684, 520), (690, 538), (676, 572), (640, 598), (582, 604), (534, 600), (522, 720)]


def cabeza_perfil(id_, x, y, s=1.0, piel="media", con_cerebro=True, espejo=False):
    """Cabeza de perfil mirando a la derecha (cuello abajo). (x, y) = centro del cuello abajo; s=1 → unos 630 px de alto.
    con_cerebro=True: el cerebro se ve «al descubierto» dentro (grupo id_+'_cerebro', hipotálamo id_+'_hipotalamo').
    Devuelve Pieza con .puntos['hipotalamo'], ['ojo'], ['boca'], ['nuca']."""
    pa, pb, pc, pl = PIELES.get(piel, PIELES["media"])
    gid = f"perfilG_{piel}"
    registrar_defs(lg(gid, [(0, pa), (0.6, pb), (1, pc)], 0, 0, 1, 1))
    o = f'<ellipse cx="460" cy="712" rx="230" ry="20" fill="{INK}" opacity="0.12"/>'
    o += f'<path d="{smooth(_HEAD)} Z" fill="url(#{gid})" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'
    o += f'<path d="M 598 336 Q 616 326 634 336" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
    o += f'<ellipse cx="620" cy="350" rx="9" ry="11" fill="{INK}"/><circle cx="617" cy="346" r="3" fill="#FFFFFF"/>'
    o += '<path d="M 590 310 Q 615 298 640 306" fill="none" stroke="#6B4632" stroke-width="8" stroke-linecap="round"/>'
    o += '<ellipse cx="600" cy="420" rx="34" ry="20" fill="#E8897A" opacity="0.35"/>'
    o += f'<path d="M 672 532 Q 660 538 648 534" fill="none" stroke="#9C4D3E" stroke-width="5" stroke-linecap="round"/>'
    o += f'<path d="M 395 380 C 370 350, 380 300, 410 300 C 440 300, 448 340, 430 370" fill="{pb}" stroke="{INK}" stroke-width="6"/>' if not con_cerebro else ""
    if con_cerebro:
        o += g(f"{id_}_cerebro" if id_ else None, _cerebro_local(id_))
    ox, oy = 462, 720
    sx = -s if espejo else s

    def P(px, py):
        return (x + (px - ox) * sx, y + (py - oy) * s)
    body = f'<g transform="translate({f(x)} {f(y)}) scale({f(sx)} {f(s)}) translate({-ox} {-oy})">{o}</g>'
    return Pieza(g(id_, body), {"hipotalamo": P(482, 352), "ojo": P(620, 350), "boca": P(660, 536), "nuca": P(215, 380), "cima": P(430, 88)},
                 (min(P(205, 0)[0], P(712, 0)[0]), y - 632 * s, max(P(205, 0)[0], P(712, 0)[0]), y))


# --------------------------------------------------------------- músculo
def musculo(id_, cx, cy, largo=240, grosor=90, contraido=False, tendones=True):
    """Músculo en tres haces de fibras con tendones. contraido=True: más corto y gordo (tiritar, hacer fuerza).
    Truco de animación: dibuja los dos (ids distintos) en el mismo sitio y alterna hide/pop."""
    if contraido:
        largo, grosor = largo * 0.73, grosor * 1.31
    x0, x1 = cx - largo / 2, cx + largo / 2
    o = ""
    if tendones:
        o += f'<rect x="{f(x0-80)}" y="{f(cy-14)}" width="84" height="28" rx="10" fill="#F4EDE0" stroke="{INK}" stroke-width="5"/>'
        o += f'<rect x="{f(x1-4)}" y="{f(cy-14)}" width="84" height="28" rx="10" fill="#F4EDE0" stroke="{INK}" stroke-width="5"/>'
    for dy in (-1, 0, 1):
        yy = cy + dy * grosor * 0.75
        rr = grosor * 0.42
        o += f'<path d="M {f(x0)} {f(yy)} C {f(x0+40)} {f(yy-rr)}, {f(x1-40)} {f(yy-rr)}, {f(x1)} {f(yy)} C {f(x1-40)} {f(yy+rr)}, {f(x0+40)} {f(yy+rr)}, {f(x0)} {f(yy)} Z" fill="url(#fibG)" stroke="{INK}" stroke-width="5"/>'
        n = int((x1 - x0) / 16)
        for i in range(2, n - 1):
            x = x0 + i * (x1 - x0) / n
            h = rr * (1 - ((x - cx) / (largo / 2)) ** 2) * 0.85
            o += f'<line x1="{f(x)}" y1="{f(yy-h)}" x2="{f(x)}" y2="{f(yy+h)}" stroke="#8E1F1A" stroke-width="3" opacity="0.7"/>'
        o += brillo(f"M {f(x0+50)} {f(yy-rr*0.55)} C {f(x0+90)} {f(yy-rr*0.8)}, {f(x1-90)} {f(yy-rr*0.8)}, {f(x1-50)} {f(yy-rr*0.55)}", 4, 0.8, "#FFD0C8")
    return g(id_, o)


# --------------------------------------------------------------- antebrazo con vello
def antebrazo(id_, p0, p1, ancho=118, piel="media", vello=True, gallina=False, manga="#F0645A", seed=7):
    """Antebrazo (tira de piel de p0 a p1, semiancho `ancho`) con vello y piel de gallina.
    Grupos: id_+'_vello' (pelos tumbados), id_+'_erizado' (pelos de punta), id_+'_bultos' (piel de gallina).
    Para «se pone de punta»: hide de _vello y pop de _erizado + _bultos en la palabra clave.
    manga = color del puño de jersey en p0 (None para no ponerlo)."""
    rnd = random.Random(seed)
    pa, pb, pc, pl = PIELES.get(piel, PIELES["media"])
    L = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
    ux, uy = (p1[0] - p0[0]) / L, (p1[1] - p0[1]) / L
    nx, ny = -uy, ux
    ang = math.degrees(math.atan2(uy, ux))

    def A(t, s_):
        return (p0[0] + ux * L * t + nx * ancho * s_, p0[1] + uy * L * t + ny * ancho * s_)
    gid = f"abG_{id_ or 'ab'}"
    a, b = A(0.5, -1), A(0.5, 1)
    registrar_defs(f'<linearGradient id="{gid}" x1="{f(a[0])}" y1="{f(a[1])}" x2="{f(b[0])}" y2="{f(b[1])}" gradientUnits="userSpaceOnUse">'
                   f'<stop offset="0" stop-color="{pa}"/><stop offset="0.45" stop-color="{pb}"/><stop offset="1" stop-color="{pc}"/></linearGradient>')
    top = [A(t / 20, -1) for t in range(21)]
    bot = [A(t / 20, 1) for t in range(20, -1, -1)]
    o = f'<path d="{poly(top + bot, True)}" fill="url(#{gid})"/>'
    m0, m1, m2 = A(0.08, 0.15), A(0.45, 0.35), A(0.7, 0.2)
    o += f'<path d="M {f(m0[0])} {f(m0[1])} C {f(A(0.3,0)[0])} {f(A(0.3,0)[1])}, {f(m1[0])} {f(m1[1])}, {f(m2[0])} {f(m2[1])}" fill="none" stroke="#B9A0C8" stroke-width="7" opacity="0.35" stroke-linecap="round"/>'
    o += f'<path d="{poly(top)}" fill="none" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>'
    o += brillo(poly([A(t / 20, -0.86) for t in range(21)]), 5, 0.8, "#FFE6D6")
    o += f'<path d="{poly([A(t / 20, 1) for t in range(21)])}" fill="none" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>'
    P = []
    for i in range(26):
        for j in range(5):
            t = (i + 0.5 + (j % 2) * 0.5) / 26 + rnd.uniform(-0.008, 0.008)
            s_ = -0.72 + j * 0.36 + rnd.uniform(-0.08, 0.08)
            if t > 0.19 and t < 0.98:
                P.append(A(t, s_))
    if gallina:
        o += g(f"{id_}_bultos" if id_ else None, "".join(
            f'<ellipse cx="{f(x+2)}" cy="{f(y+3)}" rx="13" ry="9" fill="#B87452" opacity="0.35"/>'
            f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="12" ry="9" fill="url(#bumpR)" stroke="#C07A58" stroke-width="2"/>'
            f'<ellipse cx="{f(x-4)}" cy="{f(y-3)}" rx="4" ry="2.5" fill="#FFFFFF" opacity="0.7"/>' for x, y in P))
    if vello:
        for nombre, off in (("vello", -4), ("erizado", -62)):
            hs = ""
            for x, y in P:
                a_ = math.radians(ang + off + rnd.uniform(-6, 6))
                hs += f'<line x1="{f(x)}" y1="{f(y)}" x2="{f(x + 30*math.cos(a_))}" y2="{f(y + 30*math.sin(a_))}" stroke="#3B271B" stroke-width="3.2" stroke-linecap="round"/>'
            o += g(f"{id_}_{nombre}" if id_ else None, hs)
    if manga:
        def band(t0, t1, k):
            return poly([A(t0, -k), A(t1, -k), A(t1, k), A(t0, k)], True)
        o += f'<path d="{band(-0.05, 0.16, 1.16)}" fill="{degradado(manga, 0.2)}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'
        o += f'<path d="{band(0.115, 0.175, 1.2)}" fill="{degradado(manga, 0.2)}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'
        o += f'<g stroke="{shade(manga,-0.35)}" stroke-width="4">' + "".join(
            f'<line x1="{f(A(0.115,s_)[0]+ux*4)}" y1="{f(A(0.115,s_)[1]+uy*4)}" x2="{f(A(0.175,s_)[0]-ux*4)}" y2="{f(A(0.175,s_)[1]-uy*4)}"/>' for s_ in [x / 10 for x in range(-10, 11, 2)]) + "</g>"
    return Pieza(g(id_, o), {"centro": A(0.6, 0), "punto_lupa": A(0.66, -0.25)})


def piel_lupa(cx, cy, r, erizado=True, piel="media"):
    """Contenido para base.lupa(): perfil de piel con tres bultos y pelos de punta (vista ampliada)."""
    pa, pb, pc, pl = PIELES.get(piel, PIELES["media"])
    sy = cy + r * 0.4
    x0, x1 = cx - r * 1.1, cx + r * 1.1
    prof = f"M {f(x0)} {f(sy)} "
    domes = [(cx - r * 0.76, r * 0.25), (cx, r * 0.29), (cx + r * 0.76, r * 0.25)]
    for dx, w in domes:
        prof += f"L {f(dx-w*1.3)} {f(sy)} C {f(dx-w*0.8)} {f(sy)}, {f(dx-w*0.7)} {f(sy-r*0.2)}, {f(dx)} {f(sy-r*0.2)} C {f(dx+w*0.7)} {f(sy-r*0.2)}, {f(dx+w*0.8)} {f(sy)}, {f(dx+w*1.3)} {f(sy)} "
    prof += f"L {f(x1)} {f(sy)}"
    o = f'<path d="{prof} L {f(x1)} {f(cy+r*1.2)} L {f(x0)} {f(cy+r*1.2)} Z" fill="{degradado(pb, 0.12)}"/>'
    o += f'<path d="{prof}" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
    for dx, w in domes:
        tip = (dx + r * 0.1, sy - r * (0.85 if erizado else 0.3)) if erizado else (dx + r * 0.6, sy - r * 0.28)
        o += trazo(f"M {f(dx)} {f(sy-r*0.2)} L {f(tip[0])} {f(tip[1])}", 5, "#3B271B", 5)
        o += f'<line x1="{f(dx)}" y1="{f(sy-r*0.13)}" x2="{f(dx-r*0.07)}" y2="{f(sy+r*0.34)}" stroke="#8A4E33" stroke-width="5" stroke-linecap="round" opacity="0.35"/>'
    return o


# --------------------------------------------------------------- termómetro
def termometro(id_, cx, top, h=300, nivel=0.5, col=CORAL, marcas=8, texto=None):
    """Termómetro vertical (tubo de top a top+h, bulbo abajo). La columna va en id_+'_columna'
    (anímala con "grow": sube desde abajo). texto: lectura junto al tubo (p. ej. '39 °C')."""
    w = h * 0.13
    br = w * 1.05
    bot = top + h
    s = f'<rect x="{f(cx-w/2+6)}" y="{f(top+6)}" width="{f(w)}" height="{f(h)}" rx="{f(w/2)}" fill="{INK}" opacity="0.2"/>'
    s += f'<rect x="{f(cx-w/2)}" y="{f(top)}" width="{f(w)}" height="{f(h)}" rx="{f(w/2)}" fill="#FFFFFF" stroke="{INK}" stroke-width="6"/>'
    for i in range(marcas):
        y = top + h * 0.1 + i * h * 0.75 / marcas
        s += f'<path d="M {f(cx+w*0.5)} {f(y)} L {f(cx+w*0.5+(16 if i%2==0 else 9))} {f(y)}" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
    ftop = bot - (h * 0.88) * nivel
    s += g(f"{id_}_columna" if id_ else None, f'<rect x="{f(cx-w*0.22)}" y="{f(ftop)}" width="{f(w*0.44)}" height="{f(bot-ftop+br*0.3)}" rx="{f(w*0.22)}" fill="{col}"/>')
    s += f'<circle cx="{f(cx)}" cy="{f(bot+br*0.6)}" r="{f(br)}" fill="{col}" stroke="{INK}" stroke-width="6"/>'
    s += f'<circle cx="{f(cx-br*0.35)}" cy="{f(bot+br*0.3)}" r="{f(br*0.28)}" fill="#FFFFFF" opacity="0.7"/>'
    s += brillo(f"M {f(cx-w*0.25)} {f(top+w*0.6)} L {f(cx-w*0.25)} {f(bot-w*0.4)}", w * 0.14, 0.8)
    if texto:
        s += T(cx + w * 0.5 + 24, ftop + 12, texto, max(24, h * 0.09), INK, anchor="start", font='font-family="Unbounded" font-weight="900"')
    return Pieza(g(id_, s), {"bulbo": (cx, bot + br * 0.6), "nivel": (cx, ftop)}, (cx - br, top, cx + br, bot + br * 1.6))


# --------------------------------------------------------------- articulación en corte (nudillos)
registrar_defs(
    lg("huesoG", [(0, "#FFF8E8"), (0.55, "#F1E2BF"), (1, "#CDB586")])
    + lg("cartilagoG", [(0, "#F2FBFF"), (1, "#B9DCEB")])
    + rg("sinovialR", [(0, "#FFF4C2", 0.95), (1, "#F7D774", 0.9)], 0.5, 0.5, 0.6)
    + rg("burbujaR", [(0, "#FFFFFF", 0.95), (0.6, "#D9F4FF", 0.75), (1, "#7CC8EE", 0.9)], 0.38, 0.32, 0.7)
    + lg("escanerG", [(0, "#FFFFFF"), (1, "#C9D3E3")])
    + rg("tuboR", [(0, "#4D6FB8"), (1, "#101A33")], 0.5, 0.5, 0.6)
)


def articulacion(id_, cx, cy, s=1.0, abierta=0, burbuja=False, gas=True, capsula=True):
    """Articulación de un nudillo en CORTE, horizontal (≈ 780×330 a s=1): hueso de la mano a la izquierda (cabeza redonda con
    cartílago) y falange a la derecha (base cóncava), dentro de la cápsula llena de líquido sinovial con gas disuelto.
    Sub-ids: _hueso (izq), _falange (der: muévela con move [60, 0] = «separar»), _liquido, _capsula, _gas (puntitos), _burbuja.
    abierta = separación ya aplicada (px locales); la burbuja se dibuja en el hueco de una separación de 60 (o `abierta`).
    Las sub-ids van dentro de un grupo escalado: los move son en unidades locales (× s en pantalla).
    .puntos: hueco (centro de la junta en reposo), burbuja, hueso, falange, capsula (borde de arriba), liquido."""
    o = ""
    ab = abierta
    if capsula:
        cap = (f'd="M -215 -40 C -215 -150, -60 -175, 30 -160 C 120 -150, {f(170+ab)} -120, {f(175+ab)} -40 '
               f'L {f(175+ab)} 40 C {f(170+ab)} 120, 120 150, 30 160 C -60 175, -215 150, -215 40 Z"')
        o += g(f"{id_}_liquido", f'<path {cap} fill="url(#sinovialR)"/>')
        o += g(f"{id_}_capsula", f'<path {cap} fill="none" stroke="{INK}" stroke-width="16" stroke-linejoin="round"/>'
               f'<path {cap} fill="none" stroke="#F08FA4" stroke-width="9" stroke-linejoin="round"/>'
               f'<path d="M -150 -138 C -80 -160, 0 -162, 60 -150" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity="0.6"/>')
    # hueso de la mano (metacarpo): unión de diáfisis + cabeza (contorno limpio con doble capa)
    hx = -110
    hb = (f'<rect x="-400" y="-68" width="300" height="136" fill="{INK}" stroke="{INK}" stroke-width="14"/>'
          f'<circle cx="{hx}" cy="0" r="105" fill="{INK}" stroke="{INK}" stroke-width="14"/>'
          f'<rect x="-400" y="-68" width="300" height="136" fill="url(#huesoG)"/>'
          f'<circle cx="{hx}" cy="0" r="105" fill="url(#cartilagoG)"/>'
          f'<circle cx="{hx - 6}" cy="0" r="90" fill="url(#huesoG)"/>'
          f'<rect x="-400" y="-68" width="290" height="136" fill="url(#huesoG)"/>'
          f'<path d="M -380 -40 L -170 -40" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round" opacity="0.55"/>'
          f'<path d="M -165 -70 A 90 90 0 0 1 -60 -60" fill="none" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round" opacity="0.55"/>'
          + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#D9C18F" opacity="0.6"/>' for x, y, r in
                    ((-330, 20, 7), (-280, -10, 5), (-230, 30, 6), (-190, -20, 5), (-140, 35, 6))))
    o += g(f"{id_}_hueso", hb)
    # falange: base cóncava que abraza la cabeza (arco de radio 135 centrado en la cabeza)
    fb = (f'<path d="M -14 -95 L 400 -72 L 400 72 L -14 95 A 135 135 0 0 0 -14 -95 Z" fill="url(#cartilagoG)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
          f'<path d="M 12 -88 L 396 -68 L 396 68 L 12 88 A 152 152 0 0 0 12 -88 Z" fill="url(#huesoG)"/>'
          f'<path d="M 60 -55 L 380 -45" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round" opacity="0.55"/>'
          + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#D9C18F" opacity="0.6"/>' for x, y, r in
                    ((120, 25, 6), (190, -15, 5), (260, 30, 7), (330, -5, 5))))
    o += f'<g transform="translate({f(ab)} 0)">' + g(f"{id_}_falange", fb) + "</g>"
    if gas:
        gp = ((-20, -120), (40, -128), (95, -100), (-60, -138), (10, 125), (70, 112), (-45, 130), (125, 70), (130, -60), (25, -95), (20, 100))
        o += g(f"{id_}_gas", "".join(f'<circle cx="{x + (ab if x > 0 else 0)}" cy="{y}" r="7" fill="#FFFFFF" stroke="#4FA6D6" stroke-width="3"/>' for x, y in gp))
    sep = ab or 60
    bx, br = (-5 + 25 + sep) / 2, 22 + sep * 0.36
    if burbuja:
        o += g(f"{id_}_burbuja", f'<ellipse cx="{f(bx)}" cy="0" rx="{f(br * 0.95)}" ry="{f(br * 1.5)}" fill="url(#burbujaR)" stroke="{INK}" stroke-width="6"/>'
               f'<ellipse cx="{f(bx - br*0.35)}" cy="{f(-br*0.6)}" rx="{f(br*0.2)}" ry="{f(br*0.35)}" fill="#FFFFFF" opacity="0.9"/>')
    def P(x, y):
        return (cx + x * s, cy + y * s)
    pz = {"hueco": P(10, 0), "burbuja": P(bx, 0), "hueso": P(-280, 0), "falange": P(250 + ab, 0), "capsula": P(-20, -165),
          "liquido": P(60, -135)}
    return Pieza(g(id_, f'<g transform="translate({f(cx)} {f(cy)}) scale({f(s)})">{o}</g>'), pz,
                 (cx - 400 * s, cy - 175 * s, cx + (400 + ab) * s, cy + 175 * s))


def mano(id_, cx, cy, s=1.0, piel="media", espejo=False, puntos_nudillo=True):
    """Mano abierta vista por el dorso, dedos hacia arriba (≈ 260×330 a s=1; (cx, cy) = centro del dorso). espejo=True: pulgar a
    la derecha (otra mano). Sub-ids: _dedos, _pulgar, _nudillos (círculos en los nudillos: pulse/punch al crujir).
    .puntos: nudillos (lista de 4), centro, muneca, puntas (lista de 4)."""
    pa, pb, pc, pl = PIELES.get(piel, PIELES["media"])
    k = -1 if espejo else 1
    def X(x):
        return cx + k * x * s
    def Y(y):
        return cy + y * s
    gp = f"url(#piel_{piel if piel in PIELES else 'media'})"
    o = f'<ellipse cx="{f(cx)}" cy="{f(Y(185))}" rx="{f(110*s)}" ry="{f(14*s)}" fill="{INK}" opacity="0.15"/>'
    o += trazo(f"M {f(X(0))} {f(Y(110))} L {f(X(0))} {f(Y(175))}", 92 * s, pb, 6 * s, cap="butt")  # muñeca
    dedos, nud, puntas, nudp = "", "", [], []
    for i, (x, L) in enumerate(((-54, 112), (-18, 128), (18, 120), (52, 96))):
        y0 = -38
        dedos += trazo(f"M {f(X(x))} {f(Y(y0))} L {f(X(x + (x*0.06)))} {f(Y(y0 - L))}", 31 * s, pb, 6 * s)
        tx, ty = X(x + x * 0.06), Y(y0 - L)
        dedos += f'<ellipse cx="{f(tx)}" cy="{f(ty + 4*s)}" rx="{f(9*s)}" ry="{f(11*s)}" fill="{pa}" stroke="{pl}" stroke-width="{f(2.5*s)}"/>'
        for fr in (0.42, 0.72):  # pliegues de las falanges
            yy = Y(y0 - L * fr)
            dedos += f'<path d="M {f(X(x) - 8*s)} {f(yy)} Q {f(X(x))} {f(yy - 4*s)} {f(X(x) + 8*s)} {f(yy)}" fill="none" stroke="{pl}" stroke-width="{f(3*s)}" stroke-linecap="round"/>'
        nud += f'<circle cx="{f(X(x))}" cy="{f(Y(y0 + 6))}" r="{f(13*s)}" fill="{pa}" stroke="{pl}" stroke-width="{f(3*s)}"/>'
        puntas.append((tx, ty)); nudp.append((X(x), Y(y0 + 6)))
    o += g(f"{id_}_dedos", dedos)
    o += g(f"{id_}_pulgar", trazo(f"M {f(X(-62))} {f(Y(55))} Q {f(X(-112))} {f(Y(30))} {f(X(-128))} {f(Y(-30))}", 34 * s, pb, 6 * s))
    o += (f'<path d="M {f(X(-75))} {f(Y(-40))} C {f(X(-80))} {f(Y(40))}, {f(X(-55))} {f(Y(110))}, {f(X(0))} {f(Y(112))} '
          f'C {f(X(55))} {f(Y(110))}, {f(X(78))} {f(Y(40))}, {f(X(72))} {f(Y(-40))} C {f(X(40))} {f(Y(-56))}, {f(X(-40))} {f(Y(-56))}, {f(X(-75))} {f(Y(-40))} Z" '
          f'fill="{gp}" stroke="{INK}" stroke-width="{f(6*s)}" stroke-linejoin="round"/>')
    o += f'<path d="M {f(X(-50))} {f(Y(-20))} Q {f(X(-60))} {f(Y(40))} {f(X(-35))} {f(Y(85))}" fill="none" stroke="#FFFFFF" stroke-width="{f(6*s)}" stroke-linecap="round" opacity="0.45"/>'
    if puntos_nudillo:
        o += g(f"{id_}_nudillos", nud)
    return Pieza(g(id_, o), {"nudillos": nudp, "centro": (cx, cy), "muneca": (cx, Y(170)), "puntas": puntas},
                 (cx - 140 * s, cy - 175 * s, cx + 140 * s, cy + 190 * s))


def escaner_resonancia(id_, cx, cy, w=520, texto="RM"):
    """Escáner de resonancia magnética de frente (carcasa blanca, túnel oscuro y camilla), ≈ w × 0.95w.
    Sub-ids: _anillo (luz del túnel: pulse), _pantalla (pilotito con texto). .puntos: hueco (centro del túnel), camilla."""
    h = w * 0.86
    r = w * 0.29
    x0, y0 = cx - w / 2, cy - h / 2
    o = f'<rect x="{f(x0 + 14)}" y="{f(y0 + 18)}" width="{f(w)}" height="{f(h)}" rx="{f(w*0.16)}" fill="{INK}" opacity="0.22"/>'
    o += f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" rx="{f(w*0.16)}" fill="url(#escanerG)" stroke="{INK}" stroke-width="8"/>'
    o += f'<path d="M {f(x0 + w*0.12)} {f(y0 + 22)} L {f(x0 + w*0.6)} {f(y0 + 22)}" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round" opacity="0.8"/>'
    o += f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r + 26)}" fill="#E4EAF4" stroke="{INK}" stroke-width="6"/>'
    o += g(f"{id_}_anillo", f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r + 12)}" fill="none" stroke="#5BE0FF" stroke-width="10" opacity="0.85"/>')
    o += f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="url(#tuboR)" stroke="{INK}" stroke-width="7"/>'
    cy_c = cy + r * 0.45
    o += (f'<path d="M {f(cx - r*0.8)} {f(cy_c)} L {f(cx + r*0.8)} {f(cy_c)} L {f(cx + r*1.25)} {f(y0 + h + 40)} L {f(cx - r*1.25)} {f(y0 + h + 40)} Z" '
          f'fill="url(#metalG)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
    o += f'<rect x="{f(cx - r*1.3)}" y="{f(y0 + h + 34)}" width="{f(r*2.6)}" height="26" rx="10" fill="#8F9BB3" stroke="{INK}" stroke-width="6"/>'
    o += g(f"{id_}_pantalla", f'<rect x="{f(x0 + w*0.72)}" y="{f(y0 + h*0.08)}" width="{f(w*0.18)}" height="{f(h*0.1)}" rx="8" fill="#1B1E2B" stroke="{INK}" stroke-width="5"/>'
           + T(x0 + w * 0.81, y0 + h * 0.155, texto, h * 0.06, LIME))
    return Pieza(g(id_, o), {"hueco": (cx, cy), "camilla": (cx, cy_c)}, (x0, y0, x0 + w, y0 + h + 60))

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

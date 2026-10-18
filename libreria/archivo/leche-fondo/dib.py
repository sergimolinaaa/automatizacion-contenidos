import sys, math
sys.path.insert(0, "/home/user/automatizacion-contenidos")
from libreria.svg.base import *
from libreria.svg.personajes import persona
from libreria.svg.objetos import casa as C, tienda as TI, compra as K

OUT = "/home/user/automatizacion-contenidos/content/lote7-04-leche-fondo/"
CHANDAL = "#2E6FD8"
COLS = TI.COLS_PROD


def cliente(id_, x, y, s, expresion="neutral", brazos=("relajado", "explica"), acc=()):
    return persona(id_, x, y, s, "adulto", "clara", "corto", "castano", "jersey", CHANDAL, pantalon_color="#1F4FA8",
                   zapato_color="#FFFFFF", accesorios=acc, expresion=expresion, brazos=brazos)


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


# ================================================================== 0 · gancho (full)
def gancho():
    W, H = 1080, 1920
    VP = (540, 760)
    bx0, bx1, by0, by1 = 360, 720, 560, 900   # pared del fondo
    fondo = f'<rect width="{W}" height="{H}" fill="url(#superPared)"/>'
    # techo
    fondo += f'<path d="M 0 0 L {W} 0 L {bx1} {by0} L {bx0} {by0} Z" fill="#E4EAF4"/>'
    for t in (0.25, 0.5, 0.72):
        a, b = lerp((120, 60), (bx0 + 40, by0 + 10), t), lerp((960, 60), (bx1 - 40, by0 + 10), t)
        hh = 26 * (1 - t) + 8
        fondo += f'<rect x="{f(a[0])}" y="{f(a[1])}" width="{f(b[0]-a[0])}" height="{f(hh)}" rx="{f(hh/2)}" fill="#FFFFFF" stroke="{INK}" stroke-width="3"/>'
    # suelo
    fondo += f'<path d="M {bx0} {by1} L {bx1} {by1} L {W} 1400 L {W} {H} L 0 {H} L 0 1400 Z" fill="url(#superSuelo)"/>'
    for t in (0.15, 0.35, 0.6, 0.9):
        y = by1 + (H - by1) * t * t
        fondo += f'<path d="M 0 {f(y)} L {W} {f(y)}" stroke="#B4BED0" stroke-width="3"/>'
    for k in range(-4, 5):
        fondo += f'<path d="M {f(540+k*45)} {by1} L {f(540+k*330)} {H}" stroke="#B4BED0" stroke-width="3"/>'
    # pared del fondo
    fondo += f'<rect x="{bx0}" y="{by0}" width="{bx1-bx0}" height="{by1-by0}" fill="#D7E0EE" stroke="{INK}" stroke-width="5"/>'

    # estanterías laterales en perspectiva (cara interior)
    def lado(xn, xf, seed):
        o = ""
        top_n, bot_n = 330, 1400
        top_f, bot_f = by0 + 30, by1
        quad = [(xn, top_n), (xf, top_f), (xf, bot_f), (xn, bot_n)]
        o += f'<path d="{poly(quad, True)}" fill="#5A6170" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
        nb = 4
        import random
        rnd = random.Random(seed)
        for b in range(nb):
            u0, u1 = b / nb, (b + 1) / nb
            for j in range(9):
                t0, t1 = j / 9, (j + 0.82) / 9
                def P(t, u):
                    yt = (top_n + (top_f - top_n) * t) + ((bot_n + (bot_f - bot_n) * t) - (top_n + (top_f - top_n) * t)) * u
                    return (xn + (xf - xn) * t, yt)
                uu0 = u0 + (u1 - u0) * rnd.uniform(0.15, 0.35)
                q = [P(t0, uu0), P(t1, uu0), P(t1, u1 - 0.02), P(t0, u1 - 0.02)]
                o += f'<path d="{poly(q, True)}" fill="{COLS[rnd.randrange(len(COLS))]}" stroke="{INK}" stroke-width="2.5"/>'
            def P2(t, u):
                yt = (top_n + (top_f - top_n) * t) + ((bot_n + (bot_f - bot_n) * t) - (top_n + (top_f - top_n) * t)) * u
                return (xn + (xf - xn) * t, yt)
            a, b_ = P2(0, u1), P2(1, u1)
            o += f'<path d="M {f(a[0])} {f(a[1])} L {f(b_[0])} {f(b_[1])}" stroke="#DDE4EF" stroke-width="{f(14)}" stroke-linecap="round"/>'
            o += f'<path d="M {f(a[0])} {f(a[1]+8)} L {f(b_[0])} {f(b_[1]+3)}" stroke="{INK}" stroke-width="3"/>'
        return o
    pas = lado(-10, bx0, 3) + lado(W + 10, bx1, 8)
    # nevera al fondo
    nev = K.nevera("nevera", bx0 + 25, by0 + 30, bx1 - bx0 - 50, by1 - by0 - 40, puertas=3, baldas=3, rotulo="LECHE")
    glow = g("glow", f'<ellipse cx="540" cy="{(by0+by1)/2}" rx="230" ry="200" fill="url(#resplandorY)" opacity="0.9"/>')
    brs = destellos("brillos", 540, 700, 210, LIME, 4)
    # flecha larga hasta el fondo
    fl = flecha("ruta", (470, 1150), (540, 930), col=LIME, w=14, punta=34, ctrl=(640, 1080))
    lejos = etiqueta("tlejos", 800, 1010, "AL FONDO", size=34)
    body = g("pasillo", pas) + glow + nev + brs + fl + lejos
    # cliente
    a = cliente("cli", 250, 1340, 1.12, "neutral", ("relajado", "explica"))
    b = cliente("clit", 250, 1340, 1.12, "triste", ("relajado", "explica"))
    mano = a.puntos["mano_izq"]
    bol = C.bolsa("bolsa", mano[0], mano[1] + 180, 150, 170, "#E9DCC0", "")
    duda = icono_duda("duda", 395, 600, 44)
    body += g("cliente", a + b + g("bolsa_g", bol)) + duda
    guardar(OUT + "gancho_full.svg", svg(body, "full", fondo=fondo))
    return a


# ================================================================== 1 · producto ancla (panel)
def ancla():
    body = ""
    br = K.brick_leche("brik", 190, 360, 1.2, texto="")
    an = K.ancla("ancla", 190, 268, 0.55, "#26304A")
    body += br + an
    body += etiqueta("tancla", 200, 430, "PRODUCTO ANCLA", size=30)
    # carros en fila
    carros = ""
    for i in range(5):
        cx = 120 + i * 190
        c = TI.carrito(f"car{i}", cx, 655, 150, (CORAL, TEAL, YEL, VIO, ROSA)[i], lleno=False)
        bb = K.brick_leche(None, cx - 8, 655 - 150 / 380 * 300 + 8, 0.42)
        carros += g(f"carro{i}", bb + c)
    body += carros
    # caña con brik de cebo
    cana = K.cana_pescar("cana", (520, 300), (900, 90), 170)
    ax, ay = cana.puntos["anzuelo"]
    cebo = g("cebo", f'<path d="M {ax} {ay-170} L {ax} {ay}" stroke="{INK}" stroke-width="4"/>'
             + f'<path d="M {ax} {ay} q 0 14 -12 14" fill="none" stroke="{INK}" stroke-width="5"/>'
             + K.brick_leche(None, ax, ay + 130, 0.5))
    pez = g("pez", f'<g transform="translate(700 330)">'
            f'<path d="M 0 0 C 40 -46 110 -46 140 0 C 110 46 40 46 0 0 Z" fill="{degradado(TEAL, 0.25)}" stroke="{INK}" stroke-width="6"/>'
            f'<path d="M 0 0 L -40 -32 L -40 32 Z" fill="{TEAL}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
            f'<circle cx="108" cy="-8" r="10" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/><circle cx="111" cy="-8" r="4" fill="{INK}"/>'
            f'<path d="M 40 -20 Q 55 0 40 20" fill="none" stroke="{INK}" stroke-width="4"/></g>')
    body += g("cana_g", cana) + cebo + pez
    guardar(OUT + "ancla.svg", svg(body, "panel", fondo=fondo_suave()))


# ================================================================== 2 · plano cenital (free)
def plano():
    H = 930
    x0, x1, y0, y1 = 120, 880, 40, 840
    o = sombra_caja(x0, y0, x1 - x0, y1 - y0, 22, 14, 16, 0.3)
    o += f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" rx="22" fill="#F1F4FA" stroke="{INK}" stroke-width="8"/>'
    o += f'<g stroke="#DCE2EC" stroke-width="2">' + "".join(f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{y1}"/>' for x in range(x0 + 40, x1, 40)) \
        + "".join(f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}"/>' for y in range(y0 + 40, y1, 40)) + "</g>"
    # nevera de lácteos arriba
    o += f'<rect x="{x0+30}" y="{y0+18}" width="{x1-x0-60}" height="70" rx="10" fill="{degradado(K.LECHE_AZUL, 0.25)}" stroke="{INK}" stroke-width="6"/>'
    for k in range(9):
        o += K.brick_leche(None, x0 + 90 + k * 78, y0 + 82, 0.26)
    # entrada abajo
    o += f'<rect x="440" y="{y1-12}" width="120" height="24" fill="#F1F4FA"/>'
    o += f'<path d="M 440 {y1} L 440 {y1-60} M 560 {y1} L 560 {y1-60}" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>'
    # estanterías (barras horizontales con huecos alternos)
    shelves = [(650, 160, 700), (480, 300, 860 - 20), (310, 160, 700)]
    lanes = [(735, "GALLETAS", YEL), (565, "REFRESCOS", CORAL), (395, "LIMPIEZA", TEAL), (220, None, None)]
    luces = ""
    for i, (ly, txt, col) in enumerate(lanes[:3]):
        luces += g(f"luz{i}", f'<rect x="{x0+16}" y="{ly-56}" width="{x1-x0-32}" height="112" rx="16" fill="{col}" opacity="0.32"/>'
)
    o += luces
    import random
    rnd = random.Random(4)
    for sy, sa, sb in shelves:
        o += sombra_caja(sa, sy - 26, sb - sa, 52, 10, 6, 8, 0.25)
        o += f'<rect x="{sa}" y="{sy-26}" width="{sb-sa}" height="52" rx="10" fill="#5A6170" stroke="{INK}" stroke-width="6"/>'
        x = sa + 10
        while x < sb - 30:
            w = rnd.uniform(26, 44)
            o += f'<rect x="{f(x)}" y="{sy-18}" width="{f(w)}" height="36" rx="5" fill="{COLS[rnd.randrange(len(COLS))]}" stroke="{INK}" stroke-width="2.5"/>'
            x += w + 6
    body = g("plano", o)
    # rótulos de pasillo (aparecen con la luz)
    for i, (ly, txt, col) in enumerate(lanes[:3]):
        xx = 330 if i == 1 else 670
        body += etiqueta(f"tl{i}", xx, ly + 24, txt, size=24, bg="#FFFFFF", fg=INK)
    body += etiqueta("tent", 500, y1 + 52, "ENTRADA", size=26)
    body += etiqueta("tlac", 300, y0 + 124, "LÁCTEOS", size=26, bg=K.LECHE_AZUL, fg="#FFFFFF")
    # recorrido
    P = [(500, 790), (500, 710), (790, 710), (790, 540), (215, 540), (215, 370), (790, 370), (790, 215), (500, 215), (500, 140)]
    d = "M " + " L ".join(f"{x} {y}" for x, y in P)
    body += g("ruta", f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="16" stroke-linejoin="round" stroke-linecap="round"/>'
              f'<path d="{d}" fill="none" stroke="{CORAL}" stroke-width="8" stroke-linejoin="round" stroke-linecap="round" stroke-dasharray="18 14"/>')
    body += g("punto", f'<circle cx="500" cy="790" r="30" fill="{INK}" opacity="0.25" transform="translate(4 6)"/>'
              f'<circle cx="500" cy="790" r="30" fill="{degradado(CORAL, 0.25)}" stroke="{INK}" stroke-width="6"/>'
              f'<circle cx="490" cy="780" r="8" fill="#FFFFFF" opacity="0.8"/>')
    guardar(OUT + "plano_free.svg", svg(body, "free", h=H))
    return P


# ================================================================== 3 · compras de impulso (panel)
def impulso():
    body = ""
    li = K.lista_compra("lista", 160, 360, 220, 290, items=("LECHE",), tachadas=(0,), rot_=-5)
    body += li
    body += etiqueta("timp", 620, 92, "IMPULSO = SIN PENSARLO", size=28)
    car = TI.carrito("carro", 600, 650, 400, CORAL, lleno=False)
    body += car
    cx_, cy_ = car.puntos["cesta"]
    # brik ya dentro
    body += K.brick_leche("brikc", 470, 470, 0.55)
    # galletas: empiezan en la estantería de la izquierda (fuera del carro) y saltan
    body += K.galletas("gall", 380, 250, 0.8, AZUL, "GALLETAS")
    body += TI.cartel_precio("oferta", 870, 230, 190, "2x1", None, "", YEL, cinta="OFERTA", rot_=8)
    body += K.chocolate("choco", 690, 330, 0.62, rot_=14)
    guardar(OUT + "impulso.svg", svg(body, "panel", fondo=fondo_suave()))


# ================================================================== 4 · el pan, igual (panel)
def pan():
    body = ""
    # puerta de entrada a la izquierda
    pu = (f'<rect x="50" y="250" width="150" height="330" rx="10" fill="url(#cristalG)" stroke="{INK}" stroke-width="7"/>'
          f'<path d="M 125 250 L 125 580" stroke="{INK}" stroke-width="5"/>'
          f'<rect x="40" y="200" width="170" height="50" rx="10" fill="{LIME}" stroke="{INK}" stroke-width="6"/>'
          + T(125, 236, "ENTRADA", 24, INK, font=DISP) + brillo("M 70 280 L 70 400", 6, 0.8))
    body += g("puerta", pu)
    hor = K.horno_pan("horno", 790, 580, 300, 360)
    body += hor
    # básicos en el centro
    bas = K.barra_pan(None, 450, 330, 230, -18, 50) + K.brick_leche(None, 470, 420, 0.75)
    body += g("basicos", bas)
    body += sello("sbas", 450, 160, "BÁSICOS", 44, -6, CORAL)
    # regla que se estira (dibujada en vertical y girada: grow origin top la alarga hacia la derecha)
    L = 730
    rg_ = f'<rect x="-28" y="0" width="56" height="{L}" rx="8" fill="{degradado(YEL, 0.2, "h")}" stroke="{INK}" stroke-width="6"/>'
    for k in range(0, L - 10, 25):
        ln = 22 if k % 100 == 0 else 12
        rg_ += f'<path d="M -28 {k+12} L {-28+ln} {k+12}" stroke="{INK}" stroke-width="3"/>'
    regla = f'<g transform="translate(110 625) rotate(-90)">{g("regla", rg_)}</g>'
    body += regla
    body += etiqueta("tlejos", 500, 548, "LEJOS DE LA ENTRADA", size=26)
    guardar(OUT + "pan.svg", svg(body, "panel", fondo=fondo_suave()))


# ================================================================== 5 · el frío (full)
def frio():
    W, H = 1080, 1920
    suelo = 1190
    fondo = f'<rect width="{W}" height="{H}" fill="#9CC9EE"/>'
    fondo += nube(170, 300, 0.9) + nube(860, 250, 0.7)
    fondo += f'<rect x="0" y="{suelo}" width="{W}" height="{H-suelo}" fill="#6E7687"/>'
    fondo += "".join(f'<rect x="{x}" y="{suelo+90}" width="90" height="14" rx="7" fill="#E9EDF5" opacity="0.8"/>' for x in range(-20, W, 170))
    fondo += f'<rect x="0" y="{suelo}" width="{W}" height="16" fill="{INK}"/>'
    # edificio: muelle + cámara + tienda
    fondo += f'<rect x="370" y="580" width="720" height="{suelo-580}" fill="#E8EDF5" stroke="{INK}" stroke-width="8"/>'
    fondo += f'<path d="M 350 580 L 1090 580 L 1090 540 L 370 540 Z" fill="#5A6170" stroke="{INK}" stroke-width="7"/>'
    fondo += f'<rect x="335" y="{suelo-120}" width="60" height="120" fill="#9AA3B5" stroke="{INK}" stroke-width="6"/>'
    fondo += f'<rect x="780" y="600" width="20" height="{suelo-600}" fill="#9AA3B5" stroke="{INK}" stroke-width="5"/>'
    body = ""
    # cámara frigorífica
    cam = f'<rect x="405" y="630" width="360" height="{suelo-630}" rx="6" fill="url(#frioG)" stroke="{INK}" stroke-width="7"/>'
    for k in range(5):
        cam += f'<path d="M {425+k*68} 640 q 15 22 30 0 q 15 22 30 0" fill="none" stroke="#FFFFFF" stroke-width="6" opacity="0.9"/>'
    cam += K.palet(None, 490, suelo - 4, 150, 4, 2)
    cam += K.palet(None, 670, suelo - 4, 150, 3, 2)
    body += g("camara", cam)
    body += g("copos", copo(450, 720, 18, 0, "#FFFFFF") + copo(720, 760, 22, 15, "#FFFFFF") + copo(590, 690, 16, 30, "#FFFFFF")
              + copo(440, 900, 14, 10, "#FFFFFF") + copo(735, 930, 16, 40, "#FFFFFF"))
    body += etiqueta("tcam", 585, 440, "CÁMARA FRIGORÍFICA", size=30, apunta=(585, 630), desde=(585, 470))
    body += etiqueta("thab", 585, 512, "TAMAÑO HABITACIÓN", size=24, bg="#FFFFFF", fg=INK)
    # nevera de la tienda
    body += K.nevera("nev", 830, 780, 220, suelo - 780, puertas=1, baldas=3, rotulo="LECHE")
    body += etiqueta("ttienda", 940, 710, "TIENDA", size=26, bg="#FFFFFF", fg=INK)
    # camión que llega marcha atrás (trasera contra el muelle)
    sc = 0.56
    cam_ = K.camion_frigorifico("camion", 340 - 312 * sc, suelo, sc)
    body += cam_
    body += etiqueta("tdet", 200, 860, "DESCARGA DETRÁS", size=26, apunta=(330, 1040), desde=(240, 880))
    # repartidora con carretilla
    rep = persona("rep", 575, suelo, 0.72, "adulto", "morena", "coleta", "negro", "chaqueta", "#FF9F1C",
                  pantalon_color="#2B3A5C", expresion="risa", brazos=("relajado", "explica"), mira=1)
    hx, hy = rep.puntos["mano_der"]
    car = K.carretilla("carr", hx + 14, suelo, (suelo - hy) / 286, 3)
    body += g("reparto", rep + car)
    guardar(OUT + "frio_full.svg", svg(body, "full", fondo=fondo))
    return rep, car


# ================================================================== 6 · tu defensa (free)
def defensa():
    H = 860
    body = ""
    body += sombra(500, 800, 470, 22, 0.2)
    body += f'<rect x="20" y="780" width="960" height="30" rx="12" fill="#DDE4EF" stroke="{INK}" stroke-width="6"/>'
    est = TI.estanteria("est", 300, 640, 230, 2, 260, 6, col="#5A6170")
    body += est
    body += TI.cartel_precio("oferta", 470, 200, 240, "2x1", None, "", YEL, cinta="¡OFERTA!", rot_=-6)
    nev = K.nevera("nev", 700, 300, 260, 480, puertas=1, baldas=3, rotulo="LECHE")
    body += nev
    body += icono_ok("ok", 830, 270, 44)
    a = cliente("cli", 170, 790, 0.82, "risa", ("relajado", "sujeta"), acc=("gafas_sol",))
    mano = a.puntos["mano_der"]
    li = K.lista_compra("lista", mano[0] + 30, mano[1] - 60, 110, 140, items=("LECHE",), tachadas=(), rot_=8, size=17)
    body += g("cliente", a + li)
    guardar(OUT + "defensa_free.svg", svg(body, "free", h=H))
    return a


if __name__ == "__main__":
    import os
    os.makedirs(OUT, exist_ok=True)
    a = gancho()
    print("gancho cli", a.puntos)
    ancla(); P = plano(); impulso(); pan()
    r, c = frio(); print("rep", r.puntos, c.puntos)
    d = defensa(); print("def", d.puntos)

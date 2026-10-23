"""lote8-09-gasto-campana: dibujos del vídeo «¿Cuánto puede gastar un partido en campaña?» (montaje v2).

Método rossark: cada parte es su propio grupo con pivote, las barras salen de su base dentro de un recorte
(se animan con `move`, que es ease-out sin rebote) y los números cuentan con capas que se relevan (fade/hide).
"""
import sys, os
sys.path.insert(0, "/home/user/automatizacion-contenidos")
from libreria.svg.base import *
from libreria.svg.personajes import persona, pictograma
from libreria.svg.objetos import politica as P, escenarios as E, territorio as TE, dinero as D, tienda as TI

OUT = "/home/user/automatizacion-contenidos/content/lote8-09-gasto-campana"
os.makedirs(OUT, exist_ok=True)


def cuenta(prefijo, cx, cy, valores, w, h=120, size=None, **kw):
    """Contador digital que «cuenta»: una capa por valor (ids prefijo_0, prefijo_1… y la última = prefijo)."""
    o = ""
    for i, v in enumerate(valores):
        id_ = prefijo if i == len(valores) - 1 else f"{prefijo}_{i}"
        o += contador(id_, cx, cy, v, w=w, h=h, size=size, **kw)
    return o


# ---------------------------------------------------------------- 1. gancho (full)
def gancho():
    ana = persona("ana", 290, 1300, 1.38, "adulto", "morena", "coleta", "negro", "jersey", TEAL,
                  expresion="duda", brazos=("cintura", "explica"), mira=1)
    saco = D.saco_dinero("saco", 770, 1290, 380, "€")
    mon = ""
    for i, (x, y, r, a) in enumerate(((700, 640, 50, -14), (830, 560, 44, 12), (760, 470, 40, -6))):
        mon += D.moneda_euro(f"mon{i}", x, y, r, a)
    # monedas ya caídas al pie del saco
    suelo = (D.moneda_euro(None, 560, 1268, 40, -10) + D.moneda_euro(None, 990, 1262, 36, 16)
             + D.moneda_euro(None, 610, 1300, 30, 8))
    cal = P.calendario("cal", 960, 560, 170, 190, "NOV", "29", rot_=6)
    duda = icono_duda("duda", 470, 560, 50)
    body = ana + saco + g("suelo_mon", suelo) + mon + cal + duda
    guardar(f"{OUT}/gancho_full.svg", svg(body, "full", fondo=E.habitacion(cuadro=False)))


# ---------------------------------------------------------------- 2. sin posicionarnos (free)
def neutral():
    H = 900
    doc = P.documento("pl_doc", 0, -140, 190, 250, "LEY", "LOREG", rot_=-5)
    car = P.carpeta("pl_car", 0, -100, 210, 165, "CUENTAS")
    bal = TE.balanza("bal", 500, 780, 720, 0, izq=doc, der=car, h=520)
    sp = P.sin_posicionarnos("sello", 500, 110, 54)
    t1 = etiqueta("toficial", 500, 850, "SOLO CUENTAS OFICIALES", bg=INK, fg=LIME, size=34)
    chisp = g("chisp", chispa(None, 120, 210, 30, LIME) + chispa(None, 890, 240, 24, LIME))
    body = bal + chisp + sp + t1
    guardar(f"{OUT}/neutral_free.svg", svg(body, "free", h=H))


# ---------------------------------------------------------------- 3. el tope: 0,37 € por habitante (free)
def tope():
    H = 820
    body = D.linea_tope("tope", 50, 950, 170, "TOPE")
    body += etiqueta("tley", 200, 100, "LOREG, ART. 175", bg=LIME, fg=INK, size=28)
    body += cuenta("c37", 500, 285, ("0,12 €", "0,25 €", "0,37 €"), w=360, h=130)
    body += etiqueta("tpor", 500, 385, "POR HABITANTE", bg=INK, fg=LIME, size=28)
    cols = ("#8C9BB8", "#F2A65A", "#7B5CFF", "#2EC4B6", "#FF7EB6")
    for i, x in enumerate((120, 310, 500, 690, 880)):
        s = 180 + (i % 2) * 14
        body += pictograma(f"hab{i}", x, 640 - (i % 2) * 7, s, cols[i])
        body += D.moneda_euro(f"mon{i}", x, 470 - (i % 2) * 10, 36, (i - 2) * 7)
    body += etiqueta("tdonde", 500, 775, "DONDE PRESENTA CANDIDATURA", bg=CORAL, fg="#FFFFFF", size=28)
    guardar(f"{OUT}/tope.svg", svg(body, "free", h=H))


# ---------------------------------------------------------------- 4. ejemplo: toda España (full)
def espana():
    m = TE.mapa_espana("mapa", 560, 860, 720, puntos=True, ids=False)
    body = m
    body += cuenta("c49", 540, 520, ("40 M", "49 M"), w=380, h=130)
    body += etiqueta("thab", 540, 625, "HABITANTES", bg=INK, fg=LIME, size=36)
    body += etiqueta("tpor", 210, 1185, "× 0,37 €", bg=LIME, fg=INK, size=48)
    body += flecha("fpor", (380, 1185), (450, 1185), col=LIME, w=10, punta=24)
    body += cuenta("c18", 730, 1185, ("≈ 9 M €", "≈ 18 M €"), w=470, h=140)
    body += etiqueta("taprox", 730, 1300, "CÁLCULO APROXIMADO", bg=CORAL, fg="#FFFFFF", size=30)
    guardar(f"{OUT}/espana_full.svg", svg(body, "full", fondo=E.cielo(hora="dia", colinas=False, nubes=True, sol_=False)))


# ---------------------------------------------------------------- 5. subvención por escaño (free)
def escano():
    H = 820
    cx, cy, r0, r1, fl = 500, 730, 150, 400, 7
    h = P.hemiciclo("hemi", cx, cy, 350, fl, r0, r1, "#C9CED8", r_esc=9)
    body = h
    ex, ey = h.puntos["escanos"][230]
    body += g("esc", f'<circle cx="{f(ex)}" cy="{f(ey)}" r="20" fill="{LIME}" stroke="{INK}" stroke-width="6"/>')
    body += onda_expansiva("onda", ex, ey, 34)
    bx, bbase = 185, 300
    body += bandera("bandera", bx + 34, 40, 90, 56, cols=("#C60B1E", "#FFC400", "#FFC400", "#C60B1E"), vertical=False)
    body += D.banco("estado", bx, bbase, 250, rotulo="ESTADO", euro=True)
    # billetes que salen de la puerta del Estado hacia el escaño
    body += g("bil0", TI.billete("b0", bx + 10, bbase - 50, 130, "20", -8))
    body += g("bil1", TI.billete("b1", bx - 10, bbase - 40, 130, "10", 10))
    body += cuenta("c21", 680, 120, ("7.000 €", "14.000 €", "18.000 €", "21.167,64 €"), w=480, h=120, size=58)
    body += etiqueta("tesc", 680, 225, "POR CADA ESCAÑO", bg=INK, fg=LIME, size=30)
    body += etiqueta("tsen", 500, 790, "CONGRESO O SENADO", bg="#FFFFFF", fg=INK, size=28)
    guardar(f"{OUT}/escano.svg", svg(body, "free", h=H))
    return ex, ey


# ---------------------------------------------------------------- 6. subvención por voto (free)
def voto():
    H = 820
    u = P.urna("urna", 320, 740, 380, 400, texto="CONGRESO")
    rx, ry = u.puntos["ranura"]
    body = u
    body += P.sobre(rx, ry - 230, 170, 112, -6, id_="sobre")
    for i, (x, y, a) in enumerate(((600, 330, -12), (700, 250, 6), (800, 320, 14))):
        body += D.moneda_euro(f"m{i}", x, y, 48, a)
    body += cuenta("c81", 720, 470, ("0,30 €", "0,80 €", "0,81 €"), w=330, h=120)
    body += etiqueta("tvoto", 720, 575, "POR VOTO AL CONGRESO", bg=INK, fg=LIME, size=28)
    body += etiqueta("tdip", 690, 680, "SI SACA DIPUTADO", bg=CORAL, fg="#FFFFFF", size=32)
    body += icono_ok("ok", 900, 680, 42)
    guardar(f"{OUT}/voto_free.svg", svg(body, "free", h=H))
    return rx, ry


# ---------------------------------------------------------------- 7. lo gastado en 2023 (free)
def gasto2023():
    H = 820
    base, k = 660, 6.0  # px por millón
    body = etiqueta("t2023", 500, 50, "GENERALES DE 2023", bg=CORAL, fg="#FFFFFF", size=30)
    # 16 partidos con escaño (fichas neutras, sin colores de partido)
    chips = ""
    for i in range(16):
        x = 95 + i * 54
        chips += g(f"p{i}", f'<circle cx="{f(x)}" cy="132" r="21" fill="{degradado("#E7EBF3", 0.2)}" stroke="{INK}" stroke-width="5"/>'
                         + f'<circle cx="{f(x-6)}" cy="126" r="5" fill="#FFFFFF" opacity="0.9"/>')
    body += chips
    body += etiqueta("t16", 500, 200, "16 PARTIDOS CON ESCAÑO", bg=INK, fg=LIME, size=28)
    clip = f'<clipPath id="clipBarras"><rect x="0" y="0" width="1000" height="{base}"/></clipPath>'
    barras = ""
    datos = (("b33", 110, 33, LIME), ("b25", 350, 25, TEAL), ("b58", 640, 58, AMARILLO))
    for id_, x, v, col in datos:
        h = v * k
        w = 190 if id_ != "b58" else 230
        # dibujada ya «crecida» pero desplazada h hacia abajo: un move [0, -h] la hace salir de la base
        barras += g(id_, barra(None, x, base + h, w, h, col=col))
    body += f'<g clip-path="url(#clipBarras)">{barras}</g>'
    body += f'<path d="M 70 {base} L 930 {base}" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>'
    body += T(205, base + 46, "CAMPAÑA", 30, "#FFFFFF", font=DISP, extra=f'stroke="{INK}" stroke-width="7" paint-order="stroke"')
    body += T(445, base + 46, "ENVÍOS", 30, "#FFFFFF", font=DISP, extra=f'stroke="{INK}" stroke-width="7" paint-order="stroke"')
    body += T(755, base + 46, "TOTAL", 30, "#FFFFFF", font=DISP, extra=f'stroke="{INK}" stroke-width="7" paint-order="stroke"')
    vstyle = f'stroke="{INK}" stroke-width="8" paint-order="stroke"'
    body += g("v33", T(205, base - 33 * k - 22, "33 M €", 44, "#FFFFFF", font=DISP, extra=vstyle))
    body += g("v25", T(445, base - 25 * k - 22, "25 M €", 44, "#FFFFFF", font=DISP, extra=vstyle))
    body += g("v58_0", T(755, base - 58 * k - 22, "50 M €", 52, LIME, font=DISP, extra=vstyle))
    body += g("v58", T(755, base - 58 * k - 22, "58 M €", 52, LIME, font=DISP, extra=vstyle))
    body += g("signos", T(320, base - 90, "+", 76, "#FFFFFF", font=DISP, extra=vstyle)
              + T(590, base - 90, "=", 76, "#FFFFFF", font=DISP, extra=vstyle))
    body += etiqueta("tjust", 500, 770, "JUSTIFICADO ANTE EL TRIBUNAL DE CUENTAS", bg="#FFFFFF", fg=INK, size=26)
    guardar(f"{OUT}/gasto2023.svg", svg(body, "free", h=H, defs=clip))


# ---------------------------------------------------------------- 8. nadie superó el tope + quién revisa (full)
def control():
    body = ""
    top_y, base = 545, 745
    body += D.linea_tope("tope", 70, 1010, top_y, "TOPE")
    clip = f'<clipPath id="clipCtrl"><rect x="0" y="0" width="1080" height="{base}"/></clipPath>'
    cols = ("#5B7CFF", "#8FA8FF", "#5B7CFF", "#8FA8FF", "#5B7CFF", "#8FA8FF")
    alturas = (115, 70, 150, 95, 55, 130)
    bars = ""
    for i, (hh, c) in enumerate(zip(alturas, cols)):
        x = 110 + i * 150
        bars += g(f"cb{i}", barra(None, x, base + hh, 100, hh, col=c))
    body += f'<g clip-path="url(#clipCtrl)">{bars}</g>'
    body += f'<path d="M 80 {base} L 1000 {base}" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>'
    body += icono_ok("ok", 975, 650, 50)
    tc = D.banco("tcu", 790, 1290, 400, rotulo="TRIBUNAL DE CUENTAS", euro=True)
    body += tc
    luis = persona("luis", 250, 1310, 0.9, "adulto", "clara", "corto", "canoso", "chaqueta", "#24304D",
                   accesorios=("gafas",), expresion="neutral", brazos=("relajado", "sujeta"), mira=1)
    mx, my = luis.puntos["mano_der"]
    lcx, lcy = mx + 60, my - 70
    lp = lupa("lupa", lcx, lcy, 66, 125, contenido=D.recibo_hipoteca(None, lcx, lcy, 110, 150, "CUENTAS", "PARTIDO", "GASTO"))
    body += luis + lp
    guardar(f"{OUT}/control_full.svg", svg(body, "full", fondo=E.oficina(), defs=clip))


# ---------------------------------------------------------------- 9. recorte propuesto por partido (free)
PARTIDOS_23J = (  # reducción de subvención propuesta por el Tribunal de Cuentas (EFE vía Infobae y The Objective, 28/03/2025)
    ("JUNTS", "#00C3B2", INK, 178508, "178.508 €"),
    ("UPN", "#1F4E9E", "#FFFFFF", 11261, "11.261 €"),
    ("SUMAR", "#E51C55", "#FFFFFF", 7418, "7.418 €"),
    ("PSOE", "#E30613", "#FFFFFF", 7139, "7.139 €"),
    ("VOX", "#63BE21", INK, 3915, "3.915 €"),
    ("PSC", "#D4001A", "#FFFFFF", 55, "55 €"),
)


def partidos():
    H = 900
    body = etiqueta("tlab", 500, 52, "RECORTE PROPUESTO · 23J 2023", bg=CORAL, fg="#FFFFFF", size=36)
    body += etiqueta("ttc", 500, 122, "TRIBUNAL DE CUENTAS, MARZO 2025", bg="#FFFFFF", fg=INK, size=24)
    x0, Lmax, bh = 255, 470, 74
    vmax = PARTIDOS_23J[0][3]
    clip = f'<clipPath id="clipPart"><rect x="{x0}" y="0" width="{1000 - x0}" height="{H}"/></clipPath>'
    barras, chips, vals = "", "", ""
    for i, (nom, col, fg, v, txt) in enumerate(PARTIDOS_23J):
        y = 215 + i * 105
        L = max(8, v / vmax * Lmax)
        # chip con el nombre del partido
        chips += g(f"chip{i}", sombra_caja(40, y - 36, 195, 72, 14, 6, 8, 0.25)
                   + f'<rect x="40" y="{f(y-36)}" width="195" height="72" rx="14" fill="{degradado(col, 0.18)}" stroke="{INK}" stroke-width="6"/>'
                   + brillo(f"M 56 {f(y-22)} L 150 {f(y-22)}", 5, 0.55)
                   + T(137, y + 13, nom, 36 if len(nom) <= 4 else 32, fg, font=DISP))
        # barra (dibujada a la izquierda de la base, fuera del recorte; move [L, 0] la hace salir)
        bar = (f'<rect x="{f(x0 - L + 6)}" y="{f(y - bh/2 + 8)}" width="{f(L)}" height="{f(bh)}" rx="10" fill="{INK}" opacity="0.22"/>'
               f'<rect x="{f(x0 - L)}" y="{f(y - bh/2)}" width="{f(L)}" height="{f(bh)}" rx="{f(min(10, L/2))}" fill="{degradado(col, 0.2)}" stroke="{INK}" stroke-width="{6 if L > 20 else 4}"/>')
        if L > 60:
            bar += brillo(f"M {f(x0 - L + 14)} {f(y - bh/2 + 14)} L {f(x0 - 16)} {f(y - bh/2 + 14)}", 6, 0.55)
        barras += g(f"bar{i}", bar)
        vstyle = f'stroke="{INK}" stroke-width="8" paint-order="stroke"'
        vx = x0 + L + 18
        if i == 0:  # la cifra grande va dentro de su barra y cuenta hacia arriba
            vx, anc = x0 + L - 20, "end"
            for j, t in enumerate(("60.000 €", "120.000 €")):
                vals += g(f"val0_{j}", T(vx, y + 15, t, 44, "#FFFFFF", anchor=anc, font=DISP, extra=vstyle))
        else:
            anc = "start"
        vals += g(f"val{i}", T(vx, y + 15, txt, 44 if i == 0 else 38, "#FFFFFF", anchor=anc, font=DISP, extra=vstyle))
    body += chips
    body += f'<g clip-path="url(#clipPart)">{barras}</g>'
    body += f'<path d="M {x0} 165 L {x0} 790" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>'
    body += vals
    body += etiqueta("tirr", 500, 850, "POR IRREGULARIDADES EN LAS CUENTAS", bg=INK, fg=LIME, size=28)
    guardar(f"{OUT}/partidos_free.svg", svg(body, "free", h=H, defs=clip))


if __name__ == "__main__":
    gancho(); neutral(); tope(); espana()
    print("escaño", escano()); print("ranura", voto())
    gasto2023(); control(); partidos()

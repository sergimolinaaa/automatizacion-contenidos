import sys, os
sys.path.insert(0, "/home/user/automatizacion-contenidos")
from libreria.svg.base import *
from libreria.svg.personajes import persona, pictograma
from libreria.svg.objetos import politica as P, escenarios as E, territorio as TE, dinero as D

OUT = "/home/user/automatizacion-contenidos/content/lote8-09-gasto-campana"
os.makedirs(OUT, exist_ok=True)
GRIS_E = "#C9CED8"


# ---------------------------------------------------------------- 1. gancho (full): ¿cuánto puede gastar?
def gancho():
    ana = persona("ana", 270, 1250, 1.05, "adulto", "morena", "coleta", "negro", "jersey", TEAL,
                  expresion="duda", brazos=("cintura", "explica"), mira=1)
    saco = D.saco_dinero("saco", 760, 1220, 300, "€")
    mon = ""
    for i, (x, y, r, a) in enumerate(((600, 1190, 46, -12), (905, 1200, 40, 14), (650, 1235, 34, 6))):
        mon += D.moneda_euro(f"mon{i}", x, y, r, a)
    cal = P.calendario("cal", 830, 560, 190, 210, "NOV", "29", rot_=6)
    gl = globo("globo", 500, 450, "¿CUÁNTO\nPUEDEN GASTAR?", cola=ana.puntos["boca"], size=40)
    duda = icono_duda("duda", 760, 790, 52)
    tcamp = etiqueta("tcamp", 760, 1300, "CAMPAÑA ELECTORAL", size=30)
    body = ana + saco + mon + cal + duda + tcamp + gl
    guardar(f"{OUT}/gancho_full.svg", svg(body, "full", fondo=E.habitacion(cuadro=False)))


# ---------------------------------------------------------------- 2. sin posicionarnos (free)
def neutral():
    doc = P.documento("doc", 320, 520, 300, 390, "LEY ELECTORAL", "LOREG", rot_=-6)
    car = P.carpeta("car", 730, 560, 280, 210, "CUENTAS")
    sp = P.sin_posicionarnos("sello", 500, 170, 44)
    t1 = etiqueta("toficial", 730, 760, "SOLO CUENTAS OFICIALES", size=28)
    chisp = g("chisp", chispa(None, 540, 370, 34, LIME) + chispa(None, 150, 300, 24, LIME))
    body = doc + car + sp + t1 + chisp
    guardar(f"{OUT}/neutral_free.svg", svg(body, "free", h=900))


# ---------------------------------------------------------------- 3. el tope: 0,37 € por habitante (panel)
def tope():
    body = D.linea_tope("tope", 70, 930, 200, "TOPE")
    body += etiqueta("tley", 230, 110, "LOREG, ART. 175", bg=LIME, fg=INK, size=26)
    cols = ("#8C9BB8", "#F2A65A", "#7B5CFF", "#2EC4B6", "#FF7EB6")
    for i, x in enumerate((150, 325, 500, 675, 850)):
        o = pictograma(None, x, 540, 130, cols[i])
        o += D.moneda_euro(None, x, 395, 34)
        body += g(f"hab{i}", o)
    body += g("c37", D.ficha(None, 500, 300, 300, 130, "0,37 €", "POR HABITANTE", col=AMARILLO))
    body += etiqueta("tdonde", 500, 640, "EN LAS PROVINCIAS DONDE SE PRESENTA", bg=INK, fg=LIME, size=24)
    guardar(f"{OUT}/tope.svg", svg(body, "panel", fondo=fondo_suave()))


# ---------------------------------------------------------------- 4. ejemplo: toda España (full)
def espana():
    m = TE.mapa_espana("mapa", 540, 780, 760, puntos=True, ids=False)
    body = m
    body += contador("c49", 540, 500, "49 M", w=380, h=140)
    body += etiqueta("thab", 540, 615, "HABITANTES", bg=INK, fg=LIME, size=36)
    body += etiqueta("tpor", 250, 1190, "× 0,37 €", bg=LIME, fg=INK, size=46)
    body += contador("c18", 730, 1190, "≈ 18 M €", w=460, h=140)
    body += etiqueta("taprox", 730, 1300, "APROXIMADO", bg=CORAL, fg="#FFFFFF", size=34)
    body += flecha("fpor", (410, 1190), (490, 1190), col=LIME, w=10, punta=24)
    guardar(f"{OUT}/espana_full.svg", svg(body, "full", fondo=E.cielo(hora="dia", colinas=False, nubes=True, sol_=False)))


# ---------------------------------------------------------------- 5. subvención por escaño (panel)
def escano():
    cx, cy, r0, r1, fl = 330, 560, 120, 250, 6
    h = P.hemiciclo("hemi", cx, cy, 350, fl, r0, r1, GRIS_E, r_esc=7)
    body = h
    ex, ey = h.puntos["escanos"][175]
    body += g("esc", f'<circle cx="{f(ex)}" cy="{f(ey)}" r="16" fill="{LIME}" stroke="{INK}" stroke-width="5"/>'
                     + onda_expansiva(None, ex, ey, 30))
    body += etiqueta("tesc", cx, cy + 60, "1 ESCAÑO", bg=LIME, fg=INK, size=30)
    body += D.banco("estado", 820, 470, 250, rotulo="ESTADO", euro=True)
    body += flecha("fpago", (700, 330), (470, 300), col=LIME, curva=-0.25)
    for i, (x, y, a) in enumerate(((620, 250, -10), (540, 270, 8))):
        body += g(f"bil{i}", tienda_billete(f"b{i}", x, y, a))
    body += contador("c21", 720, 610, "21.167,64 €", w=440, h=100)
    body += etiqueta("tsen", 230, 110, "CONGRESO O SENADO", bg=INK, fg=LIME, size=24)
    guardar(f"{OUT}/escano.svg", svg(body, "panel", fondo=fondo_suave()))


def tienda_billete(id_, x, y, a):
    from libreria.svg.objetos import tienda as TI
    return TI.billete(id_, x, y, 150, "20", a)


# ---------------------------------------------------------------- 6. subvención por voto (free)
def voto():
    u = P.urna("urna", 330, 760, 300, 320, texto="CONGRESO")
    body = u
    body += P.sobre(330, 260, 150, 100, -6, id_="sobre")
    for i, (x, y) in enumerate(((620, 300), (720, 380), (820, 300))):
        body += D.moneda_euro(f"m{i}", x, y, 44, (i - 1) * 12)
    body += contador("c81", 720, 520, "0,81 €", w=300, h=110)
    body += etiqueta("tvoto", 720, 615, "POR VOTO", bg=INK, fg=LIME, size=30)
    body += etiqueta("tdip", 720, 720, "SI SACA DIPUTADO", bg=CORAL, fg="#FFFFFF", size=28)
    body += icono_ok("ok", 880, 650, 40)
    body += etiqueta("tsen", 720, 820, "SENADO: 0,32 €", bg="#FFFFFF", fg=INK, size=24)
    guardar(f"{OUT}/voto_free.svg", svg(body, "free", h=900))


# ---------------------------------------------------------------- 7. lo gastado en 2023 (panel)
def gasto2023():
    base = 560
    k = 6.0  # px por millón
    body = etiqueta("t2023", 160, 100, "DATOS DE 2023", bg=CORAL, fg="#FFFFFF", size=28)
    body += etiqueta("t16", 640, 100, "16 PARTIDOS CON ESCAÑO", bg=INK, fg=LIME, size=24)
    body += barra("b33", 130, base, 150, 33 * k, col=LIME, texto="CAMPAÑA", valor="33 M €")
    body += barra("b25", 340, base, 150, 25 * k, col=TEAL, texto="ENVÍO A CASA", valor="25 M €")
    body += barra("b58", 600, base, 170, 58 * k, col=AMARILLO, texto="TOTAL", valor="58 M €")
    body += g("signos", T(310, base - 120, "+", 70, INK, font=DISP) + T(545, base - 120, "=", 70, INK, font=DISP))
    body += g("tjust", D.ficha(None, 880, 380, 180, 140, "TOTAL", "JUSTIFICADO", col="#FFFFFF"))
    body += f'<path d="M 90 {base} L 930 {base}" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
    guardar(f"{OUT}/gasto2023.svg", svg(body, "panel", fondo=fondo_suave()))


# ---------------------------------------------------------------- 8. quién lo controla (full)
def control():
    tc = D.banco("tcu", 740, 1010, 460, rotulo="TRIBUNAL DE CUENTAS", euro=True)
    luis = persona("luis", 230, 1250, 1.0, "adulto", "clara", "corto", "canoso", "chaqueta", "#24304D",
                   accesorios=("gafas",), expresion="neutral", brazos=("relajado", "sujeta"), mira=1)
    mx, my = luis.puntos["mano_der"]
    lcx, lcy = mx + 40, my - 120
    lp = lupa("lupa", lcx, lcy, 72, 115, contenido=D.recibo_hipoteca(None, lcx, lcy, 120, 160, "CUENTAS", "PARTIDO", "GASTO"))
    body = tc + luis + lp
    body += etiqueta("tjun", 540, 470, "JUNTAS ELECTORALES", bg=LIME, fg=INK, size=40)
    body += etiqueta("tnadie", 540, 560, "2023: NADIE SUPERÓ EL TOPE", bg="#FFFFFF", fg=INK, size=34)
    body += etiqueta("ttcu", 740, 1075, "FISCALIZA LAS CUENTAS", bg=INK, fg=LIME, size=32)
    body += sello("spasa", 690, 1190, "SI SE PASA: MENOS SUBVENCIÓN", 30, -5, col=CORAL)
    guardar(f"{OUT}/control_full.svg", svg(body, "full", fondo=E.oficina()))


gancho(); neutral(); tope(); espana(); escano(); voto(); gasto2023(); control()

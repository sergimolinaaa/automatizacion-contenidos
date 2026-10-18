import sys, os
sys.path.insert(0, "/home/user/automatizacion-contenidos")
from libreria.svg.base import *
from libreria.svg.personajes import persona, pictograma, multitud
from libreria.svg.objetos import politica as P, escenarios as E, territorio as TE

OUT = "/home/user/automatizacion-contenidos/content/lote8-02-voto-soria"
os.makedirs(OUT, exist_ok=True)


def sobre_voto(rot_=0):
    return P.sobre(0, -46, 120, 80, rot_, sw=5)


# ---------------------------------------------------------------- 1. gancho (full): balanza Soria / Madrid
def gancho():
    kw = dict(izq=sobre_voto(-6), der=sobre_voto(5), txt_izq="SORIA", txt_der="MADRID")
    eq = TE.balanza("bal_eq", 650, 1235, 560, 0, **kw)
    ti = TE.balanza("bal_ti", 650, 1235, 560, -14, **kw)
    ana = persona("ana", 175, 1250, 1.0, "adulto", "media", "largo", "castano", "jersey", CORAL,
                  expresion="duda", brazos=("relajado", "explica"), mira=1)
    gl = globo("globo", 330, 560, "¿PESAN\nIGUAL?", cola=ana.puntos["boca"], size=40)
    pl, pr = ti.puntos["plato_izq"], ti.puntos["plato_der"]
    t1 = etiqueta("tvoto", 650, 620, "¿1 VOTO = 1 VOTO?", size=30)
    mas = sello("mas", pl[0] + 70, pl[1] + 125, "PESA MÁS", 38, -8)
    x4 = sello("x4", pl[0] + 70, pl[1] + 125, "×4", 70, -8, col=CORAL)
    ley = etiqueta("tley", 760, 500, "LOREG · ART. 162", size=30)
    flecha_baja = flecha("fbaja", (545, pl[1] - 230), (545, pl[1] - 40), col=LIME)
    body = ana + gl + eq + ti + t1 + mas + x4 + ley + flecha_baja
    guardar(f"{OUT}/gancho_full.svg", svg(body, "full", fondo=E.habitacion(cuadro=False)))


# ---------------------------------------------------------------- 2. sin posicionarnos (free)
def ley():
    u = P.urna("urna", 500, 800, 300, 320, texto="CONGRESO")
    doc = P.documento("doc", 205, 520, 250, 320, "LOREG", "ART. 162", rot_=-8)
    ine = tarjeta("ine", 800, 520, 250, 210, acento=LIME,
                  body=T(800, 505, "INE", 64, INK, font=DISP) + T(800, 565, "POBLACIÓN", 26) + T(800, 598, "1 ENE 2025", 22, GRIS_OSC))
    sp = P.sin_posicionarnos("sello", 500, 170, 44)
    t1 = etiqueta("toficial", 500, 300, "DATOS OFICIALES", size=32)
    body = u + doc + ine + sp + t1
    guardar(f"{OUT}/ley_free.svg", svg(body, "free", h=900))


# ---------------------------------------------------------------- 3. hemiciclo: 350 y 2 fijos por provincia
def hemi():
    cx, cy = 500, 560
    h = P.hemiciclo("hemi", cx, cy, 350, 9, 185, 340, "#C9CED8")
    pos = h.puntos["escanos"]
    r = max(6, (340 - 185) / 9 * 0.42)
    idx = [round(i * (len(pos) - 1) / 99) for i in range(100)]
    fijos = ""
    for i in idx:
        x, y = pos[i]
        fijos += (f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{LIME}" stroke="{INK}" stroke-width="4"/>'
                  f'<circle cx="{f(x-r*0.3)}" cy="{f(y-r*0.35)}" r="{f(r*0.28)}" fill="#FFFFFF" opacity="0.7"/>')
    body = h + g("fijos", fijos)
    body += contador("c350", cx, 515, "350", w=200, h=86)
    body += etiqueta("tdip", cx, 628, "DIPUTADOS", size=30)
    body += etiqueta("tfijos", 600, 130, "2 FIJOS × 50 PROVINCIAS = 100", bg=LIME, fg=INK, size=28)
    guardar(f"{OUT}/hemi.svg", svg(body, "panel", fondo=fondo_suave()))


# ---------------------------------------------------------------- 4. mapa: Ceuta, Melilla y reparto por población
def mapa():
    m = TE.mapa_espana("mapa", 560, 300, 600, destacar=("Ceuta", "Melilla"))
    pts_ = m.puntos
    body = m
    body += etiqueta("t2", 860, 110, "2 POR PROVINCIA", size=26)
    ce, me = pts_["Ceuta"], pts_["Melilla"]
    body += etiqueta("tce", ce[0] - 10, ce[1] + 75, "CEUTA 1", apunta=ce, size=24)
    body += etiqueta("tme", me[0] + 120, me[1] + 35, "MELILLA 1", apunta=me, size=24)
    # burbujas de población (radio ∝ raíz de habitantes, aprox.)
    burb = ""
    for i, (nm, rr) in enumerate((("Madrid", 50), ("Barcelona", 44), ("Valencia", 30), ("Sevilla", 27), ("Alicante", 25),
                                  ("Málaga", 25), ("Murcia", 22), ("A Coruña", 20), ("Asturias", 18), ("Bizkaia", 19),
                                  ("Cádiz", 21), ("Illes Balears", 20), ("Las Palmas", 18), ("Santa Cruz de Tenerife", 18))):
        x, y = pts_[nm]
        burb += g(f"b{i}", f'<circle cx="{f(x)}" cy="{f(y)}" r="{rr}" fill="{AZUL}" fill-opacity="0.35" stroke="{INK}" stroke-width="3.5"/>')
    body += g("burbujas", burb)
    body += contador("c248", 860, 470, "248", w=200, h=96)
    body += etiqueta("tpob", 860, 560, "SEGÚN POBLACIÓN", bg=LIME, fg=INK, size=24)
    guardar(f"{OUT}/mapa.svg", svg(body, "panel", fondo=fondo_suave()))


# ---------------------------------------------------------------- 5. Madrid contra Soria (free)
def versus():
    H = 900
    mad = TE.ciudad("ciudad", 40, 470, 520, alto=360, n=6, seed=3)
    madrid = (etiqueta("tmad", 255, 70, "MADRID", bg=INK, fg=LIME, size=36)
              + mad + multitud("gentem", 40, 470, 640, n=8, s=82, seed=2)
              + g("tm7", etiqueta(None, 255, 130, "≈ 7 MILLONES", bg="#FFFFFF", fg=INK, size=28))
              + contador("c38", 255, 760, "38", w=190, h=110) + etiqueta("tdm", 255, 850, "DIPUTADOS", size=26))
    pue = TE.pueblo("pueblo", 750, 520, 380)
    soria = (etiqueta("tsor", 750, 70, "SORIA", bg=INK, fg=LIME, size=36)
             + pue + g("gentes", pictograma(None, 750, 600, 82, "#FFC83D"))
             + g("ts90", etiqueta(None, 750, 130, "≈ 90.000", bg="#FFFFFF", fg=INK, size=28))
             + contador("c2", 750, 760, "2", w=150, h=110) + etiqueta("tds", 750, 850, "DIPUTADOS", size=26)
             + etiqueta("tsolo", 880, 690, "LOS 2 FIJOS", bg=LIME, fg=INK, size=24))
    div = f'<path d="M 500 60 L 500 860" stroke="#FFFFFF" stroke-width="6" stroke-dasharray="18 16" opacity="0.7"/>'
    vs = g("vs", f'<circle cx="500" cy="420" r="46" fill="{CORAL}" stroke="{INK}" stroke-width="6"/>' + T(500, 434, "VS", 36, "#FFFFFF", font=DISP))
    body = div + g("madrid", madrid) + g("soria", soria) + vs
    guardar(f"{OUT}/versus_free.svg", svg(body, "free", h=H))


# ---------------------------------------------------------------- 6. la cuenta: habitantes por diputado
def cuenta():
    def fila(id_, y, n, col):
        out, chunks = "", []
        x0, dx = 220, 36
        full = int(n)
        grupos = [[] for _ in range(4)]
        for i in range(full):
            grupos[min(3, i * 4 // max(full, 1))].append(pictograma(None, x0 + i * dx, y, 58, col, sw=3.5))
        if n - full > 0.01:
            xm = x0 + full * dx
            grupos[3].append(f'<clipPath id="clip_{id_}"><rect x="{f(xm-20)}" y="{f(y-50)}" width="19" height="100"/></clipPath>'
                             f'<g clip-path="url(#clip_{id_})">{pictograma(None, xm, y, 58, col, sw=3.5)}</g>')
        for k, gg in enumerate(grupos):
            out += g(f"{id_}{k}", "".join(gg))
        return out, x0 + n * dx
    leyenda = g("leyenda", pictograma(None, 640, 108, 48, GRIS, sw=3.5) + T(672, 120, "= 10.000 HAB.", 28, INK, anchor="start"))
    def escano(id_, cx, cy):
        return g(id_, f'<circle cx="{cx}" cy="{cy}" r="34" fill="{LIME}" stroke="{INK}" stroke-width="6"/>'
                 f'<circle cx="{cx-10}" cy="{cy-12}" r="9" fill="#FFFFFF" opacity="0.7"/>' + T(cx, cy + 12, "1", 34, INK, font=DISP))
    fs, xs = fila("fs", 270, 4.5, "#FFC83D")
    fm, xm = fila("fm", 480, 18.5, "#8C9BB8")
    body = leyenda
    body += etiqueta("lsor", 115, 200, "SORIA", size=28) + escano("es", 115, 270)
    body += fs + etiqueta("vs45", xs + 100, 270, "45.000", bg=LIME, fg=INK, size=34)
    body += etiqueta("lmad", 115, 410, "MADRID", size=28) + escano("em", 115, 480)
    body += fm + etiqueta("vm185", xm + 0, 400, "185.000", bg=CORAL, fg="#FFFFFF", size=36)
    body += etiqueta("tpor", 520, 600, "HABITANTES POR DIPUTADO", bg="#FFFFFF", fg=INK, size=24)
    guardar(f"{OUT}/cuenta.svg", svg(body, "panel", fondo=fondo_suave()))


gancho(); ley(); hemi(); mapa(); versus(); cuenta()

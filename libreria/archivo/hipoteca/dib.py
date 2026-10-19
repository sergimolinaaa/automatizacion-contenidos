"""SVG de content/lote8-05-hipoteca (¿Por qué tu hipoteca sube o baja? Euríbor + diferencial).
Uso: python3 libreria/archivo/hipoteca/dib.py"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from libreria.svg.base import *  # noqa
from libreria.svg.personajes import persona
from libreria.svg.objetos import casa as K, escenarios as E, politica as P, cuerpo as C, tienda as TI, dinero as D

OUT = ROOT / "content" / "lote8-05-hipoteca"
OUT.mkdir(parents=True, exist_ok=True)


def cifra(id_, cx, cy, txt, col=INK, size=64):
    return g(id_, T(cx, cy + size * 0.36, txt, size, col, font=DISP))


# ---------------------------------------------------------------- 0 y 5. la carta del banco (full)
def gancho():
    body = ""
    pz = persona("ana", 270, 1300, 1.3, "adulto", "media", "largo", "castano", "jersey", CORAL,
                 pantalon_color="#3E5C93", expresion="duda", brazos=("relajado", "explica"))
    body += pz
    rc = D.recibo_hipoteca("recibo", 770, 790, 400, 520, rot_=0)
    body += rc
    cx, cy = rc.puntos["cifra"]
    body += cifra("c0", cx, cy, "710 €")
    body += cifra("c1", cx, cy, "790 €", CORAL)
    body += cifra("c2", cx, cy, "650 €", "#178A4C")
    body += flecha("fsube", (1010, 960), (1010, 650), col=CORAL, w=16, punta=36)
    body += flecha("fbaja", (1010, 650), (1010, 960), col=LIME, w=16, punta=36)
    body += globo("globo", 440, 470, "¿POR QUÉ\nSUBE Y BAJA?", cola=(pz.puntos["boca"][0] + 40, pz.puntos["boca"][1] - 20), size=40)
    body += icono_duda("duda", 560, 640, 40)
    body += K.casita("casa", 860, 1245, 160)
    body += etiqueta("lcasa", 650, 1195, "TU CASA", size=28, bg=LIME, fg=INK)
    # escena 5: revisión
    body += P.calendario("cal", 880, 440, 170, 170, "MESES", "12")
    body += etiqueta("lcada", 760, 1250, "CADA 6 O 12 MESES", size=30, bg=LIME, fg=INK)
    body += D.ficha("feur", 450, 470, 330, 140, "EURÍBOR", "EL ÚLTIMO DATO", col=LIME)
    body += sello("srecal", 770, 1060, "RECALCULADA", size=40, rot_=-7)
    return svg(body, "full", fondo=E.habitacion())


# ---------------------------------------------------------------- 1 y 2. la fórmula (free)
def formula():
    H = 880
    body = ""
    body += etiqueta("lvar", 500, 60, "HIPOTECA VARIABLE", size=34, bg=INK, fg=LIME)
    body += etiqueta("lint", 500, 160, "TU INTERÉS =", size=40, bg="#FFFFFF", fg=INK)
    fe = D.ficha("feur", 255, 340, 360, 190, "EURÍBOR", "SUBE Y BAJA", col=LIME)
    fd = D.ficha("fdif", 745, 340, 380, 190, "DIFERENCIAL", "LO PACTAS", col=CORAL, fg="#FFFFFF")
    body += fe + fd
    body += g("mas", T(500, 375, "+", 110, "#FFFFFF", font=DISP, extra=f'stroke="{INK}" stroke-width="10" paint-order="stroke"'))
    body += flecha("fup", (110, 230), (110, 120), col=CORAL, w=12, punta=28)
    body += flecha("fdown", (190, 120), (190, 230), col=LIME, w=12, punta=28)
    body += P.candado("candado", 905, 225, 80)
    body += sello("nocambia", 745, 515, "NO CAMBIA", size=44, rot_=-7, col=INK, fondo=LIME)
    bk = D.banco("banco", 760, 860, 300, rotulo="TU BANCO")
    body += bk
    pz = persona("tu", 270, 870, 0.55, "joven", "clara", "corto", "negro", "camisa", TEAL,
                 pantalon_color="#3E5C93", expresion="risa", brazos=("relajado", "explica"))
    body += pz
    body += etiqueta("ltu", 130, 600, "TÚ", size=30, bg=LIME, fg=INK)
    body += flecha("fpacto", (400, 700), (590, 700), col=LIME, w=12, punta=28)
    return svg(body, "free", h=H)


# ---------------------------------------------------------------- 3. el Euríbor (panel)
def bancos():
    body = ""
    ba = D.banco("bA", 205, 620, 290, rotulo="BANCO A")
    bb = D.banco("bB", 795, 620, 290, rotulo="BANCO B")
    body += ba + bb
    body += flecha("fpresta", (330, 270), (670, 270), col=LIME, w=12, punta=30, ctrl=(500, 130))
    body += TI.billete("billete", 330, 215, 150, "50", rot_=-8)
    body += etiqueta("leur", 500, 95, "EURÍBOR: SU INTERÉS", size=30, bg=INK, fg=LIME)
    body += D.bandera_ue("ue", 500, 365, 150, 100)
    body += P.calendario("cal", 500, 545, 140, 140, "MESES", "12")
    body += etiqueta("lano", 500, 640, "A UN AÑO", size=26, bg=LIME, fg=INK)
    return svg(body, "panel", fondo=fondo_suave())


# ---------------------------------------------------------------- 4. el BCE (panel)
def bce():
    body = ""
    tb = D.torre_bce("torre", 500, 625, 470)
    body += tb
    body += etiqueta("lbce", 500, 95, "BANCO CENTRAL EUROPEO", size=28, bg=INK, fg=LIME)
    body += g("tA", C.termometro(None, 105, 150, 400, 0.85, CORAL))
    body += g("tB", C.termometro(None, 105, 150, 400, 0.35, CORAL))
    body += etiqueta("linf", 120, 630, "INFLACIÓN", size=24, bg=CORAL, fg="#FFFFFF")
    body += D.palanca("pal", 260, 600, 200, "TIPOS")
    body += etiqueta("lsube", 260, 300, "SUBEN", size=26, bg=CORAL, fg="#FFFFFF")
    body += etiqueta("lbaja", 260, 300, "BAJAN", size=26, bg=LIME, fg=INK)
    for k, hh in enumerate((110, 170, 240)):
        body += barra(f"b{k}", 705 + k * 85, 560, 64, hh, col=(LIME, TEAL, VERDE)[k])
    body += etiqueta("leco", 820, 620, "ECONOMÍA", size=26, bg=LIME, fg=INK)
    body += chispa("chis", 920, 240, 32, YEL)
    body += etiqueta("lsigue", 820, 190, "EURÍBOR LO SIGUE", size=22, bg="#FFFFFF", fg=INK)
    return svg(body, "panel", fondo=fondo_suave())


# ---------------------------------------------------------------- 6 y 7. el ejemplo (panel)
def ejemplo():
    body = ""
    body += sello("inventado", 650, 80, "EJEMPLO INVENTADO", size=34, rot_=-4)
    body += K.casita("casa", 200, 330, 250)
    body += etiqueta("l150", 200, 380, "150.000 €", size=34, bg=LIME, fg=INK)
    body += P.calendario("cal", 200, 540, 160, 160, "AÑOS", "25")
    # fórmula
    body += D.ficha("e2", 520, 225, 210, 120, "2 %", "EURÍBOR", col=LIME)
    body += D.ficha("e3", 520, 225, 210, 120, "3 %", "EURÍBOR", col=YEL)
    body += g("mas1", T(655, 250, "+", 70, INK, font=DISP))
    body += D.ficha("dif", 790, 225, 180, 120, "1 %", "DIFERENCIAL", col=CORAL, fg="#FFFFFF")
    body += g("igual", T(650, 350, "PAGAS AL MES", 28, INK))
    body += contador("c710", 650, 440, "710 €", w=380, h=130)
    body += contador("c790", 650, 440, "790 €", w=380, h=130, col=CORAL)
    body += etiqueta("lmas80", 650, 580, "UNOS 80 € MÁS", size=30, bg=CORAL, fg="#FFFFFF")
    body += flecha("fup", (880, 520), (880, 390), col=CORAL, w=12, punta=28)
    return svg(body, "panel", fondo=fondo_suave())


if __name__ == "__main__":
    guardar(OUT / "gancho_full.svg", gancho())
    guardar(OUT / "formula_free.svg", formula())
    guardar(OUT / "bancos.svg", bancos())
    guardar(OUT / "bce.svg", bce())
    guardar(OUT / "ejemplo.svg", ejemplo())

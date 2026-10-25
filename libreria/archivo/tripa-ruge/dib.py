"""lote9-04-tripa-ruge: dibujos de «¿Por qué te ruge la tripa?».
Uso: python3 libreria/archivo/tripa-ruge/dib.py

Método rossark: cada parte es su propio grupo con pivote (cabeza en el cuello, escoba en las manos, baquetas en la
muñeca), cada repetido con su fase, y las caras cambian con capas que se relevan (hide/fade), nunca de golpe.
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from libreria.svg.base import *  # noqa
from libreria.svg.personajes import persona
from libreria.svg.objetos import casa as K, cuerpo as C, politica as P, aviones as AV

OUT = ROOT / "content" / "lote9-04-tripa-ruge"
OUT.mkdir(parents=True, exist_ok=True)
VERDE_JERSEY = "#2FA36B"


def companero(id_, x, y, s, mira, **kw):
    """Compañero de clase en dos capas iguales (mirando al frente / girado hacia ella) para relevarlas con hide/fade."""
    a = persona(f"{id_}a", x, y, s, mira=0, pose="busto", **kw)
    b = persona(f"{id_}b", x, y, s, mira=mira, pose="busto", **{**kw, "expresion": "sorpresa"})
    return g(id_, a + b)


# ---------------------------------------------------------------- 0. gancho: el examen en silencio (full)
def gancho():
    body = ""
    # pizarra al fondo
    body += K.pizarra("piz", 265, 560, 400, 190, contenido=T(265, 548, "EXAMEN", 58, "#F4F1E6", font=DISP)
                      + T(265, 610, "¡SILENCIO!", 34, "#F4F1E6"))
    body += K.reloj("rel", 920, 520, 58, 10, 10, col_marco=TEAL)
    # fila de atrás: tres compañeros con sus pupitres (dos capas cada uno para girar la cabeza hacia ella)
    body += companero("c1", 130, 930, 0.72, 1, edad="joven", piel="clara", pelo="rizado", pelo_color="negro", ropa="camiseta",
                      ropa_color="#FF7EB6", brazos=("relajado", "relajado"), expresion="neutral")
    body += companero("c2", 330, 880, 0.52, 1, edad="joven", piel="morena", pelo="corto", pelo_color="castano", ropa="camiseta",
                      ropa_color="#FFC83D", brazos=("relajado", "relajado"), expresion="neutral")
    body += companero("c3", 950, 930, 0.72, -1, edad="joven", piel="oscura", pelo="rapado", pelo_color="negro", ropa="camiseta",
                      ropa_color="#7B5CFF", brazos=("relajado", "relajado"), expresion="neutral", accesorios=("gafas",))
    body += K.mesa(None, 330, 880, 170, 120, grosor=18)
    for x in (130, 950):
        body += K.mesa(None, x, 930, 250, 150, grosor=22)
    # protagonista sentada, con las manos en la tripa
    lu = persona("lu", 560, 1300, 1.5, "joven", "media", "coleta", "castano", "jersey", VERDE_JERSEY, pose="sentado",
                 expresion="sorpresa", brazos=("junta", "junta"))
    ox, oy = lu.puntos["ojos"]
    rub = (f'<ellipse cx="{f(ox-66)}" cy="{f(oy+40)}" rx="30" ry="16" fill="#FF6F8A" opacity="0.8"/>'
           f'<ellipse cx="{f(ox+66)}" cy="{f(oy+40)}" rx="30" ry="16" fill="#FF6F8A" opacity="0.8"/>')
    body += g("luG", lu + g("rubor", rub))
    bx, by = lu.puntos["manos"]
    body += g("ondasL", ondas_sonido(None, bx - 205, by - 80, 50, 3, 150, 210, 30, 12, LIME))
    body += g("ondasR", ondas_sonido(None, bx + 205, by - 80, 50, 3, -30, 30, 30, 12, LIME))
    body += K.mesa("pupitre", 560, 1095, 660, 200, grosor=30)
    body += P.documento("examen", 790, 1062, 190, 120, "EXAMEN", "", rot_=-6, lineas=3)
    body += P.boli("boli", 700, 1080, 120, -25)
    body += onomatopeya("grrr", 190, 1150, "¡GRRR!", r=125, size=52, rot_=-10)
    guardar(f"{OUT}/gancho_full.svg", svg(body, "full", fondo=AV.aula()))


# ---------------------------------------------------------------- 1. borborigmos: nombre griego (free)
def griego():
    H = 820
    body = K.columna_griega("col", 125, 790, 600, 96)
    body += K.pergamino("perg", 590, 200, 560, 240, "βορβορυγμός", 64, "GRIEGO ANTIGUO")
    pal = "BORBORIGMOS"
    size = 72
    anchos = [size * {"I": 0.42, "M": 1.02, "O": 0.92, "G": 0.9}.get(ch, 0.84) for ch in pal]
    x = 600 - sum(anchos) / 2
    for i, ch in enumerate(pal):
        body += g(f"l{i}", T(x + anchos[i] / 2, 545, ch, size, LIME, font=DISP, extra=f'stroke="{INK}" stroke-width="9" paint-order="stroke"'))
        x += anchos[i]
    body += etiqueta("truido", 600, 680, "= RUIDOS DE LA TRIPA", bg=INK, fg=LIME, size=36)
    body += g("ondas1", ondas_sonido(None, 940, 680, 30, 3, -50, 50, 22, 8, "#FFFFFF"))
    guardar(f"{OUT}/griego_free.svg", svg(body, "free", h=H))


# ---------------------------------------------------------------- 2. un tubo que aprieta (free)
def _bolitas(id_, pts, tipo):
    o = ""
    for i, (x, y) in enumerate(pts):
        if tipo == "comida":
            o += g(f"{id_}{i}", f'<circle cx="{f(x)}" cy="{f(y)}" r="15" fill="{degradado("#9A5B2E", 0.3)}" stroke="{INK}" stroke-width="5"/>'
                   f'<circle cx="{f(x-5)}" cy="{f(y-5)}" r="4" fill="#FFFFFF" opacity="0.6"/>')
        elif tipo == "liquido":
            o += g(f"{id_}{i}", gota(x, y, 30, "#5BC0FF"))
        else:
            o += g(f"{id_}{i}", f'<circle cx="{f(x)}" cy="{f(y)}" r="14" fill="#FFFFFF" fill-opacity="0.85" stroke="{INK}" stroke-width="4"/>'
                   f'<circle cx="{f(x-4)}" cy="{f(y-4)}" r="3.5" fill="#FFFFFF"/>')
    return o


def tubo():
    H = 900
    ad = C.aparato_digestivo("ad", 290, 450, 0.98)
    body = ad
    # comida, líquido y aire dentro del estómago y del delgado
    body += _bolitas("com", [(330, 300), (372, 330), (410, 300)], "comida")
    body += _bolitas("liq", [(250, 560), (330, 600), (200, 640)], "liquido")
    body += _bolitas("air", [(380, 560), (250, 720), (360, 690)], "aire")
    body += etiqueta("ttubo", 780, 150, "TUBO DIGESTIVO", bg=INK, fg=LIME, size=30, apunta=ad.puntos["esofago"])
    # pasta de dientes: normal / estrujada en el mismo sitio
    px, py = 790, 600
    body += g("pasta", K.tubo_pasta("pasta1", px, py, 1.15))
    body += g("pastaE", K.tubo_pasta("pasta2", px, py, 1.15, estrujado=True))
    body += flecha("fpi", (620, 620), (705, 620), col=LIME, w=12, punta=28)
    body += flecha("fpd", (965, 620), (880, 620), col=LIME, w=12, punta=28)
    body += etiqueta("taprieta", 790, 840, "APRIETA Y EMPUJA", bg=LIME, fg=INK, size=32)
    guardar(f"{OUT}/tubo_free.svg", svg(body, "free", h=H))


# ---------------------------------------------------------------- 3. el barrendero: complejo motor migratorio (full)
def barrendero():
    body = ""
    # ola de limpieza: anillos lima que vienen desde el fondo del túnel
    for i in range(2):
        body += g(f"anillo{i}", f'<ellipse cx="540" cy="790" rx="420" ry="300" fill="none" stroke="{INK}" stroke-width="30" opacity="0.5"/>'
                  f'<ellipse cx="540" cy="790" rx="420" ry="300" fill="none" stroke="{LIME}" stroke-width="18"/>')
    # banda de la ola que barre el suelo
    d = "M 40 1010 " + " ".join(f"Q {x+60} {960 if (x//120)%2==0 else 1060} {x+120} 1010" for x in range(40, 1000, 120))
    body += g("ola", trazo(d, 16, LIME, 10))
    body += K.reloj("rel", 920, 570, 86, 12, 0, col_marco=TEAL)
    body += etiqueta("t2h", 920, 700, "+2 HORAS", bg=LIME, fg=INK, size=32)
    body += etiqueta("tcmm", 450, 500, "COMPLEJO MOTOR MIGRATORIO", bg=INK, fg=LIME, size=32)
    body += etiqueta("tola", 450, 570, "= OLA DE LIMPIEZA", bg=LIME, fg=INK, size=30)
    # restos que se barren
    import random as _r
    rnd = _r.Random(3)
    restos = ""
    for i in range(7):
        x, y = 680 + i * 46 + rnd.uniform(-12, 12), 1268 + rnd.uniform(-14, 10)
        col = ("#9A5B2E", "#6E9E3A", "#C98B55")[i % 3]
        restos += g(f"r{i}", f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(rnd.uniform(14, 22))}" ry="{f(rnd.uniform(9, 14))}" fill="{degradado(col, 0.3)}" stroke="{INK}" stroke-width="5" transform="rotate({f(rnd.uniform(-30, 30))} {f(x)} {f(y)})"/>')
    body += g("restos", restos)
    # barrendero
    bar = persona("barr", 260, 1290, 1.12, "adulto", "clara", "corto", "canoso", "camisa", "#FF8A1E", pantalon_color="#FF8A1E",
                  zapato_color="#2A2F3E", camisa_color="#FFC83D", accesorios=("bigote",), expresion="risa", brazos=("sujeta", "relajado"))
    mi, md = bar.puntos["mano_izq"], bar.puntos["mano_der"]
    ux, uy = md[0] - mi[0], md[1] - mi[1]
    L = (ux * ux + uy * uy) ** 0.5
    ux, uy = ux / L, uy / L
    p0 = (mi[0] - ux * 40, mi[1] - uy * 40)
    k = (1195 - mi[1]) / uy
    p1 = (mi[0] + ux * k, mi[1] + uy * k)
    esc = K.escoba("esc", p0, p1, 1.0)
    body += g("barrG", bar + esc)
    # franjas reflectantes del mono
    guardar(f"{OUT}/barrendero_full.svg", svg(body, "full", fondo=C.intestino_interior()))
    return bar


# ---------------------------------------------------------------- 4. suena a tambor (free)
def tambor():
    H = 860
    ec = C.estomago_corte("ec", 265, 400, 0.84, nivel=0.2)
    body = ec
    body += etiqueta("taire", 265, 120, "AIRE", bg="#FFFFFF", fg=INK, size=32, apunta=ec.puntos["aire"])
    body += etiqueta("tliq", 265, 680, "LÍQUIDO", bg="#5BC0FF", fg=INK, size=32, apunta=ec.puntos["charco"])
    body += g("ondasE", ondas_sonido(None, 545, 330, 50, 4, -45, 45, 34, 11, LIME))
    body += onda_expansiva("onda1", 805, 560, 150) + onda_expansiva("onda2", 805, 560, 150)
    body += K.tambor("tam", 805, 800, 290, 210)
    body += sello("svacio", 800, 170, "VACÍO", size=54, rot_=-8)
    guardar(f"{OUT}/tambor_free.svg", svg(body, "free", h=H))


# ---------------------------------------------------------------- 5. no es el estómago: el intestino delgado (free)
def delgado():
    H = 900
    ad = C.aparato_digestivo("ad2", 300, 450, 0.98)
    body = ad
    ex, ey = ad.puntos["estomago"]
    body += aspa("xest", ex, ey, 70)
    body += etiqueta("test", 720, 200, "ESTÓMAGO", bg="#FFFFFF", fg=INK, size=32, apunta=(ex + 60, ey - 40))
    body += icono_no("notest", 900, 200, 40)
    dx, dy = ad.puntos["delgado"]
    body += flecha("fdel", (720, 605), (dx + 120, dy), col=LIME, w=14, punta=34, curva=0.2)
    body += etiqueta("tdel", 730, 560, "INTESTINO DELGADO", bg=LIME, fg=INK, size=32)
    body += g("ruido", ondas_sonido(None, 470, 640, 40, 3, -45, 45, 26, 9, "#FFFFFF"))
    body += g("ruido2", ondas_sonido(None, 120, 640, 40, 3, 135, 225, 26, 9, "#FFFFFF"))
    body += icono_ok("okdel", 890, 470, 40)
    guardar(f"{OUT}/delgado_free.svg", svg(body, "free", h=H))


if __name__ == "__main__":
    import sys as _s
    que = _s.argv[1:] or ["gancho", "griego", "tubo", "barrendero", "tambor", "delgado"]
    for n in que:
        globals()[n]()

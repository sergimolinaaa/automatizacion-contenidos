"""SVG de content/lote8-08-cambio-hora (¿Este domingo es el último cambio de hora?).
Uso: python3 libreria/archivo/cambio-hora/dib.py"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from libreria.svg.base import *  # noqa
from libreria.svg.personajes import persona
from libreria.svg.objetos import casa as K, escenarios as E, politica as P, dinero as D, memoria as M, vuelo as V
from libreria.svg.objetos import tiempo as TM

OUT = ROOT / "content" / "lote8-08-cambio-hora"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1080, 1920
SY = H * 0.69
VX, VY, VW, VH = W * 0.3, SY * 0.36, W * 0.3, SY * 0.36  # ventana de habitacion()


def cuerpo_en_cama(pid, expresion, brazos, pelo_color="castano"):
    return persona(pid, 600, 1185, 1.25, "adulto", "media", "largo", pelo_color, "camiseta", "#7B5CFF",
                   expresion=expresion, pose="busto", brazos=brazos)


def dormitorio(personas):
    """Cama con varias personas superpuestas (mismo sitio, distinta cara) entre cabecero y edredón."""
    detras, delante = TM.cama("cama", 600, 1320, 780, col="#2EC4B6")
    body = detras
    for p in personas:
        body += p
    body += delante
    me = TM.mesilla("mesilla", 105, 1320, 170, 200)
    body += me
    return body, me


def bandera_h(id_, cx, cy, w, h, cols):
    """Bandera de franjas horizontales (España con 4 franjas = 1:2:1, Alemania, Polonia, Países Bajos)."""
    x0, y0 = cx - w / 2, cy - h / 2
    o = sombra_caja(x0, y0, w, h, 8, 7, 9, 0.25)
    o += f'<clipPath id="{id_}_c"><rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" rx="8"/></clipPath><g clip-path="url(#{id_}_c)">'
    n = len(cols)
    for i, c in enumerate(cols):
        o += f'<rect x="{f(x0)}" y="{f(y0 + h * i / n)}" width="{f(w)}" height="{f(h / n + 1)}" fill="{c}"/>'
    o += "</g>" + f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" rx="8" fill="none" stroke="{INK}" stroke-width="6"/>'
    o += brillo(f"M {f(x0+10)} {f(y0+12)} L {f(x0+w*0.4)} {f(y0+12)}", 4, 0.5)
    return g(id_, o)


# ---------------------------------------------------------------- 0 y 1. la noche del cambio (full)
def gancho():
    pz = cuerpo_en_cama("ana", "duda", ("relajado", "senala"))
    body, me = dormitorio([pz])
    tx, ty = me.puntos["tablero"]
    body += TM.despertador("d3", tx, ty, 180, "3:00")
    body += TM.despertador("d2", tx, ty, 180, "2:00", col_txt="#FFD23F")
    body += TM.despertador("d1", tx, ty, 180, "1:00", col_txt=CORAL)
    # reloj de pared a las 3:00 y flecha de retrasar
    body += K.reloj("rel", 845, 520, 112, 3, 0, col_marco=CORAL)
    body += TM.flecha_atras("fatras", 845, 520, 165, a0=70, a1=-40)
    body += etiqueta("lmenos", 845, 760, "UNA HORA ATRÁS", size=28, bg=LIME, fg=INK)
    body += globo("globo", 420, 700, "¿EL ÚLTIMO\nCAMBIO?", cola=(pz.puntos["boca"][0] - 40, pz.puntos["boca"][1] - 60), size=42)
    body += P.calendario("cal", 180, 880, 150, 150, "OCT", "25")
    body += etiqueta("lmadr", 600, 1250, "MADRUGADA DEL SÁBADO AL DOMINGO", size=26, bg=INK, fg=LIME)
    # escena 1: Canarias
    islas = ""
    for (x, y, rx, ry) in ((-150, 10, 34, 20), (-85, -6, 26, 18), (-30, 12, 38, 22), (40, -4, 30, 20), (100, 10, 24, 16), (150, -10, 18, 14), (190, 2, 16, 12)):
        islas += f'<ellipse cx="{f(420+x)}" cy="{f(650+y)}" rx="{rx}" ry="{ry}" fill="{degradado("#E9C27A", 0.2)}" stroke="{INK}" stroke-width="5"/>'
    can = tarjeta("can", 420, 680, 470, 270, acento=TEAL,
                  body=T(420, 600, "CANARIAS", 44, INK, font=DISP) + islas
                  + T(420, 775, "2:00 → 1:00", 56, CORAL, font=DISP))
    body += can
    body += icono_duda("duda", pz.puntos["cima"][0] + 120, pz.puntos["cima"][1] + 10, 42)
    return svg(body, "full", fondo=E.habitacion(noche=True, cuadro=False))


# ---------------------------------------------------------------- 2. para qué (free)
def sol_free():
    Hh = 900
    body = ""
    # suelo
    body += (f'<path d="M 0 700 C 200 660, 380 690, 520 676 C 700 660, 860 690, 1000 670 L 1000 {Hh} L 0 {Hh} Z" '
             f'fill="{degradado("#5FB86E", 0.15)}" stroke="{INK}" stroke-width="7"/>')
    body += brillo("M 30 702 C 200 668, 380 694, 520 682", 5, 0.6, "#B5F08F")
    body += E.sol("sol", 190, 420, 75)
    body += flecha("fluz", (290, 400), (430, 560), col=YEL, w=12, punta=30, curva=0.15)
    body += K.casita("casa", 560, 760, 330)
    body += etiqueta("lsol", 190, 260, "LUZ DEL SOL", size=30, bg=YEL, fg=INK)
    xs = (640, 780, 920)
    for i, x in enumerate(xs):
        body += K.bombilla(f"bon{i}", x, 160, 105, encendida=True)
        body += K.bombilla(f"boff{i}", x, 160, 105, encendida=False)
    body += etiqueta("lmenos", 780, 300, "MENOS BOMBILLAS", size=30, bg=LIME, fg=INK)
    return svg(body, "free", h=Hh)


# ---------------------------------------------------------------- 3 y 4. cuánto se ahorra (panel)
def ahorro():
    body = ""
    body += K.bombilla("bomb", 210, 330, 190, encendida=True)
    body += etiqueta("lidae", 210, 575, "IDAE", size=34, bg=INK, fg=LIME)
    body += etiqueta("liluz", 210, 640, "EN ILUMINACIÓN", size=26, bg="#FFFFFF", fg=INK)
    # barras
    body += f'<path d="M 470 560 L 930 560" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
    body += barra("b100", 520, 560, 150, 330, col="#FFD23F", texto="ANTES", valor="100")
    body += barra("b95", 730, 560, 150, 314, col=LIME, texto="CON CAMBIO", valor="95")
    body += etiqueta("l5", 700, 110, "HASTA 5 % MENOS", size=36, bg=CORAL, fg="#FFFFFF")
    body += etiqueta("l6", 700, 650, "UNOS 6 € POR HOGAR", size=26, bg=INK, fg=LIME)
    # escena 4
    body += sello("sest", 700, 330, "ESTIMACIÓN", size=58, rot_=-8)
    body += etiqueta("lnoconf", 700, 440, "NO CONFIRMADO AL 100 %", size=28, bg=INK, fg="#FFFFFF")
    body += etiqueta("lantigua", 210, 110, "DE HACE AÑOS", size=28, bg=LIME, fg=INK)
    body += D.bandera_ue("ue", 210, 560, 170, 112)
    body += etiqueta("lpeq", 210, 650, "AHORRO PEQUEÑO", size=26, bg=LIME, fg=INK)
    return svg(body, "panel", fondo=fondo_suave())


# ---------------------------------------------------------------- 5. el calendario del BOE (panel)
def boe():
    body = ""
    body += P.documento("doc", 230, 390, 290, 390, "BOE", "CAMBIOS DE HORA")
    body += etiqueta("lorden", 230, 625, "ORDEN PCM/186/2022", size=24, bg=INK, fg=LIME)
    anos = ("2022", "2023", "2024", "2025", "2026")
    for i, a in enumerate(anos):
        x = 470 + i * 110
        body += g(f"a{i}", f'<rect x="{x-48}" y="105" width="96" height="58" rx="12" fill="{"#FFFFFF" if i < 4 else LIME}" stroke="{INK}" stroke-width="5"/>'
                  + T(x, 145, a, 28, INK, font=DISP))
    body += P.calendario("cal", 690, 380, 230, 230, "OCT", "25")
    body += etiqueta("lult", 690, 560, "ÚLTIMO PREVISTO", size=30, bg=CORAL, fg="#FFFFFF")
    body += g("a27", f'<rect x="855" y="320" width="110" height="64" rx="12" fill="#E9EDF3" stroke="{INK}" stroke-width="5" stroke-dasharray="12 8"/>'
              + T(910, 363, "2027", 30, "#7C879C", font=DISP))
    body += icono_duda("duda", 910, 450, 38)
    return svg(body, "panel", fondo=fondo_suave())


# ---------------------------------------------------------------- 6. Europa sin acuerdo (panel)
def ue():
    body = ""
    n = 60
    import random
    cols = [LIME] * 38 + ["#9AA3B5"] * 4 + [CORAL] * 18
    random.Random(4).shuffle(cols)  # votos mezclados: sin bloques que parezcan izquierda y derecha
    hm = P.hemiciclo("hemi", 500, 470, n, 4, 120, 255, cols)
    body += hm
    body += D.bandera_ue("ue", 500, 410, 140, 94)
    body += etiqueta("lvoto", 500, 535, "EUROCÁMARA · 2019", size=28, bg=INK, fg=LIME)
    body += etiqueta("lsi", 500, 600, "410 SÍ · 192 NO · 51 ABST.", size=24, bg="#FFFFFF", fg=INK)
    body += etiqueta("lnodec", 500, 110, "NO ESTÁ DECIDIDO", size=32, bg=CORAL, fg="#FFFFFF")
    flags = [
        ("f0", 115, 250, ("#AA151B", "#F1BF00", "#F1BF00", "#AA151B"), False),
        ("f1", 115, 400, ("#0055A4", "#FFFFFF", "#EF4135"), True),
        ("f2", 115, 550, ("#000000", "#DD0000", "#FFCE00"), False),
        ("f3", 885, 250, ("#009246", "#FFFFFF", "#CE2B37"), True),
        ("f4", 885, 400, ("#FFFFFF", "#DC143C"), False),
        ("f5", 885, 550, ("#AE1C28", "#FFFFFF", "#21468B"), False),
    ]
    for i, (fid, x, y, c, vert) in enumerate(flags):
        body += (bandera(fid, x + 10, y, 120, 80, cols=c, mastil=False) if vert else bandera_h(fid, x + 10, y, 120, 80, c))
        body += icono_duda(f"q{i}", x + 70, y - 50, 24)
    body += sello("sacuerdo", 500, 300, "SIN ACUERDO", size=56, rot_=-7)
    return svg(body, "panel", fondo=fondo_suave())


# ---------------------------------------------------------------- 7 y 8. qué te pasa a ti (full)
def sueno():
    p_cans = cuerpo_en_cama("pc", "triste", ("relajado", "relajado"))
    p_duer = cuerpo_en_cama("pd", "sueno", ("relajado", "relajado"))
    p_desp = cuerpo_en_cama("pw", "risa", ("arriba", "saluda"))
    body, me = dormitorio([p_cans, p_duer, p_desp])
    tx, ty = me.puntos["tablero"]
    body += TM.despertador("d2", tx, ty, 180, "2:00", col_txt="#FFD23F")
    # reloj interno en un bocadillo
    rel = K.reloj("ri", 330, 650, 95, 2, 0, col_marco="#7B5CFF")
    body += M.bocadillo_piensa("piensa", 330, 650, 380, 300, contenido=rel, cola=(p_cans.puntos["cabeza"][0] - 80, p_cans.puntos["cabeza"][1] - 70))
    body += etiqueta("lreloj", 330, 440, "TU RELOJ INTERNO", size=28, bg=INK, fg=LIME)
    body += V.avion("avion", 830, 520, 0.6)
    body += etiqueta("ljet", 830, 640, "COMO UN JET LAG", size=28, bg=LIME, fg=INK)
    body += etiqueta("ldias", 830, 720, "2 A 5 DÍAS", size=30, bg=CORAL, fg="#FFFFFF")
    # escena 8
    body += g("zz", zzz(760, 870, 46))
    body += etiqueta("lmas", 800, 560, "+1 HORA DE SUEÑO", size=34, bg=LIME, fg=INK)
    dia = K.ventana(None, VX, VY, VW, VH)
    dia += E.sol(None, VX + VW * 0.25, VY + VH * 0.22, 40)
    body += g("vdia", dia)
    body += etiqueta("lluz", VX, VY + VH / 2 + 300, "MAÑANA, LUZ DEL SOL", size=28, bg=YEL, fg=INK)
    return svg(body, "full", fondo=E.habitacion(noche=True, cuadro=False))


if __name__ == "__main__":
    guardar(OUT / "gancho_full.svg", gancho())
    guardar(OUT / "sol_free.svg", sol_free())
    guardar(OUT / "ahorro.svg", ahorro())
    guardar(OUT / "boe.svg", boe())
    guardar(OUT / "ue.svg", ue())
    guardar(OUT / "sueno_full.svg", sueno())

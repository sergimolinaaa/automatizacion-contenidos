"""lote9-01-sacudida-dormir: dibujos de «¿Por qué das un respingo al dormirte y sientes que caes?».
Uso: python3 libreria/archivo/sacudida-dormir/dib.py

Método rossark: cada parte es su propio grupo con pivote (cabeza en el cuello, brazo en el hombro, rama en el tronco,
marioneta en la cruceta), cada repetido con su fase, y los números cuentan con capas que se relevan.
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from libreria.svg.base import *  # noqa
from libreria.svg.personajes import persona, pictograma
from libreria.svg.objetos import casa as K, escenarios as E, cuerpo as C, memoria as M, vuelo as V, tiempo as TM
from libreria.svg.objetos import animales as A, sueno as SU

OUT = ROOT / "content" / "lote9-01-sacudida-dormir"
OUT.mkdir(parents=True, exist_ok=True)
PIJAMA = "#3D6FD9"


def cuenta(prefijo, cx, cy, valores, w, h=110, size=None):
    """Contador que «cuenta»: una capa por valor (prefijo_0, prefijo_1… y la última = prefijo)."""
    o = ""
    for i, v in enumerate(valores):
        o += contador(prefijo if i == len(valores) - 1 else f"{prefijo}_{i}", cx, cy, v, w=w, h=h, size=size)
    return o


def zetas(prefijo, x, y, s=46):
    """Tres Z sueltas (cada una su grupo, para flotar con su propia fase)."""
    o = ""
    for i, k in enumerate((1.0, 0.78, 0.58)):
        o += g(f"{prefijo}{i}", T(x + i * s * 0.95, y - i * s * 1.05, "Z", s * k, "#FFFFFF", font=DISP,
                                  extra=f'stroke="{INK}" stroke-width="{f(6*k)}" paint-order="stroke"'))
    return o


# ---------------------------------------------------------------- 0. gancho: el respingo (full)
def gancho():
    detras, delante = SU.cama_lateral("cama", 70, 850, 1300, col="#7B5CFF")
    hx, hy = detras.puntos["cabeza"]
    cuerpo, brazo = SU.durmiente("dani", hx, hy + 6, 1.05, ("sueno", "sorpresa"), "media", "corto", "castano", PIJAMA)
    me = TM.mesilla("mesilla", 965, 1300, 170, 190)
    tx, ty = me.puntos["tablero"]
    body = g("camaG", detras + cuerpo + delante + brazo)
    body += me + TM.despertador("desp", tx, ty, 150, "1:07")
    body += zetas("z", hx + 110, hy - 150, 54)
    # pensamiento: «sientes que caes»
    pc = (pictograma(None, 625, 640, 150, "#FFC83D")
          + trazo("M 585 600 L 548 532", 16, "#FFC83D", 6) + trazo("M 668 598 L 712 536", 16, "#FFC83D", 6))
    rayas = "".join(f'<path d="M {x} {y0} L {x} {y0+60}" stroke="#9AA6BC" stroke-width="7" stroke-linecap="round"/>'
                    for x, y0 in ((560, 470), (625, 452), (690, 470)))
    cont = (g("pcae", f'<g transform="rotate(-14 625 610)">{pc}</g>' + rayas)
            + flecha("fcae", (790, 500), (790, 700), col=CORAL, w=12, punta=30))
    body += M.bocadillo_piensa("burbuja", 670, 600, 420, 300, contenido=cont, cola=(hx + 60, hy - 90))
    # respingo
    body += onomatopeya("boing", 600, 760, "¡BOING!", r=150, size=62, rot_=-8)
    body += g("temb", temblor(40, 960, 110, LIME) + temblor(880, 930, 110, LIME))
    guardar(f"{OUT}/gancho_full.svg", svg(body, "full", fondo=E.habitacion(noche=True, cuadro=False)))


# ---------------------------------------------------------------- 1. mioclonía hípnica (free)
def mioclonia():
    H = 860
    body = etiqueta("tnombre", 500, 52, "MIOCLONÍA HÍPNICA", bg=LIME, fg=INK, size=44)
    body += etiqueta("tsub", 500, 126, "SACUDIDA MUSCULAR AL DORMIRTE", bg=INK, fg=LIME, size=28)
    pierna = SU.pierna_corte("pierna", 70, 345, 780, 1.0, "media")
    caja = pierna.puntos["ventana"]
    # el músculo va dentro de la ventana del muslo (en el mismo grupo que el muslo, por encima)
    mus = SU.musculo_ventana("mus_rel", caja) + SU.musculo_ventana("mus_con", caja, contraido=True)
    body += g("piernaG", pierna + mus)
    rx, ry = pierna.puntos["rodilla"]
    body += g("golpes", "".join(trazo(f"M {f(x0)} {f(y0)} L {f(x1)} {f(y1)}", 9, AMARILLO, 6) for x0, y0, x1, y1 in
                                ((300, 252, 282, 214), (370, 246, 374, 206), (440, 254, 462, 218), (560, 300, 600, 290), (560, 380, 600, 392))))
    body += etiqueta("tmus", 240, 470, "MÚSCULO", bg="#FFFFFF", fg=INK, size=26)
    # 7 de cada 10
    body += cuenta("c7", 500, 560, [f"{i} DE 10" for i in range(1, 8)], w=330, h=100, size=50)
    for i in range(10):
        x = 68 + i * 96
        y = 760 - (i % 2) * 8
        body += pictograma(f"pg{i}", x, y, 116, "#8C9BB8")
        if i < 7:
            body += pictograma(f"pl{i}", x, y, 116, LIME)
    guardar(f"{OUT}/mioclonia_free.svg", svg(body, "free", h=H))


# ---------------------------------------------------------------- 2. marioneta (free)
def marioneta():
    H = 880
    body = ""
    # columna izquierda: al dormirte, los músculos se aflojan
    body += TM.luna("luna", 110, 120, 52)
    body += etiqueta("tdorm", 205, 215, "AL DORMIRTE", bg=INK, fg=LIME, size=30)
    body += C.musculo("mtenso", 185, 470, 200, 70, contraido=True)
    body += C.musculo("mflojo", 185, 470, 200, 70, contraido=False)
    body += etiqueta("tflojo", 185, 610, "SE RELAJAN", bg=LIME, fg=INK, size=30)
    # suelo y sombras (la sombra crece al caer)
    body += f'<path d="M 40 846 L 960 846" stroke="{INK}" stroke-width="8" stroke-linecap="round" opacity="0.35"/>'
    body += g("sombra_lejos", sombra(640, 846, 90, 12, 0.18))
    body += g("sombra_cerca", sombra(640, 846, 170, 20, 0.3))
    mar = SU.marioneta("tit", 640, 240, 1.0, col=CORAL, cruz_y=60)
    body += mar
    body += M.tijeras("tij", 800, 130, 0.75, rot_=-150)
    body += g("cortes", "".join(chispa(None, x, y, 20, LIME) for x, y in ((712, 112), (572, 118))))
    guardar(f"{OUT}/marioneta_free.svg", svg(body, "free", h=H))
    return mar


# ---------------------------------------------------------------- 3. el mono que resbala (full)
def mono():
    rama_y = 930
    fondo, rama = SU.arbol_rama("arbol", 170, 1700, rama_y, 1000, ancho=170)
    yb = rama.puntos["y"]
    mx = 560
    my = yb(mx)
    duerme = A.mono("mono", mx, my, 1.6, "duerme")
    agarra = A.mono("monoA", mx, my, 1.6, "agarra")
    grieta = K.grieta("grieta", (300, rama_y - 30), (350, rama_y + 28), n=6, amp=9, w=6, col="#F4E2C6")
    rayos_ = rayos("rayos", mx + 205, my - 110, 120, 175, n=9, col=AMARILLO, a0=190, a1=350)
    body = fondo
    # la rama lleva encima al mono: todo gira con ella desde el tronco
    body += g("ramaG", rama + grieta + rayos_ + duerme + agarra + zetas("mz", mx + 330, my - 165, 46))
    cer = C.cerebro("cer", 760, 470, 0.5)
    body += g("cereG", f'<circle cx="760" cy="500" r="125" fill="#FFFFFF" opacity="0.14"/>' + cer)
    body += icono_alerta("alerta", 880, 410, 44)
    body += etiqueta("tcaida", 470, 570, "¿UNA CAÍDA?", bg=CORAL, fg="#FFFFFF", size=34)
    guardar(f"{OUT}/mono_full.svg", svg(body, "full", fondo=E.cielo(hora="noche", colinas=True, nubes=False)))


# ---------------------------------------------------------------- 4. solo una hipótesis (free)
def hipotesis():
    H = 880
    # dibujo de tiza: mono en una rama y una gran interrogación
    tiza = "#F4F1E6"
    m = A.mono("tizamono", 0, 0, 1.0, "duerme")
    cont = (f'<path d="M 230 300 Q 400 280 600 296" fill="none" stroke="{tiza}" stroke-width="10" stroke-linecap="round"/>'
            f'<g transform="translate(400 296) scale(0.62)" opacity="0.9" style="filter:grayscale(1) brightness(2.2)">{m}</g>')
    body = K.pizarra("piz", 500, 230, 640, 340, contenido=g("dibtiza", cont))
    body += g("interr", T(705, 300, "?", 200, LIME, font=DISP, extra=f'stroke="{INK}" stroke-width="6" paint-order="stroke"'))
    body += etiqueta("thipo", 500, 440, "SOLO UNA HIPÓTESIS", bg=LIME, fg=INK, size=34)
    body += sello("sello", 470, 345, "SIN DEMOSTRAR", size=48, rot_=-7)
    ana = persona("ana", 175, 880, 0.72, "adulto", "morena", "coleta", "negro", "chaqueta", "#F2F4F8", "#3E5C93",
                  camisa_color="#7B5CFF", accesorios=("gafas",), expresion="duda", brazos=("cintura", "explica"), mira=1)
    luis = persona("luis", 830, 880, 0.72, "mayor", "clara", "corto", "canoso", "chaqueta", "#F2F4F8", "#4A4F5E",
                   camisa_color="#2EC4B6", accesorios=("barba",), expresion="duda", brazos=("apunta_arriba", "relajado"), mira=-1)
    body += ana + luis
    body += globo("gana", 430, 545, "¿SEGURO?", cola=(ana.puntos["boca"][0] + 50, ana.puntos["boca"][1] - 10), size=38)
    body += globo("gluis", 590, 665, "¿Y LAS\nPRUEBAS?", cola=(luis.puntos["boca"][0] - 50, luis.puntos["boca"][1] - 10), size=36)
    guardar(f"{OUT}/hipotesis_free.svg", svg(body, "free", h=H))


# ---------------------------------------------------------------- 5. lo que lo empeora (free)
def empeora():
    H = 860
    xs = (130, 375, 625, 870)
    body = ""
    # cafeína
    body += g("ic0", K.taza("taza", xs[0], 270, 150, liquido="cafe")
              + etiqueta(None, xs[0], 335, "CAFEÍNA", bg=INK, fg=LIME, size=26))
    # estrés
    p = persona("estres", xs[1], 290, 0.5, "adulto", "clara", "rizado", "pelirrojo", "camisa", "#FF7EB6", pose="busto",
                expresion="enfado", brazos=("relajado", "relajado"))
    body += g("ic1", p + M.gota_esfuerzo("sudor", xs[1] + 52, 140, 1.0) + M.gota_esfuerzo(None, xs[1] - 58, 160, 0.7)
              + etiqueta(None, xs[1], 335, "ESTRÉS", bg=INK, fg=LIME, size=26))
    # cansancio
    body += g("ic2", K.reloj("rel", xs[2], 190, 72, 3, 0, col_marco=TEAL)
              + g("zrel", zzz(xs[2] + 70, 130, 34))
              + etiqueta(None, xs[2], 335, "CANSANCIO", bg=INK, fg=LIME, size=26))
    # ejercicio por la noche
    body += g("ic3", TM.luna("lunap", xs[3] + 50, 115, 42) + V.pesa("pesa", xs[3], 280, 150, "KG")
              + etiqueta(None, xs[3], 335, "EJERCICIO", bg=INK, fg=LIME, size=26))
    # flechas a la cama
    dest = (500, 560)
    for i, x in enumerate(xs):
        body += flecha(f"f{i}", (x, 372), (dest[0] + (x - 500) * 0.4, 470), col=LIME, w=10, punta=26, curva=0.12 * (1 if i < 2 else -1))
    detras, delante = SU.cama_lateral("cama2", 240, 800, 840, col="#7B5CFF", alto=200)
    hx, hy = detras.puntos["cabeza"]
    cuerpo, brazo = SU.durmiente("dur2", hx, hy + 4, 0.8, ("sorpresa",), "oscura", "rapado", "negro", PIJAMA)
    body += g("cama2G", detras + cuerpo + delante + brazo)
    body += g("temb2", temblor(190, 660, 90, AMARILLO) + temblor(840, 640, 90, AMARILLO))
    guardar(f"{OUT}/empeora_free.svg", svg(body, "free", h=H))


if __name__ == "__main__":
    gancho()
    mioclonia()
    marioneta()
    mono()
    hipotesis()
    empeora()

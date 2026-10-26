"""lote9-07-tostada-mantequilla: dibujos de «¿Por qué la tostada cae por el lado de la mantequilla?».
Uso: python3 libreria/archivo/tostada-mantequilla/dib.py

Método rossark: la tostada vuela en dos grupos (fuera = trayectoria con move; dentro = giro sobre su centro),
cada persona respira, parpadea y mueve cabeza y brazos con su fase, y los fotogramas de la caída entran escalonados.
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from libreria.svg.base import *  # noqa
from libreria.svg.personajes import persona, multitud
from libreria.svg.objetos import casa as K, escenarios as E, animales as A, coches as CO, reptiles as R

OUT = ROOT / "content" / "lote9-07-tostada-mantequilla"
OUT.mkdir(parents=True, exist_ok=True)
BATA = "#FF8FC0"


def tost(id_, cx, cy, w, rot_=0, vista="lado", mantequilla=True):
    """Tostada en dos grupos: id_ (trayectoria) > id_+'_r' (giro sobre su centro)."""
    return g(id_, K.tostada(f"{id_}_r", cx, cy, w, vista, rot_, mantequilla))


def cuenta(prefijo, cx, cy, valores, w, h=100, size=None):
    o = ""
    for i, v in enumerate(valores):
        o += contador(prefijo if i == len(valores) - 1 else f"{prefijo}_{i}", cx, cy, v, w=w, h=h, size=size)
    return o


# ---------------------------------------------------------------- 0. gancho (full): se cae la tostada
def gancho():
    body = ""
    caras = ("ana", "anaE")
    for pid, expr in zip(caras, ("neutral", "enfado")):
        p = persona(pid, 390, 1062, 1.6, "adulto", "clara", "largo", "castano", "abrigo", BATA, camisa_color="#FFFFFF",
                    expresion=expr, pose="busto", brazos=("relajado", "explica"), mira=1)
        body += p
    body = g("anaG", body)
    body += K.mesa("mesa", 500, 1060, 780, 120)
    body += K.taza("taza", 200, 1022, 170, liquido="cafe")
    body += g("platoG", K.plato("plato", 730, 1018, 260))
    body += tost("tostada", 730, 994, 210)
    # en el suelo
    body += K.mancha_mantequilla("mancha", 950, 1222, 0.85)
    body += onomatopeya("plaf", 880, 1095, "¡PLAF!", r=120, size=50, rot_=-8)
    body += g("lineas", lineas_velocidad(860, 960, 3, 60, 30, "#FFFFFF", dir_=-1))
    body += etiqueta("tabajo", 820, 800, "BOCA ABAJO", bg=CORAL, fg="#FFFFFF", size=34)
    guardar(f"{OUT}/gancho_full.svg", svg(body, "full", fondo=E.cocina(encimera_y=1180)))


# ---------------------------------------------------------------- 1. no es mala suerte (panel)
def matthews():
    body = K.espejo_roto("espejo", 175, 215, 150, 190)
    body += A.gato("gato", 185, 485, 0.5, pelaje="negro")
    body += aspa("aspa", 180, 360, 135)
    body += etiqueta("tsuerte", 180, 640, "¿MALA SUERTE?", bg=INK, fg=LIME, size=26)
    # pizarra con la tostada girando
    tiza = "#F4F1E6"
    cont = (f'<path d="M 420 250 A 80 80 0 1 1 560 300" fill="none" stroke="{tiza}" stroke-width="6" stroke-linecap="round" stroke-dasharray="14 10"/>'
            + "".join(f'<g transform="translate({x} {y}) rotate({a})" opacity="0.95"><rect x="-34" y="-7" width="68" height="14" rx="6" fill="none" stroke="{tiza}" stroke-width="5"/>'
                      f'<path d="M -28 -10 L 28 -10" stroke="#FFE36B" stroke-width="5" stroke-linecap="round"/></g>'
                      for x, y, a in ((440, 190, 0), (540, 205, 70), (565, 290, 140), (500, 350, 180)))
            + T(610, 175, "g", 34, tiza, font='font-family="Georgia, serif" font-style="italic"')
            + T(640, 345, "θ", 34, tiza, font='font-family="Georgia, serif" font-style="italic"'))
    body += K.pizarra("piz", 520, 270, 330, 230, contenido=g("dibtiza", cont))
    body += R.revista("revista", 520, 545, 150, 200, titulo="EJP", fecha="1995",
                      contenido=T(75, 95, "European", 17, INK) + T(75, 117, "Journal", 17, INK) + T(75, 139, "of Physics", 17, INK)
                      + K.tostada(None, 75, 160, 70), col="#F4F1E6", banda="#2B4C9A")
    rm = persona("rm", 830, 690, 0.88, "adulto", "clara", "corto", "castano", "chaqueta", "#8A5A3B", "#3E4A5E",
                 camisa_color="#FFFFFF", accesorios=("gafas",), expresion="neutral", brazos=("explica", "relajado"), mira=-1)
    body += rm
    body += etiqueta("tnombre", 830, 110, "ROBERT MATTHEWS", bg=LIME, fg=INK, size=24)
    body += etiqueta("t30", 700, 600, "+30 AÑOS", bg=CORAL, fg="#FFFFFF", size=26)
    guardar(f"{OUT}/matthews.svg", svg(body, "panel", fondo=fondo_suave()))


# ---------------------------------------------------------------- 2. empieza a girar (free)
def girar():
    H = 860
    m = K.mesa_perfil("mesa", -60, 520, 400, 420)
    body = m
    body += tost("tost", 380, 382, 260)
    # fotogramas fantasma del giro alrededor del borde
    for i, (x, y, a) in enumerate(((610, 440, 30), (650, 540, 65), (665, 660, 100))):
        body += g(f"fant{i}", f'<g opacity="0.55">{K.tostada(None, x, y, 240, rot_=a)}</g>')
    body += CO.flecha_giro("giro", 560, 520, 190, -70, 70, col=LIME, w=12)
    body += etiqueta("tborde", 300, 580, "BORDE", apunta=(515, 420), bg=INK, fg=LIME, size=30)
    body += flecha("peso", (600, 330), (600, 470), col=CORAL, w=12, punta=30)
    body += etiqueta("tpeso", 790, 310, "SE VENCE", bg=CORAL, fg="#FFFFFF", size=28)
    body += etiqueta("tgira", 860, 600, "GIRA", bg=LIME, fg=INK, size=40)
    guardar(f"{OUT}/girar_free.svg", svg(body, "free", h=H))


# ---------------------------------------------------------------- 3. solo media vuelta (full)
def media_vuelta():
    body = ""
    m = K.mesa_perfil("mesa", -80, 420, 640, 540)
    body += m
    # regla vertical (en un grupo propio para el grow)
    rx, y0, y1 = 470, 640, 1180
    reg = f'<rect x="{rx-20}" y="{y0}" width="40" height="{y1-y0}" rx="6" fill="{degradado(AMARILLO, 0.15, "h")}" stroke="{INK}" stroke-width="6"/>'
    reg += "".join(f'<path d="M {rx-20} {y} L {rx-20+(22 if k % 2 == 0 else 12)} {y}" stroke="{INK}" stroke-width="4"/>'
                   for k, y in enumerate(range(y0 + 40, y1, 40)))
    body += g("regla", reg)
    body += etiqueta("tnormal", 230, 540, "MESA NORMAL", bg=INK, fg=LIME, size=34)
    # fotogramas de la caída en arco: 0, 45, 90, 135 y 180 grados
    pos = ((350, 618, 0), (560, 730, 45), (680, 870, 90), (760, 1010, 135), (800, 1150, 180))
    for i, (x, y, a) in enumerate(pos):
        op = 1 if i in (0, 4) else 0.6
        body += g(f"f{i}", f'<g opacity="{op}">{K.tostada(None, x, y, 200, rot_=a)}</g>')
    body += flecha("arco", (480, 600), (920, 1090), col=LIME, w=12, punta=32, ctrl=(880, 650))
    body += K.mancha_mantequilla("mancha", 800, 1182, 0.75)
    body += sello("s180", 200, 840, "180°", size=64, rot_=-8)
    body += etiqueta("tabajo", 760, 1245, "MANTEQUILLA ABAJO", bg=CORAL, fg="#FFFFFF", size=32)
    guardar(f"{OUT}/media_full.svg", svg(body, "full", fondo=E.cocina(encimera_y=1180)))


# ---------------------------------------------------------------- 4. mesa de tres metros (free)
def tres_metros():
    H = 1000
    suelo = 950
    body = f'<path d="M 30 {suelo} L 970 {suelo}" stroke="{INK}" stroke-width="8" stroke-linecap="round" opacity="0.35"/>'
    m = K.mesa_perfil("mesaT", 330, 620, 150, suelo - 150)
    body += g("mesaG", m + K.tostada("t0", 560, 130, 150))
    esc = K.escalera("escalera", (170, suelo), (318, 200), 90, 11)
    body += esc
    px, py = esc.puntos["peldano"](6)
    body += persona("senor", px + 8, py + 8, 0.42, "mayor", "clara", "calvo", "canoso", "camisa", "#2EC4B6", "#3E4A5E",
                    accesorios=("bigote",), expresion="sorpresa", brazos=("relajado", "apunta_arriba"), mira=1)
    # vuelta entera
    for i, (x, y, a) in enumerate(((680, 300, 90), (740, 480, 180), (775, 680, 270), (790, 915, 360))):
        op = 1 if i == 3 else 0.6
        body += g(f"v{i}", f'<g opacity="{op}">{K.tostada(None, x, y, 150, rot_=a)}</g>')
    body += CO.flecha_giro("giro", 700, 520, 260, -80, 95, col=LIME, w=11)
    body += icono_ok("ok", 790, 830, 40)
    body += flecha("altura", (945, suelo - 10), (945, 160), col=AMARILLO, w=10, punta=28)
    body += flecha("altura2", (945, 160), (945, suelo - 10), col=AMARILLO, w=10, punta=28)
    body += g("t3m", f'<g transform="rotate(-90 885 560)">{etiqueta(None, 885, 560, "UNOS 3 METROS", bg=INK, fg=LIME, size=30)}</g>')
    guardar(f"{OUT}/tres_free.svg", svg(body, "free", h=H))


# ---------------------------------------------------------------- 5. lo comprobaron los niños (panel)
def ninos():
    body = ""
    body += K.mesa("mesaN", 400, 520, 230, 140)
    nino = persona("nino", 190, 662, 0.9, "nino", "media", "corto", "castano", "jersey", "#1F3A70", "#5A6375",
                   camisa_color="#FFFFFF", expresion="sorpresa", brazos=("relajado", "explica"), mira=1)
    body += nino
    body += tost("tn", 440, 478, 120)
    body += g("plafn", onomatopeya(None, 400, 590, "¡PLAF!", r=62, size=26, rot_=-6))
    # tres tostadas: dos boca abajo (coral) y una boca arriba (lima)
    for i, (x, col, rot_) in enumerate(((640, CORAL, 180), (770, CORAL, 180), (900, LIME, 0))):
        card = (f'<rect x="{x-58}" y="140" width="116" height="150" rx="18" fill="{degradado(col, 0.15)}" stroke="{INK}" stroke-width="6"/>'
                + K.tostada(None, x, 205, 92, rot_=rot_)
                + (icono_no(None, x, 262, 18) if col == CORAL else icono_ok(None, x, 262, 18)))
        body += g(f"c{i}", card)
    body += etiqueta("t23", 770, 340, "CASI 2 DE CADA 3", bg=INK, fg=LIME, size=26)
    body += cuenta("cmil", 770, 440, ["250", "500", "750", "+1.000"], w=230, h=84, size=46)
    body += multitud("ninos", 590, 990, 650, 7, 82, seed=5, cols=("#1F3A70", "#2B4C9A", "#C8102E", "#1F3A70"))
    guardar(f"{OUT}/ninos.svg", svg(body, "panel", fondo=fondo_suave()))


if __name__ == "__main__":
    gancho()
    matthews()
    girar()
    media_vuelta()
    tres_metros()
    ninos()

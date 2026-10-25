"""lote9-05-cosquillas: dibujos de «¿Por qué no puedes hacerte cosquillas a ti mismo?».
Uso: python3 libreria/archivo/cosquillas/dib.py

Método rossark: cada parte es su propio grupo con pivote (brazos en el hombro, cabeza en el cuello, brazo robótico en
hombro, codo y muñeca con `mente.pivote`), cada repetido con su fase, barras que crecen desde la base escalonadas y
caras que se relevan con fundido corto (nunca un salto).
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from libreria.svg.base import *  # noqa
from libreria.svg.personajes import persona
from libreria.svg.objetos import casa as K, escenarios as E, cuerpo as C, politica as P, dinero as D
from libreria.svg.objetos import tecnologia as TE, mente as MN

OUT = ROOT / "content" / "lote9-05-cosquillas"
OUT.mkdir(parents=True, exist_ok=True)
ROJO = "#E63B2E"


def lagrimas(prefijo, cx, cy, sep):
    """Dos lagrimones de risa (uno a cada lado de la cara), cada uno su grupo."""
    return (g(f"{prefijo}0", gota(cx - sep, cy, 22, "#8FD3FF"))
            + g(f"{prefijo}1", gota(cx + sep, cy + 6, 20, "#8FD3FF")))


# ---------------------------------------------------------------- 0. gancho: tú solo, nada; otro, risa (full)
def gancho():
    x, y, s = 300, 1270, 1.8
    kw = dict(edad="nino", piel="clara", pelo="corto", pelo_color="castano", ropa="camiseta", ropa_color=ROJO,
              pantalon_color="#3E5C93", brazos=("arriba", "cruzados"))
    chicoN = persona("chicoN", x, y, s, expresion="neutral", mira=0, **kw)
    chicoR = persona("chicoR", x, y, s, expresion="risa", mira=1, **kw)
    hx, hy = chicoN.puntos["cabeza"]
    herm = persona("herm", 740, y, 1.3, "joven", "clara", "coleta", "castano", "jersey", "#7B5CFF", "#2E3550",
                   expresion="risa", brazos=("senala", "relajado"), mira=-1)
    body = g("chico", chicoN + chicoR)
    body += g("hermG", herm)
    body += globo("gnada", hx + 230, hy - 80, "…", cola=(hx + 80, hy - 20), size=70, tipo="piensa")
    body += etiqueta("tnada", 640, 900, "¿NADA?", bg=INK, fg=LIME, size=60)
    body += onomatopeya("jaja", 525, 610, "¡JAJA!", r=125, size=56, rot_=-8)
    body += lagrimas("lag", hx, hy + 10, 70)
    body += g("dest", destellos(None, hx - 10, hy - 40, 150, LIME, seed=3))
    guardar(f"{OUT}/gancho_full.svg", svg(body, "full", fondo=E.habitacion(cuadro=False)))
    return chicoN, herm


# ---------------------------------------------------------------- 1. culpa del cerebelo (free)
def cerebelo():
    H = 860
    cab = C.cabeza_perfil("cab", 400, 840, 1.15, "clara")
    cbx, cby = cab.puntos["nuca"]
    # el cerebelo de la cabeza de perfil: mismo punto que en cerebro() (315, 395) en coords de cabeza
    cb = (400 + (315 - 462) * 1.15, 840 + (395 - 720) * 1.15)
    body = g("cabG", cab)
    body += g("cbglow", f'<circle cx="{f(cb[0])}" cy="{f(cb[1])}" r="70" fill="url(#bolaHalo)"/>'
              f'<ellipse cx="{f(cb[0])}" cy="{f(cb[1])}" rx="60" ry="42" fill="{LIME}" opacity="0.55" stroke="{INK}" stroke-width="5"/>')
    body += flecha("fatras", (60, 250), (cb[0] - 50, cb[1] - 30), col=LIME, w=12, punta=30, curva=-0.25)
    body += etiqueta("tcb", 200, 120, "CEREBELO", bg=LIME, fg=INK, size=46)
    body += etiqueta("tcoord", 730, 120, "COORDINA TUS\nMOVIMIENTOS".split("\n")[0], bg=INK, fg=LIME, size=30)
    body += etiqueta("tcoord2", 730, 175, "MOVIMIENTOS", bg=INK, fg=LIME, size=30)
    body += MN.engranaje("eng1", 780, 360, 64, 10)
    body += MN.engranaje("eng2", 868, 300, 42, 7, col=degradado(LIME, 0.3))
    m = C.mano("mano", 820, 640, 0.75, "clara")
    body += g("manoG", m)
    guardar(f"{OUT}/cerebelo_free.svg", svg(body, "free", h=H))


# ---------------------------------------------------------------- 2. recibe una copia (free)
def copia():
    H = 860
    s = 0.95
    cer = C.cerebro("cer", 380, 230, s, hipotalamo=False)
    cbx, cby = cer.puntos["cerebelo"]
    fx, fy = cer.puntos["frente"]
    body = g("cerG", cer)
    body += g("cbglow2", f'<ellipse cx="{f(cbx)}" cy="{f(cby)}" rx="58" ry="40" fill="{LIME}" opacity="0.6" stroke="{INK}" stroke-width="5"/>')
    m = C.mano("mano2", 800, 600, 0.85, "clara")
    body += g("mano2G", m)
    # sobre de la orden (sale de la frente hacia la mano) y su fotocopia (hacia el cerebelo)
    body += flecha("fruta", (fx + 30, fy + 20), (760, 380), col="#FFFFFF", w=8, punta=22, curva=0.2)
    body += g("orden", P.sobre(fx + 40, fy + 10, 150, 100, rot_=-8) + T(fx + 40, fy + 26, "ORDEN", 26, INK, font=DISP))
    body += g("copiaS", P.sobre(fx + 40, fy + 10, 150, 100, rot_=6, fill="#FFF6C9")
              + T(fx + 40, fy + 26, "COPIA", 26, CORAL, font=DISP))
    # bola de cristal con una pluma dentro (predice lo que vas a sentir)
    bx, by = 200, 640
    dentro = MN.pluma("plb", bx - 70, by + 60, 150, -45)
    body += MN.bola_cristal("bola", bx, by, 110, dentro=dentro)
    body += etiqueta("tpred", 470, 790, "PREDICE LO QUE SENTIRÁS", bg=LIME, fg=INK, size=30)
    guardar(f"{OUT}/copia_free.svg", svg(body, "free", h=H))
    return cer


# ---------------------------------------------------------------- 3. sin sorpresa: frena la respuesta (free)
def frena():
    H = 860
    vol = MN.barra_volumen("vol", 90, 430, 420, 300, 7, texto="COSQUILLAS")
    body = vol
    body += D.palanca("fre", 300, 830, 260, "FRENO")
    body += flecha("fbaja", (560, 180), (560, 420), col=CORAL, w=14, punta=34)
    s = 0.85
    cx, cy = 770, 330
    body += g("cerA", C.cerebro("cerA_c", cx, cy, s, hipotalamo=False) + MN.cara_cerebro("cara", cx + 40, cy - 10, s * 0.9, "aburrido"))
    body += icono_ok("ok", 900, 140, 50)
    body += etiqueta("tsabe", 760, 660, "YA LO SABÍA", bg=INK, fg=LIME, size=34)
    guardar(f"{OUT}/frena_free.svg", svg(body, "free", h=H))


# ---------------------------------------------------------------- 4. el robot de Blakemore (full)
def robot():
    sarah = persona("sarah", 190, 1270, 1.1, "adulto", "clara", "largo", "castano", "chaqueta", "#F4F6FA", "#3E4A66",
                    camisa_color="#2EC4B6", expresion="neutral", brazos=("relajado", "explica"), mira=1)
    vol = persona("volN", 840, 1270, 1.12, "joven", "morena", "rizado", "negro", "camiseta", "#FFC83D", "#2E3550",
                  expresion="neutral", brazos=("explica", "coge"), mira=-1)
    mesa = K.mesa("mesa", 600, 1060, 860, 240, col="#DDE3EE")
    mx, my = vol.puntos["mano_izq"]
    rob = TE.brazo_robot("rob", 420, 1060, 0.9, hombro=-80, codo=74)
    pal = D.palanca("pal", 935, 1060, 150, "")
    body = g("sarahG", sarah) + g("volG", vol) + mesa + rob + pal
    body += medidor("med", 520, 640, 140, 0.5)
    body += etiqueta("tmed", 520, 695, "COSQUILLAS", bg=INK, fg=LIME, size=30)
    body += etiqueta("tlon", 250, 530, "LONDRES", bg=LIME, fg=INK, size=44)
    body += etiqueta("tmenos", 780, 540, "MENOS", bg=CORAL, fg="#FFFFFF", size=40)
    guardar(f"{OUT}/robot_full.svg", svg(body, "full", fondo=E.oficina()))
    print("mano voluntario", mx, my, "punta", rob.puntos["punta"], "mano_der", vol.puntos["mano_der"])
    return rob


# ---------------------------------------------------------------- 5. un retraso lo cambia (free)
def retraso():
    H = 860
    body = K.cronometro("cron", 170, 190, 110)
    body += etiqueta("tret", 560, 110, "RETRASO:", bg=CORAL, fg="#FFFFFF", size=36)
    body += etiqueta("tfrac", 560, 175, "UNA FRACCIÓN DE SEGUNDO", bg=INK, fg=LIME, size=30)
    rob = TE.brazo_robot("rob2", 150, 830, 0.95, hombro=-62, codo=80)
    body += rob
    tx, ty = rob.puntos["punta"]
    body += g("palma2G", C.mano("palma2", tx + 20, ty + 50, 0.45, "morena"))
    body += medidor("med2", 520, 520, 170, 0.5)
    body += etiqueta("tmed2", 520, 585, "COSQUILLAS", bg=INK, fg=LIME, size=30)
    vN = persona("v2N", 800, 860, 1.0, "joven", "morena", "rizado", "negro", "camiseta", "#FFC83D", pose="busto",
                 expresion="neutral", brazos=("relajado", "relajado"), mira=-1)
    vR = persona("v2R", 800, 860, 1.0, "joven", "morena", "rizado", "negro", "camiseta", "#FFC83D", pose="busto",
                 expresion="risa", brazos=("relajado", "relajado"), mira=-1)
    body += g("v2", vN + vR)
    hx, hy = vN.puntos["cabeza"]
    body += g("dest2", destellos(None, hx, hy - 20, 140, LIME, seed=5))
    body += onomatopeya("jaja2", 840, 330, "¡JAJA!", r=105, size=46, rot_=8)
    guardar(f"{OUT}/retraso_free.svg", svg(body, "free", h=H))


if __name__ == "__main__":
    gancho()
    cerebelo()
    copia()
    frena()
    robot()
    retraso()

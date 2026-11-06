"""lote10-03-pelo-cancion: dibujos de «¿Por qué una canción te pone la piel de gallina?». PRIMER VÍDEO EN PAPEL.
Uso: python3 libreria/archivo/pelo-cancion/dib.py

Todo en papel recortado (libreria/svg/papel.py): fondos con capas lejos/medio/cerca para el parallax, piezas de la
librería pasadas por a_papel() y formas sueltas con recorte(). Pieza nueva reutilizable: accesorio «cascos» en persona().
"""
import math
import random
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from libreria.svg.base import *  # noqa
from libreria.svg.personajes import persona, pictograma
from libreria.svg.papel import (a_papel, recorte, capa, fondo_casa, fondo_neutro, grano, hoja_transicion, fx, PAPEL as PP)
from libreria.svg.objetos import cuerpo as C, casa as K, memoria as M

OUT = ROOT / "content" / "lote10-03-pelo-cancion"
OUT.mkdir(parents=True, exist_ok=True)
TXT = PP["tinta"]


def nota(id_, cx, cy, s, col, doble=False, rot_=-12, semilla=0):
    return a_papel(g(id_, nota_musical(cx, cy, s, col, doble=doble, rot_=rot_)), semilla=semilla, filtro="papelFino")


def rotulo(id_, cx, cy, text, size=34, col=None, bg=None, semilla=0):
    """Tira de papel con texto (sustituye a la etiqueta negra con letras lima)."""
    col = col or PP["crema"]
    bg = bg or TXT
    w = len(text) * size * 0.62 + 50
    h = size * 1.7
    s = recorte(f"M {f(cx-w/2)} {f(cy-h/2)} L {f(cx+w/2)} {f(cy-h/2+3)} L {f(cx+w/2-4)} {f(cy+h/2)} L {f(cx-w/2+3)} {f(cy+h/2-2)} Z", bg, semilla, "papelFino")
    s += T(cx, cy + size * 0.36, text, size, col, font=DISP)
    return g(id_, s)


def chispa(cx, cy, r, col):
    pts = []
    for k in range(8):
        a = k * math.pi / 4
        rr = r if k % 2 == 0 else r * 0.38
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return f'<path d="{poly(pts, True)}" fill="{col}"/>'


# ============================================================== 0 · gancho (full)
def gancho():
    body = fondo_casa()
    kw = dict(edad="joven", piel="media", pelo="rizado", pelo_color="negro", ropa="camiseta", ropa_color=PP["naranja"],
              pantalon_color=PP["azul_osc"], accesorios=("cascos",), brazos=("relajado", "explica"), estilo="papel")
    body += g("chico", persona("chn", 360, 1290, 1.12, expresion="neutral", **kw) + persona("chs", 360, 1290, 1.12, expresion="sorpresa", **kw))
    # notas musicales que salen de los cascos
    body += nota("n0", 560, 700, 70, PP["coral"], semilla=1)
    body += nota("n1", 660, 620, 60, PP["azul_osc"], doble=True, rot_=10, semilla=2)
    body += nota("n2", 190, 660, 56, PP["mostaza_osc"], rot_=-20, semilla=3)
    # termómetro alto con copo tachado: «sin hacer frío»
    body += a_papel(C.termometro("termo", 110, 600, 300, 0.62, col=PP["coral"], marcas=6), semilla=4)
    body += a_papel(g("copo", copo(110, 520, 46, 10, PP["azul"])), semilla=5, filtro="papelFino")
    body += a_papel(aspa("aspa", 110, 520, 52, PP["coral"], 12), semilla=6, filtro="papelFino", giro=0)
    # antebrazo en primer plano con la piel de gallina
    body += a_papel(C.antebrazo("brz", (1170, 1250), (690, 1050), 112, gallina=True, manga=PP["naranja"]), semilla=7)
    body += g("rayas", recorte("M 640 960 L 660 950 L 690 1010 L 672 1018 Z", PP["mostaza"], 8, "papelFino")
              + recorte("M 600 1020 L 620 1014 L 640 1060 L 622 1066 Z", PP["mostaza"], 9, "papelFino")
              + recorte("M 700 920 L 718 916 L 736 960 L 720 966 Z", PP["mostaza"], 10, "papelFino"))
    body += hoja_transicion("salida", PP["mostaza"], None)
    body += grano()
    guardar(OUT / "gancho_full.svg", svg(body, "full"))


# ============================================================== 1 · frisson: espalda (free 880)
def espalda():
    piel, sombra_p = PP["piel"], "#E2AE86"
    cx = 500
    cab = recorte(f"M {cx-78} 205 Q {cx-90} 120 {cx} 112 Q {cx+92} 120 {cx+80} 210 Q {cx+70} 290 {cx} 296 Q {cx-70} 290 {cx-78} 205 Z", "#3A2E2A", 11, "papelCapa")
    cab += recorte(f"M {cx-86} 210 Q {cx-104} 200 {cx-100} 232 Q {cx-94} 252 {cx-80} 246 Z", piel, 12, "papelFino", giro=0)
    cab += recorte(f"M {cx+86} 210 Q {cx+104} 200 {cx+100} 232 Q {cx+94} 252 {cx+80} 246 Z", piel, 13, "papelFino", giro=0)
    tronco = recorte(f"M {cx-34} 280 L {cx+34} 280 L {cx+40} 330 Q {cx+190} 336 {cx+210} 380 L {cx+170} 860 L {cx-170} 860 L {cx-210} 380 Q {cx-190} 336 {cx-40} 330 Z",
                     piel, 14, "papelCapa", giro=0)
    tronco += recorte(f"M {cx-120} 420 Q {cx-60} 470 {cx-30} 430 Q {cx-70} 400 {cx-120} 420 Z", sombra_p, 15, "papelPlano")
    tronco += recorte(f"M {cx+120} 420 Q {cx+60} 470 {cx+30} 430 Q {cx+70} 400 {cx+120} 420 Z", sombra_p, 16, "papelPlano")
    tronco += "".join(f'<circle cx="{cx}" cy="{360+k*48}" r="7" fill="{sombra_p}"/>' for k in range(10))
    bi = recorte(f"M {cx-205} 372 Q {cx-250} 380 {cx-262} 470 L {cx-280} 820 L {cx-222} 826 L {cx-196} 520 Z", piel, 17, "papelCapa")
    bd = recorte(f"M {cx+205} 372 Q {cx+252} 384 {cx+266} 480 L {cx+276} 816 L {cx+220} 820 L {cx+198} 520 Z", piel, 18, "papelCapa")
    fig = g("esp_brazo_izq", bi) + g("esp_brazo_der", bd) + tronco + g("esp_cabeza", cab)
    body = g("esp", fig)
    # la ola de escalofrío: baja por la columna y se reparte por los brazos
    body += g("ola_col", trazo(f"M {cx} 330 C {cx-14} 450, {cx+14} 600, {cx} 800", 22, PP["mostaza"], 0))
    body += g("ola_bra", trazo(f"M {cx-10} 380 C {cx-120} 360, {cx-236} 420, {cx-250} 780", 16, PP["mostaza"], 0)
              + trazo(f"M {cx+10} 380 C {cx+120} 360, {cx+240} 420, {cx+248} 780", 16, PP["mostaza"], 0))
    for i, (x, y) in enumerate(((cx - 250, 520), (cx + 252, 600), (cx - 150, 400), (cx + 160, 420), (cx, 560))):
        body += g(f"ch{i}", chispa(x, y, 26, PP["coral"] if i % 2 else PP["mostaza_osc"]))
    body += nota("n5", 690, 150, 64, PP["coral"], semilla=19)
    body += nota("n6", 300, 120, 54, PP["azul_osc"], doble=True, rot_=12, semilla=20)
    body += rotulo("et_fr", 500, 836, "FRISSON: ESCALOFRÍO DE PLACER", 32, semilla=21)
    guardar(OUT / "espalda_free.svg", svg(body, "free", h=880))


# ============================================================== 2 · el escáner de Montreal (free 880)
def escaner():
    body = a_papel(C.escaner_resonancia("esc", 500, 300, 560, "PET"), semilla=22)
    # paciente tumbado en la camilla, con cascos (entra al túnel)
    pac = recorte("M 440 372 L 880 372 L 880 410 L 440 410 Z", PP["azul"], 23, "papelCapa", giro=0)
    pac += recorte("M 830 300 L 862 300 L 880 372 L 840 372 Z", PP["azul_osc"], 24, "papelCapa", giro=0)
    pac += f'<g{fx("papelCapa")}><circle cx="410" cy="360" r="40" fill="{PP["piel"]}"/><path d="M 372 350 Q 380 312 420 318 Q 440 330 446 352 L 430 340 Q 400 330 380 360 Z" fill="#3A2E2A"/></g>'
    pac += f'<g{fx("papelFino")}><path d="M 380 330 Q 410 296 444 330" fill="none" stroke="{PP["azul_osc"]}" stroke-width="10" stroke-linecap="round"/><rect x="396" y="350" width="26" height="36" rx="10" fill="{PP["coral"]}"/></g>'
    body += g("pac", pac)
    body += g("ondas", recolorear_ondas())
    body += rotulo("et_mtl", 230, 610, "MONTREAL", 30, bg=PP["coral"], semilla=25)
    body += rotulo("et_2001", 790, 610, "2001", 34, bg=PP["azul_osc"], semilla=26)
    # fila de diez músicos con su nota
    cols = (PP["coral"], PP["azul"], PP["mostaza_osc"], PP["verde_osc"], PP["lavanda"])
    for i in range(10):
        x = 95 + i * 90
        body += a_papel(g(f"pg{i}", pictograma(None, x, 790, 120, cols[i % 5]).replace('<g id="None">', "<g>")
                          + nota_musical(x + 22, 700, 30, TXT, rot_=-10 + 4 * i)), semilla=30 + i, filtro="papelFino")
    body += g("cor", recorte("M 640 120 C 640 92 680 86 690 112 C 700 86 740 92 740 120 C 740 150 700 166 690 182 C 680 166 640 150 640 120 Z", PP["coral"], 27, "papelFino"))
    guardar(OUT / "escaner_free.svg", svg(body, "free", h=880))


def recolorear_ondas():
    return f'<g{fx("papelFino")}>' + ondas_sonido(None, 410, 330, 70, 3, 200, 260, 28, 9, PP["coral"]).replace('<g id="None">', "<g>") + "</g>"


# ============================================================== 3 · recompensa (free 860)
def recompensa():
    cab = C.cabeza_perfil("cab", 360, 860, 1.22)
    hx, hy = cab.puntos["hipotalamo"]
    body = a_papel(cab, semilla=40)
    px, py = hx + 20, hy - 30  # zona profunda del cerebro (recompensa)
    body += g("brillo", f'<g{fx("papelFino")}><circle cx="{f(px)}" cy="{f(py)}" r="46" fill="{PP["mostaza"]}" opacity="0.75"/>'
                        f'<circle cx="{f(px)}" cy="{f(py)}" r="24" fill="{PP["luz"]}"/></g>')
    body += g("anillo", f'<circle cx="{f(px)}" cy="{f(py)}" r="60" fill="none" stroke="{PP["mostaza"]}" stroke-width="8"/>')
    body += g("anillo2", f'<circle cx="{f(px)}" cy="{f(py)}" r="60" fill="none" stroke="{PP["mostaza"]}" stroke-width="8"/>')
    body += rotulo("et_rec", 600, 130, "SISTEMA DE RECOMPENSA", 28, semilla=41)
    body += g("guia", f'<path d="M 600 160 Q 560 220 {f(px+40)} {f(py-30)}" fill="none" stroke="{TXT}" stroke-width="6" stroke-dasharray="12 10" stroke-linecap="round"/>')
    # la comida enciende lo mismo: plato con pastel
    pl = a_papel(K.plato("plato", 800, 700, 300, PP["crema"]), semilla=42)
    pastel = (recorte("M 700 690 L 900 690 L 900 600 L 700 600 Z", PP["rosa"], 43, "papelCapa", giro=0)
              + recorte("M 700 610 L 900 610 L 900 560 Q 800 530 700 560 Z", PP["crema"], 44, "papelCapa", giro=0)
              + recorte("M 700 645 L 900 645 L 900 630 L 700 630 Z", PP["coral"], 45, "papelPlano", giro=0)
              + recorte("M 784 540 Q 800 500 816 540 Q 816 566 800 566 Q 784 566 784 540 Z", PP["coral_osc"], 46, "papelFino"))
    body += g("comida", pl + g("pastel", pastel))
    body += a_papel(flecha("fl_com", (720, 520), (px + 60, py + 30), col=PP["mostaza"], w=14, punta=34, curva=-0.25), semilla=47, filtro="papelFino")
    for i, (x, y) in enumerate(((px - 70, py - 70), (px + 80, py - 60), (px - 10, py + 80))):
        body += g(f"cs{i}", chispa(x, y, 22, PP["coral"] if i % 2 else PP["mostaza_osc"]))
    guardar(OUT / "recompensa_free.svg", svg(body, "free", h=860))


# ============================================================== 4 · dopamina (full, cerebro por dentro)
def dopamina():
    rnd = random.Random(50)
    base = f'<rect width="1080" height="1920" fill="{PP["azul_marino"]}"/>'
    base += f'<rect width="1080" height="1920" filter="url(#papelFibras)" opacity="0.25"/>'
    lejos = ""
    for i in range(7):
        x, y, r = rnd.uniform(-150, 1230), rnd.uniform(500, 1500), rnd.uniform(140, 260)
        pts_ = [(x + r * (0.8 + 0.3 * rnd.random()) * math.cos(a * math.pi / 5), y + r * (0.8 + 0.3 * rnd.random()) * math.sin(a * math.pi / 5)) for a in range(10)]
        lejos += f'<g opacity="0.55">{recorte(smooth(pts_, True), "#4A5878", i, "papelPlano")}</g>'
    medio = ""
    for i in range(6):  # neuronas lejanas en lavanda
        x, y = rnd.uniform(-100, 1180), rnd.uniform(560, 1350)
        if 300 < x < 900 and 650 < y < 1000:
            y += 380
        d = f"M {f(x)} {f(y)} " + " ".join(f"L {f(x + 150*math.cos(a))} {f(y + 150*math.sin(a))} M {f(x)} {f(y)}" for a in (0.3, 1.9, 3.4, 4.8))
        medio += f'<g{fx("papelCapa")} opacity="0.7"><path d="{d}" stroke="{PP["lavanda"]}" stroke-width="14" stroke-linecap="round" fill="none"/><circle cx="{f(x)}" cy="{f(y)}" r="34" fill="{PP["lavanda"]}"/></g>'
    cerca = (recorte("M -200 1330 Q 200 1270 540 1320 Q 860 1360 1280 1300 L 1280 1960 L -200 1960 Z", "#2E3850", 51, "papelPlano")
             + recorte("M -200 520 Q -40 470 60 560 Q 20 640 -200 640 Z", "#5A4A6E", 52, "papelBorde")
             + recorte("M 1280 1160 Q 1100 1120 1040 1210 Q 1100 1290 1280 1280 Z", "#5A4A6E", 53, "papelBorde"))
    body = base + g("lejos", lejos) + g("medio", medio) + g("cerca", cerca)
    # neurona protagonista: soma, dendritas y axón hasta la terminal
    sx, sy = 330, 800
    neu = f'<g{fx("papelBorde")}>'
    for a, L in ((2.3, 210), (3.0, 240), (3.8, 200), (4.6, 180), (1.6, 170)):
        neu += f'<path d="M {sx} {sy} Q {f(sx + L*0.6*math.cos(a) + 30)} {f(sy + L*0.6*math.sin(a))} {f(sx + L*math.cos(a))} {f(sy + L*math.sin(a))}" stroke="{PP["coral"]}" stroke-width="26" stroke-linecap="round" fill="none"/>'
    neu += f'<path d="M {sx} {sy} C 470 760, 560 860, 700 820" stroke="{PP["coral"]}" stroke-width="30" stroke-linecap="round" fill="none"/>'
    neu += f'<circle cx="{sx}" cy="{sy}" r="96" fill="{PP["coral"]}"/><circle cx="{sx+10}" cy="{sy-6}" r="38" fill="{PP["coral_osc"]}"/>'
    neu += f'<path d="M 690 760 Q 780 760 790 820 Q 780 880 690 880 Q 720 820 690 760 Z" fill="{PP["coral"]}"/></g>'
    body += g("neurona", neu)
    pos = [(860, 700), (900, 820), (850, 930), (960, 740), (980, 880), (820, 800), (930, 640), (1000, 990)]
    for i, (x, y) in enumerate(pos):
        body += g(f"dp{i}", f'<g{fx("papelFino")}><circle cx="{x}" cy="{y}" r="{rnd.uniform(22, 32):.0f}" fill="{PP["lima"] if i % 3 else PP["mostaza"]}"/></g>')
    body += rotulo("et_dop", 560, 560, "DOPAMINA: LA DEL PLACER", 34, bg=PP["mostaza"], col=TXT, semilla=54)
    body += rotulo("et_2011", 170, 560, "2011", 36, bg=PP["crema"], col=TXT, semilla=55)
    # barra de la canción: cabezal que avanza hacia el «momento cumbre»
    bx0, bx1, by = 150, 930, 1150
    barra_ = (recorte(f"M {bx0} {by-14} L {bx1} {by-14} L {bx1} {by+14} L {bx0} {by+14} Z", PP["crema"], 56, "papelCapa", giro=0)
              + recorte(f"M {bx0} {by-14} L {bx0+60} {by-14} L {bx0+60} {by+14} L {bx0} {by+14} Z", PP["coral"], 57, "papelPlano", giro=0))
    body += g("barra", barra_)
    mx = 800
    body += g("cumbre", recorte(f"M {mx-6} {by-120} L {mx+6} {by-120} L {mx+6} {by} L {mx-6} {by} Z", PP["crema"], 58, "papelFino", giro=0)
              + recorte(f"M {mx+6} {by-120} L {mx+120} {by-100} L {mx+6} {by-78} Z", PP["mostaza"], 59, "papelFino", giro=0)
              + T(mx, by + 70, "MOMENTO CUMBRE", 30, PP["crema"], font=DISP))
    body += g("cabezal", f'<g{fx("papelFino")}><circle cx="{bx0+60}" cy="{by}" r="30" fill="{PP["mostaza"]}"/><circle cx="{bx0+60}" cy="{by}" r="12" fill="{TXT}"/></g>')
    body += a_papel(K.cronometro("crono", 200, 980, 70, PP["coral"]), semilla=60)
    body += hoja_transicion("salida", PP["lima"], None)
    body += grano()
    guardar(OUT / "dopamina_full.svg", svg(body, "full"))


# ============================================================== 5 · anticipar y sorprender (free 860)
def sorpresa():
    pts_ = [(60, 470), (130, 430), (190, 480), (250, 410), (320, 470), (390, 400), (450, 460), (520, 380), (590, 450),
            (650, 330), (700, 120), (750, 360), (810, 440), (870, 410), (940, 470)]
    d = smooth(pts_, False)
    body = g("onda", f'<g{fx("papelCapa")}><path d="{d}" fill="none" stroke="{PP["azul_osc"]}" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/></g>')
    body += g("onda_base", recorte("M 40 500 L 960 500 L 960 512 L 40 512 Z", PP["tinta_suave"], 61, "papelPlano", giro=0))
    body += g("cab5", recorte("M 54 80 L 66 80 L 66 520 L 54 520 Z", PP["coral"], 62, "papelFino", giro=0)
              + f'<g{fx("papelFino")}><circle cx="60" cy="520" r="18" fill="{PP["coral"]}"/></g>')
    kw = dict(edad="joven", piel="morena", pelo="coleta", pelo_color="castano", ropa="camiseta", ropa_color=PP["verde_osc"],
              accesorios=("cascos",), pose="busto", estilo="papel")
    body += g("oy", persona("oyn", 190, 860, 1.2, expresion="neutral", **kw) + persona("oys", 190, 860, 1.2, expresion="risa", **kw))
    nota_b = nota_musical(620, 700, 60, PP["coral"], rot_=-10)
    body += a_papel(M.bocadillo_piensa("pien", 620, 690, 340, 210, g("pien_nota", nota_b), cola=(330, 650)), semilla=63)
    body += a_papel(destellos("dest", 700, 130, 110, PP["mostaza_osc"]), semilla=64, filtro="papelFino")
    body += a_papel(confeti("conf", (520, 40, 900, 360), 26, 7, (PP["coral"], PP["mostaza"], PP["azul"], PP["verde"], PP["lavanda"])), semilla=65, filtro="papelFino")
    body += a_papel(onomatopeya("wow", 860, 250, "¡WOW!", r=110, size=44, rot_=10, col=PP["mostaza"], fg=TXT), semilla=66, filtro="papelFino")
    guardar(OUT / "sorpresa_free.svg", svg(body, "free", h=860))


if __name__ == "__main__":
    gancho()
    espalda()
    escaner()
    recompensa()
    dopamina()
    sorpresa()
    print("ok:", sorted(p.name for p in OUT.glob("*.svg")))

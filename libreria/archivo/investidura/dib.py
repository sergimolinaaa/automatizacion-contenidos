import sys, os
sys.path.insert(0, "/home/user/automatizacion-contenidos")
from libreria.svg.base import *
from libreria.svg.personajes import persona, pictograma
from libreria.svg.objetos import politica as P, escenarios as E, territorio as TE, casa as C, piel as PI

OUT = "/home/user/automatizacion-contenidos/content/lote8-06-investidura"
os.makedirs(OUT, exist_ok=True)
GRIS_E = "#C9CED8"


def r_esc(r0, r1, filas):
    return max(6, (r1 - r0) / filas * 0.42)


# ---------------------------------------------------------------- 1. gancho (full): hemiciclo con dudas
def gancho():
    cx, cy, r0, r1, fl = 600, 900, 170, 330, 8
    h = P.hemiciclo("hemi", cx, cy, 350, fl, r0, r1, GRIS_E)
    re_ = r_esc(r0, r1, fl)
    cap = P.capa_escanos("mix", h.puntos["escanos"], 350, "#8C9BB8", re_, grupos=1)
    ana_n = persona("ana_n", 190, 1250, 1.0, "adulto", "media", "largo", "castano", "jersey", CORAL,
                    expresion="neutral", brazos=("relajado", "explica"), mira=1)
    ana_d = persona("ana_d", 190, 1250, 1.0, "adulto", "media", "largo", "castano", "jersey", CORAL,
                    expresion="duda", brazos=("relajado", "barbilla"), mira=1)
    gl = globo("globo", 330, 520, "¿Y QUIÉN\nGOBIERNA?", cola=ana_d.puntos["boca"], size=40)
    cal = P.calendario("cal", 880, 520, 170, 190, "NOV", "29", rot_=6)
    tmay = etiqueta("tmay", cx, cy + 70, "¿MAYORÍA?", bg=LIME, fg=INK, size=34)
    duda = icono_duda("duda", cx, cy - 120, 52)
    body = ana_n + ana_d + h + cap + tmay + duda + cal + gl
    guardar(f"{OUT}/gancho_full.svg", svg(body, "full", fondo=E.habitacion(cuadro=False)))


# ---------------------------------------------------------------- 2. sin posicionarnos (free)
def ley():
    doc = P.documento("doc", 330, 520, 300, 390, "CONSTITUCIÓN", "ARTÍCULO 99", rot_=-6)
    ban = bandera("ban", 760, 430, 230, 150, cols=("#C60B1E", "#FFC400", "#FFC400", "#C60B1E"), vertical=False)
    sp = P.sin_posicionarnos("sello", 500, 160, 44)
    t1 = etiqueta("tcomo", 740, 690, "SOLO CÓMO FUNCIONA", size=30)
    chisp = g("chisp", chispa(None, 520, 360, 34, LIME) + chispa(None, 160, 300, 24, LIME))
    body = ban + doc + sp + t1 + chisp
    guardar(f"{OUT}/ley_free.svg", svg(body, "free", h=900))


# ---------------------------------------------------------------- 3. consultas del Rey (panel)
def consultas():
    rey = persona("rey", 230, 640, 1.0, "adulto", "clara", "corto", "castano", "chaqueta", "#24304D",
                  accesorios=("barba",), expresion="neutral", pose="busto", brazos=("relajado", "explica"), mira=1)
    ci = rey.puntos["cima"]
    cor = P.corona("cor", ci[0], ci[1] + 16, 96)
    m = C.mesa("mesa", 500, 560, 960, 160)
    reps = ""
    cols = ("#7B5CFF", "#2EC4B6", "#FFC83D")
    pelos = (("corto", "negro", "clara"), ("largo", "rubio", "media"), ("rizado", "castano", "morena"))
    for i, (x, col) in enumerate(zip((560, 720, 880), cols)):
        p, pc, pi = pelos[i]
        reps += g(f"rep{i}", persona(f"r{i}", x, 640, 0.78, "adulto", pi, p, pc, "camisa", col,
                                    expresion="neutral", pose="busto", brazos=("relajado", "relajado"), mira=-1)
                  + P.carpeta(None, x, 610, 110, 70, "GRUPO"))
    tg = etiqueta("tgrup", 720, 110, "GRUPOS DEL CONGRESO", size=28)
    trey = etiqueta("trey", 230, 110, "EL REY", bg=LIME, fg=INK, size=30)
    cand = tarjeta("cand", 470, 270, 210, 230, acento=LIME,
                   body=pictograma(None, 470, 270, 110, "#8C9BB8") + T(470, 365, "CANDIDATO", 26))
    fl = flecha("fcand", (300, 300), (360, 280), col=LIME, ctrl=(320, 260))
    body = m + rey + cor + reps + tg + trey + fl + cand
    guardar(f"{OUT}/consultas.svg", svg(body, "panel", fondo=fondo_suave()))


# ---------------------------------------------------------------- 4. primera votación: 176 de 350 (panel)
def votacion1():
    cx, cy, r0, r1, fl = 500, 580, 185, 340, 9
    h = P.hemiciclo("hemi", cx, cy, 350, fl, r0, r1, GRIS_E)
    re_ = r_esc(r0, r1, fl)
    si = P.capa_escanos("si", h.puntos["escanos"], 176, LIME, re_, grupos=4)
    body = h + si
    body += contador("c176", cx, 520, "176", w=200, h=90)
    body += etiqueta("tde", cx, 625, "DE 350", size=28)
    body += etiqueta("t1v", 830, 110, "1.ª VOTACIÓN", bg=INK, fg=LIME, size=28)
    body += etiqueta("tabs", 200, 110, "MAYORÍA ABSOLUTA", bg=LIME, fg=INK, size=26)
    body += flecha("fmit", (cx, 160), (cx, 225), col=CORAL, w=10)
    body += etiqueta("tmit", cx, 128, "MITAD + 1", bg=CORAL, fg="#FFFFFF", size=24)
    guardar(f"{OUT}/votacion1.svg", svg(body, "panel", fondo=fondo_suave()))


# ---------------------------------------------------------------- 5. 48 horas después (free)
def horas48():
    rel = C.reloj("rel", 500, 400, 190, 12, 0, col_marco=AZUL)
    body = rel
    body += icono_no("nolle", 250, 190, 56)
    body += etiqueta("tnolle", 250, 285, "NO LLEGA", bg=CORAL, fg="#FFFFFF", size=28)
    body += contador("c48", 500, 700, "48 H", w=260, h=110)
    body += etiqueta("t2v", 780, 190, "2.ª VOTACIÓN", bg=LIME, fg=INK, size=30)
    body += P.urna("urna", 820, 800, 210, 220, texto="SÍ / NO")
    guardar(f"{OUT}/horas48_free.svg", svg(body, "free", h=900))


# ---------------------------------------------------------------- 6. mayoría simple: más síes que noes (panel)
def simple():
    def monton(n, col, seed):
        import random
        rnd = random.Random(seed)
        o, k = "", 0
        filas = [5, 4, 3, 2, 1]
        for fi, c in enumerate(filas):
            for j in range(c):
                if k >= n:
                    break
                x = (j - (c - 1) / 2) * 34 + rnd.uniform(-2, 2)
                y = -16 - fi * 28
                o += (f'<circle cx="{f(x)}" cy="{f(y)}" r="16" fill="{col}" stroke="{INK}" stroke-width="4"/>'
                      f'<circle cx="{f(x-5)}" cy="{f(y-6)}" r="4.5" fill="#FFFFFF" opacity="0.6"/>')
                k += 1
        return o
    kw = dict(izq=monton(12, LIME, 1), der=monton(8, CORAL, 2), txt_izq="SÍ", txt_der="NO")
    eq = TE.balanza("bal_eq", 420, 640, 480, 0, **kw)
    ti = TE.balanza("bal_ti", 420, 640, 480, -12, **kw)
    body = eq + ti
    body += etiqueta("tmas", 420, 95, "MÁS SÍES QUE NOES", bg=LIME, fg=INK, size=30)
    ab = ""
    for k in range(3):
        ab += (f'<circle cx="{870 + (k-1)*44}" cy="420" r="18" fill="#9AA3B5" stroke="{INK}" stroke-width="4"/>'
               f'<circle cx="{864 + (k-1)*44}" cy="413" r="5" fill="#FFFFFF" opacity="0.6"/>')
    body += g("abst", ab + etiqueta(None, 870, 480, "ABSTENCIÓN", bg="#FFFFFF", fg=INK, size=24))
    body += sello("nocuenta", 865, 300, "NO CUENTA", 26, -8, col=INK)
    body += etiqueta("tsimp", 850, 600, "MAYORÍA SIMPLE", bg=INK, fg=LIME, size=26)
    guardar(f"{OUT}/simple.svg", svg(body, "panel", fondo=fondo_suave()))


# ---------------------------------------------------------------- 7. dos meses para más candidatos (panel)
def dosmeses():
    body = P.calendario("cal1", 170, 330, 190, 210, "1.ª VOT.", "DÍA 1", rot_=-5)
    body += P.calendario("cal2", 830, 330, 190, 210, "PLAZO", "+2 M", rot_=5)
    body += flecha("fpl", (285, 330), (715, 330), col=LIME, curva=-0.25)
    body += etiqueta("t2m", 500, 150, "2 MESES", bg=LIME, fg=INK, size=38)
    body += PI.reloj_arena("arena", 500, 330, 150)
    cands = ""
    for i, x in enumerate((330, 500, 670)):
        cands += g(f"cand{i}", tarjeta(None, x, 560, 130, 150, acento=LIME,
                                        body=pictograma(None, x, 560, 74, ("#7B5CFF", "#2EC4B6", "#FFC83D")[i]) + T(x, 622, "¿?", 24)))
    body += cands
    body += etiqueta("tdesde", 170, 470, "DESDE AQUÍ", bg=CORAL, fg="#FFFFFF", size=22)
    guardar(f"{OUT}/dosmeses.svg", svg(body, "panel", fondo=fondo_suave()))


# ---------------------------------------------------------------- 8. disolución y nuevas elecciones (full)
def disolucion():
    cx, cy, r0, r1, fl = 540, 860, 150, 300, 7
    h = P.hemiciclo("hemi", cx, cy, 350, fl, r0, r1, GRIS_E)
    body = h
    body += sello("disu", cx, cy - 150, "DISUELTAS", 56, -10, col=CORAL)
    body += etiqueta("tcortes", cx, cy + 70, "CORTES GENERALES", size=30)
    u = P.urna("urna", 720, 1250, 240, 260, texto="CONGRESO")
    ana = persona("ana", 330, 1250, 1.0, "adulto", "morena", "coleta", "negro", "chaqueta", TEAL,
                  expresion="neutral", brazos=("relajado", "sujeta"), mira=1)
    so = P.sobre(720, 880, 120, 82, -6, id_="sobre")
    body += ana + u + so
    body += etiqueta("t16", 250, 500, "26 JUN 2016", bg=LIME, fg=INK, size=40)
    body += etiqueta("t19", 830, 500, "10 NOV 2019", bg=LIME, fg=INK, size=40)
    body += etiqueta("totra", 720, 1310, "¡A VOTAR OTRA VEZ!", bg=INK, fg=LIME, size=30)
    guardar(f"{OUT}/disolucion_full.svg", svg(body, "full", fondo=P.colegio_electoral(rotulo=None)))


gancho(); ley(); consultas(); votacion1(); horas48(); simple(); dosmeses(); disolucion()

"""lote10-05-guantes-pantalla: dibujos de «¿Por qué una salchicha usa tu móvil y tu guante no?». En PAPEL.
Uso: python3 libreria/archivo/guantes-pantalla/dib.py

Todo en papel recortado (libreria/svg/papel.py), fondos claros para que los subtítulos en tinta se lean.
Piezas nuevas reutilizables en tecnologia.py: mano_guante, salchicha, mano_salchicha, campo_electrico, pantalla_capas,
paquete_salchichas.
"""
import random
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from libreria.svg.base import *  # noqa
from libreria.svg.personajes import persona
from libreria.svg.papel import (a_papel, recorte, fondo_calle, fondo_neutro, grano, fx, PAPEL as PP)
from libreria.svg.objetos import casa as K, tecnologia as TE, cuerpo as C
from libreria.svg.objetos.noche import mano_indice

OUT = ROOT / "content" / "lote10-05-guantes-pantalla"
OUT.mkdir(parents=True, exist_ok=True)
TXT = PP["tinta"]
LANA = "#D8443A"


def rotulo(id_, cx, cy, text, size=32, col=None, bg=None, semilla=0):
    """Tira de papel con texto."""
    col = col or PP["crema"]
    bg = bg or TXT
    w = len(text) * size * 0.8 + 50
    h = size * 1.7
    s = recorte(f"M {f(cx-w/2)} {f(cy-h/2)} L {f(cx+w/2)} {f(cy-h/2+3)} L {f(cx+w/2-4)} {f(cy+h/2)} L {f(cx-w/2+3)} {f(cy+h/2-2)} Z", bg, semilla, "papelFino")
    s += T(cx, cy + size * 0.36, text, size, col, font=DISP)
    return g(id_, s)


def copos(prefijo, n, w, h, seed, r=(14, 26)):
    rnd = random.Random(seed)
    s = ""
    for i in range(n):
        s += g(f"{prefijo}{i}", f'<g{fx("papelFino")}>' + copo(rnd.uniform(40, w - 40), rnd.uniform(40, h * 0.6), rnd.uniform(*r), rnd.uniform(0, 60), PP["crema"]) + "</g>")
    return s


def pantalla_apps(cx, cy, w):
    x0, y0, x1, y1 = TE.pantalla_movil(cx, cy, w)
    o = f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(x1-x0)}" height="{f(y1-y0)}" fill="{PP["cielo"]}"/>'
    o += T(cx, y0 + (x1 - x0) * 0.3, "14:00", (x1 - x0) * 0.16, TXT, font=DISP)
    cols = ((PP["verde"], "chat"), (PP["coral"], "play"), (PP["lavanda"], "mapa"), (PP["mostaza"], "nota"), (PP["rosa"], "foto"), (PP["azul_osc"], "juego"))
    sw = x1 - x0
    o += "".join(TE.icono_app(None, x0 + sw * 0.22 + (k % 3) * sw * 0.28, y0 + sw * 0.62 + (k // 3) * sw * 0.32, sw * 0.2, c, gl)
                 for k, (c, gl) in enumerate(cols))
    return o


def diana(id_, cx, cy, r, semilla=0):
    s = "".join(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r*k)}" fill="{c}"/>' for k, c in ((1, PP["coral"]), (0.66, PP["crema"]), (0.33, PP["coral"])))
    return g(id_, f'<g{fx("papelFino")}>{s}</g>')


def bandera_corea(id_, cx, cy, w=240):
    """Bandera de Corea del Sur: blanca, taegeuk rojo y azul y los cuatro trigramas negros. Mástil a la izquierda."""
    h = w * 2 / 3
    x0, y0 = cx - w / 2, cy - h / 2
    r = h * 0.25
    o = f'<rect x="{f(x0-14)}" y="{f(y0-10)}" width="10" height="{f(h+200)}" rx="5" fill="{PP["madera"] if "madera" in PP else "#8A5A32"}"/>'
    o += recorte(f"M {f(x0)} {f(y0)} L {f(x0+w)} {f(y0+4)} L {f(x0+w-3)} {f(y0+h)} L {f(x0+2)} {f(y0+h-3)} Z", "#FFFFFF", 61, "papelCapa", giro=0)
    tg = (f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="#0047A0"/>'
          f'<path d="M {f(cx-r)} {f(cy)} A {f(r)} {f(r)} 0 0 1 {f(cx+r)} {f(cy)} A {f(r/2)} {f(r/2)} 0 0 1 {f(cx)} {f(cy)} A {f(r/2)} {f(r/2)} 0 0 0 {f(cx-r)} {f(cy)} Z" fill="#CD2E3A"/>')
    tri = ""
    bw, bh, gap = w * 0.12, h * 0.035, h * 0.022
    for (dx, dy, ang, pat) in ((-1, -1, -56, "111"), (1, 1, -56, "000"), (1, -1, 56, "010"), (-1, 1, 56, "101")):
        tx, ty = cx + dx * w * 0.3, cy + dy * h * 0.3
        b = ""
        for k, full in enumerate(pat):
            yy = -1.5 * bh - gap + k * (bh + gap)
            if full == "1":
                b += f'<rect x="{f(-bw/2)}" y="{f(yy)}" width="{f(bw)}" height="{f(bh)}" fill="{TXT}"/>'
            else:
                b += (f'<rect x="{f(-bw/2)}" y="{f(yy)}" width="{f(bw*0.45)}" height="{f(bh)}" fill="{TXT}"/>'
                      f'<rect x="{f(bw*0.05)}" y="{f(yy)}" width="{f(bw*0.45)}" height="{f(bh)}" fill="{TXT}"/>')
        tri += f'<g transform="translate({f(tx)} {f(ty)}) rotate({f(ang)})">{b}</g>'
    o += f'<g{fx("papelPlano")}>{tg}{tri}</g>'
    return g(id_, o)


# ============================================================== 0 · gancho (full)
def gancho():
    body = fondo_calle("dia")
    kw = dict(edad="joven", piel="media", pelo="largo", pelo_color="negro", ropa="abrigo", ropa_color=PP["azul"],
              pantalon_color=PP["azul_osc"], accesorios=("gorro", "bufanda"), bufanda_color=PP["mostaza"], brazos=("relajado", "sujeta"),
              estilo="papel")
    body += g("chica", persona("chn", 300, 1290, 1.4, expresion="neutral", **kw) + persona("chs", 300, 1290, 1.4, expresion="duda", **kw))
    tw = 240
    tx, ty = 620, 760
    pant = pantalla_apps(tx, ty, tw)
    pant += g("tq", onda_expansiva(None, tx + 10, ty + 20, 46, PP["mostaza"], 9))
    body += a_papel(K.movil("tel", tx, ty, tw, pantalla=pant), semilla=3)
    # mano con salchicha y mano con guante: la punta toca la pantalla
    body += a_papel(TE.mano_salchicha("ms", tx + 10, ty + 20, 1.25, piel=PP["piel"], manga=PP["coral"], ang=-55), semilla=4)
    body += a_papel(TE.mano_guante("mg", tx + 10, ty + 20, 1.25, col=LANA, ang=-55), semilla=5)
    body += a_papel(icono_ok("ok", 860, 560, 62, PP["verde"]), semilla=6, filtro="papelFino")
    body += a_papel(icono_no("no", 860, 560, 62, PP["coral"]), semilla=7, filtro="papelFino")
    body += g("temb", f'<g{fx("papelFino")}>' + temblor(960, 820, 110, PP["azul_osc"]) + "</g>")
    body += copos("cp", 9, 1080, 1300, 11)
    body += grano()
    guardar(OUT / "gancho_full.svg", svg(body, "full"))


# ============================================================== 1 · Corea, 2010 (free 860)
def corea():
    body = bandera_corea("bcor", 190, 120, 230)
    body += a_papel(C.termometro("termo", 900, 30, 220, 0.12, col=PP["azul"], marcas=5), semilla=20)
    body += rotulo("et_2010", 560, 70, "COREA DEL SUR, 2010", 34, semilla=21)
    ropa = (PP["coral"], PP["verde_osc"] if "verde_osc" in PP else PP["verde"], PP["mostaza_osc"] if "mostaza_osc" in PP else PP["mostaza"])
    bufs = (PP["mostaza"], PP["coral"], PP["azul"])
    pieles = ("clara", "media", "morena")
    pelos = ("corto", "largo", "rizado")
    for i, x in enumerate((185, 500, 815)):
        p = persona(f"p{i}", x, 850, 0.98, edad="adulto", piel=pieles[i], pelo=pelos[i], pelo_color="negro", ropa="abrigo",
                    ropa_color=ropa[i], pantalon_color=PP["azul_osc"], accesorios=("gorro", "bufanda"), bufanda_color=bufs[i],
                    expresion="risa" if i == 1 else "neutral", brazos=("relajado", "sujeta"), estilo="papel")
        mx, my = p.puntos["mano_der"]
        lx, ly = p.puntos["mano_izq"]
        extra = a_papel(TE.salchicha(f"s{i}", mx - 6, my - 70, 130, -18), semilla=22 + i, filtro="papelFino")
        extra += a_papel(g(None, f'<ellipse cx="{f(mx)}" cy="{f(my)}" rx="30" ry="34" fill="{LANA}" stroke="{INK}" stroke-width="5"/>'
                           f'<ellipse cx="{f(lx)}" cy="{f(ly)}" rx="28" ry="32" fill="{LANA}" stroke="{INK}" stroke-width="5"/>'), semilla=25 + i, filtro="papelFino")
        body += g(f"gp{i}", p + extra)
    body += rotulo("et_guantes", 500, 820, "¡SIN QUITARSE LOS GUANTES!", 30, bg=PP["coral"], semilla=28)
    body += copos("cq", 7, 1000, 860, 31, (10, 18))
    guardar(OUT / "corea_free.svg", svg(body, "free", h=860))


# ============================================================== 2 · ventas disparadas (panel)
def ventas():
    body = fondo_neutro(1000, 700, PP["hueso"])
    body += a_papel(TE.paquete_salchichas("paq", 250, 380, 320, col=PP["coral"]), semilla=40)
    body += a_papel(destellos("dest", 250, 380, 210, PP["mostaza"]), semilla=41, filtro="papelFino")
    base = 590
    body += recorte(f"M 520 {base} L 960 {base-2} L 960 {base+12} L 520 {base+14} Z", TXT, 42, "papelPlano", giro=0)
    body += a_papel(barra("b_antes", 560, base, 140, 220, col="#B9B3A8"), semilla=43, giro=0)
    body += a_papel(barra("b_2010", 770, base, 140, 310, col=PP["verde"]), semilla=44, giro=0)
    body += g("t_antes", T(630, base + 50, "ANTES", 34, TXT, font=DISP))
    body += g("t_2010", T(840, base + 50, "2010", 34, TXT, font=DISP))
    body += a_papel(flecha("fl_sube", (640, 300), (800, 200), col=PP["coral"], w=12, punta=30, curva=-0.3), semilla=45, filtro="papelFino")
    body += grano(1000, 700)
    guardar(OUT / "ventas_panel.svg", svg(body, "panel"))


# ============================================================== 3 · pantalla capacitiva (full)
def capacitiva():
    body = fondo_neutro(1080, 1920, PP["cielo"])
    tw = 220
    tx, ty = 230, 700
    body += a_papel(K.movil("tel3", tx, ty, tw, pantalla=pantalla_apps(tx, ty, tw)), semilla=50)
    body += a_papel(flecha("fl3", (330, 900), (470, 960), col=PP["coral"], w=12, punta=30, curva=0.3), semilla=51, filtro="papelFino")
    capas = TE.pantalla_capas("cap", 70, 1010, 980, 1.15)
    body += a_papel(capas, semilla=52, filtro="papelCapa", giro=0)
    body += g("t_cristal", T(860, 1021, "CRISTAL", 28, TXT, font=DISP))
    body += rotulo("et_rej", 260, 1210, "REJILLA", 28, bg=PP["azul_osc"], semilla=53)
    body += rotulo("et_cap", 700, 540, "CAPACITIVA", 36, bg=PP["coral"], semilla=54)
    body += rotulo("et_det", 680, 640, "DETECTA ELECTRICIDAD", 30, semilla=55)
    body += rotulo("et_nop", 700, 735, "NO PRESIÓN", 30, bg=PP["azul_osc"], semilla=56)
    body += grano()
    guardar(OUT / "capacitiva_full.svg", svg(body, "full"))


def _corte_panel(x0, x1, y, toque, pref, semilla):
    o = a_papel(TE.pantalla_capas(f"{pref}cap", x0, x1, y, 0.9, campo=False), semilla=semilla, filtro="papelCapa", giro=0)
    o += g(None, f'<g{fx("papelFino")}>' + TE.campo_electrico(f"{pref}n", x0 + 10, x1 - 10, y - 6, 0.9, col=PP["azul"]) + "</g>")
    o += g(None, f'<g{fx("papelFino")}>' + TE.campo_electrico(f"{pref}d", x0 + 10, x1 - 10, y - 6, 0.9, toque=toque, col=PP["azul"]) + "</g>")
    return o


# ============================================================== 4 · tu dedo conduce (panel)
def dedo():
    body = fondo_neutro(1000, 700, PP["hueso"])
    body += _corte_panel(40, 760, 470, 400, "c4", 60)
    s = 0.85
    body += a_papel(mano_indice("dedo", 400 - 16 * s, 230 - 440 * s, s, piel=PP["piel"], manga=PP["azul"], ang=180), semilla=61)
    body += diana("dia", 400, 492, 26)
    body += a_papel(g("ray", f'<path d="M 520 120 L 480 200 L 510 200 L 490 270 L 560 170 L 528 170 L 548 120 Z" fill="{PP["mostaza"]}" stroke="{INK}" stroke-width="5"/>'), semilla=62, filtro="papelFino")
    body += a_papel(TE.chip("chip", 880, 300, 150, "CPU"), semilla=63)
    body += a_papel(flecha("fl4", (720, 520), (860, 400), col=PP["coral"], w=12, punta=30, curva=-0.3), semilla=64, filtro="papelFino")
    body += rotulo("et_aqui", 880, 120, "¡AQUÍ!", 34, bg=PP["coral"], semilla=65)
    body += grano(1000, 700)
    guardar(OUT / "dedo_panel.svg", svg(body, "panel"))


# ============================================================== 5 · lana aislante, salchicha conduce (panel)
def lana():
    body = fondo_neutro(1000, 700, PP["hueso"])
    body += _corte_panel(40, 960, 480, 720, "c5", 70)
    body += a_papel(TE.mano_guante("mg5", 300, 418, 0.8, col=LANA, ang=180), semilla=71)
    body += a_papel(TE.mano_salchicha("ms5", 720, 300, 0.8, piel=PP["piel"], manga=PP["azul"], ang=180), semilla=72)
    body += rotulo("et_lana", 140, 150, "LANA", 30, bg=LANA, semilla=73)
    body += rotulo("et_cuero", 150, 235, "CUERO", 30, bg="#8A5A32", semilla=74)
    body += a_papel(aspa("asp", 430, 330, 36, PP["coral"], 12), semilla=75, filtro="papelFino", giro=0)
    body += a_papel(icono_ok("ok5", 870, 230, 50, PP["verde"]), semilla=76, filtro="papelFino")
    body += grano(1000, 700)
    guardar(OUT / "lana_panel.svg", svg(body, "panel"))


if __name__ == "__main__":
    gancho()
    corea()
    ventas()
    capacitiva()
    dedo()
    lana()
    print("ok:", sorted(p.name for p in OUT.glob("*.svg")))

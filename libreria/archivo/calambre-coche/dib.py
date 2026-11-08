"""lote10-06-calambre-coche: dibujos de «¿Por qué te da calambre al tocar el coche?». En PAPEL.
Uso: python3 libreria/archivo/calambre-coche/dib.py   (después: python3 libreria/archivo/calambre-coche/guion.py)

Todo en papel recortado (libreria/svg/papel.py), fondos claros para que los subtítulos en tinta se lean.
Piezas nuevas reutilizables: coches.turismo_lateral, coches.asiento_frontal, casa.globo_frotado, casa.pelos_punta,
casa.jersey_colgado, casa.zapato_lado.
"""
import random
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from libreria.svg.base import *  # noqa
from libreria.svg.personajes import persona
from libreria.svg.papel import (a_papel, recorte, fondo_calle, fondo_neutro, grano, fx, PAPEL as PP)
from libreria.svg.objetos import casa as K, coches as CO, cuerpo as C
from libreria.svg.objetos.aviones import cochecito, signo_presion
from libreria.svg.objetos.noche import mano_indice

OUT = ROOT / "content" / "lote10-06-calambre-coche"
OUT.mkdir(parents=True, exist_ok=True)
TXT = PP["tinta"]
ROJO = PP["coral"]


def rotulo(id_, cx, cy, text, size=32, col=None, bg=None, semilla=0):
    """Tira de papel con texto."""
    col = col or PP["crema"]
    bg = bg or TXT
    w = len(text) * size * 0.8 + 50
    h = size * 1.7
    s = recorte(f"M {f(cx-w/2)} {f(cy-h/2)} L {f(cx+w/2)} {f(cy-h/2+3)} L {f(cx+w/2-4)} {f(cy+h/2)} L {f(cx-w/2+3)} {f(cy+h/2-2)} Z", bg, semilla, "papelFino")
    s += T(cx, cy + size * 0.36, text, size, col, font=DISP)
    return g(id_, s)


def mas(id_, cx, cy, r=28, semilla=0):
    """Signo «+» de carga en disco coral (papel fino)."""
    return a_papel(signo_presion(id_, cx, cy, r, "+", col=ROJO), semilla=semilla, filtro="papelFino")


def cargas(prefijo, pts, r=28, semilla=0):
    return "".join(mas(f"{prefijo}{i}", x, y, r, semilla + i) for i, (x, y) in enumerate(pts))


def zigzag(cx0, cy0, cx1, cy1, n=6, amp=26, seed=3):
    rnd = random.Random(seed)
    pts = [(cx0, cy0)]
    for i in range(1, n):
        t = i / n
        pts.append((cx0 + (cx1 - cx0) * t, cy0 + (cy1 - cy0) * t + (amp if i % 2 else -amp) * rnd.uniform(0.7, 1.2)))
    pts.append((cx1, cy1))
    return "M " + " L ".join(f"{f(x)} {f(y)}" for x, y in pts)


HOMBRE = dict(edad="adulto", piel="clara", pelo="corto", pelo_color="castano", ropa="chaqueta", ropa_color=PP["azul_marino"],
              camisa_color=PP["crema"], pantalon_color=PP["gris_osc"], accesorios=("barba",), estilo="papel")


# ============================================================== 0 · gancho (full)
def gancho():
    body = fondo_calle("dia", farola=False)
    coche = CO.turismo_lateral("coche", -179, 1250, 1.8, col=ROJO)
    body += a_papel(coche, semilla=3)
    kw = dict(HOMBRE, brazos=("relajado", "explica"))
    body += g("hombre", persona("hn", 300, 1320, 1.35, expresion="neutral", **kw) + persona("hs", 300, 1320, 1.35, expresion="sorpresa", **kw))
    hx, hy = 512, 858
    body += a_papel(rayos("rays", hx, hy, 70, 150, 10, PP["mostaza"], 12, 0, 360), semilla=4, filtro="papelFino", giro=0)
    body += a_papel(chispa("chis", hx, hy, 80, PP["mostaza"], 8), semilla=5, filtro="papelFino", giro=0)
    body += a_papel(onomatopeya("zas", 790, 580, "¡ZAS!", r=118, size=56, col=PP["mostaza"], fg=TXT), semilla=6, filtro="papelFino")
    body += g("temb", f'<g{fx("papelFino")}>' + temblor(150, 640, 110, PP["azul_osc"]) + "</g>")
    body += grano()
    guardar(OUT / "gancho_full.svg", svg(body, "full"))


# ============================================================== 1 · te cargas en el asiento (free 900)
def asiento():
    body = ""
    # hueco de la puerta abierta, a la derecha
    body += recorte("M 724 190 L 950 186 L 954 884 L 728 886 Z", PP["gris"], 10, "papelBorde", giro=0)
    body += recorte("M 752 220 L 922 218 L 926 860 L 756 862 Z", PP["cielo"], 11, "papelPlano", giro=0)
    body += g("calle1", f'<g{fx("papelPlano")}><path d="M 756 700 L 926 690 L 926 862 L 756 862 Z" fill="{PP["hueso"]}"/></g>')
    body += a_papel(CO.asiento_frontal("asi", 380, 682, 1.1, col=PP["azul_osc"]), semilla=12)
    body += g("roce", f'<g{fx("papelFino")}>' + "".join(
        f'<path d="M {x} {y} q 14 -10 28 0 t 28 0" fill="none" stroke="{TXT}" stroke-width="6" stroke-linecap="round"/>'
        for x, y in ((180, 668), (520, 672), (200, 712), (500, 714))) + "</g>")
    kw = dict(HOMBRE, pose="sentado", brazos=("relajado", "explica"))
    pts = ((320, 520), (460, 480), (390, 600), (290, 760), (480, 750))
    body += g("conductor", persona("cn", 380, 880, 1.55, expresion="neutral", **kw) + persona("cs", 380, 880, 1.55, expresion="sorpresa", **kw)
              + cargas("m1_", pts, 28, 20))
    body += a_papel(cochecito("coch", 150, 200, 1.1, col=ROJO), semilla=13)
    body += a_papel(aspa("asp1", 150, 160, 52, PP["coral_osc"], 12), semilla=14, filtro="papelFino", giro=0)
    body += rotulo("et_tu", 820, 300, "¡ERES TÚ!", 30, bg=ROJO, semilla=15)
    body += rotulo("et_est", 700, 64, "ELECTRICIDAD ESTÁTICA", 26, semilla=16)
    body += a_papel(flecha("fl1", (560, 820), (700, 820), col=PP["mostaza"], w=12, punta=30), semilla=17, filtro="papelFino")
    guardar(OUT / "asiento_free.svg", svg(body, "free", h=900))


# ============================================================== 2 · suelas de goma y globo (free 860)
def goma():
    body = recorte("M 40 700 L 480 696 L 482 716 L 42 720 Z", PP["kraft"], 30, "papelPlano", giro=0)
    body += a_papel(K.zapato_lado("zap", 60, 700, 0.95, col=ROJO), semilla=31)
    body += cargas("m2z", ((150, 600), (240, 625), (330, 655)), 24, 32)
    body += a_papel(flecha("fl2", (240, 560), (240, 690), col=PP["azul_osc"], w=10, punta=26), semilla=35, filtro="papelFino")
    body += a_papel(aspa("asp2", 380, 740, 32, PP["coral_osc"], 11), semilla=36, filtro="papelFino", giro=0)
    body += rotulo("et_goma", 200, 790, "GOMA", 30, bg=PP["azul_osc"], semilla=37)
    kw = dict(edad="joven", piel="media", pelo="corto", pelo_color="negro", ropa="jersey", ropa_color=PP["mostaza"],
              pantalon_color=PP["azul_osc"], brazos=("coge", "relajado"), estilo="papel")
    p = persona("chi", 740, 850, 1.2, expresion="risa", **kw)
    body += K.pelos_punta("pelos", 753, 150, 150, 7, "#2F2724", 80, 0.0)
    body += g("chico", str(p) + cargas("m2p", ((700, 520), (800, 470), (760, 600)), 24, 40))
    body += a_papel(K.globo_frotado("globo", 575, 445, 78, ROJO), semilla=45)
    guardar(OUT / "goma_free.svg", svg(body, "free", h=860))


# ============================================================== 3 · la chispa (full)
def chispa_full():
    body = fondo_neutro(1080, 1920, PP["cielo"])
    # puerta del coche en primer plano: marco, cristal y chapa
    puerta = recorte("M 560 330 L 1180 320 L 1190 1250 L 566 1256 Z", ROJO, 50, "papelBorde", giro=0)
    puerta += recorte("M 600 360 L 1180 352 L 1180 640 L 604 648 Z", PP["crema"], 51, "papelPlano", giro=0)
    puerta += f'<g{fx("papelPlano")}><path d="M 640 380 L 600 470 M 700 380 L 640 520" stroke="#FFFFFF" stroke-width="16" stroke-linecap="round" opacity="0.7"/></g>'
    puerta += recorte("M 566 700 L 1180 690 L 1180 708 L 566 718 Z", PP["coral_osc"], 52, "papelPlano", giro=0)
    puerta += recorte("M 700 800 L 820 796 L 822 830 L 702 834 Z", TXT, 53, "papelFino", giro=0)
    body += g("puerta", puerta)
    body += rotulo("et_metal", 860, 1010, "METAL", 34, bg=TXT, semilla=54)
    tx, ty, k = 380, 880, 1.5
    body += a_papel(mano_indice("dedo", tx - 220 - 8 * k, ty - 220, k, piel=PP["piel"], manga=PP["azul_marino"], ang=90), semilla=55)
    body += g("cargas3", cargas("m3_", ((90, 830), (200, 960), (150, 760), (40 + 30, 930)), 30, 56))
    body += g("rayo3", f'<g{fx("papelFino")}>' + trazo(zigzag(445, 880, 566, 880, 6, 30), 14, PP["mostaza"], 6) + "</g>")
    body += a_papel(destellos("dest3", 566, 880, 110, PP["mostaza"]), semilla=57, filtro="papelFino", giro=0)
    body += g("ondas", g("on1", onda_expansiva(None, 566, 880, 90, PP["mostaza"], 9)) + g("on2", onda_expansiva(None, 566, 880, 90, PP["mostaza"], 9)))
    body += rotulo("et_chispa", 820, 1140, "¡CHISPA!", 36, bg=PP["mostaza_osc"], col=TXT, semilla=58)
    body += a_papel(onomatopeya("zas3", 300, 620, "¡ZAS!", r=110, size=52, col=PP["mostaza"], fg=TXT), semilla=59, filtro="papelFino")
    body += grano()
    guardar(OUT / "chispa_full.svg", svg(body, "full"))


# ============================================================== 4 · aire húmedo / aire seco (panel)
def aire():
    body = fondo_neutro(1000, 700, PP["cielo"])
    body += recorte("M 500 0 L 1000 0 L 1000 700 L 504 700 Z", PP["arena"], 60, "papelPlano", giro=0)
    kw = dict(edad="adulto", pelo="corto", ropa="jersey", pantalon_color=PP["azul_osc"], pose="busto", brazos=("relajado", "relajado"), estilo="papel")
    body += g("bh", persona("ph", 245, 720, 1.4, piel="media", pelo_color="castano", ropa_color=PP["verde"], expresion="risa", **kw))
    body += g("bs", persona("ps", 755, 720, 1.4, piel="clara", pelo_color="rubio", ropa_color=PP["lavanda"], expresion="duda", **kw))
    rnd = random.Random(61)
    body += "".join(g(f"gt{i}", f'<g{fx("papelFino")}>' + gota(x, y, 13, PP["azul"]) + "</g>")
                    for i, (x, y) in enumerate(((80, 330), (420, 300), (110, 520), (440, 470), (150, 220), (360, 210))))
    body += g("pelicula", f'<g{fx("papelFino")}><path d="M 40 640 Q 60 540 140 520 Q 250 480 360 520 Q 440 540 460 640" fill="none" stroke="{PP["azul"]}" stroke-width="14" stroke-linecap="round" stroke-dasharray="4 22" opacity="0.9"/></g>')
    body += cargas("mh", ((200, 600), (300, 610), (250, 660)), 24, 62)
    body += cargas("ms", ((700, 600), (800, 610), (750, 660), (690, 670)), 24, 66)
    body += rotulo("et_hum", 250, 110, "HÚMEDO", 30, bg=PP["azul_osc"], semilla=70)
    body += rotulo("et_seco", 750, 110, "SECO", 30, bg=PP["coral_osc"], semilla=71)
    body += g("copo4", f'<g{fx("papelFino")}>' + copo(600, 210, 34, 0, PP["azul_osc"]) + "</g>")
    body += a_papel(C.termometro("termo4", 905, 170, 200, 0.15, col=PP["azul"], marcas=4), semilla=72)
    body += grano(1000, 700)
    guardar(OUT / "aire_panel.svg", svg(body, "panel"))


# ============================================================== 5 · algodón y poliéster (panel)
def ropa():
    body = fondo_neutro(1000, 700, PP["hueso"])
    body += recorte("M 70 100 L 930 96 L 932 116 L 72 120 Z", PP["madera"], 80, "papelBorde", giro=0)
    body += a_papel(K.jersey_colgado("jalg", 270, 108, 300, col=PP["verde"], texto="ALGODÓN", size=26), semilla=81)
    body += a_papel(K.jersey_colgado("jpol", 730, 108, 300, col=PP["azul"], rayas=PP["crema"], texto="POLIÉSTER", size=26), semilla=82)
    body += cargas("ma", ((230, 330), (310, 400)), 24, 83)
    body += cargas("mp", ((660, 290), (750, 270), (820, 320), (690, 380), (790, 400), (720, 460), (820, 470)), 24, 86)
    body += rotulo("et_pol", 500, 625, "POLIÉSTER: MÁS CARGA", 28, bg=ROJO, semilla=95)
    body += grano(1000, 700)
    guardar(OUT / "ropa_panel.svg", svg(body, "panel"))


if __name__ == "__main__":
    gancho()
    asiento()
    goma()
    chispa_full()
    aire()
    ropa()
    print("ok:", sorted(p.name for p in OUT.glob("*.svg")))

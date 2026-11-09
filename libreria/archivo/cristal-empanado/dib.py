"""lote10-07-cristal-empanado: dibujos de «¿Por qué se empañan por dentro los cristales del coche?». En PAPEL.
Uso: python3 libreria/archivo/cristal-empanado/dib.py

Todo en papel recortado (libreria/svg/papel.py), con lo de debajo de y 1300 claro para que los subtítulos se lean.
Piezas nuevas reutilizables: coches.interior_coche, coches.vaho_parabrisas, coches.boton_clima, casa.paraguas_cerrado,
casa.esponja.
"""
import math
import random
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from libreria.svg.base import *  # noqa
from libreria.svg.personajes import persona
from libreria.svg.papel import a_papel, recorte, fondo_neutro, grano, fx, PAPEL as PP
from libreria.svg.objetos import casa as K, coches as CO, cuerpo as C
from libreria.svg.objetos.mente import pivote

OUT = ROOT / "content" / "lote10-07-cristal-empanado"
OUT.mkdir(parents=True, exist_ok=True)
TXT = PP["tinta"]
VAPOR = PP["azul"]


def rotulo(id_, cx, cy, text, size=32, col=None, bg=None, semilla=0):
    """Tira de papel con texto."""
    col = col or PP["crema"]
    bg = bg or TXT
    w = len(text) * size * 0.8 + 50
    h = size * 1.7
    s = recorte(f"M {f(cx-w/2)} {f(cy-h/2)} L {f(cx+w/2)} {f(cy-h/2+3)} L {f(cx+w/2-4)} {f(cy+h/2)} L {f(cx-w/2+3)} {f(cy+h/2-2)} Z", bg, semilla, "papelFino")
    s += T(cx, cy + size * 0.36, text, size, col, font=DISP)
    return g(id_, s)


def molecula(id_, cx, cy, r=22):
    """Bolita de vapor de agua (papel azul con brillo)."""
    return g(id_, f'<g{fx("papelFino")}><circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{VAPOR}"/>'
                  f'<circle cx="{f(cx-r*0.35)}" cy="{f(cy-r*0.35)}" r="{f(r*0.3)}" fill="{PP["crema"]}" opacity="0.8"/></g>')


def gotita(id_, cx, cy, s=16, col=None):
    return g(id_, f'<g{fx("papelFino")}>' + gota(cx, cy, s, col or "#9CCBE4") + "</g>")


MUJER = dict(edad="adulto", piel="clara", pelo="largo", pelo_color="castano", ropa="abrigo", ropa_color=PP["mostaza"],
             camisa_color=PP["crema"], pose="busto", estilo="papel")


# ============================================================== 0 · gancho (full)
def gancho():
    body = CO.interior_coche(lluvia=True, gotas=10, semilla=7, volante=(845, 1130))
    body += CO.vaho_parabrisas("vaho", bandas=4)
    mu = persona("mu", 330, 1300, 1.8, expresion="duda", brazos=("relajado", "saluda"), **MUJER)
    body += str(mu)
    cx, cy = mu.puntos["cabeza"]
    body += a_papel(icono_duda("duda", cx - 170, cy - 200, 46), semilla=3, filtro="papelFino")
    body += grano()
    guardar(OUT / "gancho_full.svg", svg(body, "full"))
    return mu


# ============================================================== 1 · aire húmedo (panel)
def humedad():
    body = fondo_neutro(1000, 700, PP["hueso"])
    # ventanilla lateral con lluvia
    ven = recorte("M 600 70 L 930 64 Q 944 64 944 84 L 940 250 L 604 256 Z", PP["gris_osc"], 10, "papelBorde", giro=0)
    ven += recorte("M 620 86 L 922 82 L 920 236 L 622 240 Z", "#B7C7CF", 11, "papelPlano", giro=0)
    ven += f'<g{fx("papelPlano")}>' + "".join(f'<path d="M {x} {y} l -8 30" stroke="#FFFFFF" stroke-width="4" opacity="0.7" stroke-linecap="round"/>'
                                               for x, y in ((650, 100), (720, 150), (790, 110), (860, 170), (900, 100), (680, 190), (830, 200))) + "</g>"
    body += g("ventana", ven)
    body += recorte("M 120 230 Q 130 170 200 166 L 470 166 Q 540 170 546 230 L 560 700 L 110 700 Z", PP["azul_osc"], 12, "papelBorde", giro=0)
    mh = persona("mh", 330, 720, 1.75, expresion="neutral", brazos=("relajado", "explica"), **MUJER)
    body += str(mh)
    bx, by = mh.puntos["boca"]
    body += g("aliento", "".join(g(f"vh{i}", f'<g{fx("papelFino")}>' + vaho(bx + 40, by - 6, 0.9) + "</g>") for i in range(3)))
    body += g("ropag", "".join(gotita(f"rg{i}", x, y, 15) for i, (x, y) in enumerate(((240, 560), (420, 590), (300, 640), (390, 520)))))
    body += a_papel(K.paraguas_cerrado("par", 830, 650, 290, col=PP["coral"]), semilla=13)
    rnd = random.Random(14)
    body += "".join(molecula(f"vp{i}", x, y, rnd.uniform(16, 22)) for i, (x, y) in
                    enumerate(((560, 330), (640, 420), (520, 500), (700, 540), (600, 600), (930, 420))))
    body += rotulo("et_temp", 300, 100, "TEMPLADO", 30, bg=PP["coral_osc"], semilla=15)
    body += rotulo("et_hum", 770, 300, "HUMEDAD", 30, bg=PP["azul_osc"], semilla=16)
    body += grano(1000, 700)
    guardar(OUT / "humedad_panel.svg", svg(body, "panel"))
    return mh


# ============================================================== 2 · cristal frío y vaso con hielo (free 880)
MOL2 = ((600, 230), (660, 360), (560, 470), (650, 590), (590, 700))


def cristal():
    body = ""
    body += g("cristal", recorte("M 300 80 L 380 78 L 384 800 L 302 802 Z", "#CFE3EA", 20, "papelBorde", giro=0)
              + f'<g{fx("papelPlano")}><path d="M 318 110 L 318 770" stroke="#FFFFFF" stroke-width="10" opacity="0.7" stroke-linecap="round"/></g>')
    body += a_papel(C.termometro("ter", 160, 150, 440, 0.18, col=PP["azul"], marcas=5), semilla=21)
    rnd = random.Random(22)
    body += "".join(g(f"cp{i}", f'<g{fx("papelFino")}>' + copo(x, y, 26, rnd.uniform(0, 30), PP["azul_osc"]) + "</g>")
                    for i, (x, y) in enumerate(((90, 110), (240, 120), (80, 640))))
    body += rotulo("et_frio", 160, 790, "FRÍO", 32, bg=PP["azul_osc"], semilla=23)
    body += "".join(molecula(f"m{i}", x, y, 30) for i, (x, y) in enumerate(MOL2))
    body += "".join(gotita(f"d{i}", 400, y + 6, 19) for i, (x, y) in enumerate(MOL2))
    body += rotulo("et_vapor", 640, 110, "VAPOR", 30, bg=VAPOR, semilla=24)
    body += a_papel(K.vaso("vaso", 780, 840, alto=420, ancho=300, nivel=0.7, liquido="agua", cubitos=3), semilla=25)
    body += "".join(gotita(f"gv{i}", x, y, 13) for i, (x, y) in
                    enumerate(((665, 540), (900, 590), (690, 680), (885, 720), (760, 790), (850, 500))))
    guardar(OUT / "cristal_free.svg", svg(body, "free", h=880))


# ============================================================== 3 · punto de rocío: esponja (panel)
def rocio():
    body = fondo_neutro(1000, 700, PP["cielo"])
    body += a_papel(K.esponja("esp", 330, 330, 440, 250, col=PP["mostaza"], agua=PP["azul"]), semilla=30)
    body += "".join(gotita(f"gs{i}", x, 500, 18, PP["azul"]) for i, x in enumerate((240, 340, 430)))
    body += g("charco", f'<g{fx("papelPlano")}><ellipse cx="335" cy="625" rx="190" ry="20" fill="{PP["azul"]}" opacity="0.8"/></g>')
    body += a_papel(C.termometro("ter3", 800, 150, 330, 0.45, col=PP["azul"], marcas=6), semilla=31)
    ny = 150 + 330 - 330 * 0.88 * 0.45
    body += g("marca", f'<g{fx("papelFino")}><rect x="740" y="{f(ny-7)}" width="120" height="14" rx="7" fill="{PP["lima"]}"/></g>')
    body += rotulo("et_rocio", 500, 100, "PUNTO DE ROCÍO", 30, bg=TXT, semilla=32)
    body += rotulo("et_cabe", 790, 610, "NO CABE MÁS", 28, bg=PP["coral_osc"], semilla=33)
    body += grano(1000, 700)
    guardar(OUT / "rocio_panel.svg", svg(body, "panel"))


# ============================================================== 4 · recirculación (panel)
def recirc():
    body = fondo_neutro(1000, 700, PP["hueso"])
    body += a_papel(CO.boton_clima("brec", 250, 320, 150, "recirc"), semilla=40, giro=0)
    body += a_papel(aspa("asp", 250, 320, 130, PP["coral"], 26), semilla=41, filtro="papelFino", giro=0)
    body += recorte("M 470 600 L 980 596 L 980 616 L 470 620 Z", PP["gris"], 42, "papelPlano", giro=0)
    s, x0, base = 0.58, 480, 600
    body += a_papel(CO.turismo_lateral("car", x0, base, s, col=PP["azul"], cristal="#CFE3EA"), semilla=43)
    ventanas = ("M 112 -210 L 168 -308 L 330 -308 L 330 -210 Z M 346 -308 L 514 -308 Q 530 -308 540 -298 L 626 -210 L 346 -210 Z")
    body += g("cvaho", f'<g transform="translate({x0} {base}) scale({s})"><path d="{ventanas}" fill="#F4F7F6" opacity="0.9"/></g>')
    cx, cy = 717, 480
    giro_ = a_papel(CO.flecha_giro(None, cx, cy, 175, 200, -60, col=VAPOR, w=14), semilla=44, filtro="papelFino", giro=0)
    vd = "".join(molecula(f"vd{i}", cx + 175 * math.cos(math.radians(a)), cy + 175 * math.sin(math.radians(a)), 16)
                 for i, a in enumerate((230, 280, 330, 20)))
    body += g("giro", pivote(cx, cy, 195) + str(giro_) + vd)
    body += rotulo("et_mismo", 717, 150, "EL MISMO AIRE", 28, bg=VAPOR, semilla=45)
    body += rotulo("et_vaho", 250, 580, "MÁS VAHO", 30, bg=PP["coral_osc"], semilla=46)
    body += grano(1000, 700)
    guardar(OUT / "recirc_panel.svg", svg(body, "panel"))


# ============================================================== 5 · aire acondicionado en invierno (full)
MOL5 = ((200, 620), (420, 700), (640, 640), (860, 720), (330, 860), (760, 880))


def ac():
    body = CO.interior_coche(lluvia=True, gotas=10, semilla=7, volante=(845, 1130))
    body += CO.vaho_parabrisas("vaho", bandas=4)
    body += "".join(molecula(f"m{i}", x, y, 22) for i, (x, y) in enumerate(MOL5))
    body += "".join(gotita(f"gd{i}", x, 1150, 14, PP["azul"]) for i, x in enumerate((480, 540, 600)))
    body += g("calor", f'<g{fx("papelFino")}>' + "".join(ondas_calor(x, 1000, 110, PP["coral"]) for x in (470, 540, 610)) + "</g>")
    body += a_papel(CO.boton_clima("bac", 600, 1200, 62, "ac"), semilla=50, giro=0)
    kw = dict(MUJER, brazos=("relajado", "explica"))
    md = persona("md", 225, 1300, 1.8, expresion="duda", **kw)
    body += g("mujer", str(md) + str(persona("mr", 225, 1300, 1.8, expresion="risa", **kw)))
    cx, cy = md.puntos["cabeza"]
    body += a_papel(icono_duda("duda5", cx + 170, cy - 180, 44), semilla=51, filtro="papelFino")
    body += g("cpf", f'<g{fx("papelFino")}>' + copo(900, 560, 34, 10, PP["crema"]) + "</g>")
    body += rotulo("et_inv", 740, 640, "EN INVIERNO", 30, bg=PP["azul_osc"], semilla=52)
    body += a_papel(destellos("dest", 560, 700, 120, PP["mostaza"]), semilla=53, filtro="papelFino", giro=0)
    body += grano()
    guardar(OUT / "ac_full.svg", svg(body, "full"))
    return md


if __name__ == "__main__":
    import math  # noqa
    mu = gancho()
    mh = humedad()
    cristal()
    rocio()
    recirc()
    md = ac()
    for n, p in (("mu", mu), ("mh", mh), ("md", md)):
        print(n, {k: tuple(round(v) for v in p.puntos[k]) for k in ("cabeza", "boca", "mano_izq", "mano_der", "cima")}, getattr(p, "caja", None))
    print("ok:", sorted(p.name for p in OUT.glob("*.svg")))

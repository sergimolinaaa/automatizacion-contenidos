"""lote10-04-movil-20: dibujos de «¿Por qué tu móvil se apaga con el 20 % de batería?». En PAPEL.
Uso: python3 libreria/archivo/movil-20/dib.py

Todo en papel recortado (libreria/svg/papel.py). Fondos claros (calle de tarde, casa de día, cartulina) para que los
subtítulos en tinta se lean. Piezas nuevas reutilizables en tecnologia.py: escudo, calculadora.
"""
import math
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from libreria.svg.base import *  # noqa
from libreria.svg.personajes import persona
from libreria.svg.papel import (a_papel, recorte, fondo_calle, fondo_casa, fondo_neutro, grano, hoja_transicion, fx, PAPEL as PP)
from libreria.svg.objetos import casa as K, tecnologia as TE, cuerpo as C, memoria as M
from libreria.svg.objetos.mente import pivote

OUT = ROOT / "content" / "lote10-04-movil-20"
OUT.mkdir(parents=True, exist_ok=True)
TXT = PP["tinta"]


def rotulo(id_, cx, cy, text, size=32, col=None, bg=None, semilla=0):
    """Tira de papel con texto."""
    col = col or PP["crema"]
    bg = bg or TXT
    w = len(text) * size * 0.8 + 50
    h = size * 1.7
    s = recorte(f"M {f(cx-w/2)} {f(cy-h/2)} L {f(cx+w/2)} {f(cy-h/2+3)} L {f(cx+w/2-4)} {f(cy+h/2)} L {f(cx-w/2+3)} {f(cy+h/2-2)} Z", bg, semilla, "papelFino")
    s += T(cx, cy + size * 0.36, text, size, col, font=DISP)
    return g(id_, s)


def dial(id_, cx, cy, r, nivel=0.5, minimo=False, semilla=0):
    """Voltímetro semicircular de papel. Aguja en {id}_aguja con pivote (origin center = eje).
    Zonas de izquierda a derecha: coral (bajo), mostaza, verde. minimo=True rotula la zona roja «MÍNIMO»."""
    s = recorte(f"M {f(cx-r)} {f(cy)} A {f(r)} {f(r)} 0 0 1 {f(cx+r)} {f(cy)} Z", PP["crema"], semilla, "papelBorde")
    zon = ""
    for i, c in enumerate((PP["coral"], PP["mostaza"], PP["verde"])):
        a0, a1 = math.pi + i * math.pi / 3, math.pi + (i + 1) * math.pi / 3
        ri = r * 0.76
        zon += (f'<path d="M {f(cx+ri*math.cos(a0))} {f(cy+ri*math.sin(a0))} A {f(ri)} {f(ri)} 0 0 1 {f(cx+ri*math.cos(a1))} {f(cy+ri*math.sin(a1))}" '
                f'fill="none" stroke="{c}" stroke-width="{f(r*0.2)}"/>')
    s += f'<g{fx("papelPlano")}>{zon}</g>'
    s += T(cx, cy - r * 0.28, "V", r * 0.3, TXT, font=DISP)
    if minimo:
        s += g(f"{id_}_min", T(cx - r * 0.62, cy + r * 0.26, "MÍNIMO", r * 0.15, PP["coral_osc"], font=DISP))
    a = math.pi + nivel * math.pi
    tx, ty = cx + r * 0.72 * math.cos(a), cy + r * 0.72 * math.sin(a)
    ag = pivote(cx, cy, r * 0.74) + f'<path d="M {f(cx)} {f(cy)} L {f(tx)} {f(ty)}" stroke="{TXT}" stroke-width="{f(r*0.07)}" stroke-linecap="round"/>'
    ag += f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r*0.1)}" fill="{TXT}"/>'
    s += g(f"{id_}_aguja", f'<g{fx("papelFino")}>{ag}</g>')
    return g(id_, s)


def rayo(id_, cx, cy, s, col=None, semilla=0):
    col = col or PP["mostaza"]
    pts = [(0.15, -1.1), (-0.55, 0.12), (-0.02, 0.12), (-0.2, 1.1), (0.55, -0.15), (0.04, -0.15)]
    d = "M " + " L ".join(f"{f(cx+x*s)} {f(cy+y*s)}" for x, y in pts) + " Z"
    return g(id_, recorte(d, col, semilla, "papelBorde"))


def pantalla_20(id_, cx, cy, w):
    """Pantalla del móvil con «20 %» y una pila pequeña; capa {id}_negro (pantalla apagada) para fade."""
    x0, y0, x1, y1 = TE.pantalla_movil(cx, cy, w)
    sw = x1 - x0
    o = f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(sw)}" height="{f(y1-y0)}" fill="{PP["cielo"]}"/>'
    o += T(cx, y0 + sw * 0.32, "14:00", sw * 0.16, TXT, font=DISP)
    o += TE.bateria(None, cx, cy + sw * 0.02, sw * 0.34, sw * 0.6, 0.2, col=PP["mostaza"], rayo=False)
    o += g(f"{id_}_pct", T(cx, cy + sw * 0.72, "20 %", sw * 0.26, TXT, font=DISP))
    o += g(f"{id_}_negro", f'<rect x="{f(x0-4)}" y="{f(y0-4)}" width="{f(sw+8)}" height="{f(y1-y0+8)}" fill="{TXT}"/>')
    return o


# ============================================================== 0 · gancho (full)
def gancho():
    body = fondo_calle("tarde")
    kw = dict(edad="joven", piel="clara", pelo="largo", pelo_color="castano", ropa="abrigo", ropa_color=PP["mostaza_osc"],
              pantalon_color=PP["azul_osc"], accesorios=("bufanda",), bufanda_color=PP["coral"], brazos=("relajado", "sujeta"),
              estilo="papel")
    body += g("chica", persona("chn", 330, 1290, 1.38, expresion="neutral", **kw) + persona("chs", 330, 1290, 1.38, expresion="sorpresa", **kw))
    tw = 230
    body += a_papel(K.movil("tel", 610, 700, tw, pantalla=pantalla_20("tel", 610, 700, tw)), semilla=3)
    body += a_papel(onomatopeya("plof", 860, 620, "¡PLOF!", r=120, size=46, rot_=10, col=PP["mostaza"], fg=TXT), semilla=4, filtro="papelFino")
    body += grano()
    guardar(OUT / "gancho_full.svg", svg(body, "full"))


# ============================================================== 1 · número calculado (free 880)
def calculado():
    body = a_papel(TE.bateria("bm", 250, 255, 170, 290, 0.2, col=PP["mostaza"]), semilla=10)
    regla = recorte("M 70 232 L 430 226 L 432 282 L 72 288 Z", PP["arena"], 11, "papelCapa")
    regla += "".join(f'<rect x="{90+k*30}" y="{232 - k*0.5:.1f}" width="5" height="{26 if k % 2 == 0 else 16}" fill="{TXT}"/>' for k in range(12))
    body += g("regla", regla)
    body += a_papel(aspa("aspa", 250, 255, 92, PP["coral"], 16), semilla=12, filtro="papelFino", giro=0)
    body += a_papel(TE.calculadora("calc", 730, 250, 240, "20 %"), semilla=13)
    # lo que marca frente a lo que hay
    body += a_papel(TE.bateria("dig", 320, 650, 150, 250, 0.2, col=PP["mostaza"], rayo=False), semilla=14)
    body += a_papel(TE.bateria("qui", 680, 650, 150, 250, 0.06, col=PP["coral"], rayo=False), semilla=15)
    body += g("v20", T(320, 492, "20 %", 40, TXT, font=DISP))
    body += g("v05", T(680, 492, "5 %", 40, PP["coral_osc"], font=DISP))
    body += rotulo("et_marca", 320, 832, "LO QUE MARCA", 28, semilla=16)
    body += rotulo("et_hay", 680, 832, "LO QUE HAY", 28, bg=PP["coral"], semilla=17)
    body += g("dist", f'<path d="M 420 600 Q 500 560 580 600" fill="none" stroke="{TXT}" stroke-width="6" stroke-dasharray="12 10" stroke-linecap="round"/>'
              + T(500, 640, "≠", 70, PP["coral"], font=DISP))
    guardar(OUT / "calculado_free.svg", svg(body, "free", h=880))


# ============================================================== 2 · voltaje = fuerza del empujón (free 860)
def voltaje():
    bx, by, bw, bh = 290, 540, 300, 440
    bat = TE.bateria("bv", bx, by, bw, bh, 0.55, col=PP["verde"])
    top = by - bh / 2 - bh * 0.07
    body = a_papel(bat, semilla=20)
    jet = recorte(f"M {bx-34} {top+6} L {bx+34} {top+6} L {bx+70} 70 Q {bx} 40 {bx-70} 70 Z", PP["azul"], 21, "papelCapa", giro=0)
    jet += (f'<g id="jet_lin"><path d="M {bx-14} {top} L {bx-30} 90 M {bx+14} {top} L {bx+30} 90" stroke="{PP["crema"]}" stroke-width="8" '
            f'stroke-dasharray="26 22" stroke-linecap="round"/></g>')
    body += g("jet", jet)
    for i, (x, y, r) in enumerate(((bx - 90, 70, 18), (bx + 95, 60, 22), (bx - 40, 30, 14), (bx + 40, 26, 16))):
        body += g(f"go{i}", f'<g{fx("papelFino")}><circle cx="{x}" cy="{y}" r="{r}" fill="{PP["azul"]}"/></g>')
    body += dial("vm", 730, 470, 200, nivel=0.15, semilla=22)
    body += a_papel(flecha("fl_v", (560, 300), (650, 360), col=PP["coral"], w=12, punta=30, curva=-0.3), semilla=23, filtro="papelFino")
    body += rotulo("et_v", 500, 835, "VOLTAJE: LA FUERZA DEL EMPUJÓN", 30, semilla=24)
    guardar(OUT / "voltaje_free.svg", svg(body, "free", h=880))


# ============================================================== 3 · apagado de seguridad (panel)
def seguridad():
    body = fondo_neutro(1000, 700, PP["hueso"])
    body += dial("sm", 250, 470, 200, nivel=0.62, minimo=True, semilla=30)
    tw = 190
    body += a_papel(K.movil("tel3", 560, 360, tw, pantalla=pantalla_20("tel3", 560, 360, tw)), semilla=31)
    body += a_papel(TE.chip("chip", 830, 300, 170, "CPU"), semilla=32)
    body += a_papel(TE.escudo("esc", 830, 300, 150, col=PP["verde_osc"]), semilla=33)
    body += a_papel(sello("sello", 800, 560, "PROTEGIDO", 44, rot_=-8, col=PP["coral"]), semilla=34, filtro="papelFino")
    body += grano(1000, 700)
    guardar(OUT / "seguridad_panel.svg", svg(body, "panel"))


# ============================================================== 4 · batería cansada (full)
def cansada():
    body = fondo_casa()
    # alfombra clara bajo los subtítulos (la tarima es oscura para la tinta)
    body += g("alfombra", recorte("M -40 1318 L 1120 1308 L 1130 1600 L -50 1612 Z", PP["arena"], 45, "papelPlano", giro=0)
              + recorte("M -40 1350 L 1120 1340 L 1120 1356 L -40 1366 Z", PP["coral"], 46, "papelPlano", giro=0)
              + recorte("M -40 1560 L 1120 1550 L 1120 1566 L -40 1576 Z", PP["coral"], 47, "papelPlano", giro=0))
    kw = dict(edad="adulto", piel="morena", pelo="corto", pelo_color="negro", ropa="jersey", ropa_color=PP["azul"],
              pantalon_color=PP["azul_osc"], brazos=("relajado", "sujeta"), estilo="papel")
    body += g("chico", persona("cbn", 300, 1290, 1.38, expresion="neutral", **kw) + persona("cbs", 300, 1290, 1.38, expresion="sorpresa", **kw))
    tw = 220
    cx, cy = 590, 700
    x0, y0, x1, y1 = TE.pantalla_movil(cx, cy, tw)
    pant = f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(x1-x0)}" height="{f(y1-y0)}" fill="{PP["cielo"]}"/>'
    pant += "".join(TE.icono_app(None, x0 + 45 + (k % 3) * 60, y0 + 70 + (k // 3) * 70, 44, c, gl)
                    for k, (c, gl) in enumerate(((PP["verde"], "chat"), (PP["coral"], "play"), (PP["lavanda"], "mapa"),
                                                 (PP["mostaza"], "nota"), (PP["rosa"], "foto"), (PP["azul_osc"], "juego"))))
    pant += g("cam_app", TE.icono_app(None, cx, y0 + 300, 110, PP["azul_osc"], "camara"))
    body += a_papel(K.movil("tel4", cx, cy, tw, pantalla=pant), semilla=40)
    body += a_papel(TE.bateria("bg", 860, 760, 200, 330, 0.35, col=PP["mostaza"], gastada=True), semilla=41)
    body += a_papel(M.gota_esfuerzo("gota", 975, 640, 1.4), semilla=42, filtro="papelFino")
    body += rayo("ray", 740, 560, 80, semilla=43)
    body += dial("hm", 810, 1140, 130, nivel=0.7, semilla=44)
    body += g("temb", f'<g{fx("papelFino")}>' + temblor(860, 560) + "</g>")
    body += hoja_transicion("salida", PP["coral"], None)
    body += grano()
    guardar(OUT / "cansada_full.svg", svg(body, "full"))


# ============================================================== 5 · frío y poca carga (panel)
def frio():
    body = fondo_neutro(1000, 700, PP["cielo"])
    body += a_papel(g("copo", copo(150, 220, 80, 0, PP["azul_osc"])), semilla=50, filtro="papelFino")
    body += a_papel(C.termometro("termo", 290, 110, 230, 0.15, col=PP["azul"], marcas=5), semilla=51)
    body += a_papel(TE.bateria("b15", 220, 520, 120, 210, 0.15, col=PP["coral"], rayo=False), semilla=52)
    body += g("v15", T(360, 540, "15 %", 46, PP["coral_osc"], font=DISP))
    body += a_papel(flecha("fl1", (380, 230), (560, 380), col=PP["mostaza_osc"], w=14, punta=34, curva=-0.2), semilla=53, filtro="papelFino")
    body += a_papel(flecha("fl2", (450, 520), (580, 470), col=PP["mostaza_osc"], w=14, punta=34, curva=0.2), semilla=54, filtro="papelFino")
    body += dial("fm", 770, 500, 190, nivel=0.45, minimo=True, semilla=55)
    body += grano(1000, 700)
    guardar(OUT / "frio_panel.svg", svg(body, "panel"))


if __name__ == "__main__":
    gancho()
    calculado()
    voltaje()
    seguridad()
    cansada()
    frio()
    print("ok:", sorted(p.name for p in OUT.glob("*.svg")))

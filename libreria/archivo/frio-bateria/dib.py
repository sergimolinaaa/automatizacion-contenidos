"""lote10-01-frio-bateria: dibujos de «¿Por qué el frío se come la batería del móvil?».
Uso: python3 libreria/archivo/frio-bateria/dib.py

Método rossark: cada parte es su propio grupo con pivote (cabeza en el cuello, brazo en el hombro, aguja en su eje,
batería en los pies), cada copo e ion con su fase, y los números cuentan hacia arriba con capas que se relevan.
Piezas nuevas en libreria/svg/objetos/tecnologia.py: iones_bateria, caja_pesada, bateria_esfuerzo.
"""
import math
import random
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from libreria.svg.base import *  # noqa
from libreria.svg.personajes import persona
from libreria.svg.objetos import casa as K, escenarios as E, cuerpo as C, memoria as M, tecnologia as TE, vuelo as V
from libreria.svg.objetos import tienda as TI
from libreria.svg.objetos.mente import pivote

OUT = ROOT / "content" / "lote10-01-frio-bateria"
OUT.mkdir(parents=True, exist_ok=True)
FRIO = "#5BC0FF"
BLANCO_TXT = f'stroke="{INK}" stroke-width="7" paint-order="stroke"'


def rotulo(id_, x, y, text, size=34, col="#FFFFFF", anchor="middle"):
    return g(id_, T(x, y, text, size, col, anchor=anchor, font=DISP, extra=BLANCO_TXT))


def cuenta(prefijo, cx, cy, valores, w, h=110, size=None):
    """Contador que «cuenta»: una capa por valor (prefijo_0, prefijo_1… y la última = prefijo)."""
    o = ""
    for i, v in enumerate(valores):
        o += contador(prefijo if i == len(valores) - 1 else f"{prefijo}_{i}", cx, cy, v, w=w, h=h, size=size)
    return o


def termo_baja(id_, cx, top, h, nivel0, nivel1, col=FRIO):
    """Termómetro cuya columna «baja»: tapa blanca {id}_baja que crece desde arriba (grow origin top) de nivel0 a nivel1."""
    t = C.termometro(id_, cx, top, h, nivel0, col=col, marcas=8)
    w = h * 0.13
    bot = top + h
    y0 = bot - h * 0.88 * nivel0 - 2
    y1 = bot - h * 0.88 * nivel1
    tapa = f'<rect x="{f(cx-w*0.24)}" y="{f(y0)}" width="{f(w*0.48)}" height="{f(y1-y0)}" fill="#FFFFFF"/>'
    return t + g(f"{id_}_baja", tapa), y1


def esfera(id_, cx, cy, r, nivel=0.85):
    """Medidor semicircular con la aguja en {id}_aguja girando sobre su eje (origin center gracias a un pivote invisible)."""
    s = f'<path d="M {f(cx-r)} {f(cy)} A {f(r)} {f(r)} 0 0 1 {f(cx+r)} {f(cy)} Z" fill="#FFFFFF" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
    cols = (CORAL, AMARILLO, LIME)
    for i, c in enumerate(cols):
        a0, a1 = math.pi + i * math.pi / 3, math.pi + (i + 1) * math.pi / 3
        ri = r * 0.78
        s += (f'<path d="M {f(cx+ri*math.cos(a0))} {f(cy+ri*math.sin(a0))} A {f(ri)} {f(ri)} 0 0 1 {f(cx+ri*math.cos(a1))} {f(cy+ri*math.sin(a1))}" '
              f'fill="none" stroke="{c}" stroke-width="{f(r*0.18)}"/>')
    a = math.pi + nivel * math.pi
    tip = (cx + r * 0.7 * math.cos(a), cy + r * 0.7 * math.sin(a))
    ag = pivote(cx, cy, r * 0.75) + trazo(f"M {f(cx)} {f(cy)} L {f(tip[0])} {f(tip[1])}", r * 0.07, INK, 5)
    s += g(f"{id_}_aguja", ag) + f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r*0.1)}" fill="{INK}"/>'
    s += T(cx - r * 0.62, cy + 36, "−", 34, CORAL, font=DISP) + T(cx + r * 0.62, cy + 36, "+", 34, "#2E9E45", font=DISP)
    return g(id_, s)


# ---------------------------------------------------------------- 0. gancho: se apaga con batería (full)
def gancho():
    body = ""
    # suelo nevado
    body += (f'<path d="M 0 1290 Q 270 1250 540 1272 Q 820 1294 1080 1262 L 1080 1920 L 0 1920 Z" fill="{degradado("#F4F8FF", 0.12)}" '
             f'stroke="{INK}" stroke-width="7"/>')
    body += brillo("M 60 1290 Q 270 1262 520 1280", 6, 0.8)
    x0, y0 = 380, 1300
    kw = dict(edad="joven", piel="clara", pelo="corto", pelo_color="castano", ropa="abrigo", ropa_color="#2F6FD9",
              pantalon_color="#2A3045", accesorios=("gorro", "bufanda"), bufanda_color=CORAL, brazos=("relajado", "sujeta"), mira=1)
    pf = persona("chf", x0, y0, 1.22, expresion="frio", **kw)
    ps = persona("chs", x0, y0, 1.22, expresion="sorpresa", **kw)
    mx, my = pf.puntos["mano_der"]
    # móvil en la mano con la batería al 40 % (detrás del puño: lo sujeta)
    w = 150
    cx, cy = mx + 12, my - 105
    sx0, sy0, sx1, sy1 = TE.pantalla_movil(cx, cy, w)
    pant = (f'<rect x="{f(sx0)}" y="{f(sy0)}" width="{f(sx1-sx0)}" height="{f(sy1-sy0)}" fill="{degradado("#2347FF", 0.3)}"/>'
            + TE.bateria(None, cx, cy - 20, 70, 130, nivel=0.4, rayo=False)
            + T(cx, cy + 92, "40 %", 34, "#FFFFFF", font=DISP)
            + g("tel_negro", f'<rect x="{f(sx0-4)}" y="{f(sy0-4)}" width="{f(sx1-sx0+8)}" height="{f(sy1-sy0+8)}" fill="#05060A"/>'))
    body += g("tel", K.movil(None, cx, cy, w, pantalla=pant))
    body += g("chico", pf + ps)
    # vaho, temblor y el ¡PLOF!
    bx, by = pf.puntos["boca"]
    body += g("vaho", vaho(bx + 70, by - 10))
    body += g("temb", temblor(x0 - 230, 860, 100, FRIO) + temblor(x0 + 200, 1000, 90, FRIO))
    body += onomatopeya("plof", cx + 165, cy - 10, "¡PLOF!", r=100, size=44, rot_=8)
    body += icono_duda("duda", cx + 200, cy + 190, 46)
    # nieve: cada copo en su grupo (fase propia)
    rnd = random.Random(7)
    for i in range(14):
        x = 60 + (i * 71) % 980 + rnd.uniform(-20, 20)
        y = 470 + rnd.uniform(0, 760)
        body += g(f"cp{i}", copo(x, y, rnd.uniform(14, 26), rnd.uniform(0, 60), col="#FFFFFF" if i % 3 else "#CFE8FF"))
    guardar(f"{OUT}/gancho_full.svg", svg(body, "full", fondo=E.cielo(hora="dia", colinas=True, nubes=True, sol_=False)))


# ---------------------------------------------------------------- 1. dentro de la batería (full, fondo oscuro)
def iones():
    fondo = (f'<rect width="1080" height="1920" fill="{degradado("#1B2140", 0.35)}"/>'
             + "".join(f'<path d="M {x} 0 L {x} 1920" stroke="#2C3560" stroke-width="2"/>' for x in range(0, 1081, 60))
             + "".join(f'<path d="M 0 {y} L 1080 {y}" stroke="#2C3560" stroke-width="2"/>' for y in range(0, 1921, 60))
             + f'<circle cx="540" cy="860" r="560" fill="#2347FF" opacity="0.18"/>')
    X0, Y0, W, H = 70, 620, 940, 500
    ib = TE.iones_bateria("ib", X0, Y0, W, H, n=7, liquido="fluido", seed=5, size=34)
    ax, ay = ib.puntos["anodo"]
    kx, ky = ib.puntos["catodo"]
    # circuito con bombilla arriba
    cable = (trazo(f"M {f(ax)} {f(Y0+10)} L {f(ax)} {f(520)} L 470 520", 12, "#C9D0DC", 6)
             + trazo(f"M {f(kx)} {f(Y0+10)} L {f(kx)} {f(520)} L 610 520", 12, "#C9D0DC", 6))
    body = g("cable", cable)
    body += K.bombilla("bomb_off", 540, 520, 78, encendida=False) + K.bombilla("bomb_on", 540, 520, 78, encendida=True)
    body += ib
    l0, ly0, l1, ly1 = ib.puntos["liquido"]
    body += flecha("fviaje", (l0 + 30, ly0 + 40), (l1 - 30, ly0 + 40), col=LIME, w=12, punta=30, curva=-0.12)
    body += etiqueta("tliq", (l0 + l1) / 2, ly1 - 36, "LÍQUIDO", bg="#FFFFFF", fg=INK, size=28)
    body += etiqueta("tiones", 540, 1250, "IONES: PARTÍCULAS CON CARGA", bg=LIME, fg=INK, size=34)
    guardar(f"{OUT}/iones_full.svg", svg(body, "full", fondo=fondo))
    return ib


# ---------------------------------------------------------------- 2. líquido espeso: aceite en la nevera (panel)
def nevera_aceite(x0, top, w, h):
    """Nevera de casa pequeña, abierta, con una balda y una botella de aceite (fluida y turbia en el mismo sitio)."""
    o = sombra_caja(x0, top, w, h, rx=26, dx=12, dy=14, op=0.25)
    o += f'<rect x="{f(x0)}" y="{f(top)}" width="{f(w)}" height="{f(h)}" rx="26" fill="{degradado("#F4F7FC", 0.12, "h")}" stroke="{INK}" stroke-width="8"/>'
    ix0, iy0, iw, ih = x0 + 22, top + 22, w - 44, h - 44
    o += f'<rect x="{f(ix0)}" y="{f(iy0)}" width="{f(iw)}" height="{f(ih)}" rx="14" fill="{degradado("#D7EEFF", 0.18)}" stroke="{INK}" stroke-width="5"/>'
    o += g("nev_luz", f'<ellipse cx="{f(x0+w/2)}" cy="{f(iy0+30)}" rx="{f(iw*0.32)}" ry="18" fill="#FFFFFF" opacity="0.8"/>')
    balda = iy0 + ih * 0.78
    o += f'<path d="M {f(ix0+6)} {f(balda)} L {f(ix0+iw-6)} {f(balda)}" stroke="#9AA6BC" stroke-width="10" stroke-linecap="round"/>'
    return o, balda


def aceite():
    body = ""
    ib = TE.iones_bateria("ic", 40, 165, 500, 360, n=5, liquido="ambos", seed=11, rotulos=False)
    body += g("bat2", ib)
    tb, y1 = termo_baja("ter", 615, 175, 330, 0.8, 0.22)
    body += g("terG", tb)
    body += g("copoT", copo(675, 175 + 330 * 0.88 * 0.25 + 40, 26, 10, col=FRIO))
    body += etiqueta("tesp", 290, 115, "SE ESPESA", bg=INK, fg=LIME, size=30)
    body += etiqueta("tlento", 290, 590, "IONES MÁS LENTOS", bg=LIME, fg=INK, size=30)
    nev, balda = nevera_aceite(700, 120, 260, 470)
    bot = K.botella("acf", 830, balda - 6, 300, col="#F2C230", etiqueta_col="#2E9E45", texto="ACEITE")
    btu = K.botella("act", 830, balda - 6, 300, col="#E8DDB0", etiqueta_col="#2E9E45", texto="ACEITE")
    gota_ = g("gota", gota(830 - 300 * 0.3 / 2 - 2, balda - 300 * 0.55, 13, col="#F2C230"))
    escarcha = "".join(copo(x, y, 14, 0, col="#9FD3FF") for x, y in ((740, 190), (920, 230), (760, 330)))
    body += g("neveraG", nev + g("nev_frio", escarcha) + bot + btu + gota_)
    body += etiqueta("tnev", 830, 625, "ACEITE EN LA NEVERA", bg="#FFFFFF", fg=INK, size=24)
    guardar(f"{OUT}/aceite.svg", svg(body, "panel"))
    return ib


# ---------------------------------------------------------------- 3. más resistencia (panel)
def resistencia():
    body = f'<path d="M 40 560 L 960 560" stroke="{INK}" stroke-width="8" stroke-linecap="round" opacity="0.3"/>'
    be = TE.bateria_esfuerzo("be", 270, 560, 0.92, nivel=0.35, inclina=11)
    mx, my = be.puntos["manos"]
    cj = TE.caja_pesada("caja", mx - 2, 560, 270, 220, "ENERGÍA")
    body += g("cajaG", cj + V.pesa("pesa", mx + 133, 340, 130, "KG"))
    body += be
    sx, sy = be.puntos["sudor"]
    body += M.gota_esfuerzo("sudor", sx, sy, 1.3) + M.gota_esfuerzo("sudor2", sx + 30, sy - 50, 0.9)
    body += esfera("med", 870, 170, 95, nivel=0.85)
    body += etiqueta("tmed", 870, 222, "ENERGÍA", bg="#FFFFFF", fg=INK, size=22)
    body += etiqueta("tres", 440, 118, "RESISTENCIA INTERNA", bg=INK, fg=LIME, size=32)
    body += etiqueta("tsub", 500, 615, "LO QUE LE CUESTA DAR ENERGÍA", bg="#FFFFFF", fg=INK, size=26)
    guardar(f"{OUT}/resistencia.svg", svg(body, "panel"))


# ---------------------------------------------------------------- 4. a la mitad (free)
def mitad():
    Hh = 860
    body = ""
    tb, y1 = termo_baja("tg", 160, 80, 560, 0.78, 0.12)
    body += g("tgG", tb)
    body += rotulo("t20", 200, 815, "20 BAJO CERO", 32)
    body += g("copoG", copo(160, 50, 30, 0, col="#FFFFFF"))
    xs = (520, 820)
    xs = (560, 840)
    b1 = TE.bateria("bn", xs[0], 410, 180, 340, nivel=1.0, col=VERDE, rayo=True)
    b2 = TE.bateria("bf", xs[1], 410, 180, 340, nivel=0.5, col=AMARILLO, rayo=True)
    body += g("bnG", b1 + rotulo(None, xs[0], 650, "TEMPERATURA", 28) + rotulo(None, xs[0], 688, "NORMAL", 28))
    body += g("bfG", b2 + rotulo(None, xs[1], 650, "A 20", 28) + rotulo(None, xs[1], 688, "BAJO CERO", 28)
              + g("bf_hielo", copo(xs[1] + 92, 262, 24, 15, col="#FFFFFF") + copo(xs[1] - 96, 560, 18, 0, col="#CFE8FF")))
    # línea de la mitad
    ym = 410
    body += g("lmitad", f'<path d="M {xs[1]-130} {ym} L {xs[1]+130} {ym}" stroke="{CORAL}" stroke-width="9" stroke-dasharray="22 14" stroke-linecap="round"/>')
    body += cuenta("c50", 700, 790, [f"{v} %" for v in (10, 20, 30, 40, 50)], w=250, h=92, size=50)
    body += rotulo("taprox", 890, 802, "APROX.", 26)
    guardar(f"{OUT}/mitad_free.svg", svg(body, "free", h=Hh))


# ---------------------------------------------------------------- 5. Apple: entre 0 y 35 grados (panel)
def apple():
    body = TE.logo_apple("apple", 370, 178, 125)
    body += etiqueta("trec", 630, 175, "RECOMIENDA", bg=INK, fg=LIME, size=36)
    x0, x1, yr = 300, 920, 480
    rn = TI.recta_numerica("recta", x0, x1, yr, -10, 45, 5, etiquetas={0: "0", 35: "35", 45: "45"}, size=26)
    X = rn.puntos["x"]
    body += rn + g("tmenos10", T(X(-10), yr + 100, "10 BAJO CERO", 26, "#FFFFFF", font=DISP, extra=f'stroke="{INK}" stroke-width="5" paint-order="stroke"'))
    body += g("franja", f'<path d="M {f(X(0))} {yr} L {f(X(35))} {yr}" stroke="{INK}" stroke-width="40" stroke-linecap="round"/>'
              f'<path d="M {f(X(0))} {yr} L {f(X(35))} {yr}" stroke="{LIME}" stroke-width="28" stroke-linecap="round"/>')
    for k, v in enumerate((0, 35)):
        x = X(v)
        body += g(f"pin{k}", f'<path d="M {f(x)} {yr-34} L {f(x-18)} {yr-70} L {f(x+18)} {yr-70} Z" fill="{CORAL}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
    xm = (X(0) + X(35)) / 2
    sx0, sy0, sx1, sy1 = TE.pantalla_movil(xm, 330, 100)
    pant = f'<rect x="{f(sx0)}" y="{f(sy0)}" width="{f(sx1-sx0)}" height="{f(sy1-sy0)}" fill="{degradado("#2347FF", 0.3)}"/>' + TE.bateria(None, xm, 330, 44, 82, 0.9, rayo=False)
    body += g("iph", K.movil(None, xm, 330, 100, pantalla=pant))
    body += g("frio", copo(X(-5), 360, 48, 0, col=FRIO))
    body += g("calor", ondas_calor(X(40.5) - 24, 420, 130) + ondas_calor(X(40.5) + 24, 405, 105))
    body += etiqueta("trango", xm + 40, 615, "DE 0 A 35 °C", bg=LIME, fg=INK, size=40)
    guardar(f"{OUT}/apple.svg", svg(body, "panel"))


if __name__ == "__main__":
    gancho()
    ib1 = iones()
    ib2 = aceite()
    resistencia()
    mitad()
    apple()
    import json
    print(json.dumps({"ib1": [ib1.puntos["liquido"], ib1.puntos["iones"], ib1.puntos["r"]],
                      "ib2": [ib2.puntos["liquido"], ib2.puntos["iones"], ib2.puntos["r"]]}))

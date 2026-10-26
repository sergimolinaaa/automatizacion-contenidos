"""lote9-06-miedo-oscuridad: dibujos de «¿Por qué te da miedo la oscuridad?».
Uso: python3 libreria/archivo/miedo-oscuridad/dib.py

Método rossark: cada parte es su propio grupo con pivote (cabeza en el cuello, brazos en el hombro, copa de la acacia en
el tronco, llamas en su base, cola de la leona en la grupa), cada repetido con su fase, barras que crecen desde la base
escalonadas y números que cuentan con capas que se relevan.
"""
import math
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from libreria.svg.base import *  # noqa
from libreria.svg.personajes import persona
from libreria.svg.objetos import casa as K, escenarios as E, cuerpo as C, memoria as M, tiempo as TM
from libreria.svg.objetos import territorio as TR, noche as N

OUT = ROOT / "content" / "lote9-06-miedo-oscuridad"
OUT.mkdir(parents=True, exist_ok=True)
PIJAMA = "#FF7EB6"


def cuenta(prefijo, cx, cy, valores, w, h=110, size=None, etiqueta_txt=None):
    """Contador que «cuenta»: una capa por valor (prefijo_0, prefijo_1… y la última = prefijo)."""
    o = ""
    for i, v in enumerate(valores):
        o += contador(prefijo if i == len(valores) - 1 else f"{prefijo}_{i}", cx, cy, v, w=w, h=h, size=size)
    if etiqueta_txt:
        o += etiqueta(f"{prefijo}_et", cx, cy + h / 2 + 36, etiqueta_txt, bg=INK, fg=LIME, size=26)
    return o


def lunares(cx, cy, w, h, n=7, seed=2):
    import random
    r = random.Random(seed)
    return "".join(f'<circle cx="{f(cx + r.uniform(-w/2, w/2))}" cy="{f(cy + r.uniform(-h/2, h/2))}" r="{f(r.uniform(7, 10))}" fill="#FFFFFF" opacity="0.9"/>' for _ in range(n))


# ---------------------------------------------------------------- 0. gancho: apagas la luz (full)
def gancho():
    body = ""
    sw = N.interruptor("sw", 950, 740, 0.9)
    body += sw
    body += N.mano_indice("mano", 950, 786, 0.8, manga="#6C7A99")
    body += N.perchero("perch", 250, 1320, 600)
    body += g("velo", '<rect x="-20" y="-20" width="1120" height="1960" fill="#070B24" opacity="0.62"/>')
    body += N.sombra_monstruo("monstruo", 420, 470, 760)
    body += ondas_sonido("ondas", 330, 1060, 50, 3, -60, 30, 30, 9, LIME)
    body += onomatopeya("cric", 190, 600, "¡CRIC!", r=88, size=40, rot_=-10)
    detras, delante = TM.cama("cama", 720, 1330, 620, col="#7B5CFF", alto_cabecero=400)
    px, py = detras.puntos["persona"]
    kw = dict(edad="nino", piel="clara", pelo="coleta", pelo_color="castano", ropa="camiseta", ropa_color=PIJAMA,
              pose="busto", brazos=("relajado", "relajado"))
    ninaN = persona("ninaN", px, py, 1.55, expresion="neutral", mira=-1, **kw)
    ninaS = persona("ninaS", px, py, 1.55, expresion="sorpresa", mira=-1, **kw)
    hx, hy = ninaN.puntos["cabeza"]
    body += g("camaG", detras + g("nina", ninaN + ninaS + g("lun", lunares(px, py - 40, 180, 60))) + delante)
    body += g("temb", temblor(px - 210, hy - 20, 90, LIME) + temblor(px + 190, hy - 30, 90, LIME))
    guardar(f"{OUT}/gancho_full.svg", svg(body, "full", fondo=E.habitacion(noche=True, cuadro=False)))
    return ninaN


# ---------------------------------------------------------------- 1. vivimos de la vista (free)
def vista():
    H = 860
    body = N.ojo("ojo", 500, 270, 560)
    body += g("velo", f'<ellipse cx="500" cy="260" rx="330" ry="190" fill="#070B24" opacity="0.92" stroke="{INK}" stroke-width="7"/>')
    body += icono_duda("duda", 500, 260, 70, col=LIME, fondo=INK)
    xs = (110, 290, 470, 650, 830)
    hs = (300, 110, 80, 60, 95)
    tipos = ("ojo", "oreja", "nariz", "lengua", "mano")
    for i, (x, h_, t) in enumerate(zip(xs, hs, tipos)):
        body += barra(f"b{i}", x, 740, 120, h_, col=LIME if i == 0 else "#C9CED8")
        body += N.icono_sentido(f"i{i}", x + 60, 800, 46, t)
    body += aspa("x", 170, 800, 40)
    guardar(f"{OUT}/vista_free.svg", svg(body, "free", h=H))


# ---------------------------------------------------------------- 2. la noche era peligrosa (full)
def sabana():
    body = N.acacia("acacia", 840, 1180, 560)
    body += N.hoguera("fuego", 285, 1250, 190)
    padre = persona("padre", 110, 1260, 1.0, "adulto", "morena", "largo", "negro", "camiseta", "#8B5A2B", "#5A3A1E",
                    accesorios=("barba",), expresion="neutral", brazos=("relajado", "explica"), mira=1)
    nino = persona("nino", 425, 1262, 1.05, "nino", "morena", "rizado", "negro", "camiseta", "#A8743E", "#5A3A1E",
                   expresion="neutral", brazos=("explica", "relajado"), mira=-1)
    madre = persona("madre", 545, 1258, 0.95, "adulto", "morena", "largo", "castano", "vestido", "#9C6A3A", "#5A3A1E",
                    expresion="neutral", brazos=("relajado", "relajado"), mira=-1)
    body += g("padreG", padre) + g("madreG", madre) + g("ninoG", nino)
    body += N.leona("leona", 850, 1215, 0.72)
    body += N.matas("hierba", 620, 1090, 1234, 70, 13, seed=5)
    ox, oy = 850 + (-242) * 0.72, 1215 + (-134) * 0.72
    # los ojos de la leona brillan en la hierba antes de que se vea su silueta
    oj = ""
    for ex, ey, rr in ((-258, -132, 1.0), (-226, -137, 0.9)):
        x_, y_ = 850 + ex * 0.72, 1215 + ey * 0.72
        oj += f'<circle cx="{f(x_)}" cy="{f(y_)}" r="{f(34*0.72*rr)}" fill="url(#ojoFiera)"/>'
        oj += f'<path d="M {f(x_-11*rr)} {f(y_)} Q {f(x_)} {f(y_-9*rr)} {f(x_+11*rr)} {f(y_)} Q {f(x_)} {f(y_+7*rr)} {f(x_-11*rr)} {f(y_)} Z" fill="#FFE14A" stroke="{INK}" stroke-width="3"/>'
    body += g("ojosh", oj)
    body += icono_alerta("alerta", 900, 960, 46)
    body += etiqueta("tdep", 830, 520, "DEPREDADORES", bg=CORAL, fg="#FFFFFF", size=40)
    body += etiqueta("tant", 300, 560, "ANTEPASADOS", bg=LIME, fg=INK, size=40)
    guardar(f"{OUT}/sabana_full.svg", svg(body, "full", fondo=N.sabana_noche(suelo_y=1180)))
    return (ox, oy)


# ---------------------------------------------------------------- 3. Tanzania y la luna (free)
def tanzania():
    H = 880
    mapa = N.mapa_africa("mapa", 225, 250, 360)
    body = mapa
    tx, ty = mapa.puntos["tanzania"]
    body += etiqueta("ttz", 470, 330, "TANZANIA", apunta=(tx - 6, ty + 10), bg=CORAL, fg="#FFFFFF", size=34)
    body += cuenta("cnt", 720, 105, ["0", "100", "200", "300", "400", "500"], w=250, h=104, size=58)
    body += etiqueta("tat", 720, 190, "ATAQUES DE LEONES", bg=INK, fg=LIME, size=26)
    body += N.cabeza_leon("leon", 900, 100, 46)
    # cielo negro sin luna y reloj a las nueve
    estrellas = "".join(f'<circle cx="{f(720 + 100*math.cos(a))}" cy="{f(335 + 80*math.sin(a*1.7))}" r="3" fill="#FFFFFF"/>' for a in (0.4, 1.3, 2.2, 3.4, 4.6, 5.5))
    body += g("cielo", f'<circle cx="720" cy="335" r="118" fill="#070B24" stroke="{INK}" stroke-width="7"/>' + estrellas)
    body += K.reloj("rel", 720, 335, 70, 9, 0, col_marco="#7B5CFF")
    fases = (0.28, 0.4, 0.5, 0.62, 0.75)
    hs = (60, 70, 80, 175, 190)
    xs = (120, 300, 480, 660, 840)
    for i, (x, fz, h_) in enumerate(zip(xs, fases, hs)):
        body += N.fase_luna(f"luna{i}", x, 520, 44, fz)
        body += barra(f"bar{i}", x - 50, 830, 100, h_, col=CORAL if i >= 3 else "#C9CED8")
    body += etiqueta("tllena", 480, 460, "LUNA LLENA", bg=LIME, fg=INK, size=26)
    body += etiqueta("tdesp", 750, 604, "DE 2 A 4 VECES MÁS", bg=CORAL, fg="#FFFFFF", size=26)
    guardar(f"{OUT}/tanzania_free.svg", svg(body, "free", h=H))


# ---------------------------------------------------------------- 4. el cerebro rellena (free)
def rellena():
    H = 860
    s = 0.8
    x, y = 290, 560
    cab = C.cabeza_perfil("cab", x, y, s, "media", con_cerebro=False)
    body = g("cabG", cab)

    def P(px, py):
        return (x + (px - 462) * s, y + (py - 720) * s)
    cx, cy = P(400, 250)
    nube_pts = []
    for i in range(14):
        a = 2 * math.pi * i / 14
        rr = 1.0 if i % 2 == 0 else 0.84
        nube_pts.append((cx + 165 * rr * math.cos(a), cy + 120 * rr * math.sin(a)))
    body += g("hueco", f'<path d="{smooth(nube_pts, True, 0.6)} Z" fill="#070B24" stroke="{INK}" stroke-width="7"/>')
    # amenazas que rellenan el hueco
    garras = "".join(trazo(f"M {f(cx-120+k*26)} {f(cy-60+k*6)} Q {f(cx-96+k*26)} {f(cy-10)} {f(cx-110+k*26)} {f(cy+50-k*4)}", 9, "#FFFFFF", 5) for k in range(3))
    body += g("garras", garras)
    for i, (ex, ey) in enumerate(((cx + 20, cy - 50), (cx + 100, cy + 10))):
        o = ""
        for dx in (-20, 20):
            o += f'<circle cx="{f(ex+dx)}" cy="{f(ey)}" r="24" fill="url(#ojoFiera)"/><ellipse cx="{f(ex+dx)}" cy="{f(ey)}" rx="13" ry="9" fill="#FFE14A" stroke="{INK}" stroke-width="3"/><path d="M {f(ex+dx)} {f(ey-6)} L {f(ex+dx)} {f(ey+6)}" stroke="{INK}" stroke-width="4"/>'
        body += g(f"ojos{i}", o)
    col = "".join(f'<path d="M {f(cx-10+k*36)} {f(cy+50)} L {f(cx+8+k*36)} {f(cy+94)} L {f(cx+26+k*36)} {f(cy+50)} Z" fill="#FFFFFF" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>' for k in range(3))
    body += g("colmillos", f'<path d="M {f(cx-20)} {f(cy+50)} L {f(cx+124)} {f(cy+50)}" stroke="#9C2E3A" stroke-width="10" stroke-linecap="round"/>' + col)
    body += etiqueta("thueco", 250, 520 + 120, "RELLENA LO QUE NO VE", bg=LIME, fg=INK, size=28)
    # balanza: susto de más (ligero) frente a león (pesado)
    izq = icono_alerta(None, 0, -58, 32)
    der = N.cabeza_leon(None, 0, -66, 46)
    body += TR.balanza("bal0", 735, 840, 380, 0, izq=izq, der=der, txt_izq="SUSTO", txt_der="LEÓN")
    body += TR.balanza("bal1", 735, 840, 380, 14, izq=izq, der=der, txt_izq="SUSTO", txt_der="LEÓN")
    body += etiqueta("tmejor", 735, 325, "MEJOR PASARSE", bg=CORAL, fg="#FFFFFF", size=32)
    guardar(f"{OUT}/rellena_free.svg", svg(body, "free", h=H))


# ---------------------------------------------------------------- 5. no es cosa de niños (free)
def adultos():
    H = 860
    body = N.bandera_canada("canada", 170, 110, 230, 115)
    body += etiqueta("tcan", 170, 225, "CANADÁ", bg=INK, fg=LIME, size=30)
    detras, delante = TM.cama("cama2", 360, 840, 560, col="#2EC4B6", alto_cabecero=380)
    px, py = detras.puntos["persona"]
    uni = persona("uni", px, py, 1.15, "joven", "media", "corto", "negro", "camiseta", "#3D6FD9",
                  pose="busto", expresion="duda", brazos=("relajado", "relajado"), mira=1)
    cx_, cy_ = uni.puntos["cima"]
    bir = M.birrete("birrete", cx_, cy_ + 38 * 1.0, 1.0)
    body += g("cama2G", detras + g("uniG", uni + bir) + delante)
    body += etiqueta("tuni", 360, 400, "UNIVERSITARIOS", bg=LIME, fg=INK, size=30)
    # anillo que se llena hasta casi la mitad
    cx, cy, r = 780, 470, 140
    body += f'<circle cx="{cx+8}" cy="{cy+10}" r="{r+38}" fill="{INK}" opacity="0.2"/>'
    body += f'<circle cx="{cx}" cy="{cy}" r="{r+36}" fill="#FFFFFF" stroke="{INK}" stroke-width="7"/>'
    body += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#DDE3EE" stroke-width="56"/>'
    body += f'<circle cx="{cx}" cy="{cy}" r="{r-36}" fill="#F4F6FA" stroke="{INK}" stroke-width="6"/>'
    a1 = -math.pi / 2 + 2 * math.pi * 0.46
    d = f"M {f(cx)} {f(cy-r)} A {r} {r} 0 0 1 {f(cx + r*math.cos(a1))} {f(cy + r*math.sin(a1))}"
    body += g("arco", f'<path d="{d}" fill="none" stroke="{CORAL}" stroke-width="56" stroke-linecap="butt"/>')
    body += g("luna_c", TM.luna(None, cx, cy, 52))
    body += etiqueta("tmitad", cx, 700, "CASI LA MITAD", bg=CORAL, fg="#FFFFFF", size=36)
    body += etiqueta("tmal", cx, 770, "DE LOS QUE DORMÍAN MAL", bg=INK, fg=LIME, size=24)
    body += etiqueta("tpiloto", 560, 105, "ESTUDIO PILOTO", bg="#FFFFFF", fg=INK, size=28)
    guardar(f"{OUT}/adultos_free.svg", svg(body, "free", h=H))
    return uni


# ---------------------------------------------------------------- 6. feliz Halloween (free)
def halloween():
    H = 640
    body = TM.luna("luna", 880, 90, 56)
    body += N.calabaza("cala", 240, 600, 250)
    # sombra del fantasma en la pared (crece) y el fantasma
    body += g("sombra", f'<g transform="translate(700 600) scale(1.25 1.45)" opacity="0.55">'
              f'<path d="M -105 -22 C -118 -180 -92 -300 0 -300 C 92 -300 118 -180 105 -22 L 70 -36 L 35 -22 L 0 -36 L -35 -22 L -70 -36 Z" fill="#0C1030"/></g>')
    body += N.fantasma("fanN", 560, 600, 300)
    body += N.fantasma("fanS", 560, 600, 300, susto=True)
    body += icono_alerta("alerta", 440, 210, 40)
    body += etiqueta("tinst", 560, 50, "ES INSTINTO", bg=LIME, fg=INK, size=36)
    guardar(f"{OUT}/halloween_free.svg", svg(body, "free", h=H))


if __name__ == "__main__":
    gancho()
    vista()
    print("leona ojos", sabana())
    tanzania()
    rellena()
    adultos()
    halloween()

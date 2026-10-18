"""SVG de content/lote8-01-movil-lento (¿Por qué tu móvil va más lento con los años?). Uso: python3 libreria/archivo/movil-lento/dib.py"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from libreria.svg.base import *  # noqa
from libreria.svg.personajes import persona
from libreria.svg.objetos import casa as K, escenarios as E, politica as P, tienda as TI, tecnologia as TC

OUT = ROOT / "content" / "lote8-01-movil-lento"
FR = ("#0055A4", "#FFFFFF", "#EF4135")


def tarjeta_icono(id_, cx, cy, txt, dibujo):
    return g(id_, tarjeta(None, cx, cy, 300, 150, acento=LIME, rot_=0) + dibujo + T(cx + 40, cy + 12, txt, 28, INK, font=DISP))


# ---------------------------------------------------------------- 0. gancho (full)
def gancho():
    kw = dict(edad="joven", piel="media", pelo="coleta", pelo_color="castano", ropa="jersey", ropa_color=VIO,
              brazos=("relajado", "coge"))
    a = persona("ana_n", 300, 1400, 1.3, expresion="neutral", **kw)
    b = persona("ana_e", 300, 1400, 1.3, expresion="enfado", **kw)
    mx, my = a.puntos["mano_der"]
    pw = 190
    pcx, pcy = mx + 95, my - 120
    x0, y0, x1, y1 = TC.pantalla_movil(pcx, pcy, pw)
    tel = K.movil("tel", pcx, pcy, pw, pantalla=TC.pantalla_cargando("tel", x0, y0, x1, y1, CORAL, "play"))
    body = a + b + tel
    body += medidor("vel", 820, 640, 140, 0.5)
    body += g("lvel", T(820, 700, "VELOCIDAD", 30, INK, font=DISP))
    body += globo("globo", 300, 520, "¡VENGA YA!", cola=a.puntos["boca"], size=44, tipo="grito")
    body += onda_expansiva("onda", pcx, pcy, 150, CORAL)
    body += tarjeta_icono("c1", 820, 860, "BATERÍA", TC.bateria(None, 720, 860, 50, 90, 0.4, rayo=False))
    body += tarjeta_icono("c2", 820, 1030, "APPS", TC.icono_app(None, 720, 1030, 80, CORAL, "play"))
    body += tarjeta_icono("c3", 820, 1200, "MEMORIA", TC.barra_almacenamiento(None, 680, 1188, 80, 26, 0.95))
    return svg(body, "full", fondo=E.habitacion())


# ---------------------------------------------------------------- 1. la batería envejece (panel)
def bateria():
    body = ""
    body += TC.bateria("nueva", 190, 360, 150, 280, 1.0)
    body += etiqueta("lnueva", 230, 110, "NUEVA", size=32, bg=LIME, fg=INK)
    body += barra("pico_n", 300, 560, 80, 330, VERDE, None, None)
    body += g("lpico_n", T(340, 610, "PICO", 26, INK))
    body += TC.bateria("vieja", 640, 370, 150, 280, 0.55, gastada=True)
    body += etiqueta("lvieja", 680, 110, "CON AÑOS", size=32, bg=CORAL, fg="#FFFFFF")
    body += barra("pico_v", 760, 560, 80, 120, CORAL, None, None)
    body += g("lpico_v", T(800, 610, "PICO", 26, INK))
    body += etiqueta("llitio", 470, 620, "LITIO", size=30)
    body += g("rayo_n", rayos(None, 340, 215, 30, 70, 7, YEL, 9, 200, 340))
    return svg(body, "panel", fondo=fondo_suave())


# ---------------------------------------------------------------- 2. frena para no apagarse (free)
def freno():
    pcx, pcy, pw = 250, 430, 260
    x0, y0, x1, y1 = TC.pantalla_movil(pcx, pcy, pw)
    body = K.movil("tel", pcx, pcy, pw, pantalla=TC.pantalla_cargando("tel", x0, y0, x1, y1, VIO, "juego"))
    negro = (f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(x1-x0)}" height="{f(y1-y0)}" rx="22" fill="#05060A"/>'
             + f'<path d="M {f(pcx-38)} {f(pcy-30)} A 54 54 0 1 0 {f(pcx+38)} {f(pcy-30)}" fill="none" stroke="#5A6170" stroke-width="12" stroke-linecap="round"/>'
             + f'<path d="M {f(pcx)} {f(pcy-70)} L {f(pcx)} {f(pcy-10)}" stroke="#5A6170" stroke-width="12" stroke-linecap="round"/>')
    body += g("negro", negro)
    body += TC.bateria("bat", 800, 250, 130, 240, 0.4, gastada=True)
    body += flecha_gorda("pide", (410, 300), (700, 260), ancho=54, col=LIME)
    body += g("lpide", T(560, 220, "PIDE MUCHO", 34, "#FFFFFF", font=DISP, extra=f'stroke="{INK}" stroke-width="7" paint-order="stroke"'))
    body += onomatopeya("zas", 560, 120, "¡YA!", r=70, size=34, rot_=-8)
    body += TC.chip("cpu", 560, 700, 150, "CPU")
    body += medidor("vel", 840, 760, 120, 0.5)
    body += sello("freno", 840, 560, "FRENO", size=44, rot_=-8)
    body += etiqueta("lsis", 250, 850, "EL SISTEMA", size=32)
    return svg(body, "free", h=900)


# ---------------------------------------------------------------- 3. Apple y la multa (panel)
def multa():
    body = ""
    body += TC.logo_apple("apple", 190, 300, 210)
    body += P.calendario("cal", 420, 250, 180, 190, "AÑO", "2017")
    body += sello("avisar", 300, 560, "SIN AVISAR", size=48, rot_=-7)
    body += bandera("fr", 720, 170, 170, 110, FR)
    bill = "".join(TI.billete(None, 760 + dx, 390 + dy, 260, "50", rot_=r) for dx, dy, r in ((-20, 20, -8), (10, 0, 4), (0, -18, -2)))
    body += g("billetes", bill)
    body += contador("c25", 760, 560, "25 M€", None, w=330, h=110)
    return svg(body, "panel", fondo=fondo_suave())


# ---------------------------------------------------------------- 4. apps que engordan (panel)
def apps():
    pcx, pcy, pw = 220, 360, 230
    x0, y0, x1, y1 = TC.pantalla_movil(pcx, pcy, pw)
    body = K.movil("tel", pcx, pcy, pw, pantalla=f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(x1-x0)}" height="{f(y1-y0)}" fill="#F2F4F8"/>')
    glifos = (("play", CORAL), ("chat", TEAL), ("foto", YEL), ("mapa", VERDE), ("nota", VIO), ("camara", "#FF7EB6"),
              ("juego", "#2347FF"), ("estrella", NARANJA), ("chat", VERDE))
    for k, (gl, c) in enumerate(glifos):
        cx = x0 + (x1 - x0) * (0.2 + 0.3 * (k % 3))
        cy = y0 + 70 + 95 * (k // 3)
        body += TC.icono_app(f"app{k}", cx, cy, 58, c, gl)
    body += barra("b13", 520, 560, 120, 36, LIME, "2013", "164 MB")
    body += barra("b17", 760, 560, 120, 400, CORAL, "2017", "1,8 GB")
    body += sello("x11", 580, 300, "×11", size=70, rot_=-10, col=CORAL)
    body += etiqueta("ltop", 640, 640, "LAS 10 APPS MÁS INSTALADAS", size=24)
    return svg(body, "panel", fondo=fondo_suave())


# ---------------------------------------------------------------- 5. memoria llena (full)
def memoria():
    pcx, pcy, pw = 300, 790, 330
    x0, y0, x1, y1 = TC.pantalla_movil(pcx, pcy, pw)
    body = K.movil("tel", pcx, pcy, pw, pantalla=TC.pantalla_almacenamiento("tel", x0, y0, x1, y1))
    arm = TC.armario("arm", 800, 1230, 380, 540)
    body += arm
    body += onomatopeya("plof", 900, 600, "¡PLOF!", r=95, size=40, rot_=10)
    arch = ""
    for k, c in enumerate((CORAL, TEAL, YEL)):
        arch += f'<rect x="{f(620 + k*110)}" y="480" width="80" height="100" rx="10" fill="{degradado(c, 0.25)}" stroke="{INK}" stroke-width="6"/>'
        arch += f'<path d="M {f(636 + k*110)} 510 L {f(684 + k*110)} 510 M {f(636 + k*110)} 535 L {f(684 + k*110)} 535" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
    body += g("archivos", arch)
    body += etiqueta("lhueco", 760, 1300, "SIN HUECO NO ORDENA", size=30, bg=CORAL, fg="#FFFFFF")
    return svg(body, "full", fondo=E.habitacion())


# ---------------------------------------------------------------- 6. qué hacer (panel)
def consejo():
    pcx, pcy, pw = 250, 360, 230
    x0, y0, x1, y1 = TC.pantalla_movil(pcx, pcy, pw)
    body = K.movil("tel", pcx, pcy, pw, pantalla=TC.pantalla_salud("tel", x0, y0, x1, y1, "78 %"))
    body += etiqueta("lsalud", 250, 630, "AJUSTES · BATERÍA", size=26)
    body += icono_ok("ok1", 400, 160, 42)
    p = TC.papelera("pap", 720, 590, 170)
    body += p
    arch = ""
    for k, (c, dx) in enumerate(((CORAL, -70), (TEAL, 0), (YEL, 70))):
        arch += f'<rect x="{f(690 + dx)}" y="{f(150 + 20*(k%2))}" width="64" height="80" rx="8" fill="{degradado(c, 0.25)}" stroke="{INK}" stroke-width="5"/>'
    body += g("archivos", arch)
    body += etiqueta("lespacio", 720, 640, "LIBERA ESPACIO", size=26, bg=LIME, fg=INK)
    body += icono_ok("ok2", 860, 330, 42)
    return svg(body, "panel", fondo=fondo_suave())


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in (("gancho_full.svg", gancho), ("bateria.svg", bateria), ("freno_free.svg", freno),
                     ("multa.svg", multa), ("apps.svg", apps), ("memoria_full.svg", memoria), ("consejo.svg", consejo)):
        guardar(str(OUT / name), fn())

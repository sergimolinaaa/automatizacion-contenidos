"""SVG de content/lote7-11-nudillos (¿Por qué te crujen los nudillos?). Uso: python3 libreria/archivo/nudillos/dib.py"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from libreria.svg.base import *  # noqa
from libreria.svg.personajes import persona
from libreria.svg.objetos import cuerpo as C, casa as K, escenarios as E

OUT = ROOT / "content" / "lote7-11-nudillos"


def hueso_roto(id_, cx, cy, s=1.0):
    """Hueso de dibujo partido en dos con grieta en zigzag."""
    o = ""
    for k, dx, ang in ((-1, -14, -10), (1, 14, 10)):
        x0 = cx + dx
        body = (f'<rect x="{f(x0 - 75*s if k < 0 else x0)}" y="{f(cy - 20*s)}" width="{f(75*s)}" height="{f(40*s)}" fill="url(#huesoG)" stroke="{INK}" stroke-width="6"/>'
                + "".join(f'<circle cx="{f(x0 + k*75*s)}" cy="{f(cy + d*24*s)}" r="{f(26*s)}" fill="url(#huesoG)" stroke="{INK}" stroke-width="6"/>' for d in (-1, 1))
                + f'<rect x="{f(x0 - 75*s if k < 0 else x0)}" y="{f(cy - 17*s)}" width="{f(72*s)}" height="{f(34*s)}" fill="url(#huesoG)"/>'
                + f'<path d="M {f(x0)} {f(cy - 20*s)} l {f(-k*10*s)} {f(10*s)} l {f(k*10*s)} {f(10*s)} l {f(-k*10*s)} {f(10*s)} l {f(k*10*s)} {f(10*s)}" fill="none" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
        o += f'<g transform="rotate({ang} {f(x0)} {f(cy)})">{body}</g>'
    return g(id_, o)


# ---------------------------------------------------------------- 1. gancho (full)
def gancho():
    kw = dict(edad="joven", piel="clara", pelo="corto", pelo_color="castano", ropa="camiseta", ropa_color=CORAL,
              brazos=("junta", "junta"))
    n = persona("chico_n", 540, 1345, 1.3, expresion="neutral", **kw)
    r = persona("chico_r", 540, 1345, 1.3, expresion="risa", **kw)
    mx, my = n.puntos["manos"]
    body = n + r
    body += ondas_sonido("ondas", mx + 90, my - 10, 40, 3, -50, 30, 26, 8, INK)
    body += g("ondas2", ondas_sonido(None, mx - 90, my - 10, 40, 3, 150, 230, 26, 8, INK))
    body += onomatopeya("crac", 830, 760, "¡CRAC!", r=130, size=58, rot_=10)
    card = tarjeta(None, 230, 640, 300, 200, acento=None, rot_=-4,
                   body=hueso_roto(None, 230, 640, 1.0))
    body += g("roto", card)
    body += aspa("aspa", 230, 640, 110)
    return svg(body, "full", fondo=E.habitacion())


# ---------------------------------------------------------------- 2. líquido sinovial (panel)
def bisagra(id_, cx, cy):
    o = sombra_caja(cx - 70, cy - 90, 140, 180)
    for k in (-1, 1):
        x = cx - 72 if k < 0 else cx + 8
        o += f'<rect x="{f(x)}" y="{f(cy - 85)}" width="64" height="170" rx="10" fill="url(#metalG)" stroke="{INK}" stroke-width="6"/>'
        for yy in (-50, 0, 50):
            o += f'<circle cx="{f(x + 32)}" cy="{f(cy + yy)}" r="8" fill="#8F9BB3" stroke="{INK}" stroke-width="3"/>'
    o += f'<rect x="{f(cx - 12)}" y="{f(cy - 95)}" width="24" height="190" rx="10" fill="url(#aceroG)" stroke="{INK}" stroke-width="6"/>'
    return g(id_, o)


def liquido():
    a = C.articulacion("art", 420, 380, 0.68)
    body = a
    body += etiqueta("lhueso", 200, 210, "HUESO", apunta=a.puntos["hueso"], size=30)
    body += etiqueta("lsinovial", 520, 125, "LÍQUIDO SINOVIAL", apunta=a.puntos["liquido"], size=30)
    gx, gy = 420 + 70 * 0.68, 380 + 112 * 0.68
    body += etiqueta("lgas", 560, 600, "GAS DISUELTO", apunta=(gx, gy), size=30)
    body += bisagra("bisagra", 860, 330)
    body += g("gota", gota(860, 200, 34, "#E8B52C"))
    body += g("lbis", T(860, 480, "COMO ACEITE", 26, INK, font=DISP))
    return svg(body, "panel", fondo=fondo_suave())


# ---------------------------------------------------------------- 3. nace la burbuja (free)
def burbuja():
    a = C.articulacion("art", 450, 420, 0.8, burbuja=True)
    body = a
    body += flecha_gorda("tirar", (640, 230), (900, 230), ancho=60, col=LIME)
    body += g("ltirar", T(770, 175, "ESTIRAS", 34, "#FFFFFF", font=DISP))
    body += medidor("pres", 200, 790, 110, 0.75)
    body += g("lpres", T(200, 850, "PRESIÓN", 32, "#FFFFFF", font=DISP))
    bx, by = a.puntos["burbuja"]
    body += etiqueta("lburbuja", 620, 700, "BURBUJA DE GAS", apunta=(bx, by + 50), size=32)
    body += onomatopeya("crac", 800, 470, "¡CRAC!", r=105, size=46, rot_=-8)
    return svg(body, "free", h=900)


# ---------------------------------------------------------------- 4. resonancia en directo (panel)
def resonancia():
    rm = C.escaner_resonancia("rm", 255, 320, 380)
    body = rm
    body += C.mano("dedo", 255, 330, 0.42, piel="media")
    mon = (f'<rect x="530" y="140" width="420" height="320" rx="22" fill="#1B1E2B" stroke="{INK}" stroke-width="8"/>'
           f'<rect x="550" y="160" width="380" height="280" rx="10" fill="#0E2A44"/>'
           f'<rect x="710" y="460" width="60" height="50" fill="url(#metalG)" stroke="{INK}" stroke-width="6"/>'
           f'<rect x="650" y="505" width="180" height="22" rx="8" fill="url(#metalG)" stroke="{INK}" stroke-width="6"/>')
    mini = C.articulacion("mini", 715, 310, 0.42, burbuja=True, gas=False)
    body += g("monitor", mon + mini + g("rec", '<circle cx="590" cy="190" r="12" fill="#FF3B3B"/>' + T(630, 200, "REC", 26, "#FFFFFF", font=DISP)))
    body += etiqueta("l2015", 740, 590, "AÑO 2015", size=32)
    body += ondas_sonido("ondas", 790, 300, 50, 3, -50, 50, 24, 7, LIME)
    body += etiqueta("lalavez", 270, 610, "SUENA AL NACER", size=30, bg=CORAL, fg="#FFFFFF")
    return svg(body, "panel", fondo=fondo_suave())


# ---------------------------------------------------------------- 5. veinte minutos (free)
def espera():
    a = C.articulacion("art", 330, 250, 0.58, abierta=30, burbuja=True)
    body = a
    body += K.cronometro("crono", 800, 330, 120)
    body += etiqueta("l20", 800, 530, "20 MINUTOS", size=34)
    body += etiqueta("ldisuelve", 330, 70, "SE DISUELVE", size=30, bg=LIME, fg=INK)
    m = C.mano("mano", 300, 650, 0.62, piel="media")
    body += m
    nx, ny = m.puntos["nudillos"][1]
    body += icono_no("no", 470, 560, 52)
    body += globo("globo", 640, 700, "¿OTRA VEZ?", cola=(420, 640), size=34)
    return svg(body, "free", h=880)


# ---------------------------------------------------------------- 6. Donald Unger (full)
def unger():
    doc = persona("doc", 330, 1340, 1.25, "mayor", "clara", "calvo", "canoso", "chaqueta", "#F4F6FA",
                  pantalon_color="#5A647A", camisa_color="#9CC9FF", accesorios=("gafas", "bigote"),
                  expresion="neutral", brazos=("explica", "saluda"))
    body = doc
    body += icono_duda("duda", 330, 470, 56)
    body += etiqueta("lnombre", 330, 1250, "DR. DONALD UNGER", size=34)
    body += tarjeta("fondo_mano", 790, 735, 360, 450, acento=LIME, rot_=3)
    m = C.mano("mgrande", 790, 720, 0.85, piel="clara", espejo=True)
    body += m
    body += onomatopeya("crac", 800, 500, "¡CRAC!", r=95, size=40, rot_=8)
    body += etiqueta("lsola", 790, 930, "SOLO ESTA MANO", size=30, bg=CORAL, fg="#FFFFFF")
    body += contador("c50", 790, 1080, "50 AÑOS", None, w=330, h=110)
    return svg(body, "full", fondo=E.oficina())


# ---------------------------------------------------------------- 7. sin artrosis y premio (panel)
def premio():
    body = ""
    for i, (cx, txt, piel_) in enumerate(((190, "CRUJÍA", "clara"), (450, "NO CRUJÍA", "clara"))):
        body += C.mano(f"m{i}", cx, 330, 0.58, piel=piel_, espejo=(i == 1))
        body += etiqueta(f"lm{i}", cx, 130, txt, size=28)
        body += icono_ok(f"ok{i}", cx + 80, 420, 44)
    body += sello("sello", 320, 580, "SIN ARTROSIS", size=50, rot_=-6, col=CORAL)
    t = K.trofeo("trofeo", 790, 620, 420, "IG NOBEL")
    body += t
    body += confeti("confeti", (620, 80, 970, 300), n=22)
    return svg(body, "panel", fondo=fondo_suave())


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in (("gancho_full.svg", gancho), ("liquido.svg", liquido), ("burbuja_free.svg", burbuja),
                     ("resonancia.svg", resonancia), ("espera_free.svg", espera), ("unger_full.svg", unger),
                     ("premio.svg", premio)):
        guardar(str(OUT / name), fn())

"""SVG de content/lote8-04-agua-caliente (¿El agua caliente se congela antes que la fría? Efecto Mpemba).
Uso: python3 libreria/archivo/agua-caliente/dib.py"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from libreria.svg.base import *  # noqa
from libreria.svg.personajes import persona
from libreria.svg.objetos import casa as K, escenarios as E, politica as P, frio as F

OUT = ROOT / "content" / "lote8-04-agua-caliente"
OUT.mkdir(parents=True, exist_ok=True)
FRIA = "#2F8FE0"


def bandera_tanzania(id_, cx, cy, w=170, h=114):
    """Bandera de Tanzania (verde arriba a la izquierda, azul abajo a la derecha, franja negra con bordes amarillos)."""
    x0, y0 = cx - w / 2, cy - h / 2
    cid = f"clipTz{int(cx)}"
    registrar_defs(f'<clipPath id="{cid}"><rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" rx="6"/></clipPath>')
    o = trazo(f"M {f(x0-8)} {f(y0-14)} L {f(x0-8)} {f(y0+h*2.0)}", 9, "#8A93A6", 5)
    o += f'<circle cx="{f(x0-8)}" cy="{f(y0-16)}" r="9" fill="url(#amarilloG)" stroke="{INK}" stroke-width="4"/>'
    t = (f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" fill="#00A3DD"/>'
         f'<path d="M {f(x0)} {f(y0)} L {f(x0+w)} {f(y0)} L {f(x0)} {f(y0+h)} Z" fill="#1EB53A"/>'
         f'<path d="M {f(x0-20)} {f(y0+h+10)} L {f(x0+w+20)} {f(y0-10)}" stroke="#FCD116" stroke-width="{f(h*0.42)}"/>'
         f'<path d="M {f(x0-20)} {f(y0+h+10)} L {f(x0+w+20)} {f(y0-10)}" stroke="#000000" stroke-width="{f(h*0.28)}"/>')
    o += f'<g clip-path="url(#{cid})">{t}</g>'
    o += f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" rx="6" fill="none" stroke="{INK}" stroke-width="6"/>'
    return g(id_, o)


# ---------------------------------------------------------------- 0 y 7. cocina (full): ¿cuál se congela antes?
def cocina():
    body = ""
    cg = F.congelador("cong", 790, 1290, 420, 700, baldas=3)
    body += cg
    b = cg.puntos["baldas"]
    yb = b[1]  # balda del medio
    vc = K.vaso("vcal", 715, yb - 2, 190, 130, 0.72, "agua")
    vf = K.vaso("vfri", 870, yb - 2, 190, 130, 0.72, "agua", cubitos=1)
    body += vc + vf
    body += F.vapor_subiendo("vapor", 715, yb - 200, 110, 130)
    body += g("tcal", etiqueta(None, 715, b[0] + 50, "CALIENTE", size=26, bg=CORAL, fg="#FFFFFF"))
    body += g("tfri", etiqueta(None, 870, b[0] + 50, "FRÍA", size=26, bg=FRIA, fg="#FFFFFF"))
    body += g("frioicon", copo(870, b[2] - 120, 34, 10, "#2F6FB0"))
    pz = persona("ana", 270, 1300, 1.32, "joven", "clara", "coleta", "castano", "camiseta", TEAL,
                 pantalon_color="#3E5C93", expresion="duda", brazos=("barbilla", "explica"))
    body += pz
    body += globo("globo", 640, 515, "¿CUÁL SE\nCONGELA ANTES?", cola=(pz.puntos["boca"][0] + 50, pz.puntos["boca"][1] - 10), size=40)
    body += icono_duda("duda", 430, 640, 46)
    # gancho: la caliente gana (a veces)
    body += icono_ok("ok", 715, b[1] - 250, 42)
    body += sello("aveces", 560, 1010, "¡A VECES!", size=60, rot_=-8)
    # veredicto (escena 7)
    body += sello("veredicto", 540, 530, "A VECES SÍ", size=70, rot_=-6, col=LIME, fondo=INK)
    body += etiqueta("lvaso", 200, 1190, "EL VASO", size=34, bg=LIME, fg=INK)
    body += etiqueta("lagua", 480, 1190, "EL AGUA", size=34, bg=LIME, fg=INK)
    body += etiqueta("lcong", 800, 1190, "EL CONGELADOR", size=30, bg=LIME, fg=INK)
    return svg(body, "full", fondo=E.cocina())


# ---------------------------------------------------------------- 1. Mpemba en Tanzania (panel)
def mpemba():
    body = ""
    cg = F.congelador("cong", 790, 650, 250, 470, baldas=2, rotulo=None)
    body += cg
    b = cg.puntos["baldas"]
    body += F.cuenco("cfrio", 800, b[1] - 4, 130)
    p = persona("erasto", 250, 660, 0.9, "joven", "oscura", "rapado", "negro", "camisa", "#FFFFFF",
                pantalon_color="#3E5C93", expresion="risa", brazos=("relajado", "coge"))
    body += p
    mx, my = p.puntos["mano_der"]
    cu = F.cuenco(None, mx + 40, my + 30, 150, vapor=True)
    body += g("helado", cu)
    body += bandera_tanzania("bandera", 470, 110, 130, 86)
    body += etiqueta("ltz", 455, 205, "TANZANIA", size=28)
    body += etiqueta("l1963", 420, 600, "1963", size=40, bg=LIME, fg=INK)
    body += etiqueta("lerasto", 250, 75, "ERASTO MPEMBA", size=30)
    body += etiqueta("lcal", mx + 40, my + 110, "¡AÚN CALIENTE!", size=26, bg=CORAL, fg="#FFFFFF")
    print("delta helado", round(800 - (mx + 40)), round(b[0] - 4 - (my + 30)))
    return svg(body, "panel", fondo=fondo_suave())


# ---------------------------------------------------------------- 2. se congeló antes + publicación (free)
def helado():
    H = 860
    body = ""
    # interior del congelador (recuadro helado)
    body += sombra_caja(60, 40, 880, 420, 24, 14, 16, 0.25)
    body += f'<rect x="60" y="40" width="880" height="420" rx="24" fill="url(#congInt)" stroke="{INK}" stroke-width="8"/>'
    body += F.escarcha(None, 70, 930, 400, 22, seed=5)
    body += f'<rect x="64" y="400" width="872" height="16" rx="5" fill="#C9D6E6" stroke="{INK}" stroke-width="4"/>'
    body += g("cliq_a", F.cuenco(None, 290, 398, 250, "liquido"))
    body += g("chel_a", F.cuenco(None, 290, 398, 250, "helado"))
    body += F.cuenco("cliq_b", 710, 398, 250, "liquido")
    body += etiqueta("lsuyo", 290, 95, "EL SUYO: CALIENTE", size=26, bg=CORAL, fg="#FFFFFF")
    body += etiqueta("lotro", 710, 95, "EL OTRO: FRÍO", size=26, bg=FRIA, fg="#FFFFFF")
    body += icono_ok("ok", 420, 210, 40)
    body += g("copos", copo(170, 200, 26, 0) + copo(410, 300, 20, 20) + copo(200, 330, 16, 10))
    body += P.documento("revista", 330, 640, 300, 320, "PHYSICS EDUCATION", "1969", rot_=-5)
    body += g("lcool", T(330, 720, "«COOL?»", 38, INK, font=DISP))
    body += sello("efecto", 690, 640, "EFECTO MPEMBA", size=40, rot_=-7)
    body += etiqueta("lfisico", 720, 760, "CON EL FÍSICO DENIS OSBORNE", size=22)
    return svg(body, "free", h=H)


# ---------------------------------------------------------------- 3, 4 y 5. el vaso caliente por dentro (free)
def vaso():
    H = 900
    body = ""
    cx, base = 500, 720
    # balda del congelador
    body += f'<rect x="120" y="{base+6}" width="760" height="22" rx="6" fill="#C9D6E6" stroke="{INK}" stroke-width="5"/>'
    body += g("rejilla", "".join(f'<line x1="{x}" y1="{base+10}" x2="{x}" y2="{base+24}" stroke="#8C9BB0" stroke-width="3"/>' for x in range(140, 870, 30)))
    body += F.escarcha("escarcha", 130, 870, base + 8, 30, seed=7)
    body += F.escarcha("charco", 330, 670, base + 8, 30, derretida=True)
    va = K.vaso("vaso_a", cx, base, 500, 360, 0.82, "agua", burbujas=0)
    vb = K.vaso("vaso_b", cx, base, 500, 360, 0.6, "agua", burbujas=0)
    body += va + vb
    sa, sb = va.puntos["superficie"], vb.puntos["superficie"]
    body += F.vapor_subiendo("vapor", cx, va.puntos["borde"][1] - 10, 220, 170, n=4)
    body += flecha("fevap", (cx + 230, sa[1] + 10), (cx + 230, sa[1] - 200), col=CORAL, w=12)
    body += etiqueta("levap", 860, 150, "SE EVAPORA", size=30, bg=CORAL, fg="#FFFFFF")
    body += etiqueta("lmenos", 165, sb[1], "MENOS AGUA", size=28, bg=LIME, fg=INK)
    body += flecha("fnivel", (300, sa[1]), (300, sb[1] - 24), col=LIME, w=10, punta=24)
    # convección
    body += F.corrientes("corr", cx, (sb[1] + base) / 2 + 6, 290, base - sb[1] - 70)
    body += etiqueta("lcorr", 165, 470, "CORRIENTES", size=28)
    body += flecha("fcal1", (cx + 160, 560), (cx + 330, 520), col=CORAL, w=12)
    body += flecha("fcal2", (cx - 160, 600), (cx - 330, 650), col=CORAL, w=12)
    body += etiqueta("lcalor", 840, 450, "CALOR FUERA", size=26, bg=CORAL, fg="#FFFFFF")
    # gases
    body += F.burbujas_gas("gases", cx, base - 40, sb[1] + 10, 220, 7, texto="GAS")
    body += etiqueta("lgas", 860, 300, "MENOS GAS", size=28, bg=LIME, fg=INK)
    body += etiqueta("lcontacto", 500, base + 100, "TOCA MEJOR EL FRÍO", size=28, bg=FRIA, fg="#FFFFFF")
    return svg(body, "free", h=H)


# ---------------------------------------------------------------- 6. el estudio de 2016 (panel)
def estudio():
    body = ""
    gr = F.grafica_enfriamiento("graf", 40, 80, 580, 560, [
        ("ccal", [(0, 70), (0.12, 48), (0.28, 30), (0.45, 16), (0.62, 7), (0.8, 2), (0.95, 0)], CORAL, "CALIENTE"),
        ("cfri", [(0, 30), (0.12, 20), (0.28, 11), (0.45, 5), (0.6, 1.5), (0.72, 0)], FRIA, "FRÍA"),
    ], t_max=1.0, temp_max=80)
    body += gr
    body += etiqueta("l2016", 330, 60, "BURRIDGE Y LINDEN · 2016", size=26)
    body += sello("nolovio", 360, 560, "NO SE ADELANTA", size=40, rot_=-8)
    pa = persona("cienA", 730, 690, 0.62, "adulto", "media", "corto", "negro", "camisa", "#FFFFFF",
                 accesorios=("gafas",), expresion="risa", brazos=("cintura", "apunta_arriba"))
    pb = persona("cienB", 900, 690, 0.62, "adulto", "clara", "largo", "rubio", "jersey", VIO,
                 expresion="enfado", brazos=("cruzados", "relajado"))
    body += pa + pb
    body += globo("gsi", 720, 150, "¡PASA!", cola=pa.puntos["boca"], size=34)
    body += globo("gno", 905, 250, "¡NO!", cola=pb.puntos["boca"], size=34)
    body += etiqueta("lcons", 815, 640, "SIN CONSENSO", size=28, bg=LIME, fg=INK)
    return svg(body, "panel", fondo=fondo_suave())


if __name__ == "__main__":
    guardar(OUT / "cocina_full.svg", cocina())
    guardar(OUT / "mpemba.svg", mpemba())
    guardar(OUT / "helado_free.svg", helado())
    guardar(OUT / "vaso_free.svg", vaso())
    guardar(OUT / "estudio.svg", estudio())

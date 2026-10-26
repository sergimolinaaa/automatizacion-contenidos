"""lote9-02-pierna-dormida: dibujos de «¿Por qué se te duerme la pierna?».
Uso: python3 libreria/archivo/pierna-dormida/dib.py

Método rossark: cada parte en su grupo con su pivote (persona en los pies, cabeza en el cuello, pierna de arriba que
baja entera, aguja del medidor con caja centrada en su eje), cada repetido (hormigas, burbujas, fibras, agujas) con su
id para darle su propia fase, y todo lo que «cambia» se dibuja dos veces en el mismo sitio para relevarse con hide/fade.
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from libreria.svg.base import *  # noqa
from libreria.svg.personajes import persona
from libreria.svg.objetos import casa as K, escenarios as E, cuerpo as C, politica as P, nervios as N

OUT = ROOT / "content" / "lote9-02-pierna-dormida"
OUT.mkdir(parents=True, exist_ok=True)
MOSTAZA = "#E0A526"
MALLAS = "#2F3448"
SHORT = "#3A4256"


def cerebrito(id_, cx, cy, s):
    return g(id_, f'<circle cx="{f(cx)}" cy="{f(cy+6)}" r="{f(190*s)}" fill="#FFFFFF" opacity="0.16"/>' + C.cerebro(None, cx, cy, s, hipotalamo=False))


def golpes(id_, cx, cy, r=60, col=AMARILLO):
    """Rayitas de impacto alrededor de un punto (arriba)."""
    o = ""
    for a in (-150, -120, -90, -60, -30):
        import math
        ra = math.radians(a)
        x0, y0 = cx + r * math.cos(ra), cy + r * math.sin(ra)
        x1, y1 = cx + (r + 34) * math.cos(ra), cy + (r + 34) * math.sin(ra)
        o += trazo(f"M {f(x0)} {f(y0)} L {f(x1)} {f(y1)}", 9, col, 6)
    return g(id_, o)


# ---------------------------------------------------------------- 0. gancho: pierna de corcho (full)
def gancho():
    suelo = 1325
    body = K.sofa("sofa", 400, suelo, w=600, asiento=166, col="#2EC4B6")
    sentada = persona("luS", 400, suelo, 1.3, "adulto", "media", "coleta", "castano", "jersey", MOSTAZA, MALLAS,
                      zapato_color="#F2F4F8", expresion="neutral", pose="sentado", brazos=("abajo", "abajo"), mira=1)
    body += sentada
    e = 1.42
    x0 = 450
    lu = persona("lu", x0, suelo, e, "adulto", "media", "coleta", "castano", "jersey", MOSTAZA, MALLAS,
                 zapato_color="#F2F4F8", expresion="duda", brazos=("relajado", "cintura"), mira=-1)

    def L(lx, ly):
        return (x0 + lx * e, suelo + ly * e)
    # pierna izquierda (en pantalla) de corcho, encima de la pernera
    cd = smooth([L(-58, -250), L(-34, -258), L(-9, -250), L(-11, -140), L(-13, -30), L(-36, -24), L(-61, -30), L(-60, -140)], True, 0.2)
    cork = (f'<path d="{cd}" fill="{N.corcho()}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
            + brillo(f"M {f(L(-46, -230)[0])} {f(L(-46, -230)[1])} L {f(L(-48, -60)[0])} {f(L(-48, -60)[1])}", 5, 0.45))
    hormigas = ""
    for i, (lx, ly, a) in enumerate(((-40, -48, -100), (-24, -84, -80), (-46, -118, -95), (-22, -40, -75), (-34, -150, -88))):
        x, y = L(lx, ly)
        hormigas += g(f"hg{i}", N.hormiga(f"h{i}", x, y, 1.25, a))
    chis = ""
    for i, (lx, ly, r) in enumerate(((-88, -215, 32), (14, -175, 26), (-92, -112, 24), (12, -72, 28))):
        x, y = L(lx, ly)
        chis += chispa(f"ch{i}", x, y, r, "#FFFFFF")
    body += g("luG", lu + g("corcho", cork) + hormigas + chis)
    hx, hy = lu.puntos["cabeza"]
    body += icono_duda("duda", hx + 165, hy + 10, 46)
    body += flecha("fpierna", (170, 900), (330, 1060), col=LIME, w=12, punta=30, curva=-0.25)
    body += g("ay", T(hx - 170, hy - 40, "¡UF!", 64, "#FFFFFF", font=DISP, extra=f'stroke="{INK}" stroke-width="8" paint-order="stroke"'))
    guardar(f"{OUT}/gancho_full.svg", svg(body, "full", fondo=E.habitacion()))


# ---------------------------------------------------------------- 1. cruzar las piernas: nervio aplastado (free)
def cruzar():
    H = 880
    x0, cy, Lg = 150, 490, 740
    pres = 0.30
    # asiento (cojín del sofá) bajo el muslo
    asiento = (f'<rect x="40" y="566" width="520" height="92" rx="26" fill="{degradado(shade("#2EC4B6", 0.15), 0.2)}" stroke="{INK}" stroke-width="7"/>'
               f'<rect x="60" y="650" width="480" height="90" rx="18" fill="{degradado(shade("#2EC4B6", -0.15), 0.2)}" stroke="{INK}" stroke-width="7"/>'
               + brillo("M 80 586 L 400 586", 6, 0.5))
    pb = N.pierna_nervio("pb", x0, cy, Lg, 1.0, "media", pres=pres, short_col=SHORT)
    px, ptop = pb.puntos["presion"]
    esp, mus = N.pierna_encima("pt", 120, 350, px, ptop - 52, 1.0, "media", short_col=SHORT)
    body = g("asientoG", asiento) + g("espG", esp) + g("pbG", pb) + g("ptG", mus)
    body += flecha_gorda("fpeso", (px, 150), (px, 262), ancho=60, col=CORAL)
    body += golpes("gol", px, ptop + 4, 70)
    # mensajes atascados: puntitos lima sobre el nervio, a la derecha del apretón
    nv = [p for p in pb.puntos["nervio"] if p[0] > px + 60 and p[1] < cy + 60]
    xs = (px + 100, px + 145, px + 190)
    for i, xx in enumerate(xs):
        pnt = min(nv, key=lambda p: abs(p[0] - xx))
        body += g(f"m{i}", f'<circle cx="{f(pnt[0])}" cy="{f(pnt[1])}" r="13" fill="{LIME}" stroke="{INK}" stroke-width="4"/>')
    # cable al cerebro
    body += g("cable", f'<path d="M 132 520 Q 20 360 128 214" fill="none" stroke="{INK}" stroke-width="20" stroke-linecap="round"/>'
              f'<path d="M 132 520 Q 20 360 128 214" fill="none" stroke="{N.NERVIO}" stroke-width="11" stroke-linecap="round"/>')
    body += cerebrito("cere", 150, 140, 0.34)
    body += icono_duda("cduda", 262, 92, 30)
    body += etiqueta("tnervio", 850, 540, "NERVIO", apunta=(px + 240, cy + 30), desde=(790, 540), bg=LIME, fg=INK, size=34)
    body += etiqueta("tcable", 740, 250, "CABLE DE MENSAJES", bg=INK, fg=LIME, size=30)
    guardar(f"{OUT}/cruzar_free.svg", svg(body, "free", h=H))
    return pb


# ---------------------------------------------------------------- 2. vasos apretados: menos oxígeno (free)
def oxigeno():
    H = 860
    import math
    X0, X1, Y0, Y1 = 40, 960, 270, 790
    cid = "oxTejido"
    tej = (f'<clipPath id="{cid}"><rect x="{X0}" y="{Y0}" width="{X1-X0}" height="{Y1-Y0}" rx="40"/></clipPath>'
           f'<rect x="{X0}" y="{Y0}" width="{X1-X0}" height="{Y1-Y0}" rx="40" fill="url(#nvTejido)" stroke="{INK}" stroke-width="8"/>')
    vy, ny = 420, 640
    inner = (f'<rect x="{X0}" y="{Y0}" width="{X1-X0}" height="34" fill="#F7CFB2"/>'
             f'<path d="M {X0} {Y0+34} L {X1} {Y0+34}" stroke="#C98462" stroke-width="5"/>')
    inner += N.vaso_tubo("vaso", X0 - 20, X1 + 20, vy, 56)
    inner += N.vaso_tubo("vaso_apl", X0 - 20, X1 + 20, vy, 56, estrecho=500, k=0.32)
    inner += N.nervio_tubo("nerv", X0 - 20, X1 + 20, ny, 82, n=7)
    inner += N.nervio_tubo("nerv_apl", X0 - 20, X1 + 20, ny, 82, n=7, estrecho=500, k=0.62)
    # burbujas de oxígeno dentro del vaso
    bur = ""
    for i, x in enumerate((110, 200, 290, 375)):
        bur += N.burbuja_o2(f"oi{i}", x, vy + (-6 if i % 2 else 6), 22)
    for i, x in enumerate((640, 750, 860)):
        bur += N.burbuja_o2(f"od{i}", x, vy + (6 if i % 2 else -6), 22)
    inner += bur
    # el oxígeno pasa del vaso al nervio (flechitas azules)
    for i, x in enumerate((650, 760, 870)):
        inner += flecha(f"dif{i}", (x, vy + 62), (x, ny - 92), col="#7CC8FF", w=8, punta=18)
    tej += f'<g clip-path="url(#{cid})">{inner}</g>'
    body = g("tejG", tej)
    # la otra pierna (rodilla) que aprieta desde arriba
    rod = (f'<ellipse cx="500" cy="150" rx="170" ry="120" fill="url(#piel_media)" stroke="{INK}" stroke-width="8"/>'
           + brillo("M 380 110 Q 460 50 560 62", 7, 0.6)
           + f'<path d="M 420 210 Q 500 236 580 210" fill="none" stroke="#B0715A" stroke-width="5" stroke-linecap="round" opacity="0.7"/>')
    body += g("rodilla", rod)
    body += g("presion", flecha(None, (300, 220), (380, 300), col=CORAL, w=10, punta=24) + flecha(None, (700, 220), (620, 300), col=CORAL, w=10, punta=24))
    body += etiqueta("tvaso", 160, vy - 92, "VASO", bg=INK, fg="#FFFFFF", size=30)
    body += etiqueta("tnerv", 170, ny, "NERVIO", bg=INK, fg=LIME, size=30)
    # medidor de oxígeno (aguja en su propio grupo, con la caja centrada en el eje para girarla con origin center)
    mx, my, r = 850, 170, 92
    med = f'<path d="M {mx-r} {my} A {r} {r} 0 0 1 {mx+r} {my} Z" fill="#FFFFFF" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
    for i, c in enumerate((CORAL, AMARILLO, LIME)):
        a0, a1 = math.pi + i * math.pi / 3, math.pi + (i + 1) * math.pi / 3
        ri = r * 0.76
        med += (f'<path d="M {f(mx+ri*math.cos(a0))} {f(my+ri*math.sin(a0))} A {f(ri)} {f(ri)} 0 0 1 {f(mx+ri*math.cos(a1))} {f(my+ri*math.sin(a1))}" '
                f'fill="none" stroke="{c}" stroke-width="{f(r*0.18)}"/>')
    a = math.pi + 0.86 * math.pi
    tip = (mx + r * 0.7 * math.cos(a), my + r * 0.7 * math.sin(a))
    ag = (f'<circle cx="{mx}" cy="{my}" r="{f(r*0.72)}" fill="none" stroke="none"/>'
          + trazo(f"M {mx} {my} L {f(tip[0])} {f(tip[1])}", 7, INK, 5) + f'<circle cx="{mx}" cy="{my}" r="10" fill="{INK}"/>')
    body += g("medG", med + g("aguja", ag) + etiqueta(None, mx, my + 42, "O₂ AL NERVIO", bg=INK, fg="#7CC8FF", size=24))
    guardar(f"{OUT}/oxigeno_free.svg", svg(body, "free", h=H))


# ---------------------------------------------------------------- 3. el nervio se calla: parestesia (free)
def calla():
    H = 860
    x0, cy, Lg, s = 120, 500, 640, 0.86
    pc = N.pierna_nervio("pc", x0, cy, Lg, s, "media", pres=0.38, short_col=SHORT)
    gris = f'<path d="{pc.puntos["contorno"]}" fill="#8E9BB4" opacity="0.62"/>'
    body = g("pcG", pc + g("gris", gris))
    body += g("cable", f'<path d="M 104 528 Q 10 360 150 232" fill="none" stroke="{INK}" stroke-width="20" stroke-linecap="round"/>'
              f'<path d="M 104 528 Q 10 360 150 232" fill="none" stroke="{N.NERVIO}" stroke-width="11" stroke-linecap="round"/>')
    body += cerebrito("cere", 200, 150, 0.4)
    body += g("bon", K.bombilla(None, 420, 120, 110, encendida=True))
    body += g("boff", K.bombilla(None, 420, 120, 110, encendida=False))
    # sobres (mensajes) que suben por la pantorrilla y se atascan en la rodilla
    kx, ky = pc.puntos["rodilla"]
    ax, ay = pc.puntos["tobillo"]
    for i in range(3):
        body += P.sobre(ax - 30 + i * 6, ay - 10 - i * 4, 62, 42, rot_=-8 + i * 7, id_=f"sob{i}")
    body += aspa("x", kx - 6, ky + 70, 34)
    body += etiqueta("tpar", 790, 560, "PARESTESIA", bg=LIME, fg=INK, size=46)
    body += etiqueta("tsub1", 790, 640, "HORMIGUEO", bg=INK, fg=LIME, size=28)
    body += etiqueta("tsub2", 790, 708, "Y ADORMECIMIENTO", bg=INK, fg=LIME, size=28)
    guardar(f"{OUT}/calla_free.svg", svg(body, "free", h=H))
    return pc


# ---------------------------------------------------------------- 4. despiertan a destiempo: pinchazos (full)
def pinchazos():
    W, Hh = 1080, 1920
    registrar_defs(lg("pzFondo", [(0, "#4A1430"), (0.5, "#2C0B1E"), (1, "#16050F")]))
    fondo = f'<rect width="{W}" height="{Hh}" fill="url(#pzFondo)"/>'
    import random
    rnd = random.Random(8)
    for _ in range(22):
        fondo += f'<circle cx="{f(rnd.uniform(0, W))}" cy="{f(rnd.uniform(300, 1500))}" r="{f(rnd.uniform(14, 60))}" fill="#FF7EB6" opacity="{f(rnd.uniform(0.04, 0.12))}"/>'
    body = ""
    vy = 610
    body += g("vasoG", N.vaso_tubo("vstrecho", -30, W + 30, vy, 72, estrecho=540, k=0.3) + N.vaso_tubo("vabierto", -30, W + 30, vy, 72))
    for i, x in enumerate((70, 170, 260, 340, 410)):
        body += N.globulo(f"gl{i}", x, vy + (-10 if i % 2 else 12), 34, ang=-15 + i * 9)
    body += etiqueta("tsangre", 170, vy - 2, "SANGRE", bg=INK, fg="#FFFFFF", size=28)
    hz = N.haz_fibras("hz", 50, W - 50, 915, h=360, n=10)
    body += g("hzG", hz)
    body += etiqueta("tfib", 540, 735, "FIBRAS DEL NERVIO", bg=LIME, fg=INK, size=30)
    # piel abajo y agujas que pinchan
    piel = (f'<path d="M -20 1220 Q 270 1200 540 1216 T 1100 1210 L 1100 1370 L -20 1370 Z" fill="url(#piel_media)" stroke="{INK}" stroke-width="8"/>'
            f'<path d="M -20 1270 Q 300 1256 540 1268 T 1100 1264" fill="none" stroke="#C98462" stroke-width="5" opacity="0.6"/>')
    body += g("piel", piel)
    for i, (x, a) in enumerate(((130, 80), (300, 96), (450, 86), (620, 100), (780, 82), (950, 94))):
        body += N.aguja(f"ag{i}", x, 1212, 118, a)
        body += chispa(f"cz{i}", x + (12 if i % 2 else -12), 1220, 22, "#FFFFFF")
    body += onomatopeya("zzt", 540, 920, "¡ZZZT!", r=150, size=66, rot_=-6)
    guardar(f"{OUT}/pinchazos_full.svg", svg(body, "full", fondo=fondo))


# ---------------------------------------------------------------- 5. el nervio peroneo (free)
def peroneo():
    H = 900
    rd = N.rodilla_lateral("rod", 360, 450, 0.92, "media")
    px, py = rd.puntos["peroneo"]
    body = g("rodG", rd)
    otra = (f'<ellipse cx="60" cy="{f(py)}" rx="130" ry="100" fill="url(#piel_media)" stroke="{INK}" stroke-width="8"/>'
            + brillo(f"M -20 {f(py-60)} Q 50 {f(py-96)} 130 {f(py-70)}", 7, 0.6))
    body += g("otra", otra)
    body += golpes("gol", px + 6, py + 4, 64, AMARILLO)
    body += onda_expansiva("onda", px, py, 46, col=LIME)
    body += lupa("lupa", 735, 420, 175, ang=165, contenido=N.nervio_lupa(735, 420, 175, True))
    body += etiqueta("tper", 735, 690, "NERVIO PERONEO", apunta=(px + 20, py + 26), desde=(600, 690), bg=LIME, fg=INK, size=34)
    body += etiqueta("tlado", 735, 760, "POR EL LADO DE LA RODILLA", bg=INK, fg=LIME, size=24)
    guardar(f"{OUT}/peroneo_free.svg", svg(body, "free", h=H))
    return rd


if __name__ == "__main__":
    gancho()
    cruzar()
    oxigeno()
    calla()
    pinchazos()
    peroneo()

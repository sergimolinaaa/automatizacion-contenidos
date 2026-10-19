"""SVG de content/lote7-07-avion (¿Cómo vuela un avión de 400 toneladas?).
Uso: python3 libreria/archivo/avion/dib.py"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from libreria.svg.base import *  # noqa
from libreria.svg.personajes import persona, EDADES
from libreria.svg.objetos import aviones as A, escenarios as E, territorio as TE, casa as CA, piel as PI, coches as CO  # noqa: F401 (registra asfaltoG)

OUT = ROOT / "content" / "lote7-07-avion"
AIRE = "#3FA9F5"


def nubes_grupo(id_, lista):
    return g(id_, "".join(nube(x, y, s, contorno=True) for x, y, s in lista))


# ---------------------------------------------------------------- 0. gancho (full): jumbo, balanza y niña
def gancho():
    body = nubes_grupo("nubes", ((180, 820, 0.55), (930, 880, 0.45)))
    body += A.jumbo("jumbo", 560, 540, 0.92)
    # balanza: mini jumbo a la izquierda, pila de coches a la derecha
    mini = g("mini", f'<g transform="translate(0 -48)">{A.jumbo(None, 0, 0, 0.19)}</g>')
    cols = (CORAL, "#2EC4B6", YEL, VIO, "#3D63FF", "#36B37E")
    coches = ""
    k = 0
    for fila, (n, dy) in enumerate(((3, 0), (2, -30), (1, -60))):
        for i in range(n):
            x = (i - (n - 1) / 2) * 72
            coches += A.cochecito(f"car{k}", x, dy - 2, 0.4, cols[k % len(cols)])
            k += 1
    bal = TE.balanza("bal", 650, 1262, 500, 0, izq=mini, der=coches)
    body += bal
    lx, ly = bal.puntos["plato_izq"]
    rx_, ry_ = bal.puntos["plato_der"]
    body += etiqueta("t400", lx - 20, ly + 120, "400 TONELADAS", size=30, bg=INK, fg=LIME)
    body += etiqueta("t300", rx_ - 10, ry_ + 120, "CASI 300 COCHES", size=28, bg=LIME, fg=INK)
    # niña con chubasquero
    p = persona("nina", 150, 1300, 0.95, "nino", "clara", "coleta", "castano", "abrigo", YEL,
                pantalon_color="#3E5C93", zapato_color=CORAL, expresion="sorpresa", brazos=("relajado", "apunta_arriba"), mira=1)
    body += p
    hx, hy = p.puntos["cabeza"]
    body += icono_duda("duda", hx + 70, hy - 110, 42)
    return svg(body, "full", fondo=E.cielo(hora="dia", colinas=True, nubes=True, sol_=True))


# ---------------------------------------------------------------- 1. el ala desvía aire (panel)
def desvia():
    c = (500, 360)
    plano = A.perfil_ala("ala", c[0], c[1], 440, 0)
    incl = A.perfil_ala(None, c[0], c[1], 440, 9, curva=False)
    body = A.lineas_corriente("aire", incl, 40, 960, arriba=(55, 125), abajo=(55, 125), bajada=26)
    body += g("ref", f'<path d="M 230 {c[1]} L 790 {c[1]}" stroke="{INK}" stroke-width="4" stroke-dasharray="14 10" opacity="0.55"/>')
    body += plano
    ax, ay = rot((c[0] + 300, c[1]), c, 9)
    arco = f'<path d="M {f(c[0]+300)} {f(c[1])} A 300 300 0 0 1 {f(ax)} {f(ay)}" fill="none" stroke="{CORAL}" stroke-width="9" stroke-linecap="round"/>'
    q0, q1 = rot((c[0] - 330, c[1]), c, 9), rot((c[0] + 330, c[1]), c, 9)
    cuerda = f'<path d="M {f(q0[0])} {f(q0[1])} L {f(q1[0])} {f(q1[1])}" stroke="{CORAL}" stroke-width="5" stroke-dasharray="14 10"/>'
    body += g("angulo", cuerda + arco + etiqueta(None, 880, 470, "ÁNGULO", size=28, bg=CORAL, fg="#FFFFFF"))
    body += etiqueta("tcurva", 430, 160, "CURVADA", size=28, bg=LIME, fg=INK, apunta=(470, 285))
    body += etiqueta("tabajo", 760, 620, "AIRE HACIA ABAJO", size=28, bg=AIRE, fg=INK)
    body += CA.cronometro("crono", 880, 140, 62)
    body += etiqueta("tseg", 720, 105, "CADA SEGUNDO", size=24)
    return svg(body, "panel", fondo=fondo_suave())


# ---------------------------------------------------------------- 2. acción y reacción + Newton (free)
def newton():
    H = 860
    a = A.perfil_ala("ala", 360, 440, 440, 9, curva=False)
    body = A.lineas_corriente("aire", a, 30, 690, arriba=(60,), abajo=(60,), bajada=28, flecha_=False)
    body += a
    body += flecha_gorda("fabajo", (440, 540), (440, 790), ancho=90, col=AIRE)
    body += flecha_gorda("farriba", (340, 340), (340, 130), ancho=90, col=NARANJA)
    body += etiqueta("taccion", 640, 690, "ACCIÓN", size=32, bg=AIRE, fg=INK)
    body += etiqueta("treac", 560, 150, "REACCIÓN", size=32, bg=NARANJA, fg=INK)
    body += g("tsust", etiqueta(None, 330, 34, "SUSTENTACIÓN", size=30, bg=INK, fg=LIME)
              + T(330, 96, "LA FUERZA QUE LO SUBE", 24, "#FFFFFF", extra='stroke="#0B0B14" stroke-width="6" paint-order="stroke"'))
    nw = A.retrato_newton("newton", 820, 420, 0.62)
    body += nw
    body += g("manzana", A.manzana(None, 830, 720, 38) + flecha(None, (900, 750), (900, 680), col=LIME, w=8, punta=18))
    return svg(body, "free", h=H)


# ---------------------------------------------------------------- 3. la mano por la ventanilla (panel)
def ventanilla():
    W = 1000
    fondo = f'<rect width="{W}" height="700" fill="url(#skyDia)"/>'
    fondo += f'<path d="M 0 470 Q 250 400 520 450 Q 780 500 1000 430 L 1000 700 L 0 700 Z" fill="#8CCB9A"/>'
    fondo += f'<rect x="0" y="560" width="{W}" height="140" fill="url(#asfaltoG)" stroke="{INK}" stroke-width="6"/>'
    body = nubes_grupo("nubes", ((160, 140, 0.4), (720, 110, 0.32)))
    body += g("marcas", "".join(f'<rect x="{x}" y="636" width="110" height="14" rx="6" fill="#FFFFFF" opacity="0.9"/>' for x in range(-160, 1200, 220)))
    # gente dentro (detrás de la carrocería)
    cond = persona("cond", 500, 492, 0.52, "adulto", "clara", "corto", "canoso", "camisa", "#5B7FD6",
                   accesorios=("bigote",), expresion="risa", pose="busto", brazos=("relajado", "relajado"))
    cop = persona("cop", 640, 506, 0.56, "joven", "media", "corto", "negro", "camiseta", "#1FB5A8",
                  expresion="risa", pose="busto", brazos=("relajado", "relajado"), mira=1)
    body += cond + g("copg", cop)
    # coche rojo de perfil (morro a la derecha), con el hueco de las ventanillas
    car = ("M 120 560 L 118 470 Q 122 430 170 420 L 300 410 Q 340 330 420 318 L 640 318 Q 690 322 730 410 "
           "L 860 430 Q 900 440 902 490 L 900 560 Z")
    hueco = "M 330 412 Q 360 344 425 336 L 560 336 L 560 412 Z M 580 336 L 638 336 Q 676 340 708 412 L 580 412 Z"
    carro = f'<path d="{car} {hueco}" fill-rule="evenodd" fill="{degradado(CORAL, 0.3)}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'
    carro += f'<path d="M 580 336 L 638 336 Q 676 340 708 412 L 580 412 Z" fill="#CFEFFF" opacity="0.25"/>'
    carro += brillo("M 170 436 L 300 426 M 740 430 L 860 446", 6, 0.6)
    carro += f'<path d="M 560 420 L 560 550 M 340 420 L 340 550" stroke="{INK}" stroke-width="4" opacity="0.5"/>'
    carro += f'<rect x="470" y="440" width="40" height="10" rx="5" fill="{INK}" opacity="0.6"/><rect x="690" y="440" width="40" height="10" rx="5" fill="{INK}" opacity="0.6"/>'
    carro += f'<path d="M 882 452 Q 900 458 900 476 L 872 474 Z" fill="#FFF6C8" stroke="{INK}" stroke-width="4"/>'
    rueda = lambda x: (f'<circle cx="{x}" cy="560" r="58" fill="#2A2F3E" stroke="{INK}" stroke-width="7"/>'
                       f'<circle cx="{x}" cy="560" r="26" fill="#C9D1DE" stroke="{INK}" stroke-width="5"/>'
                       f'<path d="M {x-18} 560 L {x+18} 560 M {x} 542 L {x} 578" stroke="#7E889C" stroke-width="6"/>')
    body += g("coche", sombra(510, 620, 380, 14, 0.25) + carro + g("rueda1", rueda(260)) + g("rueda2", rueda(760)))
    body += g("velo", lineas_velocidad(95, 440, 3, 70, 34, "#FFFFFF"))
    # brazo por la ventanilla (delante de la puerta): antebrazo + mano plana
    piel_c = "#D9A07C"
    mano = (f'<ellipse cx="850" cy="372" rx="64" ry="17" fill="{piel_c}" stroke="{INK}" stroke-width="6"/>'
            f'<path d="M 800 368 L 892 364" stroke="#B9805E" stroke-width="3" opacity="0.7"/>'
            + brillo("M 812 362 L 880 360", 4, 0.6))
    brazo = f'<path d="M 596 440 Q 650 432 690 430" stroke="{INK}" stroke-width="50" stroke-linecap="round" fill="none"/>'
    brazo += f'<path d="M 596 440 Q 650 432 690 430" stroke="#1FB5A8" stroke-width="40" stroke-linecap="round" fill="none"/>'
    brazo += f'<path d="M 630 420 L 640 452 M 660 418 L 668 448" stroke="#FFFFFF" stroke-width="6" opacity="0.8"/>'
    brazo += trazo("M 700 428 Q 760 410 805 378", 32, piel_c, 7)
    body += g("brazo", brazo + g("mano", mano))
    # aire que llega a la mano y sale desviado hacia abajo
    aire = ""
    for y in (300, 336):
        d = f"M 990 {y} L 930 {y} Q 860 {y+2} 800 {y+40} L 740 {y+86}"
        aire += (f'<path d="{d}" fill="none" stroke="#FFFFFF" stroke-width="14" stroke-linecap="round" opacity="0.9"/>'
                 f'<path d="{d}" fill="none" stroke="{AIRE}" stroke-width="7" stroke-linecap="round" stroke-dasharray="30 14"/>')
    body += g("aire", aire)
    body += etiqueta("tsube", 860, 230, "¡SUBE!", size=32, bg=LIME, fg=INK)
    return svg(body, "panel", fondo=fondo)


# ---------------------------------------------------------------- 4. menos presión arriba (panel)
def presion():
    c = (500, 380)
    a = A.perfil_ala("ala", c[0], c[1], 520, 5, curva=False)
    body = ""
    rap = ""
    for i, y in enumerate((130, 178, 226)):
        rap += flecha(None, (160 + i * 30, y), (700 - i * 10, y + 8 + i * 8), col=AIRE, w=9, punta=24)
    body += g("rapido", rap)
    body += etiqueta("trap", 840, 150, "MÁS RÁPIDO", size=26, bg=AIRE, fg=INK)
    len_ = ""
    for i, x in enumerate((260, 520)):
        len_ += flecha(None, (x, 560), (x + 120, 566), col="#8FB8D8", w=9, punta=22)
    body += g("lento", len_ + etiqueta(None, 820, 566, "MÁS LENTO", size=26, bg="#8FB8D8", fg=INK))
    body += a
    menos = "".join(A.signo_presion(None, x, y, 26, "-") for x, y in ((360, 268), (560, 262)))
    body += g("menos", menos)
    mas = ""
    for i, (x, y) in enumerate(((330, 470), (430, 486), (530, 490), (630, 484), (380, 520), (580, 524))):
        mas += A.signo_presion(None, x, y, 26, "+")
    body += g("mas", mas)
    body += g("flarriba", flecha_gorda(None, (880, 470), (880, 230), ancho=70, col=NARANJA))
    body += etiqueta("tpres", 500, 628, "PRESIÓN: LO QUE APRIETA EL AIRE", size=26, bg=INK, fg=LIME)
    return svg(body, "panel", fondo=fondo_suave())


# ---------------------------------------------------------------- 5. el mito del cole (full)
def mito():
    chalk = "#F4F1E6"
    pc, pw, ph = (400, 640), 600, 310
    mini = A.perfil_ala(None, 330, 640, 300, 4, curva=False, fill="none")
    cont = mini.replace(INK, chalk)
    cont += f'<circle cx="185" cy="600" r="12" fill="#9FD8FF"/><circle cx="185" cy="676" r="12" fill="#C9D1DE"/>'
    cont += f'<path d="M 200 600 Q 330 560 470 640 M 200 676 Q 330 690 470 650" fill="none" stroke="{chalk}" stroke-width="4" stroke-dasharray="10 8"/>'
    cont += T(400, 760, "LLEGAN A LA VEZ", 34, chalk)
    body = CA.pizarra("pizarra", pc[0], pc[1], pw, ph, contenido=cont)
    body += g("tache", f'<path d="M 230 745 Q 400 728 575 740" fill="none" stroke="{CORAL}" stroke-width="12" stroke-linecap="round"/>'
              f'<path d="M 140 520 L 660 780" fill="none" stroke="{CORAL}" stroke-width="12" stroke-linecap="round"/>')
    body += sello("smito", 590, 520, "MITO", 54, -10)
    prof = persona("prof", 930, 1030, 0.8, "adulto", "clara", "corto", "castano", "chaqueta", MADERA,
                   camisa_color="#FFFFFF", accesorios=("gafas", "barba"), expresion="neutral", brazos=("explica", "relajado"))
    body += prof
    # carrera de bolitas de humo sobre un ala
    w = A.perfil_ala("ala", 450, 1150, 600, 4, curva=False)
    body += w
    ax, ay = w.puntos["ataque"]
    sx, sy = w.puntos["salida"]
    body += g("humo_az", f'<circle cx="{f(ax+10)}" cy="{f(ay-62)}" r="24" fill="{degradado_brillo("#5BB8FF")}" stroke="{INK}" stroke-width="5"/>')
    body += g("humo_gr", f'<circle cx="{f(ax+10)}" cy="{f(ay+58)}" r="24" fill="{degradado_brillo("#B9C2D0")}" stroke="{INK}" stroke-width="5"/>')
    body += bandera("meta", sx + 10, sy - 120, 90, 60, cols=("#FFFFFF", INK, "#FFFFFF"), vertical=True)
    body += etiqueta("tantes", sx - 140, sy - 230, "¡LLEGA ANTES!", size=30, bg=LIME, fg=INK)
    return svg(body, "full", fondo=A.aula())


# ---------------------------------------------------------------- 6. necesita velocidad (free)
def pista():
    H = 820
    body = ""
    body += f'<rect x="0" y="560" width="1000" height="70" fill="#7FD07A" stroke="{INK}" stroke-width="6"/>'
    body += f'<rect x="0" y="600" width="1000" height="120" fill="url(#avPista)" stroke="{INK}" stroke-width="7"/>'
    body += g("marcas", "".join(f'<rect x="{x}" y="652" width="90" height="14" rx="5" fill="#FFFFFF"/>' for x in range(-200, 1200, 180)))
    # torre de control al fondo
    body += (f'<rect x="830" y="400" width="40" height="160" fill="#C9D1DE" stroke="{INK}" stroke-width="6"/>'
             f'<path d="M 800 400 L 900 400 L 890 350 L 810 350 Z" fill="#9FDCFF" stroke="{INK}" stroke-width="6"/>'
             f'<rect x="800" y="336" width="100" height="16" fill="#5A6170" stroke="{INK}" stroke-width="5"/>')
    j = A.jumbo(None, 390, 0, 0.5)
    tren = (f'<path d="M 390 30 L 390 52 M 280 26 L 280 50" stroke="{INK}" stroke-width="8"/>'
            f'<circle cx="390" cy="58" r="12" fill="#2A2F3E" stroke="{INK}" stroke-width="4"/><circle cx="280" cy="56" r="12" fill="#2A2F3E" stroke="{INK}" stroke-width="4"/>')
    flujo = ""
    for i, x in enumerate((300, 350, 400, 450)):
        flujo += g(f"d{i}", flecha(None, (x, 108), (x - 30, 168), col=AIRE, w=8, punta=20))
    body += g("avion", f'<g transform="translate(0 540)">{j}{tren}{flujo}</g>')
    body += medidor("velo", 180, 250, 130, 0.0, texto="VELOCIDAD")
    return svg(body, "free", h=H)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for nombre, fn in (("gancho_full.svg", gancho), ("desvia.svg", desvia), ("newton_free.svg", newton),
                       ("ventanilla.svg", ventanilla), ("presion.svg", presion), ("mito_full.svg", mito),
                       ("pista_free.svg", pista)):
        guardar(OUT / nombre, fn())

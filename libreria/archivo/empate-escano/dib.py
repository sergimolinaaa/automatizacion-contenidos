"""lote10-02-empate-escano: dibujos del vídeo «Empate a votos: ¿quién gana el escaño?» (método rossark).

Ejemplo inventado con partidos ficticios (ESTRELLA 9.000 votos, CÍRCULO 6.000, 3 escaños): cocientes 9.000, 6.000 y
4.500 ganan; el cuarto cociente empata a 3.000 (ESTRELLA ÷3 y CÍRCULO ÷2) y lo gana ESTRELLA por tener más votos en total
(LOREG art. 163.1 d). Lújar (Granada, 2011) sin nombres ni colores de partidos.
Cada parte en su grupo con pivote; las pilas crecen desde la base hoja a hoja; los números cuentan con capas que se relevan;
la balanza se inclina en 4 pasos (sin saltos); el bombo se frena con un move rotate (spring), no con un corte.
"""
import sys, os, math
sys.path.insert(0, "/home/user/automatizacion-contenidos")
from libreria.svg.base import *
from libreria.svg.objetos import politica as P, territorio as TE, coches as CO

OUT = "/home/user/automatizacion-contenidos/content/lote10-02-empate-escano"
os.makedirs(OUT, exist_ok=True)
AMA, TUR = P.COLOR["star"], P.COLOR["circle"]
GR = "#C9CED8"
VST = f'stroke="{INK}" stroke-width="8" paint-order="stroke"'


def pila(id_, cx, base, forma, n=8, w=230, hh=14, seed=0):
    """Montón de papeletas visto de lado: hojas `{id}_s<k>` (de abajo arriba) para que crezca hoja a hoja + ficha delante."""
    o = sombra(cx, base + 4, w * 0.6, 10, 0.25)
    for k in range(n):
        dx = math.sin(k * 2.3 + seed) * 9
        y = base - (k + 1) * hh
        o += g(f"{id_}_s{k}", f'<rect x="{f(cx-w/2+dx)}" y="{f(y)}" width="{f(w)}" height="{f(hh+2)}" rx="4" fill="url(#paperB)" stroke="{INK}" stroke-width="4"/>'
               + f'<path d="M {f(cx-w/2+dx+10)} {f(y+hh*0.55)} L {f(cx-w*0.1+dx)} {f(y+hh*0.55)}" stroke="#C9CED8" stroke-width="3" stroke-linecap="round"/>')
    o += g(f"{id_}_chip", f'<circle cx="{f(cx)}" cy="{f(base+44)}" r="34" fill="#FFFFFF" stroke="{INK}" stroke-width="6"/>'
           + P.icono_partido(forma, cx, base + 44, 22, sw=4))
    return g(id_, o)


def ficha(id_, cx, cy, forma, r=30):
    """Ficha redonda del color del partido (la que «vuela» a un escaño)."""
    col = P.COLOR[forma]
    return g(id_, f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{degradado(col, 0.25)}" stroke="{INK}" stroke-width="6"/>'
             + P.icono_partido(forma, cx, cy, r * 0.5, col="#FFFFFF", sw=3)
             + f'<circle cx="{f(cx-r*0.35)}" cy="{f(cy-r*0.4)}" r="{f(r*0.18)}" fill="#FFFFFF" opacity="0.7"/>')


def asiento(cx, cy, r=34, col=GR):
    return (f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{col}" stroke="{INK}" stroke-width="6"/>'
            f'<circle cx="{f(cx-r*0.3)}" cy="{f(cy-r*0.35)}" r="{f(r*0.26)}" fill="#FFFFFF" opacity="0.6"/>')


def cuenta(prefijo, valores, fn):
    """Capas que se relevan para que un número «cuente»: prefijo_0, prefijo_1… y la última = prefijo."""
    return "".join(g(prefijo if i == len(valores) - 1 else f"{prefijo}_{i}", fn(v)) for i, v in enumerate(valores))


# ---------------------------------------------------------------- 0. gancho (full)
def gancho():
    body = ""
    hemi = P.hemiciclo("hemi", 540, 650, 25, 3, 80, 165, GR, r_esc=13)
    esc_i = max(range(25), key=lambda i: -hemi.puntos["escanos"][i][1])
    ex, ey = hemi.puntos["escanos"][esc_i]
    body += hemi
    body += onda_expansiva("onda", ex, ey, 30)
    body += g("esc", f'<circle cx="{f(ex)}" cy="{f(ey)}" r="21" fill="#FFFFFF" stroke="{INK}" stroke-width="6"/>')
    body += icono_duda("duda", 800, 500, 48)
    body += P.mesa_electoral("mesa", 540, 1070, w=880, alto=190, cartel="MESA A", urna_=False)
    body += pila("pilaE", 320, 1056, "star", seed=0) + pila("pilaC", 760, 1056, "circle", seed=1.3)
    # marcador que cuenta hasta 161 · 161 (capas marc_0, marc_1 y marc)
    for i, v in enumerate(("54", "108", "161")):
        body += marcador("marc" if i == 2 else f"marc_{i}", 540, 800, v, v, col_izq=AMA, col_der=TUR,
                         txt_izq="ESTRELLA", txt_der="CÍRCULO", w=560, h=160)
    guardar(f"{OUT}/gancho_full.svg", svg(body, "full", fondo=P.colegio_electoral(suelo_y=1180, rotulo=None)))
    return ex, ey


# ---------------------------------------------------------------- 1. sin posicionarnos + ley + D'Hondt (panel)
def ley():
    body = P.documento("doc", 250, 390, 300, 380, "BOE", "LOREG", rot_=-4)
    body += etiqueta("tley", 250, 625, "LEY ORGÁNICA 5/1985", bg=INK, fg=LIME, size=24)
    reparto = ["#FFC83D"] * 11 + ["#2EC4B6"] * 10
    h = P.hemiciclo("hemi", 720, 470, 21, 3, 90, 210, GR, r_esc=17)
    body += h
    pos = h.puntos["escanos"]
    capas = ["", "", ""]  # se llenan de izquierda a derecha en 3 tandas
    for i, (x, y) in enumerate(pos):
        capas[min(2, i * 3 // len(pos))] += (f'<circle cx="{f(x)}" cy="{f(y)}" r="17" fill="{degradado(reparto[i], 0.2)}" stroke="{INK}" stroke-width="4"/>'
                                             f'<circle cx="{f(x-5)}" cy="{f(y-6)}" r="5" fill="#FFFFFF" opacity="0.6"/>')
    body += "".join(g(f"eg{k}", c) for k, c in enumerate(capas))
    body += etiqueta("tdh", 720, 560, "D'HONDT: EL REPARTO DE ESCAÑOS", bg=LIME, fg=INK, size=24)
    body += P.sin_posicionarnos("sello", 610, 112, 38)
    body += g("chisp", chispa(None, 905, 250, 26, LIME) + chispa(None, 455, 250, 20, LIME))
    guardar(f"{OUT}/ley.svg", svg(body, "panel"))


# ---------------------------------------------------------------- 2. tabla D'Hondt (free)
def tabla():
    H = 820
    filas = [("star", "ESTRELLA", 9000), ("circle", "CÍRCULO", 6000)]
    aros = [(0, 0), (1, 0), (0, 1)]
    t = P.tabla_dhondt("tab", 40, 110, filas, (1, 2, 3), cw=178, ch=120, lw=300, gap=16, size=36, aros=aros)
    body = etiqueta("tinv", 500, 50, "EJEMPLO INVENTADO · 3 ESCAÑOS", bg=CORAL, fg="#FFFFFF", size=28)
    body += t
    # 3 escaños en arco; fichas que vuelan desde su casilla
    seats = [(330, 680), (500, 630), (670, 680)]
    body += g("arco", f'<path d="M 230 730 A 270 190 0 0 1 770 730 Z" fill="{degradado("#D2453B", 0.15)}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
              + "".join(asiento(x, y, 36) for x, y in seats))
    order = [((0, 0), "star"), ((1, 0), "circle"), ((0, 1), "star")]
    destinos = {}
    for k, ((i, j), forma) in enumerate(order):
        cx, cy = t.puntos[f"c{i}_{j}"]
        body += ficha(f"f{k}", cx, cy - 2, forma, 34)
        sx, sy = seats[k]
        destinos[f"f{k}"] = (round(sx - cx), round(sy - cy + 2))
    body += etiqueta("tgana", 500, 785, "LOS 3 COCIENTES MÁS ALTOS", bg=INK, fg=LIME, size=26)
    guardar(f"{OUT}/tabla_free.svg", svg(body, "free", h=H))
    return destinos


# ---------------------------------------------------------------- 3. cocientes iguales: gana el más votado (panel)
def balanza():
    body = ""
    for k, (forma, nom, x) in enumerate((("star", "ESTRELLA ÷3", 300), ("circle", "CÍRCULO ÷2", 700))):
        c = (sombra_caja(x - 150, 78, 300, 118, 16, 6, 8, 0.25)
             + f'<rect x="{x-150}" y="78" width="300" height="118" rx="16" fill="url(#paperB)" stroke="{INK}" stroke-width="7"/>'
             + P.icono_partido(forma, x - 105, 112, 16, sw=3)
             + T(x - 82, 121, nom, 24, INK, anchor="start")
             + T(x, 178, "3.000", 50, INK, font=DISP))
        body += g(f"cas{k}", c)
    body += g("igual", T(500, 165, "=", 80, CORAL, font=DISP, extra=VST))
    # 4 balanzas: 0 → −5 → −10 → −14 (el platillo de ESTRELLA baja sin saltos)
    chipE = P.icono_partido("star", 0, -34, 30, sw=5)
    chipC = P.icono_partido("circle", 0, -34, 30, sw=5)
    for k, inc in enumerate((0, -5, -10, -14)):
        body += TE.balanza(f"bal{k}", 500, 640, 560, inc, izq=chipE, der=chipC, txt_izq="9.000", txt_der="6.000", h=330)
    body += etiqueta("ttot", 175, 620, "VOTOS EN TOTAL", bg=INK, fg=LIME, size=22)
    body += icono_ok("ok", 85, 420, 44)
    body += etiqueta("tart", 830, 620, "ART. 163.1 D)", bg=LIME, fg=INK, size=26)
    guardar(f"{OUT}/balanza.svg", svg(body, "panel"))


# ---------------------------------------------------------------- 4. empate total: sorteo y luego por turnos (full)
CITA = ("el primer empate se resolverá por sorteo", "y los sucesivos de forma alternativa")


def sorteo():
    body = ""
    # tarjeta con el texto literal del art. 163.1 d) LOREG (sin cambiar ni una palabra)
    card = tarjeta(None, 540, 560, 960, 230, fill="url(#paperB)", acento=LIME, rot_=-1.5,
                   body=T(540, 535, f"«{CITA[0]}", 37, INK) + T(540, 590, f"{CITA[1]}»", 37, INK)
                   + T(540, 642, "LOREG, ART. 163.1 D)", 24, "#5A6478"))
    body += g("cita", card)
    b = P.bombo("bombo", 300, 900, 150, texto="SORTEO", bola_txt="1.º")
    body += b
    bx, by = b.puntos["boca"]
    body += marcador("marc", 790, 768, "6.000", "6.000", col_izq=AMA, col_der=TUR, txt_izq="ESTRELLA", txt_der="CÍRCULO", w=540, h=120)
    seats = [(660, 1010), (790, 1010), (920, 1010)]
    body += g("filas", f'<rect x="590" y="1050" width="400" height="34" rx="12" fill="{degradado("#D2453B", 0.15)}" stroke="{INK}" stroke-width="6"/>'
              + "".join(asiento(x, y, 44) for x, y in seats))
    for k, ((x, y), forma) in enumerate(zip(seats, ("star", "circle", "star"))):
        body += ficha(f"t{k}", x, y, forma, 44)
    body += CO.flecha_giro("giro", 790, 1010, 175, 200, 340, col=LIME, w=12)
    body += etiqueta("tturno", 790, 1150, "POR TURNOS", bg=INK, fg=LIME, size=30)
    body += etiqueta("tsort", 300, 1170, "1.ER EMPATE: SORTEO", bg=CORAL, fg="#FFFFFF", size=28)
    guardar(f"{OUT}/sorteo_full.svg", svg(body, "full", fondo=P.colegio_electoral(suelo_y=1200, rotulo=None)))
    return bx, by


# ---------------------------------------------------------------- 5. Lújar, 2011 (panel)
def lujar():
    m = TE.mapa_espana("mapa", 265, 320, 400, puntos=False, destacar=("Granada",), canarias=False)
    gx, gy = m.puntos["Granada"]
    body = m
    body += onda_expansiva("onda", gx, gy, 26, col=CORAL)
    body += g("pueblo_g", TE.pueblo("pueblo", gx + 70, gy + 140, 180))
    body += etiqueta("tluj", gx + 70, gy + 180, "LÚJAR, GRANADA", bg=INK, fg=LIME, size=24)
    body += etiqueta("t2011", 420, 110, "2011", bg=CORAL, fg="#FFFFFF", size=34)
    # marcador gris (sin colores de partido) que cuenta hasta 161 · 161
    for i, v in enumerate(("54", "108", "161")):
        id_ = "marc" if i == 2 else f"marc_{i}"
        body += marcador(id_, 740, 175, v, v, col_izq="#E7EBF3", col_der="#E7EBF3", txt_izq="CANDIDATURA A", txt_der="CANDIDATURA B", w=440, h=140)
    body += etiqueta("tvot", 740, 280, "VOTOS", bg="#FFFFFF", fg=INK, size=24)
    b = P.bombo("bombo", 620, 470, 85, n_bolas=7, texto=None, bola_txt="1")
    body += b
    body += P.baston_mando("baston", 850, 470, 300, rot_=-24)
    body += destellos("dest", 850, 400, 110)
    body += etiqueta("talc", 780, 640, "ALCALDÍA POR SORTEO", bg=CORAL, fg="#FFFFFF", size=26)
    guardar(f"{OUT}/lujar.svg", svg(body, "panel"))
    return gx, gy


# ---------------------------------------------------------------- 6. un voto evita el sorteo (free, con la mascota)
def unvoto():
    H = 720
    u = P.urna("urna", 300, 640, 340, 360, texto="URNA")
    rx, ry = u.puntos["ranura"]
    body = u
    body += P.sobre(rx, ry - 150, 160, 106, -6, id_="sobre")
    b = P.bombo("bombo", 740, 380, 140, texto="SORTEO", bola_txt="1")
    body += b
    body += g("tache", f'<path d="M 600 220 L 880 560" stroke="{INK}" stroke-width="30" stroke-linecap="round"/>'
              f'<path d="M 600 220 L 880 560" stroke="{CORAL}" stroke-width="18" stroke-linecap="round"/>')
    body += etiqueta("tstc", 500, 40, "TRIBUNAL CONSTITUCIONAL · STC 125/2011", bg=LIME, fg=INK, size=24)
    body += etiqueta("tun", 300, 690, "+1 VOTO", bg=INK, fg=LIME, size=30)
    guardar(f"{OUT}/unvoto_free.svg", svg(body, "free", h=H))
    return rx, ry


if __name__ == "__main__":
    print("escaño gancho", gancho())
    ley()
    print("destinos", tabla())
    balanza()
    print("boca", sorteo())
    print("granada", lujar())
    print("ranura", unvoto())

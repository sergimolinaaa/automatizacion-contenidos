"""SVG de content/lote7-06-puerta-olvido (¿Por qué entras en una habitación y olvidas a qué ibas?).
Uso: python3 libreria/archivo/puerta-olvido/dib.py"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from libreria.svg.base import *  # noqa
from libreria.svg.personajes import persona
from libreria.svg.objetos import casa as K, escenarios as E, memoria as M, cuerpo as C

OUT = ROOT / "content" / "lote7-06-puerta-olvido"
BATA = "#F28DB2"
MUJER = dict(edad="adulto", piel="clara", pelo="mono", pelo_color="#8A6A55", ropa="abrigo", ropa_color=BATA,
             pantalon_color="#C76A93", zapato_color="#FFB3CF", accesorios=("pendientes",))
CHICA = dict(edad="joven", piel="media", pelo="coleta", pelo_color="negro", ropa="camiseta", ropa_color=TEAL,
             pantalon_color="#3E6DB5", zapato_color="#FFFFFF")


def pared_suelo(x0, x1, suelo, H, pared="#EAF0FA", rayas=True):
    o = f'<rect x="{f(x0)}" y="0" width="{f(x1-x0)}" height="{f(suelo)}" fill="{degradado(pared, 0.06)}"/>'
    if rayas:
        o += f'<g stroke="{shade(pared,-0.06)}" stroke-width="8" opacity="0.7">' + "".join(
            f'<line x1="{x}" y1="0" x2="{x}" y2="{f(suelo)}"/>' for x in range(int(x0) + 40, int(x1), 90)) + "</g>"
    o += f'<rect x="{f(x0)}" y="{f(suelo-22)}" width="{f(x1-x0)}" height="22" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/>'
    o += f'<rect x="{f(x0)}" y="{f(suelo)}" width="{f(x1-x0)}" height="{f(H-suelo)}" fill="url(#maderaG)"/>'
    o += f'<path d="M {f(x0)} {f(suelo)} L {f(x1)} {f(suelo)}" stroke="{INK}" stroke-width="6"/>'
    o += '<g fill="none" stroke="#7A4E2A" stroke-width="3" opacity="0.4">' + "".join(
        f'<path d="M {f(x0)} {f(y)} L {f(x1)} {f(y)}"/>' for y in (suelo + 25, suelo + 55, suelo + 90)) + "</g>"
    return o


def azulejos(x0, x1, y0, y1, col="#EAF4FB", paso=60):
    o = f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(x1-x0)}" height="{f(y1-y0)}" fill="{degradado(col, 0.06)}"/>'
    o += f'<g stroke="{shade(col,-0.1)}" stroke-width="3">' + "".join(
        f'<line x1="{x}" y1="{f(y0)}" x2="{x}" y2="{f(y1)}"/>' for x in range(int(x0) + paso, int(x1), paso)) + "".join(
        f'<line x1="{f(x0)}" y1="{y}" x2="{f(x1)}" y2="{y}"/>' for y in range(int(y0) + paso, int(y1), paso)) + "</g>"
    return o


def encimera(x0, x1, top, base, col="#FFFFFF"):
    o = sombra_caja(x0, top, x1 - x0, base - top, 6, 8, 6, 0.2)
    o += f'<rect x="{f(x0)}" y="{f(top)}" width="{f(x1-x0)}" height="{f(base-top)}" rx="6" fill="{degradado(col, 0.1)}" stroke="{INK}" stroke-width="6"/>'
    o += f'<rect x="{f(x0-10)}" y="{f(top-18)}" width="{f(x1-x0+20)}" height="22" rx="6" fill="url(#maderaG)" stroke="{INK}" stroke-width="6"/>'
    n = max(1, int((x1 - x0) // 120))
    for i in range(n):
        xa = x0 + 12 + i * (x1 - x0 - 24) / n
        wa = (x1 - x0 - 24) / n - 12
        o += f'<rect x="{f(xa)}" y="{f(top+16)}" width="{f(wa)}" height="{f(base-top-30)}" rx="6" fill="none" stroke="{INK}" stroke-width="4"/>'
        o += f'<rect x="{f(xa+wa/2-18)}" y="{f(top+30)}" width="36" height="9" rx="4" fill="#9AA3B5" stroke="{INK}" stroke-width="3"/>'
    return o


def olla(cx, base, w=120):
    h = w * 0.62
    o = f'<rect x="{f(cx-w/2)}" y="{f(base-h)}" width="{f(w)}" height="{f(h)}" rx="12" fill="url(#coralG)" stroke="{INK}" stroke-width="6"/>'
    o += f'<rect x="{f(cx-w/2-8)}" y="{f(base-h-14)}" width="{f(w+16)}" height="18" rx="8" fill="{shade(CORAL,-0.2)}" stroke="{INK}" stroke-width="5"/>'
    o += f'<rect x="{f(cx-12)}" y="{f(base-h-30)}" width="24" height="18" rx="6" fill="#3A2A1C" stroke="{INK}" stroke-width="4"/>'
    o += "".join(f'<rect x="{f(cx+k*(w/2+4)-(14 if k<0 else 0))}" y="{f(base-h+14)}" width="14" height="12" rx="4" fill="{INK}"/>' for k in (-1, 1))
    o += brillo(f"M {f(cx-w/2+12)} {f(base-h+16)} L {f(cx-w/2+12)} {f(base-14)}", 5, 0.8)
    return o


# ---------------------------------------------------------------- 0. gancho (full, cocina)
def gancho():
    fondo = E.cocina(encimera_y=1250)
    fondo += encimera(760, 1080, 1010, 1250)
    fondo += olla(900, 992, 130)
    fondo += K.taza(None, 1010, 992, 90)
    fondo += encimera(-10, 200, 1010, 1250)
    fondo += K.botella(None, 90, 992, 170, "#7FD48A", CORAL, "")
    d = M.puerta("puerta", 540, 1250, 330, 640)
    body = d
    n = persona("mujer_n", 560, 1262, 1.12, expresion="neutral", brazos=("relajado", "explica"), **MUJER)
    du = persona("mujer_d", 560, 1262, 1.12, expresion="duda", brazos=("relajado", "barbilla"), mira=1, **MUJER)
    body += n + du
    hx, hy = n.puntos["cabeza"]
    tij = M.tijeras(None, 830, 600, 0.9, -25)
    body += M.bocadillo_piensa("piensa", 830, 600, 300, 210, tij, cola=(hx + 70, hy - 40))
    body += M.humo("humo", 830, 610, 1.2)
    body += icono_duda("duda", 800, 560, 95)
    return svg(body, "full", fondo=fondo)


# ---------------------------------------------------------------- 1. Radvansky (panel)
def radvansky():
    fondo = fondo_suave()
    fondo += f'<rect x="0" y="600" width="1000" height="100" fill="#CFD9E8"/><path d="M 0 600 L 1000 600" stroke="{INK}" stroke-width="5"/>'
    body = M.edificio_cupula("uni", 800, 600, 320)
    body += etiqueta("tuni", 800, 638, "NOTRE DAME, EE. UU.", size=24)
    body += M.puerta("puerta", 190, 620, 210, 430, placa="EFECTO PUERTA")
    p = persona("psico", 480, 650, 0.86, edad="adulto", piel="clara", pelo="corto", pelo_color="canoso", ropa="jersey",
                ropa_color="#3F7F5F", pantalon_color="#4A4F63", accesorios=("gafas", "barba"), brazos=("relajado", "sujeta"),
                mira=-1)
    body += p
    mx, my = p.puntos["mano_der"]
    body += g("cuaderno", K.portapapeles(None, mx + 14, my + 30, 90, 120, filas=3, marcadas=(0, 1)))
    body += etiqueta("tpsico", 600, 108, "PSICÓLOGO: ESTUDIA CÓMO PIENSAS", apunta=(p.puntos["cabeza"][0] + 30, p.puntos["cabeza"][1] - 60),
                     desde=(560, 108), size=22)
    return svg(body, "panel", fondo=fondo)


# ---------------------------------------------------------------- 2. experimento: sala real y videojuego (panel)
def experimento():
    fondo = pared_suelo(0, 500, 560, 700)
    fondo += M.sala_pixel(500, 0, 500, 700)
    body = K.mesa("mesa1", 110, 470, 170, 120)
    body += K.mesa("mesa2", 390, 470, 170, 120)
    ch = persona("chica", 250, 655, 0.7, brazos=("coge", "relajado"), **CHICA)
    body += ch
    body += M.caja_colores("caja", 110, 405, 100, 74)
    body += etiqueta("treal", 250, 110, "SALAS REALES", size=28)
    # mitad derecha: videojuego
    virt = M.bloque_pixel(615, 520, 150, 70, "#C98B55") + M.bloque_pixel(885, 520, 150, 70, "#C98B55")
    virt += M.avatar_pixel(None, 750, 620, 12)
    body += g("virtual", virt)
    body += g("cajapix", M.bloque_pixel(615, 450, 70, 56, CORAL, 14) + M.bloque_pixel(615, 418, 70, 14, LIME, 14))
    body += M.mando_consola("mando", 750, 300, 0.85)
    body += g("apagada", f'<rect x="500" y="0" width="500" height="700" fill="#151926"/>'
              + f'<rect x="520" y="300" width="460" height="6" fill="#FFFFFF" opacity="0.25"/>')
    body += etiqueta("tvirt", 750, 110, "VIDEOJUEGO", size=28)
    body += f'<path d="M 500 0 L 500 700" stroke="{INK}" stroke-width="10"/>'
    return svg(body, "panel", fondo=fondo)


# ---------------------------------------------------------------- 3. comparativa (free)
def comparativa():
    body = ""
    for y0, y1 in ((80, 380), (480, 780)):
        body += sombra_caja(40, y0, 680, y1 - y0, 18, 10, 12, 0.3)
        body += f'<rect x="40" y="{y0}" width="680" height="{y1-y0}" rx="18" fill="#EAF0FA" stroke="{INK}" stroke-width="7"/>'
        body += f'<rect x="44" y="{y1-70}" width="672" height="66" fill="url(#maderaG)"/><path d="M 44 {y1-70} L 716 {y1-70}" stroke="{INK}" stroke-width="5"/>'
    body += M.puerta("puerta", 380, 310, 110, 190, marco=16)
    body += persona("chica1", 110, 330, 0.36, brazos=("coge", "relajado"), **CHICA)
    body += persona("chica2", 110, 730, 0.36, brazos=("coge", "relajado"), **CHICA)
    body += M.bocadillo_piensa("nube1", 600, 150, 190, 130, M.caja_colores(None, 600, 150, 70, 52, borrosa=True)
                               + T(650, 140, "?", 48, CORAL, font=DISP), cola=(590, 230))
    body += M.bocadillo_piensa("nube2", 600, 550, 190, 130, M.caja_colores(None, 600, 552, 70, 52), cola=(590, 630))
    regla = trazo("M 120 740 L 600 740", 16, YEL, 6) + "".join(
        f'<path d="M {x} 734 L {x} 746" stroke="{INK}" stroke-width="3"/>' for x in range(140, 600, 40))
    body += g("regla", regla)
    body += etiqueta("tregla", 360, 800, "MISMA DISTANCIA", size=26)
    body += etiqueta("t1", 175, 50, "CON PUERTA", size=26)
    body += etiqueta("t2", 190, 450, "UNA SOLA SALA", size=26)
    body += g("lolvido", T(865, 50, "OLVIDO", 30, "#FFFFFF", font=DISP))
    body += barra("barra_roja", 820, 380, 90, 250, CORAL)
    body += barra("barra_verde", 820, 780, 90, 80, VERDE)
    body += f'<path d="M 790 380 L 940 380 M 790 780 L 940 780" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>'
    return svg(body, "free", h=860)


# ---------------------------------------------------------------- 4. capítulos (full)
def f_salon(cx, cy, w, h):
    o = f'<rect x="{f(cx-w/2)}" y="{f(cy-h/2)}" width="{f(w)}" height="{f(h)}" fill="#EAF0FA"/>'
    o += f'<rect x="{f(cx-w/2)}" y="{f(cy+h*0.22)}" width="{f(w)}" height="{f(h*0.3)}" fill="url(#maderaG)"/>'
    o += K.sofa(None, cx + 10, cy + h * 0.34, w * 0.62, 40, "#5B7FD6", 56)
    o += trazo(f"M {f(cx-w*0.38)} {f(cy+h*0.34)} L {f(cx-w*0.38)} {f(cy-h*0.18)}", 5, "#5A3A22", 4)
    o += f'<path d="M {f(cx-w*0.44)} {f(cy-h*0.16)} L {f(cx-w*0.32)} {f(cy-h*0.16)} L {f(cx-w*0.35)} {f(cy-h*0.32)} L {f(cx-w*0.41)} {f(cy-h*0.32)} Z" fill="{YEL}" stroke="{INK}" stroke-width="4"/>'
    return o + _rotulo(cx, cy, w, h, "SALÓN")


def f_pasillo(cx, cy, w, h):
    x0, y0, x1, y1 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
    o = f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" fill="#D7E2F2"/>'
    ix0, iy0, ix1, iy1 = cx - w * 0.16, cy - h * 0.26, cx + w * 0.16, cy + h * 0.2
    o += f'<path d="M {f(x0)} {f(y0)} L {f(ix0)} {f(iy0)} L {f(ix0)} {f(iy1)} L {f(x0)} {f(y1)} Z" fill="#C5D3E8" stroke="{INK}" stroke-width="3"/>'
    o += f'<path d="M {f(x1)} {f(y0)} L {f(ix1)} {f(iy0)} L {f(ix1)} {f(iy1)} L {f(x1)} {f(y1)} Z" fill="#C5D3E8" stroke="{INK}" stroke-width="3"/>'
    o += f'<path d="M {f(x0)} {f(y1)} L {f(ix0)} {f(iy1)} L {f(ix1)} {f(iy1)} L {f(x1)} {f(y1)} Z" fill="url(#maderaG)" stroke="{INK}" stroke-width="3"/>'
    o += f'<path d="M {f(cx-w*0.24)} {f(y1)} L {f(cx-w*0.07)} {f(iy1)} L {f(cx+w*0.07)} {f(iy1)} L {f(cx+w*0.24)} {f(y1)} Z" fill="{CORAL}" opacity="0.8"/>'
    o += f'<rect x="{f(cx-w*0.07)}" y="{f(iy0+h*0.08)}" width="{f(w*0.14)}" height="{f(iy1-iy0-h*0.08)}" fill="url(#puertaG)" stroke="{INK}" stroke-width="3"/>'
    for k in (-1, 1):
        o += f'<path d="M {f(cx+k*w*0.3)} {f(cy-h*0.22)} L {f(cx+k*w*0.22)} {f(cy-h*0.18)} L {f(cx+k*w*0.22)} {f(cy+h*0.16)} L {f(cx+k*w*0.3)} {f(cy+h*0.24)} Z" fill="url(#puertaHoja)" stroke="{INK}" stroke-width="3"/>'
    return o + _rotulo(cx, cy, w, h, "PASILLO")


def f_cocina(cx, cy, w, h):
    o = azulejos(cx - w / 2, cx + w / 2, cy - h / 2, cy + h / 2, paso=36)
    o += encimera(cx - w * 0.46, cx + w * 0.12, cy + h * 0.04, cy + h * 0.5)
    o += olla(cx - w * 0.2, cy - h * 0.02 + 6, 60)
    fx = cx + w * 0.3
    o += f'<rect x="{f(fx-w*0.14)}" y="{f(cy-h*0.36)}" width="{f(w*0.28)}" height="{f(h*0.86)}" rx="10" fill="{degradado("#E9EDF5", 0.1, "h")}" stroke="{INK}" stroke-width="5"/>'
    o += f'<path d="M {f(fx-w*0.14)} {f(cy-h*0.06)} L {f(fx+w*0.14)} {f(cy-h*0.06)}" stroke="{INK}" stroke-width="4"/>'
    o += f'<rect x="{f(fx-w*0.1)}" y="{f(cy-h*0.28)}" width="8" height="34" rx="4" fill="#9AA3B5" stroke="{INK}" stroke-width="2"/>'
    return o + _rotulo(cx, cy, w, h, "COCINA")


def _rotulo(cx, cy, w, h, t):
    yy = cy + h / 2 - 30
    tw = len(t) * 26 * 0.68 + 30
    return (f'<rect x="{f(cx-tw/2)}" y="{f(yy-20)}" width="{f(tw)}" height="40" rx="10" fill="{INK}"/>'
            + T(cx, yy + 9, t, 26, "#FFFFFF"))


def capitulos():
    registrar_defs(rg("cineR", [(0, "#33478A"), (1, "#121A38")], 0.5, 0.45, 0.75))
    fondo = '<rect width="1080" height="1920" fill="url(#cineR)"/>'
    fondo += '<g fill="#FFFFFF" opacity="0.18">' + "".join(
        f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x, y, r in ((120, 520, 6), (960, 480, 8), (880, 1100, 5), (160, 1150, 7), (300, 460, 4), (760, 560, 5))) + "</g>"
    body = M.tele_antigua("tele", 540, 1250, 300, "FIN DEL CAPÍTULO", patas=False)
    body += C.cerebro("cerebro", 540, 520, 0.55, hipotalamo=False, tronco=False)
    tira = M.tira_pelicula("tira", 30, 790, [f_salon, f_pasillo, f_cocina], fw=300, fh=230, sep=30)
    body += tira
    xc = tira.puntos["corte2"]
    body += M.puerta("puerta", xc, 920, 70, 250, estado="ambas", marco=12)
    return svg(body, "full", fondo=fondo)


# ---------------------------------------------------------------- 5. archivada en el salón (panel)
def archivo():
    fondo = pared_suelo(0, 470, 600, 700)
    fondo += azulejos(560, 1000, 0, 600)
    fondo += f'<rect x="560" y="600" width="440" height="100" fill="url(#maderaG)"/><path d="M 560 600 L 1000 600" stroke="{INK}" stroke-width="6"/>'
    fondo += f'<rect x="470" y="0" width="90" height="700" fill="#D7E2F2"/>'
    fondo += encimera(860, 1010, 440, 600)
    fondo += olla(930, 422, 90)
    body = K.sofa("sofa", 175, 615, 270, 110, "#5B7FD6", 150)
    a = M.archivador("arch", 385, 615, 150, 200)
    body += a
    body += M.puerta("puerta", 515, 600, 100, 330, marco=18)
    wa = persona("mujer_a", 250, 650, 0.68, expresion="neutral", brazos=("relajado", "apunta_arriba"), **MUJER)
    body += wa
    hx, hy = wa.puntos["cabeza"]
    wb = persona("mujer_b", 760, 650, 0.68, expresion="duda", brazos=("sujeta", "relajado"), mira=-1, **MUJER)
    mx, my = wb.puntos["mano_izq"]
    cx_, cy_ = a.puntos["carpeta"]
    body += g("cuerda", trazo(f"M {f(cx_+30)} {f(cy_)} Q {f((cx_+mx)/2)} {f(max(cy_, my)+60)} {f(mx)} {f(my)}", 6, "#E3B04B", 4))
    body += wb
    bx, by = wb.puntos["cabeza"]
    body += M.gota_esfuerzo("gota", bx + 62, by - 40, 1.0)
    body += M.bocadillo_piensa("idea", 300, 175, 200, 140, M.tijeras(None, 300, 175, 0.6, -25), cola=(hx + 40, hy - 50))
    return svg(body, "panel", fondo=fondo), (cx_, cy_)


# ---------------------------------------------------------------- 6. no es la edad (free)
def edad():
    body = M.puerta("puerta", 500, 760, 260, 500)
    kw = dict(edad="joven", brazos=("relajado", "explica"))
    est = [("est1", 270, dict(piel="oscura", pelo="rizado", pelo_color="negro", ropa="jersey", ropa_color=YEL)),
           ("est2", 500, dict(piel="clara", pelo="largo", pelo_color="rubio", ropa="camiseta", ropa_color=CORAL)),
           ("est3", 730, dict(piel="morena", pelo="corto", pelo_color="castano", ropa="chaqueta", ropa_color=VIOLETA))]
    birr = ""
    for i, (id_, x, extra) in enumerate(est):
        p = persona(id_, x, 790, 0.72, mira=(-1, 0, 1)[i], **kw, **extra)
        body += p
        cx, cy = p.puntos["cima"]
        birr += M.birrete(f"bir{i+1}", cx, cy + 38, 0.62)
    body += birr
    card = tarjeta(None, 200, 110, 260, 120, acento=GRIS, rot_=-4,
                   body=T(200, 126, "¿EDAD?", 44, INK, font=DISP))
    body += g("tedad", card)
    body += aspa("aspa", 200, 110, 80)
    body += etiqueta("tuni", 690, 110, "ESTUDIANTES UNIVERSITARIOS", size=24)
    return svg(body, "free", h=840)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    guardar(OUT / "gancho_full.svg", gancho())
    guardar(OUT / "radvansky.svg", radvansky())
    guardar(OUT / "experimento.svg", experimento())
    guardar(OUT / "comparativa_free.svg", comparativa())
    guardar(OUT / "capitulos_full.svg", capitulos())
    doc, _ = archivo()
    guardar(OUT / "archivo.svg", doc)
    guardar(OUT / "edad_free.svg", edad())

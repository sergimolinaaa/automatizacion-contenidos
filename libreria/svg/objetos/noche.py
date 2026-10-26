"""Noche, miedo y Halloween: ojo realista, iconos de los sentidos, interruptor con dedo, perchero con abrigo y su sombra
de monstruo, sabana nocturna con acacia, hoguera, leona agazapada, cabeza de león, mapa de África, fases de la luna,
bandera de Canadá, calabaza y fantasma de sábana.

Sale de: lote9-06-miedo-oscuridad (¿por qué da miedo la oscuridad?).
Método rossark: cada parte que se mueve es su propio grupo (llamas, cola, ojos, copa, tecla) para animarla sobre su pivote.
"""
import math
import random
from ..base import (INK, LIME, CORAL, YEL, f, g, T, DISP, MONO, shade, trazo, sombra, brillo, lg, rg, registrar_defs,
                    degradado, Pieza, poly, smooth)
from . import escenarios as E
from . import tiempo as _TM  # noqa: F401  (registra lunaG y lunaHalo)

registrar_defs(
    rg("ojoBlanco", [(0, "#FFFFFF"), (0.7, "#F4F1EC"), (1, "#D9D2CC")], 0.5, 0.45, 0.6)
    + rg("fuegoGlow", [(0, "#FFD27A", 0.85), (0.45, "#FF8A2A", 0.35), (1, "#FF5A36", 0)])
    + lg("llamaG", [(0, "#FFE36B"), (0.55, "#FF9A1C"), (1, "#FF5A36")])
    + lg("llamaIn", [(0, "#FFFFFF"), (1, "#FFE36B")])
    + rg("ojoFiera", [(0, "#FFF8B0", 0.95), (0.5, "#FFD23A", 0.45), (1, "#FFD23A", 0)])
    + lg("sabanaSuelo", [(0, "#3B3A2A"), (1, "#1C1D1A")])
    + lg("calabazaG", [(0, "#FFB24A"), (0.6, "#FF7A1C"), (1, "#D45410")], 0, 0, 1, 1)
    + rg("calabazaLuz", [(0, "#FFFBD0"), (0.6, "#FFD23A"), (1, "#FF9A1C")])
    + lg("fantasmaG", [(0, "#FFFFFF"), (0.7, "#EEF2FA"), (1, "#C9D2E6")], 0, 0, 1, 1)
    + lg("abrigoG", [(0, "#8A6A4E"), (1, "#5A4230")], 0, 0, 1, 1)
    + lg("leonaG", [(0, "#E8BD72"), (0.6, "#C8934A"), (1, "#97662C")], 0, 0, 0, 1)
)

LEONA = ("#F2D094", "#C8934A", "#8E5E28")  # claro, medio, oscuro


def _clip(cid, d):
    return f'<defs><clipPath id="{cid}"><path d="{d}"/></clipPath></defs>'


# ---------------------------------------------------------------- ojo e iconos de sentidos
def ojo(id_, cx, cy, w=520, iris="#3F86C9"):
    """Ojo humano realista de frente (almendra con párpado, pestañas, iris con brillo). Alto ≈ 0,5*w.
    Ids: {id} (blink para parpadear), {id}_iris (move para mirar), {id}_brillo (pulse). .puntos centro/iris."""
    h = w * 0.5
    x0, x1 = cx - w / 2, cx + w / 2
    alm = (f"M {f(x0)} {f(cy)} C {f(cx-w*0.28)} {f(cy-h*0.78)}, {f(cx+w*0.26)} {f(cy-h*0.8)}, {f(x1)} {f(cy-h*0.04)} "
           f"C {f(cx+w*0.24)} {f(cy+h*0.62)}, {f(cx-w*0.26)} {f(cy+h*0.62)}, {f(x0)} {f(cy)} Z")
    cid = f"clip_{id_}"
    o = _clip(cid, alm)
    # piel alrededor (párpado y pliegue)
    o += (f'<path d="M {f(x0-w*0.06)} {f(cy+h*0.02)} C {f(cx-w*0.3)} {f(cy-h*1.12)}, {f(cx+w*0.3)} {f(cy-h*1.14)}, {f(x1+w*0.06)} {f(cy-h*0.04)} '
          f'C {f(cx+w*0.3)} {f(cy+h*0.86)}, {f(cx-w*0.3)} {f(cy+h*0.86)}, {f(x0-w*0.06)} {f(cy+h*0.02)} Z" fill="{degradado("#F2C7A4", 0.2)}" stroke="{INK}" stroke-width="7"/>')
    o += f'<path d="M {f(cx-w*0.36)} {f(cy-h*0.68)} C {f(cx-w*0.12)} {f(cy-h*1.0)}, {f(cx+w*0.16)} {f(cy-h*1.0)}, {f(cx+w*0.4)} {f(cy-h*0.62)}" fill="none" stroke="#B9826A" stroke-width="6" stroke-linecap="round"/>'
    o += f'<path d="{alm}" fill="url(#ojoBlanco)"/>'
    ir = h * 0.44
    iris_g = (f'<circle cx="{f(cx)}" cy="{f(cy-h*0.02)}" r="{f(ir)}" fill="{degradado(iris, 0.35)}" stroke="{shade(iris, -0.5)}" stroke-width="6"/>'
              + "".join(f'<path d="M {f(cx+ir*0.42*math.cos(a))} {f(cy-h*0.02+ir*0.42*math.sin(a))} L {f(cx+ir*0.9*math.cos(a))} {f(cy-h*0.02+ir*0.9*math.sin(a))}" stroke="{shade(iris, 0.35)}" stroke-width="3" opacity="0.7"/>'
                        for a in [k * math.pi / 9 for k in range(18)])
              + f'<circle cx="{f(cx)}" cy="{f(cy-h*0.02)}" r="{f(ir*0.42)}" fill="{INK}"/>'
              + g(f"{id_}_brillo", f'<circle cx="{f(cx+ir*0.32)}" cy="{f(cy-h*0.02-ir*0.36)}" r="{f(ir*0.2)}" fill="#FFFFFF"/>'
                  f'<circle cx="{f(cx-ir*0.3)}" cy="{f(cy-h*0.02+ir*0.3)}" r="{f(ir*0.08)}" fill="#FFFFFF" opacity="0.8"/>'))
    o += f'<g clip-path="url(#{cid})">' + g(f"{id_}_iris", iris_g)
    o += f'<path d="M {f(x0)} {f(cy-h*0.1)} C {f(cx-w*0.28)} {f(cy-h*0.86)}, {f(cx+w*0.26)} {f(cy-h*0.88)}, {f(x1)} {f(cy-h*0.12)}" fill="none" stroke="{INK}" stroke-width="{f(h*0.16)}" opacity="0.18"/></g>'
    o += f'<path d="{alm}" fill="none" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'
    # pestañas
    for k in range(7):
        t = 0.18 + k * 0.11
        bx = (1 - t) ** 3 * x0 + 3 * (1 - t) ** 2 * t * (cx - w * 0.28) + 3 * (1 - t) * t ** 2 * (cx + w * 0.26) + t ** 3 * x1
        by = (1 - t) ** 3 * cy + 3 * (1 - t) ** 2 * t * (cy - h * 0.78) + 3 * (1 - t) * t ** 2 * (cy - h * 0.8) + t ** 3 * (cy - h * 0.04)
        ang = math.radians(-120 + k * 10)
        L = h * 0.2
        o += f'<path d="M {f(bx)} {f(by)} Q {f(bx+L*0.4*math.cos(ang))} {f(by+L*0.7*math.sin(ang))} {f(bx+L*math.cos(ang+0.25))} {f(by+L*math.sin(ang+0.25))}" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
    o += brillo(f"M {f(cx-w*0.3)} {f(cy+h*0.4)} Q {f(cx)} {f(cy+h*0.56)} {f(cx+w*0.26)} {f(cy+h*0.42)}", 5, 0.5)
    return Pieza(g(id_, o), {"centro": (cx, cy), "iris": (cx, cy - h * 0.02)}, (x0 - w * 0.06, cy - h * 0.95, x1 + w * 0.06, cy + h * 0.66))


def icono_sentido(id_, cx, cy, r=60, tipo="ojo", col="#FFFFFF"):
    """Icono redondo de un sentido: ojo, oreja, nariz, lengua, mano (dibujo en tinta sobre disco)."""
    s = r / 50
    o = f'<circle cx="0" cy="4" r="50" fill="{INK}" opacity="0.25"/><circle cx="0" cy="0" r="50" fill="{degradado(col, 0.18)}" stroke="{INK}" stroke-width="{f(6/s)}"/>'
    if tipo == "ojo":
        o += '<path d="M -34 0 Q 0 -30 34 0 Q 0 30 -34 0 Z" fill="#FFFFFF" stroke="#0B0B14" stroke-width="5"/>'
        o += '<circle cx="0" cy="0" r="12" fill="#3F86C9" stroke="#0B0B14" stroke-width="4"/><circle cx="0" cy="0" r="5" fill="#0B0B14"/><circle cx="4" cy="-4" r="3" fill="#FFFFFF"/>'
    elif tipo == "oreja":
        o += '<path d="M -8 34 C -22 34 -22 18 -16 10 C -26 -2 -24 -30 2 -32 C 26 -33 30 -8 18 6 C 10 16 8 26 -8 34 Z" fill="#F2C7A4" stroke="#0B0B14" stroke-width="5" stroke-linejoin="round"/>'
        o += '<path d="M -6 -16 C 8 -22 18 -10 8 0 C 2 6 4 12 -4 14" fill="none" stroke="#B9826A" stroke-width="5" stroke-linecap="round"/>'
    elif tipo == "nariz":
        o += '<path d="M -4 -34 C -6 -10 -24 6 -22 18 C -20 28 -4 28 6 24 C 16 30 26 22 20 12 C 12 0 4 -14 4 -34" fill="#F2C7A4" stroke="#0B0B14" stroke-width="5" stroke-linejoin="round"/>'
        o += '<path d="M -10 20 Q -4 16 0 22 M 8 20 Q 12 16 16 20" fill="none" stroke="#0B0B14" stroke-width="4" stroke-linecap="round"/>'
    elif tipo == "lengua":
        o += '<path d="M -32 -8 Q 0 -22 32 -8 Q 26 12 0 14 Q -26 12 -32 -8 Z" fill="#9C2E3A" stroke="#0B0B14" stroke-width="5" stroke-linejoin="round"/>'
        o += '<path d="M -16 2 Q -18 34 0 34 Q 18 34 16 2 Z" fill="#FF7E9A" stroke="#0B0B14" stroke-width="5" stroke-linejoin="round"/><path d="M 0 8 L 0 24" stroke="#C94B66" stroke-width="4" stroke-linecap="round"/>'
    elif tipo == "mano":
        o += '<path d="M -20 32 L -22 -6 Q -22 -12 -16 -12 Q -11 -12 -11 -6 L -11 -26 Q -11 -32 -5 -32 Q 1 -32 1 -26 L 1 -30 Q 1 -36 7 -36 Q 13 -36 13 -30 L 13 -24 Q 13 -30 19 -30 Q 25 -30 25 -24 L 25 10 Q 25 32 6 34 Z" fill="#F2C7A4" stroke="#0B0B14" stroke-width="5" stroke-linejoin="round"/>'
        o += '<path d="M -22 -2 Q -32 -14 -36 -4 Q -38 4 -22 16" fill="#F2C7A4" stroke="#0B0B14" stroke-width="5" stroke-linejoin="round"/>'
    return g(id_, f'<g transform="translate({f(cx)} {f(cy)}) scale({f(s)})">{o}</g>')


# ---------------------------------------------------------------- casa de noche
def interruptor(id_, cx, cy, s=1.0, col="#FFFFFF"):
    """Interruptor de pared (placa con tecla arriba = encendido). La tecla va en {id}_tecla: para apagar,
    move [0, 46*s] (dur 0.2). .puntos tecla (centro de la tecla encendida)."""
    w, h = 110 * s, 160 * s
    o = f'<rect x="{f(cx-w/2+8)}" y="{f(cy-h/2+10)}" width="{f(w)}" height="{f(h)}" rx="{f(16*s)}" fill="{INK}" opacity="0.25"/>'
    o += f'<rect x="{f(cx-w/2)}" y="{f(cy-h/2)}" width="{f(w)}" height="{f(h)}" rx="{f(16*s)}" fill="{degradado(col, 0.12)}" stroke="{INK}" stroke-width="7"/>'
    o += f'<rect x="{f(cx-26*s)}" y="{f(cy-52*s)}" width="{f(52*s)}" height="{f(104*s)}" rx="{f(10*s)}" fill="#C9CED8" stroke="{INK}" stroke-width="5"/>'
    tec = (f'<rect x="{f(cx-20*s)}" y="{f(cy-46*s)}" width="{f(40*s)}" height="{f(46*s)}" rx="{f(8*s)}" fill="{degradado("#FFFFFF", 0.2)}" stroke="{INK}" stroke-width="5"/>'
           + brillo(f"M {f(cx-12*s)} {f(cy-38*s)} L {f(cx+10*s)} {f(cy-38*s)}", 4, 0.9))
    o += g(f"{id_}_tecla", tec)
    o += "".join(f'<circle cx="{f(cx)}" cy="{f(cy+k*h*0.4)}" r="{f(5*s)}" fill="#AEB4C2" stroke="{INK}" stroke-width="2"/>' for k in (-1, 1))
    return Pieza(g(id_, o), {"tecla": (cx, cy - 23 * s), "abajo": (cx, cy + h / 2)}, (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2))


def mano_indice(id_, x, y, s=1.0, piel="#F2C7A4", manga="#FF7EB6", ang=0):
    """Mano con el índice estirado hacia arriba; (x, y) = yema del dedo. ang gira toda la mano sobre la muñeca.
    Ids: {id}_dedo (move [0, 30] = pulsar). .puntos muneca."""
    k = s
    loc = (f'<path d="M -46 300 L -36 150 L 52 150 L 62 300 Z" fill="{degradado(manga, 0.2)}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
           f'<path d="M -40 160 L 56 160" stroke="#FFFFFF" stroke-width="10" opacity="0.6"/>'
           f'<path d="M -40 70 Q -48 72 -48 92 L -44 150 Q -10 166 50 152 L 56 96 Q 58 72 40 70 Z" fill="{degradado(piel, 0.18)}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
           f'<path d="M -48 100 Q -70 96 -66 118 Q -60 134 -40 130" fill="{piel}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
           f'<path d="M -8 84 L -8 74 M 12 86 L 12 76 M 32 86 L 32 76" stroke="#B9826A" stroke-width="5" stroke-linecap="round"/>')
    dedo = (f'<path d="M -22 80 L -22 12 Q -22 0 -8 0 Q 6 0 6 12 L 6 80 Z" fill="{degradado(piel, 0.18)}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
            f'<path d="M -16 10 Q -8 4 0 10" fill="none" stroke="#FFFFFF" stroke-width="4" opacity="0.8"/>'
            f'<path d="M -18 40 L 2 40" stroke="#B9826A" stroke-width="4" stroke-linecap="round"/>')
    body = f'<g transform="translate({f(x+8*k)} {f(y)}) rotate({f(ang)} 0 220) scale({f(k)})">{loc}{g(f"{id_}_dedo", dedo)}</g>'
    return Pieza(g(id_, body), {"muneca": (x, y + 220 * k)}, (x - 70 * k, y, x + 70 * k, y + 300 * k))


def perchero(id_, cx, base, h=640, abrigo="#7A5A3E", sombrero=True):
    """Perchero de pie con un abrigo largo y sombrero colgados. {id}_abrigo (sway origin top, muy suave).
    .puntos gancho (de donde cuelga el abrigo), centro."""
    top = base - h
    o = sombra(cx, base + 4, 120, 14, 0.25)
    o += trazo(f"M {f(cx)} {f(base-20)} L {f(cx)} {f(top+10)}", 16, "#8A5A32", 7)
    for dx in (-90, 90):
        o += trazo(f"M {f(cx)} {f(base-40)} L {f(cx+dx)} {f(base)}", 12, "#8A5A32", 7)
    for dx in (-60, 60):
        o += trazo(f"M {f(cx)} {f(top+40)} Q {f(cx+dx*0.6)} {f(top+30)} {f(cx+dx)} {f(top)}", 9, "#8A5A32", 6)
    o += f'<circle cx="{f(cx)}" cy="{f(top+6)}" r="16" fill="url(#maderaG)" stroke="{INK}" stroke-width="6"/>'
    gy = top + 40
    ab = (f'<path d="M {f(cx-60)} {f(gy+30)} Q {f(cx)} {f(gy)} {f(cx+60)} {f(gy+30)} L {f(cx+120)} {f(gy+420)} '
          f'Q {f(cx)} {f(gy+450)} {f(cx-120)} {f(gy+420)} Z" fill="url(#abrigoG)" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>')
    ab += f'<path d="M {f(cx-60)} {f(gy+30)} L {f(cx-95)} {f(gy+330)} Q {f(cx-110)} {f(gy+350)} {f(cx-118)} {f(gy+330)} L {f(cx-86)} {f(gy+40)} Z" fill="{shade(abrigo, -0.25)}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
    ab += f'<path d="M {f(cx)} {f(gy+20)} L {f(cx+4)} {f(gy+440)}" stroke="{INK}" stroke-width="5" opacity="0.6"/>'
    ab += "".join(f'<circle cx="{f(cx+14)}" cy="{f(gy+100+k*90)}" r="8" fill="{YEL}" stroke="{INK}" stroke-width="3"/>' for k in range(3))
    ab += f'<path d="M {f(cx-40)} {f(gy+20)} L {f(cx)} {f(gy+110)} L {f(cx+40)} {f(gy+20)}" fill="{shade(abrigo, 0.2)}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
    ab += brillo(f"M {f(cx-44)} {f(gy+70)} L {f(cx-80)} {f(gy+380)}", 6, 0.35)
    if sombrero:
        ab += (f'<ellipse cx="{f(cx)}" cy="{f(gy-4)}" rx="78" ry="16" fill="#3A3F52" stroke="{INK}" stroke-width="6"/>'
               f'<path d="M {f(cx-44)} {f(gy-6)} L {f(cx-38)} {f(gy-62)} Q {f(cx)} {f(gy-78)} {f(cx+38)} {f(gy-62)} L {f(cx+44)} {f(gy-6)} Z" fill="{degradado("#3A3F52", 0.2)}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
               f'<path d="M {f(cx-42)} {f(gy-20)} L {f(cx+42)} {f(gy-20)}" stroke="{CORAL}" stroke-width="9"/>')
    o += g(f"{id_}_abrigo", ab)
    return Pieza(g(id_, o), {"gancho": (cx, gy), "centro": (cx, gy + 220)}, (cx - 125, top - 40, cx + 125, base + 10))


def sombra_monstruo(id_, cx, top, h=760, col="#0C1030"):
    """Sombra de monstruo en la pared (la del abrigo y el sombrero, agrandada): cuernos, hombros, brazos largos con
    garras. Ojos amarillos que brillan en {id}_ojos (pop + pulse). (cx, top) = punta de la cabeza."""
    k = h / 760
    def P(x, y):
        return (cx + x * k, top + y * k)
    sil = [(-40, 40), (-70, -10), (-60, 70), (-120, 120), (-200, 170), (-250, 260), (-290, 420), (-300, 560), (-320, 640), (-280, 600),
           (-270, 680), (-240, 610), (-210, 690), (-220, 560), (-200, 420), (-160, 330), (-150, 560), (-130, 760), (130, 760), (150, 560),
           (160, 330), (200, 420), (220, 560), (210, 690), (240, 610), (270, 680), (280, 600), (320, 640), (300, 560), (290, 420),
           (250, 260), (200, 170), (120, 120), (60, 70), (70, -10), (40, 40), (0, 30)]
    o = f'<path d="{smooth([P(*p) for p in sil], True, 0.35)} Z" fill="{col}" opacity="0.88"/>'
    ojos = ""
    for ex in (-38, 38):
        x, y = P(ex, 100)
        ojos += f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(46*k)}" fill="url(#ojoFiera)"/>'
        ojos += f'<path d="M {f(x-24*k)} {f(y)} Q {f(x)} {f(y-18*k)} {f(x+24*k)} {f(y)} Q {f(x)} {f(y+14*k)} {f(x-24*k)} {f(y)} Z" fill="#FFE14A" stroke="{INK}" stroke-width="3"/>'
        ojos += f'<path d="M {f(x)} {f(y-9*k)} L {f(x)} {f(y+8*k)}" stroke="{INK}" stroke-width="{f(5*k)}" stroke-linecap="round"/>'
    o += g(f"{id_}_ojos", ojos)
    bx, by = P(0, 170)
    o += g(f"{id_}_boca", f'<path d="M {f(bx-44*k)} {f(by)} L {f(bx-30*k)} {f(by+18*k)} L {f(bx-15*k)} {f(by)} L {f(bx)} {f(by+18*k)} L {f(bx+15*k)} {f(by)} L {f(bx+30*k)} {f(by+18*k)} L {f(bx+44*k)} {f(by)}" fill="none" stroke="#FFE14A" stroke-width="{f(5*k)}" stroke-linejoin="round" opacity="0.85"/>')
    return Pieza(g(id_, o), {"ojos": P(0, 100)}, (cx - 320 * k, top - 10 * k, cx + 320 * k, top + h))


# ---------------------------------------------------------------- sabana de noche
def acacia(id_, cx, base, h=620, col="#2E4A36"):
    """Acacia de sabana (tronco que se abre en ramas y copa plana en paraguas). {id}_copa (sway origin bottom, 1-2°)."""
    top = base - h
    tr = "#4A3626"
    o = trazo(f"M {f(cx)} {f(base)} Q {f(cx-10)} {f(base-h*0.4)} {f(cx+6)} {f(base-h*0.62)}", 34, tr, 8)
    for a, b in (((cx + 6, base - h * 0.62), (cx - h * 0.32, top + h * 0.16)), ((cx + 6, base - h * 0.62), (cx + h * 0.36, top + h * 0.18)),
                 ((cx + 4, base - h * 0.55), (cx + h * 0.05, top + h * 0.12))):
        o += trazo(f"M {f(a[0])} {f(a[1])} Q {f((a[0]+b[0])/2)} {f(a[1]-h*0.08)} {f(b[0])} {f(b[1])}", 18, tr, 7)
    copa = ""
    for i, (dx, dy, rx, ry) in enumerate(((-0.3, 0.12, 0.34, 0.09), (0.32, 0.13, 0.36, 0.09), (0.02, 0.06, 0.46, 0.1), (-0.12, 0.02, 0.24, 0.07), (0.2, 0.0, 0.22, 0.06))):
        copa += f'<ellipse cx="{f(cx+dx*h)}" cy="{f(top+dy*h)}" rx="{f(rx*h)}" ry="{f(ry*h)}" fill="{degradado(shade(col, 0.06*i), 0.25)}" stroke="{INK}" stroke-width="7"/>'
    copa += brillo(f"M {f(cx-h*0.3)} {f(top+h*0.0)} Q {f(cx)} {f(top-h*0.06)} {f(cx+h*0.3)} {f(top+h*0.0)}", 5, 0.25, "#B5F08F")
    o += g(f"{id_}_copa", copa)
    return Pieza(g(id_, o), {"copa": (cx, top)}, (cx - h * 0.58, top - h * 0.06, cx + h * 0.6, base))


def matas(id_, x0, x1, base, alto=90, n=14, seed=3, col="#5E5A2E"):
    """Matas de hierba alta de la sabana (cada mata un trazo curvo; ponlas delante de lo que se esconde)."""
    rnd = random.Random(seed)
    o = ""
    for i in range(n):
        x = x0 + (x1 - x0) * (i + rnd.uniform(0.1, 0.9)) / n
        for j in range(3):
            hh = alto * rnd.uniform(0.6, 1.1)
            dx = rnd.uniform(-30, 30)
            o += (f'<path d="M {f(x-8+j*8)} {f(base)} Q {f(x+dx*0.3)} {f(base-hh*0.6)} {f(x+dx)} {f(base-hh)}" fill="none" stroke="{INK}" stroke-width="12" stroke-linecap="round"/>'
                  f'<path d="M {f(x-8+j*8)} {f(base)} Q {f(x+dx*0.3)} {f(base-hh*0.6)} {f(x+dx)} {f(base-hh)}" fill="none" stroke="{shade(col, rnd.uniform(-0.1, 0.2))}" stroke-width="6" stroke-linecap="round"/>')
    return g(id_, o)


def sabana_noche(W=1080, H=1920, suelo_y=None, seed=4, luna=None):
    """Fondo: cielo de noche con estrellas y luna creciente, colinas lejanas oscuras y suelo de sabana con hierba seca.
    luna = (x, y) de la luna (por defecto arriba a la izquierda, fuera de la zona del titular en `full`)."""
    sy = suelo_y or H * 0.62
    rnd0 = random.Random(seed)
    o = f'<rect width="{W}" height="{H}" fill="url(#skyNoche)"/>'
    o += "".join(f'<circle cx="{f(rnd0.uniform(0, W))}" cy="{f(rnd0.uniform(0, sy*0.85))}" r="{f(rnd0.uniform(2, 4))}" fill="#FFFFFF" opacity="{f(rnd0.uniform(0.5, 1))}"/>' for _ in range(46))
    lx, ly = luna or (W * 0.09, H * 0.25)
    o += _TM.luna(None, lx, ly, W * 0.045)
    o += f'<path d="M 0 {f(sy-70)} C {f(W*0.2)} {f(sy-120)}, {f(W*0.4)} {f(sy-60)}, {f(W*0.6)} {f(sy-100)} C {f(W*0.78)} {f(sy-130)}, {f(W*0.9)} {f(sy-80)}, {W} {f(sy-96)} L {W} {f(sy)} L 0 {f(sy)} Z" fill="#1E2B52"/>'
    o += f'<rect x="0" y="{f(sy)}" width="{W}" height="{f(H-sy)}" fill="url(#sabanaSuelo)"/>'
    o += f'<path d="M 0 {f(sy)} C {f(W*0.3)} {f(sy-18)}, {f(W*0.6)} {f(sy+10)}, {W} {f(sy-8)}" fill="none" stroke="{INK}" stroke-width="7"/>'
    rnd = random.Random(seed)
    for _ in range(40):
        x, y = rnd.uniform(0, W), rnd.uniform(sy + 20, H)
        hh = rnd.uniform(14, 34)
        o += f'<path d="M {f(x)} {f(y)} l {f(-6)} {f(-hh)} M {f(x)} {f(y)} l 4 {f(-hh*0.8)} M {f(x)} {f(y)} l 12 {f(-hh*0.6)}" stroke="#57502F" stroke-width="4" stroke-linecap="round" opacity="0.8"/>'
    return o


def hoguera(id_, cx, base, w=220):
    """Hoguera con troncos cruzados, piedras y llamas. Ids: {id}_brillo (pulse lento), {id}_llama (sway origin bottom +
    pulse), {id}_llama_in (otra fase), {id}_chispas (float). .puntos fuego."""
    k = w / 220
    o = g(f"{id_}_brillo", f'<circle cx="{f(cx)}" cy="{f(base-80*k)}" r="{f(260*k)}" fill="url(#fuegoGlow)"/>')
    for i in range(7):
        a = math.pi * (0.05 + 0.9 * i / 6)
        x = cx - math.cos(a) * w * 0.52
        y = base - 6 * k + math.sin(a) * 10 * k
        o += f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(22*k)}" ry="{f(16*k)}" fill="{degradado("#8C93A6", 0.25)}" stroke="{INK}" stroke-width="5"/>'
    for a in (-24, 24):
        o += f'<g transform="rotate({a} {f(cx)} {f(base-24*k)})"><rect x="{f(cx-100*k)}" y="{f(base-40*k)}" width="{f(200*k)}" height="{f(30*k)}" rx="{f(15*k)}" fill="url(#maderaOsc)" stroke="{INK}" stroke-width="6"/></g>'
    ll = (f'<path d="M {f(cx-70*k)} {f(base-30*k)} C {f(cx-90*k)} {f(base-120*k)}, {f(cx-30*k)} {f(base-150*k)}, {f(cx-20*k)} {f(base-230*k)} '
          f'C {f(cx+10*k)} {f(base-180*k)}, {f(cx+30*k)} {f(base-200*k)}, {f(cx+26*k)} {f(base-270*k)} C {f(cx+80*k)} {f(base-190*k)}, {f(cx+96*k)} {f(base-110*k)}, {f(cx+70*k)} {f(base-30*k)} Z" '
          f'fill="url(#llamaG)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
    o += g(f"{id_}_llama", ll)
    li = (f'<path d="M {f(cx-36*k)} {f(base-34*k)} C {f(cx-46*k)} {f(base-90*k)}, {f(cx-6*k)} {f(base-110*k)}, {f(cx+4*k)} {f(base-170*k)} '
          f'C {f(cx+40*k)} {f(base-110*k)}, {f(cx+50*k)} {f(base-70*k)}, {f(cx+36*k)} {f(base-34*k)} Z" fill="url(#llamaIn)"/>')
    o += g(f"{id_}_llama_in", li)
    ch = "".join(f'<circle cx="{f(cx+dx*k)}" cy="{f(base-dy*k)}" r="{f(r*k)}" fill="#FFE36B" stroke="{INK}" stroke-width="2"/>'
                 for dx, dy, r in ((-60, 300, 6), (40, 330, 5), (10, 380, 4), (70, 290, 5)))
    o += g(f"{id_}_chispas", ch)
    return Pieza(g(id_, o), {"fuego": (cx, base - 120 * k)}, (cx - w * 0.6, base - 300 * k, cx + w * 0.6, base))


def leona(id_, cx, base, s=1.0):
    """Leona agazapada de perfil mirando a la izquierda, al acecho, con los dos ojos brillando (cabeza en tres cuartos).
    (cx, base) = suelo bajo el centro del cuerpo; ≈ 620×200 a s=1. Ids: {id}_cuerpo (breathe), {id}_cabeza (origin right),
    {id}_ojos (glow: pop + pulse), {id}_cola (sway origin left), {id}_orejas. .puntos ojos/cabeza/cola."""
    a, b, c = LEONA

    def P(x, y):
        return (cx + x * s, base + y * s)

    def sm(pts_, t=0.45):
        return smooth([P(*p) for p in pts_], True, t) + " Z"
    sw = 7
    o = sombra(cx, base + 4 * s, 300 * s, 16 * s, 0.35)
    # cola (detrás)
    cola = (trazo(f"M {f(P(225,-110)[0])} {f(P(225,-110)[1])} C {f(P(300,-110)[0])} {f(P(300,-110)[1])}, {f(P(300,-200)[0])} {f(P(300,-200)[1])}, {f(P(352,-190)[0])} {f(P(352,-190)[1])}", 16 * s, b, 7)
            + f'<ellipse cx="{f(P(362,-192)[0])}" cy="{f(P(362,-192)[1])}" rx="{f(22*s)}" ry="{f(16*s)}" fill="{shade(c, -0.3)}" stroke="{INK}" stroke-width="6" transform="rotate(-20 {f(P(362,-192)[0])} {f(P(362,-192)[1])})"/>')
    o += g(f"{id_}_cola", cola)
    # patas de atrás (la lejana más oscura)
    o += f'<path d="{sm([(-120,-90),(-80,-70),(-150,-18),(-160,0),(-210,0),(-212,-20),(-170,-40)])}" fill="{shade(b, -0.25)}" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"/>'
    o += f'<path d="{sm([(160,-60),(200,-50),(232,-20),(240,0),(160,0),(150,-24)])}" fill="{shade(b, -0.25)}" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"/>'
    cuerpo = f'<path d="{sm([(-150,-150),(-104,-196),(-40,-178),(80,-166),(190,-150),(240,-100),(228,-34),(170,-22),(60,-40),(-60,-44),(-150,-72)])}" fill="url(#leonaG)" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"/>'
    cuerpo += f'<path d="{sm([(-90,-52),(0,-48),(110,-44),(60,-30),(-40,-34)])}" fill="{a}" opacity="0.7"/>'
    cuerpo += f'<ellipse cx="{f(P(168,-84)[0])}" cy="{f(P(168,-84)[1])}" rx="{f(84*s)}" ry="{f(72*s)}" fill="{degradado(b, 0.22)}" stroke="{INK}" stroke-width="6"/>'
    cuerpo += f'<path d="{sm([(140,-60),(210,-48),(250,-14),(250,0),(140,0),(130,-24)])}" fill="{degradado(b, 0.18)}" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"/>'
    cuerpo += brillo(f"M {f(P(-90,-160)[0])} {f(P(-90,-160)[1])} Q {f(P(40,-180)[0])} {f(P(40,-180)[1])} {f(P(170,-152)[0])} {f(P(170,-152)[1])}", 6 * s, 0.5)
    # pata delantera cercana, estirada hacia delante
    cuerpo += f'<path d="{sm([(-160,-140),(-90,-120),(-104,-50),(-126,-24),(-206,-20),(-210,0),(-140,4),(-84,-10),(-66,-84)])}" fill="{degradado(b, 0.2)}" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"/>'
    cuerpo += "".join(f'<path d="M {f(P(x,-16)[0])} {f(P(x,-16)[1])} L {f(P(x,0)[0])} {f(P(x,0)[1])}" stroke="{INK}" stroke-width="4"/>' for x in (-192, -174))
    o += g(f"{id_}_cuerpo", cuerpo)
    # cabeza baja, tres cuartos
    cab = f'<path d="{sm([(-168,-168),(-214,-178),(-264,-156),(-298,-118),(-294,-90),(-258,-76),(-210,-80),(-172,-104)])}" fill="url(#leonaG)" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"/>'
    orejas = ""
    for ex, ey in ((-196, -176), (-236, -180)):
        x, y = P(ex, ey)
        orejas += f'<path d="M {f(x-18*s)} {f(y+8*s)} Q {f(x-14*s)} {f(y-26*s)} {f(x+4*s)} {f(y-24*s)} Q {f(x+20*s)} {f(y-18*s)} {f(x+16*s)} {f(y+8*s)} Z" fill="{b}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
        orejas += f'<path d="M {f(x-8*s)} {f(y+2*s)} Q {f(x-4*s)} {f(y-14*s)} {f(x+8*s)} {f(y+2*s)}" fill="{shade(c, -0.3)}"/>'
    cab = g(f"{id_}_orejas", orejas) + cab
    mx, my = P(-268, -98)
    cab += f'<ellipse cx="{f(mx)}" cy="{f(my)}" rx="{f(30*s)}" ry="{f(20*s)}" fill="{a}" stroke="{INK}" stroke-width="5"/>'
    nx, ny = P(-292, -112)
    cab += f'<path d="M {f(nx-12*s)} {f(ny-6*s)} L {f(nx+10*s)} {f(ny-8*s)} L {f(nx)} {f(ny+8*s)} Z" fill="#5A3A2A" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
    cab += f'<path d="M {f(nx)} {f(ny+8*s)} Q {f(nx+4*s)} {f(ny+22*s)} {f(nx+22*s)} {f(ny+22*s)}" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
    ojos = ""
    for ex, ey, rr in ((-258, -132, 1.0), (-226, -137, 0.9)):
        x, y = P(ex, ey)
        ojos += f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(34*s*rr)}" fill="url(#ojoFiera)"/>'
        ojos += f'<path d="M {f(x-15*s*rr)} {f(y)} Q {f(x)} {f(y-12*s*rr)} {f(x+15*s*rr)} {f(y)} Q {f(x)} {f(y+10*s*rr)} {f(x-15*s*rr)} {f(y)} Z" fill="#FFE14A" stroke="{INK}" stroke-width="4"/>'
        ojos += f'<path d="M {f(x)} {f(y-7*s*rr)} L {f(x)} {f(y+6*s*rr)}" stroke="{INK}" stroke-width="{f(4*s)}" stroke-linecap="round"/>'
    cab += g(f"{id_}_ojos", ojos)
    o += g(f"{id_}_cabeza", cab)
    return Pieza(g(id_, o), {"ojos": P(-242, -134), "cabeza": P(-230, -130), "cola": P(352, -190)},
                 (cx - 300 * s, base - 215 * s, cx + 385 * s, base + 10 * s))


def cabeza_leon(id_, cx, cy, r=60):
    """Icono de cabeza de león de frente (melena en picos, cara, hocico). Para platillos, avisos y cuadrículas."""
    s = r / 60
    o = ""
    pts_ = []
    for i in range(24):
        a = math.pi * 2 * i / 24
        rr = 60 if i % 2 == 0 else 46
        pts_.append((rr * math.cos(a), rr * math.sin(a)))
    o += f'<path d="{poly(pts_, True)}" fill="{degradado("#B8642A", 0.25)}" stroke="{INK}" stroke-width="{f(6/s)}" stroke-linejoin="round"/>'
    o += f'<circle cx="0" cy="2" r="36" fill="{degradado("#F2C46E", 0.2)}" stroke="{INK}" stroke-width="{f(5/s)}"/>'
    o += '<circle cx="-24" cy="-26" r="9" fill="#E8B060" stroke="#0B0B14" stroke-width="4"/><circle cx="24" cy="-26" r="9" fill="#E8B060" stroke="#0B0B14" stroke-width="4"/>'
    o += '<circle cx="-13" cy="-6" r="5" fill="#0B0B14"/><circle cx="13" cy="-6" r="5" fill="#0B0B14"/>'
    o += '<ellipse cx="0" cy="16" rx="18" ry="13" fill="#FBE3B0" stroke="#0B0B14" stroke-width="3"/><path d="M -7 8 L 7 8 L 0 16 Z" fill="#5A3A2A"/>'
    o += '<path d="M 0 16 L 0 22 M -8 25 Q 0 30 8 25" fill="none" stroke="#0B0B14" stroke-width="3" stroke-linecap="round"/>'
    return g(id_, f'<g transform="translate({f(cx)} {f(cy)}) scale({f(s)})">{o}</g>')


# ---------------------------------------------------------------- mapa y luna
_AFRICA = [(-5.8, 35.8), (-1, 35.3), (5, 36.8), (9.8, 37.3), (10.3, 34), (11, 33.4), (15, 32.3), (19.5, 30.4), (20.2, 32.2), (25, 31.6),
           (29, 30.9), (32.3, 31.3), (32.6, 29.9), (35.5, 24), (37.2, 19.6), (39.5, 15.5), (43.3, 12.5), (44.5, 10.5), (51.2, 11.8),
           (49.6, 7), (47.6, 4.5), (42.6, -0.5), (40.2, -2.8), (39.2, -4.7), (39.3, -6.8), (39.6, -9), (40.5, -10.5), (40.6, -15),
           (36.8, -18.5), (35.5, -22), (35.5, -24), (32.8, -26), (32.4, -28.6), (30.6, -31), (27.5, -33.5), (25.6, -34), (20, -34.8), (18.4, -34),
           (17.2, -30.5), (15.2, -27), (14.5, -22.9), (11.8, -17), (13.4, -12.5), (13.1, -9), (12, -5), (9.3, -0.5), (9.7, 3.5),
           (8.5, 4.5), (6.2, 4.3), (4.6, 6.2), (2.5, 6.3), (-0.5, 5.5), (-3, 5), (-7.5, 4.4), (-11, 6.8), (-13.2, 8.5), (-15, 11),
           (-17.4, 14.7), (-16.2, 19), (-17, 21), (-13, 27.5), (-9.8, 29.5), (-9.4, 32.5), (-6.8, 34)]
_MADAGASCAR = [(49.3, -12), (50.5, -15.5), (49.4, -18), (47.2, -25), (45, -25.4), (43.3, -22), (44.4, -16.2), (47, -14)]
_TANZANIA = [(30.4, -1), (33.9, -1), (37.6, -3), (39.2, -4.7), (39.3, -6.8), (39.5, -8.5), (40.4, -10.4), (37.8, -11.6),
             (34.6, -11.5), (32.9, -9.4), (30.8, -8.3), (29.6, -5.5), (30.6, -3.4), (30.8, -2.4)]


def mapa_africa(id_, cx, cy, w=420, destacar=True, col="#F2E3C2", col_dest=CORAL):
    """Mapa simple de África (con Madagascar) y Tanzania destacada en {id}_tz (pop + pulse) con chincheta.
    (cx, cy) = centro del mapa; alto ≈ 1,04*w. .puntos tanzania."""
    k = w / 70
    lon0, lat0 = 17, 1.5

    def P(lon, lat):
        return (cx + (lon - lon0) * k, cy - (lat - lat0) * k)
    o = f'<path d="{smooth([P(*p) for p in _AFRICA], True, 0.25)} Z" fill="{INK}" opacity="0.25" transform="translate(10 12)"/>'
    o += f'<path d="{smooth([P(*p) for p in _AFRICA], True, 0.25)} Z" fill="{degradado(col, 0.18)}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
    o += f'<path d="{smooth([P(*p) for p in _MADAGASCAR], True, 0.4)} Z" fill="{degradado(col, 0.18)}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
    o += brillo(f"M {f(P(-12,26)[0])} {f(P(-12,26)[1])} Q {f(P(5,34)[0])} {f(P(5,34)[1])} {f(P(25,30)[0])} {f(P(25,30)[1])}", 5, 0.6)
    tx, ty = P(35, -6.3)
    if destacar:
        tz = f'<path d="{poly([P(*p) for p in _TANZANIA], True)}" fill="{degradado(col_dest, 0.2)}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
        o += g(f"{id_}_tz", tz)
    return Pieza(g(id_, o), {"tanzania": (tx, ty)}, (cx - w / 2, P(0, 38)[1], cx + w / 2, P(0, -35)[1]))


def fase_luna(id_, cx, cy, r=50, fase=0.5, lit="#FFF3C0", oscuro="#2A3358"):
    """Luna en una fase: 0 nueva, 0.25 cuarto creciente (luz a la derecha), 0.5 llena, 0.75 cuarto menguante (luz a la izquierda)."""
    fase = fase % 1
    o = f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r*1.5)}" fill="url(#lunaHalo)" opacity="{f(0.35*math.sin(math.pi*fase))}"/>'
    o += f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{oscuro}"/>'
    rx = abs(math.cos(2 * math.pi * fase)) * r
    T_, B_ = (cx, cy - r), (cx, cy + r)
    if abs(fase - 0.5) < 0.01:
        o += f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="url(#lunaG)"/>'
    elif fase > 0.01 and fase < 0.99:
        if fase < 0.5:
            sw2 = 0 if fase < 0.25 else 1
            d = f"M {f(T_[0])} {f(T_[1])} A {f(r)} {f(r)} 0 0 1 {f(B_[0])} {f(B_[1])} A {f(rx)} {f(r)} 0 0 {sw2} {f(T_[0])} {f(T_[1])} Z"
        else:
            sw2 = 1 if fase > 0.75 else 0
            d = f"M {f(T_[0])} {f(T_[1])} A {f(r)} {f(r)} 0 0 0 {f(B_[0])} {f(B_[1])} A {f(rx)} {f(r)} 0 0 {sw2} {f(T_[0])} {f(T_[1])} Z"
        o += f'<path d="{d}" fill="url(#lunaG)"/>'
    o += f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="none" stroke="{INK}" stroke-width="6"/>'
    return g(id_, o)


# ---------------------------------------------------------------- banderas, Halloween
def hoja_arce(cx, cy, s=1.0, col="#D52B1E"):
    """Hoja de arce (bandera de Canadá). s=1 → unos 100 px de alto."""
    p = [(0, -50), (-9, -32), (-20, -38), (-15, -10), (-30, -22), (-34, -14), (-48, -18), (-42, 0), (-48, 4), (-22, 22), (-26, 30),
         (-3, 26), (-3, 50), (3, 50), (3, 26), (26, 30), (22, 22), (48, 4), (42, 0), (48, -18), (34, -14), (30, -22), (15, -10), (20, -38), (9, -32)]
    return f'<path d="{poly([(cx + x * s, cy + y * s) for x, y in p], True)}" fill="{col}" stroke-linejoin="round"/>'


def bandera_canada(id_, cx, cy, w=240, h=120, mastil=True):
    """Bandera de Canadá ondeando (franjas 1:2:1 y hoja de arce). Mástil a la izquierda; para que ondee sway origin left."""
    x0, y0 = cx - w / 2, cy - h / 2
    a = h * 0.08

    def yy(x, base):
        return base + a * math.sin((x - x0) / w * 6.28)

    def tela(xa, xb):
        return f"M {f(xa)} {f(yy(xa, y0))} L {f(xb)} {f(yy(xb, y0))} L {f(xb)} {f(yy(xb, y0+h))} L {f(xa)} {f(yy(xa, y0+h))} Z"
    o = ""
    if mastil:
        o += trazo(f"M {f(x0-6)} {f(y0-16)} L {f(x0-6)} {f(y0+h*2.1)}", 9, "#8A93A6", 5)
        o += f'<circle cx="{f(x0-6)}" cy="{f(y0-18)}" r="9" fill="url(#amarilloG)" stroke="{INK}" stroke-width="4"/>'
    o += f'<path d="{tela(x0, x0+w)}" fill="#FFFFFF"/>'
    o += f'<path d="{tela(x0, x0+w*0.25)}" fill="#D52B1E"/><path d="{tela(x0+w*0.75, x0+w)}" fill="#D52B1E"/>'
    o += hoja_arce(cx, yy(cx, cy) - 2, h / 135)
    o += f'<path d="{tela(x0, x0+w)}" fill="none" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
    o += brillo(f"M {f(x0+8)} {f(y0+12)} L {f(x0+w*0.4)} {f(y0+10)}", 4, 0.5)
    return g(id_, o)


def calabaza(id_, cx, base, w=260, cara=True):
    """Calabaza de Halloween tallada con la luz dentro. Ids: {id}_luz (pulse lento = vela), {id}_tallo (sway origin bottom).
    Alto ≈ 0,85*w. .puntos cara."""
    h = w * 0.72
    cy = base - h / 2
    o = sombra(cx, base + 4, w * 0.5, w * 0.06, 0.3)
    for dx, rx in ((-0.3, 0.26), (0.3, 0.26), (-0.14, 0.27), (0.14, 0.27), (0, 0.26)):
        o += f'<ellipse cx="{f(cx+dx*w)}" cy="{f(cy)}" rx="{f(rx*w)}" ry="{f(h/2)}" fill="url(#calabazaG)" stroke="{INK}" stroke-width="7"/>'
    o += brillo(f"M {f(cx-w*0.36)} {f(cy-h*0.2)} Q {f(cx-w*0.32)} {f(cy-h*0.38)} {f(cx-w*0.2)} {f(cy-h*0.42)}", 7, 0.6)
    tallo = (f'<path d="M {f(cx-12)} {f(cy-h/2+8)} Q {f(cx-14)} {f(cy-h/2-30)} {f(cx+8)} {f(cy-h/2-46)} L {f(cx+22)} {f(cy-h/2-36)} Q {f(cx+8)} {f(cy-h/2-20)} {f(cx+14)} {f(cy-h/2+8)} Z" '
             f'fill="{degradado("#5C8A3A", 0.2)}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
             f'<path d="M {f(cx+14)} {f(cy-h/2-6)} q 30 -10 40 10" fill="none" stroke="#5C8A3A" stroke-width="6" stroke-linecap="round"/>')
    o += g(f"{id_}_tallo", tallo)
    if cara:
        luz = ""
        for sx in (-1, 1):
            ex = cx + sx * w * 0.17
            luz += f'<path d="M {f(ex-w*0.08)} {f(cy-h*0.04)} L {f(ex)} {f(cy-h*0.26)} L {f(ex+w*0.08)} {f(cy-h*0.04)} Z" fill="url(#calabazaLuz)" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
        luz += f'<path d="M {f(cx-w*0.05)} {f(cy+h*0.06)} L {f(cx)} {f(cy-h*0.04)} L {f(cx+w*0.05)} {f(cy+h*0.06)} Z" fill="url(#calabazaLuz)" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
        m = [(-0.28, 0.12), (-0.18, 0.2), (-0.12, 0.14), (-0.04, 0.22), (0.04, 0.14), (0.12, 0.22), (0.18, 0.14), (0.28, 0.12),
             (0.2, 0.3), (0.08, 0.34), (0.02, 0.28), (-0.06, 0.34), (-0.16, 0.3)]
        luz += f'<path d="{poly([(cx + x * w, cy + y * h) for x, y in m], True)}" fill="url(#calabazaLuz)" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
        o += g(f"{id_}_luz", luz)
    return Pieza(g(id_, o), {"cara": (cx, cy)}, (cx - w * 0.56, cy - h / 2 - 50, cx + w * 0.56, base + 6))


def fantasma(id_, cx, base, h=300, susto=False):
    """Fantasma de sábana (disfraz) con dos agujeros de ojos y bajo ondulado; asoman dos pies. Ids: {id}_ojos (blink),
    {id}_cuerpo (breathe), {id}_tela (sway origin top). susto=True: ojos y boca muy abiertos. .puntos cabeza/pies."""
    w = h * 0.7
    top = base - h
    o = sombra(cx, base + 4, w * 0.5, 12, 0.25)
    o += "".join(f'<ellipse cx="{f(cx+dx)}" cy="{f(base-8)}" rx="{f(w*0.13)}" ry="{f(w*0.07)}" fill="#3A3F52" stroke="{INK}" stroke-width="5"/>' for dx in (-w * 0.16, w * 0.18))
    hem = []
    n = 6
    for i in range(n + 1):
        x = cx + w / 2 - w * i / n
        hem.append((x, base - 22 - (14 if i % 2 else 0)))
    d = (f"M {f(cx-w/2)} {f(base-22)} C {f(cx-w*0.56)} {f(top+h*0.4)}, {f(cx-w*0.44)} {f(top)}, {f(cx)} {f(top)} "
         f"C {f(cx+w*0.44)} {f(top)}, {f(cx+w*0.56)} {f(top+h*0.4)}, {f(cx+w/2)} {f(base-22)} " + " ".join(f"L {f(x)} {f(y)}" for x, y in hem[1:]) + " Z")
    tela = f'<path d="{d}" fill="url(#fantasmaG)" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'
    tela += brillo(f"M {f(cx-w*0.28)} {f(top+h*0.3)} Q {f(cx-w*0.26)} {f(top+h*0.08)} {f(cx-w*0.06)} {f(top+h*0.05)}", 7, 0.9)
    tela += f'<path d="M {f(cx+w*0.2)} {f(top+h*0.5)} Q {f(cx+w*0.24)} {f(top+h*0.7)} {f(cx+w*0.16)} {f(base-36)}" fill="none" stroke="#B7C2DA" stroke-width="6" stroke-linecap="round"/>'
    ey = top + h * 0.3
    rr = 1.35 if susto else 1.0
    ojos = "".join(f'<ellipse cx="{f(cx+dx)}" cy="{f(ey)}" rx="{f(w*0.08*rr)}" ry="{f(w*0.11*rr)}" fill="{INK}"/>' for dx in (-w * 0.15, w * 0.15))
    tela += g(f"{id_}_ojos", ojos)
    if susto:
        tela += f'<ellipse cx="{f(cx)}" cy="{f(ey+h*0.2)}" rx="{f(w*0.08)}" ry="{f(w*0.11)}" fill="{INK}"/>'
    o += g(f"{id_}_cuerpo", g(f"{id_}_tela", tela))
    return Pieza(g(id_, o), {"cabeza": (cx, top + h * 0.3), "pies": (cx, base), "cima": (cx, top)}, (cx - w * 0.56, top, cx + w * 0.56, base + 6))

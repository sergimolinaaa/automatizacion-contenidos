"""Base de la librería «El truco es…»: paleta, degradados, trazos con contorno de tinta, etiquetas, flechas,
globos, sellos, iconos de reacción, contadores, efectos y el documento SVG (layouts panel / free / full).

Todas las funciones devuelven cadenas SVG (o `Pieza`, que es una cadena con `.puntos` y `.caja`).
Uso típico:
    import sys; sys.path.insert(0, "/home/user/automatizacion-contenidos")
    from libreria.svg.base import *
    cuerpo = etiqueta("tagua", 500, 120, "AGUA", apunta=(500, 300))
    guardar("content/<carpeta>/escena.svg", svg(cuerpo, "panel", fondo=fondo_suave()))

Convenciones:
- Contorno de tinta TINTA (#0B0B14), 6-9 px, stroke-linejoin round. Claro arriba / oscuro abajo. Brillo blanco fino arriba.
- Los ids de grupo que se animan NUNCA llevan atributo transform (se pone en un <g> interior), para que
  los efectos del motor (translate/rotate/scale CSS) se sumen bien.
- Los degradados que usa cada pieza se registran solos y `svg()` los mete en <defs>.
"""
import math
import random
import xml.etree.ElementTree as ET

# ------------------------------------------------------------------ paleta
TINTA = INK = "#0B0B14"
LIMA = LIME = "#C8FF2E"
CORAL = "#FF5A36"
AZUL = "#2347FF"          # fondo de la marca
AZUL_OSC = "#1631C9"
PAPEL = "#FFFFFF"
PAPEL_GRIS = "#EEF0F5"
AMARILLO = YEL = "#FFC928"
NARANJA = "#FF9F1C"
TURQUESA = TEAL = "#1FB5A8"
VIOLETA = VIO = "#7B5CFF"
ROSA = "#FF7EB6"
CIELO = "#8FD3FF"
AGUA = "#2F7FD6"
VERDE = "#36B37E"
VERDE_CLARO = "#7BE07B"
TIERRA = "#E7C487"
MADERA = "#C98B55"
GRIS = "#9AA3B5"
GRIS_OSC = "#5A6170"
PIZARRA = "#2B3A5C"

MONO = 'font-family="JetBrains Mono" font-weight="800"'
DISP = 'font-family="Unbounded" font-weight="900"'

# Zonas seguras de cada layout (ver CLAUDE.md)
LAYOUTS = {
    "panel": (1000, 700),   # nada importante fuera de y 45-655; esquina 0-340 x 0-70 reservada a «Fig.»
    "free": (1000, 900),    # transparente; alto 800-1100 (pon "height" 800-900 en el guion)
    "full": (1080, 1920),   # fondo completo; lo importante entre y 450 y 1250
}
ZONA_FIG = (0, 0, 340, 70)
ZONA_SEGURA = {"panel": (40, 45, 960, 655), "free": (30, 30, 970, None), "full": (40, 450, 1040, 1250)}


# ------------------------------------------------------------------ utilidades numéricas
def f(v):
    """Número corto para SVG."""
    return f"{v:.1f}".rstrip("0").rstrip(".")


def pts(p):
    return " ".join(f"{f(x)} {f(y)}" for x, y in p)


def poly(p, closed=False):
    d = "M " + " L ".join(f"{f(x)} {f(y)}" for x, y in p)
    return d + (" Z" if closed else "")


def smooth(p, closed=False, t=0.5):
    """Curva Catmull-Rom suave que pasa por los puntos p (devuelve el atributo d)."""
    n = len(p)
    if n < 3:
        return poly(p, closed)
    P = [p[-1]] + list(p) + [p[0], p[1]] if closed else [p[0]] + list(p) + [p[-1]]
    d = f"M {f(P[1][0])} {f(P[1][1])}"
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        c1 = (p1[0] + (p2[0] - p0[0]) * t / 3, p1[1] + (p2[1] - p0[1]) * t / 3)
        c2 = (p2[0] - (p3[0] - p1[0]) * t / 3, p2[1] - (p3[1] - p1[1]) * t / 3)
        d += f" C {f(c1[0])} {f(c1[1])}, {f(c2[0])} {f(c2[1])}, {f(p2[0])} {f(p2[1])}"
    return d + (" Z" if closed else "")


def rot(p, c, deg):
    """Gira el punto p alrededor de c."""
    a = math.radians(deg)
    x, y = p[0] - c[0], p[1] - c[1]
    return (c[0] + x * math.cos(a) - y * math.sin(a), c[1] + x * math.sin(a) + y * math.cos(a))


def shade(hexc, k):
    """Aclara (k>0) u oscurece (k<0) un color hex. k entre -1 y 1."""
    h = hexc.lstrip("#")
    r, g_, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    if k >= 0:
        r, g_, b = [int(v + (255 - v) * k) for v in (r, g_, b)]
    else:
        r, g_, b = [int(v * (1 + k)) for v in (r, g_, b)]
    return f"#{r:02X}{g_:02X}{b:02X}"


def text_w(text, size=30, font="mono"):
    """Ancho aproximado de una etiqueta (texto + márgenes). font: 'mono' (JetBrains) o 'disp' (Unbounded, más ancha)."""
    k = 0.6 if font == "mono" else 0.86
    return int(len(text) * size * k + 44)


def solapan(a, b, pad=6):
    """¿Se solapan dos cajas (x0, y0, x1, y1)?"""
    return not (a[2] + pad < b[0] or b[2] + pad < a[0] or a[3] + pad < b[1] or b[3] + pad < a[1])


class Pieza(str):
    """Cadena SVG con datos extra: .puntos (anclajes útiles, coordenadas finales) y .caja (x0, y0, x1, y1)."""

    def __new__(cls, s, puntos=None, caja=None):
        o = super().__new__(cls, s)
        o.puntos = puntos or {}
        o.caja = caja
        return o


# ------------------------------------------------------------------ degradados (se registran solos)
_DEFS = {}


def lg(id_, stops, x1=0, y1=0, x2=0, y2=1):
    """<linearGradient>. stops = [(offset, color[, opacidad]), ...]. Vertical por defecto."""
    s = f'<linearGradient id="{id_}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">'
    for o, c, *op in stops:
        s += f'<stop offset="{o}" stop-color="{c}"' + (f' stop-opacity="{op[0]}"' if op else "") + "/>"
    return s + "</linearGradient>"


def rg(id_, stops, cx=0.5, cy=0.5, r=0.5, fx=None, fy=None):
    s = f'<radialGradient id="{id_}" cx="{cx}" cy="{cy}" r="{r}"' + (f' fx="{fx}" fy="{fy}"' if fx is not None else "") + ">"
    for o, c, *op in stops:
        s += f'<stop offset="{o}" stop-color="{c}"' + (f' stop-opacity="{op[0]}"' if op else "") + "/>"
    return s + "</radialGradient>"


def registrar_defs(*bloques):
    """Registra bloques de <defs> (cadenas con uno o varios gradientes). Los repetidos se ignoran."""
    for b in bloques:
        for part in b.replace("</linearGradient>", "</linearGradient>\n").replace("</radialGradient>", "</radialGradient>\n").replace("</clipPath>", "</clipPath>\n").split("\n"):
            part = part.strip()
            if not part:
                continue
            i = part.find('id="')
            key = part[i + 4:part.find('"', i + 4)] if i >= 0 else part
            _DEFS.setdefault(key, part)


def defs_registradas():
    return "".join(_DEFS.values())


def degradado(col, k=0.28, dir="v", id_=None):
    """Devuelve 'url(#...)' de un degradado claro→oscuro del color dado (lo registra). dir: v (arriba-abajo), h, d (diagonal)."""
    x2, y2 = {"v": (0, 1), "h": (1, 0), "d": (1, 1)}[dir]
    id_ = id_ or f"dg{dir}{col.lstrip('#').lower()}{int(k*100)}"
    if id_ not in _DEFS:
        registrar_defs(lg(id_, [(0, shade(col, k)), (1, shade(col, -k))], 0, 0, x2, y2))
    return f"url(#{id_})"


def degradado_brillo(col, k=0.3, id_=None):
    """Degradado radial con brillo arriba-izquierda (esferas, cabezas, frutas). Devuelve 'url(#...)'."""
    id_ = id_ or f"dr{col.lstrip('#').lower()}{int(k*100)}"
    if id_ not in _DEFS:
        registrar_defs(rg(id_, [(0, shade(col, k + 0.2)), (0.6, col), (1, shade(col, -k))], 0.4, 0.35, 0.75))
    return f"url(#{id_})"


BASE_DEFS = (
    lg("papelG", [(0, "#FFFFFF"), (1, "#EDEFF5")])
    + lg("papelCrema", [(0, "#FFF8E8"), (1, "#F1E3C4")])
    + lg("cristalG", [(0, "#EAF8FF", 0.75), (1, "#9FD3F2", 0.55)])
    + lg("cristalLado", [(0, "#C4E6FA", 0.7), (1, "#7DB8DE", 0.6)])
    + lg("metalG", [(0, "#F2F4F8"), (1, "#A9B2C2")])
    + lg("metalH", [(0, "#F4F6FA"), (1, "#9AA6BC")], 0, 0, 1, 0)
    + lg("aceroG", [(0, "#9AA6BC"), (1, "#5E6A82")])
    + lg("maderaG", [(0, "#D9A46C"), (1, "#9C6334")])
    + lg("maderaOsc", [(0, "#C98B55"), (1, "#8A5A31")])
    + lg("limaG", [(0, "#E2FF8A"), (1, "#A8E000")])
    + lg("coralG", [(0, "#FF8A6B"), (1, "#E2432A")])
    + lg("amarilloG", [(0, "#FFD95A"), (1, "#E8A800")])
    + lg("tarjetaG", [(0, "#FFFFFF"), (1, "#EEF1F7")])
    + rg("sombraR", [(0, INK, 0.35), (1, INK, 0)])
    + rg("resplandorY", [(0, "#FFF6B8", 0.95), (1, "#FFC928", 0)])
    + rg("resplandorC", [(0, "#FFE15A", 0.95), (1, "#FF5A36", 0)])
    + lg("fondoSuave", [(0, "#DCEBFA"), (1, "#F4F8FD")])
)
registrar_defs(BASE_DEFS)


# ------------------------------------------------------------------ primitivas de estilo
def g(id_, body, extra=""):
    """Grupo con id (para animar). No pongas transform en extra si lo vas a animar: anida otro <g>."""
    return f'<g id="{id_}"{extra}>{body}</g>' if id_ else f"<g{extra}>{body}</g>"


def gt(id_, transform, body):
    """Grupo animable con transform interior: <g id><g transform>…</g></g>."""
    return g(id_, f'<g transform="{transform}">{body}</g>')


def T(x, y, s, size=30, fill=INK, anchor="middle", font=MONO, extra=""):
    """Texto. font=MONO (etiquetas) o DISP (titulares/sellos, Unbounded 900)."""
    return f'<text x="{f(x)}" y="{f(y)}" text-anchor="{anchor}" {font} font-size="{f(size) if not isinstance(size, str) else size}" fill="{fill}" {extra}>{s}</text>'


def trazo(d, w, col, borde=7, cap="round", extra=""):
    """Trazo doble: tinta ancha debajo y color encima (patas, tubos, cables, brazos finos)."""
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{f(w + borde)}" stroke-linecap="{cap}" stroke-linejoin="round"{extra}/>'
            f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{f(w)}" stroke-linecap="{cap}" stroke-linejoin="round"{extra}/>')


dbl = trazo  # alias de los scripts antiguos


def pegatina(d, fill, sw=7, blanco=0, extra=""):
    """Forma con contorno de tinta. blanco>0 añade un borde blanco exterior de troquel (pegatina recortada)."""
    s = ""
    if blanco:
        s += f'<path d="{d}" fill="#FFFFFF" stroke="#FFFFFF" stroke-width="{f(sw + blanco * 2)}" stroke-linejoin="round"/>'
    return s + f'<path d="{d}" fill="{fill}" stroke="{INK}" stroke-width="{f(sw)}" stroke-linejoin="round"{extra}/>'


def sombra(cx, cy, rx, ry=None, op=0.22, col=INK):
    """Sombra proyectada en el suelo (elipse)."""
    return f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(rx)}" ry="{f(ry if ry else rx * 0.12)}" fill="{col}" opacity="{op}"/>'


def sombra_caja(x, y, w, h, rx=12, dx=10, dy=12, op=0.22):
    """Sombra desplazada de una tarjeta/rectángulo (estilo pegatina)."""
    return f'<rect x="{f(x+dx)}" y="{f(y+dy)}" width="{f(w)}" height="{f(h)}" rx="{f(rx)}" fill="{INK}" opacity="{op}"/>'


def brillo(d, w=6, op=0.8, col="#FFFFFF"):
    """Línea de brillo (reflejo) fina y clara."""
    return f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{f(w)}" stroke-linecap="round" opacity="{op}"/>'


def brillo_arco(cx, cy, r, a0=200, a1=250, w=None, op=0.85):
    """Brillo en arco sobre un círculo/esfera (por defecto arriba-izquierda)."""
    p0 = (cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0)))
    p1 = (cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1)))
    return brillo(f"M {f(p0[0])} {f(p0[1])} A {f(r)} {f(r)} 0 0 1 {f(p1[0])} {f(p1[1])}", w or max(3, r * 0.1), op)


def tarjeta(id_, cx, cy, w, h, fill="url(#tarjetaG)", acento=None, rx=18, rot_=0, body=""):
    """Tarjeta blanca con sombra, contorno y franja de color opcional arriba. body: contenido extra encima."""
    x, y = cx - w / 2, cy - h / 2
    s = sombra_caja(x, y, w, h, rx, 9, 11, 0.25)
    s += f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{f(rx)}" fill="{fill}" stroke="{INK}" stroke-width="6"/>'
    if acento:
        s += f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="16" rx="8" fill="{acento}" stroke="{INK}" stroke-width="4"/>'
    s += brillo(f"M {f(x+14)} {f(y+26)} L {f(x+14)} {f(y+h-18)}", 6, 0.9)
    inner = s + body
    if rot_:
        inner = f'<g transform="rotate({f(rot_)} {f(cx)} {f(cy)})">{inner}</g>'
    return Pieza(g(id_, inner), {"centro": (cx, cy)}, (x, y, x + w, y + h))


# ------------------------------------------------------------------ etiquetas, flechas, globos, sellos
def etiqueta_caja(cx, cy, text, size=30):
    w = text_w(text, size)
    h = 58 if size >= 28 else 48
    return (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)


def etiqueta(id_, cx, cy, text, apunta=None, desde=None, bg=INK, fg=LIME, size=30, punto=True, w=None):
    """Etiqueta MAYÚSCULAS (rect rx 12 + JetBrains Mono 800) centrada en (cx, cy), con línea guía opcional
    hasta `apunta` (x, y) terminada en un punto lima. `desde` = punto de salida de la línea (por defecto, el centro).
    Devuelve Pieza con .caja para comprobar solapes."""
    tw_ = w or text_w(text, size)
    h = 58 if size >= 28 else 48
    x, y = cx - tw_ / 2, cy - h / 2
    s = ""
    if apunta:
        sx, sy = desde or (cx, cy)
        s += f'<line x1="{f(sx)}" y1="{f(sy)}" x2="{f(apunta[0])}" y2="{f(apunta[1])}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
        if punto:
            s += f'<circle cx="{f(apunta[0])}" cy="{f(apunta[1])}" r="9" fill="{LIME}" stroke="{INK}" stroke-width="4"/>'
    s += (f'<rect x="{f(x)}" y="{f(y)}" width="{f(tw_)}" height="{h}" rx="12" fill="{bg}" stroke="{INK}" stroke-width="3"/>'
          + T(cx, cy + size * 0.36, text, size, fg))
    return Pieza(g(id_, s), {"centro": (cx, cy), "apunta": apunta}, (x, y, x + tw_, y + h))


def flecha(id_, p0, p1, col=LIME, w=12, punta=30, curva=0.0, ctrl=None, ctrl2=None, borde=9):
    """Flecha con contorno. curva: curvatura relativa (0 = recta, 0.3 = curva suave hacia la izquierda del avance,
    negativa hacia la derecha). ctrl = punto de control cuadrático; ctrl + ctrl2 = cúbica. Anímala con "draw"."""
    (x1, y1), (x2, y2) = p0, p1
    if ctrl2 and ctrl:
        d = f"M {f(x1)} {f(y1)} C {f(ctrl[0])} {f(ctrl[1])}, {f(ctrl2[0])} {f(ctrl2[1])}, {f(x2)} {f(y2)}"
        ang = math.atan2(y2 - ctrl2[1], x2 - ctrl2[0])
    else:
        if ctrl is None and curva:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            L = math.hypot(x2 - x1, y2 - y1)
            nx, ny = (y2 - y1) / L, -(x2 - x1) / L
            ctrl = (mx + nx * L * curva, my + ny * L * curva)
        if ctrl:
            d = f"M {f(x1)} {f(y1)} Q {f(ctrl[0])} {f(ctrl[1])} {f(x2)} {f(y2)}"
            ang = math.atan2(y2 - ctrl[1], x2 - ctrl[0])
        else:
            d = f"M {f(x1)} {f(y1)} L {f(x2)} {f(y2)}"
            ang = math.atan2(y2 - y1, x2 - x1)
    q1 = (x2 - punta * math.cos(ang - 0.5), y2 - punta * math.sin(ang - 0.5))
    q2 = (x2 - punta * math.cos(ang + 0.5), y2 - punta * math.sin(ang + 0.5))
    hd = f"M {f(q1[0])} {f(q1[1])} L {f(x2)} {f(y2)} L {f(q2[0])} {f(q2[1])}"
    return g(id_, trazo(d, w, col, borde) + trazo(hd, w, col, borde))


def flecha_gorda(id_, p0, p1, ancho=56, col=CORAL, sw=6):
    """Flecha gruesa rellena (bloque), para «pasa de aquí a allí» o «sube/baja»."""
    (x1, y1), (x2, y2) = p0, p1
    L = math.hypot(x2 - x1, y2 - y1)
    a = math.degrees(math.atan2(y2 - y1, x2 - x1))
    hw, hl = ancho / 2, min(L * 0.45, ancho * 1.3)
    shape = [(0, -hw * 0.55), (L - hl, -hw * 0.55), (L - hl, -hw * 1.15), (L, 0), (L - hl, hw * 1.15), (L - hl, hw * 0.55), (0, hw * 0.55)]
    d = poly(shape, True)
    body = (f'<path d="{d}" fill="{degradado(col)}" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"/>'
            + brillo(f"M 10 {f(-hw*0.3)} L {f(L-hl-8)} {f(-hw*0.3)}", 5, 0.7))
    return gt(id_, f"translate({f(x1)} {f(y1)}) rotate({f(a)})", body)


def globo(id_, cx, cy, text, cola=None, size=40, tipo="habla", fondo="#FFFFFF", color=INK, font=DISP, w=None):
    """Bocadillo. tipo: 'habla' (píldora con pico), 'piensa' (nube con burbujitas), 'grito' (estallido).
    cola = punto (x, y) al que apunta el pico. Texto en una línea (usa \\n para dos líneas)."""
    lines = text.split("\n")
    k = 0.8 if font == DISP else 0.62
    ww = w or max(len(t) for t in lines) * size * k + 64
    hh = size * (1.25 * len(lines) + 0.95)
    x, y = cx - ww / 2, cy - hh / 2
    s = ""
    if tipo == "piensa":
        rnd = random.Random(len(text))
        blobs = []
        n = max(6, int(ww / 70))
        for i in range(n):
            t = i / n * 2 * math.pi
            blobs.append((cx + ww * 0.5 * math.cos(t), cy + hh * 0.5 * math.sin(t), hh * (0.32 + 0.06 * rnd.random())))
        circ = "".join(f'<circle cx="{f(a)}" cy="{f(b)}" r="{f(r)}"/>' for a, b, r in blobs)
        el = f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(ww/2)}" ry="{f(hh/2)}"/>'
        s += f'<g fill="{INK}" opacity="0.25" transform="translate(8 10)">{circ}{el}</g>'
        s += f'<g fill="{INK}" stroke="{INK}" stroke-width="14">{circ}{el}</g><g fill="{fondo}">{circ}{el}</g>'
        if cola:
            tx, ty = cola
            for j, r in enumerate((16, 11, 7)):
                k_ = 0.45 + j * 0.22
                bx, by = cx + (tx - cx) * k_, cy + hh * 0.45 + (ty - cy - hh * 0.45) * k_
                s += f'<circle cx="{f(bx)}" cy="{f(by)}" r="{r}" fill="{fondo}" stroke="{INK}" stroke-width="5"/>'
    elif tipo == "grito":
        rnd = random.Random(len(text) + 3)
        P = []
        n = 18
        for i in range(n * 2):
            t = i / (n * 2) * 2 * math.pi
            r = 1.0 if i % 2 == 0 else 0.78 + 0.06 * rnd.random()
            P.append((cx + ww * 0.62 * r * math.cos(t), cy + hh * 0.85 * r * math.sin(t)))
        d = poly(P, True)
        s += f'<path d="{d}" fill="{INK}" opacity="0.25" transform="translate(8 10)"/>'
        s += f'<path d="{d}" fill="{fondo}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
    else:
        r = hh / 2
        s += sombra_caja(x, y, ww, hh, r, 8, 10, 0.3)
        if cola:
            tx, ty = cola
            bx = max(x + r, min(x + ww - r, tx))
            by = y + hh - 4 if ty > cy else y + 4
            s += f'<path d="M {f(bx-30)} {f(by)} L {f(tx)} {f(ty)} L {f(bx+30)} {f(by)} Z" fill="{fondo}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
        s += f'<rect x="{f(x)}" y="{f(y)}" width="{f(ww)}" height="{f(hh)}" rx="{f(r)}" fill="{fondo}" stroke="{INK}" stroke-width="7"/>'
        if cola:
            yy = y + hh - 8 if cola[1] > cy else y + 8
            s += f'<path d="M {f(bx-27)} {f(yy)} L {f(bx+27)} {f(yy)}" stroke="{fondo}" stroke-width="10"/>'
    y0 = cy - (len(lines) - 1) * size * 0.62 + size * 0.36
    for i, t in enumerate(lines):
        s += T(cx, y0 + i * size * 1.25, t, size, color, font=font)
    return Pieza(g(id_, s), {"centro": (cx, cy)}, (x, y, x + ww, y + hh))


def sello(id_, cx, cy, text, size=60, rot_=-8, col=CORAL, fondo="#FFFFFF"):
    """Sello de goma (doble marco, Unbounded). Anímalo con pop + punch: «golpe de sello» (sfx sello)."""
    w = len(text) * size * 0.86 + 50
    h = size * 1.7
    body = (f'<rect x="{f(cx-w/2)}" y="{f(cy-h/2)}" width="{f(w)}" height="{f(h)}" rx="10" fill="{fondo}" fill-opacity="0.92" stroke="{col}" stroke-width="7"/>'
            f'<rect x="{f(cx-w/2+8)}" y="{f(cy-h/2+8)}" width="{f(w-16)}" height="{f(h-16)}" rx="6" fill="none" stroke="{col}" stroke-width="3"/>'
            + T(cx, cy + size * 0.36, text, size, col, font=DISP))
    return Pieza(gt(id_, f"rotate({f(rot_)} {f(cx)} {f(cy)})", body), {"centro": (cx, cy)}, (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2))


def cartel(id_, cx, cy, text, size=46, bg=LIME, fg=INK, w=None):
    """Pancarta con puntas en cola de milano (p. ej. «¡PARTIDO NUEVO!»)."""
    ww = w or len(text) * size * 0.86 + 90
    h = size * 1.95
    x0, x1, y0, y1 = cx - ww / 2, cx + ww / 2, cy - h / 2, cy + h / 2
    d = poly([(x0, y0), (x1, y0), (x1 - 30, cy), (x1, y1), (x0, y1), (x0 + 30, cy)], True)
    return g(id_, f'<path d="{d}" fill="{INK}" opacity="0.25" transform="translate(8 10)"/>'
             f'<path d="{d}" fill="{bg}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>' + T(cx, cy + size * 0.36, text, size, fg, font=DISP))


# ------------------------------------------------------------------ iconos de reacción
def _burbuja(cx, cy, r, fill, sw=6):
    return (f'<circle cx="{f(cx+r*0.1)}" cy="{f(cy+r*0.14)}" r="{f(r)}" fill="{INK}" opacity="0.25"/>'
            f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{fill}" stroke="{INK}" stroke-width="{sw}"/>'
            + brillo_arco(cx, cy, r * 0.75, 200, 245, r * 0.1, 0.8))


def icono_duda(id_, cx, cy, r=40, col=CORAL, fondo="#FFFFFF", cola=True):
    """«?» en burbuja (con burbujita de pensamiento)."""
    s = _burbuja(cx, cy, r, fondo)
    if cola:
        s += f'<circle cx="{f(cx-r)}" cy="{f(cy+r*1.25)}" r="{f(r*0.22)}" fill="{fondo}" stroke="{INK}" stroke-width="5"/>'
    s += T(cx, cy + r * 0.6, "?", r * 1.7, col)
    return g(id_, s)


def icono_alerta(id_, cx, cy, r=40, col=AMARILLO):
    """«!» en triángulo de aviso."""
    P = [(cx, cy - r * 1.05), (cx + r * 1.1, cy + r * 0.85), (cx - r * 1.1, cy + r * 0.85)]
    d = poly(P, True)
    s = f'<path d="{d}" fill="{INK}" opacity="0.25" transform="translate(6 8)"/>'
    s += f'<path d="{d}" fill="{degradado(col)}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
    s += f'<path d="M {f(cx)} {f(cy-r*0.45)} L {f(cx)} {f(cy+r*0.2)}" stroke="{INK}" stroke-width="{f(r*0.2)}" stroke-linecap="round"/>'
    s += f'<circle cx="{f(cx)}" cy="{f(cy+r*0.52)}" r="{f(r*0.12)}" fill="{INK}"/>'
    return g(id_, s)


def icono_ok(id_, cx, cy, r=40, col=LIME):
    """✓ en círculo lima."""
    s = _burbuja(cx, cy, r, col)
    s += f'<path d="M {f(cx-r*0.45)} {f(cy)} L {f(cx-r*0.1)} {f(cy+r*0.38)} L {f(cx+r*0.5)} {f(cy-r*0.38)}" fill="none" stroke="{INK}" stroke-width="{f(r*0.24)}" stroke-linecap="round" stroke-linejoin="round"/>'
    return g(id_, s)


def icono_no(id_, cx, cy, r=40, col=CORAL):
    """✗ en círculo coral."""
    s = _burbuja(cx, cy, r, col)
    s += f'<path d="M {f(cx-r*0.4)} {f(cy-r*0.4)} L {f(cx+r*0.4)} {f(cy+r*0.4)} M {f(cx+r*0.4)} {f(cy-r*0.4)} L {f(cx-r*0.4)} {f(cy+r*0.4)}" stroke="#FFFFFF" stroke-width="{f(r*0.24)}" stroke-linecap="round"/>'
    return g(id_, s)


def aspa(id_, cx, cy, r, col=CORAL, sw=10):
    """✗ suelta (sin círculo), con contorno: tachar algo."""
    d = f"M {f(cx-r)} {f(cy-r)} L {f(cx+r)} {f(cy+r)} M {f(cx+r)} {f(cy-r)} L {f(cx-r)} {f(cy+r)}"
    return g(id_, trazo(d, sw, col, 7))


def corazon(id_, cx, cy, s=1.0, col=CORAL):
    """Corazón brillante (s=1 → unos 80 px de ancho)."""
    d = (f"M {f(cx)} {f(cy+30*s)} C {f(cx-50*s)} {f(cy-2*s)}, {f(cx-40*s)} {f(cy-44*s)}, {f(cx)} {f(cy-22*s)} "
         f"C {f(cx+40*s)} {f(cy-44*s)}, {f(cx+50*s)} {f(cy-2*s)}, {f(cx)} {f(cy+30*s)} Z")
    return g(id_, f'<path d="{d}" fill="{INK}" opacity="0.25" transform="translate({f(5*s)} {f(6*s)})"/>'
             f'<path d="{d}" fill="{degradado(col)}" stroke="{INK}" stroke-width="{f(max(4, 6*s))}" stroke-linejoin="round"/>'
             f'<ellipse cx="{f(cx-20*s)}" cy="{f(cy-16*s)}" rx="{f(9*s)}" ry="{f(6*s)}" fill="#FFFFFF" opacity="0.6" transform="rotate(-30 {f(cx-20*s)} {f(cy-16*s)})"/>')


def chispa(id_, cx, cy, r=30, col=LIME, puntas=4):
    """Destello de 4 (u 8) puntas: «¡aquí está el truco!»."""
    P = []
    n = puntas * 2
    for i in range(n):
        rr = r if i % 2 == 0 else r * 0.32
        a = -math.pi / 2 + i * math.pi / puntas
        P.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d = smooth(P, True, 0.15)
    return g(id_, f'<path d="{d}" fill="{col}" stroke="{INK}" stroke-width="{f(max(3, r*0.14))}" stroke-linejoin="round"/>')


def destellos(id_, cx, cy, r=60, col=LIME, seed=1):
    """Tres chispas alrededor de un punto."""
    rnd = random.Random(seed)
    s = ""
    for k, (a, rr) in enumerate(((-60, 1.0), (40, 0.7), (170, 0.55))):
        x, y = cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))
        s += chispa(None, x, y, r * 0.38 * rr + rnd.uniform(0, 3), col)
    return g(id_, s)


def rayos(id_, cx, cy, r1, r2, n=8, col=AMARILLO, w=10, a0=180, a1=360):
    """Rayos de luz/idea en abanico (por defecto, semicírculo superior)."""
    s = ""
    for i in range(n):
        a = math.radians(a0 + (a1 - a0) * i / (n - 1 if a1 - a0 < 360 else n))
        s += trazo(f"M {f(cx+r1*math.cos(a))} {f(cy+r1*math.sin(a))} L {f(cx+r2*math.cos(a))} {f(cy+r2*math.sin(a))}", w, col, 7)
    return g(id_, s)


def confeti(id_, caja, n=24, seed=7, cols=(TEAL, CORAL, YEL, LIME, VIO, "#FFFFFF")):
    """Confeti repartido en caja (x0, y0, x1, y1)."""
    rnd = random.Random(seed)
    x0, y0, x1, y1 = caja
    s = ""
    for i in range(n):
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
        c = cols[i % len(cols)]
        if i % 3 == 0:
            s += f'<circle cx="{f(x)}" cy="{f(y)}" r="9" fill="{c}" stroke="{INK}" stroke-width="3"/>'
        else:
            s += f'<rect x="{f(x-12)}" y="{f(y-5)}" width="24" height="10" rx="3" fill="{c}" stroke="{INK}" stroke-width="3" transform="rotate({f(rnd.uniform(0, 180))} {f(x)} {f(y)})"/>'
    return g(id_, s)


# ------------------------------------------------------------------ contadores y medidores
def contador(id_, cx, cy, valor, etiqueta_txt=None, w=None, h=120, fondo="#1B1E2B", col=LIME, size=None):
    """Marcador digital (pantalla oscura con cifras lima). Para que «cuente», pon varios grupos superpuestos
    con valores distintos (ids id_0, id_1…) y alterna hide/pop; o usa el elemento "stat" del motor."""
    size = size or h * 0.55
    w = w or len(str(valor)) * size * 0.72 + 70
    x, y = cx - w / 2, cy - h / 2
    s = sombra_caja(x, y, w, h, 18, 9, 11, 0.28)
    s += f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="18" fill="{degradado("#3A4258", 0.15)}" stroke="{INK}" stroke-width="7"/>'
    s += f'<rect x="{f(x+12)}" y="{f(y+12)}" width="{f(w-24)}" height="{f(h-24)}" rx="10" fill="{fondo}" stroke="{INK}" stroke-width="3"/>'
    s += T(cx, cy + size * 0.36, valor, size, col, font=DISP)
    s += brillo(f"M {f(x+22)} {f(y+20)} L {f(x+w*0.45)} {f(y+20)}", 4, 0.35)
    if etiqueta_txt:
        s += etiqueta(None, cx, y + h + 34, etiqueta_txt, bg=INK, fg=LIME, size=26)
    return Pieza(g(id_, s), {"centro": (cx, cy)}, (x, y, x + w, y + h))


def marcador(id_, cx, cy, izq, der, col_izq=CORAL, col_der=TEAL, txt_izq="", txt_der="", w=520, h=150):
    """Marcador de dos lados (antes/después, A contra B)."""
    x, y = cx - w / 2, cy - h / 2
    s = sombra_caja(x, y, w, h, 20, 9, 11, 0.28)
    s += f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="20" fill="{degradado("#3A4258", 0.15)}" stroke="{INK}" stroke-width="7"/>'
    for k, (val, col, tx) in enumerate(((izq, col_izq, txt_izq), (der, col_der, txt_der))):
        bx = x + 14 + k * (w / 2 - 7)
        s += f'<rect x="{f(bx)}" y="{f(y+14)}" width="{f(w/2-21)}" height="{f(h-28)}" rx="12" fill="#1B1E2B" stroke="{INK}" stroke-width="3"/>'
        s += T(bx + (w / 2 - 21) / 2, y + h * 0.58 + (0 if not tx else -8), val, h * 0.42, col, font=DISP)
        if tx:
            s += T(bx + (w / 2 - 21) / 2, y + h - 24, tx, 20, "#FFFFFF")
    s += f'<circle cx="{f(cx)}" cy="{f(cy-14)}" r="6" fill="#FFFFFF"/><circle cx="{f(cx)}" cy="{f(cy+14)}" r="6" fill="#FFFFFF"/>'
    return Pieza(g(id_, s), {"centro": (cx, cy)}, (x, y, x + w, y + h))


def barra(id_, x, base, w, h, col=LIME, texto=None, valor=None):
    """Barra vertical de gráfico apoyada en `base` (anímala con "grow": crece desde abajo). Texto debajo, valor encima."""
    s = f'<rect x="{f(x+8)}" y="{f(base-h+10)}" width="{f(w)}" height="{f(h)}" rx="10" fill="{INK}" opacity="0.22"/>'
    s += f'<rect x="{f(x)}" y="{f(base-h)}" width="{f(w)}" height="{f(h)}" rx="10" fill="{degradado(col, 0.22, "h")}" stroke="{INK}" stroke-width="6"/>'
    s += brillo(f"M {f(x+12)} {f(base-h+16)} L {f(x+12)} {f(base-12)}", 6, 0.6)
    if valor is not None:
        s += T(x + w / 2, base - h - 18, valor, 36, "#FFFFFF", font=DISP, extra=f'stroke="{INK}" stroke-width="6" paint-order="stroke"')
    if texto:
        s += T(x + w / 2, base + 40, texto, 26, INK)
    return Pieza(g(id_, s), {"cima": (x + w / 2, base - h)}, (x, base - h, x + w, base))


def medidor(id_, cx, cy, r, nivel=0.5, cols=(LIME, AMARILLO, CORAL), texto=None):
    """Velocímetro semicircular; la aguja va en el grupo id_+'_aguja' (anímala con move rotate, origin bottom)."""
    s = f'<path d="M {f(cx-r)} {f(cy)} A {f(r)} {f(r)} 0 0 1 {f(cx+r)} {f(cy)} Z" fill="#FFFFFF" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
    n = len(cols)
    for i, c in enumerate(cols):
        a0, a1 = math.pi + i * math.pi / n, math.pi + (i + 1) * math.pi / n
        ri = r * 0.78
        s += (f'<path d="M {f(cx+ri*math.cos(a0))} {f(cy+ri*math.sin(a0))} A {f(ri)} {f(ri)} 0 0 1 {f(cx+ri*math.cos(a1))} {f(cy+ri*math.sin(a1))}" '
              f'fill="none" stroke="{c}" stroke-width="{f(r*0.18)}"/>')
    a = math.pi + nivel * math.pi
    tip = (cx + r * 0.7 * math.cos(a), cy + r * 0.7 * math.sin(a))
    ag = trazo(f"M {f(cx)} {f(cy)} L {f(tip[0])} {f(tip[1])}", r * 0.07, CORAL, 6) + f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r*0.1)}" fill="{INK}"/>'
    s += g(f"{id_}_aguja" if id_ else None, ag)
    if texto:
        s += T(cx, cy + 46, texto, 28, INK)
    return g(id_, s)


# ------------------------------------------------------------------ efectos y ambiente
def copo(cx, cy, r, rotd=0, col="#2F6FB0"):
    """Copo de nieve (frío)."""
    arms = []
    for k in range(6):
        a = math.radians(k * 60 + rotd)
        arms.append(f"M {f(cx)} {f(cy)} L {f(cx + r*math.cos(a))} {f(cy + r*math.sin(a))}")
        bx, by = cx + r * 0.55 * math.cos(a), cy + r * 0.55 * math.sin(a)
        for sgn in (-1, 1):
            b2 = a + sgn * math.radians(45)
            arms.append(f"M {f(bx)} {f(by)} L {f(bx + r*0.35*math.cos(b2))} {f(by + r*0.35*math.sin(b2))}")
    d = " ".join(arms)
    return (f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{f(r*0.26+5)}" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="#FFFFFF" stroke-width="{f(r*0.26)}" stroke-linecap="round"/>')


def ondas_calor(x, y, alto=120, col=CORAL):
    """Onda vertical de calor (sube desde (x, y))."""
    q = alto / 4
    return trazo(f"M {f(x)} {f(y)} c {f(-q*0.55)} {f(-q*0.65)} {f(q*0.55)} {f(-q*1.3)} 0 {f(-q*2)} c {f(-q*0.55)} {f(-q*0.65)} {f(q*0.55)} {f(-q*1.3)} 0 {f(-q*2)}", 9, col, 7)


def temblor(x, y, alto=84, col="#5BC0FF"):
    """Rayitas de temblor/vibración junto a algo que tiembla."""
    q = alto / 6
    return trazo(f"M {f(x)} {f(y)} q {f(q*0.65)} {f(q)} 0 {f(2*q)} q {f(-q*0.65)} {f(q)} 0 {f(2*q)} q {f(q*0.65)} {f(q)} 0 {f(2*q)}", 7, col, 6)


def lineas_velocidad(x, y, n=3, largo=70, sep=34, col="#FFFFFF", dir_=-1):
    """Rayas de velocidad horizontales (dir_=-1: el objeto va hacia la derecha, rayas detrás a la izquierda)."""
    s = ""
    for i in range(n):
        yy = y + (i - (n - 1) / 2) * sep
        x0 = x + (i % 2) * 18 * dir_
        s += trazo(f"M {f(x0)} {f(yy)} L {f(x0 + dir_*largo*(1 - 0.2*(i % 2)))} {f(yy)}", 7, col, 8)
    return s


def nota_musical(cx, cy, s=60, col=INK, doble=False, rot_=-12):
    """Nota musical (♪ / ♫)."""
    k = s / 60
    if doble:
        b = (f'<path d="M 18 -60 L 58 -70 L 58 -56 L 18 -46 Z" fill="{col}"/><line x1="18" y1="-58" x2="18" y2="0" stroke="{col}" stroke-width="7"/>'
             f'<line x1="58" y1="-68" x2="58" y2="-10" stroke="{col}" stroke-width="7"/>'
             f'<ellipse cx="6" cy="2" rx="15" ry="11" fill="{col}" transform="rotate(-20 6 2)"/><ellipse cx="46" cy="-8" rx="15" ry="11" fill="{col}" transform="rotate(-20 46 -8)"/>')
    else:
        b = (f'<line x1="18" y1="-62" x2="18" y2="0" stroke="{col}" stroke-width="7"/>'
             f'<path d="M 18 -62 C 30 -50, 44 -46, 38 -26" fill="none" stroke="{col}" stroke-width="7" stroke-linecap="round"/>'
             f'<ellipse cx="6" cy="2" rx="15" ry="11" fill="{col}" transform="rotate(-20 6 2)"/>')
    return f'<g transform="translate({f(cx)} {f(cy)}) scale({f(k)}) rotate({f(rot_)})">{b}<ellipse cx="2" cy="-1" rx="5" ry="3" fill="#FFFFFF" opacity="0.6"/></g>'


def zzz(cx, cy, s=40, col="#FFFFFF"):
    """«Z z z» de sueño, de mayor a menor hacia arriba a la derecha."""
    out = ""
    for i, k in enumerate((1.0, 0.75, 0.55)):
        out += T(cx + i * s * 0.8, cy - i * s * 0.9, "Z", s * k, col, font=DISP, extra=f'stroke="{INK}" stroke-width="{f(5*k)}" paint-order="stroke"')
    return out


def gota(cx, cy, s=30, col="#8FD3FF"):
    """Gota (sudor, agua, lágrima). (cx, cy) = centro de la parte redonda."""
    d = f"M {f(cx)} {f(cy-s*1.6)} C {f(cx+s*0.3)} {f(cy-s*0.9)}, {f(cx+s)} {f(cy-s*0.4)}, {f(cx+s)} {f(cy+s*0.15)} A {f(s)} {f(s)} 0 0 1 {f(cx-s)} {f(cy+s*0.15)} C {f(cx-s)} {f(cy-s*0.4)}, {f(cx-s*0.3)} {f(cy-s*0.9)}, {f(cx)} {f(cy-s*1.6)} Z"
    return (f'<path d="{d}" fill="{degradado(col, 0.25)}" stroke="{INK}" stroke-width="{f(max(3, s*0.16))}" stroke-linejoin="round"/>'
            f'<ellipse cx="{f(cx-s*0.4)}" cy="{f(cy-s*0.05)}" rx="{f(s*0.18)}" ry="{f(s*0.3)}" fill="#FFFFFF" opacity="0.8"/>')


def vaho(cx, cy, s=1.0):
    """Nubecitas de vaho/aliento."""
    return "".join(f'<circle cx="{f(cx+dx*s)}" cy="{f(cy+dy*s)}" r="{f(r*s)}" fill="#FFFFFF" stroke="#7FA6CC" stroke-width="4" opacity="0.9"/>'
                   for dx, dy, r in ((0, 0, 16), (30, -15, 22), (65, -30, 18)))


def onda_expansiva(id_, cx, cy, r, col=LIME, w=8):
    """Anillo para el efecto "ripple" (pon dos con phase 0 y 0.5)."""
    return g(id_, f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="none" stroke="{INK}" stroke-width="{f(w+6)}"/>'
             f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="none" stroke="{col}" stroke-width="{f(w)}"/>')


def resplandor(cx, cy, r, tipo="Y"):
    """Halo suave sin contorno (Y amarillo, C coral-fuego)."""
    return f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="url(#resplandor{tipo})"/>'


def lupa(id_, cx, cy, r, ang=40, contenido="", mango="#7A4E28"):
    """Lupa con cristal; `contenido` se recorta dentro del cristal (dibújalo centrado en cx, cy)."""
    a = math.radians(ang)
    hx, hy = cx + r * math.cos(a), cy + r * math.sin(a)
    ex, ey = cx + r * 2.1 * math.cos(a), cy + r * 2.1 * math.sin(a)
    cid = f"clip_{id_ or 'lupa'}_{int(cx)}_{int(cy)}"
    s = f'<path d="M {f(hx)} {f(hy)} L {f(ex)} {f(ey)}" stroke="{INK}" stroke-width="{f(r*0.42)}" stroke-linecap="round"/>'
    s += f'<path d="M {f(hx+r*0.15*math.cos(a))} {f(hy+r*0.15*math.sin(a))} L {f(ex)} {f(ey)}" stroke="{mango}" stroke-width="{f(r*0.26)}" stroke-linecap="round"/>'
    s += f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="url(#cristalG)"/>'
    if contenido:
        s += f'<clipPath id="{cid}"><circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r*0.95)}"/></clipPath><g clip-path="url(#{cid})">{contenido}</g>'
    s += f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="none" stroke="{INK}" stroke-width="{f(max(6, r*0.12))}"/>'
    s += f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r*0.9)}" fill="none" stroke="#9FB4C8" stroke-width="{f(max(3, r*0.04))}"/>'
    s += brillo(f"M {f(cx-r*0.62)} {f(cy-r*0.18)} A {f(r*0.65)} {f(r*0.65)} 0 0 1 {f(cx-r*0.12)} {f(cy-r*0.64)}", max(4, r * 0.08), 0.9)
    return g(id_, s)


def nube(cx, cy, s=1.0, contorno=True, op=1.0, col="#FFFFFF", sombra_col="#CFE3F5"):
    """Nube esponjosa (s=1 → unos 220 px de ancho)."""
    blobs = [(-60, 10, 40), (-20, -14, 52), (30, -4, 46), (68, 14, 34), (0, 20, 44)]
    base = "".join(f'<circle cx="{f(cx+dx*s)}" cy="{f(cy+dy*s)}" r="{f(r*s)}"/>' for dx, dy, r in blobs)
    o = f'<g opacity="{op}">'
    if contorno:
        o += f'<g fill="{INK}" stroke="{INK}" stroke-width="{f(14*max(0.6, s))}">{base}</g>'
    o += f'<g fill="{col}">{base}</g>'
    o += f'<ellipse cx="{f(cx+4*s)}" cy="{f(cy+40*s)}" rx="{f(86*s)}" ry="{f(16*s)}" fill="{sombra_col}"/>'
    o += brillo(f"M {f(cx-50*s)} {f(cy-26*s)} A {f(40*s)} {f(40*s)} 0 0 1 {f(cx-10*s)} {f(cy-58*s)}", 5, 0.9)
    return o + "</g>"


def onomatopeya(id_, cx, cy, texto, r=110, size=48, rot_=-8, col="url(#resplandorBurst)", fg=INK, puntas=12):
    """Estallido de cómic con onomatopeya (¡CRAC!, ¡PLAF!, ¡HIC!). Anímalo con pop + punch."""
    P = []
    for i in range(puntas * 2):
        a = math.pi * i / puntas
        rr = r if i % 2 == 0 else r * 0.72
        P.append((cx + rr * math.cos(a), cy + rr * 0.78 * math.sin(a)))
    d = poly(P, True)
    s = f'<path d="{d}" fill="{INK}" opacity="0.25" transform="translate(8 9)"/>'
    s += f'<path d="{d}" fill="{col}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
    s += T(cx, cy + size * 0.36, texto, size, fg, font=DISP)
    return gt(id_, f"rotate({f(rot_)} {f(cx)} {f(cy)})", s)


registrar_defs(rg("resplandorBurst", [(0, "#FFF6B8"), (1, "#FFC928")]))


def ondas_sonido(id_, cx, cy, r0=40, n=3, a0=-40, a1=40, sep=26, w=8, col=INK):
    """Arcos concéntricos de sonido (o señal) saliendo de (cx, cy) entre los ángulos a0 y a1 (0 = derecha)."""
    s = ""
    for i in range(n):
        r = r0 + i * sep
        p0 = (cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0)))
        p1 = (cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1)))
        s += f'<path d="M {f(p0[0])} {f(p0[1])} A {f(r)} {f(r)} 0 0 1 {f(p1[0])} {f(p1[1])}" fill="none" stroke="{col}" stroke-width="{f(w)}" stroke-linecap="round" opacity="{f(1 - i*0.18)}"/>'
    return g(id_, s)


# ------------------------------------------------------------------ documento
def fondo_suave(w=1000, h=700, col1="#DCEBFA", col2="#F4F8FD", bokeh=True, seed=5):
    """Fondo de panel claro con círculos de bokeh sin contorno."""
    gid = f"fs_{col1[1:]}{col2[1:]}"
    registrar_defs(lg(gid, [(0, col1), (1, col2)]))
    s = f'<rect width="{w}" height="{h}" fill="url(#{gid})"/>'
    if bokeh:
        rnd = random.Random(seed)
        s += '<g fill="#FFFFFF" opacity="0.55">' + "".join(
            f'<circle cx="{f(rnd.uniform(0, w))}" cy="{f(rnd.uniform(0, h))}" r="{f(rnd.uniform(16, 44))}"/>' for _ in range(7)) + "</g>"
    return s


def svg(body, layout="panel", h=None, w=None, fondo=None, defs=""):
    """Documento SVG completo. layout: 'panel' (1000x700), 'free' (1000xh, transparente) o 'full' (1080x1920).
    fondo: cadena SVG que va debajo de todo (p. ej. un escenario o fondo_suave()). defs: defs extra."""
    W, H = LAYOUTS[layout]
    if layout == "free" and h:
        H = h
    if w:
        W = w
    if h and layout != "free":
        H = h
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">\n<defs>{defs_registradas()}{defs}</defs>\n'
            + (fondo or "") + "\n" + body + "\n</svg>")


def validar(doc):
    """Lanza excepción si el SVG no es XML válido. Devuelve el árbol."""
    return ET.fromstring(doc)


def guardar(path, doc):
    """Valida (xml.etree) y guarda el SVG."""
    validar(doc)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(doc)
    print("ok", path, len(doc))
    return path

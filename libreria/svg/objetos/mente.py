"""Mente y cerebro que predice: pluma, bola de cristal (con lo que «predice» dentro), engranaje, barra de volumen por
segmentos, cara para el cerebro de `cuerpo.cerebro()` (aburrido, sorprendido, con gafas) y pivote invisible.

Sale de: lote9-05-cosquillas (por qué no puedes hacerte cosquillas a ti mismo).

Pivotes con el motor (transform-box: fill-box): el `origin` de una animación es un punto de la CAJA del grupo. Para que
algo gire sobre un punto que no está en su borde (un hombro, un codo, la base de un brazo robótico), mete en el grupo
`pivote(px, py, r)`: un rectángulo invisible centrado en el pivote y más grande que la pieza, y anima con origin "center".
"""
import math
from ..base import (INK, LIME, CORAL, AMARILLO, f, g, T, DISP, shade, trazo, sombra, brillo, brillo_arco, lg, rg,
                    registrar_defs, degradado, Pieza, smooth)

registrar_defs(
    rg("bolaCristal", [(0, "#F4FBFF", 0.95), (0.55, "#BFE3FF", 0.75), (1, "#6E8BFF", 0.85)], 0.38, 0.32, 0.8)
    + rg("bolaHalo", [(0, "#C8FF2E", 0.55), (1, "#C8FF2E", 0)])
    + lg("plumaG", [(0, "#FFFFFF"), (1, "#FFC6DA")], 0, 0, 1, 1)
    + lg("engranajeG", [(0, "#E6EBF3"), (1, "#8C96AB")], 0, 0, 1, 1)
)


def pivote(px, py, r):
    """Rectángulo invisible de 2r×2r centrado en (px, py): con él dentro, origin "center" = (px, py)."""
    return f'<rect x="{f(px-r)}" y="{f(py-r)}" width="{f(2*r)}" height="{f(2*r)}" fill="none" stroke="none"/>'


def pluma(id_, cx, cy, L=220, ang=-30, col="#FF7EB6"):
    """Pluma de ave (para hacer cosquillas): cañón blanco curvado y barbas con degradado blanco→rosa.
    (cx, cy) = punta del cañón (la que toca); ang = dirección hacia la punta suave (0 = derecha, -90 = arriba).
    .puntos: punta (la que hace cosquillas), copete (el otro extremo)."""
    a = math.radians(ang)
    ux, uy = math.cos(a), math.sin(a)
    nx, ny = -uy, ux

    def P(t, d=0.0):
        return (cx + ux * L * t + nx * d, cy + uy * L * t + ny * d)
    # barbas: contorno en hoja asimétrica con muescas
    izq = [P(0.18, 0)] + [P(t, (0.2 + 0.8 * math.sin(math.pi * (t - 0.18) / 0.84)) * L * 0.17 * (1 if k % 3 else 0.82))
                          for k, t in enumerate([0.26, 0.36, 0.46, 0.56, 0.66, 0.76, 0.86, 0.95])] + [P(1.02, 0)]
    der = [P(t, -(0.2 + 0.8 * math.sin(math.pi * (t - 0.18) / 0.84)) * L * 0.13 * (1 if k % 4 else 0.8))
           for k, t in enumerate([0.95, 0.86, 0.76, 0.66, 0.56, 0.46, 0.36, 0.26])]
    pts = izq + der
    o = f'<path d="{smooth(pts, True)}" fill="url(#plumaG)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
    o += f'<path d="{smooth(pts[2:7], False)}" fill="none" stroke="{col}" stroke-width="{f(L*0.05)}" stroke-linecap="round" opacity="0.55"/>'
    for t in (0.34, 0.5, 0.66, 0.8):  # muescas de las barbas
        x0, y0 = P(t, 0)
        x1, y1 = P(t + 0.07, L * 0.12)
        o += f'<path d="M {f(x0)} {f(y0)} L {f(x1)} {f(y1)}" stroke="{shade(col, -0.25)}" stroke-width="3" stroke-linecap="round" opacity="0.6"/>'
    x0, y0 = P(0, 0)
    xm, ym = P(0.55, L * 0.02)
    x1, y1 = P(1.0, 0)
    o += trazo(f"M {f(x0)} {f(y0)} Q {f(xm)} {f(ym)} {f(x1)} {f(y1)}", max(4, L * 0.022), "#FFFFFF", 4)
    return Pieza(g(id_, o), {"punta": P(1.0, 0), "copete": (cx, cy)},
                 (min(x0, x1) - L * 0.2, min(y0, y1) - L * 0.2, max(x0, x1) + L * 0.2, max(y0, y1) + L * 0.2))


def bola_cristal(id_, cx, cy, r=110, dentro="", col_base="#7B5CFF"):
    """Bola de adivino en su peana. `dentro` = SVG (en coordenadas finales) que se ve dentro de la bola, recortado.
    Sub-ids: _halo (pulse), _dentro (float suave), _brillo. .puntos: centro, base."""
    cid = f"clipBola_{id_ or 'b'}"
    o = sombra(cx, cy + r * 1.18, r * 0.95, r * 0.14, 0.25)
    o += g(f"{id_}_halo" if id_ else None, f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r*1.45)}" fill="url(#bolaHalo)"/>')
    # peana
    o += (f'<path d="M {f(cx-r*0.82)} {f(cy+r*1.15)} L {f(cx-r*0.58)} {f(cy+r*0.72)} L {f(cx+r*0.58)} {f(cy+r*0.72)} '
          f'L {f(cx+r*0.82)} {f(cy+r*1.15)} Z" fill="{degradado(col_base, 0.3)}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
    o += f'<rect x="{f(cx-r*0.9)}" y="{f(cy+r*1.08)}" width="{f(r*1.8)}" height="{f(r*0.16)}" rx="{f(r*0.06)}" fill="{shade(col_base, -0.3)}" stroke="{INK}" stroke-width="6"/>'
    o += f'<defs><clipPath id="{cid}"><circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r-4)}"/></clipPath></defs>'
    o += f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="url(#bolaCristal)" stroke="{INK}" stroke-width="7"/>'
    o += f'<g clip-path="url(#{cid})">' + g(f"{id_}_dentro" if id_ else None, dentro) + '</g>'
    o += g(f"{id_}_brillo" if id_ else None, brillo_arco(cx, cy, r * 0.78, 200, 255, r * 0.08, 0.9)
           + f'<circle cx="{f(cx+r*0.42)}" cy="{f(cy-r*0.45)}" r="{f(r*0.08)}" fill="#FFFFFF" opacity="0.9"/>')
    return Pieza(g(id_, o), {"centro": (cx, cy), "base": (cx, cy + r * 1.24)}, (cx - r * 1.45, cy - r * 1.45, cx + r * 1.45, cy + r * 1.3))


def engranaje(id_, cx, cy, r=60, dientes=10, col="url(#engranajeG)"):
    """Rueda dentada (para «coordina», «mecanismo»): centrada, así que spin gira sobre su eje (amount negativo = al revés).
    Para engranar dos: r2 = r1 * d2 / d1 y velocidades inversas a los dientes."""
    pts = []
    for i in range(dientes * 4):
        a = 2 * math.pi * i / (dientes * 4)
        rr = r if (i % 4) in (1, 2) else r * 0.8
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d = "M " + " L ".join(f"{f(x)} {f(y)}" for x, y in pts) + " Z"
    o = f'<path d="{d}" fill="{col}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
    o += f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r*0.42)}" fill="none" stroke="{INK}" stroke-width="4" opacity="0.4"/>'
    o += f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r*0.2)}" fill="{INK}"/>'
    return Pieza(g(id_, o), {"centro": (cx, cy)}, (cx - r, cy - r, cx + r, cy + r))


def barra_volumen(id_, x0, base, w=440, h=300, n=7, cols=(LIME, LIME, AMARILLO, AMARILLO, "#FF9F2E", CORAL, CORAL), texto=None):
    """Indicador de volumen por segmentos crecientes (como el de la radio). Cada segmento en {id}_b<i> (grow origin
    bottom en cascada para subir; hide de derecha a izquierda para bajar). Texto opcional debajo.
    .puntos: tope (arriba del último), base (centro abajo); .puntos['seg'] = centros de cada segmento."""
    gap = w * 0.035
    bw = (w - gap * (n - 1)) / n
    o = f'<rect x="{f(x0-18)}" y="{f(base-h-22)}" width="{f(w+36)}" height="{f(h+44)}" rx="22" fill="#1B1E2B" stroke="{INK}" stroke-width="7"/>'
    segs = []
    for i in range(n):
        x = x0 + i * (bw + gap)
        hh = h * (0.22 + 0.78 * (i + 1) / n)
        c = cols[i % len(cols)]
        # hueco apagado detrás
        o += f'<rect x="{f(x)}" y="{f(base-hh)}" width="{f(bw)}" height="{f(hh)}" rx="8" fill="#2C3144" stroke="#3A4058" stroke-width="3"/>'
        seg = (f'<rect x="{f(x)}" y="{f(base-hh)}" width="{f(bw)}" height="{f(hh)}" rx="8" fill="{degradado(c, 0.25)}" stroke="{INK}" stroke-width="5"/>'
               f'<rect x="{f(x+bw*0.18)}" y="{f(base-hh+8)}" width="{f(bw*0.18)}" height="{f(hh*0.5)}" rx="4" fill="#FFFFFF" opacity="0.45"/>')
        o += g(f"{id_}_b{i}" if id_ else None, seg)
        segs.append((x + bw / 2, base - hh / 2))
    if texto:
        o += T(x0 + w / 2, base + 82, texto, 34, "#FFFFFF", font=DISP, extra=f'stroke="{INK}" stroke-width="7" paint-order="stroke"')
    return Pieza(g(id_, o), {"tope": (x0 + w - bw / 2, base - h), "base": (x0 + w / 2, base), "seg": segs},
                 (x0 - 18, base - h - 22, x0 + w + 18, base + (100 if texto else 22)))


def cara_cerebro(id_, cx, cy, s=1.0, expresion="aburrido", gafas=True):
    """Cara para pegar encima de `cuerpo.cerebro(id, cx, cy, s)` (mismo cx, cy, s): ojos, cejas, boca y gafas.
    expresion: aburrido (párpados a media asta, boca plana), sorpresa, contento. Sub-ids: _ojos (blink), _boca, _gafas.
    """
    def P(x, y):
        return (cx + x * s, cy + y * s)
    o = ""
    ojos = ""
    for k, ex in enumerate((-48, 52)):
        x, y = P(ex, -18)
        r = 26 * s
        ojos += f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(r)}" ry="{f(r*1.08)}" fill="#FFFFFF" stroke="{INK}" stroke-width="{f(5*s)}"/>'
        if expresion == "aburrido":
            ojos += f'<circle cx="{f(x+4*s)}" cy="{f(y+8*s)}" r="{f(10*s)}" fill="{INK}"/>'
            # párpado a media asta
            ojos += (f'<path d="M {f(x-r)} {f(y)} A {f(r)} {f(r*1.08)} 0 0 1 {f(x+r)} {f(y)} Z" fill="#E996A4" stroke="{INK}" stroke-width="{f(5*s)}"/>')
        elif expresion == "sorpresa":
            ojos += f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(9*s)}" fill="{INK}"/>'
        else:
            ojos += f'<circle cx="{f(x+2*s)}" cy="{f(y+2*s)}" r="{f(11*s)}" fill="{INK}"/><circle cx="{f(x+6*s)}" cy="{f(y-3*s)}" r="{f(3.5*s)}" fill="#FFFFFF"/>'
    o += g(f"{id_}_ojos" if id_ else None, ojos)
    if gafas:
        gs = ""
        for ex in (-48, 52):
            x, y = P(ex, -18)
            gs += f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(38*s)}" fill="#FFFFFF" fill-opacity="0.12" stroke="{INK}" stroke-width="{f(8*s)}"/>'
        x0, y0 = P(-10, -24)
        x1, y1 = P(14, -24)
        gs += f'<path d="M {f(x0)} {f(y0)} Q {f((x0+x1)/2)} {f(y0-10*s)} {f(x1)} {f(y1)}" fill="none" stroke="{INK}" stroke-width="{f(7*s)}" stroke-linecap="round"/>'
        o += g(f"{id_}_gafas" if id_ else None, gs)
    bx, by = P(4, 52)
    if expresion == "aburrido":
        boca = f'<path d="M {f(bx-30*s)} {f(by)} Q {f(bx)} {f(by+4*s)} {f(bx+30*s)} {f(by-3*s)}" fill="none" stroke="{INK}" stroke-width="{f(7*s)}" stroke-linecap="round"/>'
    elif expresion == "sorpresa":
        boca = f'<ellipse cx="{f(bx)}" cy="{f(by)}" rx="{f(16*s)}" ry="{f(20*s)}" fill="#7A2236" stroke="{INK}" stroke-width="{f(6*s)}"/>'
    else:
        boca = f'<path d="M {f(bx-32*s)} {f(by-6*s)} Q {f(bx)} {f(by+30*s)} {f(bx+32*s)} {f(by-6*s)} Z" fill="#7A2236" stroke="{INK}" stroke-width="{f(6*s)}" stroke-linejoin="round"/>'
    o += g(f"{id_}_boca" if id_ else None, boca)
    return Pieza(g(id_, o), {"ojos": P(0, -18), "boca": (bx, by)}, (cx - 100 * s, cy - 70 * s, cx + 100 * s, cy + 80 * s))

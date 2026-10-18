"""Territorio y comparación: mapa de España con capitales de provincia, balanza de dos platillos, ciudad de rascacielos
y pueblo pequeño (lote8-02-voto-soria: «¿por qué un voto en Soria pesa más que uno en Madrid?»).

Uso:
    from libreria.svg.objetos import territorio as TE
    m = TE.mapa_espana("mapa", 500, 420, 760, destacar=("Madrid", "Soria"))   # .puntos["Madrid"] = (x, y)
    b = TE.balanza("bal", 540, 1200, 620, inclina=-14, izq=..., der=...)       # dos llamadas (recta / inclinada) + hide/fade
"""
import math
import random
from ..base import (INK, LIME, CORAL, YEL, f, g, T, MONO, DISP, sombra, brillo, lg, registrar_defs, degradado, Pieza, smooth)

registrar_defs(
    lg("mapaTierra", [(0, "#FFF4D6"), (1, "#F2D9A0")]) + lg("mapaMar", [(0, "#BFE3FF"), (1, "#8CC8F2")])
    + lg("balMetal", [(0, "#FFE38A"), (1, "#D49A12")]) + lg("balPlato", [(0, "#FFF0B8"), (1, "#E3AE2A")])
    + lg("torreG", [(0, "#B9C7E6"), (1, "#6F82AE")]) + lg("torreG2", [(0, "#D9E2F5"), (1, "#8C9DC4")])
    + lg("torreG3", [(0, "#9FB0D8"), (1, "#56699A")]) + lg("piedraG", [(0, "#F6E3C0"), (1, "#D8B47E")])
    + lg("tejaG", [(0, "#E8805C"), (1, "#B24A2C")])
)

# Costa y frontera de la Península (lon, lat), en sentido horario desde la desembocadura del Miño.
_PENINSULA = [
    (-8.9, 41.9), (-8.85, 42.25), (-9.05, 42.6), (-9.27, 42.9), (-9.2, 43.2), (-8.6, 43.35), (-8.3, 43.47), (-7.7, 43.75),
    (-7.0, 43.55), (-6.2, 43.57), (-5.7, 43.58), (-4.8, 43.42), (-3.8, 43.47), (-3.0, 43.4), (-2.0, 43.32), (-1.8, 43.38),
    (-1.4, 43.05), (-0.7, 42.85), (0.7, 42.8), (1.4, 42.6), (2.0, 42.42), (3.15, 42.45), (3.3, 42.3), (3.2, 41.9),
    (2.2, 41.35), (1.0, 41.05), (0.85, 40.72), (0.0, 40.0), (-0.3, 39.45), (0.2, 38.78), (-0.5, 38.3), (-0.75, 37.85),
    (-1.0, 37.58), (-1.6, 37.25), (-1.9, 36.75), (-2.5, 36.8), (-3.5, 36.72), (-4.4, 36.7), (-5.0, 36.45), (-5.35, 36.15),
    (-5.6, 36.0), (-6.0, 36.3), (-6.3, 36.55), (-6.45, 36.85), (-7.4, 37.2), (-7.5, 37.55), (-7.25, 38.2), (-7.1, 38.8),
    (-7.5, 39.6), (-7.0, 40.2), (-6.85, 41.0), (-6.4, 41.6), (-6.9, 41.95), (-8.1, 41.85),
]
_BALEARES = [(2.95, 39.62, 0.5, 0.28), (4.1, 39.95, 0.25, 0.1), (1.4, 38.98, 0.2, 0.13)]  # lon, lat, rx, ry (grados)
# Capitales de las 50 provincias + Ceuta y Melilla (lon, lat). Las dos canarias se dibujan en el recuadro.
CAPITALES = {
    "A Coruña": (-8.4, 43.37), "Lugo": (-7.56, 43.01), "Ourense": (-7.86, 42.34), "Pontevedra": (-8.64, 42.43),
    "Asturias": (-5.85, 43.36), "Cantabria": (-3.8, 43.42), "Bizkaia": (-2.93, 43.26), "Gipuzkoa": (-1.98, 43.25),
    "Araba": (-2.67, 42.85), "Navarra": (-1.64, 42.81), "La Rioja": (-2.45, 42.47), "Huesca": (-0.41, 42.14),
    "Zaragoza": (-0.88, 41.65), "Teruel": (-1.1, 40.34), "Lleida": (0.62, 41.62), "Girona": (2.82, 41.98),
    "Barcelona": (2.17, 41.39), "Tarragona": (1.25, 41.12), "Castellón": (-0.05, 39.99), "Valencia": (-0.38, 39.47),
    "Alicante": (-0.48, 38.35), "Murcia": (-1.13, 37.99), "Albacete": (-1.86, 38.99), "Cuenca": (-2.13, 40.07),
    "Guadalajara": (-3.17, 40.63), "Madrid": (-3.7, 40.42), "Toledo": (-4.02, 39.86), "Ciudad Real": (-3.93, 38.98),
    "León": (-5.57, 42.6), "Palencia": (-4.53, 42.01), "Burgos": (-3.7, 42.34), "Soria": (-2.47, 41.76),
    "Segovia": (-4.12, 40.95), "Ávila": (-4.7, 40.66), "Salamanca": (-5.66, 40.97), "Zamora": (-5.75, 41.5),
    "Valladolid": (-4.72, 41.65), "Cáceres": (-6.37, 39.47), "Badajoz": (-6.97, 38.88), "Huelva": (-6.95, 37.26),
    "Sevilla": (-5.98, 37.39), "Córdoba": (-4.78, 37.89), "Jaén": (-3.79, 37.77), "Granada": (-3.6, 37.18),
    "Almería": (-2.46, 36.84), "Málaga": (-4.42, 36.72), "Cádiz": (-6.29, 36.53), "Illes Balears": (2.65, 39.57),
    "Ceuta": (-5.32, 35.89), "Melilla": (-2.94, 35.29),
}
_CANARIAS = {"Las Palmas": 0.72, "Santa Cruz de Tenerife": 0.28}  # posición relativa dentro del recuadro


def _slug(nombre):
    t = nombre.lower()
    for a, b in (("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"), ("ñ", "n"), (" ", "_")):
        t = t.replace(a, b)
    return t


def mapa_espana(id_, cx, cy, w=760, puntos=True, ids=False, destacar=(), col_punto=LIME, r_punto=None,
                canarias=True, ceuta_melilla=True, mar=False):
    """Mapa estilizado de España (Península, Baleares, Ceuta, Melilla y recuadro de Canarias), estilo pegatina.
    (cx, cy) = centro de la Península; w = ancho de la Península. Alto total ≈ 0,92·w con Ceuta, Melilla y Canarias.
    puntos=True dibuja las 52 capitales en el grupo `<id>_puntos`; ids=True pone cada una en `<id>_p_<slug>`
    (para cascadas). `destacar` = nombres que van aparte en `<id>_<slug>` (más grandes, coral) para pop/pulse.
    Devuelve Pieza con .puntos[nombre] = (x, y) de cada capital y .puntos["canarias"] = centro del recuadro."""
    k = w / 12.7
    lon0, lat0 = -3.0, 40.0
    def P(lon, lat):
        return (cx + (lon - lon0 + 0.0) * k, cy - (lat - lat0 - 0.0) * k * 1.31)
    r = r_punto or max(7, w * 0.012)
    out = ""
    if mar:
        out += f'<rect x="{f(cx - w*0.58)}" y="{f(cy - w*0.5)}" width="{f(w*1.16)}" height="{f(w*0.98)}" rx="30" fill="url(#mapaMar)" stroke="{INK}" stroke-width="6"/>'
    pen = [P(lo, la) for lo, la in _PENINSULA]
    d = smooth(pen, True, 0.35)
    out += f'<path d="{d}" transform="translate({f(w*0.012)} {f(w*0.016)})" fill="{INK}" opacity="0.25"/>'
    out += f'<path d="{d}" fill="url(#mapaTierra)" stroke="{INK}" stroke-width="{f(max(5, w*0.009))}" stroke-linejoin="round"/>'
    # Portugal (silueta gris para dar contexto)
    pt = [P(lo, la) for lo, la in [(-8.9, 41.9), (-8.1, 41.85), (-6.9, 41.95), (-6.4, 41.6), (-6.85, 41.0), (-7.0, 40.2),
                                   (-7.5, 39.6), (-7.1, 38.8), (-7.25, 38.2), (-7.5, 37.55), (-7.4, 37.2), (-8.0, 37.0),
                                   (-8.9, 37.0), (-8.8, 38.0), (-9.45, 38.75), (-9.0, 39.6), (-8.7, 40.6), (-8.75, 41.4)]]
    out += f'<path d="{smooth(pt, True, 0.35)}" fill="#D9DEE8" stroke="{INK}" stroke-width="{f(max(4, w*0.007))}" stroke-linejoin="round" opacity="0.9"/>'
    out += brillo(f"M {f(P(-7.6, 43.5)[0])} {f(P(-7.6, 43.5)[1])} L {f(P(-3.5, 43.3)[0])} {f(P(-3.5, 43.3)[1])}", max(4, w * 0.008), 0.75)
    for lo, la, rx, ry in _BALEARES:
        x, y = P(lo, la)
        out += f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(rx*k)}" ry="{f(ry*k*1.31)}" fill="url(#mapaTierra)" stroke="{INK}" stroke-width="{f(max(4, w*0.007))}"/>'
    pos = {}
    if ceuta_melilla:
        for nm in ("Ceuta", "Melilla"):
            x, y = P(*CAPITALES[nm])
            out += f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(r*1.6)}" ry="{f(r*1.1)}" fill="url(#mapaTierra)" stroke="{INK}" stroke-width="4"/>'
    can = None
    if canarias:
        bw, bh = w * 0.28, w * 0.12
        bx0, by0 = cx - w * 0.54, P(0, 35.75)[1] - bh / 2
        out += f'<rect x="{f(bx0)}" y="{f(by0)}" width="{f(bw)}" height="{f(bh)}" rx="12" fill="none" stroke="{INK}" stroke-width="4" stroke-dasharray="10 8"/>'
        rnd = random.Random(4)
        for i in range(7):
            ix = bx0 + bw * (0.1 + 0.8 * i / 6)
            iy = by0 + bh * (0.5 + 0.18 * math.sin(i * 1.7))
            out += f'<ellipse cx="{f(ix)}" cy="{f(iy)}" rx="{f(bw*rnd.uniform(0.035, 0.06))}" ry="{f(bh*rnd.uniform(0.12, 0.2))}" fill="url(#mapaTierra)" stroke="{INK}" stroke-width="3.5"/>'
        for nm, rel in _CANARIAS.items():
            pos[nm] = (bx0 + bw * rel, by0 + bh * 0.5)
        can = (bx0 + bw / 2, by0 + bh / 2)
    for nm, ll in CAPITALES.items():
        if nm in ("Ceuta", "Melilla") and not ceuta_melilla:
            continue
        pos[nm] = P(*ll)
    if puntos:
        dots = ""
        for nm, (x, y) in pos.items():
            if nm in destacar:
                continue
            c = (f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{col_punto}" stroke="{INK}" stroke-width="3.5"/>'
                 f'<circle cx="{f(x-r*0.3)}" cy="{f(y-r*0.35)}" r="{f(r*0.3)}" fill="#FFFFFF" opacity="0.7"/>')
            dots += g(f"{id_}_p_{_slug(nm)}", c) if ids else c
        out += g(f"{id_}_puntos", dots)
    for nm in destacar:
        x, y = pos[nm]
        R = r * 1.9
        out += g(f"{id_}_{_slug(nm)}", f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(R)}" fill="{CORAL}" stroke="{INK}" stroke-width="5"/>'
                 f'<circle cx="{f(x-R*0.3)}" cy="{f(y-R*0.35)}" r="{f(R*0.3)}" fill="#FFFFFF" opacity="0.7"/>')
    pts_ = dict(pos)
    if can:
        pts_["canarias"] = can
    return Pieza(g(id_, out), pts_, (cx - w * 0.55, cy - w * 0.4, cx + w * 0.55, cy + w * 0.5))


def balanza(id_, cx, base, w=600, inclina=0.0, izq="", der="", txt_izq=None, txt_der=None, h=None):
    """Balanza de dos platillos dorada. inclina en grados (negativo = baja el platillo izquierdo).
    izq / der: SVG que se dibuja SOBRE cada platillo, en coordenadas relativas al centro del platillo (0, 0 = encima).
    txt_izq / txt_der: rótulo en el frontal del platillo. Para que «se incline», dibuja dos balanzas (inclina 0 y ±14)
    en el mismo sitio y alterna hide/fade (dur 0.2) con el mismo trigger.
    .puntos: plato_izq, plato_der (centro de la superficie de cada platillo), fiel (punto de giro)."""
    h = h or w * 0.95
    fx, fy = cx, base - h
    L = w * 0.46
    a = math.radians(inclina)
    ex = [(fx - L * math.cos(a), fy - L * math.sin(a)), (fx + L * math.cos(a), fy + L * math.sin(a))]
    o = sombra(cx, base + 6, w * 0.4, w * 0.05)
    # pie y columna
    o += f'<path d="M {f(cx-w*0.22)} {f(base)} Q {f(cx)} {f(base-w*0.12)} {f(cx+w*0.22)} {f(base)} Z" fill="url(#balMetal)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
    o += f'<rect x="{f(cx-w*0.03)}" y="{f(fy)}" width="{f(w*0.06)}" height="{f(h-w*0.07)}" rx="8" fill="url(#balMetal)" stroke="{INK}" stroke-width="6"/>'
    o += brillo(f"M {f(cx-w*0.012)} {f(fy+20)} L {f(cx-w*0.012)} {f(base-w*0.1)}", 4, 0.7)
    platos = []
    for i, (x, y) in enumerate(ex):
        cuerda = h * 0.42
        py = y + cuerda
        pw = w * 0.36
        o += (f'<path d="M {f(x)} {f(y)} L {f(x-pw*0.42)} {f(py)} M {f(x)} {f(y)} L {f(x+pw*0.42)} {f(py)}" stroke="{INK}" stroke-width="5" fill="none"/>'
              f'<path d="M {f(x)} {f(y)} L {f(x-pw*0.42)} {f(py)} M {f(x)} {f(y)} L {f(x+pw*0.42)} {f(py)}" stroke="#E8B830" stroke-width="2" fill="none"/>')
        contenido = izq if i == 0 else der
        if contenido:
            o += f'<g transform="translate({f(x)} {f(py)})">{contenido}</g>'
        o += (f'<path d="M {f(x-pw/2)} {f(py)} Q {f(x)} {f(py+pw*0.56)} {f(x+pw/2)} {f(py)} Z" fill="url(#balPlato)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
              f'<ellipse cx="{f(x)}" cy="{f(py)}" rx="{f(pw/2)}" ry="{f(pw*0.06)}" fill="#FFF3C4" stroke="{INK}" stroke-width="5"/>')
        tx = txt_izq if i == 0 else txt_der
        if tx:
            size = min(26, pw * 0.6 / max(1, len(tx) * 0.62))
            o += T(x, py + pw * 0.105 + size * 0.36, tx, size, INK)
        platos.append((x, py))
    # brazo (cruz) encima de las cuerdas
    d = f"M {f(ex[0][0])} {f(ex[0][1])} L {f(ex[1][0])} {f(ex[1][1])}"
    o += f'<path d="{d}" stroke="{INK}" stroke-width="{f(w*0.04+8)}" stroke-linecap="round"/>'
    o += f'<path d="{d}" stroke="url(#balMetal)" stroke-width="{f(w*0.04)}" stroke-linecap="round"/>'
    o += f'<path d="{d}" stroke="#FFF6CC" stroke-width="3" stroke-linecap="round" opacity="0.8" transform="translate(0 {-w*0.008})"/>'
    for x, y in ex:
        o += f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(w*0.022)}" fill="url(#balMetal)" stroke="{INK}" stroke-width="5"/>'
    o += f'<path d="M {f(fx)} {f(fy-w*0.11)} L {f(fx-w*0.03)} {f(fy)} L {f(fx+w*0.03)} {f(fy)} Z" fill="url(#balMetal)" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    o += f'<circle cx="{f(fx)}" cy="{f(fy)}" r="{f(w*0.035)}" fill="url(#balMetal)" stroke="{INK}" stroke-width="6"/>'
    return Pieza(g(id_, o), {"plato_izq": platos[0], "plato_der": platos[1], "fiel": (fx, fy)},
                 (cx - w / 2, fy - w * 0.12, cx + w / 2, base))


def ciudad(id_, x0, x1, base, alto=420, n=7, seed=2, ventanas=True):
    """Fila de rascacielos y bloques (gran ciudad) de x0 a x1 apoyada en `base`. Las torres en `<id>_t<i>`
    (de izquierda a derecha) para hacerlas crecer en cascada con grow origin bottom."""
    rnd = random.Random(seed)
    W = (x1 - x0) / n
    out = ""
    grads = ("torreG", "torreG2", "torreG3")
    for i in range(n):
        tw = W * rnd.uniform(0.78, 0.98)
        th = alto * rnd.uniform(0.45, 1.0) if i % 3 else alto * rnd.uniform(0.85, 1.0)
        x = x0 + i * W + (W - tw) / 2
        y = base - th
        t = f'<rect x="{f(x+8)}" y="{f(y+10)}" width="{f(tw)}" height="{f(th)}" rx="6" fill="{INK}" opacity="0.2"/>'
        t += f'<rect x="{f(x)}" y="{f(y)}" width="{f(tw)}" height="{f(th)}" rx="6" fill="url(#{grads[i % 3]})" stroke="{INK}" stroke-width="6"/>'
        if i % 3 == 0:
            t += f'<path d="M {f(x+tw/2)} {f(y)} L {f(x+tw/2)} {f(y-th*0.12)}" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
            t += f'<circle cx="{f(x+tw/2)}" cy="{f(y-th*0.12)}" r="7" fill="{CORAL}" stroke="{INK}" stroke-width="3"/>'
        if ventanas:
            cols = max(2, int(tw // 34))
            filas = max(2, int(th // 46))
            vw = tw / cols * 0.5
            for c in range(cols):
                for r_ in range(filas - 1):
                    vx = x + tw / cols * (c + 0.25)
                    vy = y + 22 + r_ * 46
                    luz = "#FFE38A" if rnd.random() < 0.35 else "#E6F2FF"
                    t += f'<rect x="{f(vx)}" y="{f(vy)}" width="{f(vw)}" height="22" rx="3" fill="{luz}" stroke="{INK}" stroke-width="2.5"/>'
        t += brillo(f"M {f(x+10)} {f(y+14)} L {f(x+10)} {f(base-14)}", 5, 0.55)
        out += g(f"{id_}_t{i}", t)
    return Pieza(g(id_, out), {}, (x0, base - alto * 1.12, x1, base))


def pueblo(id_, cx, base, w=420, seed=5, iglesia=True):
    """Pueblo pequeño castellano: casitas de piedra con tejado de teja y campanario. Casas en `<id>_c<i>`."""
    rnd = random.Random(seed)
    out = sombra(cx, base + 4, w * 0.52, w * 0.04)
    out += f'<path d="M {f(cx-w*0.56)} {f(base)} Q {f(cx)} {f(base-w*0.16)} {f(cx+w*0.56)} {f(base)} Z" fill="{degradado("#9BD36A", 0.25)}" stroke="{INK}" stroke-width="6"/>'
    out += "<!--iglesia-->"
    xs = [cx - w * 0.38, cx - w * 0.12, cx + w * 0.14, cx + w * 0.38]
    for i, x in enumerate(xs):
        hw = w * rnd.uniform(0.17, 0.21)
        hh = hw * rnd.uniform(0.7, 0.9)
        y = base - hh - (w * 0.03 if 0 < i < 3 else 0)
        c = f'<rect x="{f(x-hw/2+5)}" y="{f(y+7)}" width="{f(hw)}" height="{f(hh)}" fill="{INK}" opacity="0.2"/>'
        c += f'<rect x="{f(x-hw/2)}" y="{f(y)}" width="{f(hw)}" height="{f(hh)}" fill="url(#piedraG)" stroke="{INK}" stroke-width="5"/>'
        c += f'<path d="M {f(x-hw*0.62)} {f(y+3)} L {f(x)} {f(y-hw*0.4)} L {f(x+hw*0.62)} {f(y+3)} Z" fill="url(#tejaG)" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
        c += f'<rect x="{f(x-hw*0.12)}" y="{f(y+hh*0.45)}" width="{f(hw*0.24)}" height="{f(hh*0.55)}" rx="3" fill="#8A5A31" stroke="{INK}" stroke-width="3.5"/>'
        c += f'<rect x="{f(x+hw*0.18)}" y="{f(y+hh*0.22)}" width="{f(hw*0.18)}" height="{f(hw*0.16)}" rx="2" fill="#BFE6FF" stroke="{INK}" stroke-width="3"/>'
        out += g(f"{id_}_c{i}", c)
    if iglesia:
        tx = cx + w * 0.01
        tw = w * 0.11
        th = w * 0.42
        ty = base - th - w * 0.04
        c = f'<rect x="{f(tx-tw/2)}" y="{f(ty)}" width="{f(tw)}" height="{f(th)}" fill="url(#piedraG)" stroke="{INK}" stroke-width="5"/>'
        c += f'<path d="M {f(tx-tw*0.65)} {f(ty+2)} L {f(tx)} {f(ty-tw*0.9)} L {f(tx+tw*0.65)} {f(ty+2)} Z" fill="url(#tejaG)" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
        c += f'<path d="M {f(tx-tw*0.2)} {f(ty+th*0.35)} L {f(tx-tw*0.2)} {f(ty+th*0.18)} Q {f(tx)} {f(ty+th*0.08)} {f(tx+tw*0.2)} {f(ty+th*0.18)} L {f(tx+tw*0.2)} {f(ty+th*0.35)} Z" fill="{INK}"/>'
        c += f'<circle cx="{f(tx)}" cy="{f(ty+th*0.27)}" r="{f(tw*0.12)}" fill="{YEL}" stroke="{INK}" stroke-width="2.5"/>'
        out = out.replace("<!--iglesia-->", g(f"{id_}_iglesia", c))
    return Pieza(g(id_, out), {}, (cx - w * 0.56, base - w * 0.55, cx + w * 0.56, base))

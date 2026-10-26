"""Nervios y hormigueo: pierna de perfil con nervio y vaso a la vista (normal y aplastada), tubos de nervio y vaso
en corte, haz de fibras que se encienden, rodilla lateral con el nervio peroneo, hormiga, aguja de pinchazo y textura
de corcho («pierna dormida»).

Sale de: lote9-02-pierna-dormida (archivo/pierna-dormida/dib.py), «¿por qué se te duerme la pierna?».
Método de movimiento (skill rossark): cada parte va en su propio grupo con su pivote (pierna de arriba en la cadera,
aguja en su base, hormiga en su centro) y cada repetido (fibras, glóbulos, hormigas) tiene su id para darle su fase.
"""
import math
import random
from ..base import (INK, LIME, CORAL, YEL, f, g, gt, T, DISP, shade, trazo, sombra, brillo, lg, rg, registrar_defs,
                    degradado, Pieza, smooth)
from ..personajes import PIELES

NERVIO = "#FFC83D"
NERVIO_OSC = "#C98A12"
SANGRE = "#E0313F"

registrar_defs(
    lg("nvNervio", [(0, "#FFE48A"), (0.55, "#FFC83D"), (1, "#C98A12")])
    + lg("nvVaso", [(0, "#FF7A7A"), (0.55, "#E0313F"), (1, "#8E1626")])
    + lg("nvVasoIn", [(0, "#B3192B"), (1, "#6E0E1C")])
    + lg("nvFibraOff", [(0, "#8C93A6"), (1, "#4E5468")])
    + lg("nvFibraOn", [(0, "#F4FFB8"), (0.5, "#C8FF2E"), (1, "#7FB800")])
    + lg("nvTejido", [(0, "#F6B7A8"), (1, "#D9867A")])
    + lg("nvHueso", [(0, "#FFFDF4"), (1, "#E2D6B8")], 0, 0, 1, 0)
    + lg("nvAguja", [(0, "#FFFFFF"), (0.5, "#C9D2DE"), (1, "#7D8899")], 0, 0, 1, 0)
    + rg("nvGlobulo", [(0, "#FF8A8A"), (0.6, "#E0313F"), (1, "#9C1424")], 0.4, 0.35, 0.7)
    + rg("nvO2", [(0, "#E6F6FF"), (0.6, "#7CC8FF"), (1, "#2F86D9")], 0.4, 0.35, 0.7)
)


def _uid(pre, *v):
    return pre + "_" + "_".join(str(int(x)) for x in v)


# ----------------------------------------------------------------------------- corcho y hormiga
def corcho(seed=3):
    """Textura de corcho (pattern) para pintar una pierna «dormida». Devuelve 'url(#nvCorcho)'."""
    rnd = random.Random(seed)
    o = '<rect width="90" height="90" fill="#C9965C"/>'
    for _ in range(26):
        x, y, r = rnd.uniform(0, 90), rnd.uniform(0, 90), rnd.uniform(2, 6)
        col = rnd.choice(("#8A5A2E", "#9E6A38", "#E4BE84", "#B07E46", "#6E4422"))
        o += f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(r)}" ry="{f(r*rnd.uniform(0.5, 1))}" fill="{col}" opacity="0.9"/>'
    registrar_defs(f'<pattern id="nvCorcho" patternUnits="userSpaceOnUse" width="90" height="90">{o}</pattern>')
    return "url(#nvCorcho)"


def hormiga(id_, cx, cy, s=1.0, ang=-90, col="#2A1A14"):
    """Hormiga vista desde arriba (≈ 44×64 a s=1), cabeza hacia `ang` (-90 = arriba). Tres segmentos, seis patas y
    antenas; las patas van en {id}_patas (wiggle = andar)."""
    sw = 3.2
    o = ""
    pat = ""
    for k in (-1, 1):
        for j, (y0, a) in enumerate(((-6, -35), (2, 0), (10, 35))):
            x1, y1 = k * 20, y0 + a * 0.35
            pat += (f'<path d="M 0 {y0} L {f(k*11)} {f(y0 - 4 + j*3)} L {f(x1)} {f(y1)}" fill="none" stroke="{col}" '
                    f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>')
    o += g(f"{id_}_patas" if id_ else None, pat)
    o += f'<ellipse cx="0" cy="18" rx="9" ry="12" fill="{col}" stroke="{INK}" stroke-width="2"/>'
    o += f'<ellipse cx="0" cy="2" rx="6" ry="8" fill="{col}" stroke="{INK}" stroke-width="2"/>'
    o += f'<circle cx="0" cy="-12" r="7" fill="{col}" stroke="{INK}" stroke-width="2"/>'
    o += (f'<path d="M -3 -17 Q -8 -26 -13 -28 M 3 -17 Q 8 -26 13 -28" fill="none" stroke="{col}" stroke-width="2.6" '
          f'stroke-linecap="round"/>')
    o += f'<ellipse cx="-2.5" cy="15" rx="3" ry="4" fill="#FFFFFF" opacity="0.35"/>'
    return gt(id_, f"translate({f(cx)} {f(cy)}) rotate({f(ang + 90)}) scale({f(s)})", o)


def aguja(id_, cx, cy, L=120, ang=-90, w=14):
    """Aguja de pinchazo con la punta en (cx, cy) apuntando hacia `ang` (grados; -90 = hacia arriba). Base gruesa en
    el otro extremo (pivote para punch/wiggle)."""
    o = (f'<path d="M 0 0 L {f(-L*0.28)} {f(-w*0.32)} L {f(-L)} {f(-w*0.5)} Q {f(-L-w*0.6)} 0 {f(-L)} {f(w*0.5)} '
         f'L {f(-L*0.28)} {f(w*0.32)} Z" fill="url(#nvAguja)" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
         f'<ellipse cx="{f(-L*0.86)}" cy="0" rx="{f(w*0.5)}" ry="{f(w*0.18)}" fill="{INK}" opacity="0.7"/>'
         + brillo(f"M {f(-L*0.75)} {f(-w*0.22)} L {f(-L*0.3)} {f(-w*0.12)}", 2.5, 0.9))
    return gt(id_, f"translate({f(cx)} {f(cy)}) rotate({f(ang)})", o)


# ----------------------------------------------------------------------------- pierna con nervio y vaso
def _cinta(pts, ws):
    """Contorno de una cinta de anchura variable a lo largo de pts (semianchos ws)."""
    izq, der = [], []
    n = len(pts)
    for i, (x, y) in enumerate(pts):
        a = pts[min(i + 1, n - 1)]
        b = pts[max(i - 1, 0)]
        dx, dy = a[0] - b[0], a[1] - b[1]
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L, dx / L
        izq.append((x + nx * ws[i], y + ny * ws[i]))
        der.append((x - nx * ws[i], y - ny * ws[i]))
    return smooth(izq + der[::-1], True, 0.35)


def _pierna_eje(x0, cy, L, s):
    """Eje de la pierna sentada: cadera → rodilla (horizontal) → tobillo (hacia abajo)."""
    kx = x0 + L * 0.62
    ank = (kx + 40 * s, cy + L * 0.42)
    return (x0, cy), (kx, cy), ank


def pierna_nervio(id_, x0, cy, L=760, s=1.0, piel="media", pres=0.42, short_col="#3A4256", vaso=True, apretada=0.75):
    """Pierna sentada de perfil (muslo horizontal hacia la derecha, rodilla, espinilla hacia abajo y pie) con el nervio
    amarillo y el vaso rojo a la vista bajo la piel. (x0, cy) = cadera (tapada por el borde del pantalón corto).
    Dibuja las dos versiones del nervio y del vaso en el mismo sitio: {id}_nervio / {id}_nervio_apl y {id}_vaso /
    {id}_vaso_apl (estrechados en `pres`, fracción del muslo): oculta las «_apl» al principio y alterna con hide/fade.
    Ids: {id}_piel, {id}_pie. .puntos: cadera, rodilla, tobillo, presion (encima del muslo en `pres`),
    apriete (sobre el nervio en `pres`), nervio (lista de puntos del nervio, de la cadera al pie), contorno (d de la piel,
    para pintar encima un velo gris de «pierna dormida»)."""
    pa, pb, pc, pl = PIELES.get(piel, PIELES["media"])
    H, K, A = _pierna_eje(x0, cy, L, s)
    t0, tk, ta = 74 * s, 60 * s, 34 * s
    kx = K[0]
    # contorno de la piel en un solo trazo (sin costuras): arriba del muslo, rodilla, espinilla delante, pie, detrás, abajo
    top = [(x0, cy - t0), (x0 + L * 0.3, cy - t0 * 1.02), (kx - 30 * s, cy - tk), (kx + 40 * s, cy - tk * 0.9),
           (kx + tk * 0.95, cy - tk * 0.15)]
    frente = [(kx + tk * 0.95, cy + tk * 0.4), (A[0] + ta * 1.0, A[1] - L * 0.2), (A[0] + ta * 0.9, A[1] - 8 * s)]
    pie = [(A[0] + ta * 1.3, A[1] + 6 * s), (A[0] + ta + 120 * s, A[1] + 28 * s), (A[0] + ta + 128 * s, A[1] + 52 * s),
           (A[0] - ta * 0.9, A[1] + 54 * s)]
    detras = [(A[0] - ta * 1.0, A[1] - 6 * s), (kx - tk * 0.75, cy + L * 0.2), (kx - tk * 0.9, cy + tk * 0.95),
              (x0 + L * 0.3, cy + t0 * 1.0), (x0, cy + t0)]
    d = smooth(top + frente + pie + detras, True, 0.22)
    cid = _uid("nvPierna", x0, cy)
    piel_svg = (f'<clipPath id="{cid}"><path d="{d}"/></clipPath>'
                f'<path d="{d}" fill="url(#piel_{piel})" stroke="{INK}" stroke-width="{f(8*s)}" stroke-linejoin="round"/>')
    # rótula y brillo
    piel_svg += f'<path d="M {f(kx+tk*0.55)} {f(cy-tk*0.7)} Q {f(kx+tk*1.0)} {f(cy-tk*0.1)} {f(kx+tk*0.6)} {f(cy+tk*0.5)}" fill="none" stroke="{pl}" stroke-width="{f(4*s)}" stroke-linecap="round" opacity="0.7"/>'
    piel_svg += brillo(f"M {f(x0+60*s)} {f(cy-t0*0.72)} Q {f(x0+L*0.3)} {f(cy-t0*0.86)} {f(kx-40*s)} {f(cy-tk*0.7)}", 6 * s, 0.55)
    # nervio: por la parte de atrás del muslo, detrás de la rodilla y por la pantorrilla
    nv = [(x0 - 10 * s, cy + t0 * 0.38), (x0 + L * 0.2, cy + t0 * 0.4), (x0 + L * 0.42, cy + t0 * 0.42),
          (kx - 40 * s, cy + tk * 0.45), (kx - tk * 0.2, cy + tk * 0.9), (kx - tk * 0.15, cy + L * 0.18),
          (A[0] - ta * 0.3, A[1] - 30 * s), (A[0] + 20 * s, A[1] + 26 * s)]
    vs = [(x0 - 10 * s, cy - t0 * 0.12), (x0 + L * 0.2, cy - t0 * 0.12), (x0 + L * 0.42, cy - t0 * 0.08),
          (kx - 30 * s, cy + tk * 0.05), (kx, cy + tk * 0.5), (kx + 6 * s, cy + L * 0.18),
          (A[0] - ta * 0.05, A[1] - 34 * s), (A[0] + 40 * s, A[1] + 22 * s)]

    def denso(p, n=60):
        out = []
        for i in range(len(p) - 1):
            for j in range(n // (len(p) - 1)):
                u = j / (n // (len(p) - 1))
                out.append((p[i][0] + (p[i + 1][0] - p[i][0]) * u, p[i][1] + (p[i + 1][1] - p[i][1]) * u))
        out.append(p[-1])
        return out

    px = x0 + L * pres

    def anchos(p, w0, apl):
        ws = []
        for (x, y) in p:
            k = 1.0
            if apl:
                dd = abs(x - px) / (70 * s)
                k = 1 - apretada * math.exp(-dd * dd) if y < cy + t0 else 1.0
            ws.append(w0 * k)
        return ws

    nvd, vsd = denso(nv), denso(vs)
    halo = f'<path d="M {" L ".join(f"{f(x)} {f(y)}" for x, y in nvd)}" fill="none" stroke="#D9867A" stroke-width="{f(40*s)}" stroke-linecap="round" stroke-linejoin="round" opacity="0.45"/>'
    if vaso:
        halo += f'<path d="M {" L ".join(f"{f(x)} {f(y)}" for x, y in vsd)}" fill="none" stroke="#D9867A" stroke-width="{f(36*s)}" stroke-linecap="round" stroke-linejoin="round" opacity="0.4"/>'

    def tubo(p, w0, fill, apl, brillo_col):
        dd = _cinta(p, anchos(p, w0, apl))
        o = f'<path d="{dd}" fill="{fill}" stroke="{INK}" stroke-width="{f(4.5*s)}" stroke-linejoin="round"/>'
        o += f'<path d="M {" L ".join(f"{f(x)} {f(y - w0*0.35)}" for x, y in p[2:-6:2])}" fill="none" stroke="{brillo_col}" stroke-width="{f(3*s)}" stroke-linecap="round" opacity="0.8" stroke-dasharray="{f(18*s)} {f(14*s)}"/>'
        return o

    interior = halo
    if vaso:
        interior += g(f"{id_}_vaso", tubo(vsd, 11 * s, "url(#nvVaso)", False, "#FFC4C4"))
        interior += g(f"{id_}_vaso_apl", tubo(vsd, 11 * s, "url(#nvVaso)", True, "#FFC4C4"))
    interior += g(f"{id_}_nervio", tubo(nvd, 12 * s, "url(#nvNervio)", False, "#FFF6C8"))
    interior += g(f"{id_}_nervio_apl", tubo(nvd, 12 * s, "url(#nvNervio)", True, "#FFF6C8"))
    piel_svg += f'<g clip-path="url(#{cid})">{interior}</g>'
    # borde del pantalón corto (tapa la cadera)
    sh = (f'<path d="M {f(x0-40*s)} {f(cy-t0-14*s)} L {f(x0+70*s)} {f(cy-t0-10*s)} Q {f(x0+92*s)} {f(cy)} {f(x0+76*s)} {f(cy+t0+12*s)} '
          f'L {f(x0-40*s)} {f(cy+t0+16*s)} Z" fill="{degradado(short_col, 0.25)}" stroke="{INK}" stroke-width="{f(7*s)}" stroke-linejoin="round"/>'
          + f'<path d="M {f(x0+58*s)} {f(cy-t0)} Q {f(x0+78*s)} {f(cy)} {f(x0+64*s)} {f(cy+t0)}" fill="none" stroke="{shade(short_col, 0.4)}" stroke-width="{f(4*s)}" stroke-dasharray="{f(10*s)} {f(8*s)}"/>')
    yv = min(y for x, y in nvd if abs(x - px) < 20 * s) if any(abs(x - px) < 20 * s for x, y in nvd) else cy + t0 * 0.4
    pts_ = {"cadera": H, "rodilla": K, "tobillo": A, "presion": (px, cy - t0 * 1.02), "apriete": (px, yv), "nervio": nvd,
            "vaso": vsd, "contorno": d}
    return Pieza(g(f"{id_}_piel", piel_svg) + sh, pts_, (x0 - 40 * s, cy - t0 - 16 * s, A[0] + ta + 130 * s, A[1] + 56 * s))


def pierna_encima(id_, x0, y0, x1, y1, s=1.0, piel="media", short_col="#3A4256"):
    """La otra pierna cruzada por encima, de perfil: muslo de la cadera (x0, y0) a la rodilla (x1, y1), que apoya en
    la pierna de abajo. Devuelve (espinilla, muslo): dibuja `espinilla` ANTES de la pierna de abajo (cuelga por detrás)
    y `muslo` después. Ids {id}_esp, {id}_muslo; anímalos juntos con move (bajar = cruzar)."""
    t = 66 * s
    dx, dy = x1 - x0, y1 - y0
    a = math.degrees(math.atan2(dy, dx))
    Lm = math.hypot(dx, dy)
    mus = (f'<g transform="translate({f(x0)} {f(y0)}) rotate({f(a)})">'
           f'<path d="M 0 {f(-t)} Q {f(Lm*0.5)} {f(-t*1.08)} {f(Lm)} {f(-t*0.86)} A {f(t*0.9)} {f(t*0.9)} 0 0 1 {f(Lm)} {f(t*0.86)} '
           f'Q {f(Lm*0.5)} {f(t*1.02)} 0 {f(t)} Z" fill="url(#piel_{piel})" stroke="{INK}" stroke-width="{f(8*s)}" stroke-linejoin="round"/>'
           + brillo(f"M {f(60*s)} {f(-t*0.7)} Q {f(Lm*0.5)} {f(-t*0.86)} {f(Lm-30*s)} {f(-t*0.62)}", 6 * s, 0.55)
           + f'<path d="M -40 {f(-t-14*s)} L {f(70*s)} {f(-t-10*s)} Q {f(92*s)} 0 {f(76*s)} {f(t+12*s)} L -40 {f(t+16*s)} Z" '
           f'fill="{degradado(short_col, 0.25)}" stroke="{INK}" stroke-width="{f(7*s)}" stroke-linejoin="round"/></g>')
    # espinilla que cuelga por detrás de la otra pierna
    ex, ey = x1 + 70 * s, y1 + 330 * s
    esp = (trazo(f"M {f(x1)} {f(y1)} L {f(ex)} {f(ey)}", 76 * s, PIELES.get(piel, PIELES['media'])[2], 8 * s)
           + f'<path d="M {f(ex-34*s)} {f(ey+10*s)} Q {f(ex+20*s)} {f(ey+20*s)} {f(ex+110*s)} {f(ey+40*s)} Q {f(ex+120*s)} {f(ey+66*s)} {f(ex-30*s)} {f(ey+62*s)} Z" '
           f'fill="{PIELES.get(piel, PIELES["media"])[2]}" stroke="{INK}" stroke-width="{f(7*s)}" stroke-linejoin="round"/>')
    return (Pieza(g(f"{id_}_esp", esp), {"pie": (ex, ey)}, (x1 - 40 * s, y1, ex + 120 * s, ey + 70 * s)),
            Pieza(g(f"{id_}_muslo", mus), {"rodilla": (x1, y1), "abajo": (x1, y1 + t * 0.9)}, (x0 - 40 * s, min(y0, y1) - t, x1 + t, max(y0, y1) + t)))


# ----------------------------------------------------------------------------- tubos en corte (zoom)
def vaso_tubo(id_, x0, x1, cy, r=48, estrecho=None, k=0.35):
    """Vaso sanguíneo horizontal en corte (pared roja, luz oscura). estrecho = x donde lo aprieta algo (se estrecha a
    k del radio). .puntos: centro(x) = y del centro, luz = radio interior en cada x (función)."""
    n = 40
    xs = [x0 + (x1 - x0) * i / n for i in range(n + 1)]

    def rr(x):
        if estrecho is None:
            return r
        d = (x - estrecho) / (r * 1.8)
        return r * (1 - (1 - k) * math.exp(-d * d))

    up = [(x, cy - rr(x)) for x in xs]
    dn = [(x, cy + rr(x)) for x in xs[::-1]]
    d = "M " + " L ".join(f"{f(x)} {f(y)}" for x, y in up + dn) + " Z"
    inn_up = [(x, cy - rr(x) * 0.62) for x in xs]
    inn_dn = [(x, cy + rr(x) * 0.62) for x in xs[::-1]]
    d2 = "M " + " L ".join(f"{f(x)} {f(y)}" for x, y in inn_up + inn_dn) + " Z"
    o = (f'<path d="{d}" fill="url(#nvVaso)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
         f'<path d="{d2}" fill="url(#nvVasoIn)"/>'
         + brillo("M " + " L ".join(f"{f(x)} {f(y + rr(x)*0.18)}" for x, y in up[2:-2]), 5, 0.6))
    p = Pieza(g(id_, o), {"centro": (x0 + x1) / 2}, (x0, cy - r, x1, cy + r))
    p.puntos["luz"] = lambda x: rr(x) * 0.62
    return p


def nervio_tubo(id_, x0, x1, cy, r=70, n=7, estrecho=None, k=0.55):
    """Nervio horizontal en corte: vaina amarilla con `n` fibras finas dentro (cada una en {id}_f<i>). estrecho = x donde
    lo aprieta algo. .puntos: fibras (lista de y de cada fibra)."""
    m = 40
    xs = [x0 + (x1 - x0) * i / m for i in range(m + 1)]

    def rr(x):
        if estrecho is None:
            return r
        d = (x - estrecho) / (r * 1.5)
        return r * (1 - (1 - k) * math.exp(-d * d))

    up = [(x, cy - rr(x)) for x in xs]
    dn = [(x, cy + rr(x)) for x in xs[::-1]]
    d = "M " + " L ".join(f"{f(x)} {f(y)}" for x, y in up + dn) + " Z"
    o = f'<path d="{d}" fill="url(#nvNervio)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
    ys = []
    for i in range(n):
        u = (i + 0.5) / n * 2 - 1           # -1..1
        path = "M " + " L ".join(f"{f(x)} {f(cy + u * rr(x) * 0.78)}" for x in xs)
        o += g(f"{id_}_f{i}" if id_ else None, f'<path d="{path}" fill="none" stroke="{NERVIO_OSC}" stroke-width="{f(r*1.2/n)}" stroke-linecap="round" opacity="0.75"/>')
        ys.append(cy + u * r * 0.78)
    o += brillo("M " + " L ".join(f"{f(x)} {f(y + rr(x)*0.12)}" for x, y in up[2:-2]), 6, 0.7)
    return Pieza(g(id_, o), {"fibras": ys}, (x0, cy - r, x1, cy + r))


def globulo(id_, cx, cy, r=26, ang=0):
    """Glóbulo rojo (disco con el centro hundido), visto algo inclinado."""
    o = (f'<ellipse cx="0" cy="0" rx="{f(r)}" ry="{f(r*0.78)}" fill="url(#nvGlobulo)" stroke="{INK}" stroke-width="{f(max(3, r*0.16))}"/>'
         f'<ellipse cx="{f(r*0.05)}" cy="{f(r*0.06)}" rx="{f(r*0.48)}" ry="{f(r*0.32)}" fill="#B71C2C" opacity="0.75"/>'
         f'<path d="M {f(-r*0.6)} {f(-r*0.35)} Q {f(-r*0.1)} {f(-r*0.7)} {f(r*0.45)} {f(-r*0.45)}" fill="none" stroke="#FFFFFF" stroke-width="{f(max(2, r*0.12))}" stroke-linecap="round" opacity="0.7"/>')
    return gt(id_, f"translate({f(cx)} {f(cy)}) rotate({f(ang)})", o)


def burbuja_o2(id_, cx, cy, r=26):
    """Burbujita de oxígeno azul con «O₂»."""
    return g(id_, f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="url(#nvO2)" stroke="{INK}" stroke-width="4"/>'
             + T(cx, cy + r * 0.32, "O₂", r * 0.9, INK, font=DISP)
             + f'<circle cx="{f(cx - r*0.45)}" cy="{f(cy - r*0.45)}" r="{f(r*0.18)}" fill="#FFFFFF"/>')


def haz_fibras(id_, x0, x1, cy, h=420, n=10, seed=5):
    """Nervio grande en corte longitudinal con `n` fibras que pueden «encenderse»: cada fibra apagada en {id}_f<i> (gris)
    y encendida en {id}_on<i> (lima, en el mismo sitio, para fade/pop + pulse a destiempo). Vaina amarilla alrededor.
    .puntos: fibras (lista de (y, grosor)), caja."""
    rnd = random.Random(seed)
    r = h / 2
    o = (f'<rect x="{f(x0)}" y="{f(cy-r)}" width="{f(x1-x0)}" height="{f(h)}" rx="{f(r*0.5)}" fill="url(#nvNervio)" stroke="{INK}" stroke-width="9"/>'
         f'<rect x="{f(x0+18)}" y="{f(cy-r+18)}" width="{f(x1-x0-36)}" height="{f(h-36)}" rx="{f(r*0.4)}" fill="#5A3A10" opacity="0.55"/>')
    o += brillo(f"M {f(x0+r*0.5)} {f(cy-r+10)} L {f(x1-r*0.5)} {f(cy-r+10)}", 7, 0.7)
    fibras = []
    gap = (h - 60) / n
    apag, enc = "", ""
    for i in range(n):
        y = cy - r + 30 + gap * (i + 0.5)
        w = gap * 0.62
        amp = rnd.uniform(4, 9)
        ph = rnd.uniform(0, 6.28)
        xs = [x0 + 40 + (x1 - x0 - 80) * j / 30 for j in range(31)]
        path = "M " + " L ".join(f"{f(x)} {f(y + amp * math.sin(ph + j * 0.45))}" for j, x in enumerate(xs))
        apag += g(f"{id_}_f{i}", f'<path d="{path}" fill="none" stroke="{INK}" stroke-width="{f(w+6)}" stroke-linecap="round"/>'
                  f'<path d="{path}" fill="none" stroke="url(#nvFibraOff)" stroke-width="{f(w)}" stroke-linecap="round"/>')
        enc += g(f"{id_}_on{i}", f'<path d="{path}" fill="none" stroke="{LIME}" stroke-width="{f(w+18)}" stroke-linecap="round" opacity="0.28"/>'
                 f'<path d="{path}" fill="none" stroke="{INK}" stroke-width="{f(w+6)}" stroke-linecap="round"/>'
                 f'<path d="{path}" fill="none" stroke="url(#nvFibraOn)" stroke-width="{f(w)}" stroke-linecap="round"/>'
                 f'<path d="{path}" fill="none" stroke="#FFFFFF" stroke-width="{f(w*0.22)}" stroke-linecap="round" opacity="0.7" transform="translate(0 {f(-w*0.18)})"/>')
        fibras.append((y, w))
    o += apag + enc
    return Pieza(g(id_, o), {"fibras": fibras}, (x0, cy - r, x1, cy + r))


# ----------------------------------------------------------------------------- rodilla con el peroneo
def rodilla_lateral(id_, cx, cy, s=1.0, piel="media"):
    """Rodilla vista de lado (la de fuera), con la piel semitransparente: fémur arriba, rótula delante, tibia y peroné
    abajo y el nervio peroneo amarillo que baja por detrás y rodea la cabeza del peroné por fuera ({id}_nervio, un
    solo trazo para draw). (cx, cy) = centro de la articulación. Ids {id}_piel, {id}_huesos, {id}_nervio.
    .puntos: peroneo (donde el nervio rodea el peroné, el punto que se aplasta), rotula, femur, tobillo."""
    pa, pb, pc, pl = PIELES.get(piel, PIELES["media"])

    def P(x, y):
        return (cx + x * s, cy + y * s)

    def D(pp):
        return smooth([P(x, y) for x, y in pp], True, 0.3)

    piel_d = D([(-150, -430), (130, -430), (150, -200), (175, -40), (160, 80), (110, 200), (95, 430), (-120, 430),
                (-130, 200), (-175, 40), (-165, -120)])
    o = f'<path d="{piel_d}" fill="{shade(pa, 0.35)}" stroke="{INK}" stroke-width="{f(8*s)}" stroke-linejoin="round"/>'
    o += f'<path d="{piel_d}" fill="url(#piel_{piel})" opacity="0.35"/>'
    hue = ""
    # fémur
    hue += f'<path d="{D([(-62, -440), (50, -440), (60, -120), (110, -50), (95, 10), (-110, 10), (-125, -60), (-68, -130)])}" fill="url(#nvHueso)" stroke="{INK}" stroke-width="{f(6*s)}"/>'
    # tibia
    hue += f'<path d="{D([(-100, 40), (95, 40), (90, 110), (45, 170), (40, 440), (-50, 440), (-55, 170), (-105, 110)])}" fill="url(#nvHueso)" stroke="{INK}" stroke-width="{f(6*s)}"/>'
    # peroné (detrás, más fino) con su cabeza
    hue += f'<path d="{D([(-150, 100), (-95, 92), (-92, 140), (-108, 170), (-108, 440), (-140, 440), (-140, 170), (-160, 140)])}" fill="url(#nvHueso)" stroke="{INK}" stroke-width="{f(6*s)}"/>'
    # rótula
    hue += f'<ellipse cx="{f(P(118, -40)[0])}" cy="{f(P(118, -40)[1])}" rx="{f(40*s)}" ry="{f(58*s)}" fill="url(#nvHueso)" stroke="{INK}" stroke-width="{f(6*s)}"/>'
    hue += brillo(f"M {f(P(-30, -400)[0])} {f(P(-30, -400)[1])} L {f(P(-24, -160)[0])} {f(P(-24, -160)[1])}", 5 * s, 0.8)
    hue += brillo(f"M {f(P(-10, 200)[0])} {f(P(-10, 200)[1])} L {f(P(-8, 400)[0])} {f(P(-8, 400)[1])}", 5 * s, 0.8)
    o += g(f"{id_}_huesos", hue)
    o += f'<path d="{piel_d}" fill="none" stroke="{INK}" stroke-width="{f(8*s)}" stroke-linejoin="round"/>'
    # nervio peroneo: baja por detrás del muslo, rodea el cuello del peroné por fuera y se va hacia delante
    nv = [P(-150, -430), P(-140, -250), P(-150, -60), P(-170, 70), P(-150, 160), P(-100, 190), P(-40, 210), P(10, 260), P(20, 420)]
    dn = smooth(nv, False, 0.35)
    o += g(f"{id_}_nervio", f'<path d="{dn}" fill="none" stroke="{INK}" stroke-width="{f(24*s)}" stroke-linecap="round" stroke-linejoin="round"/>'
           f'<path d="{dn}" fill="none" stroke="{NERVIO}" stroke-width="{f(14*s)}" stroke-linecap="round" stroke-linejoin="round"/>')
    pts_ = {"peroneo": P(-150, 165), "rotula": P(118, -40), "femur": P(0, -300), "tobillo": P(0, 430)}
    return Pieza(g(id_, o), pts_, (cx - 180 * s, cy - 440 * s, cx + 180 * s, cy + 440 * s))


def nervio_lupa(cx, cy, r, aplastado=True):
    """Contenido para base.lupa(): un trozo de nervio (y el borde del peroné) visto de cerca, aplastado o no."""
    o = f'<rect x="{f(cx-r)}" y="{f(cy-r)}" width="{f(2*r)}" height="{f(2*r)}" fill="#F2B6A2"/>'
    o += f'<path d="M {f(cx-r)} {f(cy+r*0.55)} Q {f(cx)} {f(cy+r*0.35)} {f(cx+r)} {f(cy+r*0.55)} L {f(cx+r)} {f(cy+r)} L {f(cx-r)} {f(cy+r)} Z" fill="url(#nvHueso)" stroke="{INK}" stroke-width="6"/>'
    p = nervio_tubo(None, cx - r * 1.1, cx + r * 1.1, cy, r * 0.32, n=5, estrecho=cx if aplastado else None, k=0.38)
    return o + p

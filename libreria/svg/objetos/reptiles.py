"""Reptiles y agua: basilisco corriendo sobre el agua, su pata con flecos de escamas, la pisada en corte (pata lateral,
bolsa de aire, salpicadura, agua en corte), revista científica y fondo de río en la selva.

Sale de: lote8-07-basilisco («¿Cómo corre el basilisco sobre el agua?»).
"""
import math as _m
import random

from ..base import (INK, LIME, CORAL, f, g, gt, T, trazo, brillo, sombra, smooth, lg, rg, registrar_defs, degradado,
                    Pieza, shade, MONO, DISP)

registrar_defs(
    lg("basilG", [(0, "#A6F07A"), (0.5, "#45B84B"), (1, "#22793A")]),
    lg("basilBarriga", [(0, "#F4F7A8"), (1, "#C9D96A")]),
    lg("basilOsc", [(0, "#3E9E45"), (1, "#1B5C2D")]),
    lg("aguaCorte", [(0, "#5FB4F0"), (0.5, "#2F7FD6"), (1, "#1A4FA0")]),
    lg("aguaSup", [(0, "#BFE6FF"), (1, "#5FB4F0")]),
    rg("bolsaAireG", [(0, "#FFFFFF"), (0.6, "#E6F6FF"), (1, "#A9DBF7")], 0.4, 0.35, 0.7),
    lg("cieloSelva", [(0, "#8FD3FF"), (1, "#E8F7FF")]),
    lg("rioG", [(0, "#4FA9E8"), (0.45, "#2F7FD6"), (1, "#1C5AAE")]),
)

VERDE_B, VERDE_C, VERDE_O = "#45B84B", "#A6F07A", "#22793A"


def _dedo_flecos(p0, p1, ancho, col, flecos=True, n=5, lado=1):
    """Dedo largo de p0 a p1 con flecos de escamas a los lados (triangulitos claros)."""
    o = trazo(f"M {f(p0[0])} {f(p0[1])} L {f(p1[0])} {f(p1[1])}", ancho, col, 7)
    if not flecos:
        return o
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    L = _m.hypot(dx, dy) or 1
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux
    fl = ""
    for k in (-1, 1):
        for i in range(n):
            t = 0.2 + 0.75 * i / max(1, n - 1)
            bx, by = p0[0] + dx * t, p0[1] + dy * t
            ox, oy = bx + nx * k * ancho * 0.5, by + ny * k * ancho * 0.5
            tip = (ox + nx * k * ancho * 0.75 + ux * ancho * 0.25, oy + ny * k * ancho * 0.75 + uy * ancho * 0.25)
            a = (ox - ux * ancho * 0.3, oy - uy * ancho * 0.3)
            b = (ox + ux * ancho * 0.45, oy + uy * ancho * 0.45)
            fl += (f'<path d="M {f(a[0])} {f(a[1])} L {f(tip[0])} {f(tip[1])} L {f(b[0])} {f(b[1])} Z" fill="#E9F9B0" '
                   f'stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>')
    return fl + o


def _pie_lado(x, y, s, col, ang=0, flecos=True):
    """Pie de basilisco visto de lado: talón en (x, y), dedos hacia delante (derecha) con flecos debajo."""
    o = ""
    for i, (dx, dy) in enumerate(((95, 6), (80, 16), (62, -6))):
        o += _dedo_flecos((0, 0), (dx, dy), 13, col if i != 2 else shade(col, -0.15), flecos, 4)
    return f'<g transform="translate({f(x)} {f(y)}) rotate({f(ang)}) scale({f(s)})">{o}</g>'


def basilisco(id_, cx, cy, s=1.0, pose="a", espejo=False, rot_=0):
    """Basilisco verde (lagarto Jesucristo) corriendo a dos patas, de perfil, morro a la derecha.
    (cx, cy) = cadera; la pata apoyada llega a cy + 150*s (nivel del agua). Largo ≈ 760*s (cola incluida), alto ≈ 420*s.
    pose «a»: pata cercana apoyada y la lejana atrás; «b»: al revés (alterna las dos con hide/pop para que corra).
    Ids: {id}, {id}_cola (sway origin right), {id}_cabeza, {id}_ojos (blink), {id}_cresta, {id}_brazos (wiggle),
    {id}_pata_apoyo, {id}_pata_aire (wiggle origin top). .puntos: pie (pie apoyado), cabeza, ojo, cola, centro, agua."""
    o = ""
    # cola larga y afilada (detrás)
    cola = smooth([(-10, -14), (-140, -30), (-300, -60), (-450, -48), (-470, -40), (-300, -36), (-140, 2), (-6, 26)], True)
    cbody = f'<path d="{cola}" fill="url(#basilG)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
    for i in range(5):  # bandas oscuras
        x = -90 - i * 70
        cbody += f'<path d="M {x} {f(-26 - i*7)} Q {x-10} {f(-12 - i*6)} {x+4} {f(4 - i*8)}" stroke="{VERDE_O}" stroke-width="8" fill="none" stroke-linecap="round" opacity="0.7"/>'
    # cresta de la cola
    for i in range(7):
        x = -40 - i * 52
        y = -22 - i * 6.5
        cbody += f'<path d="M {f(x-18)} {f(y+4)} Q {f(x-6)} {f(y-30 + i*2)} {f(x+12)} {f(y)} Z" fill="{VERDE_B}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
    cbody += brillo("M -60 -24 Q -200 -46 -330 -58", 5, 0.5)
    o += g(f"{id_}_cola", cbody)

    def pata(cerca, apoyo):
        col = VERDE_B if cerca else "#2E8E3E"
        hip = (8, 6) if cerca else (-6, 0)
        if apoyo:
            knee, ank = (78, 70), (44, 146)
            pie = _pie_lado(ank[0] - 6, ank[1] + 2, 1.0, col, 0)
        else:
            knee, ank = (-30, 70), (-118, 84)
            pie = _pie_lado(ank[0], ank[1], 0.9, col, 150)
        d1 = f"M {f(hip[0])} {f(hip[1])} L {f(knee[0])} {f(knee[1])}"
        d2 = f"M {f(knee[0])} {f(knee[1])} L {f(ank[0])} {f(ank[1])}"
        muslo = (f'<ellipse cx="{f((hip[0]+knee[0])/2)}" cy="{f((hip[1]+knee[1])/2)}" rx="48" ry="30" '
                 f'transform="rotate({f(_m.degrees(_m.atan2(knee[1]-hip[1], knee[0]-hip[0])))} {f((hip[0]+knee[0])/2)} {f((hip[1]+knee[1])/2)})" '
                 f'fill="{degradado(col, 0.18)}" stroke="{INK}" stroke-width="6"/>')
        return pie + trazo(d2, 20, col, 7) + muslo + trazo(d1, 6, col, 0)

    near_apoyo = pose == "a"
    o += g(f"{id_}_pata_{'aire' if near_apoyo else 'apoyo'}", pata(False, not near_apoyo))
    # brazo lejano
    brazo_l = trazo("M 150 -60 L 170 -24 L 196 -18", 12, "#2E8E3E", 6)
    # cuerpo inclinado
    tor = smooth([(-34, -8), (20, -52), (96, -92), (160, -112), (196, -104), (198, -72), (164, -40), (100, -6), (40, 24), (-22, 28)], True)
    cuerpo = f'<path d="{tor}" fill="url(#basilG)" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'
    cuerpo += f'<path d="{smooth([(20, 18), (90, -10), (160, -46), (186, -72), (170, -44), (100, 2), (30, 24)], True)}" fill="url(#basilBarriga)" opacity="0.9"/>'
    for (x, y, r) in ((40, -14, 8), (78, -38, 7), (112, -62, 8), (60, 4, 6), (140, -82, 6)):
        cuerpo += f'<circle cx="{x}" cy="{y}" r="{r}" fill="#CFF6FF" opacity="0.85"/>'
    cuerpo += brillo("M 10 -40 Q 80 -86 160 -104", 6, 0.55)
    # cresta dorsal (vela)
    cr = ""
    for i in range(8):
        t = i / 7
        x, y = -10 + t * 170, -26 - t * 84
        h = 46 - abs(t - 0.45) * 50
        cr += f'<path d="M {f(x-14)} {f(y+6)} Q {f(x-12)} {f(y-h)} {f(x+16)} {f(y-6)} Z" fill="{VERDE_B}" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round"/>'
    o += brazo_l + g(f"{id_}_cresta", cr) + cuerpo
    # cabeza con casco
    cab = smooth([(0, 0), (30, -20), (80, -14), (108, 0), (98, 16), (52, 24), (10, 22), (-14, 8)], True)
    casco = f"M -10 -6 Q -30 -96 -64 -112 Q -20 -60 30 -18 Z"
    hc = (f'<path d="{casco}" fill="url(#basilOsc)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
          f'<path d="{cab}" fill="url(#basilG)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
          f'<path d="M 30 12 Q 70 18 100 6" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
          f'<path d="M 12 20 Q 40 26 70 20" fill="url(#basilBarriga)" stroke="none" opacity="0.8"/>'
          + brillo("M 20 -16 Q 54 -24 84 -12", 5, 0.6))
    ojos = (f'<circle cx="42" cy="-4" r="14" fill="#FFB52E" stroke="{INK}" stroke-width="4"/>'
            f'<circle cx="45" cy="-4" r="6.5" fill="{INK}"/><circle cx="48" cy="-8" r="3" fill="#FFFFFF"/>')
    hc += g(f"{id_}_ojos", ojos) + f'<circle cx="96" cy="-2" r="2.6" fill="{INK}"/>'
    o += gt(f"{id_}_cabeza", "translate(186 -118) rotate(-6)", hc)
    # pata cercana y brazo cercano
    o += g(f"{id_}_pata_{'apoyo' if near_apoyo else 'aire'}", pata(True, near_apoyo))
    o += g(f"{id_}_brazos", trazo("M 160 -54 L 186 -18 L 214 -12", 13, VERDE_B, 6)
           + f'<path d="M 214 -12 l 14 -6 M 214 -12 l 16 4 M 214 -12 l 10 12" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>')
    sx = -s if espejo else s
    tr = f"translate({f(cx)} {f(cy)}) rotate({f(rot_)}) scale({f(sx)} {f(s)})"

    def P(x, y):
        x = -x if espejo else x
        r = _m.radians(rot_)
        return (cx + s * (x * _m.cos(r) - y * _m.sin(r)), cy + s * (x * _m.sin(r) + y * _m.cos(r)))
    pts_ = {"pie": P(80, 150), "cabeza": P(240, -130), "ojo": P(228, -126), "cola": P(-460, -44), "centro": (cx, cy),
            "agua": P(0, 152)}
    return Pieza(g(id_, f'<g transform="{tr}">{o}</g>'), pts_, (cx - 480 * s, cy - 240 * s, cx + 310 * s, cy + 170 * s))


def pata_basilisco(id_, cx, cy, s=1.0, abiertos=True, col=VERDE_B):
    """Pata trasera vista desde abajo (planta), dedos largos en abanico hacia arriba. (cx, cy) = talón.
    abiertos=True: flecos de escamas desplegados en {id}_flecos (la pisada se agranda); False: plegados.
    Para «abrir los flecos», dibuja las dos (ids distintos) en el mismo sitio y alterna hide/pop. Alto ≈ 430*s, ancho ≈ 380*s.
    .puntos: talon, dedos (lista de puntas), centro."""
    o = ""
    o += (f'<path d="M -50 130 L -46 -20 Q 0 -60 46 -20 L 50 130 Z" fill="{degradado(col, 0.2)}" stroke="{INK}" '
          f'stroke-width="7" stroke-linejoin="round"/>')
    angs = (-58, -30, -6, 18, 46)
    largos = (190, 270, 330, 300, 150)
    puntas, fl, dedos = [], "", ""
    for a, L in zip(angs, largos):
        r = _m.radians(a - 90)
        p0 = (22 * _m.cos(r), -60 + 22 * _m.sin(r))
        p1 = (p0[0] + L * _m.cos(r), p0[1] + L * _m.sin(r))
        puntas.append((cx + p1[0] * s, cy + p1[1] * s))
        dedos += trazo(f"M {f(p0[0])} {f(p0[1])} L {f(p1[0])} {f(p1[1])}", 26, col, 8)
        dedos += f'<circle cx="{f(p1[0])}" cy="{f(p1[1])}" r="9" fill="#F4F7A8" stroke="{INK}" stroke-width="3.5"/>'
        dedos += brillo(f"M {f(p0[0]*1.1)} {f(p0[1])} L {f(p0[0] + (p1[0]-p0[0])*0.7)} {f(p0[1] + (p1[1]-p0[1])*0.7)}", 4, 0.45)
        if abiertos:
            fl += _dedo_flecos(p0, p1, 26, col, True, 6)
        else:
            nx, ny = -_m.sin(r), _m.cos(r)
            for k in (-1, 1):
                q0 = (p0[0] + nx * k * 15, p0[1] + ny * k * 15)
                q1 = (p1[0] + nx * k * 13, p1[1] + ny * k * 13)
                fl += f'<path d="M {f(q0[0])} {f(q0[1])} L {f(q1[0])} {f(q1[1])}" stroke="#E9F9B0" stroke-width="5" stroke-linecap="round" stroke-dasharray="8 10"/>'
    planta = smooth([(-60, -40), (-30, -90), (30, -96), (66, -50), (50, 10), (-50, 10)], True)
    o += g(f"{id_}_flecos", fl) + dedos
    o += f'<path d="{planta}" fill="{degradado(col, 0.22)}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
    o += "".join(f'<circle cx="{x}" cy="{y}" r="6" fill="{shade(col, -0.2)}" opacity="0.6"/>' for x, y in ((-20, -40), (10, -60), (26, -24), (-6, -10)))
    o += brillo("M -40 -50 Q -10 -84 30 -84", 5, 0.6)
    return Pieza(g(id_, f'<g transform="translate({f(cx)} {f(cy)}) scale({f(s)})">{o}</g>'),
                 {"talon": (cx, cy + 100 * s), "dedos": puntas, "centro": (cx, cy - 150 * s)},
                 (cx - 210 * s, cy - 400 * s, cx + 230 * s, cy + 120 * s))


def pie_lateral(id_, cx, cy, s=1.0, col=VERDE_B, pierna=220, ang=0):
    """Pierna + pie de basilisco de lado para la pisada en corte. (cx, cy) = planta del pie (bajo el tobillo);
    la pierna sube recta pierna*s. Dedos hacia la derecha con flecos abiertos. .puntos: planta, rodilla, punta."""
    o = trazo(f"M 0 0 L 22 {-pierna*0.5} L -6 {-pierna}", 26, col, 8)
    o += f'<ellipse cx="8" cy="{f(-pierna*0.78)}" rx="30" ry="{f(pierna*0.26)}" transform="rotate(-14 8 {f(-pierna*0.78)})" fill="{degradado(col, 0.2)}" stroke="{INK}" stroke-width="7"/>'
    o += brillo(f"M -10 {f(-pierna*0.95)} Q -16 {f(-pierna*0.8)} -8 {f(-pierna*0.62)}", 5, 0.55)
    for i, (dx, dy) in enumerate(((150, 4), (128, 14), (104, -4))):
        o += _dedo_flecos((-10, 0), (dx, dy), 20, col if i != 2 else shade(col, -0.15), True, 5)
    o += f'<ellipse cx="-4" cy="-4" rx="28" ry="20" fill="{degradado(col, 0.2)}" stroke="{INK}" stroke-width="6"/>'
    r = _m.radians(ang)
    return Pieza(g(id_, f'<g transform="translate({f(cx)} {f(cy)}) rotate({f(ang)}) scale({f(s)})">{o}</g>'),
                 {"planta": (cx, cy), "rodilla": (cx - 18 * s, cy - pierna * 0.55 * s), "punta": (cx + 150 * s * _m.cos(r), cy + 150 * s * _m.sin(r))},
                 (cx - 60 * s, cy - pierna * s - 20, cx + 170 * s, cy + 30 * s))


def bolsa_aire(id_, cx, sup_y, w=200, h=260, cierre=0.0):
    """Bolsa (cavidad) de aire que abre una pata al bajar en el agua. Boca en la superficie (sup_y), fondo en sup_y + h.
    cierre 0 = abierta del todo; 0.5 = cuello estrechándose; 1 = cerrada (burbuja suelta abajo y cuello sellado).
    Dibújala con varios cierres en el mismo sitio y alterna hide/pop. .puntos: boca, fondo, cuello."""
    hw = w / 2
    boca = hw * (0.75 * (1 - cierre) + 0.08)
    cuello = hw * (0.85 * (1 - cierre) + 0.02)
    yc = sup_y + h * 0.42
    if cierre < 1:
        d = (f"M {f(cx-boca)} {f(sup_y)} C {f(cx-boca)} {f(sup_y+h*0.2)}, {f(cx-cuello)} {f(yc-h*0.1)}, {f(cx-cuello)} {f(yc)} "
             f"C {f(cx-cuello)} {f(yc+h*0.1)}, {f(cx-hw)} {f(sup_y+h*0.6)}, {f(cx-hw)} {f(sup_y+h*0.78)} "
             f"C {f(cx-hw)} {f(sup_y+h*1.02)}, {f(cx+hw)} {f(sup_y+h*1.02)}, {f(cx+hw)} {f(sup_y+h*0.78)} "
             f"C {f(cx+hw)} {f(sup_y+h*0.6)}, {f(cx+cuello)} {f(yc+h*0.1)}, {f(cx+cuello)} {f(yc)} "
             f"C {f(cx+cuello)} {f(yc-h*0.1)}, {f(cx+boca)} {f(sup_y+h*0.2)}, {f(cx+boca)} {f(sup_y)} Z")
        o = f'<path d="{d}" fill="url(#bolsaAireG)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
    else:
        o = (f'<ellipse cx="{f(cx)}" cy="{f(sup_y+h*0.8)}" rx="{f(hw*0.85)}" ry="{f(h*0.2)}" fill="url(#bolsaAireG)" stroke="{INK}" stroke-width="6"/>'
             f'<path d="M {f(cx)} {f(sup_y)} L {f(cx)} {f(sup_y+h*0.45)}" stroke="#FFFFFF" stroke-width="5" stroke-dasharray="6 10" opacity="0.6"/>')
    o += brillo(f"M {f(cx-hw*0.6)} {f(sup_y+h*0.7)} Q {f(cx-hw*0.5)} {f(sup_y+h*0.55)} {f(cx-hw*0.3)} {f(sup_y+h*0.5)}", 6, 0.8)
    return Pieza(g(id_, o), {"boca": (cx, sup_y), "fondo": (cx, sup_y + h), "cuello": (cx, yc)},
                 (cx - hw, sup_y, cx + hw, sup_y + h))


def salpicadura(id_, cx, cy, s=1.0, col="#BFE6FF", seed=3):
    """Corona de salpicadura con gotas que salen hacia arriba. (cx, cy) = punto de impacto en la superficie. Ancho ≈ 260*s."""
    rnd = random.Random(seed)
    n = 14
    d = "M -130 0"
    for i in range(1, n):
        t = i / n
        x = (t - 0.5) * 260
        if i % 2:
            hgt = (70 + rnd.uniform(0, 50)) * (1 - abs(t - 0.5) * 1.1)
            d += f" L {f(x - 6)} {f(-hgt)} L {f(x + 6)} {f(-hgt + 6)}"
        else:
            d += f" L {f(x)} {f(-18 - rnd.uniform(0, 14))}"
    d += " L 130 0 Q 0 22 -130 0 Z"
    o = f'<path d="{d}" fill="{col}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    o += f'<path d="M -80 -10 Q 0 -40 80 -10" fill="none" stroke="#FFFFFF" stroke-width="6" opacity="0.8" stroke-linecap="round"/>'
    for i in range(7):
        a = _m.radians(-165 + i * 25)
        r = 130 + rnd.uniform(0, 50)
        x, y = r * _m.cos(a), r * _m.sin(a) * 0.95 - 20
        rr = rnd.uniform(9, 15)
        o += f'<path d="M {f(x)} {f(y-rr*1.6)} Q {f(x+rr)} {f(y)} {f(x)} {f(y+rr)} Q {f(x-rr)} {f(y)} {f(x)} {f(y-rr*1.6)} Z" fill="{col}" stroke="{INK}" stroke-width="3.5"/>'
    return g(id_, f'<g transform="translate({f(cx)} {f(cy)}) scale({f(s)})">{o}</g>')


def agua_corte(x0, x1, sup_y, fondo_y, seed=5, ondas=True):
    """Agua en corte (sin id): superficie ondulada clara en sup_y, cuerpo azul hasta fondo_y, reflejos y burbujitas."""
    rnd = random.Random(seed)
    o = f'<rect x="{f(x0)}" y="{f(sup_y)}" width="{f(x1-x0)}" height="{f(fondo_y-sup_y)}" fill="url(#aguaCorte)"/>'
    o += f'<rect x="{f(x0)}" y="{f(sup_y)}" width="{f(x1-x0)}" height="24" fill="url(#aguaSup)" opacity="0.8"/>'
    if ondas:
        d = f"M {f(x0)} {f(sup_y)} " + " ".join(f"q 25 -9 50 0 t 50 0" for _ in range(int((x1 - x0) / 100) + 1))
        o += f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
    for _ in range(14):
        x, y = rnd.uniform(x0 + 20, x1 - 20), rnd.uniform(sup_y + 60, fondo_y - 20)
        o += f'<path d="M {f(x)} {f(y)} q 18 -6 36 0" stroke="#FFFFFF" stroke-width="4" fill="none" opacity="0.3" stroke-linecap="round"/>'
    for _ in range(8):
        x, y = rnd.uniform(x0 + 20, x1 - 20), rnd.uniform(sup_y + 60, fondo_y - 20)
        o += f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(rnd.uniform(4, 8))}" fill="none" stroke="#FFFFFF" stroke-width="2.5" opacity="0.45"/>'
    return o


def revista(id_, cx, cy, w=260, h=350, titulo="nature", fecha="1996", contenido="", col="#E8E4D8", banda="#C8102E", rot_=0):
    """Portada de revista científica (por defecto «nature», cabecera con serifa). contenido: SVG en coordenadas de la
    portada (0..w, 0..h); la ilustración va entre 0.24h y 0.86h. fecha en la esquina. .puntos: centro, cabecera."""
    o = f'<rect x="10" y="12" width="{f(w)}" height="{f(h)}" rx="8" fill="{INK}" opacity="0.25"/>'
    o += f'<rect x="0" y="0" width="{f(w)}" height="{f(h)}" rx="8" fill="{col}" stroke="{INK}" stroke-width="6"/>'
    o += f'<rect x="3" y="3" width="{f(w-6)}" height="{f(h*0.2)}" rx="6" fill="{banda}"/>'
    o += (f'<text x="{f(w/2)}" y="{f(h*0.16)}" text-anchor="middle" font-family="Georgia, \'Times New Roman\', serif" '
          f'font-weight="700" font-size="{f(h*0.15)}" fill="#FFFFFF">{titulo}</text>')
    o += f'<g>{contenido}</g>'
    o += f'<rect x="0" y="{f(h*0.88)}" width="{f(w)}" height="{f(h*0.12)}" fill="#FFFFFF" opacity="0.9"/>'
    o += T(w / 2, h * 0.965, fecha, h * 0.07, INK)
    o += f'<rect x="0" y="0" width="{f(w)}" height="{f(h)}" rx="8" fill="none" stroke="{INK}" stroke-width="6"/>'
    o += brillo(f"M 14 {f(h*0.3)} L 14 {f(h*0.7)}", 5, 0.5)
    return Pieza(gt(id_, f"translate({f(cx-w/2)} {f(cy-h/2)}) rotate({f(rot_)} {f(w/2)} {f(h/2)})", o),
                 {"centro": (cx, cy), "cabecera": (cx, cy - h * 0.4)}, (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2))


def selva_rio(W=1080, H=1920, agua_y=None, seed=4):
    """Fondo (sin ids): río tranquilo en la selva. Cielo claro, colinas de selva, palmeras y hojas grandes a los lados,
    orilla lejana y agua con reflejos desde agua_y (por defecto 0,52H) hasta abajo."""
    rnd = random.Random(seed)
    ay = agua_y or H * 0.52
    o = f'<rect width="{W}" height="{f(ay)}" fill="url(#cieloSelva)"/>'
    o += f'<circle cx="{f(W*0.78)}" cy="{f(ay*0.28)}" r="70" fill="#FFE36B" stroke="{INK}" stroke-width="6"/>'
    o += f'<circle cx="{f(W*0.78)}" cy="{f(ay*0.28)}" r="130" fill="#FFE36B" opacity="0.25"/>'
    for capa, (yb, col, rr) in enumerate(((ay - 120, "#6FC48A", 120), (ay - 40, "#3E9E5A", 100))):
        for i in range(10):
            x = i * W / 9 + rnd.uniform(-30, 30)
            o += f'<circle cx="{f(x)}" cy="{f(yb)}" r="{f(rr + rnd.uniform(-20, 30))}" fill="{degradado(col, 0.15)}" stroke="{INK}" stroke-width="5"/>'
        o += f'<rect x="0" y="{f(yb)}" width="{W}" height="{f(ay - yb + 2)}" fill="{shade(col, -0.15)}"/>'
    o += f'<rect x="0" y="{f(ay - 16)}" width="{W}" height="22" fill="#C9A66B" stroke="{INK}" stroke-width="5"/>'
    o += f'<rect x="0" y="{f(ay)}" width="{W}" height="{f(H - ay)}" fill="url(#rioG)"/>'
    o += '<g fill="none" stroke="#FFFFFF" stroke-width="6" opacity="0.35" stroke-linecap="round">' + "".join(
        f'<path d="M {f(rnd.uniform(-40, W))} {f(rnd.uniform(ay + 40, H - 40))} q 30 -12 60 0 t 60 0"/>' for _ in range(22)) + "</g>"
    # hojas grandes en los lados
    for (x, y, a, k) in ((-30, ay - 420, 30, 1), (W + 30, ay - 380, 150, -1), (-20, ay - 120, 10, 1), (W + 20, ay - 90, 170, -1)):
        for j in range(3):
            aa = _m.radians(a + (j - 1) * 28 * k)
            L = 300
            tip = (x + L * _m.cos(aa), y + L * _m.sin(aa) * 0.7)
            mid = ((x + tip[0]) / 2, (y + tip[1]) / 2)
            nx, ny = -_m.sin(aa) * 60, _m.cos(aa) * 60
            o += (f'<path d="M {f(x)} {f(y)} Q {f(mid[0]+nx)} {f(mid[1]+ny)} {f(tip[0])} {f(tip[1])} Q {f(mid[0]-nx)} {f(mid[1]-ny)} {f(x)} {f(y)} Z" '
                  f'fill="{degradado("#2E9A4E", 0.2)}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
            o += f'<path d="M {f(x)} {f(y)} L {f(tip[0])} {f(tip[1])}" stroke="#9BE38E" stroke-width="4" opacity="0.7"/>'
    return o

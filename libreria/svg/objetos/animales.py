"""Animales: perro sentado de frente (labrador u otros colores) que puede bostezar, e icono de perro para cuadrículas.

Sale de: bostezo (lote7-03-bostezo, perros que se contagian el bostezo).
"""
from ..base import (INK, CORAL, f, g, shade, sombra, brillo, lg, rg, registrar_defs, degradado, Pieza, smooth)

PELAJES = {  # claro, medio, oscuro
    "labrador": ("#F6D79A", "#E4B464", "#B9843A"),
    "chocolate": ("#B07A52", "#7D4F2E", "#4E2E18"),
    "negro": ("#5A5F70", "#2E3240", "#15171F"),
    "blanco": ("#FFFFFF", "#ECE8E0", "#C9C2B4"),
}
for _k, (_a, _b, _c) in PELAJES.items():
    registrar_defs(rg(f"pelo_{_k}", [(0, _a), (0.7, _b), (1, _c)], 0.42, 0.32, 0.8),
                   lg(f"peloL_{_k}", [(0, _a), (1, _c)]))


def perro(id_, cx, base, s=1.0, pelaje="labrador", collar=CORAL, bostezo=True):
    """Perro sentado de frente. (cx, base) = suelo entre las patas; alto ≈ 430*s, ancho ≈ 330*s.
    Ids: {id}, {id}_cabeza, {id}_cola (sway, origin bottom-left), {id}_ojos (abiertos), {id}_ojos_cerrados,
    {id}_boca (bocaza de bostezo con lengua enroscada: anímala con grow origin top; debajo queda la boca cerrada),
    {id}_orejas. Con bostezo=False no dibuja {id}_boca ni {id}_ojos_cerrados.
    .puntos: cabeza, boca, nariz, collar."""
    a, b, c = PELAJES.get(pelaje, PELAJES["labrador"])
    P = f"url(#pelo_{pelaje if pelaje in PELAJES else 'labrador'})"
    PL = f"url(#peloL_{pelaje if pelaje in PELAJES else 'labrador'})"
    o = sombra(0, 4, 170, 22, 0.2)
    # cola (detrás, asoma a la derecha)
    cola = (f'<path d="M 70 -40 C 150 -40, 200 -70, 190 -140 C 186 -160, 168 -158, 170 -138 C 172 -90, 130 -72, 70 -72 Z" '
            f'fill="{PL}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
    o += g(f"{id_}_cola", cola)
    # cuartos traseros
    for k in (-1, 1):
        o += f'<ellipse cx="{f(k*98)}" cy="-62" rx="66" ry="62" fill="{P}" stroke="{INK}" stroke-width="7"/>'
        o += f'<path d="M {f(k*60)} -10 Q {f(k*120)} -2 {f(k*150)} -18" fill="none" stroke="{c}" stroke-width="4" stroke-linecap="round" opacity="0.6"/>'
    # cuerpo (pera)
    body = [(-92, -40), (-110, -140), (-82, -230), (0, -262), (82, -230), (110, -140), (92, -40), (0, -20)]
    o += f'<path d="{smooth(body, True)}" fill="{P}" stroke="{INK}" stroke-width="8"/>'
    o += f'<path d="{smooth([(-46, -60), (-58, -150), (0, -210), (58, -150), (46, -60), (0, -44)], True)}" fill="{a}" opacity="0.75"/>'
    # patas delanteras (sin contorno arriba: salen del pecho)
    for k in (-1, 1):
        x = k * 40
        d = f"M {f(x-24)} -170 L {f(x-26)} -18 Q {f(x)} -6 {f(x+26)} -18 L {f(x+24)} -170 Q {f(x)} -182 {f(x-24)} -170 Z"
        o += f'<path d="{d}" fill="{PL}"/>'
        o += f'<path d="M {f(x-24)} -150 L {f(x-26)} -18 M {f(x+26)} -18 L {f(x+24)} -150" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
        o += f'<ellipse cx="{f(x)}" cy="-14" rx="36" ry="20" fill="{P}" stroke="{INK}" stroke-width="7"/>'
        o += "".join(f'<path d="M {f(x+d)} -24 L {f(x+d)} -10" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/>' for d in (-12, 0, 12))
        o += brillo(f"M {f(x-12)} -150 L {f(x-14)} -50", 5, 0.45)
    # collar con chapa
    o += f'<path d="M -70 -238 Q 0 -200 70 -238 L 72 -214 Q 0 -176 -72 -214 Z" fill="{degradado(collar, 0.25)}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
    o += f'<circle cx="0" cy="-184" r="15" fill="url(#amarilloG)" stroke="{INK}" stroke-width="5"/><circle cx="-4" cy="-189" r="4" fill="#FFFFFF" opacity="0.8"/>'
    # cabeza
    hy = -318
    cab = ""
    orejas = ""
    for k in (-1, 1):
        d = (f"M {f(k*62)} {f(hy-62)} C {f(k*120)} {f(hy-70)}, {f(k*136)} {f(hy-10)}, {f(k*128)} {f(hy+48)} "
             f"C {f(k*124)} {f(hy+76)}, {f(k*92)} {f(hy+78)}, {f(k*86)} {f(hy+44)} C {f(k*82)} {f(hy+10)}, {f(k*72)} {f(hy-20)}, {f(k*50)} {f(hy-40)} Z")
        orejas += f'<path d="{d}" fill="{degradado(b, 0.3)}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
    cab += f'<ellipse cx="0" cy="{f(hy)}" rx="96" ry="84" fill="{P}" stroke="{INK}" stroke-width="8"/>'
    cab += g(f"{id_}_orejas", orejas)
    cab += brillo(f"M -50 {f(hy-58)} Q 0 {f(hy-78)} 46 {f(hy-60)}", 7, 0.6)
    # hocico
    cab += f'<ellipse cx="0" cy="{f(hy+40)}" rx="60" ry="44" fill="{a}" stroke="{INK}" stroke-width="6"/>'
    # boca cerrada (debajo de la bocaza)
    cab += f'<path d="M 0 {f(hy+38)} L 0 {f(hy+56)} M -26 {f(hy+60)} Q -12 {f(hy+70)} 0 {f(hy+56)} Q 12 {f(hy+70)} 26 {f(hy+60)}" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
    # ojos abiertos
    ojos = ""
    for k in (-1, 1):
        ojos += f'<ellipse cx="{f(k*38)}" cy="{f(hy-12)}" rx="13" ry="15" fill="#2A1A10" stroke="{INK}" stroke-width="3"/><circle cx="{f(k*38+4)}" cy="{f(hy-18)}" r="5" fill="#FFFFFF"/>'
        ojos += f'<path d="M {f(k*24)} {f(hy-38)} Q {f(k*38)} {f(hy-46)} {f(k*54)} {f(hy-38)}" fill="none" stroke="{c}" stroke-width="5" stroke-linecap="round"/>'
    cab += g(f"{id_}_ojos", ojos)
    if bostezo:
        cerr = ""
        for k in (-1, 1):
            cerr += f'<path d="M {f(k*24)} {f(hy-10)} Q {f(k*38)} {f(hy-24)} {f(k*54)} {f(hy-10)}" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
            cerr += f'<path d="M {f(k*58)} {f(hy-18)} l {f(k*10)} -6 M {f(k*58)} {f(hy-8)} l {f(k*11)} 2" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/>'
        cab += g(f"{id_}_ojos_cerrados", f'<g>{cerr}</g>')
        # bocaza: óvalo oscuro, colmillos, lengua enroscada hacia arriba
        my = hy + 82
        boca = (f'<path d="M -44 {f(hy+44)} C -50 {f(my+30)}, -26 {f(my+64)}, 0 {f(my+64)} C 26 {f(my+64)}, 50 {f(my+30)}, 44 {f(hy+44)} Q 0 {f(hy+58)} -44 {f(hy+44)} Z" fill="#5A1420" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
                f'<path d="M -34 {f(hy+50)} l 8 20 l 7 -18 Z M 34 {f(hy+50)} l -8 20 l -7 -18 Z" fill="#FFFFFF" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>'
                f'<path d="M -30 {f(my+44)} C -40 {f(my+4)}, 40 {f(my+4)}, 30 {f(my+40)} C 26 {f(my+54)}, 12 {f(my+50)}, 14 {f(my+36)} C 6 {f(my+22)}, -10 {f(my+24)}, -12 {f(my+40)} C -14 {f(my+54)}, -26 {f(my+56)}, -30 {f(my+44)} Z" fill="#FF7F95" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
                f'<path d="M 0 {f(my+16)} L 0 {f(my+30)}" stroke="#D9566E" stroke-width="3" stroke-linecap="round"/>'
                f'<path d="M -16 {f(my+18)} Q 0 {f(my+10)} 16 {f(my+18)}" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.6" stroke-linecap="round"/>')
        cab += g(f"{id_}_boca", boca)
    # nariz por encima de todo
    cab += f'<path d="M -22 {f(hy+18)} Q 0 {f(hy+8)} 22 {f(hy+18)} Q 20 {f(hy+36)} 0 {f(hy+40)} Q -20 {f(hy+36)} -22 {f(hy+18)} Z" fill="#2A1A14" stroke="{INK}" stroke-width="4"/>'
    cab += f'<ellipse cx="-7" cy="{f(hy+18)}" rx="7" ry="4" fill="#FFFFFF" opacity="0.7"/>'
    o += g(f"{id_}_cabeza", cab)
    pts_ = {"cabeza": (cx, base + hy * s), "boca": (cx, base + (hy + 80) * s), "nariz": (cx, base + (hy + 26) * s),
            "collar": (cx, base - 184 * s)}
    return Pieza(g(id_, f'<g transform="translate({f(cx)} {f(base)}) scale({f(s)})">{o}</g>'), pts_,
                 (cx - 170 * s, base - 410 * s, cx + 200 * s, base))


def icono_perro(id_, cx, cy, s=60, col="#C9CED8", sw=4):
    """Cabeza de perro de frente para cuadrículas/recuentos (ancho ≈ 1.2*s). col: relleno (gris = no, dorado = sí)."""
    k = s / 60
    o = ""
    for d in (-1, 1):
        o += f'<path d="M {f(cx+d*18*k)} {f(cy-20*k)} C {f(cx+d*38*k)} {f(cy-26*k)}, {f(cx+d*40*k)} {f(cy+4*k)}, {f(cx+d*34*k)} {f(cy+18*k)} C {f(cx+d*28*k)} {f(cy+24*k)}, {f(cx+d*22*k)} {f(cy+10*k)}, {f(cx+d*18*k)} {f(cy-4*k)} Z" fill="{shade(col, -0.22)}" stroke="{INK}" stroke-width="{f(sw)}" stroke-linejoin="round"/>'
    o += f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(26*k)}" ry="{f(24*k)}" fill="{degradado(col, 0.18)}" stroke="{INK}" stroke-width="{f(sw)}"/>'
    o += f'<ellipse cx="{f(cx)}" cy="{f(cy+11*k)}" rx="{f(14*k)}" ry="{f(10*k)}" fill="{shade(col, 0.35)}"/>'
    o += f'<ellipse cx="{f(cx)}" cy="{f(cy+6*k)}" rx="{f(6*k)}" ry="{f(4.5*k)}" fill="{INK}"/>'
    o += "".join(f'<circle cx="{f(cx+d*10*k)}" cy="{f(cy-5*k)}" r="{f(3.4*k)}" fill="{INK}"/>' for d in (-1, 1))
    o += f'<path d="M {f(cx-12*k)} {f(cy-16*k)} Q {f(cx)} {f(cy-22*k)} {f(cx+12*k)} {f(cy-16*k)}" fill="none" stroke="#FFFFFF" stroke-width="{f(2.5*k)}" opacity="0.6" stroke-linecap="round"/>'
    return g(id_, o)


# ------------------------------------------------------------------ gato (lote8-03-gatos-caen)
import math as _m
from ..base import trazo, gt

GATOS = {  # claro, medio, oscuro, rayas
    "naranja": ("#FFD39A", "#F5A24A", "#C9701F", "#B5561A"),
    "gris": ("#D9DDE6", "#A3AAB8", "#6B7283", "#545A69"),
    "negro": ("#5A5F70", "#2E3240", "#15171F", None),
    "blanco": ("#FFFFFF", "#ECE8E0", "#C9C2B4", None),
}
for _k, (_a, _b, _c, _r) in GATOS.items():
    registrar_defs(lg(f"gatoG_{_k}", [(0, _a), (0.55, _b), (1, _c)]),
                   rg(f"gatoR_{_k}", [(0, _a), (0.7, _b), (1, _c)], 0.4, 0.3, 0.8))

# patas: (cadera/hombro, rodilla, pie) en coordenadas locales (patas abajo, morro a la derecha)
_PATAS = {
    "normal": {"del_lejos": [(78, 20), (74, 90), (72, 150)], "del_cerca": [(118, 20), (120, 90), (124, 150)],
               "tras_lejos": [(-70, 20), (-52, 92), (-78, 150)], "tras_cerca": [(-112, 24), (-92, 96), (-120, 150)]},
    "encogidas": {"del_lejos": [(80, 20), (118, 70), (84, 96)], "del_cerca": [(118, 20), (156, 70), (120, 98)],
                  "tras_lejos": [(-70, 20), (-30, 70), (-68, 96)], "tras_cerca": [(-112, 24), (-70, 74), (-110, 100)]},
    "estiradas": {"del_lejos": [(84, 20), (132, 96), (128, 158)], "del_cerca": [(118, 20), (172, 92), (170, 156)],
                  "tras_lejos": [(-74, 20), (-120, 92), (-112, 158)], "tras_cerca": [(-112, 24), (-162, 90), (-160, 156)]},
}


def _kgiro(giro):
    k = _m.cos(_m.radians(giro))
    return (1 if k >= 0 else -1) * max(abs(k), 0.3)


def gato(id_, cx, cy, s=1.0, pelaje="naranja", giro_del=0, giro_tras=0, doblez=0, patas="normal", cola=0,
         rot_=0, expresion="normal", cria=False, espejo=False):
    """Gato de perfil (morro a la derecha) pensado para la secuencia de caída. (cx, cy) = centro del cuerpo (cintura);
    largo ≈ 520*s (cola incluida), alto de pie ≈ 360*s (el suelo queda en cy + 165*s con patas="normal").
    giro_del / giro_tras: giro de cada mitad alrededor de la columna en grados (0 = patas abajo, 180 = patas arriba;
    90 aplastado = a medio girar). doblez: grados que se dobla por la cintura (V). patas: normal | encogidas | estiradas.
    cola: grados que gira la cola. expresion: normal | susto | feliz. cria: cabeza grande (gatito). espejo: mira a la izquierda.
    Ids: {id}, {id}_cabeza, {id}_ojos (blink), {id}_cola (sway origin bottom-right). .puntos: cabeza, oreja, cola, centro, suelo."""
    cl, md, os_, ry = GATOS.get(pelaje, GATOS["naranja"])
    pg = f"url(#gatoG_{pelaje if pelaje in GATOS else 'naranja'})"
    pr = f"url(#gatoR_{pelaje if pelaje in GATOS else 'naranja'})"
    kd, kt = _kgiro(giro_del), _kgiro(giro_tras)
    tf_d = f"rotate({f(doblez / 2)}) scale(1 {f(kd)})"
    tf_t = f"rotate({f(-doblez / 2)}) scale(1 {f(kt)})"
    P = _PATAS.get(patas, _PATAS["normal"])
    W = 38

    def pata(p, col, ancho=W):
        d = f"M {f(p[0][0])} {f(p[0][1])} Q {f(p[1][0])} {f(p[1][1])} {f(p[2][0])} {f(p[2][1])}"
        x, y = p[2]
        px, py = p[1]
        ang = _m.degrees(_m.atan2(y - py, x - px)) - 90
        return (trazo(d, ancho, col, 14)
                + f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(ancho*0.66)}" ry="{f(ancho*0.42)}" transform="rotate({f(ang)} {f(x)} {f(y)})" '
                  f'fill="{cl}" stroke="{INK}" stroke-width="6"/>')

    tor_d = smooth([(-34, -50), (40, -60), (112, -54), (160, -28), (174, 8), (152, 46), (92, 60), (20, 56), (-34, 48)], True)
    tor_t = smooth([(34, -50), (-40, -60), (-122, -56), (-172, -26), (-182, 14), (-154, 52), (-84, 62), (-20, 56), (34, 48)], True)
    o = ""
    # cola (detrás de todo, sale del lomo trasero)
    cd = smooth([(-166, -24), (-222, -40), (-256, -92), (-250, -150), (-222, -184)])
    c_body = trazo(cd, 30, md, 14) + brillo(smooth([(-200, -46), (-236, -84), (-240, -130)]), 5, 0.45)
    if ry:
        for t_ in ((-236, -64), (-252, -110), (-240, -158)):
            c_body += f'<circle cx="{f(t_[0])}" cy="{f(t_[1])}" r="9" fill="{ry}" opacity="0.7"/>'
    c_body += f'<circle cx="-222" cy="-184" r="15" fill="{os_}"/>'
    o += f'<g transform="{tf_t}">{gt(f"{id_}_cola", f"rotate({f(cola)} -166 -24)", c_body)}</g>'
    # patas del lado lejano (más oscuras)
    o += f'<g transform="{tf_t}">{pata(P["tras_lejos"], os_)}</g><g transform="{tf_d}">{pata(P["del_lejos"], os_)}</g>'
    # silueta: contorno de las dos mitades a la vez y relleno encima (sin costura en la cintura)
    o += f'<g transform="{tf_t}"><path d="{tor_t}" fill="{INK}" stroke="{INK}" stroke-width="16" stroke-linejoin="round"/></g>'
    o += f'<g transform="{tf_d}"><path d="{tor_d}" fill="{INK}" stroke="{INK}" stroke-width="16" stroke-linejoin="round"/></g>'
    o += f'<g transform="{tf_t}"><path d="{tor_t}" fill="{pg}"/></g><g transform="{tf_d}"><path d="{tor_d}" fill="{pg}"/></g>'
    # tripa clara, muslo y rayas
    det_t = f'<ellipse cx="-70" cy="44" rx="70" ry="13" fill="{cl}" opacity="0.85"/>'
    det_t += f'<ellipse cx="-118" cy="6" rx="52" ry="50" fill="{pr}" stroke="{os_}" stroke-width="4" opacity="0.95"/>'
    det_d = f'<ellipse cx="80" cy="44" rx="66" ry="13" fill="{cl}" opacity="0.85"/>'
    det_d += f'<ellipse cx="116" cy="10" rx="40" ry="44" fill="{pr}" stroke="{os_}" stroke-width="4" opacity="0.95"/>'
    det_d += brillo("M 10 -50 Q 70 -60 128 -46", 7, 0.55)
    det_t += brillo("M -10 -50 Q -70 -60 -130 -48", 7, 0.45)
    if ry:
        for x in (-150, -104, -58):
            det_t += f'<path d="M {x} -56 Q {x+10} -36 {x+2} -16" fill="none" stroke="{ry}" stroke-width="9" stroke-linecap="round" opacity="0.8"/>'
        for x in (-12, 34, 80, 122):
            det_d += f'<path d="M {x} -58 Q {x+10} -38 {x+2} -18" fill="none" stroke="{ry}" stroke-width="9" stroke-linecap="round" opacity="0.8"/>'
    o += f'<g transform="{tf_t}">{det_t}</g><g transform="{tf_d}">{det_d}</g>'
    # patas cercanas
    o += f'<g transform="{tf_t}">{pata(P["tras_cerca"], md)}</g><g transform="{tf_d}">{pata(P["del_cerca"], md)}</g>'
    # cabeza (3/4, mirando al frente y algo a la derecha)
    hs = 1.32 if cria else 1.0
    hx, hy = 196, -70
    cab = ""
    for (a, b, c) in (((-50, -26), (-44, -92), (-6, -48)), ((14, -50), (48, -90), (58, -24))):
        cab += f'<path d="M {a[0]} {a[1]} L {b[0]} {b[1]} L {c[0]} {c[1]} Z" fill="{pg}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
        mx, my = (a[0] + b[0] + c[0]) / 3, (a[1] + b[1] + c[1]) / 3
        cab += (f'<path d="M {f((a[0]+mx)/2)} {f((a[1]+my)/2+4)} L {f((b[0]*2+mx)/3)} {f((b[1]*2+my)/3)} L {f((c[0]+mx)/2)} {f((c[1]+my)/2+4)} Z" '
                f'fill="#FF9DB0"/>')
    cab += f'<ellipse cx="0" cy="0" rx="66" ry="56" fill="{pr}" stroke="{INK}" stroke-width="8"/>'
    if ry:
        cab += "".join(f'<path d="M {x} -54 Q {x+2} -40 {x} -28" stroke="{ry}" stroke-width="7" stroke-linecap="round" fill="none" opacity="0.8"/>' for x in (-14, 0, 14))
    cab += brillo("M -42 -32 Q -20 -50 8 -50", 6, 0.6)
    cab += f'<ellipse cx="6" cy="24" rx="34" ry="20" fill="{cl}"/>'
    # ojos
    ojos = ""
    for ex in (-22, 30):
        if expresion == "feliz":
            ojos += f'<path d="M {ex-12} -4 Q {ex} -18 {ex+12} -4" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
        else:
            r_ = 15 if expresion == "susto" else 12
            ojos += (f'<ellipse cx="{ex}" cy="-6" rx="{r_}" ry="{r_+3}" fill="#B9E85A" stroke="{INK}" stroke-width="4"/>'
                     f'<ellipse cx="{ex+1}" cy="-6" rx="{3.5 if expresion == "susto" else 4.5}" ry="{r_}" fill="{INK}"/>'
                     f'<circle cx="{ex+4}" cy="-12" r="4" fill="#FFFFFF"/>')
    cab += g(f"{id_}_ojos", ojos)
    # nariz, boca y bigotes
    cab += f'<path d="M -2 12 L 14 12 L 6 22 Z" fill="#FF7F95" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>'
    if expresion == "susto":
        cab += f'<ellipse cx="6" cy="34" rx="8" ry="9" fill="#5A1420" stroke="{INK}" stroke-width="3.5"/>'
    else:
        cab += f'<path d="M 6 22 L 6 28 M -6 30 Q 0 36 6 28 Q 12 36 18 30" fill="none" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/>'
    for dy in (-4, 6):
        cab += f'<path d="M 34 {22+dy} Q 70 {16+dy*1.6} 96 {14+dy*2.4}" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
        cab += f'<path d="M -22 {22+dy} Q -56 {16+dy*1.6} -80 {14+dy*2.4}" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
    cab_g = gt(f"{id_}_cabeza", f"translate({hx} {hy}) scale({f(hs)})", cab)
    o += f'<g transform="{tf_d}">{cab_g}</g>'
    sx = -s if espejo else s
    tr = f"translate({f(cx)} {f(cy)}) rotate({f(rot_)}) scale({f(sx)} {f(s)})"

    def P_(x, y, half=1):
        k = kd if half else kt
        a = _m.radians((doblez / 2 if half else -doblez / 2))
        x2, y2 = x, y * k
        x3, y3 = x2 * _m.cos(a) - y2 * _m.sin(a), x2 * _m.sin(a) + y2 * _m.cos(a)
        x3 *= (-1 if espejo else 1)
        r = _m.radians(rot_)
        return (cx + s * (x3 * _m.cos(r) - y3 * _m.sin(r)), cy + s * (x3 * _m.sin(r) + y3 * _m.cos(r)))
    pts_ = {"cabeza": P_(hx, hy), "oreja": P_(hx - 44, hy - 92), "cola": P_(-222, -184, 0), "centro": (cx, cy),
            "suelo": (cx, cy + 165 * s), "patas_del": P_(124, 150), "patas_tras": P_(-120, 150, 0)}
    return Pieza(g(id_, f'<g transform="{tr}">{o}</g>'), pts_, (cx - 270 * s, cy - 200 * s, cx + 270 * s, cy + 170 * s))

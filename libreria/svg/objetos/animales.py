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

import math, random, sys
sys.path.insert(0, "/tmp/claude-0/-home-user-automatizacion-contenidos/039df981-7a17-5355-b711-18510fb209db/scratchpad/dedos")
from common import *

random.seed(2)
TOPY, BOTY = 190, 590       # borde y fondo del vaso
RT, RB, EY = 128, 104, 22    # radio arriba, abajo, achatamiento elipse
SURF = 290                   # nivel del liquido


def rx_at(y):
    return RT + (RB - RT) * (y - TOPY) / (BOTY - TOPY)


def glass_parts(cx, liquid_grad, surf_col, idp):
    """devuelve (fondo, liquido, frente) del vaso centrado en cx"""
    back = []
    rT, rB = RT, RB
    body = f"M {cx - rT} {TOPY} L {cx - rB} {BOTY} A {rB} {EY * rB / rT:.1f} 0 0 0 {cx + rB} {BOTY} L {cx + rT} {TOPY}"
    back.append(f'<path d="{body} A {rT} {EY} 0 0 0 {cx - rT} {TOPY} Z" fill="#FFFFFF" fill-opacity="0.35"/>')
    back.append(f'<ellipse cx="{cx}" cy="{TOPY}" rx="{rT}" ry="{EY}" fill="#E9F6FF" fill-opacity="0.6" stroke="{INK}" stroke-width="5"/>')
    rs = rx_at(SURF)
    liq = (f"M {cx - rs:.1f} {SURF} L {cx - rB + 6} {BOTY - 4} A {rB - 6} {EY * (rB - 6) / rT:.1f} 0 0 0 {cx + rB - 6} {BOTY - 4} "
           f"L {cx + rs:.1f} {SURF} A {rs:.1f} {EY * rs / rT:.1f} 0 0 1 {cx - rs:.1f} {SURF} Z")
    liquid = f'<path d="{liq}" fill="url(#{liquid_grad})"/>'
    surf = f'<ellipse cx="{cx}" cy="{SURF}" rx="{rs:.1f}" ry="{EY * rs / rT:.1f}" fill="{surf_col}" stroke="{INK}" stroke-width="4"/>'
    front = []
    front.append(f'<path d="{body}" fill="none" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
    front.append(f'<path d="M {cx - rT} {TOPY} A {rT} {EY} 0 0 0 {cx + rT} {TOPY}" fill="none" stroke="{INK}" stroke-width="7"/>')
    # brillos del cristal
    front.append(f'<path d="M {cx - rT + 26} {TOPY + 40} L {cx - rB + 22} {BOTY - 40}" stroke="#FFFFFF" stroke-width="12" stroke-linecap="round" opacity="0.75"/>')
    front.append(f'<path d="M {cx - rT + 52} {TOPY + 60} L {cx - rB + 44} {BOTY - 120}" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity="0.6"/>')
    front.append(f'<path d="M {cx + rT - 24} {TOPY + 50} L {cx + rB - 20} {BOTY - 60}" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" opacity="0.45"/>')
    # fondo grueso del vaso
    front.append(f'<path d="M {cx - rB + 4} {BOTY - 14} A {rB - 4} {EY * 0.8:.1f} 0 0 0 {cx + rB - 4} {BOTY - 14}" fill="none" stroke="#FFFFFF" stroke-width="5" opacity="0.6"/>')
    return "".join(back), liquid, surf, "".join(front)


def cube(cx, cy, s, ang, fill_top, fill_front, fill_side, op=1.0):
    """cubo isometrico sencillo: centro de la cara frontal (cx,cy)"""
    h = s / 2
    d = s * 0.32
    a = math.radians(ang)
    def R(x, y):
        return (cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a))
    F = [R(-h, -h), R(h, -h), R(h, h), R(-h, h)]
    T = [R(-h, -h), R(-h + d, -h - d * 0.8), R(h + d, -h - d * 0.8), R(h, -h)]
    S = [R(h, -h), R(h + d, -h - d * 0.8), R(h + d, h - d * 0.8), R(h, h)]
    p = lambda pts: "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts) + " Z"
    o = f'<g opacity="{op}">'
    o += f'<path d="{p(F)}" fill="{fill_front}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    o += f'<path d="{p(T)}" fill="{fill_top}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    o += f'<path d="{p(S)}" fill="{fill_side}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    x1, y1 = R(-h + 10, -h + 12); x2, y2 = R(-h + 10, h - 16)
    o += f'<path d="M {x1:.1f} {y1:.1f} L {x2:.1f} {y2:.1f}" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity="0.9"/>'
    for k in range(3):  # burbujitas de aire atrapadas
        bx, by = R(random.uniform(-h + 14, h - 14), random.uniform(-h + 14, h - 14))
        o += f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="{random.uniform(2.5, 4.5):.1f}" fill="#FFFFFF" opacity="0.8"/>'
    return o + '</g>'


o = [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 700">
<defs>
<linearGradient id="wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFF6E8"/><stop offset="1" stop-color="#F6E6CF"/></linearGradient>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#BFE6FF"/><stop offset="1" stop-color="#E6F6FF"/></linearGradient>
<linearGradient id="wood" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E7C487"/><stop offset="1" stop-color="#C89B5B"/></linearGradient>
<linearGradient id="water" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#BEE6FF"/><stop offset="1" stop-color="#5FAEEA"/></linearGradient>
<linearGradient id="waxliq" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFD873"/><stop offset="1" stop-color="#E9A13B"/></linearGradient>
<linearGradient id="icef" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F4FCFF"/><stop offset="1" stop-color="#BFE7FA"/></linearGradient>
<linearGradient id="waxs" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFF8E6"/><stop offset="1" stop-color="#EBD9AE"/></linearGradient>
</defs>
<rect width="1000" height="700" fill="url(#wall)"/>''']
# ventana al fondo (lejos, sin contorno)
o.append('<rect x="380" y="40" width="240" height="250" rx="14" fill="#E3D2BA"/><rect x="394" y="54" width="212" height="222" rx="8" fill="url(#sky)"/>'
         '<path d="M 500 54 L 500 276 M 394 165 L 606 165" stroke="#E3D2BA" stroke-width="10"/>'
         '<g fill="#FFFFFF" opacity="0.9"><ellipse cx="450" cy="110" rx="34" ry="12"/><ellipse cx="560" cy="210" rx="28" ry="10"/></g>')
o.append('<g fill="#EADBC4" opacity="0.8"><rect x="0" y="470" width="1000" height="8"/></g>')
# encimera
o.append(f'<path d="M 0 600 L 1000 600 L 1000 700 L 0 700 Z" fill="url(#wood)"/>')
o.append(f'<path d="M 0 600 L 1000 600" stroke="{INK}" stroke-width="7"/>')
o.append('<g stroke="#B88B4E" stroke-width="3" fill="none" opacity="0.7"><path d="M 40 640 C 200 632, 340 650, 520 642"/><path d="M 560 668 C 700 660, 820 676, 980 664"/></g>')
o.append('<path d="M 0 610 L 1000 610" stroke="#F6DDB0" stroke-width="4"/>')

L, R = 270, 690
for cx in (L, R):
    o.append(f'<ellipse cx="{cx + 10}" cy="{BOTY + 10}" rx="{RB + 30}" ry="14" fill="#8A6A3C" opacity="0.35"/>')

# VASO DE AGUA + HIELO
b, liq, surf, fr = glass_parts(L, "water", "#D6F0FF", "a")
o.append(b + liq)
# cubos: 91,7 % sumergidos -> cara visible por encima de SURF minima
S = 92
o.append('<g id="ice">')
o.append(cube(L - 40, SURF + S / 2 - 8, S, -8, "url(#icef)", "url(#icef)", "#A9DBF4"))
o.append(cube(L + 50, SURF + S / 2 - 6, S - 10, 10, "url(#icef)", "url(#icef)", "#A9DBF4"))
o.append('</g>')
# agua por delante de la parte sumergida (tinte) + superficie
rs = rx_at(SURF)
o.append(f'<path d="M {L - rs:.1f} {SURF} L {L - RB + 6} {BOTY - 4} A {RB - 6} {EY * (RB - 6) / RT:.1f} 0 0 0 {L + RB - 6} {BOTY - 4} L {L + rs:.1f} {SURF} A {rs:.1f} {EY * rs / RT:.1f} 0 0 0 {L - rs:.1f} {SURF} Z" fill="#5FAEEA" opacity="0.38"/>')
o.append(f'<path d="M {L - rs + 6:.1f} {SURF} A {rs - 6:.1f} {EY * rs / RT - 2:.1f} 0 0 0 {L + rs - 6:.1f} {SURF}" fill="none" stroke="#FFFFFF" stroke-width="4" opacity="0.9"/>')
o.append(f'<g id="bubs" fill="#FFFFFF" opacity="0.8">' + "".join(f'<circle cx="{L + dx}" cy="{y}" r="{r}"/>' for dx, y, r in [(-60, 520, 5), (-50, 470, 3.5), (70, 540, 4), (40, 500, 3)]) + '</g>')
o.append(fr)

# VASO DE CERA
b, liq, surf, fr = glass_parts(R, "waxliq", "#FFE49A", "b")
o.append(b + liq)
o.append('<g id="wax">' + cube(R, SURF + 20, 84, 6, "url(#waxs)", "url(#waxs)", "#E2CC93") + '</g>')
o.append(f'<path d="M {R - rs:.1f} {SURF} L {R - RB + 6} {BOTY - 4} A {RB - 6} {EY * (RB - 6) / RT:.1f} 0 0 0 {R + RB - 6} {BOTY - 4} L {R + rs:.1f} {SURF} A {rs:.1f} {EY * rs / RT:.1f} 0 0 0 {R - rs:.1f} {SURF} Z" fill="#E9A13B" opacity="0.35"/>')
o.append(f'<path d="M {R - rs + 6:.1f} {SURF} A {rs - 6:.1f} {EY * rs / RT - 2:.1f} 0 0 0 {R + rs - 6:.1f} {SURF}" fill="none" stroke="#FFF3C4" stroke-width="4" opacity="0.9"/>')
o.append(fr)
# onda en la cera al caer
o.append(f'<g id="splash"><ellipse cx="{R}" cy="{SURF}" rx="70" ry="10" fill="none" stroke="#FFF3C4" stroke-width="5"/></g>')
# vela al lado (de donde sale la cera)
o.append(f'''<g id="candle"><rect x="452" y="470" width="56" height="130" rx="8" fill="url(#waxs)" stroke="{INK}" stroke-width="6"/>
<path d="M 456 486 C 472 498, 488 482, 504 492" fill="none" stroke="#E2CC93" stroke-width="5"/>
<path d="M 480 470 L 480 452" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>
<g id="flame"><path d="M 480 452 C 464 440, 468 418, 480 398 C 492 418, 496 440, 480 452 Z" fill="#FFB238" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>
<path d="M 480 446 C 474 438, 476 428, 480 420 C 484 428, 486 438, 480 446 Z" fill="#FFF1A8"/></g>
<rect x="462" y="490" width="8" height="90" rx="4" fill="#FFFFFF" opacity="0.7"/></g>''')
# etiquetas y flechas
o.append(tag("la", 18, 440, "AGUA", fs=26, lead=(132, 469, L - 50, 490)))
o.append(tag("lb", 850, 200, "CERA", fs=26, lead=(860, 258, R + 88, 390)))
o.append(tag("lflota", 18, 236, "FLOTA", bg=LIME, fg=INK, fs=26, lead=(140, 265, L - 70, 280)))
o.append(tag("lhunde", 822, 410, "SE HUNDE", bg=CORAL, fg=INK, fs=26))
o.append('</svg>')
print("\n".join(o))

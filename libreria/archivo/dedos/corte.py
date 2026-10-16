import math, random, sys
sys.path.insert(0, sys.path[0])
from common import *

random.seed(3)
X0, X1, YB, YF = 60, 700, 575, 465  # slab: izquierda, derecha, fondo, limite dermis/grasa


def top_flat(x):
    return 282


def top_wavy(x):
    return 304 + 20 * math.sin((x - X0) / (X1 - X0) * 5.5 * 2 * math.pi + 1.2)


def contour(f, off=0.0, amp=1.0, step=5):
    pts = []
    for x in range(X0, X1 + 1, step):
        base = f(x)
        mean = 304 if f is top_wavy else 282
        pts.append((x, mean + (base - mean) * amp + off))
    return pts


def P(pts):
    return " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)


o = [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 700">
<defs>
<radialGradient id="bg" cx="0.45" cy="0.5" r="0.8"><stop offset="0" stop-color="#FFF8F2"/><stop offset="1" stop-color="#F6E3D6"/></radialGradient>
<linearGradient id="derm" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F7B9A6"/><stop offset="1" stop-color="#EB9784"/></linearGradient>
<linearGradient id="epi" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFE3D2"/><stop offset="1" stop-color="#F6C3A9"/></linearGradient>
<linearGradient id="fat" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFE9A8"/><stop offset="1" stop-color="#F5CF73"/></linearGradient>
<linearGradient id="artw" gradientUnits="userSpaceOnUse" x1="0" y1="400" x2="0" y2="436"><stop offset="0" stop-color="#FF7A6A"/><stop offset="0.5" stop-color="#E0352B"/><stop offset="1" stop-color="#A3161A"/></linearGradient><linearGradient id="artt" gradientUnits="userSpaceOnUse" x1="0" y1="411" x2="0" y2="425"><stop offset="0" stop-color="#FF7A6A"/><stop offset="0.5" stop-color="#E0352B"/><stop offset="1" stop-color="#A3161A"/></linearGradient>
<linearGradient id="nrv" gradientUnits="userSpaceOnUse" x1="0" y1="503" x2="0" y2="527"><stop offset="0" stop-color="#FFF3A0"/><stop offset="1" stop-color="#F2B705"/></linearGradient>
<radialGradient id="glow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#FFFFFF"/><stop offset="0.35" stop-color="#C8FF2E"/><stop offset="1" stop-color="#C8FF2E" stop-opacity="0"/></radialGradient>
<radialGradient id="skin2" cx="0.4" cy="0.35" r="0.8"><stop offset="0" stop-color="#FCDCC7"/><stop offset="1" stop-color="#E9A584"/></radialGradient>
</defs>
<rect width="1000" height="700" fill="url(#bg)"/>
<g fill="none" stroke="#EED3C3" stroke-width="2"><circle cx="380" cy="420" r="330"/><circle cx="380" cy="420" r="450"/></g>
<ellipse cx="385" cy="{YB + 22}" rx="340" ry="18" fill="#C9A08A" opacity="0.45"/>''']


def state(id_, f, wave):
    s = [f'<g id="{id_}">']
    top = contour(f)
    epi_bot = contour(f, 44, 0.7)
    sil = f"M {X0} {YB - 30} L {P(top)} L {X1} {YB - 30} Q {X1} {YB} {X1 - 30} {YB} L {X0 + 30} {YB} Q {X0} {YB} {X0} {YB - 30} Z"
    s.append(f'<path d="{sil}" fill="url(#derm)"/>')
    # papilas dermicas: borde inferior ondulado de la epidermis
    pap = []
    for x, y in epi_bot:
        pap.append((x, y + 7 * math.sin((x - X0) / 40 * 2 * math.pi)))
    s.append(f'<path d="M {P(top)} L {P(pap[::-1])} Z" fill="url(#epi)"/>')
    s.append(f'<path d="M {P(pap)}" fill="none" stroke="#D9826E" stroke-width="4" stroke-linejoin="round"/>')
    # capa cornea (linea fina bajo la superficie)
    s.append(f'<path d="M {P(contour(f, 12, 0.95))}" fill="none" stroke="#F0B699" stroke-width="3" opacity="0.9"/>')
    s.append(f'<path d="M {P(top)}" fill="none" stroke="{INK}" stroke-width="8" stroke-linejoin="round" stroke-linecap="round"/>')
    s.append(f'<path d="M {P(contour(f, 7, 1.0)[2:-2])}" fill="none" stroke="#FFFFFF" stroke-width="3.5" opacity="0.8" stroke-linecap="round"/>')
    s.append(f'<path d="M {X0} {top[0][1]:.1f} L {X0} {YB - 30}" stroke="{INK}" stroke-width="8"/><path d="M {X1} {top[-1][1]:.1f} L {X1} {YB - 30}" stroke="{INK}" stroke-width="8"/>')
    s.append('</g>')
    return "".join(s)


o.append(state("flat", top_flat, False))
o.append(state("wavy", top_wavy, True))
# grasa de la yema (compartida)
fat = f"M {X0 + 4} {YF} C 200 {YF - 6}, 500 {YF + 6}, {X1 - 4} {YF} L {X1 - 4} {YB - 30} Q {X1 - 4} {YB - 4} {X1 - 30} {YB - 4} L {X0 + 30} {YB - 4} Q {X0 + 4} {YB - 4} {X0 + 4} {YB - 30} Z"
o.append(f'<path d="{fat}" fill="url(#fat)"/>')
o.append('<g fill="#FFF4CF" stroke="#E2B95B" stroke-width="3">')
for i in range(24):
    x = X0 + 34 + (i % 12) * 51 + (14 if (i // 12) % 2 else 0)
    y = YF + 30 + (i // 12) * 42
    o.append(f'<ellipse cx="{x}" cy="{y}" rx="21" ry="16"/>')
o.append('</g>')
o.append(f'<path d="M {X0} {YB - 30} Q {X0} {YB} {X0 + 30} {YB} L {X1 - 30} {YB} Q {X1} {YB} {X1} {YB - 30}" fill="none" stroke="{INK}" stroke-width="8"/>')
o.append(f'<path d="M {X0} {YF - 40} L {X0} {YB - 30} M {X1} {YF - 40} L {X1} {YB - 30}" stroke="{INK}" stroke-width="8"/>')

# vasos sanguineos: arteriola horizontal + asas capilares hacia las papilas
YA = 418


def vessels(id_, wa, wc, loop_top):
    s = [f'<g id="{id_}">']
    loops = []
    for x in range(110, 680, 80):
        loops.append(f"M {x - 14} {YA} C {x - 14} {loop_top + 10}, {x - 12} {loop_top}, {x} {loop_top} C {x + 12} {loop_top}, {x + 14} {loop_top + 10}, {x + 14} {YA}")
    for d in loops:
        s.append(dbl(d, wc, "#E0352B", 6))
    d = f"M {X0 + 4} {YA} L {X1 - 4} {YA}"
    s.append(f'<path d="{d}" stroke="{INK}" stroke-width="{wa + 8}" stroke-linecap="butt"/>')
    s.append(f'<path d="{d}" stroke="url(#art{'w' if wa > 20 else 't'})" stroke-width="{wa}" stroke-linecap="butt"/>')
    s.append(f'<path d="M {X0 + 20} {YA - wa * 0.25:.1f} L {X1 - 20} {YA - wa * 0.25:.1f}" stroke="#FFB4A8" stroke-width="{max(2, wa * 0.14):.1f}" stroke-linecap="round" opacity="0.9"/>')
    # globulos rojos
    for x in range(100, 680, 46 if wa > 20 else 92):
        r = wa * 0.22
        s.append(f'<ellipse cx="{x}" cy="{YA + 2}" rx="{r * 1.3:.1f}" ry="{r:.1f}" fill="#B81E22" opacity="0.7"/>')
    s.append('</g>')
    return "".join(s)


o.append(vessels("vwide", 36, 13, 340))
o.append(vessels("vthin", 14, 6, 362))

# nervio: entra por la izquierda y manda ramas a la arteriola
YN = 515
o.append('<g id="nerve">')
o.append(dbl(f"M {X0 + 4} {YN} C 250 {YN - 6}, 450 {YN + 6}, 640 {YN}", 18, "url(#nrv)", 8, cap="butt"))
o.append(f'<path d="M {X0 + 20} {YN - 4} C 250 {YN - 10}, 450 {YN + 2}, 630 {YN - 4}" fill="none" stroke="#FFFBE0" stroke-width="4" opacity="0.9"/>')
o.append('<g id="branches">')
for x in (190, 350, 510):
    d = f"M {x} {YN - 8} C {x + 10} {YN - 40}, {x + 30} {YA + 40}, {x + 40} {YA + 14}"
    o.append(dbl(d, 7, "#F7CF2A", 6))
o.append('</g></g>')
# señal que recorre el nervio
o.append(f'<g id="signal"><circle cx="90" cy="{YN}" r="34" fill="url(#glow)"/><circle cx="90" cy="{YN}" r="11" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/></g>')

# agua sobre la piel (escena del mito)
o.append('<g id="soak">')
for x in (190, 380, 570):
    o.append(f'<path d="M {x} 150 C {x + 16} 175, {x + 16} 196, {x} 196 C {x - 16} 196, {x - 16} 175, {x} 150 Z" fill="#8FD3FF" stroke="{INK}" stroke-width="5"/>'
             f'<circle cx="{x - 6}" cy="182" r="4" fill="#FFFFFF"/>')
    o.append(arrow(f"sk{x}", [(x, 206), (x, 262)], "#8FD3FF", 8, 22))
o.append('</g>')
o.append(f'<g id="nox"><path d="M 300 130 L 460 250 M 460 130 L 300 250" stroke="{INK}" stroke-width="30" stroke-linecap="round"/>'
         f'<path d="M 300 130 L 460 250 M 460 130 L 300 250" stroke="{CORAL}" stroke-width="16" stroke-linecap="round"/></g>')
# encogimiento
o.append('<g id="shrink">' + arrow("sh1", [(360, 150), (360, 236)], CORAL, 10, 26) + arrow("sh2", [(580, 150), (580, 236)], CORAL, 10, 26) + '</g>')

# lupa: donde esta este trozo (yema del dedo)
cx, cy, R = 862, 162, 82
o.append(f'<g id="inset"><circle cx="{cx}" cy="{cy}" r="{R}" fill="#EAF4F7" stroke="{INK}" stroke-width="7"/>')
fin = f"M {cx - 100} {cy - 20} L {cx + 10} {cy - 40} C {cx + 60} {cy - 44}, {cx + 70} {cy + 20}, {cx + 30} {cy + 34} L {cx - 100} {cy + 50} Z"
o.append(f'<path d="{fin}" fill="url(#skin2)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
o.append(f'<path d="M {cx - 60} {cy - 30} L {cx + 8} {cy - 40} C {cx + 34} {cy - 42}, {cx + 46} {cy - 32}, {cx + 50} {cy - 18} L {cx - 60} {cy - 18} Z" fill="#F8E6DC" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')
o.append(f'<rect x="{cx + 2}" y="{cy + 14}" width="36" height="30" rx="5" fill="none" stroke="{LIME}" stroke-width="6"/><rect x="{cx + 2}" y="{cy + 14}" width="36" height="30" rx="5" fill="none" stroke="{INK}" stroke-width="2"/>')
o.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{INK}" stroke-width="7"/></g>')
o.append(f'<line x1="{cx + 4}" y1="{cy + 44}" x2="{X1 - 20}" y2="268" stroke="{INK}" stroke-width="4" stroke-linecap="round" opacity="0.6"/>')

# etiquetas (columna derecha)
o.append(tag("lpiel", 740, 262, "PIEL", lead=(740, 291, 690, 296)))
o.append(tag("lvasos", 740, 389, "VASOS", lead=(740, 418, 700, 418)))
o.append(tag("lnervio", 740, 486, "NERVIO", lead=(740, 515, 640, 515)))
o.append(tag("larrugas", 40, 150, "ARRUGAS", lead=(130, 208, 183, 314)))
o.append(tag("lmenos", 330, 76, "MENOS VOLUMEN", bg=CORAL, fg=INK))
o.append('</svg>')
print("\n".join(o))

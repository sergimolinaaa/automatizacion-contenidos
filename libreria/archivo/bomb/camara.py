import sys, random, math
sys.path.insert(0, '/tmp/claude-0/-home-user-automatizacion-contenidos/039df981-7a17-5355-b711-18510fb209db/scratchpad/bomb')
from lib import *

CY = 370  # eje del sistema
defs = '''
<radialGradient id="bg" cx="0.5" cy="0.5" r="0.75"><stop offset="0" stop-color="#FFF1E6"/><stop offset="1" stop-color="#F3D4C2"/></radialGradient>
<linearGradient id="resG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFF6C9"/><stop offset="0.6" stop-color="#F7DB78"/><stop offset="1" stop-color="#E8B83A"/></linearGradient>
<linearGradient id="wallG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#C2541F"/><stop offset="0.5" stop-color="#8A3412"/><stop offset="1" stop-color="#5A1E08"/></linearGradient>
<radialGradient id="cavG" cx="0.45" cy="0.4" r="0.7"><stop offset="0" stop-color="#FFF4E6"/><stop offset="1" stop-color="#FFCFA6"/></radialGradient>
<radialGradient id="glowG" cx="0.5" cy="0.55" r="0.6"><stop offset="0" stop-color="#FF5A36" stop-opacity="0.75"/><stop offset="0.7" stop-color="#FF8A3A" stop-opacity="0.35"/><stop offset="1" stop-color="#FFB050" stop-opacity="0"/></radialGradient>
<linearGradient id="musG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#F08A6A"/><stop offset="1" stop-color="#C9503A"/></linearGradient>
<linearGradient id="mercG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FF8A6A"/><stop offset="1" stop-color="#D9341A"/></linearGradient>
<radialGradient id="bubG" cx="0.35" cy="0.3" r="0.75"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#D8ECFF"/></radialGradient>
<clipPath id="cavClip"><ellipse cx="628" cy="370" rx="130" ry="114"/></clipPath>
<clipPath id="resClip"><path d="M 70 230 C 120 170, 270 170, 320 240 C 350 290, 350 450, 320 500 C 270 570, 120 570, 70 510 C 40 460, 40 280, 70 230 Z"/></clipPath>
'''
o = [svg_open(defs)]
o.append('<rect width="1000" height="700" fill="url(#bg)"/>')
# células del tejido de fondo (sin contorno, desaturadas)
random.seed(11)
cells = []
for _ in range(60):
    x, y = random.uniform(0, 1000), random.uniform(0, 700)
    r = random.uniform(16, 34)
    cells.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="#F7DCCB"/><circle cx="{x+3:.0f}" cy="{y+2:.0f}" r="{r*0.25:.0f}" fill="#EFC8B4"/>')
o.append('<g opacity="0.9">' + "".join(cells) + '</g>')

# ---------- depósito ----------
resd = "M 70 230 C 120 170, 270 170, 320 240 C 350 290, 350 450, 320 500 C 270 570, 120 570, 70 510 C 40 460, 40 280, 70 230 Z"
o.append('<g id="reservoir">')
o.append(f'<path d="{resd}" fill="url(#resG)"/>')
# moléculas en el líquido
def hq(cx, cy, r=15, a=0):
    pts = [(cx + r * math.cos(math.radians(30 + 60 * k + a)), cy + r * math.sin(math.radians(30 + 60 * k + a))) for k in range(6)]
    g = f'<path d="{P(pts)} Z" fill="#FFFFFF" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>'
    g += f'<circle cx="{cx}" cy="{cy}" r="{r*0.45:.1f}" fill="none" stroke="{INK}" stroke-width="2"/>'
    for sgn in (-1, 1):
        ex = cx + sgn * (r + 9) * math.sin(math.radians(-a)) * 0
        ax_, ay_ = cx + sgn * r * math.sin(math.radians(a)) * -1, cy + sgn * r * math.cos(math.radians(a))
        bx_, by_ = cx + sgn * (r + 12) * math.sin(math.radians(a)) * -1, cy + sgn * (r + 12) * math.cos(math.radians(a))
        g += f'<path d="M {ax_:.1f} {ay_:.1f} L {bx_:.1f} {by_:.1f}" stroke="{INK}" stroke-width="3"/><circle cx="{bx_:.1f}" cy="{by_:.1f}" r="6" fill="#FF6B4A" stroke="{INK}" stroke-width="2.5"/>'
    return g
def h2o2(cx, cy, a=0):
    g = f'<g transform="translate({cx} {cy}) rotate({a})">'
    g += f'<circle cx="-24" cy="-9" r="5.5" fill="#FFFFFF" stroke="{INK}" stroke-width="2.5"/><circle cx="24" cy="9" r="5.5" fill="#FFFFFF" stroke="{INK}" stroke-width="2.5"/>'
    g += f'<circle cx="-9" cy="0" r="10" fill="#FF6B4A" stroke="{INK}" stroke-width="3"/><circle cx="9" cy="0" r="10" fill="#FF6B4A" stroke="{INK}" stroke-width="3"/>'
    g += '<circle cx="-12" cy="-3" r="3" fill="#FFFFFF" opacity="0.7"/><circle cx="6" cy="-3" r="3" fill="#FFFFFF" opacity="0.7"/></g>'
    return g
o.append('<g id="mols">' + hq(140, 290) + hq(250, 450, a=20) + hq(130, 450, a=-15) + h2o2(230, 280, 25) + h2o2(180, 370, -20) + h2o2(282, 300, 60) + h2o2(110, 520 - 30, 10) + '</g>')
# bandas musculares
o.append('<g clip-path="url(#resClip)" fill="none" stroke="#D9824E" stroke-width="3" opacity="0.55">' + "".join(
    f'<path d="M {x} 160 C {x+16} 300, {x+16} 440, {x} 580"/>' for x in range(80, 340, 40)) + '</g>')
o.append(f'<path d="{resd}" fill="none" stroke="{INK}" stroke-width="7"/>')
o.append('<path d="M 96 236 C 140 196, 240 192, 290 232" fill="none" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round" opacity="0.85"/>')
o.append('</g>')

# ---------- conducto + válvula ----------
o.append(f'<path d="M 330 {CY-34} C 350 {CY-30}, 375 {CY-30}, 400 {CY-26} L 400 {CY+26} C 375 {CY+30}, 360 {CY+30}, 330 {CY+34} Z" fill="#F7D873" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
o.append(f'<path d="M 336 {CY-24} C 356 {CY-22}, 378 {CY-21}, 396 {CY-18}" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" opacity="0.8"/>')
# flujo de líquido (se dibuja)
# labios de la válvula (abiertos: hueco en el centro)
o.append(f'<g id="valvetop"><path d="M 392 {CY-48} C 428 {CY-50}, 446 {CY-30}, 442 {CY-14} C 426 {CY-10}, 406 {CY-12}, 392 {CY-16} Z" fill="url(#musG)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
         f'<path d="M 400 {CY-40} C 420 {CY-42}, 432 {CY-34}, 434 {CY-24}" fill="none" stroke="#FFC0A8" stroke-width="3.5" stroke-linecap="round"/></g>')
o.append(f'<g id="valvebot"><path d="M 392 {CY+48} C 428 {CY+50}, 446 {CY+30}, 442 {CY+14} C 426 {CY+10}, 406 {CY+12}, 392 {CY+16} Z" fill="url(#musG)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/></g>')

# ---------- cámara de reacción ----------
o.append(f'<path d="M 430 {CY-16} L 500 {CY-16} L 500 {CY+16} L 430 {CY+16} Z" fill="#FFCFA6" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
o.append('<g id="chamber">')
o.append(f'<ellipse cx="628" cy="{CY}" rx="165" ry="148" fill="url(#wallG)" stroke="{INK}" stroke-width="8"/>')
# textura esclerotizada
o.append('<g fill="#5A1E08" opacity="0.45">' + "".join(
    f'<circle cx="{628+153*math.cos(math.radians(a)):.0f}" cy="{CY+136*math.sin(math.radians(a)):.0f}" r="4"/>' for a in range(0, 360, 14)) + '</g>')
o.append(f'<path d="M 470 {CY-80} C 520 {CY-138}, 680 {CY-146}, 740 {CY-90}" fill="none" stroke="#F08A50" stroke-width="6" stroke-linecap="round" opacity="0.8"/>')
o.append(f'<ellipse cx="628" cy="{CY}" rx="130" ry="114" fill="url(#cavG)" stroke="{INK}" stroke-width="5"/>')
o.append('</g>')
# brillo de calor (aparece)
o.append(f'<g id="glow"><ellipse cx="628" cy="{CY}" rx="128" ry="112" fill="url(#glowG)"/></g>')
o.append(f'<path d="M 440 {CY-13} L 506 {CY-13} L 506 {CY+13} L 440 {CY+13} Z" fill="#FFCFA6"/>')
o.append(f'<path d="M 440 {CY-13} L 504 {CY-13} M 440 {CY+13} L 504 {CY+13}" stroke="{INK}" stroke-width="4"/>')
FD = f"M 250 {CY} C 330 {CY}, 380 {CY}, 430 {CY} C 470 {CY}, 500 {CY-6}, 540 {CY+4}"
o.append('<g id="flow">' + stroke2(FD, 10, "#F7C531", extra=6) + f'<g id="flowlines"><path d="{FD}" fill="none" stroke="#FFF6C9" stroke-width="4" stroke-linecap="round"/></g></g>')
# enzimas: glándulas en la pared
o.append('<g id="enzymes">')
for a in range(0, 360, 24):
    if 340 > a > 20 or True:
        x, y = 628 + 130 * math.cos(math.radians(a)), CY + 114 * math.sin(math.radians(a))
        if x > 745 and abs(y - CY) < 40:
            continue  # salida
        if x < 510 and abs(y - CY) < 40:
            continue  # entrada
        o.append(f'<path d="M {x-12*math.cos(math.radians(a)):.1f} {y-12*math.sin(math.radians(a)):.1f} L {x:.1f} {y:.1f}" stroke="{INK}" stroke-width="3"/>')
        o.append(f'<circle cx="{x-15*math.cos(math.radians(a)):.1f}" cy="{y-15*math.sin(math.radians(a)):.1f}" r="8.5" fill="#8C6CE8" stroke="{INK}" stroke-width="3"/>'
                 f'<circle cx="{x-17*math.cos(math.radians(a))-2:.1f}" cy="{y-17*math.sin(math.radians(a))-2:.1f}" r="2.5" fill="#FFFFFF" opacity="0.8"/>')
o.append('</g>')
# burbujas de oxígeno y ebullición
random.seed(2)
o.append('<g id="bubbles">')
for _ in range(16):
    a = random.uniform(0, 2 * math.pi); rr = random.uniform(0, 0.78)
    x = 628 + 112 * rr * math.cos(a); y = CY + 98 * rr * math.sin(a)
    r = random.uniform(7, 15)
    o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="url(#bubG)" stroke="{INK}" stroke-width="3"/><circle cx="{x-r*0.35:.0f}" cy="{y-r*0.35:.0f}" r="{r*0.28:.1f}" fill="#FFFFFF"/>')
o.append('</g>')
# flechas de presión (dentro)
o.append('<g id="press">')
for a in (-50, 0, 50, 180 - 40, 180 + 40):
    if a == 0:
        continue
    c, s_ = math.cos(math.radians(a)), math.sin(math.radians(a))
    o.append(arrow(f"pr{a%360}", [(628 + 40 * c, CY + 34 * s_), (628 + 98 * c, CY + 82 * s_)], CORAL, w=8, head=20))
o.append(arrow("prout", [(680, CY), (742, CY)], CORAL, w=9, head=22))
o.append('</g>')
# boquilla de salida
o.append(f'<path d="M 782 {CY-30} L 850 {CY-16} L 850 {CY+16} L 782 {CY+30} Z" fill="url(#wallG)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
o.append(f'<path d="M 756 {CY-14} L 850 {CY-6} L 850 {CY+6} L 756 {CY+14} Z" fill="#FFCFA6" stroke="{INK}" stroke-width="3"/>')

# ráfagas (3 nubecillas en fila)
def puff(id_, cx, cy, s):
    g = f'<g id="{id_}">'
    for dx, dy, r in ((0, 0, 22), (-16, -12, 14), (14, -14, 15), (18, 10, 13), (-14, 12, 12)):
        g += f'<circle cx="{cx+dx*s:.1f}" cy="{cy+dy*s:.1f}" r="{r*s:.1f}" fill="#FFF3D6" stroke="{INK}" stroke-width="3.5"/>'
    g += f'<circle cx="{cx-6*s:.1f}" cy="{cy-6*s:.1f}" r="{6*s:.1f}" fill="#FFFFFF"/>'
    return g + '</g>'
o.append('<g id="pulses">' + puff("p1", 888, CY, 1.0) + puff("p2", 940, CY - 8, 1.15) + puff("p3", 985, CY - 16, 0.9) + '</g>')

# termómetro
TX = 900
o.append('<g id="thermo">')
o.append(f'<rect x="{TX-20}" y="108" width="40" height="172" rx="20" fill="#FFFFFF" stroke="{INK}" stroke-width="6"/>')
o.append(f'<circle cx="{TX}" cy="292" r="30" fill="#FFFFFF" stroke="{INK}" stroke-width="6"/>')
o.append(f'<circle cx="{TX}" cy="292" r="20" fill="url(#mercG)" stroke="{INK}" stroke-width="3"/>')
for k, y in enumerate(range(132, 262, 26)):
    o.append(f'<path d="M {TX+20} {y} L {TX+8} {y}" stroke="{INK}" stroke-width="3.5"/>')
o.append('</g>')
o.append(f'<g id="mercury"><rect x="{TX-9}" y="122" width="18" height="150" rx="9" fill="url(#mercG)" stroke="{INK}" stroke-width="3"/></g>')
o.append(f'<path d="M {TX-10} 120 L {TX-10} 262" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" opacity="0.7"/>')

# etiquetas
o.append(tag("l100", 760, 140, "100 °C", bg=CORAL, fg=INK, leader=(TX - 22, 140), dot=False))
o.append(tag("lenz", 628, 612, "ENZIMAS", leader=(560, CY + 100)))
o.append(tag("lval", 430, 150, "VÁLVULA", leader=(420, CY - 48)))
o.append(tag("ldep", 190, 612, "DEPÓSITO", leader=(190, 548)))
o.append('</svg>')
print("\n".join(o))

import sys, random, math
sys.path.insert(0, '/tmp/claude-0/-home-user-automatizacion-contenidos/039df981-7a17-5355-b711-18510fb209db/scratchpad/bomb')
from lib import *
from beetle import jleg, antenna

CY = 320
PX, TL = 640, 92  # pivote de la punta del abdomen y su longitud
A_LADO, A_DEL = 70, 130
PRE = sys.argv[1] if len(sys.argv) > 1 else ""

defs = '''
<radialGradient id="soil" cx="0.5" cy="0.45" r="0.8"><stop offset="0" stop-color="#EBD3A6"/><stop offset="1" stop-color="#CFAE78"/></radialGradient>
<linearGradient id="orG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FF9A55"/><stop offset="0.5" stop-color="#E2561F"/><stop offset="1" stop-color="#A8380F"/></linearGradient>
<linearGradient id="bOrLeg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F58A45"/><stop offset="1" stop-color="#C0461A"/></linearGradient>
<linearGradient id="elU" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3D5AA8"/><stop offset="1" stop-color="#121A42"/></linearGradient>
<linearGradient id="elD" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2A3F80"/><stop offset="1" stop-color="#0B1030"/></linearGradient>
<radialGradient id="eyeG" cx="0.35" cy="0.35" r="0.75"><stop offset="0" stop-color="#3A3A48"/><stop offset="1" stop-color="#050508"/></radialGradient>
<linearGradient id="jetG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#FFD08A"/></linearGradient>
<linearGradient id="aBody" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7A4028"/><stop offset="1" stop-color="#2A120A"/></linearGradient>
<linearGradient id="leafG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#D99A45"/><stop offset="1" stop-color="#9C5E22"/></linearGradient>
'''
o = [svg_open(defs)]
o.append('<rect width="1000" height="700" fill="url(#soil)"/>')
random.seed(21)
g = []
for _ in range(220):
    x, y = random.uniform(0, 1000), random.uniform(0, 700)
    g.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.uniform(1.5, 4):.1f}"/>')
o.append('<g fill="#A9834E" opacity="0.5">' + "".join(g) + '</g>')
# piedras y hojas (con contorno suave)
for x, y, rx, ry, c in ((80, 140, 34, 24, "#C9B79F"), (930, 110, 40, 26, "#BCA98F"), (60, 620, 30, 20, "#BCA98F"), (560, 640, 24, 14, "#C9B79F"), (960, 640, 26, 18, "#C9B79F")):
    o.append(f'<ellipse cx="{x}" cy="{y+5}" rx="{rx}" ry="{ry}" fill="#8B6A3E" opacity="0.35"/><ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{c}" stroke="{INK}" stroke-width="4"/><ellipse cx="{x-rx*0.3:.0f}" cy="{y-ry*0.35:.0f}" rx="{rx*0.4:.0f}" ry="{ry*0.25:.0f}" fill="#FFFFFF" opacity="0.5"/>')
def leaf(cx, cy, L, ang, col="url(#leafG)"):
    s = f'<g transform="translate({cx} {cy}) rotate({ang})">'
    s += f'<path d="M {-L} 0 C {-L*0.5} {-L*0.45}, {L*0.5} {-L*0.45}, {L} 0 C {L*0.5} {L*0.45}, {-L*0.5} {L*0.45}, {-L} 0 Z" fill="{col}" stroke="{INK}" stroke-width="4" stroke-linejoin="round" opacity="0.85"/>'
    s += f'<path d="M {-L*0.95} 0 L {L*0.9} 0" stroke="#7A4614" stroke-width="3"/>'
    for t in (-0.5, -0.1, 0.3):
        s += f'<path d="M {L*t:.0f} 0 L {L*(t+0.25):.0f} {-L*0.27:.0f} M {L*t:.0f} 0 L {L*(t+0.25):.0f} {L*0.27:.0f}" stroke="#7A4614" stroke-width="2.5"/>'
    return s + '</g>'
o.append(leaf(470, 90, 70, -8))
o.append(leaf(860, 470, 55, 40, "#C7873A"))

# sombra del escarabajo
o.append(f'<ellipse cx="440" cy="{CY+14}" rx="270" ry="110" fill="#6B4A22" opacity="0.22"/>')

# patas (por debajo del cuerpo), simétricas
def legs_side(sgn):
    def m(p):
        return (p[0], CY + sgn * (p[1] - CY))
    s = ""
    s += jleg(m((300, 345)), m((262, 420)), m((214, 452)), m((176, 466)), "url(#bOrLeg)", 12, 8)
    s += jleg(m((372, 350)), m((392, 446)), m((424, 500)), m((446, 532)), "url(#bOrLeg)", 12, 8)
    s += jleg(m((420, 352)), m((506, 440)), m((592, 488)), m((634, 502)), "url(#bOrLeg)", 13, 8)
    return s
o.append('<g id="legs">' + legs_side(1) + legs_side(-1) + '</g>')

# punta del abdomen (gira sobre su base PX,CY)
o.append('<g id="tip">')
o.append(f'<rect x="{PX}" y="{CY-48}" width="{TL+4}" height="96" fill="none" opacity="0"/>')
o.append(f'<path d="M {PX} {CY-44} C {PX+50} {CY-44}, {PX+TL} {CY-24}, {PX+TL} {CY} C {PX+TL} {CY+24}, {PX+50} {CY+44}, {PX} {CY+44} Z" fill="url(#orG)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
for k, x in enumerate((PX + 30, PX + 56, PX + 76)):
    h = 40 - k * 9
    o.append(f'<path d="M {x} {CY-h} C {x+6} {CY-h/2}, {x+6} {CY+h/2}, {x} {CY+h}" fill="none" stroke="{INK}" stroke-width="3" opacity="0.55"/>')
o.append(f'<path d="M {PX+8} {CY-32} C {PX+40} {CY-34}, {PX+70} {CY-22}, {PX+82} {CY-8}" fill="none" stroke="#FFC69A" stroke-width="4" stroke-linecap="round"/>')
o.append(f'<circle cx="{PX+TL-4}" cy="{CY}" r="7" fill="#3A1206" stroke="{INK}" stroke-width="3"/>')
o.append('</g>')

# punta doblada hacia delante (bajo el cuerpo, asoma por el costado)
o.append('<g id="tipdel"><g transform="translate(604 396) rotate(130)">'
         f'<path d="M -20 -30 C 20 -30, 66 -20, 66 0 C 66 20, 20 30, -20 30 Z" fill="url(#orG)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
         f'<path d="M 30 -26 C 36 -12, 36 12, 30 26 M 48 -20 C 53 -8, 53 8, 48 20" fill="none" stroke="{INK}" stroke-width="3" opacity="0.55"/>'
         f'<circle cx="60" cy="0" r="7" fill="#3A1206" stroke="{INK}" stroke-width="3"/></g></g>')
# élitros (dos mitades)
def elytron(sgn):
    y0 = CY
    yo = CY + sgn * 98
    d = (f"M 352 {y0} L 352 {CY+sgn*70} C 356 {CY+sgn*96}, 380 {CY+sgn*102}, 420 {yo} "
         f"C 520 {yo}, 600 {CY+sgn*96}, 636 {CY+sgn*70} C 650 {CY+sgn*50}, 652 {CY+sgn*20}, 648 {y0} Z")
    col = "url(#elU)" if sgn < 0 else "url(#elD)"
    s = f'<path d="{d}" fill="{col}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
    for k in range(1, 6):
        yy = CY + sgn * k * 15
        s += f'<path d="M 370 {yy} C 450 {yy+sgn*2}, 560 {yy+sgn*2}, 630 {yy-sgn*k*2}" fill="none" stroke="#7F98DA" stroke-width="2" opacity="0.45"/>'
    # manchas amarillas
    s += f'<path d="M 400 {CY+sgn*30} C 404 {CY+sgn*70}, 430 {CY+sgn*88}, 456 {CY+sgn*80} C 470 {CY+sgn*70}, 462 {CY+sgn*52}, 476 {CY+sgn*40} C 486 {CY+sgn*28}, 470 {CY+sgn*18}, 450 {CY+sgn*20} C 430 {CY+sgn*22}, 408 {CY+sgn*16}, 400 {CY+sgn*30} Z" fill="#F7C531" stroke="#5A3A00" stroke-width="2.5"/>'
    s += f'<path d="M 560 {CY+sgn*36} C 570 {CY+sgn*22}, 600 {CY+sgn*24}, 606 {CY+sgn*44} C 612 {CY+sgn*64}, 590 {CY+sgn*78}, 572 {CY+sgn*72} C 556 {CY+sgn*66}, 552 {CY+sgn*48}, 560 {CY+sgn*36} Z" fill="#F7C531" stroke="#5A3A00" stroke-width="2.5"/>'
    return s
o.append('<g id="elytra">' + elytron(-1) + elytron(1))
o.append(f'<path d="M 380 {CY-78} C 460 {CY-92}, 560 {CY-90}, 620 {CY-70}" fill="none" stroke="#B9CBFF" stroke-width="5" stroke-linecap="round" opacity="0.8"/>')
o.append(f'<path d="M 352 {CY} L 648 {CY}" stroke="{INK}" stroke-width="4"/>')
o.append('</g>')
# pronoto
o.append(f'<path d="M 270 {CY-52} C 290 {CY-66}, 340 {CY-66}, 360 {CY-56} C 366 {CY-30}, 366 {CY+30}, 360 {CY+56} C 340 {CY+66}, 290 {CY+66}, 270 {CY+52} C 262 {CY+20}, 262 {CY-20}, 270 {CY-52} Z" fill="url(#orG)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
o.append(f'<path d="M 280 {CY-50} C 300 {CY-58}, 336 {CY-58}, 350 {CY-50}" fill="none" stroke="#FFD2A8" stroke-width="4" stroke-linecap="round"/>')
o.append(f'<path d="M 272 {CY} L 360 {CY}" stroke="{INK}" stroke-width="2.5" opacity="0.4"/>')
# cabeza
o.append('<g id="head">')
o.append(f'<path d="M 214 {CY-10} C 196 {CY-24}, 176 {CY-24}, 166 {CY-12} C 176 {CY-14}, 190 {CY-10}, 200 {CY-2} Z" fill="#5A1A08" stroke="{INK}" stroke-width="4"/>')
o.append(f'<path d="M 214 {CY+10} C 196 {CY+24}, 176 {CY+24}, 166 {CY+12} C 176 {CY+14}, 190 {CY+10}, 200 {CY+2} Z" fill="#5A1A08" stroke="{INK}" stroke-width="4"/>')
o.append(f'<path d="M 272 {CY-34} C 250 {CY-44}, 212 {CY-38}, 202 {CY-14} C 198 {CY}, 198 {CY}, 202 {CY+14} C 212 {CY+38}, 250 {CY+44}, 272 {CY+34} Z" fill="url(#orG)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
for sgn in (-1, 1):
    o.append(f'<ellipse cx="236" cy="{CY+sgn*36}" rx="14" ry="11" fill="url(#eyeG)" stroke="{INK}" stroke-width="4"/><circle cx="232" cy="{CY+sgn*36-4}" r="3.5" fill="#FFFFFF"/>')
o.append(f'<path d="M 222 {CY-24} C 236 {CY-30}, 254 {CY-30}, 264 {CY-24}" fill="none" stroke="#FFD2A8" stroke-width="4" stroke-linecap="round"/>')
o.append('</g>')
o.append('<g id="antennae">' + antenna((214, CY - 26), (170, CY - 80), (96, CY - 120), "url(#bOrLeg)") + antenna((214, CY + 26), (170, CY + 80), (96, CY + 120), "url(#bOrLeg)") + '</g>')


# ---- chorros ----
def jet(id_, pts, w0=6, w1=24):
    (x0, y0), (cx, cy), (x1, y1) = pts
    def q(t):
        return ((1-t)**2*x0 + 2*(1-t)*t*cx + t*t*x1, (1-t)**2*y0 + 2*(1-t)*t*cy + t*t*y1)
    L_, R_ = [], []
    for k in range(21):
        t = k / 20 * 0.98
        x, y = q(t); x2, y2 = q(t + 0.01)
        dx, dy = x2 - x, y2 - y; ln = math.hypot(dx, dy); nx, ny = -dy/ln, dx/ln
        w = w0 + (w1 - w0) * t
        L_.append((x + nx*w/2*1.6, y + ny*w/2*1.6)); R_.append((x - nx*w/2*1.6, y - ny*w/2*1.6))
    s = f'<g id="{id_}"><path d="{P(L_ + R_[::-1])} Z" fill="url(#jetG)" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    core = "M " + " L ".join(f"{q(0.05+0.85*k/10)[0]:.1f} {q(0.05+0.85*k/10)[1]:.1f}" for k in range(11))
    s += f'<path d="{core}" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>'
    ex, ey = q(1)
    for dx, dy, r in ((0, 0, 24), (-18, -16, 16), (18, -14, 17), (16, 16, 15), (-16, 14, 13)):
        s += f'<circle cx="{ex+dx:.1f}" cy="{ey+dy:.1f}" r="{r}" fill="#FFF3D6" stroke="{INK}" stroke-width="3.5"/>'
    s += f'<circle cx="{ex-7:.1f}" cy="{ey-7:.1f}" r="7" fill="#FFFFFF"/>'
    return s + '</g>'


def tipend(deg, extra=0):
    a = math.radians(deg)
    return (PX + (TL + extra) * math.cos(a), CY + (TL + extra) * math.sin(a))
e0 = tipend(0, 4)
o.append(jet("jback", [e0, (e0[0] + 90, CY - 6), (870, CY - 4)]))
e1 = tipend(A_LADO, 4)
o.append(jet("jside", [e1, (e1[0] + 30, e1[1] + 80), (e1[0] + 60, 572)]))
# delante: la punta se dobla bajo el cuerpo; el chorro asoma por el costado y va hacia delante
e2 = (604 + 70 * math.cos(math.radians(130)), 396 + 70 * math.sin(math.radians(130)))
o.append(jet("jfront", [e2, (500, 610), (300, 560)]))

# etiquetas
o.append(tag("latras", 860, 200, "ATRÁS", leader=(860, CY - 30)))
o.append(tag("llado", 870, 560, "DE LADO", leader=(e1[0] + 84, 560)))
o.append(tag("ldel", 150, 470, "DELANTE", leader=(262, 552)))

if PRE:
    ang = {"lado": A_LADO, "del": 0}.get(PRE, 0)
    if PRE == "del": o.append('<style>#tip{opacity:0}</style>')
    o.append(f'<style>#tip{{transform-box:fill-box;transform-origin:0% 50%;rotate:{ang}deg}}</style>')
o.append('</svg>')
print("\n".join(o))

import sys, re, random, math
sys.path.insert(0, '/tmp/claude-0/-home-user-automatizacion-contenidos/039df981-7a17-5355-b711-18510fb209db/scratchpad/bomb')
from lib import *
import beetle as B

X, Y, S = 520, 360, 1.6
PRE = len(sys.argv) > 1


def W(x, y):
    return (X + x * S, Y + y * S)


def thin_filled(svg, k):
    """Reduce el contorno de las formas rellenas (no de los trazos de patas) al escalar."""
    def fix(m):
        tag_ = m.group(0)
        if 'fill="none"' in tag_ or 'stroke-width' not in tag_:
            return tag_
        return re.sub(r'stroke-width="([\d.]+)"', lambda n: f'stroke-width="{float(n.group(1))*k:.1f}"', tag_)
    return re.sub(r'<(path|ellipse|circle|rect)\b[^>]*>', fix, svg)


defs = B.DEFS + '''
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#EEF4E6"/><stop offset="1" stop-color="#E4D8C0"/></linearGradient>
<linearGradient id="flesh" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFE9DC"/><stop offset="1" stop-color="#F2B9A0"/></linearGradient>
<linearGradient id="resG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFF6C9"/><stop offset="1" stop-color="#F1CB4E"/></linearGradient>
<radialGradient id="chG" cx="0.4" cy="0.35" r="0.7"><stop offset="0" stop-color="#FFF1DE"/><stop offset="1" stop-color="#FFC9A0"/></radialGradient>
'''
o = [svg_open(defs)]
o.append('<rect width="1000" height="700" fill="url(#bg)"/>')
# retícula técnica suave
o.append('<g stroke="#C9D3BE" stroke-width="2" opacity="0.6">' + "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="700"/>' for x in range(50, 1000, 50)) + "".join(f'<line x1="0" y1="{y}" x2="1000" y2="{y}"/>' for y in range(50, 700, 50)) + '</g>')
o.append('<ellipse cx="490" cy="530" rx="390" ry="20" fill="#6B5034" opacity="0.2"/>')

inner = B.legs_far() + B.body()
ant_ = B.antennae_custom(((-200, -30), (-232, -120), (-262, -176)), ((-206, -26), (-250, -110), (-300, -150)))
cut = []
# ventana de corte: borde izquierdo en zigzag
zz = [(-20, -56)]
for k in range(1, 10):
    zz.append((-20 + (6 if k % 2 else -6), -56 + k * 10))
zz = zz[::-1]
cutd = ("M -20 -57 C 20 -63, 60 -63, 100 -59 C 140 -55, 162 -42, 168 -24 L 196 -18 C 212 -10, 212 8, 198 15 "
        "C 170 26, 100 40, 40 41 C 10 41, -10 39, -20 36 " + " ".join(f"L {x} {y}" for x, y in zz) + " Z")
cut.append(f'<path d="{cutd}" fill="url(#flesh)" stroke="{INK}" stroke-width="3.2" stroke-linejoin="round"/>')
# fibras / tejido
cut.append('<g stroke="#E7A68C" stroke-width="1.2" fill="none" opacity="0.8">' + "".join(
    f'<path d="M {x} -50 C {x+10} -20, {x-6} 10, {x+4} 36"/>' for x in range(-6, 50, 12)) + '</g>')
# glándulas secretoras (racimo)
random.seed(5)
gl = ['<g id="glands">']
for (x, y, r) in ((-4, -40, 6.5), (8, -46, 6), (10, -34, 7), (-2, -26, 6), (22, -42, 6), (20, -28, 6.5), (30, -36, 5.5), (-8, -14, 6), (6, -16, 6.5)):
    gl.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#F59BB0" stroke="{INK}" stroke-width="1.8"/><circle cx="{x-2}" cy="{y-2}" r="{r*0.35:.1f}" fill="#FFFFFF" opacity="0.6"/>')
gl.append(stroke2("M 30 -36 C 40 -40, 46 -36, 52 -30", 2.2, "#F59BB0", extra=2.6))
gl.append(stroke2("M 8 -16 C 24 -8, 36 -12, 46 -14", 2.2, "#F59BB0", extra=2.6))
gl.append('</g>')
cut += gl
# depósito
resd = "M 50 -30 C 70 -48, 118 -48, 138 -28 C 150 -14, 150 10, 138 20 C 116 32, 70 32, 52 20 C 40 8, 38 -16, 50 -30 Z"
cut.append('<g id="reservoir">')
cut.append(f'<path d="{resd}" fill="url(#resG)" stroke="{INK}" stroke-width="3.2"/>')
cut.append('<g stroke="#D9824E" stroke-width="1.3" fill="none" opacity="0.7">' + "".join(
    f'<path d="M {x} {-44+abs(x-94)*0.12:.0f} C {x+4} -10, {x+4} 10, {x} {28-abs(x-94)*0.1:.0f}"/>' for x in range(60, 136, 12)) + '</g>')
cut.append('<path d="M 62 -32 C 80 -42, 110 -42, 128 -32" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" opacity="0.8"/>')


def hq(cx, cy, r=7):
    pts = [(cx + r * math.cos(math.radians(30 + 60 * k)), cy + r * math.sin(math.radians(30 + 60 * k))) for k in range(6)]
    g = f'<path d="{P(pts)} Z" fill="#FFFFFF" stroke="{INK}" stroke-width="1.6"/>'
    g += f'<circle cx="{cx}" cy="{cy}" r="{r*0.45:.1f}" fill="none" stroke="{INK}" stroke-width="1"/>'
    for sgn in (-1, 1):
        g += f'<path d="M {cx} {cy+sgn*r} L {cx} {cy+sgn*(r+3.5)}" stroke="{INK}" stroke-width="1.4"/><circle cx="{cx}" cy="{cy+sgn*(r+5.5)}" r="2.6" fill="#FF6B4A" stroke="{INK}" stroke-width="1"/>'
    return g


def h2o2(cx, cy, a=0):
    g = f'<g transform="translate({cx} {cy}) rotate({a})">'
    g += f'<circle cx="-12" cy="-4" r="2.3" fill="#FFFFFF" stroke="{INK}" stroke-width="1"/><circle cx="12" cy="4" r="2.3" fill="#FFFFFF" stroke="{INK}" stroke-width="1"/>'
    g += f'<circle cx="-4.5" cy="0" r="4.2" fill="#FF6B4A" stroke="{INK}" stroke-width="1.2"/><circle cx="4.5" cy="0" r="4.2" fill="#FF6B4A" stroke="{INK}" stroke-width="1.2"/></g>'
    return g


cut.append('<g id="mols">' + hq(72, -16) + hq(116, 6) + hq(88, 14) + h2o2(100, -22, 20) + h2o2(70, 10, -30) + h2o2(124, -16, 60) + '</g>')
cut.append('</g>')
# cuello hacia la válvula
cut.append(f'<path d="M 140 -9 L 152 -7 L 152 5 L 140 7 Z" fill="#F7D873" stroke="{INK}" stroke-width="2.6" stroke-linejoin="round"/>')
# cámara de reacción
cut.append('<g id="chamber">')
cut.append(f'<ellipse cx="180" cy="-1" rx="25" ry="17" fill="#8A3412" stroke="{INK}" stroke-width="3"/>')
cut.append(f'<ellipse cx="180" cy="-1" rx="18" ry="11" fill="url(#chG)" stroke="{INK}" stroke-width="1.6"/>')
cut.append('<path d="M 166 -14 C 176 -19, 188 -19, 196 -13" fill="none" stroke="#E0743C" stroke-width="2" stroke-linecap="round"/>')
cut.append(f'<path d="M 203 -4 L 214 -4 L 214 2 L 203 2 Z" fill="#FFC9A0" stroke="{INK}" stroke-width="1.6"/>')
cut.append('</g>')
enz = ['<g id="enzymes">']
for k in range(12):
    a = math.radians(k * 30 + 10)
    enz.append(f'<circle cx="{180+16*math.cos(a):.1f}" cy="{-1+9.5*math.sin(a):.1f}" r="2.3" fill="#7B5CD6" stroke="{INK}" stroke-width="0.9"/>')
enz.append('</g>')
cut += enz
# válvula (dos labios musculares)
cut.append(f'<g id="valvetop"><path d="M 151 -9 C 156 -9, 158 -4, 157 -1 L 151 -1 Z" fill="#D9541C" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/></g>')
cut.append(f'<g id="valvebot"><path d="M 151 7 C 156 7, 158 2, 157 -1 L 151 -1 Z" fill="#D9541C" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/></g>')
# chorro de líquido depósito -> cámara (se dibuja)
cut.append('<g id="flow">' + stroke2("M 120 -2 C 136 -2, 150 -1, 158 -1 C 166 -1, 172 -2, 180 -1", 3.2, "#F7C531", extra=2.4) + '</g>')

inner_full = thin_filled(inner, 0.6) + "".join(cut) + thin_filled(B.legs_near(), 0.6) + thin_filled(ant_, 0.6)
o.append(f'<g transform="translate({X} {Y}) scale({S})">' + inner_full + '</g>')

# etiquetas (coordenadas del lienzo)
o.append(tag("lres", 560, 112, "DEPÓSITO", leader=W(100, -40)))
o.append(tag("lval", 800, 190, "VÁLVULA", leader=W(154, -8)))
o.append(tag("lcam", 884, 282, "CÁMARA", leader=W(194, -12)))
o.append(tag("lenz", 892, 452, "ENZIMAS", leader=W(186, 9)))
# leyenda de moléculas (fichas con icono)
def chip(id_, cx, cy, text, icon):
    w = text_w(text) + 60
    g = f'<g id="{id_}"><rect x="{cx-w/2:.1f}" y="{cy-29}" width="{w:.1f}" height="58" rx="12" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/>'
    g += f'<g transform="translate({cx-w/2+40:.1f} {cy}) scale(1.5)">{icon}</g>'
    g += f'<text x="{cx+30:.1f}" y="{cy+11}" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="30" fill="{INK}">{text}</text></g>'
    return g
o.append(chip("lhq", 270, 618, "HIDROQUINONAS", hq(0, 0)))
o.append(chip("lh2o2", 720, 618, "AGUA OXIGENADA", h2o2(0, 0)))
o.append('</svg>')
print("\n".join(o))

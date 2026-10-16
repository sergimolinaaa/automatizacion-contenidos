"""Fig. · Corte de la cabeza del pez arquero: lengua + surco del paladar = tubo; las tapas de las branquias aprietan."""
import math
from lib import *

TOP = ((130, 168), (420, 120), (720, 150), (900, 250))          # perfil superior (cúbica)
BOT = ((910, 290), (830, 334), (700, 392), (560, 462))           # barbilla
BOT2 = ((560, 462), (450, 520), (300, 556), (130, 566))          # garganta
top = lambda t: cbez(*TOP, t)
f_top = lambda x: y_at_x(top, x)
head = (f"M 130 168 C 420 120, 720 150, 900 250 L 912 262 L 914 286 L 910 290 "
        f"C 830 334, 700 392, 560 462 C 450 520, 300 556, 130 566 Z")
PAL = ((470, 306), (600, 296), (760, 284), (900, 266))           # superficie inferior del paladar
pal = lambda t: cbez(*PAL, t)

defs = """
<radialGradient id="bg" cx="0.5" cy="0.45" r="0.8"><stop offset="0" stop-color="#EAF6FF"/><stop offset="1" stop-color="#BFE0F7"/></radialGradient>
<linearGradient id="skin" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8E9C78"/><stop offset="0.3" stop-color="#D5DCC6"/><stop offset="1" stop-color="#FFFFFF"/></linearGradient>
<linearGradient id="flesh" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F9E1D6"/><stop offset="1" stop-color="#EDB9A8"/></linearGradient>
<linearGradient id="bone" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFF6E2"/><stop offset="1" stop-color="#E6CFA2"/></linearGradient>
<linearGradient id="tongue" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFA3A0"/><stop offset="0.6" stop-color="#E5626A"/><stop offset="1" stop-color="#B23A4A"/></linearGradient>
<linearGradient id="cav" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#3D8FE0"/><stop offset="1" stop-color="#8FD3FF"/></linearGradient>
<radialGradient id="iris" cx="0.4" cy="0.35" r="0.7"><stop offset="0" stop-color="#F6E7A8"/><stop offset="0.6" stop-color="#C9A24A"/><stop offset="1" stop-color="#7A5A1E"/></radialGradient>
<radialGradient id="dropg" cx="0.35" cy="0.3" r="0.8"><stop offset="0" stop-color="#FFFFFF"/><stop offset="0.5" stop-color="#9FDBFF"/><stop offset="1" stop-color="#2F7FD6"/></radialGradient>
<clipPath id="hc"><path d="{head}"/></clipPath>
<clipPath id="ic"><circle cx="790" cy="522" r="92"/></clipPath>
""".replace("{head}", head)
o = [svg_open(defs)]
o.append('<rect width="1000" height="700" fill="url(#bg)"/>')
o.append('<g fill="none" stroke="#B9D9F0" stroke-width="2"><circle cx="560" cy="360" r="300"/><circle cx="560" cy="360" r="430"/></g>')
# resto del cuerpo, insinuado detrás del corte (sin contorno)
o.append('<path d="M 130 168 C 60 172, 0 190, -20 230 L -20 520 C 20 556, 80 566, 130 566 Z" fill="#CFE3EE"/>')

# cabeza: piel exterior + carne del corte
o.append(f'<path d="{head}" fill="url(#skin)"/>')
o.append('<g clip-path="url(#hc)">')
o.append(f'<path d="{head}" fill="url(#flesh)" transform="translate(0 0)" stroke="#E3E8DA" stroke-width="34"/>')
# fibras musculares
o.append('<g fill="none" stroke="#E0A796" stroke-width="2.5" opacity="0.7">' + "".join(
    f'<path d="M {x} 170 C {x + 30} 260, {x - 20} 400, {x + 10} 560"/>' for x in range(150, 330, 34)) + '</g>')
# cráneo (hueso sobre el paladar)
o.append(f'<path d="M 420 300 C 520 230, 700 200, 900 262 L 900 268 C 760 286, 600 298, 470 306 Z" fill="url(#bone)" stroke="{INK}" stroke-width="4"/>')
o.append('</g>')

# cavidad de la boca y de las branquias (agua)
cav = ("M 210 300 C 260 268, 380 280, 470 306 C 520 302, 560 300, 600 298 "
       "C 560 330, 540 360, 520 392 C 470 440, 360 470, 250 470 C 200 440, 190 340, 210 300 Z")
o.append(f'<g id="cavity"><path d="{cav}" fill="url(#cav)" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
         f'<path d="M 240 300 C 300 286, 380 290, 450 308" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.6"/></g>')
# branquias: 4 arcos con filamentos rojos
gl = []
for i in range(4):
    x0 = 228 + i * 30
    arc = [(x0 + 30 * math.sin(t / 10 * math.pi) * 0.4, 318 + t * 14) for t in range(11)]
    gl.append(f'<path d="{pts_d(arc)}" fill="none" stroke="#F3E3C3" stroke-width="7" stroke-linecap="round"/>')
    gl.append('<g stroke="#D9434F" stroke-width="4" stroke-linecap="round">' + "".join(
        f'<line x1="{f(x)}" y1="{f(y)}" x2="{f(x - 18)}" y2="{f(y + 4)}"/>' for x, y in arc[1:-1]) + '</g>')
o.append(f'<g id="gills">{"".join(gl)}</g>')

# lengua apretada contra el paladar
tongue = (f"M 520 392 C 540 350, 580 318, 640 302 C 720 290, 820 280, 884 272 "
          f"C 890 280, 884 290, 870 296 C 780 316, 690 350, 600 420 C 570 440, 530 430, 520 392 Z")
o.append(f'<g id="tongue"><path d="{tongue}" fill="url(#tongue)" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
         f'<path d="M 560 352 C 620 312, 720 300, 860 284" fill="none" stroke="#FFD2CC" stroke-width="4" stroke-linecap="round" opacity="0.8"/></g>')
# tubo: canal de agua entre lengua y surco
tube = "M 600 300 C 700 290, 800 280, 908 268"
o.append(f'<g id="tube"><path d="{tube}" fill="none" stroke="{INK}" stroke-width="18" stroke-linecap="round"/>'
         f'<path d="{tube}" fill="none" stroke="#8FD3FF" stroke-width="10" stroke-linecap="round"/></g>')
o.append(f'<g id="tubeflow"><path d="{tube}" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/></g>')
# surco del paladar (línea más oscura justo encima del tubo)
o.append(f'<g id="groove"><path d="M 600 290 C 700 280, 800 270, 900 258" fill="none" stroke="#B48A55" stroke-width="5" stroke-linecap="round"/></g>')
# mandíbula inferior
o.append(f'<path d="M 914 286 C 880 300, 860 312, 840 330" fill="none" stroke="{INK}" stroke-width="4" opacity="0.6"/>')

# contorno de la cabeza y corte
o.append(f'<path d="M 130 168 C 420 120, 720 150, 900 250 L 912 262 L 914 286 L 910 290 C 830 334, 700 392, 560 462 C 450 520, 300 556, 130 566" fill="none" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
zz = [(130 + (8 if k % 2 else -8), 168 + k * (566 - 168) / 16) for k in range(17)]
o.append(f'<path d="{dash_d(zz, 22, 10)}" fill="none" stroke="{INK}" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/>')
o.append('<path d="M 160 160 C 420 116, 700 146, 870 228" fill="none" stroke="#FFFFFF" stroke-width="4" opacity="0.7" stroke-linecap="round"/>')
# tapa de las branquias (opérculo): placa translúcida sobre las branquias
op = "M 360 150 C 300 240, 290 420, 340 530"
o.append(f'<g id="gill"><path d="M 360 150 C 300 240, 290 420, 340 530 C 260 520, 196 440, 196 330 C 200 240, 260 170, 360 150 Z" fill="#E8EEF2" fill-opacity="0.35"/>'
         f'<path d="{op}" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
         f'<path d="M 372 156 C 314 244, 304 418, 352 524" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.7"/></g>')
# ojo
o.append(f'<g id="eye"><circle cx="726" cy="224" r="25" fill="url(#iris)" stroke="{INK}" stroke-width="6"/><circle cx="730" cy="224" r="13" fill="{INK}"/>'
         f'<circle cx="719" cy="216" r="6" fill="#FFFFFF"/><circle cx="737" cy="232" r="2.5" fill="#FFFFFF"/></g>')

# flechas: las tapas aprietan
o.append('<g id="press">' + arrow(None, 420, 62, 412, f_top(412) - 6, CORAL) + arrow(None, 380, 654, 370, 548, CORAL) + '</g>')
# flujo de agua dentro
o.append(curved_arrow("wflow", "M 250 420 C 330 440, 440 400, 540 340", (540, 340), (500, 372), LIME, w=9, head=24))
# chorro saliendo por la boca
jd = "M 914 268 C 940 250, 966 226, 990 196"
o.append(f'<g id="jet"><path d="{jd}" fill="none" stroke="{INK}" stroke-width="20" stroke-linecap="round"/>'
         f'<path d="{jd}" fill="none" stroke="#8FD3FF" stroke-width="12" stroke-linecap="round"/>'
         f'<path d="{jd}" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" transform="translate(-3 -2)"/></g>')
o.append('<g id="jdrops">' + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#dropg)" stroke="{INK}" stroke-width="3"/>' for x, y, r in [(950, 200, 7), (976, 248, 6), (930, 222, 5)]) + '</g>')

# lupa: corte transversal del tubo
IC = (790, 522)
o.append('<g id="inset">')
o.append(f'<path d="{dash_d([(IC[0] - 20, IC[1] - 96), (760, 304)], 12, 9)}" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>')
o.append(f'<circle cx="760" cy="288" r="16" fill="none" stroke="{INK}" stroke-width="4"/>')
o.append(f'<circle cx="{IC[0]}" cy="{IC[1]}" r="98" fill="#FFFFFF" stroke="{INK}" stroke-width="7"/>')
o.append('<g clip-path="url(#ic)">')
o.append(f'<rect x="680" y="410" width="220" height="112" fill="url(#bone)"/>')
o.append(f'<path d="M 680 522 L 760 522 C 760 488, 820 488, 820 522 L 900 522" fill="none" stroke="{INK}" stroke-width="5"/>')
o.append(f'<rect x="680" y="524" width="220" height="110" fill="url(#tongue)"/>')
o.append(f'<path d="M 680 524 L 900 524" stroke="{INK}" stroke-width="5"/>')
o.append(f'<path d="M 763 522 C 763 492, 817 492, 817 522 Z" fill="#8FD3FF" stroke="{INK}" stroke-width="4"/>')
o.append('<circle cx="780" cy="508" r="5" fill="#FFFFFF"/>')
o.append('<path d="M 700 470 l 20 -10 M 850 452 l 20 -8 M 700 580 l 24 6 M 852 590 l 22 4" stroke="#C9A877" stroke-width="3"/>')
o.append('</g>')
o.append(f'<circle cx="{IC[0]}" cy="{IC[1]}" r="98" fill="none" stroke="{INK}" stroke-width="7"/>')
o.append(f'<text x="790" y="470" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="20" fill="#8A6A3A">PALADAR</text>')
o.append(f'<text x="790" y="586" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="20" fill="#FFFFFF">LENGUA</text>')
o.append('</g>')

L = []
L.append(label("lsurco", 880, 112, "SURCO", line_to=(846, 263)))
L.append(label("llengua", 520, 622, "LENGUA", line_to=(640, 340)))
L.append(label("ltubo", 932, 412, "TUBO", line_to=(796, 510)))
L.append(label("lbranq", 214, 622, "BRANQUIAS", line_to=(262, 440)))
for s_, box in L:
    o.append(s_)
print([b for _, b in L])
o.append('</svg>')
open("boca.svg", "w").write("\n".join(o))

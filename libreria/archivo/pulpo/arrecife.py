import math, random
from lib import *
import octo
W, H = 1080, 1920
defs = (octo.defs("rojo") + octo.defs("camu") +
        lg("sea", [(0, "#8ED8F8"), (0.45, "#3A9AD8"), (1, "#14457E")]) +
        lg("rock", [(0, "#A69479"), (0.6, "#857560"), (1, "#5A4D3E")]) +
        lg("rock2", [(0, "#9A8A70"), (1, "#5E5242")]) +
        lg("sand", [(0, "#E8D2A0"), (1, "#B99A64")]) +
        lg("ray", [(0, "#FFFFFF", 0.55), (1, "#FFFFFF", 0)]) +
        lg("coral", [(0, "#FF9E7A"), (1, "#E8603E")]) + lg("fan", [(0, "#B98CFF"), (1, "#7A4FD6")]) +
        lg("fish", [(0, "#FFE35A"), (1, "#F2A900")]) + lg("crono", [(0, "#FFFFFF"), (1, "#DCE3EA")]))
o = [header(defs, W, H)]
o.append(f'<rect width="{W}" height="{H}" fill="url(#sea)"/>')
# rayos de luz
o.append('<g id="rayos" opacity="0.8">' + "".join(f'<path d="M {x} -20 L {x + 70} -20 L {x + 260} 1300 L {x + 120} 1300 Z" fill="url(#ray)"/>' for x in (80, 380, 700)) + '</g>')
# arrecife lejano (sin contorno, desaturado)
o.append('<path d="M 0 1050 C 120 980, 200 1010, 300 960 C 420 900, 520 990, 640 950 C 760 910, 880 980, 1080 930 L 1080 1400 L 0 1400 Z" fill="#4E8FBF" opacity="0.7"/>')
o.append('<g fill="#5FA0CC" opacity="0.8"><path d="M 120 1000 q -10 -80 20 -150 q 10 60 0 150 Z"/><path d="M 880 960 q 10 -90 -14 -170 q -16 80 -6 170 Z"/><circle cx="760" cy="960" r="40"/><circle cx="260" cy="980" r="34"/></g>')
# peces lejanos
def fish(x, y, s=1.0, col="url(#fish)", flip=False):
    sx = -s if flip else s
    return (f'<g transform="translate({x} {y}) scale({sx} {s})">'
            f'<path d="M -40 0 C -20 -26, 30 -24, 44 0 C 30 24, -20 26, -40 0 Z" fill="{col}" stroke="{INK}" stroke-width="5"/>'
            f'<path d="M -38 0 L -66 -20 L -60 0 L -66 20 Z" fill="{col}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
            f'<path d="M -4 -20 Q 6 -2 -4 20" fill="none" stroke="#2347FF" stroke-width="7"/>'
            f'<circle cx="26" cy="-5" r="6" fill="#FFFFFF" stroke="{INK}" stroke-width="3"/><circle cx="28" cy="-5" r="3" fill="{INK}"/></g>')
o.append('<g id="peces">' + fish(170, 560, 0.9, flip=True) + fish(250, 500, 0.7, flip=True) + fish(110, 640, 0.6, flip=True) + '</g>')
# arena
o.append(f'<path d="M 0 1290 C 200 1270, 420 1300, 640 1282 C 820 1268, 960 1290, 1080 1280 L 1080 1920 L 0 1920 Z" fill="url(#sand)" stroke="{INK}" stroke-width="6"/>')
random.seed(4)
o.append('<g fill="#C9A86E" opacity="0.7">' + "".join(f'<ellipse cx="{random.uniform(0, 1080):.0f}" cy="{random.uniform(1310, 1900):.0f}" rx="{random.uniform(3, 9):.0f}" ry="{random.uniform(2, 5):.0f}"/>' for _ in range(120)) + '</g>')
# roca grande donde se posa el pulpo
rock = "M 120 1300 C 110 1200, 180 1120, 300 1110 C 380 1060, 520 1070, 600 1090 C 720 1060, 900 1100, 960 1180 C 1000 1230, 990 1290, 970 1310 Z"
o.append(f'<path d="{rock}" fill="url(#rock)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
o.append('<path d="M 220 1150 C 300 1110, 400 1100, 480 1105" fill="none" stroke="#C9B89A" stroke-width="6" stroke-linecap="round" opacity="0.8"/>')
random.seed(9)
blots = []
for _ in range(40):
    x, y = random.uniform(180, 920), random.uniform(1130, 1290)
    r = random.uniform(6, 20)
    blots.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r:.0f}" ry="{r * 0.6:.0f}" fill="#5B4E3C" opacity="0.5"/>')
for _ in range(40):
    x, y = random.uniform(180, 920), random.uniform(1130, 1290)
    blots.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.uniform(2, 5):.1f}" fill="#D8CDB6" opacity="0.8"/>')
o.append('<g>' + "".join(blots) + '</g>')
# roca de fondo detrás del pulpo (para que el camuflaje "desaparezca")
o.append(f'<path d="M 300 1110 C 280 900, 360 760, 460 720 C 560 680, 700 700, 760 800 C 820 900, 800 1040, 740 1090 Z" fill="url(#rock2)" stroke="{INK}" stroke-width="6" stroke-linejoin="round" opacity="0.95"/>')
for _ in range(22):
    x, y = random.uniform(360, 760), random.uniform(760, 1080)
    r = random.uniform(6, 16)
    o.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r:.0f}" ry="{r * 0.6:.0f}" fill="#4F4334" opacity="0.45"/>')
# corales (izquierda) y gorgonia (derecha), con contorno
CO = ['<g id="coral">']
def branch(x0, y0, pts, w):
    return dbl(f"M {x0} {y0} " + " ".join(f"Q {a} {b} {c} {d}" for a, b, c, d in pts), w, "#FF7F5C", 8)
CO.append(branch(120, 1300, [(110, 1200, 70, 1150)], 16) + branch(120, 1300, [(140, 1190, 190, 1130)], 16) + branch(120, 1250, [(80, 1230, 50, 1190)], 12) + branch(160, 1200, [(200, 1180, 210, 1150)], 10))
for x, y in ((70, 1150), (190, 1130), (50, 1190), (210, 1150)):
    CO.append(f'<circle cx="{x}" cy="{y}" r="9" fill="#FFC2A8" stroke="{INK}" stroke-width="4"/>')
CO.append('</g>')
o.append("".join(CO))
o.append('<g id="algas">' + dbl("M 1000 1300 C 980 1200, 1030 1120, 1000 1020 C 980 960, 1010 900, 1000 860", 14, "#36B37E") + dbl("M 1040 1300 C 1060 1220, 1020 1150, 1050 1080", 10, "#5CCB8A") + '</g>')
o.append(f'<g id="anemona"><ellipse cx="900" cy="1296" rx="50" ry="14" fill="#000" opacity="0.2"/>' + "".join(dbl(f"M 900 1290 Q {900 + 50 * math.sin(a)} {1250} {900 + 60 * math.sin(a)} {1220 + 10 * abs(math.cos(a))}", 7, "#FF9EC8", 6) for a in (-1.2, -0.7, -0.25, 0.25, 0.7, 1.2)) + f'<ellipse cx="900" cy="1290" rx="34" ry="14" fill="#E85A9A" stroke="{INK}" stroke-width="5"/></g>')
# ---- pulpo: estado camuflado y estado rojo ----
o.append('<g id="pulpo">')
o.append('<g id="camu">' + octo.body("camu") + '</g>')
o.append('<g id="rojo">' + octo.body("rojo") + '</g>')
o.append('<g id="ojos">' + octo.eyes() + '</g>')
o.append('</g>')
# burbujas
o.append('<g id="burbujas" fill="#FFFFFF" fill-opacity="0.35" stroke="#FFFFFF" stroke-width="3">' + "".join(f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x, y, r in ((690, 560, 10), (712, 510, 7), (700, 470, 5), (380, 640, 8), (366, 590, 5))) + '</g>')
# cronómetro
C = ['<g id="crono">']
cx, cy = 880, 600
C.append(f'<rect x="{cx - 14}" y="{cy - 102}" width="28" height="22" rx="5" fill="#C7CFD8" stroke="{INK}" stroke-width="5"/>')
C.append(f'<circle cx="{cx}" cy="{cy}" r="86" fill="url(#crono)" stroke="{INK}" stroke-width="7"/>')
C.append(f'<circle cx="{cx}" cy="{cy}" r="70" fill="none" stroke="#D6DCE3" stroke-width="4"/>')
for k in range(12):
    a = math.radians(k * 30)
    C.append(f'<path d="M {cx + 62 * math.sin(a):.0f} {cy - 62 * math.cos(a):.0f} L {cx + 72 * math.sin(a):.0f} {cy - 72 * math.cos(a):.0f}" stroke="{INK}" stroke-width="4"/>')
C.append(f'<path d="M {cx} {cy} L {cx + 60 * math.sin(math.radians(80)):.0f} {cy - 60 * math.cos(math.radians(80)):.0f} A 60 60 0 0 0 {cx} {cy - 60} Z" fill="{LIME}" opacity="0.9"/>')
C.append(txt(cx, cy + 40, "&lt;1 s", 26))
C.append('</g>')
o.append("".join(C))
o.append(f'<g id="aguja"><path d="M {cx} {cy} L {cx} {cy - 62}" stroke="{CORAL}" stroke-width="7" stroke-linecap="round"/></g>')
o.append(f'<g id="eje"><circle cx="{cx}" cy="{cy}" r="8" fill="{INK}"/></g>')
# etiqueta
s, _ = tag("lpulpo", 250, 720, "¡ES UN PULPO!", size=30)
s = s.replace('<g id="lpulpo">', f'<g id="lpulpo"><line x1="290" y1="749" x2="410" y2="790" stroke="{INK}" stroke-width="5" stroke-linecap="round"/><circle cx="410" cy="790" r="9" fill="{LIME}" stroke="{INK}" stroke-width="4"/>')
o.append(s)
o.append('</svg>')
open("arrecife_full.svg", "w").write("\n".join(o))

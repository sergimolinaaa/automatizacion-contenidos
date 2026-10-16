import sys, math, random
sys.path.insert(0, sys.path[0])
from dl import *

G = 520                      # suelo
E = (752, 343)               # ojo del observador
ALT = 22                     # altura del Sol (grados)
dsun = (math.cos(math.radians(ALT)), -math.sin(math.radians(ALT)))      # hacia el Sol
danti = (-dsun[0], -dsun[1])                                             # punto antisolar (hacia la sombra)

def rot(v, deg):  # gira en pantalla (positivo = horario)
    a = math.radians(deg)
    return (v[0] * math.cos(a) - v[1] * math.sin(a), v[0] * math.sin(a) + v[1] * math.cos(a))

up42 = rot(danti, 42)        # 42° por encima de la dirección antisolar (rojo)
up40 = rot(danti, 40)        # violeta
lo42 = rot(danti, -42)       # 42° por debajo: se mete bajo el suelo

def at_x(d, x):
    t = (x - E[0]) / d[0]
    return (x, E[1] + d[1] * t)

def at_y(d, y):
    t = (y - E[1]) / d[1]
    return (E[0] + d[0] * t, y)

DX = 322
D = at_x(up42, DX)
D2 = at_x(up40, DX)
S = at_y(danti, G)           # sombra de la cabeza
L = at_y(lo42, G)
print("D", D, "D2", D2, "S", S, "L", L, file=sys.stderr)

defs = "\n".join([
    lg("sky", [(0, "#5E7491"), (0.55, "#9DB7CF"), (1, "#E9F1F6")], 0, 0, 1, 0.15),
    lg("skyr", [(0, "#BFE0F5", 0), (1, "#FFE9B8", 0.85)], 0, 0, 1, 0),
    lg("grass", [(0, "#7CCB6A"), (1, "#3F9A4A")]),
    lg("soil", [(0, "#A27A55"), (1, "#6E4E35")]),
    rg("sun", [(0, "#FFFFFF"), (0.45, "#FFF1A8"), (1, "#FFC93C")], 0.4, 0.4, 0.6),
    rg("sunglow", [(0, "#FFE680", 0.7), (1, "#FFE680", 0)]),
    rg("cloud", [(0, "#8C9AAE"), (1, "#56657A")], 0.5, 0.3, 0.7),
    lg("jacket", [(0, "#FF7A57"), (1, "#D9431F")]),
    lg("pants", [(0, "#3C4A66"), (1, "#222B3D")]),
    rg("skin", [(0, "#F6CBA6"), (1, "#D99A6C")], 0.4, 0.35, 0.7),
    rg("rdrop", [(0, "#FFFFFF"), (0.5, "#FF8A80"), (1, "#E3261B")], 0.38, 0.32, 0.7),
    rg("vdrop", [(0, "#FFFFFF"), (0.5, "#C39BFF"), (1, "#7B35E8")], 0.38, 0.32, 0.7),
    rg("gdrop", [(0, "#FFFFFF", 0.9), (1, "#8DB8DA", 0.9)], 0.38, 0.32, 0.7),
])
o = [header(defs)]
o.append('<rect width="1000" height="700" fill="url(#sky)"/>')
o.append('<rect width="1000" height="700" fill="url(#skyr)"/>')
# colinas lejanas
o.append(f'<path d="M 0 {G - 30} C 160 {G - 60}, 300 {G - 40}, 460 {G - 55} C 620 {G - 70}, 800 {G - 38}, 1000 {G - 52} L 1000 {G} L 0 {G} Z" fill="#AFC9B4" opacity="0.8"/>')
# sol (bajo, detrás del observador)
SUN = (E[0] + dsun[0] * 210, E[1] + dsun[1] * 210)
o.append(f'<g id="sol"><circle cx="{SUN[0]:.0f}" cy="{SUN[1]:.0f}" r="120" fill="url(#sunglow)"/>'
         f'<circle cx="{SUN[0]:.0f}" cy="{SUN[1]:.0f}" r="44" fill="url(#sun)" stroke="{INK}" stroke-width="6"/>'
         f'<ellipse cx="{SUN[0] - 13:.0f}" cy="{SUN[1] - 15:.0f}" rx="12" ry="7" fill="#FFFFFF" opacity="0.8"/></g>')
# rayos de sol paralelos (tenues)
rs = []
for k in range(-3, 4):
    p0 = (SUN[0] - dsun[1] * k * 60, SUN[1] + dsun[0] * k * 60)
    p1 = (p0[0] + danti[0] * 900, p0[1] + danti[1] * 900)
    rs.append(f"M {p0[0]:.0f} {p0[1]:.0f} L {p1[0]:.0f} {p1[1]:.0f}")
o.append(f'<g id="rayos"><path d="{" ".join(rs)}" stroke="#FFF3C4" stroke-width="10" opacity="0.18"/></g>')

# nube de lluvia y cortina de lluvia (a la izquierda)
o.append('<g id="lluvia">')
rnd = random.Random(8)
st = []
for _ in range(70):
    x, y = rnd.uniform(50, 470), rnd.uniform(130, G - 30)
    st.append(f"M {x:.0f} {y:.0f} L {x - 7:.0f} {y + 30:.0f}")
o.append(f'<path d="{" ".join(st)}" stroke="#6C86A6" stroke-width="3.5" opacity="0.55" stroke-linecap="round"/>')
o.append('</g>')
gd = []
for _ in range(26):
    x, y = rnd.uniform(60, 460), rnd.uniform(150, G - 40)
    if math.hypot(x - D[0], y - D[1]) < 50 or math.hypot(x - D2[0], y - D2[1]) < 40:
        continue
    gd.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="5" fill="url(#gdrop)" stroke="#3E5674" stroke-width="1.5"/>')
o.append('<g id="gotitas">' + "".join(gd) + '</g>')
cl = [(120, 120, 70, 40), (210, 98, 80, 52), (310, 112, 78, 44), (400, 128, 60, 34), (180, 138, 90, 30), (330, 140, 100, 28)]
cpath = "".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}"/>' for x, y, rx, ry in cl)
o.append(f'<g id="nube"><g fill="{INK}" transform="translate(0 0)">' + "".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx + 5}" ry="{ry + 5}"/>' for x, y, rx, ry in cl) + '</g>'
         f'<g fill="url(#cloud)">{cpath}</g>'
         f'<path d="M 140 92 C 170 72, 230 60, 270 74" fill="none" stroke="#B9C4D3" stroke-width="6" stroke-linecap="round" opacity="0.8"/></g>')

# suelo en corte: hierba + tierra
o.append(f'<path d="M 0 {G} L 1000 {G} L 1000 700 L 0 700 Z" fill="url(#soil)"/>')
o.append(f'<g fill="#8A6444" opacity="0.6"><ellipse cx="140" cy="600" rx="22" ry="9"/><ellipse cx="520" cy="640" rx="16" ry="7"/><ellipse cx="880" cy="610" rx="26" ry="10"/></g>')
o.append(f'<path d="M 0 {G} L 1000 {G} L 1000 {G + 22} L 0 {G + 22} Z" fill="url(#grass)" stroke="{INK}" stroke-width="6"/>')
o.append(f'<path d="M 0 {G + 3} L 1000 {G + 3}" stroke="#B5EBA0" stroke-width="3" opacity="0.8"/>')
blades = []
for x in range(10, 1000, 22):
    h = rnd.uniform(8, 16)
    blades.append(f"M {x} {G} L {x + 3:.0f} {G - h:.0f} L {x + 7} {G}")
o.append(f'<path d="{" ".join(blades)}" fill="#5DB257" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>')

# sombra alargada del observador sobre la hierba
o.append(f'<g id="sombra"><path d="M 800 {G - 2} L 760 {G - 2} L {S[0] + 30:.0f} {G - 1} C {S[0] + 4:.0f} {G - 9}, {S[0] - 22:.0f} {G - 6}, {S[0] - 22:.0f} {G} C {S[0] - 20:.0f} {G + 6}, {S[0] + 6:.0f} {G + 8}, {S[0] + 30:.0f} {G + 3} L 760 {G + 4} L 800 {G + 4} Z" fill="#1E3A20" opacity="0.55"/></g>')

# líneas de 42°
anti_d = f"M {E[0]} {E[1]} L {S[0]:.1f} {S[1]:.1f}"
under = f"M {S[0]:.1f} {S[1]:.1f} L {S[0] + danti[0] * 220:.1f} {S[1] + danti[1] * 220:.1f}"
o.append(f'<g id="anti"><path d="{anti_d}" stroke="{INK}" stroke-width="9" stroke-dasharray="18 12"/><path d="{anti_d}" stroke="#FFFFFF" stroke-width="4" stroke-dasharray="18 12"/>'
         f'<path d="{under}" stroke="#FFFFFF" stroke-width="4" stroke-dasharray="12 12" opacity="0.6"/></g>')
o.append(f'<g id="lower"><path d="M {E[0]} {E[1]} L {L[0]:.1f} {L[1]:.1f}" stroke="{LIME}" stroke-width="4" stroke-dasharray="14 10"/>'
         f'<path d="M {L[0]:.1f} {L[1]:.1f} L {L[0] + lo42[0] * 120:.1f} {L[1] + lo42[1] * 120:.1f}" stroke="{LIME}" stroke-width="4" stroke-dasharray="10 10" opacity="0.55"/></g>')
o.append(f'<g id="upline"><path d="M {E[0]} {E[1]} L {D[0]:.1f} {D[1]:.1f}" stroke="{LIME}" stroke-width="4" stroke-dasharray="14 10"/></g>')
# rayo de sol que llega a la gota y luz roja/violeta que va al ojo
t0 = (D[1] - 45) / -dsun[1]
P = (D[0] + dsun[0] * t0, D[1] + dsun[1] * t0)
o.append(arrow("sunray", P[0], P[1], D[0] + dsun[0] * 20, D[1] + dsun[1] * 20, "#FFE14D", w=7, head=22))
o.append('<g id="toeye">' + dbl(f"M {D2[0] + 10:.1f} {D2[1]:.1f} L {E[0] - 6} {E[1] + 2}", 4, "#9B4DFF", 5) +
         dbl(f"M {D[0] + 10:.1f} {D[1]:.1f} L {E[0] - 6} {E[1] - 2}", 6, "#FF3B30", 6) + '</g>')
# gotas protagonistas
o.append(f'<g id="gotar"><circle cx="{D[0]:.1f}" cy="{D[1]:.1f}" r="15" fill="url(#rdrop)" stroke="{INK}" stroke-width="4"/><circle cx="{D[0] - 5:.1f}" cy="{D[1] - 5:.1f}" r="4" fill="#FFFFFF"/></g>')
o.append(f'<g id="gotav"><circle cx="{D2[0]:.1f}" cy="{D2[1]:.1f}" r="12" fill="url(#vdrop)" stroke="{INK}" stroke-width="4"/><circle cx="{D2[0] - 4:.1f}" cy="{D2[1] - 4:.1f}" r="3.5" fill="#FFFFFF"/></g>')

# observador de perfil, mirando a la izquierda
def person():
    s = '<g id="persona">'
    # piernas
    s += dbl(f"M 786 452 L 790 486 L 796 {G - 4}", 17, "url(#pants)", 8)
    s += dbl(f"M 772 452 L 764 488 L 758 {G - 4}", 17, "url(#pants)", 8)
    # botas
    s += f'<path d="M 744 {G - 14} L 768 {G - 14} L 770 {G} L 738 {G} Q 736 {G - 10}, 744 {G - 14} Z" fill="#4A3426" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    s += f'<path d="M 784 {G - 14} L 808 {G - 14} L 808 {G} L 778 {G} Q 776 {G - 10}, 784 {G - 14} Z" fill="#4A3426" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    # mochila
    s += f'<rect x="796" y="376" width="34" height="66" rx="12" fill="#3E8E6A" stroke="{INK}" stroke-width="6"/><rect x="802" y="384" width="8" height="40" rx="4" fill="#7DD3A8" opacity="0.7"/>'
    # torso (chaqueta)
    s += f'<path d="M 756 384 C 756 368, 800 366, 802 384 L 806 452 C 790 460, 768 460, 754 452 Z" fill="url(#jacket)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
    s += '<path d="M 764 382 C 772 374, 790 374, 796 382" fill="none" stroke="#FFB49E" stroke-width="4" stroke-linecap="round"/>'
    s += f'<path d="M 776 392 L 778 450" stroke="{INK}" stroke-width="3" opacity="0.4"/>'
    # brazo señalando hacia la lluvia
    s += dbl("M 768 392 L 742 420 L 712 404", 14, "url(#jacket)", 7)
    s += f'<circle cx="708" cy="402" r="8" fill="url(#skin)" stroke="{INK}" stroke-width="4"/>'
    # cuello y cabeza
    s += f'<rect x="770" y="358" width="14" height="14" fill="url(#skin)" stroke="{INK}" stroke-width="4"/>'
    s += f'<circle cx="772" cy="338" r="26" fill="url(#skin)" stroke="{INK}" stroke-width="6"/>'
    s += f'<path d="M 748 334 L 740 343 L 749 346" fill="url(#skin)" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
    # gorro
    s += f'<path d="M 748 330 C 748 302, 798 300, 798 330 L 806 332 C 806 338, 744 336, 744 330 Z" fill="#2F6FD6" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    s += '<path d="M 758 318 C 766 310, 780 308, 788 312" fill="none" stroke="#8FB8FF" stroke-width="4" stroke-linecap="round"/>'
    s += f'<circle cx="{E[0]}" cy="{E[1]}" r="3.5" fill="{INK}"/>'
    s += f'<path d="M 780 340 C 784 336, 790 338, 790 344" fill="none" stroke="#B9774A" stroke-width="3"/>'
    s += '</g>'
    return s
o.append(person())

# arco de 42° en el ojo
ra = 120
a0 = math.atan2(danti[1], danti[0]); a1 = math.atan2(up42[1], up42[0])
p0 = (E[0] + math.cos(a0) * ra, E[1] + math.sin(a0) * ra)
p1 = (E[0] + math.cos(a1) * ra, E[1] + math.sin(a1) * ra)
o.append('<g id="ang">' + dbl(f"M {p0[0]:.1f} {p0[1]:.1f} A {ra} {ra} 0 0 1 {p1[0]:.1f} {p1[1]:.1f}", 6, LIME, 6) + '</g>')
am = a0 + math.radians(21)
lx, ly = E[0] + math.cos(am) * 190, E[1] + math.sin(am) * 190
o.append(f'<g id="l42"><text x="{lx:.0f}" y="{ly + 20:.0f}" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="56" fill="{LIME}" stroke="{INK}" stroke-width="10" paint-order="stroke" stroke-linejoin="round">42°</text></g>')

labels = []
t, b = tag("lsombra", S[0], 600, "TU SOMBRA", target=(S[0] - 6, G - 2), anchor_from=(S[0], 572)); o.append(t); labels.append(b)
t, b = tag("lgota", 160, 262, "GOTA", target=(D[0] - 17, D[1] + 4), anchor_from=(180, 234)); o.append(t); labels.append(b)
t, b = tag("lsuelo", 640, 610, "BAJO TIERRA", bg="#FFFFFF", fg=INK, target=(L[0] + lo42[0] * 70, L[1] + lo42[1] * 70), anchor_from=(660, 582)); o.append(t); labels.append(b)
for i in range(len(labels)):
    for j in range(i + 1, len(labels)):
        if boxes_overlap(labels[i], labels[j]):
            print("SOLAPE", i, j, file=sys.stderr)
print("42 label", lx, ly, "sun", SUN, file=sys.stderr)
o.append('</svg>')
open(sys.argv[1], "w").write("\n".join(o))

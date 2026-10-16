import sys, math, random
sys.path.insert(0, sys.path[0])
from seeds import *

AX, AY = 500, 250        # ápice del vilano
BEAK_END = 532           # fin del pico / arranque del aquenio
ACH_L, ACH_W = 112, 34

defs = "\n".join([
    rg("bg", [(0, "#5E9FC0"), (0.55, "#2F6A8C"), (1, "#173A55")], 0.5, 0.35, 0.8),
    rg("bokeh", [(0, "#CFF0FF", 0.35), (1, "#CFF0FF", 0)]),
    rg("bokehg", [(0, "#7FC77A", 0.6), (1, "#7FC77A", 0)]),
    lg("beak", [(0, "#F7F2DE"), (0.5, "#E6DCB8"), (1, "#C9BC90")], 0, 0, 1, 0),
    rg("drop", [(0, "#FFFFFF"), (0.45, "#BFE6FF"), (1, "#4C9BE0")], 0.38, 0.32, 0.75),
    DEFS_SEED,
])
o = [header(defs)]
o.append('<rect width="1000" height="700" fill="url(#bg)"/>')
# fondo desenfocado: bokeh y hierba lejana sin contorno
rnd = random.Random(2)
bk = []
for _ in range(14):
    x, y, r = rnd.uniform(0, 1000), rnd.uniform(60, 640), rnd.uniform(25, 70)
    bk.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="url(#bokeh)"/>')
o.append('<g id="bokeh">' + "".join(bk) + '</g>')
o.append('<path d="M 0 610 C 150 590, 300 615, 500 600 C 700 588, 850 612, 1000 598 L 1000 700 L 0 700 Z" fill="#2E6A4A" opacity="0.85"/>')
o.append('<g fill="url(#bokehg)"><circle cx="120" cy="600" r="80"/><circle cx="880" cy="590" r="90"/><circle cx="320" cy="640" r="60"/></g>')

# ---- semilla
o.append('<g id="seed">')
# sombra suave de la semilla
o.append('<ellipse cx="520" cy="660" rx="70" ry="9" fill="#0B1F30" opacity="0.35"/>')

open_lines = pappus_lines(AX, AY, 250, n=100, theta=12, elev=15, seed=21, curl=0.22)
back_o, front_o = fil_svg(open_lines, w=2.6, edge=5.4, barbs=7, back_op=0.6, edgecol="#22384C")
closed_lines = pappus_lines(AX, AY, 188, n=100, theta=64, elev=15, seed=21, curl=0.12)
back_c, front_c = fil_svg(closed_lines, w=2.6, edge=5.4, barbs=5, back_op=0.6, edgecol="#22384C")

o.append('<g id="abierto">' + back_o + '</g>')
o.append('<g id="cerradob">' + back_c + '</g>')
# pico
beak = f"M {AX} {AY} L {AX} {BEAK_END}"
o.append(f'<g id="pico"><path d="{beak}" stroke="{INK}" stroke-width="15" stroke-linecap="round"/>'
         f'<path d="{beak}" stroke="#EDE4C4" stroke-width="8" stroke-linecap="round"/>'
         f'<path d="M {AX - 1.5} {AY + 20} L {AX - 1.5} {BEAK_END - 20}" stroke="#FFFFFF" stroke-width="2" opacity="0.8"/></g>')
o.append('<g id="aquenio">' + achene(AX, BEAK_END - 4, ACH_L, ACH_W) + '</g>')
o.append('<g id="abiertof">' + front_o + '</g>')
o.append('<g id="cerradof">' + front_c + '</g>')
o.append(f'<circle cx="{AX}" cy="{AY}" r="7" fill="#F4EEDA" stroke="{INK}" stroke-width="3.5"/>')
o.append('</g>')

# ---- lluvia y gotitas pegadas (para la escena de humedad)
rain = []
rnd = random.Random(7)
for _ in range(26):
    x, y = rnd.uniform(40, 960), rnd.uniform(60, 600)
    if (abs(x - AX) < 150 and y < 470) or abs(x - AX) < 70:
        continue
    rain.append(f"M {x:.0f} {y:.0f} L {x - 10:.0f} {y + 44:.0f}")
o.append(f'<g id="rain"><path d="{" ".join(rain)}" stroke="#A9DDFF" stroke-width="4" stroke-linecap="round" opacity="0.7"/></g>')
def drop(x, y, r):
    return (f'<path d="M {x} {y - r * 1.5:.1f} C {x + r * 0.6:.1f} {y - r * 0.7:.1f}, {x + r} {y - r * 0.2:.1f}, {x + r} {y + r * 0.25:.1f} '
            f'A {r} {r} 0 0 1 {x - r} {y + r * 0.25:.1f} C {x - r} {y - r * 0.2:.1f}, {x - r * 0.6:.1f} {y - r * 0.7:.1f}, {x} {y - r * 1.5:.1f} Z" '
            f'fill="url(#drop)" stroke="{INK}" stroke-width="4"/>'
            f'<ellipse cx="{x - r * 0.35:.1f}" cy="{y - r * 0.1:.1f}" rx="{r * 0.22:.1f}" ry="{r * 0.35:.1f}" fill="#FFFFFF" opacity="0.9"/>')
# gotitas sobre los pelos del vilano cerrado (en puntos reales de los filamentos)
wd = []
for k in (3, 18, 31, 47, 64, 79, 92):
    z, p = closed_lines[k]
    x, y = p[2]
    wd.append(drop(round(x), round(y), 9))
o.append('<g id="wet">' + "".join(wd) + '</g>')
o.append('<g id="bigdrops">' + drop(170, 200, 20) + drop(840, 330, 17) + drop(250, 470, 14) + '</g>')

# ---- etiquetas
# punta derecha del vilano abierto (filamento más a la derecha)
rt = max((p[-1] for z, p in open_lines), key=lambda q: q[0])
lt_ = min((p[-1] for z, p in open_lines), key=lambda q: q[0])
labels = []
t, b1 = tag("lvilano", 830, 330, "VILANO", target=(rt[0] - 30, rt[1] + 4), anchor_from=(830, 302)); o.append(t); labels.append(b1)
t, b2 = tag("lpelos", 170, 330, "~100 PELOS", target=(lt_[0] + 40, lt_[1] + 6), anchor_from=(170, 302)); o.append(t); labels.append(b2)
t, b3 = tag("lpico", 760, 440, "PICO", target=(AX + 6, 420), anchor_from=(722, 440)); o.append(t); labels.append(b3)
t, b4 = tag("lsemilla", 270, 590, "SEMILLA", target=(AX - 16, 590), anchor_from=(330, 590)); o.append(t); labels.append(b4)
t, b5 = tag("lcerrado", 735, 150, "CERRADO", target=(560, 110), anchor_from=(660, 150), bg=CORAL, fg=INK); o.append(t); labels.append(b5)
# barra de escala (vilano real ≈ 14 mm de diámetro → ~36 px/mm)
o.append(f'<g id="escala"><path d="M 846 628 L 882 628" stroke="#FFFFFF" stroke-width="6" stroke-linecap="square"/>'
         f'<path d="M 846 620 L 846 636 M 882 620 L 882 636" stroke="#FFFFFF" stroke-width="4"/>'
         f'<text x="864" y="612" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="22" fill="#FFFFFF">1 MM</text></g>')
o.append('</svg>')
for i in range(len(labels)):
    for j in range(i + 1, len(labels)):
        if boxes_overlap(labels[i], labels[j]):
            print("SOLAPE", i, j, file=sys.stderr)
print("puntas", rt, lt_, file=sys.stderr)
open(sys.argv[1], "w").write("\n".join(o))

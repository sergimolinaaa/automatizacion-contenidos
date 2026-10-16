from hc import *

OUT = "vaso_full.svg"
W, H = 1080, 1920
o = [header(W, H, lg("wallC", [(0, "#EAF4FB"), (1, "#C9DDEC")]))]
o.append(f'<rect width="{W}" height="{H}" fill="url(#wallC)"/>')
# azulejos de cocina
o.append('<g stroke="#D7E6F1" stroke-width="4">' + "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="1300"/>' for x in range(90, W, 150))
         + "".join(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}"/>' for y in range(100, 1300, 150)) + "</g>")
o.append('<rect x="0" y="1300" width="1080" height="620" fill="url(#woodG2)"/>')
o.append(f'<path d="M 0 1300 L 1080 1300" stroke="{INK}" stroke-width="8"/>')
o.append('<path d="M 0 1312 L 1080 1312" stroke="#F3D3A6" stroke-width="5"/>')
o.append('<g fill="none" stroke="#7A4E2A" stroke-width="3" opacity="0.45">' + "".join(f'<path d="M 0 {y} C 300 {y-12}, 700 {y+14}, 1080 {y}"/>' for y in (1390, 1500, 1630, 1770)) + "</g>")

# ---------- vaso ----------
CX, TOP, BOT = 560, 700, 1290
RT, RB, EY = 215, 178, 34
SURF = 905


def rx(y):
    return RT + (RB - RT) * (y - TOP) / (BOT - TOP)


rs = rx(SURF)
eys = EY * rs / RT
o.append(f'<ellipse cx="{CX+16}" cy="{BOT+8}" rx="{RB+50}" ry="20" fill="#6B4A25" opacity="0.35"/>')
body = f"M {CX-RT} {TOP} L {CX-RB} {BOT} A {RB} {f(EY*RB/RT)} 0 0 0 {CX+RB} {BOT} L {CX+RT} {TOP}"
o.append(f'<path d="{body} A {RT} {EY} 0 0 0 {CX-RT} {TOP} Z" fill="url(#glassB)"/>')
o.append(f'<ellipse cx="{CX}" cy="{TOP}" rx="{RT}" ry="{EY}" fill="#EAF6FF" fill-opacity="0.55" stroke="{INK}" stroke-width="6"/>')
liq = (f"M {f(CX-rs)} {SURF} L {CX-RB+8} {BOT-6} A {RB-8} {f(EY*(RB-8)/RT)} 0 0 0 {CX+RB-8} {BOT-6} "
       f"L {f(CX+rs)} {SURF} A {f(rs)} {f(eys)} 0 0 1 {f(CX-rs)} {SURF} Z")
o.append(f'<path d="{liq}" fill="url(#sodaG)"/>')
o.append(f'<ellipse cx="{CX}" cy="{SURF}" rx="{f(rs-4)}" ry="{f(eys)}" fill="url(#sodaS)" stroke="{INK}" stroke-width="5"/>')
# burbujas del refresco
rnd = random.Random(5)
bub = "".join(f'<circle cx="{f(CX + rnd.uniform(-150, 150))}" cy="{f(rnd.uniform(1000, 1250))}" r="{f(rnd.uniform(4, 9))}" fill="#FFF3CF" stroke="#C9741B" stroke-width="2.5"/>' for _ in range(16))
o.append(g("burbujas", bub))

# ---------- cubitos ----------
CUBES = [(468, 891, 150, -12, 1), (642, 887, 136, 11, 2), (566, 851, 104, 30, 3)]


def rot(cx, cy, ang, x, y):
    a = math.radians(ang)
    return (cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a))


cubes_svg = cube(*CUBES[2][:4], seed=3, bubbles=3)
cubes_svg += g("cubo1", cube(*CUBES[0][:4], seed=1, bubbles=5))
cubes_svg += g("cubo2", cube(*CUBES[1][:4], seed=2, bubbles=4))
# grietas sobre las caras frontales
c1x, c1y, s1, a1, _ = CUBES[0]
h1 = s1 / 2
g1 = [rot(c1x, c1y, a1, x, y) for x, y in zig(-h1 * 0.2, -h1, h1 * 0.15, h1 * 0.55, n=5, amp=10, seed=4)]
g1b = [rot(c1x, c1y, a1, x, y) for x, y in zig(-h1 * 0.02, -h1 * 0.25, -h1 * 0.85, h1 * 0.2, n=3, amp=7, seed=8)]
c2x, c2y, s2, a2, _ = CUBES[1]
h2 = s2 / 2
g2 = [rot(c2x, c2y, a2, x, y) for x, y in zig(h2, -h2 * 0.5, -h2 * 0.35, h2 * 0.35, n=5, amp=9, seed=6)]
g2b = [rot(c2x, c2y, a2, x, y) for x, y in zig(h2 * 0.3, -h2 * 0.15, h2 * 0.5, h2, n=3, amp=6, seed=9)]
cubes_svg += crack(g1, 7, id_="grieta1") + crack(g1b, 5, id_="grieta1b")
cubes_svg += crack(g2, 7, id_="grieta2") + crack(g2b, 5, id_="grieta2b")
o.append(g("cubos", cubes_svg))
# tinte del refresco sobre la parte sumergida
o.append(f'<path d="M {f(CX-rs)} {SURF} L {CX-RB+8} {BOT-6} A {RB-8} {f(EY*(RB-8)/RT)} 0 0 0 {CX+RB-8} {BOT-6} L {f(CX+rs)} {SURF} '
         f'A {f(rs)} {f(eys)} 0 0 0 {f(CX-rs)} {SURF} Z" fill="#E98A22" opacity="0.42"/>')
o.append(f'<path d="M {f(CX-rs+10)} {SURF} A {f(rs-10)} {f(eys-3)} 0 0 0 {f(CX+rs-10)} {SURF}" fill="none" stroke="#FFF4D2" stroke-width="5" opacity="0.9"/>')
# frente del vaso
o.append(f'<path d="{body}" fill="none" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>')
o.append(f'<path d="M {CX-RT} {TOP} A {RT} {EY} 0 0 0 {CX+RT} {TOP}" fill="none" stroke="{INK}" stroke-width="8"/>')
o.append(f'<path d="M {CX-RT+34} {TOP+60} L {CX-RB+28} {BOT-60}" stroke="#FFFFFF" stroke-width="16" stroke-linecap="round" opacity="0.75"/>')
o.append(f'<path d="M {CX-RT+70} {TOP+80} L {CX-RB+58} {BOT-200}" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round" opacity="0.6"/>')
o.append(f'<path d="M {CX+RT-30} {TOP+70} L {CX+RB-26} {BOT-80}" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round" opacity="0.45"/>')
o.append(f'<path d="M {CX-RB+10} {BOT-22} A {RB-10} {f(EY*0.8)} 0 0 0 {CX+RB-10} {BOT-22}" fill="none" stroke="#FFFFFF" stroke-width="6" opacity="0.6"/>')

# ---------- chorro + botella ----------
MX, MY = 418, 655
tgt = (462, 815)
stream = f"M {MX} {MY+6} C {MX+40} {MY+40}, {tgt[0]-8} {tgt[1]-110}, {tgt[0]} {tgt[1]}"
o.append(g("chorro", f'<path d="{stream}" fill="none" stroke="{INK}" stroke-width="34" stroke-linecap="round"/>'
           f'<path d="{stream}" fill="none" stroke="#F5A52A" stroke-width="24" stroke-linecap="round"/>'
           f'<path d="{stream}" fill="none" stroke="#FFE3A0" stroke-width="7" stroke-linecap="round" transform="translate(-6 0)"/>'))
drops = ""
for dx, dy, r in ((-70, -40, 11), (-40, -78, 8), (48, -60, 10), (80, -24, 7), (-95, 4, 7), (24, -96, 6)):
    drops += f'<ellipse cx="{tgt[0]+dx}" cy="{tgt[1]+dy}" rx="{r}" ry="{f(r*1.25)}" fill="#F5A52A" stroke="{INK}" stroke-width="4"/>'
    drops += f'<circle cx="{f(tgt[0]+dx-r*0.3)}" cy="{f(tgt[1]+dy-r*0.4)}" r="{f(r*0.3)}" fill="#FFFFFF" opacity="0.8"/>'
o.append(g("gotas", drops))
# botella (local: boca en el origen, cuerpo hacia -x), girada para verter
bt = []
bt.append('<ellipse cx="-230" cy="70" rx="180" ry="18" fill="#0B0B14" opacity="0.0"/>')
neck = "M 0 -22 L -90 -22 Q -125 -22 -150 -56 L -340 -56 L -340 56 L -150 56 Q -125 22 -90 22 L 0 22 Z"
bt.append(f'<path d="{neck}" fill="url(#bottleG)" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>')
bt.append(f'<path d="M -325 -30 L -165 -30 M -125 -10 L -20 -10" stroke="#FFFFFF" stroke-width="9" stroke-linecap="round" opacity="0.75"/>')
bt.append(f'<rect x="-315" y="-56" width="140" height="112" fill="url(#labelG)" stroke="{INK}" stroke-width="6"/>')
bt.append(f'<circle cx="-245" cy="0" r="30" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/>')
bt.append(f'<path d="M -258 -10 Q -245 -28 -232 -10 Q -222 6 -245 18 Q -268 6 -258 -10 Z" fill="#5DB7EC" stroke="{INK}" stroke-width="3"/>')
bt.append(f'<rect x="-12" y="-27" width="18" height="54" rx="5" fill="#DDF0D8" stroke="{INK}" stroke-width="6"/>')
o.append(f'<g id="botella"><g transform="translate({MX} {MY}) rotate(25)">{"".join(bt)}</g></g>')

# ---------- onomatopeyas ----------
o.append(burst(205, 810, 130, "¡CRAC!", 36, rot=-10, id_="crac1"))
o.append(burst(890, 650, 115, "¡CRIC!", 34, rot=9, id_="crac2", col="#FFFFFF"))
o.append(burst(885, 1100, 112, "¡CRAC!", 30, rot=-6, id_="crac3"))

# ---------- escena +: oreja, ondas, flota, segundos ----------
o.append(waves(640, 865, 150, 3, -38, 30, gap=40, w=10, col="#FFFFFF", id_="ondasW"))
o.append(waves(640, 865, 150, 3, -38, 30, gap=40, w=5, col=INK, id_="ondas"))
EX, EY0 = 975, 840
ear = smooth([(EX + 70, EY0 - 120), (EX - 10, EY0 - 135), (EX - 60, EY0 - 80), (EX - 60, EY0 - 10), (EX - 35, EY0 + 50),
              (EX - 40, EY0 + 105), (EX + 5, EY0 + 135), (EX + 70, EY0 + 120)], closed=False)
o.append(g("oreja", f'<path d="{ear} L {EX+110} {EY0+120} L {EX+110} {EY0-120} Z" fill="url(#skinR)" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'
           f'<path d="{smooth([(EX+40,EY0-90),(EX-8,EY0-88),(EX-28,EY0-40),(EX-10,EY0+5),(EX+20,EY0+20)])}" fill="none" stroke="#C47552" stroke-width="10" stroke-linecap="round"/>'
           f'<path d="{smooth([(EX+5,EY0+40),(EX-5,EY0+75),(EX+25,EY0+95)])}" fill="none" stroke="#C47552" stroke-width="9" stroke-linecap="round"/>'
           f'<path d="M {EX-45} {EY0-60} Q {EX-50} {EY0-20} {EX-38} {EY0+20}" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round" opacity="0.6"/>'))
s, _ = label("lflota", 190, 1000, "FLOTA ARRIBA", target=(440, 895), src=(250, 1000), size=32); o.append(s)
# cronómetro
SX, SY, SR = 180, 1128, 58
crono = (f'<circle cx="{SX+6}" cy="{SY+8}" r="{SR}" fill="{INK}" opacity="0.2"/>'
         f'<rect x="{SX-14}" y="{SY-SR-26}" width="28" height="22" rx="5" fill="url(#metalG)" stroke="{INK}" stroke-width="5"/>'
         f'<circle cx="{SX}" cy="{SY}" r="{SR}" fill="url(#metalG)" stroke="{INK}" stroke-width="7"/>'
         f'<circle cx="{SX}" cy="{SY}" r="{SR-14}" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/>'
         + "".join(f'<path d="M {f(SX+(SR-20)*math.cos(math.radians(a)))} {f(SY+(SR-20)*math.sin(math.radians(a)))} L {f(SX+(SR-27)*math.cos(math.radians(a)))} {f(SY+(SR-27)*math.sin(math.radians(a)))}" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>' for a in range(0, 360, 30))
         + f'<circle cx="{SX}" cy="{SY}" r="6" fill="{CORAL}"/>')
o.append(g("crono", crono))
o.append(g("aguja", f'<path d="M {SX} {SY} L {SX} {SY-36}" stroke="{CORAL}" stroke-width="7" stroke-linecap="round"/>'))
s, _ = label("lseg", 180, 1222, "SEGUNDOS", bg=LIME, fg=INK, size=32); o.append(s)
o.append("</svg>")
save(OUT, "\n".join(o))

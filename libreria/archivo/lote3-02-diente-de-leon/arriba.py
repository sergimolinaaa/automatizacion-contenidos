import sys, math, random
sys.path.insert(0, sys.path[0])
from seeds import *

CX, CY, R0, R = 500, 358, 20, 282
N = 100
defs = "\n".join([
    rg("bg", [(0, "#3F86A8"), (0.6, "#24597A"), (1, "#122F47")], 0.5, 0.5, 0.75),
    rg("disk", [(0, "#FFFFFF", 0.10), (1, "#FFFFFF", 0.02)]),
    rg("hub", [(0, "#FFF8E6"), (1, "#D9CBA0")], 0.4, 0.35, 0.7),
])
o = [header(defs)]
o.append('<rect width="1000" height="700" fill="url(#bg)"/>')
# cuadrícula milimetrada (40 px = 1 mm), tenue
g = []
for x in range(20, 1000, 40):
    g.append(f"M {x} 0 L {x} 700")
for y in range(38, 700, 40):
    g.append(f"M 0 {y} L 1000 {y}")
o.append(f'<path d="{" ".join(g)}" stroke="#FFFFFF" stroke-width="1" opacity="0.08"/>')
# disco imaginario que ocupa el vilano
o.append(f'<circle cx="{CX}" cy="{CY}" r="{R + 6}" fill="url(#disk)"/>')
o.append(f'<g id="disco"><circle cx="{CX}" cy="{CY}" r="{R + 6}" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-dasharray="12 10" opacity="0.6"/></g>')

rnd = random.Random(4)
angs = sorted((2 * math.pi * (k + rnd.uniform(-0.28, 0.28)) / N) for k in range(N))
lines = []
for a in angs:
    L = R * rnd.uniform(0.93, 1.02)
    bend = rnd.uniform(-0.04, 0.04)
    p = []
    for s in (0, 0.33, 0.66, 1):
        aa = a + bend * s * s
        r = R0 + (L - R0) * s
        p.append((CX + math.cos(aa) * r, CY + math.sin(aa) * r))
    lines.append((1, p))

# hueco resaltado entre dos pelos (arriba a la derecha)
k = min(range(N), key=lambda i: abs(angs[i] - math.radians(330 - 360 + 360) % (2 * math.pi)))
a1, a2 = angs[k], angs[(k + 1) % N]
sector = []
for t in range(0, 11):
    sector.append((CX + math.cos(a1 + (a2 - a1) * t / 10) * 268, CY + math.sin(a1 + (a2 - a1) * t / 10) * 268))
for t in range(10, -1, -1):
    sector.append((CX + math.cos(a1 + (a2 - a1) * t / 10) * 70, CY + math.sin(a1 + (a2 - a1) * t / 10) * 70))
o.append(f'<g id="airefill"><circle cx="{CX}" cy="{CY}" r="{R + 4}" fill="{LIME}" fill-opacity="0.32"/></g>')
o.append(f'<g id="hueco"><path d="{poly(sector, True)}" fill="{LIME}" fill-opacity="0.75" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/></g>')

_, front = fil_svg(lines, w=2.8, edge=5.6, barbs=9, edgecol="#22384C")
o.append('<g id="pelos">' + front + '</g>')
# pico visto desde arriba (en el centro)
o.append(f'<circle cx="{CX}" cy="{CY}" r="{R0 + 2}" fill="url(#hub)" stroke="{INK}" stroke-width="5"/>'
         f'<circle cx="{CX - 6}" cy="{CY - 6}" r="5" fill="#FFFFFF" opacity="0.8"/>')

# motas de aire que pasan entre los pelos
motas = []
for _ in range(16):
    a = rnd.uniform(0, 2 * math.pi); r = rnd.uniform(60, 300)
    motas.append(f'<circle cx="{CX + math.cos(a) * r:.0f}" cy="{CY + math.sin(a) * r:.0f}" r="{rnd.uniform(3, 6):.1f}" fill="#BFF3FF" opacity="0.7"/>')
o.append('<g id="motas">' + "".join(motas) + '</g>')

am = (a1 + a2) / 2
tgt = (CX + math.cos(am) * 215, CY + math.sin(am) * 215)
t, b1 = tag("laire", 800, 112, "92% AIRE", target=tgt, anchor_from=(780, 140)); o.append(t)
pk = min(range(N), key=lambda i: abs(angs[i] - math.radians(140)))
pa = angs[pk]
tgt2 = (CX + math.cos(pa) * 230, CY + math.sin(pa) * 230)
t, b2 = tag("lpelo", 120, 520, "PELO", target=tgt2, anchor_from=(150, 492)); o.append(t)
o.append(f'<g id="escala"><path d="M 870 628 L 910 628" stroke="#FFFFFF" stroke-width="6"/>'
         f'<path d="M 870 620 L 870 636 M 910 620 L 910 636" stroke="#FFFFFF" stroke-width="4"/>'
         f'<text x="890" y="612" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="22" fill="#FFFFFF">1 MM</text></g>')
o.append('</svg>')
print("hueco", a1, a2, tgt, file=sys.stderr)
open(sys.argv[1], "w").write("\n".join(o))

"""Corte: las burbujas suben en forma de hongo (anillo de vórtice) y la espuma rebosa (layout free)."""
import math, random, sys
sys.path.insert(0, ".")
from lib import *

VH = 860
CX, BASE, H, W = 500, 836, 720, 300
o = [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 {VH}">
<defs>
{BOTTLE_DEFS}
{CUT_DEFS}
</defs>''']
LEVEL = BASE - H + 0.13 * H
back, front, out, inn = cut_bottle(CX, BASE, H, W, LEVEL, t=18, uid="hg")
o.append(f'<ellipse cx="{CX + 20}" cy="{BASE + 6}" rx="{W * 0.62:.0f}" ry="14" fill="#0B0B14" opacity="0.25"/>')
o.append(back)
o.append(f'<g clip-path="url(#hgin)">')
# tallo: columna de burbujas que se ensancha hacia arriba
random.seed(7)
stem = []
y = BASE - 30
while y > 560:
    t = (BASE - 30 - y) / (BASE - 30 - 560)
    hw = 22 + 40 * t
    for _ in range(3):
        stem.append((CX + random.uniform(-hw, hw), y + random.uniform(-6, 6), random.uniform(5, 9 + 6 * t)))
    y -= 16
o.append('<g id="stem">' + "".join(bubble(x, yy, r) for x, yy, r in stem) + '</g>')
# sombrero del hongo: nube densa con forma de cúpula
cap = []
random.seed(8)
CY = 520
while len(cap) < 130:
    x = random.uniform(-108, 108)
    yy = random.uniform(-90, 40)
    # cúpula: media elipse arriba, borde inferior que se enrolla hacia dentro
    top_ok = yy <= 0 and (x / 108) ** 2 + (yy / 90) ** 2 <= 1
    rim_ok = 0 < yy <= 40 and 55 < abs(x) < 108 - yy * 0.4
    if top_ok or rim_ok:
        cap.append((CX + x, CY + yy, random.uniform(7, 14)))
o.append('<g id="capm">' + "".join(bubble(x, yy, r) for x, yy, r in sorted(cap, key=lambda c: c[1])) + '</g>')
# burbujas sueltas que suben
o.append('<g id="loose">' + "".join(bubble(CX + dx, yy, r) for dx, yy, r in ((-90, 640, 6), (80, 700, 5), (-60, 760, 4), (100, 600, 6), (40, 430, 7), (-30, 400, 6))) + '</g>')
o.append('</g>')
# anillos de vórtice: flechas curvas a ambos lados del sombrero
def curl(id_, cx, cy, sg):
    pts = [(cx + 34 * math.cos(a) * sg, cy + 30 * math.sin(a)) for a in [math.radians(d) for d in range(200, 470, 15)]]
    return f'<g id="{id_}">' + arrow(id_ + "a", pts, LIME, 7, 20) + '</g>'
o.append(curl("vl", CX - 80, CY + 70, -1) + curl("vr", CX + 80, CY + 70, 1))
o.append(front)
# espuma en el cuello y rebosando
foam_pts = []
for yy in range(int(LEVEL + 10), int(out.top - 70), -14):
    hw = (out.nw - 14) if yy > out.top else (out.nw - 14) + (out.top - yy) * 0.9
    for k in range(2):
        foam_pts.append((CX + random.uniform(-hw, hw), yy))
o.append('<g id="foamtop">' + foam_blob(foam_pts, 16, seed=3) + '</g>')
drip = P([(CX + out.halfwidth(yy) + 10 + (4 if yy < out.yl else 0), yy) for yy in range(int(out.top + 8), int(out.ys + 60), 6)])
o.append(f'<g id="overflow"><path d="{drip}" fill="none" stroke="{INK}" stroke-width="26" stroke-linecap="round"/><path d="{drip}" fill="none" stroke="#FFF6E0" stroke-width="15" stroke-linecap="round"/></g>')
o.append(tag("lhongo", 180, 380, "HONGO", CX - 80, CY - 60))
o.append(tag("lvortex", 840, 640, "REMOLINO", CX + 80 + 34, CY + 70))
o.append(tag("lespuma", 820, 160, "ESPUMA", CX + 40, out.top - 40))
o.append('</svg>')
print("\n".join(o))

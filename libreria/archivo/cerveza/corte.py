"""Corte de la botella golpeada: la onda de presión recorre el líquido y encuentra las burbujitas (layout free, sin fondo)."""
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
back, front, out, inn = cut_bottle(CX, BASE, H, W, LEVEL, t=18, uid="cb")
o.append(f'<ellipse cx="{CX + 20}" cy="{BASE + 6}" rx="{W * 0.62:.0f}" ry="14" fill="#0B0B14" opacity="0.25"/>')
o.append('<g id="botb">' + back)

# burbujitas preexistentes (pegadas a las paredes y sueltas)
random.seed(3)
bubs = []
for k in range(34):
    y = random.uniform(out.ys + 10, BASE - 40)
    hw = inn.halfwidth(y) - 14
    side = random.choice((-1, 1))
    x = CX + (side * random.uniform(hw * 0.75, hw) if k < 18 else random.uniform(-hw * 0.8, hw * 0.8))
    bubs.append((x, y, random.uniform(3.5, 8.5)))
o.append('<g id="bubbles">' + "".join(bubble(x, y, r) for x, y, r in bubs) + '</g>')
BX, BY, _ = min(bubs, key=lambda b: (b[0] - 620) ** 2 + (b[1] - 575) ** 2)

# frentes de onda (bajan por el líquido)
def wave(y, k):
    hw = inn.halfwidth(y) - 18
    d = f"M {CX - hw:.1f} {y:.1f} Q {CX} {y + 34:.1f} {CX + hw:.1f} {y:.1f}"
    return (f'<g id="w{k}"><path d="{d}" fill="none" stroke="{INK}" stroke-width="16" stroke-linecap="round" opacity="0.85"/>'
            f'<path d="{d}" fill="none" stroke="{LIME}" stroke-width="9" stroke-linecap="round"/>'
            f'<path d="M {CX - hw * 0.5:.1f} {y + 34:.1f} Q {CX} {y + 56:.1f} {CX + hw * 0.5:.1f} {y + 34:.1f}" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity="0.8"/></g>')
for k, y in enumerate((out.ys + 40, 640, 760), 1):
    o.append(wave(y, k))
o.append(front + '</g>')

lip_x, lip_y = CX, out.top
ix, iy = lip_x, lip_y - 6
star = []
for i in range(16):
    a = i / 16 * 2 * math.pi
    r = 40 if i % 2 == 0 else 17
    star.append((ix + r * math.cos(a), iy + r * math.sin(a)))
o.append(f'<g id="impact"><path d="{P(star)} Z" fill="{LIME}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/></g>')
o.append(''.join(f'<g id="ring{k}"><circle cx="{ix}" cy="{iy}" r="46" fill="none" stroke="#FFFFFF" stroke-width="6"/></g>' for k in (1, 2)))
# flechas de la onda hacia abajo (fuera de la botella)
o.append(arrow("down", [(CX - out.w - 60, 530), (CX - out.w - 60, 790)], LIME, 10, 30))
o.append(arrow("golpe", [(CX, -10), (CX, lip_y - 50)], CORAL, 14, 36))
o.append(tag("londa", 185, 470, "ONDA DE PRESIÓN", CX - inn.halfwidth(out.ys + 40) + 30, out.ys + 44, size=26))
o.append(tag("lbub", 840, 640, "BURBUJITAS", BX, BY, size=26))
o.append('</svg>')
print("\n".join(o))

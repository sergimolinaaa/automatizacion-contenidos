"""Al microscopio: la burbuja madre se estira y se aplasta, colapsa y se rompe en miles de burbujas hijas que se hinchan de CO2."""
import math, random, sys
sys.path.insert(0, ".")
from lib import *

C = (500, 380)
o = [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 700">
<defs>
{CUT_DEFS}
<radialGradient id="liq" cx="0.5" cy="0.45" r="0.75"><stop offset="0" stop-color="#FBCB5C"/><stop offset="0.7" stop-color="#E8A02A"/><stop offset="1" stop-color="#B86A0C"/></radialGradient>
<radialGradient id="big" cx="0.36" cy="0.3" r="0.8"><stop offset="0" stop-color="#FFFFFF"/><stop offset="0.55" stop-color="#FFF4D8" stop-opacity="0.9"/><stop offset="1" stop-color="#F0C070" stop-opacity="0.9"/></radialGradient>
</defs>
<rect width="1000" height="700" fill="url(#liq)"/>''']
o.append('<g fill="none" stroke="#FFE7A8" stroke-width="2" opacity="0.6"><circle cx="500" cy="350" r="300"/><circle cx="500" cy="350" r="430"/><line x1="500" y1="0" x2="500" y2="700"/><line x1="0" y1="350" x2="1000" y2="350"/></g>')
# motas de fondo (desenfocadas, sin contorno)
random.seed(2)
o.append('<g fill="#FFF0C0" opacity="0.35">' + "".join(f'<circle cx="{random.uniform(0, 1000):.0f}" cy="{random.uniform(0, 700):.0f}" r="{random.uniform(3, 9):.1f}"/>' for _ in range(40)) + '</g>')

# moléculas de CO2 disueltas (O=C=O)
def co2(x, y, a):
    dx, dy = 15 * math.cos(math.radians(a)), 15 * math.sin(math.radians(a))
    return (f'<g><line x1="{x - dx:.1f}" y1="{y - dy:.1f}" x2="{x + dx:.1f}" y2="{y + dy:.1f}" stroke="{INK}" stroke-width="4"/>'
            f'<circle cx="{x - dx:.1f}" cy="{y - dy:.1f}" r="8" fill="#FF5A36" stroke="{INK}" stroke-width="3"/>'
            f'<circle cx="{x + dx:.1f}" cy="{y + dy:.1f}" r="8" fill="#FF5A36" stroke="{INK}" stroke-width="3"/>'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9" fill="#3A3A44" stroke="{INK}" stroke-width="3"/>'
            f'<circle cx="{x - 2:.1f}" cy="{y - 3:.1f}" r="2.5" fill="#FFFFFF"/></g>')
random.seed(9)
mols = []
for k in range(26):
    while True:
        x, y = random.uniform(70, 930), random.uniform(80, 640)
        if math.hypot(x - C[0], y - C[1]) > 250 and not (x < 340 and y < 90):
            break
    mols.append((x, y))
o.append('<g id="co2">' + "".join(co2(x, y, random.uniform(0, 180)) for x, y in mols) + '</g>')
# flechitas del CO2 hacia la nube de burbujas
arr = []
for x, y in mols[:10]:
    dx, dy = C[0] - x, C[1] - y
    L = math.hypot(dx, dy)
    sx, sy = x + dx / L * 26, y + dy / L * 26
    ex, ey = x + dx / L * 70, y + dy / L * 70
    arr.append(f'M {sx:.1f} {sy:.1f} L {ex:.1f} {ey:.1f}')
o.append(f'<g id="co2arr"><path d="{" ".join(arr)}" stroke="{INK}" stroke-width="10" stroke-linecap="round"/><path d="{" ".join(arr)}" stroke="{LIME}" stroke-width="5" stroke-linecap="round"/></g>')

# burbuja madre
R = 150
o.append(f'<g id="madre"><circle cx="{C[0]}" cy="{C[1]}" r="{R}" fill="url(#big)" stroke="{INK}" stroke-width="8"/>'
         f'<ellipse cx="{C[0] - 55}" cy="{C[1] - 62}" rx="42" ry="24" fill="#FFFFFF" transform="rotate(-35 {C[0] - 55} {C[1] - 62})"/>'
         f'<circle cx="{C[0] + 70}" cy="{C[1] + 60}" r="10" fill="#FFFFFF" opacity="0.8"/>'
         f'<path d="M {C[0] + 40} {C[1] + 120} A {R - 20} {R - 20} 0 0 0 {C[0] + 122} {C[1] + 40}" fill="none" stroke="#E0A040" stroke-width="6" stroke-linecap="round" opacity="0.7"/></g>')
# flechas: estira (hacia fuera) y aplasta (hacia dentro)
def radial_arrows(id_, r0, r1, col):
    s = f'<g id="{id_}">'
    for a in (0, 90, 180, 270):
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        s += arrow(f"{id_}{a}", [(C[0] + r0 * ca, C[1] + r0 * sa), (C[0] + r1 * ca, C[1] + r1 * sa)], col, 10, 28)
    return s + '</g>'
o.append(radial_arrows("estira", R + 24, R + 96, LIME))
o.append(radial_arrows("aplasta", R + 110, R + 34, CORAL))

# colapso
star = []
for i in range(24):
    a = i / 24 * 2 * math.pi
    r = 120 if i % 2 == 0 else 50
    star.append((C[0] + r * math.cos(a), C[1] + r * math.sin(a)))
o.append(f'<g id="burst"><path d="{P(star)} Z" fill="#FFFFFF" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
         + "".join(f'<line x1="{C[0] + 140 * math.cos(a):.1f}" y1="{C[1] + 140 * math.sin(a):.1f}" x2="{C[0] + 185 * math.cos(a):.1f}" y2="{C[1] + 185 * math.sin(a):.1f}" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
                   for a in (math.radians(d) for d in range(15, 360, 45))) + '</g>')

# nube de burbujas hijas (diminutas)
random.seed(4)
hijas = []
while len(hijas) < 120:
    a = random.uniform(0, 2 * math.pi)
    r = 210 * math.sqrt(random.random())
    x, y = C[0] + r * math.cos(a) * 1.15, C[1] + r * math.sin(a) * 0.95
    if all((x - hx) ** 2 + (y - hy) ** 2 > 260 for hx, hy, _ in hijas):
        hijas.append((x, y, random.uniform(4.5, 8)))
o.append('<g id="hijas">' + "".join(bubble(x, y, r) for x, y, r in hijas) + '</g>')
# las mismas, ya hinchadas de gas
random.seed(5)
grandes = []
for x, y, r in hijas:
    if all((x - gx) ** 2 + (y - gy) ** 2 > (gr + 16) ** 2 for gx, gy, gr in grandes):
        grandes.append((x, y, r * random.uniform(2.2, 3.0)))
o.append('<g id="grandes">' + "".join(bubble(x, y, r) for x, y, r in grandes) + '</g>')

o.append(tag("lmadre", 820, 110, "BURBUJA", C[0] + 105, C[1] - 105))
o.append(tag("lcav", 500, 640, "CAVITACIÓN", C[0], C[1] + 120, bg=CORAL, fg=INK))
o.append(tag("lhijas", 820, 110, "MILES DE HIJAS", C[0] + 170, C[1] - 90))
mx, my = min(mols, key=lambda m: (m[0] - 160) ** 2 + (m[1] - 470) ** 2)
o.append(tag("lco2", mx, my - 80, "CO₂", mx, my - 14))
o.append('</svg>')
print("\n".join(o))

"""Lago Nyos (Camerún) en corte: el CO2 disuelto en el fondo sale de golpe y baja por el valle."""
import math, random, sys
sys.path.insert(0, ".")
from lib import *

o = [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 700">
<defs>
{CUT_DEFS}
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#BFE3FF"/><stop offset="1" stop-color="#FFF1DA"/></linearGradient>
<linearGradient id="lake" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7FC8F2"/><stop offset="0.45" stop-color="#3C86C8"/><stop offset="1" stop-color="#1D4E86"/></linearGradient>
<linearGradient id="rock" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8C6A52"/><stop offset="1" stop-color="#5A4232"/></linearGradient>
<linearGradient id="grass" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7BD07B"/><stop offset="1" stop-color="#36A86A"/></linearGradient>
<linearGradient id="gas" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0.92"/><stop offset="1" stop-color="#D8DCE6" stop-opacity="0.85"/></linearGradient>
</defs>
<rect width="1000" height="700" fill="url(#sky)"/>''']
# montañas lejanas
o.append('<path d="M 0 250 L 120 170 L 210 230 L 330 140 L 450 220 L 560 160 L 690 230 L 800 150 L 1000 240 L 1000 330 L 0 330 Z" fill="#B7D8C4"/>')
o.append('<path d="M 0 300 C 150 270, 260 290, 380 280 C 520 268, 700 300, 1000 280 L 1000 360 L 0 360 Z" fill="#9FCFAE"/>')
# terreno en corte: cráter con lago y valle a la derecha
ground = [(-10, 330), (90, 300), (170, 250), (230, 262), (260, 330), (300, 420), (380, 520), (500, 560), (620, 520), (690, 420), (720, 330), (750, 262), (800, 280), (860, 360), (930, 430), (1010, 470), (1010, 710), (-10, 710)]
gd = "M " + " L ".join(f"{x} {y}" for x, y in ground) + " Z"
o.append(f'<path d="{gd}" fill="url(#rock)"/>')
o.append(grains(ground, 260, ["#7A5A44", "#A08068", "#6A4C38"], 3, 8, seed=3, op=0.8))
# lago
W0 = 330
lake = [(260, W0), (300, 420), (380, 520), (500, 560), (620, 520), (690, 420), (720, W0)]
o.append(f'<path d="M {lake[0][0]} {lake[0][1]} ' + " ".join(f"L {x} {y}" for x, y in lake[1:]) + ' Z" fill="url(#lake)"/>')
# capa profunda cargada de CO2
o.append('<path d="M 352 480 Q 500 470 648 480 L 620 520 L 500 560 L 380 520 Z" fill="#163C6A" opacity="0.7"/>')
random.seed(5)
o.append('<g fill="#9FD0FF" opacity="0.6">' + "".join(f'<circle cx="{random.uniform(400, 600):.0f}" cy="{random.uniform(490, 540):.0f}" r="{random.uniform(2, 4):.1f}"/>' for _ in range(30)) + '</g>')
o.append(f'<line x1="260" y1="{W0}" x2="720" y2="{W0}" stroke="#FFFFFF" stroke-width="4" opacity="0.8"/>')
# hierba en el borde y contorno del terreno
o.append(f'<path d="M -10 330 L 90 300 L 170 250 L 230 262 L 260 330" fill="none" stroke="#36A86A" stroke-width="14" stroke-linejoin="round"/>')
o.append(f'<path d="M 720 330 L 750 262 L 800 280 L 860 360 L 930 430 L 1010 470" fill="none" stroke="#36A86A" stroke-width="14" stroke-linejoin="round"/>')
o.append(f'<path d="{gd}" fill="none" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
o.append(f'<path d="M 260 {W0} L 720 {W0}" stroke="{INK}" stroke-width="6"/>')
# chozas en el valle
for x, y in ((880, 392), (948, 425)):
    o.append(f'<g><rect x="{x - 18}" y="{y - 20}" width="36" height="26" fill="#E8C690" stroke="{INK}" stroke-width="4"/><path d="M {x - 26} {y - 18} L {x} {y - 42} L {x + 26} {y - 18} Z" fill="#B5793A" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/></g>')
# columna de burbujas subiendo desde el fondo
random.seed(9)
plume = [(500 + random.uniform(-30 - (560 - y) * 0.25, 30 + (560 - y) * 0.25), y, random.uniform(4, 10)) for y in range(540, 340, -9) for _ in range(2)]
o.append('<g id="plume">' + "".join(bubble(x, y, r) for x, y, r in plume) + '</g>')
# nube de CO2: sale del lago, rebosa el borde y baja por el valle
cloud = "M 380 330 C 380 250, 470 200, 540 230 C 600 190, 700 220, 720 270 C 750 200, 830 210, 870 270 C 920 300, 960 320, 1010 330 L 1010 470 L 930 430 L 860 360 L 800 280 L 750 262 L 720 330 Z"
o.append(f'<g id="cloud"><path d="{cloud}" fill="url(#gas)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
         '<path d="M 450 260 C 480 240, 520 238, 545 250" fill="none" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round"/></g>')
o.append(arrow("flow", [(800, 260), (870, 310), (935, 370)], CORAL, 10, 28))
o.append(tag("lnyos", 170, 470, "LAGO NYOS", 330, 420))
o.append(tag("lco2", 600, 110, "CO₂", 590, 228))
o.append(tag("lyear", 880, 560, "1986", bg="#FFFFFF", fg=INK))
o.append('</svg>')
print("\n".join(o))

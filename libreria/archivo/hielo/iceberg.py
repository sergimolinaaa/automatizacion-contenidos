import math, random, sys
sys.path.insert(0, "/tmp/claude-0/-home-user-automatizacion-contenidos/039df981-7a17-5355-b711-18510fb209db/scratchpad/dedos")
from common import *

random.seed(9)
WL = 250
# contorno del iceberg (sentido horario). La parte de arriba se escala para que sea ~10 % del area.
above = [(452, WL), (470, 196), (500, 168), (520, 128), (548, 112), (566, 138), (590, 150), (612, 190), (632, 214), (650, WL)]
below = [(650, WL), (720, 300), (790, 350), (820, 420), (800, 500), (760, 560), (680, 610), (560, 632), (430, 620), (320, 580),
         (250, 520), (220, 440), (240, 360), (310, 300), (390, 270), (452, WL)]


def area(pts):
    a = 0
    for (x1, y1), (x2, y2) in zip(pts, pts[1:] + pts[:1]):
        a += x1 * y2 - x2 * y1
    return abs(a) / 2


def scale_above(k):
    return [(x, WL - (WL - y) * k) for x, y in above]


Ab = area(below)
k = 1.0
for _ in range(60):
    Aa = area(scale_above(k))
    frac = Aa / (Aa + Ab)
    k *= (0.10 / frac) ** 0.5
up = scale_above(k)
Aa = area(up)
print(f"<!-- encima: {Aa / (Aa + Ab) * 100:.1f} % k={k:.2f} -->", file=sys.stderr)
P = lambda pts: "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts) + " Z"

o = [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 700">
<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#BFE3FF"/><stop offset="1" stop-color="#EAF6FF"/></linearGradient>
<linearGradient id="sea" gradientUnits="userSpaceOnUse" x1="0" y1="{WL}" x2="0" y2="700"><stop offset="0" stop-color="#4FA3E3"/><stop offset="0.6" stop-color="#1F5FA8"/><stop offset="1" stop-color="#123E78"/></linearGradient>
<linearGradient id="top" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#CFEFFF"/></linearGradient>
<linearGradient id="under" gradientUnits="userSpaceOnUse" x1="0" y1="{WL}" x2="0" y2="640"><stop offset="0" stop-color="#B8ECFF"/><stop offset="1" stop-color="#5DB4DE"/></linearGradient>
<radialGradient id="sun" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#FFF6C8"/><stop offset="1" stop-color="#FFF6C8" stop-opacity="0"/></radialGradient>
</defs>
<rect width="1000" height="{WL}" fill="url(#sky)"/>
<circle cx="840" cy="110" r="90" fill="url(#sun)"/><circle cx="840" cy="110" r="34" fill="#FFF1A8"/>
<g fill="#FFFFFF" opacity="0.9"><ellipse cx="220" cy="120" rx="60" ry="16"/><ellipse cx="260" cy="108" rx="40" ry="14"/><ellipse cx="700" cy="70" rx="46" ry="12"/></g>
<g fill="#DCEFFA"><path d="M 60 {WL} L 90 222 L 120 230 L 150 {WL} Z"/><path d="M 860 {WL} L 880 230 L 905 236 L 930 {WL} Z"/></g>
<rect y="{WL}" width="1000" height="{700 - WL}" fill="url(#sea)"/>
<g fill="#FFFFFF" opacity="0.12"><path d="M 100 {WL} L 170 {WL} L 90 700 L 0 700 Z"/><path d="M 880 {WL} L 940 {WL} L 1000 560 L 1000 700 L 960 700 Z"/></g>''']
# gaviotas
o.append(f'<g id="gulls" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round">'
         '<path d="M 370 96 Q 384 82 398 96 Q 412 82 426 96"/><path d="M 300 140 Q 310 130 320 140 Q 330 130 340 140"/></g>')
# parte sumergida
o.append('<g id="berg">')
o.append(f'<path d="{P(below)}" fill="url(#under)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
o.append(f'<g fill="#FFFFFF" opacity="0.25"><path d="M 470 {WL + 10} L 600 {WL + 10} L 520 420 L 420 400 Z"/><path d="M 260 440 L 330 330 L 400 360 L 330 520 Z"/></g>')
o.append(f'<g fill="#2F7FD6" opacity="0.22"><path d="M 650 {WL} L 790 350 L 820 420 L 700 470 Z"/><path d="M 430 620 L 560 632 L 600 520 L 470 500 Z"/></g>')
o.append(f'<g fill="none" stroke="#3E8CC4" stroke-width="4" stroke-linecap="round" opacity="0.6"><path d="M 520 420 L 600 520 L 700 470"/><path d="M 330 520 L 470 500"/></g>')
# punta
o.append(f'<path d="{P(up)}" fill="url(#top)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
pk = max(up, key=lambda p: -p[1])
i_pk = up.index(pk)
o.append(f'<path d="M {pk[0]:.1f} {pk[1]:.1f} L ' + " L ".join(f"{x:.1f} {y:.1f}" for x, y in up[i_pk + 1:]) + f' L {pk[0] + 30:.1f} {WL} Z" fill="#A9DDF6" opacity="0.7"/>')
o.append(f'<path d="M {up[1][0] + 6:.1f} {up[1][1] + 4:.1f} L {up[3][0]:.1f} {up[3][1] + 8:.1f}" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>')
o.append('</g>')
# linea de flotacion
o.append(f'<path d="M 0 {WL} L 1000 {WL}" stroke="{INK}" stroke-width="6"/>')
o.append(f'<path d="M 0 {WL + 8} L 1000 {WL + 8}" stroke="#FFFFFF" stroke-width="3" opacity="0.5"/>')
for k2 in (1, 2):
    o.append(f'<g id="rip{k2}"><ellipse cx="551" cy="{WL + 4}" rx="140" ry="12" fill="none" stroke="#FFFFFF" stroke-width="4"/></g>')
# peces
def fish(id_, x, y, s, col, flip=False):
    t = f'translate({x} {y}) scale({-s if flip else s} {s})'
    return (f'<g id="{id_}"><g transform="{t}">'
            f'<path d="M -40 0 C -20 -22, 20 -22, 34 0 C 20 22, -20 22, -40 0 Z" fill="{col}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
            f'<path d="M 30 0 L 54 -18 L 50 0 L 54 18 Z" fill="{col}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
            f'<circle cx="-22" cy="-4" r="5" fill="{INK}"/><circle cx="-23.5" cy="-5.5" r="1.8" fill="#FFFFFF"/>'
            f'<path d="M -6 -12 C 0 -4, 0 4, -6 12" fill="none" stroke="{INK}" stroke-width="3" opacity="0.6"/>'
            f'<path d="M -30 -8 C -16 -16, 6 -16, 20 -10" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.6"/></g></g>')
o.append(fish("fish1", 130, 430, 1.0, "#FF9F43"))
o.append(fish("fish2", 120, 518, 0.7, "#FFD23F"))
# burbujas
o.append('<g id="bubbles" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.8">' + "".join(f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x, y, r in [(170, 400, 6), (180, 372, 4), (176, 350, 3), (96, 490, 4)]) + '</g>')
# corchetes 10 % / 90 %
BX = 850
top_y = min(p[1] for p in up)
o.append(f'<g id="b10">{dbl(f"M {BX - 14} {top_y:.0f} L {BX} {top_y:.0f} L {BX} {WL - 6} L {BX - 14} {WL - 6}", 7, LIME, 7)}</g>')
o.append(f'<g id="b90">{dbl(f"M {BX - 14} {WL + 6} L {BX} {WL + 6} L {BX} 630 L {BX - 14} 630", 7, LIME, 7)}</g>')
o.append(tag("l10", 868, 134, "10 %", fs=28, w=110))
o.append(tag("l90", 868, 410, "90 %", fs=28, w=110))
o.append(tag("lbajo", 40, 560, "BAJO EL AGUA", lead=(268, 560, 300, 500), fs=26))
o.append('</svg>')
print("\n".join(o))

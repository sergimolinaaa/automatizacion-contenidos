"""Vista desde arriba: embudos en la arena, rastro en espiral y mandíbulas asomando en el fondo."""
import math, random, sys
sys.path.insert(0, ".")
from lib import *
from lib import _mandible

C = (500, 380)
RP = 235
o = [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 700">
<defs>
{ANT_DEFS}
{LARVA_DEFS}
<linearGradient id="sand" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F6E4BA"/><stop offset="1" stop-color="#E4C48C"/></linearGradient>
</defs>
<rect width="1000" height="700" fill="url(#sand)"/>''']
o.append(grains([(0, 0), (1000, 0), (1000, 700), (0, 700)], 1100, ["#D9B77C", "#C99E5E", "#FFF6DE", "#B98F5A"], 1.6, 4, seed=2, avoid=[(C[0], C[1], RP + 6, RP + 6)]))

# rastros sinuosos (por eso en inglés las llaman "doodlebugs")
def trail(pts):
    d = "M " + " ".join(f"{x} {y}" for x, y in pts[:1]) + " " + " ".join(
        f"Q {pts[i][0]} {pts[i][1]} {(pts[i][0] + pts[i + 1][0]) / 2:.0f} {(pts[i][1] + pts[i + 1][1]) / 2:.0f}" for i in range(len(pts) - 1))
    return (f'<path d="{d}" fill="none" stroke="#B88E54" stroke-width="12" stroke-linecap="round" opacity="0.55"/>'
            f'<path d="{d}" fill="none" stroke="#FFF4D8" stroke-width="4" stroke-linecap="round" opacity="0.8" transform="translate(-3 -4)"/>')
o.append('<g id="trails">' + trail([(40, 640), (110, 600), (90, 540), (170, 520), (200, 580), (250, 560), (300, 520)]) +
         trail([(960, 650), (900, 600), (930, 560), (870, 540), (840, 590), (790, 600)]) + '</g>')

# embudo: anillos que se oscurecen hacia el fondo y se desplazan hacia la luz
N = 26
for k in range(N + 1):
    f = k / N
    r = RP * (1 - f) + 6
    cx, cy = C[0] + 16 * f, C[1] + 12 * f
    c0, c1 = (0xF5, 0xE2, 0xB4), (0x7A, 0x52, 0x2C)
    col = "#%02X%02X%02X" % tuple(int(a + (b - a) * f ** 1.6) for a, b in zip(c0, c1))
    o.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{col}"/>')
# sombra en la pared más alejada de la luz (arriba a la izquierda)
o.append(f'<path d="M {C[0] - RP} {C[1]} A {RP} {RP} 0 0 1 {C[0]} {C[1] - RP} A {RP * 1.05:.0f} {RP:.0f} 0 0 0 {C[0] - RP} {C[1]} Z" fill="#7A5530" opacity="0.28"/>')
o.append(f'<path d="M {C[0] - RP + 14} {C[1] + 30} A {RP - 10} {RP - 10} 0 0 1 {C[0] + 30} {C[1] - RP + 14}" fill="none" stroke="#7A5530" stroke-width="40" opacity="0.22" stroke-linecap="round"/>')
o.append(grains([(C[0] + RP * math.cos(a) * 0.95, C[1] + RP * math.sin(a) * 0.95) for a in [i / 24 * 2 * math.pi for i in range(24)]],
                330, ["#C49A5C", "#E8CD98", "#A57A46", "#FFF2D0"], 1.4, 3.4, seed=4, avoid=[(C[0] + 16, C[1] + 12, 40, 40)], op=0.85))
# borde
o.append(f'<circle cx="{C[0]}" cy="{C[1]}" r="{RP}" fill="none" stroke="{INK}" stroke-width="7"/>')
o.append(f'<path d="M {C[0] + RP * 0.2:.0f} {C[1] + RP * 0.97:.0f} A {RP - 9} {RP - 9} 0 0 0 {C[0] + RP * 0.97:.0f} {C[1] + RP * 0.2:.0f}" fill="none" stroke="#FFF6DE" stroke-width="5" opacity="0.8" stroke-linecap="round"/>')

# espiral de excavación (de fuera hacia dentro)
pts = []
turns = 2.6
for i in range(260):
    t = i / 259
    a = -math.pi / 2 + t * turns * 2 * math.pi
    r = (RP - 28) * (1 - t) + 26
    pts.append((C[0] + 16 * t + r * math.cos(a), C[1] + 12 * t + r * math.sin(a)))
d = P(pts)
o.append(f'<g id="spiral"><path d="{d}" fill="none" stroke="{INK}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>'
         f'<path d="{d}" fill="none" stroke="{LIME}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></g>')

# mandíbulas asomando en el fondo
BX, BY = C[0] + 16, C[1] + 30
o.append(f'<g id="jaws"><g transform="translate({BX} {BY}) scale(0.95)">{_mandible(-1, 0.9)}{_mandible(1, 0.9)}'
         f'<path d="M -26 -14 C -20 -24, 20 -24, 26 -14 C 20 0, -20 0, -26 -14 Z" fill="url(#lvah)" stroke="{INK}" stroke-width="5"/>'
         f'<circle cx="-24" cy="-10" r="6" fill="#6E5236" stroke="{INK}" stroke-width="3.5"/><circle cx="24" cy="-10" r="6" fill="#6E5236" stroke="{INK}" stroke-width="3.5"/></g>'
         + grains([(BX - 40, BY - 8), (BX + 40, BY - 14), (BX + 46, BY + 20), (BX - 40, BY + 24)], 40, ["#A57A46", "#C49A5C", "#8E6438"], 2, 4.5, seed=6) + '</g>')

o.append(f'<g id="ant"><g transform="translate(770 165) rotate(-130) scale(1.0)">{ant_top()}</g></g>')
# piedras y hojita
for x, y, rx, ry, c in ((140, 180, 34, 22, "#B5ADA2"), (880, 520, 26, 18, "#A9A39A"), (190, 420, 18, 12, "#C2B9AC"), (820, 330, 14, 10, "#B0A698")):
    o.append(f'<ellipse cx="{x + 6}" cy="{y + 8}" rx="{rx}" ry="{ry}" fill="#8E6438" opacity="0.35"/><ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{c}" stroke="{INK}" stroke-width="5"/><ellipse cx="{x - rx * 0.3:.0f}" cy="{y - ry * 0.35:.0f}" rx="{rx * 0.35:.0f}" ry="{ry * 0.25:.0f}" fill="#FFFFFF" opacity="0.6"/>')
o.append(f'<g id="leaf"><path d="M 760 600 C 800 560, 870 560, 900 590 C 870 625, 800 630, 760 600 Z" fill="#C9A24A" stroke="{INK}" stroke-width="5"/><path d="M 760 600 L 900 590 M 800 598 l 16 -18 M 840 595 l 16 -18 M 800 600 l 16 16 M 840 597 l 16 16" stroke="{INK}" stroke-width="3" opacity="0.6"/></g>')

o.append(tag("lembudo", 150, 300, "EMBUDO", C[0] - RP * 0.86, C[1] - RP * 0.3))
o.append(tag("lespiral", 860, 420, "ESPIRAL", C[0] + 150, C[1] + 70))
o.append(tag("llarva", 500, 652, "LARVA", BX, BY + 22))
o.append('</svg>')
print("\n".join(o))

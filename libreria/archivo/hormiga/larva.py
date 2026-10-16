"""Primer plano: la larva atrapa a la hormiga con sus mandíbulas-jeringa. Detalle del canal interior."""
import math, random, sys
sys.path.insert(0, ".")
from lib import *
from lib import _mandible, bez

AP = (430, 372)
K = 0.65
o = [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 700">
<defs>
{ANT_DEFS}
{LARVA_DEFS}
<linearGradient id="cut" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E9C98E"/><stop offset="0.6" stop-color="#CFA466"/><stop offset="1" stop-color="#A97C48"/></linearGradient>
<linearGradient id="wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F7E6C0"/><stop offset="1" stop-color="#DDB97E"/></linearGradient>
<radialGradient id="lens" cx="0.4" cy="0.35" r="0.8"><stop offset="0" stop-color="#FFFDF5"/><stop offset="1" stop-color="#EADCC0"/></radialGradient>
<linearGradient id="tube" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#C98A50"/><stop offset="0.5" stop-color="#8B4A22"/><stop offset="1" stop-color="#4A220E"/></linearGradient>
<radialGradient id="pocket" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#8A6436" stop-opacity="0.5"/><stop offset="1" stop-color="#8A6436" stop-opacity="0"/></radialGradient>
</defs>
<rect width="1000" height="700" fill="#F3DFB0"/>''']
HX, HY, ROT, SC = 476, 400, -90, 1.4
N = 30
for k in range(N + 1):
    f = k / N
    r = 760 * (1 - f) + 60
    c0, c1 = (0xF5, 0xE2, 0xB4), (0xA8, 0x7C, 0x48)
    col = "#%02X%02X%02X" % tuple(int(a + (b - a) * f ** 1.5) for a, b in zip(c0, c1))
    o.append(f'<circle cx="{HX + 40 * f:.1f}" cy="{HY + 30 * f:.1f}" r="{r:.1f}" fill="{col}"/>')
o.append(grains([(0, 0), (1000, 0), (1000, 700), (0, 700)], 900, ["#C99A5C", "#B5864A", "#E9CC95", "#FFF6DE", "#9C7040"], 2.2, 6, seed=13))
# hormiga (vista cenital) atravesada por las puntas de las mandíbulas
AX, AY, ASC = 292, 372, 1.55
o.append(f'<g id="ant"><g transform="translate({AX} {AY}) scale({ASC})">{ant_top()}</g></g>')
o.append(f'<g id="antdry"><g transform="translate({AX} {AY}) scale({ASC})">{ant_top(True)}</g></g>')
enz = [(AX + x * ASC, AY + y * ASC, r) for x, y, r in ((0, 44, 8), (-8, 56, 6), (8, 34, 5), (0, -2, 6), (3, 12, 4), (-4, -30, 5), (7, 62, 4))]
o.append('<g id="enz">' + "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#FF5A36" opacity="0.9" stroke="{INK}" stroke-width="2"/>' for x, y, r in enz) + '</g>')
EX, EY = AX, AY + 44 * ASC

# larva
o.append(f'<ellipse cx="{HX + 200}" cy="{HY + 14}" rx="230" ry="150" fill="url(#pocket)"/>')
o.append(f'<g id="larva"><g transform="translate({HX} {HY}) rotate({ROT}) scale({SC})">{larva(0.9)}</g></g>')

# punto del detalle: a media mandíbula derecha (coordenadas locales -> globales)
def glob(lx, ly):
    a = math.radians(ROT)
    return HX + SC * (lx * math.cos(a) - ly * math.sin(a)), HY + SC * (lx * math.sin(a) + ly * math.cos(a))
mx, my = glob(30, -64)
IC, IR = (800, 168), 120
# conos del aumento
dx, dy = IC[0] - mx, IC[1] - my
dl = math.hypot(dx, dy)
nx, ny = -dy / dl, dx / dl
o.append(f'<g id="inset">')
o.append(f'<path d="M {mx + nx * 12:.1f} {my + ny * 12:.1f} L {IC[0] + nx * IR:.1f} {IC[1] + ny * IR:.1f} L {IC[0] - nx * IR:.1f} {IC[1] - ny * IR:.1f} L {mx - nx * 12:.1f} {my - ny * 12:.1f} Z" fill="#FFFFFF" opacity="0.35"/>')
o.append(f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="16" fill="none" stroke="{INK}" stroke-width="5"/><circle cx="{mx:.1f}" cy="{my:.1f}" r="16" fill="none" stroke="#FFFFFF" stroke-width="2"/>')
o.append(f'<circle cx="{IC[0] + 8}" cy="{IC[1] + 10}" r="{IR}" fill="{INK}" opacity="0.25"/>')
o.append(f'<circle cx="{IC[0]}" cy="{IC[1]}" r="{IR}" fill="url(#lens)"/>')
o.append(f'<clipPath id="lensclip"><circle cx="{IC[0]}" cy="{IC[1]}" r="{IR - 3}"/></clipPath><g clip-path="url(#lensclip)">')
# mandíbula en detalle: hoz afilada con su canal interior
c0, c1, c2, c3 = (IC[0] - 170, IC[1] + 95), (IC[0] - 60, IC[1] + 40), (IC[0] + 30, IC[1] - 10), (IC[0] + 112, IC[1] - 88)
def side(sg, wmax, wmin=0):
    pts = []
    for i in range(41):
        t = i / 40
        x, y = bez(c0, c1, c2, c3, t)
        x2, y2 = bez(c0, c1, c2, c3, min(1, t + 0.01))
        x1, y1 = bez(c0, c1, c2, c3, max(0, t - 0.01))
        dx, dy = x2 - x1, y2 - y1
        l = math.hypot(dx, dy) or 1
        w = wmin + (wmax - wmin) * (1 - t) ** 0.8
        pts.append((x - dy / l * w * sg, y + dx / l * w * sg))
    return pts
up, dn = side(1, 52, 1), side(-1, 52, 1)
shape = P(up + dn[::-1]) + " Z"
o.append(f'<path d="{shape}" fill="url(#tube)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
hi = side(1, 36, 1)[3:30]
o.append(f'<path d="{P([(x + 4, y - 4) for x, y in hi])}" fill="none" stroke="#E0A070" stroke-width="5" stroke-linecap="round" opacity="0.8"/>')
cu, cd = side(1, 18, 3), side(-1, 18, 3)
chan = P(cu[:37] + cd[:37][::-1]) + " Z"
o.append(f'<path d="{chan}" fill="#FFF1DA" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')
mid = [bez(c0, c1, c2, c3, i / 40) for i in range(37)]
tube_d = P(mid)
o.append(f'<g id="flowin"><path d="{tube_d}" fill="none" stroke="{CORAL}" stroke-width="12" stroke-linecap="round" stroke-dasharray="0.08 0.05"/></g>')
o.append(f'<g id="flowout"><path d="{P(mid[::-1])}" fill="none" stroke="#E0A030" stroke-width="12" stroke-linecap="round" stroke-dasharray="0.08 0.05"/></g>')
# máscara del círculo: tapar lo que sobresale del tubo fuera de la lente
o.append(f'</g><circle cx="{IC[0]}" cy="{IC[1]}" r="{IR}" fill="none" stroke="{INK}" stroke-width="8"/>')
o.append(f'<path d="M {IC[0] - IR * 0.75:.0f} {IC[1] - IR * 0.45:.0f} A {IR * 0.88:.0f} {IR * 0.88:.0f} 0 0 1 {IC[0] - IR * 0.2:.0f} {IC[1] - IR * 0.86:.0f}" fill="none" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round" opacity="0.8"/>')
ring = f"M {IC[0] - IR - 120} {IC[1] - IR - 120} H {IC[0] + IR + 120} V {IC[1] + IR + 120} H {IC[0] - IR - 120} Z M {IC[0] + IR} {IC[1]} A {IR} {IR} 0 1 0 {IC[0] - IR} {IC[1]} A {IR} {IR} 0 1 0 {IC[0] + IR} {IC[1]} Z"
o.append('</g>')
o_inset_end = len(o)
o.append(tag("lx40", IC[0] + 92, IC[1] - IR + 4, "×40", bg="#FFFFFF", fg=INK, size=24))
o.append(tag("lhueca", 515, 225, "CANAL HUECO", IC[0] - 60, IC[1] + 34))
o.append(tag("lenz", 150, 600, "ENZIMAS", EX - 10, EY + 10))
o.append(tag("ljugo", 170, 600, "SE LA BEBE", EX - 10, EY + 10))
o.append('</svg>')
svg = "\n".join(o)
print(svg)

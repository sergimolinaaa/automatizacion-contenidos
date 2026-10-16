"""Fig. · El peso del agua de encima impide que el agua del fondo hierva: se sobrecalienta."""
import math, random
from lib import *

SG = 96                 # superficie
X0, X1 = 380, 560       # paredes de la columna de agua
YB = 600                # fondo
PX, PY = 470, 548       # «parcela» de agua del fondo
TX, TB, TT = 800, 566, 116   # termómetro: x, bulbo, tope
Y100, YHOT = 380, 226        # marca de 100 °C y temperatura final

defs = """
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#A9D8FF"/><stop offset="1" stop-color="#E6F3FF"/></linearGradient>
<linearGradient id="rock" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#C9B38C"/><stop offset="0.3" stop-color="#A49482"/><stop offset="1" stop-color="#7D6A5A"/></linearGradient>
<linearGradient id="hot" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8E5A44"/><stop offset="0.5" stop-color="#C2482E"/><stop offset="1" stop-color="#FF5A36"/></linearGradient>
<linearGradient id="water" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9FDBFF"/><stop offset="1" stop-color="#1F5FB0"/></linearGradient>
<radialGradient id="parcel" cx="0.4" cy="0.35" r="0.7"><stop offset="0" stop-color="#FFD1B8"/><stop offset="0.6" stop-color="#FF8A5C"/><stop offset="1" stop-color="#E5482A"/></radialGradient>
<radialGradient id="bub" cx="0.35" cy="0.3" r="0.8"><stop offset="0" stop-color="#FFFFFF"/><stop offset="0.6" stop-color="#E4F4FF"/><stop offset="1" stop-color="#A9D8FA"/></radialGradient>
<linearGradient id="glass" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#DCEBF5"/></linearGradient>
<linearGradient id="merc" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FF8A6B"/><stop offset="0.5" stop-color="#FF5A36"/><stop offset="1" stop-color="#C2321C"/></linearGradient>
"""
o = [svg_open(defs)]
o.append('<rect width="1000" height="700" fill="url(#sky)"/>')
o.append(f'<rect y="{SG}" width="1000" height="{700 - SG}" fill="url(#rock)"/>')
o.append(f'<path d="M 0 612 C 200 602, 400 626, 600 610 C 780 596, 900 618, 1000 606 L 1000 700 L 0 700 Z" fill="url(#hot)"/>')
random.seed(3)
o.append('<g fill="#6E5A48" opacity="0.35">' + "".join(f'<ellipse cx="{random.randint(20, 980)}" cy="{random.randint(SG + 30, 590)}" rx="{random.randint(4, 10)}" ry="{random.randint(3, 5)}"/>' for _ in range(46)) + '</g>')
o.append(f'<line x1="0" y1="{SG}" x2="1000" y2="{SG}" stroke="{INK}" stroke-width="6"/>')

# columna de agua (pozo del géiser, ensanchado para el esquema)
o.append(f'<rect x="{X0 - 12}" y="{SG}" width="{X1 - X0 + 24}" height="{YB - SG + 12}" rx="20" fill="#3E3228"/>')
o.append(f'<rect x="{X0}" y="{SG - 3}" width="{X1 - X0}" height="{YB - SG + 3}" rx="14" fill="url(#water)" stroke="{INK}" stroke-width="7"/>')
o.append(f'<path d="M {X0 + 18} {SG + 16} L {X0 + 18} {YB - 30}" stroke="#FFFFFF" stroke-width="5" opacity="0.5" stroke-linecap="round"/>')
# capas de agua (líneas finas) para que se lea «agua de encima»
o.append('<g stroke="#FFFFFF" stroke-width="2" opacity="0.35">' + "".join(f'<line x1="{X0 + 10}" y1="{y}" x2="{X1 - 10}" y2="{y}"/>' for y in range(150, 560, 50)) + '</g>')

# flechas de peso: más gordas cuanto más abajo
cx = (X0 + X1) / 2
for i, (y, w, ln) in enumerate([(130, 7, 50), (250, 10, 62), (370, 13, 74)]):
    o.append(arrow(f"press{i + 1}", cx, y, cx, y + ln, CORAL, w=w, head=18 + i * 6))
# parcela del fondo + burbuja aplastada
o.append(f'<g id="parcel"><circle cx="{PX}" cy="{PY}" r="34" fill="url(#parcel)" stroke="{INK}" stroke-width="6"/><circle cx="{PX - 10}" cy="{PY - 12}" r="7" fill="#FFFFFF" opacity="0.8"/></g>')
o.append(f'<g id="nobubble"><ellipse cx="{PX}" cy="{PY}" rx="13" ry="7" fill="url(#bub)" stroke="{INK}" stroke-width="3.5"/></g>')
sq = []
for a in (0, 90, 180, 270):
    r = math.radians(a)
    x1, y1 = PX + 78 * math.cos(r), PY + 78 * math.sin(r)
    x2, y2 = PX + 46 * math.cos(r), PY + 46 * math.sin(r)
    if a == 90:
        continue
    sq.append(arrow(None, x1, y1, x2, y2, CORAL, w=7, head=16, ink=8))
o.append('<g id="squeeze">' + "".join(sq) + '</g>')

# calor desde abajo
def inner(g):
    return g[g.index(">") + 1:-4]
heat = []
for x in (410, 470, 530):
    pts = [(x + 8 * math.sin((690 - y) / 14), y) for y in range(690, 621, -4)]
    heat.append(inner(curved_arrow("h", pts_d(pts), pts[-1], pts[-3], "#FFD34A", w=7, head=18)))
o.append('<g id="heat">' + "".join(heat) + '</g>')

# termómetro
o.append(f'<rect x="{TX - 26}" y="{TT - 12}" width="52" height="{TB - TT + 12}" rx="26" fill="url(#glass)" stroke="{INK}" stroke-width="7"/>')
o.append(f'<circle cx="{TX}" cy="{TB + 20}" r="44" fill="url(#merc)" stroke="{INK}" stroke-width="7"/>')
o.append(f'<rect x="{TX - 11}" y="{Y100}" width="22" height="{TB - Y100 + 10}" fill="url(#merc)"/>')
o.append(f'<g id="hotter"><rect x="{TX - 11}" y="{YHOT}" width="22" height="{Y100 - YHOT + 2}" fill="url(#merc)"/></g>')
o.append(f'<circle cx="{TX - 12}" cy="{TB + 8}" r="10" fill="#FFFFFF" opacity="0.7"/>')
o.append(f'<path d="M {TX - 14} {TT + 10} L {TX - 14} {TB - 30}" stroke="#FFFFFF" stroke-width="4" opacity="0.8" stroke-linecap="round"/>')
for k in range(0, 13):
    y = TB - 30 - k * (TB - 30 - TT - 10) / 12
    o.append(f'<line x1="{TX + 26}" y1="{f(y)}" x2="{TX + (44 if k % 3 == 0 else 36)}" y2="{f(y)}" stroke="{INK}" stroke-width="4"/>')
o.append(f'<g id="mark100"><path d="M {TX - 40} {Y100} L {TX + 50} {Y100}" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
         f'<rect x="{TX + 56}" y="{Y100 - 22}" width="96" height="44" rx="10" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/>'
         f'<text x="{TX + 104}" y="{Y100 + 9}" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="24" fill="{INK}">100 °C</text></g>')

L = [label("lpeso", 196, 200, "PESO DEL AGUA", bg=CORAL, fg=INK, line_to=(cx - 22, 160)),
     label("lnohierve", 220, 612, "NO HIERVE", line_to=(PX - 26, PY + 24)),
     label("lmas", 664, YHOT, "+100 °C", bg=CORAL, fg=INK, line_to=(TX - 14, YHOT + 4))]
for s_, b in L:
    o.append(s_)
o.append('</svg>')
open("presion.svg", "w").write("\n".join(o))
print([b for _, b in L])

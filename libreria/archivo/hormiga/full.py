"""Versión pantalla completa (1080x1920) del corte del embudo para el gancho."""
import re, sys
sys.path.insert(0, ".")
from lib import *
src = open("escena.svg").read()
defs = re.search(r"<defs>.*?</defs>", src, re.S).group(0)
inner = src[src.index("</defs>") + 7: src.rindex("</svg>")]
TY, SC, TX = 200, 1.5, -210
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920">', defs]
o.append(f'<rect width="1080" height="{TY + 10}" fill="#CFEAFF"/>')
# nubes suaves en el cielo alto
o.append('<g fill="#FFFFFF" opacity="0.75"><ellipse cx="220" cy="300" rx="120" ry="34"/><ellipse cx="300" cy="280" rx="80" ry="40"/><ellipse cx="820" cy="380" rx="140" ry="36"/><ellipse cx="760" cy="360" rx="70" ry="38"/></g>')
o.append(f'<rect y="{TY + 700 * SC - 20}" width="1080" height="{1920 - TY - 700 * SC + 20}" fill="#A97C48"/>')
poly = [(0, TY + 700 * SC - 10), (1080, TY + 700 * SC - 10), (1080, 1920), (0, 1920)]
o.append(grains(poly, 700, ["#C99A5C", "#B5864A", "#E9CC95", "#9C7040", "#8A6036"], 2, 6, seed=41))
for y0 in (1420, 1560, 1700, 1840):
    o.append(f'<path d="M 0 {y0} q 270 -14 540 0 t 540 0" fill="none" stroke="#8E6438" stroke-width="5" opacity="0.4"/>')
for x, y, rx, ry in ((160, 1460, 34, 20), (820, 1580, 44, 24), (480, 1740, 28, 16), (950, 1840, 30, 18)):
    o.append(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#A9A39A" stroke="{INK}" stroke-width="5"/><ellipse cx="{x - rx * 0.3:.0f}" cy="{y - ry * 0.4:.0f}" rx="{rx * 0.35:.0f}" ry="{ry * 0.25:.0f}" fill="#FFFFFF" opacity="0.6"/>')
o.append(f'<g transform="translate({TX} {TY}) scale({SC})">{inner}</g>')
o.append("</svg>")
print("\n".join(o))

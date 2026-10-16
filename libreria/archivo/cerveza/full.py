"""Versión pantalla completa (1080x1920) de la escena de las botellas para el gancho."""
import re, sys
sys.path.insert(0, ".")
from lib import *
src = open("escena.svg").read()
defs = re.search(r"<defs>.*?</defs>", src, re.S).group(0)
inner = src[src.index("</defs>") + 7: src.rindex("</svg>")]
TX, TY, SC = -160, 340, 1.4
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920">', defs]
o.append(f'<rect width="1080" height="{TY + 4}" fill="#FFF4E2"/>')
# azulejos que continúan hacia arriba
o.append('<g stroke="#EAD3B2" stroke-width="4">' + "".join(f'<line x1="0" y1="{TY + SC * y:.0f}" x2="1080" y2="{TY + SC * y:.0f}"/>' for y in range(-280, 0, 90)) +
         "".join(f'<line x1="{TX + SC * (x + (45 if (y // 90) % 2 else 0)):.0f}" y1="{TY + SC * y:.0f}" x2="{TX + SC * (x + (45 if (y // 90) % 2 else 0)):.0f}" y2="{TY + SC * (y + 90):.0f}"/>' for y in range(-280, 0, 90) for x in range(-180, 1180, 180)) + '</g>')
o.append(f'<g transform="translate({TX} {TY}) scale({SC})">{inner}</g>')
bot = TY + SC * 718
o.append(f'<rect y="{bot:.0f}" width="1080" height="{1920 - bot:.0f}" fill="#7A4A26"/>')
o.append(f'<line x1="0" y1="{bot:.0f}" x2="1080" y2="{bot:.0f}" stroke="{INK}" stroke-width="8"/>')
o.append(f'<rect y="{bot + 4:.0f}" width="1080" height="40" fill="#5A3416" opacity="0.6"/>')
o.append("</svg>")
print("\n".join(o))

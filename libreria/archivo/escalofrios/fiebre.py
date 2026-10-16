"""Full 1080x1920: persona con fiebre envuelta en una manta, termómetro 37 -> 39, bocadillo «¡QUÉ FRÍO!»."""
import math, sys
sys.path.insert(0, sys.path[0])
from common import *

defs = '''
<linearGradient id="wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2E3A66"/><stop offset="0.5" stop-color="#46578C"/><stop offset="1" stop-color="#5D6FA3"/></linearGradient>
<radialGradient id="lamp" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#FFE7A8" stop-opacity="0.75"/><stop offset="1" stop-color="#FFE7A8" stop-opacity="0"/></radialGradient>
<radialGradient id="face" cx="0.42" cy="0.35" r="0.75"><stop offset="0" stop-color="#FBD9C0"/><stop offset="0.7" stop-color="#EDB08C"/><stop offset="1" stop-color="#C98462"/></radialGradient>
<linearGradient id="manta" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#C792EA"/><stop offset="0.6" stop-color="#9558C9"/><stop offset="1" stop-color="#6A3496"/></linearGradient>
<linearGradient id="wood" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#C98B55"/><stop offset="1" stop-color="#7A4A26"/></linearGradient>
<linearGradient id="sheet" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#C9D6EA"/></linearGradient>
<linearGradient id="night" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0F1A3A"/><stop offset="1" stop-color="#2C3F7A"/></linearGradient>
<linearGradient id="lcd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E8F7E0"/><stop offset="1" stop-color="#BFE0B0"/></linearGradient>
'''
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920">\n<defs>{defs}</defs>']
o.append('<rect width="1080" height="1920" fill="url(#wall)"/>')
# ventana de noche con luna
o.append(f'<rect x="110" y="200" width="300" height="250" rx="10" fill="url(#night)" stroke="#1B2140" stroke-width="10"/>')
o.append('<circle cx="320" cy="270" r="40" fill="#FFF6D0"/><circle cx="338" cy="258" r="38" fill="#1A2652"/>')
o.append('<g fill="#FFFFFF">' + "".join(f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x, y, r in [(170, 250, 4), (230, 330, 3), (360, 390, 3), (200, 410, 2)]) + '</g>')
o.append('<line x1="260" y1="200" x2="260" y2="450" stroke="#1B2140" stroke-width="8"/><line x1="110" y1="325" x2="410" y2="325" stroke="#1B2140" stroke-width="8"/>')
o.append('<circle cx="900" cy="300" r="260" fill="url(#lamp)"/>')
# suelo
o.append('<rect x="0" y="1420" width="1080" height="500" fill="#2A2F4E"/>')
# cama: cabecero + colchón
o.append(f'<rect x="120" y="930" width="840" height="420" rx="40" fill="url(#wood)" stroke="{INK}" stroke-width="8"/>')
o.append('<path d="M 150 960 L 930 960" stroke="#E2AE7E" stroke-width="7" stroke-linecap="round" opacity="0.8"/>')
o.append(f'<rect x="60" y="1260" width="960" height="200" rx="30" fill="url(#sheet)" stroke="{INK}" stroke-width="8"/>')
o.append(f'<rect x="60" y="1440" width="960" height="70" rx="16" fill="url(#wood)" stroke="{INK}" stroke-width="8"/>')

# persona envuelta (grupo que tiembla)
o.append('<g id="persona">')
o.append('<ellipse cx="540" cy="1300" rx="330" ry="26" fill="#0B0B14" opacity="0.25"/>')
manta = "M 540 500 C 690 500, 735 620, 730 760 C 800 860, 880 1050, 880 1300 L 200 1300 C 200 1050, 280 860, 350 760 C 345 620, 390 500, 540 500 Z"
o.append(f'<path d="{manta}" fill="url(#manta)" stroke="{INK}" stroke-width="9" stroke-linejoin="round"/>')
o.append('<g stroke="#7C3FB0" stroke-width="6" opacity="0.6" fill="none">' + "".join(
    f'<path d="M {x} 860 Q {x + (x-540)*0.15:.0f} 1080 {x + (x-540)*0.3:.0f} 1290"/>' for x in (400, 470, 610, 680)) + '</g>')
o.append('<path d="M 430 530 C 480 508, 560 506, 620 520" fill="none" stroke="#E9C8FF" stroke-width="8" stroke-linecap="round"/>')
# abertura de la capucha
o.append(f'<ellipse cx="540" cy="715" rx="150" ry="170" fill="#5A2C84" stroke="{INK}" stroke-width="8"/>')
# cara
o.append(f'<ellipse cx="540" cy="725" rx="122" ry="142" fill="url(#face)" stroke="{INK}" stroke-width="8"/>')
o.append(f'<path d="M 465 690 L 505 702" stroke="#6B4632" stroke-width="9" stroke-linecap="round"/><path d="M 615 690 L 575 702" stroke="#6B4632" stroke-width="9" stroke-linecap="round"/>')
o.append(f'<path d="M 470 728 Q 490 742 510 728" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/><path d="M 570 728 Q 590 742 610 728" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>')
o.append('<ellipse cx="470" cy="775" rx="30" ry="17" fill="#FF5A36" opacity="0.45"/><ellipse cx="610" cy="775" rx="30" ry="17" fill="#FF5A36" opacity="0.45"/>')
o.append(f'<path d="M 540 750 Q 528 775 545 780" fill="none" stroke="#B0715A" stroke-width="6" stroke-linecap="round"/>')
o.append(f'<ellipse cx="545" cy="815" rx="22" ry="14" fill="#7A2E2E" stroke="{INK}" stroke-width="6"/>')
# gota de sudor
o.append(f'<path d="M 640 640 C 652 662, 660 676, 648 688 C 636 698, 622 686, 628 670 Z" fill="#9FD8FF" stroke="{INK}" stroke-width="5"/>')
# manos asomando sujetando la manta
o.append(f'<ellipse cx="470" cy="930" rx="38" ry="30" fill="url(#face)" stroke="{INK}" stroke-width="7"/><ellipse cx="610" cy="930" rx="38" ry="30" fill="url(#face)" stroke="{INK}" stroke-width="7"/>')
o.append(f'<path d="M 455 905 C 500 950, 580 950, 625 905" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>')
o.append('</g>')

# termómetro en la boca
o.append('<g id="termometro">')
o.append(stroke2("M 556 818 L 740 880", 22, "#FFFFFF", 8))
o.append(f'<circle cx="556" cy="818" r="9" fill="#B9C3CF" stroke="{INK}" stroke-width="4"/>')
o.append(f'<rect x="720" y="840" width="250" height="110" rx="28" fill="#3D8BFF" stroke="{INK}" stroke-width="8"/>')
o.append(f'<rect x="742" y="858" width="206" height="74" rx="12" fill="url(#lcd)" stroke="{INK}" stroke-width="5"/>')
o.append('</g>')
o.append(f'<g id="t37"><text x="845" y="912" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="50" fill="{INK}">37,0°</text></g>')
o.append(f'<g id="t39"><text x="845" y="912" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="50" fill="#D2311C">39,0°</text></g>')

# bocadillo de pensamiento
o.append('<g id="bocadillo">')
for x, y, r in [(700, 625, 12), (738, 598, 18)]:
    o.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFFFFF" stroke="{INK}" stroke-width="6"/>')
o.append(f'<ellipse cx="870" cy="532" rx="180" ry="68" fill="#FFFFFF" stroke="{INK}" stroke-width="8"/>')
o.append(f'<text x="870" y="547" text-anchor="middle" font-family="Unbounded" font-weight="800" font-size="42" fill="#2F6FB0">¡QUÉ FRÍO!</text>')
o.append('</g>')

# líneas de temblor
def shiver(x, y):
    return stroke2(f"M {x} {y} q 10 16 0 32 q -10 16 0 32 q 10 16 0 32", 8, "#5BC0FF", 6)
o.append('<g id="temblor">' + shiver(170, 1000) + shiver(140, 1050) + shiver(910, 1000) + shiver(940, 1050) + shiver(320, 600) + shiver(290, 650) + '</g>')
# etiqueta
o.append(tag("lfiebre", 120, 1150 - 260, tw("CON FIEBRE"), "CON FIEBRE", bg=CORAL, fg="#FFFFFF"))
o.append('</svg>')
print("\n".join(o))

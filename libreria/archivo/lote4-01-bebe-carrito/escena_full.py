import sys; sys.path.insert(0, "../tools")
from tofull import tofull
INK = "#0B0B14"
back = []
# guirnalda de banderines y lámpara (arriba, lejos: sin contorno)
pts = [(0, 250), (270, 330), (540, 360), (810, 330), (1080, 250)]
back.append('<path d="M 0 250 Q 270 360 540 360 Q 810 360 1080 250" fill="none" stroke="#D9BC96" stroke-width="5"/>')
cols = ["#F7B5B5", "#B5D8F7", "#F7DFA0", "#B9E3C6", "#C9B9E8"]
import math
for i in range(1, 16):
    t = i / 16
    x = t * 1080
    y = 250 + (1 - (2 * t - 1) ** 2) * 108
    back.append(f'<path d="M {x-26:.0f} {y-4:.0f} L {x+26:.0f} {y+4:.0f} L {x:.0f} {y+56:.0f} Z" fill="{cols[i%5]}"/>')
back.append('<rect x="80" y="520" width="0" height="0"/>')
# suelo: juguetes desenfocados
back.append('<g opacity="0.85"><circle cx="160" cy="1420" r="70" fill="#F7C3D6"/><path d="M 100 1400 Q 160 1360 220 1400" fill="none" stroke="#FFFFFF" stroke-width="10" opacity="0.6"/>'
            '<rect x="760" y="1360" width="110" height="110" rx="12" fill="#B5D8F7"/><rect x="880" y="1400" width="90" height="90" rx="10" fill="#F7DFA0"/><rect x="820" y="1290" width="90" height="80" rx="10" fill="#B9E3C6"/></g>'
            '<g stroke="#B8895A" stroke-width="3" opacity="0.5">' + "".join(f'<line x1="0" y1="{y}" x2="1080" y2="{y}"/>' for y in (1260, 1340, 1440, 1560, 1700, 1860)) + '</g>')
tofull("escena.svg", "escena_full.svg", "#FFF4E2", "#C99A62", "\n".join(back))

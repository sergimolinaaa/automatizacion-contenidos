import sys, math, random
sys.path.insert(0, "/tmp/claude-0/-home-user-automatizacion-contenidos/039df981-7a17-5355-b711-18510fb209db/scratchpad/volcan")
from vlib import *
random.seed(5)
VX, VY = 390, 262
shield = "M -10 470 C 110 400, 230 290, 320 262 L 460 258 C 570 268, 770 370, 1010 452 L 1010 700 L -10 700 Z"
sea = "M 560 700 C 660 650, 800 596, 1010 572 L 1010 700 Z"
river = [(VX + 8, VY + 6), (440, 292), (500, 316), (548, 352), (600, 386), (660, 410), (712, 446), (760, 488), (812, 526), (858, 560), (884, 590)]
rd = smooth(river)
defs = "\n".join([
    lg("sky", [(0, "#46589A"), (0.55, "#B583A6"), (1, "#FFB27A")]),
    lg("rock", [(0, "#5A5560"), (0.5, "#3A3640"), (1, "#1E1B22")]),
    lg("sea", [(0, "#4FA7E0"), (1, "#1F5FA8")]),
    rg("glow", [(0, "#FFE38A", 0.9), (0.5, "#FF8A3D", 0.5), (1, "#FF5A36", 0)]),
    rg("puff", [(0, "#FFFFFF"), (0.7, "#E9E4EE"), (1, "#BDB6C6")], 0.4, 0.35, 0.7),
    lg("palm", [(0, "#A0703F"), (1, "#6B4524")], 0, 0, 1, 0),
    f'<clipPath id="shc"><path d="{shield}"/></clipPath>',
])
o = [head(defs)]
o.append('<rect width="1000" height="700" fill="url(#sky)"/>')
o.append('<g fill="#FFFFFF" opacity="0.8">' + "".join(f'<circle cx="{random.uniform(360, 980):.0f}" cy="{random.uniform(60, 180):.0f}" r="{random.uniform(1.2, 2.6):.1f}"/>' for _ in range(22)) + '</g>')
# isla lejana
o.append('<path d="M 600 470 C 680 440, 760 430, 840 446 C 900 456, 960 450, 1010 444 L 1010 600 L 600 600 Z" fill="#7C6E8E" opacity="0.7"/>')
# escudo
o.append(f'<path d="{shield}" fill="url(#rock)"/>')
o.append('<g clip-path="url(#shc)">')
for _ in range(120):
    x, y = random.uniform(0, 1000), random.uniform(270, 700)
    r = random.uniform(3, 9)
    o.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r:.1f}" ry="{r * 0.45:.1f}" fill="#141217" opacity="0.5"/><ellipse cx="{x - 1:.0f}" cy="{y - 2:.0f}" rx="{r * 0.6:.1f}" ry="{r * 0.18:.1f}" fill="#8A8494" opacity="0.5"/>')
# coladas viejas solidificadas
for k, (a, b) in enumerate([((300, 300), (150, 560)), ((350, 300), (330, 640)), ((520, 300), (560, 560))]):
    o.append(f'<path d="M {a[0]} {a[1]} Q {(a[0] + b[0]) / 2 + 40} {(a[1] + b[1]) / 2} {b[0]} {b[1]}" fill="none" stroke="#2A2630" stroke-width="22" stroke-linecap="round" opacity="0.6"/>')
# resplandor de la lava sobre la roca
o.append(f'<path d="{rd}" fill="none" stroke="#FF7A3A" stroke-width="80" stroke-linecap="round" opacity="0.18"/>')
o.append('</g>')
o.append(f'<path d="M -10 470 C 110 400, 230 290, 320 262 L 460 258 C 570 268, 770 370, 1010 452" fill="none" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
o.append('<path d="M 40 438 C 140 380, 240 290, 320 270" fill="none" stroke="#8C8698" stroke-width="5" stroke-linecap="round" opacity="0.7"/>')
# mar
o.append(f'<path d="{sea}" fill="url(#sea)"/>')
o.append(f'<path d="M 560 700 C 660 650, 800 596, 1010 572" fill="none" stroke="{INK}" stroke-width="6"/>')
o.append('<g id="waves" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" opacity="0.7"><path d="M 760 660 q 15 -8 30 0 q 15 8 30 0"/><path d="M 900 630 q 15 -8 30 0 q 15 8 30 0"/><path d="M 700 690 q 15 -8 30 0"/></g>')
# cono de salpicaduras + resplandor
o.append(f'<ellipse cx="{VX}" cy="{VY}" rx="120" ry="60" fill="url(#glow)"/>')
o.append(f'<path d="M {VX - 52} {VY + 4} Q {VX - 30} {VY - 26} {VX - 14} {VY - 20} L {VX + 18} {VY - 20} Q {VX + 34} {VY - 26} {VX + 56} {VY + 4} Z" fill="#2A2630" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
# río de lava
o.append('<g id="rio">'
         f'<path d="{rd}" fill="none" stroke="{INK}" stroke-width="40" stroke-linecap="round" stroke-linejoin="round"/>'
         f'<path d="{rd}" fill="none" stroke="#E5432A" stroke-width="28" stroke-linecap="round" stroke-linejoin="round"/>'
         f'<path d="{rd}" fill="none" stroke="#FF8A3D" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/></g>')
o.append(f'<g id="riocore"><path d="{rd}" fill="none" stroke="#FFE38A" stroke-width="7" stroke-linecap="round"/></g>')
# vapor donde la lava toca el mar
st = [(884, 572, 22), (900, 540, 26), (880, 506, 28), (906, 470, 24), (888, 440, 20)]
o.append('<g id="vapor">' + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#puff)" opacity="0.9"/>' for x, y, r in st) + '</g>')
# fuente de lava
V = VY - 14
fo = f"M {VX - 16} {V + 2} C {VX - 34} {V - 50}, {VX - 30} {V - 104}, {VX - 4} {V - 136} C {VX + 22} {V - 104}, {VX + 32} {V - 50}, {VX + 16} {V + 2} Z"
fi = f"M {VX - 7} {V} C {VX - 16} {V - 44}, {VX - 14} {V - 82}, {VX - 3} {V - 104} C {VX + 10} {V - 82}, {VX + 16} {V - 44}, {VX + 7} {V} Z"
col = f"M {VX - 12} {V + 2} C {VX - 16} {V - 40}, {VX - 26} {V - 70}, {VX - 30} {V - 92} L {VX + 30} {V - 92} C {VX + 26} {V - 70}, {VX + 16} {V - 40}, {VX + 12} {V + 2} Z"
tops = [(VX - 26, V - 98, 17), (VX, V - 112, 21), (VX + 25, V - 97, 17), (VX - 10, V - 90, 14), (VX + 12, V - 88, 14)]
o.append('<g id="fuente">')
o.append(f'<path d="{col}" fill="{INK}" stroke="{INK}" stroke-width="12" stroke-linejoin="round"/>' + "".join(f'<circle cx="{x}" cy="{y}" r="{r + 6}" fill="{INK}"/>' for x, y, r in tops))
o.append(f'<path d="{col}" fill="#FF6A30"/>' + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FF7A36"/>' for x, y, r in tops))
o.append(f'<path d="M {VX - 5} {V} C {VX - 8} {V - 40}, {VX - 12} {V - 70}, {VX - 6} {V - 104}" stroke="#FFD34D" stroke-width="9" stroke-linecap="round" fill="none"/>' + "".join(f'<circle cx="{x - r * 0.25:.1f}" cy="{y - r * 0.25:.1f}" r="{r * 0.45:.1f}" fill="#FFD34D"/>' for x, y, r in tops))
for x, y, r in [(VX - 42, V - 112, 8), (VX + 36, V - 122, 9), (VX - 22, V - 158, 7), (VX + 18, V - 160, 6), (VX + 52, V - 84, 7), (VX - 54, V - 78, 6)]:
    o.append(f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r * 1.25:.1f}" fill="#FF8A3D" stroke="{INK}" stroke-width="4"/><circle cx="{x - r * 0.3:.1f}" cy="{y - r * 0.4:.1f}" r="{r * 0.3:.1f}" fill="#FFE38A"/>')
o.append('</g>')
# gas que se escapa: burbujas que revientan + bocanadas
o.append('<g id="gasup">' + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#puff)" stroke="{INK}" stroke-width="3" opacity="0.85"/>' for x, y, r in [(VX + 60, 200, 9), (VX + 76, 168, 11), (VX + 70, 132, 13), (VX + 92, 100, 15)]) + '</g>')
o.append('<g id="puffs">' + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#puff)" opacity="0.75"/>' for x, y, r in [(VX + 130, 120, 26), (VX + 168, 100, 30), (VX + 210, 84, 24)]) + '</g>')
# palmera
def palm(x0, y0, x1, y1):
    d = f"M {x0} {y0} Q {x0 + 40} {(y0 + y1) / 2} {x1} {y1}"
    s = f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="26" stroke-linecap="round"/><path d="{d}" fill="none" stroke="url(#palm)" stroke-width="16" stroke-linecap="round"/>'
    for k in range(8):
        t = 0.1 + k * 0.11
        px = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * (x0 + 40) + t * t * x1
        py = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * ((y0 + y1) / 2) + t * t * y1
        s += f'<path d="M {px - 7:.0f} {py:.0f} L {px + 7:.0f} {py - 3:.0f}" stroke="#4A2E16" stroke-width="3"/>'
    for ang, ln in [(-160, 120), (-130, 110), (-60, 115), (-25, 120), (20, 100), (160, 100)]:
        a = math.radians(ang)
        ex, ey = x1 + ln * math.cos(a), y1 + ln * math.sin(a) + 30
        cx, cy = x1 + ln * 0.5 * math.cos(a), y1 + ln * 0.5 * math.sin(a) - 30
        fd = f"M {x1} {y1} Q {cx:.0f} {cy:.0f} {ex:.0f} {ey:.0f}"
        s += f'<path d="{fd}" fill="none" stroke="{INK}" stroke-width="24" stroke-linecap="round"/><path d="{fd}" fill="none" stroke="#2F9A5A" stroke-width="14" stroke-linecap="round"/><path d="{fd}" fill="none" stroke="#7BE07B" stroke-width="3" stroke-linecap="round" transform="translate(0 -3)"/>'
    s += f'<circle cx="{x1 - 6}" cy="{y1 + 10}" r="9" fill="#6B4524" stroke="{INK}" stroke-width="4"/><circle cx="{x1 + 8}" cy="{y1 + 12}" r="9" fill="#6B4524" stroke="{INK}" stroke-width="4"/>'
    return s
o.append('<g id="palm">' + palm(110, 700, 150, 440) + '</g>')
# primer plano: lava cordada solidificada
o.append(f'<path d="M -10 640 C 80 620, 200 630, 300 650 C 380 666, 460 672, 560 700 L -10 700 Z" fill="#2A2630" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
o.append('<g fill="none" stroke="#5A5560" stroke-width="4" stroke-linecap="round">' + "".join(
    f'<path d="M {x} {y} q 12 -10 24 0 q 12 10 24 0"/>' for x, y in [(230, 668), (300, 676), (380, 686), (40, 662)]) + '</g>')
o.append(label("lliquido", 560, 200, "LÍQUIDO", 540, 350))
o.append(label("lgas", 610, 70, "GAS", VX + 104, 92))
o.append(label("lrio", 620, 584, "RÍO DE LAVA", 790, 510))
o.append('</svg>')
open(sys.argv[1], "w").write("\n".join(o))

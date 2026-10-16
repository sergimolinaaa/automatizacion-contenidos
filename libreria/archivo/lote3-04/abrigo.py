import math, random, sys
sys.path.insert(0, sys.path[0])
from common import *

random.seed(3)
SK = 540   # superficie de la piel
MID = 470  # separación entre las dos mitades
defs = '''
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9FC3E6"/><stop offset="1" stop-color="#DCEBF8"/></linearGradient>
<linearGradient id="skin" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F2C1A0"/><stop offset="0.35" stop-color="#E3A07C"/><stop offset="1" stop-color="#B9704F"/></linearGradient>
<linearGradient id="skin2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#D9A483"/><stop offset="0.35" stop-color="#C08460"/><stop offset="1" stop-color="#94573A"/></linearGradient>
<linearGradient id="warm" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#FF9A3D" stop-opacity="0.85"/><stop offset="0.7" stop-color="#FFC27A" stop-opacity="0.55"/><stop offset="1" stop-color="#FFE2B8" stop-opacity="0"/></linearGradient>
<radialGradient id="bump" cx="0.4" cy="0.3" r="0.8"><stop offset="0" stop-color="#FBD3B8"/><stop offset="1" stop-color="#DE9A76"/></radialGradient>
'''
o = [head(defs)]
o.append('<rect width="1000" height="700" fill="url(#sky)"/>')
o.append('<path d="M 0 300 C 150 250, 260 280, 400 240 C 560 200, 700 270, 860 230 C 930 215, 980 225, 1000 220 L 1000 560 L 0 560 Z" fill="#EAF3FB"/>')
o.append('<path d="M 0 380 C 180 350, 360 390, 540 360 C 700 335, 860 370, 1000 350 L 1000 560 L 0 560 Z" fill="#F7FBFF"/>')


def flake(cx, cy, r):
    d = " ".join(f"M {cx} {cy} L {cx + r*math.cos(math.radians(k*60+15)):.1f} {cy + r*math.sin(math.radians(k*60+15)):.1f}" for k in range(6))
    d += " " + " ".join(f"M {cx + r*0.55*math.cos(math.radians(k*60+15)):.1f} {cy + r*0.55*math.sin(math.radians(k*60+15)):.1f} L {cx + r*0.85*math.cos(math.radians(k*60+45)):.1f} {cy + r*0.85*math.sin(math.radians(k*60+45)):.1f}" for k in range(6))
    return (f'<path d="{d}" stroke="#6FA2D2" stroke-width="{r*0.22+5:.1f}" stroke-linecap="round"/>'
            f'<path d="{d}" stroke="#FFFFFF" stroke-width="{r*0.22:.1f}" stroke-linecap="round"/>')


o.append('<g id="snow">' + "".join(flake(x, y, r) for x, y, r in [(400, 160, 20), (600, 200, 16), (700, 120, 22), (930, 190, 18), (90, 230, 16), (250, 170, 13), (820, 250, 12)]) + '</g>')

# aire caliente atrapado en el pelaje (mitad derecha)
o.append(f'<g id="aireflat"><rect x="{MID}" y="{SK-62}" width="{1000-MID}" height="64" fill="url(#warm)"/></g>')
o.append(f'<g id="aireup"><rect x="{MID}" y="{SK-215}" width="{1000-MID}" height="217" fill="url(#warm)"/></g>')

# piel: izquierda (humano, hoy) y derecha (antepasado peludo)
o.append(f'<rect x="0" y="{SK}" width="{MID}" height="{700-SK}" fill="url(#skin)"/>')
o.append(f'<rect x="{MID}" y="{SK}" width="{1000-MID}" height="{700-SK}" fill="url(#skin2)"/>')
o.append(f'<g stroke="#A35A3E" stroke-width="3" opacity="0.35" fill="none">' + "".join(f'<path d="M {x} {SK+70} q 20 -10 40 0 t 40 0"/>' for x in range(30, 1000, 150)) + '</g>')

roots = list(range(MID + 10, 1010, 20))


def hairs(gid, ang, ln, bend):
    g = [f'<g id="{gid}">']
    random.seed(5)
    for x in roots:
        a = math.radians(ang + random.uniform(-5, 5))
        l = ln * random.uniform(0.9, 1.06)
        ex, ey = x + l * math.cos(a), SK + l * math.sin(a)
        mx, my = x + l * 0.5 * math.cos(a) + bend * math.sin(a), SK + l * 0.5 * math.sin(a) - bend * math.cos(a)
        col = random.choice(["#6B4428", "#7E5232", "#5A3820", "#8C5E3A"])
        d = f"M {x} {SK+4} Q {mx:.1f} {my:.1f} {ex:.1f} {ey:.1f}"
        g.append(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>'
                 f'<path d="{d}" fill="none" stroke="{col}" stroke-width="4.5" stroke-linecap="round"/>')
    g.append('</g>')
    return "".join(g)


# clip para que el pelo tumbado no invada la mitad humana
o.append(f'<clipPath id="right"><rect x="{MID}" y="0" width="{1000-MID}" height="700"/></clipPath>')
o.append(f'<g clip-path="url(#right)">' + hairs("furflat", -14, 200, 10) + hairs("furup", -72, 205, 12) + '</g>')
o.append('<g id="calor" fill="none" stroke="#FF5A1F" stroke-width="6" stroke-linecap="round">' + "".join(
    f'<path d="M {x} {y} c 8 -10, -8 -20, 0 -30 s -8 -20, 0 -30"/>' for x, y in [(560, 470), (700, 440), (840, 470), (950, 430)]) + '</g>')
o.append(f'<line x1="0" y1="{SK}" x2="1000" y2="{SK}" stroke="{INK}" stroke-width="8"/>')
o.append(f'<line x1="0" y1="{SK+10}" x2="1000" y2="{SK+10}" stroke="#FBDCC8" stroke-width="5" opacity="0.7"/>')
# humano: pocos pelos cortos sobre bultitos
o.append('<g id="humano">')
for x in range(60, MID - 30, 70):
    o.append(f'<path d="M {x-26} {SK} C {x-16} {SK}, {x-14} {SK-16}, {x} {SK-16} C {x+14} {SK-16}, {x+16} {SK}, {x+26} {SK} Z" fill="url(#bump)" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    o.append(stroke2(f"M {x} {SK-14} L {x+14} {SK-66}", 4, "#4A2E1C", 5))
o.append('</g>')

# separador
o.append(f'<rect x="{MID-8}" y="0" width="16" height="700" fill="#FFFFFF"/>')
o.append(f'<line x1="{MID-8}" y1="0" x2="{MID-8}" y2="700" stroke="{INK}" stroke-width="6"/><line x1="{MID+8}" y1="0" x2="{MID+8}" y2="700" stroke="{INK}" stroke-width="6"/>')

# el frío llega a la piel humana; en el pelaje se queda fuera
o.append('<g id="frio">' + arrow("fa1", [(170, 250), (180, 360), (170, 455)], col="#6FB8FF", w=10, head_len=30)
         + arrow("fa2", [(330, 270), (340, 380), (330, 455)], col="#6FB8FF", w=10, head_len=30) + '</g>')
o.append('<g id="frio2">' + arrow("fb1", [(640, 165), (650, 225), (640, 280)], col="#6FB8FF", w=10, head_len=30)
         + arrow("fb2", [(880, 165), (890, 225), (880, 280)], col="#6FB8FF", w=10, head_len=30) + '</g>')

o.append(tag("ltu", 40, 92, tw("HOY"), "HOY", bg="#FFFFFF", fg=INK))
o.append(tag("lantes", 520, 92, tw("ANTEPASADO"), "ANTEPASADO", bg="#FFFFFF", fg=INK))
o.append(tag("laire", 560, 590, tw("AIRE CALIENTE"), "AIRE CALIENTE", 760, 590, 760, 400))
o.append(tag("lmucho", 640, 330, tw("MUCHO PELO"), "MUCHO PELO", 760, 388, 760, 482))
o.append(tag("lpoco", 120, 590, tw("POCO PELO"), "POCO PELO", 200, 590, 200, 520))
o.append('</svg>')
print("\n".join(o))

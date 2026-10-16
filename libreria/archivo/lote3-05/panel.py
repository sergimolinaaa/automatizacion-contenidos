import math, random, sys
sys.path.insert(0, sys.path[0])
from common import *

random.seed(12)
M = 90  # avance de placas y piedras (escena de los surcos)
defs = '''
<linearGradient id="ice" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0.7"/><stop offset="0.5" stop-color="#E6F7FF" stop-opacity="0.5"/><stop offset="1" stop-color="#C6EBFC" stop-opacity="0.6"/></linearGradient>
<radialGradient id="glare" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#FFFBE0" stop-opacity="0.95"/><stop offset="0.5" stop-color="#FFF3B0" stop-opacity="0.5"/><stop offset="1" stop-color="#FFF3B0" stop-opacity="0"/></radialGradient>
<linearGradient id="sheet" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F4FBFF"/><stop offset="1" stop-color="#C9EBFB"/></linearGradient>
<radialGradient id="rock" cx="0.35" cy="0.3" r="0.8"><stop offset="0" stop-color="#A39486"/><stop offset="0.55" stop-color="#6A5E54"/><stop offset="1" stop-color="#3A322C"/></radialGradient>
'''
o = [head(defs)]
o.append('<rect width="1000" height="700" fill="#D9C4A0"/>')
# barro agrietado (vista cenital)
pts = {}
for i in range(-1, 12):
    for j in range(-1, 9):
        pts[(i, j)] = (i * 100 + random.uniform(-30, 30), j * 95 + random.uniform(-28, 28))
o.append('<g stroke="#A88B64" stroke-width="5" stroke-linejoin="round">')
for i in range(-1, 11):
    for j in range(-1, 8):
        q = [pts[(i, j)], pts[(i + 1, j)], pts[(i + 1, j + 1)], pts[(i, j + 1)]]
        o.append(f'<path d="{poly(q)} Z" fill="{random.choice(["#DCC7A2", "#D5BE97", "#E0CDAA"])}"/>')
o.append('</g>')

# surcos antiguos (en el barro, bajo el agua)
rocks = {"ra": (270, 175, 42), "rb": (470, 400, 52), "rc": (640, 110, 36), "rd": (880, 540, 46), "re": (200, 575, 40)}
trails = {
    "ra": [(270, 175), (190, 190), (100, 150), (-10, 175)],
    "rb": [(470, 400), (380, 385), (290, 440), (160, 410)],
    "rc": [(640, 110), (560, 125), (490, 95), (400, 120)],
    "rd": [(880, 540), (790, 560), (700, 515), (610, 545)],
    "re": [(200, 575), (120, 595), (20, 565)],
}


def cr(ctrl, n=20):
    out = []
    for i in range(len(ctrl) - 1):
        p0 = ctrl[max(0, i - 1)]; p1 = ctrl[i]; p2 = ctrl[i + 1]; p3 = ctrl[min(len(ctrl) - 1, i + 2)]
        for k in range(n):
            t = k / n
            out.append(tuple(0.5 * ((2 * p1[c]) + (-p0[c] + p2[c]) * t + (2 * p0[c] - 5 * p1[c] + 4 * p2[c] - p3[c]) * t * t + (-p0[c] + 3 * p1[c] - 3 * p2[c] + p3[c]) * t ** 3) for c in (0, 1)))
    out.append(ctrl[-1])
    return out


for rid, tr in trails.items():
    w = rocks[rid][2] * 1.2
    d = poly(cr(tr))
    o.append(f'<path d="{d}" fill="none" stroke="#F2E4C8" stroke-width="{w+14:.0f}" stroke-linecap="round" stroke-linejoin="round"/>'
             f'<path d="{d}" fill="none" stroke="#6E5232" stroke-width="{w:.0f}" stroke-linecap="round" stroke-linejoin="round"/>'
             f'<path d="{d}" fill="none" stroke="#8C6E48" stroke-width="{w*0.4:.0f}" stroke-linecap="round" stroke-linejoin="round"/>')
# surcos nuevos (se dibujan cuando avanzan las piedras)
o.append('<g id="nuevos">')
for rid, (x, y, r) in rocks.items():
    w = r * 1.2
    d = f"M {x} {y} L {x+M} {y}"
    o.append(f'<path d="{d}" fill="none" stroke="#F2E4C8" stroke-width="{w+14:.0f}" stroke-linecap="round"/>'
             f'<path d="{d}" fill="none" stroke="#6E5232" stroke-width="{w:.0f}" stroke-linecap="round"/>'
             f'<path d="{d}" fill="none" stroke="#8C6E48" stroke-width="{w*0.4:.0f}" stroke-linecap="round"/>')
o.append('</g>')
# lámina de agua
o.append('<rect width="1000" height="700" fill="#3F8FDA" opacity="0.5"/>')

# placas de hielo
panels = {
    "p1": [(-40, -40), (360, -40), (330, 140), (300, 270), (-40, 300)],
    "p2": [(360, -40), (720, -40), (690, 180), (560, 230), (300, 270), (330, 140)],
    "p3": [(720, -40), (1040, -40), (1040, 330), (800, 300), (690, 180)],
    "p4": [(-40, 300), (300, 270), (360, 450), (280, 740), (-40, 740)],
    "p5": [(300, 270), (560, 230), (520, 470), (600, 740), (280, 740), (360, 450)],
    "p6": [(560, 230), (690, 180), (800, 300), (740, 480), (600, 740), (520, 470)],
    "p7": [(800, 300), (1040, 330), (1040, 740), (600, 740), (740, 480)],
}
member = {"ra": "p1", "rb": "p5", "rc": "p2", "rd": "p7", "re": "p4"}


def shrink(q, k=12):
    cx = sum(p[0] for p in q) / len(q); cy = sum(p[1] for p in q) / len(q)
    out = []
    for x, y in q:
        dx, dy = x - cx, y - cy; d = math.hypot(dx, dy)
        out.append((x - dx / d * k, y - dy / d * k))
    return out


def rock(rid):
    x, y, r = rocks[rid]
    random.seed(sum(map(ord, rid)))
    q = []
    for k in range(10):
        a = k * math.pi / 5
        rr = r * random.uniform(0.85, 1.1)
        q.append((x + rr * math.cos(a), y + rr * 0.85 * math.sin(a)))
    return (f'<g id="{rid}"><ellipse cx="{x+8}" cy="{y+10}" rx="{r*1.05:.0f}" ry="{r*0.9:.0f}" fill="#22303F" opacity="0.35"/>'
            f'<path d="{poly(q)} Z" fill="url(#rock)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
            f'<ellipse cx="{x-r*0.3:.0f}" cy="{y-r*0.35:.0f}" rx="{r*0.35:.0f}" ry="{r*0.18:.0f}" fill="#D2C6BA" opacity="0.8" transform="rotate(-20 {x-r*0.3:.0f} {y-r*0.35:.0f})"/>'
            f'<circle cx="{x}" cy="{y}" r="{r+9:.0f}" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.7"/></g>')


o.append('<g id="paneles">')
for pid, q in panels.items():
    s = shrink(q)
    g = f'<g id="{pid}"><path d="{poly(s)} Z" fill="url(#ice)" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    g += f'<path d="{poly(shrink(q, 20))} Z" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.8" stroke-linejoin="round"/>'
    cx = sum(p[0] for p in q) / len(q); cy = sum(p[1] for p in q) / len(q)
    g += f'<path d="M {cx-60:.0f} {cy-30:.0f} l 50 -20 M {cx-30:.0f} {cy+10:.0f} l 70 -28" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round" opacity="0.7"/>'
    for rid, p in member.items():
        if p == pid:
            g += rock(rid)
    g += '</g>'
    o.append(g)
o.append('</g>')

# lámina entera (antes de romperse)
o.append(f'<g id="entero"><rect x="-20" y="-20" width="1040" height="740" fill="url(#sheet)" opacity="0.93"/>'
         f'<g stroke="#FFFFFF" stroke-width="8" stroke-linecap="round" opacity="0.8"><path d="M 120 200 l 160 -70 M 560 520 l 200 -90 M 700 150 l 120 -50"/></g>'
         + "".join(rock(r).replace(f'id="{r}"', f'id="{r}0"') for r in rocks) + '</g>')
# grietas que se abren
crack_paths = ["M 360 -40 L 330 140 L 300 270 L 360 450 L 280 740", "M -40 300 L 300 270 L 560 230 L 690 180 L 720 -40",
               "M 690 180 L 800 300 L 1040 330", "M 800 300 L 740 480 L 600 740", "M 560 230 L 520 470 L 600 740", "M 330 140 L 360 -40"]
o.append('<g id="grietas">' + "".join(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"/>' for d in crack_paths) + '</g>')
# sol que calienta (rayos en diagonal)
o.append('<g id="brillo"><circle cx="930" cy="40" r="330" fill="url(#glare)"/>' + "".join(f'<path d="M {x} {y-16} L {x+4} {y-4} L {x+16} {y} L {x+4} {y+4} L {x} {y+16} L {x-4} {y+4} L {x-16} {y} L {x-4} {y-4} Z" fill="#FFFFFF" stroke="#E8B830" stroke-width="2"/>' for x, y in [(780, 150), (600, 300), (900, 260), (420, 230), (700, 420)]) + '</g>')
o.append('<g id="viento">' + arrow("wv", [(370, 630), (480, 620), (600, 630)], col=LIME, w=12) + '</g>')

o.append(tag("lpanel", 540, 600, tw("PLACA DE HIELO"), "PLACA DE HIELO", 740, 600, 760, 560))
o.append(tag("lgrieta", 60, 330, tw("GRIETA"), "GRIETA", 140, 330, 150, 286))
o.append(tag("lsurco", 60, 300, tw("SURCO"), "SURCO", 120, 300, 110, 160))
o.append('</svg>')
print("\n".join(o))

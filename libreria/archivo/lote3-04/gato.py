import math, random, sys
sys.path.insert(0, sys.path[0])
from common import *

random.seed(2)
FL = 600  # suelo


def bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0], u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1])


def dbez(p0, p1, p2, p3, t):
    u = 1 - t
    return (3*u*u*(p1[0]-p0[0]) + 6*u*t*(p2[0]-p1[0]) + 3*t*t*(p3[0]-p2[0]), 3*u*u*(p1[1]-p0[1]) + 6*u*t*(p2[1]-p1[1]) + 3*t*t*(p3[1]-p2[1]))


defs = '''
<linearGradient id="wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3E3A66"/><stop offset="1" stop-color="#6A5E8E"/></linearGradient>
<linearGradient id="floor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#B5835A"/><stop offset="1" stop-color="#7E5636"/></linearGradient>
<linearGradient id="fur" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFB25C"/><stop offset="0.55" stop-color="#F08A2C"/><stop offset="1" stop-color="#C8641A"/></linearGradient>
<linearGradient id="legfur" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#D87022"/><stop offset="1" stop-color="#E68A3A"/></linearGradient>
<linearGradient id="furdark" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#D9782A"/><stop offset="1" stop-color="#A24E14"/></linearGradient>
<radialGradient id="head" cx="0.45" cy="0.35" r="0.75"><stop offset="0" stop-color="#FFC27A"/><stop offset="0.7" stop-color="#F08A2C"/><stop offset="1" stop-color="#D06E1E"/></radialGradient>
<radialGradient id="iris" cx="0.4" cy="0.35" r="0.7"><stop offset="0" stop-color="#F4FF8A"/><stop offset="1" stop-color="#9CC420"/></radialGradient>
<radialGradient id="moon" cx="0.4" cy="0.4" r="0.7"><stop offset="0" stop-color="#FFFBE0"/><stop offset="1" stop-color="#F6E7A0"/></radialGradient>
'''
FREE = len(sys.argv) > 1 and sys.argv[1] == "free"
if FREE:
    o = [head(defs).replace('viewBox="0 0 1000 700"', 'viewBox="0 0 1000 860"'), '<g transform="translate(0 120)">']
    o.append(f'<ellipse cx="500" cy="{FL+6}" rx="360" ry="46" fill="#C9935E" stroke="{INK}" stroke-width="7"/>')
    o.append(f'<ellipse cx="500" cy="{FL+6}" rx="320" ry="32" fill="none" stroke="#9E6A3C" stroke-width="5" stroke-dasharray="14 10"/>')
    o.append(f'<ellipse cx="500" cy="{FL+4}" rx="250" ry="16" fill="#3A2412" opacity="0.4"/>')
else:
    o = [head(defs)]
    o.append('<rect width="1000" height="700" fill="url(#wall)"/>')
    # ventana con luna (fondo, sin contorno grueso)
    o.append('<rect x="70" y="90" width="230" height="250" rx="10" fill="#26234A"/><circle cx="200" cy="180" r="50" fill="url(#moon)"/>'
             '<circle cx="185" cy="170" r="9" fill="#EAD98A"/><circle cx="215" cy="200" r="6" fill="#EAD98A"/>'
             '<g fill="#FFFFFF" opacity="0.8"><circle cx="110" cy="130" r="3"/><circle cx="260" cy="280" r="3"/><circle cx="130" cy="290" r="2.5"/></g>'
             '<path d="M 185 90 L 185 340 M 70 215 L 300 215" stroke="#7E6FA8" stroke-width="10"/><rect x="70" y="90" width="230" height="250" rx="10" fill="none" stroke="#7E6FA8" stroke-width="12"/>')
    o.append(f'<rect y="{FL}" width="1000" height="{700-FL}" fill="url(#floor)"/>')
    o.append(f'<g stroke="#6A4528" stroke-width="3" opacity="0.6">' + "".join(f'<line x1="{x}" y1="{FL+4}" x2="{x-60}" y2="700"/>' for x in range(80, 1100, 160)) + '</g>')
    o.append(f'<line x1="0" y1="{FL}" x2="1000" y2="{FL}" stroke="{INK}" stroke-width="7"/>')
    o.append(f'<ellipse cx="500" cy="{FL+12}" rx="270" ry="18" fill="#3A2412" opacity="0.4"/>')

# --- cuerpo arqueado (curvas cúbicas) ---
B0 = (338, 440)
segs = [  # espalda: grupa -> cima -> cuello
    (B0, (318, 340), (380, 248), (476, 238)),
    ((476, 238), (572, 228), (632, 292), (668, 372)),
]
rest = "C 692 422, 686 470, 656 488 C 610 482, 560 418, 492 412 C 430 410, 396 444, 382 488 C 362 500, 340 480, 338 440 Z"
body_d = f"M {B0[0]} {B0[1]} " + " ".join(f"C {a[0]} {a[1]}, {b[0]} {b[1]}, {c[0]} {c[1]}" for _, a, b, c in segs) + " " + rest

# pelo erizado: púas a lo largo de la espalda
spk = []
inner = []
N = 34
for k in range(N + 1):
    s = k / N * 2
    i = min(1, int(s)); t = s - i
    p = bez(*segs[i], t); d = dbez(*segs[i], t)
    ln = math.hypot(*d); nx_, ny_ = d[1] / ln, -d[0] / ln
    tx, ty = d[0] / ln, d[1] / ln
    off = random.uniform(34, 50) if k % 2 else random.uniform(2, 8)
    ramp = min(1, k / 5, (N - k) / 5)
    off *= max(0.25, ramp)
    spk.append((p[0] + nx_ * off - tx * (random.uniform(4, 16) if k % 2 else 0), p[1] + ny_ * off - ty * (random.uniform(4, 16) if k % 2 else 0)))
    inner.append((p[0] - nx_ * 22, p[1] - ny_ * 22))
fr = poly(spk) + " L " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in reversed(inner)) + " Z"

# cola: lisa y esponjada
tail_c = [(342, 410), (290, 360), (232, 300), (258, 168)]


def tail_shape(w0, w1, spiky):
    left, right = [], []
    N = 30
    for k in range(N + 1):
        t = k / N
        p = bez(*tail_c, t); d = dbez(*tail_c, t)
        ln = math.hypot(*d); nx_, ny_ = -d[1] / ln, d[0] / ln
        w = w0 + (w1 - w0) * t
        if t > 0.85:
            w *= math.sqrt(max(0.0, (1 - t) / 0.15)) * 0.9 + 0.1
        j = (random.uniform(10, 20) if (spiky and k % 2) else 0) * (1 if 0.05 < t < 0.97 else 0)
        left.append((p[0] + nx_ * (w + j), p[1] + ny_ * (w + j)))
        right.append((p[0] - nx_ * (w + j), p[1] - ny_ * (w + j)))
    return poly(left) + " L " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in reversed(right)) + " Z"


def leg(x0, y0, x1, w0, w1, col):
    d = f"M {x0-w0/2} {y0} C {x0-w0/2} {y0+60}, {x1-w1/2} {FL-70}, {x1-w1/2} {FL-14} L {x1+w1/2} {FL-14} C {x1+w1/2} {FL-70}, {x0+w0/2} {y0+60}, {x0+w0/2} {y0} Z"
    dopen = d.replace(" Z", "")
    return (f'<path d="{d}" fill="{col}"/><path d="{dopen}" fill="none" stroke="{INK}" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"/>'
            f'<ellipse cx="{x1+6}" cy="{FL-10}" rx="{w1*0.85:.0f}" ry="13" fill="{col}" stroke="{INK}" stroke-width="7"/>'
            f'<path d="M {x1-2} {FL-14} l 0 9 M {x1+12} {FL-14} l 0 9" stroke="{INK}" stroke-width="3" opacity="0.6"/>')


o.append('<g id="cat">')
# patas lejanas
o.append(leg(612, 450, 616, 40, 28, "url(#furdark)"))
o.append(leg(392, 450, 402, 42, 28, "url(#furdark)"))
# cola
o.append(f'<g id="tailthin"><path d="{tail_shape(15, 12, False)}" fill="url(#fur)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
         + "".join(f'<path d="M {bez(*tail_c,t)[0]-14:.0f} {bez(*tail_c,t)[1]+4:.0f} l 26 -8" stroke="#B85A16" stroke-width="6" stroke-linecap="round"/>' for t in (0.3, 0.5, 0.7)) + '</g>')
o.append(f'<g id="tailpuff"><path d="{tail_shape(34, 30, True)}" fill="url(#fur)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
         + "".join(f'<path d="M {bez(*tail_c,t)[0]-24:.0f} {bez(*tail_c,t)[1]+8:.0f} l 46 -14" stroke="#B85A16" stroke-width="8" stroke-linecap="round"/>' for t in (0.3, 0.5, 0.7)) + '</g>')
# púas de pelo erizado
o.append(f'<g id="bristle"><path d="{fr}" fill="url(#fur)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/></g>')
# cuerpo
o.append(f'<path d="{body_d}" fill="url(#fur)" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>')
# rayas atigradas
for i, t in enumerate([0.25, 0.42, 0.58, 0.75]):
    s = t * 2; k = min(1, int(s)); tt = s - k
    p = bez(*segs[k], tt); d = dbez(*segs[k], tt); ln = math.hypot(*d)
    nx_, ny_ = -d[1] / ln, d[0] / ln  # hacia dentro
    a = (p[0] + nx_ * 6, p[1] + ny_ * 6); b = (p[0] + nx_ * 70 + d[0] / ln * 12, p[1] + ny_ * 70 + d[1] / ln * 12)
    o.append(f'<path d="M {a[0]:.1f} {a[1]:.1f} Q {(a[0]+b[0])/2 - d[0]/ln*10:.1f} {(a[1]+b[1])/2 - d[1]/ln*10:.1f} {b[0]:.1f} {b[1]:.1f}" fill="none" stroke="#B85A16" stroke-width="12" stroke-linecap="round"/>')
o.append('<path d="M 400 300 C 440 260, 520 250, 580 270" fill="none" stroke="#FFD49A" stroke-width="7" stroke-linecap="round" opacity="0.8"/>')
# patas cercanas
o.append(leg(648, 455, 662, 46, 30, "url(#legfur)"))
o.append('<path d="M 340 380 C 320 420, 330 470, 352 490 C 370 470, 380 430, 372 400 Z" fill="#E07A24" stroke="none"/>')
o.append(leg(356, 470, 348, 50, 30, "url(#legfur)"))
for x0, x1 in ((648, 662), (356, 348)):
    o.append(f'<path d="M {x1-12} {FL-70} l 26 -4 M {x1-13} {FL-110} l 26 -4" stroke="#B85A16" stroke-width="6" stroke-linecap="round"/>')

# cabeza (de frente, mirando al espectador)
HX, HY = 742, 372
o.append(f'<g id="headg">')
o.append(f'<path d="M {HX-62} {HY-30} L {HX-78} {HY-112} L {HX-18} {HY-62} Z" fill="url(#fur)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
o.append(f'<path d="M {HX+62} {HY-30} L {HX+78} {HY-112} L {HX+18} {HY-62} Z" fill="url(#fur)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
o.append(f'<path d="M {HX-58} {HY-46} L {HX-68} {HY-92} L {HX-34} {HY-62} Z" fill="#FFB3B0"/><path d="M {HX+58} {HY-46} L {HX+68} {HY-92} L {HX+34} {HY-62} Z" fill="#FFB3B0"/>')
o.append(f'<path d="M {HX-80} {HY+5} C {HX-80} {HY-60}, {HX+80} {HY-60}, {HX+80} {HY+5} C {HX+88} {HY+30}, {HX+70} {HY+40}, {HX+76} {HY+52} C {HX+40} {HY+78}, {HX-40} {HY+78}, {HX-76} {HY+52} C {HX-70} {HY+40}, {HX-88} {HY+30}, {HX-80} {HY+5} Z" fill="url(#head)" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>')
o.append(f'<path d="M {HX-14} {HY-56} l 4 22 M {HX} {HY-58} l 0 24 M {HX+14} {HY-56} l -4 22" stroke="#B85A16" stroke-width="6" stroke-linecap="round"/>')
o.append(f'<path d="M {HX-78} {HY+10} l 22 4 M {HX-80} {HY+26} l 20 0 M {HX+78} {HY+10} l -22 4 M {HX+80} {HY+26} l -20 0" stroke="#B85A16" stroke-width="5" stroke-linecap="round"/>')
o.append(f'<ellipse cx="{HX}" cy="{HY+40}" rx="40" ry="26" fill="#FFE2B8"/>')
for sx in (-1, 1):
    ex = HX + sx * 32
    o.append(f'<ellipse cx="{ex}" cy="{HY-6}" rx="21" ry="23" fill="url(#iris)" stroke="{INK}" stroke-width="5"/>'
             f'<ellipse cx="{ex}" cy="{HY-6}" rx="11" ry="17" fill="{INK}"/>'
             f'<circle cx="{ex-6}" cy="{HY-14}" r="5" fill="#FFFFFF"/>')
o.append(f'<path d="M {HX-9} {HY+20} L {HX+9} {HY+20} L {HX} {HY+30} Z" fill="#E86F8A" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>')
# boca abierta bufando con colmillos
o.append(f'<path d="M {HX-22} {HY+38} C {HX-14} {HY+66}, {HX+14} {HY+66}, {HX+22} {HY+38} C {HX+10} {HY+34}, {HX-10} {HY+34}, {HX-22} {HY+38} Z" fill="#7A1E2A" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')
o.append(f'<path d="M {HX-16} {HY+39} l 4 12 l 4 -12 Z M {HX+16} {HY+39} l -4 12 l -4 -12 Z" fill="#FFFFFF" stroke="{INK}" stroke-width="2"/>')
o.append(f'<path d="M {HX-10} {HY+56} C {HX-4} {HY+50}, {HX+4} {HY+50}, {HX+10} {HY+56}" fill="none" stroke="#E86F8A" stroke-width="5" stroke-linecap="round"/>')
o.append(f'<g stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" opacity="0.95">'
         f'<path d="M {HX-30} {HY+30} L {HX-104} {HY+18} M {HX-30} {HY+38} L {HX-106} {HY+42} M {HX+30} {HY+30} L {HX+104} {HY+18} M {HX+30} {HY+38} L {HX+106} {HY+42}"/></g>')
o.append('</g>')
o.append('</g>')

# indicador de tamaño
o.append('<g id="grande">' + arrow("gup", [(890, 470), (890, 230)], col=LIME, w=12, head_len=34)
         + '</g>')
o.append(tag("lerizado", 420, 92, tw("PELO ERIZADO"), "PELO ERIZADO", 520, 150, 520, 205))
o.append(tag("lgrande", 700, 120, tw("¡MÁS GRANDE!"), "¡MÁS GRANDE!", bg=LIME, fg=INK))
if FREE:
    o.append('</g>')
o.append('</svg>')
print("\n".join(o))

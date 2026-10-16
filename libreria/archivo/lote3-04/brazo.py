import math, random, sys
sys.path.insert(0, sys.path[0])
from common import *

random.seed(7)
P0, P1, HW = (-80, 600), (1080, 380), 118
L = math.hypot(P1[0] - P0[0], P1[1] - P0[1])
ux, uy = (P1[0] - P0[0]) / L, (P1[1] - P0[1]) / L
nx, ny = -uy, ux  # normal hacia abajo
ANG = math.degrees(math.atan2(uy, ux))


def A(t, s):
    return (P0[0] + ux * L * t + nx * HW * s, P0[1] + uy * L * t + ny * HW * s)


defs = f'''
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#BFE0FA"/><stop offset="1" stop-color="#EAF5FF"/></linearGradient>
<linearGradient id="skin" x1="{A(0.5,-1)[0]:.0f}" y1="{A(0.5,-1)[1]:.0f}" x2="{A(0.5,1)[0]:.0f}" y2="{A(0.5,1)[1]:.0f}" gradientUnits="userSpaceOnUse">
<stop offset="0" stop-color="#F7CFB2"/><stop offset="0.45" stop-color="#EDB08C"/><stop offset="1" stop-color="#C98462"/></linearGradient>
<radialGradient id="bump" cx="0.4" cy="0.35" r="0.7"><stop offset="0" stop-color="#FFE3D0"/><stop offset="0.6" stop-color="#F2B996"/><stop offset="1" stop-color="#D9906C"/></radialGradient>
<radialGradient id="glass" cx="0.35" cy="0.3" r="0.8"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#E3F3FF"/></radialGradient>
<linearGradient id="wood" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#C98B55"/><stop offset="1" stop-color="#7A4A26"/></linearGradient>
<linearGradient id="skin2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F4C3A3"/><stop offset="1" stop-color="#D08A66"/></linearGradient>
<linearGradient id="wool" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F0645A"/><stop offset="1" stop-color="#A82A22"/></linearGradient>
<clipPath id="lensclip"><circle cx="690" cy="178" r="118"/></clipPath>
'''
FULL = len(sys.argv) > 1 and sys.argv[1] == "full"
if FULL:
    o = [head(defs).replace('viewBox="0 0 1000 700"', 'viewBox="0 0 1080 1920"')]
    o.append('<rect width="1080" height="1920" fill="url(#sky)"/>')
    o.append('<g fill="#FFFFFF" opacity="0.5">' + "".join(f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x, y, r in [(150, 300, 60), (820, 220, 44), (500, 380, 30), (240, 1500, 50), (880, 1380, 70), (600, 1700, 40)]) + '</g>')
    o.append('__EXTRA__')
    o.append('<g transform="translate(-85 430) scale(1.25)">')
else:
    o = [head(defs)]
    o.append('<rect width="1000" height="700" fill="url(#sky)"/>')
# bokeh lejano (sin contorno)
o.append('<g fill="#FFFFFF" opacity="0.5">' + "".join(f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x, y, r in
         [(120, 140, 40), (260, 260, 26), (470, 110, 34), (940, 300, 30), (380, 300, 18), (880, 440, 24), (560, 260, 20)]) + '</g>')


def flake(cx, cy, r, rotd=0):
    arms = []
    for k in range(6):
        a = math.radians(k * 60 + rotd)
        ex, ey = cx + r * math.cos(a), cy + r * math.sin(a)
        arms.append(f"M {cx} {cy} L {ex:.1f} {ey:.1f}")
        for f in (0.55,):
            bx, by = cx + r * f * math.cos(a), cy + r * f * math.sin(a)
            for sgn in (-1, 1):
                b2 = a + sgn * math.radians(45)
                arms.append(f"M {bx:.1f} {by:.1f} L {bx + r*0.35*math.cos(b2):.1f} {by + r*0.35*math.sin(b2):.1f}")
    d = " ".join(arms)
    return (f'<path d="{d}" fill="none" stroke="#5E9BD1" stroke-width="{r*0.26+5:.1f}" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="#FFFFFF" stroke-width="{r*0.26:.1f}" stroke-linecap="round"/>')


o.append('<g id="snow1">' + flake(120, 250, 26, 10) + flake(300, 150, 20, 0) + flake(450, 300, 16, 20) + '</g>')
o.append('<g id="snow2">' + flake(210, 370, 18, 5) + flake(400, 200, 28, 15) + flake(520, 390, 12, 0) + '</g>')
# notas musicales
def note(x, y, s, dbl=False):
    g = f'<g transform="translate({x} {y}) scale({s}) rotate(-12)">'
    if dbl:
        g += (f'<path d="M 18 -60 L 58 -70 L 58 -56 L 18 -46 Z" fill="{INK}"/><line x1="18" y1="-58" x2="18" y2="0" stroke="{INK}" stroke-width="7"/>'
              f'<line x1="58" y1="-68" x2="58" y2="-10" stroke="{INK}" stroke-width="7"/>'
              f'<ellipse cx="6" cy="2" rx="15" ry="11" fill="{INK}" transform="rotate(-20 6 2)"/><ellipse cx="46" cy="-8" rx="15" ry="11" fill="{INK}" transform="rotate(-20 46 -8)"/>'
              f'<ellipse cx="2" cy="-1" rx="5" ry="3" fill="#FFFFFF" opacity="0.7"/>')
    else:
        g += (f'<line x1="18" y1="-62" x2="18" y2="0" stroke="{INK}" stroke-width="7"/>'
              f'<path d="M 18 -62 C 30 -50, 44 -46, 38 -26" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
              f'<ellipse cx="6" cy="2" rx="15" ry="11" fill="{INK}" transform="rotate(-20 6 2)"/>')
    return g + '</g>'


o.append('<g id="notes">' + note(845, 115, 1.0, True) + note(880, 235, 0.8) + note(560, 80, 0.75) + '</g>')

# antebrazo
top = [A(t / 20, -1) for t in range(21)]
bot = [A(t / 20, 1) for t in range(20, -1, -1)]
d = poly(top) + " L " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in bot) + " Z"
o.append(f'<ellipse cx="{A(0.75,1.25)[0]:.0f}" cy="{A(0.75,1.25)[1]:.0f}" rx="260" ry="22" fill="#6E8FB0" opacity="0.25" transform="rotate({ANG:.1f} {A(0.75,1.25)[0]:.0f} {A(0.75,1.25)[1]:.0f})"/>')
o.append(f'<path d="{d}" fill="url(#skin)"/>')
# venas suaves y pliegues
o.append(f'<path d="M {A(0.08,0.15)[0]:.0f} {A(0.08,0.15)[1]:.0f} C {A(0.3,0.0)[0]:.0f} {A(0.3,0.0)[1]:.0f}, {A(0.45,0.35)[0]:.0f} {A(0.45,0.35)[1]:.0f}, {A(0.7,0.2)[0]:.0f} {A(0.7,0.2)[1]:.0f}" fill="none" stroke="#B9A0C8" stroke-width="7" opacity="0.35" stroke-linecap="round"/>')
o.append(poly(top).join([f'<path d="', f'" fill="none" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>']))
o.append(poly([A(t / 20, -0.86) for t in range(21)]).join([f'<path d="', f'" fill="none" stroke="#FFE6D6" stroke-width="5" opacity="0.8"/>']))
o.append(poly([A(t / 20, 1) for t in range(21)]).join([f'<path d="', f'" fill="none" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>']))

# pelos y bultos
pts = []
for i in range(26):
    for j in range(5):
        t = (i + 0.5 + (j % 2) * 0.5) / 26 + random.uniform(-0.008, 0.008)
        s = -0.72 + j * 0.36 + random.uniform(-0.08, 0.08)
        x, y = A(t, s)
        if -20 < x < 1020 and y < 690 and t > 0.19:
            pts.append((x, y, s))
o.append('<g id="bumps">')
for x, y, s in pts:
    o.append(f'<ellipse cx="{x+2:.1f}" cy="{y+3:.1f}" rx="13" ry="9" fill="#B87452" opacity="0.35"/>'
             f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="12" ry="9" fill="url(#bump)" stroke="#C07A58" stroke-width="2"/>'
             f'<ellipse cx="{x-4:.1f}" cy="{y-3:.1f}" rx="4" ry="2.5" fill="#FFFFFF" opacity="0.7"/>')
o.append('</g>')


def hairs(gid, ang_off, ln):
    g = [f'<g id="{gid}" stroke-linecap="round">']
    for x, y, s in pts:
        a = math.radians(ANG + ang_off + random.uniform(-6, 6))
        ex, ey = x + ln * math.cos(a), y + ln * math.sin(a)
        g.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="#3B271B" stroke-width="3.2"/>')
    g.append('</g>')
    return "".join(g)


random.seed(11)
o.append(hairs("hairflat", -4, 30))
o.append(hairs("hairup", -62, 30))

# manga de jersey (lana roja) para que se lea como un brazo abrigado
def band(t0, t1, k):
    return poly([A(t0, -k), A(t1, -k), A(t1, k), A(t0, k)]) + " Z"
o.append(f'<path d="{band(-0.05, 0.16, 1.16)}" fill="url(#wool)" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>')
o.append('<g stroke="#8E1F1A" stroke-width="5" fill="none" opacity="0.7">' + "".join(
    f'<path d="M {A(t,-0.8)[0]:.1f} {A(t,-0.8)[1]:.1f} Q {A(t+0.012,0)[0]:.1f} {A(t+0.012,0)[1]:.1f} {A(t,0.8)[0]:.1f} {A(t,0.8)[1]:.1f}"/>' for t in (0.01, 0.045, 0.08)) + '</g>')
o.append(f'<path d="{band(0.115, 0.175, 1.2)}" fill="url(#wool)" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>')
o.append('<g stroke="#8E1F1A" stroke-width="4">' + "".join(
    f'<line x1="{A(0.115,s_)[0]+ux*4:.1f}" y1="{A(0.115,s_)[1]+uy*4:.1f}" x2="{A(0.175,s_)[0]-ux*4:.1f}" y2="{A(0.175,s_)[1]-uy*4:.1f}"/>' for s_ in [x/10 for x in range(-10, 11, 2)]) + '</g>')
o.append(poly([A(0.0, -1.0), A(0.11, -1.0)]).join(['<path d="', '" stroke="#FF9C8A" stroke-width="5" opacity="0.7" fill="none"/>']))

# punto examinado + lupa
spot = A(0.66, -0.25)
o.append(f'<g id="lupa">')
o.append(f'<circle cx="{spot[0]:.0f}" cy="{spot[1]:.0f}" r="34" fill="none" stroke="{INK}" stroke-width="5" stroke-dasharray="10 8"/>')
for sgn in (-1, 1):
    o.append(f'<line x1="{spot[0]+sgn*30:.0f}" y1="{spot[1]-14:.0f}" x2="{690+sgn*112:.0f}" y2="{178+40:.0f}" stroke="{INK}" stroke-width="4" stroke-dasharray="10 8" opacity="0.7"/>')
o.append(stroke2("M 778 262 L 856 340", 26, "url(#wood)", 8, cap="round"))
o.append(f'<circle cx="690" cy="178" r="118" fill="url(#glass)"/>')
# dentro de la lupa: perfil de piel con bultos y pelos de punta
inner = ['<g clip-path="url(#lensclip)">']
sy = 225
prof = f"M 560 {sy} "
domes = [(600, 30), (690, 34), (780, 30)]
x = 560
for cx, w in domes:
    prof += f"L {cx-w*1.3} {sy} C {cx-w*0.8} {sy}, {cx-w*0.7} {sy-24}, {cx} {sy-24} C {cx+w*0.7} {sy-24}, {cx+w*0.8} {sy}, {cx+w*1.3} {sy} "
prof += f"L 820 {sy}"
inner.append(f'<path d="{prof} L 820 320 L 560 320 Z" fill="url(#skin2)"/>')
inner.append(f'<path d="{prof}" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>')
inner.append(f'<path d="{prof}" fill="none" stroke="#FFE3D0" stroke-width="3" transform="translate(0 7)" opacity="0.8"/>')
for cx, w in domes:
    inner.append(stroke2(f"M {cx} {sy-24} L {cx+12} {sy-100}", 5, "#3B271B", 5))
    inner.append(f'<g opacity="0.35" stroke="#8A4E33" stroke-width="5" stroke-linecap="round"><line x1="{cx}" y1="{sy-16}" x2="{cx-8}" y2="{sy+40}"/></g>')
inner.append('</g>')
o.extend(inner)
o.append(f'<path d="M 612 120 A 98 98 0 0 1 700 82" fill="none" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round" opacity="0.9"/>')
o.append(f'<circle cx="690" cy="178" r="118" fill="none" stroke="{INK}" stroke-width="9"/>')
o.append(f'<circle cx="690" cy="178" r="108" fill="none" stroke="#9FB4C8" stroke-width="5"/>')
o.append('</g>')

lx, ly = A(0.48, -0.45)
o.append(tag("lgallina", 300, 306, tw("PIEL DE GALLINA"), "PIEL DE GALLINA", 470, 364, f"{lx:.0f}", f"{ly:.0f}"))
if FULL:
    o.append('</g>')
    ex = '<g id="snowtop">' + flake(140, 200, 30, 5) + flake(420, 140, 22, 12) + flake(700, 330, 26, 0) + flake(960, 150, 20, 8) + '</g>'
    ex += '<g id="snowbot">' + flake(160, 1480, 26, 3) + flake(520, 1380, 20, 10) + flake(820, 1560, 30, 0) + flake(380, 1700, 18, 5) + '</g>'
    o[o.index('__EXTRA__')] = ex
o.append('</svg>')
print("\n".join(o))

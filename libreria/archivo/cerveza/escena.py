"""Escena general: el culo de una botella golpea la boca de otra y la espuma entra en erupción."""
import math, random, sys
sys.path.insert(0, ".")
from lib import *

TABLE = 600
B = Bottle(600, 640, 340, 124)
A = Bottle(0, 0, 340, 124)
TILT = -42
# esquina inferior derecha de A (w, 0) sobre la esquina izquierda del labio de B
lip_x, lip_y = B.cx - B.nw - 6, B.top + 2
ca, sa = math.cos(math.radians(TILT)), math.sin(math.radians(TILT))
cx_, cy_ = A.w * ca, A.w * sa
PX, PY = lip_x - cx_ + 4, lip_y - cy_ - 2

o = [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 700">
<defs>
{BOTTLE_DEFS}
<linearGradient id="wallg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFF4E2"/><stop offset="1" stop-color="#F3DFC2"/></linearGradient>
<linearGradient id="wood" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#C98A52"/><stop offset="1" stop-color="#8E5A30"/></linearGradient>
<linearGradient id="woodtop" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E2A86C"/><stop offset="1" stop-color="#C98A52"/></linearGradient>
<radialGradient id="light" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0.8"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient>
<radialGradient id="puddle" cx="0.5" cy="0.4" r="0.6"><stop offset="0" stop-color="#FFF8E8"/><stop offset="1" stop-color="#E8C88A"/></radialGradient>
</defs>
<rect width="1000" height="700" fill="url(#wallg)"/>''']
# azulejos suaves y ventana con luz (fondo, sin contorno)
o.append('<g stroke="#EAD3B2" stroke-width="3">' + "".join(f'<line x1="0" y1="{y}" x2="1000" y2="{y}"/>' for y in range(80, TABLE, 90)) +
         "".join(f'<line x1="{x + (45 if (y // 90) % 2 else 0)}" y1="{y}" x2="{x + (45 if (y // 90) % 2 else 0)}" y2="{y + 90}"/>' for y in range(-10, TABLE, 90) for x in range(0, 1000, 180)) + '</g>')
o.append('<rect x="60" y="70" width="250" height="300" rx="14" fill="#DCEEFF"/><rect x="60" y="70" width="250" height="300" rx="14" fill="none" stroke="#E7D2B0" stroke-width="12"/>'
         '<line x1="185" y1="70" x2="185" y2="370" stroke="#E7D2B0" stroke-width="10"/><line x1="60" y1="220" x2="310" y2="220" stroke="#E7D2B0" stroke-width="10"/>'
         '<path d="M 90 100 L 150 100 L 100 190 Z" fill="#FFFFFF" opacity="0.6"/>')
o.append('<ellipse cx="200" cy="300" rx="260" ry="200" fill="url(#light)"/>')
# estante con maceta lejana
o.append('<rect x="760" y="210" width="210" height="14" fill="#E2C49A"/><path d="M 820 210 L 830 160 L 880 160 L 890 210 Z" fill="#E9B08A"/>'
         '<g fill="#A8D5A0"><ellipse cx="840" cy="140" rx="16" ry="30" transform="rotate(-25 840 140)"/><ellipse cx="858" cy="128" rx="14" ry="34"/><ellipse cx="876" cy="142" rx="16" ry="28" transform="rotate(28 876 142)"/></g>')
# mesa
o.append(f'<rect x="-10" y="{TABLE}" width="1020" height="40" fill="url(#woodtop)"/>')
o.append(f'<rect x="-10" y="{TABLE + 40}" width="1020" height="80" fill="url(#wood)" stroke="{INK}" stroke-width="7"/>')
o.append(f'<line x1="-10" y1="{TABLE}" x2="1010" y2="{TABLE}" stroke="{INK}" stroke-width="5"/>')
o.append(f'<line x1="-10" y1="{TABLE + 46}" x2="1010" y2="{TABLE + 46}" stroke="#E8B47E" stroke-width="3" opacity="0.8"/>')
o.append('<g fill="none" stroke="#A86E3C" stroke-width="3" opacity="0.6"><path d="M 40 612 q 120 -6 240 2 t 240 -2"/><path d="M 560 626 q 140 6 300 -2"/><path d="M 120 664 q 160 -8 320 2 t 300 0"/><path d="M 50 690 q 200 6 420 -2"/></g>')
# sombras
o.append(f'<ellipse cx="{B.cx + 26}" cy="{B.base + 2}" rx="{B.w + 30}" ry="12" fill="#5A3416" opacity="0.35"/>')
# chapa suelta sobre la mesa
o.append(f'<g id="chapa"><ellipse cx="826" cy="628" rx="30" ry="9" fill="#5A3416" opacity="0.35"/>'
         f'<path d="M 796 616 L 800 626 L 806 618 L 812 628 L 818 619 L 824 629 L 830 619 L 836 628 L 842 618 L 848 626 L 852 616 Q 852 604 824 604 Q 796 604 796 616 Z" fill="url(#cap)" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
         f'<ellipse cx="824" cy="609" rx="20" ry="4" fill="#FFFFFF" opacity="0.8"/></g>')
# botella de abajo (abierta)
o.append(f'<g id="botb">{B.draw(cap=False)}')
o.append(f'<ellipse cx="{B.cx}" cy="{B.top + 1}" rx="{B.nw - 2:.1f}" ry="5" fill="#3A1A06" stroke="{INK}" stroke-width="3"/>')
o.append('</g>')

# espuma en erupción (oculta hasta su momento)
random.seed(5)
col = []
y = B.top - 6
while y > 70:
    t = (B.top - y) / (B.top - 70)
    spread = 18 + 70 * t ** 1.4
    for k in range(3):
        col.append((B.cx + random.uniform(-spread, spread) * (0.5 + 0.5 * k / 2), y - random.uniform(0, 10)))
    y -= 20
cap_pts = [(B.cx + 95 * math.cos(a), 110 + 34 * math.sin(a)) for a in [i / 16 * 2 * math.pi for i in range(16)]]
o.append('<g id="foam">')
# chorreones por el cuello y el cuerpo
for sx, ln in ((-1, 210), (1, 160)):
    x0 = B.cx + sx * (B.nw + 2)
    d = f"M {x0} {B.top + 4} C {x0 + sx * 6} {B.top + 60}, {B.cx + sx * (B.w - 4)} {B.yn + 40}, {B.cx + sx * (B.w + 2)} {B.top + ln}"
    o.append(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="24" stroke-linecap="round"/><path d="{d}" fill="none" stroke="#FFF6E0" stroke-width="13" stroke-linecap="round"/>')
o.append(foam_blob(col + cap_pts, 24, seed=6))
o.append('</g>')
o.append(f'<g id="drops">' + "".join(
    f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFF6E0" stroke="{INK}" stroke-width="4"/>' for x, y, r in ((470, 120, 10), (450, 180, 7), (735, 96, 9), (760, 160, 7), (700, 60, 6))) + '</g>')
o.append(f'<g id="puddle"><ellipse cx="{B.cx + 40}" cy="{B.base + 4}" rx="{B.w + 70}" ry="16" fill="url(#puddle)" stroke="{INK}" stroke-width="5"/>'
         f'<ellipse cx="{B.cx + 10}" cy="{B.base}" rx="40" ry="4" fill="#FFFFFF"/></g>')

# botella que golpea (inclinada, con chapa)
o.append(f'<g id="bota"><g transform="translate({PX:.1f} {PY:.1f}) rotate({TILT})">{A.draw(cap=True)}</g></g>')
# golpe
ix, iy = lip_x + 6, lip_y - 6
star = []
for i in range(16):
    a = i / 16 * 2 * math.pi
    r = 46 if i % 2 == 0 else 20
    star.append((ix + r * math.cos(a), iy + r * math.sin(a)))
o.append(f'<g id="impact"><path d="{P(star)} Z" fill="{LIME}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
         + "".join(f'<line x1="{ix + 58 * math.cos(a):.1f}" y1="{iy + 58 * math.sin(a):.1f}" x2="{ix + 84 * math.cos(a):.1f}" y2="{iy + 84 * math.sin(a):.1f}" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
                   for a in (math.radians(d) for d in (-150, -100, -40, 10, 40))) + '</g>')
# ondas del golpe
o.append(''.join(f'<g id="ring{k}"><circle cx="{ix}" cy="{iy}" r="70" fill="none" stroke="{LIME}" stroke-width="6"/></g>' for k in (1, 2)))
o.append(tag("lgolpe", 770, 390, "¡CLINC!", ix + 30, iy + 20, bg="#FFFFFF", fg=INK))
o.append('</svg>')
print("\n".join(o))

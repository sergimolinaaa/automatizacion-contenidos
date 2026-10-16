"""Panel 1000x700: cabeza de perfil con el cerebro al descubierto, hipotálamo y termostato (37 -> 39), cascos y dopamina."""
import math, random, sys
sys.path.insert(0, sys.path[0])
from common import *

random.seed(5)
defs = '''
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#DCEBFA"/><stop offset="1" stop-color="#F4F8FD"/></linearGradient>
<linearGradient id="skin" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F7CFB2"/><stop offset="0.6" stop-color="#EDB08C"/><stop offset="1" stop-color="#C98462"/></linearGradient>
<radialGradient id="brain" cx="0.45" cy="0.35" r="0.75"><stop offset="0" stop-color="#FFD3DA"/><stop offset="0.65" stop-color="#F3A2AF"/><stop offset="1" stop-color="#D9788A"/></radialGradient>
<radialGradient id="cereb" cx="0.4" cy="0.3" r="0.8"><stop offset="0" stop-color="#F7B9C3"/><stop offset="1" stop-color="#C9677A"/></radialGradient>
<radialGradient id="hglow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#FFE15A" stop-opacity="0.95"/><stop offset="1" stop-color="#FF5A36" stop-opacity="0"/></radialGradient>
<radialGradient id="hyp" cx="0.4" cy="0.35" r="0.7"><stop offset="0" stop-color="#FFB199"/><stop offset="1" stop-color="#FF5A36"/></radialGradient>
<radialGradient id="dial" cx="0.4" cy="0.3" r="0.8"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#DDE5EE"/></radialGradient>
<linearGradient id="metal" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#B9C3CF"/><stop offset="1" stop-color="#6E7B8B"/></linearGradient>
<linearGradient id="phone" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4A4E63"/><stop offset="1" stop-color="#1D1F2C"/></linearGradient>
<radialGradient id="virus" cx="0.4" cy="0.35" r="0.7"><stop offset="0" stop-color="#C6F2A0"/><stop offset="1" stop-color="#5DA83A"/></radialGradient>
'''
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 700">\n<defs>{defs}</defs>']
o.append('<rect width="1000" height="700" fill="url(#bg)"/>')
o.append('<g fill="#FFFFFF" opacity="0.6">' + "".join(f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x, y, r in
         [(90, 520, 40), (960, 520, 30), (720, 620, 24), (560, 40, 26), (120, 160, 22)]) + '</g>')

# cabeza de perfil (mira a la derecha)
head = [(300, 720), (292, 600), (250, 520), (208, 430), (205, 320), (240, 205), (320, 120), (430, 88), (535, 105),
        (610, 165), (648, 245), (658, 300), (668, 335), (664, 362), (676, 400), (712, 448), (700, 466), (680, 472),
        (690, 500), (684, 520), (690, 538), (676, 572), (640, 598), (582, 604), (534, 600), (522, 720)]
d = smooth(head) if 'smooth' in globals() else poly(head)
o.append(f'<ellipse cx="460" cy="660" rx="260" ry="26" fill="#6E8FB0" opacity="0.18"/>')
o.append(f'<path d="{d} Z" fill="url(#skin)" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>')
# ojo, ceja, mejilla
o.append(f'<path d="M 598 336 Q 616 326 634 336" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>')
o.append(f'<ellipse cx="620" cy="350" rx="9" ry="11" fill="{INK}"/><circle cx="617" cy="346" r="3" fill="#FFFFFF"/>')
o.append(f'<path d="M 590 310 Q 615 298 640 306" fill="none" stroke="#6B4632" stroke-width="8" stroke-linecap="round"/>')
o.append('<ellipse cx="600" cy="420" rx="34" ry="20" fill="#E8897A" opacity="0.35"/>')
o.append(f'<path d="M 672 532 Q 660 538 648 534" fill="none" stroke="#9C4D3E" stroke-width="5" stroke-linecap="round"/>')
# oreja
# cerebro (corte)
o.append('<g id="cerebro">')
bd = smooth([(250, 300), (270, 210), (340, 150), (440, 128), (540, 150), (600, 215), (612, 290), (580, 345), (500, 370),
             (420, 368), (330, 360), (268, 340)], closed=True)
o.append(f'<path d="{bd}" fill="url(#brain)" stroke="{INK}" stroke-width="7"/>')
gy = ["M 300 230 C 330 200, 360 240, 390 210 S 440 190, 460 220", "M 280 290 C 320 270, 340 310, 380 280 S 430 260, 470 290",
      "M 480 180 C 510 200, 540 170, 570 205", "M 500 250 C 530 230, 560 270, 590 250", "M 360 160 C 380 180, 410 160, 430 175",
      "M 330 330 C 360 315, 390 345, 420 325", "M 520 310 C 545 295, 560 320, 585 300"]
for g in gy:
    o.append(f'<path d="{g}" fill="none" stroke="#B85568" stroke-width="6" stroke-linecap="round"/>')
o.append('<path d="M 300 190 C 360 140, 460 125, 540 150" fill="none" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round" opacity="0.7"/>')
# cerebelo y tronco
o.append(f'<path d="{smooth([(270, 352), (320, 362), (370, 380), (360, 420), (310, 428), (272, 400)], closed=True)}" fill="url(#cereb)" stroke="{INK}" stroke-width="6"/>')
for k in range(3):
    o.append(f'<path d="M {285+k*6} {378+k*13} Q 320 {372+k*14} {355-k*4} {388+k*12}" fill="none" stroke="#A84D60" stroke-width="4" stroke-linecap="round"/>')
o.append(f'<path d="M 410 362 C 400 420, 410 480, 405 560 L 455 560 C 452 480, 470 420, 470 365 Z" fill="#E996A4" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
o.append('</g>')
# hipotálamo
o.append('<g id="hipo">')
o.append('<circle cx="482" cy="352" r="48" fill="url(#hglow)"/>')
o.append(f'<ellipse cx="482" cy="352" rx="20" ry="16" fill="url(#hyp)" stroke="{INK}" stroke-width="5"/>')
o.append('<ellipse cx="476" cy="346" rx="6" ry="4" fill="#FFFFFF" opacity="0.8"/>')
o.append('</g>')
# dopamina (núcleo accumbens / estriado): chispas lima
o.append('<g id="dopa">')
for i in range(14):
    a = random.uniform(0, 2 * math.pi); r = random.uniform(10, 70)
    x, y = 470 + r * math.cos(a) * 1.3, 270 + r * math.sin(a) * 0.8
    o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.choice([7, 9, 11])}" fill="{LIME}" stroke="{INK}" stroke-width="3"/>')
o.append('</g>')
# orden hacia el cuerpo (señal por la médula)
o.append(f'<g id="orden"><path d="M 482 372 C 455 420, 432 470, 430 640" fill="none" stroke="{INK}" stroke-width="16" stroke-linecap="round"/>'
         f'<path d="M 482 372 C 455 420, 432 470, 430 640" fill="none" stroke="#5BC0FF" stroke-width="9" stroke-linecap="round"/></g>')
# cascos (auriculares)
o.append('<g id="cascos">')
o.append(stroke2("M 300 400 C 250 230, 330 70, 450 64 C 560 60, 640 140, 640 250", 22, "url(#phone)", 8))
o.append(f'<rect x="318" y="356" width="80" height="128" rx="34" fill="url(#phone)" stroke="{INK}" stroke-width="7"/>')
o.append(f'<rect x="334" y="370" width="22" height="90" rx="10" fill="#FFFFFF" opacity="0.25"/>')
o.append('</g>')
# notas
def note(x, y, s):
    return (f'<g transform="translate({x} {y}) scale({s}) rotate(-12)"><line x1="18" y1="-62" x2="18" y2="0" stroke="{INK}" stroke-width="7"/>'
            f'<path d="M 18 -62 C 30 -50, 44 -46, 38 -26" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
            f'<ellipse cx="6" cy="2" rx="15" ry="11" fill="{INK}" transform="rotate(-20 6 2)"/></g>')
o.append('<g id="notas">' + note(150, 300, 1.1) + note(120, 470, 0.9) + note(200, 150, 0.8) + '</g>')
# virus / pirógenos (fiebre)
o.append('<g id="virus">')
for cx, cy, r in [(110, 560, 30), (190, 610, 22), (90, 420, 20)]:
    for k in range(8):
        a = math.radians(k * 45)
        o.append(f'<line x1="{cx + r*math.cos(a):.0f}" y1="{cy + r*math.sin(a):.0f}" x2="{cx + (r+12)*math.cos(a):.0f}" y2="{cy + (r+12)*math.sin(a):.0f}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
                 f'<circle cx="{cx + (r+13)*math.cos(a):.0f}" cy="{cy + (r+13)*math.sin(a):.0f}" r="5" fill="#9BDB6E" stroke="{INK}" stroke-width="3"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#virus)" stroke="{INK}" stroke-width="5"/>')
    o.append(f'<circle cx="{cx - r*0.35:.0f}" cy="{cy - r*0.35:.0f}" r="{r*0.2:.0f}" fill="#FFFFFF" opacity="0.7"/>')
o.append('</g>')

# termostato
CX, CY, R = 840, 235, 112
o.append(f'<g id="guia"><line x1="500" y1="345" x2="{CX - R*0.82:.0f}" y2="{CY + R*0.55:.0f}" stroke="{INK}" stroke-width="5" stroke-dasharray="12 9" stroke-linecap="round"/></g>')
o.append('<g id="termo">')
o.append(f'<circle cx="{CX+6}" cy="{CY+10}" r="{R}" fill="#2B4A6B" opacity="0.2"/>')
o.append(f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="url(#metal)" stroke="{INK}" stroke-width="8"/>')
o.append(f'<circle cx="{CX}" cy="{CY}" r="{R-16}" fill="url(#dial)" stroke="{INK}" stroke-width="4"/>')


def ang(t):  # 35..41 -> -135..135 grados desde arriba
    return math.radians(-135 + (t - 35) * 45)


# arco de colores frío->calor
for t0 in range(35, 41):
    a0, a1 = ang(t0), ang(t0 + 1)
    col = ["#3D8BFF", "#6FB7FF", "#9FD27A", "#FFC94A", "#FF8A3D", "#FF5A36"][t0 - 35]
    rr = R - 30
    x0, y0 = CX + rr * math.sin(a0), CY - rr * math.cos(a0)
    x1, y1 = CX + rr * math.sin(a1), CY - rr * math.cos(a1)
    o.append(f'<path d="M {x0:.1f} {y0:.1f} A {rr} {rr} 0 0 1 {x1:.1f} {y1:.1f}" fill="none" stroke="{col}" stroke-width="12"/>')
for t in range(35, 42):
    a = ang(t)
    x0, y0 = CX + (R - 40) * math.sin(a), CY - (R - 40) * math.cos(a)
    x1, y1 = CX + (R - 20) * math.sin(a), CY - (R - 20) * math.cos(a)
    o.append(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="{INK}" stroke-width="4"/>')
for t in (35, 37, 39, 41):
    a = ang(t)
    x, y = CX + (R - 58) * math.sin(a), CY - (R - 58) * math.cos(a)
    o.append(f'<text x="{x:.0f}" y="{y + 8:.0f}" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="22" fill="{INK}">{t}</text>')
o.append(f'<text x="{CX}" y="{CY + 70}" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="20" fill="#5B6478">°C</text>')
o.append(f'<path d="M {CX-70} {CY-58} A 90 90 0 0 1 {CX-10} {CY-90}" fill="none" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round" opacity="0.9"/>')
o.append('</g>')
# aguja (simétrica respecto al centro para girar con origin center)
a = ang(37)
tx, ty = CX + 40 * math.sin(a), CY - 40 * math.cos(a)
bx, by = CX - 16 * math.sin(a), CY + 16 * math.cos(a)
o.append(f'<g id="aguja"><circle cx="{CX}" cy="{CY}" r="42" fill="none"/>'
         + stroke2(f"M {bx:.1f} {by:.1f} L {tx:.1f} {ty:.1f}", 8, CORAL, 6) +
         f'<circle cx="{CX}" cy="{CY}" r="14" fill="{INK}"/><circle cx="{CX-3}" cy="{CY-3}" r="4" fill="#FFFFFF"/></g>')

# etiquetas
o.append(tag("lhipo", 60, 590, tw("HIPOTÁLAMO"), "HIPOTÁLAMO", 230, 590, 470, 362))
o.append(tag("l37", 760, 372, tw("37 °C"), "37 °C"))
o.append(tag("l39", 760, 372, tw("39 °C"), "39 °C", bg=CORAL, fg="#FFFFFF"))
o.append(tag("ldopa", 640, 70, tw("DOPAMINA"), "DOPAMINA", 680, 128, 520, 240))
o.append('</svg>')
print("\n".join(o))

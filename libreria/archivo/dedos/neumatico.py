import math, random, sys
sys.path.insert(0, sys.path[0])
from common import *

random.seed(5)
SY = 300  # superficie mojada (fila de arriba)
o = [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 700">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#EEF6FA"/><stop offset="1" stop-color="#DCEAF1"/></linearGradient>
<linearGradient id="road" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8E99A6"/><stop offset="1" stop-color="#6B7682"/></linearGradient>
<linearGradient id="tile" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#D6E3EA"/></linearGradient>
<linearGradient id="skin" gradientUnits="userSpaceOnUse" x1="0" y1="170" x2="0" y2="300"><stop offset="0" stop-color="#FBD3B8"/><stop offset="0.6" stop-color="#F3B897"/><stop offset="1" stop-color="#DE9573"/></linearGradient>
<radialGradient id="tyre" cx="0.4" cy="0.35" r="0.75"><stop offset="0" stop-color="#4A4D57"/><stop offset="1" stop-color="#16171C"/></radialGradient>
<radialGradient id="rim" cx="0.4" cy="0.35" r="0.7"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#9AA7B4"/></radialGradient>
<linearGradient id="glass" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#D9F0FF"/><stop offset="1" stop-color="#9FD4F7"/></linearGradient>
<radialGradient id="pad" cx="0.45" cy="0.4" r="0.7"><stop offset="0" stop-color="#FCDCC7"/><stop offset="1" stop-color="#EDA987"/></radialGradient>
</defs>
<rect width="1000" height="700" fill="url(#bg)"/>''']
# ---- fila de arriba: superficies ----
o.append(f'<rect x="0" y="{SY}" width="500" height="34" fill="url(#tile)"/>')
o.append(f'<rect x="500" y="{SY}" width="500" height="34" fill="url(#road)"/>')
o.append(f'<path d="M 0 {SY} L 1000 {SY}" stroke="{INK}" stroke-width="6"/>')
o.append(f'<path d="M 0 {SY + 34} L 1000 {SY + 34}" stroke="{INK}" stroke-width="4" opacity="0.5"/>')
# pelicula de agua
o.append(f'<g fill="#8FD3FF" stroke="{INK}" stroke-width="3"><path d="M 20 {SY} C 40 {SY - 9}, 120 {SY - 9}, 150 {SY} Z"/><path d="M 470 {SY} C 500 {SY - 10}, 580 {SY - 10}, 600 {SY} Z"/><path d="M 900 {SY} C 920 {SY - 9}, 970 {SY - 9}, 990 {SY} Z"/></g>')

# DEDO de lado, yema apoyada
fd = (f"M -30 172 L 300 168 C 370 166, 430 196, 438 246 C 444 284, 420 {SY - 2}, 380 {SY - 2} "
      f"L 140 {SY - 2} C 80 {SY - 2}, 20 290, -30 286 Z")
o.append(f'<ellipse cx="260" cy="{SY + 6}" rx="190" ry="8" fill="{INK}" opacity="0.2"/>')
o.append('<g id="finger">')
o.append(f'<path d="{fd}" fill="url(#skin)" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>')
# uña (dorso)
o.append(f'<path d="M 300 170 C 350 166, 400 180, 418 210 C 380 196, 340 192, 300 194 Z" fill="#F8E2D6" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
o.append('<path d="M 320 178 C 350 176, 380 182, 398 194" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>')
o.append('<path d="M 20 186 L 280 182" stroke="#FFEADB" stroke-width="6" stroke-linecap="round" opacity="0.9"/>')
# pliegue de la articulacion
o.append('<path d="M 196 176 Q 190 230 200 292" fill="none" stroke="#C97B5C" stroke-width="4" stroke-linecap="round"/>')
# yema arrugada: bultitos en el borde inferior
o.append('<g id="bumps" fill="none" stroke="#A9573F" stroke-width="3.5" stroke-linecap="round">')
for x in range(232, 420, 26):
    o.append(f'<path d="M {x} {SY - 10} Q {x + 6} {SY - 30} {x + 2} {SY - 48}"/>')
o.append('</g></g>')
# gotas que salen despedidas
o.append('<g id="squirt">')
for (x, y, r, a) in [(462, 268, 10, 30), (492, 240, 7, 40), (520, 270, 6, 55)]:
    o.append(f'<g transform="rotate({a} {x} {y})"><path d="M {x} {y - r * 1.8} C {x + r} {y - r * 0.4}, {x + r} {y + r}, {x} {y + r} C {x - r} {y + r}, {x - r} {y - r * 0.4}, {x} {y - r * 1.8} Z" fill="#8FD3FF" stroke="{INK}" stroke-width="3.5"/></g>')
o.append('</g>')

# NEUMATICO de lado
TX, TY, TR = 770, 180, 118
o.append(f'<ellipse cx="{TX}" cy="{SY + 6}" rx="130" ry="9" fill="{INK}" opacity="0.25"/>')
o.append('<g id="tire">')
o.append(f'<circle cx="{TX}" cy="{TY}" r="{TR}" fill="url(#tyre)" stroke="{INK}" stroke-width="8"/>')
for k in range(24):
    a = k * 15
    x1, y1 = rot(0, -TR + 4, a, TX, TY)
    x2, y2 = rot(0, -TR + 20, a, TX, TY)
    o.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#5A5E69" stroke-width="7" stroke-linecap="round"/>')
o.append(f'<circle cx="{TX}" cy="{TY}" r="72" fill="url(#rim)" stroke="{INK}" stroke-width="6"/>')
for k in range(5):
    a = k * 72
    x1, y1 = rot(0, -22, a, TX, TY)
    x2, y2 = rot(0, -62, a, TX, TY)
    o.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#7D8A97" stroke-width="16" stroke-linecap="round"/>')
o.append(f'<circle cx="{TX}" cy="{TY}" r="22" fill="#C9D3DC" stroke="{INK}" stroke-width="5"/>')
for k in range(5):
    x, y = rot(0, -12, k * 72 + 36, TX, TY)
    o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="{INK}"/>')
o.append('</g>')
o.append(f'<path d="M {TX - 64} {TY - 70} A 96 96 0 0 1 {TX + 40} {TY - 88}" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity="0.5"/>')
# rociada detras de la rueda
o.append('<g id="spray" fill="#8FD3FF" stroke="{INK}" stroke-width="3">'.replace("{INK}", INK))
for x, y, r in [(904, 270, 10), (930, 240, 8), (950, 280, 7), (920, 210, 6), (958, 230, 5)]:
    o.append(f'<circle cx="{x}" cy="{y}" r="{r}"/>')
o.append('</g>')

# ---- fila de abajo: huellas vistas desde abajo ----
FY0, FY1 = 360, 640
o.append(f'<rect x="40" y="{FY0}" width="420" height="{FY1 - FY0}" rx="30" fill="url(#glass)" stroke="{INK}" stroke-width="6"/>')
o.append(f'<rect x="540" y="{FY0}" width="420" height="{FY1 - FY0}" rx="30" fill="#7D8792" stroke="{INK}" stroke-width="6"/>')
# brillos de agua en los marcos
o.append('<g fill="#FFFFFF" opacity="0.35"><path d="M 70 380 L 120 380 L 80 620 L 60 620 Z"/></g>')
o.append('<g fill="#8FD3FF" opacity="0.55"><ellipse cx="600" cy="400" rx="30" ry="9"/><ellipse cx="910" cy="610" rx="34" ry="9"/><ellipse cx="900" cy="410" rx="22" ry="7"/></g>')

# huella del dedo
PX, PY, PA, PB = 250, 500, 160, 108
o.append(f'<ellipse cx="{PX}" cy="{PY}" rx="{PA + 14}" ry="{PB + 14}" fill="#8FD3FF" opacity="0.6"/>')
o.append(f'<ellipse cx="{PX}" cy="{PY}" rx="{PA}" ry="{PB}" fill="url(#pad)" stroke="{INK}" stroke-width="6"/>')
o.append('<g id="ridges" fill="none" stroke="#E7A487" stroke-width="3" opacity="0.8">'
         + "".join(f'<ellipse cx="{PX}" cy="{PY + 10}" rx="{PA * f:.0f}" ry="{PB * f:.0f}"/>' for f in (0.25, 0.45, 0.65, 0.82)) + '</g>')
# surcos-canales (agua) desde el centro hacia fuera
o.append('<g id="channels" fill="none" stroke-linecap="round">')
ch_ends = []
for k, a in enumerate([-160, -120, -60, -20, 20, 70, 115, 160]):
    ar = math.radians(a)
    x0, y0 = PX + 0.25 * PA * math.cos(ar), PY + 0.25 * PB * math.sin(ar)
    x1, y1 = PX + 1.0 * PA * math.cos(ar), PY + 1.0 * PB * math.sin(ar)
    d = wavy(x0, y0, x1, y1, 5, 2, 20)
    o.append(f'<path d="{d}" stroke="{INK}" stroke-width="15"/>')
    o.append(f'<path d="{d}" stroke="#4FA8EE" stroke-width="8"/>')
    ch_ends.append((x1, y1, ar))
o.append('</g>')
o.append('<g id="outl">')
for x1, y1, ar in ch_ends:
    x2, y2 = x1 + 44 * math.cos(ar), y1 + 34 * math.sin(ar)
    o.append(arrow(f"o{int(x1)}", [(round(x1 + 10 * math.cos(ar), 1), round(y1 + 8 * math.sin(ar), 1)), (round(x2, 1), round(y2, 1))], "#FFFFFF", 6, 16))
o.append('</g>')

# huella del neumatico
NX0, NY0, NW, NH = 600, 395, 300, 210
o.append(f'<rect x="{NX0}" y="{NY0}" width="{NW}" height="{NH}" rx="26" fill="#25262D" stroke="{INK}" stroke-width="6"/>')
# tacos (bloques) con brillo
o.append('<g fill="#3B3E48">')
for i in range(4):
    for j in range(5):
        x = NX0 + 18 + i * 70
        y = NY0 + 14 + j * 40
        o.append(f'<rect x="{x}" y="{y}" width="56" height="28" rx="6"/>')
o.append('</g>')
o.append('<g id="channels2" fill="none" stroke-linecap="round">')
for i in range(3):
    x = NX0 + 81 + i * 70
    d = f"M {x} {NY0 + 8} L {x} {NY0 + NH - 8}"
    o.append(f'<path d="{d}" stroke="#4FA8EE" stroke-width="12"/>')
for j in range(4):
    y = NY0 + 48 + j * 40
    d = f"M {NX0 + 8} {y} L {NX0 + NW - 8} {y}"
    o.append(f'<path d="{d}" stroke="#4FA8EE" stroke-width="7"/>')
o.append('</g>')
o.append('<g id="outr">')
for y in (NY0 + 48, NY0 + 128):
    o.append(arrow(f"or{y}", [(NX0 - 6, y), (NX0 - 46, y)], "#FFFFFF", 6, 16))
    o.append(arrow(f"orr{y}", [(NX0 + NW + 6, y + 40), (NX0 + NW + 46, y + 40)], "#FFFFFF", 6, 16))
o.append('</g>')
# signo igual
o.append(f'<g id="eq"><circle cx="500" cy="500" r="36" fill="{LIME}" stroke="{INK}" stroke-width="6"/>'
         f'<path d="M 484 490 L 516 490 M 484 510 L 516 510" stroke="{INK}" stroke-width="7" stroke-linecap="round"/></g>')
# etiquetas
o.append(tag("ldedo", 170, 92, "DEDO", lead=(227, 150, 250, 196)))
o.append(tag("lneum", 470, 92, "NEUMÁTICO", lead=(676, 121, 690, 140)))
o.append('</svg>')
print("\n".join(o))

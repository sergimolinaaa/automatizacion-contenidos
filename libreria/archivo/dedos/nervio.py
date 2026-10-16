import math, random, sys
sys.path.insert(0, sys.path[0])
from common import *

random.seed(11)
WL = 575          # nivel del agua
W = 150           # ancho del dedo
TOP = 112         # punta del dedo
SK = "#C97B5C"
o = [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 700">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#EAF4F7"/><stop offset="1" stop-color="#D3E5EC"/></linearGradient>
<linearGradient id="water" gradientUnits="userSpaceOnUse" x1="0" y1="{WL}" x2="0" y2="700"><stop offset="0" stop-color="#8FD3FF"/><stop offset="1" stop-color="#2F7FD6"/></linearGradient>
<linearGradient id="sk1" gradientUnits="userSpaceOnUse" x1="250" y1="0" x2="410" y2="0"><stop offset="0" stop-color="#E9A27F"/><stop offset="0.35" stop-color="#FBD3B8"/><stop offset="1" stop-color="#EBA886"/></linearGradient>
<linearGradient id="sk2" gradientUnits="userSpaceOnUse" x1="590" y1="0" x2="750" y2="0"><stop offset="0" stop-color="#E9A27F"/><stop offset="0.35" stop-color="#FBD3B8"/><stop offset="1" stop-color="#EBA886"/></linearGradient>
<linearGradient id="nrv" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFF3A0"/><stop offset="1" stop-color="#F2B705"/></linearGradient>
<radialGradient id="glow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#FFFFFF"/><stop offset="0.35" stop-color="#C8FF2E"/><stop offset="1" stop-color="#C8FF2E" stop-opacity="0"/></radialGradient>
</defs>
<rect width="1000" height="700" fill="url(#bg)"/>''']
g = ['<g stroke="#C4D8E1" stroke-width="4">']
for x in range(55, 1001, 110):
    g.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{WL}"/>')
for y in range(95, WL, 110):
    g.append(f'<line x1="0" y1="{y}" x2="1000" y2="{y}"/>')
o += g + ['</g>']
o.append(f'<rect y="{WL}" width="1000" height="{700 - WL}" fill="url(#water)"/>')
o.append(f'<g fill="#FFFFFF" opacity="0.15"><path d="M 120 {WL} L 200 {WL} L 140 700 L 50 700 Z"/><path d="M 820 {WL} L 880 {WL} L 860 700 L 780 700 Z"/></g>')
o.append('<g id="divider"><path d="M 500 70 L 500 545" stroke="#B9CDD8" stroke-width="5" stroke-linecap="round"/></g>')


def finger(cx, grad, wr, id_):
    s = [f'<g id="{id_}">']
    s.append(f'<path d="M {cx - 50} {TOP + 50} C {cx - 46} {TOP - 4}, {cx + 46} {TOP - 4}, {cx + 50} {TOP + 50} Z" fill="#F8E6DC" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
    s.append(f'<path d="M {cx - 26} {TOP + 14} Q {cx} {TOP + 4} {cx + 26} {TOP + 14}" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>')
    d = f"M {cx - 76} 720 L {cx - 70} {TOP + 78} C {cx - 70} {TOP - 6}, {cx + 70} {TOP - 6}, {cx + 70} {TOP + 78} L {cx + 76} 720 Z"
    s.append(f'<path d="{d}" fill="url(#{grad})" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>')
    s.append(f'<ellipse cx="{cx + 6}" cy="{TOP + 120}" rx="52" ry="70" fill="#FFE3D2" opacity="0.35"/>')
    # brillo lateral
    s.append(f'<path d="M {cx - W / 2 + 14} {WL - 20} L {cx - W / 2 + 14} {TOP + 70}" stroke="#FFEADB" stroke-width="7" stroke-linecap="round" opacity="0.85"/>')
    # pliegues de las articulaciones (cara palmar)
    for y in (300, 470):
        s.append(f'<path d="M {cx - 50} {y} Q {cx} {y + 12} {cx + 50} {y}" fill="none" stroke="{SK}" stroke-width="5" stroke-linecap="round"/>')
        s.append(f'<path d="M {cx - 34} {y + 14} Q {cx} {y + 22} {cx + 34} {y + 14}" fill="none" stroke="{SK}" stroke-width="3.5" stroke-linecap="round" opacity="0.7"/>')
    # borde de la uña asomando por arriba
    s.append('</g>')
    return "".join(s)


L, R = 300, 700
o.append(finger(L, "sk1", True, "fingl"))
o.append(finger(R, "sk2", False, "fingr"))
# yema derecha: lisa y brillante
o.append(f'<g id="smooth"><path d="M {R - 40} {TOP + 70} Q {R - 30} {TOP + 40} {R} {TOP + 34}" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round" opacity="0.9"/>'
         f'<ellipse cx="{R + 20}" cy="{TOP + 120}" rx="34" ry="44" fill="#FFFFFF" opacity="0.18"/></g>')
# arrugas de la yema izquierda
o.append('<g id="wrinkles" fill="none" stroke="#A9573F" stroke-width="4.5" stroke-linecap="round">')
for k in (-2, -1, 0, 1, 2):
    x = L + k * 22
    y0 = TOP + 30 + abs(k) * 14
    o.append(f'<path d="{wavy(x, y0, x + k * 6, TOP + 165, 4, 3, 30)}"/>')
for y in (TOP + 175, TOP + 195):
    o.append(f'<path d="{wavy(L - 46, y, L + 46, y + 2, 3, 3, 30)}"/>')
o.append('</g>')


# nervios digitales (vista "rayos X")
def nerve(cx, cut):
    s = []
    for side in (-1, 1):
        x = cx + side * 44
        if cut:
            s.append(dbl(f"M {x} {WL + 60} L {x} {cut + 16}", 9, "#F7CF2A", 7, cap="round"))
            s.append(f'<path d="M {x} {cut - 16} L {x} {TOP + 120} Q {x} {TOP + 80} {x - side * 16} {TOP + 60}" fill="none" stroke="#9AA5AE" stroke-width="7" stroke-linecap="round" opacity="0.8"/>')
        else:
            s.append(dbl(f"M {x} {WL + 60} L {x} {TOP + 120} Q {x} {TOP + 80} {x - side * 16} {TOP + 60}", 9, "#F7CF2A", 7))
            for yy in (TOP + 100, TOP + 140):
                s.append(dbl(f"M {x} {yy} L {x - side * 22} {yy - 20}", 4, "#F7CF2A", 5))
    return "".join(s)


o.append('<g id="nervel" opacity="0.9">' + nerve(L, None) + '</g>')
CUT = 420
o.append('<g id="nerver" opacity="0.9">' + nerve(R, CUT) + '</g>')
# corte (rayo coral)
z = f"M {R - 80} {CUT - 14} L {R - 40} {CUT + 10} L {R - 4} {CUT - 12} L {R + 36} {CUT + 12} L {R + 80} {CUT - 10}"
o.append(f'<g id="cut">{dbl(z, 10, CORAL, 10)}</g>')
# señales
o.append(f'<g id="sigl"><circle cx="{L - 44}" cy="{WL - 10}" r="30" fill="url(#glow)"/><circle cx="{L - 44}" cy="{WL - 10}" r="10" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/></g>')
o.append(f'<g id="sigr"><circle cx="{R + 44}" cy="{WL - 10}" r="30" fill="url(#glow)"/><circle cx="{R + 44}" cy="{WL - 10}" r="10" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/></g>')
# agua delante de la base + ondas
for cx in (L, R):
    o.append(f'<path d="M {cx - 80} {WL} L {cx + 80} {WL} L {cx + 80} 700 L {cx - 80} 700 Z" fill="url(#water)" opacity="0.86"/>')
    o.append(f'<ellipse cx="{cx}" cy="{WL + 4}" rx="96" ry="12" fill="none" stroke="#FFFFFF" stroke-width="5"/>')
    for k in (1, 2):
        o.append(f'<g id="rip{"l" if cx == L else "r"}{k}"><ellipse cx="{cx}" cy="{WL + 4}" rx="110" ry="16" fill="none" stroke="#FFFFFF" stroke-width="4"/></g>')
o.append(f'<line x1="0" y1="{WL}" x2="1000" y2="{WL}" stroke="{INK}" stroke-width="6"/>')
for cx in (L, R):
    o.append(f'<path d="M {cx - 83} {WL} L {cx + 83} {WL}" stroke="url(#water)" stroke-width="8"/>')
# etiquetas
o.append(tag("lsano", 40, 380, "SANO", lead=(160, 409, L - 44, 409)))
o.append(tag("ldanado", 800, 330, "DAÑADO", lead=(860, 388, R + 70, CUT - 2)))
o.append(tag("larrugas", 40, 150, "ARRUGAS", lead=(210, 180, L + 22, 250)))
o.append(tag("lliso", 820, 150, "LISO", lead=(840, 180, R + 50, 210)))
o.append('</svg>')
print("\n".join(o))

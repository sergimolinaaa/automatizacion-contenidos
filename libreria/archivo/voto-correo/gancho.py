import sys, math
from vc import *

OUT = "gancho_full.svg"
defs = BASE_DEFS + EXTRA_DEFS + lg("skyG", [(0, "#8FD0FF"), (1, "#DDF2FF")]) + lg("hillG", [(0, "#8ED36E"), (1, "#5FA846")]) \
    + lg("groundG", [(0, "#4F8E3C"), (1, "#2F5E26")]) + lg("wingG", [(0, "#FFFFFF"), (1, "#D9E4F2")]) + rg("burstY", [(0, "#FFF2A8"), (1, YEL)])
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920">\n<defs>{defs}</defs>']
o.append('<rect width="1080" height="1920" fill="url(#skyG)"/>')
# nubes
def cloud(x, y, s):
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M -110 30 C -130 -10, -80 -40, -50 -20 C -40 -70, 30 -70, 40 -25 C 80 -50, 130 -10, 110 30 Z" fill="#FFFFFF" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
            f'<path d="M -70 10 C -60 -5, -40 -8, -30 -2" fill="none" stroke="#D8ECFA" stroke-width="6" stroke-linecap="round"/></g>')
o.append(f'<g id="nubes">{cloud(170, 470, 1.0)}{cloud(900, 420, 0.8)}</g>')
# colinas y suelo
o.append(f'<path d="M 0 1140 C 200 1060, 380 1080, 560 1130 C 740 1080, 900 1060, 1080 1110 L 1080 1920 L 0 1920 Z" fill="url(#hillG)" stroke="{INK}" stroke-width="7"/>')
o.append(f'<path d="M 0 1230 L 1080 1230 L 1080 1920 L 0 1920 Z" fill="url(#groundG)"/>')
o.append(f'<path d="M 0 1230 L 1080 1230" stroke="{INK}" stroke-width="7"/>')
o.append('<g stroke="#3D7530" stroke-width="5" stroke-linecap="round" opacity="0.7">' + "".join(
    f'<path d="M {x} {y} l -8 -18 M {x} {y} l 8 -18"/>' for x, y in ((120, 1190), (330, 1170), (700, 1180), (980, 1175), (480, 1200))) + "</g>")

# buzón (izquierda)
BX, BB = 230, 1232
o.append(f'<ellipse cx="{BX}" cy="{BB+6}" rx="130" ry="16" fill="{INK}" opacity="0.25"/>')
o.append(f'<g id="buzon">')
o.append(f'<rect x="{BX-22}" y="{BB-250}" width="44" height="250" fill="url(#steelD)" stroke="{INK}" stroke-width="6"/>')
bw, bh, bt = 230, 250, BB - 520
o.append(f'<path d="M {BX-bw/2} {bt+bh} L {BX-bw/2} {bt+70} C {BX-bw/2} {bt-20}, {BX+bw/2} {bt-20}, {BX+bw/2} {bt+70} L {BX+bw/2} {bt+bh} Z" fill="url(#yelG)" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>')
o.append(f'<path d="M {BX-bw/2+18} {bt+bh-14} L {BX-bw/2+18} {bt+80}" stroke="#FFF0B0" stroke-width="10" stroke-linecap="round"/>')
o.append(f'<rect x="{BX-70}" y="{bt+70}" width="140" height="22" rx="11" fill="{INK}"/>')
o.append(f'<rect x="{BX-60}" y="{bt+140}" width="120" height="74" rx="10" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/>')
o.append(sobre(BX, bt + 177, 80, 50, 0, sw=4))
o.append(f'<rect x="{BX-bw/2-8}" y="{bt+bh-6}" width="{bw+16}" height="22" rx="6" fill="url(#yelS)" stroke="{INK}" stroke-width="6"/>')
o.append("</g>")
SLOT_B = (BX, bt + 81)

# urna (derecha)
u, slot = urna(830, BB, 250, 270, "VOTO", n_sobres=8, seed=4)
o.append(f'<g id="urna">{u}</g>')
print("slot", slot)

# ruta punteada buzón -> urna
x1, y1 = SLOT_B[0] + 40, SLOT_B[1] - 40
x2, y2 = slot[0] - 30, slot[1] - 40
ruta = f"M {x1} {y1} C {x1+40} 560, {x2-80} 560, {x2} {y2}"
o.append(f'<g id="ruta"><path d="{ruta}" fill="none" stroke="{INK}" stroke-width="16" stroke-linecap="round"/>'
         f'<path d="{ruta}" fill="none" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round" stroke-dasharray="2 26"/></g>')
o.append(arrow("punta", ((x2 - 20, y2 - 60), (x2, y2)), col="#FFFFFF", w=8, head=30))

# sobre certificado con alas, en lo alto del arco
SX, SY = 560, 690
wing = lambda s: (f'<path d="M {SX+s*60} {SY-30} C {SX+s*140} {SY-150}, {SX+s*230} {SY-130}, {SX+s*250} {SY-90} C {SX+s*200} {SY-80}, {SX+s*215} {SY-50}, {SX+s*170} {SY-40} C {SX+s*190} {SY-20}, {SX+s*150} {SY}, {SX+s*80} {SY+10} Z" '
                  f'fill="url(#wingG)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
                  f'<path d="M {SX+s*90} {SY-36} C {SX+s*130} {SY-80}, {SX+s*170} {SY-96}, {SX+s*210} {SY-98}" fill="none" stroke="#B8C6DA" stroke-width="5" stroke-linecap="round"/>')
o.append(f'<g id="sobre">{wing(-1)}{wing(1)}{cert_envelope(SX, SY, 280, 180, -4)}</g>')

# interrogantes
def qm(x, y, s, rot):
    return (f'<g transform="rotate({rot} {x} {y})"><circle cx="{x}" cy="{y}" r="{46*s}" fill="url(#burstY)" stroke="{INK}" stroke-width="6"/>'
            + T(x, y + 22 * s, "?", 62 * s, INK, font=DISP) + "</g>")
o.append(f'<g id="dudas">{qm(300, 600, 1.0, -12)}{qm(870, 600, 1.15, 10)}{qm(560, 920, 0.8, 8)}</g>')

# etiqueta «¿SE PIERDE?»
s, _ = label("tpierde", 540, 1040, "¿SE PIERDE?", bg=CORAL, fg="#FFFFFF", size=36)
o.append(s)
o.append("</svg>")
save(OUT, "\n".join(o))

import sys, math
sys.path.insert(0, "/tmp/claude-0/-home-user-automatizacion-contenidos/039df981-7a17-5355-b711-18510fb209db/scratchpad/volcan")
from vlib import *
CX, CY, R = 500, 362, 272
AX, AY = 500, 236          # comisura anterior (vértice de la V)
PY = 500                   # extremo posterior de las cuerdas
defs = "\n".join([
    rg("throat", [(0, "#B6404F"), (0.6, "#D9707A"), (1, "#F2A0A0")], 0.5, 0.55, 0.65),
    rg("hole", [(0, "#1A0408"), (0.7, "#3C0C16"), (1, "#5A1A24")], 0.5, 0.75, 0.8),
    lg("cord", [(0, "#FFFFFF"), (1, "#E9DED2")], 0, 0, 1, 0),
    lg("epi", [(0, "#FBD8CB"), (1, "#E7A99A")]),
    rg("ary", [(0, "#F7B4B4"), (1, "#C8606C")], 0.4, 0.35, 0.7),
    lg("fold2", [(0, "#F09AA4"), (1, "#C85A6A")], 0, 0, 1, 0),
    f'<clipPath id="view"><circle cx="{CX}" cy="{CY}" r="{R}"/></clipPath>',
])
o = [head(defs)]
o.append('<rect width="1000" height="700" fill="#1B1420"/>')
o.append('<g fill="none" stroke="#2C2334" stroke-width="2">' + "".join(f'<circle cx="{CX}" cy="{CY}" r="{R + 30 + k * 40}"/>' for k in range(6)) + '</g>')
o.append(f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="url(#throat)"/>')
o.append('<g clip-path="url(#view)">')
# base de la lengua y valécula (arriba)
o.append(f'<path d="M 200 60 L 800 60 L 800 170 C 700 150, 300 150, 200 170 Z" fill="#C8606C"/>')
o.append('<g fill="none" stroke="#A8485A" stroke-width="3" opacity="0.6"><path d="M 300 120 q 20 -10 40 0"/><path d="M 640 116 q 20 -10 40 0"/><path d="M 470 104 q 20 -10 40 0"/></g>')
# pliegues aritenoepiglóticos (borde de la entrada)
rim = smooth([(372, 190), (330, 280), (338, 420), (372, 520), (430, 566), (500, 576), (570, 566), (628, 520), (662, 420), (670, 280), (628, 190)], False)
o.append(f'<path d="{rim} C 600 230, 400 230, 372 190 Z" fill="#E98C98" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
# pliegues vestibulares (falsas cuerdas)
for s in (-1, 1):
    d = smooth([(AX + s * 14, 226), (AX + s * 60, 280), (AX + s * 108, 380), (AX + s * 124, 470), (AX + s * 112, 520)])
    o.append(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="40" stroke-linecap="round"/><path d="{d}" fill="none" stroke="url(#fold2)" stroke-width="30" stroke-linecap="round"/>')
# hueco de la glotis (oscuro, se ve la tráquea)
hole = f"M {AX} {AY} L {AX - 82} {PY + 4} Q {AX} {PY + 30} {AX + 82} {PY + 4} Z"
o.append(f'<g id="hueco"><path d="{hole}" fill="url(#hole)"/>')
o.append('<g fill="none" stroke="#7A2A36" stroke-width="5" stroke-linecap="round" opacity="0.8">' + "".join(
    f'<path d="M {AX - w} {y} Q {AX} {y + 10} {AX + w} {y}"/>' for y, w in [(330, 18), (380, 30), (430, 44), (470, 56)]) + '</g></g>')
# cuerdas vocales verdaderas (blancas) + aritenoides; giran desde la comisura anterior
def cord(s):
    inner = (AX + s * 78, PY)
    outer = (AX + s * 128, PY - 4)
    d = (f"M {AX} {AY} L {inner[0]} {inner[1]} C {inner[0] + s * 6} {PY + 14}, {outer[0] - s * 4} {PY + 10}, {outer[0]} {outer[1]} "
         f"C {AX + s * 106} {380}, {AX + s * 42} {270}, {AX} {AY} Z")
    ary = (AX + s * 108, PY + 22)
    g = (f'<ellipse cx="{ary[0]}" cy="{ary[1]}" rx="34" ry="28" fill="url(#ary)" stroke="{INK}" stroke-width="6"/>'
         f'<ellipse cx="{ary[0] - s * 8}" cy="{ary[1] - 10}" rx="10" ry="6" fill="#FFD6D6" opacity="0.8"/>'
         f'<path d="{d}" fill="url(#cord)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
         f'<path d="M {AX + s * 6} {AY + 20} L {AX + s * 66} {PY - 20}" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>'
         f'<path d="M {AX + s * 26} {AY + 40} C {AX + s * 60} {330}, {AX + s * 90} {420}, {AX + s * 100} {PY - 14}" fill="none" stroke="#E5B9B0" stroke-width="3" stroke-linecap="round" opacity="0.8"/>')
    return g
o.append('<g id="cordl">' + cord(-1) + '</g>')
o.append('<g id="cordr">' + cord(1) + '</g>')
# epiglotis (arriba, delante)
o.append(f'<g id="epi"><path d="M 372 196 C 400 120, 600 120, 628 196 C 604 176, 560 166, 500 166 C 440 166, 396 176, 372 196 Z" fill="url(#epi)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
         '<path d="M 410 160 C 450 138, 550 138, 590 160" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" opacity="0.8"/></g>')
o.append('</g>')
# golpe al cerrarse
sb = []
for k in range(16):
    a = k * 2 * math.pi / 16
    r = 56 if k % 2 == 0 else 26
    sb.append((AX + r * math.cos(a), 380 + r * math.sin(a)))
o.append(f'<g id="golpe"><path d="M ' + " L ".join(f"{x:.1f} {y:.1f}" for x, y in sb) + f' Z" fill="{CORAL}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/></g>')
# marco del endoscopio
o.append(f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="none" stroke="{INK}" stroke-width="12"/><circle cx="{CX}" cy="{CY}" r="{R - 9}" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.35"/>')
o.append(label("lglotis", 40, 300, "GLOTIS", AX - 4, 420))
o.append(label("lcuerdas", 640, 574, "CUERDAS VOCALES", AX + 60, 440))
o.append(label("lepi", 690, 120, "EPIGLOTIS", 592, 160))
t1, _ = tag("lopen", 50, 560, "ABIERTA", bg="#FFFFFF", fg=INK)
t2, _ = tag("lclosed", 640, 124, "¡CERRADA!", bg=CORAL, fg=INK)
o.append(t1 + t2)
o.append('</svg>')
open(sys.argv[1], "w").write("\n".join(o))

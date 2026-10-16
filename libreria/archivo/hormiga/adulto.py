"""Hormiga león adulta (Myrmeleontidae): alas largas con nervaduras, antenas en maza; detalle de la larva."""
import math, random, sys
sys.path.insert(0, ".")
from lib import *
from lib import bez

o = [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 700">
<defs>
{LARVA_DEFS}
<linearGradient id="dusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#B9C3F0"/><stop offset="0.55" stop-color="#F3C9C0"/><stop offset="1" stop-color="#FFE3B8"/></linearGradient>
<linearGradient id="abd" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2A221C"/><stop offset="0.45" stop-color="#6B5A48"/><stop offset="1" stop-color="#1E1712"/></linearGradient>
<radialGradient id="eyeg" cx="0.35" cy="0.3" r="0.8"><stop offset="0" stop-color="#8C8A7A"/><stop offset="0.5" stop-color="#3A3830"/><stop offset="1" stop-color="#121210"/></radialGradient>
<linearGradient id="wing" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0.75"/><stop offset="1" stop-color="#DCEBFF" stop-opacity="0.45"/></linearGradient>
<radialGradient id="moon" cx="0.4" cy="0.4" r="0.6"><stop offset="0" stop-color="#FFFBEA"/><stop offset="1" stop-color="#FFE9A8"/></radialGradient>
</defs>
''']
FREE = len(sys.argv) > 1 and sys.argv[1] == "free"
if FREE:
    o[0] = o[0].replace('viewBox="0 0 1000 700"', 'viewBox="0 0 1000 860"')
    o.append('<g transform="translate(0 70)">')
else:
    o.append('<rect width="1000" height="700" fill="url(#dusk)"/>')
bg = []
bg.append('<circle cx="905" cy="420" r="50" fill="url(#moon)" opacity="0.9"/>')
# horizonte: dunas y hierbas lejanas (sin contorno)
bg.append('<path d="M 0 560 C 160 520, 300 545, 460 530 C 640 512, 800 548, 1000 520 L 1000 700 L 0 700 Z" fill="#E9C995" opacity="0.8"/>')
bg.append('<path d="M 0 610 C 200 585, 380 612, 560 596 C 740 580, 880 606, 1000 590 L 1000 700 L 0 700 Z" fill="#DDB77C"/>')
random.seed(3)
bg.append('<g stroke="#B7A16E" stroke-width="5" stroke-linecap="round" fill="none" opacity="0.8">' + "".join(
    f'<path d="M {x} 600 q {random.randint(-12, 12)} -40 {random.randint(-20, 20)} -{random.randint(50, 90)}"/>' for x in range(30, 1000, 37) if not 360 < x < 640) + '</g>')

if not FREE:
    o += bg
CX = 520
# alas: base en el tórax, punta, anchura
def wing(base, tip, w, sg, spots):
    bx, by = base
    tx, ty = tip
    dx, dy = tx - bx, ty - by
    L = math.hypot(dx, dy)
    nx, ny = -dy / L, dx / L
    # borde delantero (algo recto) y trasero (curvo)
    a1 = (bx + dx * 0.3 + nx * w * 0.55 * sg, by + dy * 0.3 + ny * w * 0.55 * sg)
    a2 = (bx + dx * 0.85 + nx * w * 0.6 * sg, by + dy * 0.85 + ny * w * 0.6 * sg)
    b1 = (bx + dx * 0.85 - nx * w * 0.7 * sg, by + dy * 0.85 - ny * w * 0.7 * sg)
    b2 = (bx + dx * 0.25 - nx * w * 0.9 * sg, by + dy * 0.25 - ny * w * 0.9 * sg)
    d = (f"M {bx:.1f} {by:.1f} C {a1[0]:.1f} {a1[1]:.1f}, {a2[0]:.1f} {a2[1]:.1f}, {tx:.1f} {ty:.1f} "
         f"C {b1[0]:.1f} {b1[1]:.1f}, {b2[0]:.1f} {b2[1]:.1f}, {bx:.1f} {by:.1f} Z")
    s = f'<path d="{d}" fill="url(#wing)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
    # nervaduras longitudinales
    veins = []
    for k in (-0.45, -0.15, 0.15, 0.4):
        c = (bx + dx * 0.5 + nx * w * k * sg, by + dy * 0.5 + ny * w * k * sg)
        e = (bx + dx * (0.97 - abs(k) * 0.25) + nx * w * k * 0.5 * sg, by + dy * (0.97 - abs(k) * 0.25) + ny * w * k * 0.5 * sg)
        veins.append(f"M {bx:.1f} {by:.1f} Q {c[0]:.1f} {c[1]:.1f} {e[0]:.1f} {e[1]:.1f}")
    s += f'<path d="{" ".join(veins)}" fill="none" stroke="#5A4A3A" stroke-width="2.6" opacity="0.75"/>'
    # nervaduras transversales (red)
    cross = []
    for i in range(3, 19):
        t = i / 20
        half = w * (0.55 if t < 0.8 else 0.55 * (1 - (t - 0.8) * 4)) * (0.6 + 0.4 * math.sin(math.pi * min(1, t * 1.3)))
        px, py = bx + dx * t, by + dy * t
        cross.append(f"M {px + nx * half * 0.85:.1f} {py + ny * half * 0.85:.1f} L {px - nx * half * 0.85:.1f} {py - ny * half * 0.85:.1f}")
    s += f'<path d="{" ".join(cross)}" fill="none" stroke="#5A4A3A" stroke-width="1.6" opacity="0.55"/>'
    # pterostigma y manchas
    px, py = bx + dx * 0.84 + nx * w * 0.18 * sg, by + dy * 0.84 + ny * w * 0.18 * sg
    s += f'<ellipse cx="{px:.1f}" cy="{py:.1f}" rx="12" ry="4.5" fill="#4A3828" transform="rotate({math.degrees(math.atan2(dy, dx)):.0f} {px:.1f} {py:.1f})"/>'
    for t, k, r in spots:
        qx, qy = bx + dx * t + nx * w * k * sg, by + dy * t + ny * w * k * sg
        s += f'<circle cx="{qx:.1f}" cy="{qy:.1f}" r="{r}" fill="#4A3828" opacity="0.7"/>'
    # brillo
    s += f'<path d="M {bx + dx * 0.2 + nx * w * 0.25 * sg:.1f} {by + dy * 0.2 + ny * w * 0.25 * sg:.1f} L {bx + dx * 0.6 + nx * w * 0.32 * sg:.1f} {by + dy * 0.6 + ny * w * 0.32 * sg:.1f}" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity="0.8"/>'
    return s

TH = (CX, 262)
spots = [(0.55, 0.1, 6), (0.7, -0.2, 5), (0.4, -0.3, 4)]
o.append('<g id="wingl">' + wing((CX - 14, 266), (110, 340), 64, 1, spots) + wing((CX - 16, 248), (128, 190), 70, -1, spots) + '</g>')
o.append('<g id="wingr">' + wing((CX + 14, 266), (930, 340), 64, -1, spots) + wing((CX + 16, 248), (912, 190), 70, 1, spots) + '</g>')

# cuerpo
o.append('<g id="body">')
# abdomen largo y fino
o.append(f'<path d="M {CX - 14} 290 C {CX - 16} 380, {CX - 10} 480, {CX - 4} 560 Q {CX} 572 {CX + 4} 560 C {CX + 10} 480, {CX + 16} 380, {CX + 14} 290 Z" fill="url(#abd)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
o.append(f'<g stroke="#B9A58A" stroke-width="2.5" opacity="0.7">' + "".join(f'<line x1="{CX - 14 + (y - 290) * 0.02:.1f}" y1="{y}" x2="{CX + 14 - (y - 290) * 0.02:.1f}" y2="{y}"/>' for y in range(318, 556, 30)) + '</g>')
o.append(f'<path d="M {CX - 5} 300 C {CX - 6} 380, {CX - 4} 460, {CX - 2} 540" fill="none" stroke="#C9B497" stroke-width="3" stroke-linecap="round" opacity="0.7"/>')
# patas cortas (6) desde el tórax
for y0, dx, dy in ((238, 40, -22), (258, 46, 10), (276, 42, 40)):
    for sg in (-1, 1):
        o.append(leg([(CX + 12 * sg, y0), (CX + dx * sg, y0 + dy * 0.4), (CX + (dx + 12) * sg, y0 + dy + 14)], 4, "#3A3028", 5))
# tórax
o.append(f'<ellipse cx="{CX}" cy="262" rx="26" ry="34" fill="url(#abd)" stroke="{INK}" stroke-width="6"/>')
o.append(f'<path d="M {CX - 12} 240 Q {CX} 232 {CX + 12} 240" fill="none" stroke="#E6D7BF" stroke-width="4" stroke-linecap="round"/>')
o.append(f'<path d="M {CX - 4} 236 L {CX - 4} 290 M {CX + 4} 236 L {CX + 4} 290" stroke="#C9A982" stroke-width="2.5" opacity="0.6"/>')
o.append('</g>')
# cabeza y antenas en maza
o.append('<g id="antennae">' + leg([(CX - 8, 196), (CX - 30, 150), (CX - 46, 118)], 4, "#3A3028", 5) + leg([(CX + 8, 196), (CX + 30, 150), (CX + 46, 118)], 4, "#3A3028", 5) +
         f'<ellipse cx="{CX - 48}" cy="114" rx="9" ry="12" fill="#3A3028" stroke="{INK}" stroke-width="4" transform="rotate(-30 {CX - 48} 114)"/>'
         f'<ellipse cx="{CX + 48}" cy="114" rx="9" ry="12" fill="#3A3028" stroke="{INK}" stroke-width="4" transform="rotate(30 {CX + 48} 114)"/></g>')
o.append(f'<g id="head"><ellipse cx="{CX}" cy="210" rx="30" ry="22" fill="url(#abd)" stroke="{INK}" stroke-width="6"/>'
         f'<circle cx="{CX - 26}" cy="206" r="15" fill="url(#eyeg)" stroke="{INK}" stroke-width="5"/><circle cx="{CX + 26}" cy="206" r="15" fill="url(#eyeg)" stroke="{INK}" stroke-width="5"/>'
         f'<circle cx="{CX - 30}" cy="201" r="4.5" fill="#FFFFFF"/><circle cx="{CX + 22}" cy="201" r="4.5" fill="#FFFFFF"/>'
         f'<path d="M {CX - 8} 226 Q {CX} 232 {CX + 8} 226" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/></g>')

# detalle: la larva (antes)
IC, IR = (150, 560), 92
o.append(f'<g id="inset"><circle cx="{IC[0] + 6}" cy="{IC[1] + 8}" r="{IR}" fill="{INK}" opacity="0.25"/>'
         f'<circle cx="{IC[0]}" cy="{IC[1]}" r="{IR}" fill="#EBD3A0" stroke="{INK}" stroke-width="7"/>'
         + grains([(IC[0] + IR * 0.9 * math.cos(a), IC[1] + IR * 0.9 * math.sin(a)) for a in [i / 20 * 2 * math.pi for i in range(20)]], 70, ["#C99A5C", "#FFF6DE", "#B5864A"], 1.5, 3.5, seed=8)
         + f'<g transform="translate({IC[0]} {IC[1] - 26}) scale(0.36)">{larva(0.9)}</g>'
         + '</g>')
o.append(arrow("evo", [(258, 560), (330, 520), (402, 448)], LIME, 9, 26))
o.append(tag("lalas", 820, 470, "ALAS", 800, 330))
o.append(tag("lmaza", 770, 80, "ANTENAS EN MAZA", CX + 56, 112))
o.append(tag("lanos", 215, 420, "AÑOS COMO LARVA", IC[0] + 20, IC[1] - 74))
if FREE:
    o.append('</g>')
o.append('</svg>')
print("\n".join(o))

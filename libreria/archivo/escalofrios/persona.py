"""Free 1000x1100 transparente: persona tiritando + lupa del músculo (relajado / contraído) + ondas de calor."""
import math, random, sys
sys.path.insert(0, sys.path[0])
from common import *

defs = '''
<radialGradient id="face" cx="0.42" cy="0.35" r="0.75"><stop offset="0" stop-color="#FBD9C0"/><stop offset="0.7" stop-color="#EDB08C"/><stop offset="1" stop-color="#C98462"/></radialGradient>
<linearGradient id="jersey" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5BA3E8"/><stop offset="1" stop-color="#2A5FA8"/></linearGradient>
<linearGradient id="wool" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F0645A"/><stop offset="1" stop-color="#A82A22"/></linearGradient>
<linearGradient id="scarf" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFD24A"/><stop offset="1" stop-color="#E09A1E"/></linearGradient>
<radialGradient id="lens" cx="0.4" cy="0.35" r="0.8"><stop offset="0" stop-color="#FFF4F0"/><stop offset="1" stop-color="#F6D8D2"/></radialGradient>
<linearGradient id="fib" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F08A80"/><stop offset="0.5" stop-color="#D2463E"/><stop offset="1" stop-color="#8E1F1A"/></linearGradient>
<clipPath id="lc"><circle cx="800" cy="600" r="150"/></clipPath>
'''
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1100">\n<defs>{defs}</defs>']


def flake(cx, cy, r, rotd=0):
    arms = []
    for k in range(6):
        a = math.radians(k * 60 + rotd)
        arms.append(f"M {cx} {cy} L {cx + r*math.cos(a):.1f} {cy + r*math.sin(a):.1f}")
        bx, by = cx + r * 0.55 * math.cos(a), cy + r * 0.55 * math.sin(a)
        for sgn in (-1, 1):
            b2 = a + sgn * math.radians(45)
            arms.append(f"M {bx:.1f} {by:.1f} L {bx + r*0.35*math.cos(b2):.1f} {by + r*0.35*math.sin(b2):.1f}")
    d = " ".join(arms)
    return (f'<path d="{d}" fill="none" stroke="#2F6FB0" stroke-width="{r*0.26+5:.1f}" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="#FFFFFF" stroke-width="{r*0.26:.1f}" stroke-linecap="round"/>')


o.append('<g id="nieve">' + flake(90, 160, 26, 5) + flake(640, 120, 22, 12) + flake(870, 260, 28, 0) + flake(60, 700, 20, 8) + '</g>')

# --- persona (grupo que tiembla)
o.append('<g id="persona">')
o.append('<ellipse cx="380" cy="1085" rx="300" ry="18" fill="#0B0B14" opacity="0.15"/>')
body = "M 120 1090 L 140 700 C 150 610, 250 572, 380 572 C 510 572, 610 610, 620 700 L 640 1090 Z"
o.append(f'<path d="{body}" fill="url(#jersey)" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>')
o.append('<path d="M 165 680 C 190 615, 270 592, 380 590" fill="none" stroke="#A9D2FF" stroke-width="7" stroke-linecap="round" opacity="0.8"/>')
# cuello
o.append(f'<path d="M 330 450 L 330 560 L 430 560 L 430 450 Z" fill="#E3A07C" stroke="{INK}" stroke-width="7"/>')
# bufanda
o.append(f'<path d="M 250 540 C 300 590, 460 590, 510 540 L 520 600 C 460 640, 300 640, 240 600 Z" fill="url(#scarf)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
o.append(f'<path d="M 440 600 L 470 760 L 410 770 L 395 610 Z" fill="url(#scarf)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
o.append('<g stroke="#B86E10" stroke-width="5">' + "".join(f'<line x1="{x}" y1="{y}" x2="{x+40}" y2="{y-4}"/>' for x, y in [(410, 680), (418, 720)]) + '</g>')
# brazos cruzados (abrazándose)
def arm(p0, p1, hand):
    s = (f'<path d="M {p0[0]} {p0[1]} L {p1[0]} {p1[1]}" stroke="{INK}" stroke-width="104" stroke-linecap="round"/>'
         f'<path d="M {p0[0]} {p0[1]} L {p1[0]} {p1[1]}" stroke="#3B80CF" stroke-width="90" stroke-linecap="round"/>'
         f'<path d="M {p0[0]} {p0[1]-30} L {p1[0]} {p1[1]-30}" stroke="#7DB8F2" stroke-width="10" stroke-linecap="round" opacity="0.7"/>')
    hx, hy = hand
    s += (f'<ellipse cx="{hx}" cy="{hy}" rx="40" ry="34" fill="url(#face)" stroke="{INK}" stroke-width="7"/>'
          + "".join(f'<path d="M {hx-22+k*14} {hy-26} L {hx-26+k*14} {hy+6}" stroke="#B0715A" stroke-width="4" stroke-linecap="round"/>' for k in range(4)))
    return s
o.append(arm((610, 900), (230, 780), (205, 760)))
o.append(arm((150, 900), (540, 780), (565, 760)))
# cabeza
o.append('<g id="cabeza">')
o.append(f'<ellipse cx="250" cy="340" rx="26" ry="38" fill="#E3A07C" stroke="{INK}" stroke-width="7"/>')
o.append(f'<ellipse cx="510" cy="340" rx="26" ry="38" fill="#E3A07C" stroke="{INK}" stroke-width="7"/>')
o.append(f'<ellipse cx="380" cy="335" rx="128" ry="148" fill="url(#face)" stroke="{INK}" stroke-width="8"/>')
# gorro de lana
o.append(f'<path d="M 245 290 C 240 150, 520 150, 515 290 Z" fill="url(#wool)" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>')
o.append(f'<rect x="232" y="262" width="296" height="54" rx="22" fill="#C83A30" stroke="{INK}" stroke-width="8"/>')
o.append('<g stroke="#8E1F1A" stroke-width="5">' + "".join(f'<line x1="{x}" y1="270" x2="{x}" y2="308"/>' for x in range(256, 520, 22)) + '</g>')
o.append(f'<circle cx="380" cy="150" r="34" fill="#FFF3E6" stroke="{INK}" stroke-width="7"/>')
# cejas preocupadas, ojos apretados
o.append(f'<path d="M 300 340 L 345 352" stroke="#6B4632" stroke-width="9" stroke-linecap="round"/><path d="M 460 340 L 415 352" stroke="#6B4632" stroke-width="9" stroke-linecap="round"/>')
o.append(f'<path d="M 305 380 L 340 372 L 305 362" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>')
o.append(f'<path d="M 455 380 L 420 372 L 455 362" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>')
# nariz roja y mejillas azuladas
o.append(f'<ellipse cx="380" cy="410" rx="22" ry="18" fill="#F07A6A" stroke="{INK}" stroke-width="5"/><circle cx="373" cy="404" r="5" fill="#FFFFFF" opacity="0.8"/>')
o.append('<ellipse cx="300" cy="420" rx="28" ry="16" fill="#9EC9F0" opacity="0.6"/><ellipse cx="460" cy="420" rx="28" ry="16" fill="#9EC9F0" opacity="0.6"/>')
o.append('</g>')
# boca que castañetea
o.append('<g id="boca">')
o.append(f'<rect x="330" y="440" width="100" height="40" rx="12" fill="#FFFFFF" stroke="{INK}" stroke-width="6"/>')
o.append(f'<line x1="330" y1="460" x2="430" y2="460" stroke="{INK}" stroke-width="4"/>' + "".join(f'<line x1="{x}" y1="442" x2="{x}" y2="478" stroke="{INK}" stroke-width="3"/>' for x in (355, 380, 405)))
o.append('</g>')
o.append('</g>')  # persona

# vaho
o.append('<g id="vaho" fill="#FFFFFF" stroke="#7FA6CC" stroke-width="4" opacity="0.9">' + "".join(
    f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x, y, r in [(470, 470, 16), (500, 455, 22), (535, 440, 18)]) + '</g>')
# líneas de temblor
def shiver(x, y):
    return stroke2(f"M {x} {y} q 9 14 0 28 q -9 14 0 28 q 9 14 0 28", 7, "#5BC0FF", 6)
o.append('<g id="temblor">' + shiver(205, 200) + shiver(180, 240) + shiver(560, 200) + shiver(585, 240) + shiver(100, 760) + shiver(75, 800) + '</g>')
# ondas de calor
def wave(x, y):
    return stroke2(f"M {x} {y} c -16 -20 16 -40 0 -60 c -16 -20 16 -40 0 -60", 9, CORAL, 7)
o.append('<g id="calor">' + wave(150, 640) + wave(200, 610) + wave(560, 610) + wave(610, 640) + '</g>')

# lupa del músculo
o.append(f'<g id="lineas"><line x1="560" y1="790" x2="690" y2="700" stroke="{INK}" stroke-width="5" stroke-dasharray="12 9"/>'
         f'<circle cx="560" cy="790" r="12" fill="{LIME}" stroke="{INK}" stroke-width="4"/></g>')
o.append('<g id="lupa">')
o.append('<circle cx="808" cy="610" r="158" fill="#0B0B14" opacity="0.15"/>')
o.append('<circle cx="800" cy="600" r="150" fill="url(#lens)"/>')
o.append('</g>')


def fibers(gid, x0, x1, ry, cy=600):
    g = [f'<g id="{gid}" clip-path="url(#lc)">']
    for k, dy in enumerate((-1, 0, 1)):
        yy = cy + dy * ry * 0.75
        rr = ry * 0.42
        g.append(f'<path d="M {x0} {yy} C {x0+40} {yy-rr}, {x1-40} {yy-rr}, {x1} {yy} C {x1-40} {yy+rr}, {x0+40} {yy+rr}, {x0} {yy} Z" fill="url(#fib)" stroke="{INK}" stroke-width="5"/>')
        n = int((x1 - x0) / 16)
        for i in range(2, n - 1):
            x = x0 + i * (x1 - x0) / n
            h = rr * (1 - ((x - (x0 + x1) / 2) / ((x1 - x0) / 2)) ** 2) * 0.85
            g.append(f'<line x1="{x:.1f}" y1="{yy-h:.1f}" x2="{x:.1f}" y2="{yy+h:.1f}" stroke="#8E1F1A" stroke-width="3" opacity="0.7"/>')
        g.append(f'<path d="M {x0+50} {yy-rr*0.55:.1f} C {x0+90} {yy-rr*0.8:.1f}, {x1-90} {yy-rr*0.8:.1f}, {x1-50} {yy-rr*0.55:.1f}" fill="none" stroke="#FFD0C8" stroke-width="4" stroke-linecap="round" opacity="0.8"/>')
    # tendones
    g.append(f'<rect x="{x0-80}" y="{cy-14}" width="84" height="28" rx="10" fill="#F4EDE0" stroke="{INK}" stroke-width="5"/>')
    g.append(f'<rect x="{x1-4}" y="{cy-14}" width="84" height="28" rx="10" fill="#F4EDE0" stroke="{INK}" stroke-width="5"/>')
    g.append('</g>')
    return "".join(g)


o.append(fibers("relajado", 680, 920, 90))
o.append(fibers("contraido", 712, 888, 118))
o.append(f'<g id="tira">' + stroke2("M 680 760 L 740 760", 8, LIME, 6) + f'<path d="M 740 742 L 768 760 L 740 778 Z" fill="{LIME}" stroke="{INK}" stroke-width="5"/>'
         + stroke2("M 920 760 L 860 760", 8, LIME, 6) + f'<path d="M 860 742 L 832 760 L 860 778 Z" fill="{LIME}" stroke="{INK}" stroke-width="5"/></g>')
o.append(f'<circle cx="800" cy="600" r="150" fill="none" stroke="{INK}" stroke-width="9"/>')
o.append(f'<path d="M 690 520 A 120 120 0 0 1 770 466" fill="none" stroke="#FFFFFF" stroke-width="9" stroke-linecap="round" opacity="0.9"/>')

# etiquetas
o.append(tag("lmusculo", 800 - tw("MÚSCULO") / 2, 400, tw("MÚSCULO"), "MÚSCULO"))
o.append(tag("ltiritar", 800 - tw("TIRITAR") / 2, 790, tw("TIRITAR"), "TIRITAR", bg=LIME, fg=INK))
o.append(tag("lcalor", 40, 470, tw("CALOR"), "CALOR", bg=CORAL, fg="#FFFFFF"))
o.append('</svg>')
print("\n".join(o))

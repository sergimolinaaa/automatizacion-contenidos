import sys, math, random
sys.path.insert(0, '/tmp/claude-0/-home-user-automatizacion-contenidos/039df981-7a17-5355-b711-18510fb209db/scratchpad/venus')
from trap import *

PRE = sys.argv[1] if len(sys.argv) > 1 else ""
MX, MY, MS, MA = 440, 390, 0.74, 26  # trampa principal
defs = DEFS + '''
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#DDF1FF"/><stop offset="1" stop-color="#F4F8E4"/></linearGradient>
<linearGradient id="moss" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9CCB6A"/><stop offset="1" stop-color="#5E8F3E"/></linearGradient>
<linearGradient id="water" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9FD6F0"/><stop offset="1" stop-color="#5FA8D6"/></linearGradient>
'''
o = [svg_open(defs)]
o.append('<rect width="1000" height="700" fill="url(#sky)"/>')
# pinos lejanos (sabana de pinos de las Carolinas), sin contorno
for x, h in ((80, 330), (230, 280), (620, 300), (780, 350), (930, 290)):
    o.append(f'<rect x="{x-5}" y="{460-h}" width="10" height="{h}" fill="#B8C9B4"/>')
    for k in range(3):
        y = 460 - h + k * 34
        o.append(f'<ellipse cx="{x}" cy="{y}" rx="{46-k*4}" ry="20" fill="#A9C4A4"/>')
o.append('<path d="M 0 440 C 160 420, 300 444, 480 430 C 650 418, 820 444, 1000 428 L 1000 520 L 0 520 Z" fill="#C9E2B0"/>')
# hierba alta lejana
random.seed(5)
gr = []
for _ in range(70):
    x = random.uniform(0, 1000); h = random.uniform(30, 70)
    gr.append(f'<path d="M {x:.0f} 470 q {random.uniform(-10,10):.0f} {-h/2:.0f} {random.uniform(-14,14):.0f} {-h:.0f}"/>')
o.append('<g stroke="#9DC98A" stroke-width="4" stroke-linecap="round" fill="none">' + "".join(gr) + '</g>')
# suelo de musgo
o.append('<path d="M 0 500 C 140 488, 280 506, 420 494 C 560 482, 700 504, 1000 490 L 1000 700 L 0 700 Z" fill="url(#moss)"/>')
o.append('<path d="M 0 500 C 140 488, 280 506, 420 494 C 560 482, 700 504, 740 500" fill="none" stroke="#0B0B14" stroke-width="5"/>')
o.append('<ellipse cx="850" cy="560" rx="120" ry="22" fill="url(#water)" stroke="#0B0B14" stroke-width="5"/><path d="M 770 556 L 830 552 M 880 566 L 910 564" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" opacity="0.8"/>')
mo = []
for _ in range(160):
    x = random.uniform(5, 995); y = random.uniform(510, 690)
    if (x - 850) ** 2 / 130 ** 2 + (y - 560) ** 2 / 30 ** 2 < 1:
        continue
    mo.append(f'<path d="M {x:.0f} {y:.0f} l -6 -8 M {x:.0f} {y:.0f} l 6 -8 M {x:.0f} {y:.0f} l 0 -10"/>')
o.append('<g stroke="#3F6E2A" stroke-width="2.5" stroke-linecap="round" opacity="0.7">' + "".join(mo) + '</g>')

# tallo floral con flores blancas (las flores van altas, lejos de las trampas)
o.append('<g id="flower">')
o.append(stroke2("M 300 600 C 296 440, 270 260, 262 150", 7, "#7FBF5A", extra=6))
o.append(stroke2("M 266 190 C 250 170, 236 160, 214 158", 4, "#7FBF5A", extra=5))
def flower(cx, cy, r=24):
    s = ""
    for k in range(5):
        a = math.radians(k * 72 - 90)
        px, py = cx + r * 0.75 * math.cos(a), cy + r * 0.75 * math.sin(a)
        s += f'<ellipse cx="{px:.1f}" cy="{py:.1f}" rx="{r*0.55:.1f}" ry="{r*0.42:.1f}" transform="rotate({k*72} {px:.1f} {py:.1f})" fill="#FFFFFF" stroke="{INK}" stroke-width="3.5"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="{r*0.3:.1f}" fill="#7FBF5A" stroke="{INK}" stroke-width="3"/>'
    for k in range(5):
        a = math.radians(k * 72 - 54)
        s += f'<circle cx="{cx+r*0.38*math.cos(a):.1f}" cy="{cy+r*0.38*math.sin(a):.1f}" r="2.5" fill="#F7C531"/>'
    return s
o.append(flower(262, 140) + flower(206, 156, 18))
o.append('</g>')

# trampa cerrada a la izquierda
o.append('<g id="trapl">' + petiole(300, 610, 150, 480, w=34, scale=0.6)
         + lobe("lcb", 150, 480, -18, 0.4, lower=True) + lobe("lct", 150, 480, -18, 0.4, lower=False) + '</g>')
# trampa pequeña a la derecha
o.append('<g id="trapr">' + petiole(330, 610, 690, 520, w=36, scale=0.6)
         + lobe("rbot", 690, 520, 22, 0.42, lower=True) + lobe("rtop", 690, 520, -34, 0.42, lower=False) + '</g>')
# trampa principal
o.append(petiole(310, 615, MX, MY, w=44, scale=0.85))
o.append(lobe("lobebot", MX, MY, MA, MS, lower=True))
# mosca dentro (para la escena del cierre)
def lw(cx, cy, lower, ang):
    sg = -1 if lower else 1
    y = -sg * cy
    a = math.radians(ang)
    return (MX + MS * (cx * math.cos(a) - y * math.sin(a)), MY + MS * (cx * math.sin(a) + y * math.cos(a)))
fin = lw(250, 50, True, MA)
o.append(fly("flyin", fin[0] + 10, fin[1] - 26, 0.9, 16))
o.append(lobe("lobetop", MX, MY, -MA, MS, lower=False))
# roseta: base
o.append(f'<ellipse cx="305" cy="612" rx="40" ry="14" fill="#2F7D34" stroke="{INK}" stroke-width="5"/>')
# mosca volando
o.append(fly("fly", 840, 220, 1.1, -8, wings_id="wings"))
# contador 1..5
o.append('<g id="count">')
for k in range(5):
    o.append(counter(f"c{k+1}", 560 + k * 80, 108, str(k + 1), col=(LIME if k < 2 else "#FFFFFF" if k < 4 else CORAL), r=30))
o.append('</g>')
# ¡zas!
o.append(f'<g id="zas"><path d="M 700 270 L 740 220 L 752 260 L 810 220 L 792 280 L 850 284 L 786 316 L 810 360 L 750 332 L 722 370 L 716 322 L 670 320 Z" fill="#FFE14D" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
         f'<text x="760" y="306" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="34" fill="{INK}">¡ZAS!</text></g>')
if PRE == "closed":
    o.append(f'<style>#lobetop,#lobebot{{transform-box:fill-box;transform-origin:center}}#lobetop{{rotate:{MA}deg}}#lobebot{{rotate:-{MA}deg}}</style>')
o.append('</svg>')
print("\n".join(o))

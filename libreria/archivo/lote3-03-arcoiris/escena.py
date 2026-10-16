import sys, math, random
sys.path.insert(0, sys.path[0])
from rb import *

H = 432
O = (560, 650)
R1, W1 = 430, 8
R2 = round(R1 * 50.4 / 42.3)
W2 = 9

defs = "\n".join([
    lg("sky", [(0, "#56677F"), (0.5, "#8EA3BA"), (1, "#E4EDF2")]),
    lg("skyr", [(0, "#FFF2CC", 0), (1, "#FFF2CC", 0.65)], 0, 0, 1, 0),
    rg("cloud", [(0, "#8D9AAE"), (1, "#56657A")], 0.5, 0.3, 0.7),
    lg("hillfar", [(0, "#A9C7B2"), (1, "#93B9A0")]),
    lg("hill", [(0, "#8ED17A"), (1, "#5DAF5A")]),
    lg("meadow", [(0, "#7CC96A"), (1, "#3B934A")]),
    lg("path", [(0, "#E9CF9E"), (1, "#C9A06A")]),
    rg("puddle", [(0, "#DDEFFF"), (1, "#8FB8DA")], 0.4, 0.4, 0.7),
    DEFS_P,
])
o = [header(defs)]
o.append('<rect width="1000" height="700" fill="url(#sky)"/>')
o.append('<rect width="1000" height="700" fill="url(#skyr)"/>')
rnd = random.Random(5)
st = []
for _ in range(110):
    x, y = rnd.uniform(0, 1000), rnd.uniform(60, H - 20)
    st.append(f"M {x:.0f} {y:.0f} L {x - 6:.0f} {y + 34:.0f}")
o.append(f'<g id="lluvia"><path d="{" ".join(st)}" stroke="#E6EEF5" stroke-width="2.5" opacity="0.3" stroke-linecap="round"/></g>')
# arcoíris (principal + secundario tenue)
o.append('<g id="arco">'
         f'<path d="{disc_above(O[0], O[1], R1 - 6 * W1, H)}" fill="#FFFFFF" opacity="0.16"/>'
         f'<path d="{annulus_above(O[0], O[1], R1, R2, H)}" fill="#1A2235" opacity="0.18"/>'
         + band(O[0], O[1], R1, W1, H, SPEC, 1.0) + band(O[0], O[1], R2 + 6 * W2, W2, H, list(reversed(SPEC)), 0.45) + '</g>')
# nube de tormenta que se aleja (arriba a la derecha, sin tapar el rótulo)
cl = [(700, 92, 90, 40), (800, 70, 90, 50), (900, 90, 90, 42), (760, 112, 110, 30), (880, 116, 110, 28), (990, 100, 60, 40)]
o.append('<g id="nube"><g fill="#0B0B14">' + "".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx + 5}" ry="{ry + 5}"/>' for x, y, rx, ry in cl) + '</g>'
         '<g fill="url(#cloud)">' + "".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}"/>' for x, y, rx, ry in cl) + '</g>'
         '<path d="M 740 62 C 770 44, 830 38, 860 48" fill="none" stroke="#B9C4D3" stroke-width="6" stroke-linecap="round" opacity="0.8"/></g>')
# pájaros
o.append('<g id="pajaros" fill="none" stroke="#0B0B14" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">'
         '<path d="M 420 150 Q 432 140, 444 150 Q 456 140, 468 150"/><path d="M 480 182 Q 489 175, 498 182 Q 507 175, 516 182"/></g>')
# colinas
o.append(f'<path d="M 0 {H - 6} C 140 {H - 40}, 280 {H - 30}, 420 {H - 46} C 560 {H - 60}, 700 {H - 30}, 840 {H - 44} C 920 {H - 50}, 970 {H - 40}, 1000 {H - 42} L 1000 {H + 20} L 0 {H + 20} Z" fill="url(#hillfar)"/>')
o.append('<g>' + tree(250, H - 30, 0.5, "#7FA98C", far=True) + tree(780, H - 36, 0.55, "#7FA98C", far=True) + tree(812, H - 32, 0.4, "#7FA98C", far=True) + '</g>')
o.append(f'<path d="M 0 {H + 10} C 160 {H - 14}, 320 {H + 6}, 470 {H} C 640 {H - 8}, 820 {H + 20}, 1000 {H + 4} L 1000 700 L 0 700 Z" fill="url(#hill)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
o.append(f'<path d="M 0 {H + 70} C 200 {H + 40}, 420 {H + 70}, 620 {H + 60} C 780 {H + 52}, 900 {H + 70}, 1000 {H + 60} L 1000 700 L 0 700 Z" fill="url(#meadow)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
o.append(f'<path d="M 30 {H + 76} C 200 {H + 50}, 400 {H + 74}, 600 {H + 66}" fill="none" stroke="#B5EBA0" stroke-width="4" stroke-linecap="round" opacity="0.7"/>')
# camino serpenteante
o.append(f'<path d="M 130 700 C 230 640, 420 620, 470 580 C 520 540, 560 520, 600 {H + 6} L 616 {H + 6} C 590 530, 560 560, 520 600 C 460 650, 360 680, 330 700 Z" fill="url(#path)" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
o.append('<g fill="#B88D5A" opacity="0.8"><ellipse cx="300" cy="672" rx="9" ry="4"/><ellipse cx="455" cy="606" rx="6" ry="3"/><ellipse cx="540" cy="548" rx="4" ry="2"/></g>')
# charco
o.append(f'<ellipse cx="760" cy="620" rx="90" ry="20" fill="url(#puddle)" stroke="{INK}" stroke-width="5"/>'
         '<path d="M 700 616 L 780 612" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" opacity="0.8"/>')
o.append('<g id="ondas" fill="none" stroke="#FFFFFF" stroke-width="3"><g id="rip1"><ellipse cx="740" cy="622" rx="26" ry="6"/></g><g id="rip2"><ellipse cx="740" cy="622" rx="26" ry="6"/></g></g>')
# arbustos y flores en primer plano
o.append('<g id="arboles">' + tree(70, H + 96, 1.1, "#2E8B57") + tree(930, H + 92, 1.0, "#3FA066") + '</g>')
fl = []
for x, y, c in [(600, 660, "#FFD21F"), (630, 676, "#FF8FB1"), (880, 650, "#FFD21F"), (190, 610, "#FF8FB1"), (230, 628, "#FFFFFF")]:
    fl.append(f'<path d="M {x} {y} L {x} {y + 22}" stroke="{INK}" stroke-width="7"/><path d="M {x} {y} L {x} {y + 22}" stroke="#4FA34A" stroke-width="3"/>'
              f'<circle cx="{x}" cy="{y}" r="9" fill="{c}" stroke="{INK}" stroke-width="4"/><circle cx="{x}" cy="{y}" r="3" fill="#FF9F1A"/>')
o.append('<g id="flores">' + "".join(fl) + '</g>')
# persona de espaldas caminando hacia el arcoíris
o.append(person_back(395, 652, 0.78))
o.append(f'<ellipse cx="395" cy="654" rx="26" ry="6" fill="#1F4D27" opacity="0.35"/>')
o.append('</svg>')
open(sys.argv[1], "w").write("\n".join(o))

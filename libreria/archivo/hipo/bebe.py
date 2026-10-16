import sys, math
sys.path.insert(0, "/tmp/claude-0/-home-user-automatizacion-contenidos/039df981-7a17-5355-b711-18510fb209db/scratchpad/volcan")
from vlib import *
UX, UY, URX, URY = 500, 368, 340, 282
defs = "\n".join([
    lg("bg", [(0, "#FFE7DA"), (1, "#F6C9B6")]),
    rg("wall", [(0.8, "#F3A0AA"), (1, "#C9566C")], 0.5, 0.5, 0.5),
    rg("fluid", [(0, "#FFF1E4"), (0.7, "#FFD9C6"), (1, "#F7B9A6")], 0.45, 0.4, 0.6),
    rg("skin", [(0, "#FFE0CC"), (0.6, "#F7BFA0"), (1, "#E39A7A")], 0.4, 0.35, 0.75),
    rg("plac", [(0, "#C2465A"), (1, "#7A1E30")], 0.4, 0.4, 0.7),
    lg("cord", [(0, "#F2F0FF"), (1, "#C9C2E6")]),
    f'<clipPath id="ut"><ellipse cx="{UX}" cy="{UY}" rx="{URX - 30}" ry="{URY - 30}"/></clipPath>',
])
o = [head(defs)]
o.append('<rect width="1000" height="700" fill="url(#bg)"/>')
o.append('<g fill="#F2B8A4" opacity="0.6"><circle cx="90" cy="600" r="70"/><circle cx="930" cy="140" r="90"/><circle cx="120" cy="140" r="40"/></g>')
# útero
o.append(f'<ellipse cx="{UX}" cy="{UY}" rx="{URX}" ry="{URY}" fill="url(#wall)" stroke="{INK}" stroke-width="8"/>')
o.append(f'<ellipse cx="{UX}" cy="{UY}" rx="{URX - 30}" ry="{URY - 30}" fill="url(#fluid)" stroke="#B84A60" stroke-width="5"/>')
o.append(f'<path d="M {UX - 250} {UY - 150} C {UX - 180} {UY - 225}, {UX - 60} {UY - 250}, {UX + 40} {UY - 248}" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round" opacity="0.6"/>')
o.append('<g clip-path="url(#ut)">')
# placenta (arriba a la derecha)
o.append(f'<g transform="rotate(39 292 536)"><ellipse cx="292" cy="536" rx="92" ry="40" fill="url(#plac)" stroke="{INK}" stroke-width="6"/>'
         '<g fill="none" stroke="#E07A8A" stroke-width="3" opacity="0.8"><path d="M 252 530 q 20 -16 40 0"/><path d="M 296 524 q 18 -16 36 -2"/><path d="M 270 552 q 20 -12 40 0"/></g></g>')
# partículas en el líquido
o.append('<g id="motas" fill="#FFFFFF" opacity="0.7">' + "".join(f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x, y, r in [(260, 260, 5), (300, 560, 4), (720, 520, 6), (780, 380, 4), (520, 160, 4), (240, 420, 3)]) + '</g>')
o.append('</g>')
# feto (posición fetal, mirando a la izquierda)
o.append('<g id="feto">')
# pierna de atrás
o.append(f'<path d="M 650 470 C 610 500, 560 520, 520 528 C 540 560, 590 580, 640 586" fill="none" stroke="{INK}" stroke-width="58" stroke-linecap="round" stroke-linejoin="round"/>')
o.append(f'<path d="M 650 470 C 610 500, 560 520, 520 528 C 540 560, 590 580, 640 586" fill="none" stroke="#E8A486" stroke-width="44" stroke-linecap="round" stroke-linejoin="round"/>')
# cuerpo (judía)
body = smooth([(450, 330), (520, 276), (610, 270), (676, 316), (704, 400), (690, 476), (640, 520), (570, 520), (510, 492), (470, 450), (440, 400)], True)
o.append(f'<path d="{body}" fill="url(#skin)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
o.append('<path d="M 540 292 C 590 280, 640 292, 670 324" fill="none" stroke="#FFF0E4" stroke-width="6" stroke-linecap="round" opacity="0.8"/>')
o.append(f'<path d="M 560 300 C 620 300, 670 340, 684 400" fill="none" stroke="#E39A7A" stroke-width="4" stroke-linecap="round" opacity="0.6"/>')
# pierna de delante: muslo + pie
leg = "M 668 452 C 640 500, 580 530, 528 530 C 520 560, 560 588, 620 596"
o.append(f'<path d="{leg}" fill="none" stroke="{INK}" stroke-width="64" stroke-linecap="round" stroke-linejoin="round"/>')
o.append(f'<path d="{leg}" fill="none" stroke="#F7BFA0" stroke-width="50" stroke-linecap="round" stroke-linejoin="round"/>')
o.append('<path d="M 650 456 C 624 492, 584 512, 540 516" fill="none" stroke="#FFE6D6" stroke-width="7" stroke-linecap="round" opacity="0.8"/>')
o.append(f'<ellipse cx="628" cy="600" rx="34" ry="20" fill="url(#skin)" stroke="{INK}" stroke-width="6" transform="rotate(10 628 600)"/>')
o.append(f'<path d="M 650 592 L 656 604 M 640 590 L 646 606" stroke="#C9806A" stroke-width="3" stroke-linecap="round"/>')
# brazo hacia la cara
arm = "M 520 380 C 520 430, 500 466, 456 470"
o.append(f'<path d="{arm}" fill="none" stroke="{INK}" stroke-width="44" stroke-linecap="round" stroke-linejoin="round"/>')
o.append(f'<path d="{arm}" fill="none" stroke="#F7BFA0" stroke-width="31" stroke-linecap="round" stroke-linejoin="round"/>')
o.append(f'<circle cx="446" cy="470" r="22" fill="url(#skin)" stroke="{INK}" stroke-width="6"/>')
o.append(f'<path d="M 432 458 L 426 450 M 440 454 L 436 444" stroke="#C9806A" stroke-width="3" stroke-linecap="round"/>')
# cabeza
o.append('<g id="cabeza">')
o.append(f'<circle cx="380" cy="390" r="104" fill="url(#skin)" stroke="{INK}" stroke-width="7"/>')
o.append('<path d="M 310 330 C 340 300, 390 290, 430 304" fill="none" stroke="#FFF0E4" stroke-width="7" stroke-linecap="round" opacity="0.8"/>')
o.append(f'<path d="M 420 380 C 440 370, 452 392, 440 410 C 432 420, 420 414, 418 404" fill="#EBA88A" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>')
o.append(f'<path d="M 318 412 Q 334 422 350 412" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>')
o.append(f'<path d="M 296 432 Q 286 446 300 452" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>')
o.append(f'<g id="boca"><ellipse cx="320" cy="470" rx="9" ry="7" fill="#C25A60" stroke="{INK}" stroke-width="4"/></g>')
o.append('<ellipse cx="350" cy="440" rx="14" ry="8" fill="#F49A8A" opacity="0.55"/>')
o.append('</g>')
o.append('</g>')
# cordón umbilical (de la placenta al ombligo)
cd = smooth([(318, 530), (360, 540), (420, 566), (480, 556), (524, 512)])
o.append(f'<path d="{cd}" fill="none" stroke="{INK}" stroke-width="26" stroke-linecap="round"/><path d="{cd}" fill="none" stroke="url(#cord)" stroke-width="16" stroke-linecap="round"/>'
         f'<path d="{cd}" fill="none" stroke="#5A6FD8" stroke-width="4" stroke-linecap="round" transform="translate(-3 0)" opacity="0.7"/>'
         f'<path d="{cd}" fill="none" stroke="#E0475A" stroke-width="3" stroke-linecap="round" transform="translate(4 2)" opacity="0.7"/>')
# ondas cerebrales
o.append('<g id="ondas" fill="none" stroke="#0B0B14" stroke-width="12" stroke-linecap="round">'
         + "".join(f'<path d="M {380 + r * math.cos(a0):.0f} {390 + r * math.sin(a0):.0f} A {r} {r} 0 0 1 {380 + r * math.cos(a1):.0f} {390 + r * math.sin(a1):.0f}"/>' for r, a0, a1 in [(128, -2.3, -1.2), (150, -2.25, -1.25)]) + '</g>')
o.append('<g id="ondasc" fill="none" stroke="#C8FF2E" stroke-width="6" stroke-linecap="round">'
         + "".join(f'<path d="M {380 + r * math.cos(a0):.0f} {390 + r * math.sin(a0):.0f} A {r} {r} 0 0 1 {380 + r * math.cos(a1):.0f} {390 + r * math.sin(a1):.0f}"/>' for r, a0, a1 in [(128, -2.3, -1.2), (150, -2.25, -1.25)]) + '</g>')
o.append(f'<g id="hic"><path d="M 742 236 L 900 226 L 906 286 L 760 296 L 736 318 L 744 290 Z" fill="{LIME}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
         f'<text x="822" y="276" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="40" fill="{INK}" transform="rotate(-4 822 266)">¡HIC!</text></g>')
o.append('<g id="jolt" fill="none" stroke="#0B0B14" stroke-width="6" stroke-linecap="round"><path d="M 716 330 L 744 316"/><path d="M 724 372 L 756 370"/><path d="M 716 414 L 744 426"/></g>')
o.append(label("lcerebro", 520, 112, "CEREBRO", 436, 262))
o.append('</svg>')
open(sys.argv[1], "w").write("\n".join(o))

from lib import *
W, H = 1000, 820
defs = (lg("coin", [(0, "#FFE58A"), (0.5, "#F5C542"), (1, "#C99421")], 0, 0, 1, 0) +
        lg("cointop", [(0, "#FFF0B0"), (1, "#F2C23A")]))
o = [header(defs, W, H)]


def facet(p, col, sw=5):
    return f'<path d="{poly(p, True)}" fill="{col}" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"/>'


def crease(p, op=0.35):
    return f'<path d="{poly(p)}" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round" opacity="{op}"/>'


# ---------- rana de papel (hecha por el participante: algo torcida) ----------
fr = ['<ellipse cx="300" cy="436" rx="180" ry="18" fill="#000" opacity="0.25"/>']
# pata trasera lejana
fr.append(facet([(150, 420), (205, 352), (250, 428)], "#3E8F3A"))
# cuerpo
tail, hump, nose, belly, mid = (128, 418), (282, 228), (452, 352), (300, 428), (292, 372)
fr.append(facet([tail, hump, mid], "#8BD86A"))
fr.append(facet([hump, nose, mid], "#5DBB4C"))
fr.append(facet([tail, mid, nose, belly], "#3F9A3C"))
# pliegue torcido (chapuza) y arruga
fr.append(crease([(200, 330), (240, 300), (262, 344)], 0.4))
fr.append(crease([(330, 300), (352, 330)], 0.4))
fr.append(f'<path d="M 252 262 L 280 236" stroke="#D6FFC0" stroke-width="5" stroke-linecap="round"/>')
# pata delantera
fr.append(facet([(392, 372), (452, 352), (470, 432), (436, 432)], "#4FAE43"))
fr.append(facet([(436, 432), (470, 432), (486, 444), (430, 444)], "#3E8F3A", 4))
# pata trasera cercana (doblada)
fr.append(facet([(140, 418), (236, 330), (262, 432), (170, 440)], "#4FAE43"))
fr.append(crease([(236, 330), (200, 436)], 0.45))
# ojos dibujados a boli
fr.append(f'<circle cx="398" cy="314" r="13" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/><circle cx="401" cy="316" r="6" fill="{INK}"/>')
fr.append(f'<circle cx="372" cy="300" r="11" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/><circle cx="375" cy="302" r="5" fill="{INK}"/>')
# trozo de celo (para que no se abra)
fr.append(f'<g transform="rotate(-24 330 395)"><rect x="300" y="384" width="62" height="22" fill="#FFFFFF" opacity="0.55" stroke="#9FB3C8" stroke-width="2"/></g>')
FROG = "".join(fr)
# rana centrada (escena 1) y a la izquierda (escena 2, junto a la grulla)
o.append(f'<g id="rana"><g transform="translate(500 300) scale(1.75) translate(-300 -340)">{FROG}</g></g>')
o.append(f'<g id="rana2"><g transform="translate(255 330) scale(1.3) translate(-300 -340)">{FROG}</g></g>')

# ---------- grulla de experto ----------
cr = ['<g id="grulla"><g transform="translate(750 300) scale(1.25) translate(-740 -290)">', '<ellipse cx="740" cy="432" rx="150" ry="18" fill="#000" opacity="0.25"/>']
cx, cy = 740, 360
# ala lejana
cr.append(facet([(700, 330), (790, 330), (850, 120)], "#C93A24"))
# cola
cr.append(facet([(780, 360), (822, 352), (920, 214), (900, 212)], "#E0503A"))
# cuello y cabeza
cr.append(facet([(700, 360), (660, 352), (578, 214), (596, 210)], "#E0503A"))
cr.append(facet([(578, 214), (596, 210), (560, 236)], "#B8301C"))
# cuerpo
cr.append(facet([(660, 352), (740, 300), (822, 352), (740, 420)], "#FF6A4E"))
cr.append(facet([(660, 352), (740, 300), (740, 420)], "#FF8A70"))
cr.append(crease([(740, 300), (740, 420)], 0.4))
# ala cercana
cr.append(facet([(700, 334), (780, 334), (640, 116)], "#FF7A5E"))
cr.append(crease([(740, 334), (650, 132)], 0.35))
cr.append(f'<path d="M 660 140 L 690 200" stroke="#FFC2B2" stroke-width="5" stroke-linecap="round"/>')
cr.append('</g></g>')
o.append("".join(cr))

# ---------- pilas de monedas ----------
def stack(cxs, n, base=712, rx=70, ry=21, th=16):
    s = [f'<ellipse cx="{cxs}" cy="{base + 6}" rx="{rx + 18}" ry="{ry + 4}" fill="#000" opacity="0.25"/>']
    for k in range(n):
        y = base - k * th
        s.append(f'<path d="M {cxs - rx} {y - th} L {cxs - rx} {y} A {rx} {ry} 0 0 0 {cxs + rx} {y} L {cxs + rx} {y - th}" fill="url(#coin)" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
        s.append(f'<path d="M {cxs - rx + 10} {y - 2} L {cxs - rx + 10} {y - th + 6} M {cxs - 20} {y + ry - 4} L {cxs - 20} {y + ry - th + 2} M {cxs + 20} {y + ry - 4} L {cxs + 20} {y + ry - th + 2} M {cxs + rx - 10} {y - 2} L {cxs + rx - 10} {y - th + 6}" stroke="#A97A16" stroke-width="2.5" opacity="0.8"/>')
    yt = base - n * th
    s.append(f'<ellipse cx="{cxs}" cy="{yt}" rx="{rx}" ry="{ry}" fill="url(#cointop)" stroke="{INK}" stroke-width="5"/>')
    s.append(f'<ellipse cx="{cxs}" cy="{yt}" rx="{rx - 14}" ry="{ry - 6}" fill="none" stroke="#C99421" stroke-width="3"/>')
    s.append(f'<path d="M {cxs - 30} {yt - 6} Q {cxs - 10} {yt - 12} {cxs + 12} {yt - 10}" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" fill="none"/>')
    return "".join(s), yt


s1, t1 = stack(250, 9)
s2, t2 = stack(520, 2)
s3, t3 = stack(760, 10)
o.append(f'<g id="pila_tu">{s1}</g>')
o.append(f'<g id="pila_otros">{s2}</g>')
o.append(f'<g id="pila_exp">{s3}</g>')
l1, _ = tag("l_tu", 250, 772, "TÚ: 0,23 $", size=30)
l2, _ = tag("l_otros", 520, 772, "OTROS: 0,05 $", size=30)
l3, _ = tag("l_exp", 760, 772, "EXPERTO", size=30)
o += [l1, l2, l3]
o.append(f'<g id="badge"><path d="{star(780, 630, 100, 80, 20)}" fill="#C8FF2E" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>' + txt(780, 618, "CASI", 28) + txt(780, 664, "×5", 52) + '</g>')
# signo ≈ entre tu pila y la del experto
o.append(f'<g id="igual"><circle cx="505" cy="640" r="46" fill="#FFFFFF" stroke="{INK}" stroke-width="6"/>' + txt(505, 662, "≈", 62) + '</g>')
o.append('</svg>')
open("origami_free.svg", "w").write("\n".join(o))

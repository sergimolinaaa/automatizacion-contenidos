from rot import *

extra = (lg("bookC", [(0, "#2F5BD3"), (1, "#1A3A94")]) + lg("pagesG", [(0, "#FFFFFF"), (1, "#D9DCE5")], 0, 0, 1, 0)
         + lg("signB", [(0, "#3D8BFF"), (1, "#1F5FBF")]) + lg("deskG", [(0, "#D9A46C"), (1, "#B07A45")]))
o = [header(1000, 700, extra)]
o.append('<rect width="1000" height="700" fill="#EAF0FA"/>')
o.append('<rect x="0" y="560" width="1000" height="140" fill="url(#deskG)"/>')
o.append(f'<path d="M 0 560 L 1000 560" stroke="{INK}" stroke-width="6"/>')

# libro (de pie, ligeramente girado)
bx, by, bw, bh = 80, 120, 290, 420
book = f'<g transform="rotate(-4 {bx+bw/2} {by+bh})">'
book += f'<rect x="{bx+14}" y="{by+16}" width="{bw}" height="{bh}" rx="10" fill="{INK}" opacity="0.25"/>'
book += f'<rect x="{bx+bw-10}" y="{by+10}" width="34" height="{bh-16}" rx="6" fill="url(#pagesG)" stroke="{INK}" stroke-width="5"/>'
for k in range(6):
    book += f'<path d="M {bx+bw-4} {by+30+k*65} L {bx+bw+18} {by+30+k*65}" stroke="#B9C0CE" stroke-width="2"/>'
book += f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="12" fill="url(#bookC)" stroke="{INK}" stroke-width="7"/>'
book += f'<rect x="{bx+10}" y="{by}" width="16" height="{bh}" fill="#163080" opacity="0.6"/>'
book += f'<path d="M {bx+40} {by+14} L {bx+bw-24} {by+14}" stroke="#FFFFFF" stroke-width="4" opacity="0.4" stroke-linecap="round"/>'
book += f'<rect x="{bx+44}" y="{by+40}" width="{bw-80}" height="4" fill="#FFC83D"/>'
for i, t in enumerate(["REGLAMENTO", "GENERAL DE", "CIRCULACIÓN"]):
    book += T(bx + bw / 2 + 8, by + 90 + i * 40, t, 30, "#FFFFFF", font=MONO)
book += f'<rect x="{bx+44}" y="{by+206}" width="{bw-80}" height="4" fill="#FFC83D"/>'
# señal de rotonda (círculo azul con tres flechas giratorias)
sx, sy, sr = bx + bw / 2 + 8, by + 315, 72
book += f'<circle cx="{sx}" cy="{sy}" r="{sr}" fill="#FFFFFF" stroke="{INK}" stroke-width="6"/>'
book += f'<circle cx="{sx}" cy="{sy}" r="{sr-8}" fill="url(#signB)"/>'
for k in range(3):
    a0 = math.radians(90 + k * 120 + 20)
    a1 = math.radians(90 + k * 120 + 95)
    r = 36
    p0 = (sx + r * math.cos(a0), sy - r * math.sin(a0))
    p1 = (sx + r * math.cos(a1), sy - r * math.sin(a1))
    book += f'<path d="M {f(p0[0])} {f(p0[1])} A {r} {r} 0 0 0 {f(p1[0])} {f(p1[1])}" fill="none" stroke="#FFFFFF" stroke-width="11" stroke-linecap="round"/>'
    # punta de flecha en p1 (sentido antihorario)
    tx, ty = -math.sin(a1), -math.cos(a1)  # tangente antihoraria en pantalla
    tip = (p1[0] + tx * 16, p1[1] + ty * 16)
    nx, ny = math.cos(a1), -math.sin(a1)
    book += f'<path d="M {f(p1[0]+nx*12)} {f(p1[1]+ny*12)} L {f(tip[0])} {f(tip[1])} L {f(p1[0]-nx*12)} {f(p1[1]-ny*12)} Z" fill="#FFFFFF"/>'
book += "</g>"
o.append(g("libro", book))
s, _ = label("tlibro", 235, 618, "EL LIBRO DE NORMAS DEL TRÁFICO", bg=INK, fg=LIME, size=22); o.append(s)

# ficha del artículo
cx0, cy0, cw, ch = 440, 92, 510, 440
card = f'<rect x="{cx0+12}" y="{cy0+14}" width="{cw}" height="{ch}" rx="16" fill="{INK}" opacity="0.22"/>'
card += f'<rect x="{cx0}" y="{cy0}" width="{cw}" height="{ch}" rx="16" fill="url(#paperB)" stroke="{INK}" stroke-width="6"/>'
card += f'<path d="M {cx0} {cy0+16} Q {cx0} {cy0} {cx0+16} {cy0} L {cx0+cw-16} {cy0} Q {cx0+cw} {cy0} {cx0+cw} {cy0+16} L {cx0+cw} {cy0+70} L {cx0} {cy0+70} Z" fill="{INK}"/>'
card += T(cx0 + 24, cy0 + 47, "RGC · ART. 57.1.c", 28, LIME, anchor="start")
lines = ["«En las glorietas, los que", "se hallen dentro de la vía", "circular tendrán preferencia", "de paso sobre los que", "pretendan acceder a", "aquéllas.»"]
cw_ch = 26 * 0.6
lx, ly0, lh = cx0 + 26, cy0 + 122, 46
hl = {}
for i, t in enumerate(lines):
    for word in ("dentro", "preferencia"):
        j = t.find(word)
        if j >= 0:
            hl[word] = (lx + j * cw_ch - 4, ly0 + i * lh - 27, len(word) * cw_ch + 8, 36)
o_card = card
o.append(g("ficha", o_card + "".join(T(lx, ly0 + i * lh, t, 26, INK, anchor="start") for i, t in enumerate(lines))))
# subrayados (debajo del texto no se puede porque la ficha va entera; se usan marcos de rotulador encima, semitransparentes)
for k, (x, y, w, h) in hl.items():
    o.append(g(f"hl_{k}", f'<path d="M {f(x)} {f(y+h-4)} L {f(x+w)} {f(y+h-4)}" stroke="{LIME}" stroke-width="12" stroke-linecap="round" opacity="0.95"/>'
                + f'<path d="M {f(x)} {f(y+h+4)} L {f(x+w)} {f(y+h+4)}" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'))
o.append(g("pie", T(cx0 + 26, cy0 + ch - 22, "Real Decreto 1428/2003", 20, "#6B7385", anchor="start")))
# sello 57
o.append(g("sello", f'<g transform="rotate(-10 880 520)"><circle cx="880" cy="520" r="62" fill="#FFFFFF" stroke="{CORAL}" stroke-width="8"/>'
                     f'<circle cx="880" cy="520" r="50" fill="none" stroke="{CORAL}" stroke-width="3"/>' + T(880, 540, "57", 52, CORAL, font=DISP) + "</g>"))
o.append("</svg>")
save(OUT + "norma.svg", "\n".join(o))
print(hl)

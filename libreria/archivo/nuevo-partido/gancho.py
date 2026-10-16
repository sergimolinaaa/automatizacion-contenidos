from np import *

OUT = "gancho_full.svg"
defs = BASE_DEFS + NP_DEFS + lg("wallN", [(0, "#1E2A4A"), (1, "#33476F")]) + lg("stageG", [(0, "#B57A45"), (1, "#7A4E28")]) \
    + lg("curtG", [(0, "#C2324A"), (1, "#86182C")], 0, 0, 1, 0) + rg("burstY", [(0, "#FFF2A8"), (1, YEL)])
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920">\n<defs>{defs}</defs>']
o.append('<rect width="1080" height="1920" fill="url(#wallN)"/>')
# cortinas laterales
for k in (0, 1):
    x = 0 if k == 0 else 1080
    s = 1 if k == 0 else -1
    o.append(f'<path d="M {x} 0 L {x+s*150} 0 C {x+s*120} 500, {x+s*170} 900, {x+s*90} 1250 L {x} 1250 Z" fill="url(#curtG)" stroke="{INK}" stroke-width="7"/>')
    for j in (40, 85):
        o.append(f'<path d="M {x+s*j} 20 C {x+s*(j-10)} 500, {x+s*(j+15)} 900, {x+s*(j-20)} 1240" fill="none" stroke="#6E1022" stroke-width="5" opacity="0.7"/>')
# foco
o.append('<path d="M 470 0 L 610 0 L 640 1250 L 80 1250 Z" fill="url(#spotR)" opacity="0.9"/>')
o.append('<ellipse cx="360" cy="1262" rx="300" ry="40" fill="#FFF7D6" opacity="0.35"/>')
# escenario
o.append(f'<rect x="0" y="1250" width="1080" height="670" fill="url(#stageG)"/><path d="M 0 1250 L 1080 1250" stroke="{INK}" stroke-width="8"/>')
o.append('<g stroke="#5E3B1C" stroke-width="3" opacity="0.6">' + "".join(f'<line x1="0" y1="{y}" x2="1080" y2="{y}"/>' for y in (1330, 1440, 1580, 1760)) + "</g>")

# confeti
o.append(G("confeti", confetti(7, (190, 600, 900, 860), 26)))
# pancarta PARTIDO NUEVO
o.append(G("tnuevo", f'<path d="M 230 470 L 850 470 L 820 515 L 850 560 L 230 560 L 260 515 Z" fill="{LIME}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
           + T(540, 532, "¡PARTIDO NUEVO!", 46, INK, font=DISP)))
# atril
o.append(G("atril", lectern(360, 1252, 300, 330)))

# calendarios 10 OCT -> 29 NOV
o.append(cal_page(720, 720, 190, 210, "OCT", "10", id_="hoy", rot=-6))
o.append(cal_page(880, 1000, 220, 240, "NOV", "29", id_="nov", rot=5))
o.append(arrow("flecha", ((800, 700), (885, 860)), col=LIME, w=12, head=30, curve=(890, 700)))
s, _ = label("t50", 690, 920, "50 DÍAS", bg=CORAL, fg="#FFFFFF", size=36); o.append(s)

# bocadillos
def bubble(id_, cx, cy, text, size, tail):
    w = len(text) * size * 0.8 + 56
    h = size * 2.2
    x, y = cx - w / 2, cy - h / 2
    tx, ty = tail
    return G(id_, f'<rect x="{f(x+8)}" y="{f(y+10)}" width="{f(w)}" height="{f(h)}" rx="{f(h/2)}" fill="{INK}" opacity="0.3"/>'
             f'<path d="M {f(cx-30)} {f(y+h-4)} L {f(tx)} {f(ty)} L {f(cx+30)} {f(y+h-4)} Z" fill="#FFFFFF" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
             f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{f(h/2)}" fill="#FFFFFF" stroke="{INK}" stroke-width="7"/>'
             f'<path d="M {f(cx-28)} {f(y+h-8)} L {f(cx+28)} {f(y+h-8)}" stroke="#FFFFFF" stroke-width="10"/>'
             + T(cx, cy + size * 0.36, text, size, INK, font=DISP))
o.append(bubble("tque", 370, 660, "¿QUÉ PROPONE?", 40, (330, 790)))
o.append(bubble("ttiempo", 700, 1170, "¿LLEGA A TIEMPO?", 34, (840, 1110)))

# escena «ideas y papeles»
o.append(G("brillo", rays(360, 615, 125, 175, n=7, col=YEL, w=10)))
o.append(G("ideas", bulb(360, 615, 150)))
s, _ = label("tideas", 360, 425, "1 · IDEAS", bg=INK, fg=LIME, size=38); o.append(s)
o.append(G("papeles", folder(780, 990, 320, 240, "INSCRIPCIÓN")))
s, _ = label("tpapeles", 780, 800, "2 · PAPELES", bg=INK, fg=LIME, size=38); o.append(s)
o.append("</svg>")
save(OUT, "\n".join(o))

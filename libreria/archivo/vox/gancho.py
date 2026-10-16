from vx import *

OUT = "gancho_full.svg"
defs = BASE_DEFS + VX_DEFS + lg("wallN", [(0, "#1E2A4A"), (1, "#33476F")]) + lg("stageG", [(0, "#B57A45"), (1, "#7A4E28")]) \
    + lg("curtG", [(0, "#6C7A99"), (1, "#3E4A66")], 0, 0, 1, 0)
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920">\n<defs>{defs}</defs>']
o.append('<rect width="1080" height="1920" fill="url(#wallN)"/>')
for k in (0, 1):
    x = 0 if k == 0 else 1080
    s = 1 if k == 0 else -1
    o.append(f'<path d="M {x} 0 L {x+s*150} 0 C {x+s*120} 500, {x+s*170} 900, {x+s*90} 1250 L {x} 1250 Z" fill="url(#curtG)" stroke="{INK}" stroke-width="7"/>')
    for j in (40, 85):
        o.append(f'<path d="M {x+s*j} 20 C {x+s*(j-10)} 500, {x+s*(j+15)} 900, {x+s*(j-20)} 1240" fill="none" stroke="#2C3650" stroke-width="5" opacity="0.7"/>')
o.append('<path d="M 470 0 L 610 0 L 640 1250 L 80 1250 Z" fill="url(#spotR)" opacity="0.9"/>')
o.append('<ellipse cx="360" cy="1262" rx="300" ry="40" fill="#FFF7D6" opacity="0.35"/>')
o.append(f'<rect x="0" y="1250" width="1080" height="670" fill="url(#stageG)"/><path d="M 0 1250 L 1080 1250" stroke="{INK}" stroke-width="8"/>')
o.append('<g stroke="#5E3B1C" stroke-width="3" opacity="0.6">' + "".join(f'<line x1="0" y1="{y}" x2="1080" y2="{y}"/>' for y in (1330, 1440, 1580, 1760)) + "</g>")

# --- escena 0: gancho ---
o.append(G("tque", f'<path d="M 200 470 L 880 470 L 850 520 L 880 570 L 200 570 L 230 520 Z" fill="{LIME}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
           + T(540, 540, "GENERALES 2026", 50, INK, font=DISP)))
o.append(G("atril", lectern_vx(360, 1252, 300, 330)))
s, _ = label("tcand", 360, 735, "CANDIDATO: SANTIAGO ABASCAL", bg=INK, fg=LIME, size=24); o.append(s)
o.append(cal_page(800, 700, 200, 220, "NOV", "29", id_="nov", rot=6, col="url(#navyG)"))
s, _ = label("t29", 800, 860, "ELECCIONES", bg=CORAL, fg="#FFFFFF", size=26); o.append(s)
o.append(G("prog26", doc(720, 1050, 260, 330, "PROGRAMA", "2026", rot=4, band="url(#steelG)")))
o.append(G("aun", stamp(720, 1070, "AÚN NO", 44, rot=-12, col=CORAL)))
o.append(G("aun2", stamp(720, 1150, "PUBLICADO", 30, rot=-12, col=CORAL)))

# --- escena 1: el truco = leer el último programa ---
o.append(G("prog23", doc(540, 870, 440, 560, "PROGRAMA", "ELECCIONES 2023", rot=-3, lines=8)))
o.append(G("lupa", lupa(700, 980, 95)))
s, _ = label("tult", 540, 520, "ÚLTIMO PROGRAMA OFICIAL", bg=INK, fg=LIME, size=34); o.append(s)
s, _ = label("t23j", 540, 1225, "GENERALES · 23-J 2023", bg=CORAL, fg="#FFFFFF", size=30); o.append(s)
o.append("</svg>")
save(OUT, "\n".join(o))

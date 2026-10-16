import datetime
from np import *

OUT = "calendario_full.svg"
defs = BASE_DEFS + NP_DEFS + lg("wallK", [(0, "#FCE9C8"), (1, "#F2D29E")]) + lg("deskK", [(0, "#B98654"), (1, "#7E5430")]) \
    + lg("juntaG", [(0, "#5C78E8"), (1, "#2E47B8")])
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920">\n<defs>{defs}</defs>']
o.append('<rect width="1080" height="1920" fill="url(#wallK)"/>')
o.append('<g stroke="#EBC88C" stroke-width="4">' + "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="1300"/>' for x in range(60, 1080, 120)) + "</g>")
o.append(f'<rect x="0" y="1300" width="1080" height="620" fill="url(#deskK)"/><path d="M 0 1300 L 1080 1300" stroke="{INK}" stroke-width="8"/>')

# calendario de pared
X0, Y0, W, H = 130, 472, 820, 488
o.append(f'<rect x="{X0+12}" y="{Y0+16}" width="{W}" height="{H}" rx="26" fill="{INK}" opacity="0.25"/>')
o.append(f'<rect x="{X0}" y="{Y0}" width="{W}" height="{H}" rx="26" fill="url(#calG)" stroke="{INK}" stroke-width="8"/>')
o.append(f'<path d="M {X0} {Y0+100} L {X0} {Y0+26} Q {X0} {Y0} {X0+26} {Y0} L {X0+W-26} {Y0} Q {X0+W} {Y0} {X0+W} {Y0+26} L {X0+W} {Y0+100} Z" fill="url(#calR)" stroke="{INK}" stroke-width="8"/>')
o.append(T(X0 + W / 2, Y0 + 68, "OCTUBRE 2026", 46, "#FFFFFF", font=DISP))
for k in (0.2, 0.5, 0.8):
    o.append(f'<rect x="{X0+W*k-11}" y="{Y0-26}" width="22" height="52" rx="11" fill="#9AA3B5" stroke="{INK}" stroke-width="6"/>')
cw = (W - 40) / 7
rh = 62
gx, gy = X0 + 20, Y0 + 120
for i, d in enumerate("LMXJVSD"):
    o.append(T(gx + cw * i + cw / 2, gy + 30, d, 26, "#5A6170", font=DISP))
first = datetime.date(2026, 10, 1).weekday()
cells = {}
for day in range(1, 32):
    idx = first + day - 1
    r, c = idx // 7, idx % 7
    cx, cy = gx + c * cw + cw / 2, gy + 44 + r * rh + rh / 2
    cells[day] = (cx, cy)
    col = "#B3BAC8" if day < 10 else INK
    o.append(T(cx, cy + 12, str(day), 34, col, font=DISP))
# días pasados tachados levemente
o.append('<g stroke="#C9CFDA" stroke-width="4" stroke-linecap="round">' + "".join(
    f'<path d="M {f(cells[d][0]-22)} {f(cells[d][1]+10)} L {f(cells[d][0]+22)} {f(cells[d][1]-14)}"/>' for d in range(1, 10)) + "</g>")
# hoy = 10
hx, hy = cells[10]
o.append(G("hoy", f'<circle cx="{f(hx)}" cy="{f(hy)}" r="31" fill="none" stroke="{TEAL}" stroke-width="9"/>'))
s, _ = label("thoy", hx, hy - 52, "HOY", bg=TEAL, fg="#FFFFFF", size=26); o.append(s)
# rango 21-26
def seg(d1, d2):
    (x1, y1), (x2, _) = cells[d1], cells[d2]
    return (f'<rect x="{f(x1-cw/2+6)}" y="{f(y1-28)}" width="{f(x2-x1+cw-12)}" height="56" rx="28" fill="{LIME}" stroke="{INK}" stroke-width="6"/>'
            + "".join(T(cells[d][0], cells[d][1] + 12, str(d), 34, INK, font=DISP) for d in range(d1, d2 + 1)))
o.append(G("rango", seg(21, 25) + seg(26, 26)))
s, _ = label("tplazo", X0 + W / 2, Y0 + H + 40, "PLAZO: 21 → 26 OCT", bg=INK, fg=LIME, size=34); o.append(s)
# 29 noviembre no está en octubre: chincheta de recordatorio
o.append(G("nota", f'<g transform="rotate(8 880 500)"><rect x="800" y="440" width="170" height="130" rx="8" fill="#FFE97A" stroke="{INK}" stroke-width="6"/>'
           + T(885, 495, "29-N", 40, INK, font=DISP) + T(885, 540, "ELECCIONES", 20, "#5A6170") + "</g>"
           f'<circle cx="885" cy="448" r="13" fill="{CORAL}" stroke="{INK}" stroke-width="4"/>'))

# lista de candidatura
LX, LY, LW, LH = 290, 1148, 290, 210
l = f'<g transform="rotate(-5 {LX} {LY})">'
l += f'<rect x="{LX-LW/2+10}" y="{LY-LH/2+14}" width="{LW}" height="{LH}" rx="12" fill="{INK}" opacity="0.25"/>'
l += f'<rect x="{LX-LW/2}" y="{LY-LH/2}" width="{LW}" height="{LH}" rx="12" fill="url(#cardG)" stroke="{INK}" stroke-width="7"/>'
l += f'<rect x="{LX-LW/2}" y="{LY-LH/2}" width="{LW}" height="62" rx="12" fill="url(#tealG)" stroke="{INK}" stroke-width="6"/>'
l += logo(LX - LW / 2 + 36, LY - LH / 2 + 31, 22, sw=4)
l += T(LX + 22, LY - LH / 2 + 42, "CANDIDATURA", 24, "#FFFFFF", font=DISP)
for i in range(5):
    yy = LY - LH / 2 + 88 + i * 26
    l += T(LX - LW / 2 + 30, yy + 8, f"{i+1}.", 22, INK, font=DISP)
    l += f'<path d="M {LX-LW/2+64} {yy} L {LX+LW/2-(30 if i % 2 else 70)} {yy}" stroke="#9AA3B5" stroke-width="10" stroke-linecap="round"/>'
l += "</g>"
o.append(G("lista", l))
s, _ = label("tdef", 760, 1040, "= LISTA DE CANDIDATOS", target=(420, 1080), src=(600, 1040), bg=CORAL, fg="#FFFFFF", size=24); o.append(s)
# junta electoral
JX, JY = 800, 1172
o.append(G("junta", f'<rect x="{JX-150+8}" y="{JY-80+10}" width="300" height="160" rx="18" fill="{INK}" opacity="0.25"/>'
           f'<rect x="{JX-150}" y="{JY-80}" width="300" height="160" rx="18" fill="url(#juntaG)" stroke="{INK}" stroke-width="7"/>'
           f'<path d="M {JX-110} {JY-40} L {JX} {JY-66} L {JX+110} {JY-40} Z" fill="#FFFFFF" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
           + "".join(f'<rect x="{JX+k*40-8}" y="{JY-36}" width="16" height="50" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/>' for k in (-2, -1, 0, 1, 2))
           + T(JX, JY + 50, "JUNTA ELECTORAL", 24, "#FFFFFF", font=DISP)))
o.append(arrow("fl", ((455, 1175), (630, 1175)), col=LIME, w=12, head=30, curve=(545, 1130)))
o.append("</svg>")
save(OUT, "\n".join(o))

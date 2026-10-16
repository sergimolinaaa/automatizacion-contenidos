import datetime, random
from vx import *

OUT = "calendario_full.svg"
defs = BASE_DEFS + VX_DEFS + lg("wallK", [(0, "#FCE9C8"), (1, "#F2D29E")]) + lg("deskK", [(0, "#B98654"), (1, "#7E5430")])
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920">\n<defs>{defs}</defs>']
o.append('<rect width="1080" height="1920" fill="url(#wallK)"/>')
o.append('<g stroke="#EBC88C" stroke-width="4">' + "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="1300"/>' for x in range(60, 1080, 120)) + "</g>")
o.append(f'<rect x="0" y="1300" width="1080" height="620" fill="url(#deskK)"/><path d="M 0 1300 L 1080 1300" stroke="{INK}" stroke-width="8"/>')

# pregunta
o.append(G("tpreg", f'<path d="M 190 360 L 890 360 L 860 405 L 890 450 L 190 450 L 220 405 Z" fill="{LIME}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
           + T(540, 420, "¿Y PARA PRESENTARSE?", 40, INK, font=DISP)))

# calendario de pared
X0, Y0, W, H = 150, 500, 780, 400
o.append(f'<rect x="{X0+12}" y="{Y0+16}" width="{W}" height="{H}" rx="26" fill="{INK}" opacity="0.25"/>')
o.append(f'<rect x="{X0}" y="{Y0}" width="{W}" height="{H}" rx="26" fill="url(#calG)" stroke="{INK}" stroke-width="8"/>')
o.append(f'<path d="M {X0} {Y0+96} L {X0} {Y0+26} Q {X0} {Y0} {X0+26} {Y0} L {X0+W-26} {Y0} Q {X0+W} {Y0} {X0+W} {Y0+26} L {X0+W} {Y0+96} Z" fill="url(#navyG)" stroke="{INK}" stroke-width="8"/>')
o.append(T(X0 + W / 2, Y0 + 66, "OCTUBRE 2026", 44, "#FFFFFF", font=DISP))
for k in (0.2, 0.5, 0.8):
    o.append(f'<rect x="{X0+W*k-11}" y="{Y0-26}" width="22" height="52" rx="11" fill="#9AA3B5" stroke="{INK}" stroke-width="6"/>')
cw = (W - 40) / 7
rh = 50
gx, gy = X0 + 20, Y0 + 100
for i, d in enumerate("LMXJVSD"):
    o.append(T(gx + cw * i + cw / 2, gy + 28, d, 26, "#5A6170", font=DISP))
first = datetime.date(2026, 10, 1).weekday()
cells = {}
for day in range(1, 32):
    idx = first + day - 1
    r, c = idx // 7, idx % 7
    cx, cy = gx + c * cw + cw / 2, gy + 40 + r * rh + rh / 2
    cells[day] = (cx, cy)
    o.append(T(cx, cy + 12, str(day), 32, INK, font=DISP))
def seg(d1, d2):
    (x1, y1), (x2, _) = cells[d1], cells[d2]
    return (f'<rect x="{f(x1-cw/2+6)}" y="{f(y1-27)}" width="{f(x2-x1+cw-12)}" height="54" rx="27" fill="{LIME}" stroke="{INK}" stroke-width="6"/>'
            + "".join(T(cells[d][0], cells[d][1] + 12, str(d), 32, INK, font=DISP) for d in range(d1, d2 + 1)))
o.append(G("rango", seg(21, 25) + seg(26, 26)))
s, _ = label("tplazo", X0 + W / 2, Y0 + H + 40, "LISTAS: 21 → 26 OCT", bg=INK, fg=LIME, size=34); o.append(s)

# hemiciclo esquemático (escritorio, izquierda)
HX, HY = 290, 1188
n = 70
cols = ["#C9CFDA"] * n
for i in range(4, n, 10):   # ~1 de cada 10 escaños (33 de 350), en color neutro
    cols[i] = NAVY
seats = hemiciclo(HX, HY, n, 4, 90, 180, cols, 11, sw=3)
hb = f'<path d="M {HX-205} {HY+14} A 205 205 0 0 1 {HX+205} {HY+14} Z" fill="#F6EBD9" stroke="{INK}" stroke-width="6"/>'
o.append(G("hemi", hb + "".join(s for s, _, _ in seats)))
s, _ = label("tesc", HX, HY + 50, "33 ESCAÑOS EN 2023", bg=NAVY, fg="#FFFFFF", size=28); o.append(s)
s, _ = label("tdefesc", HX, HY + 106, "ESCAÑO = ASIENTO DEL CONGRESO", bg=INK, fg=LIME, size=22); o.append(s)

# portapapeles de firmas tachado (derecha)
KX, KY, KW, KH = 815, 1118, 220, 270
rnd = random.Random(5)
k = f'<g transform="rotate(5 {KX} {KY})">'
k += f'<rect x="{KX-KW/2+10}" y="{KY-KH/2+14}" width="{KW}" height="{KH}" rx="16" fill="{INK}" opacity="0.25"/>'
k += f'<rect x="{KX-KW/2}" y="{KY-KH/2}" width="{KW}" height="{KH}" rx="16" fill="url(#clipG)" stroke="{INK}" stroke-width="7"/>'
k += f'<rect x="{KX-KW/2+18}" y="{KY-KH/2+30}" width="{KW-36}" height="{KH-48}" rx="6" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/>'
k += f'<rect x="{KX-40}" y="{KY-KH/2-14}" width="80" height="36" rx="10" fill="#9AA3B5" stroke="{INK}" stroke-width="6"/>'
k += T(KX, KY - KH / 2 + 66, "FIRMAS", 24, INK, font=DISP)
for i in range(5):
    yy = KY - KH / 2 + 100 + i * 36
    x0 = KX - KW / 2 + 40 + rnd.uniform(0, 20)
    k += f'<path d="{smooth([(x0 + j * 22, yy + rnd.uniform(-8, 6)) for j in range(7)])}" fill="none" stroke="#2F4BD6" stroke-width="4" stroke-linecap="round"/>'
k += "</g>"
o.append(G("firmas", k))
o.append(G("cruz", dbl(f"M {KX-95} {KY-110} L {KX+95} {KY+110} M {KX+95} {KY-110} L {KX-95} {KY+110}", 26, CORAL, 9)))
s, _ = label("tnofirm", KX, KY + 180, "NO NECESITA FIRMAS", bg=CORAL, fg="#FFFFFF", size=26); o.append(s)
o.append("</svg>")
save(OUT, "\n".join(o))

from pn import *

OUT = "senado_full.svg"
o = [header(1080, 1920, SEPIA + lg("wallS", [(0, "#F2E9FF"), (1, "#D9CCF2")]) + lg("floorG", [(0, "#C98B55"), (1, "#8A5A31")]))]
o.append('<rect width="1080" height="1920" fill="url(#wallS)"/>')
o.append('<g stroke="#E2D6F5" stroke-width="3">' + "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="1320"/>' for x in range(60, 1080, 120)) + "</g>")
o.append('<rect x="0" y="1320" width="1080" height="600" fill="url(#woodG)"/>')
o.append(f'<path d="M 0 1320 L 1080 1320" stroke="{INK}" stroke-width="7"/>')
BX, BY, BW, BH = 540, 900, 600, 700
x0, y0 = BX - BW / 2, BY - BH / 2
b = f'<rect x="{x0+16}" y="{y0+18}" width="{BW}" height="{BH}" rx="14" fill="{INK}" opacity="0.2"/>'
b += f'<rect x="{x0}" y="{y0}" width="{BW}" height="{BH}" rx="14" fill="url(#sepiaG)" stroke="{INK}" stroke-width="8"/>'
b += f'<rect x="{x0+30}" y="{y0+28}" width="{BW-60}" height="92" rx="10" fill="#8B5E34" stroke="{INK}" stroke-width="6"/>'
b += T(BX, y0 + 92, "SENADO", 50, "#FFF4DD", font=DISP)
shapes = ["star", "circle", "tri", "square", "diamond", "star"]
rows = []
for i, sh in enumerate(shapes):
    yy = y0 + 180 + i * 88
    rows.append(yy)
    b += f'<rect x="{x0+48}" y="{yy-30}" width="60" height="60" rx="8" fill="#FFFFFF" stroke="{INK}" stroke-width="6"/>'
    b += f'<circle cx="{x0+160}" cy="{yy}" r="30" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/>' + icon(sh, x0 + 160, yy + 1, 18, PCOL[sh], sw=3)
    b += f'<path d="M {x0+215} {yy} L {x0+BW-(60 if i%2 else 130)} {yy}" stroke="#A88A5E" stroke-width="22" stroke-linecap="round"/>'
o.append(g("papeleta", b))
marks = [0, 2, 3, 5]
for k, i in enumerate(marks):
    o.append(xmark(x0 + 78, rows[i], 22, col=BLUE, sw=10, id_=f"c{k+1}"))
s, _ = label("thasta", 540, 470, "HASTA 3 CRUCES", bg=LIME, fg=INK, size=34); o.append(s)
s, _ = label("tok", 930, 1160, "VÁLIDO", bg=LIME, fg=INK, size=30); o.append(s)
o.append(check(930, 1060, 58, id_="okv"))
o.append(stamp2(600, 1020, "NULO", 96, rot=-12, id_="nulo"))
o.append(pen(x0 + 100, rows[5] + 18, 170, rot=-40, id_="boli"))
o.append("</svg>")
save(OUT, "\n".join(o))

from hc import *

OUT = "termos.svg"
o = [header(1000, 700, lg("wallP", [(0, "#FFF6E8"), (1, "#F3E2C8")]) + lg("frostG", [(0, "#E6F6FF"), (1, "#A9D8F2")]) + lg("appG", [(0, "#FFFFFF"), (1, "#DCE2EA")], 0, 0, 1, 0))]
o.append('<rect width="1000" height="700" fill="url(#wallP)"/>')
o.append('<rect x="0" y="590" width="1000" height="110" fill="url(#woodG2)"/>')
o.append(f'<path d="M 0 590 L 1000 590" stroke="{INK}" stroke-width="7"/>')
o.append('<path d="M 0 600 L 1000 600" stroke="#F3D3A6" stroke-width="4"/>')

# ---------- congelador ----------
FX0, FY0, FX1, FY1 = 50, 100, 330, 585
fz = []
fz.append(f'<rect x="{FX0+10}" y="{FY0+12}" width="{FX1-FX0}" height="{FY1-FY0}" rx="22" fill="{INK}" opacity="0.18"/>')
fz.append(f'<rect x="{FX0}" y="{FY0}" width="{FX1-FX0}" height="{FY1-FY0}" rx="22" fill="url(#appG)" stroke="{INK}" stroke-width="7"/>')
fz.append(f'<rect x="{FX0+24}" y="{FY0+24}" width="{FX1-FX0-48}" height="{FY1-FY0-48}" rx="12" fill="url(#frostG)" stroke="{INK}" stroke-width="5"/>')
for y in (250, 400):
    fz.append(f'<path d="M {FX0+24} {y} L {FX1-24} {y}" stroke="#7FA9C4" stroke-width="7"/>')
rnd = random.Random(4)
for _ in range(16):
    x, y = rnd.uniform(FX0 + 40, FX1 - 40), rnd.uniform(FY0 + 40, FY1 - 50)
    r = rnd.uniform(5, 10)
    fz.append(f'<path d="M {f(x-r)} {f(y)} L {f(x+r)} {f(y)} M {f(x)} {f(y-r)} L {f(x)} {f(y+r)} M {f(x-r*0.7)} {f(y-r*0.7)} L {f(x+r*0.7)} {f(y+r*0.7)} M {f(x+r*0.7)} {f(y-r*0.7)} L {f(x-r*0.7)} {f(y+r*0.7)}" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/>')
fz.append(f'<path d="M {FX0+40} {FY0+40} L {FX0+40} {FY1-60}" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round" opacity="0.7"/>')
# escarcha arriba
icicles = "M " + " L ".join(f"{f(FX0+24+i*20)} {f(FY0+24 + (16 if i%2 else 0))}" for i in range(12))
fz.append(f'<path d="{icicles}" fill="none" stroke="#FFFFFF" stroke-width="6" stroke-linejoin="round"/>')
o.append(g("congelador", "".join(fz)))
# bandeja de cubitos (balda de abajo)
tray = f'<rect x="{FX0+46}" y="{FY0+392}" width="196" height="40" rx="8" fill="#9ED7F5" stroke="{INK}" stroke-width="5"/>'
for i in range(3):
    tray += cube(FX0 + 82 + i * 62, FY0 + 372, 48, 0, seed=10 + i, bubbles=1, sw=4)
o.append(g("bandeja", tray))
# vaho frío
o.append(g("vaho", "".join(f'<path d="{smooth([(x, 300), (x+18, 270), (x-6, 240), (x+14, 210)])}" fill="none" stroke="#FFFFFF" stroke-width="9" stroke-linecap="round" opacity="0.85"/>' for x in (130, 190, 250))))
# termómetro frío
o.append(g("termoF", thermo(395, 150, 330, 0.1, "#3E95E0", id_fill="fillF")))
s, _ = label("lfrio", 225, 618, "18 BAJO CERO", bg="#3E95E0", fg="#FFFFFF", size=32); o.append(s)

# ---------- bebida ----------
GX, GT, GB = 705, 300, 575
gr_t, gr_b = 95, 78
gs = 360
bev = f'<ellipse cx="{GX+10}" cy="{GB+6}" rx="{gr_b+30}" ry="10" fill="#6B4A25" opacity="0.3"/>'
gbody = f"M {GX-gr_t} {GT} L {GX-gr_b} {GB} A {gr_b} 14 0 0 0 {GX+gr_b} {GB} L {GX+gr_t} {GT}"
rsx = gr_t + (gr_b - gr_t) * (gs - GT) / (GB - GT)
bev += f'<path d="{gbody} A {gr_t} 16 0 0 0 {GX-gr_t} {GT} Z" fill="url(#glassB)"/>'
bev += f'<path d="M {f(GX-rsx)} {gs} L {GX-gr_b+5} {GB-4} A {gr_b-5} 12 0 0 0 {GX+gr_b-5} {GB-4} L {f(GX+rsx)} {gs} Z" fill="url(#sodaG)"/>'
bev += f'<ellipse cx="{GX}" cy="{gs}" rx="{f(rsx-3)}" ry="14" fill="url(#sodaS)" stroke="{INK}" stroke-width="4"/>'
rnd = random.Random(7)
bev += "".join(f'<circle cx="{f(GX+rnd.uniform(-60,60))}" cy="{f(rnd.uniform(400,550))}" r="{f(rnd.uniform(3,6))}" fill="#FFF3CF" stroke="#C9741B" stroke-width="2"/>' for _ in range(9))
bev += f'<path d="{gbody}" fill="none" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
bev += f'<ellipse cx="{GX}" cy="{GT}" rx="{gr_t}" ry="16" fill="none" stroke="{INK}" stroke-width="7"/>'
bev += f'<path d="M {GX-gr_t+18} {GT+30} L {GX-gr_b+16} {GB-30}" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round" opacity="0.75"/>'
o.append(g("bebida", bev))
o.append(g("termoC", thermo(880, 150, 330, 0.62, "#E8452E", id_fill="fillC")))
s, _ = label("lcalor", 775, 618, "MÁS TEMPLADA", bg=CORAL, fg="#FFFFFF", size=32); o.append(s)

# ---------- choque en medio ----------
bolt = "M 545 170 L 500 300 L 545 300 L 505 430 L 600 270 L 552 270 L 590 170 Z"
o.append(g("rayo", "<g transform=\"translate(-48 0)\">" + f'<path d="{bolt}" fill="{INK}" opacity="0.25" transform="translate(8 8)"/><path d="{bolt}" fill="{YEL}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
           f'<path d="M 560 186 L 528 280" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round" opacity="0.8"/></g>'))
o.append("</svg>")
save(OUT, "\n".join(o))

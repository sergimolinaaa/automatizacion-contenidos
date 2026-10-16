from metro import *
T = G = 44
R1, R2 = 230, 330
Z = 140   # el cero real (misma x en los dos casos)
PX = 70   # px por cm
o = [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 700">
<defs>{DEFS}
<linearGradient id="plaster" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#E9E2D8"/><stop offset="1" stop-color="#CFC4B4"/></linearGradient>
<linearGradient id="top" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F7F2EA"/><stop offset="1" stop-color="#ECE3D6"/></linearGradient>
<linearGradient id="bot" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#EEF5FB"/><stop offset="1" stop-color="#DCE8F2"/></linearGradient>
</defs>
<rect width="1000" height="360" fill="url(#top)"/><rect y="360" width="1000" height="340" fill="url(#bot)"/>
<line x1="0" y1="360" x2="1000" y2="360" stroke="{INK}" stroke-width="5"/>
''']
def rivet(rx, ty, by):
    return (f'<rect x="{rx-16}" y="{ty-4}" width="32" height="{by-ty+8}" fill="#9AA3B1" stroke="{INK}" stroke-width="4"/>'
            f'<path d="M {rx-40} {ty} C {rx-36} {ty-18} {rx+36} {ty-18} {rx+40} {ty} Z" fill="url(#rivet)" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
            f'<path d="M {rx-36} {by} C {rx-32} {by+14} {rx+32} {by+14} {rx+36} {by} Z" fill="url(#rivet)" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
def blade(by0, by1):
    s = [f'<rect x="{Z+G}" y="{by0}" width="900" height="{by1-by0}" fill="url(#blade)" stroke="{INK}" stroke-width="5"/>']
    for mm in range(2, 130):
        x = Z + mm * PX / 10
        if x > 1000: break
        L = 10 if mm % 10 == 0 else (7 if mm % 5 == 0 else 4)
        s.append(f'<line x1="{x:.1f}" y1="{by0+2}" x2="{x:.1f}" y2="{by0+2+L}" stroke="{INK}" stroke-width="{2.2 if mm%10==0 else 1.3}"/>')
    for c in range(4, 13):
        x = Z + c * PX
        if x < 980:
            s.append(f'<text x="{x}" y="{by0-12}" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="24" fill="#6B5A20">{c}</text>')
    return "".join(s)
def hook(x0, ty, by, drop, segs):
    s = [f'<path d="M {x0+T} {ty} L {x0+12} {ty} Q {x0} {ty} {x0} {ty+12} L {x0} {drop} L {x0+T} {drop} Z" fill="url(#steelh)" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>']
    for a, b in segs:
        s.append(f'<rect x="{a}" y="{ty}" width="{b-a}" height="{T}" fill="url(#steel)" stroke="{INK}" stroke-width="5"/>')
    s.append(f'<line x1="{x0+8}" y1="{ty+6}" x2="{segs[-1][1]-4}" y2="{ty+6}" stroke="#FFFFFF" stroke-width="3" opacity="0.8"/>')
    return "".join(s)

# ---------- A: tirando (medida exterior)
A_B0, A_B1 = 220, 236
o.append(f'<g id="tabla"><rect x="{Z}" y="{A_B1}" width="640" height="96" fill="url(#wood)" stroke="{INK}" stroke-width="6"/>'
         f'<path d="M {Z+30} {A_B1+30} C {Z+200} {A_B1+20} {Z+400} {A_B1+40} {Z+620} {A_B1+28} M {Z+40} {A_B1+66} C {Z+260} {A_B1+56} {Z+420} {A_B1+76} {Z+620} {A_B1+62}" fill="none" stroke="#B57A42" stroke-width="3" opacity="0.6"/></g>')
o.append(f'<g id="cintaA">{blade(A_B0, A_B1)}</g>')
o.append('<g id="ganchoA">' + hook(Z - G, A_B0 - T, A_B0, A_B1 + 82, [(Z - G + T - 4, R1 - 16 - G), (R1 + 16, R2 - 16 - G), (R2 + 16, 380)]) + '</g>')
o.append('<g id="remA">' + rivet(R1, A_B0 - T, A_B1) + rivet(R2, A_B0 - T, A_B1) + '</g>')
o.append(f'<g id="huecoA"><rect x="{Z+3}" y="{A_B0}" width="{G-6}" height="{A_B1-A_B0}" fill="{LIME}" stroke="{INK}" stroke-width="3"/></g>')
o.append(arrow("tira", 540, 180, 740, 180, CORAL, w=14, head=32))
o.append(tag("ltira", 560, 96, 230, "TIRANDO", bg=CORAL, fg=INK))
o.append(tag("lsale", 250, 96, 260, "SALE HACIA FUERA", Z + 120, 154, Z + 10, A_B0 + 8, fs=24))

# ---------- B: empujando (medida interior)
B_B0, B_B1 = 500, 516
o.append(f'<g id="pared"><rect x="-10" y="380" width="{Z+10}" height="330" fill="url(#plaster)" stroke="{INK}" stroke-width="6"/>' +
         "".join(f'<path d="M 0 {y} L {Z} {y}" stroke="#BDB09C" stroke-width="3"/>' for y in (430, 500, 570, 640)) +
         "".join(f'<path d="M {x} {y} L {x} {y+70}" stroke="#BDB09C" stroke-width="3"/>' for x, y in ((60, 430), (100, 500), (40, 570))) + '</g>')
o.append(f'<g id="cintaB">{blade(B_B0, B_B1)}</g>')
o.append('<g id="ganchoB">' + hook(Z, B_B0 - T, B_B0, B_B1 + 82, [(Z + T - 4, R1 - 16), (R1 + 16 + G, R2 - 16), (R2 + 16 + G, 424)]) + '</g>')
o.append('<g id="remB">' + rivet(R1, B_B0 - T, B_B1) + rivet(R2, B_B0 - T, B_B1) + '</g>')
o.append(arrow("empuja", 760, 430, 560, 430, CORAL, w=14, head=32))
o.append(tag("lempuja", 550, 580, 270, "EMPUJANDO", bg=CORAL, fg=INK))
o.append(tag("lentra", 250, 580, 270, "SE METE DENTRO", Z + 60, 580, Z + 24, B_B1 + 50, fs=24))

# ---------- el cero
o.append(f'<g id="cero">' + "".join(f'<rect x="{Z-3}" y="{y}" width="6" height="16" rx="3" fill="{INK}"/>' for y in range(116, 640, 28)) +
         f'<circle cx="{Z}" cy="104" r="0" fill="none"/></g>')
o.append(f'<g id="lcero"><rect x="{Z-56}" y="644" width="112" height="0" fill="none"/>'
         f'<circle cx="{Z+60}" cy="{(A_B1+B_B0)/2+12:.0f}" r="44" fill="{LIME}" stroke="{INK}" stroke-width="5"/>'
         f'<text x="{Z+60}" y="{(A_B1+B_B0)/2+30:.0f}" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="50" fill="{INK}">0</text>'
         f'<path d="M {Z+16} {(A_B1+B_B0)/2+12:.0f} L {Z+4} {(A_B1+B_B0)/2+12:.0f}" stroke="{INK}" stroke-width="5"/></g>')
o.append('</svg>')
open("medidas.svg", "w").write("\n".join(o))

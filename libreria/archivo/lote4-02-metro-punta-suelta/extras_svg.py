from metro import *
o = [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 700">
<defs>{DEFS}
<linearGradient id="ply" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#E8C38C"/><stop offset="1" stop-color="#CF9E62"/></linearGradient>
<linearGradient id="top" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#EEF5FB"/><stop offset="1" stop-color="#DCE8F2"/></linearGradient>
<linearGradient id="nail" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E9EDF2"/><stop offset="1" stop-color="#7F8898"/></linearGradient>
<clipPath id="ins"><circle cx="560" cy="275" r="72"/></clipPath>
</defs>
<rect width="1000" height="372" fill="url(#top)"/><rect y="372" width="1000" height="328" fill="#F7F2EA"/>
<line x1="0" y1="372" x2="1000" y2="372" stroke="{INK}" stroke-width="5"/>
''']
# ---------- arriba: clavo en la pared
o.append(f'<g id="pared"><rect x="-10" y="70" width="180" height="300" fill="url(#ply)" stroke="{INK}" stroke-width="6"/>'
         '<path d="M 30 70 L 30 370 M 100 70 L 100 370" stroke="#B9874F" stroke-width="3" opacity="0.6"/>'
         '<path d="M 60 120 c 10 30 -10 60 0 90 M 140 160 c 8 30 -8 50 0 80" fill="none" stroke="#B9874F" stroke-width="3" opacity="0.6"/></g>')
NY = 262
o.append('<g id="clavo">')
o.append(f'<rect x="168" y="{NY-6}" width="90" height="12" fill="url(#nail)" stroke="{INK}" stroke-width="4"/>')
o.append('</g>')
# gancho colgado del clavo + cinta hacia la derecha
o.append('<g id="gancho">')
o.append(f'<path d="M 222 300 L 222 196 Q 222 182 236 182 L 330 182 L 330 200 L 240 200 L 240 300 Z" fill="url(#steelh)" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
o.append(f'<rect x="240" y="200" width="640" height="12" fill="url(#blade)" stroke="{INK}" stroke-width="4"/>')
for rx in (270, 308):
    o.append(f'<path d="M {rx-16} 182 C {rx-14} 172 {rx+14} 172 {rx+16} 182 Z" fill="url(#rivet)" stroke="{INK}" stroke-width="4"/>')
o.append('</g>')
o.append(f'<g id="cabeza"><ellipse cx="258" cy="{NY}" rx="8" ry="24" fill="url(#nail)" stroke="{INK}" stroke-width="5"/></g>')
# carcasa a la derecha (parcial)
o.append(f'<path d="M 870 120 Q 870 100 890 100 L 1010 100 L 1010 300 L 890 300 Q 870 300 870 280 Z" fill="url(#case)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
         f'<rect x="862" y="190" width="24" height="32" rx="6" fill="url(#rub)" stroke="{INK}" stroke-width="5"/><circle cx="960" cy="200" r="58" fill="#F2B60F" stroke="{INK}" stroke-width="5"/>')
# lupa: vista de frente de la pestaña con su agujero
o.append('<g id="lupa">')
o.append(f'<line x1="245" y1="{NY}" x2="492" y2="262" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>')
o.append(f'<circle cx="560" cy="275" r="72" fill="#FFFFFF"/>')
o.append('<g clip-path="url(#ins)">'
         f'<rect x="480" y="190" width="160" height="200" fill="url(#ply)"/>'
         f'<rect x="512" y="200" width="96" height="170" rx="10" fill="url(#steel)" stroke="{INK}" stroke-width="5"/>'
         f'<rect x="540" y="258" width="40" height="44" rx="20" fill="#5D6676" stroke="{INK}" stroke-width="4"/>'
         f'<circle cx="560" cy="276" r="15" fill="url(#rivet)" stroke="{INK}" stroke-width="4"/></g>')
o.append(f'<circle cx="560" cy="275" r="72" fill="none" stroke="{INK}" stroke-width="7"/>')
o.append('</g>')
o.append(tag("lagujero", 480, 96, 200, "AGUJERO", 580, 154, 576, 262))
o.append(tag("lclavo", 300, 280, 140, "CLAVO", 300, 300, 256, NY + 22))
# ---------- abajo: cinta en pulgadas
Y0, Y1 = 436, 556
X0, PPI = 30, 140
def X(inch): return X0 + (inch - 13.75) * PPI
o.append('<g id="pulgadas">')
o.append(f'<rect x="-10" y="{Y0}" width="1020" height="{Y1-Y0}" fill="url(#blade)" stroke="{INK}" stroke-width="6"/>')
o.append(f'<line x1="0" y1="{Y0+6}" x2="1000" y2="{Y0+6}" stroke="#FFFBD6" stroke-width="3"/>')
for s16 in range(int(13.75 * 16), int(20.9 * 16)):
    x = X(s16 / 16)
    if x < -5 or x > 1005: continue
    L = 46 if s16 % 16 == 0 else 32 if s16 % 8 == 0 else 22 if s16 % 4 == 0 else 15 if s16 % 2 == 0 else 9
    o.append(f'<line x1="{x:.1f}" y1="{Y0+3}" x2="{x:.1f}" y2="{Y0+3+L}" stroke="{INK}" stroke-width="{3 if s16%16==0 else 1.6}"/>')
    o.append(f'<line x1="{x:.1f}" y1="{Y1-3}" x2="{x:.1f}" y2="{Y1-3-L*0.6:.1f}" stroke="{INK}" stroke-width="{3 if s16%16==0 else 1.6}"/>')
for n in range(14, 21):
    x = X(n) - 26
    o.append(f'<text x="{x:.0f}" y="{Y0+86}" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="40" fill="{INK}">{n}</text>')
o.append('</g>')
x16 = X(16) - 26
o.append(f'<g id="rojo"><rect x="{x16-34:.0f}" y="{Y0+50}" width="68" height="48" rx="4" fill="#E5392F"/>'
         f'<text x="{x16:.0f}" y="{Y0+87}" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="40" fill="#FFFFFF">16</text></g>')
o.append(tag("l16", 330, 582, 300, "CADA 16 PULGADAS", x16 + 40, 582, x16 + 10, Y1 - 18, fs=24))
o.append(tag("lmontante", 380, 374, 290, "≈ 40 CM ENTRE MONTANTES", fs=20))
o.append('</svg>')
open("extras.svg", "w").write("\n".join(o))

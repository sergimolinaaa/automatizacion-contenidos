from metro import *
Y0, Y1 = 394, 466   # cinta (cara superior visible)
HOOKX = 880
o = [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 700">
<defs>{DEFS}</defs>
<rect width="1000" height="700" fill="url(#wall)"/>
<g opacity="0.9"><rect x="560" y="70" width="380" height="250" rx="8" fill="#C9D8E4"/>''' +
"".join(f'<circle cx="{x}" cy="{y}" r="5" fill="#AFC1D0"/>' for x in range(590, 930, 40) for y in range(100, 310, 40)) +
'''<rect x="610" y="110" width="12" height="90" rx="5" fill="#B7C7D4"/><circle cx="616" cy="104" r="12" fill="#B7C7D4"/>
<rect x="680" y="130" width="70" height="20" rx="8" fill="#B7C7D4"/><rect x="740" y="120" width="12" height="80" fill="#B7C7D4"/>
<path d="M 820 110 L 870 110 L 860 210 L 830 210 Z" fill="#B7C7D4"/><rect x="40" y="110" width="200" height="140" rx="10" fill="#D2DFEA"/></g>
''']
# banco de trabajo
o.append(f'<rect x="0" y="474" width="1000" height="226" fill="url(#benchfront)"/>')
o.append(f'<path d="M 0 340 L 1000 340 L 1000 474 L 0 474 Z" fill="url(#bench)"/>')
o.append(f'<line x1="0" y1="474" x2="1000" y2="474" stroke="{INK}" stroke-width="6"/>')
o.append('<g stroke="#A8743F" stroke-width="2.5" opacity="0.5" fill="none"><path d="M 0 370 C 200 364 400 374 600 366 S 900 372 1000 364"/><path d="M 0 440 C 250 432 500 446 750 436 S 950 440 1000 436"/></g>')
o.append('<g stroke="#5E3A1C" stroke-width="2" opacity="0.4"><line x1="0" y1="560" x2="1000" y2="560"/><line x1="0" y1="630" x2="1000" y2="630"/></g>')
# sombra de cinta y carcasa
o.append(f'<path d="M 360 {Y1+2} L {HOOKX} {Y1+2} L {HOOKX} {Y1+8} L 360 {Y1+8} Z" fill="{INK}" opacity="0.18"/>')
o.append(f'<ellipse cx="200" cy="470" rx="180" ry="16" fill="{INK}" opacity="0.25"/>')
# cinta
o.append(f'<g id="cinta">')
o.append(f'<path d="M 360 {Y0} L {HOOKX} {Y0} L {HOOKX} {Y1} L 360 {Y1} Z" fill="url(#blade)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
o.append(f'<line x1="360" y1="{Y0+5}" x2="{HOOKX-4}" y2="{Y0+5}" stroke="#FFFBD6" stroke-width="3"/>')
o.append(blade_marks(HOOKX, Y0 + 4, Y1 - 4, 66, 8, fs=30))
o.append('</g>')
# gancho (placa sobre la cinta + pestaña doblada hacia abajo)
o.append(f'<g id="gancho">')
o.append(f'<path d="M {HOOKX-96} {Y0-6} L {HOOKX+4} {Y0-6} L {HOOKX+4} {Y1+30} L {HOOKX+18} {Y1+30} L {HOOKX+18} {Y0-6} Q {HOOKX+18} {Y0-14} {HOOKX+10} {Y0-14} L {HOOKX-96} {Y0-14} Z" fill="url(#steelh)" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
o.append(f'<path d="M {HOOKX-96} {Y0-14} L {HOOKX-96} {Y1-10} L {HOOKX+4} {Y1-10} L {HOOKX+4} {Y0-6}" fill="none"/>')
o.append(f'<rect x="{HOOKX-100}" y="{Y0-2}" width="104" height="{Y1-Y0-8}" rx="6" fill="url(#steel)" stroke="{INK}" stroke-width="5"/>')
for rx in (HOOKX - 66, HOOKX - 28):
    o.append(f'<rect x="{rx-12}" y="{(Y0+Y1)/2-12:.0f}" width="24" height="16" rx="8" fill="#5D6676" stroke="{INK}" stroke-width="3"/>')
    o.append(f'<circle cx="{rx-4}" cy="{(Y0+Y1)/2-4:.0f}" r="7.5" fill="url(#rivet)" stroke="{INK}" stroke-width="3"/>')
o.append(f'<path d="M {HOOKX+4} {Y1+30} L {HOOKX+18} {Y1+30}" stroke="{INK}" stroke-width="5"/>')
o.append('</g>')
# carcasa del metro
o.append('<g id="carcasa"><g transform="translate(-40 -116) scale(1.18)">')
o.append(f'<path d="M 70 280 Q 70 230 120 230 L 300 230 Q 340 230 340 270 L 340 470 Q 340 500 310 500 L 110 500 Q 70 500 70 460 Z" fill="url(#case)" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>')
o.append(f'<path d="M 70 300 Q 70 230 130 230 L 160 230 L 160 250 Q 100 250 92 300 L 92 440 Q 92 478 130 478 L 160 478 L 160 500 L 110 500 Q 70 500 70 460 Z" fill="url(#rub)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
o.append(f'<path d="M 300 230 Q 340 230 340 270 L 340 330 L 318 330 L 318 272 Q 318 252 296 252 L 270 252 L 270 230 Z" fill="url(#rub)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
o.append(f'<circle cx="205" cy="365" r="86" fill="#F2B60F" stroke="{INK}" stroke-width="6"/>')
o.append(f'<circle cx="205" cy="365" r="72" fill="url(#case)" stroke="#C48E05" stroke-width="3"/>')
o.append(f'<text x="205" y="382" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="46" fill="{INK}">5 m</text>')
o.append(f'<path d="M 130 254 Q 205 242 290 254" fill="none" stroke="#FFF3B0" stroke-width="5" stroke-linecap="round"/>')
# boca y freno
o.append(f'<rect x="318" y="{(Y0+116)/1.18-14:.0f}" width="30" height="{(Y1-Y0)/1.18+28:.0f}" rx="6" fill="url(#rub)" stroke="{INK}" stroke-width="6"/>')
o.append(f'<rect x="230" y="206" width="70" height="30" rx="12" fill="#E5392F" stroke="{INK}" stroke-width="6"/>')
o.append(f'<path d="M 240 214 L 290 214" stroke="#FF8A7E" stroke-width="4" stroke-linecap="round"/>')
o.append('</g></g>')
# holgura y señal
o.append('<g id="baila">' + arrow("bl", HOOKX + 50, Y0 - 50, HOOKX + 10, Y0 - 50, LIME, w=8, head=18) + arrow("br", HOOKX + 30, Y0 - 50, HOOKX + 70, Y0 - 50, LIME, w=8, head=18) + '</g>')
o.append(tag("lgancho", 600, 230, 180, "GANCHO", 700, 288, HOOKX - 50, Y0 - 12))
o.append(tag("lrota", 620, 540, 280, "¿ESTÁ ROTA?", bg=CORAL, fg=INK))
o.append('</svg>')
open("metro.svg", "w").write("\n".join(o))

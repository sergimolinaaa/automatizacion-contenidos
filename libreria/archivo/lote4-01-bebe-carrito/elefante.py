from dib import *
G = 622
o = [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 700">
<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#D9EEFF"/><stop offset="1" stop-color="#FFF1DA"/></linearGradient>
<linearGradient id="dirt" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E7C487"/><stop offset="1" stop-color="#C99A5E"/></linearGradient>
<linearGradient id="ele" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#B3AEB2"/><stop offset="0.55" stop-color="#8C878D"/><stop offset="1" stop-color="#5F5A61"/></linearGradient>
<linearGradient id="elefar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8E898E"/><stop offset="1" stop-color="#4E4A50"/></linearGradient>
<linearGradient id="rubber" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#55606A"/><stop offset="1" stop-color="#2E353C"/></linearGradient>
</defs>
<rect width="1000" height="700" fill="url(#sky)"/>
<path d="M 0 330 C 120 270 240 300 360 280 C 500 250 620 300 760 270 C 860 250 940 280 1000 270 L 1000 {G} L 0 {G} Z" fill="#CFE5C8"/>
<path d="M 0 400 C 160 370 300 390 460 372 C 640 352 820 386 1000 366 L 1000 {G} L 0 {G} Z" fill="#B3D8AE"/>
<g fill="#9CCB98"><circle cx="90" cy="360" r="48"/><circle cx="140" cy="340" r="40"/><rect x="108" y="370" width="12" height="70"/><circle cx="880" cy="330" r="52"/><circle cx="930" cy="352" r="40"/><rect x="890" y="360" width="12" height="80"/></g>
<rect y="440" width="1000" height="260" fill="url(#dirt)"/>
<path d="M 0 440 C 200 432 400 446 600 438 C 800 430 900 442 1000 436" fill="none" stroke="#B98F5A" stroke-width="3" opacity="0.6"/>
<g fill="#B98F5A" opacity="0.7"><ellipse cx="120" cy="560" rx="16" ry="5"/><ellipse cx="520" cy="600" rx="12" ry="4"/><ellipse cx="300" cy="650" rx="20" ry="6"/><ellipse cx="940" cy="520" rx="14" ry="5"/></g>
<ellipse cx="400" cy="{G}" rx="300" ry="22" fill="{INK}" opacity="0.2"/>
''']
# alfombra de goma (delante, a la derecha)
fl, fr, nr, nl = (640, 590), (930, 590), (950, 648), (620, 648)
o.append(f'<g id="alfombra"><path d="M {nl[0]} {nl[1]} L {nr[0]} {nr[1]} L {nr[0]} {nr[1]+8} L {nl[0]} {nl[1]+8} Z" fill="#1F252B" stroke="{INK}" stroke-width="5"/>'
         f'<path d="M {fl[0]} {fl[1]} L {fr[0]} {fr[1]} L {nr[0]} {nr[1]} L {nl[0]} {nl[1]} Z" fill="url(#rubber)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
         + "".join(f'<path d="M {fl[0]+t*(fr[0]-fl[0]):.0f} {fl[1]} L {nl[0]+t*(nr[0]-nl[0]):.0f} {nl[1]}" stroke="#6C7884" stroke-width="3"/>' for t in (0.2, 0.4, 0.6, 0.8)) + '</g>')
# cuerda del palo a la alfombra
o.append(f'<g id="cuerda">' + capd("M 700 604 C 690 560 720 520 744 488", 6, "#E9D8B0") + f'<circle cx="700" cy="604" r="7" fill="#E9D8B0" stroke="{INK}" stroke-width="4"/></g>')
o.append('<g id="elefante">')
# patas lejanas
for x in (270, 520):
    o.append(f'<path d="M {x-36} 430 L {x-34} {G-14} Q {x} {G-4} {x+34} {G-14} L {x+36} 430 Z" fill="url(#elefar)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
# cola
o.append(capd("M 168 330 C 150 380 150 420 156 470", 7, "#7A757B") + f'<path d="M 148 466 L 156 498 L 166 466 Z" fill="#3B373D" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')
# patas cercanas
for x in (230, 470):
    o.append(f'<path d="M {x-44} 400 C {x-42} 480 {x-40} 560 {x-48} {G} Q {x} {G+10} {x+48} {G} C {x+40} 560 {x+42} 480 {x+44} 400 Z" fill="url(#ele)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
             f'<g fill="#E6E0D6" stroke="{INK}" stroke-width="3">' + "".join(f'<ellipse cx="{x+dx}" cy="{G-4}" rx="9" ry="6"/>' for dx in (-24, 0, 24)) + '</g>'
             f'<path d="M {x-30} {G-60} q 30 8 60 0 M {x-30} {G-90} q 30 8 60 0" stroke="{INK}" stroke-width="3" fill="none" opacity="0.3"/>')
# cuerpo
o.append(f'<path d="M 170 330 C 160 230 260 180 380 182 C 470 184 560 200 610 250 C 650 300 650 400 610 450 C 560 490 300 500 220 470 C 180 450 172 390 170 330 Z" fill="url(#ele)" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>')
o.append('<path d="M 230 230 C 300 190 420 186 520 208" fill="none" stroke="#D4D0D4" stroke-width="6" stroke-linecap="round" opacity="0.8"/>')
o.append(f'<g stroke="{INK}" stroke-width="3" fill="none" opacity="0.3"><path d="M 300 300 q 20 10 40 0"/><path d="M 420 320 q 20 10 40 0"/><path d="M 360 400 q 20 10 40 0"/><path d="M 250 380 q 16 8 32 0"/></g>')
# cabeza (domo doble típico del elefante asiático)
o.append(f'<path d="M 560 250 C 560 190 600 150 640 156 C 660 140 700 146 712 176 C 740 200 746 260 730 300 C 720 330 700 352 680 360 L 600 380 C 570 350 560 300 560 250 Z" fill="url(#ele)" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>')
o.append('<path d="M 600 176 C 620 160 650 158 672 168" fill="none" stroke="#D4D0D4" stroke-width="5" stroke-linecap="round" opacity="0.8"/>')
o.append(f'<path d="M 664 346 Q 690 372 716 352" fill="#8C878D" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>')
# oreja (pequeña, con manchas despigmentadas)
o.append(f'<path d="M 600 210 C 560 214 540 260 548 310 C 552 350 580 380 610 372 C 640 360 640 300 632 250 C 628 226 618 212 600 210 Z" fill="#8F8A90" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
o.append('<g fill="#E7B9B0" opacity="0.85"><circle cx="560" cy="290" r="6"/><circle cx="566" cy="312" r="5"/><circle cx="574" cy="334" r="6"/><circle cx="588" cy="352" r="5"/></g>')
o.append(f'<path d="M 612 226 C 620 270 620 320 606 356" fill="none" stroke="{INK}" stroke-width="3" opacity="0.35"/>')
# ojo
o.append(f'<g id="ojo"><ellipse cx="690" cy="250" rx="9" ry="7" fill="{INK}"/><circle cx="692" cy="247" r="2.5" fill="#FFFFFF"/></g>')
o.append(f'<path d="M 676 238 Q 690 230 704 238" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>')
o.append('</g>')
# trompa + palo (se animan juntos)
o.append('<g id="trompa">')
trunk = "M 700 300 C 740 360 746 430 760 470 C 770 500 800 500 812 470"
o.append(f'<path d="{trunk}" fill="none" stroke="{INK}" stroke-width="64" stroke-linecap="round"/>')
o.append(f'<path d="{trunk}" fill="none" stroke="#8C878D" stroke-width="50" stroke-linecap="round"/>')
o.append(f'<path d="M 714 330 C 742 380 748 430 758 462" fill="none" stroke="#B3AEB2" stroke-width="10" stroke-linecap="round" opacity="0.7"/>')
o.append(f'<g stroke="{INK}" stroke-width="3" opacity="0.35">' + "".join(f'<path d="M {730+i*3} {340+i*24} l 30 -6"/>' for i in range(6)) + '</g>')
o.append('<g fill="#E7B9B0" opacity="0.8"><circle cx="716" cy="318" r="5"/><circle cx="726" cy="336" r="4"/></g>')
o.append(capd("M 744 492 L 892 350", 12, "#B07A45"))
o.append(f'<path d="M 760 478 L 880 362" stroke="#D9A46A" stroke-width="3" stroke-linecap="round"/>')
o.append(f'<path d="M 800 462 C 830 478 840 452 826 440" fill="none" stroke="{INK}" stroke-width="22" stroke-linecap="round"/><path d="M 800 462 C 830 478 840 452 826 440" fill="none" stroke="#8C878D" stroke-width="12" stroke-linecap="round"/>')
o.append('</g>')
# mano del investigador
o.append(f'<g id="mano"><path d="M 1010 300 L 930 330" stroke="{INK}" stroke-width="56" stroke-linecap="round"/><path d="M 1010 300 L 930 330" stroke="#5B8DEF" stroke-width="42" stroke-linecap="round"/>'
         f'<ellipse cx="912" cy="338" rx="30" ry="22" fill="#E9B48C" stroke="{INK}" stroke-width="6"/><path d="M 890 330 q -12 -4 -16 6 M 892 342 q -14 0 -16 10" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/></g>')
o.append(tag("lpalo", 690, 100, 230, "PALO ATADO", 800, 158, 840, 400))
o.append(tag("lalfombra", 640, 500, 220, "ALFOMBRA", 760, 558, 790, 610))
o.append('</svg>')
open("elefante.svg", "w").write("\n".join(o))

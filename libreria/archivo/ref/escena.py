import sys
INK="#0B0B14"
def leg(pts, w=9, col="#4A382B"):
    d="M "+" L ".join(f"{x} {y}" for x,y in pts)
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w+7}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')
def tarsus(x0,y0,x1,y1,sag,col="#4A382B"):
    d=f"M {x0} {y0} Q {(x0+x1)/2} {max(y0,y1)+sag} {x1} {y1}"
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="12" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="{col}" stroke-width="5" stroke-linecap="round"/>')
S=440
def dip(cx,half,depth):
    # tramo de superficie hundido (curva suave) de cx-half a cx+half
    return (f"M {cx-half} {S} C {cx-half*0.45} {S}, {cx-half*0.5} {S+depth}, {cx} {S+depth} "
            f"C {cx+half*0.5} {S+depth}, {cx+half*0.45} {S}, {cx+half} {S}")
dips=[(345,95,15),(712,130,26),(905,100,21)]
o=[]
o.append(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 700">
<defs>
<linearGradient id="air" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#DDF1FF"/><stop offset="0.8" stop-color="#FFF4E4"/><stop offset="1" stop-color="#FFF4E4"/></linearGradient>
<linearGradient id="water" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8FD3FF"/><stop offset="0.12" stop-color="#8FD3FF"/><stop offset="1" stop-color="#2F7FD6"/></linearGradient>
<linearGradient id="body" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9A7A5C"/><stop offset="0.45" stop-color="#5E4634"/><stop offset="1" stop-color="#2E2119"/></linearGradient>
<radialGradient id="eye" cx="0.35" cy="0.35" r="0.7"><stop offset="0" stop-color="#7A3B2A"/><stop offset="1" stop-color="#1A0E0A"/></radialGradient>
</defs>
<rect width="1000" height="700" fill="url(#air)"/>
<path d="M 0 330 C 140 300, 260 318, 400 300 C 560 280, 700 312, 840 296 C 920 288, 970 300, 1000 296 L 1000 {S} L 0 {S} Z" fill="#CBEBD3"/>
<path d="M 0 380 C 160 360, 300 376, 470 364 C 640 352, 820 372, 1000 360 L 1000 {S} L 0 {S} Z" fill="#A9DDB7"/>
<rect y="{S}" width="1000" height="{700-S}" fill="url(#water)"/>
<g fill="#FFFFFF" opacity="0.14"><path d="M 180 {S} L 260 {S} L 150 700 L 40 700 Z"/><path d="M 520 {S} L 580 {S} L 520 700 L 430 700 Z"/><path d="M 820 {S} L 900 {S} L 880 700 L 770 700 Z"/></g>
<path d="M 0 646 C 180 630, 330 652, 520 638 C 700 626, 860 650, 1000 636 L 1000 700 L 0 700 Z" fill="#E7C487" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>
<g fill="#B98F5A" stroke="{INK}" stroke-width="4"><ellipse cx="150" cy="660" rx="26" ry="12"/><ellipse cx="610" cy="664" rx="18" ry="9"/><ellipse cx="860" cy="660" rx="30" ry="13"/></g>
<g id="shadows" fill="#1D5FA8" opacity="0.55"><ellipse cx="345" cy="640" rx="34" ry="7"/><ellipse cx="700" cy="636" rx="52" ry="9"/><ellipse cx="895" cy="640" rx="40" ry="8"/></g>
<line x1="0" y1="{S}" x2="1000" y2="{S}" stroke="{INK}" stroke-width="6"/>
<line x1="0" y1="{S+9}" x2="1000" y2="{S+9}" stroke="#FFFFFF" stroke-width="3" opacity="0.55"/>
<g id="reeds">
<path d="M 70 {S} C 64 330, 76 220, 70 120" fill="none" stroke="{INK}" stroke-width="15" stroke-linecap="round"/>
<path d="M 70 {S} C 64 330, 76 220, 70 120" fill="none" stroke="#36B37E" stroke-width="7" stroke-linecap="round"/>
<rect x="56" y="120" width="28" height="92" rx="14" fill="#7A4E2D" stroke="{INK}" stroke-width="6"/>
<rect x="63" y="132" width="7" height="60" rx="3.5" fill="#A87449"/>
<path d="M 112 {S} C 100 360, 128 290, 150 230" fill="none" stroke="{INK}" stroke-width="13" stroke-linecap="round"/>
<path d="M 112 {S} C 100 360, 128 290, 150 230" fill="none" stroke="#5CCB8A" stroke-width="6" stroke-linecap="round"/>
<path d="M 40 {S} C 36 380, 20 330, 4 300" fill="none" stroke="{INK}" stroke-width="13" stroke-linecap="round"/>
<path d="M 40 {S} C 36 380, 20 330, 4 300" fill="none" stroke="#2E9C6A" stroke-width="6" stroke-linecap="round"/>
</g>
<g id="pad"><ellipse cx="190" cy="{S}" rx="74" ry="13" fill="#36B37E" stroke="{INK}" stroke-width="6"/><path d="M 190 {S-1} L 240 {S-8}" stroke="{INK}" stroke-width="4"/><ellipse cx="172" cy="{S-4}" rx="34" ry="4" fill="#7BE07B"/></g>
''')
# hoyuelos: parche de aire que tapa la línea plana + curva hundida
o.append('<g id="dimples">')
for cx,h,dp in dips:
    d=dip(cx,h,dp)
    o.append(f'<path d="{d} Z" fill="#A9DDB7"/>'.replace(" Z", f" L {cx+h} {S-2} L {cx-h} {S-2} Z"))
    o.append(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>')
    o.append(f'<path d="{d}" fill="none" stroke="#2F7FD6" stroke-width="8" opacity="0.35" transform="translate(0 10)"/>')
    o.append(f'<path d="{d}" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.7" transform="translate(0 6)"/>')
o.append('</g>')
# ondas
o.append('<g fill="none" stroke="#FFFFFF" stroke-width="4">')
for n,(cx,h,dp) in zip("abc",dips):
    for k in (1,2):
        o.append(f'<g id="rip{n}{k}"><ellipse cx="{cx}" cy="{S+dp/2+2}" rx="{h*0.85:.0f}" ry="{6+dp*0.5:.0f}"/></g>')
o.append('</g>')
# zapatero
far="#7C6450"
o.append('<g id="strider">')
o.append('<g id="farlegs" opacity="0.9">')
o.append(leg([(410,378),(392,406),(352,452)],7,far)+tarsus(352,452,374,448,3,far))
o.append(leg([(462,380),(552,298),(716,462)],8,far)+tarsus(716,462,772,450,5,far))
o.append(leg([(492,380),(668,340),(906,458)],8,far)+tarsus(906,458,954,446,4,far))
o.append('</g>')
# cuerpo
o.append(f'<path d="M 382 362 C 430 340, 560 340, 660 360 C 670 362, 670 370, 660 372 C 560 392, 440 394, 382 382 Z" fill="url(#body)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
o.append('<path d="M 410 356 C 470 346, 560 347, 630 357" fill="none" stroke="#C9A982" stroke-width="5" stroke-linecap="round" opacity="0.8"/>')
o.append(f'<path d="M 455 350 C 456 365, 456 378, 455 388 M 520 347 C 521 362, 521 378, 520 390 M 585 350 C 586 364, 586 376, 585 386" fill="none" stroke="{INK}" stroke-width="3" opacity="0.45"/>')
# cabeza
o.append(f'<g id="head"><ellipse cx="358" cy="368" rx="34" ry="22" fill="url(#body)" stroke="{INK}" stroke-width="7"/>'
         f'<path d="M 334 382 Q 326 392, 322 404" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
         f'<circle cx="350" cy="362" r="14" fill="url(#eye)" stroke="{INK}" stroke-width="5"/>'
         f'<circle cx="345" cy="357" r="5" fill="#FFFFFF"/><circle cx="354" cy="367" r="2" fill="#FFFFFF" opacity="0.7"/></g>')
o.append('<g id="antennae">'+leg([(344,350),(318,318),(282,302)],5)+leg([(352,348),(336,312),(306,284)],5,far)+'</g>')
# patas cercanas
o.append(leg([(404,382),(380,412),(340,452)],8)+tarsus(340,452,318,446,2))
o.append(leg([(455,386),(522,288),(690,462)],10)+tarsus(690,462,742,452,6))
o.append(leg([(486,386),(642,332),(888,458)],9)+tarsus(888,458,940,448,5))
o.append('</g>')
o.append('</svg>')
print("\n".join(o))

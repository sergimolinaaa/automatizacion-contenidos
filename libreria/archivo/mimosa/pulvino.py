import math,random
from h import *
from plant import *
random.seed(9)
CX,CY=340,330
o=[SVG0,'<defs>'+DEFS+f'''
<radialGradient id="bg" cx="0.6" cy="0.4" r="0.9"><stop offset="0" stop-color="#F3FBEA"/><stop offset="1" stop-color="#CFE8C0"/></radialGradient>
<linearGradient id="stemv" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#C46A55"/><stop offset="0.45" stop-color="#9A4136"/><stop offset="1" stop-color="#5E2620"/></linearGradient>
<radialGradient id="pulv" cx="0.4" cy="0.3" r="0.8"><stop offset="0" stop-color="#B8E68C"/><stop offset="1" stop-color="#5DA03E"/></radialGradient>
<radialGradient id="cellf" cx="0.35" cy="0.3" r="0.75"><stop offset="0" stop-color="#E4F7FF"/><stop offset="0.6" stop-color="#8FD3FF"/><stop offset="1" stop-color="#3D8FDB"/></radialGradient>
<radialGradient id="celle" cx="0.35" cy="0.3" r="0.75"><stop offset="0" stop-color="#F0EBD0"/><stop offset="1" stop-color="#B9B58A"/></radialGradient>
<radialGradient id="cellu" cx="0.35" cy="0.3" r="0.75"><stop offset="0" stop-color="#E6F6D2"/><stop offset="1" stop-color="#9CCB7A"/></radialGradient>
<clipPath id="cut"><ellipse cx="{CX}" cy="{CY}" rx="84" ry="56"/></clipPath>
</defs>
<rect width="1000" height="700" fill="url(#bg)"/>''']
# fondo: hojitas lejanas desenfocadas
o.append('<g opacity="0.35">'+"".join(leaflet(random.uniform(500,980),random.uniform(80,660),random.uniform(0,360),60,22,"#9CCB7A",0) for _ in range(14))+'</g>')
# tallo
SX=230
o.append(f'<rect x="{SX-38}" y="-20" width="76" height="740" fill="url(#stemv)" stroke="{INK}" stroke-width="8"/>')
o.append(f'<path d="M {SX-24} 0 L {SX-24} 700" stroke="#E39A86" stroke-width="5" opacity="0.7"/>')
for y,sd in [(120,-1),(200,1),(470,-1),(560,1),(640,-1),(90,1)]:
    x=SX+sd*38
    o.append(f'<path d="M {x} {y} L {x+sd*22} {y-14} L {x} {y-10} Z" fill="#E8D7B0" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')
o.append('<g stroke="#F1C9B8" stroke-width="2" opacity="0.8">'+"".join(f'<path d="M {SX+random.uniform(-30,30):.0f} {y} l {random.uniform(-6,6):.0f} -9"/>' for y in range(20,700,22))+'</g>')
# pecíolo + hoja (gira en bisagra) -- caja simétrica respecto al pivote
PVX=CX+88
st=[f'<g id="stalk"><rect x="{PVX}" y="{CY-300}" width="560" height="600" fill="#000" opacity="0"/>']
d=f"M {PVX-6} {CY} L {PVX+300} {CY}"
st.append(stroke2(d,20,"#5DAA45",10))
st.append(f'<path d="M {PVX} {CY-5} L {PVX+290} {CY-5}" stroke="#A8E07E" stroke-width="4" stroke-linecap="round"/>')
for sp in (-38,-12,12,38):
    st.append(pinna(PVX+300,CY,sp,200,11,False,1.5))
st.append(f'<circle cx="{PVX+300}" cy="{CY}" r="10" fill="#5DAA45" stroke="{INK}" stroke-width="5"/></g>')
o.append("".join(st))
# pulvino
o.append(f'<g id="pulvinus"><ellipse cx="{CX}" cy="{CY}" rx="100" ry="68" fill="url(#pulv)" stroke="{INK}" stroke-width="8"/>')
o.append(f'<ellipse cx="{CX}" cy="{CY}" rx="84" ry="56" fill="#F7F3E0" stroke="{INK}" stroke-width="5"/>')
up=[];full=[];emp=[];wat=[]
for row,y in enumerate([CY-36,CY-12,CY+14,CY+40]):
    for k in range(-4,5):
        x=CX+k*24+(12 if row%2 else 0)
        if y<CY:
            up.append(f'<circle cx="{x}" cy="{y}" r="13" fill="url(#cellu)" stroke="{INK}" stroke-width="3"/>')
        else:
            full.append(f'<circle cx="{x}" cy="{y}" r="14" fill="url(#cellf)" stroke="{INK}" stroke-width="3"/><circle cx="{x-5}" cy="{y-5}" r="3.5" fill="#FFFFFF" opacity="0.85"/>')
            pts=[(x+math.cos(a)*(8+2.4*math.sin(a*5)), y+3+math.sin(a)*(7+2.4*math.sin(a*5))) for a in [i*2*math.pi/20 for i in range(20)]]
            emp.append(f'<path d="{P(pts)} Z" fill="url(#celle)" stroke="{INK}" stroke-width="3"/>')
o.append(f'<g clip-path="url(#cut)">{"".join(up)}<g id="full">{"".join(full)}</g><g id="empty">{"".join(emp)}</g></g>')
o.append(f'<path d="M {CX-60} {CY-44} A 70 46 0 0 1 {CX+30} {CY-54}" fill="none" stroke="#FFFFFF" stroke-width="4" opacity="0.6"/></g>')
# agua que sale
for x,y in [(CX-50,CY+48),(CX-10,CY+60),(CX+30,CY+52),(CX+60,CY+40),(CX-30,CY+70)]:
    wat.append(f'<path d="M {x} {y-14} C {x+9} {y-2}, {x+10} {y+10}, {x} {y+10} C {x-10} {y+10}, {x-9} {y-2}, {x} {y-14} Z" fill="#8FD3FF" stroke="{INK}" stroke-width="3.5"/><circle cx="{x-3}" cy="{y+2}" r="2.5" fill="#FFFFFF"/>')
o.append(f'<g id="water">{"".join(wat)}</g>')
# señal eléctrica por el tallo
sig=f"M {SX} 660 L {SX} 380 C {SX} 340, {CX-60} {CY}, {CX-20} {CY}"
o.append(f'<g id="signal"><path d="{sig}" fill="none" stroke="#C8FF2E" stroke-width="26" stroke-linecap="round" opacity="0.35"/><path d="{sig}" fill="none" stroke="{INK}" stroke-width="12" stroke-linecap="round" stroke-dasharray="0.04 0.025"/><path d="{sig}" fill="none" stroke="#C8FF2E" stroke-width="6" stroke-linecap="round" stroke-dasharray="0.04 0.025"/></g>')
# rayito en el punto de contacto
bx,by=SX-90,592
o.append(f'<g id="bolt"><path d="M {bx} {by-44} L {bx-18} {by+2} L {bx-2} {by+2} L {bx-12} {by+40} L {bx+20} {by-10} L {bx+4} {by-10} L {bx+14} {by-44} Z" fill="#C8FF2E" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/></g>')
o.append(tag("l1",400,140,"BISAGRA",w=180,lead=(470,198,380,262)))
o.append(tag("l2",420,520,"CÉLULAS CON AGUA",w=330,lead=(520,520,372,358)))
o.append(tag("l3",300,580,"SEÑAL ELÉCTRICA",w=320,lead=(300,609,236,560)))
o.append('</svg>')
open("pulvino.svg","w").write("\n".join(o))

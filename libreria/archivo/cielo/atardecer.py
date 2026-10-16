import math,random
from h import *
random.seed(5)
EX,EY,ER=500,1100,600
AR=720
o=[SVG0,f'''<defs>
<linearGradient id="space" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0C1230"/><stop offset="1" stop-color="#1B2556"/></linearGradient>
<radialGradient id="atm" cx="{EX}" cy="{EY}" r="{AR}" gradientUnits="userSpaceOnUse"><stop offset="{ER/AR:.3f}" stop-color="#7CC4FF" stop-opacity="0.95"/><stop offset="0.93" stop-color="#4D8BFF" stop-opacity="0.45"/><stop offset="1" stop-color="#4D8BFF" stop-opacity="0.12"/></radialGradient>
<radialGradient id="earth" cx="0.45" cy="0.1" r="0.6"><stop offset="0" stop-color="#4FB4E8"/><stop offset="1" stop-color="#1F5FA8"/></radialGradient>
<radialGradient id="sun" cx="0.4" cy="0.38" r="0.65"><stop offset="0" stop-color="#FFFBE0"/><stop offset="0.6" stop-color="#FFE45C"/><stop offset="1" stop-color="#FFB21E"/></radialGradient>
<radialGradient id="sun2" cx="0.4" cy="0.38" r="0.65"><stop offset="0" stop-color="#FFE9B0"/><stop offset="0.6" stop-color="#FFA640"/><stop offset="1" stop-color="#F0602A"/></radialGradient>
<linearGradient id="longray" x1="880" y1="0" x2="520" y2="0" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#FFFFFF"/><stop offset="0.35" stop-color="#FFE7A0"/><stop offset="1" stop-color="#FF7A2E"/></linearGradient>
</defs>
<rect width="1000" height="700" fill="url(#space)"/>''']
o.append('<g id="stars" fill="#FFFFFF">'+"".join(f'<circle cx="{random.uniform(20,980):.0f}" cy="{random.uniform(20,330):.0f}" r="{random.uniform(1.2,3):.1f}" opacity="{random.uniform(0.3,0.9):.2f}"/>' for _ in range(55))+'</g>')
o.append(f'<circle cx="{EX}" cy="{EY}" r="{AR}" fill="url(#atm)"/>')
o.append(f'<circle cx="{EX}" cy="{EY}" r="{AR}" fill="none" stroke="#BFE3FF" stroke-width="3" stroke-dasharray="10 12" opacity="0.7"/>')
# Tierra
o.append(f'<circle cx="{EX}" cy="{EY}" r="{ER}" fill="url(#earth)" stroke="{INK}" stroke-width="8"/>')
o.append(f'<clipPath id="ec"><circle cx="{EX}" cy="{EY}" r="{ER-4}"/></clipPath>')
o.append('<g clip-path="url(#ec)">')
o.append(f'<path d="M 60 600 C 140 560, 260 540, 360 556 C 420 566, 400 610, 330 640 C 260 670, 200 700, 60 720 Z" fill="#4FBF6A" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
o.append(f'<path d="M 120 610 C 180 590, 240 580, 300 586" fill="none" stroke="#A8EFA0" stroke-width="5" stroke-linecap="round"/>')
o.append(f'<path d="M 650 540 C 700 528, 790 548, 880 600 C 940 640, 900 700, 820 690 C 760 670, 700 640, 670 600 C 650 580, 630 556, 650 540 Z" fill="#4FBF6A" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
o.append('</g>')
# C 200 590, 300 560, 380 548 C 420 560, 400 600, 340 630 C 280 660, 200 690, 120 700 Z" fill="#4FBF6A" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
#o.append(f'<path d="M 640 520 C 720 528, 800 560, 860 610 C 820 640, 760 620, 720 600 C 680 580, 640 560, 640 520 Z" fill="#4FBF6A" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
o.append(f'<path d="M {EX-260} {EY-ER+64} A {ER-14} {ER-14} 0 0 1 {EX+150} {EY-ER+20}" fill="none" stroke="#BFE8FF" stroke-width="6" stroke-linecap="round" opacity="0.7"/>')
# observador (alfiler-persona) en lo alto
px,py=EX,EY-ER
o.append(f'<g id="person"><path d="M {px-12} {py-4} L {px-10} {py-34} L {px+10} {py-34} L {px+12} {py-4} Z" fill="#FFC23F" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
         f'<circle cx="{px}" cy="{py-46}" r="13" fill="#F2C19A" stroke="{INK}" stroke-width="5"/>'
         f'<path d="M {px-13} {py-50} C {px-12} {py-62}, {px+8} {py-64}, {px+12} {py-52}" fill="#5A3A22" stroke="{INK}" stroke-width="3"/></g>')
EYEY=py-46
# sol de mediodía arriba
def sun(id_,x,y,r,g):
    rays="".join(stroke2(f"M {x+(r+10)*math.cos(k*math.pi/4):.1f} {y+(r+10)*math.sin(k*math.pi/4):.1f} L {x+(r+24)*math.cos(k*math.pi/4):.1f} {y+(r+24)*math.sin(k*math.pi/4):.1f}",6,"#FFD23F",5) for k in range(8))
    return f'<g id="{id_}">{rays}<circle cx="{x}" cy="{y}" r="{r}" fill="url(#{g})" stroke="{INK}" stroke-width="6"/><circle cx="{x-r*0.35:.0f}" cy="{y-r*0.35:.0f}" r="{r*0.2:.0f}" fill="#FFFFFF" opacity="0.8"/></g>'
o.append(sun("sunnoon",EX,120,34,"sun"))
o.append('<g id="shortray">'+stroke2(f"M {EX} 170 L {EX} {EYEY-30}",14,"#FFF6C8",8)+stroke2(head(EX,170,EX,EYEY-24,24),10,"#FFF6C8",8)+'</g>')
# sol del atardecer a la derecha
o.append(sun("sunset",895,EYEY,36,"sun2"))
o.append('<g id="longray">'+stroke2(f"M 850 {EYEY} L {px+30} {EYEY}",14,"url(#longray)",8)+stroke2(head(850,EYEY,px+24,EYEY,24),10,"#FF7A2E",8)+'</g>')
# azul perdido por el camino
lost=[]
for x,up in [(830,True),(770,False),(715,True),(655,False),(600,True)]:
    y0=EYEY-12 if up else EYEY+12
    y1=y0-62 if up else y0+34
    lost.append(arrow(None,wave(x,y0,x+(-18 if up else 18),y1,24,6),"#4D8BFF",6,16))
o.append('<g id="lost">'+"".join(lost)+'</g>')
o.append(tag("lnoon",560,92,"MEDIODÍA",w=190))
o.append(tag("lshort",250,330,"POCO AIRE",w=200,lead=(450,372,492,408)))
o.append(tag("llong",640,250,"MUCHO AIRE",w=220,lead=(750,388,740,{EYEY}-0) if False else (750,308,745,EYEY-6)))
o.append(tag("lset",740,580,"ATARDECER",w=210,bg="#FF7A2E",fg=INK,lead=(880,580,895,EYEY+42)))
o.append('</svg>')
open("atardecer.svg","w").write("\n".join(o))

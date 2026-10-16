import math,random
from h import *
random.seed(11)
o=[SVG0,'''<defs>
<radialGradient id="bg" cx="0.5" cy="0.45" r="0.8"><stop offset="0" stop-color="#DDF0FF"/><stop offset="1" stop-color="#9FCBF2"/></radialGradient>
<radialGradient id="nit" cx="0.35" cy="0.3" r="0.75"><stop offset="0" stop-color="#C9D6F5"/><stop offset="0.55" stop-color="#7F94CC"/><stop offset="1" stop-color="#4A5B94"/></radialGradient>
<radialGradient id="oxy" cx="0.35" cy="0.3" r="0.75"><stop offset="0" stop-color="#FFC1B5"/><stop offset="0.55" stop-color="#F0624A"/><stop offset="1" stop-color="#A8321F"/></radialGradient>
<radialGradient id="halo" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#4D8BFF" stop-opacity="0.45"/><stop offset="1" stop-color="#4D8BFF" stop-opacity="0"/></radialGradient>
</defs>
<rect width="1000" height="700" fill="url(#bg)"/>''']
# moléculas lejanas desenfocadas (sin contorno)
far=[]
for _ in range(16):
    x,y=random.uniform(60,960),random.uniform(90,640); a=random.uniform(0,180); r=random.uniform(9,14)
    far.append(f'<g transform="translate({x:.0f} {y:.0f}) rotate({a:.0f})" opacity="0.3"><circle cx="{-r*0.8:.1f}" cy="0" r="{r:.1f}" fill="#FFFFFF"/><circle cx="{r*0.8:.1f}" cy="0" r="{r:.1f}" fill="#FFFFFF"/></g>')
o.append('<g id="farmols">'+"".join(far)+'</g>')
def mol(id_,x,y,r,ang,grad):
    d=r*0.82
    ca,sa=math.cos(math.radians(ang)),math.sin(math.radians(ang))
    p1=(x-d*ca,y-d*sa); p2=(x+d*ca,y+d*sa)
    s=f'<g id="{id_}">' if id_ else '<g>'
    s+=f'<ellipse cx="{x}" cy="{y+r*1.5:.0f}" rx="{r*1.6:.0f}" ry="{r*0.3:.0f}" fill="#4A6E9A" opacity="0.25"/>'
    for px,py in (p1,p2):
        s+=f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r}" fill="url(#{grad})" stroke="{INK}" stroke-width="{max(4,r/6):.0f}"/>'
    for px,py in (p1,p2):
        s+=f'<circle cx="{px-r*0.35:.1f}" cy="{py-r*0.38:.1f}" r="{r*0.22:.1f}" fill="#FFFFFF" opacity="0.8"/>'
    return s+'</g>'
CX,CY=560,460
# ondas
redp=wave(70,140,930,140,150,26)
o.append('<g id="red">'+arrow(None,redp,"#FF4B3A",10,30)+'</g>')
bluep=wave(70,CY,CX-118,CY,52,24)
o.append('<g id="blue">'+arrow(None,bluep,"#2F6BFF",10,28)+'</g>')
# halo + dispersión
o.append(f'<g id="halo"><circle cx="{CX}" cy="{CY}" r="150" fill="url(#halo)"/></g>')
sc=[]
for ang in (-90,-40,0,40,90,140,-140):
    a=math.radians(ang)
    x0,y0=CX+108*math.cos(a),CY+108*math.sin(a); x1,y1=CX+225*math.cos(a),CY+225*math.sin(a)
    if y1>640: x1,y1=CX+180*math.cos(a),CY+180*math.sin(a)
    sc.append(arrow(None,wave(x0,y0,x1,y1,34,10),"#4D8BFF",8,22))
o.append('<g id="scatter">'+"".join(sc)+'</g>')
o.append('<g id="mols">')
o.append(mol("m1",190,300,30,20,"oxy"))
o.append(mol("m2",330,240,28,-30,"nit"))
o.append(mol("m3",890,330,30,35,"nit"))
o.append(mol("m4",880,560,26,-15,"oxy"))
o.append('</g>')
o.append(mol("big",CX,CY,48,-25,"nit"))
o.append(tag("lnit",640,330,"NITRÓGENO",w=220,lead=(690,388,612,436)))
o.append(tag("loxy",60,360,"OXÍGENO",w=180,lead=(150,360,180,334)))
o.append(tag("lrojo",640,186,"ROJO: PASA",w=230,bg="#FFFFFF",fg="#D8261A"))
o.append(tag("lazul",60,560,"AZUL: REBOTA",w=270,bg="#FFFFFF",fg="#1F55D6"))
o.append('</svg>')
open("choque.svg","w").write("\n".join(o))

import math,random
from h import *
from plant import *
random.seed(4)
RY=390
o=[SVG0,'<defs>'+DEFS+'''
<radialGradient id="bg" cx="0.5" cy="0.45" r="0.85"><stop offset="0" stop-color="#EEF9E4"/><stop offset="1" stop-color="#B9DDA4"/></radialGradient>
<linearGradient id="lfb" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#7AD06A"/><stop offset="1" stop-color="#3F9C4B"/></linearGradient>
</defs>
<rect width="1000" height="700" fill="url(#bg)"/>''']
o.append('<g opacity="0.3" fill="#8CC77A">'+"".join(f'<circle cx="{random.uniform(0,1000):.0f}" cy="{random.uniform(60,680):.0f}" r="{random.uniform(20,60):.0f}"/>' for _ in range(14))+'</g>')
def big_leaflet(bx,by,ang,L,W,fill):
    a=math.radians(ang); mx,my=bx+math.cos(a)*L/2, by+math.sin(a)*L/2
    s=(f'<ellipse cx="{mx:.1f}" cy="{my:.1f}" rx="{L/2:.1f}" ry="{W/2:.1f}" transform="rotate({ang:.1f} {mx:.1f} {my:.1f})" fill="{fill}" stroke="{INK}" stroke-width="6"/>')
    # nervio central y venitas
    ex,ey=bx+math.cos(a)*L*0.9, by+math.sin(a)*L*0.9
    s+=f'<path d="M {bx:.1f} {by:.1f} L {ex:.1f} {ey:.1f}" stroke="#2E7D3E" stroke-width="3" stroke-linecap="round"/>'
    for t in (0.3,0.5,0.7):
        cx,cy=bx+math.cos(a)*L*t, by+math.sin(a)*L*t
        for sd in (1,-1):
            b=a+sd*0.7
            s+=f'<path d="M {cx:.1f} {cy:.1f} L {cx+math.cos(b)*W*0.38:.1f} {cy+math.sin(b)*W*0.38:.1f}" stroke="#2E7D3E" stroke-width="1.8" opacity="0.7"/>'
    # brillo
    hx,hy=bx+math.cos(a)*L*0.35-math.sin(a)*W*0.18, by+math.sin(a)*L*0.35+math.cos(a)*W*0.18
    hx2,hy2=bx+math.cos(a)*L*0.7-math.sin(a)*W*0.18, by+math.sin(a)*L*0.7+math.cos(a)*W*0.18
    s+=f'<path d="M {hx:.1f} {hy:.1f} L {hx2:.1f} {hy2:.1f}" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" opacity="0.55"/>'
    return s
xs=[130+108*i for i in range(7)]
L=[165+20*math.sin(math.pi*(i+1)/8) for i in range(7)]
# raquis
d=f"M 50 {RY} L 900 {RY}"
o.append(stroke2(d,16,"#5DAA45",10))
o.append(f'<path d="M 50 {RY-4} L 895 {RY-4}" stroke="#A8E07E" stroke-width="4" stroke-linecap="round"/>')
o.append('<g fill="#E8F5D6" stroke="#2E7D3E" stroke-width="1.5">'+"".join(f'<path d="M {x} {RY+9} l -4 9" />' for x in range(60,890,22))+'</g>')
batches={"A":range(5,7),"B":range(2,5),"C":range(0,2)}
for name,idx in batches.items():
    op=[];cl=[]
    for i in idx:
        x=xs[i]; l=L[i]; w=l*0.36
        op.append(big_leaflet(x,RY-8,-72,l,w,"url(#lf)")+big_leaflet(x,RY+8,72,l,w,"url(#lf)"))
        cl.append(big_leaflet(x,RY-10,-6,l,w*0.8,"url(#lfc)")+big_leaflet(x+4,RY-14,-14,l,w*0.8,"url(#lfc)"))
    o.append(f'<g id="close{name}">'+"".join(cl)+'</g>')
    o.append(f'<g id="open{name}">'+"".join(op)+'</g>')
# minibisagras (pulvínulos)
o.append('<g id="pulvinules">'+"".join(f'<ellipse cx="{x}" cy="{RY-9}" rx="9" ry="7" fill="#C9EE8A" stroke="{INK}" stroke-width="3.5"/><ellipse cx="{x}" cy="{RY+9}" rx="9" ry="7" fill="#C9EE8A" stroke="{INK}" stroke-width="3.5"/>' for x in xs)+'</g>')
# flecha de plegado en la pareja 4
x=xs[4]; 
fold=arrow(None,[(x+40,RY+130),(x+70,RY+70),(x+70,RY+20),(x+46,RY-40)],"#C8FF2E",8,22)

o.append(tag("lfol",420,70,"FOLÍOLOS",w=200,lead=(520,128,xs[3]+30,RY-120)))
o.append(tag("lbis",40,590,"MINI BISAGRAS",w=280,lead=(110,590,xs[0]-8,RY+12)))
o.append('</svg>')
open("foliolos.svg","w").write("\n".join(o))

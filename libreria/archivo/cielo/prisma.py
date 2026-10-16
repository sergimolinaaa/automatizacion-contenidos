import math,random
from h import *
random.seed(7)
o=[SVG0,'''<defs>
<linearGradient id="room" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1C2150"/><stop offset="1" stop-color="#2C2F66"/></linearGradient>
<linearGradient id="table" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8A5A36"/><stop offset="1" stop-color="#4A2E1A"/></linearGradient>
<linearGradient id="glass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#E8FBFF" stop-opacity="0.75"/><stop offset="1" stop-color="#7FC8E8" stop-opacity="0.55"/></linearGradient>
<linearGradient id="beamg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0.5"/><stop offset="1" stop-color="#FFFFFF"/></linearGradient>
<radialGradient id="wglow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0.35"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient>
</defs>
<rect width="1000" height="700" fill="url(#room)"/>''']
# estrellitas/polvo
o.append('<g id="dust" fill="#FFFFFF">'+"".join(f'<circle cx="{random.uniform(360,980):.0f}" cy="{random.uniform(80,440):.0f}" r="{random.uniform(1.5,3.5):.1f}" opacity="{random.uniform(0.2,0.6):.2f}"/>' for _ in range(40))+'</g>')
TY=500
o.append(f'<path d="M 0 {TY} L 1000 {TY} L 1000 700 L 0 700 Z" fill="url(#table)" stroke="{INK}" stroke-width="7"/>')
o.append(f'<path d="M 0 {TY+10} L 1000 {TY+10}" stroke="#B9814F" stroke-width="5" opacity="0.7"/>')
o.append('<g stroke="#3A2312" stroke-width="3" opacity="0.5" fill="none">'+"".join(f'<path d="M {x} {y} C {x+120} {y-6}, {x+240} {y+8}, {x+360} {y}"/>' for x,y in [(40,560),(420,600),(140,640),(600,550),(560,660)])+'</g>')
# prisma
A=(470,180); B=(310,TY-2); C=(630,TY-2)
def lerp(p,q,t): return (p[0]+(q[0]-p[0])*t, p[1]+(q[1]-p[1])*t)
entry=lerp(A,B,0.5)
cols=["#FF3B30","#FF9500","#FFD60A","#34C759","#2F8CFF","#8E44EC"]
exits=[lerp(A,C,0.44+0.035*i) for i in range(7)]
screen=[(985, 210+ 48*i) for i in range(7)]
# pared/pantalla
# haz blanco
src=(40,410)
o.append(f'<g id="lamp"><rect x="-30" y="{src[1]-34}" width="78" height="68" rx="14" fill="#3C4270" stroke="{INK}" stroke-width="7"/><rect x="40" y="{src[1]-24}" width="18" height="48" rx="5" fill="#FFF3B0" stroke="{INK}" stroke-width="5"/></g>')
o.append(f'<g id="beam"><path d="M {src[0]+18} {src[1]} L {entry[0]:.1f} {entry[1]:.1f}" stroke="{INK}" stroke-width="30" stroke-linecap="round"/><path d="M {src[0]+18} {src[1]} L {entry[0]:.1f} {entry[1]:.1f}" stroke="#FFFFFF" stroke-width="20" stroke-linecap="round"/></g>')
# interior (abanico dentro del cristal)
inner=[]
for i in range(6):
    m=lerp(exits[i],exits[i+1],0.5)
    inner.append(f'<path d="M {entry[0]:.1f} {entry[1]:.1f} L {m[0]:.1f} {m[1]:.1f}" stroke="{cols[i]}" stroke-width="7" opacity="0.85"/>')
# arcoíris fuera: hilos finos para poder "dibujarlos"
spec=[]
for i in range(6):
    for k in range(9):
        t=k/8
        e=lerp(exits[i],exits[i+1],t); s=lerp(screen[i],screen[i+1],t)
        spec.append(f'<path d="M {e[0]:.1f} {e[1]:.1f} L {s[0]:.1f} {s[1]:.1f}" stroke="{cols[i]}" stroke-width="8"/>')
o.append('<g id="rays">'+"".join(spec)+'</g>')
o.append(f'<g id="prism"><path d="M {A[0]} {A[1]} L {B[0]} {B[1]} L {C[0]} {C[1]} Z" fill="url(#glass)" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'
         f'<g id="inner">{"".join(inner)}</g>'
         f'<path d="M {A[0]-10} {A[1]+40} L {B[0]+40} {B[1]-24}" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round" opacity="0.8"/>'
         f'<path d="M {A[0]+16} {A[1]+50} L {A[0]+40} {A[1]+92}" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity="0.6"/></g>')
o.append(f'<ellipse cx="470" cy="{TY+8}" rx="170" ry="10" fill="{INK}" opacity="0.35"/>')
o.append(tag("l1",60,250,"LUZ BLANCA",lead=(160,308,180,388),leadcol="#FFFFFF",bg="#FFFFFF",fg=INK))
o.append(tag("lprism",380,590,"PRISMA",lead=(470,590,470,440)))
o.append(tag("l2",620,96,"TODOS LOS COLORES",lead=(840,154,900,262)))
o.append('</svg>')
open("prisma.svg","w").write("\n".join(o))

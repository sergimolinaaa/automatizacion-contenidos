import math,random
from h import *
random.seed(3)
o=[SVG0,'''<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3E9BFF"/><stop offset="0.55" stop-color="#7CC4FF"/><stop offset="1" stop-color="#D4EEFF"/></linearGradient>
<linearGradient id="dusksky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3B3F8F"/><stop offset="0.35" stop-color="#B0558A"/><stop offset="0.65" stop-color="#FF7A3D"/><stop offset="1" stop-color="#FFC56B"/></linearGradient>
<radialGradient id="sun" cx="0.4" cy="0.38" r="0.65"><stop offset="0" stop-color="#FFFBE0"/><stop offset="0.6" stop-color="#FFE45C"/><stop offset="1" stop-color="#FFB21E"/></radialGradient>
<radialGradient id="glow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0.75"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient>
<radialGradient id="dglow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#FFE08A" stop-opacity="0.9"/><stop offset="1" stop-color="#FF7A3D" stop-opacity="0"/></radialGradient>
<linearGradient id="near" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7DD36F"/><stop offset="1" stop-color="#3E9A4A"/></linearGradient>
<linearGradient id="crown" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6ED07A"/><stop offset="1" stop-color="#2E8B4E"/></linearGradient>
<linearGradient id="trunk" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#9A6A3F"/><stop offset="1" stop-color="#5E3B22"/></linearGradient>
<linearGradient id="shirt" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFD15C"/><stop offset="1" stop-color="#F0A21E"/></linearGradient>
<linearGradient id="jeans" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4D6FB8"/><stop offset="1" stop-color="#2D4A86"/></linearGradient>
<radialGradient id="skin" cx="0.4" cy="0.35" r="0.7"><stop offset="0" stop-color="#FBD7B5"/><stop offset="1" stop-color="#DFA57A"/></radialGradient>
</defs>
<rect width="1000" height="700" fill="url(#sky)"/>
<g id="sunset"><rect width="1000" height="700" fill="url(#dusksky)"/><circle cx="620" cy="430" r="260" fill="url(#dglow)"/></g>
''']
# sol
sx,sy,sr=730,160,58
rays=[]
for k in range(12):
    a=k*math.pi/6
    rays.append(f"M {sx+(sr+16)*math.cos(a):.1f} {sy+(sr+16)*math.sin(a):.1f} L {sx+(sr+40)*math.cos(a):.1f} {sy+(sr+40)*math.sin(a):.1f}")
o.append(f'<g id="sun"><circle cx="{sx}" cy="{sy}" r="150" fill="url(#glow)"/>'
         f'<g id="sunrays">'+"".join(stroke2(r,8,"#FFD23F",6) for r in rays)+'</g>'
         f'<circle cx="{sx}" cy="{sy}" r="{sr}" fill="url(#sun)" stroke="{INK}" stroke-width="7"/>'
         f'<path d="M {sx-38} {sy-20} A 42 42 0 0 1 {sx-10} {sy-42}" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round" opacity="0.85"/></g>')
def cloud(id_,cx,cy,s,outline=True,op=1):
    blobs=[(-60,10,40),(-20,-14,52),(30,-4,46),(68,14,34),(0,20,44)]
    base="".join(f'<circle cx="{cx+dx*s:.0f}" cy="{cy+dy*s:.0f}" r="{r*s:.0f}"/>' for dx,dy,r in blobs)
    g=f'<g id="{id_}" opacity="{op}">'
    if outline: g+=f'<g fill="{INK}" stroke="{INK}" stroke-width="14">{base}</g>'
    g+=f'<g fill="#FFFFFF">{base}</g>'
    g+=f'<ellipse cx="{cx+4*s:.0f}" cy="{cy+40*s:.0f}" rx="{86*s:.0f}" ry="{16*s:.0f}" fill="#CFE3F5"/>'
    g+=f'<path d="M {cx-50*s:.0f} {cy-26*s:.0f} A {40*s:.0f} {40*s:.0f} 0 0 1 {cx-10*s:.0f} {cy-58*s:.0f}" fill="none" stroke="#FFFFFF" stroke-width="5" opacity="0.9"/></g>'
    return g
o.append(cloud("cloudfar",420,250,0.7,False,0.75))
o.append(cloud("cloud1",520,140,1.0))
o.append(cloud("cloud2",150,250,0.85))
# pájaros
o.append('<g id="birds">'+"".join(stroke2(f"M {x-16} {y-6} Q {x-8} {y-14} {x} {y} Q {x+8} {y-14} {x+16} {y-6}",4,"#2A2F4A",4) for x,y in [(600,280),(640,262),(668,292)])+'</g>')
# colinas
o.append('<path d="M 0 440 C 120 400, 260 420, 380 400 C 520 378, 640 420, 760 410 C 860 402, 940 420, 1000 412 L 1000 700 L 0 700 Z" fill="#B8DDC4"/>')
o.append('<path d="M 0 490 C 180 460, 340 488, 520 470 C 700 452, 860 482, 1000 466 L 1000 700 L 0 700 Z" fill="#8CCB9A"/>')
o.append(f'<g id="dusk" opacity="0.32"><path d="M 0 440 C 120 400, 260 420, 380 400 C 520 378, 640 420, 760 410 C 860 402, 940 420, 1000 412 L 1000 700 L 0 700 Z" fill="#FF7A3D"/></g>')
o.append(f'<path d="M 0 560 C 200 530, 420 552, 620 540 C 800 530, 900 546, 1000 540 L 1000 700 L 0 700 Z" fill="url(#near)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
o.append('<path d="M 30 566 C 200 540, 420 560, 600 548" fill="none" stroke="#B5F08F" stroke-width="5" stroke-linecap="round" opacity="0.8"/>')
# matas de hierba
gr=[]
for x in list(range(40,1000,70)):
    y=560-0.0+(-10 if 300<x<700 else 0)
    yy=548+random.uniform(-6,6)+40+random.uniform(0,60)
    if yy>650: yy=640
    gr.append(f"M {x} {yy:.0f} l -8 -18 M {x} {yy:.0f} l 0 -22 M {x} {yy:.0f} l 9 -17")
o.append(f'<path d="{" ".join(gr)}" fill="none" stroke="#2E7D3E" stroke-width="5" stroke-linecap="round"/>')
# flores
for x,y,c in [(120,620,"#FF5A8A"),(470,632,"#FFFFFF"),(690,612,"#FFD23F"),(560,650,"#FF5A8A")]:
    o.append(f'<g><circle cx="{x}" cy="{y}" r="10" fill="{c}" stroke="{INK}" stroke-width="4"/><circle cx="{x}" cy="{y}" r="4" fill="#F0A21E"/></g>')
# árbol
tx,ty=890,548
o.append(f'<ellipse cx="{tx-10}" cy="{ty+12}" rx="80" ry="12" fill="#1F5E2E" opacity="0.35"/>')
o.append(f'<path d="M {tx-18} {ty+8} C {tx-14} {ty-60}, {tx-16} {ty-110}, {tx-8} {ty-130} L {tx+10} {ty-130} C {tx+14} {ty-100}, {tx+14} {ty-60}, {tx+20} {ty+8} Z" fill="url(#trunk)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
o.append(f'<g id="tree">')
blobs=[(-50,-170,52),(0,-212,62),(52,-174,50),(-16,-150,48),(26,-142,46)]
base="".join(f'<circle cx="{tx+dx}" cy="{ty+dy}" r="{r}"/>' for dx,dy,r in blobs)
o.append(f'<g fill="{INK}" stroke="{INK}" stroke-width="14">{base}</g><g fill="url(#crown)">{base}</g>')
o.append(f'<path d="M {tx-90} {ty-210} A 60 60 0 0 1 {tx-24} {ty-262}" fill="none" stroke="#A8EFA0" stroke-width="7" stroke-linecap="round" opacity="0.8"/>')
o.append("".join(f'<path d="M {tx+dx} {ty+dy} q 8 -8 16 0" fill="none" stroke="#2A7A44" stroke-width="4" stroke-linecap="round"/>' for dx,dy in [(-34,-190),(16,-222),(34,-160),(-8,-136),(-60,-150)]))
o.append('</g>')
# niña / niño mirando al cielo (perfil, mira a la derecha)
kx=330; ground=592
o.append(f'<ellipse cx="{kx}" cy="{ground+6}" rx="58" ry="10" fill="#1F5E2E" opacity="0.4"/>')
o.append('<g id="kid">')
# piernas
o.append(stroke2(f"M {kx-10} 512 L {kx-14} {ground-8}",22,"url(#jeans)",9,"butt"))
o.append(stroke2(f"M {kx+12} 512 L {kx+16} {ground-8}",22,"url(#jeans)",9,"butt"))
o.append(f'<path d="M {kx-34} {ground} C {kx-34} {ground-18}, {kx-4} {ground-20}, {kx+2} {ground-6} L {kx+2} {ground+2} Z" fill="#FF5A36" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
o.append(f'<path d="M {kx-4} {ground} C {kx-4} {ground-18}, {kx+26} {ground-20}, {kx+34} {ground-6} L {kx+34} {ground+2} Z" fill="#FF5A36" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
# brazo de atrás (colgando)
o.append(stroke2(f"M {kx-6} 440 L {kx-22} 482 L {kx-20} 516",16,"#F0A21E",8))
o.append(f'<circle cx="{kx-20}" cy="520" r="10" fill="url(#skin)" stroke="{INK}" stroke-width="5"/>')
# torso
o.append(f'<path d="M {kx-32} 436 C {kx-34} 470, {kx-34} 500, {kx-30} 520 L {kx+34} 520 C {kx+36} 496, {kx+34} 466, {kx+28} 436 C {kx+14} 424, {kx-18} 424, {kx-32} 436 Z" fill="url(#shirt)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
o.append(f'<path d="M {kx-24} 440 C {kx-10} 432, {kx+10} 432, {kx+20} 438" fill="none" stroke="#FFF1B8" stroke-width="5" stroke-linecap="round"/>')
# cuello + cabeza inclinada hacia arriba
hx,hy=kx+6,388
o.append(f'<rect x="{kx-6}" y="414" width="18" height="18" fill="url(#skin)" stroke="{INK}" stroke-width="5"/>')
o.append(f'<g id="headk"><circle cx="{hx}" cy="{hy}" r="36" fill="url(#skin)" stroke="{INK}" stroke-width="7"/>')
o.append(f'<path d="M {hx-36} {hy+4} C {hx-44} {hy-30}, {hx-10} {hy-52}, {hx+20} {hy-36} C {hx+8} {hy-30}, {hx-6} {hy-18}, {hx-10} {hy+6} C {hx-18} {hy+24}, {hx-30} {hy+26}, {hx-36} {hy+4} Z" fill="#5A3A22" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
o.append(f'<circle cx="{hx-12}" cy="{hy+4}" r="7" fill="#E9A57E" stroke="{INK}" stroke-width="3"/>')
o.append(f'<g id="eyek"><ellipse cx="{hx+20}" cy="{hy-10}" rx="5" ry="6" fill="{INK}"/><circle cx="{hx+22}" cy="{hy-12}" r="2" fill="#FFFFFF"/></g>')
o.append(f'<path d="M {hx+16} {hy+16} Q {hx+24} {hy+20} {hx+30} {hy+12}" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>')
o.append(f'<circle cx="{hx+18}" cy="{hy+4}" r="6" fill="#FF8A8A" opacity="0.5"/></g>')
# brazo delantero apuntando al cielo
o.append(stroke2(f"M {kx+16} 442 L {kx+52} 414 L {kx+84} 376",16,"#FFC23F",8))
o.append(f'<circle cx="{kx+88}" cy="371" r="11" fill="url(#skin)" stroke="{INK}" stroke-width="5"/>')
o.append(stroke2(f"M {kx+92} 366 L {kx+104} 352",6,"#F2C19A",6))
o.append('</g>')
# pregunta
o.append(f'<g id="mark"><path d="M 246 250 C 246 206, 330 206, 330 250 C 330 284, 300 290, 290 300 L 300 318 L 272 298 C 254 292, 246 276, 246 250 Z" fill="#FFFFFF" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
         f'<text x="288" y="270" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="50" fill="#2F6BFF">?</text></g>')
# luz azul rebotada que llega al ojo desde todo el cielo
ex,ey=hx+20,hy-10
rays=[]
for px,py in [(520,250),(640,110),(420,90),(130,150),(720,330),(560,420),(100,360)]:
    dx,dy=ex-px,ey-py; L=math.hypot(dx,dy); ux,uy=dx/L,dy/L
    a=(px,py); b=(px+ux*min(110,L-60),py+uy*min(110,L-60))
    rays.append((a,b))
o.append('<g id="skyrays">')
for a,b in rays:
    o.append(f'<circle cx="{a[0]}" cy="{a[1]}" r="11" fill="#FFFFFF" stroke="#2F6BFF" stroke-width="5"/>')
    o.append(arrow(None,[a,b],"#4D8BFF",8,20))
o.append('</g>')
o.append(tag("lazul",620,560,"AZUL REBOTADO",w=300,lead=(660,560,566,428),leadcol="#C8FF2E"))
o.append('</svg>')
open("paisaje.svg","w").write("\n".join(o))

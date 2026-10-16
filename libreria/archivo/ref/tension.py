import math
INK="#0B0B14"
def ys(x): return 300+52*math.exp(-((x-500)/125)**2)
def surf_path(x0=0,x1=1000,step=10):
    return "M "+" L ".join(f"{x} {ys(x):.1f}" for x in range(x0,x1+1,step))
o=[f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 700">
<defs>
<linearGradient id="air" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E3F3FF"/><stop offset="1" stop-color="#FFF4E4"/></linearGradient>
<linearGradient id="water" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8FD3FF"/><stop offset="1" stop-color="#2F7FD6"/></linearGradient>
<linearGradient id="seg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#A88563"/><stop offset="0.4" stop-color="#6E5240"/><stop offset="1" stop-color="#33251C"/></linearGradient>
</defs>
<rect width="1000" height="700" fill="url(#air)"/>
<path d="{surf_path()} L 1000 700 L 0 700 Z" fill="url(#water)"/>''']
# moléculas
rows=[(30,1.0),(108,0.55),(186,0.25),(264,0.08),(342,0)]
o.append('<g id="hbonds" stroke="#FFFFFF" stroke-width="3" opacity="0.5" stroke-dasharray="8 8">')
pts=[[(x, ys(x)+dy*1+ (ys(x)-300)*(f-1)) for x in range(40,1000,80)] for dy,f in rows]
for r in range(len(pts)-1):
    for (x,y),(x2,y2) in zip(pts[r],pts[r+1]):
        o.append(f'<line x1="{x}" y1="{y:.1f}" x2="{x2}" y2="{y2:.1f}"/>')
    for (x,y),(x2,y2) in zip(pts[r+1],pts[r+1][1:]):
        o.append(f'<line x1="{x}" y1="{y:.1f}" x2="{x2}" y2="{y2:.1f}"/>')
o.append('</g>')
o.append('<g id="bonds">')
d="M "+" L ".join(f"{x} {y:.1f}" for x,y in pts[0])
o.append(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="16" stroke-linejoin="round" stroke-linecap="round"/>')
o.append(f'<path d="{d}" fill="none" stroke="#C8FF2E" stroke-width="8" stroke-linejoin="round" stroke-linecap="round"/>')
o.append('</g>')
import random
random.seed(4)
o.append('<g id="mols">')
for r,row in enumerate(pts):
    for x,y in row:
        a=random.uniform(-40,40)
        g=[f'<g transform="translate({x} {y:.1f}) rotate({a:.0f})">']
        g.append(f'<circle cx="-16" cy="13" r="9" fill="#FFFFFF" stroke="{INK}" stroke-width="3.5"/>')
        g.append(f'<circle cx="16" cy="13" r="9" fill="#FFFFFF" stroke="{INK}" stroke-width="3.5"/>')
        g.append(f'<circle cx="0" cy="0" r="17" fill="#FF6B4A" stroke="{INK}" stroke-width="4"/>')
        g.append('<circle cx="-6" cy="-6" r="5" fill="#FFFFFF" opacity="0.6"/></g>')
        o.append("".join(g))
o.append('</g>')
o.append(f'<path d="{surf_path()}" fill="none" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
o.append(f'<path d="{surf_path()}" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.7" transform="translate(0 7)"/>')
# pata: tarso apoyado siguiendo la curva + resto de la pata subiendo
tar=[(x, ys(x)-14) for x in range(400,601,20)]
td="M "+" L ".join(f"{x} {y:.1f}" for x,y in tar)
leg=f"{td} L 650 {ys(650)-40:.1f} L 790 40"
o.append('<g id="foot">')
o.append(f'<path d="{leg}" fill="none" stroke="{INK}" stroke-width="34" stroke-linejoin="round" stroke-linecap="round"/>')
o.append(f'<path d="{leg}" fill="none" stroke="url(#seg)" stroke-width="22" stroke-linejoin="round" stroke-linecap="round"/>')
o.append(f'<path d="{leg}" fill="none" stroke="#C9A982" stroke-width="5" stroke-linejoin="round" stroke-linecap="round" opacity="0.6" transform="translate(-3 -6)"/>')
hs=[]
for x,y in tar[:-1]:
    hs.append(f'<line x1="{x}" y1="{y-8:.1f}" x2="{x+16}" y2="{y-26:.1f}"/>')
o.append(f'<g stroke="#4A382B" stroke-width="4" stroke-linecap="round">{"".join(hs)}</g>')
o.append('</g>')
def arrow(id_,x1,y1,x2,y2,col):
    ang=math.atan2(y2-y1,x2-x1); L=30
    p1=(x2-L*math.cos(ang-0.5), y2-L*math.sin(ang-0.5)); p2=(x2-L*math.cos(ang+0.5), y2-L*math.sin(ang+0.5))
    return (f'<g id="{id_}"><path d="M {x1} {y1} L {x2} {y2}" stroke="{INK}" stroke-width="20" stroke-linecap="round"/>'
            f'<path d="M {x1} {y1} L {x2} {y2}" stroke="{col}" stroke-width="10" stroke-linecap="round"/>'
            f'<path d="M {p1[0]:.1f} {p1[1]:.1f} L {x2} {y2} L {p2[0]:.1f} {p2[1]:.1f}" fill="none" stroke="{INK}" stroke-width="20" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="M {p1[0]:.1f} {p1[1]:.1f} L {x2} {y2} L {p2[0]:.1f} {p2[1]:.1f}" fill="none" stroke="{col}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></g>')
o.append(arrow("weight",500,120,500,272,"#FF5A36"))
o.append('<g id="pull">'+arrow("pullL",380,ys(380)-30,250,ys(250)-48,"#FFFFFF")+arrow("pullR",620,ys(620)-34,740,ys(740)-50,"#FFFFFF")+'</g>')
def tag(id_,x,y,w,text,bg="#0B0B14",fg="#C8FF2E"):
    return (f'<g id="{id_}"><rect x="{x}" y="{y}" width="{w}" height="58" rx="12" fill="{bg}"/>'
            f'<text x="{x+w/2}" y="{y+40}" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="30" fill="{fg}">{text}</text></g>')
o.append(tag("lpeso",530,110,140,"PESO",bg="#FF5A36",fg="#0B0B14"))
o.append(tag("lskin",40,130,360,"«PIEL» DEL AGUA"))
o.append(tag("ltira",800,170,150,"TIRA",bg="#FFFFFF",fg="#0B0B14"))
o.append('</svg>')
print("\n".join(o))

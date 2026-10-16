import math
INK="#0B0B14"
def P(pts): return "M "+" L ".join(f"{x:.1f} {y:.1f}" for x,y in pts)
def stroke2(d,w,col,extra=7,cap="round",op=1):
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w+extra}" stroke-linecap="{cap}" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="{cap}" stroke-linejoin="round" opacity="{op}"/>')
def head(x1,y1,x2,y2,L=28,a=0.5):
    ang=math.atan2(y2-y1,x2-x1)
    p1=(x2-L*math.cos(ang-a), y2-L*math.sin(ang-a)); p2=(x2-L*math.cos(ang+a), y2-L*math.sin(ang+a))
    return f"M {p1[0]:.1f} {p1[1]:.1f} L {x2:.1f} {y2:.1f} L {p2[0]:.1f} {p2[1]:.1f}"
def arrow(id_,pts,col,w=10,L=28):
    d=P(pts); (x1,y1),(x2,y2)=pts[-2],pts[-1]
    hd=head(x1,y1,x2,y2,L)
    return (f'<g id="{id_}">'+stroke2(d,w,col,w)+stroke2(hd,w,col,w)+'</g>') if id_ else (stroke2(d,w,col,w)+stroke2(hd,w,col,w))
def tag(id_,x,y,text,bg=INK,fg="#C8FF2E",w=None,lead=None,leadcol=INK):
    if w is None: w=len(text)*18.5+40
    s=f'<g id="{id_}">'
    if lead:
        lx,ly,tx,ty=lead
        s+=f'<path d="M {lx} {ly} L {tx} {ty}" stroke="{INK}" stroke-width="9" stroke-linecap="round"/><path d="M {lx} {ly} L {tx} {ty}" stroke="{leadcol}" stroke-width="4" stroke-linecap="round"/><circle cx="{tx}" cy="{ty}" r="8" fill="{leadcol}" stroke="{INK}" stroke-width="4"/>'
    s+=(f'<rect x="{x}" y="{y}" width="{w:.0f}" height="58" rx="12" fill="{bg}" stroke="{INK}" stroke-width="4"/>'
        f'<text x="{x+w/2:.0f}" y="{y+40}" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="30" fill="{fg}">{text}</text></g>')
    return s
def wave(x0,y0,x1,y1,lam,amp,step=4):
    L=math.hypot(x1-x0,y1-y0); ux,uy=(x1-x0)/L,(y1-y0)/L; nx,ny=-uy,ux
    pts=[]
    n=int(L/step)
    for i in range(n+1):
        s=i*L/n; a=amp*math.sin(2*math.pi*s/lam)*min(1,s/30,(L-s)/30+0.0001)
        pts.append((x0+ux*s+nx*a, y0+uy*s+ny*a))
    return pts
SVG0='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 700">'

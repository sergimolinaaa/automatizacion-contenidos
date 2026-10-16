import math
from h import *
DEFS='''<linearGradient id="lf" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8EE07A"/><stop offset="1" stop-color="#3E9A4A"/></linearGradient>
<linearGradient id="lfc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#C2E8A0"/><stop offset="1" stop-color="#7DB862"/></linearGradient>
<linearGradient id="stem" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#B3584A"/><stop offset="0.5" stop-color="#8C3B32"/><stop offset="1" stop-color="#5E2620"/></linearGradient>
<radialGradient id="pom" cx="0.4" cy="0.35" r="0.6"><stop offset="0" stop-color="#FFE0F2"/><stop offset="0.6" stop-color="#F58AC8"/><stop offset="1" stop-color="#C9549A"/></radialGradient>'''
def rot(x,y,a): c,s=math.cos(a),math.sin(a); return (x*c-y*s, x*s+y*c)
def leaflet(cx,cy,ang,L,W,fill="url(#lf)",sw=2.6):
    # elipse con eje mayor en dirección ang (grados), base en (cx,cy)
    a=math.radians(ang); mx,my=cx+math.cos(a)*L/2, cy+math.sin(a)*L/2
    return (f'<ellipse cx="{mx:.1f}" cy="{my:.1f}" rx="{L/2:.1f}" ry="{W/2:.1f}" transform="rotate({ang:.1f} {mx:.1f} {my:.1f})" fill="{fill}" stroke="{INK}" stroke-width="{sw}"/>'
            f'<path d="M {cx+math.cos(a)*3:.1f} {cy+math.sin(a)*3:.1f} L {cx+math.cos(a)*L*0.8:.1f} {cy+math.sin(a)*L*0.8:.1f}" stroke="#2E7D3E" stroke-width="1.2" opacity="0.7"/>')
def pinna(x0,y0,ang,L,n,closed,s=1.0):
    a=math.radians(ang); out=[]
    x1,y1=x0+math.cos(a)*L, y0+math.sin(a)*L
    d=f"M {x0:.1f} {y0:.1f} L {x1:.1f} {y1:.1f}"
    out.append(f'<path d="{d}" stroke="{INK}" stroke-width="{6*s:.1f}" stroke-linecap="round"/><path d="{d}" stroke="#4E9A3A" stroke-width="{2.6*s:.1f}" stroke-linecap="round"/>')
    for i in range(n):
        t=0.1+0.88*i/(n-1)
        bx,by=x0+math.cos(a)*L*t, y0+math.sin(a)*L*t
        ll=(12+9*math.sin(math.pi*min(1,t*1.15)))*s
        if closed:
            for side in (1,-1):
                out.append(leaflet(bx,by,ang+side*14,ll*0.95,ll*0.33,"url(#lfc)",2.2*s))
        else:
            for side in (1,-1):
                out.append(leaflet(bx,by,ang+side*72,ll,ll*0.36,"url(#lf)",2.4*s))
    return "".join(out)
def leaf(px,py,ang,L,closed,s=1.0,npin=4,nlet=13,pl=125):
    """hoja bipinnada: pecíolo desde (px,py) con ángulo ang; al cerrarse el pecíolo cae y las pinnas se juntan"""
    a=math.radians(ang); tx,ty=px+math.cos(a)*L, py+math.sin(a)*L
    out=[]
    d=f"M {px:.1f} {py:.1f} Q {px+math.cos(a)*L*0.5+math.sin(a)*8:.1f} {py+math.sin(a)*L*0.5-math.cos(a)*8:.1f} {tx:.1f} {ty:.1f}"
    spreads=[-42,-14,14,42] if npin==4 else [-22,22]
    if closed: spreads=[x*0.18 for x in spreads]
    for sp in spreads: out.append(pinna(tx,ty,ang+sp,pl*s,nlet,closed,s))
    out.insert(0,f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{11*s:.1f}" stroke-linecap="round"/><path d="{d}" fill="none" stroke="#5DAA45" stroke-width="{5*s:.1f}" stroke-linecap="round"/>')
    out.append(f'<ellipse cx="{px+math.cos(a)*9*s:.1f}" cy="{py+math.sin(a)*9*s:.1f}" rx="{12*s:.1f}" ry="{8*s:.1f}" transform="rotate({ang:.1f} {px+math.cos(a)*9*s:.1f} {py+math.sin(a)*9*s:.1f})" fill="#7FC25A" stroke="{INK}" stroke-width="{4*s:.1f}"/>')
    out.append(f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="{5*s:.1f}" fill="#5DAA45" stroke="{INK}" stroke-width="{3*s:.1f}"/>')
    return "".join(out)
def pompom(x,y,r):
    out=[]
    for k in range(40):
        a=k*2*math.pi/40+0.07*(k%3)
        rr=r*(0.92+0.1*((k*7)%5)/5)
        x1,y1=x+math.cos(a)*rr*0.35,y+math.sin(a)*rr*0.35; x2,y2=x+math.cos(a)*rr,y+math.sin(a)*rr
        out.append(f'<path d="M {x1:.1f} {y1:.1f} L {x2:.1f} {y2:.1f}" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>')
    for k in range(40):
        a=k*2*math.pi/40+0.07*(k%3); rr=r*(0.92+0.1*((k*7)%5)/5)
        x1,y1=x+math.cos(a)*rr*0.35,y+math.sin(a)*rr*0.35; x2,y2=x+math.cos(a)*rr,y+math.sin(a)*rr
        out.append(f'<path d="M {x1:.1f} {y1:.1f} L {x2:.1f} {y2:.1f}" stroke="#F08ACB" stroke-width="2.6" stroke-linecap="round"/>')
    out.append(f'<circle cx="{x}" cy="{y}" r="{r*0.5:.1f}" fill="url(#pom)" stroke="{INK}" stroke-width="3"/>')
    for k in range(40):
        a=k*2*math.pi/40+0.07*(k%3); rr=r*(0.92+0.1*((k*7)%5)/5)
        out.append(f'<circle cx="{x+math.cos(a)*rr:.1f}" cy="{y+math.sin(a)*rr:.1f}" r="2.6" fill="#FFF3A6"/>')
    out.append(f'<circle cx="{x-r*0.25:.1f}" cy="{y-r*0.25:.1f}" r="{r*0.15:.1f}" fill="#FFFFFF" opacity="0.7"/>')
    return "".join(out)

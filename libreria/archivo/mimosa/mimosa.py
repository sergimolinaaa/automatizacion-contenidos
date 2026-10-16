import math,random
from h import *
from plant import *
random.seed(2)
o=[SVG0,'<defs>'+DEFS+'''
<linearGradient id="wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFF4DD"/><stop offset="1" stop-color="#FCE3C0"/></linearGradient>
<linearGradient id="pot" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#E08A5A"/><stop offset="0.45" stop-color="#C96A3C"/><stop offset="1" stop-color="#8E4426"/></linearGradient>
<linearGradient id="tbl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#D9A86C"/><stop offset="1" stop-color="#A8743F"/></linearGradient>
<radialGradient id="skin" cx="0.4" cy="0.35" r="0.7"><stop offset="0" stop-color="#FBD7B5"/><stop offset="1" stop-color="#DFA57A"/></radialGradient>
</defs>
<rect width="1000" height="700" fill="url(#wall)"/>''']
# ventana y plantas lejanas (sin contorno)
o.append('<rect x="620" y="80" width="300" height="300" rx="10" fill="#CDEBFF"/><path d="M 770 80 L 770 380 M 620 230 L 920 230" stroke="#FFF4DD" stroke-width="12"/>')
o.append('<g opacity="0.45" fill="#9CCB8A"><ellipse cx="700" cy="330" rx="60" ry="40"/><ellipse cx="860" cy="320" rx="70" ry="50"/><ellipse cx="80" cy="460" rx="90" ry="60"/><ellipse cx="160" cy="430" rx="60" ry="50"/></g>')
TY=560
o.append(f'<path d="M 0 {TY} L 1000 {TY} L 1000 700 L 0 700 Z" fill="url(#tbl)" stroke="{INK}" stroke-width="7"/>')
o.append(f'<path d="M 0 {TY+10} L 1000 {TY+10}" stroke="#F0C88E" stroke-width="5"/>')
o.append('<g stroke="#8A5A2B" stroke-width="3" opacity="0.4">'+"".join(f'<path d="M {x} {y} l 260 0"/>' for x,y in [(40,610),(520,630),(240,660),(700,600)])+'</g>')
# maceta
PX=430; RIM=470
o.append(f'<ellipse cx="{PX}" cy="{TY+4}" rx="120" ry="14" fill="{INK}" opacity="0.25"/>')
o.append(f'<path d="M {PX-95} {RIM+20} L {PX-75} {TY} L {PX+75} {TY} L {PX+95} {RIM+20} Z" fill="url(#pot)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
o.append(f'<rect x="{PX-110}" y="{RIM-8}" width="220" height="36" rx="8" fill="url(#pot)" stroke="{INK}" stroke-width="7"/>')
o.append(f'<path d="M {PX-96} {RIM} L {PX+60} {RIM}" stroke="#F4B58A" stroke-width="5" stroke-linecap="round"/>')
o.append(f'<ellipse cx="{PX}" cy="{RIM-6}" rx="100" ry="10" fill="#5A3A22" stroke="{INK}" stroke-width="5"/>')
# tallo
o.append(f'<g transform="translate({PX} {RIM}) scale(0.86) translate({-PX} {-RIM})">')
stem_pts=[(PX,RIM-8),(PX-6,420),(PX+4,340),(PX-2,260),(PX+6,190)]
d="M "+" ".join(f"{x} {y}" for x,y in stem_pts[:1])+f" C {PX-14} 400, {PX+12} 330, {PX-2} 270 S {PX+10} 200, {PX+6} 180"
o.append(stroke2(d,13,"url(#stem)",8))
o.append(f'<path d="M {PX-4} {RIM-20} C {PX-14} 400, {PX+8} 330, {PX-6} 270" fill="none" stroke="#D7877A" stroke-width="3" opacity="0.8"/>')
# espinitas
for y,sd in [(440,1),(400,-1),(360,1),(300,-1),(250,1),(215,-1)]:
    x=PX+(-6 if y>380 else 0)+sd*7
    o.append(f'<path d="M {x} {y} L {x+sd*12} {y-8}" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>')
# hojas: (id, pivote, ángulo abierto, ángulo cerrado, longitud pecíolo)
leaves=[("a",(PX-6,410),196,150,135),("b",(PX+4,330),-16,40,150),("c",(PX-2,250),206,158,120),("d",(PX-4,448),-4,48,110)]
for n,(px,py),ao,ac,L in leaves:
    o.append(f'<g id="{n}closed">'+leaf(px,py,ac,L*0.95,True,1.05)+'</g>')
    o.append(f'<g id="{n}open">'+leaf(px,py,ao,L,False,1.05)+'</g>')
# flor
o.append(f'<g id="flower"><path d="M {PX+6} 182 C {PX+10} 150, {PX+30} 120, {PX+40} 104" fill="none" stroke="{INK}" stroke-width="10" stroke-linecap="round"/><path d="M {PX+6} 182 C {PX+10} 150, {PX+30} 120, {PX+40} 104" fill="none" stroke="#5DAA45" stroke-width="4" stroke-linecap="round"/>'+pompom(PX+42,98,34)+'</g>')
o.append('</g>')
# dedo (mano desde la derecha)
fx,fy=930,300
o.append(f'<g id="finger"><path d="M 1060 {fy+10} L {fx+70} {fy-6} L {fx+70} {fy+70} L 1060 {fy+80} Z" fill="#4D6FB8" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
         f'<path d="M {fx+76} {fy-10} C {fx+40} {fy-16}, {fx+10} {fy-6}, {fx-6} {fy+8} C {fx-40} {fy+6}, {fx-60} {fy+10}, {fx-62} {fy+22} C {fx-60} {fy+34}, {fx-30} {fy+34}, {fx} {fy+34} C {fx+10} {fy+60}, {fx+40} {fy+74}, {fx+76} {fy+70} Z" fill="url(#skin)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
         f'<path d="M {fx-50} {fy+14} C {fx-56} {fy+18}, {fx-56} {fy+26}, {fx-50} {fy+28}" fill="#FFE9DA" stroke="{INK}" stroke-width="3"/>'
         f'<path d="M {fx+8} {fy+40} C {fx+20} {fy+44}, {fx+30} {fy+46}, {fx+44} {fy+44} M {fx+14} {fy+54} C {fx+26} {fy+58}, {fx+36} {fy+60}, {fx+50} {fy+58}" fill="none" stroke="#B9785A" stroke-width="4" stroke-linecap="round"/>'
         f'<path d="M {fx-40} {fy+12} C {fx-20} {fy+6}, {fx} {fy+4}, {fx+20} {fy}" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" opacity="0.6"/></g>')
# chispa al tocar (en el punto de contacto tras el movimiento)
cx,cy=650,318
sp="".join(f'M {cx+math.cos(k*math.pi/4)*20:.1f} {cy+math.sin(k*math.pi/4)*20:.1f} L {cx+math.cos(k*math.pi/4)*44:.1f} {cy+math.sin(k*math.pi/4)*44:.1f} ' for k in range(8))
o.append(f'<g id="zap"><path d="{sp}" stroke="{INK}" stroke-width="12" stroke-linecap="round"/><path d="{sp}" stroke="#C8FF2E" stroke-width="6" stroke-linecap="round"/></g>')
# gota (para el experimento: no usada aquí)
o.append('</svg>')
open("mimosa.svg","w").write("\n".join(o))
print("touch",cx,cy)

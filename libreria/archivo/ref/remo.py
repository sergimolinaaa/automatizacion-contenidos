import math
INK="#0B0B14"
def leg(pts, w=10, col="#4A382B"):
    d="M "+" L ".join(f"{x} {y}" for x,y in pts)
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w+7}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')
def mirror(pts): return [(x,700-y) for x,y in pts]
o=[f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 700">
<defs>
<radialGradient id="pond" cx="0.45" cy="0.45" r="0.8"><stop offset="0" stop-color="#8FD3FF"/><stop offset="1" stop-color="#3D8FE0"/></radialGradient>
<linearGradient id="body" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9A7A5C"/><stop offset="0.5" stop-color="#5E4634"/><stop offset="1" stop-color="#2E2119"/></linearGradient>
<radialGradient id="dimple" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#2F7FD6" stop-opacity="0.65"/><stop offset="0.7" stop-color="#2F7FD6" stop-opacity="0.15"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0.7"/></radialGradient>
</defs>
<rect width="1000" height="700" fill="url(#pond)"/>
<g fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.25"><path d="M 60 120 Q 140 100 220 120"/><path d="M 760 600 Q 840 580 920 600"/><path d="M 820 110 Q 880 95 940 110"/><path d="M 80 590 Q 150 575 220 590"/></g>
<g id="leaf"><path d="M 110 520 C 150 470, 230 480, 250 530 C 210 570, 140 570, 110 520 Z" fill="#36B37E" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/><path d="M 120 522 L 240 528" stroke="{INK}" stroke-width="3"/></g>
''']
mid=[(430,322),(410,150),(560,70)]
hind=[(452,330),(580,250),(900,215)]
front=[(372,330),(330,282),(268,272)]
feet=[(560,70),(900,215),(268,272)]
feet+= [(x,700-y) for x,y in feet]
o.append('<g id="dimples">')
for i,(x,y) in enumerate(feet):
    o.append(f'<circle cx="{x}" cy="{y}" r="30" fill="url(#dimple)"/>')
o.append('</g>')
o.append('<g fill="none" stroke="#FFFFFF" stroke-width="4">')
for i,(x,y) in enumerate(feet):
    for k in (1,2):
        o.append(f'<g id="r{i}{k}"><circle cx="{x}" cy="{y}" r="44"/></g>')
o.append('</g>')
# remolinos detrás de las patas del medio
def swirl(cx,cy,s,ccw):
    pts=[]
    for k in range(0,60):
        t=k/59*3.4*math.pi
        r=s*(0.15+0.85*k/59)
        a=t if ccw else -t
        pts.append((cx+r*math.cos(a), cy+r*math.sin(a)))
    return "M "+" L ".join(f"{x:.1f} {y:.1f}" for x,y in pts)
for i,(cx,cy,ccw) in enumerate([(690,95,True),(690,605,False)]):
    d=swirl(cx,cy,62,ccw)
    o.append(f'<g id="vortex{i+1}"><circle cx="{cx}" cy="{cy}" r="70" fill="#1D5FA8" opacity="0.35"/>'
             f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="13" stroke-linecap="round"/>'
             f'<path d="{d}" fill="none" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round"/></g>')
o.append('<g id="push" opacity="0.9">')
for y in (150,550):
    o.append(f'<path d="M 790 {y} L 900 {y}" stroke="{INK}" stroke-width="16" stroke-linecap="round"/><path d="M 790 {y} L 900 {y}" stroke="#C8FF2E" stroke-width="8" stroke-linecap="round"/>'
             f'<path d="M 878 {y-18} L 902 {y} L 878 {y+18}" fill="none" stroke="{INK}" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/><path d="M 878 {y-18} L 902 {y} L 878 {y+18}" fill="none" stroke="#C8FF2E" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>')
o.append('</g>')
o.append('<g id="strider">')
o.append('<g id="legtop">'+leg(mid,11)+'</g>')
o.append('<g id="legbot">'+leg(mirror(mid),11)+'</g>')
o.append(leg(hind,10)+leg(mirror(hind),10)+leg(front,8)+leg(mirror(front),8))
o.append(f'<path d="M 440 350 C 470 318, 600 322, 680 342 C 694 346, 694 354, 680 358 C 600 378, 470 382, 440 350 Z" fill="url(#body)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
o.append(f'<ellipse cx="400" cy="350" rx="56" ry="34" fill="url(#body)" stroke="{INK}" stroke-width="7"/>')
o.append('<path d="M 470 338 C 530 328, 600 330, 660 342" fill="none" stroke="#C9A982" stroke-width="5" stroke-linecap="round" opacity="0.8"/>')
o.append('<path d="M 372 334 C 392 326, 420 326, 436 334" fill="none" stroke="#C9A982" stroke-width="5" stroke-linecap="round" opacity="0.8"/>')
o.append(f'<ellipse cx="322" cy="350" rx="34" ry="24" fill="url(#body)" stroke="{INK}" stroke-width="7"/>')
for y in (330,370):
    o.append(f'<circle cx="318" cy="{y}" r="13" fill="#2A1A14" stroke="{INK}" stroke-width="4"/><circle cx="313" cy="{y-5}" r="4.5" fill="#FFFFFF"/>')
o.append('<g id="antennae">'+leg([(292,340),(250,322),(205,326)],5)+leg([(292,360),(250,378),(205,374)],5)+'</g>')
o.append('</g>')
# flecha de avance
o.append(f'<g id="go"><path d="M 180 350 L 60 350" stroke="{INK}" stroke-width="22" stroke-linecap="round"/><path d="M 180 350 L 60 350" stroke="#C8FF2E" stroke-width="12" stroke-linecap="round"/>'
         f'<path d="M 92 318 L 58 350 L 92 382" fill="none" stroke="{INK}" stroke-width="22" stroke-linecap="round" stroke-linejoin="round"/><path d="M 92 318 L 58 350 L 92 382" fill="none" stroke="#C8FF2E" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/></g>')
def tag(id_,x,y,w,text,bg="#0B0B14",fg="#C8FF2E"):
    return (f'<g id="{id_}"><rect x="{x}" y="{y}" width="{w}" height="58" rx="12" fill="{bg}"/>'
            f'<text x="{x+w/2}" y="{y+40}" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="30" fill="{fg}">{text}</text></g>')
o.append(tag("lremo",200,118,150,"REMOS",bg="#FFFFFF",fg="#0B0B14"))
o.append(tag("lvortex",770,40,220,"REMOLINOS"))
o.append('</svg>')
print("\n".join(o))

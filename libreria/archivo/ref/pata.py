import math
INK="#0B0B14"
o=[f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 700">
<defs>
<radialGradient id="bg" cx="0.5" cy="0.5" r="0.75"><stop offset="0" stop-color="#F2FAFF"/><stop offset="1" stop-color="#CFE8FA"/></radialGradient>
<linearGradient id="seg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#A88563"/><stop offset="0.35" stop-color="#6E5240"/><stop offset="1" stop-color="#33251C"/></linearGradient>
<radialGradient id="drop" cx="0.38" cy="0.32" r="0.75"><stop offset="0" stop-color="#E4F5FF"/><stop offset="0.55" stop-color="#7CC6FF"/><stop offset="1" stop-color="#2F7FD6"/></radialGradient>
</defs>
<rect width="1000" height="700" fill="url(#bg)"/>
<g fill="none" stroke="#B9D9F0" stroke-width="2"><circle cx="500" cy="350" r="300"/><circle cx="500" cy="350" r="420"/><line x1="500" y1="0" x2="500" y2="700"/><line x1="0" y1="350" x2="1000" y2="350"/></g>
<g transform="rotate(-15 500 385)">
<g id="air"><rect x="44" y="282" width="912" height="206" rx="103" fill="#FFFFFF" fill-opacity="0.55" stroke="#FFFFFF" stroke-width="5"/></g>
<rect x="60" y="330" width="880" height="110" rx="55" fill="url(#seg)" stroke="{INK}" stroke-width="8"/>
<rect x="100" y="344" width="800" height="16" rx="8" fill="#D2B48C" opacity="0.55"/>
<g stroke="{INK}" stroke-width="3" opacity="0.35"><path d="M 330 334 Q 322 385 330 436"/><path d="M 640 334 Q 632 385 640 436"/></g>
<g id="setae" stroke="#4A382B" stroke-width="5" stroke-linecap="round">''']
hairs=[]
for x in range(112,872,20):
    if 80<x<920:
        hairs.append(f'<line x1="{x}" y1="333" x2="{x+30}" y2="290"/>')
        hairs.append(f'<line x1="{x+8}" y1="437" x2="{x+38}" y2="480"/>')
o+=hairs
o.append('</g>')
o.append(f'<g stroke="{INK}" stroke-width="2" opacity="0.5" stroke-linecap="round">'+"".join(f'<line x1="{x}" y1="333" x2="{x+30}" y2="290"/>' for x in range(112,872,60))+'</g>')
for i,(cx,cy,r) in enumerate([(330,232,58),(700,248,42)]):
    o.append(f'<g id="drop{i+1}"><ellipse cx="{cx}" cy="{cy+r-2}" rx="{r*0.5:.0f}" ry="5" fill="#2F7FD6" opacity="0.35"/>'
             f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#drop)" stroke="{INK}" stroke-width="6"/>'
             f'<ellipse cx="{cx-r*0.35:.0f}" cy="{cy-r*0.4:.0f}" rx="{r*0.28:.0f}" ry="{r*0.17:.0f}" fill="#FFFFFF" transform="rotate(-30 {cx-r*0.35:.0f} {cy-r*0.4:.0f})"/>'
             f'<circle cx="{cx+r*0.38:.0f}" cy="{cy+r*0.35:.0f}" r="{max(3,r*0.08):.0f}" fill="#FFFFFF" opacity="0.8"/></g>')
o.append('</g>')
def tag(id_,x,y,w,text,lx1,ly1,lx2,ly2,bg="#0B0B14",fg="#C8FF2E"):
    return (f'<g id="{id_}"><line x1="{lx1}" y1="{ly1}" x2="{lx2}" y2="{ly2}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
            f'<circle cx="{lx2}" cy="{ly2}" r="9" fill="#C8FF2E" stroke="{INK}" stroke-width="4"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="58" rx="12" fill="{bg}"/>'
            f'<text x="{x+w/2}" y="{y+40}" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="30" fill="{fg}">{text}</text></g>')
o.append(tag("lgota",760,118,160,"GOTA",800,176,690,222))
o.append(tag("lpelos",650,560,250,"PELITOS",720,560,632,462))
o.append(tag("laire",250,592,330,"AIRE ATRAPADO",400,592,392,528))
o.append(f'<g id="zoomtag"><rect x="830" y="40" width="130" height="50" rx="25" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/><text x="895" y="75" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="26" fill="{INK}">×1000</text></g>')
o.append('</svg>')
print("\n".join(o))

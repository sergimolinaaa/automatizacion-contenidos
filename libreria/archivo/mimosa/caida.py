import math,random
from h import *
from plant import *
random.seed(8)
o=[SVG0,'<defs>'+DEFS+'''
<linearGradient id="lab" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#EAF2FA"/><stop offset="1" stop-color="#CCDCEB"/></linearGradient>
<linearGradient id="metal" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#E6ECF2"/><stop offset="0.5" stop-color="#A9B6C4"/><stop offset="1" stop-color="#6E7C8C"/></linearGradient>
<linearGradient id="pot" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#E08A5A"/><stop offset="0.45" stop-color="#C96A3C"/><stop offset="1" stop-color="#8E4426"/></linearGradient>
<linearGradient id="foam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFE68A"/><stop offset="1" stop-color="#F2C14E"/></linearGradient>
<linearGradient id="bench" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9AA9B8"/><stop offset="1" stop-color="#6C7A88"/></linearGradient>
</defs>
<rect width="1000" height="700" fill="url(#lab)"/>''']
o.append('<g opacity="0.5"><rect x="40" y="110" width="200" height="14" rx="4" fill="#B7C7D8"/><rect x="760" y="140" width="200" height="14" rx="4" fill="#B7C7D8"/>'
         '<rect x="70" y="60" width="30" height="50" rx="6" fill="#9FD3B0"/><rect x="120" y="76" width="40" height="34" rx="6" fill="#F3B6A0"/><rect x="800" y="96" width="34" height="44" rx="6" fill="#A8C8F0"/><circle cx="890" cy="118" r="20" fill="#9FD3B0"/></g>')
BY=590
o.append(f'<rect x="-10" y="{BY}" width="1020" height="120" fill="url(#bench)" stroke="{INK}" stroke-width="7"/>')
o.append(f'<path d="M 0 {BY+10} L 1000 {BY+10}" stroke="#C9D5E0" stroke-width="5"/>')
# espuma
FT=530
o.append(f'<g id="foam"><rect x="300" y="{FT}" width="400" height="{BY-FT}" rx="10" fill="url(#foam)" stroke="{INK}" stroke-width="7"/>'+"".join(f'<ellipse cx="{random.uniform(320,680):.0f}" cy="{random.uniform(FT+14,BY-12):.0f}" rx="{random.uniform(4,8):.0f}" ry="{random.uniform(3,5):.0f}" fill="#D9A43A"/>' for _ in range(22))+f'<path d="M 312 {FT+8} L 680 {FT+8}" stroke="#FFF6C8" stroke-width="5" stroke-linecap="round"/></g>')
# raíles
for x in (320,680):
    o.append(f'<rect x="{x-11}" y="110" width="22" height="{BY-110}" rx="6" fill="url(#metal)" stroke="{INK}" stroke-width="6"/>')
o.append("".join(f'<circle cx="{x}" cy="110" r="16" fill="url(#metal)" stroke="{INK}" stroke-width="6"/>' for x in (320,680)))
# regla
o.append(f'<g id="ruler"><rect x="730" y="200" width="46" height="{FT-200}" rx="6" fill="#FFF4DD" stroke="{INK}" stroke-width="6"/>'+"".join(f'<path d="M 730 {y} l {22 if (y-200)%60==0 else 12} 0" stroke="{INK}" stroke-width="4"/>' for y in range(220,FT,20))+'</g>')
# maceta con planta, arriba (cae DROP unidades)
DROP=140
PB=FT-DROP   # base de la maceta arriba
cx=500
pot=[f'<g id="pot">']
pot.append(f'<rect x="{cx-180}" y="{PB-14}" width="360" height="20" rx="6" fill="url(#metal)" stroke="{INK}" stroke-width="6"/>')
pot.append(f'<path d="M {cx-62} {PB-90} L {cx-48} {PB-14} L {cx+48} {PB-14} L {cx+62} {PB-90} Z" fill="url(#pot)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
pot.append(f'<rect x="{cx-74}" y="{PB-110}" width="148" height="26" rx="7" fill="url(#pot)" stroke="{INK}" stroke-width="6"/>')
pot.append(f'<ellipse cx="{cx}" cy="{PB-108}" rx="66" ry="7" fill="#5A3A22" stroke="{INK}" stroke-width="4"/>')
top=PB-112
sd=f"M {cx} {top} C {cx-6} {top-34}, {cx+6} {top-70}, {cx+2} {top-104}"
pot.append(stroke2(sd,9,"url(#stem)",6))
lv=[((cx-2,top-26),194,145,78),((cx+2,top-52),-14,40,82),((cx-1,top-78),206,155,66),((cx+2,top-100),-34,25,52)]
pot.append('<g id="pclosed">'+"".join(leaf(p[0],p[1],ac,L*0.95,True,0.62,nlet=10) for p,ao,ac,L in lv)+'</g>')
pot.append('<g id="popen">'+"".join(leaf(p[0],p[1],ao,L,False,0.62,nlet=10) for p,ao,ac,L in lv)+'</g>')
pot.append('</g>')
o.append("".join(pot))
# líneas de velocidad (sobre la maceta ya caída)
ml="".join(stroke2(f"M {x} {FT-330} L {x} {FT-230}",6,"#FFFFFF",6) for x in (380,620))
o.append(f'<g id="motion">{ml}</g>')
# rebote/golpe
o.append(f'<g id="bump">'+"".join(stroke2(f"M {x1} {y1} L {x2} {y2}",6,"#FF5A36",6) for x1,y1,x2,y2 in [(710,FT-6,738,FT-26),(718,FT+12,750,FT+12)])+'</g>')
# memoria: calendario
kx,ky=790,90
o.append(f'<g id="calendar"><rect x="{kx}" y="{ky}" width="170" height="150" rx="16" fill="#FFFFFF" stroke="{INK}" stroke-width="7"/><path d="M {kx} {ky+16} a 16 16 0 0 1 16 -16 L {kx+154} {ky} a 16 16 0 0 1 16 16 L {kx+170} {ky+46} L {kx} {ky+46} Z" fill="#FF5A36" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
         f'<rect x="{kx+34}" y="{ky-18}" width="14" height="36" rx="6" fill="{INK}"/><rect x="{kx+122}" y="{ky-18}" width="14" height="36" rx="6" fill="{INK}"/>'
         f'<text x="{kx+85}" y="{ky+108}" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="44" fill="{INK}">1 MES</text></g>')
o.append(tag("lfoam",40,420,"SIN DAÑO",w=190,lead=(135,478,310,548)))
o.append('</svg>')
open("caida.svg","w").write("\n".join(o))
print("DROP",DROP)

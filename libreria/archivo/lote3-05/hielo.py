import math, random, sys
sys.path.insert(0, sys.path[0])
from common import *

random.seed(8)
WS = 410     # superficie del agua
MT = 480     # superficie del barro (fondo del charco)
IT, IB = 402, 420  # hielo: arriba / abajo
RX0, RX1 = 430, 700  # piedra
MOVE = 130

defs = '''
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8EC2EC"/><stop offset="1" stop-color="#F7E6CC"/></linearGradient>
<linearGradient id="water" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8FD3FF" stop-opacity="0.9"/><stop offset="1" stop-color="#3C8EDB" stop-opacity="0.9"/></linearGradient>
<linearGradient id="ice" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="0.5" stop-color="#D8F3FF"/><stop offset="1" stop-color="#A9DDF5"/></linearGradient>
<linearGradient id="mud" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9C7B58"/><stop offset="0.25" stop-color="#B8936A"/><stop offset="1" stop-color="#7C5C40"/></linearGradient>
<linearGradient id="rock" x1="0" y1="0" x2="0.35" y2="1"><stop offset="0" stop-color="#93867A"/><stop offset="0.5" stop-color="#655A51"/><stop offset="1" stop-color="#3A322C"/></linearGradient>
<radialGradient id="sunglow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#FFF6D0"/><stop offset="0.6" stop-color="#FFE48A" stop-opacity="0.8"/><stop offset="1" stop-color="#FFE48A" stop-opacity="0"/></radialGradient>
<radialGradient id="moon" cx="0.4" cy="0.4" r="0.7"><stop offset="0" stop-color="#FFFBE6"/><stop offset="1" stop-color="#E9DDA8"/></radialGradient>
'''
o = [head(defs)]
o.append('<rect width="1000" height="700" fill="url(#sky)"/>')
o.append(f'<path d="M 0 {WS-60} L 110 {WS-130} L 220 {WS-95} L 330 {WS-170} L 450 {WS-110} L 560 {WS-150} L 680 {WS-95} L 790 {WS-160} L 900 {WS-115} L 1000 {WS-140} L 1000 {WS} L 0 {WS} Z" fill="#D2BFC6"/>')
o.append(f'<path d="M 0 {WS-25} L 150 {WS-60} L 300 {WS-35} L 460 {WS-70} L 620 {WS-40} L 780 {WS-65} L 1000 {WS-35} L 1000 {WS} L 0 {WS} Z" fill="#C2A595"/>')
# sol
o.append('<g id="sol"><circle cx="860" cy="130" r="95" fill="url(#sunglow)"/>'
         + "".join(f'<line x1="{860+60*math.cos(math.radians(a)):.0f}" y1="{130+60*math.sin(math.radians(a)):.0f}" x2="{860+82*math.cos(math.radians(a)):.0f}" y2="{130+82*math.sin(math.radians(a)):.0f}" stroke="#FFB52E" stroke-width="8" stroke-linecap="round"/>' for a in range(0, 360, 45))
         + f'<circle cx="860" cy="130" r="44" fill="#FFE27A" stroke="{INK}" stroke-width="6"/><circle cx="846" cy="116" r="12" fill="#FFF6C8"/></g>')
# lluvia
o.append('<g id="lluvia" stroke="#4F8FD6" stroke-width="5" stroke-linecap="round">' + "".join(
    f'<line x1="{x}" y1="{y}" x2="{x-10}" y2="{y+34}"/>' for x, y in [(390, 120), (470, 200), (560, 110), (640, 240), (720, 150), (300, 230), (220, 140), (420, 300), (600, 330), (140, 260), (980, 300), (900, 360)]) + '</g>')

# playa lejana detrás del charco
o.append(f'<rect y="{WS-6}" width="1000" height="{MT-WS+6}" fill="#E4D3B2"/>')
o.append(f'<line x1="0" y1="{WS-6}" x2="1000" y2="{WS-6}" stroke="#CDB792" stroke-width="3"/>')
# barro (corte) con surco ya hecho detrás de la piedra
o.append(f'<rect y="{MT}" width="1000" height="{700-MT}" fill="url(#mud)"/>')
o.append('<g stroke="#8A6A4A" stroke-width="3" opacity="0.5" fill="none">' + "".join(f'<path d="M {x} {y} q 30 -6 60 0 t 60 0"/>' for x, y in [(40, 580), (300, 620), (620, 570), (820, 640), (160, 660), (500, 670)]) + '</g>')
o.append('<g fill="#6E5034" opacity="0.6">' + "".join(f'<ellipse cx="{random.randint(20, 980)}" cy="{random.randint(540, 690)}" rx="{random.randint(4, 9)}" ry="{random.randint(3, 6)}"/>' for _ in range(22)) + '</g>')
# fondo del surco antiguo (detrás de la piedra)
o.append(f'<line x1="0" y1="{MT}" x2="1000" y2="{MT}" stroke="{INK}" stroke-width="6"/>')
o.append(f'<path d="M 30 {MT+8} L {RX0+20} {MT+8}" stroke="#3E2A18" stroke-width="16" stroke-linecap="round"/>')
# surco nuevo que se dibuja al moverse
o.append(f'<g id="surconuevo"><path d="M {RX0+20} {MT+8} L {RX0+MOVE+20} {MT+8}" stroke="#3E2A18" stroke-width="16" stroke-linecap="round"/></g>')

def rock_d(x0, x1):
    w = x1 - x0
    return (f"M {x0+10} {MT+8} C {x0-14} {MT-80}, {x0+14} {MT-190}, {x0+90} {MT-240} C {x0+140} {MT-268}, {x0+205} {MT-258}, {x0+240} {MT-215} "
            f"C {x1+8} {MT-170}, {x1+16} {MT-70}, {x1-6} {MT+8} Z")


o.append(f'<g id="piedra">')
o.append(f'<ellipse cx="{(RX0+RX1)/2}" cy="{MT+10}" rx="{(RX1-RX0)/2+10}" ry="10" fill="#3A2A1A" opacity="0.5"/>')
o.append(f'<path d="{rock_d(RX0, RX1)}" fill="url(#rock)" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>')
o.append(f'<path d="M {RX0+34} {MT-150} C {RX0+44} {MT-200}, {RX0+95} {MT-240}, {RX0+150} {MT-248}" fill="none" stroke="#C2B6AA" stroke-width="8" stroke-linecap="round" opacity="0.85"/>')
o.append(f'<g stroke="#2A2420" stroke-width="4" stroke-linecap="round" opacity="0.55" fill="none"><path d="M {RX0+90} {MT-120} l 30 26 l -6 30"/><path d="M {RX0+170} {MT-150} l -14 40"/><path d="M {RX0+60} {MT-60} l 40 6"/></g>')
o.append(f'<g fill="#A89C90" opacity="0.7"><circle cx="{RX0+150}" cy="{MT-100}" r="6"/><circle cx="{RX0+70}" cy="{MT-150}" r="4"/><circle cx="{RX0+190}" cy="{MT-60}" r="5"/></g>')
o.append('</g>')

# agua del charco
o.append(f'<g id="agua"><rect x="0" y="{WS}" width="1000" height="{MT-WS}" fill="url(#water)" opacity="0.8"/>'
         f'<line x1="0" y1="{WS}" x2="1000" y2="{WS}" stroke="{INK}" stroke-width="5"/>'
         f'<line x1="0" y1="{WS+7}" x2="1000" y2="{WS+7}" stroke="#FFFFFF" stroke-width="3" opacity="0.6"/></g>')


# placa de hielo (izquierda, empuja la piedra) y otra a la derecha
def ice(x0, x1, gid, cracks):
    s = f'<g id="{gid}"><path d="M {x0} {IT+2} L {x1-4} {IT} L {x1} {IB} L {x0} {IB+1} Z" fill="url(#ice)" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    s += f'<line x1="{x0+6}" y1="{IT+4}" x2="{x1-10}" y2="{IT+3}" stroke="#FFFFFF" stroke-width="3"/>'
    s += '</g>'
    return s


o.append(ice(-20, RX0 + 4, "hielo", []))
o.append(ice(RX1 + 16, 1020, "hielo2", []))
# grietas
o.append(f'<g id="grietas" stroke="{INK}" stroke-width="4" stroke-linecap="round">' + "".join(
    f'<path d="M {x} {IT} l -4 6 l 6 4 l -3 6"/>' for x in (120, 300, 860)) + '</g>')

# noche (capa) + luna
o.append(f'<g id="noche"><rect width="1000" height="700" fill="#14214A" opacity="0.6"/></g>')
o.append(f'<g id="luna"><circle cx="840" cy="130" r="42" fill="url(#moon)" stroke="{INK}" stroke-width="6"/><circle cx="826" cy="120" r="8" fill="#D8CB8E"/><circle cx="854" cy="146" r="6" fill="#D8CB8E"/>'
         + "".join(f'<circle cx="{x}" cy="{y}" r="3" fill="#FFFFFF"/>' for x, y in [(520, 90), (650, 160), (420, 200), (720, 70), (940, 230)]) + '</g>')
# viento
o.append('<g id="viento">' + arrow("w1", [(40, 290), (160, 280), (290, 290)], col=LIME, w=12)
         + arrow("w2", [(70, 350), (180, 342), (320, 350)], col=LIME, w=12) + '</g>')
# empuje del hielo sobre la piedra
o.append('<g id="empuje">' + arrow("e1", [(290, 380), (385, 380)], col=CORAL, w=12, head_len=30) + '</g>')

o.append(tag("lhielo", 150, 560, tw("HIELO"), "HIELO", 230, 560, 240, 412))
o.append(tag("lagua", 330, 600, tw("AGUA"), "AGUA", 390, 600, 380, 452))
o.append(tag("lbarro", 760, 600, tw("BARRO"), "BARRO", 830, 600, 830, 520))
o.append(tag("lviento", 80, 190, tw("VIENTO"), "VIENTO"))
o.append(tag("lsurco", 300, 600, tw("SURCO"), "SURCO", 380, 600, 400, 492))
if len(sys.argv) > 1 and sys.argv[1] == "free":
    skip = ['url(#sky)', 'fill="#D2BFC6"', 'fill="#C2A595"', 'id="sol"', 'id="lluvia"', '#E4D3B2', '#CDB792', 'id="noche"', 'id="luna"']
    clip = ['url(#mud)', '#8A6A4A', '#6E5034', f'y2="{MT}" stroke', f'M 30 {MT+8}', 'id="surconuevo"', 'id="agua"', 'id="hielo"', 'id="hielo2"', 'id="grietas"']
    out = [o[0].replace('viewBox="0 0 1000 700"', 'viewBox="0 0 1000 860"').replace('</defs>', f'<clipPath id="slab"><rect x="30" y="{WS-40}" width="940" height="{700-WS+40}" rx="34"/></clipPath>\n</defs>'),
           '<g transform="translate(0 110)">']
    for item in o[1:]:
        if any(k in item for k in skip):
            continue
        if item.startswith('<g id="viento"'):
            out.append(f'<path d="M 30 {WS} L 30 666 Q 30 700, 64 700 L 936 700 Q 970 700, 970 666 L 970 {WS}" fill="none" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>')
            out.append(f'<ellipse cx="500" cy="720" rx="430" ry="16" fill="#0B0B14" opacity="0.25"/>')
        if any(k in item for k in clip):
            item = f'<g clip-path="url(#slab)">{item}</g>'
        out.append(item)
    out.append('</g>')
    o = out
o.append('</svg>')
print("\n".join(o))

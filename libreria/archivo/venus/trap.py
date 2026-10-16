"""Trampa de venus atrapamoscas de perfil (bisagra a la izquierda, se abre hacia la derecha)."""
import sys, math, random
sys.path.insert(0, '/tmp/claude-0/-home-user-automatizacion-contenidos/039df981-7a17-5355-b711-18510fb209db/scratchpad/bomb')
from lib import *

DEFS = '''
<linearGradient id="vShell" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9BE36B"/><stop offset="0.55" stop-color="#4FB047"/><stop offset="1" stop-color="#2F7D34"/></linearGradient>
<linearGradient id="vShellB" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#7FD15A"/><stop offset="0.55" stop-color="#3F9A3C"/><stop offset="1" stop-color="#236A2B"/></linearGradient>
<radialGradient id="vRed" cx="0.5" cy="0.9" r="0.9"><stop offset="0" stop-color="#FF5A5F"/><stop offset="0.6" stop-color="#D7263D"/><stop offset="1" stop-color="#8E1328"/></radialGradient>
<linearGradient id="vPet" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#3F9A3C"/><stop offset="0.5" stop-color="#7FD15A"/><stop offset="1" stop-color="#3F9A3C"/></linearGradient>
'''

L = 420


def lobe_canonical(lower=False, hair_id=None, teeth=True, hairs=(150, 235, 315)):
    """Lóbulo superior en posición cerrada: bisagra en (0,0), labio sobre y=0, se extiende a +x y hacia arriba.
    Con lower=True se refleja (y -> -y)."""
    sg = -1 if lower else 1  # sg=1: hacia arriba (y negativo)
    def Y(v):
        return -sg * v
    o = []
    # dientes (cilios) del borde: salen del labio, apuntan hacia fuera y en diagonal
    if teeth:
        tt = []
        for k, x in enumerate(range(40, 420, 24)):
            ln = 44 + 8 * math.sin(k * 1.3)
            d = f"M {x} {Y(2)} Q {x+ln*0.45} {Y(-ln*0.15)} {x+ln*0.8} {Y(-ln*0.5)}"
            tt.append(stroke2(d, 5, "#B6E36A", extra=6))
        o.append('<g>' + "".join(tt) + '</g>')
    shell = (f"M 0 0 C 14 {Y(92)}, 150 {Y(150)}, 290 {Y(134)} C 380 {Y(124)}, 432 {Y(72)}, 426 {Y(12)} L 420 0 Z")
    o.append(f'<path d="{shell}" fill="{"url(#vShellB)" if lower else "url(#vShell)"}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>')
    # venas del dorso
    for k in range(5):
        x = 80 + k * 70
        o.append(f'<path d="M {x-50} {Y(20)} C {x-30} {Y(76)}, {x} {Y(100)}, {x+30} {Y(118-k*9)}" fill="none" stroke="#2F7D34" stroke-width="2.5" opacity="0.45"/>')
    if not lower:
        o.append(f'<path d="M 40 {Y(100)} C 120 {Y(140)}, 240 {Y(144)}, 330 {Y(124)}" fill="none" stroke="#D9FFB0" stroke-width="5" stroke-linecap="round" opacity="0.85"/>')
    # cara interior roja (se ve en escorzo)
    face = f"M 12 {Y(2)} C 90 {Y(60)}, 280 {Y(80)}, 414 {Y(14)} L 418 0 L 12 0 Z"
    o.append(f'<path d="{face}" fill="url(#vRed)" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')
    # glándulas digestivas (puntitos)
    random.seed(9 if lower else 4)
    dots = []
    for _ in range(46):
        x = random.uniform(40, 400)
        top = 60 * math.sin(math.pi * (x - 12) / 406) + 6
        y = random.uniform(6, max(8, top - 6))
        dots.append(f'<circle cx="{x:.0f}" cy="{Y(y):.0f}" r="{random.uniform(1.8, 3.2):.1f}"/>')
    o.append('<g fill="#7A0E20" opacity="0.6">' + "".join(dots) + '</g>')
    # borde verde claro (zona de néctar)
    o.append(f'<path d="M 18 0 L 416 0" stroke="#C9F27E" stroke-width="7" stroke-linecap="round"/>')
    o.append(f'<path d="M 18 0 L 416 0" stroke="{INK}" stroke-width="2.5" stroke-linecap="round" opacity="0.6" transform="translate(0 {sg*-4})"/>')
    # pelitos sensores (3): salen de la cara roja hacia el interior de la trampa
    hs = []
    for x in hairs:
        top = 60 * math.sin(math.pi * (x - 12) / 406)
        y0 = top * 0.55
        d = f"M {x} {Y(y0)} L {x+6} {Y(y0-30)}"
        hs.append(stroke2(d, 3.5, "#FFD6A8", extra=4) + f'<circle cx="{x}" cy="{Y(y0):.1f}" r="4.5" fill="#FFB27A" stroke="{INK}" stroke-width="2"/>')
    ids = hair_id or {}
    for k, h in enumerate(hs):
        o.append(f'<g id="{ids[k]}">' + h + '</g>' if k in ids else h)
    return "".join(o)


def lobe(id_, hx, hy, ang, scale=1.0, lower=False, hair_id=None, R=480, teeth=True):
    """Lóbulo colocado: bisagra en (hx,hy), girado `ang` grados. Caja invisible centrada en la bisagra
    para que origin=center gire justo sobre la bisagra."""
    r = R * scale
    return (f'<g id="{id_}"><rect x="{hx-r:.1f}" y="{hy-r:.1f}" width="{2*r:.1f}" height="{2*r:.1f}" fill="none" stroke="none"/>'
            f'<g transform="translate({hx} {hy}) rotate({ang}) scale({scale})">' + lobe_canonical(lower, hair_id, teeth) + '</g></g>')


def petiole(x0, y0, hx, hy, w=46, scale=1.0):
    """Peciolo alado (hoja aplanada) desde (x0,y0) hasta la bisagra."""
    mx, my = (x0 + hx) / 2, (y0 + hy) / 2
    dx, dy = hx - x0, hy - y0
    ln = math.hypot(dx, dy); nx, ny = -dy / ln, dx / ln
    w *= scale
    a = (x0 + nx * 6 * scale, y0 + ny * 6 * scale); b = (x0 - nx * 6 * scale, y0 - ny * 6 * scale)
    c1 = (mx + nx * w + dx * 0.1, my + ny * w + dy * 0.1); c2 = (mx - nx * w + dx * 0.1, my - ny * w + dy * 0.1)
    d = (f"M {a[0]:.1f} {a[1]:.1f} Q {c1[0]:.1f} {c1[1]:.1f} {hx+nx*10*scale:.1f} {hy+ny*10*scale:.1f} "
         f"L {hx-nx*10*scale:.1f} {hy-ny*10*scale:.1f} Q {c2[0]:.1f} {c2[1]:.1f} {b[0]:.1f} {b[1]:.1f} Z")
    s = f'<path d="{d}" fill="url(#vShell)" stroke="{INK}" stroke-width="{7*min(1,scale+0.2):.1f}" stroke-linejoin="round"/>'
    s += f'<path d="M {x0:.1f} {y0:.1f} L {hx:.1f} {hy:.1f}" stroke="#2F7D34" stroke-width="{4*scale:.1f}" opacity="0.7"/>'
    s += f'<circle cx="{hx}" cy="{hy}" r="{12*scale:.1f}" fill="#3F9A3C" stroke="{INK}" stroke-width="{5*scale:.1f}"/>'
    return s


def fly(id_, x, y, s=1.0, ang=0, wings_id=None):
    """Mosca vista de lado/arriba, mirando a la izquierda."""
    g = [f'<g id="{id_}"><g transform="translate({x} {y}) rotate({ang}) scale({s})">']
    # patas
    for (ax, bx, cx_) in ((-8, -22, -30), (2, 0, -4), (12, 24, 30)):
        g.append(stroke2(f"M {ax} 8 L {bx} 24 L {cx_} 34", 3, "#2A2A33", extra=3))
    w = (f'<g id="{wings_id}">' if wings_id else '<g>')
    w += f'<path d="M 4 -10 C 10 -46, 40 -54, 50 -36 C 54 -22, 30 -12, 6 -8 Z" fill="#E6F4FF" fill-opacity="0.75" stroke="{INK}" stroke-width="3"/>'
    w += f'<path d="M 10 -14 C 24 -30, 36 -38, 44 -36" fill="none" stroke="#9CB6CC" stroke-width="2"/>'
    w += f'<path d="M 0 -8 C -2 -40, 22 -56, 34 -44 C 42 -34, 22 -16, 2 -6 Z" fill="#F2FAFF" fill-opacity="0.8" stroke="{INK}" stroke-width="3"/></g>'
    g.append(f'<ellipse cx="14" cy="2" rx="22" ry="14" fill="#3D4A3A" stroke="{INK}" stroke-width="4"/>')
    g.append('<path d="M 4 -6 L 4 10 M 14 -10 L 14 12 M 24 -8 L 24 10" stroke="#9AA88A" stroke-width="2.5" opacity="0.8"/>')
    g.append(f'<ellipse cx="-10" cy="-2" rx="13" ry="12" fill="#2E3A2C" stroke="{INK}" stroke-width="4"/>')
    g.append(f'<circle cx="-22" cy="-4" r="9" fill="#C0392B" stroke="{INK}" stroke-width="3.5"/><circle cx="-25" cy="-7" r="3" fill="#FFFFFF"/>')
    g.append(w)
    g.append('</g></g>')
    return "".join(g)


def counter(id_, cx, cy, n, col=LIME, r=34):
    return (f'<g id="{id_}"><circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}" stroke="{INK}" stroke-width="6"/>'
            f'<text x="{cx}" y="{cy+15}" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="44" fill="{INK}">{n}</text></g>')

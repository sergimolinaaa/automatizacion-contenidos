"""Gancho: tarjeta de comentario estilo red social (full 1080x1920). Avatar y nombre en grupos separados (id avatar / nombre)."""
import math, random, sys
sys.path.insert(0, sys.path[0])
from common import *

random.seed(3)
W, H = 1080, 1920
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">']
o.append('''<defs>
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9FD0F5"/><stop offset="0.55" stop-color="#D6ECFB"/><stop offset="1" stop-color="#F2F9FF"/></linearGradient>
<linearGradient id="card" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#EEF1F6"/></linearGradient>
<radialGradient id="av" cx="0.4" cy="0.3" r="0.8"><stop offset="0" stop-color="#D9DEE8"/><stop offset="1" stop-color="#9AA3B5"/></radialGradient>
<linearGradient id="sil" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#E4E8F0"/></linearGradient>
<clipPath id="avclip"><circle cx="215" cy="770" r="66"/></clipPath>
</defs>''')
o.append(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')
# bokeh lejano
o.append('<g fill="#FFFFFF" opacity="0.55">' + "".join(f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x, y, r in
         [(140, 260, 70), (900, 200, 50), (520, 360, 34), (220, 1450, 60), (880, 1420, 80), (620, 1760, 46), (90, 1000, 30), (1000, 900, 40)]) + '</g>')


def flake(cx, cy, r, rotd=0):
    arms = []
    for k in range(6):
        a = math.radians(k * 60 + rotd)
        arms.append(f"M {cx} {cy} L {cx + r*math.cos(a):.1f} {cy + r*math.sin(a):.1f}")
        bx, by = cx + r * 0.55 * math.cos(a), cy + r * 0.55 * math.sin(a)
        for sgn in (-1, 1):
            b2 = a + sgn * math.radians(45)
            arms.append(f"M {bx:.1f} {by:.1f} L {bx + r*0.35*math.cos(b2):.1f} {by + r*0.35*math.sin(b2):.1f}")
    d = " ".join(arms)
    return (f'<path d="{d}" fill="none" stroke="#5E9BD1" stroke-width="{r*0.26+5:.1f}" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="#FFFFFF" stroke-width="{r*0.26:.1f}" stroke-linecap="round"/>')


o.append('<g id="snowtop">' + flake(150, 230, 30, 5) + flake(430, 150, 22, 12) + flake(760, 330, 26, 0) + flake(960, 140, 20, 8) + '</g>')
o.append('<g id="snowbot">' + flake(170, 1500, 26, 3) + flake(520, 1400, 20, 10) + flake(840, 1580, 30, 0) + flake(390, 1720, 18, 5) + '</g>')

o.append('<g transform="translate(540 835) scale(1.13) translate(-540 -835)">')
# tarjeta
X0, Y0, X1, Y1 = 90, 660, 990, 1010
o.append('<g id="card">')
o.append(f'<rect x="{X0+10}" y="{Y0+22}" width="{X1-X0}" height="{Y1-Y0}" rx="44" fill="#2B4A6B" opacity="0.22"/>')
o.append(f'<rect x="{X0}" y="{Y0}" width="{X1-X0}" height="{Y1-Y0}" rx="44" fill="url(#card)" stroke="{INK}" stroke-width="8"/>')
o.append(f'<path d="M {X0+40} {Y0+14} L {X1-40} {Y0+14}" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round" opacity="0.9"/>')
# comentario
o.append(f'<text x="310" y="878" font-family="Unbounded" font-weight="800" font-size="50" fill="{INK}">¿Y los escalofríos?</text>')
# fila de acciones
o.append(f'<text x="310" y="958" font-family="JetBrains Mono" font-weight="800" font-size="30" fill="#8A93A6">Responder</text>')
o.append('</g>')
# corazón (me gusta)
hx, hy = 915, 780
hd = (f"M {hx} {hy+30} C {hx-50} {hy-2}, {hx-34} {hy-40}, {hx} {hy-18} C {hx+34} {hy-40}, {hx+50} {hy-2}, {hx} {hy+30} Z")
o.append(f'<g id="corazon"><path d="{hd}" fill="#FF5A6E" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
         f'<ellipse cx="{hx-14}" cy="{hy-14}" rx="8" ry="5" fill="#FFFFFF" opacity="0.8" transform="rotate(-30 {hx-14} {hy-14})"/></g>')
# avatar genérico (silueta) -> sustituible
o.append('<g id="avatar">')
o.append('<circle cx="219" cy="776" r="66" fill="#2B4A6B" opacity="0.2"/>')
o.append('<circle cx="215" cy="770" r="66" fill="url(#av)"/>')
o.append('<g clip-path="url(#avclip)">'
         '<circle cx="215" cy="750" r="26" fill="url(#sil)"/>'
         '<path d="M 160 840 C 160 795, 185 782, 215 782 C 245 782, 270 795, 270 840 Z" fill="url(#sil)"/></g>')
o.append(f'<circle cx="215" cy="770" r="66" fill="none" stroke="{INK}" stroke-width="7"/>')
o.append('</g>')
# nombre genérico -> sustituible
o.append(f'<g id="nombre"><text x="310" y="780" font-family="JetBrains Mono" font-weight="800" font-size="34" fill="#5B6478">Un seguidor</text></g>')

# rótulo superior "NOS PREGUNTÁIS"
t = "NOS PREGUNTÁIS"
w = tw(t, 34)
o.append(f'<g id="lpregunta"><rect x="{X0+30}" y="{Y0-48}" width="{w}" height="64" rx="14" fill="{INK}"/>'
         f'<text x="{X0+30+w/2}" y="{Y0-4}" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="34" fill="{LIME}">{t}</text></g>')

# líneas de temblor a los lados
def shiver(x, y, s):
    d = f"M {x} {y} q {8*s} 14 0 28 q {-8*s} 14 0 28 q {8*s} 14 0 28"
    return stroke2(d, 7, "#5E9BD1", 6)
o.append('<g id="temblor">' + shiver(860, 540, 1) + shiver(900, 560, 1) + shiver(940, 540, 1) + '</g>')

o.append('</g>')
# respuesta: flecha + bocadillo lima
o.append('<g id="respuesta">')
o.append(stroke2("M 300 1060 C 300 1140, 360 1170, 450 1170", 12, LIME, 8))
o.append(f'<path d="M 440 1140 L 482 1170 L 440 1200 Z" fill="{LIME}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
t2 = "EL TRUCO, AQUÍ"
w2 = tw(t2, 34)
o.append(f'<rect x="500" y="1136" width="{w2}" height="68" rx="16" fill="{LIME}" stroke="{INK}" stroke-width="6"/>'
         f'<text x="{500+w2/2}" y="1182" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="34" fill="{INK}">{t2}</text>')
o.append('</g>')
o.append('</svg>')
print("\n".join(o))

"""Hormiga de perfil mirando a la izquierda. Coordenadas locales: cabeza en x~0, suelo en y=+58."""
from lib import *

DEFS = '''
<linearGradient id="aBody" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8A4A30"/><stop offset="0.5" stop-color="#4A2216"/><stop offset="1" stop-color="#1E0C08"/></linearGradient>
'''
AL = "#5A2C1C"
AF = "#3A1C12"


def aleg(pts, col, w=5.5):
    return stroke2(P(pts), w, col, extra=5)


def ant(id_="ant"):
    o = [f'<g id="{id_}">']
    o.append('<ellipse cx="85" cy="60" rx="95" ry="8" fill="#3B2412" opacity="0.25"/>')
    # patas lejanas
    o.append(aleg([(52, 18), (30, 30), (14, 56), (2, 57)], AF, 4.5))
    o.append(aleg([(68, 20), (78, 36), (92, 56), (104, 57)], AF, 4.5))
    o.append(aleg([(82, 18), (112, 30), (134, 56), (148, 57)], AF, 4.5))
    # gáster
    o.append(f'<path d="M 120 6 C 140 -16, 186 -14, 200 6 C 210 22, 196 40, 170 42 C 146 44, 122 32, 118 18 Z" fill="url(#aBody)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
    o.append(f'<path d="M 146 -6 C 150 10, 150 28, 144 40 M 170 -8 C 176 10, 176 28, 170 42" fill="none" stroke="#C07A5A" stroke-width="2.5" opacity="0.6"/>')
    o.append('<path d="M 136 -4 C 152 -14, 178 -14, 192 -2" fill="none" stroke="#E0A080" stroke-width="3.5" stroke-linecap="round" opacity="0.8"/>')
    # peciolo
    o.append(f'<path d="M 98 14 C 102 -2, 114 -2, 118 14 C 116 22, 102 22, 98 14 Z" fill="url(#aBody)" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    # mesosoma
    o.append(f'<path d="M 38 4 C 46 -14, 70 -14, 80 -4 C 88 2, 98 6, 102 14 C 100 24, 80 26, 62 24 C 46 22, 36 16, 38 4 Z" fill="url(#aBody)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
    o.append('<path d="M 46 -4 C 54 -12, 68 -12, 76 -6" fill="none" stroke="#E0A080" stroke-width="3.5" stroke-linecap="round" opacity="0.8"/>')
    # cabeza
    o.append('<g id="anthead">')
    o.append(f'<path d="M -8 18 C -26 18, -34 26, -36 34 C -28 30, -20 30, -12 30 Z" fill="#2A120A" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')
    o.append(f'<ellipse cx="10" cy="6" rx="30" ry="24" fill="url(#aBody)" stroke="{INK}" stroke-width="6"/>')
    o.append('<path d="M -8 -8 C 0 -16, 16 -17, 26 -10" fill="none" stroke="#E0A080" stroke-width="3.5" stroke-linecap="round" opacity="0.8"/>')
    o.append(f'<ellipse cx="2" cy="0" rx="7" ry="6" fill="#050508" stroke="{INK}" stroke-width="2"/><circle cx="0" cy="-2" r="2.2" fill="#FFFFFF"/>')
    o.append('</g>')
    # antenas acodadas
    o.append('<g id="antant">')
    o.append(aleg([(-6, -12), (-4, -44), (-30, -40), (-48, -22)], AF, 4))
    o.append(aleg([(-2, -14), (6, -48), (-22, -50), (-44, -36)], AL, 4.5))
    o.append('</g>')
    # patas cercanas
    o.append(aleg([(48, 20), (26, 34), (8, 58), (-6, 59)], AL))
    o.append(aleg([(64, 22), (70, 40), (84, 58), (98, 59)], AL))
    o.append(aleg([(80, 20), (106, 34), (126, 58), (142, 59)], AL))
    o.append('</g>')
    return "".join(o)

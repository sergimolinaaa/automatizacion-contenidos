"""Pez arquero (Toxotes jaculatrix) y mosca, en coordenadas locales."""
import math
from lib import INK, f, dbl, pts_d, dash_d, cbez, sample

# ---- pez arquero: cabeza hacia +x, boca en MOUTH ----
MOUTH = (206, -4)      # punta de la boca (de aquí sale el chorro)
EYE = (150, -32)
BODY = ("M 196 -15 C 150 -46, 80 -70, 0 -76 C -70 -80, -122 -62, -160 -30 L -172 -22 L -172 22 "
        "C -132 48, -60 86, 20 84 C 100 82, 160 54, 190 18 L 208 2 L 206 -6 Z")

FISH_DEFS = """
<linearGradient id="{p}body" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7F8F6A"/><stop offset="0.28" stop-color="#C9D2B8"/><stop offset="0.55" stop-color="#F1F4EA"/><stop offset="1" stop-color="#FFFFFF"/></linearGradient>
<linearGradient id="{p}fin" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#3C3F33"/><stop offset="1" stop-color="#8C8A5E"/></linearGradient>
<linearGradient id="{p}tailg" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="#C9C38E"/><stop offset="1" stop-color="#6E6A45"/></linearGradient>
<radialGradient id="{p}iris" cx="0.4" cy="0.35" r="0.7"><stop offset="0" stop-color="#F6E7A8"/><stop offset="0.6" stop-color="#C9A24A"/><stop offset="1" stop-color="#7A5A1E"/></radialGradient>
<clipPath id="{p}clip"><path d="{body}"/></clipPath>
"""


def fish_defs(p="f"):
    return FISH_DEFS.replace("{p}", p).replace("{body}", BODY)


def fish(p="f", ids=True, gill_open=0.0):
    """Devuelve el SVG del pez en coordenadas locales (sin transform)."""
    tid = (lambda n: f' id="{n}"') if ids else (lambda n: "")
    o = []
    # aletas traseras (detrás del cuerpo)
    o.append(f'<path d="M -30 -74 C -40 -100, -58 -124, -86 -130 C -116 -126, -144 -96, -160 -40 Z" fill="url(#{p}fin)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
    o.append(f'<g stroke="#20221A" stroke-width="2.5" opacity="0.6"><path d="M -60 -74 L -72 -116"/><path d="M -84 -70 L -96 -120"/><path d="M -108 -62 L -122 -106"/><path d="M -132 -50 L -144 -76"/></g>')
    o.append(f'<path d="M -16 82 C -36 112, -68 134, -106 132 C -136 122, -154 92, -164 30 Z" fill="url(#{p}fin)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
    o.append(f'<g stroke="#20221A" stroke-width="2.5" opacity="0.6"><path d="M -48 80 L -66 120"/><path d="M -76 72 L -90 122"/><path d="M -104 62 L -118 116"/><path d="M -130 48 L -144 84"/></g>')
    # cola
    o.append(f'<g{tid("tail")}><path d="M -166 -26 C -196 -50, -226 -70, -252 -74 C -240 -26, -240 26, -252 74 C -226 70, -196 50, -166 26 Z" '
             f'fill="url(#{p}tailg)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
             f'<g stroke="#5A5636" stroke-width="2.5" opacity="0.7"><path d="M -172 -14 L -240 -50"/><path d="M -172 0 L -238 -16"/><path d="M -172 0 L -238 18"/><path d="M -172 14 L -240 52"/></g></g>')
    # cuerpo
    o.append(f'<path d="{BODY}" fill="url(#{p}body)"/>')
    o.append(f'<g clip-path="url(#{p}clip)">')
    # escamas
    sc = []
    for row, yy in enumerate(range(-70, 90, 16)):
        off = 8 if row % 2 else 0
        for xx in range(-170 + off, 120, 16):
            sc.append(f"M {xx} {yy} q 8 9 16 0")
    o.append(f'<path d="{" ".join(sc)}" fill="none" stroke="#6F7F62" stroke-width="2" opacity="0.16"/>')
    # bandas negras (5, en cuña desde el lomo)
    for cx, wtop, depth in [(96, 30, 18), (26, 34, 10), (-48, 34, 6), (-112, 30, 0), (-162, 22, 30)]:
        o.append(f'<path d="M {cx - wtop/2} -90 L {cx + wtop/2} -90 L {cx + 7} {depth} L {cx - 3} {depth + 4} Z" fill="#17181A" opacity="0.92"/>')
    # sombra del vientre y línea lateral
    o.append(f'<path d="M -170 40 C -100 70, 0 96, 100 80 L 200 40 L 200 120 L -180 120 Z" fill="#A9B4A0" opacity="0.35"/>')
    o.append(f'<path d="{dash_d(sample(lambda t: cbez((100, -40), (40, -54), (-60, -50), (-170, -8), t)), 7, 6)}" fill="none" stroke="#5E6B55" stroke-width="2.5" opacity="0.5"/>')
    o.append('</g>')
    o.append(f'<path d="{BODY}" fill="none" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
    # brillo del lomo
    o.append('<path d="M 176 -26 C 136 -50, 76 -64, 0 -68 C -60 -71, -108 -58, -146 -32" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" opacity="0.65"/>')
    # opérculo (tapa de las branquias)
    o.append(f'<g{tid("gill")}><path d="M 112 -60 C 88 -24, 86 30, 110 74" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
             f'<path d="M 120 -58 C 100 -24, 98 28, 118 70" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.6"/></g>')
    # boca
    o.append(f'<path d="M 207 -2 L 176 6" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>')
    o.append(f'<path d="M 196 18 C 186 12, 180 10, 172 10" fill="none" stroke="{INK}" stroke-width="3" opacity="0.5"/>')
    # ojo grande
    ex, ey = EYE
    o.append(f'<g{tid("eye")}><circle cx="{ex}" cy="{ey}" r="21" fill="url(#{p}iris)" stroke="{INK}" stroke-width="5"/>'
             f'<circle cx="{ex + 3}" cy="{ey}" r="11" fill="{INK}"/>'
             f'<circle cx="{ex - 4}" cy="{ey - 7}" r="5" fill="#FFFFFF"/><circle cx="{ex + 8}" cy="{ey + 6}" r="2.2" fill="#FFFFFF" opacity="0.8"/></g>')
    # aleta pectoral y pélvica
    o.append(f'<g{tid("pec")}><path d="M 86 22 C 60 8, 34 16, 20 40 C 44 50, 70 44, 86 32 Z" fill="#E8DFA0" fill-opacity="0.85" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
             f'<path d="M 80 26 L 32 38 M 80 28 L 42 46" stroke="#9C9150" stroke-width="2"/></g>')
    o.append(f'<path d="M 54 80 L 26 112 L 14 90 Z" fill="url(#{p}fin)" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    return "".join(o)


# ---- mosca (vista lateral), mirando a la izquierda; pies en y=0 ----
FLY_DEFS = """
<radialGradient id="flyeye" cx="0.35" cy="0.3" r="0.8"><stop offset="0" stop-color="#FF8A6B"/><stop offset="0.6" stop-color="#C0261C"/><stop offset="1" stop-color="#5E0E0A"/></radialGradient>
<linearGradient id="flybody" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6B6E78"/><stop offset="0.5" stop-color="#34363E"/><stop offset="1" stop-color="#15161B"/></linearGradient>
<linearGradient id="flywing" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0.85"/><stop offset="1" stop-color="#BFE3FF" stop-opacity="0.45"/></linearGradient>
"""


def fly(foot_y=None, s=1.0, ids=True):
    """Mosca de lado mirando a la izquierda; pies en y=foot_y(x) (por defecto 0)."""
    fy = foot_y or (lambda x: 0)
    tid = (lambda n: f' id="{n}"') if ids else (lambda n: "")
    o = []
    # patas lejanas: nacen bajo el tórax
    far = [((-8, -30), (-24, -20), -32), ((2, -28), (8, -16), 6), ((12, -30), (36, -22), 42)]
    near = [((-12, -28), (-30, -16), -40), ((-2, -26), (-6, -14), -10), ((10, -28), (28, -16), 34)]
    for (a, k, footx) in far:
        o.append(dbl(pts_d([a, k, (footx, fy(footx))]), 2.6, "#4A4D57", ink_extra=3.5, opacity=0.75))
    # abdomen
    o.append(f'<path d="M 12 -42 C 36 -54, 66 -48, 70 -32 C 70 -18, 44 -14, 14 -22 Z" fill="url(#flybody)" stroke="{INK}" stroke-width="4"/>')
    o.append('<path d="M 30 -48 Q 26 -34 30 -18 M 46 -48 Q 42 -34 46 -18 M 60 -42 Q 57 -32 60 -22" fill="none" stroke="#A9ADB8" stroke-width="2.5" opacity="0.55"/>')
    # tórax (gris con rayas)
    o.append(f'<ellipse cx="0" cy="-38" rx="19" ry="17" fill="url(#flybody)" stroke="{INK}" stroke-width="4"/>')
    o.append('<path d="M -12 -48 Q 0 -54 12 -48 M -14 -42 Q 0 -48 14 -42" fill="none" stroke="#B9BDC6" stroke-width="2.5" opacity="0.75"/>')
    o.append(f'<path d="M -6 -54 l -3 -7 M 4 -55 l 1 -8 M 14 -51 l 4 -6 M 40 -51 l 3 -6 M 58 -46 l 5 -5" stroke="{INK}" stroke-width="2" stroke-linecap="round"/>')
    # alas sobre el abdomen (translúcidas, con venas)
    o.append(f'<path d="M 6 -50 C 34 -70, 80 -70, 94 -54 C 86 -44, 44 -42, 6 -46 Z" fill="url(#flywing)" stroke="{INK}" stroke-width="3"/>')
    o.append('<path d="M 10 -48 C 40 -56, 70 -60, 90 -55 M 26 -47 L 58 -63 M 44 -46 L 78 -60" fill="none" stroke="#5F7184" stroke-width="1.6" opacity="0.7"/>')
    o.append(f'<path d="M 8 -46 C 34 -56, 74 -52, 86 -40 C 76 -32, 40 -34, 8 -42 Z" fill="url(#flywing)" stroke="{INK}" stroke-width="2.5" opacity="0.9"/>')
    # cabeza con ojo compuesto
    o.append(f'<circle cx="-24" cy="-38" r="13" fill="url(#flybody)" stroke="{INK}" stroke-width="4"/>')
    o.append(f'<g{tid("flyeye")}><ellipse cx="-26" cy="-41" rx="11" ry="12" fill="url(#flyeye)" stroke="{INK}" stroke-width="3"/>'
             f'<circle cx="-30" cy="-46" r="3.2" fill="#FFFFFF"/><circle cx="-22" cy="-36" r="1.5" fill="#FFFFFF" opacity="0.7"/></g>')
    o.append(f'<path d="M -34 -50 l -4 -6" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>')
    o.append(f'<path d="M -30 -28 L -35 -18" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/><ellipse cx="-36" cy="-17" rx="4" ry="2.5" fill="#34363E" stroke="{INK}" stroke-width="2"/>')
    # patas cercanas
    for (a, k, footx) in near:
        o.append(dbl(pts_d([a, k, (footx, fy(footx))]), 3.2, "#545864", ink_extra=3.5))
    return "".join(o)

"""Escarabajo bombardero de perfil (mirando a la izquierda), coordenadas locales.
Origen ~ centro del cuerpo; suelo (patas cercanas) en y=+100, patas lejanas en y=+88."""
from lib import *

DEFS = '''
<linearGradient id="bOr" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FF9A55"/><stop offset="0.45" stop-color="#E2561F"/><stop offset="1" stop-color="#8E2A0E"/></linearGradient>
<linearGradient id="bOrLeg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F58A45"/><stop offset="1" stop-color="#C0461A"/></linearGradient>
<linearGradient id="bEl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4E6BB8"/><stop offset="0.35" stop-color="#26386E"/><stop offset="1" stop-color="#0D1230"/></linearGradient>
<linearGradient id="bVen" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#D9581F"/><stop offset="1" stop-color="#7A240C"/></linearGradient>
<radialGradient id="bEye" cx="0.35" cy="0.35" r="0.75"><stop offset="0" stop-color="#3A3A48"/><stop offset="1" stop-color="#050508"/></radialGradient>
<radialGradient id="bShine" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0.55"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient>
<clipPath id="bElClip"><path d="M -76 -14 C -70 -50, -10 -66, 52 -66 C 122 -65, 166 -48, 174 -10 L 168 16 C 100 24, 0 24, -72 16 Z"/></clipPath>
'''
EL = "M -76 -14 C -70 -50, -10 -66, 52 -66 C 122 -65, 166 -48, 174 -10 L 168 16 C 100 24, 0 24, -72 16 Z"

NEAR = "url(#bOrLeg)"
FAR = "#A5401A"


def jleg(coxa, knee, foot, tend, col, wf=14, wt=10, far=False):
    """Pata articulada: coxa -> rodilla (fémur) -> pie (tibia) -> tarso de 5 artejos con uñas."""
    o = []
    cx, cy = coxa
    kx, ky = knee
    fx, fy = foot
    ex, ey = tend
    # fémur engrosado en el centro
    o.append(stroke2(P([coxa, knee]), wf, col, extra=7))
    o.append(stroke2(P([knee, foot]), wt, col, extra=7))
    # espinas de la tibia
    for t in (0.45, 0.7, 0.92):
        px, py = kx + (fx - kx) * t, ky + (fy - ky) * t
        dx, dy = fx - kx, fy - ky
        L = math.hypot(dx, dy)
        nx, ny = -dy / L, dx / L
        if nx < 0:
            nx, ny = -nx, -ny
        o.append(f'<path d="M {px:.1f} {py:.1f} l {nx*9 + dx/L*6:.1f} {ny*9 + dy/L*6:.1f}" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>')
    # tarso: 5 artejos
    segs = []
    for i in range(6):
        t = i / 5
        segs.append((fx + (ex - fx) * t, fy + (ey - fy) * t - math.sin(t * math.pi) * 3))
    o.append(stroke2(P(segs), 6, col, extra=6))
    for (x, y) in segs[1:-1]:
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.2" fill="{col if not col.startswith("url") else "#E0682A"}" stroke="{INK}" stroke-width="2.5"/>')
    # uñas
    d = 1 if ex > fx else -1
    o.append(f'<path d="M {ex:.1f} {ey:.1f} q {d*9:.1f} 0 {d*10:.1f} 7" fill="none" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/>')
    # rodilla
    o.append(f'<circle cx="{kx:.1f}" cy="{ky:.1f}" r="{wt*0.62:.1f}" fill="{col if not col.startswith("url") else "#D9541C"}" stroke="{INK}" stroke-width="3"/>')
    return "".join(o)


def antenna(base, ctrl, end, col, n=11, w=6.5):
    (x0, y0), (cx, cy), (x1, y1) = base, ctrl, end
    pts = []
    for i in range(n + 1):
        t = i / n
        pts.append(((1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t * t * x1, (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t * t * y1))
    d = f"M {x0} {y0} Q {cx} {cy} {x1} {y1}"
    o = [stroke2(d, w, col, extra=6)]
    for i, (x, y) in enumerate(pts[1:]):
        r = 4.6 if i < 2 else 4.0
        o.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{r:.1f}" ry="{r:.1f}" fill="{col if not col.startswith("url") else "#E36A2C"}" stroke="{INK}" stroke-width="2.5"/>')
    return "".join(o)


def legs_far():
    o = ['<g id="legsfar">']
    o.append(jleg((-104, 14), (-150, 42), (-178, 88), (-214, 90), FAR, 10, 7))
    o.append(jleg((-44, 24), (28, 48), (60, 88), (94, 90), FAR, 10, 7))
    o.append(jleg((-4, 26), (110, 44), (190, 88), (226, 90), FAR, 10, 7))
    o.append('</g>')
    return "".join(o)


def legs_near():
    o = ['<g id="legsnear">']
    # coxas (arranque) sobre la cara ventral
    o.append(jleg((-110, 18), (-165, 46), (-205, 100), (-245, 103), NEAR, 12, 8))
    o.append(jleg((-50, 28), (-30, 60), (-5, 100), (32, 103), NEAR, 12, 8))
    o.append(jleg((-10, 30), (72, 56), (140, 100), (180, 103), NEAR, 12, 8))
    for (x, y) in ((-110, 18), (-50, 28), (-10, 30)):
        o.append(f'<ellipse cx="{x}" cy="{y+2}" rx="11" ry="8" fill="#D9541C" stroke="{INK}" stroke-width="4"/>')
    o.append('</g>')
    return "".join(o)


def tip(spray_ready=False):
    """Punta del abdomen (sale por detrás de los élitros). Base en x=156, eje y=0."""
    o = ['<g id="abdtip">']
    # caja simétrica respecto a y=0 para que origin=left gire sobre la base
    o.append('<rect x="156" y="-30" width="62" height="60" fill="none" stroke="none" opacity="0"/>')
    o.append(f'<path d="M 156 -26 C 182 -27, 204 -18, 214 -5 C 218 2, 214 12, 202 18 C 188 24, 168 24, 156 22 Z" fill="url(#bVen)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
    o.append(f'<path d="M 176 -24 C 182 -10, 182 10, 176 22 M 194 -18 C 199 -6, 199 8, 194 18" fill="none" stroke="{INK}" stroke-width="3" opacity="0.55"/>')
    o.append('<path d="M 162 -18 C 180 -20, 196 -14, 206 -6" fill="none" stroke="#FFB27A" stroke-width="4" stroke-linecap="round" opacity="0.8"/>')
    # boquilla
    o.append(f'<ellipse cx="214" cy="-2" rx="6" ry="8" fill="#3A1206" stroke="{INK}" stroke-width="3.5"/>')
    o.append('</g>')
    return "".join(o)


def body():
    o = []
    # abdomen ventral (esternitos)
    o.append(f'<path d="M -72 12 C 0 24, 100 24, 166 14 C 162 30, 120 42, 50 44 C 0 44, -50 38, -70 26 Z" fill="url(#bVen)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
    o.append(f'<path d="M -20 24 L -18 42 M 25 26 L 26 44 M 70 25 L 70 42 M 115 22 L 114 37" stroke="{INK}" stroke-width="3" opacity="0.5"/>')
    o.append(tip())
    # élitros
    o.append('<g id="elytra">')
    o.append(f'<path d="{EL}" fill="url(#bEl)"/>')
    o.append('<g clip-path="url(#bElClip)">')
    # estrías
    for k in range(1, 6):
        o.append(f'<path d="M -70 {12-k*11} C -20 {6-k*12}, 80 {6-k*12}, 172 {8-k*10}" fill="none" stroke="#7F98DA" stroke-width="2" opacity="0.45"/>')
    # manchas amarillas (banda irregular delantera + mancha apical)
    o.append(f'<path d="M -34 -52 C -20 -60, 0 -62, 14 -56 C 22 -46, 12 -38, 18 -26 C 22 -14, 8 -4, -6 -6 C -18 -8, -16 -20, -28 -24 C -40 -30, -42 -44, -34 -52 Z" fill="#F7C531" stroke="#5A3A00" stroke-width="2.5"/>')
    o.append(f'<path d="M 104 -50 C 118 -54, 136 -48, 142 -36 C 146 -24, 136 -12, 122 -12 C 112 -12, 108 -20, 100 -26 C 92 -34, 94 -46, 104 -50 Z" fill="#F7C531" stroke="#5A3A00" stroke-width="2.5"/>')
    o.append('<path d="M -26 -52 C -12 -58, 2 -58, 10 -54" fill="none" stroke="#FFF1B0" stroke-width="4" stroke-linecap="round"/>')
    o.append('<ellipse cx="40" cy="-46" rx="80" ry="14" fill="url(#bShine)"/>')
    o.append('</g>')
    o.append(f'<path d="{EL}" fill="none" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
    o.append('<path d="M -62 -34 C -40 -54, 10 -61, 60 -60 C 110 -59, 148 -46, 162 -30" fill="none" stroke="#B9CBFF" stroke-width="4" stroke-linecap="round" opacity="0.75"/>')
    # sutura
    o.append(f'<path d="M -70 -6 C -10 -2, 90 0, 170 2" fill="none" stroke="{INK}" stroke-width="2.5" opacity="0.35"/>')
    o.append('</g>')
    # pronoto
    o.append(f'<path d="M -152 -30 C -142 -50, -98 -54, -70 -46 C -66 -26, -64 -6, -66 18 C -98 28, -134 26, -152 12 C -158 -4, -158 -20, -152 -34 Z" fill="url(#bOr)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
    o.append('<path d="M -142 -36 C -126 -47, -96 -50, -78 -44" fill="none" stroke="#FFD2A8" stroke-width="4" stroke-linecap="round" opacity="0.85"/>')
    o.append(f'<path d="M -110 -50 C -108 -30, -108 -4, -110 20" fill="none" stroke="{INK}" stroke-width="2.5" opacity="0.3"/>')
    # cabeza
    o.append('<g id="head">')
    # mandíbulas
    o.append(f'<path d="M -214 6 C -236 4, -250 12, -252 26 C -244 20, -234 18, -222 20 Z" fill="#5A1A08" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round"/>')
    o.append(stroke2("M -212 16 L -226 30 L -232 44", 4, "#E36A2C", extra=5))
    o.append(f'<path d="M -150 -40 C -172 -48, -208 -40, -222 -16 C -230 -2, -224 16, -204 22 C -182 28, -162 22, -152 14 Z" fill="url(#bOr)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
    o.append('<path d="M -164 -40 C -184 -42, -204 -34, -214 -20" fill="none" stroke="#FFD2A8" stroke-width="4" stroke-linecap="round" opacity="0.85"/>')
    o.append(f'<ellipse cx="-188" cy="-14" rx="14" ry="13" fill="url(#bEye)" stroke="{INK}" stroke-width="4"/>')
    o.append('<circle cx="-193" cy="-19" r="4.5" fill="#FFFFFF"/><circle cx="-183" cy="-9" r="1.8" fill="#FFFFFF" opacity="0.7"/>')
    o.append('</g>')
    return "".join(o)


def antennae():
    return ('<g id="antennae">' + antenna((-200, -30), (-240, -120), (-300, -158), FAR, w=5.5)
            + antenna((-206, -26), (-262, -96), (-330, -116), NEAR) + '</g>')


def beetle(extra_tip=""):
    """Devuelve el escarabajo completo (sin transformar)."""
    return ('<g id="beetle">' + legs_far() + body() + legs_near() + antennae() + '</g>')


def shadow():
    return '<ellipse cx="-20" cy="104" rx="230" ry="16" fill="#3B2412" opacity="0.28"/>'


def antennae_custom(far, near):
    return '<g id="antennae">' + antenna(*far, FAR, w=5.5) + antenna(*near, NEAR) + '</g>'

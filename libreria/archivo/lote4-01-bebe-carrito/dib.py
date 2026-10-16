"""Piezas de dibujo compartidas: bebé, carrito, manta, mamá, etiquetas, flechas."""
import math
INK = "#0B0B14"
LIME = "#C8FF2E"
CORAL = "#FF5A36"

DEFS = '''
<linearGradient id="skin" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FAD7BC"/><stop offset="1" stop-color="#E9A57F"/></linearGradient>
<radialGradient id="head" cx="0.62" cy="0.38" r="0.75"><stop offset="0" stop-color="#FCDCC3"/><stop offset="0.7" stop-color="#F3BE98"/><stop offset="1" stop-color="#E3A07A"/></radialGradient>
<linearGradient id="shirt" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFE07A"/><stop offset="1" stop-color="#F2B835"/></linearGradient>
<linearGradient id="shorts" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9CC8F2"/><stop offset="1" stop-color="#5B92D0"/></linearGradient>
<linearGradient id="hair" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#B07A48"/><stop offset="1" stop-color="#7A4E2B"/></linearGradient>
<linearGradient id="cartred" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FF7A6B"/><stop offset="0.5" stop-color="#E5392F"/><stop offset="1" stop-color="#B0221C"/></linearGradient>
<linearGradient id="metal" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F4F6FA"/><stop offset="1" stop-color="#A9B2C2"/></linearGradient>
<radialGradient id="wheel" cx="0.4" cy="0.35" r="0.7"><stop offset="0" stop-color="#5A5F6E"/><stop offset="1" stop-color="#1C1E26"/></radialGradient>
<linearGradient id="sweater" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7FCFA2"/><stop offset="1" stop-color="#3E9A6A"/></linearGradient>
<linearGradient id="jeans" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6F8FC4"/><stop offset="1" stop-color="#3E5C93"/></linearGradient>
<linearGradient id="momhair" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6B4430"/><stop offset="1" stop-color="#3B2418"/></linearGradient>
'''


def cap(x1, y1, x2, y2, w, col, k=1.0, ow=None, extra=""):
    """Trazo grueso con contorno de tinta (doble trazo)."""
    ow = ow if ow is not None else w + 12 * k
    d = f"M {x1:.1f} {y1:.1f} L {x2:.1f} {y2:.1f}"
    return (f'<path d="{d}" stroke="{INK}" stroke-width="{ow:.1f}" stroke-linecap="round" fill="none"/>'
            f'<path d="{d}" stroke="{col}" stroke-width="{w:.1f}" stroke-linecap="round" fill="none" {extra}/>')


def capd(d, w, col, k=1.0, ow=None):
    ow = ow if ow is not None else w + 12 * k
    return (f'<path d="{d}" stroke="{INK}" stroke-width="{ow:.1f}" stroke-linecap="round" stroke-linejoin="round" fill="none"/>'
            f'<path d="{d}" stroke="{col}" stroke-width="{w:.1f}" stroke-linecap="round" stroke-linejoin="round" fill="none"/>')


def baby(k=1.0, uid="b", look="fwd", arms="push", hand=(100, -192)):
    """Bebé de pie de perfil 3/4 mirando a la derecha. Origen = punto medio entre los pies en el suelo.
    Manos en (100,-192) si arms='push'. k = factor de grosor de trazo (1 = normal)."""
    s = 6 * k
    o = []
    # sombra
    o.append(f'<ellipse cx="14" cy="0" rx="62" ry="9" fill="{INK}" opacity="0.22"/>')
    # brazo lejano
    if arms == "push":
        hx, hy = hand
        o.append(capd(f"M 2 -232 Q {hx*0.5:.0f} {(-232+hy)/2+10:.0f} {hx+4} {hy-10}", 26, "#E6A27C", k))
        o.append(f'<circle cx="{hx+6}" cy="{hy-9}" r="14" fill="#E6A27C" stroke="{INK}" stroke-width="{s}"/>')
    else:
        o.append(capd("M 2 -232 Q -6 -190 -2 -150", 26, "#E6A27C", k))
    # pierna lejana + zapato
    o.append(cap(-20, -100, -16, -24, 38, "#EDB08C", k))
    o.append(f'<path d="M -34 -6 C -34 -26 -2 -30 18 -20 C 30 -14 32 -2 26 0 L -30 0 C -35 0 -35 -3 -34 -6 Z" fill="#E4E8F0" stroke="{INK}" stroke-width="{s}" stroke-linejoin="round"/>')
    # torso (camiseta a rayas)
    torso = "M -40 -252 C -60 -232 -66 -172 -58 -126 L 60 -126 C 68 -168 64 -228 42 -252 C 20 -266 -18 -266 -40 -252 Z"
    o.append(f'<clipPath id="{uid}tc"><path d="{torso}"/></clipPath>')
    o.append(f'<path d="{torso}" fill="url(#shirt)"/>')
    o.append(f'<g clip-path="url(#{uid}tc)" fill="#3BB3A8">' + "".join(
        f'<rect x="-80" y="{y}" width="160" height="11"/>' for y in range(-238, -126, 26)) + '</g>')
    o.append(f'<path d="{torso}" fill="none" stroke="{INK}" stroke-width="{s}" stroke-linejoin="round"/>')
    o.append(f'<path d="M -30 -248 C -10 -258 20 -258 34 -248" fill="none" stroke="#FFF3C4" stroke-width="{4*k}" stroke-linecap="round" opacity="0.8"/>')
    # pantalón / pañal abombado
    o.append(f'<path d="M -60 -134 C -72 -110 -66 -84 -40 -78 C -10 -72 32 -74 52 -84 C 68 -96 68 -118 61 -134 Z" fill="url(#shorts)" stroke="{INK}" stroke-width="{s}" stroke-linejoin="round"/>')
    o.append(f'<path d="M -50 -126 L 52 -126" stroke="#C9E2FA" stroke-width="{4*k}" stroke-linecap="round" opacity="0.8"/>')
    o.append(f'<path d="M 4 -122 Q 6 -100 2 -84" fill="none" stroke="{INK}" stroke-width="{3*k}" opacity="0.4"/>')
    # pierna cercana + zapato
    o.append(cap(16, -96, 22, -24, 40, "#F3BE98", k))
    o.append(f'<path d="M 12 -50 Q 22 -46 30 -51" fill="none" stroke="#C98763" stroke-width="{3*k}" stroke-linecap="round"/>')
    o.append(f'<path d="M 0 -8 C 0 -30 34 -34 56 -22 C 70 -15 72 -2 64 0 L 4 0 C -1 0 -1 -4 0 -8 Z" fill="#FFFFFF" stroke="{INK}" stroke-width="{s}" stroke-linejoin="round"/>')
    o.append(f'<path d="M 2 -4 L 66 -4" stroke="#FF6B5A" stroke-width="{5*k}"/>')
    o.append(f'<path d="M 20 -24 L 32 -17 M 28 -27 L 40 -20" stroke="{INK}" stroke-width="{2.5*k}" stroke-linecap="round" opacity="0.6"/>')
    # cabeza
    o.append(f'<g id="{uid}head">')
    o.append(f'<ellipse cx="-14" cy="-304" rx="15" ry="19" fill="#F0B48E" stroke="{INK}" stroke-width="{s}"/>')
    o.append(f'<path d="M -16 -312 Q -8 -304 -16 -296" fill="none" stroke="#C98763" stroke-width="{3*k}" stroke-linecap="round"/>')
    o.append(f'<circle cx="16" cy="-310" r="63" fill="url(#head)" stroke="{INK}" stroke-width="{s}"/>')
    # pelo
    o.append(f'<path d="M -42 -330 C -40 -372 0 -384 34 -374 C 54 -368 70 -356 76 -340 C 60 -352 40 -350 30 -344 C 22 -356 0 -356 -6 -346 C -16 -352 -30 -344 -32 -326 C -36 -322 -40 -322 -42 -330 Z" fill="url(#hair)" stroke="{INK}" stroke-width="{5*k}" stroke-linejoin="round"/>')
    o.append(f'<path d="M 22 -372 C 30 -392 52 -390 50 -376 C 48 -368 38 -370 40 -378" fill="none" stroke="{INK}" stroke-width="{9*k}" stroke-linecap="round"/>')
    o.append(f'<path d="M 22 -372 C 30 -392 52 -390 50 -376 C 48 -368 38 -370 40 -378" fill="none" stroke="#9A6A3E" stroke-width="{4*k}" stroke-linecap="round"/>')
    o.append(f'<path d="M -18 -362 C 0 -374 30 -374 44 -366" fill="none" stroke="#D2A06A" stroke-width="{4*k}" stroke-linecap="round" opacity="0.8"/>')
    # cara
    ey = -310 if look == "fwd" else -300
    ex = 0 if look == "fwd" else -2
    o.append(f'<ellipse cx="{36+ex}" cy="-272" rx="15" ry="9" fill="#FF8FA0" opacity="0.45"/>')
    o.append(f'<g id="{uid}eyes">')
    o.append(f'<ellipse cx="{40+ex}" cy="{ey}" rx="7.5" ry="10" fill="{INK}"/><circle cx="{42+ex}" cy="{ey-4}" r="3" fill="#FFFFFF"/>')
    o.append(f'<ellipse cx="{68+ex}" cy="{ey-1}" rx="5.5" ry="9" fill="{INK}"/><circle cx="{69.5+ex}" cy="{ey-5}" r="2.2" fill="#FFFFFF"/>')
    o.append('</g>')
    o.append(f'<path d="M {30+ex} {ey-20} Q {40+ex} {ey-27} {50+ex} {ey-21} M {62+ex} {ey-21} Q {69+ex} {ey-26} {75+ex} {ey-20}" fill="none" stroke="#8A5A35" stroke-width="{4*k}" stroke-linecap="round"/>')
    o.append(f'<path d="M 74 -296 Q 82 -288 74 -282" fill="none" stroke="#C98763" stroke-width="{4*k}" stroke-linecap="round"/>')
    o.append(f'<ellipse cx="60" cy="-264" rx="7.5" ry="9" fill="#9C2F3A" stroke="{INK}" stroke-width="{3*k}"/>')
    o.append(f'<path d="M -10 -352 C 6 -366 30 -366 44 -360" fill="none" stroke="#FFFFFF" stroke-width="{0*k}"/>')
    o.append('</g>')
    # brazo cercano (manga + antebrazo)
    if arms in ("push", "touch"):
        hx, hy = hand
        mx, my = (20 + hx) / 2, (-230 + hy) / 2 + 12
        o.append(capd(f"M 20 -230 Q {mx:.0f} {my:.0f} {hx-2} {hy-2}", 30, "#F3BE98", k))
        sx, sy = 20 + (mx - 20) * 0.55, -230 + (my + 230) * 0.55
        o.append(capd(f"M 20 -230 L {sx:.0f} {sy:.0f}", 36, "#3BB3A8", k))
        o.append(f'<circle cx="{hx}" cy="{hy}" r="16" fill="#F3BE98" stroke="{INK}" stroke-width="{s}"/>')
        o.append(f'<path d="M {hx-8} {hy+10} Q {hx+2} {hy+14} {hx+10} {hy+8}" fill="none" stroke="#C98763" stroke-width="{3*k}" stroke-linecap="round"/>')
    else:
        o.append(capd("M 20 -230 Q 30 -190 26 -150", 30, "#F3BE98", k))
        o.append(capd("M 20 -230 Q 26 -220 28 -206", 36, "#3BB3A8", k))
        o.append(f'<circle cx="26" cy="-146" r="16" fill="#F3BE98" stroke="{INK}" stroke-width="{s}"/>')
    return "".join(o)


def cart(hx, hy, k=1.0, uid="c", items=True):
    """Carrito de juguete visto de lado; (hx,hy) = punto del asa donde agarran las manos. Ruedas apoyan en hy+198."""
    s = 6 * k
    o = []
    gy = hy + 198  # suelo
    bx0, bx1, by0, by1 = hx + 28, hx + 252, hy + 22, hy + 122  # cesta
    wb, wf = hx + 58, hx + 228  # ruedas
    o.append(f'<ellipse cx="{(wb+wf)/2}" cy="{gy}" rx="{(wf-wb)/2+40}" ry="10" fill="{INK}" opacity="0.2"/>')
    # ruedas lejanas
    for wx in (wb + 22, wf + 18):
        o.append(f'<circle cx="{wx}" cy="{gy-22}" r="13" fill="#3A3E4A" stroke="{INK}" stroke-width="{5*k}"/>')
    # patas y bandeja
    o.append(cap(bx0 + 24, by1, wb, gy - 18, 9, "#D5DBE5", k))
    o.append(cap(bx1 - 20, by1, wf, gy - 18, 9, "#D5DBE5", k))
    o.append(cap(wb + 4, gy - 46, wf - 4, gy - 46, 9, "#D5DBE5", k))
    # asa
    o.append(cap(hx - 6, hy - 2, bx0 + 6, by0 + 2, 10, "#D5DBE5", k))
    # cesta
    body = f"M {bx0} {by0} L {bx1} {by0} L {bx1-16} {by1} L {bx0+22} {by1} Z"
    if items:
        # cosas dentro (asoman por arriba)
        o.append(f'<g id="{uid}items">')
        o.append(f'<rect x="{bx0+120}" y="{by0-62}" width="44" height="74" rx="6" fill="#FFFFFF" stroke="{INK}" stroke-width="{5*k}"/>'
                 f'<path d="M {bx0+120} {by0-62} L {bx0+142} {by0-80} L {bx0+164} {by0-62}" fill="#E8EEF7" stroke="{INK}" stroke-width="{5*k}" stroke-linejoin="round"/>'
                 f'<rect x="{bx0+126}" y="{by0-40}" width="32" height="18" rx="4" fill="#4FA3FF"/>')
        o.append(f'<circle cx="{bx0+70}" cy="{by0-14}" r="30" fill="#FF5A5A" stroke="{INK}" stroke-width="{5*k}"/>'
                 f'<path d="M {bx0+70} {by0-44} q 4 -12 12 -16" fill="none" stroke="{INK}" stroke-width="{5*k}" stroke-linecap="round"/>'
                 f'<path d="M {bx0+74} {by0-48} q 16 -10 24 2 q -14 6 -24 -2 Z" fill="#36B37E" stroke="{INK}" stroke-width="{3*k}"/>'
                 f'<ellipse cx="{bx0+60}" cy="{by0-26}" rx="8" ry="5" fill="#FFFFFF" opacity="0.7"/>')
        o.append(f'<path d="M {bx0+178} {by0-4} C {bx0+182} {by0-50} {bx0+214} {by0-66} {bx0+236} {by0-58} C {bx0+214} {by0-48} {bx0+200} {by0-30} {bx0+200} {by0-4} Z" fill="#FFD84A" stroke="{INK}" stroke-width="{5*k}" stroke-linejoin="round"/>')
        o.append('</g>')
    o.append(f'<path d="{body}" fill="url(#cartred)" stroke="{INK}" stroke-width="{s}" stroke-linejoin="round"/>')
    # rejilla
    holes = []
    for r in range(3):
        y = by0 + 22 + r * 28
        t0 = (y - by0) / (by1 - by0)
        xl = bx0 + 22 * t0 + 14
        xr = bx1 - 16 * t0 - 14
        n = 7
        wseg = (xr - xl) / n
        for c in range(n):
            holes.append(f'<rect x="{xl + c*wseg + 4:.1f}" y="{y-9}" width="{wseg-8:.1f}" height="18" rx="5"/>')
    o.append(f'<g fill="#8E1A15" opacity="0.75">{"".join(holes)}</g>')
    o.append(f'<path d="M {bx0-4} {by0} L {bx1+4} {by0}" stroke="{INK}" stroke-width="{18*k}" stroke-linecap="round"/>')
    o.append(f'<path d="M {bx0-4} {by0} L {bx1+4} {by0}" stroke="#FF8C7E" stroke-width="{8*k}" stroke-linecap="round"/>')
    o.append(f'<path d="M {bx0+10} {by0-2} L {bx1-10} {by0-2}" stroke="#FFFFFF" stroke-width="{3*k}" stroke-linecap="round" opacity="0.7"/>')
    # empuñadura
    o.append(cap(hx - 14, hy - 8, hx + 12, hy + 6, 16, "#2F6FD6", k))
    o.append(f'<path d="M {hx-10} {hy-8} L {hx+6} {hy}" stroke="#8FB8FF" stroke-width="{4*k}" stroke-linecap="round"/>')
    # ruedas cercanas
    for wx in (wb, wf):
        o.append(f'<circle cx="{wx}" cy="{gy-18}" r="18" fill="url(#wheel)" stroke="{INK}" stroke-width="{s}"/>'
                 f'<circle cx="{wx}" cy="{gy-18}" r="6" fill="url(#metal)" stroke="{INK}" stroke-width="{3*k}"/>')
    return "".join(o)


def mat(fl, fr, nr, nl, cols=9, rows=3, k=1.0, uid="m"):
    """Manta de cuadros rosa y blanco en perspectiva: esquinas lejana-izq, lejana-der, cercana-der, cercana-izq."""
    def lerp(a, b, t):
        return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)

    def pt(u, v):
        return lerp(lerp(fl, fr, u), lerp(nl, nr, u), v)
    o = []
    th = 7 * k
    o.append(f'<path d="M {nl[0]} {nl[1]} L {nr[0]} {nr[1]} L {nr[0]} {nr[1]+th} L {nl[0]} {nl[1]+th} Z" fill="#C9577D" stroke="{INK}" stroke-width="{5*k}" stroke-linejoin="round"/>')
    o.append(f'<path d="M {fl[0]} {fl[1]} L {fr[0]} {fr[1]} L {nr[0]} {nr[1]} L {nl[0]} {nl[1]} Z" fill="#FFF4F7"/>')
    cells = []
    for i in range(cols):
        for j in range(rows):
            if (i + j) % 2 == 0:
                a, b, c, d = pt(i / cols, j / rows), pt((i + 1) / cols, j / rows), pt((i + 1) / cols, (j + 1) / rows), pt(i / cols, (j + 1) / rows)
                cells.append(f'<path d="M {a[0]:.1f} {a[1]:.1f} L {b[0]:.1f} {b[1]:.1f} L {c[0]:.1f} {c[1]:.1f} L {d[0]:.1f} {d[1]:.1f} Z"/>')
    o.append(f'<g fill="#F49BB9">{"".join(cells)}</g>')
    # costura
    a, b, c, d = pt(0.02, 0.1), pt(0.98, 0.1), pt(0.98, 0.9), pt(0.02, 0.9)
    o.append(f'<path d="M {fl[0]} {fl[1]} L {fr[0]} {fr[1]} L {nr[0]} {nr[1]} L {nl[0]} {nl[1]} Z" fill="none" stroke="{INK}" stroke-width="{5*k}" stroke-linejoin="round"/>')
    return "".join(o)


def mom(k=1.0):
    """Mamá arrodillada mirando a la izquierda con los brazos abiertos. Origen: suelo bajo la rodilla-cadera. Coordenadas locales."""
    s = 5 * k
    o = []
    o.append(f'<ellipse cx="10" cy="0" rx="80" ry="8" fill="{INK}" opacity="0.18"/>')
    # brazo lejano
    o.append(capd("M 40 -172 Q 12 -150 -6 -150 Q -22 -152 -38 -166", 16, "#4E9E70", k))
    o.append(f'<ellipse cx="-44" cy="-170" rx="10" ry="8" fill="#E8B08A" stroke="{INK}" stroke-width="{s}"/>')
    # pierna: espinilla en el suelo + muslo
    o.append(capd("M 62 -9 L -30 -10", 26, "#5374AE", k))
    o.append(f'<path d="M 58 -2 C 60 -16 76 -20 84 -12 C 88 -6 86 0 82 0 Z" fill="#E9E2D6" stroke="{INK}" stroke-width="{s}" stroke-linejoin="round"/>')
    o.append(capd("M -30 -20 L 44 -50", 36, "#5374AE", k))
    # torso
    torso = "M 16 -42 C 6 -84 0 -134 4 -170 C 16 -186 46 -186 56 -170 C 64 -132 66 -84 62 -42 Z"
    o.append(f'<path d="{torso}" fill="url(#sweater)" stroke="{INK}" stroke-width="{s}" stroke-linejoin="round"/>')
    o.append(f'<path d="M 12 -168 C 22 -180 42 -180 50 -170" fill="none" stroke="#B5EBCB" stroke-width="{3*k}" stroke-linecap="round"/>')
    o.append(f'<path d="M 14 -56 L 62 -56" stroke="#2F7A52" stroke-width="{3*k}" opacity="0.6"/>')
    # cuello y cabeza
    o.append(f'<rect x="20" y="-196" width="18" height="24" rx="6" fill="#E8B08A" stroke="{INK}" stroke-width="{s}"/>')
    o.append(f'<g id="momhead">')
    o.append(f'<path d="M 46 -240 C 70 -236 78 -214 70 -196 C 66 -186 58 -190 60 -200 C 64 -214 58 -226 46 -228 Z" fill="url(#momhair)" stroke="{INK}" stroke-width="{s}" stroke-linejoin="round"/>')
    o.append(f'<ellipse cx="26" cy="-220" rx="26" ry="29" fill="#F2C3A0" stroke="{INK}" stroke-width="{s}"/>')
    o.append(f'<path d="M 0 -226 C 0 -252 32 -262 50 -244 C 56 -234 54 -214 48 -204 C 44 -218 40 -228 30 -234 C 22 -230 10 -228 0 -226 Z" fill="url(#momhair)" stroke="{INK}" stroke-width="{s}" stroke-linejoin="round"/>')
    o.append(f'<ellipse cx="12" cy="-218" rx="3" ry="4" fill="{INK}"/>')
    o.append(f'<path d="M 6 -226 Q 12 -229 17 -226" fill="none" stroke="{INK}" stroke-width="{2*k}" stroke-linecap="round"/>')
    o.append(f'<path d="M 4 -206 Q 12 -200 18 -205" fill="none" stroke="{INK}" stroke-width="{2.6*k}" stroke-linecap="round"/>')
    o.append(f'<ellipse cx="20" cy="-208" rx="7" ry="4" fill="#FF8FA0" opacity="0.4"/>')
    o.append(f'<path d="M 1 -218 Q -3 -213 2 -210" fill="none" stroke="#C98763" stroke-width="{2*k}" stroke-linecap="round"/>')
    o.append('</g>')
    # brazo cercano abierto
    o.append(capd("M 22 -168 Q 0 -140 -18 -138 Q -34 -138 -50 -150", 18, "#5DB585", k))
    o.append(f'<ellipse cx="-58" cy="-154" rx="11" ry="9" fill="#F2C3A0" stroke="{INK}" stroke-width="{s}"/>')
    o.append(f'<path d="M -66 -160 L -72 -166 M -68 -154 L -76 -156" stroke="{INK}" stroke-width="{4*k}" stroke-linecap="round"/>')
    return "".join(o)


def arrow(id_, x1, y1, x2, y2, col, w=10, head=28, extra=""):
    ang = math.atan2(y2 - y1, x2 - x1)
    p1 = (x2 - head * math.cos(ang - 0.5), y2 - head * math.sin(ang - 0.5))
    p2 = (x2 - head * math.cos(ang + 0.5), y2 - head * math.sin(ang + 0.5))
    hd = f"M {p1[0]:.1f} {p1[1]:.1f} L {x2} {y2} L {p2[0]:.1f} {p2[1]:.1f}"
    return (f'<g id="{id_}" {extra}><path d="M {x1} {y1} L {x2} {y2}" stroke="{INK}" stroke-width="{w+10}" stroke-linecap="round"/>'
            f'<path d="{hd}" fill="none" stroke="{INK}" stroke-width="{w+10}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="M {x1} {y1} L {x2} {y2}" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>'
            f'<path d="{hd}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/></g>')


def tag(id_, x, y, w, text, lx1=None, ly1=None, lx2=None, ly2=None, bg=INK, fg=LIME, fs=30):
    o = [f'<g id="{id_}">']
    if lx1 is not None:
        o.append(f'<line x1="{lx1}" y1="{ly1}" x2="{lx2}" y2="{ly2}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
                 f'<circle cx="{lx2}" cy="{ly2}" r="9" fill="{LIME}" stroke="{INK}" stroke-width="4"/>')
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="58" rx="12" fill="{bg}" stroke="{INK}" stroke-width="4"/>'
             f'<text x="{x+w/2}" y="{y+40}" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="{fs}" fill="{fg}">{text}</text></g>')
    return "".join(o)

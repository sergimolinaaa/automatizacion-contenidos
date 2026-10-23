"""Tiempo, horas y sueño: cama con cabecero y edredón (persona dentro), mesilla, despertador digital,
luna, persiana de luz del amanecer y reloj de pared con flecha de «retrasar».

Sale de: lote8-08-cambio-hora (archivo/cambio-hora/dib.py), «¿este domingo es el último cambio de hora?».
"""
import math
from ..base import (INK, LIME, CORAL, YEL, f, g, T, MONO, DISP, shade, trazo, sombra, brillo, brillo_arco,
                    lg, rg, registrar_defs, degradado, Pieza, smooth)

registrar_defs(
    lg("cabeceroG", [(0, "#C98B55"), (1, "#8E5A2E")])
    + lg("almohadaG", [(0, "#FFFFFF"), (1, "#D9E2F0")])
    + lg("despG", [(0, "#3A4158"), (1, "#1B1F2C")])
    + rg("despScr", [(0, "#14203A"), (1, "#0A0F1C")], 0.5, 0.4, 0.8)
    + rg("lunaG", [(0, "#FFFBE6"), (0.7, "#FFF0B3"), (1, "#F2D97A")], 0.4, 0.35, 0.8)
    + rg("lunaHalo", [(0, "#FFF6C8"), (1, "#FFF6C8")], 0.5, 0.5, 0.5)
)


def cama(id_, cx, base, w=780, col="#5B7FD6", alto_cabecero=430):
    """Cama de frente con cabecero de madera, almohada y edredón.
    Devuelve (detras, delante): dibuja `detras`, luego la persona (`persona(pose="busto")` con (x, y) en
    .puntos["persona"]) y por último `delante` (edredón que la tapa de cintura para abajo).
    Ids: `{id}_cabecero`, `{id}_almohada`, `{id}_manta` (sway suave origin bottom). .puntos: persona, almohada, borde."""
    x0, x1 = cx - w / 2, cx + w / 2
    top = base - alto_cabecero
    mt = base - alto_cabecero * 0.42  # borde superior del edredón
    o = sombra(cx, base + 6, w * 0.55, 20, 0.25)
    cab = (f'<path d="M {f(x0)} {f(base)} L {f(x0)} {f(top+60)} Q {f(x0)} {f(top)} {f(x0+70)} {f(top)} '
           f'Q {f(cx)} {f(top-50)} {f(x1-70)} {f(top)} Q {f(x1)} {f(top)} {f(x1)} {f(top+60)} L {f(x1)} {f(base)} Z" '
           f'fill="url(#cabeceroG)" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>')
    for k in range(1, 5):
        xx = x0 + w * k / 5
        cab += f'<path d="M {f(xx)} {f(top+40)} L {f(xx)} {f(mt)}" stroke="{shade("#8E5A2E", -0.15)}" stroke-width="6" opacity="0.6"/>'
    cab += brillo(f"M {f(x0+30)} {f(top+70)} Q {f(x0+30)} {f(top+24)} {f(x0+90)} {f(top+20)} Q {f(cx-80)} {f(top-14)} {f(cx)} {f(top-18)}", 7, 0.55)
    alm_y = top + alto_cabecero * 0.32
    alm = (f'<path d="M {f(cx-w*0.3)} {f(alm_y+70)} Q {f(cx-w*0.34)} {f(alm_y-30)} {f(cx-w*0.2)} {f(alm_y-40)} '
           f'Q {f(cx)} {f(alm_y-60)} {f(cx+w*0.2)} {f(alm_y-40)} Q {f(cx+w*0.34)} {f(alm_y-30)} {f(cx+w*0.3)} {f(alm_y+70)} Z" '
           f'fill="url(#almohadaG)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
    alm += brillo(f"M {f(cx-w*0.22)} {f(alm_y-20)} Q {f(cx-w*0.05)} {f(alm_y-38)} {f(cx+w*0.1)} {f(alm_y-30)}", 6, 0.8)
    detras = Pieza(o + g(f"{id_}_cabecero", cab) + g(f"{id_}_almohada", alm),
                   {"persona": (cx, mt + 40), "almohada": (cx, alm_y)}, (x0, top - 50, x1, base))
    # edredón
    oscuro = shade(col, -0.25)
    man = (f'<path d="M {f(x0-30)} {f(base+4)} L {f(x0-24)} {f(mt+30)} Q {f(x0-20)} {f(mt-6)} {f(x0+30)} {f(mt)} '
           f'Q {f(cx-w*0.2)} {f(mt-26)} {f(cx)} {f(mt-10)} Q {f(cx+w*0.22)} {f(mt+6)} {f(x1-30)} {f(mt-4)} '
           f'Q {f(x1+20)} {f(mt-4)} {f(x1+24)} {f(mt+30)} L {f(x1+30)} {f(base+4)} Z" '
           f'fill="{degradado(col, 0.22)}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>')
    # embozo blanco y pliegues
    man += (f'<path d="M {f(x0-22)} {f(mt+46)} Q {f(cx-w*0.2)} {f(mt+18)} {f(cx)} {f(mt+34)} Q {f(cx+w*0.22)} {f(mt+50)} {f(x1+22)} {f(mt+40)}" '
            f'fill="none" stroke="#FFFFFF" stroke-width="22" stroke-linecap="round" opacity="0.92"/>')
    for k, dx in enumerate((-0.28, -0.05, 0.2, 0.36)):
        xx = cx + w * dx
        man += f'<path d="M {f(xx)} {f(mt+90)} Q {f(xx+16)} {f(mt+150)} {f(xx-6)} {f(base-20)}" fill="none" stroke="{oscuro}" stroke-width="6" stroke-linecap="round" opacity="0.55"/>'
    man += brillo(f"M {f(x0)} {f(mt+80)} Q {f(x0+4)} {f(mt+30)} {f(x0+60)} {f(mt+24)}", 7, 0.6)
    delante = Pieza(g(f"{id_}_manta", man), {"borde": (cx, mt)}, (x0 - 30, mt - 30, x1 + 30, base + 4))
    return detras, delante


def mesilla(id_, cx, base, w=200, h=210, col="#C98B55"):
    """Mesilla de noche con cajón. .puntos["tablero"] = centro de la tapa (pon encima el despertador o una lámpara)."""
    x0, top = cx - w / 2, base - h
    o = sombra(cx, base + 4, w * 0.6, 12, 0.22)
    o += f'<rect x="{f(x0)}" y="{f(top)}" width="{f(w)}" height="{f(h)}" rx="12" fill="{degradado(col, 0.22)}" stroke="{INK}" stroke-width="7"/>'
    o += f'<rect x="{f(x0-10)}" y="{f(top-18)}" width="{f(w+20)}" height="26" rx="8" fill="{degradado(shade(col, 0.1), 0.2)}" stroke="{INK}" stroke-width="7"/>'
    o += f'<rect x="{f(x0+18)}" y="{f(top+34)}" width="{f(w-36)}" height="{f(h*0.36)}" rx="8" fill="{shade(col, -0.08)}" stroke="{INK}" stroke-width="5"/>'
    o += f'<circle cx="{f(cx)}" cy="{f(top+34+h*0.18)}" r="9" fill="{YEL}" stroke="{INK}" stroke-width="4"/>'
    o += brillo(f"M {f(x0+12)} {f(top+20)} L {f(x0+12)} {f(base-20)}", 5, 0.5)
    return Pieza(g(id_, o), {"tablero": (cx, top - 18)}, (x0 - 10, top - 18, x0 + w + 10, base))


def despertador(id_, cx, base, w=230, texto="3:00", col_txt=LIME, rot_=0):
    """Despertador digital de mesilla (pantalla con la hora en dígitos). Para cambiar la hora dibuja dos con
    distinto `texto` en el mismo sitio y alterna hide/pop. Sub-id `{id}_hora` (pulse). .puntos pantalla."""
    h = w * 0.55
    x0, top = cx - w / 2, base - h
    o = sombra(cx, base + 3, w * 0.55, 9, 0.25)
    o += f'<rect x="{f(x0)}" y="{f(top)}" width="{f(w)}" height="{f(h)}" rx="{f(h*0.3)}" fill="url(#despG)" stroke="{INK}" stroke-width="7"/>'
    o += f'<rect x="{f(x0+w*0.08)}" y="{f(top+h*0.16)}" width="{f(w*0.84)}" height="{f(h*0.62)}" rx="{f(h*0.14)}" fill="url(#despScr)" stroke="{INK}" stroke-width="4"/>'
    o += g(f"{id_}_hora", T(cx, top + h * 0.47 + h * 0.2, texto, h * 0.5, col_txt, font=DISP,
                             extra=f'style="filter:drop-shadow(0 0 6px {col_txt})"'))
    o += f'<rect x="{f(cx-w*0.18)}" y="{f(top-12)}" width="{f(w*0.36)}" height="16" rx="6" fill="{CORAL}" stroke="{INK}" stroke-width="5"/>'
    o += brillo(f"M {f(x0+h*0.25)} {f(top+8)} L {f(x0+w*0.5)} {f(top+8)}", 4, 0.5)
    body = o if not rot_ else f'<g transform="rotate({f(rot_)} {f(cx)} {f(base)})">{o}</g>'
    return Pieza(g(id_, body), {"pantalla": (cx, top + h * 0.47)}, (x0, top - 12, x0 + w, base))


def luna(id_, cx, cy, r=60):
    """Luna creciente con halo suave (pegatina)."""
    o = f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r*1.9)}" fill="url(#lunaHalo)" opacity="0.18"/>'
    o += (f'<path d="M {f(cx+r*0.35)} {f(cy-r*0.94)} A {f(r)} {f(r)} 0 1 0 {f(cx+r*0.35)} {f(cy+r*0.94)} '
          f'A {f(r*0.8)} {f(r*0.8)} 0 1 1 {f(cx+r*0.35)} {f(cy-r*0.94)} Z" fill="url(#lunaG)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
    o += f'<circle cx="{f(cx-r*0.5)}" cy="{f(cy+r*0.2)}" r="{f(r*0.12)}" fill="#EAD38A"/>'
    return g(id_, o)


def flecha_atras(id_, cx, cy, r=150, col=LIME, a0=40, a1=-80, w=14):
    """Flecha en arco que gira hacia atrás (antihoraria) alrededor de un reloj: «retrasar la hora».
    a0, a1 en grados desde las 12 en sentido horario (a1 < a0). Para draw."""
    pts_ = []
    n = 18
    for i in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * i / n)
        pts_.append((cx + r * math.sin(a), cy - r * math.cos(a)))
    d = "M " + " L ".join(f"{f(x)} {f(y)}" for x, y in pts_)
    o = trazo(d, w, col, 8)
    # punta
    a = math.radians(a1)
    px, py = pts_[-1]
    tx, ty = -math.cos(a), -math.sin(a)  # tangente (sentido antihorario)
    nx, ny = math.sin(a), -math.cos(a)
    L = w * 2.6
    tip = (px + tx * L, py + ty * L)
    b1 = (px + nx * L * 0.6, py + ny * L * 0.6)
    b2 = (px - nx * L * 0.6, py - ny * L * 0.6)
    o += f'<path d="M {f(tip[0])} {f(tip[1])} L {f(b1[0])} {f(b1[1])} L {f(b2[0])} {f(b2[1])} Z" fill="{col}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
    return g(id_, o)

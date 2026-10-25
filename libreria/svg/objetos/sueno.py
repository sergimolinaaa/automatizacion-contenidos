"""Sueño y cuerpo dormido: cama de lado con persona tumbada en pijama, marioneta de madera con cruceta e hilos,
árbol nocturno con rama larga y pierna en corte con su músculo.

Sale de: lote9-01-sacudida-dormir (archivo/sacudida-dormir/dib.py), «¿por qué das un respingo al dormirte?».
Método de movimiento (skill rossark): cada parte va en su propio grupo con el pivote en su articulación
(cabeza en el cuello, brazo en el hombro, antebrazo en el codo, rama en el tronco) para animarla con sway/move rotate.
"""
import math
from ..base import (INK, LIME, CORAL, YEL, f, g, gt, T, DISP, shade, trazo, sombra, brillo, lg, rg, registrar_defs,
                    degradado, Pieza, smooth)
from ..personajes import cabeza, PIELES

registrar_defs(
    lg("slColchon", [(0, "#FFFFFF"), (1, "#D5DEEC")])
    + lg("slMadera", [(0, "#D49A62"), (1, "#8E5A2E")])
    + lg("slMaderaH", [(0, "#E6B27C"), (1, "#A86E3C")], 0, 0, 1, 0)
    + lg("slAlmohada", [(0, "#FFFFFF"), (1, "#C9D6EA")])
    + rg("slTitere", [(0, "#F6D3A4"), (0.7, "#E2AE72"), (1, "#B97F45")], 0.4, 0.35, 0.75)
    + lg("slTronco", [(0, "#7A5236"), (0.5, "#5C3B26"), (1, "#3E2618")], 0, 0, 1, 0)
    + lg("slRama", [(0, "#7A5236"), (1, "#3E2618")])
    + rg("slCopa", [(0, "#2F7A55"), (0.7, "#1F5A40"), (1, "#123A2A")], 0.4, 0.35, 0.75)
    + lg("slMusculo", [(0, "#F0777A"), (1, "#B83440")])
)


def _rayas(col, claro=None, ancho=26, ang=72):
    """Patrón de rayas de pijama (se registra una vez por color). Devuelve 'url(#…)'."""
    claro = claro or shade(col, 0.45)
    pid = f"slRayas{col.lstrip('#').lower()}"
    registrar_defs(f'<pattern id="{pid}" patternUnits="userSpaceOnUse" width="{ancho}" height="{ancho}" '
                   f'patternTransform="rotate({ang})"><rect width="{ancho}" height="{ancho}" fill="{col}"/>'
                   f'<rect width="{f(ancho*0.38)}" height="{ancho}" fill="{claro}"/></pattern>')
    return f"url(#{pid})"


# ----------------------------------------------------------------------------- cama de lado
def cama_lateral(id_, x0, x1, base, col="#5B7FD6", alto=230):
    """Cama vista de lado: cabecero a la izquierda, piecero a la derecha, colchón, almohada y edredón con el bulto
    de un cuerpo tumbado (pecho, cadera, rodillas y pies).
    Devuelve (detras, delante): dibuja `detras`, luego `durmiente()` (cuerpo) y por último `delante`
    (edredón) + el brazo del durmiente. Ids `{id}_cabecero`, `{id}_colchon`, `{id}_almohada`, `{id}_manta`
    (breathe origin bottom). .puntos: cabeza (sitio de la cabeza en la almohada), colchon (y), pecho (x donde empieza el edredón)."""
    w = x1 - x0
    top = base - alto              # parte de arriba del colchón
    o = sombra((x0 + x1) / 2, base + 4, w * 0.52, 18, 0.28)
    # patas
    for x in (x0 + 34, x1 - 40):
        o += f'<rect x="{f(x-14)}" y="{f(base-60)}" width="28" height="62" rx="8" fill="url(#slMadera)" stroke="{INK}" stroke-width="6"/>'
    # larguero
    o += f'<rect x="{f(x0)}" y="{f(base-120)}" width="{f(w)}" height="66" rx="14" fill="url(#slMadera)" stroke="{INK}" stroke-width="7"/>'
    o += brillo(f"M {f(x0+30)} {f(base-106)} L {f(x1-40)} {f(base-106)}", 5, 0.45)
    # cabecero (alto, izquierda) y piecero (bajo, derecha)
    cab = (f'<path d="M {f(x0-10)} {f(base-40)} L {f(x0-10)} {f(top-170)} Q {f(x0-10)} {f(top-215)} {f(x0+28)} {f(top-215)} '
           f'Q {f(x0+62)} {f(top-215)} {f(x0+62)} {f(top-170)} L {f(x0+62)} {f(base-40)} Z" fill="url(#slMaderaH)" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>')
    cab += brillo(f"M {f(x0+8)} {f(top-160)} L {f(x0+8)} {f(base-70)}", 6, 0.5)
    pie = (f'<path d="M {f(x1-56)} {f(base-40)} L {f(x1-56)} {f(top-40)} Q {f(x1-56)} {f(top-80)} {f(x1-22)} {f(top-80)} '
           f'Q {f(x1+12)} {f(top-80)} {f(x1+12)} {f(top-40)} L {f(x1+12)} {f(base-40)} Z" fill="url(#slMaderaH)" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>')
    pie += brillo(f"M {f(x1-40)} {f(top-34)} L {f(x1-40)} {f(base-70)}", 5, 0.45)
    # colchón
    col_ = (f'<rect x="{f(x0+56)}" y="{f(top)}" width="{f(w-108)}" height="{f(alto-112)}" rx="26" fill="url(#slColchon)" stroke="{INK}" stroke-width="7"/>'
            f'<path d="M {f(x0+80)} {f(top+(alto-112)*0.5)} L {f(x1-80)} {f(top+(alto-112)*0.5)}" stroke="#AFC0DA" stroke-width="4" stroke-dasharray="14 12"/>')
    # almohada
    ax0, ax1 = x0 + 70, x0 + 70 + w * 0.24
    alm = (f'<path d="M {f(ax0)} {f(top+6)} Q {f(ax0-14)} {f(top-62)} {f(ax0+40)} {f(top-76)} Q {f((ax0+ax1)/2)} {f(top-96)} {f(ax1-30)} {f(top-74)} '
           f'Q {f(ax1+18)} {f(top-56)} {f(ax1)} {f(top+6)} Z" fill="url(#slAlmohada)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
    alm += brillo(f"M {f(ax0+30)} {f(top-58)} Q {f((ax0+ax1)/2)} {f(top-82)} {f(ax1-40)} {f(top-62)}", 6, 0.8)
    detras = Pieza(o + g(f"{id_}_cabecero", cab) + g(f"{id_}_piecero", pie) + g(f"{id_}_colchon", col_) + g(f"{id_}_almohada", alm),
                   {"cabeza": ((ax0 + ax1) / 2 - 6, top - 70), "colchon": top, "pecho": ax1 + 20},
                   (x0 - 10, top - 215, x1 + 12, base))
    # edredón con el bulto del cuerpo
    px = ax1 + 6                    # empieza en el pecho
    b = [(px - 10, top - 44), (px + w * 0.08, top - 66), (px + w * 0.2, top - 58), (px + w * 0.32, top - 72),
         (px + w * 0.44, top - 52), (px + w * 0.52, top - 60), (x1 - 150, top - 60), (x1 - 112, top - 94), (x1 - 82, top - 90), (x1 - 66, top - 56)]
    d = f"M {f(px-26)} {f(top+40)} L {f(b[0][0]-14)} {f(b[0][1]+16)} " + smooth(b).replace("M", "L", 1)
    d += f" Q {f(x1-48)} {f(top-30)} {f(x1-54)} {f(top+30)} L {f(x1-60)} {f(base-104)} Q {f((px+x1)/2)} {f(base-86)} {f(px-30)} {f(base-104)} Z"
    oscuro = shade(col, -0.28)
    man = f'<path d="{d}" fill="{degradado(col, 0.22)}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'
    # embozo blanco doblado y pliegues
    man += (f'<path d="M {f(px-24)} {f(top+36)} L {f(px-12)} {f(top-38)} Q {f(px+30)} {f(top-60)} {f(px+56)} {f(top-62)} L {f(px+40)} {f(top+30)} Z" '
            f'fill="#F4F7FC" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
    for k, xx in enumerate((px + w * 0.16, px + w * 0.3, px + w * 0.46)):
        man += f'<path d="M {f(xx)} {f(top-30)} Q {f(xx+18)} {f(top+30)} {f(xx-4)} {f(base-112)}" fill="none" stroke="{oscuro}" stroke-width="6" stroke-linecap="round" opacity="0.5"/>'
    man += brillo(f"M {f(px+70)} {f(top-48)} Q {f(px+w*0.14)} {f(top-70)} {f(px+w*0.26)} {f(top-60)}", 7, 0.55)
    delante = Pieza(g(f"{id_}_manta", man), {"borde": (px, top - 40), "pies": (x1 - 100, top - 94)}, (px - 30, top - 100, x1, base - 86))
    return detras, delante


def durmiente(id_, cx, cy, s=1.0, expresiones=("sueno",), piel="media", pelo="corto", pelo_color="castano",
              pijama="#3D6FD9", rot_=-78, accesorios=()):
    """Persona tumbada boca arriba en la cama, vista de lado con la cara hacia nosotros (cabeza en (cx, cy), sobre la almohada
    de `cama_lateral`; el cuerpo sigue hacia la derecha bajo el edredón). Pijama de rayas.
    Devuelve (cuerpo, brazo): dibuja `cuerpo` antes del edredón y `brazo` después (descansa encima).
    Ids: {id} (todo), {id}_torso, {id}_cabeza (pivote en el cuello: sway origin right), {id}_cara_<exp> (una por expresión,
    en el mismo sitio: alterna hide/fade), dentro {id}_<exp>_ojos / _boca…, {id}_brazo (hombro: origin top-left),
    {id}_antebrazo (codo), {id}_mano. .puntos: cabeza, boca, hombro, mano, cima."""
    pa, pb, pc, pl = PIELES.get(piel, PIELES["media"])
    rx, ry = 58 * s, 64 * s
    tela = _rayas(pijama)
    # torso: del cuello hacia la derecha (se esconde bajo el edredón)
    nx, ny = cx + 52 * s, cy + 22 * s          # cuello
    tor = (f'<path d="M {f(nx-6*s)} {f(ny-46*s)} Q {f(nx+60*s)} {f(ny-70*s)} {f(nx+190*s)} {f(ny-58*s)} L {f(nx+200*s)} {f(ny+70*s)} '
           f'Q {f(nx+80*s)} {f(ny+76*s)} {f(nx-6*s)} {f(ny+50*s)} Z" fill="{tela}" stroke="{INK}" stroke-width="{f(7*s)}" stroke-linejoin="round"/>')
    # cuello de la camisa del pijama
    tor += (f'<path d="M {f(nx-4*s)} {f(ny-40*s)} L {f(nx+44*s)} {f(ny-18*s)} L {f(nx+6*s)} {f(ny+6*s)} Z" fill="{shade(pijama, 0.55)}" '
            f'stroke="{INK}" stroke-width="{f(5*s)}" stroke-linejoin="round"/>')
    cuello = (f'<rect x="{f(nx-34*s)}" y="{f(ny-22*s)}" width="{f(44*s)}" height="{f(40*s)}" rx="{f(14*s)}" '
              f'fill="url(#pielL_{piel})" stroke="{INK}" stroke-width="{f(6*s)}"/>')
    caras = ""
    for i, e in enumerate(expresiones):
        caras += g(f"{id_}_cara_{e}", cabeza(f"{id_}_{e}", rx, ry, 0, piel, pelo, pelo_color, e, 0, accesorios))
    head = gt(f"{id_}_cabeza", f"translate({f(cx)} {f(cy)}) rotate({f(rot_)})", caras)
    cuerpo = g(id_, g(f"{id_}_torso", tor + cuello) + head)
    # brazo encima del edredón: hombro → codo → mano
    S = (nx + 70 * s, ny - 30 * s)
    E = (S[0] + 120 * s, S[1] + 26 * s)
    H = (E[0] + 120 * s, E[1] - 18 * s)
    aw = 30 * s

    def manga(p0, p1, w_):
        dx, dy = p1[0] - p0[0], p1[1] - p0[1]
        L = math.hypot(dx, dy)
        a = math.degrees(math.atan2(dy, dx))
        return (f'<g transform="translate({f(p0[0])} {f(p0[1])}) rotate({f(a)})">'
                f'<rect x="{f(-w_*0.5)}" y="{f(-w_)}" width="{f(L+w_)}" height="{f(2*w_)}" rx="{f(w_)}" fill="{tela}" stroke="{INK}" stroke-width="{f(7*s)}"/></g>')
    mano = (f'<ellipse cx="{f(H[0]+14*s)}" cy="{f(H[1]+2*s)}" rx="{f(30*s)}" ry="{f(22*s)}" fill="url(#piel_{piel})" stroke="{INK}" stroke-width="{f(6*s)}"/>'
            f'<path d="M {f(H[0]+18*s)} {f(H[1]-12*s)} q {f(18*s)} {f(4*s)} {f(22*s)} {f(16*s)}" fill="none" stroke="{pl}" stroke-width="{f(3.5*s)}" stroke-linecap="round"/>')
    puno = (f'<rect x="{f(H[0]-16*s)}" y="{f(H[1]-aw*1.05)}" width="{f(20*s)}" height="{f(aw*2.1)}" rx="{f(8*s)}" fill="{shade(pijama, 0.5)}" stroke="{INK}" stroke-width="{f(5*s)}"/>')
    ante = g(f"{id_}_antebrazo", manga(E, H, aw * 0.94) + puno + g(f"{id_}_mano", mano))
    brazo = g(f"{id_}_brazo", manga(S, E, aw) + ante)
    pts_ = {"cabeza": (cx, cy), "boca": (cx + ry * 0.5, cy - 4 * s), "hombro": S, "mano": H, "cima": (cx - ry, cy)}
    return Pieza(cuerpo, pts_, (cx - ry * 1.2, cy - rx * 1.4, nx + 200 * s, ny + 76 * s)), Pieza(brazo, pts_, (S[0] - aw, S[1] - aw, H[0] + 50 * s, H[1] + aw))


# ----------------------------------------------------------------------------- marioneta
def marioneta(id_, cx, cy, s=1.0, col="#E4572E", hilos=True, cruz_y=None):
    """Marioneta de madera colgada de una cruceta. (cx, cy) = centro de la cabeza; alto ≈ 470*s de cabeza a pies.
    Ids (cada parte con su pivote): {id}_cruz (cruceta: sway origin top), {id}_hilos (hide al «soltar»), {id} (la marioneta),
    {id}_cabeza (cuello: origin bottom), {id}_tronco, {id}_brazo_izq / _der (hombro: origin top), {id}_pierna_izq / _der (cadera:
    origin top). .puntos: cruz, manos, pies, suelo (y de los pies)."""
    r = 50 * s
    ty0, ty1 = cy + r + 18 * s, cy + r + 190 * s       # tronco
    sx = 70 * s                                         # semiancho hombros
    madera = "url(#slTitere)"
    o = {}
    # cabeza con cara pintada
    hd = f'<rect x="{f(cx-12*s)}" y="{f(cy+r-6*s)}" width="{f(24*s)}" height="{f(30*s)}" rx="{f(6*s)}" fill="{madera}" stroke="{INK}" stroke-width="{f(6*s)}"/>'
    hd += f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{madera}" stroke="{INK}" stroke-width="{f(7*s)}"/>'
    hd += f'<path d="M {f(cx-r*0.95)} {f(cy-r*0.2)} Q {f(cx-r*0.8)} {f(cy-r*1.25)} {f(cx+r*0.2)} {f(cy-r*1.05)} Q {f(cx+r)} {f(cy-r*0.9)} {f(cx+r*0.95)} {f(cy-r*0.25)} Q {f(cx+r*0.4)} {f(cy-r*0.7)} {f(cx-r*0.95)} {f(cy-r*0.2)} Z" fill="{shade(col, -0.2)}" stroke="{INK}" stroke-width="{f(6*s)}" stroke-linejoin="round"/>'
    for k in (-1, 1):
        hd += f'<circle cx="{f(cx+k*r*0.36)}" cy="{f(cy+r*0.02)}" r="{f(r*0.11)}" fill="{INK}"/>'
        hd += f'<circle cx="{f(cx+k*r*0.55)}" cy="{f(cy+r*0.36)}" r="{f(r*0.16)}" fill="#FF8FA0" opacity="0.7"/>'
    hd += f'<path d="M {f(cx-r*0.3)} {f(cy+r*0.42)} Q {f(cx)} {f(cy+r*0.66)} {f(cx+r*0.3)} {f(cy+r*0.42)}" fill="none" stroke="{INK}" stroke-width="{f(5*s)}" stroke-linecap="round"/>'
    hd += brillo(f"M {f(cx-r*0.55)} {f(cy-r*0.15)} Q {f(cx-r*0.5)} {f(cy-r*0.5)} {f(cx-r*0.2)} {f(cy-r*0.6)}", 5 * s, 0.6)
    o["cabeza"] = hd
    # tronco con camisola
    tr = (f'<path d="M {f(cx-sx)} {f(ty0+10*s)} Q {f(cx-sx)} {f(ty0)} {f(cx-sx+16*s)} {f(ty0)} L {f(cx+sx-16*s)} {f(ty0)} Q {f(cx+sx)} {f(ty0)} {f(cx+sx)} {f(ty0+10*s)} '
          f'L {f(cx+sx*0.78)} {f(ty1)} L {f(cx-sx*0.78)} {f(ty1)} Z" fill="{degradado(col, 0.25)}" stroke="{INK}" stroke-width="{f(7*s)}" stroke-linejoin="round"/>')
    tr += f'<path d="M {f(cx-sx*0.8)} {f(ty1-30*s)} L {f(cx+sx*0.8)} {f(ty1-30*s)}" stroke="{YEL}" stroke-width="{f(12*s)}"/>'
    for yy in (ty0 + 50 * s, ty0 + 95 * s):
        tr += f'<circle cx="{f(cx)}" cy="{f(yy)}" r="{f(8*s)}" fill="{YEL}" stroke="{INK}" stroke-width="{f(4*s)}"/>'
    tr += brillo(f"M {f(cx-sx+18*s)} {f(ty0+20*s)} L {f(cx-sx*0.72)} {f(ty1-46*s)}", 5 * s, 0.5)
    o["tronco"] = tr
    manos, pies = {}, {}
    # brazos colgando de los hilos (algo levantados), distintos a cada lado
    for lado, k, ang_b, ang_t in (("izq", -1, 30, 62), ("der", 1, 22, 74)):
        S = (cx + k * (sx + 4 * s), ty0 + 16 * s)
        L1, L2 = 92 * s, 86 * s
        a1 = math.radians(90 - k * ang_b)   # brazo: hacia abajo y afuera
        E = (S[0] + L1 * math.cos(a1), S[1] + L1 * math.sin(a1))
        a2 = math.radians(90 - k * ang_t)   # antebrazo: levantado por el hilo
        Hh = (E[0] + L2 * math.cos(a2), E[1] + L2 * math.sin(a2))
        br = trazo(f"M {f(S[0])} {f(S[1])} L {f(E[0])} {f(E[1])}", 30 * s, shade(col, -0.05), 7 * s)
        br += trazo(f"M {f(E[0])} {f(E[1])} L {f(Hh[0])} {f(Hh[1])}", 24 * s, "#E2AE72", 7 * s)
        br += f'<circle cx="{f(E[0])}" cy="{f(E[1])}" r="{f(12*s)}" fill="{madera}" stroke="{INK}" stroke-width="{f(5*s)}"/>'
        br += f'<circle cx="{f(Hh[0])}" cy="{f(Hh[1])}" r="{f(20*s)}" fill="{madera}" stroke="{INK}" stroke-width="{f(6*s)}"/>'
        o[f"brazo_{lado}"] = br
        manos[lado] = Hh
    # piernas
    for lado, k, ang in (("izq", -1, 8), ("der", 1, 3)):
        Hp = (cx + k * sx * 0.45, ty1 - 6 * s)
        K = (Hp[0] + k * 14 * s, Hp[1] + 110 * s)
        P_ = (K[0] + k * ang * s, K[1] + 104 * s)
        pi = trazo(f"M {f(Hp[0])} {f(Hp[1])} L {f(K[0])} {f(K[1])}", 32 * s, "#3E5C93", 7 * s)
        pi += trazo(f"M {f(K[0])} {f(K[1])} L {f(P_[0])} {f(P_[1])}", 26 * s, "#E2AE72", 7 * s)
        pi += f'<circle cx="{f(K[0])}" cy="{f(K[1])}" r="{f(13*s)}" fill="{madera}" stroke="{INK}" stroke-width="{f(5*s)}"/>'
        pi += (f'<path d="M {f(P_[0]-18*s)} {f(P_[1]-8*s)} Q {f(P_[0]-20*s)} {f(P_[1]+22*s)} {f(P_[0]+k*44*s)} {f(P_[1]+20*s)} '
               f'Q {f(P_[0]+k*50*s)} {f(P_[1])} {f(P_[0]+18*s)} {f(P_[1]-8*s)} Z" fill="{shade(col, -0.25)}" stroke="{INK}" stroke-width="{f(6*s)}" stroke-linejoin="round"/>')
        o[f"pierna_{lado}"] = pi
        pies[lado] = P_
    cuerpo = (g(f"{id_}_pierna_izq", o["pierna_izq"]) + g(f"{id_}_pierna_der", o["pierna_der"]) + g(f"{id_}_brazo_izq", o["brazo_izq"])
              + g(f"{id_}_tronco", o["tronco"]) + g(f"{id_}_brazo_der", o["brazo_der"]) + g(f"{id_}_cabeza", o["cabeza"]))
    # cruceta e hilos
    cyc = cruz_y if cruz_y is not None else cy - 230 * s
    cw = 200 * s
    cruz = (f'<rect x="{f(cx-cw/2)}" y="{f(cyc-14*s)}" width="{f(cw)}" height="{f(28*s)}" rx="{f(12*s)}" fill="url(#slMadera)" stroke="{INK}" stroke-width="{f(7*s)}"/>'
            f'<rect x="{f(cx-14*s)}" y="{f(cyc-70*s)}" width="{f(28*s)}" height="{f(140*s)}" rx="{f(12*s)}" fill="url(#slMadera)" stroke="{INK}" stroke-width="{f(7*s)}"/>'
            + brillo(f"M {f(cx-cw/2+14*s)} {f(cyc-6*s)} L {f(cx+cw/2-14*s)} {f(cyc-6*s)}", 4 * s, 0.5))
    hil = ""
    if hilos:
        anclas = ((cx - cw / 2 + 12 * s, cyc), (cx + cw / 2 - 12 * s, cyc), (cx, cyc + 60 * s), (cx - 14 * s, cyc - 60 * s), (cx + 14 * s, cyc - 60 * s))
        dest = (manos["izq"], manos["der"], (cx, cy - r), (cx - sx * 0.55, ty1 + 100 * s), (cx + sx * 0.55, ty1 + 100 * s))
        for (a, b_) in zip(anclas, dest):
            hil += f'<path d="M {f(a[0])} {f(a[1])} L {f(b_[0])} {f(b_[1])}" stroke="#F4F1E6" stroke-width="{f(3.5*s)}" opacity="0.95"/>'
    pts_ = {"cruz": (cx, cyc), "manos": manos, "pies": pies, "suelo": max(p[1] for p in pies.values()) + 22 * s}
    return Pieza(g(f"{id_}_cruz", cruz) + g(f"{id_}_hilos", hil) + g(id_, cuerpo), pts_, (cx - cw / 2, cyc - 70 * s, cx + cw / 2, pts_["suelo"]))


# ----------------------------------------------------------------------------- árbol con rama larga
def arbol_rama(id_, x_tronco, base, rama_y, rama_x1, ancho=150, copa=True, noche=True):
    """Árbol grande de perfil con una rama larga horizontal hacia la derecha (para un animal dormido encima).
    Devuelve (fondo, rama): `fondo` = tronco y copa ({id}_copa: sway origin bottom); `rama` = la rama sola en {id}_rama
    (mete dentro lo que esté encima y anímalo con sway origin left: el pivote es el tronco). .puntos: rama (y de la parte de
    arriba de la rama en cada x: función), punta, union."""
    xt = x_tronco
    o = ""
    tron = (f'<path d="M {f(xt-ancho*0.62)} {f(base)} Q {f(xt-ancho*0.42)} {f(base-140)} {f(xt-ancho*0.48)} {f(rama_y-60)} '
            f'L {f(xt-ancho*0.4)} {f(rama_y-460)} L {f(xt+ancho*0.4)} {f(rama_y-460)} L {f(xt+ancho*0.5)} {f(rama_y-40)} '
            f'Q {f(xt+ancho*0.44)} {f(base-140)} {f(xt+ancho*0.66)} {f(base)} Z" fill="url(#slTronco)" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>')
    for k, yy in enumerate((rama_y + 120, rama_y + 300, rama_y - 200)):
        tron += f'<path d="M {f(xt-ancho*0.25)} {f(yy)} q {f(ancho*0.15)} -30 {f(ancho*0.3)} -6" fill="none" stroke="#2C1A10" stroke-width="5" stroke-linecap="round" opacity="0.7"/>'
    tron += brillo(f"M {f(xt-ancho*0.3)} {f(rama_y-380)} L {f(xt-ancho*0.32)} {f(base-60)}", 7, 0.25)
    o += tron
    if copa:
        cop = ""
        for (dx, dy, r) in ((-120, -40, 190), (90, -110, 210), (-40, -250, 200), (210, 10, 150), (-230, 90, 140)):
            cop += f'<circle cx="{f(xt+dx)}" cy="{f(rama_y-330+dy)}" r="{r}" fill="url(#slCopa)" stroke="{INK}" stroke-width="8"/>'
        for (dx, dy, r) in ((-150, -80, 46), (60, -180, 40), (170, -30, 30)):
            cop += f'<circle cx="{f(xt+dx)}" cy="{f(rama_y-330+dy)}" r="{r}" fill="#4FA77A" opacity="0.45"/>'
        o += g(f"{id_}_copa", cop)
    # rama: se estrecha hacia la punta, con hojitas
    t0, t1 = 34, 12   # semigrosor en la unión y en la punta
    x0 = xt + ancho * 0.3
    L = rama_x1 - x0

    def yb(x):  # eje de la rama (algo curvado hacia arriba)
        u = (x - x0) / L
        return rama_y - 16 * math.sin(u * math.pi * 0.9)

    def th(x):
        u = (x - x0) / L
        return t0 + (t1 - t0) * u

    n = 14
    sup = [(x0 + L * i / n, yb(x0 + L * i / n) - th(x0 + L * i / n)) for i in range(n + 1)]
    inf = [(x0 + L * i / n, yb(x0 + L * i / n) + th(x0 + L * i / n)) for i in range(n, -1, -1)]
    d = "M " + " L ".join(f"{f(x)} {f(y)}" for x, y in sup + inf) + " Z"
    ram = f'<path d="{d}" fill="url(#slRama)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
    ram += brillo("M " + " L ".join(f"{f(x)} {f(y+7)}" for x, y in sup[1:-2]), 5, 0.35)
    for (u, a, k) in ((0.86, -30, 1), (0.95, 20, -1), (0.72, -60, 1), (0.99, -10, 1)):
        x = x0 + L * u
        y = yb(x) - th(x)
        ram += (f'<g transform="translate({f(x)} {f(y)}) rotate({a})"><path d="M 0 0 Q 22 -34 0 -70 Q -22 -34 0 0 Z" fill="#3FAE6A" stroke="{INK}" stroke-width="5"/>'
                f'<path d="M 0 -6 L 0 -60" stroke="#1E7A43" stroke-width="3"/></g>')
    rama = Pieza(g(f"{id_}_rama", ram), {"punta": (rama_x1, yb(rama_x1)), "union": (x0, rama_y)}, (x0, rama_y - 120, rama_x1 + 30, rama_y + 40))
    rama.puntos["y"] = lambda x: yb(x) - th(x)
    return Pieza(o, {}, None), rama


# ----------------------------------------------------------------------------- pierna en corte
def pierna_corte(id_, x0, cy, L=760, s=1.0, piel="media", contraido=False, ventana=True):
    """Pierna estirada de lado (muslo, rodilla, espinilla y pie) con una «ventana» en el muslo que deja ver el músculo
    (cuádriceps) en tres haces. contraido=True: músculo corto y gordo. (x0, cy) = cadera; la pierna va hacia la derecha.
    Ids: {id}_muslo, {id}_musculo (dibuja dos piernas o usa musculo_ventana para alternar), {id}_tibia (pivote en la rodilla:
    origin left), {id}_pie. .puntos: rodilla, musculo, pie."""
    pa, pb, pc, pl = PIELES.get(piel, PIELES["media"])
    km = x0 + L * 0.5            # rodilla
    t = 70 * s
    mus = (f'<path d="M {f(x0)} {f(cy-t)} Q {f(x0+L*0.25)} {f(cy-t*1.1)} {f(km)} {f(cy-t*0.72)} L {f(km)} {f(cy+t*0.72)} '
           f'Q {f(x0+L*0.25)} {f(cy+t*1.05)} {f(x0)} {f(cy+t)} Z" fill="url(#piel_{piel})" stroke="{INK}" stroke-width="{f(8*s)}" stroke-linejoin="round"/>')
    if ventana:
        wx0, wx1 = x0 + 50 * s, km - 40 * s
        cid = f"{id_}_vent"
        mus += (f'<clipPath id="{cid}"><rect x="{f(wx0)}" y="{f(cy-t*0.7)}" width="{f(wx1-wx0)}" height="{f(t*1.4)}" rx="{f(26*s)}"/></clipPath>'
                f'<rect x="{f(wx0)}" y="{f(cy-t*0.7)}" width="{f(wx1-wx0)}" height="{f(t*1.4)}" rx="{f(26*s)}" fill="#5A1E28" stroke="{INK}" stroke-width="{f(6*s)}"/>')
    tib = (f'<path d="M {f(km)} {f(cy-t*0.72)} Q {f(km+L*0.22)} {f(cy-t*0.6)} {f(x0+L*0.92)} {f(cy-t*0.4)} L {f(x0+L*0.92)} {f(cy+t*0.42)} '
           f'Q {f(km+L*0.25)} {f(cy+t*0.9)} {f(km)} {f(cy+t*0.72)} Z" fill="url(#piel_{piel})" stroke="{INK}" stroke-width="{f(8*s)}" stroke-linejoin="round"/>')
    tib += f'<ellipse cx="{f(km)}" cy="{f(cy-t*0.15)}" rx="{f(34*s)}" ry="{f(44*s)}" fill="url(#piel_{piel})" stroke="{INK}" stroke-width="{f(6*s)}"/>'
    px = x0 + L * 0.92
    pie = (f'<path d="M {f(px-10*s)} {f(cy-t*0.42)} Q {f(px+30*s)} {f(cy-t*1.9)} {f(px+70*s)} {f(cy-t*1.8)} Q {f(px+92*s)} {f(cy-t*1.5)} {f(px+56*s)} {f(cy-t*0.3)} '
           f'Q {f(px+40*s)} {f(cy+t*0.5)} {f(px-10*s)} {f(cy+t*0.44)} Z" fill="url(#piel_{piel})" stroke="{INK}" stroke-width="{f(7*s)}" stroke-linejoin="round"/>')
    tib += g(f"{id_}_pie", pie)
    tib += brillo(f"M {f(km+40*s)} {f(cy-t*0.45)} Q {f(km+L*0.2)} {f(cy-t*0.5)} {f(x0+L*0.86)} {f(cy-t*0.3)}", 5 * s, 0.5)
    pts_ = {"rodilla": (km, cy), "musculo": ((x0 + km) / 2, cy), "pie": (px + 50 * s, cy - t * 1.4),
            "ventana": (x0 + 50 * s, cy - t * 0.7, km - 40 * s, cy + t * 0.7)}
    return Pieza(g(f"{id_}_muslo", mus) + g(f"{id_}_tibia", tib), pts_, (x0, cy - t * 2, px + 92 * s, cy + t * 1.1))


def musculo_ventana(id_, caja, contraido=False):
    """Haces del músculo dentro de la ventana de `pierna_corte` (caja = .puntos["ventana"]). Dos en el mismo sitio
    (relajado y contraído) + hide/fade para que «se contraiga»."""
    x0, y0, x1, y1 = caja
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    w, h = x1 - x0, y1 - y0
    k = (0.72, 1.18) if contraido else (0.96, 0.82)
    lw, hh = w * k[0], h * k[1] * 0.3
    o = ""
    for dy in (-1, 0, 1):
        yy = cy + dy * h * 0.27
        o += (f'<path d="M {f(cx-lw/2)} {f(yy)} Q {f(cx-lw*0.25)} {f(yy-hh)} {f(cx)} {f(yy-hh)} Q {f(cx+lw*0.25)} {f(yy-hh)} {f(cx+lw/2)} {f(yy)} '
              f'Q {f(cx+lw*0.25)} {f(yy+hh)} {f(cx)} {f(yy+hh)} Q {f(cx-lw*0.25)} {f(yy+hh)} {f(cx-lw/2)} {f(yy)} Z" fill="url(#slMusculo)" stroke="{INK}" stroke-width="5"/>')
        o += f'<path d="M {f(cx-lw*0.35)} {f(yy-hh*0.3)} Q {f(cx)} {f(yy-hh*0.75)} {f(cx+lw*0.35)} {f(yy-hh*0.3)}" fill="none" stroke="#FFB3B8" stroke-width="3.5" stroke-linecap="round" opacity="0.8"/>'
    return g(id_, o)

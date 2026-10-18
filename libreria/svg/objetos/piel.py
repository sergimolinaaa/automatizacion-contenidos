"""Piel, picaduras y bichos: corte de piel en capas (epidermis, dermis, vaso con glóbulos, grasa), habón (bulto rojo),
mosquito realista, mastocito (célula de defensa con gránulos), histamina, sirena de alarma, bacteria, ratón de laboratorio,
mano rascando con uñas, reloj de arena, gorra y delantal (para encima de persona()) y fondo de piscina.

Sale de: lote7-05-picadura (libreria/archivo/picadura/dib.py).
"""
import math
import random
from ..base import (INK, LIME, CORAL, YEL, VERDE, f, g, T, DISP, shade, trazo, sombra, brillo, brillo_arco, lg, rg,
                    registrar_defs, degradado, Pieza, smooth, poly)
from ..personajes import PIELES, EDADES

registrar_defs(
    lg("epiG", [(0, "#FBE0C8"), (1, "#EDB98F")]) + lg("dermG", [(0, "#F9C2B6"), (1, "#E58F86")])
    + lg("vasoG", [(0, "#F0605A"), (0.5, "#C9302C"), (1, "#8E1A1A")])
    + rg("habonR", [(0, "#FFC2B4"), (0.55, "#F47A6C"), (1, "#D9473E")], 0.45, 0.35, 0.75)
    + rg("haloR", [(0, "#FF6F61", 0.55), (1, "#FF6F61", 0)])
    + rg("mastR", [(0, "#D9C8FF"), (0.6, "#9C7BFF"), (1, "#5B3BC9")], 0.4, 0.35, 0.75)
    + rg("histR", [(0, "#FFF3A6"), (1, "#FFC21A")], 0.4, 0.35, 0.7)
    + rg("salivaR", [(0, "#D8FFB0"), (1, "#5FC23A")], 0.4, 0.35, 0.7)
    + lg("mosqG", [(0, "#5C6378"), (1, "#23273A")]) + lg("alaG", [(0, "#F4FBFF"), (1, "#BFDDF5")])
    + rg("bacR", [(0, "#C9F7A8"), (0.6, "#6FD45A"), (1, "#2E9446")], 0.4, 0.35, 0.75)
    + lg("ratonG", [(0, "#FFFFFF"), (1, "#D5DAE6")]) + rg("orejaR", [(0, "#FFC9D6"), (1, "#F48BA6")])
    + lg("sirenaG", [(0, "#FF8A7A"), (0.5, "#F2382A"), (1, "#A8160E")]) + lg("haz", [(0, "#FFE36B", 0.75), (1, "#FFE36B", 0)], 0, 0, 1, 0)
    + lg("arenaG", [(0, "#FFE08A"), (1, "#E5A93A")])
    + lg("aguaPis", [(0, "#5ED3F7"), (1, "#1B86D6")]) + lg("cieloPis", [(0, "#7CC8FF"), (1, "#DDF2FF")])
    + lg("baldosaPis", [(0, "#F7EEDD"), (1, "#E6D6BA")])
)
_N = [0]


def _uid(pre):
    _N[0] += 1
    return f"{pre}{_N[0]}"


# --------------------------------------------------------------- piel en corte
def piel_corte(id_, x0, y0, w, h, vaso=True, pelos=True, grasa=True, seed=4):
    """Corte de piel en capas (≈ w×h): epidermis beige ondulada arriba, dermis rosada con fibras, vaso sanguíneo rojo
    con glóbulos (grupo id_+'_globulos': drift en bucle = sangre que fluye), grasa amarilla abajo y pelos.
    .puntos: sup (centro de la superficie), vaso (centro del vaso), dermis. La superficie está en y0."""
    rnd = random.Random(seed)
    cid = _uid("pcClip")
    eh, vy, vh = h * 0.2, y0 + h * 0.56, h * 0.12
    top = [(x0 + w * i / 24, y0 + 4 * math.sin(i * 1.3)) for i in range(25)]
    bot = [(x0 + w * i / 24, y0 + eh + 6 * math.sin(i * 0.9 + 1)) for i in range(24, -1, -1)]
    o = f'<clipPath id="{cid}"><rect x="{f(x0)}" y="{f(y0 - 12)}" width="{f(w)}" height="{f(h + 12)}" rx="26"/></clipPath>'
    inn = f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" fill="url(#dermG)"/>'
    inn += '<g fill="none" stroke="#F7D3CB" stroke-width="5" opacity="0.7" stroke-linecap="round">' + "".join(
        f'<path d="M {f(x0 + rnd.uniform(0, w))} {f(y0 + eh + rnd.uniform(20, h * 0.3))} q 30 -14 60 0 t 60 0"/>' for _ in range(9)) + "</g>"
    if grasa:
        gy = y0 + h * 0.8
        for j in range(3):
            for i in range(int(w / 70) + 2):
                cx, cy = x0 + i * 70 + (j % 2) * 35, gy + j * 40 + 18
                inn += f'<circle cx="{f(cx)}" cy="{f(cy)}" r="30" fill="#FFE29A" stroke="#E2B357" stroke-width="4"/>'
                inn += f'<circle cx="{f(cx - 9)}" cy="{f(cy - 9)}" r="7" fill="#FFFFFF" opacity="0.6"/>'
    if vaso:
        inn += f'<rect x="{f(x0 - 20)}" y="{f(vy - vh / 2)}" width="{f(w + 40)}" height="{f(vh)}" fill="url(#vasoG)" stroke="{INK}" stroke-width="6"/>'
        inn += brillo(f"M {f(x0)} {f(vy - vh * 0.28)} L {f(x0 + w)} {f(vy - vh * 0.28)}", 5, 0.45)
        gl = ""
        for i in range(int(w / 62) + 2):
            cx = x0 - 30 + i * 62 + rnd.uniform(-8, 8)
            cy = vy + rnd.uniform(-vh * 0.12, vh * 0.12)
            r = vh * 0.3
            gl += (f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(r * 1.25)}" ry="{f(r)}" fill="#FF7468" stroke="#8E1A1A" stroke-width="3"/>'
                   f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(r * 0.55)}" ry="{f(r * 0.4)}" fill="#D23A33"/>')
        inn += g(f"{id_}_globulos" if id_ else None, gl)
    inn += f'<path d="{poly(top + bot, True)}" fill="url(#epiG)"/>'
    inn += f'<path d="{poly(bot)}" fill="none" stroke="#C98763" stroke-width="5"/>'
    inn += f'<path d="{poly([(x, y + eh * 0.45) for x, y in top])}" fill="none" stroke="#E7B48E" stroke-width="3" stroke-dasharray="14 10"/>'
    if pelos:
        for i in range(3):
            px = x0 + w * (0.12 + i * 0.38) + rnd.uniform(-10, 10)
            inn += f'<ellipse cx="{f(px)}" cy="{f(y0 + eh + 50)}" rx="13" ry="26" fill="#E8A79C" stroke="#B5675B" stroke-width="3"/>'
            inn += f'<path d="M {f(px)} {f(y0 + eh + 60)} Q {f(px + 6)} {f(y0)} {f(px + 30)} {f(y0 - 60)}" fill="none" stroke="#3B271B" stroke-width="5" stroke-linecap="round"/>'
    o += f'<g clip-path="url(#{cid})">{inn}</g>'
    o += f'<path d="{poly(top)}" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
    o += brillo(poly([(x, y + 9) for x, y in top[1:-1]]), 4, 0.6)
    o += f'<rect x="{f(x0)}" y="{f(y0 - 4)}" width="{f(w)}" height="{f(h + 4)}" rx="26" fill="none" stroke="{INK}" stroke-width="7"/>'
    return Pieza(g(id_, o), {"sup": (x0 + w / 2, y0), "vaso": (x0 + w / 2, vy), "dermis": (x0 + w / 2, y0 + eh + 40)},
                 (x0, y0 - 12, x0 + w, y0 + h))


def habon(id_, cx, base, w=180, h=70, halo=True, corte=False, herida=False, arriba=False):
    """Habón (bulto rojo de la picadura) apoyado en `base`. corte=True: con capa de epidermis encima y puntitos de
    histamina dentro (para cortes de piel). halo=True: aureola rosada. herida=True añade el arañazo abierto
    (grupo id_+'_herida', anímalo con draw). Para que se hinche: grow origin bottom.
    arriba=True: visto desde arriba (mancha redonda de diámetro w centrada en (cx, base)); para que salga: pop."""
    if arriba:
        r = w / 2
        o = f'<circle cx="{f(cx)}" cy="{f(base)}" r="{f(r * 1.7)}" fill="url(#haloR)"/>' if halo else ""
        o += f'<circle cx="{f(cx + 5)}" cy="{f(base + 7)}" r="{f(r)}" fill="#9E2A22" opacity="0.25"/>'
        o += f'<circle cx="{f(cx)}" cy="{f(base)}" r="{f(r)}" fill="url(#habonR)" stroke="{INK}" stroke-width="5"/>'
        o += f'<circle cx="{f(cx + r * 0.1)}" cy="{f(base + r * 0.05)}" r="{f(max(3, r * 0.08))}" fill="#9E2A22"/>'
        o += brillo_arco(cx, base, r * 0.72, 200, 255, max(4, r * 0.1), 0.75)
        if herida:
            hd = f"M {f(cx - r * 0.75)} {f(base + r * 0.2)} L {f(cx - r * 0.25)} {f(base - r * 0.15)} L {f(cx + r * 0.2)} {f(base + r * 0.1)} L {f(cx + r * 0.8)} {f(base - r * 0.3)}"
            o += g(f"{id_}_herida" if id_ else None, trazo(hd, max(6, r * 0.12), "#B3201A", 5))
        return Pieza(g(id_, o), {"centro": (cx, base)}, (cx - r, base - r, cx + r, base + r))
    d = (f"M {f(cx - w / 2)} {f(base)} C {f(cx - w * 0.32)} {f(base - h * 1.3)}, {f(cx + w * 0.32)} {f(base - h * 1.3)}, "
         f"{f(cx + w / 2)} {f(base)} Z")
    o = ""
    if halo:
        o += f'<ellipse cx="{f(cx)}" cy="{f(base - h * 0.2)}" rx="{f(w * 0.95)}" ry="{f(h * 1.0)}" fill="url(#haloR)"/>'
    if corte:
        o += f'<path d="{d}" fill="#F2A79B" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
        top = f"M {f(cx - w / 2)} {f(base)} C {f(cx - w * 0.32)} {f(base - h * 1.3)}, {f(cx + w * 0.32)} {f(base - h * 1.3)}, {f(cx + w / 2)} {f(base)}"
        o += f'<path d="{top}" fill="none" stroke="#F3C59F" stroke-width="{f(h * 0.22)}"/>'
        o += f'<path d="{top}" fill="none" stroke="{INK}" stroke-width="7"/>'
        rnd = random.Random(3)
        for _ in range(9):
            x = cx + rnd.uniform(-w * 0.28, w * 0.28)
            y = base - rnd.uniform(h * 0.12, h * 0.6)
            o += f'<circle cx="{f(x)}" cy="{f(y)}" r="7" fill="url(#histR)" stroke="{INK}" stroke-width="2.5"/>'
    else:
        o += f'<path d="{d}" fill="url(#habonR)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
        o += f'<circle cx="{f(cx)}" cy="{f(base - h * 0.62)}" r="5" fill="#9E2A22"/>'
        o += brillo(f"M {f(cx - w * 0.22)} {f(base - h * 0.62)} Q {f(cx - w * 0.1)} {f(base - h * 0.88)} {f(cx + w * 0.06)} {f(base - h * 0.9)}", 6, 0.75)
    if herida:
        hd = f"M {f(cx - w * 0.3)} {f(base - h * 0.45)} L {f(cx - w * 0.1)} {f(base - h * 0.62)} L {f(cx + w * 0.1)} {f(base - h * 0.55)} L {f(cx + w * 0.32)} {f(base - h * 0.75)}"
        o += g(f"{id_}_herida" if id_ else None, trazo(hd, 9, "#B3201A", 5))
    return Pieza(g(id_, o), {"cima": (cx, base - h), "centro": (cx, base - h * 0.5)}, (cx - w / 2, base - h, cx + w / 2, base))


def rayitas_picor(id_, cx, cy, r=110, n=8, col=YEL, a0=0):
    """Rayitas de picor alrededor de un punto (para pulse/shake en bucle)."""
    o = ""
    for i in range(n):
        a = math.radians(a0 + i * 360 / n)
        p0 = (cx + r * math.cos(a), cy + r * math.sin(a))
        p1 = (cx + (r + 34) * math.cos(a), cy + (r + 34) * math.sin(a))
        o += trazo(f"M {f(p0[0])} {f(p0[1])} L {f(p1[0])} {f(p1[1])}", 8, col, 6)
    return g(id_, o)


# --------------------------------------------------------------- mosquito
def mosquito(id_, cx, cy, s=1.0, ang=0, espejo=False):
    """Mosquito tigre realista de perfil (cabeza a la izquierda, trompa hacia abajo a la izquierda), ≈ 230×170 a s=1.
    (cx, cy) = tórax. Sub-id id_+'_alas' (pulse o wiggle en bucle = zumbido). .puntos: trompa (punta), cuerpo."""
    k = -1 if espejo else 1
    o = ""
    # patas (detrás)
    for x0, xk, yk, xf in ((-10, -50, -28, -78), (-2, -20, -36, -36), (6, 20, -34, 10), (12, 70, -40, 112), (16, 96, -30, 150), (2, -64, -18, -96)):
        d = f"M {x0} 14 L {xk} {yk + 40} L {xf} 78"
        o += f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'
        o += f'<path d="{d}" fill="none" stroke="#6A7186" stroke-width="3" stroke-linecap="round" stroke-dasharray="10 7" stroke-linejoin="round"/>'
    # abdomen con bandas blancas
    cid = _uid("abClip")
    ab = 'M 14 -6 C 40 -30, 110 -48, 142 -40 C 150 -30, 120 -6, 60 10 C 36 14, 18 8, 14 -6 Z'
    o += f'<clipPath id="{cid}"><path d="{ab}"/></clipPath>'
    o += f'<path d="{ab}" fill="url(#mosqG)"/>'
    o += f'<g clip-path="url(#{cid})" stroke="#F4F6FA" stroke-width="7">' + "".join(
        f'<line x1="{x}" y1="-60" x2="{x - 14}" y2="30"/>' for x in (48, 72, 96, 120)) + "</g>"
    o += f'<path d="{ab}" fill="none" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    # tórax y cabeza
    o += f'<ellipse cx="0" cy="0" rx="28" ry="23" fill="url(#mosqG)" stroke="{INK}" stroke-width="5"/>'
    o += '<path d="M -14 -14 Q 2 -24 18 -12" fill="none" stroke="#F4F6FA" stroke-width="5" stroke-linecap="round"/>'
    o += f'<circle cx="-36" cy="12" r="16" fill="url(#mosqG)" stroke="{INK}" stroke-width="5"/>'
    o += '<circle cx="-40" cy="8" r="10" fill="#3A0F14"/><circle cx="-44" cy="4" r="3.5" fill="#FFFFFF" opacity="0.9"/>'
    # antenas plumosas
    for ax, ay in ((-66, -26), (-58, -36)):
        o += f'<path d="M -42 0 Q {ax + 10} {ay + 14} {ax} {ay}" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
        o += "".join(f'<line x1="{f(-42 + (ax + 42) * t)}" y1="{f(ay * t)}" x2="{f(-42 + (ax + 42) * t - 7)}" y2="{f(ay * t - 6)}" stroke="{INK}" stroke-width="2"/>' for t in (0.4, 0.6, 0.8))
    # trompa
    o += f'<path d="M -48 22 L -104 76" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
    o += '<path d="M -50 21 L -100 70" fill="none" stroke="#8A91A6" stroke-width="2.5" stroke-linecap="round"/>'
    o += f'<path d="M -46 24 L -66 40" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
    # alas
    alas = ""
    for cxa, cya, rot_, op in ((46, -50, -24, 0.55), (34, -58, -40, 0.7)):
        alas += (f'<ellipse cx="{cxa}" cy="{cya}" rx="62" ry="17" transform="rotate({rot_} {cxa} {cya})" fill="url(#alaG)" '
                 f'opacity="{op}" stroke="{INK}" stroke-width="3"/>'
                 f'<path d="M {cxa - 50} {cya + 4} L {cxa + 50} {cya - 2}" transform="rotate({rot_} {cxa} {cya})" stroke="#7FA3C4" stroke-width="2" fill="none"/>')
    o += g(f"{id_}_alas" if id_ else None, alas)
    tr = f"translate({f(cx)} {f(cy)}) rotate({f(ang)}) scale({f(s * k)} {f(s)})"

    def P(x, y):
        a = math.radians(ang)
        x, y = x * s * k, y * s
        return (cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a))
    return Pieza(g(id_, f'<g transform="{tr}">{o}</g>'), {"trompa": P(-104, 76), "cuerpo": P(0, 0), "cabeza": P(-36, 12)},
                 (cx - 110 * s, cy - 90 * s, cx + 150 * s, cy + 80 * s))


def gota_saliva(id_, cx, cy, r=16):
    """Gotita verde de saliva (para pop escalonado)."""
    d = f"M {f(cx)} {f(cy - r * 1.5)} C {f(cx + r * 0.5)} {f(cy - r * 0.6)}, {f(cx + r)} {f(cy - r * 0.2)}, {f(cx + r)} {f(cy + r * 0.3)} A {f(r)} {f(r)} 0 0 1 {f(cx - r)} {f(cy + r * 0.3)} C {f(cx - r)} {f(cy - r * 0.2)}, {f(cx - r * 0.5)} {f(cy - r * 0.6)}, {f(cx)} {f(cy - r * 1.5)} Z"
    return g(id_, f'<path d="{d}" fill="url(#salivaR)" stroke="{INK}" stroke-width="4"/>'
             f'<circle cx="{f(cx - r * 0.35)}" cy="{f(cy)}" r="{f(r * 0.25)}" fill="#FFFFFF" opacity="0.8"/>')


# --------------------------------------------------------------- defensas
def mastocito(id_, cx, cy, r=140, cara=True, seed=2):
    """Mastocito (célula de defensa) morado y blandito con gránulos (grupo id_+'_granulos') y cara de vigilante
    (id_+'_cara', ojos en id_+'_ojos' para blink). .puntos: centro, der (borde derecho)."""
    rnd = random.Random(seed)
    pts_ = [(cx + r * (1 + rnd.uniform(-0.06, 0.06)) * math.cos(a), cy + r * (1 + rnd.uniform(-0.06, 0.06)) * math.sin(a))
            for a in [i * math.pi / 7 for i in range(14)]]
    o = sombra(cx + 10, cy + r + 20, r * 0.8, 14)
    o += f'<path d="{smooth(pts_, True)}" fill="url(#mastR)" stroke="{INK}" stroke-width="7"/>'
    o += f'<ellipse cx="{f(cx - r * 0.25)}" cy="{f(cy + r * 0.3)}" rx="{f(r * 0.32)}" ry="{f(r * 0.26)}" fill="#5B3BC9" opacity="0.55"/>'
    gr = ""
    for _ in range(22):
        a, rr = rnd.uniform(0, 6.28), r * math.sqrt(rnd.uniform(0.05, 0.62))
        x, y = cx + rr * math.cos(a), cy + rr * math.sin(a)
        if cara and abs(x - cx) < r * 0.5 and -r * 0.5 < y - cy < r * 0.2:
            continue
        gr += f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(rnd.uniform(8, 13))}" fill="#3B1E8F" stroke="#2A1468" stroke-width="2"/>'
        gr += f'<circle cx="{f(x - 3)}" cy="{f(y - 3)}" r="3" fill="#B9A3FF"/>'
    o += g(f"{id_}_granulos" if id_ else None, gr)
    o += brillo_arco(cx, cy, r * 0.82, 200, 250, 9, 0.7)
    if cara:
        ey = cy - r * 0.22
        ojos = "".join(f'<ellipse cx="{f(cx + dx)}" cy="{f(ey)}" rx="{f(r * 0.13)}" ry="{f(r * 0.15)}" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/>'
                       f'<circle cx="{f(cx + dx + r * 0.05)}" cy="{f(ey + 2)}" r="{f(r * 0.07)}" fill="{INK}"/>' for dx in (-r * 0.2, r * 0.2))
        c = g(f"{id_}_ojos" if id_ else None, ojos)
        c += "".join(f'<path d="M {f(cx + dx - k * r * 0.12)} {f(ey - r * 0.27)} L {f(cx + dx + k * r * 0.12)} {f(ey - r * 0.19)}" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
                     for dx, k in ((-r * 0.2, 1), (r * 0.2, -1)))
        c += f'<path d="M {f(cx - r * 0.1)} {f(cy + r * 0.06)} L {f(cx + r * 0.1)} {f(cy + r * 0.06)}" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
        o += g(f"{id_}_cara" if id_ else None, c)
    return Pieza(g(id_, o), {"centro": (cx, cy), "der": (cx + r, cy)}, (cx - r, cy - r, cx + r, cy + r))


def histamina(id_, cx, cy, r=90, n=16, seed=6, rmin=8, rmax=14):
    """Nube de puntitos amarillos de histamina (pop o grow + move para que se esparzan)."""
    rnd = random.Random(seed)
    o = ""
    for _ in range(n):
        a, rr = rnd.uniform(0, 6.28), r * math.sqrt(rnd.uniform(0, 1))
        x, y, q = cx + rr * math.cos(a), cy + rr * math.sin(a), rnd.uniform(rmin, rmax)
        o += f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(q)}" fill="url(#histR)" stroke="{INK}" stroke-width="3"/>'
        o += f'<circle cx="{f(x - q * 0.3)}" cy="{f(y - q * 0.3)}" r="{f(q * 0.28)}" fill="#FFFFFF" opacity="0.8"/>'
    return g(id_, o)


def sirena(id_, cx, base, s=1.0):
    """Sirena (luz de alarma) roja con haces de luz (grupo id_+'_luz': spin en bucle). .puntos: luz."""
    ly = base - 78 * s
    haz = (f'<path d="M {f(cx)} {f(ly)} L {f(cx + 230 * s)} {f(ly - 60 * s)} L {f(cx + 230 * s)} {f(ly + 60 * s)} Z" fill="url(#haz)"/>'
           f'<path d="M {f(cx)} {f(ly)} L {f(cx + 230 * s)} {f(ly - 60 * s)} L {f(cx + 230 * s)} {f(ly + 60 * s)} Z" fill="url(#haz)" transform="rotate(180 {f(cx)} {f(ly)})"/>')
    o = g(f"{id_}_luz" if id_ else None, haz)
    o += sombra(cx, base + 4, 90 * s, 12 * s)
    o += f'<rect x="{f(cx - 80 * s)}" y="{f(base - 34 * s)}" width="{f(160 * s)}" height="{f(34 * s)}" rx="{f(10 * s)}" fill="url(#metalG)" stroke="{INK}" stroke-width="6"/>'
    dome = f"M {f(cx - 58 * s)} {f(base - 34 * s)} L {f(cx - 58 * s)} {f(base - 90 * s)} A {f(58 * s)} {f(58 * s)} 0 0 1 {f(cx + 58 * s)} {f(base - 90 * s)} L {f(cx + 58 * s)} {f(base - 34 * s)} Z"
    o += f'<path d="{dome}" fill="url(#sirenaG)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
    o += f'<circle cx="{f(cx)}" cy="{f(ly)}" r="{f(22 * s)}" fill="#FFF2A8" opacity="0.9"/>'
    o += brillo(f"M {f(cx - 38 * s)} {f(base - 50 * s)} L {f(cx - 38 * s)} {f(base - 100 * s)} Q {f(cx - 30 * s)} {f(base - 132 * s)} {f(cx - 6 * s)} {f(base - 140 * s)}", 8, 0.7)
    o += f'<rect x="{f(cx - 20 * s)}" y="{f(base - 160 * s)}" width="{f(40 * s)}" height="{f(14 * s)}" rx="{f(6 * s)}" fill="url(#metalG)" stroke="{INK}" stroke-width="5"/>'
    return Pieza(g(id_, o), {"luz": (cx, ly)}, (cx - 80 * s, base - 160 * s, cx + 80 * s, base))


def bacteria(id_, cx, cy, s=1.0, ang=0, cara=True):
    """Bacteria verde (bacilo) con cilios y cara de pilla, ≈ 120×60 a s=1."""
    o = ""
    for i in range(12):
        a = i * math.pi / 6
        x, y = 50 * math.cos(a), 26 * math.sin(a)
        x2, y2 = 64 * math.cos(a), 38 * math.sin(a)
        o += f'<path d="M {f(x)} {f(y)} Q {f((x + x2) / 2 + 6)} {f((y + y2) / 2 - 6)} {f(x2)} {f(y2)}" fill="none" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/>'
    o += f'<rect x="-52" y="-26" width="104" height="52" rx="26" fill="url(#bacR)" stroke="{INK}" stroke-width="5"/>'
    o += '<circle cx="-24" cy="10" r="5" fill="#2E9446" opacity="0.6"/><circle cx="28" cy="12" r="4" fill="#2E9446" opacity="0.6"/>'
    o += brillo("M -36 -14 L 24 -14", 5, 0.7)
    if cara:
        o += ''.join(f'<circle cx="{dx}" cy="-2" r="5" fill="{INK}"/>' for dx in (-9, 9))
        o += f'<path d="M -16 -12 L -4 -8 M 16 -12 L 4 -8" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/>'
        o += f'<path d="M -8 9 Q 0 14 8 9" fill="none" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/>'
    return g(id_, f'<g transform="translate({f(cx)} {f(cy)}) rotate({f(ang)}) scale({f(s)})">{o}</g>')


def raton_lab(id_, cx, base, s=1.0, espejo=False):
    """Ratón blanco de laboratorio sentado de perfil (mira a la derecha), orejas rosas, ≈ 300×190 a s=1.
    Sub-id id_+'_pata' (pata delantera rascándose la oreja: wiggle en bucle), id_+'_ojo'. .puntos: cabeza."""
    k = -1 if espejo else 1
    o = sombra(0, 0, 120, 12)
    o += trazo("M -70 -14 C -120 -6, -150 -6, -168 -36 S -150 -80, -128 -66", 9, "#F7A7B8", 6)
    o += '<path d="M -88 -64 C -96 -120, -10 -140, 40 -110 C 76 -88, 80 -40, 60 -10 L -66 -6 C -86 -14, -90 -40, -88 -64 Z" fill="url(#ratonG)" stroke="#0B0B14" stroke-width="7" stroke-linejoin="round"/>'
    o += brillo("M -70 -80 C -50 -112, 0 -122, 30 -110", 6, 0.9)
    o += '<ellipse cx="-24" cy="-6" rx="30" ry="9" fill="#F7A7B8" stroke="#0B0B14" stroke-width="5"/>'
    # orejas
    o += '<circle cx="52" cy="-158" r="30" fill="#E9ECF3" stroke="#0B0B14" stroke-width="6"/><circle cx="52" cy="-158" r="18" fill="url(#orejaR)"/>'
    # cabeza
    o += '<path d="M 20 -120 C 30 -160, 90 -160, 112 -128 C 124 -116, 140 -106, 146 -96 C 140 -86, 110 -78, 80 -80 C 50 -80, 22 -94, 20 -120 Z" fill="url(#ratonG)" stroke="#0B0B14" stroke-width="7" stroke-linejoin="round"/>'
    o += '<circle cx="18" cy="-150" r="32" fill="#F4F6FA" stroke="#0B0B14" stroke-width="6"/><circle cx="18" cy="-150" r="20" fill="url(#orejaR)"/>'
    o += '<circle cx="146" cy="-96" r="9" fill="#FF8FAA" stroke="#0B0B14" stroke-width="4"/>'
    o += g(f"{id_}_ojo" if id_ else None, '<circle cx="96" cy="-118" r="9" fill="#9E1F3A"/><circle cx="93" cy="-121" r="3.2" fill="#FFFFFF"/>')
    o += '<g stroke="#0B0B14" stroke-width="2.5" stroke-linecap="round">' + "".join(
        f'<line x1="138" y1="-92" x2="{x}" y2="{y}"/>' for x, y in ((182, -110), (186, -92), (180, -76))) + "</g>"
    pata = trazo("M 50 -40 Q 74 -64 84 -96", 12, "#F7A7B8", 6) + '<circle cx="86" cy="-100" r="10" fill="#F7A7B8" stroke="#0B0B14" stroke-width="4"/>'
    o += g(f"{id_}_pata" if id_ else None, pata)
    return Pieza(g(id_, f'<g transform="translate({f(cx)} {f(base)}) scale({f(s * k)} {f(s)})">{o}</g>'),
                 {"cabeza": (cx + k * 80 * s, base - 120 * s)}, (cx - 180 * s, base - 190 * s, cx + 190 * s, base))


# --------------------------------------------------------------- rascar
def mano_rasca(id_, cx, cy, s=1.0, piel="media", manga=None, espejo=False):
    """Mano de perfil con los dedos curvados hacia abajo y uñas a la vista (rascando), ≈ 260×200 a s=1 sin el
    antebrazo, que sale hacia arriba a la derecha. (cx, cy) = punto bajo las uñas. Sub-id id_+'_unas'.
    Para rascar: shake en bucle (amount 2-3). .puntos: unas."""
    pa, pb, pc, pl = PIELES.get(piel, PIELES["media"])
    k = -1 if espejo else 1
    o = trazo("M 70 -120 L 210 -270", 92, f"url(#pielL_{piel if piel in PIELES else 'media'})", 8)
    if manga:
        o += trazo("M 170 -226 L 240 -302", 112, manga, 8, cap="butt")
    o += f'<path d="M -70 -110 C -70 -160, 40 -170, 96 -150 C 130 -136, 130 -90, 100 -70 C 60 -50, -30 -50, -70 -70 Z" fill="url(#piel_{piel if piel in PIELES else "media"})" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
    unas = ""
    for i, x in enumerate((-70, -40, -10, 20)):
        sh = shade(pb, -0.06 * (3 - i))
        d = f"M {x + 10} -96 C {x - 14} -80, {x - 18} -40, {x - 2} -14"
        o += trazo(d, 30, sh, 7)
        unas += (f'<path d="M {x - 16} -24 Q {x - 12} -2 {x + 2} -2 Q {x + 10} -6 {x + 8} -16 Z" fill="#FFE9E4" stroke="{INK}" stroke-width="3.5"/>')
    o += g(f"{id_}_unas" if id_ else None, unas)
    o += trazo("M 70 -80 Q 60 -40 34 -36", 30, pb, 7)
    o += brillo("M -50 -132 C 0 -150, 50 -150, 90 -138", 6, 0.6)
    return Pieza(g(id_, f'<g transform="translate({f(cx)} {f(cy)}) scale({f(s * k)} {f(s)})">{o}</g>'),
                 {"unas": (cx - 30 * s * k, cy)}, (cx - 90 * s, cy - 300 * s, cx + 250 * s, cy))


def reloj_arena(id_, cx, cy, h=170):
    """Reloj de arena de madera. Sub-ids id_+'_arriba' (arena de arriba), id_+'_abajo' (montoncito: grow origin bottom),
    id_+'_chorro' (hilo de arena: pulse)."""
    w = h * 0.62
    t, b = cy - h / 2, cy + h / 2
    o = sombra(cx, b + 6, w * 0.6, 8)
    o += f'<path d="M {f(cx - w * 0.38)} {f(t + 14)} C {f(cx - w * 0.38)} {f(cy - h * 0.12)}, {f(cx - 8)} {f(cy - 10)}, {f(cx - 6)} {f(cy)} C {f(cx - 8)} {f(cy + 10)}, {f(cx - w * 0.38)} {f(cy + h * 0.12)}, {f(cx - w * 0.38)} {f(b - 14)} L {f(cx + w * 0.38)} {f(b - 14)} C {f(cx + w * 0.38)} {f(cy + h * 0.12)}, {f(cx + 8)} {f(cy + 10)}, {f(cx + 6)} {f(cy)} C {f(cx + 8)} {f(cy - 10)}, {f(cx + w * 0.38)} {f(cy - h * 0.12)}, {f(cx + w * 0.38)} {f(t + 14)} Z" fill="#E8F6FF" fill-opacity="0.75" stroke="{INK}" stroke-width="5"/>'
    o += g(f"{id_}_arriba" if id_ else None, f'<path d="M {f(cx - w * 0.28)} {f(cy - h * 0.2)} Q {f(cx)} {f(cy - h * 0.26)} {f(cx + w * 0.28)} {f(cy - h * 0.2)} L {f(cx)} {f(cy - 6)} Z" fill="url(#arenaG)" stroke="#B5832B" stroke-width="2"/>')
    o += g(f"{id_}_chorro" if id_ else None, f'<line x1="{f(cx)}" y1="{f(cy - 4)}" x2="{f(cx)}" y2="{f(b - 30)}" stroke="#E5A93A" stroke-width="4"/>')
    o += g(f"{id_}_abajo" if id_ else None, f'<path d="M {f(cx - w * 0.34)} {f(b - 15)} Q {f(cx)} {f(b - 15 - h * 0.22)} {f(cx + w * 0.34)} {f(b - 15)} Z" fill="url(#arenaG)" stroke="#B5832B" stroke-width="2"/>')
    o += brillo(f"M {f(cx - w * 0.26)} {f(t + 26)} Q {f(cx - w * 0.24)} {f(cy - h * 0.16)} {f(cx - 14)} {f(cy - 16)}", 4, 0.8)
    for y in (t, b - 14):
        o += f'<rect x="{f(cx - w / 2)}" y="{f(y)}" width="{f(w)}" height="14" rx="6" fill="url(#maderaG)" stroke="{INK}" stroke-width="5"/>'
    for x in (cx - w * 0.44, cx + w * 0.44):
        o += f'<rect x="{f(x - 5)}" y="{f(t + 12)}" width="10" height="{f(h - 26)}" rx="4" fill="url(#maderaG)" stroke="{INK}" stroke-width="3.5"/>'
    return g(id_, o)


# --------------------------------------------------------------- complementos para persona()
def gorra(id_, cx, cy, r, col=CORAL, visera=None):
    """Gorra de béisbol de frente para poner encima de persona(): (cx, cy) = persona.puntos['cabeza'], r = radio
    horizontal de la cabeza ya escalado (EDADES[edad]['rx'] * escala). Ponla en el mismo grupo que la persona."""
    visera = visera or shade(col, -0.18)
    yb = cy - r * 0.5
    o = f'<path d="M {f(cx - r * 1.04)} {f(yb)} C {f(cx - r * 1.05)} {f(cy - r * 1.55)}, {f(cx + r * 1.05)} {f(cy - r * 1.55)}, {f(cx + r * 1.04)} {f(yb)} Q {f(cx)} {f(yb - r * 0.12)} {f(cx - r * 1.04)} {f(yb)} Z" fill="{degradado(col, 0.22)}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
    o += f'<path d="M {f(cx)} {f(cy - r * 1.3)} L {f(cx)} {f(yb - r * 0.08)}" stroke="{shade(col, -0.3)}" stroke-width="4"/>'
    o += f'<circle cx="{f(cx)}" cy="{f(cy - r * 1.3)}" r="{f(r * 0.1)}" fill="{shade(col, -0.2)}" stroke="{INK}" stroke-width="3.5"/>'
    o += f'<path d="M {f(cx - r * 1.1)} {f(yb + 2)} Q {f(cx)} {f(yb - r * 0.2)} {f(cx + r * 1.1)} {f(yb + 2)} Q {f(cx + r * 0.9)} {f(yb + r * 0.3)} {f(cx)} {f(yb + r * 0.3)} Q {f(cx - r * 0.9)} {f(yb + r * 0.3)} {f(cx - r * 1.1)} {f(yb + 2)} Z" fill="{degradado(visera, 0.15)}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
    o += brillo(f"M {f(cx - r * 0.6)} {f(cy - r * 0.95)} Q {f(cx - r * 0.3)} {f(cy - r * 1.22)} {f(cx)} {f(cy - r * 1.25)}", 5, 0.6)
    return g(id_, o)


def delantal(id_, x, y, escala=1.0, edad="mayor", col="#FF7EB6", busto=False):
    """Delantal de cocina (peto con lunares, bolsillo y tirante al cuello) para dibujar encima de persona() con los mismos
    x, y, escala, edad (y busto=True si la persona tiene pose='busto'). Ponlo en el mismo grupo que la persona."""
    e = EDADES.get(edad, EDADES["mayor"])
    sy, cy, nw, cw = e["sy"], e["cy"], e["nw"], e["cw"]
    cut = sy + (cy - sy) * 0.62
    oy = -cut if busto else 0

    def P(lx, ly):
        return f"{f(x + lx * escala)} {f(y + (ly + oy) * escala)}"
    bot = (cut - 6) if busto else cy + 120
    o = f'<path d="M {P(-nw * 1.3, sy - 10)} Q {P(0, sy - 40)} {P(nw * 1.3, sy - 10)}" fill="none" stroke="{INK}" stroke-width="{f(11 * escala)}"/>'
    o += f'<path d="M {P(-nw * 1.3, sy - 10)} Q {P(0, sy - 40)} {P(nw * 1.3, sy - 10)}" fill="none" stroke="#FFFFFF" stroke-width="{f(5 * escala)}"/>'
    d = (f"M {P(-nw * 1.9, sy + 22)} L {P(nw * 1.9, sy + 22)} L {P(nw * 2.1, cy - 8)} L {P(cw * 1.25, cy - 8)} L {P(cw * 1.35, bot)} "
         f"L {P(-cw * 1.35, bot)} L {P(-cw * 1.25, cy - 8)} L {P(-nw * 2.1, cy - 8)} Z")
    cid = _uid("delClip")
    o += f'<clipPath id="{cid}"><path d="{d}"/></clipPath>'
    o += f'<path d="{d}" fill="{degradado(col, 0.15)}"/>'
    rnd = random.Random(5)
    o += f'<g clip-path="url(#{cid})" fill="#FFFFFF" opacity="0.8">' + "".join(
        f'<circle cx="{f(x + rnd.uniform(-cw * 1.3, cw * 1.3) * escala)}" cy="{f(y + (rnd.uniform(sy + 20, bot) + oy) * escala)}" r="{f(5 * escala)}"/>' for _ in range(26)) + "</g>"
    o += f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{f(6 * escala)}" stroke-linejoin="round"/>'
    o += f'<rect x="{f(x - nw * 1.2 * escala)}" y="{f(y + (sy + 50 + oy) * escala)}" width="{f(nw * 2.4 * escala)}" height="{f(36 * escala)}" rx="{f(6 * escala)}" fill="{shade(col, -0.12)}" stroke="{INK}" stroke-width="{f(4 * escala)}"/>'
    return g(id_, o)


# --------------------------------------------------------------- fondo
def piscina(W=1080, H=1920, agua_y0=None, agua_y1=None, seed=3):
    """Fondo de piscina de verano (sin ids): cielo, setos, sombrilla, agua con reflejos, escalerilla, flotador y suelo
    de baldosas delante. Por defecto el agua va de 0,36H a 0,6H y el suelo empieza en 0,6H."""
    rnd = random.Random(seed)
    a0, a1 = agua_y0 or H * 0.36, agua_y1 or H * 0.6
    o = f'<rect width="{W}" height="{f(a0)}" fill="url(#cieloPis)"/>'
    o += f'<circle cx="{f(W * 0.82)}" cy="{f(a0 * 0.3)}" r="{f(W * 0.09)}" fill="#FFE36B" stroke="{INK}" stroke-width="6"/>'
    o += f'<circle cx="{f(W * 0.82)}" cy="{f(a0 * 0.3)}" r="{f(W * 0.16)}" fill="#FFE36B" opacity="0.25"/>'
    hy = a0 - 90
    o += f'<rect x="0" y="{f(hy)}" width="{W}" height="90" fill="#F3E8D3"/>'
    for i in range(9):
        cx = i * W / 8 + rnd.uniform(-20, 20)
        o += f'<circle cx="{f(cx)}" cy="{f(hy)}" r="{f(rnd.uniform(70, 95))}" fill="{degradado("#4FBF6A", 0.2)}" stroke="{INK}" stroke-width="5"/>'
    o += f'<rect x="0" y="{f(hy)}" width="{W}" height="90" fill="url(#baldosaPis)"/>'
    o += f'<path d="M 0 {f(hy)} L {W} {f(hy)}" stroke="{INK}" stroke-width="5"/>'
    # sombrilla al fondo
    sx, st = W * 0.14, hy - 150
    o += f'<rect x="{f(sx - 6)}" y="{f(st)}" width="12" height="{f(hy + 60 - st)}" fill="#E8EBF2" stroke="{INK}" stroke-width="4"/>'
    for i in range(6):
        a_0, a_1 = math.pi + i * math.pi / 6, math.pi + (i + 1) * math.pi / 6
        p0 = (sx + 170 * math.cos(a_0), st + 50 + 60 * math.sin(a_0))
        p1 = (sx + 170 * math.cos(a_1), st + 50 + 60 * math.sin(a_1))
        o += f'<path d="M {f(sx)} {f(st)} L {f(p0[0])} {f(p0[1])} L {f(p1[0])} {f(p1[1])} Z" fill="{CORAL if i % 2 == 0 else "#FFFFFF"}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
    # borde del vaso y agua
    o += f'<rect x="0" y="{f(a0 - 22)}" width="{W}" height="22" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/>'
    o += f'<rect x="0" y="{f(a0)}" width="{W}" height="{f(a1 - a0)}" fill="url(#aguaPis)"/>'
    o += '<g fill="none" stroke="#FFFFFF" stroke-width="6" opacity="0.4" stroke-linecap="round">' + "".join(
        f'<path d="M {f(x)} {f(y)} q 30 -12 60 0 t 60 0"/>' for x, y in [(rnd.uniform(-40, W), rnd.uniform(a0 + 30, a1 - 30)) for _ in range(16)]) + "</g>"
    o += f'<g stroke="#2E6FB8" stroke-width="3" opacity="0.5">' + "".join(
        f'<line x1="0" y1="{f(a0 + 4 + j * 26)}" x2="{W}" y2="{f(a0 + 4 + j * 26)}"/>' for j in range(1)) + "</g>"
    # flotador
    fx, fy = W * 0.8, a0 + (a1 - a0) * 0.42
    o += f'<ellipse cx="{f(fx)}" cy="{f(fy)}" rx="96" ry="40" fill="#FFFFFF" stroke="{INK}" stroke-width="6"/>'
    for a in (0, 90, 180, 270):
        o += f'<path d="M {f(fx + 96 * math.cos(math.radians(a)))} {f(fy + 40 * math.sin(math.radians(a)))} A 96 40 0 0 1 {f(fx + 96 * math.cos(math.radians(a + 45)))} {f(fy + 40 * math.sin(math.radians(a + 45)))}" fill="none" stroke="{CORAL}" stroke-width="22"/>'
    o += f'<ellipse cx="{f(fx)}" cy="{f(fy)}" rx="44" ry="15" fill="#2E8FDA" stroke="{INK}" stroke-width="5"/>'
    # escalerilla
    lx = W * 0.6
    for dx in (0, 90):
        o += f'<path d="M {f(lx + dx)} {f(a1 - 10)} L {f(lx + dx)} {f(a0 - 70)} Q {f(lx + dx)} {f(a0 - 120)} {f(lx + dx + 40)} {f(a0 - 110)}" fill="none" stroke="{INK}" stroke-width="16" stroke-linecap="round"/>'
        o += f'<path d="M {f(lx + dx)} {f(a1 - 10)} L {f(lx + dx)} {f(a0 - 70)} Q {f(lx + dx)} {f(a0 - 120)} {f(lx + dx + 40)} {f(a0 - 110)}" fill="none" stroke="#DDE3EE" stroke-width="8" stroke-linecap="round"/>'
    # suelo delantero
    o += f'<rect x="0" y="{f(a1)}" width="{W}" height="{f(H - a1)}" fill="url(#baldosaPis)"/>'
    o += f'<rect x="0" y="{f(a1)}" width="{W}" height="26" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/>'
    o += f'<rect x="0" y="{f(a1 + 26)}" width="{W}" height="18" fill="#2F7FD6"/>'
    o += '<g stroke="#D3C09E" stroke-width="3">' + "".join(
        f'<line x1="0" y1="{f(y)}" x2="{W}" y2="{f(y)}"/>' for y in range(int(a1 + 120), H, 110)) + "".join(
        f'<line x1="{x}" y1="{f(a1 + 44)}" x2="{x}" y2="{H}"/>' for x in range(0, W, 135)) + "</g>"
    return o

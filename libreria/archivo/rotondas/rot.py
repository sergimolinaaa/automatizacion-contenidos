"""Piezas comunes del vídeo de las rotondas (vista aérea, coches, GPS)."""
import math, sys
SP = "/tmp/claude-0/-home-user-automatizacion-contenidos/039df981-7a17-5355-b711-18510fb209db/scratchpad"
for p in (SP, SP + "/lote5"):
    if p not in sys.path:
        sys.path.insert(0, p)
from lib import f, smooth, dbl, text_w, lg, rg, INK, LIME, CORAL  # noqa
from pol import T, label, MONO, DISP, save  # noqa

CX, CY = 540, 880
R_ISL, R_MID, R_OUT = 140, 235, 330
R_IN_L, R_OUT_L = 188, 283     # centro de carril interior / exterior
HALF = 130                      # media anchura de cada ramal
LANE = 65                       # desplazamiento del carril respecto al eje
OUT = "/home/user/automatizacion-contenidos/content/lote6-04-rotondas/"

CARS = {  # nombre: (oscuro, medio, claro)
    "rojo": ("#B3261E", "#F0483E", "#FF8A80"),
    "blanco": ("#B9C0CE", "#F4F6FA", "#FFFFFF"),
    "amarillo": ("#D99A00", "#FFC83D", "#FFE8A0"),
    "azul": ("#1F5FBF", "#3D8BFF", "#9CC6FF"),
    "verde": ("#1E8E5A", "#36C27E", "#9BEFC3"),
}


def polar(th, r):
    a = math.radians(th)
    return (CX + r * math.cos(a), CY - r * math.sin(a))


def arc(t0, t1, r, n=None):
    n = n or max(3, int(abs(t1 - t0) / 8))
    return [polar(t0 + (t1 - t0) * i / n, r) for i in range(n + 1)]


def defs():
    s = ""
    for k, (d, m, l) in CARS.items():
        s += lg(f"car_{k}", [(0, d), (0.22, m), (0.5, l), (0.78, m), (1, d)], 0, 0, 1, 0)
        s += lg(f"roof_{k}", [(0, m), (1, l)])
    s += lg("glass", [(0, "#9FD8FF"), (1, "#2B4C7E")])
    s += lg("asph", [(0, "#5A6070"), (1, "#434856")])
    s += rg("asphR", [(0, "#5C6272"), (0.8, "#4C5160"), (1, "#3F4350")])
    s += rg("grassR", [(0, "#8EE07E"), (1, "#3FAE5A")])
    s += lg("grassBg", [(0, "#A9D98F"), (1, "#7FBF6E")])
    s += lg("roofA", [(0, "#F2C9A0"), (1, "#D99B6C")])
    s += lg("roofB", [(0, "#E9EDF5"), (1, "#B9C2D3")])
    s += lg("roofC", [(0, "#F7A98F"), (1, "#D9705A")])
    s += rg("treeR", [(0, "#7FE38A"), (0.7, "#2FA35A"), (1, "#1E7A43")], 0.4, 0.35, 0.65)
    s += lg("gpsG", [(0, "#2A3045"), (1, "#151926")])
    s += lg("paperB", [(0, "#FFFFFF"), (1, "#EEF0F5")])
    s += rg("glow", [(0, "#FFB020", 0.9), (1, "#FFB020", 0)])
    return s


def header(w, h, extra=""):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">\n<defs>{defs()}{extra}</defs>'


def g(id_, body, extra=""):
    return f'<g id="{id_}"{extra}>{body}</g>'


def car(id_, x, y, hd, col, tag=None, blink=False, s=1.0):
    """Coche visto desde arriba, centrado en (x, y), hd = rumbo en grados (0 = hacia arriba, positivo = horario)."""
    d, m, l = CARS[col]
    w, h = 58, 112
    b = f'<g transform="translate({f(x)} {f(y)}) rotate({f(hd)}) scale({s})">'
    b += f'<rect x="{-w/2+5}" y="{-h/2+9}" width="{w}" height="{h}" rx="20" fill="{INK}" opacity="0.28"/>'
    # retrovisores
    b += f'<rect x="{-w/2-9}" y="-22" width="12" height="9" rx="4" fill="{m}" stroke="{INK}" stroke-width="3.5"/>'
    b += f'<rect x="{w/2-3}" y="-22" width="12" height="9" rx="4" fill="{m}" stroke="{INK}" stroke-width="3.5"/>'
    # carrocería
    b += f'<rect x="{-w/2}" y="{-h/2}" width="{w}" height="{h}" rx="19" fill="url(#car_{col})" stroke="{INK}" stroke-width="5"/>'
    # capó: líneas
    b += f'<path d="M -14 -50 Q 0 -54 14 -50" fill="none" stroke="{d}" stroke-width="2.5" opacity="0.7"/>'
    # parabrisas
    b += f'<path d="M -22 -26 Q 0 -36 22 -26 L 19 -10 Q 0 -14 -19 -10 Z" fill="url(#glass)" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>'
    b += '<path d="M -14 -27 L -8 -14" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" opacity="0.8"/>'
    # techo
    b += f'<rect x="-19" y="-10" width="38" height="36" rx="7" fill="url(#roof_{col})" stroke="{INK}" stroke-width="3"/>'
    b += f'<path d="M -14 -6 L 12 -6" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" opacity="0.7"/>'
    # luneta
    b += f'<path d="M -19 27 Q 0 31 19 27 L 21 40 Q 0 45 -21 40 Z" fill="url(#glass)" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>'
    # faros y pilotos
    b += '<ellipse cx="-17" cy="-52" rx="7" ry="3.5" fill="#FFF6C2" stroke="#0B0B14" stroke-width="2"/>'
    b += '<ellipse cx="17" cy="-52" rx="7" ry="3.5" fill="#FFF6C2" stroke="#0B0B14" stroke-width="2"/>'
    b += '<rect x="-24" y="50" width="12" height="5" rx="2" fill="#FF3B30" stroke="#0B0B14" stroke-width="2"/>'
    b += '<rect x="12" y="50" width="12" height="5" rx="2" fill="#FF3B30" stroke="#0B0B14" stroke-width="2"/>'
    # brillo lateral
    b += f'<path d="M {-w/2+6} -30 L {-w/2+6} 30" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" opacity="0.55"/>'
    if tag:
        b += T(0, 15, tag, 20, INK, font=DISP)
    if blink:  # intermitente derecho (delante y detrás)
        bl = ""
        for yy in (-50, 50):
            bl += f'<circle cx="25" cy="{yy}" r="17" fill="url(#glow)"/><circle cx="25" cy="{yy}" r="6.5" fill="#FFB020" stroke="{INK}" stroke-width="2.5"/>'
        b += f'<g id="{id_}b">{bl}</g>'
    b += "</g>"
    return g(id_, b)


def route(id_, pts_, col, w=16, op=0.92):
    d = smooth(pts_)
    return g(id_, dbl(d, w, col, 8), f' opacity="{op}"')


def tree(x, y, r):
    return (f'<circle cx="{f(x+6)}" cy="{f(y+8)}" r="{f(r)}" fill="{INK}" opacity="0.22"/>'
            f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="url(#treeR)" stroke="{INK}" stroke-width="4"/>'
            f'<circle cx="{f(x-r*0.3)}" cy="{f(y-r*0.3)}" r="{f(r*0.25)}" fill="#B8F5B0" opacity="0.6"/>')


def building(x, y, w, h, roof):
    return (f'<rect x="{x+10}" y="{y+12}" width="{w}" height="{h}" rx="6" fill="{INK}" opacity="0.25"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="url(#{roof})" stroke="{INK}" stroke-width="5"/>'
            f'<rect x="{x+14}" y="{y+14}" width="{w-28}" height="{h-28}" rx="4" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.45"/>'
            f'<rect x="{x+w*0.6}" y="{y+h*0.2}" width="{w*0.22}" height="{h*0.18}" rx="3" fill="#8E97AA" stroke="{INK}" stroke-width="3"/>')


def base(W=1080, H=1920):
    o = [f'<rect width="{W}" height="{H}" fill="url(#grassBg)"/>']
    # aceras de los ramales y del anillo
    sw = 26
    o.append(f'<rect x="{CX-HALF-sw}" y="0" width="{2*(HALF+sw)}" height="{H}" fill="#D9DCE3" stroke="{INK}" stroke-width="4"/>')
    o.append(f'<rect x="0" y="{CY-HALF-sw}" width="{W}" height="{2*(HALF+sw)}" fill="#D9DCE3" stroke="{INK}" stroke-width="4"/>')
    o.append(f'<circle cx="{CX}" cy="{CY}" r="{R_OUT+sw}" fill="#D9DCE3" stroke="{INK}" stroke-width="4"/>')
    # manzanas de edificios y árboles en los cuatro cuadrantes
    for (x, y, w, h, r) in [(20, 120, 300, 250, "roofA"), (760, 140, 300, 220, "roofB"), (40, 470, 230, 190, "roofC"),
                            (830, 480, 230, 200, "roofA"), (30, 1090, 250, 260, "roofB"), (820, 1110, 240, 230, "roofC"),
                            (40, 1420, 300, 330, "roofA"), (750, 1440, 300, 300, "roofB")]:
        o.append(building(x, y, w, h, r))
    for (x, y, r) in [(330, 650, 34), (760, 650, 30), (300, 1120, 32), (780, 1110, 30), (360, 470, 26), (720, 470, 26),
                      (360, 1300, 28), (720, 1300, 28), (180, 410, 28), (900, 420, 26), (200, 1820, 30), (900, 1830, 30)]:
        o.append(tree(x, y, r))
    # asfalto
    o.append(f'<rect x="{CX-HALF}" y="0" width="{2*HALF}" height="{H}" fill="url(#asph)"/>')
    o.append(f'<rect x="0" y="{CY-HALF}" width="{W}" height="{2*HALF}" fill="url(#asph)"/>')
    o.append(f'<circle cx="{CX}" cy="{CY}" r="{R_OUT}" fill="url(#asphR)" stroke="{INK}" stroke-width="6"/>')
    # tapar bordes del anillo dentro de los ramales
    for (x, y, w, h) in [(CX-HALF+3, 0, 2*HALF-6, CY-R_OUT+40), (CX-HALF+3, CY+R_OUT-40, 2*HALF-6, H), (0, CY-HALF+3, CX-R_OUT+40, 2*HALF-6), (CX+R_OUT-40, CY-HALF+3, W, 2*HALF-6)]:
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#asph)"/>')
    # bordillos de los ramales
    for xx in (CX-HALF, CX+HALF):
        o.append(f'<path d="M {xx} 0 L {xx} {CY-R_OUT+math.sqrt(0)}" stroke="{INK}" stroke-width="6"/>')
    ky = CY - math.sqrt(R_OUT**2 - HALF**2)
    for xx in (CX-HALF, CX+HALF):
        o.append(f'<path d="M {xx} 0 L {xx} {f(ky)} M {xx} {f(2*CY-ky)} L {xx} {H}" stroke="{INK}" stroke-width="6"/>')
    kx = CX - math.sqrt(R_OUT**2 - HALF**2)
    for yy in (CY-HALF, CY+HALF):
        o.append(f'<path d="M 0 {yy} L {f(kx)} {yy} M {f(2*CX-kx)} {yy} L {W} {yy}" stroke="{INK}" stroke-width="6"/>')
    # quitar la línea del borde del anillo entre bordillos (repintar asfalto en las bocas)
    # (se dibuja el anillo con contorno y luego las bocas encima)
    for (x, y, w, h) in [(CX-HALF+3, ky-20, 2*HALF-6, 60), (CX-HALF+3, 2*CY-ky-40, 2*HALF-6, 60), (kx-20, CY-HALF+3, 60, 2*HALF-6), (2*CX-kx-40, CY-HALF+3, 60, 2*HALF-6)]:
        o.append(f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" fill="#4F5463"/>')
    # isletas separadoras (gota) en cada ramal
    for ang in (0, 90, 180, 270):
        p0 = polar(ang, R_OUT + 14)
        p1 = polar(ang, R_OUT + 115)
        a = math.radians(ang)
        nx, ny = -math.sin(a), -math.cos(a)  # perpendicular (pantalla)
        q = [(p0[0] + nx * 26, p0[1] + ny * 26), (p1[0] + nx * 8, p1[1] + ny * 8), (p1[0] - nx * 8, p1[1] - ny * 8), (p0[0] - nx * 26, p0[1] - ny * 26)]
        d = smooth(q + [q[0]], closed=False, t=0.6)
        o.append(f'<path d="{d}" fill="#E4E7EE" stroke="{INK}" stroke-width="5"/>')
        o.append(f'<path d="{smooth([(p0[0]+nx*14, p0[1]+ny*14), (p1[0], p1[1])])}" stroke="#7FD06E" stroke-width="9" stroke-linecap="round" fill="none"/>')
    # eje continuo de los ramales (más allá de la isleta)
    o.append(f'<path d="M {CX} 0 L {CX} {CY-R_OUT-115} M {CX} {CY+R_OUT+115} L {CX} {H} M 0 {CY} L {CX-R_OUT-115} {CY} M {CX+R_OUT+115} {CY} L {W} {CY}" stroke="#F5F5F0" stroke-width="6" stroke-dasharray="40 30"/>')
    # línea discontinua entre carriles del anillo
    o.append(f'<circle cx="{CX}" cy="{CY}" r="{R_MID}" fill="none" stroke="#F5F5F0" stroke-width="6" stroke-dasharray="34 26"/>')
    # líneas de ceda el paso (discontinuas transversales) en las entradas + triángulos pintados
    for ang in (0, 90, 180, 270):
        a = math.radians(ang)
        ux, uy = math.cos(a), -math.sin(a)           # hacia fuera
        nx, ny = -math.sin(a), -math.cos(a)          # sentido de la circulación (antihorario)
        # carril de entrada: lado "anterior" en el sentido de giro -> -n
        c = (CX + ux * (R_OUT + 8), CY + uy * (R_OUT + 8))
        o.append(f'<path d="M {f(c[0]+nx*30)} {f(c[1]+ny*30)} L {f(c[0]+nx*124)} {f(c[1]+ny*124)}" stroke="#F5F5F0" stroke-width="9" stroke-dasharray="18 12"/>')
        tc = (CX + ux * (R_OUT + 175) + nx * LANE, CY + uy * (R_OUT + 175) + ny * LANE)
        tip = (tc[0] + ux * 34, tc[1] + uy * 34)
        bl = (tc[0] - ux * 30 - nx * 22, tc[1] - uy * 30 - ny * 22)
        br = (tc[0] - ux * 30 + nx * 22, tc[1] - uy * 30 + ny * 22)
        o.append(f'<path d="M {f(tip[0])} {f(tip[1])} L {f(bl[0])} {f(bl[1])} L {f(br[0])} {f(br[1])} Z" fill="none" stroke="#F5F5F0" stroke-width="7" stroke-linejoin="round"/>')
    # pasos de cebra
    for ang in (0, 90, 180, 270):
        a = math.radians(ang)
        ux, uy = math.cos(a), -math.sin(a)
        nx, ny = -math.sin(a), -math.cos(a)
        for k in range(-5, 6):
            c = (CX + ux * (R_OUT + 290) + nx * k * 23, CY + uy * (R_OUT + 290) + ny * k * 23)
            o.append(f'<path d="M {f(c[0]-ux*24)} {f(c[1]-uy*24)} L {f(c[0]+ux*24)} {f(c[1]+uy*24)}" stroke="#F5F5F0" stroke-width="12"/>')
    # isleta central
    o.append(f'<circle cx="{CX}" cy="{CY}" r="{R_ISL+12}" fill="#E4E7EE" stroke="{INK}" stroke-width="6"/>')
    o.append(f'<circle cx="{CX}" cy="{CY}" r="{R_ISL}" fill="url(#grassR)" stroke="{INK}" stroke-width="4"/>')
    o.append(f'<circle cx="{CX}" cy="{CY}" r="{R_ISL-28}" fill="none" stroke="#B8F5B0" stroke-width="4" stroke-dasharray="10 14" opacity="0.7"/>')
    for (dx, dy, r) in [(-52, -40, 30), (48, -52, 26), (-30, 58, 28), (60, 40, 30), (0, 0, 38)]:
        o.append(tree(CX + dx, CY + dy, r))
    return "\n".join(o)


def gps(id_, x, y, w, top, big, sub, badge=None, col="#FFC83D", icon="ring"):
    """Tarjeta tipo navegador GPS."""
    h = 128
    s = f'<rect x="{x+7}" y="{y+9}" width="{w}" height="{h}" rx="22" fill="{INK}" opacity="0.35"/>'
    s += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="url(#gpsG)" stroke="{INK}" stroke-width="6"/>'
    s += f'<path d="M {x+24} {y+7} L {x+w-24} {y+7}" stroke="#FFFFFF" stroke-width="3" opacity="0.25" stroke-linecap="round"/>'
    ix, iy = x + 16, y + 16
    s += f'<rect x="{ix}" y="{iy}" width="96" height="96" rx="18" fill="{col}" stroke="{INK}" stroke-width="5"/>'
    c = (ix + 48, iy + 48)
    k = 1.25
    if icon == "ring":
        s += f'<circle cx="{c[0]}" cy="{c[1]}" r="{17*k}" fill="none" stroke="{INK}" stroke-width="8"/>'
        s += f'<path d="M {c[0]+8*k} {c[1]+34*k} L {c[0]+8*k} {c[1]+14*k} M {c[0]-15*k} {c[1]-8*k} L {c[0]-30*k} {c[1]-8*k}" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>'
        s += f'<path d="M {c[0]-24*k} {c[1]-15*k} L {c[0]-32*k} {c[1]-8*k} L {c[0]-24*k} {c[1]-1*k}" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'
    elif icon == "recalc":
        s += f'<path d="M {c[0]+22} {c[1]-12} A 25 25 0 1 0 {c[0]+25} {c[1]+8}" fill="none" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round"/>'
        s += f'<path d="M {c[0]+8} {c[1]-17} L {c[0]+25} {c[1]-14} L {c[0]+27} {c[1]-31}" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'
    elif icon == "loop":
        s += f'<path d="M {c[0]} {c[1]-25} A 25 25 0 1 1 {c[0]-25} {c[1]}" fill="none" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>'
        s += f'<path d="M {c[0]-37} {c[1]-10} L {c[0]-25} {c[1]+5} L {c[0]-10} {c[1]-7}" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'
    tx = ix + 116
    if top:
        s += T(tx, y + 48, top, 26, "#AEB6C8", anchor="start")
        s += T(tx, y + 98, big, 40, "#FFFFFF", anchor="start")
    else:
        s += T(tx, y + 80, big, 42, "#FFFFFF", anchor="start")
    if badge:
        s += T(x + w - 24, y + 92, badge, 62, col, anchor="end", font=DISP)
    return g(id_, s)


def badge(id_, x, y, n, col="#FFC83D"):
    return g(id_, f'<circle cx="{x+4}" cy="{y+6}" r="30" fill="{INK}" opacity="0.3"/><circle cx="{x}" cy="{y}" r="30" fill="{col}" stroke="{INK}" stroke-width="5"/>'
             + T(x, y + 12, n, 34, INK, font=DISP))


def horn(id_, x, y, text="¡PIII!", r=70):
    pts = []
    for i in range(24):
        rr = r if i % 2 == 0 else r * 0.72
        a = math.pi * 2 * i / 24
        pts.append((x + rr * math.cos(a) * 1.25, y + rr * math.sin(a)))
    d = "M " + " L ".join(f"{f(a)} {f(b)}" for a, b in pts) + " Z"
    return g(id_, f'<path d="{d}" fill="#FFE14D" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>' + T(x, y + 11, text, 30, INK, font=DISP))


def ceda_sign(id_, x, y, s=1.0):
    """Señal de ceda el paso (R-1) sobre poste, vista algo inclinada para leerse desde arriba."""
    r = 44 * s
    p = [(x, y + r), (x - r * 1.1, y - r * 0.85), (x + r * 1.1, y - r * 0.85)]
    pi = [(x, y + r * 0.45), (x - r * 0.6, y - r * 0.55), (x + r * 0.6, y - r * 0.55)]
    d = lambda q: "M " + " L ".join(f"{f(a)} {f(b)}" for a, b in q) + " Z"
    return g(id_, f'<rect x="{x-5}" y="{y+r-6}" width="10" height="{f(40*s)}" fill="#9AA3B5" stroke="{INK}" stroke-width="3"/>'
             f'<path d="{d(p)}" fill="#E8322B" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
             f'<path d="{d(pi)}" fill="#FFFFFF" stroke="#B3261E" stroke-width="2" stroke-linejoin="round"/>')


def crossmark(id_, x, y, r=34):
    return g(id_, f'<circle cx="{x}" cy="{y}" r="{r}" fill="{CORAL}" stroke="{INK}" stroke-width="5"/>'
             f'<path d="M {x-r*0.4} {y-r*0.4} L {x+r*0.4} {y+r*0.4} M {x+r*0.4} {y-r*0.4} L {x-r*0.4} {y+r*0.4}" stroke="#FFFFFF" stroke-width="{r*0.25}" stroke-linecap="round"/>')


def checkmark(id_, x, y, r=34):
    return g(id_, f'<circle cx="{x}" cy="{y}" r="{r}" fill="{LIME}" stroke="{INK}" stroke-width="5"/>'
             f'<path d="M {x-r*0.45} {y} L {x-r*0.1} {y+r*0.38} L {x+r*0.5} {y-r*0.38}" fill="none" stroke="{INK}" stroke-width="{r*0.22}" stroke-linecap="round" stroke-linejoin="round"/>')

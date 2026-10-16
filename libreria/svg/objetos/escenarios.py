"""Fondos completos (para layout full 1080x1920 o panel 1000x700): habitación, escenario con cortinas y foco,
cocina con azulejos, oficina, cielo/paisaje con colinas, rotonda vista desde arriba (con coches cenitales).
Todos devuelven SVG sin ids (son fondo); cada uno acepta W, H para encajar en cualquier layout.
Recuerda: en full, lo importante entre y 450 y 1250 (arriba titular, abajo subtítulos).

Sale de: nuevo-partido/gancho.py (cortinas, foco, tarima), hielo-cruje/vaso.py (cocina), papeleta-nula/senado.py y
voto-blanco (pared y suelo de madera), cielo/paisaje.py y atardecer.py (nubes, sol, colinas), rotondas/rot.py (rotonda,
coches, árboles y edificios vistos desde arriba).
"""
import math
import random
from ..base import (INK, LIME, CORAL, YEL, f, g, gt, T, DISP, shade, trazo, sombra, brillo, lg, rg, registrar_defs, degradado,
                    nube, smooth, poly)
from .casa import ventana

registrar_defs(
    lg("curtG", [(0, "#C2324A"), (1, "#86182C")], 0, 0, 1, 0) + lg("stageG", [(0, "#B57A45"), (1, "#7A4E28")])
    + lg("wallN", [(0, "#1E2A4A"), (1, "#33476F")]) + rg("spotR", [(0, "#FFF7D6", 0.55), (1, "#FFF7D6", 0)])
    + lg("skyDia", [(0, "#8FCBFF"), (1, "#E3F3FF")]) + lg("skyTarde", [(0, "#5B6FD6"), (0.55, "#FF9E7A"), (1, "#FFD59A")])
    + lg("skyNoche", [(0, "#0F1838"), (1, "#2E3F7A")])
    + rg("solR", [(0, "#FFF6B8"), (1, "#FFC928")], 0.4, 0.35, 0.7) + rg("solGlow", [(0, "#FFE15A", 0.6), (1, "#FFE15A", 0)])
    + lg("asph", [(0, "#5A6070"), (1, "#434856")]) + rg("asphR", [(0, "#5C6272"), (0.8, "#4C5160"), (1, "#3F4350")])
    + rg("grassR", [(0, "#8EE07E"), (1, "#3FAE5A")]) + lg("grassBg", [(0, "#A9D98F"), (1, "#7FBF6E")])
    + lg("roofA", [(0, "#F2C9A0"), (1, "#D99B6C")]) + lg("roofB", [(0, "#E9EDF5"), (1, "#B9C2D3")]) + lg("roofC", [(0, "#F7A98F"), (1, "#D9705A")])
    + rg("treeR", [(0, "#7FE38A"), (0.7, "#2FA35A"), (1, "#1E7A43")], 0.4, 0.35, 0.65)
    + lg("carGlass", [(0, "#9FD8FF"), (1, "#2B4C7E")]) + rg("blinkGlow", [(0, "#FFB020", 0.9), (1, "#FFB020", 0)])
)

COCHES = {  # nombre: (oscuro, medio, claro)
    "rojo": ("#B3261E", "#F0483E", "#FF8A80"),
    "blanco": ("#B9C0CE", "#F4F6FA", "#FFFFFF"),
    "amarillo": ("#D99A00", "#FFC83D", "#FFE8A0"),
    "azul": ("#1F5FBF", "#3D8BFF", "#9CC6FF"),
    "verde": ("#1E8E5A", "#36C27E", "#9BEFC3"),
}
for _k, (_d, _m, _l) in COCHES.items():
    registrar_defs(lg(f"car_{_k}", [(0, _d), (0.22, _m), (0.5, _l), (0.78, _m), (1, _d)], 0, 0, 1, 0), lg(f"carRoof_{_k}", [(0, _m), (1, _l)]))


# --------------------------------------------------------------- interiores
def _suelo_madera(W, y0, H, col="maderaG"):
    o = f'<rect x="0" y="{f(y0)}" width="{W}" height="{f(H-y0)}" fill="url(#{col})"/>'
    o += f'<path d="M 0 {f(y0)} L {W} {f(y0)}" stroke="{INK}" stroke-width="8"/>'
    o += f'<path d="M 0 {f(y0+12)} L {W} {f(y0+12)}" stroke="#F3D3A6" stroke-width="5"/>'
    o += '<g fill="none" stroke="#7A4E2A" stroke-width="3" opacity="0.45">' + "".join(
        f'<path d="M 0 {f(y)} C {W*0.28} {f(y-12)}, {W*0.65} {f(y+14)}, {W} {f(y)}"/>' for y in [y0 + (H - y0) * k for k in (0.15, 0.35, 0.58, 0.82)]) + "</g>"
    return o


def habitacion(W=1080, H=1920, pared="#EAF0FA", suelo_y=None, ventana_=True, cuadro=True, zocalo=True, noche=False):
    """Salón/habitación: pared con papel de rayas suaves, zócalo, suelo de madera, ventana y cuadro."""
    sy = suelo_y or H * 0.69
    gid = f"pared_{pared[1:]}"
    registrar_defs(lg(gid, [(0, shade(pared, 0.3)), (1, shade(pared, -0.08))]))
    o = f'<rect width="{W}" height="{H}" fill="url(#{gid})"/>'
    o += f'<g stroke="{shade(pared,-0.06)}" stroke-width="10" opacity="0.7">' + "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="{f(sy)}"/>' for x in range(60, W, 120)) + "</g>"
    if ventana_:
        o += ventana(None, W * 0.3, sy * 0.36, W * 0.3, sy * 0.36, noche=noche)
    if cuadro:
        cx, cy, cw, ch = W * 0.76, sy * 0.33, W * 0.2, W * 0.15
        o += f'<rect x="{f(cx-cw/2+8)}" y="{f(cy-ch/2+10)}" width="{f(cw)}" height="{f(ch)}" rx="6" fill="{INK}" opacity="0.2"/>'
        o += f'<rect x="{f(cx-cw/2)}" y="{f(cy-ch/2)}" width="{f(cw)}" height="{f(ch)}" rx="6" fill="{degradado("#C98B55", 0.2)}" stroke="{INK}" stroke-width="6"/>'
        o += f'<rect x="{f(cx-cw/2+14)}" y="{f(cy-ch/2+14)}" width="{f(cw-28)}" height="{f(ch-28)}" fill="#BFE6FF" stroke="{INK}" stroke-width="3"/>'
        o += f'<path d="M {f(cx-cw/2+14)} {f(cy+ch/2-14)} L {f(cx-cw*0.15)} {f(cy-ch*0.1)} L {f(cx+cw*0.05)} {f(cy+ch*0.15)} L {f(cx+cw*0.2)} {f(cy-ch*0.05)} L {f(cx+cw/2-14)} {f(cy+ch/2-14)} Z" fill="#7BC77F" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
        o += f'<circle cx="{f(cx+cw*0.22)}" cy="{f(cy-ch*0.22)}" r="{f(cw*0.07)}" fill="{YEL}" stroke="{INK}" stroke-width="3"/>'
    if zocalo:
        o += f'<rect x="0" y="{f(sy-34)}" width="{W}" height="34" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/>'
    o += _suelo_madera(W, sy, H)
    if noche:
        o += f'<rect width="{W}" height="{H}" fill="#1B2550" opacity="0.25"/>'
    return o


def cocina(W=1080, H=1920, encimera_y=None, pared="#EAF4FB"):
    """Cocina: azulejos blancos y encimera de madera (para vasos, ollas, comida)."""
    ey = encimera_y or H * 0.68
    gid = f"coc_{pared[1:]}"
    registrar_defs(lg(gid, [(0, pared), (1, shade(pared, -0.12))]))
    o = f'<rect width="{W}" height="{H}" fill="url(#{gid})"/>'
    o += f'<g stroke="{shade(pared,-0.08)}" stroke-width="4">' + "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="{f(ey)}"/>' for x in range(90, W, 150)) \
        + "".join(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}"/>' for y in range(100, int(ey), 150)) + "</g>"
    o += _suelo_madera(W, ey, H, "maderaG")
    return o


def oficina(W=1080, H=1920, suelo_y=None):
    """Oficina: pared gris azulada, ventana con lamas, estantería con archivadores y suelo de moqueta."""
    sy = suelo_y or H * 0.7
    registrar_defs(lg("ofiPared", [(0, "#E4E9F2"), (1, "#C9D2E2")]), lg("moqueta", [(0, "#7C879C"), (1, "#5A647A")]))
    o = f'<rect width="{W}" height="{H}" fill="url(#ofiPared)"/>'
    wx, wy, ww, wh = W * 0.08, sy * 0.12, W * 0.38, sy * 0.42
    o += f'<rect x="{f(wx)}" y="{f(wy)}" width="{f(ww)}" height="{f(wh)}" rx="8" fill="url(#skyWin)" stroke="{INK}" stroke-width="7"/>'
    o += f'<g stroke="#E9EDF5" stroke-width="12">' + "".join(f'<line x1="{f(wx+6)}" y1="{f(y)}" x2="{f(wx+ww-6)}" y2="{f(y)}"/>' for y in [wy + wh * k / 9 for k in range(1, 9)]) + "</g>"
    o += f'<g stroke="{INK}" stroke-width="2" opacity="0.35">' + "".join(f'<line x1="{f(wx+6)}" y1="{f(y+6)}" x2="{f(wx+ww-6)}" y2="{f(y+6)}"/>' for y in [wy + wh * k / 9 for k in range(1, 9)]) + "</g>"
    sx_, sy_, sw_, sh_ = W * 0.6, sy * 0.1, W * 0.32, sy * 0.62
    o += f'<rect x="{f(sx_)}" y="{f(sy_)}" width="{f(sw_)}" height="{f(sh_)}" rx="6" fill="{degradado("#B08A62", 0.2)}" stroke="{INK}" stroke-width="7"/>'
    rnd = random.Random(4)
    cols = ["#2347FF", CORAL, YEL, "#1FB5A8", "#7B5CFF", "#FFFFFF"]
    for r in range(3):
        y1 = sy_ + sh_ * (r + 1) / 3
        o += f'<rect x="{f(sx_)}" y="{f(y1-12)}" width="{f(sw_)}" height="12" fill="#8A6A48" stroke="{INK}" stroke-width="4"/>'
        x = sx_ + 14
        while x < sx_ + sw_ - 40:
            bw = rnd.uniform(24, 40)
            bh = sh_ / 3 * rnd.uniform(0.55, 0.8)
            c = cols[rnd.randrange(len(cols))]
            o += f'<rect x="{f(x)}" y="{f(y1-12-bh)}" width="{f(bw)}" height="{f(bh)}" rx="4" fill="{degradado(c, 0.15, "h")}" stroke="{INK}" stroke-width="4"/>'
            o += f'<rect x="{f(x+bw*0.25)}" y="{f(y1-12-bh*0.75)}" width="{f(bw*0.5)}" height="{f(bh*0.18)}" rx="2" fill="#FFFFFF" opacity="0.8"/>'
            x += bw + 4
    o += f'<rect x="0" y="{f(sy)}" width="{W}" height="{f(H-sy)}" fill="url(#moqueta)"/><path d="M 0 {f(sy)} L {W} {f(sy)}" stroke="{INK}" stroke-width="8"/>'
    o += f'<rect x="0" y="{f(sy-26)}" width="{W}" height="26" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/>'
    return o


def escenario(W=1080, H=1920, suelo_y=None, foco_x=None):
    """Escenario de mitin/teatro: pared oscura, cortinas rojas laterales, foco de luz y tarima de madera."""
    sy = suelo_y or H * 0.65
    fx = foco_x or W * 0.5
    o = f'<rect width="{W}" height="{H}" fill="url(#wallN)"/>'
    for k in (0, 1):
        x = 0 if k == 0 else W
        s = 1 if k == 0 else -1
        cw = W * 0.14
        o += f'<path d="M {x} 0 L {f(x+s*cw)} 0 C {f(x+s*cw*0.8)} {f(sy*0.4)}, {f(x+s*cw*1.13)} {f(sy*0.72)}, {f(x+s*cw*0.6)} {f(sy)} L {x} {f(sy)} Z" fill="url(#curtG)" stroke="{INK}" stroke-width="7"/>'
        for j in (0.27, 0.57):
            o += f'<path d="M {f(x+s*cw*j)} 20 C {f(x+s*cw*(j-0.07))} {f(sy*0.4)}, {f(x+s*cw*(j+0.1))} {f(sy*0.72)}, {f(x+s*cw*(j-0.13))} {f(sy-10)}" fill="none" stroke="#6E1022" stroke-width="5" opacity="0.7"/>'
    o += f'<path d="M 0 0 L {W} 0 L {W} {f(H*0.05)} Q {f(W*0.75)} {f(H*0.085)} {f(W*0.5)} {f(H*0.05)} Q {f(W*0.25)} {f(H*0.085)} 0 {f(H*0.05)} Z" fill="url(#curtG)" stroke="{INK}" stroke-width="7"/>'
    o += f'<path d="M {f(fx-70)} 0 L {f(fx+70)} 0 L {f(fx+W*0.26)} {f(sy)} L {f(fx-W*0.26)} {f(sy)} Z" fill="url(#spotR)" opacity="0.9"/>'
    o += f'<ellipse cx="{f(fx)}" cy="{f(sy+12)}" rx="{f(W*0.28)}" ry="{f(H*0.02)}" fill="#FFF7D6" opacity="0.35"/>'
    o += f'<rect x="0" y="{f(sy)}" width="{W}" height="{f(H-sy)}" fill="url(#stageG)"/><path d="M 0 {f(sy)} L {W} {f(sy)}" stroke="{INK}" stroke-width="8"/>'
    o += '<g stroke="#5E3B1C" stroke-width="3" opacity="0.6">' + "".join(f'<line x1="0" y1="{f(y)}" x2="{W}" y2="{f(y)}"/>' for y in [sy + (H - sy) * k for k in (0.12, 0.3, 0.52, 0.8)]) + "</g>"
    return o


# --------------------------------------------------------------- exteriores
def sol(id_, cx, cy, r=60, rayos=True):
    """Sol con halo, rayos (grupo id_+'_rayos': anímalo con spin) y brillo."""
    o = f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r*2.4)}" fill="url(#solGlow)"/>'
    if rayos:
        rs = "".join(trazo(f"M {f(cx+(r+16)*math.cos(k*math.pi/6))} {f(cy+(r+16)*math.sin(k*math.pi/6))} L {f(cx+(r+40)*math.cos(k*math.pi/6))} {f(cy+(r+40)*math.sin(k*math.pi/6))}", 8, "#FFD23F", 6) for k in range(12))
        o += g(f"{id_}_rayos" if id_ else None, rs)
    o += f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="url(#solR)" stroke="{INK}" stroke-width="7"/>'
    o += brillo(f"M {f(cx-r*0.62)} {f(cy-r*0.33)} A {f(r*0.7)} {f(r*0.7)} 0 0 1 {f(cx-r*0.17)} {f(cy-r*0.7)}", 7, 0.85)
    return g(id_, o)


def cielo(W=1080, H=1920, hora="dia", colinas=True, nubes=True, sol_=True, seed=2):
    """Cielo con degradado (hora: dia, tarde, noche), nubes, sol/luna y colinas en capas (lejos sin contorno)."""
    sky = {"dia": "skyDia", "tarde": "skyTarde", "noche": "skyNoche"}[hora]
    o = f'<rect width="{W}" height="{H}" fill="url(#{sky})"/>'
    rnd = random.Random(seed)
    if hora == "noche":
        o += "".join(f'<circle cx="{f(rnd.uniform(0, W))}" cy="{f(rnd.uniform(0, H*0.5))}" r="{f(rnd.uniform(2, 4))}" fill="#FFFFFF" opacity="{f(rnd.uniform(0.5, 1))}"/>' for _ in range(40))
        o += f'<circle cx="{f(W*0.75)}" cy="{f(H*0.14)}" r="{f(W*0.06)}" fill="#FFF6C8" stroke="{INK}" stroke-width="6"/><circle cx="{f(W*0.78)}" cy="{f(H*0.13)}" r="{f(W*0.06)}" fill="url(#skyNoche)"/>'
    elif sol_:
        o += sol(None, W * 0.78, H * (0.14 if hora == "dia" else 0.42), W * 0.07)
    if nubes and hora != "noche":
        for i, (a, b, s) in enumerate(((0.22, 0.1, 0.9), (0.55, 0.2, 0.7), (0.15, 0.32, 0.6), (0.82, 0.3, 0.55))):
            o += nube(W * a, H * b, s * W / 1000, contorno=i < 2, op=1 if i < 2 else 0.75)
    if colinas:
        hy = H * 0.62
        far = "#B8DDC4" if hora == "dia" else ("#C9A0B8" if hora == "tarde" else "#2A3A66")
        mid = "#8CCB9A" if hora == "dia" else ("#B07A8E" if hora == "tarde" else "#22305A")
        near = "#5FB86E" if hora != "noche" else "#1B2850"
        o += f'<path d="M 0 {f(hy-60)} C {f(W*0.12)} {f(hy-100)}, {f(W*0.26)} {f(hy-80)}, {f(W*0.38)} {f(hy-100)} C {f(W*0.52)} {f(hy-122)}, {f(W*0.64)} {f(hy-80)}, {f(W*0.76)} {f(hy-90)} C {f(W*0.86)} {f(hy-98)}, {f(W*0.94)} {f(hy-80)}, {W} {f(hy-88)} L {W} {H} L 0 {H} Z" fill="{far}"/>'
        o += f'<path d="M 0 {f(hy)} C {f(W*0.18)} {f(hy-30)}, {f(W*0.34)} {f(hy-2)}, {f(W*0.52)} {f(hy-20)} C {f(W*0.7)} {f(hy-38)}, {f(W*0.86)} {f(hy-8)}, {W} {f(hy-24)} L {W} {H} L 0 {H} Z" fill="{mid}"/>'
        ny = hy + H * 0.04
        o += f'<path d="M 0 {f(ny)} C {f(W*0.2)} {f(ny-30)}, {f(W*0.42)} {f(ny-8)}, {f(W*0.62)} {f(ny-20)} C {f(W*0.8)} {f(ny-30)}, {f(W*0.9)} {f(ny-14)}, {W} {f(ny-20)} L {W} {H} L 0 {H} Z" fill="{degradado(near, 0.15)}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
        o += brillo(f"M {f(W*0.03)} {f(ny+6)} C {f(W*0.2)} {f(ny-20)}, {f(W*0.42)} {f(ny)}, {f(W*0.6)} {f(ny-12)}", 5, 0.6, "#B5F08F")
    return o


def arbol_aereo(x, y, r):
    """Copa de árbol vista desde arriba."""
    return (f'<circle cx="{f(x+6)}" cy="{f(y+8)}" r="{f(r)}" fill="{INK}" opacity="0.22"/>'
            f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="url(#treeR)" stroke="{INK}" stroke-width="4"/>'
            f'<circle cx="{f(x-r*0.3)}" cy="{f(y-r*0.3)}" r="{f(r*0.25)}" fill="#B8F5B0" opacity="0.6"/>')


def edificio_aereo(x, y, w, h, tejado="roofA"):
    """Tejado de edificio visto desde arriba (roofA, roofB, roofC)."""
    return (f'<rect x="{f(x+10)}" y="{f(y+12)}" width="{f(w)}" height="{f(h)}" rx="6" fill="{INK}" opacity="0.25"/>'
            f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="6" fill="url(#{tejado})" stroke="{INK}" stroke-width="5"/>'
            f'<rect x="{f(x+14)}" y="{f(y+14)}" width="{f(w-28)}" height="{f(h-28)}" rx="4" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.45"/>'
            f'<rect x="{f(x+w*0.6)}" y="{f(y+h*0.2)}" width="{f(w*0.22)}" height="{f(h*0.18)}" rx="3" fill="#8E97AA" stroke="{INK}" stroke-width="3"/>')


def coche_aereo(id_, x, y, rumbo=0, color="rojo", s=1.0, intermitente=None, texto=None):
    """Coche visto desde arriba centrado en (x, y). rumbo en grados (0 = hacia arriba, positivo = horario).
    intermitente: 'der' o 'izq' añade el grupo id_+'_inter' (anímalo con pulse amount 3)."""
    d, m, l = COCHES[color]
    w, h = 58, 112
    b = f'<rect x="{-w/2+5}" y="{-h/2+9}" width="{w}" height="{h}" rx="20" fill="{INK}" opacity="0.28"/>'
    b += f'<rect x="{-w/2-9}" y="-22" width="12" height="9" rx="4" fill="{m}" stroke="{INK}" stroke-width="3.5"/>'
    b += f'<rect x="{w/2-3}" y="-22" width="12" height="9" rx="4" fill="{m}" stroke="{INK}" stroke-width="3.5"/>'
    b += f'<rect x="{-w/2}" y="{-h/2}" width="{w}" height="{h}" rx="19" fill="url(#car_{color})" stroke="{INK}" stroke-width="5"/>'
    b += f'<path d="M -14 -50 Q 0 -54 14 -50" fill="none" stroke="{d}" stroke-width="2.5" opacity="0.7"/>'
    b += f'<path d="M -22 -26 Q 0 -36 22 -26 L 19 -10 Q 0 -14 -19 -10 Z" fill="url(#carGlass)" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>'
    b += '<path d="M -14 -27 L -8 -14" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" opacity="0.8"/>'
    b += f'<rect x="-19" y="-10" width="38" height="36" rx="7" fill="url(#carRoof_{color})" stroke="{INK}" stroke-width="3"/>'
    b += '<path d="M -14 -6 L 12 -6" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" opacity="0.7"/>'
    b += f'<path d="M -19 27 Q 0 31 19 27 L 21 40 Q 0 45 -21 40 Z" fill="url(#carGlass)" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>'
    b += f'<ellipse cx="-17" cy="-52" rx="7" ry="3.5" fill="#FFF6C2" stroke="{INK}" stroke-width="2"/><ellipse cx="17" cy="-52" rx="7" ry="3.5" fill="#FFF6C2" stroke="{INK}" stroke-width="2"/>'
    b += f'<rect x="-24" y="50" width="12" height="5" rx="2" fill="#FF3B30" stroke="{INK}" stroke-width="2"/><rect x="12" y="50" width="12" height="5" rx="2" fill="#FF3B30" stroke="{INK}" stroke-width="2"/>'
    b += brillo(f"M {-w/2+6} -30 L {-w/2+6} 30", 3, 0.55)
    if texto:
        b += T(0, 15, texto, 20, INK, font=DISP)
    if intermitente:
        sx = 25 if intermitente == "der" else -25
        bl = "".join(f'<circle cx="{sx}" cy="{yy}" r="17" fill="url(#blinkGlow)"/><circle cx="{sx}" cy="{yy}" r="6.5" fill="#FFB020" stroke="{INK}" stroke-width="2.5"/>' for yy in (-50, 50))
        b += g(f"{id_}_inter" if id_ else None, bl)
    return gt(id_, f"translate({f(x)} {f(y)}) rotate({f(rumbo)}) scale({f(s)})", b)


def rotonda(W=1080, H=1920, cx=540, cy=880, r_isla=140, r_ext=330, semiancho=130, sw=26):
    """Rotonda de 4 ramales vista desde arriba: césped, edificios, árboles, asfalto, isletas, ceda el paso,
    pasos de cebra e isleta central con árboles. Devuelve SVG de fondo; los coches van con coche_aereo().
    Carriles del anillo: interior r ≈ (r_isla+r_mid)/2, exterior r ≈ (r_mid+r_ext)/2 con r_mid = (r_isla+r_ext)/2 + 0."""
    R_MID = (r_isla + r_ext) / 2 + 0
    HALF = semiancho
    LANE = HALF / 2

    def polar(th, r):
        a = math.radians(th)
        return (cx + r * math.cos(a), cy - r * math.sin(a))
    o = [f'<rect width="{W}" height="{H}" fill="url(#grassBg)"/>']
    o.append(f'<rect x="{f(cx-HALF-sw)}" y="0" width="{f(2*(HALF+sw))}" height="{H}" fill="#D9DCE3" stroke="{INK}" stroke-width="4"/>')
    o.append(f'<rect x="0" y="{f(cy-HALF-sw)}" width="{W}" height="{f(2*(HALF+sw))}" fill="#D9DCE3" stroke="{INK}" stroke-width="4"/>')
    o.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r_ext+sw)}" fill="#D9DCE3" stroke="{INK}" stroke-width="4"/>')
    # manzanas y árboles en los cuatro cuadrantes (proporcionales al lienzo)
    qx0, qx1 = cx - HALF - sw - 20, cx + HALF + sw + 20
    for (bx, by, bw, bh, r_) in [(20, 0.06, 0.28, 0.13, "roofA"), (None, 0.07, 0.28, 0.11, "roofB"), (40, 0.245, 0.21, 0.1, "roofC"),
                                 (None, 0.25, 0.21, 0.1, "roofA"), (30, 0.57, 0.23, 0.135, "roofB"), (None, 0.58, 0.22, 0.12, "roofC"),
                                 (40, 0.74, 0.28, 0.17, "roofA"), (None, 0.75, 0.28, 0.16, "roofB")]:
        ww, hh = W * bw, H * bh
        x = bx if bx is not None else W - ww - 20
        y = H * by
        if (x + ww < qx0 or x > qx1) and (y + hh < cy - HALF - sw - 20 or y > cy + HALF + sw + 20):
            if math.hypot(min(abs(x - cx), abs(x + ww - cx)), min(abs(y - cy), abs(y + hh - cy))) > r_ext + sw + 30:
                o.append(edificio_aereo(x, y, ww, hh, r_))
    for (tx, ty, r_) in [(-210, -230, 34), (220, -230, 30), (-240, 240, 32), (240, 230, 30), (-180, -410, 26), (180, -410, 26),
                         (-180, 420, 28), (180, 420, 28), (-360, -470, 28), (360, -460, 26)]:
        x, y = cx + tx, cy + ty
        if 0 < x < W and 0 < y < H and (abs(x - cx) > HALF + sw + r_ and abs(y - cy) > HALF + sw + r_) and math.hypot(x - cx, y - cy) > r_ext + sw + r_:
            o.append(arbol_aereo(x, y, r_))
    o.append(f'<rect x="{f(cx-HALF)}" y="0" width="{f(2*HALF)}" height="{H}" fill="url(#asph)"/>')
    o.append(f'<rect x="0" y="{f(cy-HALF)}" width="{W}" height="{f(2*HALF)}" fill="url(#asph)"/>')
    o.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r_ext)}" fill="url(#asphR)" stroke="{INK}" stroke-width="6"/>')
    ky = math.sqrt(r_ext ** 2 - HALF ** 2)
    for (x, y, w_, h_) in [(cx - HALF + 3, cy - ky - 20, 2 * HALF - 6, 60), (cx - HALF + 3, cy + ky - 40, 2 * HALF - 6, 60),
                           (cx - ky - 20, cy - HALF + 3, 60, 2 * HALF - 6), (cx + ky - 40, cy - HALF + 3, 60, 2 * HALF - 6)]:
        o.append(f'<rect x="{f(x)}" y="{f(y)}" width="{f(w_)}" height="{f(h_)}" fill="#4F5463"/>')
    for xx in (cx - HALF, cx + HALF):
        o.append(f'<path d="M {f(xx)} 0 L {f(xx)} {f(cy-ky)} M {f(xx)} {f(cy+ky)} L {f(xx)} {H}" stroke="{INK}" stroke-width="6"/>')
    for yy in (cy - HALF, cy + HALF):
        o.append(f'<path d="M 0 {f(yy)} L {f(cx-ky)} {f(yy)} M {f(cx+ky)} {f(yy)} L {W} {f(yy)}" stroke="{INK}" stroke-width="6"/>')
    for ang in (0, 90, 180, 270):
        p0, p1 = polar(ang, r_ext + 14), polar(ang, r_ext + 115)
        a = math.radians(ang)
        nx, ny = -math.sin(a), -math.cos(a)
        q = [(p0[0] + nx * 26, p0[1] + ny * 26), (p1[0] + nx * 8, p1[1] + ny * 8), (p1[0] - nx * 8, p1[1] - ny * 8), (p0[0] - nx * 26, p0[1] - ny * 26)]
        o.append(f'<path d="{smooth(q + [q[0]], False, 0.6)}" fill="#E4E7EE" stroke="{INK}" stroke-width="5"/>')
        o.append(f'<path d="{smooth([(p0[0]+nx*14, p0[1]+ny*14), (p1[0], p1[1])])}" stroke="#7FD06E" stroke-width="9" stroke-linecap="round" fill="none"/>')
    e = r_ext + 115
    o.append(f'<path d="M {f(cx)} 0 L {f(cx)} {f(cy-e)} M {f(cx)} {f(cy+e)} L {f(cx)} {H} M 0 {f(cy)} L {f(cx-e)} {f(cy)} M {f(cx+e)} {f(cy)} L {W} {f(cy)}" stroke="#F5F5F0" stroke-width="6" stroke-dasharray="40 30"/>')
    o.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(R_MID)}" fill="none" stroke="#F5F5F0" stroke-width="6" stroke-dasharray="34 26"/>')
    for ang in (0, 90, 180, 270):
        a = math.radians(ang)
        ux, uy = math.cos(a), -math.sin(a)
        nx, ny = -math.sin(a), -math.cos(a)
        c = (cx + ux * (r_ext + 8), cy + uy * (r_ext + 8))
        o.append(f'<path d="M {f(c[0]+nx*30)} {f(c[1]+ny*30)} L {f(c[0]+nx*(HALF-6))} {f(c[1]+ny*(HALF-6))}" stroke="#F5F5F0" stroke-width="9" stroke-dasharray="18 12"/>')
        tc = (cx + ux * (r_ext + 175) + nx * LANE, cy + uy * (r_ext + 175) + ny * LANE)
        tip = (tc[0] + ux * 34, tc[1] + uy * 34)
        bl = (tc[0] - ux * 30 - nx * 22, tc[1] - uy * 30 - ny * 22)
        br = (tc[0] - ux * 30 + nx * 22, tc[1] - uy * 30 + ny * 22)
        o.append(f'<path d="M {f(tip[0])} {f(tip[1])} L {f(bl[0])} {f(bl[1])} L {f(br[0])} {f(br[1])} Z" fill="none" stroke="#F5F5F0" stroke-width="7" stroke-linejoin="round"/>')
        for k in range(-5, 6):
            c2 = (cx + ux * (r_ext + 290) + nx * k * 23, cy + uy * (r_ext + 290) + ny * k * 23)
            o.append(f'<path d="M {f(c2[0]-ux*24)} {f(c2[1]-uy*24)} L {f(c2[0]+ux*24)} {f(c2[1]+uy*24)}" stroke="#F5F5F0" stroke-width="12"/>')
    o.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r_isla+12)}" fill="#E4E7EE" stroke="{INK}" stroke-width="6"/>')
    o.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r_isla)}" fill="url(#grassR)" stroke="{INK}" stroke-width="4"/>')
    o.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r_isla-28)}" fill="none" stroke="#B8F5B0" stroke-width="4" stroke-dasharray="10 14" opacity="0.7"/>')
    k = r_isla / 140
    for (dx, dy, r_) in [(-52, -40, 30), (48, -52, 26), (-30, 58, 28), (60, 40, 30), (0, 0, 38)]:
        o.append(arbol_aereo(cx + dx * k, cy + dy * k, r_ * k))
    return "\n".join(o)


def carriles_rotonda(cx=540, cy=880, r_isla=140, r_ext=330):
    """Radios de los carriles interior y exterior del anillo (para colocar coches con coche_aereo)."""
    r_mid = (r_isla + r_ext) / 2
    return {"interior": (r_isla + r_mid) / 2 + 0, "exterior": (r_mid + r_ext) / 2}


def punto_en_anillo(cx, cy, r, ang):
    """(x, y, rumbo) de un coche que circula en sentido antihorario por el anillo a `ang` grados (0 = este)."""
    a = math.radians(ang)
    return cx + r * math.cos(a), cy - r * math.sin(a), -ang

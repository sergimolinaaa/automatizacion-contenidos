"""Propulsión y «coches que vuelan»: deportivo eléctrico de perfil con toberas (abajo o atrás), chorro de aire comprimido,
depósito de aire con manómetro, rampa curva, avión de perfil, globo de aire que se escapa, extintor, pesa de «menos peso»,
logotipo de Tesla simplificado (estilo pegatina, sin imágenes externas) y fondo de pista de pruebas al atardecer.

Sale de: lote7-10-tesla-vuela (acción y reacción: el aire sale hacia abajo y el coche sube).
"""
import math
from ..base import (INK, LIME, CORAL, YEL, f, g, gt, T, MONO, DISP, shade, trazo, sombra, brillo, brillo_arco,
                    lg, rg, registrar_defs, degradado, pegatina, Pieza)

registrar_defs(
    lg("rsRojo", [(0, "#FF6A55"), (0.5, "#E31937"), (1, "#9C0F22")])
    + lg("rsBlanco", [(0, "#FFFFFF"), (1, "#C9D2E2")])
    + lg("rsNegro", [(0, "#4A5163"), (1, "#151821")])
    + lg("rsCristal", [(0, "#E4F6FF", 0.95), (1, "#6FA6D6", 0.9)])
    + rg("rsLlanta", [(0, "#FFFFFF"), (0.55, "#BFC7D6"), (1, "#6E7890")], 0.4, 0.35, 0.7)
    + lg("rsChorro", [(0, "#FFFFFF", 0.95), (0.6, "#CDEFFF", 0.75), (1, "#9ED8FF", 0)])
    + lg("rsTanque", [(0, "#F2F5FA"), (0.45, "#B9C3D3"), (1, "#7C879C")])
    + lg("rsRampa", [(0, "#8E99AE"), (1, "#4D566B")])
    + lg("rsCieloT", [(0, "#3B2E7E"), (0.45, "#C2508A"), (0.8, "#FF9A5A"), (1, "#FFC872")])
    + lg("rsArena", [(0, "#E8B57A"), (1, "#C98A4E")])
    + lg("rsMesa", [(0, "#B4605A"), (1, "#7E3A44")])
    + lg("rsAvion", [(0, "#FFFFFF"), (1, "#C3CCDD")])
    + lg("rsGlobo", [(0, "#FF8C6E"), (1, "#D63A1E")])
    + lg("rsPesa", [(0, "#6C768C"), (1, "#2E3445")])
)

TESLA_ROJO = "#E31937"
COLORES = {"rojo": "url(#rsRojo)", "blanco": "url(#rsBlanco)", "negro": "url(#rsNegro)"}


def logo_tesla(id_, cx, cy, r=70, fondo=TESLA_ROJO, col="#FFFFFF", borde=True):
    """Logotipo de Tesla simplificado: «T» con el arco de arriba, en un disco tipo pegatina (troquel blanco)."""
    k = r / 60

    def P(x, y):
        return f"{f(cx + x * k)} {f(cy + y * k)}"
    o = ""
    if borde:
        o += f'<circle cx="{f(cx+5*k)}" cy="{f(cy+7*k)}" r="{f(r+8*k)}" fill="{INK}" opacity="0.25"/>'
        o += f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r+8*k)}" fill="#FFFFFF" stroke="{INK}" stroke-width="{f(6*k)}"/>'
    o += f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{fondo}" stroke="{INK}" stroke-width="{f(5*k)}"/>'
    o += f'<path d="M {P(-36, -30)} Q {P(0, -46)} {P(36, -30)} L {P(34, -25)} Q {P(0, -38)} {P(-34, -25)} Z" fill="{col}"/>'
    o += (f'<path d="M {P(-32, -19)} Q {P(0, -33)} {P(32, -19)} L {P(29, -13)} Q {P(16, -18)} {P(8, -16)} L {P(4, -11)} '
          f'L {P(4, 38)} L {P(0, 42)} L {P(-4, 38)} L {P(-4, -11)} L {P(-8, -16)} Q {P(-16, -18)} {P(-29, -13)} Z" fill="{col}"/>')
    o += brillo_arco(cx, cy, r * 0.86, 200, 250, max(3, r * 0.07), 0.5)
    return g(id_, o)


def _rueda(cx, cy, r):
    o = f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="url(#rsNegro)" stroke="{INK}" stroke-width="7"/>'
    o += f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r*0.6)}" fill="url(#rsLlanta)" stroke="{INK}" stroke-width="5"/>'
    for a in range(0, 360, 72):
        x, y = cx + r * 0.5 * math.cos(math.radians(a)), cy + r * 0.5 * math.sin(math.radians(a))
        o += f'<path d="M {f(cx)} {f(cy)} L {f(x)} {f(y)}" stroke="#7E889C" stroke-width="{f(r*0.12)}" stroke-linecap="round"/>'
    o += f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r*0.16)}" fill="#E4E8F0" stroke="{INK}" stroke-width="4"/>'
    return o


def roadster(id_, cx, base, s=1.0, col="rojo", toberas=None, logo=True, rot_=0, espejo=False):
    """Deportivo eléctrico biplaza de perfil (morro a la derecha). (cx, base) = centro entre ruedas a ras de suelo.
    toberas: None, "abajo" (3 boquillas en los bajos) o "atras" (boquilla trasera). rot_ gira el coche sobre su centro.
    Ids: {id}_ruedas, {id}_faro. .puntos: toberas (lista de (x, y) de cada boquilla), centro, morro, cola. Largo ≈ 540*s."""
    o = sombra(0, 2, 250, 16, 0.2) if rot_ == 0 else ""
    fill = COLORES.get(col, col)
    body = ("M -258 -58 L -266 -96 Q -262 -126 -226 -134 L -122 -144 Q -62 -210 8 -206 Q 72 -202 124 -152 "
            "L 232 -122 Q 266 -112 266 -84 L 262 -60 Q 258 -46 240 -46 L -240 -46 Q -256 -46 -258 -58 Z")
    for x in (-165, 165):  # pasos de rueda
        o += f'<circle cx="{x}" cy="-52" r="64" fill="{INK}"/>'
    o += pegatina(body, fill, 8)
    o += f'<path d="M -98 -146 Q -50 -194 8 -192 Q 62 -190 102 -152 Z" fill="url(#rsCristal)" stroke="{INK}" stroke-width="6"/>'
    o += f'<path d="M -2 -192 L 4 -148" stroke="{INK}" stroke-width="7"/>'
    o += brillo("M -70 -160 Q -40 -184 -10 -184", 5, 0.8)
    o += f'<path d="M -30 -140 L -24 -66 M 112 -140 Q 118 -100 108 -66" fill="none" stroke="{shade("#E31937", -0.45)}" stroke-width="4" opacity="0.7"/>'
    o += brillo("M -228 -122 L -120 -132 M 128 -138 L 228 -112", 6, 0.55)
    o += f'<path d="M -226 -78 L 228 -78" stroke="#FFFFFF" stroke-width="4" opacity="0.25"/>'
    o += g(f"{id_}_faro", f'<path d="M 232 -106 Q 256 -102 260 -88 L 236 -90 Z" fill="#FFF6C8" stroke="{INK}" stroke-width="4"/>')
    o += f'<path d="M -262 -100 L -244 -104 L -244 -86 L -262 -84 Z" fill="#FF3A2A" stroke="{INK}" stroke-width="4"/>'
    o += f'<rect x="30" y="-108" width="34" height="6" rx="3" fill="{INK}" opacity="0.7"/>'
    if logo:
        o += logo_tesla(None, 196, -96, 13, borde=False)
    toberas_pts = []
    if toberas == "abajo":
        for x in (-110, 0, 110):
            o += f'<path d="M {x-20} -46 L {x+20} -46 L {x+14} -30 L {x-14} -30 Z" fill="url(#rsTanque)" stroke="{INK}" stroke-width="5"/>'
            toberas_pts.append((x, -30))
    elif toberas == "atras":
        o += f'<path d="M -262 -82 L -262 -58 L -284 -54 L -284 -86 Z" fill="url(#rsTanque)" stroke="{INK}" stroke-width="5"/>'
        toberas_pts.append((-284, -70))
    o += g(f"{id_}_ruedas", _rueda(-165, -52, 50) + _rueda(165, -52, 50))
    sx = -s if espejo else s
    cyc = -110 * s  # centro del coche (para girarlo)
    tr = f"translate({f(cx)} {f(base)}) rotate({f(rot_)} 0 {f(cyc)}) scale({f(sx)} {f(s)})"
    c, sn = math.cos(math.radians(rot_)), math.sin(math.radians(rot_))

    def P(p):
        x, y = p[0] * sx, p[1] * s - cyc
        return (cx + x * c - y * sn, base + x * sn + y * c + cyc)
    pts_ = {"toberas": [P(t) for t in toberas_pts], "centro": P((0, -110)), "morro": P((266, -84)), "cola": P((-266, -96))}
    return Pieza(gt(id_, tr, o), pts_, (cx - 270 * s, base - 210 * s, cx + 270 * s, base))


def chorro(id_, x, y, largo=220, ancho=90, ang=90, soplos=3):
    """Chorro de aire comprimido que sale de una boquilla en (x, y) hacia el ángulo ang (90 = hacia abajo, 180 = izquierda).
    Cono blanco translúcido + bocanadas + líneas de flujo (ids {id}_lineas para «flow», {id}_soplos para «pulse»)."""
    L, W = largo, ancho
    o = f'<path d="M -12 0 L 12 0 L {f(W/2)} {f(L)} Q 0 {f(L*1.12)} {f(-W/2)} {f(L)} Z" fill="url(#rsChorro)" stroke="#FFFFFF" stroke-width="3" opacity="0.95"/>'
    lin = ""
    for dx in (-0.22, 0, 0.22):
        lin += f'<path d="M {f(dx*14)} 8 L {f(dx*W)} {f(L*0.92)}" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round" stroke-dasharray="0.08 0.05" opacity="0.9"/>'
    o += g(f"{id_}_lineas" if id_ else None, lin)
    so = ""
    for i in range(soplos):
        t = (i + 1) / (soplos + 1)
        r = W * (0.18 + 0.12 * t)
        xx = (W * 0.32) * (1 if i % 2 else -1) * t
        so += f'<circle cx="{f(xx)}" cy="{f(L*(0.55+0.45*t))}" r="{f(r)}" fill="#FFFFFF" stroke="#BFE6FF" stroke-width="4" opacity="0.85"/>'
    o += g(f"{id_}_soplos" if id_ else None, so)
    return gt(id_, f"translate({f(x)} {f(y)}) rotate({f(ang-90)})", o)


def deposito_aire(id_, cx, cy, w=300, h=120, nivel=1.0, texto="AIRE", seed=3):
    """Bombona horizontal de aire comprimido con manómetro arriba; la ventana muestra moléculas (muchas si nivel=1,
    pocas si 0). Ids {id}_moleculas (shake = apretadas), {id}_aguja (manómetro: lleno a la derecha, vacío a la izquierda)."""
    import random
    rnd = random.Random(seed)
    x, y = cx - w / 2, cy - h / 2
    o = f'<rect x="{f(x+8)}" y="{f(y+10)}" width="{f(w)}" height="{f(h)}" rx="{f(h/2)}" fill="{INK}" opacity="0.22"/>'
    o += f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{f(h/2)}" fill="url(#rsTanque)" stroke="{INK}" stroke-width="7"/>'
    o += brillo(f"M {f(x+h*0.45)} {f(y+h*0.2)} L {f(x+w-h*0.45)} {f(y+h*0.2)}", 7, 0.8)
    wx, ww, wy, wh = x + h * 0.45, w - h * 0.9, cy - h * 0.2, h * 0.5
    o += f'<rect x="{f(wx)}" y="{f(wy)}" width="{f(ww)}" height="{f(wh)}" rx="10" fill="#E9F7FF" stroke="{INK}" stroke-width="5"/>'
    n = int(4 + 34 * nivel)
    mol = "".join(f'<circle cx="{f(rnd.uniform(wx+8, wx+ww-8))}" cy="{f(rnd.uniform(wy+8, wy+wh-8))}" r="6" fill="#3FA9F5" stroke="{INK}" stroke-width="2"/>' for _ in range(n))
    o += g(f"{id_}_moleculas", mol)
    o += T(cx, y + h + 44, texto, 32, "#FFFFFF", font=DISP, extra='stroke="#0B0B14" stroke-width="8" paint-order="stroke"') if texto else ""
    mx, my, mr = x + w - h * 0.6, y - 30, 34
    o += f'<rect x="{f(mx-6)}" y="{f(my+20)}" width="12" height="22" fill="#9AA3B5" stroke="{INK}" stroke-width="4"/>'
    o += f'<circle cx="{f(mx)}" cy="{f(my)}" r="{mr}" fill="#FFFFFF" stroke="{INK}" stroke-width="6"/>'
    o += f'<path d="M {f(mx-mr*0.7)} {f(my+mr*0.2)} A {f(mr*0.72)} {f(mr*0.72)} 0 0 1 {f(mx+mr*0.7)} {f(my+mr*0.2)}" fill="none" stroke="{LIME}" stroke-width="7"/>'
    a = math.radians(200 + 140 * nivel)
    o += g(f"{id_}_aguja", f'<path d="M {f(mx)} {f(my)} L {f(mx+mr*0.75*math.cos(a))} {f(my+mr*0.75*math.sin(a))}" stroke="{CORAL}" stroke-width="6" stroke-linecap="round"/>'
           f'<circle cx="{f(mx)}" cy="{f(my)}" r="6" fill="{INK}"/>')
    return Pieza(g(id_, o), {"boquilla": (x + w, cy), "manometro": (mx, my)}, (x, my - mr, x + w, y + h + 50))


def rampa(id_, x0, x1, base, alto=260, col="url(#rsRampa)"):
    """Rampa curva tipo trampolín: sube de x0 (a ras de suelo) a x1 (altura alto), con patas. .puntos: borde (salida)."""
    w = x1 - x0
    top = (f"M {f(x0)} {f(base)} Q {f(x0+w*0.75)} {f(base)} {f(x1)} {f(base-alto)} L {f(x1+18)} {f(base-alto+10)} "
           f"L {f(x1+18)} {f(base)} Z")
    o = sombra((x0 + x1) / 2, base + 4, w * 0.6, 14, 0.2)
    for t in (0.45, 0.7, 0.9):
        xx = x0 + w * t
        yy = base - alto * (t ** 2.2)
        o += f'<path d="M {f(xx)} {f(yy)} L {f(xx)} {f(base)}" stroke="{INK}" stroke-width="16"/><path d="M {f(xx)} {f(yy)} L {f(xx)} {f(base)}" stroke="#9AA3B5" stroke-width="8"/>'
    o += pegatina(top, col, 7)
    o += brillo(f"M {f(x0+w*0.25)} {f(base-6)} Q {f(x0+w*0.72)} {f(base-8)} {f(x1-6)} {f(base-alto+12)}", 6, 0.6)
    for t in (0.3, 0.55, 0.8):
        xx = x0 + w * t
        o += f'<path d="M {f(xx-14)} {f(base - alto*(t**2.2) - 4)} l 28 0" stroke="{YEL}" stroke-width="6" stroke-linecap="round"/>'
    return Pieza(g(id_, o), {"borde": (x1, base - alto)}, (x0, base - alto, x1 + 18, base))


def avion(id_, cx, cy, s=1.0):
    """Avión de pasajeros de perfil (morro a la derecha) con el ala bien visible. Ids {id}_ala."""
    o = pegatina("M -230 -10 Q -236 -40 -200 -40 L 160 -40 Q 230 -36 240 0 Q 230 30 160 34 L -200 34 Q -236 30 -230 -10 Z", "url(#rsAvion)", 7)
    o += pegatina("M -190 -40 L -240 -130 L -196 -130 L -130 -40 Z", "url(#rsAvion)", 7)
    for i in range(7):
        o += f'<circle cx="{-120 + i * 38}" cy="-12" r="9" fill="url(#rsCristal)" stroke="{INK}" stroke-width="3"/>'
    o += f'<path d="M 170 -30 Q 205 -28 222 -12 L 180 -12 Z" fill="url(#rsCristal)" stroke="{INK}" stroke-width="4"/>'
    o += g(f"{id_}_ala", pegatina("M -40 14 L 70 14 L -10 120 L -70 120 Z", "#2EC4B6", 7)
           + brillo("M -30 24 L 50 24", 5, 0.6))
    o += brillo("M -190 -28 L 150 -28", 6, 0.7)
    return gt(id_, f"translate({f(cx)} {f(cy)}) scale({f(s)})", o)


def globo_aire(id_, cx, cy, r=90, col="url(#rsGlobo)", ang=0):
    """Globo de goma visto de lado, con la boquilla abierta (por donde se escapa el aire). ang: inclinación.
    .puntos: boquilla."""
    o = f'<ellipse cx="0" cy="0" rx="{f(r*0.82)}" ry="{f(r)}" fill="{col}" stroke="{INK}" stroke-width="7"/>'
    o += brillo_arco(0, 0, r * 0.72, 200, 250, r * 0.1, 0.8)
    o += f'<path d="M -12 {f(r-4)} L 12 {f(r-4)} L 8 {f(r+18)} L -8 {f(r+18)} Z" fill="#D63A1E" stroke="{INK}" stroke-width="5"/>'
    c, s_ = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    bx, by = -(r + 18) * s_, (r + 18) * c
    return Pieza(gt(id_, f"translate({f(cx)} {f(cy)}) rotate({f(ang)})", o), {"boquilla": (cx + bx, cy + by)}, (cx - r, cy - r, cx + r, cy + r + 20))


def extintor(id_, cx, base, h=260, ang_manguera=0):
    """Extintor rojo de pie con manguera y boquilla (a la derecha). .puntos: boquilla."""
    w = h * 0.36
    o = sombra(cx, base + 2, w * 0.7, 10, 0.2)
    o += pegatina(f"M {f(cx-w/2)} {f(base)} L {f(cx-w/2)} {f(base-h*0.78)} Q {f(cx-w/2)} {f(base-h*0.9)} {f(cx)} {f(base-h*0.9)} Q {f(cx+w/2)} {f(base-h*0.9)} {f(cx+w/2)} {f(base-h*0.78)} L {f(cx+w/2)} {f(base)} Z", "url(#rsGlobo)", 7)
    o += f'<rect x="{f(cx-w*0.32)}" y="{f(base-h*0.6)}" width="{f(w*0.64)}" height="{f(h*0.24)}" rx="6" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/>'
    o += brillo(f"M {f(cx-w*0.3)} {f(base-h*0.75)} L {f(cx-w*0.3)} {f(base-h*0.1)}", 6, 0.6)
    o += f'<rect x="{f(cx-12)}" y="{f(base-h)}" width="24" height="{f(h*0.12)}" fill="#3A4256" stroke="{INK}" stroke-width="5"/>'
    bx, by = cx + w * 1.1, base - h * 0.96
    o += trazo(f"M {f(cx+8)} {f(base-h*0.95)} Q {f(cx+w*0.6)} {f(base-h*1.05)} {f(bx)} {f(by)}", 12, INK, 5)
    o += f'<path d="M {f(bx-4)} {f(by-12)} L {f(bx+30)} {f(by-8)} L {f(bx+30)} {f(by+8)} L {f(bx-4)} {f(by+12)} Z" fill="#3A4256" stroke="{INK}" stroke-width="5"/>'
    return Pieza(g(id_, o), {"boquilla": (bx + 30, by)}, (cx - w / 2, base - h, bx + 30, base))


def pesa(id_, cx, base, w=170, texto="KG"):
    """Pesa de gimnasio/báscula (trapecio con asa) para hablar de peso."""
    h = w * 0.7
    o = sombra(cx, base + 2, w * 0.6, 10, 0.2)
    o += f'<path d="M {f(cx-w*0.22)} {f(base-h)} Q {f(cx)} {f(base-h*1.55)} {f(cx+w*0.22)} {f(base-h)}" fill="none" stroke="{INK}" stroke-width="26"/>'
    o += f'<path d="M {f(cx-w*0.22)} {f(base-h)} Q {f(cx)} {f(base-h*1.55)} {f(cx+w*0.22)} {f(base-h)}" fill="none" stroke="#6C768C" stroke-width="13"/>'
    o += pegatina(f"M {f(cx-w*0.32)} {f(base-h)} L {f(cx+w*0.32)} {f(base-h)} L {f(cx+w/2)} {f(base)} L {f(cx-w/2)} {f(base)} Z", "url(#rsPesa)", 7)
    o += T(cx, base - h * 0.3, texto, w * 0.2, "#FFFFFF", font=DISP)
    o += brillo(f"M {f(cx-w*0.24)} {f(base-h*0.86)} L {f(cx+w*0.1)} {f(base-h*0.86)}", 5, 0.5)
    return g(id_, o)


def pista_pruebas(W=1080, H=1920, suelo_y=1200):
    """Fondo: cielo de atardecer, mesetas lejanas de desierto, arena y una franja de asfalto con línea discontinua."""
    o = f'<rect width="{W}" height="{H}" fill="url(#rsCieloT)"/>'
    o += f'<circle cx="{f(W*0.74)}" cy="{f(suelo_y-260)}" r="{f(W*0.11)}" fill="#FFE9A8" opacity="0.9"/>'
    o += (f'<path d="M 0 {f(suelo_y-150)} L {f(W*0.08)} {f(suelo_y-150)} L {f(W*0.12)} {f(suelo_y-230)} L {f(W*0.3)} {f(suelo_y-230)} '
          f'L {f(W*0.34)} {f(suelo_y-150)} L {f(W*0.58)} {f(suelo_y-150)} L {f(W*0.62)} {f(suelo_y-200)} L {f(W*0.82)} {f(suelo_y-200)} '
          f'L {f(W*0.86)} {f(suelo_y-150)} L {W} {f(suelo_y-150)} L {W} {H} L 0 {H} Z" fill="url(#rsMesa)" opacity="0.85"/>')
    o += f'<rect x="0" y="{f(suelo_y-150)}" width="{W}" height="{f(H)}" fill="url(#rsArena)"/>'
    o += f'<path d="M 0 {f(suelo_y-150)} L {W} {f(suelo_y-150)}" stroke="{INK}" stroke-width="6" opacity="0.5"/>'
    o += f'<rect x="0" y="{f(suelo_y-40)}" width="{W}" height="140" fill="#4A5163" stroke="{INK}" stroke-width="7"/>'
    o += "".join(f'<rect x="{x}" y="{f(suelo_y+24)}" width="70" height="12" rx="6" fill="#FFFFFF" opacity="0.8"/>' for x in range(20, W, 140))
    for i, x in enumerate((90, 330, 860, 1010)):
        yy = suelo_y - 110 + (i % 2) * 20
        o += f'<path d="M {x} {yy} q 10 -40 0 -70 m 0 30 q -20 -6 -22 -26 m 22 10 q 18 -4 20 -22" fill="none" stroke="#3E7A4A" stroke-width="10" stroke-linecap="round"/>'
    return o

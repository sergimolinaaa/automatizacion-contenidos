"""Coches deportivos y física del giro: deportivo de perfil EN CORTE (motor delante, en medio o detrás, piloto,
ruedas que giran), deportivo visto desde arriba con el motor a la vista, bloque de motor, símbolo de centro de gravedad,
escudo de Porsche simplificado (estilo pegatina, sin imágenes externas), maleta, marcas de derrape, persona vista desde
arriba (brazos estirados con bolsas o pegados), pista de hielo y fondos (sala de presentación, carretera).

Sale de: lote7-09-motor-central (por qué los superdeportivos llevan el motor en medio).
"""
import math
from ..base import (INK, LIME, CORAL, YEL, TEAL, VIO, f, g, gt, T, MONO, DISP, shade, trazo, sombra, brillo,
                    lg, rg, registrar_defs, degradado, Pieza)

registrar_defs(
    lg("cocheRojo", [(0, "#FF7A5C"), (0.55, "#E8341C"), (1, "#A51C0C")])
    + lg("cocheInterior", [(0, "#F4F6FB"), (1, "#C9D1E0")])
    + lg("motorG", [(0, "#C9D0DC"), (1, "#6B7488")])
    + lg("motorTapa", [(0, "#FF6B4A"), (1, "#B8240F")])
    + lg("neumaticoG", [(0, "#3A3F4E"), (1, "#14161E")])
    + rg("llantaG", [(0, "#FFFFFF"), (0.6, "#C3CAD8"), (1, "#7E889C")], 0.4, 0.35, 0.7)
    + lg("cristalCoche", [(0, "#DFF4FF", 0.85), (1, "#7FB7DD", 0.75)])
    + lg("oroEscudo", [(0, "#FFE07A"), (1, "#D99A00")])
    + lg("rojoEscudo", [(0, "#F0412B"), (1, "#B3160B")])
    + lg("salaFondo", [(0, "#1B1F33"), (1, "#2E3552")])
    + lg("salaSuelo", [(0, "#3B4366"), (1, "#151829")])
    + rg("focoSala", [(0, "#FFFFFF", 0.55), (1, "#FFFFFF", 0)])
    + lg("asfaltoG", [(0, "#5A6070"), (1, "#3C414E")])
    + lg("hieloG", [(0, "#F2FBFF"), (1, "#BFE3F5")])
    + lg("maletaG", [(0, "#FFD95A"), (1, "#E09A00")])
)

COLORES = {"rojo": "url(#cocheRojo)", "amarillo": "url(#amarilloG)", "lima": "url(#limaG)"}


# ------------------------------------------------------------------ piezas sueltas
def centro_gravedad(id_, cx, cy, r=26):
    """Símbolo clásico de centro de gravedad (círculo a cuartos blanco y negro)."""
    o = f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r+5)}" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/>'
    o += f'<path d="M {f(cx)} {f(cy)} L {f(cx+r)} {f(cy)} A {f(r)} {f(r)} 0 0 0 {f(cx)} {f(cy-r)} Z" fill="{INK}"/>'
    o += f'<path d="M {f(cx)} {f(cy)} L {f(cx-r)} {f(cy)} A {f(r)} {f(r)} 0 0 0 {f(cx)} {f(cy+r)} Z" fill="{INK}"/>'
    return g(id_, o)


def motor_bloque(id_, cx, cy, w=150, h=90):
    """Bloque de motor visto de lado: cárter metálico, culata roja con aletas, colector y brillo."""
    x0, y0 = cx - w / 2, cy - h / 2
    o = f'<rect x="{f(x0)}" y="{f(y0 + h*0.32)}" width="{f(w)}" height="{f(h*0.68)}" rx="{f(h*0.12)}" fill="url(#motorG)" stroke="{INK}" stroke-width="5"/>'
    o += f'<rect x="{f(x0 + w*0.06)}" y="{f(y0)}" width="{f(w*0.88)}" height="{f(h*0.38)}" rx="{f(h*0.1)}" fill="url(#motorTapa)" stroke="{INK}" stroke-width="5"/>'
    for k in range(5):
        xx = x0 + w * (0.18 + k * 0.16)
        o += f'<line x1="{f(xx)}" y1="{f(y0 + h*0.08)}" x2="{f(xx)}" y2="{f(y0 + h*0.3)}" stroke="#7E1408" stroke-width="4" stroke-linecap="round"/>'
    for k in range(3):
        yy = y0 + h * (0.5 + k * 0.15)
        o += f'<line x1="{f(x0 + w*0.12)}" y1="{f(yy)}" x2="{f(x0 + w*0.88)}" y2="{f(yy)}" stroke="#56607A" stroke-width="3.5" opacity="0.8"/>'
    o += brillo(f"M {f(x0 + w*0.14)} {f(y0 + h*0.1)} L {f(x0 + w*0.5)} {f(y0 + h*0.1)}", 3.5, 0.7)
    return g(id_, o)


def _rueda(id_, cx, cy, r):
    o = f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="url(#neumaticoG)" stroke="{INK}" stroke-width="6"/>'
    o += f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r*0.62)}" fill="url(#llantaG)" stroke="{INK}" stroke-width="4"/>'
    for k in range(5):
        a = math.radians(k * 72 - 90)
        o += f'<line x1="{f(cx)}" y1="{f(cy)}" x2="{f(cx + r*0.56*math.cos(a))}" y2="{f(cy + r*0.56*math.sin(a))}" stroke="#6A7488" stroke-width="{f(r*0.13)}" stroke-linecap="round"/>'
    o += f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r*0.14)}" fill="{INK}"/>'
    return g(id_, o)


def escudo_porsche(id_, cx, cy, s=1.0):
    """Escudo de Porsche simplificado (pegatina): marco dorado, rótulo PORSCHE, cuarteles con franjas rojas y negras
    y astas negras, y escudo central dorado con caballo negro. Alto ≈ 240*s, ancho ≈ 200*s. (cx, cy) = centro."""
    W, H = 100, 120
    sh = (f"M {-W} {-H+18} Q 0 {-H-6} {W} {-H+18} L {W} -10 Q {W-6} {H*0.62} 0 {H} Q {-W+6} {H*0.62} {-W} -10 Z")
    o = f'<path d="{sh}" transform="translate(7 9)" fill="{INK}" opacity="0.25"/>'
    o += f'<path d="{sh}" fill="#FFFFFF" stroke="#FFFFFF" stroke-width="22" stroke-linejoin="round"/>'
    o += f'<path d="{sh}" fill="url(#oroEscudo)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
    o += T(0, -H + 42, "PORSCHE", 25, INK, font=DISP)
    # campo interior
    cid = f"{id_}_campo"
    inner = f"M {-W+14} -62 L {W-14} -62 L {W-14} -12 Q {W-20} {H*0.55} 0 {H-16} Q {-W+20} {H*0.55} {-W+14} -12 Z"
    o += f'<clipPath id="{cid}"><path d="{inner}"/></clipPath>'
    q = f'<rect x="-120" y="-80" width="240" height="220" fill="url(#oroEscudo)"/>'
    # cuarteles con franjas (arriba izquierda y abajo derecha)
    for (x0, y0) in ((-W, -62), (0, 28)):
        for k in range(4):
            col = "url(#rojoEscudo)" if k % 2 == 0 else INK
            q += f'<rect x="{x0}" y="{f(y0 + k*22.5)}" width="{W}" height="22.5" fill="{col}"/>'
    # astas de ciervo (arriba derecha y abajo izquierda): 3 por cuartel, viga curva que adelgaza y 4 puntas hacia arriba
    for (ax, ay) in ((50, -24), (-50, 66)):
        for k in (-1, 0, 1):
            yy = ay + k * 24
            q += (f'<path d="M {ax-38} {yy+9} Q {ax-6} {yy-6} {ax+38} {yy+1} L {ax+38} {yy+5} '
                  f'Q {ax-6} {yy} {ax-38} {yy+13} Z" fill="{INK}"/>')
            for j, h in ((-24, 11), (-9, 13), (6, 13), (21, 11)):
                bx, by = ax + j, yy + (2 if j < 0 else 0)
                q += (f'<path d="M {bx-3} {by} Q {bx-1} {by-h*0.6} {bx+4} {by-h} Q {bx+2} {by-h*0.5} {bx+3} {by} Z" '
                      f'fill="{INK}"/>')
    o += f'<g clip-path="url(#{cid})">{q}</g>'
    o += f'<path d="{inner}" fill="none" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    o += f'<line x1="0" y1="-62" x2="0" y2="{H-16}" stroke="{INK}" stroke-width="4"/><line x1="{-W+14}" y1="28" x2="{W-14}" y2="28" stroke="{INK}" stroke-width="4"/>'
    # escudo central (escudo de Stuttgart): rótulo STUTTGART y caballo negro encabritado mirando a la izquierda
    cs = "M -40 -16 L 40 -16 L 40 28 Q 36 66 0 82 Q -36 66 -40 28 Z"
    o += f'<path d="{cs}" fill="url(#oroEscudo)" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    o += T(0, -4, "STUTTGART", 9.5, INK, font=DISP, extra='letter-spacing="0.6"')
    horse = ("M 6 32 Q 8 20 18 11 L 22 0 L 28 6 L 31 4 L 32 10 Q 42 12 47 24 Q 50 32 56 36 Q 68 42 74 54 Q 84 44 96 50 "
             "Q 100 60 92 72 Q 90 62 80 64 Q 84 80 80 90 L 84 108 L 88 116 L 76 116 L 74 100 L 68 90 L 64 102 "
             "L 62 116 L 52 116 L 54 102 L 56 86 Q 50 76 42 70 L 30 70 L 22 76 L 20 86 L 13 86 L 15 78 L 22 68 "
             "L 32 64 L 34 58 L 24 56 L 16 60 L 10 70 L 5 68 L 9 56 L 18 50 L 30 48 Q 32 40 30 32 "
             "Q 26 34 14 37 Q 7 37 6 32 Z")
    o += (f'<path d="{horse}" transform="translate(-28 4) scale(0.56)" fill="{INK}" stroke="{INK}" stroke-width="2.5" '
          f'stroke-linejoin="round"/>')
    o += brillo(f"M {-W+16} {-H+30} Q -40 {-H+12} 0 {-H+10}", 5, 0.75)
    return gt(id_, f"translate({f(cx)} {f(cy)}) scale({f(s)})", o)


# ------------------------------------------------------------------ deportivo de perfil en corte
_EJE_DEL, _EJE_TRAS, _R = -300, 290, 66
_CUERPO = ("M -458 -60 Q -462 -92 -422 -102 L -205 -140 Q -160 -148 -118 -186 Q -66 -226 40 -226 "
           "Q 160 -222 300 -168 L 440 -146 Q 464 -140 464 -110 L 462 -62 Q 460 -40 436 -40 L 370 -40 "
           "A 84 84 0 1 0 210 -40 L -220 -40 A 84 84 0 1 0 -380 -40 L -432 -40 Q -458 -40 -458 -60 Z")
_VENTANA = "M -112 -176 Q -64 -212 34 -212 L 150 -206 Q 200 -198 236 -178 Z"


def deportivo_lateral(id_, cx, base, s=1.0, col="rojo", motor="centro", corte=True, logo=False, piloto=True, aleron=True):
    """Superdeportivo genérico de perfil (mira a la IZQUIERDA), largo ≈ 920*s, alto ≈ 230*s. (cx, base) = centro y suelo.
    motor: 'centro' (entre el piloto y el eje trasero), 'delante' (sobre el eje delantero) o 'detras' (tras el eje trasero, como el 911).
    corte=True muestra el interior en rayos X (piloto, asiento y motor). logo=True pega el escudo de Porsche en el morro.
    Sub-ids: {id}_carroceria, {id}_motor, {id}_piloto, {id}_rueda_del, {id}_rueda_tras (spin), {id}_cg.
    .puntos: eje_del, eje_tras, motor, cg, piloto, morro, cola, techo, maletero (en coordenadas finales)."""
    c = COLORES.get(col, col)
    mx = {"centro": 150, "delante": -300, "detras": 375}[motor]
    my = -92 if motor != "delante" else -80
    mw = {"centro": 170, "delante": 120, "detras": 125}[motor]
    mh = 92 if motor != "delante" else 70
    cgx = {"centro": 62, "delante": -160, "detras": 140}[motor]
    o = sombra(0, 4, 470, 22, 0.28)
    carr = f'<path d="{_CUERPO}" fill="{c}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'
    carr += brillo("M -420 -96 L -215 -132", 6, 0.7) + brillo("M -40 -218 Q 120 -216 250 -184", 5, 0.55)
    carr += f'<path d="M -440 -70 L 440 -70" stroke="{shade("#E8341C", -0.35)}" stroke-width="4" opacity="0.5"/>'
    if aleron:
        carr += f'<path d="M 360 -160 L 372 -184 L 456 -190 L 452 -176 Z" fill="{c}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    # faro y piloto trasero
    carr += f'<path d="M -446 -84 Q -430 -98 -396 -100 L -400 -86 Z" fill="#FFF6C2" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
    carr += f'<rect x="446" y="-132" width="16" height="22" rx="5" fill="#FF3B30" stroke="{INK}" stroke-width="4"/>'
    o += g(f"{id_}_carroceria", carr)
    inner = ""
    if corte:
        clip = f"{id_}_clip"
        x0c, x1c = (-440, 110) if motor == "delante" else (-215, 452)
        inner += f'<clipPath id="{clip}"><rect x="{x0c}" y="-260" width="{x1c-x0c}" height="260"/></clipPath>'
        xr = f'<path d="{_CUERPO}" transform="translate(0 -112) scale(0.965 0.88) translate(0 112)" fill="url(#cocheInterior)" stroke="{INK}" stroke-width="4" stroke-dasharray="14 10"/>'
        inner += f'<g clip-path="url(#{clip})">{xr}</g>'
    o += inner
    o += f'<path d="{_VENTANA}" fill="url(#cristalCoche)" stroke="{INK}" stroke-width="5" stroke-linejoin="round" opacity="{0.55 if corte else 1}"/>'
    if piloto:
        p = ""
        p += f'<path d="M 30 -60 L 44 -170 Q 46 -184 34 -186 L 22 -186 Q 12 -184 10 -172 L 2 -64 Z" fill="#2B3A5C" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
        p += f'<path d="M 4 -64 L -96 -62 Q -110 -62 -108 -76 L -100 -86 L 2 -90 Z" fill="#2B3A5C" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
        p += f'<path d="M 18 -150 Q -10 -152 -24 -120 L -14 -84 L 18 -84 Z" fill="#1FB5A8" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
        p += f'<path d="M -6 -130 Q -40 -124 -64 -126" fill="none" stroke="{INK}" stroke-width="16" stroke-linecap="round"/><path d="M -6 -130 Q -40 -124 -64 -126" fill="none" stroke="#1FB5A8" stroke-width="9" stroke-linecap="round"/>'
        p += f'<line x1="-74" y1="-104" x2="-60" y2="-150" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>'
        p += f'<circle cx="-2" cy="-172" r="26" fill="url(#oroEscudo)" stroke="{INK}" stroke-width="5"/>'
        p += f'<path d="M -28 -172 Q -26 -160 -8 -160 L -26 -178 Z" fill="#2B3A5C" stroke="{INK}" stroke-width="3"/>'
        p += brillo("M -16 -188 Q -6 -195 8 -192", 4, 0.8)
        o += g(f"{id_}_piloto", p)
    o += _rueda(f"{id_}_rueda_del", _EJE_DEL, -_R, _R) + _rueda(f"{id_}_rueda_tras", _EJE_TRAS, -_R, _R)
    if corte:  # en rayos X el motor se ve por encima de las ruedas
        o += motor_bloque(f"{id_}_motor", mx, my, mw, mh)
    if logo:
        o += escudo_porsche(None, -330, -112, 0.12)
    if corte:
        o += centro_gravedad(f"{id_}_cg", cgx, -96, 18)

    def P(x, y):
        return (cx + x * s, base + y * s)
    pts_ = {"eje_del": P(_EJE_DEL, -_R), "eje_tras": P(_EJE_TRAS, -_R), "motor": P(mx, my), "cg": P(cgx, -96),
            "piloto": P(-2, -172), "morro": P(-458, -80), "cola": P(462, -100), "techo": P(40, -226), "maletero": P(-380, -110)}
    return Pieza(gt(id_, f"translate({f(cx)} {f(base)}) scale({f(s)})", o), pts_, (cx - 470 * s, base - 236 * s, cx + 470 * s, base + 8 * s))


# ------------------------------------------------------------------ deportivo visto desde arriba
def deportivo_cenital(id_, cx, cy, s=1.0, col="rojo", motor="centro", cg=True, rumbo=0):
    """Deportivo desde arriba (morro hacia ARRIBA), largo ≈ 440*s, ancho ≈ 210*s, con el motor a la vista y el punto
    de centro de gravedad. motor: centro | delante | detras. Sub-ids {id}_motor, {id}_cg. .puntos: centro, motor, morro, cola."""
    c = COLORES.get(col, col)
    my = {"centro": 70, "delante": -130, "detras": 175}[motor]
    o = f'<rect x="-100" y="-212" width="210" height="440" rx="70" fill="{INK}" opacity="0.25"/>'
    for (wx, wy) in ((-104, -130), (104, -130), (-108, 130), (108, 130)):
        o += f'<rect x="{wx-20}" y="{wy-40}" width="40" height="80" rx="12" fill="url(#neumaticoG)" stroke="{INK}" stroke-width="5"/>'
    body = "M 0 -222 Q 92 -220 98 -150 L 104 -60 Q 112 0 108 80 L 106 170 Q 100 222 0 224 Q -100 222 -106 170 L -108 80 Q -112 0 -104 -60 L -98 -150 Q -92 -220 0 -222 Z"
    o += f'<path d="{body}" fill="{c}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
    o += f'<path d="M -70 -70 Q 0 -96 70 -70 L 60 -20 Q 0 -32 -60 -20 Z" fill="url(#cristalCoche)" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    o += f'<path d="M -60 -20 Q 0 -32 60 -20 L 58 20 Q 0 12 -58 20 Z" fill="{shade("#E8341C", -0.25)}" stroke="{INK}" stroke-width="4"/>'
    # cubierta de motor de cristal
    o += f'<rect x="-62" y="{my-48}" width="124" height="96" rx="18" fill="url(#cocheInterior)" stroke="{INK}" stroke-width="4" stroke-dasharray="10 7"/>'
    eng = f'<rect x="-46" y="{my-36}" width="92" height="72" rx="12" fill="url(#motorG)" stroke="{INK}" stroke-width="4"/>'
    for k in range(4):
        eng += f'<rect x="-34" y="{f(my-28 + k*16)}" width="68" height="10" rx="5" fill="url(#motorTapa)" stroke="{INK}" stroke-width="2.5"/>'
    o += g(f"{id_}_motor", eng)
    o += f'<ellipse cx="-58" cy="-206" rx="22" ry="8" fill="#FFF6C2" stroke="{INK}" stroke-width="3"/><ellipse cx="58" cy="-206" rx="22" ry="8" fill="#FFF6C2" stroke="{INK}" stroke-width="3"/>'
    o += f'<rect x="-70" y="212" width="40" height="9" rx="4" fill="#FF3B30" stroke="{INK}" stroke-width="3"/><rect x="30" y="212" width="40" height="9" rx="4" fill="#FF3B30" stroke="{INK}" stroke-width="3"/>'
    o += brillo("M -86 -150 L -90 60", 5, 0.55)
    if cg:
        o += centro_gravedad(f"{id_}_cg", 0, 30, 20)
    pts_ = {"centro": (cx, cy), "motor": (cx, cy + my * s), "morro": (cx, cy - 222 * s), "cola": (cx, cy + 224 * s)}
    tr = f"translate({f(cx)} {f(cy)}) rotate({f(rumbo)}) scale({f(s)})"
    return Pieza(gt(id_, tr, o), pts_, (cx - 130 * s, cy - 230 * s, cx + 130 * s, cy + 230 * s))


# ------------------------------------------------------------------ persona vista desde arriba
def persona_cenital(id_, cx, cy, s=1.0, brazos="estirados", bolsas=True, ropa="#7B5CFF", pelo="#4A2E1C", piel="#F1B48A"):
    """Persona vista desde arriba (mira hacia ABAJO de la pantalla, nariz visible). brazos: 'estirados' (en cruz, con
    bolsas en las manos) o 'pegados' (abrazándose el pecho). Ancho con brazos estirados ≈ 560*s. Sub-ids {id}_brazos."""
    o = f'<ellipse cx="6" cy="10" rx="{"260" if brazos == "estirados" else "92"}" ry="70" fill="{INK}" opacity="0.18"/>'
    arms = ""
    if brazos == "estirados":
        for k in (-1, 1):
            arms += trazo(f"M {k*70} 0 L {k*215} 4", 34, ropa, 8)
            arms += f'<circle cx="{k*228}" cy="4" r="20" fill="{piel}" stroke="{INK}" stroke-width="5"/>'
            if bolsas:
                bx = k * 250
                arms += f'<rect x="{bx-30}" y="-6" width="60" height="78" rx="10" transform="rotate({k*-8} {bx} 30)" fill="{degradado(CORAL if k < 0 else TEAL)}" stroke="{INK}" stroke-width="5"/>'
                arms += f'<path d="M {bx-14} 0 Q {bx} -18 {bx+14} 0" fill="none" stroke="{INK}" stroke-width="4"/>'
    else:
        for k in (-1, 1):
            arms += trazo(f"M {k*70} -4 Q {k*72} 40 {k*10} 46", 30, ropa, 8)
            arms += f'<circle cx="{k*6}" cy="46" r="17" fill="{piel}" stroke="{INK}" stroke-width="5"/>'
    o += f'<ellipse cx="0" cy="0" rx="88" ry="46" fill="{degradado(ropa)}" stroke="{INK}" stroke-width="7"/>'
    o += g(f"{id_}_brazos", arms)
    o += f'<circle cx="0" cy="0" r="40" fill="{degradado(pelo, 0.2)}" stroke="{INK}" stroke-width="6"/>'
    o += f'<path d="M -10 36 Q 0 52 10 36" fill="{piel}" stroke="{INK}" stroke-width="4"/>'
    o += brillo("M -22 -18 Q -10 -30 8 -28", 5, 0.6)
    return gt(id_, f"translate({f(cx)} {f(cy)}) scale({f(s)})", o)


# ------------------------------------------------------------------ objetos y efectos
def maleta(id_, cx, base, w=150, h=200, col=None):
    """Maleta de viaje con asa, ruedas y pegatinas. (cx, base) = centro abajo."""
    x0, y0 = cx - w / 2, base - h
    o = sombra(cx, base + 4, w * 0.6, 10, 0.25)
    o += f'<path d="M {f(cx-w*0.22)} {f(y0)} L {f(cx-w*0.22)} {f(y0-h*0.2)} L {f(cx+w*0.22)} {f(y0-h*0.2)} L {f(cx+w*0.22)} {f(y0)}" fill="none" stroke="{INK}" stroke-width="12" stroke-linejoin="round"/>'
    o += f'<path d="M {f(cx-w*0.22)} {f(y0)} L {f(cx-w*0.22)} {f(y0-h*0.2)} L {f(cx+w*0.22)} {f(y0-h*0.2)} L {f(cx+w*0.22)} {f(y0)}" fill="none" stroke="#9AA6BC" stroke-width="5" stroke-linejoin="round"/>'
    o += f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h-14)}" rx="18" fill="{col or "url(#maletaG)"}" stroke="{INK}" stroke-width="7"/>'
    for k in (0.3, 0.7):
        o += f'<line x1="{f(x0 + w*k)}" y1="{f(y0+12)}" x2="{f(x0 + w*k)}" y2="{f(base-26)}" stroke="{INK}" stroke-width="4" opacity="0.35"/>'
    o += f'<circle cx="{f(x0+22)}" cy="{f(base-6)}" r="10" fill="{INK}"/><circle cx="{f(x0+w-22)}" cy="{f(base-6)}" r="10" fill="{INK}"/>'
    o += f'<rect x="{f(cx-w*0.1)}" y="{f(y0+h*0.25)}" width="{f(w*0.36)}" height="{f(h*0.16)}" rx="6" fill="#FFFFFF" stroke="{INK}" stroke-width="3" transform="rotate(-10 {f(cx)} {f(y0+h*0.3)})"/>'
    o += brillo(f"M {f(x0+14)} {f(y0+20)} L {f(x0+14)} {f(y0+h*0.5)}", 5, 0.7)
    return g(id_, o)


def marcas_derrape(id_, p0, p1, ctrl, sep=60, w=16):
    """Dos marcas negras de neumático en curva (de p0 a p1 con punto de control ctrl). Anímalas con draw."""
    o = ""
    for k in (-0.5, 0.5):
        d = f"M {f(p0[0] + k*sep)} {f(p0[1])} Q {f(ctrl[0] + k*sep)} {f(ctrl[1])} {f(p1[0] + k*sep)} {f(p1[1])}"
        o += f'<path d="{d}" fill="none" stroke="#1B1E2B" stroke-width="{w}" stroke-linecap="round" opacity="0.75"/>'
    return g(id_, o)


def flecha_giro(id_, cx, cy, r, a0=200, a1=-20, col=LIME, w=12):
    """Flecha en arco alrededor de (cx, cy), de a0 a a1 grados (sentido horario si a1 < a0 en pantalla)."""
    p0 = (cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0)))
    p1 = (cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1)))
    large = 1 if abs(a1 - a0) > 180 else 0
    sweep = 1 if a1 > a0 else 0
    d = f"M {f(p0[0])} {f(p0[1])} A {f(r)} {f(r)} 0 {large} {sweep} {f(p1[0])} {f(p1[1])}"
    tang = math.radians(a1 + (90 if sweep else -90))
    pt = 28
    q1 = (p1[0] - pt * math.cos(tang - 0.5), p1[1] - pt * math.sin(tang - 0.5))
    q2 = (p1[0] - pt * math.cos(tang + 0.5), p1[1] - pt * math.sin(tang + 0.5))
    hd = f"M {f(q1[0])} {f(q1[1])} L {f(p1[0])} {f(p1[1])} L {f(q2[0])} {f(q2[1])}"
    return g(id_, trazo(d, w, col, 9) + trazo(hd, w, col, 9))


# ------------------------------------------------------------------ fondos
def sala_presentacion(W=1080, H=1920, suelo_y=1180):
    """Sala oscura de presentación de coches: foco cenital, pantalla de fondo con líneas, suelo brillante con reflejo."""
    o = f'<rect width="{W}" height="{H}" fill="url(#salaFondo)"/>'
    for k in range(9):
        y = 260 + k * 95
        o += f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="#3E4770" stroke-width="3" opacity="0.6"/>'
    o += f'<path d="M {W*0.36} 0 L {W*0.64} 0 L {W*0.95} {suelo_y} L {W*0.05} {suelo_y} Z" fill="url(#focoSala)"/>'
    o += f'<rect x="0" y="{suelo_y}" width="{W}" height="{H-suelo_y}" fill="url(#salaSuelo)"/>'
    o += f'<path d="M 0 {suelo_y} L {W} {suelo_y}" stroke="{INK}" stroke-width="8"/>'
    o += f'<ellipse cx="{W/2}" cy="{suelo_y+40}" rx="{W*0.45}" ry="38" fill="#FFFFFF" opacity="0.12"/>'
    return o


def carretera(W=1080, H=1920, y0=900, y1=1300):
    """Exterior de día: cielo, colinas, carretera recta en perspectiva lateral (franja de asfalto con líneas) y arcén."""
    o = f'<rect width="{W}" height="{H}" fill="#8FD3FF"/>'
    o += f'<path d="M 0 {y0-180} Q {W*0.3} {y0-320} {W*0.6} {y0-200} Q {W*0.85} {y0-110} {W} {y0-230} L {W} {y0} L 0 {y0} Z" fill="#7BE07B" stroke="{INK}" stroke-width="6"/>'
    o += f'<rect x="0" y="{y0}" width="{W}" height="{y1-y0}" fill="url(#asfaltoG)" stroke="{INK}" stroke-width="6"/>'
    for x in range(-40, W, 200):
        o += f'<rect x="{x}" y="{(y0+y1)/2-8}" width="110" height="16" rx="6" fill="#FFFFFF" opacity="0.9"/>'
    o += f'<rect x="0" y="{y1}" width="{W}" height="{H-y1}" fill="#5FC46B"/>'
    return o


def pista_hielo(W=1080, H=1920, y0=980):
    """Pista de patinaje: grada azul oscura al fondo, valla blanca y hielo brillante con marcas de cuchillas."""
    o = f'<rect width="{W}" height="{H}" fill="#203A78"/>'
    for k in range(6):
        y = 300 + k * 110
        o += f'<rect x="0" y="{y}" width="{W}" height="56" fill="#2C4C93" opacity="0.8"/>'
    o += f'<rect x="0" y="{y0-90}" width="{W}" height="90" fill="#FFFFFF" stroke="{INK}" stroke-width="7"/>'
    o += f'<rect x="0" y="{y0-90}" width="{W}" height="18" fill="{CORAL}"/>'
    o += f'<rect x="0" y="{y0}" width="{W}" height="{H-y0}" fill="url(#hieloG)"/>'
    o += f'<path d="M 0 {y0} L {W} {y0}" stroke="{INK}" stroke-width="7"/>'
    for (a, b, c_, d) in ((120, y0+200, 420, y0+260), (600, y0+160, 980, y0+230), (200, y0+380, 760, y0+330)):
        o += f'<path d="M {a} {b} Q {(a+c_)/2} {b-60} {c_} {d}" fill="none" stroke="#FFFFFF" stroke-width="6" opacity="0.8"/>'
    return o

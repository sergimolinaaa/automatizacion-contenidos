"""Aviones y aerodinámica: jumbo de cuatro motores de perfil, perfil de ala (corte NACA) con líneas de corriente que se
desvían hacia abajo, signos de presión, cochecito de perfil (para pilas y comparaciones de peso), retrato de Newton con
manzana, pista de despegue en perspectiva y fondo de aula.

Sale de: lote7-07-avion (¿cómo vuela un avión de 400 toneladas?).
"""
import math
from ..base import (INK, LIME, CORAL, YEL, AZUL, f, g, gt, T, MONO, DISP, shade, trazo, sombra, brillo, brillo_arco,
                    lg, rg, registrar_defs, degradado, pegatina, Pieza)

registrar_defs(
    lg("avFus", [(0, "#FFFFFF"), (0.55, "#E9EEF6"), (1, "#AEB9CC")])
    + lg("avMotor", [(0, "#F4F6FA"), (0.5, "#BCC5D4"), (1, "#7D889C")])
    + lg("avAzul", [(0, "#3D63FF"), (1, "#1631C9")])
    + lg("avCristal", [(0, "#E4F6FF"), (1, "#5E93C8")])
    + lg("avAla", [(0, "#F6F8FC"), (0.5, "#C9D1DE"), (1, "#8C97AB")])
    + lg("avPerfil", [(0, "#FFFFFF"), (0.35, "#D7DDE7"), (1, "#7F8AA0")])
    + lg("avPista", [(0, "#3A4152"), (1, "#5A6275")])
    + lg("avHierba", [(0, "#7FD07A"), (1, "#4FA85A")])
    + rg("avManzana", [(0, "#FF8A7A"), (0.6, "#E2262C"), (1, "#9E1218")], 0.38, 0.32, 0.7)
)


# ------------------------------------------------------------------ jumbo
def jumbo(id_, cx, cy, s=1.0, franja="url(#avAzul)", rot_=0, texto=None):
    """Jumbo de pasajeros de cuatro motores (tipo 747, con la «joroba» de la cubierta superior) de perfil, morro a la
    derecha. Largo ≈ 1000*s. Se ven los dos motores del ala cercana y, por detrás del fuselaje, los dos del ala lejana.
    Ids: {id}_motores (los 4), {id}_ventanillas, {id}_ala. .puntos: morro, cola, ala, ventanilla (una de la cubierta
    superior, para asomar a alguien), tren (bajo el fuselaje)."""
    o = ""
    # ala lejana y sus dos motores (por detrás del fuselaje)
    o += pegatina("M 150 -20 L 40 -20 L -110 -150 L -60 -150 Z", "#B8C2D3", 6)
    for (x, y) in ((70, -70), (-30, -112)):
        o += f'<rect x="{x-46}" y="{y-16}" width="92" height="32" rx="16" fill="#9AA5B9" stroke="{INK}" stroke-width="5"/>'
    # estabilizador horizontal lejano
    o += pegatina("M -400 -18 L -470 -70 L -440 -70 L -360 -18 Z", "#B8C2D3", 5)
    # fuselaje con joroba
    fus = ("M -500 -34 Q -470 -54 -380 -56 L 150 -56 Q 220 -112 330 -112 Q 410 -110 450 -66 Q 500 -50 506 -8 "
           "Q 504 30 452 50 L -300 54 Q -420 50 -500 -4 Z")
    o += pegatina(fus, "url(#avFus)", 7)
    # deriva (cola vertical) con la franja de color
    o += pegatina("M -300 -56 L -420 -210 L -484 -210 L -470 -40 Z", franja, 7)
    o += brillo("M -432 -196 L -466 -60", 5, 0.5)
    # franja (cheatline) y vientre
    o += f'<path d="M -470 4 L 470 4 Q 492 6 500 16 L 500 26 Q 470 20 452 20 L -440 22 Z" fill="{franja}" stroke="{INK}" stroke-width="4"/>'
    o += f'<path d="M -300 54 L 452 50 Q 490 36 502 14" fill="none" stroke="{INK}" stroke-width="3" opacity="0.35"/>'
    o += brillo("M -460 -44 L 150 -46 Q 220 -100 330 -100", 6, 0.8)
    # ventanillas: cubierta principal y superior
    ven = "".join(f'<rect x="{x}" y="-24" width="14" height="18" rx="6" fill="url(#avCristal)" stroke="{INK}" stroke-width="3"/>'
                  for x in range(-380, 420, 34))
    ven += "".join(f'<rect x="{x}" y="-88" width="14" height="18" rx="6" fill="url(#avCristal)" stroke="{INK}" stroke-width="3"/>'
                   for x in range(200, 360, 34))
    ven += f'<rect x="-262" y="-36" width="30" height="66" rx="8" fill="#DCE3EE" stroke="{INK}" stroke-width="4"/>'
    ven += f'<rect x="246" y="-36" width="30" height="62" rx="8" fill="#DCE3EE" stroke="{INK}" stroke-width="4"/>'
    o += g(f"{id_}_ventanillas" if id_ else None, ven)
    o += f'<path d="M 412 -84 L 446 -70 L 452 -56 L 404 -60 Z" fill="url(#avCristal)" stroke="{INK}" stroke-width="4"/>'
    if texto:
        o += T(-60, -24 - 14, texto, 24, "#1631C9", font=DISP)
    # ala cercana (hacia el espectador) con dos motores colgados
    ala = pegatina("M 190 18 L 20 26 L -230 170 L -170 176 Z", "url(#avAla)", 7)
    ala += brillo("M 160 26 L 0 36", 5, 0.7)
    ala += f'<path d="M -190 172 L -214 196 L -180 196 Z" fill="#C9D1DE" stroke="{INK}" stroke-width="5"/>'
    o += g(f"{id_}_ala" if id_ else None, ala)
    mot = ""
    for (x, y, k) in ((70, 90, 1.0), (-70, 150, 0.92)):
        w, h = 120 * k, 50 * k
        mot += f'<path d="M {f(x-20)} {f(y-h/2-8)} L {f(x+10)} {f(y-h/2-28)}" stroke="{INK}" stroke-width="16"/>'
        mot += f'<path d="M {f(x-20)} {f(y-h/2-8)} L {f(x+10)} {f(y-h/2-28)}" stroke="#AEB9CC" stroke-width="8"/>'
        mot += f'<rect x="{f(x-w/2)}" y="{f(y-h/2)}" width="{f(w)}" height="{f(h)}" rx="{f(h/2)}" fill="url(#avMotor)" stroke="{INK}" stroke-width="6"/>'
        mot += f'<ellipse cx="{f(x+w/2-6)}" cy="{f(y)}" rx="{f(10*k)}" ry="{f(h/2-3)}" fill="#3A4152" stroke="{INK}" stroke-width="5"/>'
        mot += brillo(f"M {f(x-w/2+14)} {f(y-h/2+9)} L {f(x+w/2-24)} {f(y-h/2+9)}", 4, 0.8)
    o += g(f"{id_}_motores" if id_ else None, mot)
    # estabilizador horizontal cercano
    o += pegatina("M -380 10 L -470 60 L -436 64 L -330 14 Z", "url(#avAla)", 6)
    tr = f"translate({f(cx)} {f(cy)}) rotate({f(rot_)}) scale({f(s)})"
    c, sn = math.cos(math.radians(rot_)), math.sin(math.radians(rot_))

    def P(x, y):
        x, y = x * s, y * s
        return (cx + x * c - y * sn, cy + x * sn + y * c)
    pts_ = {"morro": P(506, -8), "cola": P(-450, -210), "ala": P(0, 100), "ventanilla": P(268, -79), "tren": P(60, 56)}
    return Pieza(gt(id_, tr, o), pts_, (cx - 510 * s, cy - 210 * s, cx + 510 * s, cy + 200 * s))


# ------------------------------------------------------------------ perfil de ala
def _naca(L, t=0.13, m=0.05, p=0.4, n=40):
    """Perfil NACA de 4 cifras: listas (sup, inf) de puntos locales, borde de ataque en (0, 0), cuerda L hacia +x."""
    sup, inf = [], []
    for i in range(n + 1):
        b = math.pi * i / n
        x = (1 - math.cos(b)) / 2
        yt = 5 * t * (0.2969 * math.sqrt(x) - 0.126 * x - 0.3516 * x ** 2 + 0.2843 * x ** 3 - 0.1036 * x ** 4)
        if x < p:
            yc, dy = m / p ** 2 * (2 * p * x - x * x), 2 * m / p ** 2 * (p - x)
        else:
            yc, dy = m / (1 - p) ** 2 * ((1 - 2 * p) + 2 * p * x - x * x), 2 * m / (1 - p) ** 2 * (p - x)
        th = math.atan(dy)
        sup.append(((x - yt * math.sin(th)) * L, -(yc + yt * math.cos(th)) * L))
        inf.append(((x + yt * math.sin(th)) * L, -(yc - yt * math.cos(th)) * L))
    return sup, inf


def perfil_ala(id_, cx, cy, L=420, ang=0, t=0.16, m=0.06, curva=True, fill="url(#avPerfil)"):
    """Corte de un ala (perfil curvado, borde de ataque redondo a la izquierda, borde de salida fino a la derecha).
    (cx, cy) = centro de la cuerda; ang = ángulo de ataque en grados (positivo = morro arriba).
    Ids: {id}_curva (línea lima sobre el extradós, para «draw»). .puntos: ataque, salida, arriba, abajo, centro,
    sup / inf (listas de puntos del extradós e intradós, en coordenadas finales) para trazar líneas de corriente."""
    sup, inf = _naca(L, t, m)
    c = (L / 2, 0)

    def P(q):
        a = math.radians(ang)
        x, y = q[0] - c[0], q[1] - c[1]
        return (cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a))
    S, I = [P(q) for q in sup], [P(q) for q in inf]
    d = "M " + " L ".join(f"{f(x)} {f(y)}" for x, y in S) + " L " + " L ".join(f"{f(x)} {f(y)}" for x, y in reversed(I[1:])) + " Z"
    o = f'<path d="{d}" fill="{INK}" opacity="0.18" transform="translate(10 14)"/>'
    o += pegatina(d, fill, 8)
    hi = S[4:len(S) // 2 + 4]
    o += f'<path d="M ' + " L ".join(f"{f(x)} {f(y + 9)}" for x, y in hi) + '" fill="none" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round" opacity="0.85"/>'
    for k in (0.3, 0.6):  # remaches
        j = int(len(S) * k)
        x, y = (S[j][0] + I[j][0]) / 2, (S[j][1] + I[j][1]) / 2
        o += f'<circle cx="{f(x)}" cy="{f(y)}" r="4" fill="#6E7890"/>'
    if curva:
        o += g(f"{id_}_curva", f'<path d="M ' + " L ".join(f"{f(x)} {f(y)}" for x, y in S[1:-2]) +
               f'" fill="none" stroke="{LIME}" stroke-width="9" stroke-linecap="round"/>')
    j = len(S) * 2 // 5
    pts_ = {"ataque": S[0], "salida": S[-1], "arriba": S[j], "abajo": I[j], "centro": (cx, cy), "sup": S, "inf": I}
    xs = [p[0] for p in S + I]
    ys = [p[1] for p in S + I]
    return Pieza(g(id_, o), pts_, (min(xs), min(ys), max(xs), max(ys)))


def lineas_corriente(id_, ala, x0, x1, arriba=(50, 120, 190), abajo=(50, 120), bajada=25, col="#3FA9F5", w=9, flecha_=True):
    """Líneas de corriente alrededor de un `perfil_ala` (la Pieza): llegan rectas desde x0, rodean el ala y salen
    inclinadas hacia abajo `bajada` grados detrás (la desviación que da la sustentación). arriba / abajo = distancias
    al ala de cada línea. Ids {id}_l0, {id}_l1… (de arriba abajo, para «draw» escalonado). Las líneas son discontinuas:
    con «flow» corren."""
    S, I = ala.puntos["sup"], ala.puntos["inf"]
    xa, xs = ala.puntos["ataque"][0], ala.puntos["salida"][0]
    ya, ys = ala.puntos["ataque"][1], ala.puntos["salida"][1]
    xs_s = [p[0] for p in S]

    def interp(lst, x):
        for k in range(1, len(lst)):
            if lst[k][0] >= x:
                a, b = lst[k - 1], lst[k]
                t = (x - a[0]) / max(1e-6, b[0] - a[0])
                return a[1] + (b[1] - a[1]) * t
        return lst[-1][1]

    def media(x):
        return (interp(S, x) + interp(I, x)) / 2
    yref = (ya + ys) / 2
    tb = math.tan(math.radians(bajada))
    lineas = [(-d, d) for d in arriba] + [(d, d) for d in abajo]
    lineas.sort()
    out = ""
    for i, (off, dist) in enumerate(lineas):
        dec = math.exp(-dist / 260)
        n = 160
        xs_ = [x0 + (x1 - x0) * k / n for k in range(n + 1)]
        Ds, ths = [], []
        for x in xs_:
            if x < xa:
                Ds.append((ya - yref) * math.exp(-(xa - x) / 140))
                ths.append(0)
            elif x <= xs:
                Ds.append(media(x) - yref)
                ths.append((interp(I, x) - interp(S, x)) / 2)
            else:
                Ds.append((ys - yref) + (x - xs) * tb * (1 - math.exp(-(x - xs) / 90)))
                ths.append(0)
        paso = (x1 - x0) / n
        r = max(1, int(45 / paso))
        ths = [max(ths[max(0, k - r):k + r + 1]) for k in range(n + 1)]  # dilata el grosor para no pisar el ala
        ys_ = []
        for k, x in enumerate(xs_):
            y = yref + off + Ds[k] * (0.55 + 0.45 * dec) + (-ths[k] if off < 0 else ths[k]) * dec * 1.3
            if x > xs:
                y += (x - xs) * tb * 0.35 * (1 - dec)
            ys_.append(y)
        sig = 40 / paso
        ker = [math.exp(-(j / sig) ** 2 / 2) for j in range(-int(3 * sig), int(3 * sig) + 1)]
        h = len(ker) // 2
        pad = [ys_[0]] * h + ys_ + [ys_[-1] + (ys_[-1] - ys_[-2]) * j for j in range(1, h + 1)]
        ys_ = [sum(ker[j] * pad[k + j] for j in range(len(ker))) / sum(ker) for k in range(n + 1)]
        pts_ = list(zip(xs_, ys_))
        d = "M " + " L ".join(f"{f(x)} {f(y)}" for x, y in pts_)
        body = (f'<path d="{d}" fill="none" stroke="#FFFFFF" stroke-width="{w+8}" stroke-linecap="round" stroke-linejoin="round" opacity="0.9"/>'
                f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="46 18"/>')
        if flecha_:
            (ax_, ay_), (bx_, by_) = pts_[-3], pts_[-1]
            a = math.atan2(by_ - ay_, bx_ - ax_)
            q1 = (bx_ - 26 * math.cos(a - 0.55), by_ - 26 * math.sin(a - 0.55))
            q2 = (bx_ - 26 * math.cos(a + 0.55), by_ - 26 * math.sin(a + 0.55))
            body += f'<path d="M {f(q1[0])} {f(q1[1])} L {f(bx_ + 6*math.cos(a))} {f(by_ + 6*math.sin(a))} L {f(q2[0])} {f(q2[1])} Z" fill="{col}" stroke="#FFFFFF" stroke-width="4" stroke-linejoin="round"/>'
        out += g(f"{id_}_l{i}", body)
    return g(id_, out)


def signo_presion(id_, cx, cy, r=34, signo="+", col=None):
    """Signo de presión en un disco: «+» (coral, mucha presión) o «−» dibujado (azul claro, poca presión)."""
    col = col or (CORAL if signo == "+" else "#8FD3FF")
    o = f'<circle cx="{f(cx+3)}" cy="{f(cy+4)}" r="{f(r)}" fill="{INK}" opacity="0.2"/>'
    o += f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{degradado(col, 0.25)}" stroke="{INK}" stroke-width="5"/>'
    k = r * 0.55
    o += f'<path d="M {f(cx-k)} {f(cy)} L {f(cx+k)} {f(cy)}" stroke="#FFFFFF" stroke-width="{f(r*0.28)}" stroke-linecap="round"/>'
    if signo == "+":
        o += f'<path d="M {f(cx)} {f(cy-k)} L {f(cx)} {f(cy+k)}" stroke="#FFFFFF" stroke-width="{f(r*0.28)}" stroke-linecap="round"/>'
    o += brillo_arco(cx, cy, r * 0.75, 200, 250, max(3, r * 0.1), 0.6)
    return g(id_, o)


# ------------------------------------------------------------------ cochecito, Newton, manzana
def cochecito(id_, cx, base, s=1.0, col=CORAL):
    """Turismo pequeño de perfil (morro a la derecha), ≈ 180×80 a s=1, para apilar o comparar pesos."""
    o = sombra(0, 2, 80, 6, 0.18)
    o += pegatina("M -88 -18 Q -90 -40 -70 -42 L -44 -44 Q -26 -72 8 -72 Q 40 -72 56 -46 L 78 -42 Q 92 -38 92 -22 L 90 -14 L -86 -14 Z",
                  degradado(col, 0.3), 6)
    o += f'<path d="M -36 -46 Q -22 -64 4 -64 L 4 -46 Z M 14 -64 Q 38 -64 48 -46 L 14 -46 Z" fill="url(#avCristal)" stroke="{INK}" stroke-width="4"/>'
    o += brillo("M -66 -36 L 70 -38", 4, 0.6)
    for x in (-52, 54):
        o += f'<circle cx="{x}" cy="-12" r="17" fill="#2A2F3E" stroke="{INK}" stroke-width="5"/><circle cx="{x}" cy="-12" r="7" fill="#C9D1DE"/>'
    return gt(id_, f"translate({f(cx)} {f(base)}) scale({f(s)})", o)


def manzana(id_, cx, cy, r=36):
    """Manzana roja con rabito y hoja."""
    o = f'<path d="M {f(cx)} {f(cy-r*0.7)} C {f(cx+r*1.25)} {f(cy-r*1.25)}, {f(cx+r*1.25)} {f(cy+r*0.95)}, {f(cx)} {f(cy+r*0.95)} C {f(cx-r*1.25)} {f(cy+r*0.95)}, {f(cx-r*1.25)} {f(cy-r*1.25)}, {f(cx)} {f(cy-r*0.7)} Z" fill="url(#avManzana)" stroke="{INK}" stroke-width="5"/>'
    o += f'<path d="M {f(cx)} {f(cy-r*0.7)} Q {f(cx+2)} {f(cy-r*1.1)} {f(cx+r*0.15)} {f(cy-r*1.3)}" fill="none" stroke="#5A3A1E" stroke-width="6" stroke-linecap="round"/>'
    o += f'<path d="M {f(cx+r*0.1)} {f(cy-r*1.05)} Q {f(cx+r*0.7)} {f(cy-r*1.4)} {f(cx+r*0.9)} {f(cy-r*0.95)} Q {f(cx+r*0.4)} {f(cy-r*0.8)} {f(cx+r*0.1)} {f(cy-r*1.05)} Z" fill="#5FC46B" stroke="{INK}" stroke-width="4"/>'
    o += brillo(f"M {f(cx-r*0.55)} {f(cy-r*0.25)} Q {f(cx-r*0.5)} {f(cy-r*0.6)} {f(cx-r*0.2)} {f(cy-r*0.65)}", max(3, r * 0.12), 0.8)
    return g(id_, o)


def retrato_newton(id_, cx, cy, s=1.0):
    """Retrato de Isaac Newton en marco ovalado dorado (peluca larga blanca, levita oscura, pañuelo blanco) con placa
    «ISAAC NEWTON». Ids: {id}_cara (cabeza, para sway), {id}_ojos. ≈ 300×400 a s=1. .puntos: hombro (para poner la manzana)."""
    from ..personajes import persona
    rx, ry = 140 * s, 180 * s
    o = f'<ellipse cx="{f(cx+8)}" cy="{f(cy+12)}" rx="{f(rx+18)}" ry="{f(ry+18)}" fill="{INK}" opacity="0.25"/>'
    o += f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(rx+18)}" ry="{f(ry+18)}" fill="{degradado("#E8B830", 0.3)}" stroke="{INK}" stroke-width="7"/>'
    o += f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(rx)}" ry="{f(ry)}" fill="{degradado("#C9A27A", 0.35)}" stroke="{INK}" stroke-width="6"/>'
    registrar_defs(f'<clipPath id="{id_}_clip"><ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(rx-3)}" ry="{f(ry-3)}"/></clipPath>')
    p = persona(f"{id_}_p", cx, cy + ry * 0.98, 1.05 * s, "mayor", "clara", "largo", "blanco", "chaqueta", "#3A2E3A",
                camisa_color="#FFFFFF", expresion="neutral", pose="busto", brazos=("relajado", "relajado"))
    o += f'<g clip-path="url(#{id_}_clip)">{p}</g>'
    o += brillo_arco(cx, cy, rx + 9, 200, 250, 6, 0.7)
    pw, ph = 230 * s, 46 * s
    o += f'<rect x="{f(cx-pw/2)}" y="{f(cy+ry+4)}" width="{f(pw)}" height="{f(ph)}" rx="8" fill="{degradado("#E8B830", 0.3)}" stroke="{INK}" stroke-width="5"/>'
    o += T(cx, cy + ry + 4 + ph * 0.68, "ISAAC NEWTON", 22 * s, INK)
    return Pieza(g(id_, o), {"hombro": p.puntos["hombro_der"], "cabeza": p.puntos["cabeza"]},
                 (cx - rx - 18, cy - ry - 18, cx + rx + 18, cy + ry + 4 + ph))


# ------------------------------------------------------------------ escenarios
def pista_despegue(id_, W=1000, H=820, horizonte=300, ancho_lejos=160, ancho_cerca=900):
    """Pista de aterrizaje en perspectiva (para layout free): franja de hierba, asfalto que se estrecha al fondo, línea
    central discontinua en {id}_marcas (para «flow» o move en bucle), bordes y umbral con rayas."""
    cx = W / 2
    o = f'<path d="M 0 {f(horizonte)} L {W} {f(horizonte)} L {W} {H} L 0 {H} Z" fill="url(#avHierba)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
    l0, l1 = ancho_lejos / 2, ancho_cerca / 2
    o += pegatina(f"M {f(cx-l0)} {f(horizonte)} L {f(cx+l0)} {f(horizonte)} L {f(cx+l1)} {H} L {f(cx-l1)} {H} Z", "url(#avPista)", 7)
    for k in (0.08, 0.92):
        o += f'<path d="M {f(cx-l0+2*l0*k)} {f(horizonte)} L {f(cx-l1+2*l1*k)} {H}" stroke="#FFFFFF" stroke-width="6" opacity="0.85"/>'
    mk = ""
    n = 9
    for i in range(n):
        t0 = (i / n) ** 1.6
        t1 = ((i + 0.45) / n) ** 1.6
        y0, y1 = horizonte + (H - horizonte) * t0, horizonte + (H - horizonte) * t1
        w0, w1 = 4 + 18 * t0, 4 + 18 * t1
        mk += f'<path d="M {f(cx-w0/2)} {f(y0)} L {f(cx+w0/2)} {f(y0)} L {f(cx+w1/2)} {f(y1)} L {f(cx-w1/2)} {f(y1)} Z" fill="#FFFFFF"/>'
    o += g(f"{id_}_marcas", mk)
    for i in range(6):
        xa = cx - l1 * 0.8 + i * l1 * 0.12
        xb = cx + l1 * 0.2 + i * l1 * 0.12
        for xx in (xa, xb):
            o += f'<rect x="{f(xx)}" y="{f(H-60)}" width="{f(l1*0.07)}" height="50" fill="#FFFFFF" opacity="0.9"/>'
    return g(id_, o)


def aula(W=1080, H=1920, suelo_y=1280, pared="#F3E7C9"):
    """Fondo de aula: pared cálida con zócalo, ventanal con cielo a la derecha, corcho con papeles y suelo de madera."""
    o = f'<rect width="{W}" height="{H}" fill="{degradado(pared, 0.12)}"/>'
    o += f'<rect x="0" y="{f(suelo_y-90)}" width="{W}" height="90" fill="#D8C49A" stroke="{INK}" stroke-width="5"/>'
    o += f'<rect x="0" y="{f(suelo_y)}" width="{W}" height="{f(H-suelo_y)}" fill="url(#maderaG)" stroke="{INK}" stroke-width="7"/>'
    for x in range(-60, W + 80, 150):
        o += f'<path d="M {x} {f(suelo_y)} L {x - 80} {H}" stroke="{INK}" stroke-width="3" opacity="0.3"/>'
    o += f'<rect x="{f(W-170)}" y="300" width="230" height="420" rx="10" fill="#9FDCFF" stroke="{INK}" stroke-width="7"/>'
    o += f'<path d="M {f(W-55)} 300 L {f(W-55)} 720 M {f(W-170)} 510 L {W+60} 510" stroke="{INK}" stroke-width="7"/>'
    o += brillo(f"M {f(W-150)} 330 L {f(W-90)} 330", 6, 0.8)
    return o

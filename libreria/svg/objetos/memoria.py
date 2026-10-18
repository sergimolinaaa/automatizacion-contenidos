"""Memoria y psicología cotidiana: puerta de madera (abierta / cerrada, con placa), tijeras, caja de colores,
bocadillo de pensamiento con dibujo dentro, mando de consola, sala pixelada de videojuego, tele antigua,
tira de película con fotogramas, edificio universitario con cúpula dorada, archivador con carpeta y birrete.

Sale de: lote7-06-puerta-olvido (archivo/puerta-olvido/dib.py), «el efecto puerta».
"""
import math
from ..base import (INK, LIME, CORAL, YEL, f, g, gt, T, MONO, DISP, shade, trazo, sombra, sombra_caja, brillo, brillo_arco,
                    lg, rg, registrar_defs, degradado, Pieza, poly, smooth)

registrar_defs(
    lg("puertaG", [(0, "#D9A06A"), (0.5, "#C2834C"), (1, "#9C6334")], 0, 0, 1, 0)
    + lg("puertaHoja", [(0, "#B87840"), (1, "#E0AC76")], 0, 0, 1, 0)
    + lg("marcoG", [(0, "#8A5530"), (1, "#B97D4B")], 0, 0, 1, 0)
    + rg("luzPuerta", [(0, "#FFF6D6"), (0.7, "#FFE3A0"), (1, "#F5C76A")], 0.5, 0.45, 0.75)
    + lg("oroG", [(0, "#FFE58A"), (0.45, "#F5C030"), (1, "#C98A12")])
    + lg("teleG", [(0, "#B9875A"), (1, "#7E5230")])
    + rg("teleScr", [(0, "#3C4A6E"), (1, "#141A2C")], 0.45, 0.4, 0.75)
    + lg("filmG", [(0, "#2A2F40"), (1, "#151926")])
    + lg("archG", [(0, "#AEB7C8"), (1, "#7C879C")], 0, 0, 1, 0)
    + lg("mandoG", [(0, "#4A5168"), (1, "#20242F")])
    + lg("cupulaG", [(0, "#FFE58A"), (0.5, "#F2B925"), (1, "#B67A0C")], 0, 0, 1, 0)
    + lg("piedraG", [(0, "#F4EBDD"), (1, "#D8C7AE")])
)


# ------------------------------------------------------------------ puerta
def puerta(id_, cx, base, w=300, h=560, estado="abierta", placa=None, luz=True, marco=34):
    """Puerta de madera de frente con marco. estado: 'abierta' (hoja girada hacia la izquierda y luz de la otra
    habitación), 'cerrada' o 'ambas' (dibuja las dos hojas: `{id}_hoja` abierta y `{id}_cerrada` para alternar
    con hide/pop al «cerrar la puerta»). placa = texto de una placa dorada (`{id}_placa`).
    Devuelve Pieza con .puntos hueco (centro del hueco), pomo, placa, suelo."""
    x0, x1, top = cx - w / 2, cx + w / 2, base - h
    o = sombra(cx, base + 4, w * 0.75, 16, 0.22)
    # marco
    o += (f'<path d="M {f(x0-marco)} {f(base)} L {f(x0-marco)} {f(top-marco)} L {f(x1+marco)} {f(top-marco)} L {f(x1+marco)} {f(base)} Z" '
          f'fill="url(#marcoG)" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>')
    o += brillo(f"M {f(x0-marco+10)} {f(base-20)} L {f(x0-marco+10)} {f(top-marco+12)} L {f(x1+marco-14)} {f(top-marco+12)}", 5, 0.45)
    # hueco: luz de la otra habitación
    hueco = "url(#luzPuerta)" if luz else "#2A2F40"
    o += f'<rect x="{f(x0)}" y="{f(top)}" width="{f(w)}" height="{f(h)}" fill="{hueco}" stroke="{INK}" stroke-width="6"/>'
    if luz:
        # suelo y zócalo de la habitación del fondo
        o += f'<path d="M {f(x0)} {f(base - h*0.16)} L {f(x1)} {f(base - h*0.16)} L {f(x1)} {f(base)} L {f(x0)} {f(base)} Z" fill="#E6C08A" opacity="0.85"/>'
        o += f'<path d="M {f(x0)} {f(base - h*0.16)} L {f(x1)} {f(base - h*0.16)}" stroke="#B98A52" stroke-width="4"/>'
        o += f'<path d="M {f(x0+w*0.12)} {f(base)} L {f(x0+w*0.3)} {f(base-h*0.16)} M {f(x1-w*0.12)} {f(base)} L {f(x1-w*0.3)} {f(base-h*0.16)}" stroke="#C99B60" stroke-width="3" opacity="0.7"/>'
    # hoja abierta (girada hacia el espectador por la izquierda)
    hx = x0 - w * 0.42
    hoja = (f'<path d="M {f(x0)} {f(top)} L {f(hx)} {f(top - h*0.05)} L {f(hx)} {f(base + h*0.04)} L {f(x0)} {f(base)} Z" '
            f'fill="url(#puertaHoja)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
    for a, b in ((0.1, 0.45), (0.55, 0.9)):
        ya0, ya1 = top + h * a, top + h * b
        hoja += (f'<path d="M {f(x0 - w*0.07)} {f(ya0 - h*0.004)} L {f(hx + w*0.06)} {f(ya0 - h*0.03)} L {f(hx + w*0.06)} {f(ya1 + h*0.02)} '
                 f'L {f(x0 - w*0.07)} {f(ya1 + h*0.004)} Z" fill="none" stroke="{shade("#9C6334", -0.2)}" stroke-width="5" stroke-linejoin="round"/>')
    hoja += f'<circle cx="{f(hx + w*0.07)}" cy="{f(top + h*0.52)}" r="{f(w*0.04)}" fill="url(#oroG)" stroke="{INK}" stroke-width="4"/>'
    hoja += brillo(f"M {f(hx + 12)} {f(top - h*0.03)} L {f(hx + 12)} {f(base)}", 5, 0.5)
    # hoja cerrada
    cerr = f'<rect x="{f(x0)}" y="{f(top)}" width="{f(w)}" height="{f(h)}" fill="url(#puertaG)" stroke="{INK}" stroke-width="7"/>'
    for a, b in ((0.08, 0.44), (0.54, 0.92)):
        cerr += (f'<rect x="{f(x0 + w*0.14)}" y="{f(top + h*a)}" width="{f(w*0.72)}" height="{f(h*(b-a))}" rx="8" '
                 f'fill="{degradado("#C98B55", 0.18)}" stroke="{shade("#9C6334", -0.2)}" stroke-width="5"/>')
    pomo = (x1 - w * 0.12, top + h * 0.52)
    cerr += f'<circle cx="{f(pomo[0])}" cy="{f(pomo[1])}" r="{f(w*0.045)}" fill="url(#oroG)" stroke="{INK}" stroke-width="4"/>'
    cerr += brillo(f"M {f(x0 + 14)} {f(top + 16)} L {f(x0 + 14)} {f(base - 16)}", 6, 0.55)
    if estado in ("abierta", "ambas"):
        o += g(f"{id_}_hoja" if id_ else None, hoja)
    if estado in ("cerrada", "ambas"):
        o += g(f"{id_}_cerrada" if id_ else None, cerr)
    pl = (cx, top - marco / 2)
    if placa:
        fs = min(34, w * 1.15 / (len(placa) * 0.8))
        pw = len(placa) * fs * 0.8 + 50
        ph = fs * 1.9
        pc = (cx, top + h * 0.14)
        pl = pc
        pb = sombra_caja(pc[0] - pw / 2, pc[1] - ph / 2, pw, ph, 10, 6, 8, 0.3)
        pb += f'<rect x="{f(pc[0]-pw/2)}" y="{f(pc[1]-ph/2)}" width="{f(pw)}" height="{f(ph)}" rx="10" fill="url(#oroG)" stroke="{INK}" stroke-width="6"/>'
        pb += f'<rect x="{f(pc[0]-pw/2+8)}" y="{f(pc[1]-ph/2+8)}" width="{f(pw-16)}" height="{f(ph-16)}" rx="6" fill="none" stroke="#9A6A0A" stroke-width="3"/>'
        pb += "".join(f'<circle cx="{f(pc[0] + k*(pw/2-16))}" cy="{f(pc[1])}" r="5" fill="#9A6A0A"/>' for k in (-1, 1))
        pb += T(pc[0], pc[1] + fs * 0.36, placa, fs, "#3A2600", font=DISP)
        pb += brillo(f"M {f(pc[0]-pw/2+16)} {f(pc[1]-ph/2+12)} L {f(pc[0]+pw/2-40)} {f(pc[1]-ph/2+12)}", 4, 0.8)
        o += g(f"{id_}_placa" if id_ else None, pb)
    return Pieza(g(id_, o), {"hueco": (cx, top + h / 2), "pomo": pomo, "placa": pl, "suelo": (cx, base)},
                 (x0 - w * 0.42 if estado != "cerrada" else x0 - marco, top - marco, x1 + marco, base))


# ------------------------------------------------------------------ objetos pequeños
def tijeras(id_, cx, cy, s=1.0, rot_=-30, col=CORAL):
    """Tijeras abiertas (≈ 220×120 a s=1), mangos de color y hojas de acero."""
    o = ""
    for k in (-1, 1):
        a = math.radians(k * 14)
        tip = (cx + 120 * s * math.cos(a), cy + 120 * s * math.sin(a))
        bx, by = cx - 4 * s * math.cos(a), cy - 4 * s * math.sin(a)
        nx, ny = -math.sin(a), math.cos(a)
        d = (f"M {f(bx + nx*k*12*s)} {f(by + ny*k*12*s)} L {f(tip[0])} {f(tip[1])} "
             f"L {f(bx - nx*k*6*s)} {f(by - ny*k*6*s)} Z")
        o += f'<path d="{d}" fill="url(#aceroG)" stroke="{INK}" stroke-width="{f(5*s)}" stroke-linejoin="round"/>'
    for k in (-1, 1):
        a = math.radians(180 - k * 24)
        hx, hy = cx + 62 * s * math.cos(a), cy + 62 * s * math.sin(a)
        o += trazo(f"M {f(cx)} {f(cy)} L {f(hx)} {f(hy)}", 16 * s, shade(col, -0.1), 5 * s)
        o += f'<ellipse cx="{f(hx - 14*s)}" cy="{f(hy)}" rx="{f(32*s)}" ry="{f(24*s)}" fill="none" stroke="{INK}" stroke-width="{f(22*s)}"/>'
        o += f'<ellipse cx="{f(hx - 14*s)}" cy="{f(hy)}" rx="{f(32*s)}" ry="{f(24*s)}" fill="none" stroke="{col}" stroke-width="{f(13*s)}"/>'
        o += brillo(f"M {f(hx - 36*s)} {f(hy - 8*s)} A {f(28*s)} {f(20*s)} 0 0 1 {f(hx - 12*s)} {f(hy - 22*s)}", 4 * s, 0.8)
    o += f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(8*s)}" fill="#E9EDF5" stroke="{INK}" stroke-width="{f(4*s)}"/>'
    return gt(id_, f"rotate({f(rot_)} {f(cx)} {f(cy)})", o)


def caja_colores(id_, cx, cy, w=120, h=90, col=CORAL, lazo=LIME, borrosa=False):
    """Caja de regalo / objeto de colores. borrosa=True: versión desvaída (recuerdo que se olvida)."""
    x, y = cx - w / 2, cy - h / 2
    op = ' opacity="0.45"' if borrosa else ""
    o = sombra_caja(x, y, w, h, 8, 6, 8, 0.25)
    o += f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="8" fill="{degradado(col, 0.25)}" stroke="{INK}" stroke-width="6"/>'
    o += f'<rect x="{f(x - 6)}" y="{f(y - 4)}" width="{f(w + 12)}" height="{f(h*0.26)}" rx="6" fill="{degradado(shade(col, 0.15), 0.2)}" stroke="{INK}" stroke-width="6"/>'
    o += f'<rect x="{f(cx - w*0.09)}" y="{f(y - 4)}" width="{f(w*0.18)}" height="{f(h + 4)}" fill="{lazo}" stroke="{INK}" stroke-width="4"/>'
    o += (f'<path d="M {f(cx)} {f(y-4)} C {f(cx - w*0.35)} {f(y - h*0.45)}, {f(cx - w*0.4)} {f(y + h*0.05)}, {f(cx)} {f(y-4)} '
          f'C {f(cx + w*0.35)} {f(y - h*0.45)}, {f(cx + w*0.4)} {f(y + h*0.05)}, {f(cx)} {f(y-4)} Z" fill="{lazo}" stroke="{INK}" stroke-width="5"/>')
    o += brillo(f"M {f(x + 10)} {f(y + h*0.35)} L {f(x + 10)} {f(y + h - 10)}", 5, 0.8)
    if borrosa:
        o = f'<g{op} filter="url(#borroso)">{o}</g>'
    return g(id_, o)


registrar_defs('<filter id="borroso" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="5"/></filter>')


def bocadillo_piensa(id_, cx, cy, w, h, contenido="", cola=None):
    """Nube de pensamiento (≈ w×h) con un DIBUJO dentro (contenido en coordenadas finales) y burbujitas hacia `cola`.
    Sub-ids: `{id}_nube` (la nube) y `{id}_burbujas`."""
    blobs = []
    n = 9
    for i in range(n):
        t = i / n * 2 * math.pi
        blobs.append((cx + w * 0.42 * math.cos(t), cy + h * 0.38 * math.sin(t), min(w, h) * (0.26 + 0.04 * (i % 3))))
    circ = "".join(f'<circle cx="{f(a)}" cy="{f(b)}" r="{f(r)}"/>' for a, b, r in blobs)
    el = f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(w*0.44)}" ry="{f(h*0.4)}"/>'
    s = f'<g fill="{INK}" opacity="0.22" transform="translate(9 11)">{circ}{el}</g>'
    s += f'<g fill="{INK}" stroke="{INK}" stroke-width="14">{circ}{el}</g><g fill="#FFFFFF">{circ}{el}</g>'
    s += brillo(f"M {f(cx - w*0.36)} {f(cy - h*0.12)} A {f(w*0.3)} {f(h*0.3)} 0 0 1 {f(cx - w*0.1)} {f(cy - h*0.42)}", 7, 0.9, "#DDEBFA")
    bur = ""
    if cola:
        tx, ty = cola
        for j, r in enumerate((20, 14, 9)):
            k_ = 0.5 + j * 0.2
            bx, by = cx + (tx - cx) * k_, cy + (ty - cy) * k_
            bur += f'<circle cx="{f(bx)}" cy="{f(by)}" r="{r}" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/>'
    return g(id_, g(f"{id_}_burbujas", bur) + g(f"{id_}_nube", s + contenido))


def humo(id_, cx, cy, s=1.0):
    """Bocanada de humo gris (para «se deshace en humo»)."""
    o = ""
    for dx, dy, r, op in ((-60, 10, 46, 0.9), (0, -20, 58, 0.85), (60, 6, 44, 0.8), (-20, 40, 36, 0.7), (40, 46, 30, 0.6)):
        o += f'<circle cx="{f(cx + dx*s)}" cy="{f(cy + dy*s)}" r="{f(r*s)}" fill="#C9CFDB" stroke="{INK}" stroke-width="{f(4*s)}" opacity="{op}"/>'
    o += "".join(f'<path d="M {f(cx + dx*s)} {f(cy - 70*s)} q {f(12*s)} {f(-18*s)} 0 {f(-36*s)} q {f(-12*s)} {f(-18*s)} 0 {f(-36*s)}" fill="none" stroke="#C9CFDB" stroke-width="{f(9*s)}" stroke-linecap="round" opacity="0.8"/>' for dx in (-40, 30))
    return g(id_, o)


def gota_esfuerzo(id_, cx, cy, s=1.0):
    """Gotita de sudor azul con brillo (esfuerzo, nervios)."""
    d = f"M {f(cx)} {f(cy - 30*s)} C {f(cx + 22*s)} {f(cy - 2*s)}, {f(cx + 20*s)} {f(cy + 22*s)}, {f(cx)} {f(cy + 22*s)} C {f(cx - 20*s)} {f(cy + 22*s)}, {f(cx - 22*s)} {f(cy - 2*s)}, {f(cx)} {f(cy - 30*s)} Z"
    return g(id_, f'<path d="{d}" fill="{degradado("#8FD3FF", 0.3)}" stroke="{INK}" stroke-width="{f(5*s)}"/>'
             + brillo(f"M {f(cx - 8*s)} {f(cy)} L {f(cx - 8*s)} {f(cy + 10*s)}", 4 * s, 0.9))


def mando_consola(id_, cx, cy, s=1.0, col="url(#mandoG)"):
    """Mando de videoconsola genérico (≈ 260×160 a s=1): cruceta y 4 botones de colores."""
    w, h = 260 * s, 130 * s
    d = (f"M {f(cx - w*0.32)} {f(cy - h*0.5)} L {f(cx + w*0.32)} {f(cy - h*0.5)} "
         f"C {f(cx + w*0.55)} {f(cy - h*0.5)}, {f(cx + w*0.56)} {f(cy + h*0.9)}, {f(cx + w*0.38)} {f(cy + h*0.72)} "
         f"L {f(cx + w*0.2)} {f(cy + h*0.3)} L {f(cx - w*0.2)} {f(cy + h*0.3)} L {f(cx - w*0.38)} {f(cy + h*0.72)} "
         f"C {f(cx - w*0.56)} {f(cy + h*0.9)}, {f(cx - w*0.55)} {f(cy - h*0.5)}, {f(cx - w*0.32)} {f(cy - h*0.5)} Z")
    o = f'<path d="{d}" fill="{INK}" opacity="0.25" transform="translate(8 10)"/>'
    o += f'<path d="{d}" fill="{col}" stroke="{INK}" stroke-width="{f(7*s)}" stroke-linejoin="round"/>'
    o += brillo(f"M {f(cx - w*0.3)} {f(cy - h*0.36)} L {f(cx + w*0.2)} {f(cy - h*0.36)}", 5 * s, 0.45)
    px, py = cx - w * 0.28, cy - h * 0.02
    a = 13 * s
    o += f'<path d="M {f(px-a)} {f(py-a*3)} h {f(2*a)} v {f(2*a)} h {f(2*a)} v {f(2*a)} h {f(-2*a)} v {f(2*a)} h {f(-2*a)} v {f(-2*a)} h {f(-2*a)} v {f(-2*a)} h {f(2*a)} Z" fill="#11141D" stroke="#6E7690" stroke-width="{f(3*s)}"/>'
    bx, by = cx + w * 0.28, cy - h * 0.02
    for (dx, dy), c in zip(((0, -1), (1, 0), (0, 1), (-1, 0)), (LIME, CORAL, "#3D8BFF", YEL)):
        o += f'<circle cx="{f(bx + dx*24*s)}" cy="{f(by + dy*24*s)}" r="{f(13*s)}" fill="{c}" stroke="{INK}" stroke-width="{f(4*s)}"/>'
    o += "".join(f'<rect x="{f(cx + k*22*s - 12*s)}" y="{f(cy - h*0.12)}" width="{f(24*s)}" height="{f(9*s)}" rx="4" fill="#9AA3B5"/>' for k in (-1, 1))
    return g(id_, o)


def sala_pixel(x0, y0, w, h, px=20, pared="#7B5CFF", suelo="#3FB57A"):
    """Fondo de sala en estilo videojuego pixelado (sin id): pared de ladrillos-píxel y suelo a cuadros."""
    sy = y0 + h * 0.62
    o = f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" fill="{pared}"/>'
    nx, ny = int(w // px), int((sy - y0) // px)
    for j in range(ny):
        for i in range(nx):
            if (i * 7 + j * 3) % 5 == 0:
                o += f'<rect x="{f(x0 + i*px)}" y="{f(y0 + j*px)}" width="{px}" height="{px}" fill="{shade(pared, 0.12 if (i+j) % 2 else -0.1)}"/>'
    o += f'<rect x="{f(x0)}" y="{f(sy)}" width="{f(w)}" height="{f(y0 + h - sy)}" fill="{suelo}"/>'
    for j in range(int((y0 + h - sy) // px) + 1):
        for i in range(nx):
            if (i + j) % 2 == 0:
                o += f'<rect x="{f(x0 + i*px)}" y="{f(sy + j*px)}" width="{px}" height="{f(min(px, y0 + h - sy - j*px))}" fill="{shade(suelo, -0.12)}"/>'
    o += f'<rect x="{f(x0)}" y="{f(sy - px/2)}" width="{f(w)}" height="{f(px/2)}" fill="{shade(pared, -0.3)}"/>'
    return o


def bloque_pixel(cx, base, w, h, col, px=20):
    """Bloque pixelado (mesa o caja de videojuego): rectángulo con borde negro de píxel y brillo cuadrado."""
    x, y = cx - w / 2, base - h
    o = f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" fill="{INK}"/>'
    o += f'<rect x="{f(x + px/2)}" y="{f(y + px/2)}" width="{f(w - px)}" height="{f(h - px)}" fill="{col}"/>'
    o += f'<rect x="{f(x + px/2)}" y="{f(y + px/2)}" width="{f(w - px)}" height="{f(px/2)}" fill="{shade(col, 0.3)}"/>'
    o += f'<rect x="{f(x + px/2)}" y="{f(y + h - px)}" width="{f(w - px)}" height="{f(px/2)}" fill="{shade(col, -0.25)}"/>'
    return o


def avatar_pixel(id_, cx, base, px=12, ropa=CORAL, pelo="#7A4E2B", piel="#F3BE98"):
    """Personaje de videojuego en píxeles (≈ 8×14 píxeles) de pie en (cx, base)."""
    mapa = ["..HHHH..", ".HHHHHH.", ".HSSSSH.", ".SKSSKS.", ".SSSSSS.", "..SSSS..", ".RRRRRR.", "RRRRRRRR",
            "SRRRRRRS", "S.RRRR.S", "..PPPP..", "..PP.PP.", "..PP.PP.", ".ZZZ.ZZZ"]
    cols = {"H": pelo, "S": piel, "K": INK, "R": ropa, "P": "#3E5C93", "Z": "#2A2F3E"}
    x0, y0 = cx - 4 * px, base - len(mapa) * px
    o = sombra(cx, base + 2, px * 5, px * 0.8, 0.25)
    for j, fila in enumerate(mapa):
        for i, c in enumerate(fila):
            if c != ".":
                o += f'<rect x="{f(x0 + i*px)}" y="{f(y0 + j*px)}" width="{px}" height="{px}" fill="{cols[c]}"/>'
    return Pieza(g(id_, o), {"manos": (cx, y0 + 8.5 * px), "cima": (cx, y0)}, (x0, y0, x0 + 8 * px, base))


# ------------------------------------------------------------------ tele, película, edificio
def tele_antigua(id_, cx, base, w=360, texto="FIN DEL CAPÍTULO", patas=True):
    """Televisor de tubo con mueble de madera, antena y pantalla con texto (`{id}_pantalla`)."""
    h = w * 0.78
    x, y = cx - w / 2, base - h - (w * 0.12 if patas else 0)
    o = sombra(cx, base + 4, w * 0.55, 14, 0.22)
    if patas:
        for k in (-1, 1):
            o += trazo(f"M {f(cx + k*w*0.3)} {f(y + h - 6)} L {f(cx + k*w*0.36)} {f(base)}", 10, "#5A3A22", 5)
    for k in (-1, 1):
        o += trazo(f"M {f(cx)} {f(y + 4)} L {f(cx + k*w*0.28)} {f(y - h*0.36)}", 5, "#9AA3B5", 5)
        o += f'<circle cx="{f(cx + k*w*0.28)}" cy="{f(y - h*0.36)}" r="8" fill="#9AA3B5" stroke="{INK}" stroke-width="4"/>'
    o += f'<path d="M {f(cx - w*0.12)} {f(y + 4)} A {f(w*0.12)} {f(w*0.08)} 0 0 1 {f(cx + w*0.12)} {f(y + 4)} Z" fill="#5A3A22" stroke="{INK}" stroke-width="5"/>'
    o += sombra_caja(x, y, w, h, 26, 10, 12, 0.25)
    o += f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="26" fill="url(#teleG)" stroke="{INK}" stroke-width="8"/>'
    sx, sy, sw_, sh_ = x + w * 0.07, y + h * 0.1, w * 0.66, h * 0.8
    pant = f'<rect x="{f(sx)}" y="{f(sy)}" width="{f(sw_)}" height="{f(sh_)}" rx="34" fill="url(#teleScr)" stroke="{INK}" stroke-width="7"/>'
    lines = texto.split(" ")
    mitad = (len(lines) + 1) // 2
    l1, l2 = " ".join(lines[:mitad]), " ".join(lines[mitad:])
    fs = min(sh_ * 0.2, sw_ * 0.85 / (max(len(l1), len(l2), 1) * 0.8))
    pant += T(sx + sw_ / 2, sy + sh_ / 2 - fs * 0.2, l1, fs, "#FFFFFF", font=DISP)
    if l2:
        pant += T(sx + sw_ / 2, sy + sh_ / 2 + fs * 1.05, l2, fs, LIME, font=DISP)
    pant += f'<g stroke="#FFFFFF" stroke-width="2" opacity="0.08">' + "".join(
        f'<line x1="{f(sx + 10)}" y1="{f(yy)}" x2="{f(sx + sw_ - 10)}" y2="{f(yy)}"/>' for yy in [sy + 12 + k * 9 for k in range(int(sh_ / 9) - 2)]) + "</g>"
    pant += brillo(f"M {f(sx + 24)} {f(sy + sh_*0.3)} A {f(sw_*0.4)} {f(sh_*0.4)} 0 0 1 {f(sx + sw_*0.35)} {f(sy + 18)}", 7, 0.35)
    o += g(f"{id_}_pantalla", pant)
    kx = x + w * 0.86
    for k, yy in enumerate((0.25, 0.48)):
        o += f'<circle cx="{f(kx)}" cy="{f(y + h*yy)}" r="{f(w*0.05)}" fill="#3A2A1C" stroke="{INK}" stroke-width="5"/>'
        o += f'<path d="M {f(kx)} {f(y + h*yy)} l {f(w*0.03)} {f(-w*0.025)}" stroke="#D8C7AE" stroke-width="4" stroke-linecap="round"/>'
    o += "".join(f'<line x1="{f(kx - w*0.05)}" y1="{f(y + h*(0.66 + k*0.06))}" x2="{f(kx + w*0.05)}" y2="{f(y + h*(0.66 + k*0.06))}" stroke="#3A2A1C" stroke-width="5" stroke-linecap="round"/>' for k in range(3))
    o += brillo(f"M {f(x + 18)} {f(y + 30)} L {f(x + 18)} {f(y + h - 30)}", 6, 0.4)
    return Pieza(g(id_, o), {"pantalla": (sx + sw_ / 2, sy + sh_ / 2)}, (x, y - h * 0.4, x + w, base))


def tira_pelicula(id_, x0, cy, fotogramas, fw=280, fh=220, sep=26, cortes=True):
    """Tira de película horizontal con perforaciones. fotogramas = lista de funciones f(cx, cy, w, h) → SVG
    (o cadenas «sin coordenadas» ignoradas). Sub-ids: `{id}_f<i>` (cada fotograma), `{id}_n<i>` (número),
    `{id}_corte<i>` (líneas de corte discontinuas entre fotogramas, para draw). .puntos: f<i> = centro, corte<i> = x."""
    n = len(fotogramas)
    W = n * fw + (n + 1) * sep
    H = fh + 110
    y = cy - H / 2
    o = sombra_caja(x0, y, W, H, 14, 10, 12, 0.3)
    o += f'<rect x="{f(x0)}" y="{f(y)}" width="{f(W)}" height="{f(H)}" rx="14" fill="url(#filmG)" stroke="{INK}" stroke-width="7"/>'
    for yy in (y + 18, y + H - 40):
        xx = x0 + 18
        while xx < x0 + W - 36:
            o += f'<rect x="{f(xx)}" y="{f(yy)}" width="24" height="22" rx="5" fill="#EEF2FA" opacity="0.9"/>'
            xx += 44
    puntos = {}
    for i, fn in enumerate(fotogramas):
        fx = x0 + sep + i * (fw + sep)
        fcx, fcy = fx + fw / 2, cy
        cont = fn(fcx, fcy, fw, fh) if callable(fn) else ""
        fr = (f'<clipPath id="{id_}_clip{i}"><rect x="{f(fx)}" y="{f(cy - fh/2)}" width="{f(fw)}" height="{f(fh)}" rx="8"/></clipPath>'
              f'<rect x="{f(fx)}" y="{f(cy - fh/2)}" width="{f(fw)}" height="{f(fh)}" rx="8" fill="#FFF6E0"/>'
              f'<g clip-path="url(#{id_}_clip{i})">{cont}</g>'
              f'<rect x="{f(fx)}" y="{f(cy - fh/2)}" width="{f(fw)}" height="{f(fh)}" rx="8" fill="none" stroke="{INK}" stroke-width="5"/>')
        o += g(f"{id_}_f{i}", fr)
        puntos[f"f{i}"] = (fcx, fcy)
    nums = ""
    for i in range(n):
        fx = x0 + sep + i * (fw + sep)
        nx, ny = fx + fw / 2, cy - fh / 2 - 4
        nums += g(f"{id_}_n{i}", f'<circle cx="{f(nx+3)}" cy="{f(ny+4)}" r="28" fill="{INK}" opacity="0.3"/>'
                  f'<circle cx="{f(nx)}" cy="{f(ny)}" r="28" fill="{LIME}" stroke="{INK}" stroke-width="5"/>' + T(nx, ny + 12, str(i + 1), 34, INK, font=DISP))
    if cortes:
        for i in range(1, n):
            xc = x0 + i * (fw + sep) + sep / 2
            puntos[f"corte{i}"] = xc
            o += g(f"{id_}_corte{i}", f'<path d="M {f(xc)} {f(y - 30)} L {f(xc)} {f(y + H + 30)}" stroke="{LIME}" stroke-width="9" stroke-dasharray="22 14" stroke-linecap="round"/>')
    o += nums
    return Pieza(g(id_, o), puntos, (x0, y, x0 + W, y + H))


def edificio_cupula(id_, cx, base, w=360, col_piedra="url(#piedraG)"):
    """Edificio universitario clásico: fachada de piedra con columnas, frontón y cúpula dorada con estatua."""
    h = w * 0.55
    x, y = cx - w / 2, base - h
    o = sombra(cx, base + 4, w * 0.6, 14, 0.2)
    # cuerpo de la cúpula
    tw, th = w * 0.36, w * 0.24
    o += f'<rect x="{f(cx - tw/2)}" y="{f(y - th)}" width="{f(tw)}" height="{f(th + 10)}" fill="{col_piedra}" stroke="{INK}" stroke-width="6"/>'
    o += "".join(f'<rect x="{f(cx - tw/2 + 10 + k*(tw-20)/4)}" y="{f(y - th + 14)}" width="{f((tw-20)/4 - 10)}" height="{f(th - 26)}" rx="6" fill="#8FA7CF" stroke="{INK}" stroke-width="3"/>' for k in range(4))
    r = tw * 0.55
    o += f'<path d="M {f(cx - r)} {f(y - th)} A {f(r)} {f(r*1.05)} 0 0 1 {f(cx + r)} {f(y - th)} Z" fill="url(#cupulaG)" stroke="{INK}" stroke-width="7"/>'
    o += "".join(f'<path d="M {f(cx + k*r*0.45)} {f(y - th)} Q {f(cx + k*r*0.3)} {f(y - th - r*0.8)} {f(cx)} {f(y - th - r*1.02)}" fill="none" stroke="#B67A0C" stroke-width="3"/>' for k in (-1, 1))
    o += brillo_arco(cx, y - th, r * 0.8, 200, 245, 6, 0.85)
    o += f'<rect x="{f(cx - 5)}" y="{f(y - th - r*1.02 - 34)}" width="10" height="34" fill="url(#cupulaG)" stroke="{INK}" stroke-width="4"/>'
    o += f'<circle cx="{f(cx)}" cy="{f(y - th - r*1.02 - 42)}" r="11" fill="url(#cupulaG)" stroke="{INK}" stroke-width="4"/>'
    # fachada
    o += f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" fill="{col_piedra}" stroke="{INK}" stroke-width="7"/>'
    o += f'<path d="M {f(x - 10)} {f(y + 4)} L {f(cx)} {f(y - h*0.32)} L {f(x + w + 10)} {f(y + 4)} Z" fill="{col_piedra}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
    o += f'<circle cx="{f(cx)}" cy="{f(y - h*0.1)}" r="{f(h*0.09)}" fill="url(#oroG)" stroke="{INK}" stroke-width="4"/>'
    nc = 6
    for k in range(nc):
        colx = x + w * 0.1 + k * w * 0.8 / (nc - 1)
        o += f'<rect x="{f(colx - w*0.025)}" y="{f(y + 18)}" width="{f(w*0.05)}" height="{f(h - 40)}" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/>'
        o += f'<line x1="{f(colx)}" y1="{f(y + 26)}" x2="{f(colx)}" y2="{f(base - 30)}" stroke="#D8C7AE" stroke-width="3"/>'
    o += f'<rect x="{f(cx - w*0.07)}" y="{f(base - h*0.42)}" width="{f(w*0.14)}" height="{f(h*0.42 - 18)}" rx="{f(w*0.07)}" fill="#6B4A2E" stroke="{INK}" stroke-width="4"/>'
    o += f'<rect x="{f(x - 14)}" y="{f(base - 22)}" width="{f(w + 28)}" height="22" fill="#CDBB9E" stroke="{INK}" stroke-width="6"/>'
    o += brillo(f"M {f(x + 12)} {f(y + 14)} L {f(x + 12)} {f(base - 30)}", 5, 0.7)
    return Pieza(g(id_, o), {"cupula": (cx, y - th - r * 0.5)}, (x - 14, y - th - r * 1.02 - 54, x + w + 14, base))


def archivador(id_, cx, base, w=200, h=300, etiqueta=("CAPÍTULO 1", "SALÓN")):
    """Archivador metálico de 2 cajones; el de arriba abierto con una carpeta (`{id}_carpeta`, con etiqueta de 2 líneas).
    .puntos: carpeta (centro de la carpeta), asa (asa del cajón abierto)."""
    x, y = cx - w / 2, base - h
    o = sombra(cx, base + 4, w * 0.6, 12, 0.22)
    o += f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="10" fill="url(#archG)" stroke="{INK}" stroke-width="7"/>'
    dh = h / 2 - 16
    for k in range(2):
        dy = y + 10 + k * (dh + 12)
        o += f'<rect x="{f(x + 12)}" y="{f(dy)}" width="{f(w - 24)}" height="{f(dh)}" rx="8" fill="{degradado("#C3CBD9", 0.15)}" stroke="{INK}" stroke-width="5"/>'
        o += f'<rect x="{f(cx - w*0.16)}" y="{f(dy + dh*0.22)}" width="{f(w*0.32)}" height="{f(dh*0.16)}" rx="4" fill="#FFFFFF" stroke="{INK}" stroke-width="3"/>'
        o += f'<rect x="{f(cx - w*0.18)}" y="{f(dy + dh*0.55)}" width="{f(w*0.36)}" height="{f(dh*0.12)}" rx="6" fill="#6E7690" stroke="{INK}" stroke-width="4"/>'
    o += brillo(f"M {f(x + 8)} {f(y + 16)} L {f(x + 8)} {f(base - 16)}", 5, 0.7)
    # carpeta asomando por arriba
    fw_, fh_ = w * 0.78, h * 0.42
    fcx, fcy = cx, y - fh_ * 0.28
    fx, fy = fcx - fw_ / 2, fcy - fh_ / 2
    c = f'<rect x="{f(fx + 8)}" y="{f(fy + 10)}" width="{f(fw_)}" height="{f(fh_)}" rx="10" fill="{INK}" opacity="0.25"/>'
    c += f'<path d="M {f(fx)} {f(fy + 16)} L {f(fx)} {f(fy)} L {f(fx + fw_*0.4)} {f(fy)} L {f(fx + fw_*0.48)} {f(fy + 16)} Z" fill="#E8AE2E" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    c += f'<rect x="{f(fx)}" y="{f(fy + 16)}" width="{f(fw_)}" height="{f(fh_ - 16)}" rx="10" fill="url(#folderG)" stroke="{INK}" stroke-width="6"/>'
    l1, l2 = etiqueta
    fs = min(fh_ * 0.17, fw_ * 0.86 / (max(len(l1), len(l2)) * 0.8))
    c += f'<rect x="{f(fx + fw_*0.07)}" y="{f(fy + fh_*0.3)}" width="{f(fw_*0.86)}" height="{f(fs*2.9)}" rx="6" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/>'
    c += T(fcx, fy + fh_ * 0.3 + fs * 1.2, l1, fs, INK, font=DISP)
    c += T(fcx, fy + fh_ * 0.3 + fs * 2.45, l2, fs, CORAL, font=DISP)
    o += g(f"{id_}_carpeta", c)
    return Pieza(g(id_, o), {"carpeta": (fcx, fcy), "asa": (fx + fw_, fcy)}, (x, fy, x + w, base))


registrar_defs(lg("folderG", [(0, "#FFD86B"), (1, "#E8AE2E")]))


def birrete(id_, cx, cy, s=1.0, col="#1B1E2B", borla=YEL):
    """Birrete de graduado (≈ 200×110 a s=1) centrado en la base del gorro (cx, cy)."""
    w = 200 * s
    o = f'<path d="M {f(cx - w*0.3)} {f(cy)} L {f(cx - w*0.3)} {f(cy - 34*s)} L {f(cx + w*0.3)} {f(cy - 34*s)} L {f(cx + w*0.3)} {f(cy)} Q {f(cx)} {f(cy + 16*s)} {f(cx - w*0.3)} {f(cy)} Z" fill="{col}" stroke="{INK}" stroke-width="{f(5*s)}"/>'
    top = cy - 40 * s
    d = poly([(cx - w / 2, top), (cx, top - 36 * s), (cx + w / 2, top), (cx, top + 36 * s)], True)
    o += f'<path d="{d}" fill="{degradado("#2A2F40", 0.3)}" stroke="{INK}" stroke-width="{f(6*s)}" stroke-linejoin="round"/>'
    o += brillo(f"M {f(cx - w*0.3)} {f(top - 4*s)} L {f(cx - 8*s)} {f(top - 26*s)}", 4 * s, 0.4)
    o += f'<circle cx="{f(cx)}" cy="{f(top)}" r="{f(7*s)}" fill="{borla}" stroke="{INK}" stroke-width="{f(3*s)}"/>'
    o += trazo(f"M {f(cx)} {f(top)} Q {f(cx + w*0.3)} {f(top + 4*s)} {f(cx + w*0.36)} {f(top + 44*s)}", 4 * s, borla, 4 * s)
    o += f'<rect x="{f(cx + w*0.36 - 8*s)}" y="{f(top + 40*s)}" width="{f(16*s)}" height="{f(30*s)}" rx="{f(5*s)}" fill="{borla}" stroke="{INK}" stroke-width="{f(3*s)}"/>'
    return g(id_, o)

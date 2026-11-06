"""Estilo PAPEL RECORTADO (obligatorio desde el 2-nov). Sale de la muestra C (`muestras/estilos/dib.py`, estilo_c).

Qué hay aquí:
- defs de papel (se registran solos al importar, `svg()` los mete en <defs>):
    url(#papelBorde)  borde irregular + sombra de papel levantado (piezas sueltas)
    url(#papelCapa)   borde irregular + sombra corta (capas dentro de una pieza: brazos, cabeza…)
    url(#papelFino)   borde menos roto para piezas pequeñas (< 120 px) + sombra corta
    url(#papelGrano)  grano para poner ENCIMA de todo (`grano()`)
    url(#papelFibras) fibras blancas para fondos
- paleta cálida apagada `PAPEL` y `EQUIV` (color de base.py → color de papel); `color_papel(hex)` convierte cualquiera.
- `a_papel(pieza, semilla)`: convierte una pieza YA EXISTENTE de la librería (objetos/*.py, persona(), iconos de base).
- `recolorear(svg)`: solo los colores y contornos (sin filtro ni giro).
- `recorte(d, fill, semilla)`: forma suelta de papel. `grano(w, h)`: textura final.
- fondos: `fondo_neutro`, `fondo_cielo(hora)`, `fondo_calle(hora)`, `fondo_casa()` (con capas lejos/medio/cerca para parallax).
- `hoja_transicion(id_, col, texto)`: hoja rasgada que sube y tapa la escena (salida de escena de papel).

Uso típico:
    from libreria.svg.base import *
    from libreria.svg.papel import a_papel, fondo_calle, grano, PAPEL
    from libreria.svg.personajes import persona
    body = fondo_calle(hora="dia")
    body += persona("ana", 400, 1290, 1.2, estilo="papel", expresion="duda", brazos=("relajado", "explica"))
    body += a_papel(TE.bateria("bat", 760, 900, 150, 280, nivel=0.3), semilla=3)
    body += grano()
    guardar("…/escena_full.svg", svg(body, "full"))
"""
import colorsys
import math
import random
import re

from . import base as B
from .base import f, g, poly, smooth, registrar_defs, T, DISP

# ------------------------------------------------------------------ paleta
PAPEL = dict(
    crema="#FBF6EC", hueso="#F3E6CF", carton="#E3C99A", kraft="#C9A27A", tinta="#3A2E2A", tinta_suave="#6B5A50",
    coral="#E86A4A", coral_osc="#C9563B", mostaza="#F2C14E", mostaza_osc="#D9A43A", naranja="#E8925A",
    cielo="#BFD9E2", cielo_tarde="#F2C9A0", cielo_noche="#3F4C68", azul="#6FA8C8", azul_osc="#4B5A7A", azul_marino="#3F4C68",
    salvia="#93B7C9", pizarra="#7FA5BA", verde="#7FBF7A", verde_osc="#5E9A5C", oliva="#A8B86A", lima="#C9D86A",
    terracota="#D98E6A", arena="#E9B872", lavanda="#8FA7C4", violeta="#8B7BB8", rosa="#E99AAE", mejilla="#E99486",
    piel="#F1C7A1", madera="#B98457", gris="#A7A49C", gris_osc="#6E6A64", nieve="#FFFFFF", luz="#F7E6B5",
)
P = PAPEL
TINTA_PAPEL = P["tinta"]

# equivalencias de los colores de base.py (y los más usados de las piezas) → papel
EQUIV = {
    B.INK: P["tinta"], "#000000": P["tinta"], B.LIME: P["lima"], B.CORAL: P["coral"], B.AZUL: P["azul_osc"],
    B.AZUL_OSC: P["azul_marino"], "#FFFFFF": P["crema"], B.PAPEL_GRIS: P["hueso"], B.AMARILLO: P["mostaza"],
    B.NARANJA: P["naranja"], B.TURQUESA: "#5FA89A", B.VIOLETA: P["violeta"], B.ROSA: P["rosa"], B.CIELO: P["cielo"],
    B.AGUA: "#4F86B0", B.VERDE: P["verde_osc"], B.VERDE_CLARO: P["verde"], B.TIERRA: P["carton"], B.MADERA: P["madera"],
    B.GRIS: P["gris"], B.GRIS_OSC: P["gris_osc"], B.PIZARRA: P["azul_osc"], "#FFC83D": P["mostaza"], "#2A2F3E": P["tinta"],
    "#3B80CF": "#5E8FB8", "#3E5C93": P["azul_osc"], "#FF8FA0": P["rosa"], "#7A1F2B": "#7A3B34",
}
EQUIV = {k.upper(): v for k, v in EQUIV.items()}
_CREMA_RGB = (0xF3, 0xE3, 0xC8)


# ------------------------------------------------------------------ colores
def _rgb(c):
    c = c.strip().lstrip("#")
    if len(c) == 3:
        c = "".join(ch * 2 for ch in c)
    if len(c) != 6 or not re.fullmatch(r"[0-9a-fA-F]{6}", c):
        return None
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def _hex(rgb):
    return "#" + "".join(f"{max(0, min(255, int(round(v)))):02X}" for v in rgb)


def _lum(c):
    rgb = _rgb(c)
    if not rgb:
        return None
    return colorsys.rgb_to_hls(*(v / 255 for v in rgb))[1]


def color_papel(c):
    """Convierte un color (hex) a la paleta de papel: equivalencia directa o versión apagada y cálida."""
    if not c or not c.startswith("#"):
        return c
    up = c.upper() if len(c) == 7 else c
    if up in EQUIV:
        return EQUIV[up]
    rgb = _rgb(c)
    if rgb is None:
        return c
    h, l, s = colorsys.rgb_to_hls(*(v / 255 for v in rgb))
    if l > 0.95:
        return P["crema"]
    if l < 0.12:
        return P["tinta"]
    s *= 0.74
    l = l * 0.88 + 0.08
    r, g_, b = colorsys.hls_to_rgb(h, l, s)
    mix = 0.12
    return _hex([(v * 255) * (1 - mix) + cr * mix for v, cr in zip((r, g_, b), _CREMA_RGB)])


def _gradiente(id_):
    """(color_plano, tiene_transparencia) de un degradado registrado en base._DEFS, o (None, None)."""
    d = B._DEFS.get(id_)
    if not d:
        return None, None
    cols = re.findall(r'stop-color="(#[0-9A-Fa-f]{3,6})"', d)
    ops = [float(o) for o in re.findall(r'stop-opacity="([\d.]+)"', d)]
    if not cols:
        return None, None
    trans = any(o < 0.9 for o in ops)
    if len(cols) >= 3:
        plano = cols[len(cols) // 2]
    else:
        a, b = _rgb(cols[0]), _rgb(cols[-1])
        plano = _hex([(x + y) / 2 for x, y in zip(a, b)]) if a and b else cols[0]
    return plano, trans


# ------------------------------------------------------------------ defs
def _filtro_papel(id_, escala=9, freq=0.035, seed=2, dx=3, dy=6, blur=4, op=0.35):
    sombra = ""
    merge = '<feMergeNode in="r"/>'
    if op:
        sombra = ('<feDisplacementMap in="SourceAlpha" in2="n" scale="{e}" xChannelSelector="R" yChannelSelector="G" result="ra"/>'
                  '<feGaussianBlur in="ra" stdDeviation="{b}"/><feOffset dx="{dx}" dy="{dy}" result="sb"/>'
                  '<feFlood flood-color="{c}" flood-opacity="{op}"/><feComposite in2="sb" operator="in" result="sh"/>'
                  ).format(e=escala, b=blur, dx=dx, dy=dy, c=P["tinta"], op=op)
        merge = '<feMergeNode in="sh"/><feMergeNode in="r"/>'
    return (f'<filter id="{id_}" x="-10%" y="-10%" width="120%" height="125%" color-interpolation-filters="sRGB">'
            f'<feTurbulence type="fractalNoise" baseFrequency="{freq}" numOctaves="3" seed="{seed}" result="n"/>'
            f'<feDisplacementMap in="SourceGraphic" in2="n" scale="{escala}" xChannelSelector="R" yChannelSelector="G" result="r"/>'
            f'{sombra}<feMerge>{merge}</feMerge></filter>')


FILTROS = {
    "papelBorde": _filtro_papel("papelBorde"),
    "papelBorde2": _filtro_papel("papelBorde2", seed=7),
    "papelBorde3": _filtro_papel("papelBorde3", seed=13),
    "papelCapa": _filtro_papel("papelCapa", escala=7, seed=4, dx=2, dy=3, blur=2, op=0.3),
    "papelFino": _filtro_papel("papelFino", escala=4, freq=0.06, seed=5, dx=2, dy=3, blur=2, op=0.3),
    "papelPlano": _filtro_papel("papelPlano", escala=9, seed=3, op=0),
    "papelGrano": ('<filter id="papelGrano" x="0" y="0" width="100%" height="100%">'
                   '<feTurbulence type="fractalNoise" baseFrequency="0.75" numOctaves="3" seed="9"/>'
                   '<feColorMatrix values="0 0 0 0 0.23  0 0 0 0 0.18  0 0 0 0 0.16  0 0 0 0.9 0"/></filter>'),
    "papelFibras": ('<filter id="papelFibras" x="0" y="0" width="100%" height="100%">'
                    '<feTurbulence type="fractalNoise" baseFrequency="0.012 0.15" numOctaves="2" seed="5"/>'
                    '<feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.6 -0.1"/></filter>'),
}
for _v in FILTROS.values():
    registrar_defs(_v)


def defs_papel():
    """Todos los filtros de papel en una cadena (por si montas el documento a mano sin svg())."""
    return "".join(FILTROS.values())


def fx(nombre="papelBorde"):
    """Atributo filter listo para meter en un <g>: f'<g{fx()}>…</g>'."""
    return f' filter="url(#{nombre})"'


# ------------------------------------------------------------------ conversión de piezas
_TAG = re.compile(r"<(path|rect|circle|ellipse|polygon|polyline|line|text|g|use|tspan)\b([^>]*?)(/?)>", re.S)
_ATR = re.compile(r'([\w:-]+)="([^"]*)"')


def _es_tinta(c):
    if not c or not c.startswith("#"):
        return False
    l = _lum(c)
    return l is not None and l < 0.13


def _num(v, d=0.0):
    try:
        return float(v)
    except (TypeError, ValueError):
        return d


def recolorear(s, contorno=0.45, brillos=False, bordes=True):
    """Pasa una cadena SVG a papel: quita los contornos de tinta de las formas rellenas, adelgaza (×contorno) y pasa a
    tinta marrón las líneas de detalle, quita el trazo de tinta de debajo de `trazo()`, aplana los degradados opacos a
    su color central, pasa todos los colores a la paleta de papel y quita los brillos blancos (brillos=False).
    Las formas claras (papeles, ojos) o translúcidas (cristal) conservan un contorno fino para que se vean.
    bordes=True: las formas rellenas cambian su contorno de tinta por un filo fino del mismo color algo más oscuro
    (separa dedos, cojines, piezas iguales que solo se distinguían por la tinta); False = sin filo (personas papel)."""
    s = str(s)
    # 1) d de los trazos de color (para borrar su tinta de debajo)
    colores_d = set()
    for m in _TAG.finditer(s):
        a = dict(_ATR.findall(m.group(2)))
        if m.group(1) == "path" and a.get("fill", "none") == "none" and a.get("stroke") and not _es_tinta(a["stroke"]):
            colores_d.add(a.get("d"))

    def rep(m):
        tag, raw, slash = m.group(1), m.group(2), m.group(3)
        attrs = _ATR.findall(raw)
        a = dict(attrs)
        fill, stroke = a.get("fill"), a.get("stroke")
        op = min(_num(a.get("opacity"), 1), _num(a.get("fill-opacity"), 1))
        relleno_trans = False
        # degradados → color plano (los translúcidos se quedan)
        for k in ("fill", "stroke"):
            v = a.get(k)
            if v and v.startswith("url(#"):
                gid = v[5:-1]
                plano, trans = _gradiente(gid)
                if plano and not trans:
                    a[k] = color_papel(plano)
                elif trans and k == "fill":
                    relleno_trans = True
        fill = a.get("fill")
        sin_relleno = fill in (None, "none", "transparent") or tag in ("line", "polyline")
        if tag == "g":
            sin_relleno = fill in (None, "none")
        # brillos: líneas claras con opacidad
        if (not brillos and slash and tag in ("path", "line") and sin_relleno and stroke and stroke.startswith("#")
                and (_lum(stroke) or 0) > 0.82 and _num(a.get("opacity"), 1) < 1):
            return ""
        if stroke and _es_tinta(stroke):
            if tag == "path" and slash and sin_relleno and a.get("d") in colores_d:
                return ""  # tinta de debajo de trazo(): fuera
            claro = fill and fill.startswith("#") and (_lum(fill) or 0) > 0.9
            if sin_relleno or claro or relleno_trans or op < 0.6 or tag in ("text", "tspan"):
                a["stroke"] = P["tinta"]
                w = _num(a.get("stroke-width"), 1) * (contorno if not sin_relleno else max(contorno, 0.55))
                a["stroke-width"] = f(max(2.0, w))
            elif bordes and fill and fill.startswith("#"):
                a["stroke"] = B.shade(color_papel(fill), -0.2)
                a["stroke-width"] = f(max(1.5, _num(a.get("stroke-width"), 6) * 0.3))
            else:
                a["stroke"] = "none"
                a.pop("stroke-width", None)
                a.pop("paint-order", None)
        elif stroke and stroke.startswith("#"):
            a["stroke"] = color_papel(stroke)
        if a.get("fill", "").startswith("#"):
            a["fill"] = color_papel(a["fill"])
        for k in ("flood-color", "stop-color", "color"):
            if a.get(k, "").startswith("#"):
                a[k] = color_papel(a[k])
        keys = [k for k, _ in attrs] + [k for k in a if k not in dict(attrs)]
        out = " ".join(f'{k}="{a[k]}"' for k in keys if k in a)
        return f"<{tag} {out}{' /' if slash else ''}>" if out else f"<{tag}{' /' if slash else ''}>"

    return _TAG.sub(rep, s)


def _id_exterior(s):
    """Si s es UN solo <g id="…">…</g>, devuelve (id, interior); si no, (None, s)."""
    m = re.match(r'\s*<g id="([^"]+)"([^>]*)>', s)
    if not m or m.group(2).strip().endswith("/"):
        return None, s
    depth, i = 0, 0
    for t in re.finditer(r"<(/?)g\b[^>]*?(/?)>", s):
        if t.group(2):
            continue
        depth += -1 if t.group(1) else 1
        if depth == 0:
            i = t.end()
            break
    if s[i:].strip():
        return None, s
    inner = s[m.end():s.rfind("</g>")]
    extra = m.group(2)
    return m.group(1), (f"<g{extra}>{inner}</g>" if extra.strip() else inner)


def a_papel(pieza, semilla=0, giro=None, filtro=None, contorno=0.45, brillos=False, bordes=True):
    """Convierte una pieza YA EXISTENTE de la librería a papel recortado.

    pieza: cadena o Pieza (objetos/*.py, persona(), iconos de base…). semilla: elige giro (±0,6-2°) y variante de borde.
    giro: grados fijos (None = por semilla; 0 = sin giro). filtro: 'papelBorde' (por defecto), 'papelFino' (piezas
    pequeñas o con mucho detalle), 'papelCapa', 'papelPlano' (sin sombra). contorno: grosor que conservan las líneas
    de tinta (0 = las quita todas menos las imprescindibles). bordes: filo fino tono sobre tono (ver recolorear).
    El id exterior se conserva fuera (las anims siguen funcionando) y el giro va en un grupo interior con
    transform-box: fill-box, así gira sobre su propio centro sin desplazarse. Devuelve Pieza con los mismos .puntos/.caja."""
    rnd = random.Random(semilla)
    if giro is None:
        giro = rnd.choice((-1, 1)) * rnd.uniform(0.6, 2.0)
    if filtro is None:  # con texto, borde fino (el desplazamiento grande rompe las letras)
        filtro = "papelFino" if "<text" in str(pieza) else ("papelBorde", "papelBorde2", "papelBorde3")[semilla % 3]
    id_, inner = _id_exterior(str(pieza))
    inner = recolorear(inner, contorno, brillos, bordes)
    if giro:
        inner = (f'<g style="transform:rotate({giro:.2f}deg);transform-box:fill-box;transform-origin:50% 50%">'
                 f"{inner}</g>")
    out = f'<g filter="url(#{filtro})">{inner}</g>'
    if id_:
        out = f'<g id="{id_}">{out}</g>'
    return B.Pieza(out, getattr(pieza, "puntos", None), getattr(pieza, "caja", None))


def recorte(d, fill, semilla=0, filtro="papelBorde", id_=None, giro=None):
    """Forma suelta de papel (path d) con borde irregular, sombra y un giro leve."""
    rnd = random.Random(semilla)
    giro = rnd.uniform(-2, 2) if giro is None else giro
    s = (f'<g filter="url(#{filtro})"><g style="transform:rotate({giro:.2f}deg);transform-box:fill-box;'
         f'transform-origin:50% 50%"><path d="{d}" fill="{fill}"/></g></g>')
    return g(id_, s) if id_ else s


def capa(s, filtro="papelCapa"):
    """Mete el contenido de un grupo con id en un <g filter> interior (la pieza sigue animándose por su id)."""
    id_, inner = _id_exterior(str(s))
    if id_:
        return f'<g id="{id_}"><g filter="url(#{filtro})">{inner}</g></g>'
    return f'<g filter="url(#{filtro})">{s}</g>' if str(s).strip() else ""


def grano(w=1080, h=1920, op=0.16):
    """Textura de grano: ponla AL FINAL del body (encima de todo)."""
    return f'<rect width="{w}" height="{h}" filter="url(#papelGrano)" opacity="{op}" style="mix-blend-mode:multiply" pointer-events="none"/>'


# ------------------------------------------------------------------ fondos
def _fibras(w, h, op=0.5):
    return f'<rect width="{w}" height="{h}" filter="url(#papelFibras)" opacity="{op}"/>'


def fondo_neutro(w=1080, h=1920, col=None, fibras=True, motas=True, seed=4):
    """Cartulina lisa con fibras y unos recortes suaves del mismo tono (sirve para panel, free con fondo o full)."""
    col = col or P["hueso"]
    s = f'<rect width="{w}" height="{h}" fill="{col}"/>'
    if fibras:
        s += _fibras(w, h, 0.55)
    if motas:
        rnd = random.Random(seed)
        for i in range(4):  # recortes muy suaves en los bordes, para que no sea una cartulina muerta
            x = rnd.choice((rnd.uniform(-0.05, 0.12), rnd.uniform(0.88, 1.05))) * w
            y, r = rnd.uniform(0, h), rnd.uniform(min(w, h) * 0.08, min(w, h) * 0.15)
            pts_ = [(x + r * (0.8 + 0.3 * rnd.random()) * math.cos(a * math.pi / 4), y + r * (0.8 + 0.3 * rnd.random()) * math.sin(a * math.pi / 4)) for a in range(8)]
            s += f'<g opacity="0.55">{recorte(smooth(pts_, True), B.shade(col, 0.3 if i % 2 else -0.03), i, "papelPlano")}</g>'
    return s


def _nube(cx, cy, s, col, semilla):
    d = (f"M {f(cx-110*s)} {f(cy+30*s)} Q {f(cx-120*s)} {f(cy-30*s)} {f(cx-60*s)} {f(cy-28*s)} Q {f(cx-40*s)} {f(cy-80*s)} {f(cx+10*s)} {f(cy-60*s)} "
         f"Q {f(cx+60*s)} {f(cy-90*s)} {f(cx+80*s)} {f(cy-30*s)} Q {f(cx+130*s)} {f(cy-20*s)} {f(cx+115*s)} {f(cy+30*s)} Z")
    return recorte(d, col, semilla)


def fondo_cielo(hora="dia", w=1080, h=1920, astro=(300, 560), nubes=True, id_astro="astro"):
    """Cielo de papel: hora 'dia' (sol), 'tarde' (sol bajo y cálido) o 'noche' (luna y estrellas).
    El astro va en su grupo `id_astro` (anímalo con spin lento o float). Nubes en `nube0..2` (drift)."""
    cielo = {"dia": P["cielo"], "tarde": P["cielo_tarde"], "noche": P["cielo_noche"]}[hora]
    s = f'<rect width="{w}" height="{h}" fill="{cielo}"/>' + _fibras(w, h, 0.5 if hora != "noche" else 0.18)
    ax, ay = astro
    if hora == "noche":
        luna = (f'<path d="M {f(ax+40)} {f(ay-100)} A 105 105 0 1 0 {f(ax+40)} {f(ay+100)} A 80 80 0 1 1 {f(ax+40)} {f(ay-100)} Z" fill="{P["luz"]}"/>')
        s += g(id_astro, f'<g filter="url(#papelBorde)">{luna}</g>')
        rnd = random.Random(8)
        est = ""
        for i in range(14):
            x, y, r = rnd.uniform(40, w - 40), rnd.uniform(120, h * 0.55), rnd.uniform(7, 13)
            est += f'<path d="{poly([(x + (r if k % 2 == 0 else r*0.42) * math.cos(k*math.pi/4 - math.pi/2), y + (r if k % 2 == 0 else r*0.42) * math.sin(k*math.pi/4 - math.pi/2)) for k in range(8)], True)}" fill="{P["crema"]}"/>'
        s += g(f"{id_astro}_estrellas", f'<g filter="url(#papelFino)">{est}</g>')
    else:
        col = P["luz"] if hora == "dia" else "#F2A766"
        rayos = "".join(f'<path d="{poly([(ax + 130*math.cos(a-0.12), ay + 130*math.sin(a-0.12)), (ax + 185*math.cos(a), ay + 185*math.sin(a)), (ax + 130*math.cos(a+0.12), ay + 130*math.sin(a+0.12))], True)}" fill="{col}"/>'
                        for a in [i * math.pi / 6 for i in range(12)])
        s += g(id_astro, f'<g filter="url(#papelBorde)">{rayos}<circle cx="{f(ax)}" cy="{f(ay)}" r="110" fill="{col}"/></g>')
    if nubes:
        cn = P["crema"] if hora != "noche" else "#56627E"
        for i, (x, y, k) in enumerate(((760, 430, 1.0), (180, 900, 0.8), (880, 820, 0.7))):
            s += g(f"nube{i}", _nube(x * w / 1080, y * h / 1920, k, cn, i + 2))
    return s


def _edificio(x, w_, h_, suelo, col, rt, seed, tejado=True, encendidas=0.33):
    rnd = random.Random(seed)
    y = suelo - h_
    win = "".join(f'<rect x="{f(x+20+c*52)}" y="{f(y+40+r*72)}" width="26" height="34" fill="{P["luz"] if rnd.random() < encendidas else P["azul_osc"]}"/>'
                  for r in range(int(h_ // 80)) for c in range(max(1, int((w_ - 20) // 52))))
    techo = f'<path d="M {f(x-14)} {f(y+6)} L {f(x+w_/2)} {f(y-70)} L {f(x+w_+14)} {f(y+6)} Z" fill="{P["crema"]}"/>' if tejado else \
        f'<rect x="{f(x-10)}" y="{f(y-14)}" width="{f(w_+20)}" height="22" fill="{P["crema"]}"/>'
    return (f'<g filter="url(#papelBorde)"><g transform="rotate({rt} {f(x+w_/2)} {f(suelo)})">'
            f'<rect x="{f(x)}" y="{f(y)}" width="{f(w_)}" height="{f(h_+30)}" fill="{col}"/>{techo}{win}</g></g>')


def fondo_calle(hora="dia", w=1080, h=1920, suelo=1290, capas=("lejos", "medio", "cerca"), farola=True):
    """Calle de papel: cielo (fondo_cielo), lejos = montes de cartulina, medio = edificios con ventanas, cerca = acera y
    farola. Las capas van en grupos `capas` para el parallax (pan −14 / −40 / −110 en 6 s) y sobran 200 px por cada lado."""
    s = fondo_cielo(hora, w, h, astro=(300, 560))
    noche = hora == "noche"
    lejos = ""
    for x, y, w_, col, rt in ((-200, 1020, 600, P["salvia"], -2), (230, 960, 660, P["pizarra"], 1.5), (720, 1040, 620, P["salvia"], -1)):
        col = B.shade(col, -0.35) if noche else col
        lejos += (f'<g filter="url(#papelBorde)"><g transform="rotate({rt} {x+w_/2} {suelo})"><path d="M {x} {suelo+20} L {x+w_*0.5} {y-240} L {x+w_} {suelo+20} Z" fill="{col}"/></g></g>')
    medio = ""
    for i, (x, w_, h_, col, rt) in enumerate(((-150, 230, 330, P["terracota"], -2.5), (100, 160, 250, P["arena"], 2), (300, 140, 190, P["lavanda"], -1),
                                               (690, 180, 380, P["lavanda"], 1.5), (890, 250, 290, P["terracota"], -2))):
        col = B.shade(col, -0.3) if noche else col
        medio += _edificio(x, w_, h_, suelo, col, rt, i + 1, tejado=i % 2 == 0, encendidas=0.6 if noche else 0.3)
    cerca = (f'<g filter="url(#papelBorde)"><path d="M -240 {suelo+10} Q 200 {suelo-30} 600 {suelo} Q 900 {suelo+20} 1320 {suelo-16} L 1320 {h+40} L -240 {h+40} Z" fill="{P["hueso"] if not noche else "#B9B2A6"}"/></g>'
             f'<g filter="url(#papelCapa)"><path d="M -240 {suelo+70} L 1320 {suelo+56} L 1320 {suelo+84} L -240 {suelo+98} Z" fill="{P["carton"]}"/></g>')
    if farola:
        cerca += (f'<g filter="url(#papelBorde)"><rect x="892" y="{suelo-540}" width="24" height="540" fill="{P["azul_marino"]}"/>'
                  f'<path d="M 848 {suelo-540} L 960 {suelo-540} L 934 {suelo-600} L 874 {suelo-600} Z" fill="{P["azul_marino"]}"/>'
                  f'<ellipse cx="904" cy="{suelo-532}" rx="40" ry="12" fill="{P["luz"]}"/></g>')
        if noche:
            cerca += f'<path d="M 870 {suelo-526} L 938 {suelo-526} L 1010 {suelo} L 798 {suelo} Z" fill="{P["luz"]}" opacity="0.18"/>'
    cerca += (f'<g filter="url(#papelBorde)"><path d="M -60 {suelo+20} Q -40 {suelo-120} 60 {suelo-110} Q 130 {suelo-170} 190 {suelo-80} Q 240 {suelo-60} 230 {suelo+20} Z" fill="{P["verde_osc"]}"/>'
              f'<path d="M 0 {suelo} Q 40 {suelo-90} 110 {suelo-80} Q 150 {suelo-40} 160 {suelo} Z" fill="{P["verde"]}"/></g>')
    s += g(capas[0], lejos) + g(capas[1], medio) + g(capas[2], cerca)
    return s


def fondo_casa(w=1080, h=1920, suelo=1290, pared=None, noche=False, capas=("lejos", "medio", "cerca")):
    """Interior de casa: pared con papel pintado a rayas, ventana (día o noche), cuadro y zócalo (lejos), estantería
    con libros y lámpara (medio), suelo de tarima y planta (cerca)."""
    pared = pared or P["arena"]
    s = f'<rect width="{w}" height="{h}" fill="{pared}"/>' + _fibras(w, h, 0.45)
    s += "".join(f'<rect x="{x}" y="0" width="34" height="{suelo}" fill="{B.shade(pared, 0.18)}" opacity="0.55"/>' for x in range(20, w + 80, 120))
    cielo = P["cielo_noche"] if noche else P["cielo"]
    lejos = (f'<g filter="url(#papelBorde)"><rect x="560" y="560" width="380" height="440" fill="{P["crema"]}"/>'
             f'<rect x="588" y="588" width="324" height="384" fill="{cielo}"/>'
             + (f'<circle cx="840" cy="680" r="42" fill="{P["luz"]}"/>' if noche else f'<path d="M 620 900 Q 700 820 780 900 Q 840 850 900 920 L 900 972 L 620 972 Z" fill="{P["verde"]}"/><circle cx="840" cy="670" r="40" fill="{P["luz"]}"/>')
             + f'<rect x="745" y="588" width="12" height="384" fill="{P["crema"]}"/><rect x="588" y="775" width="324" height="12" fill="{P["crema"]}"/></g>'
             f'<g filter="url(#papelCapa)"><path d="M 540 540 Q 600 760 580 1020 L 520 1020 L 520 540 Z" fill="{P["coral"]}"/>'
             f'<path d="M 960 540 Q 900 760 920 1020 L 980 1020 L 980 540 Z" fill="{P["coral"]}"/>'
             f'<rect x="510" y="526" width="480" height="20" rx="8" fill="{P["madera"]}"/></g>'
             f'<g filter="url(#papelBorde2)"><g transform="rotate(-3 220 640)"><rect x="120" y="560" width="200" height="160" fill="{P["madera"]}"/>'
             f'<rect x="138" y="578" width="164" height="124" fill="{P["crema"]}"/><path d="M 150 690 L 205 620 L 245 670 L 270 640 L 292 690 Z" fill="{P["azul"]}"/></g></g>'
             f'<g filter="url(#papelCapa)"><rect x="-240" y="{suelo-60}" width="{w+480}" height="60" fill="{P["crema"]}"/></g>')
    libros = ""
    rnd = random.Random(3)
    x = 50
    for i in range(7):
        bw = rnd.uniform(26, 40)
        bh = rnd.uniform(80, 110)
        libros += f'<rect x="{f(x)}" y="{f(900-bh)}" width="{f(bw)}" height="{f(bh)}" fill="{(P["coral"], P["azul"], P["mostaza"], P["verde_osc"], P["lavanda"])[i % 5]}"/>'
        x += bw + 4
    medio = (f'<g filter="url(#papelBorde)"><rect x="30" y="900" width="320" height="22" fill="{P["madera"]}"/>'
             f'<rect x="30" y="1060" width="320" height="22" fill="{P["madera"]}"/>{libros}'
             f'<path d="M 120 1060 Q 140 980 200 990 Q 250 960 280 1060 Z" fill="{P["verde"]}"/></g>')
    cerca = (f'<g filter="url(#papelPlano)"><rect x="-240" y="{suelo}" width="{w+480}" height="{h-suelo+40}" fill="{P["madera"]}"/>'
             + "".join(f'<rect x="-240" y="{suelo + 18 + k*90}" width="{w+480}" height="6" fill="{B.shade(P["madera"], -0.2)}"/>' for k in range(7))
             + "</g>"
             f'<g filter="url(#papelBorde3)"><path d="M 900 {suelo+10} L 1010 {suelo+10} L 990 {suelo-110} L 920 {suelo-110} Z" fill="{P["terracota"]}"/>'
             f'<path d="M 955 {suelo-110} Q 860 {suelo-260} 900 {suelo-330} Q 950 {suelo-240} 955 {suelo-110} Z" fill="{P["verde_osc"]}"/>'
             f'<path d="M 955 {suelo-110} Q 1060 {suelo-280} 1030 {suelo-360} Q 980 {suelo-260} 955 {suelo-110} Z" fill="{P["verde"]}"/>'
             f'<path d="M 955 {suelo-110} Q 940 {suelo-300} 960 {suelo-420} Q 990 {suelo-300} 955 {suelo-110} Z" fill="{P["oliva"]}"/></g>')
    s += g(capas[0], lejos) + g(capas[1], medio) + g(capas[2], cerca)
    return s


# ------------------------------------------------------------------ transiciones
def hoja_transicion(id_="salida", col=None, texto="?", col_texto=None, w=1080, h=1920):
    """Hoja de papel rasgada que espera DEBAJO del encuadre (y > h). Con la anim
    {"target": id_, "effect": "pan", "delay": <fin-0,8>, "to": [0, -(h+100)], "rotate": -3, "dur": 0.75, "sfx": "papel"}
    sube y tapa la escena (salida de papel). texto = lo que lleva escrito (None = nada)."""
    col = col or P["mostaza"]
    col_texto = col_texto or P["coral"]
    rnd = random.Random(5)
    borde = [(x, h + 60 + rnd.uniform(-22, 22)) for x in range(-80, w + 120, 40)]
    d = poly([(-80, h + 2200)] + borde + [(w + 80, h + 2200)], True)
    s = f'<g transform="rotate(3 {w/2} {h+1070})"><g filter="url(#papelBorde)"><path d="{d}" fill="{col}"/></g>'
    if texto:
        s += T(w / 2, h + 1160, texto, 300, col_texto, font=DISP)
    return g(id_, s + "</g>")

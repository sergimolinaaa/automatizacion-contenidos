"""Muestrario de estilo: la misma escena de gancho (frío → el móvil pierde batería) en 3 direcciones.
Uso: python3 muestras/estilos/dib.py   → muestras/estilos/{A,B,C}/gancho_full.svg + guion.json

A «Actual pulido»: pegatina de ahora + luz/sombra suave, contorno de grosor variable (filtro), textura y 3 planos.
B «Flat premium»: formas planas sin contorno, paleta corta, sombras largas, brillos geométricos.
C «Papel recortado»: bordes irregulares (filtro de desplazamiento), sombra de papel, grano y rotaciones leves.
Las tres usan los efectos nuevos del motor: squash, move+antic, pan (parallax), flutter, puff, fall, jitter.
"""
import json
import math
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from libreria.svg.base import *  # noqa
from libreria.svg.personajes import persona
from libreria.svg.objetos import casa as K, tecnologia as TE
from libreria.svg.objetos.mente import pivote

HERE = Path(__file__).resolve().parent
W, H = 1080, 1920
SUELO = 1290
PCTS = ("40 %", "31 %", "22 %", "13 %", "6 %", "1 %")
PCT_T = (None, 2.55, 2.95, 3.35, 3.75, 4.15)  # cuándo entra cada cifra (s desde el inicio de la escena)


def ancla(id_):
    return f'<g id="{id_}"></g>'


# ======================================================================= piezas comunes de animación
def anims_comunes(tel="tel", chico="chico", cab="chico_cabeza", ojos=("chico_ojos",), brazo_izq="chico_brazo_izq",
                  brazo_der="chico_brazo_der", cara_frio=None, cara_sorpresa=None, n_copos=16, n_vaho=3, extra=(), zoom=((600, 900), 1.2)):
    A = []
    # cámara: zoom lento + paneo; antes del acercón al móvil, un pequeño retroceso (anticipación de cámara)
    A += [{"target": "camera", "effect": "zoom", "delay": 0, "to": [500, 930], "amount": 1.08, "dur": 2.6},
          {"target": "camera", "effect": "zoom", "delay": 2.9, "to": [520, 960], "amount": 1.03, "dur": 0.35},
          {"target": "camera", "effect": "zoom", "delay": 3.2, "to": list(zoom[0]), "amount": zoom[1], "dur": 1.3}]
    # parallax: cada plano se desplaza distinto (lejos poco, cerca mucho)
    A += [{"target": "lejos", "effect": "pan", "delay": 0, "to": [-14, 0], "dur": 6},
          {"target": "medio", "effect": "pan", "delay": 0, "to": [-40, 0], "dur": 6},
          {"target": "cerca", "effect": "pan", "delay": 0, "to": [-110, 0], "dur": 6}]
    # entrada con squash and stretch + persona viva
    A += [{"target": chico, "effect": "squash", "delay": 0, "dur": 0.6, "sfx": "boing"},
          {"target": chico, "effect": "breathe", "origin": "bottom", "amount": 0.6, "phase": 0.2, "delay": 0.7},
          {"target": chico, "effect": "sway", "origin": "bottom", "amount": 0.1, "delay": 0.8},
          {"target": cab, "effect": "sway", "origin": "bottom", "amount": 0.25, "delay": 1.05},
          {"target": brazo_izq, "effect": "sway", "origin": "top-right", "amount": 0.14, "delay": 0.9}]
    A += [{"target": o, "effect": "blink", "delay": 0.9} for o in ojos]
    # frío: tiembla, rayitas, la cabeza se encoge (anticipa hacia arriba y baja)
    A += [{"target": chico, "effect": "shake", "trigger": "frío", "amount": 0.28},
          {"target": "temb", "effect": "pop", "trigger": "frío", "sfx": "pop"},
          {"target": "temb", "effect": "wiggle", "trigger": "frío", "amount": 0.5},
          {"target": cab, "effect": "move", "trigger": "frío", "to": [0, 10], "rotate": -4, "antic": 0.4, "origin": "bottom", "dur": 0.5}]
    # bufanda y pompón: movimiento secundario con retraso
    A += [{"target": "bufanda", "effect": "flutter", "origin": "top", "amount": 0.8, "phase": 0.1, "delay": 0.25},
          {"target": "pompon", "effect": "sway", "origin": "bottom", "amount": 0.6, "delay": 0.45}]
    # partículas: vaho del aliento y copos que caen
    A += [{"target": f"vh{i}", "effect": "puff", "delay": 0.3, "phase": i / n_vaho, "to": [70, -110]} for i in range(n_vaho)]
    rnd = random.Random(11)
    for i in range(n_copos):
        A += [{"target": f"cp{i}", "effect": "fall", "delay": 0, "amount": rnd.uniform(0.7, 1.3), "phase": rnd.random(), "to": [0, 1500]},
              {"target": f"cp{i}", "effect": "drift", "delay": 0, "amount": rnd.uniform(0.4, 1.0), "phase": rnd.random()},
              {"target": f"cp{i}", "effect": "spin", "delay": 0, "amount": rnd.uniform(0.05, 0.15)}]
    # saca el móvil: anticipación (baja un poco) y lo levanta
    A += [{"target": tel, "effect": "punch", "trigger": "batería", "amount": 0.3, "sfx": "pop"}]
    # la batería cae en picado: nivel que baja, cifras que se relevan y tiemblan
    A += [{"target": "carga", "effect": "pan", "trigger": "batería", "to": [0, 0], "dur": 2.0},  # sustituida por cada estilo
          {"target": "pct_grp", "effect": "jitter", "delay": 2.5, "amount": 0.9}]
    for i, t in enumerate(PCT_T):
        idn = "pct" if i == len(PCTS) - 1 else f"pct_{i}"
        if i + 1 < len(PCTS):
            nxt = PCT_T[i + 1]
            A.append({"target": idn, "effect": "hide", "delay": nxt})
        if t is not None:
            A.append({"target": idn, "effect": "fade", "delay": t, "dur": 0.1, **({"sfx": "chasquido"} if i == 1 else {})})
    A += [{"target": "carga_roja", "effect": "fade", "delay": 3.3, "dur": 0.3},
          {"target": "alerta", "effect": "squash", "delay": 3.7, "dur": 0.5, "to": [0, -160], "sfx": "sorpresa"},
          {"target": "alerta", "effect": "wiggle", "delay": 4.2, "amount": 0.5},
          {"target": tel, "effect": "shake", "delay": 4.15, "amount": 0.35},
          {"target": "pct", "effect": "punch", "delay": 4.15, "amount": 0.5}]
    if cara_frio:
        A += [{"target": cara_sorpresa, "effect": "hide"},
              {"target": cara_frio, "effect": "hide", "delay": 3.7},
              {"target": cara_sorpresa, "effect": "fade", "delay": 3.7, "dur": 0.15}]
    A += list(extra)
    return A


def poner_carga(A, dy):
    for a in A:
        if a["target"] == "carga":
            a["to"] = [0, dy]
    A.append({"target": "carga_roja", "effect": "pan", "trigger": "batería", "to": [0, dy], "dur": 2.0})
    return A


def guion(estilo, nombre, anims):
    return {
        "topic": f"Muestrario de estilo {estilo} ({nombre}): gancho del frío y la batería. NO PUBLICAR.",
        "categoria": "moviles",
        "title": "¿Por qué el frío se come tu batería?",
        "source": "Muestra de estilo",
        "chapters": ["?", "1", "2", "3", "+", "TÚ"],
        "scenes": [{
            "chapter": 0, "headline": "¿Se *congela* la batería?",
            "narration": "¿Por qué el frío se come tu batería?",
            "illustration": {"svg_file": "gancho_full.svg", "layout": "full", "caption": f"Estilo {estilo}", "anims": anims}}],
    }


def bateria_pantalla(cx, cy, w, h, col_ok, col_mal, marco, fondo, texto_col, txt_extra=""):
    """Batería grande en la pantalla: carga (verde) y carga_roja que bajan con pan dentro de un recorte.
    Devuelve (svg, dy) con dy = cuánto baja la carga para quedarse casi vacía."""
    x0, y0 = cx - w / 2, cy - h / 2
    pad = w * 0.1
    ix0, iy0, iw, ih = x0 + pad, y0 + pad, w - 2 * pad, h - 2 * pad
    nivel = 0.4
    top = iy0 + ih * (1 - nivel)
    clip = f'<clipPath id="clipCarga"><rect x="{f(ix0)}" y="{f(iy0)}" width="{f(iw)}" height="{f(ih)}" rx="{f(w*0.06)}"/></clipPath>'
    s = clip
    s += f'<rect x="{f(cx-w*0.18)}" y="{f(y0-h*0.07)}" width="{f(w*0.36)}" height="{f(h*0.08)}" rx="6" fill="{marco}"/>'
    s += f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" rx="{f(w*0.14)}" fill="{marco}"/>'
    s += f'<rect x="{f(ix0-3)}" y="{f(iy0-3)}" width="{f(iw+6)}" height="{f(ih+6)}" rx="{f(w*0.08)}" fill="{fondo}"/>'
    lvl = f'<rect x="{f(ix0)}" y="{f(top)}" width="{f(iw)}" height="{f(ih*nivel+4)}" fill="{{c}}"/>'
    s += (f'<g clip-path="url(#clipCarga)">' + g("carga", lvl.format(c=col_ok) + txt_extra)
          + g("carga_roja", lvl.format(c=col_mal)) + "</g>")
    dy = ih * nivel * 0.97
    return s, dy


def cifras(cx, cy, size, col, extra=""):
    return g("pct_grp", "".join(g("pct" if i == len(PCTS) - 1 else f"pct_{i}", T(cx, cy, v, size, col, font=DISP, extra=extra))
                                for i, v in enumerate(PCTS)))


# ======================================================================= A · ACTUAL PULIDO
def estilo_a():
    INKC = INK
    defs = (
        # contorno de grosor variable: la silueta dilatada y desplazada abajo-derecha queda más gruesa en la sombra
        '<filter id="contorno" x="-10%" y="-10%" width="120%" height="120%">'
        '<feMorphology in="SourceAlpha" operator="dilate" radius="2.5" result="d"/>'
        '<feOffset in="d" dx="4" dy="6" result="o"/>'
        f'<feFlood flood-color="{INKC}"/><feComposite in2="o" operator="in" result="s"/>'
        '<feMerge><feMergeNode in="s"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
        '<filter id="grano" x="0" y="0" width="100%" height="100%">'
        '<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="4"/>'
        '<feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.55 0"/></filter>'
        '<filter id="difuso"><feGaussianBlur stdDeviation="14"/></filter>'
        + rg("luzA", [(0, "#FFFFFF", 0.55), (1, "#FFFFFF", 0)], cx=0.25, cy=0.15, r=0.75)
        + rg("sombraA", [(0, "#0B1A40", 0), (1, "#0B1A40", 0.38)], cx=0.4, cy=0.35, r=0.85)
        + lg("cieloA", [(0, "#6EC3FF"), (0.6, "#BFE6FF"), (1, "#EAF6FF")])
    )
    fondo = f'<rect width="{W}" height="{H}" fill="url(#cieloA)"/>'
    fondo += f'<circle cx="230" cy="560" r="150" fill="#FFFFFF" opacity="0.55" filter="url(#difuso)"/>'
    # --- lejos: montañas nevadas
    lejos = ""
    for x, y, w_, col in ((-120, 1080, 520, "#9CC7EE"), (260, 1010, 620, "#86B6E6"), (720, 1060, 560, "#9CC7EE")):
        d = f"M {x} {SUELO} L {x+w_*0.5} {y-260} L {x+w_} {SUELO} Z"
        lejos += f'<path d="{d}" fill="{degradado(col, 0.18)}" stroke="#4E79B5" stroke-width="5" stroke-linejoin="round"/>'
        nieve = f"M {x+w_*0.36} {y-150} L {x+w_*0.5} {y-260} L {x+w_*0.64} {y-150} Q {x+w_*0.57} {y-125} {x+w_*0.5} {y-150} Q {x+w_*0.43} {y-125} {x+w_*0.36} {y-150} Z"
        lejos += f'<path d="{nieve}" fill="#FFFFFF" stroke="#4E79B5" stroke-width="5" stroke-linejoin="round"/>'
    # --- medio: edificios con ventanas, sombra y brillo
    medio = ""
    rnd = random.Random(3)
    for x, w_, h_, col in ((-90, 210, 420, "#5C7FC4"), (130, 170, 330, "#7495D8"), (690, 190, 470, "#5C7FC4"),
                           (890, 260, 360, "#7495D8")):
        y = SUELO - h_
        medio += sombra_caja(x, y, w_, h_, rx=10, dx=12, dy=0, op=0.18)
        medio += f'<rect x="{x}" y="{y}" width="{w_}" height="{h_}" rx="10" fill="{degradado(col, 0.25)}" stroke="{INK}" stroke-width="7"/>'
        medio += f'<rect x="{x-8}" y="{y-16}" width="{w_+16}" height="26" rx="13" fill="#FFFFFF" stroke="{INK}" stroke-width="6"/>'
        for r_ in range(int(h_ // 80)):
            for c_ in range(int(w_ // 60)):
                on = rnd.random() < 0.35
                medio += (f'<rect x="{x+22+c_*60}" y="{y+40+r_*80}" width="30" height="42" rx="5" '
                          f'fill="{"#FFE27A" if on else "#3B5596"}" stroke="{INK}" stroke-width="4"/>')
        medio += brillo(f"M {x+14} {y+30} L {x+14} {y+h_*0.5}", 6, 0.5)
    # --- cerca: montón de nieve en primer plano y farola
    cerca = (f'<path d="M -150 {SUELO} Q 300 {SUELO-40} 700 {SUELO-10} Q 1000 {SUELO-30} 1300 {SUELO} L 1300 1920 L -150 1920 Z" '
             f'fill="{degradado("#F4F9FF", 0.14)}"/>')
    cerca += brillo(f"M -40 {SUELO+8} Q 300 {SUELO-26} 680 {SUELO+4}", 7, 0.9)
    cerca += (f'<rect x="882" y="760" width="26" height="540" rx="10" fill="{degradado("#3B4560", 0.3)}"/>'
              f'<path d="M 840 760 L 950 760 L 925 700 L 865 700 Z" fill="{degradado("#3B4560", 0.3)}" stroke-linejoin="round"/>'
              f'<ellipse cx="895" cy="770" rx="44" ry="14" fill="#FFE27A"/>'
              f'<path d="M 838 700 Q 895 670 952 700" fill="#FFFFFF"/>')
    cerca += (f'<path d="M 1120 1400 Q 960 1300 840 1420 Q 1000 1380 1120 1460 Z" fill="#FFFFFF"/>')
    body = g("lejos", lejos)
    body += g("medio", medio)
    body += g("cerca", f'<g filter="url(#contorno)">{cerca}</g>')
    # --- personaje (librería) con luz, sombra y contorno variable
    x0, y0 = 380, 1300
    kw = dict(edad="joven", piel="clara", pelo="corto", pelo_color="castano", ropa="abrigo", ropa_color="#2F6FD9",
              pantalon_color="#2A3045", accesorios=("gorro", "bufanda"), bufanda_color=CORAL, brazos=("relajado", "sujeta"), mira=1)
    pf = persona("chf", x0, y0, 1.22, expresion="frio", **kw)
    ps = persona("chs", x0, y0, 1.22, expresion="sorpresa", **kw)
    mx, my = pf.puntos["mano_der"]
    hi, hd = pf.puntos["hombro_izq"], pf.puntos["hombro_der"]
    nx, ny = (hi[0] + hd[0]) / 2, (hi[1] + hd[1]) / 2
    body += f'<ellipse cx="{x0+20}" cy="{y0+6}" rx="200" ry="26" fill="#0B1A40" opacity="0.28" filter="url(#difuso)"/>'
    cola = (f'<path d="M {f(nx+18)} {f(ny-4)} q 22 70 6 150 l 46 -6 q 6 -80 -12 -146 z" fill="{degradado(CORAL, 0.3)}" '
            f'stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
            f'<path d="M {f(nx+30)} {f(ny+120)} l 40 -6" stroke="#FFFFFF" stroke-width="8" opacity="0.8"/>'
            f'<path d="M {f(nx+24)} {f(ny+60)} l 34 -4" stroke="#FFFFFF" stroke-width="8" opacity="0.8"/>')
    # pompón propio sobre el gorro (movimiento secundario)
    cx_, cy_ = pf.puntos["cima"]
    pompon = (f'<circle cx="{f(cx_)}" cy="{f(cy_-18)}" r="30" fill="{degradado("#FFFFFF", 0.25)}" stroke="{INK}" stroke-width="6"/>'
              + pivote(cx_, cy_ - 18 + 8, 38))
    luz = (f'<g style="mix-blend-mode:soft-light"><rect x="{x0-260}" y="{y0-760}" width="560" height="770" fill="url(#luzA)"/></g>'
)
    chico = g("chico_caras", g("chf", pf) + g("chs", ps)) + g("bufanda", cola)
    body += g("chico", f'<g filter="url(#contorno)">{chico}</g>' + f'<g opacity="0.6">{luz}</g>')
    # --- móvil con la batería
    w = 170
    cx, cy = mx + 14, my - 118
    sx0, sy0, sx1, sy1 = TE.pantalla_movil(cx, cy, w)
    bat, dy = bateria_pantalla(cx, cy - 30, 78, 150, VERDE, CORAL, "#FFFFFF", "#10204F", "#FFFFFF")
    pant = (f'<rect x="{f(sx0)}" y="{f(sy0)}" width="{f(sx1-sx0)}" height="{f(sy1-sy0)}" fill="{degradado("#2347FF", 0.35)}"/>'
            + bat + cifras(cx, cy + 100, 40, "#FFFFFF"))
    body += g("tel", f'<g filter="url(#contorno)">{K.movil(None, cx, cy, w, pantalla=pant)}</g>'
              + brillo(f"M {f(cx-w*0.36)} {f(cy-w*0.7)} L {f(cx-w*0.36)} {f(cy-w*0.2)}", 8, 0.5))
    bx, by = pf.puntos["boca"]
    body += "".join(g(f"vh{i}", f'<circle cx="{f(bx+40)}" cy="{f(by-6)}" r="22" fill="#FFFFFF" stroke="#7FA6CC" stroke-width="4"/>')
                    for i in range(3))
    body += g("temb", temblor(x0 - 230, 860, 100, "#5BC0FF") + temblor(x0 + 190, 1010, 90, "#5BC0FF"))
    body += g("alerta", f'<g filter="url(#contorno)">{icono_alerta(None, cx + 175, cy + 60, 54, CORAL)}</g>')
    rnd = random.Random(7)
    for i in range(16):
        x = 40 + (i * 67) % 1000 + rnd.uniform(-20, 20)
        body += g(f"cp{i}", copo(x, 950 + rnd.uniform(-60, 60), rnd.uniform(14, 24), rnd.uniform(0, 60), col="#FFFFFF" if i % 3 else "#CFE8FF"))
    # textura sutil sobre todo
    body += f'<rect width="{W}" height="{H}" filter="url(#grano)" opacity="0.10" style="mix-blend-mode:multiply"/>'
    # salida: iris azul que nace del móvil
    body += g("salida", f'<circle cx="{f(cx)}" cy="{f(cy)}" r="2300" fill="{AZUL}"/>'
              + T(cx, cy + 40, "?", 260, LIME, font=DISP, extra=f'stroke="{INK}" stroke-width="12" paint-order="stroke"'))
    A = anims_comunes(chico="chico", cab="chf_cabeza", ojos=("chf_ojos", "chs_ojos"), brazo_izq="chf_brazo_izq",
                      brazo_der="chf_brazo_der", cara_frio="chf", cara_sorpresa="chs", zoom=((560, 1000), 1.12), extra=[
                          {"target": "chs_cabeza", "effect": "sway", "origin": "bottom", "amount": 0.25, "delay": 1.05},
                          {"target": "chs_brazo_izq", "effect": "sway", "origin": "top-right", "amount": 0.14, "delay": 0.9},
                          {"target": "tel", "effect": "squash", "trigger": "come", "to": [0, 170], "dur": 0.55, "amount": 0.7, "sfx": "whoosh"},
                          {"target": "chf_brazo_der", "effect": "move", "trigger": "come", "rotate": -8, "antic": 0.5, "origin": "top-left", "dur": 0.55},
                          {"target": "chs_brazo_der", "effect": "move", "trigger": "come", "rotate": -8, "antic": 0.5, "origin": "top-left", "dur": 0.55},
                          {"target": "pompon", "effect": "move", "trigger": "frío", "rotate": 12, "origin": "bottom", "dur": 0.8},
                          {"target": "salida", "effect": "pop", "delay": 5.2, "sfx": "whoosh"}])
    return body, defs, poner_carga(A, dy)


# ======================================================================= figura plana (B y C)
def figura(P, papel=""):
    """Personaje de formas simples para B y C. P = paleta. papel = atributo filter para cada pieza (C)."""
    fx = papel
    x = 400
    s = ""
    s += f'<g{fx}><rect x="348" y="1120" width="40" height="175" rx="18" fill="{P["pant"]}"/><rect x="410" y="1120" width="40" height="175" rx="18" fill="{P["pant_osc"]}"/></g>'
    s += f'<g{fx}><rect x="330" y="1272" width="70" height="30" rx="14" fill="{P["zap"]}"/><rect x="404" y="1272" width="70" height="30" rx="14" fill="{P["zap"]}"/></g>'
    # brazo izquierdo (pantalla) detrás del cuerpo
    bi = (f'<g{fx}><path d="M 300 905 Q 262 1000 270 1100 L 312 1104 Q 318 1010 336 930 Z" fill="{P["abrigo_osc"]}"/>'
          f'<circle cx="291" cy="1112" r="24" fill="{P["piel"]}"/></g>')
    s += g("chico_brazo_izq", bi)
    # abrigo
    s += (f'<g{fx}><path d="M 300 890 Q 400 860 500 890 L 530 1150 Q 400 1172 270 1150 Z" fill="{P["abrigo"]}"/>'
          + (f'<path d="M 400 870 L 400 1160 L 530 1150 L 500 890 Q 450 874 400 870 Z" fill="{P["abrigo_sombra"]}" opacity="{P["sombra_op"]}"/>' if P.get("abrigo_sombra") else "")
          + f'<circle cx="400" cy="960" r="9" fill="{P["boton"]}"/><circle cx="400" cy="1030" r="9" fill="{P["boton"]}"/><circle cx="400" cy="1100" r="9" fill="{P["boton"]}"/></g>')
    # bufanda: vuelta al cuello + cola que ondea
    s += f'<g{fx}><rect x="312" y="858" width="176" height="52" rx="26" fill="{P["bufanda"]}"/></g>'
    cola = (f'<g{fx}><path d="M 430 890 L 486 890 L 500 1030 L 444 1036 Z" fill="{P["bufanda_osc"]}"/>'
            f'<path d="M 440 960 L 494 956 L 497 984 L 442 988 Z" fill="{P["bufanda"]}"/>'
            f'<path d="M 444 1036 l 4 22 M 462 1034 l 4 22 M 480 1032 l 4 22 M 497 1030 l 4 22" stroke="{P["bufanda_osc"]}" stroke-width="7" stroke-linecap="round"/></g>')
    s += g("bufanda", cola + '<rect x="308" y="890" width="300" height="300" fill="none"/>')
    # cabeza
    cab = f'<g{fx}><circle cx="{x}" cy="790" r="86" fill="{P["piel"]}"/>'
    if P.get("geo"):  # brillo geométrico (semicírculo de luz) del flat
        cab += f'<path d="M {x-86} 790 A 86 86 0 0 1 {x+86} 790 Z" fill="#FFFFFF" opacity="0.10"/>'
        cab += f'<path d="M {x+30} 720 A 86 86 0 0 1 {x+86} 790 L {x+56} 790 A 56 56 0 0 0 {x+20} 742 Z" fill="#FFFFFF" opacity="0.22"/>'
    cab += f'<ellipse cx="{x-48}" cy="828" rx="20" ry="12" fill="{P["mejilla"]}"/><ellipse cx="{x+52}" cy="828" rx="20" ry="12" fill="{P["mejilla"]}"/></g>'
    ojos = f'<ellipse cx="{x-26}" cy="792" rx="10" ry="14" fill="{P["ojo"]}"/><ellipse cx="{x+38}" cy="792" rx="10" ry="14" fill="{P["ojo"]}"/>'
    cab += g("chico_ojos", ojos)
    cab += g("cara_frio", f'<path d="M {x-14} 845 q 9 -10 18 0 q 9 10 18 0 q 9 -10 18 0" fill="none" stroke="{P["ojo"]}" stroke-width="6" stroke-linecap="round"/>'
             f'<path d="M {x-44} 762 l 26 8 M {x+56} 762 l -26 8" stroke="{P["ojo"]}" stroke-width="6" stroke-linecap="round"/>')
    cab += g("cara_sorpresa", f'<ellipse cx="{x+8}" cy="848" rx="14" ry="18" fill="{P["ojo"]}"/>'
             f'<path d="M {x-44} 756 q 14 -12 28 -4 M {x+56} 756 q -14 -12 -28 -4" fill="none" stroke="{P["ojo"]}" stroke-width="6" stroke-linecap="round"/>')
    # gorro
    cab += (f'<g{fx}><path d="M {x-90} 760 Q {x-86} 650 {x} 648 Q {x+86} 650 {x+90} 760 Z" fill="{P["gorro"]}"/>'
            f'<rect x="{x-96}" y="738" width="192" height="40" rx="20" fill="{P["gorro_osc"]}"/></g>')
    pomp = f'<g{fx}><circle cx="{x}" cy="640" r="30" fill="{P["pompon"]}"/></g>' + pivote(x, 648, 40)
    cab += g("pompon", pomp)
    s += g("chico_cabeza", cab + f'<rect x="{x-240}" y="560" width="480" height="320" fill="none"/>')
    return s


def brazo_movil(P, papel, pantalla_svg, cx=640, cy=860, w=170):
    """Brazo derecho que sostiene el móvil (todo en un grupo con pivote en el hombro (500, 905))."""
    fx = papel
    h = w * 1.95
    s = (f'<g{fx}><path d="M 488 900 Q 560 960 590 1040 L 632 1012 Q 602 930 516 880 Z" fill="{P["abrigo_osc"]}"/>'
         f'<path d="M 590 1040 Q 610 1000 622 960 L 660 978 Q 650 1020 628 1050 Z" fill="{P["abrigo_osc"]}"/></g>')
    tel = f'<g{fx}><rect x="{f(cx-w/2)}" y="{f(cy-h/2)}" width="{w}" height="{f(h)}" rx="30" fill="{P["tel"]}"/>'
    tel += f'<rect x="{f(cx-w/2+10)}" y="{f(cy-h/2+12)}" width="{w-20}" height="{f(h-24)}" rx="22" fill="{P["pantalla"]}"/>'
    tel += pantalla_svg + "</g>"
    s += g("tel", tel)
    s += f'<g{fx}><circle cx="{cx-w/2+6}" cy="{cy+128}" r="30" fill="{P["piel"]}"/><rect x="{cx-w/2+10}" y="{cy+96}" width="20" height="44" rx="10" fill="{P["piel"]}"/></g>'
    return g("chico_brazo_der", s + pivote(500, 905, 330))


def anims_figura(extra=()):
    A = anims_comunes(chico="chico", cab="chico_cabeza", ojos=("chico_ojos",), cara_frio="cara_frio", cara_sorpresa="cara_sorpresa")
    # el brazo empieza bajado (móvil en el bolsillo), anticipa hacia abajo y lo levanta
    A += [{"target": "chico_brazo_der", "effect": "move", "delay": 0, "rotate": 62, "origin": "center", "dur": 0.05},
          {"target": "chico_brazo_der", "effect": "move", "trigger": "come", "rotate": -62, "antic": 0.18, "origin": "center", "dur": 0.7, "sfx": "whoosh"},
          {"target": "chico_brazo_der", "effect": "sway", "origin": "center", "amount": 0.08, "delay": 2.4}]
    A += list(extra)
    return A


# ======================================================================= B · FLAT PREMIUM
PB = dict(fondo_a="#14213D", fondo_b="#2B3F75", lejos="#2E4A86", medio="#3C5FA6", cerca="#E9F1FB", sombra="#0E1830",
          pant="#22305A", pant_osc="#1B274B", zap="#0E1830", abrigo="#FF6B5B", abrigo_osc="#E2554A", abrigo_sombra="#C9463E",
          sombra_op=0.45, boton="#FFD166", bufanda="#FFD166", bufanda_osc="#F2B53A", piel="#F6C9A8", mejilla="#F29A8A",
          ojo="#14213D", gorro="#4CC9F0", gorro_osc="#3AA9D0", pompon="#FFFFFF", tel="#0E1830", pantalla="#4CC9F0", geo=True)


def estilo_b():
    P = PB
    defs = lg("cieloB", [(0, P["fondo_a"]), (1, P["fondo_b"])])
    fondo = f'<rect width="{W}" height="{H}" fill="url(#cieloB)"/>'
    # luna con anillos geométricos: mucho espacio negativo
    fondo += "".join(f'<circle cx="790" cy="610" r="{r}" fill="#FFFFFF" opacity="{op}"/>' for r, op in ((260, 0.04), (190, 0.06), (120, 0.95)))
    fondo += '<circle cx="830" cy="580" r="120" fill="#E9F1FB"/><circle cx="760" cy="640" r="18" fill="#D2DEEF"/><circle cx="830" cy="560" r="10" fill="#D2DEEF"/>'
    # lejos: colinas planas
    lejos = (f'<path d="M -120 {SUELO} L -120 1080 Q 160 940 420 1060 Q 700 1180 1000 1020 Q 1120 980 1200 1000 L 1200 {SUELO} Z" fill="{P["lejos"]}"/>')
    # medio: edificios con sombras largas a 45°
    medio = ""
    for x, w_, h_ in ((-60, 170, 360), (150, 120, 250), (700, 150, 420), (880, 220, 300)):
        y = SUELO - h_
        L = 520
        medio += f'<path d="M {x+w_} {y} L {x+w_+L} {y+L} L {x+w_+L} {SUELO} L {x+w_} {SUELO} Z" fill="{P["sombra"]}" opacity="0.22"/>'
        medio += f'<rect x="{x}" y="{y}" width="{w_}" height="{h_}" fill="{P["medio"]}"/>'
        medio += f'<rect x="{x+w_*0.62}" y="{y}" width="{w_*0.38}" height="{h_}" fill="{P["sombra"]}" opacity="0.18"/>'
        for r_ in range(int(h_ // 70)):
            for c_ in range(int(w_ // 50)):
                on = (r_ * 3 + c_ * 7 + x) % 5 == 0
                medio += f'<rect x="{x+18+c_*50}" y="{y+30+r_*70}" width="22" height="30" fill="{"#FFD166" if on else "#2E4A86"}"/>'
    # cerca: suelo nevado y farola minimal
    cerca = f'<rect x="-200" y="{SUELO}" width="1500" height="700" fill="{P["cerca"]}"/>'
    cerca += f'<rect x="-200" y="{SUELO}" width="1500" height="16" fill="#FFFFFF"/>'
    cerca += f'<path d="M 520 {SUELO} L 1300 {SUELO+420} L 1300 {SUELO} Z" fill="#C9D8EE" opacity="0.6"/>'  # sombra larga del personaje
    cerca += (f'<rect x="900" y="800" width="18" height="{SUELO-800}" fill="{P["sombra"]}"/><rect x="862" y="790" width="94" height="22" rx="11" fill="{P["sombra"]}"/>'
              f'<path d="M 875 812 L 943 812 L 1000 1000 L 818 1000 Z" fill="#FFD166" opacity="0.14"/>')
    body = g("lejos", lejos) + g("medio", medio) + g("cerca", cerca)
    # personaje: sombra larga + figura plana
    body += f'<path d="M 330 1300 L 470 1300 L 900 1700 L 700 1700 Z" fill="#B7C9E6" opacity="0.55"/>'
    bat, dy = bateria_pantalla(640, 820, 80, 150, "#7BE0AD", "#FF6B5B", "#FFFFFF", "#22305A", "#FFFFFF")
    pant = bat + cifras(640, 960, 40, "#FFFFFF") + '<path d="M 575 700 L 625 700 L 560 780 L 560 740 Z" fill="#FFFFFF" opacity="0.25"/>'
    body += g("chico", figura(P) + brazo_movil(P, "", pant))
    body += "".join(g(f"vh{i}", f'<circle cx="455" cy="842" r="20" fill="#FFFFFF" opacity="0.85"/>') for i in range(3))
    body += g("temb", "".join(f'<rect x="{x}" y="{y}" width="10" height="56" rx="5" fill="#4CC9F0"/>' for x, y in ((210, 880), (230, 930), (560, 1080))))
    body += g("alerta", '<circle cx="800" cy="680" r="62" fill="#FF6B5B"/><rect x="792" y="640" width="16" height="54" rx="8" fill="#FFFFFF"/><circle cx="800" cy="716" r="9" fill="#FFFFFF"/>')
    rnd = random.Random(7)
    for i in range(16):
        x = 40 + (i * 67) % 1000 + rnd.uniform(-20, 20)
        r = rnd.uniform(5, 11)
        body += g(f"cp{i}", f'<circle cx="{f(x)}" cy="{f(950+rnd.uniform(-60, 60))}" r="{f(r)}" fill="#FFFFFF" opacity="{0.6 + 0.4*(i%2)}"/>')
    # salida: dos bandas diagonales que barren la pantalla
    for i, col in enumerate(("#FF6B5B", P["fondo_a"])):
        body += g(f"salida{i}", f'<path d="M -3200 -200 L -1100 -200 L -1700 2200 L -3800 2200 Z" fill="{col}"/>'
                  + (T(-2760, 1080, "?", 300, "#FFD166", font=DISP) if i else ""))
    A = anims_figura(extra=[{"target": "salida0", "effect": "pan", "delay": 5.1, "to": [3300, 0], "dur": 0.7, "sfx": "whoosh"},
                            {"target": "salida1", "effect": "pan", "delay": 5.25, "to": [3300, 0], "dur": 0.7}])
    return body, defs, poner_carga(A, dy)


# ======================================================================= C · PAPEL RECORTADO
PC = dict(pant="#4B5A7A", pant_osc="#3F4C68", zap="#3A2E2A", abrigo="#E86A4A", abrigo_osc="#C9563B", abrigo_sombra=None,
          sombra_op=0, boton="#F3D9A4", bufanda="#F2C14E", bufanda_osc="#D9A43A", piel="#F1C7A1", mejilla="#E99486",
          ojo="#3A2E2A", gorro="#6FA8C8", gorro_osc="#5A90AE", pompon="#FBF6EC", tel="#3A2E2A", pantalla="#9BC8D8", geo=False)


def estilo_c():
    P = PC
    defs = (
        # papel: bordes irregulares + sombra de papel levantado
        '<filter id="papel" x="-8%" y="-8%" width="116%" height="116%">'
        '<feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="3" seed="2" result="n"/>'
        '<feDisplacementMap in="SourceGraphic" in2="n" scale="9" xChannelSelector="R" yChannelSelector="G" result="r"/>'
        '<feGaussianBlur in="r" stdDeviation="0" result="r2"/>'
        '<feComponentTransfer in="SourceAlpha" result="a"><feFuncA type="linear" slope="1"/></feComponentTransfer>'
        '<feDisplacementMap in="a" in2="n" scale="9" xChannelSelector="R" yChannelSelector="G" result="ra"/>'
        '<feGaussianBlur in="ra" stdDeviation="4"/><feOffset dx="3" dy="6" result="sb"/>'
        '<feFlood flood-color="#3A2E2A" flood-opacity="0.35"/><feComposite in2="sb" operator="in" result="sh"/>'
        '<feMerge><feMergeNode in="sh"/><feMergeNode in="r2"/></feMerge></filter>'
        '<filter id="granoC" x="0" y="0" width="100%" height="100%">'
        '<feTurbulence type="fractalNoise" baseFrequency="0.75" numOctaves="3" seed="9"/>'
        '<feColorMatrix values="0 0 0 0 0.23  0 0 0 0 0.18  0 0 0 0 0.16  0 0 0 0.9 0"/></filter>'
        '<filter id="fibras" x="0" y="0" width="100%" height="100%">'
        '<feTurbulence type="fractalNoise" baseFrequency="0.012 0.15" numOctaves="2" seed="5"/>'
        '<feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.6 -0.1"/></filter>'
    )
    fp = ' filter="url(#papel)"'
    fondo = f'<rect width="{W}" height="{H}" fill="#BFD9E2"/>'
    fondo += f'<rect width="{W}" height="{H}" filter="url(#fibras)" opacity="0.5"/>'
    fondo += f'<g{fp}><g transform="rotate(-3 300 560)"><circle cx="300" cy="560" r="110" fill="#F7E6B5"/></g></g>'
    # lejos: montañas de cartulina
    lejos = ""
    for x, y, w_, col, rt in ((-140, 1020, 560, "#93B7C9", -2), (250, 960, 640, "#7FA5BA", 1.5), (700, 1040, 560, "#93B7C9", -1)):
        lejos += (f'<g{fp}><g transform="rotate({rt} {x+w_/2} {SUELO})"><path d="M {x} {SUELO+20} L {x+w_*0.5} {y-240} L {x+w_} {SUELO+20} Z" fill="{col}"/>'
                  f'<path d="M {x+w_*0.38} {y-150} L {x+w_*0.5} {y-240} L {x+w_*0.62} {y-150} L {x+w_*0.55} {y-170} L {x+w_*0.5} {y-140} L {x+w_*0.44} {y-172} Z" fill="#FBF6EC"/></g></g>')
    # medio: casitas de papel
    medio = ""
    for x, w_, h_, col, rt in ((-60, 200, 330, "#D98E6A", -2.5), (150, 150, 250, "#E9B872", 2), (700, 170, 380, "#8FA7C4", 1.5), (890, 230, 290, "#D98E6A", -2)):
        y = SUELO - h_
        win = "".join(f'<rect x="{x+20+c*52}" y="{y+40+r*72}" width="26" height="34" fill="{"#F7E6B5" if (r+c+x) % 3 == 0 else "#4B5A7A"}"/>'
                      for r in range(int(h_ // 80)) for c in range(int(w_ // 55)))
        medio += (f'<g{fp}><g transform="rotate({rt} {x+w_/2} {SUELO})"><rect x="{x}" y="{y}" width="{w_}" height="{h_+20}" fill="{col}"/>'
                  f'<path d="M {x-14} {y+6} L {x+w_/2} {y-70} L {x+w_+14} {y+6} Z" fill="#FBF6EC"/>{win}</g></g>')
    cerca = (f'<g{fp}><path d="M -200 {SUELO+10} Q 200 {SUELO-36} 600 {SUELO} Q 900 {SUELO+24} 1300 {SUELO-20} L 1300 1960 L -200 1960 Z" fill="#FBF6EC"/></g>'
             f'<g{fp}><g transform="rotate(4 980 1440)"><path d="M 860 1500 Q 980 1340 1140 1460 L 1140 1560 L 860 1560 Z" fill="#FFFFFF"/></g></g>')
    body = g("lejos", lejos) + g("medio", medio) + g("cerca", cerca)
    bat, dy = bateria_pantalla(640, 820, 80, 150, "#7FBF7A", "#E86A4A", "#FBF6EC", "#4B5A7A", "#FBF6EC")
    pant = bat + cifras(640, 960, 40, "#3A2E2A")
    # la figura entera con un leve giro de collage
    body += g("chico", f'<g transform="rotate(-1.5 400 1300)">' + figura(P, fp) + brazo_movil(P, fp, pant) + "</g>")
    body += "".join(g(f"vh{i}", f'<g{fp}><circle cx="455" cy="842" r="22" fill="#FBF6EC"/></g>') for i in range(3))
    body += g("temb", f'<g{fp}>' + "".join(f'<path d="M {x} {y} l 14 0 l -6 60 l -14 0 Z" fill="#6FA8C8"/>' for x, y in ((205, 880), (232, 940), (565, 1080))) + "</g>")
    body += g("alerta", f'<g{fp}><g transform="rotate(8 800 680)"><path d="M 800 600 L 880 740 L 720 740 Z" fill="#F2C14E"/>'
              f'<rect x="792" y="640" width="16" height="60" fill="#3A2E2A"/><rect x="792" y="710" width="16" height="16" fill="#3A2E2A"/></g></g>')
    rnd = random.Random(7)
    for i in range(16):
        x = 40 + (i * 67) % 1000 + rnd.uniform(-20, 20)
        r = rnd.uniform(9, 16)
        y = 950 + rnd.uniform(-60, 60)
        body += g(f"cp{i}", f'<g{fp}><path d="{poly([(x+r*math.cos(a*math.pi/3+0.3), y+r*math.sin(a*math.pi/3+0.3)) for a in range(6)], True)}" fill="#FFFFFF"/></g>')
    body += f'<rect width="{W}" height="{H}" filter="url(#granoC)" opacity="0.16" style="mix-blend-mode:multiply"/>'
    # salida: una hoja de papel rasgada sube y tapa la escena
    hoja = (f'<g transform="rotate(3 540 2990)"><g{fp}><path d="M -80 1980 L 1160 1980 L 1160 4000 L -80 4000 Z" fill="#F3D9A4"/></g>'
            + T(540, 3080, "?", 300, "#E86A4A", font=DISP) + "</g>")
    body += g("salida", hoja)
    A = anims_figura(extra=[{"target": "salida", "effect": "pan", "delay": 5.15, "to": [0, -2020], "rotate": -3, "dur": 0.75, "sfx": "papel"}])
    return body, defs, poner_carga(A, dy)


if __name__ == "__main__":
    for estilo, nombre, fn in (("A", "Actual pulido", estilo_a), ("B", "Flat premium", estilo_b), ("C", "Papel recortado", estilo_c)):
        out = HERE / estilo
        out.mkdir(parents=True, exist_ok=True)
        body, defs, A = fn()
        fondo = None
        if estilo == "A":
            fondo = '<rect width="1080" height="1920" fill="url(#cieloA)"/><circle cx="230" cy="560" r="150" fill="#FFFFFF" opacity="0.55" filter="url(#difuso)"/>'
        elif estilo == "B":
            fondo = ('<rect width="1080" height="1920" fill="url(#cieloB)"/>'
                     + "".join(f'<circle cx="790" cy="610" r="{r}" fill="#FFFFFF" opacity="{op}"/>' for r, op in ((260, 0.04), (190, 0.06)))
                     + '<circle cx="790" cy="610" r="120" fill="#E9F1FB"/><circle cx="752" cy="640" r="18" fill="#D2DEEF"/><circle cx="820" cy="570" r="10" fill="#D2DEEF"/>')
        else:
            fondo = ('<rect width="1080" height="1920" fill="#BFD9E2"/><rect width="1080" height="1920" filter="url(#fibras)" opacity="0.5"/>'
                     '<g filter="url(#papel)"><g transform="rotate(-3 300 560)"><circle cx="300" cy="560" r="110" fill="#F7E6B5"/></g></g>')
        guardar(out / "gancho_full.svg", svg(body, "full", fondo=fondo, defs=defs))
        (out / "guion.json").write_text(json.dumps(guion(estilo, nombre, A), ensure_ascii=False, indent=1), encoding="utf-8")

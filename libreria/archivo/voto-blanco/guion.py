import json, re

OUT = "/home/user/automatizacion-contenidos/content/lote6-03-voto-en-blanco/guion.json"


def A(target, effect, trigger=None, **kw):
    a = {"target": target, "effect": effect}
    if trigger:
        a["trigger"] = trigger
    a.update(kw)
    return a


def hides(*ids):
    return [A(i, "hide") for i in ids]


scenes = [
    {
        "chapter": 0,
        "headline": "¿Castigar a *todos*?",
        "narration": "Si el 29-N votas en blanco para castigar a todos… mira esto.",
        "illustration": {
            "svg_file": "gancho_full.svg", "layout": "full", "caption": "Fig. 1 · Un sobre vacío",
            "anims": hides("tsinpap", "valido", "tvalido", "tley") + [
                A("sobre", "bob", amount=0.6),
                A("t29", "pop", "29-N", sfx="ding"),
                A("urna", "punch", "votas", amount=0.2),
                A("tblanco", "pop", "blanco", sfx="pop"),
                A("tcast", "pop", "castigar", sfx="sello"),
                A("partidos", "shake", "castigar", amount=0.5),
                A("partidos", "punch", "todos", amount=0.2),
                A("duda", "pop", "mira", sfx="sorpresa"),
                A("duda", "pulse", amount=0.6),
            ],
        },
    },
    {"chapter": 0, "signature": True, "headline": "El truco es…", "narration": "El truco es…"},
    {
        "chapter": 1, "number": "1",
        "headline": "Blanco = *válido*",
        "narration": "Sin posicionarnos: solo cómo funciona. Votar en blanco es meter el sobre sin papeleta. Y la ley lo cuenta como voto válido.",
        "elements": [{"type": "tag", "text": "SIN POSICIONARNOS", "tone": "ink", "trigger": "posicionarnos"}],
        "illustration": {
            "svg_file": "gancho_full.svg", "layout": "full", "caption": "Fig. 2 · LOREG, art. 96.5",
            "anims": hides("t29", "tcast", "duda", "partidos") + [
                A("tblanco", "punch", "blanco", amount=0.25),
                A("sobre", "move", "meter", to=[0, 95], dur=0.6, sfx="whoosh"),
                A("tsinpap", "pop", "papeleta", sfx="papel"),
                A("sobre", "hide", "ley"),
                A("urna", "punch", "ley", amount=0.25),
                A("tley", "pop", "ley", sfx="sello"),
                A("valido", "pop", "válido", sfx="ding"),
                A("tvalido", "pop", "válido"),
                A("valido", "pulse", amount=0.5),
            ],
        },
    },
    {
        "chapter": 1, "number": "1",
        "headline": "Ningún escaño *vacío*",
        "narration": "No deja escaños vacíos: todos se reparten entre los partidos.",
        "illustration": {
            "svg_file": "hemi_free.svg", "layout": "free", "height": 820, "caption": "Fig. 3 · 30 de 30",
            "anims": hides("nuevo", "anillo", "c2circle", "c2diamond", "fuera", "tpasa") + [
                A("asientos", "grow", "escaños", dur=0.6, sfx="pop"),
                A("cero", "pop", "vacíos", sfx="sello"),
                A("t30", "pop", "todos", sfx="ding"),
                A("asientos", "punch", "reparten", amount=0.15),
                A("chips", "slide-up", "partidos", dur=0.5, sfx="whoosh"),
            ],
        },
    },
    {
        "chapter": 2, "number": "2",
        "headline": "El listón del *3 %*",
        "narration": "Pero suma al total de votos válidos. Y para entrar en el reparto del Congreso, cada partido necesita el 3 % de ese total en su provincia.",
        "illustration": {
            "svg_file": "liston.svg", "caption": "Fig. 4 · LOREG, art. 163.1",
            "anims": hides("t3000", "t3270", "v109", "tmas", "monton", "entra", "nollega", "t3100") + [
                A("v100", "pop", "suma", sfx="ding"),
                A("v100", "punch", "válidos", amount=0.2),
                A("liston", "slide-right", "entrar", dur=0.6, sfx="whoosh"),
                A("t3", "pop", "3", sfx="pop"),
                A("rombo", "slide-up", "partido", dur=0.5, sfx="whoosh"),
                A("tley", "pop", "provincia", sfx="sello"),
            ],
        },
    },
    {
        "chapter": 2, "number": "2",
        "headline": "Rombo *entra*",
        "narration": "Imagina una provincia con 100.000 votos válidos. Listón: 3.000. El partido Rombo tiene 3.100: entra.",
        "illustration": {
            "svg_file": "liston.svg", "caption": "Fig. 5 · Partidos ficticios",
            "anims": hides("t3", "t3270", "v109", "tmas", "tley", "monton", "nollega") + [
                A("v100", "punch", "100.000", amount=0.25),
                A("liston", "punch", "Listón", amount=0.15),
                A("t3000", "pop", "3.000", sfx="pop"),
                A("rombo", "punch", "Rombo", amount=0.2),
                A("t3100", "pop", "3.100", sfx="pop"),
                A("entra", "pop", "entra", sfx="ding"),
                A("entra", "pulse", amount=0.4),
            ],
        },
        "mascot": {"trigger": "Rombo", "pose": "cheer", "note": "¡Por los pelos!", "side": "left"},
    },
    {
        "chapter": 3, "number": "3",
        "headline": "El listón *sube*",
        "narration": "Ahora llegan 9.000 votos en blanco de castigo. Hay 109.000 válidos, y el listón sube a 3.270.",
        "illustration": {
            "svg_file": "liston.svg", "caption": "Fig. 6 · Mismos votos",
            "anims": hides("t3", "t3270", "v109", "tmas", "tley", "monton", "entra", "nollega") + [
                A("monton", "slide-up", "9.000", dur=0.5, sfx="papel"),
                A("tmas", "pop", "blanco", sfx="pop"),
                A("monton", "punch", "castigo", amount=0.2),
                A("v100", "hide", "109.000"),
                A("v109", "pop", "109.000", sfx="ding"),
                A("liston", "move", "sube", to=[0, -135], dur=0.8, sfx="whoosh"),
                A("t3000", "hide", "3.270"),
                A("t3270", "pop", "3.270", sfx="pop"),
                A("nollega", "pop", "3.270", sfx="sello"),
                A("rombo", "shake", "3.270", amount=0.4),
            ],
        },
    },
    {
        "chapter": 3, "number": "3",
        "headline": "Rombo, *fuera*",
        "narration": "Rombo, con los mismos votos, se queda fuera. Y su escaño pasa a otro partido.",
        "illustration": {
            "svg_file": "hemi_free.svg", "layout": "free", "height": 820, "caption": "Fig. 7 · Provincia de 30 escaños",
            "anims": hides("cero", "t30") + [
                A("anillo", "pop", "Rombo", sfx="pop"),
                A("anillo", "pulse", amount=0.5),
                A("cdiamond", "punch", "mismos", amount=0.25),
                A("cdiamond", "hide", "fuera"),
                A("c2diamond", "pop", "fuera", sfx="sello"),
                A("fuera", "pop", "fuera"),
                A("nuevo", "pop", "escaño", sfx="pop"),
                A("ccircle", "hide", "otro"),
                A("c2circle", "pop", "otro", sfx="ding"),
                A("tpasa", "pop", "partido", sfx="pop"),
            ],
        },
    },
    {
        "chapter": 4, "number": "+",
        "headline": "¿Y el *nulo*?",
        "narration": "¿Y el nulo? No cuenta para el 3 %. La abstención, tampoco. Solo el blanco sube el listón.",
        "illustration": {
            "svg_file": "cuenta_full.svg", "layout": "full", "caption": "Fig. 8 · LOREG, arts. 96 y 163",
            "anims": [
                A("zzz", "bob", amount=0.6),
                A("cnulo", "pop", "nulo", sfx="pop"),
                A("sn", "pop", "nulo"),
                A("kon", "pop", "No", sfx="pop"),
                A("vn", "pop", "cuenta"),
                A("titulo", "punch", "3", amount=0.2),
                A("cabst", "pop", "abstención", sfx="pop"),
                A("sa", "pop", "abstención"),
                A("koa", "pop", "tampoco", sfx="pop"),
                A("va", "pop", "tampoco"),
                A("cblanco", "punch", "Solo", amount=0.15),
                A("okb", "pop", "blanco", sfx="ding"),
                A("vb", "pop", "blanco"),
                A("sube", "slide-up", "sube", dur=0.5, sfx="whoosh"),
            ],
        },
    },
    {
        "chapter": 5, "number": "TÚ",
        "headline": "*Confiesa*",
        "narration": "Síguenos para más trucos. ¿Quién diría que un sobre vacío pesa tanto?",
        "elements": [
            {"type": "follow", "trigger": "Síguenos"},
            {"type": "ask", "text": "¿Quién diría que un sobre *vacío* pesa tanto?", "trigger": "Quién"},
        ],
    },
]

g = {
    "topic": "Qué hace de verdad el voto en blanco en las elecciones generales del 29 de noviembre de 2026",
    "categoria": "politica",
    "title": "Votar en blanco no hace lo que crees 🗳️",
    "source": "Fuentes: LOREG (LO 5/1985), arts. 96.5 y 163.1.a · BOE 6/10/2026 (Real Decreto 806/2026) · Ejemplo con partidos ficticios calculado con la regla D'Hondt",
    "chapters": ["?", "1", "2", "3", "+", "TÚ"],
    "outro_cta": "Todo tiene un truco",
    "cover": {"text": "Blanco: *no es lo que crees*", "scene": 0},
    "publish": {
        "caption": "¿Vas a votar en blanco el 29-N? 🗳️ El voto en blanco es válido: no deja escaños vacíos, pero suma al total y sube el listón del 3 % que cada partido necesita en su provincia. El nulo y la abstención no cuentan para ese 3 %. Sin posicionarnos: solo explicamos cómo funciona. ¿Lo sabías?",
        "description": "Qué hace de verdad el voto en blanco en las elecciones generales del 29 de noviembre de 2026 (Real Decreto 806/2026, BOE del 6 de octubre). 1) Votar en blanco al Congreso es meter en la urna el sobre sin papeleta; la LOREG lo considera voto válido (art. 96.5). 2) No deja escaños vacíos: todos los escaños de la provincia se reparten entre las candidaturas. 3) Para entrar en el reparto del Congreso, una candidatura necesita al menos el 3 % de los votos válidos de su circunscripción (art. 163.1.a), y los votos en blanco forman parte de ese total. 4) Ejemplo con partidos ficticios en una provincia imaginaria de 30 escaños: con 100.000 votos válidos el listón es 3.000 y el partido Rombo, con 3.100, entra y saca 1 escaño; si llegan 9.000 votos en blanco más (109.000 válidos), el listón sube a 3.270, Rombo queda fuera con los mismos votos y su escaño pasa a otro partido. 5) Los votos nulos y la abstención no cuentan como votos válidos, así que no mueven ese listón. Sin posicionarnos: solo explicamos cómo funciona. Fuentes: LOREG, arts. 96 y 163; BOE (Real Decreto 806/2026).",
        "hashtags": ["votoenblanco", "elecciones", "eleccionesgenerales", "29N", "leyelectoral", "politica", "aprendeentiktok", "eltrucoes"],
    },
    "scenes": scenes,
}
json.dump(g, open(OUT, "w"), ensure_ascii=False, indent=2)
n = sum(len(s["narration"].split()) for s in scenes)
print("palabras", n)
for i, s in enumerate(scenes):
    print(i, len(s["narration"].split()), s["narration"])

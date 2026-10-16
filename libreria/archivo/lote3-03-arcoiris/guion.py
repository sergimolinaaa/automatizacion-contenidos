import json, sys

def A(target, effect, **kw):
    d = {"target": target, "effect": effect}
    d.update(kw)
    return d

def cam(x, y, amount, trigger=None, dur=0.8):
    d = {"target": "camera", "effect": "zoom", "to": [x, y], "amount": amount, "dur": dur}
    if trigger:
        d["trigger"] = trigger
    return d

hide = lambda *ids: [A(i, "hide") for i in ids]
GOTA_ALL = ["inwhite", "whiteback", "whiteout", "fanin", "fanback", "fanout", "ang", "l42", "lrebota", "lrojo", "lvioleta", "lluz", "ldobla"]
def gota_hide(*keep):
    return hide(*[i for i in GOTA_ALL if i not in keep])

scenes = [
    {
        "chapter": 0,
        "headline": "Nunca lo *alcanzarás*",
        "narration": "Lo tienes delante… pero nunca podrás llegar hasta él.",
        "illustration": {
            "svg_file": "escena.svg",
            "caption": "Fig. 1 · Después de la lluvia",
            "anims": [
                A("lluvia", "drift", amount=0.3),
                A("nube", "drift", amount=0.6),
                A("pajaros", "float", amount=0.8),
                A("arboles", "sway", origin="bottom", amount=0.3),
                A("flores", "sway", origin="bottom", amount=0.6),
                A("rip1", "ripple", phase=0),
                A("rip2", "ripple", phase=0.5),
                cam(560, 330, 1.2, "tienes"),
                A("arco", "punch", trigger="delante", amount=0.6),
                A("persona", "move", to=[80, -45], trigger="nunca", dur=1.6),
                A("arco", "move", to=[80, 0], trigger="nunca", dur=1.6),
                cam(500, 350, 1, "llegar"),
            ],
        },
        "elements": [{"type": "stamp", "text": "¡IMPOSIBLE!", "tone": "hot", "trigger": "llegar"}],
    },
    {"chapter": 0, "signature": True, "headline": "El truco es…", "narration": "El truco es…"},
    {
        "chapter": 1, "number": "1",
        "headline": "Cada gota, un *prisma*",
        "narration": "Cada gota de lluvia hace de prisma: la luz del Sol entra y se dobla.",
        "illustration": {
            "svg_file": "gota.svg",
            "caption": "Fig. 2 · Una gota de lluvia",
            "anims": gota_hide("inwhite", "lluz", "ldobla") + [
                A("lluvia", "drift", amount=0.3),
                A("gotas", "float", amount=0.4),
                A("sol", "pulse", amount=0.5),
                A("gota", "punch", trigger="gota", amount=0.5),
                A("beam", "draw", trigger="luz", dur=0.6, sfx="whoosh"),
                A("lluz", "pop", trigger="Sol"),
                cam(420, 220, 1.5, "entra"),
                A("inwhite", "draw", trigger="entra", dur=0.6),
                A("ldobla", "pop", trigger="dobla", sfx="pop"),
            ],
        },
    },
    {
        "chapter": 1, "number": "1",
        "headline": "Rebota *dentro*",
        "narration": "Dentro, rebota en el fondo de la gota como en un espejo… y vuelve a salir.",
        "illustration": {
            "svg_file": "gota.svg",
            "caption": "Fig. 3 · Un espejo dentro",
            "anims": gota_hide("inwhite", "whiteback", "whiteout", "lrebota") + [
                A("lluvia", "drift", amount=0.3),
                A("gotas", "float", amount=0.4),
                A("sol", "pulse", amount=0.5),
                A("inwhite", "punch", trigger="Dentro", amount=0.4),
                A("whiteback", "draw", trigger="rebota", dur=0.6, sfx="boing"),
                cam(760, 230, 1.6, "fondo"),
                A("lrebota", "pop", trigger="espejo", sfx="pop"),
                cam(500, 350, 1, "salir"),
                A("whiteout", "draw", trigger="salir", dur=0.7, sfx="whoosh"),
            ],
        },
        "mascot": {"trigger": "espejo", "pose": "point", "note": "Espejito, espejito…", "side": "right"},
    },
    {
        "chapter": 2, "number": "2",
        "headline": "Los colores *se separan*",
        "narration": "Pero cada color se dobla distinto: el violeta más que el rojo. Así se separan.",
        "illustration": {
            "svg_file": "gota.svg",
            "caption": "Fig. 4 · Se abre en colores",
            "anims": gota_hide("fanin", "fanback", "fanout", "lrojo", "lvioleta") + [
                A("lluvia", "drift", amount=0.3),
                A("gotas", "float", amount=0.4),
                A("sol", "pulse", amount=0.5),
                A("fanin", "draw", trigger="color", dur=0.5, sfx="magia"),
                A("fanback", "draw", trigger="dobla", dur=0.5),
                A("fanout", "draw", trigger="distinto", dur=0.7),
                A("lvioleta", "pop", trigger="violeta", sfx="pop"),
                A("lrojo", "pop", trigger="rojo", sfx="pop"),
                cam(480, 520, 1.4, "separan"),
                A("fanout", "punch", trigger="separan", amount=0.4),
            ],
        },
    },
    {
        "chapter": 2, "number": "2",
        "headline": "El ángulo *mágico*",
        "narration": "Y sale formando unos 42 grados con los rayos del Sol.",
        "illustration": {
            "svg_file": "gota.svg",
            "caption": "Fig. 5 · Siempre 42°",
            "anims": gota_hide("fanin", "fanback", "fanout", "lrojo", "ang", "l42") + [
                A("lluvia", "drift", amount=0.3),
                A("gotas", "float", amount=0.4),
                A("sol", "pulse", amount=0.5),
                A("fanout", "punch", trigger="sale", amount=0.4),
                A("ang", "draw", trigger="formando", dur=0.6, sfx="rotulador"),
                cam(560, 500, 1.4, "42"),
                A("l42", "pop", trigger="42", sfx="ding"),
                cam(500, 350, 1, "rayos"),
                A("beam", "punch", trigger="Sol", amount=0.6),
                A("sol", "punch", trigger="Sol"),
            ],
        },
    },
    {
        "chapter": 3, "number": "3",
        "headline": "Tu *sombra* manda",
        "narration": "Solo te mandan color las gotas a 42 grados de la sombra de tu cabeza.",
        "illustration": {
            "svg_file": "geometria.svg",
            "caption": "Fig. 6 · Visto de lado",
            "anims": hide("lsuelo", "lower") + [
                A("lluvia", "drift", amount=0.2),
                A("nube", "drift", amount=0.3),
                A("sol", "pulse", amount=0.4),
                A("gotitas", "float", amount=0.3),
                A("sunray", "draw", trigger="mandan", dur=0.6),
                A("toeye", "draw", trigger="color", dur=0.6, sfx="whoosh"),
                cam(330, 260, 1.5, "gotas"),
                A("lgota", "pop", trigger="gotas", sfx="pop"),
                A("gotar", "punch", trigger="gotas"),
                A("upline", "draw", trigger="42", dur=0.5),
                cam(500, 350, 1, "grados"),
                A("ang", "draw", trigger="grados", dur=0.5),
                A("l42", "pop", trigger="grados", sfx="ding"),
                A("anti", "draw", trigger="sombra", dur=0.6),
                A("lsombra", "pop", trigger="sombra"),
                A("persona", "punch", trigger="cabeza", amount=0.5),
            ],
        },
    },
    {
        "chapter": 3, "number": "3",
        "headline": "Por eso es un *arco*",
        "narration": "Esas gotas forman un círculo alrededor de tu sombra; el suelo lo corta y queda un arco.",
        "illustration": {
            "svg_file": "arcos.svg",
            "caption": "Fig. 7 · Un círculo cortado",
            "anims": hide("sec", "banda", "lrojo1", "lrojo2", "lsec", "lbanda") + [
                A("lluvia", "drift", amount=0.3),
                A("arboles", "sway", origin="bottom", amount=0.3),
                A("prim", "punch", trigger="gotas", amount=0.5),
                A("circ", "draw", trigger="círculo", dur=1.0, sfx="rotulador"),
                A("lsombra", "pop", trigger="sombra", sfx="pop"),
                A("sombra", "punch", trigger="sombra"),
                cam(500, 560, 1.4, "suelo"),
                A("circ", "pulse", trigger="corta", amount=0.6),
                cam(500, 350, 1, "arco"),
                A("prim", "punch", trigger="arco", amount=0.6),
            ],
        },
    },
    {
        "chapter": 4, "number": "+",
        "headline": "Cada uno, *el suyo*",
        "narration": "Si te mueves, cambian las gotas que te sirven: cada persona ve su propio arcoíris.",
        "illustration": {
            "svg_file": "escena.svg",
            "caption": "Fig. 8 · Te sigue",
            "anims": [
                A("lluvia", "drift", amount=0.3),
                A("nube", "drift", amount=0.6),
                A("pajaros", "float", amount=0.8),
                A("arboles", "sway", origin="bottom", amount=0.3),
                A("flores", "sway", origin="bottom", amount=0.6),
                A("rip1", "ripple", phase=0),
                A("rip2", "ripple", phase=0.5),
                A("persona", "move", to=[80, -45], trigger="mueves", dur=1.4),
                A("arco", "move", to=[80, 0], trigger="mueves", dur=1.4, sfx="whoosh"),
                cam(560, 320, 1.25, "cambian"),
                A("arco", "punch", trigger="gotas", amount=0.5),
                A("persona", "punch", trigger="persona", amount=0.6),
                cam(500, 350, 1, "arcoíris"),
            ],
        },
        "elements": [{"type": "tag", "text": "Uno por persona", "tone": "accent", "trigger": "propio"}],
    },
    {
        "chapter": 4, "number": "+",
        "headline": "Doble y *al revés*",
        "narration": "Con dos rebotes dentro, sale un segundo arco más alto… con los colores al revés.",
        "illustration": {
            "svg_file": "arcos.svg",
            "caption": "Fig. 9 · Doble arcoíris",
            "anims": hide("lsombra", "banda", "lbanda", "circ", "sec", "lsec", "lrojo1", "lrojo2") + [
                A("lluvia", "drift", amount=0.3),
                A("arboles", "sway", origin="bottom", amount=0.3),
                A("prim", "punch", trigger="rebotes", amount=0.5),
                A("sec", "fade", trigger="segundo", dur=0.6, sfx="magia"),
                A("lsec", "pop", trigger="alto", sfx="pop"),
                A("lsec", "hide", trigger="colores"),
                cam(300, 280, 1.5, "colores"),
                A("lrojo1", "pop", trigger="colores", sfx="pop"),
                A("lrojo2", "pop", trigger="revés", sfx="pop"),
                A("sec", "punch", trigger="revés", amount=0.4),
            ],
        },
    },
    {
        "chapter": 4, "number": "+",
        "headline": "La banda *oscura*",
        "narration": "Entre los dos arcos, el cielo se ve más oscuro: la banda de Alejandro.",
        "illustration": {
            "svg_file": "arcos.svg",
            "caption": "Fig. 10 · Banda de Alejandro",
            "anims": hide("lsombra", "circ", "lrojo1", "lrojo2", "lsec", "banda", "lbanda") + [
                A("lluvia", "drift", amount=0.3),
                A("arboles", "sway", origin="bottom", amount=0.3),
                A("prim", "punch", trigger="arcos", amount=0.4),
                A("sec", "punch", trigger="arcos", amount=0.4),
                cam(500, 260, 1.5, "cielo"),
                A("banda", "fade", trigger="oscuro", dur=0.8),
                A("lbanda", "pop", trigger="Alejandro", sfx="ding"),
                A("banda", "pulse", trigger="Alejandro", amount=0.4),
            ],
        },
    },
    {
        "chapter": 5, "number": "TÚ",
        "headline": "Te *toca*",
        "narration": "Síguenos para más trucos. ¿Alguna vez has perseguido un arcoíris?",
        "elements": [
            {"type": "follow", "trigger": "Síguenos"},
            {"type": "ask", "text": "¿Alguna vez has *perseguido* un arcoíris?", "trigger": "Alguna"},
        ],
    },
]

script = {
    "topic": "Cómo se forma un arcoíris",
    "categoria": "fisica",
    "title": "Por qué el arcoíris es un arco (y nunca podrás alcanzarlo) 🌈",
    "source": "Fuentes: Atmospheric Optics (L. Cowley) · HyperPhysics, Georgia State University",
    "chapters": ["?", "1", "2", "3", "+", "TÚ"],
    "outro_cta": "La naturaleza tiene trucos",
    "cover": {"text": "Nunca podrás *alcanzarlo*", "badge": "¿POR QUÉ?", "scene": 0},
    "publish": {
        "caption": "Lo tienes delante, pero nunca podrás llegar al arcoíris 🌈 Cada gota de lluvia hace de prisma y espejo, y solo te mandan color las que están a 42° de tu sombra. ¿Alguna vez lo has perseguido?",
        "description": "Cada gota de lluvia refracta la luz del Sol al entrar, la refleja en su fondo y la vuelve a refractar al salir, separando los colores: el rojo sale a unos 42° de la luz del Sol y el violeta a unos 40°. Solo ves color en las gotas que forman ese ángulo con tu sombra, así que todas juntas dibujan un círculo alrededor de ella; el suelo corta la mitad de abajo y por eso ves un arco. Con dos reflexiones dentro de la gota aparece un segundo arco más alto con los colores invertidos, y entre ambos el cielo se ve más oscuro: la banda de Alejandro. Fuentes: Atmospheric Optics (Les Cowley); HyperPhysics, Georgia State University.",
        "hashtags": ["arcoiris", "fisica", "luz", "ciencia", "curiosidades", "optica", "eltrucoes"],
    },
    "scenes": scenes,
}
assert len(script["title"]) <= 70, len(script["title"])
print("palabras:", sum(len(s["narration"].split()) for s in scenes), "escenas:", len(scenes), "título:", len(script["title"]), file=sys.stderr)
json.dump(script, open(sys.argv[1], "w"), ensure_ascii=False, indent=2)

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

scenes = [
    {
        "chapter": 0,
        "headline": "Un paracaídas *con agujeros*",
        "narration": "Vuela más de un kilómetro… colgada de un paracaídas lleno de agujeros.",
        "illustration": {
            "svg_file": "escena.svg",
            "caption": "Fig. 1 · Diente de león",
            "anims": hide("sensor", "lsensor") + [
                A("clouds", "drift", amount=0.5),
                A("wind", "flow", amount=0.8),
                A("clock", "sway", origin="bottom", amount=0.2),
                A("fl1", "sway", origin="bottom", amount=0.5),
                A("fl2", "sway", origin="bottom", amount=0.4, phase=0.3),
                A("fs1", "float", amount=0.5),
                A("fs3", "float", amount=0.7),
                A("fs4", "float", amount=0.6),
                A("fs2", "float", amount=0.4, phase=0.5),
                A("clock", "punch", trigger="Vuela"),
                A("fs2", "move", to=[-90, -50], rotate=-10, trigger="kilómetro", dur=1.4, sfx="whoosh"),
                cam(300, 215, 1.7, "paracaídas"),
                A("lpara", "pop", trigger="paracaídas", sfx="pop"),
                A("fs1", "punch", trigger="agujeros"),
            ],
        },
    },
    {"chapter": 0, "signature": True, "headline": "El truco es…", "narration": "El truco es…"},
    {
        "chapter": 1, "number": "1",
        "headline": "Un *pincel* de pelos",
        "narration": "Su paracaídas se llama vilano: unos cien pelitos finísimos sobre un palito.",
        "illustration": {
            "svg_file": "semilla.svg",
            "caption": "Fig. 2 · Una semilla",
            "anims": hide("cerradob", "cerradof", "rain", "wet", "bigdrops", "lcerrado") + [
                A("bokeh", "drift", amount=0.6),
                A("lsemilla", "pop", trigger="Su"),
                A("lvilano", "pop", trigger="vilano", sfx="pop"),
                A("seed", "punch", trigger="vilano", amount=0.5),
                cam(500, 210, 1.5, "pelitos"),
                A("lpelos", "pop", trigger="cien"),
                A("abiertof", "punch", trigger="finísimos", amount=0.4),
                cam(500, 350, 1, "palito"),
                A("lpico", "pop", trigger="palito", sfx="pop"),
            ],
        },
    },
    {
        "chapter": 1, "number": "1",
        "headline": "Casi todo es *aire*",
        "narration": "Visto desde arriba, casi todo es hueco: un 92% del vilano es aire.",
        "illustration": {
            "svg_file": "arriba.svg",
            "caption": "Fig. 3 · Vista desde arriba",
            "anims": [
                A("motas", "drift", amount=0.5),
                A("disco", "spin", amount=0.05),
                A("lpelo", "pop", trigger="Visto"),
                A("lpelo", "hide", trigger="casi"),
                A("lpelo", "pop", trigger="92"),
                cam(640, 290, 1.6, "hueco"),
                A("hueco", "pop", trigger="hueco", sfx="pop"),
                A("hueco", "pulse", trigger="hueco", amount=0.8),
                cam(500, 350, 1, "92"),
                A("laire", "pop", trigger="92", sfx="ding"),
                A("airefill", "fade", trigger="aire", dur=0.5),
                A("pelos", "punch", trigger="vilano", amount=0.4),
            ],
        },
    },
    {
        "chapter": 2, "number": "2",
        "headline": "Un *anillo* de aire",
        "narration": "Al caer, el aire cruza entre los pelos… y forma un anillo que gira justo encima.",
        "illustration": {
            "svg_file": "vortice.svg",
            "caption": "Fig. 4 · Túnel de viento",
            "anims": hide("lbaja", "menos", "freno", "lhuecos", "lvel") + [
                A("aire", "flow", amount=1),
                A("cae", "pop", trigger="caer"),
                A("lcae", "pop", trigger="caer"),
                cam(500, 420, 1.4, "cruza"),
                A("vilano", "punch", trigger="pelos", amount=0.5),
                A("anillo", "pop", trigger="anillo", sfx="magia"),
                cam(500, 350, 1, "anillo"),
                A("lanillo", "pop", trigger="anillo"),
                A("swl", "spin", trigger="gira", amount=1.2),
                A("swr", "spin", trigger="gira", amount=-1.2),
                A("lsep", "pop", trigger="encima", sfx="pop"),
            ],
        },
    },
    {
        "chapter": 2, "number": "2",
        "headline": "Frena *la caída*",
        "narration": "Ese remolino crea baja presión encima y frena la caída: unos 40 centímetros por segundo.",
        "illustration": {
            "svg_file": "vortice.svg",
            "caption": "Fig. 5 · Baja presión",
            "anims": hide("lhuecos", "lsep", "lanillo", "lvel") + [
                A("aire", "flow", amount=1),
                A("swl", "spin", amount=1.2),
                A("swr", "spin", amount=-1.2),
                A("anillo", "punch", trigger="remolino"),
                A("menos", "pop", trigger="baja"),
                A("lbaja", "pop", trigger="presión", sfx="pop"),
                A("baja", "pulse", trigger="presión", amount=1),
                cam(560, 340, 1.25, "frena"),
                A("freno", "draw", trigger="frena", sfx="whoosh"),
                A("cae", "punch", trigger="caída"),
                A("lvel", "pop", trigger="40", sfx="ding"),
            ],
        },
    },
    {
        "chapter": 3, "number": "3",
        "headline": "Huecos *justos*",
        "narration": "La clave son los huecos justos: con menos, el anillo se vuelve inestable y se escapa.",
        "illustration": {
            "svg_file": "vortice.svg",
            "caption": "Fig. 6 · Huecos justos",
            "anims": hide("lbaja", "menos", "freno", "lsep", "lanillo", "cae", "lcae", "lvel") + [
                A("aire", "flow", amount=1),
                A("swl", "spin", amount=1.2),
                A("swr", "spin", amount=-1.2),
                cam(450, 450, 1.6, "huecos"),
                A("lhuecos", "pop", trigger="huecos", sfx="pop"),
                A("vilano", "punch", trigger="justos", amount=0.5),
                cam(500, 350, 1, "anillo"),
                A("anillo", "shake", trigger="inestable", amount=1.6),
                A("anillo", "move", to=[170, -340], rotate=25, trigger="escapa", dur=1.0, sfx="whoosh"),
            ],
        },
    },
    {
        "chapter": 3, "number": "3",
        "headline": "Menos es *más*",
        "narration": "Resultado: con el mismo material, frena unas cuatro veces más que un disco macizo.",
        "illustration": {
            "svg_file": "vortice.svg",
            "caption": "Fig. 7 · Poco material, mucho freno",
            "anims": hide("lbaja", "lsep", "lanillo", "lhuecos", "lvel", "cae", "lcae") + [
                A("aire", "flow", amount=1),
                A("swl", "spin", amount=1.2),
                A("swr", "spin", amount=-1.2),
                A("baja", "pulse", amount=0.6),
                A("vilano", "punch", trigger="material", amount=0.5),
                A("freno", "draw", trigger="frena", sfx="whoosh"),
                cam(500, 380, 1.3, "frena"),
                A("freno", "punch", trigger="cuatro"),
                A("menos", "pop", trigger="veces"),
                cam(500, 350, 1, "macizo"),
                A("anillo", "punch", trigger="macizo", amount=0.5),
            ],
        },
        "elements": [{"type": "tag", "text": "×4 de freno", "tone": "accent", "trigger": "cuatro"}],
    },
    {
        "chapter": 4, "number": "+",
        "headline": "Se cierra *con lluvia*",
        "narration": "Con humedad, el vilano se cierra como un paraguas: así casi no se suelta si llueve.",
        "illustration": {
            "svg_file": "semilla.svg",
            "caption": "Fig. 8 · Con humedad",
            "anims": hide("lpelos", "lpico", "lsemilla", "lvilano", "cerradob", "cerradof", "wet", "lcerrado") + [
                A("bokeh", "drift", amount=0.6),
                A("rain", "fade", trigger="humedad", dur=0.5),
                A("bigdrops", "pop", trigger="humedad", sfx="splash"),
                A("bigdrops", "float", trigger="humedad", amount=0.6),
                cam(540, 250, 1.35, "cierra"),
                A("abierto", "hide", trigger="cierra"),
                A("abiertof", "hide", trigger="cierra"),
                A("cerradob", "pop", trigger="cierra"),
                A("cerradof", "pop", trigger="cierra", sfx="chasquido"),
                A("wet", "pop", trigger="paraguas"),
                A("lcerrado", "pop", trigger="paraguas"),
                cam(500, 350, 1, "suelta"),
                A("seed", "punch", trigger="suelta", amount=0.5),
            ],
        },
        "mascot": {"trigger": "llueve", "pose": "surprise", "note": "Paraguas de serie", "side": "right"},
    },
    {
        "chapter": 4, "number": "+",
        "headline": "Copiado por *ingenieros*",
        "narration": "Y ya inspira sensores sin batería que viajan con el viento.",
        "illustration": {
            "svg_file": "escena.svg",
            "caption": "Fig. 9 · Sensor volador",
            "anims": hide("lpara") + [
                A("clouds", "drift", amount=0.5),
                A("wind", "flow", amount=0.8),
                A("clock", "sway", origin="bottom", amount=0.2),
                A("fl1", "sway", origin="bottom", amount=0.5),
                A("fl2", "sway", origin="bottom", amount=0.4, phase=0.3),
                A("fs1", "float", amount=0.5),
                A("fs2", "float", amount=0.4, phase=0.5),
                A("fs3", "float", amount=0.7),
                A("fs4", "float", amount=0.6),
                A("sensor", "pop", trigger="sensores", sfx="pop"),
                cam(800, 250, 1.5, "sensores"),
                A("lsensor", "pop", trigger="batería", sfx="ding"),
                A("sensor", "float", trigger="batería", amount=0.6),
                cam(500, 350, 1, "viento"),
                A("fs1", "punch", trigger="viento"),
            ],
        },
    },
    {
        "chapter": 5, "number": "TÚ",
        "headline": "Te *toca*",
        "narration": "Síguenos para más trucos. ¿Cuántos deseos has pedido soplando uno de estos?",
        "elements": [
            {"type": "follow", "trigger": "Síguenos"},
            {"type": "ask", "text": "¿Cuántos *deseos* has pedido soplando uno?", "trigger": "Cuántos"},
        ],
    },
]

script = {
    "topic": "Las semillas del diente de león vuelan con un anillo de aire",
    "categoria": "plantas",
    "title": "Vuela más de un kilómetro con un paracaídas lleno de agujeros 🌬️",
    "source": "Fuentes: Cummins et al., Nature (2018) · Seale et al., eLife (2022) · Iyer et al., Nature (2022)",
    "chapters": ["?", "1", "2", "3", "+", "TÚ"],
    "outro_cta": "La naturaleza tiene trucos",
    "cover": {"text": "Vuela con un *anillo de aire*", "badge": "¿CÓMO LO HACE?", "scene": 0},
    "publish": {
        "caption": "Su paracaídas es un 92% aire… y aun así vuela más de un kilómetro 🌬️ El truco: un anillo de aire que gira justo encima y frena la caída. ¿Cuántos deseos has pedido soplando uno?",
        "description": "La semilla del diente de león cuelga de un vilano: unos cien pelitos finísimos que dejan pasar el aire (más del 90% es hueco). Al caer, el aire que cruza entre los pelos forma un anillo giratorio que flota separado justo encima, crea baja presión y frena la caída a unos 40 cm/s. Con la misma cantidad de material frena unas cuatro veces más que un disco macizo, y con humedad el vilano se cierra para no soltarse con lluvia. Fuentes: Cummins et al., Nature (2018); Seale et al., eLife (2022); Iyer et al., Nature (2022).",
        "hashtags": ["dientedeleon", "plantas", "naturaleza", "ciencia", "fisica", "curiosidades", "eltrucoes"],
    },
    "scenes": scenes,
}
assert len(script["title"]) <= 70, len(script["title"])
words = sum(len(s["narration"].split()) for s in scenes)
print("palabras:", words, "escenas:", len(scenes), "título:", len(script["title"]), file=sys.stderr)
json.dump(script, open(sys.argv[1], "w"), ensure_ascii=False, indent=2)

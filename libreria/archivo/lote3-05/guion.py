import json, shutil, sys
from pathlib import Path

OUT = Path("/home/user/automatizacion-contenidos/content/lote3-05-piedras-que-se-mueven")
OUT.mkdir(parents=True, exist_ok=True)
HERE = Path(sys.path[0])


def hide(*ids):
    return [{"target": i, "effect": "hide"} for i in ids]


def A(target, effect, trigger=None, **kw):
    a = {"target": target, "effect": effect}
    if trigger:
        a["trigger"] = trigger
    a.update(kw)
    return a


def zoom(x, y, amount, trigger=None, dur=0.8):
    return A("camera", "zoom", trigger, to=[x, y], amount=amount, dur=dur)


INSTR = ["gps", "gw1", "gw2", "camara", "meteo", "cups", "lgps", "lcamara", "lmeteo"]
scenes = []
# 0 · gancho
scenes.append({
    "chapter": 0,
    "headline": "Piedras *que se mueven*",
    "narration": "En este desierto, las piedras se mueven solas… y dejan su rastro.",
    "illustration": {"svg_file": "playa_full.svg", "layout": "full", "caption": "Fig. 1 · Racetrack Playa", "anims": hide(*INSTR, "lsurco") + [
        A("clouds", "drift", amount=0.6),
        A("sun", "pulse", amount=0.4),
        A("sun", "punch", "desierto", amount=0.5),
        A("r1", "punch", "piedras", amount=0.8, sfx="pop"),
        A("r2", "punch", "piedras", amount=0.8),
        A("r0", "punch", "mueven", amount=0.5),
        A("r0", "move", "solas", to=[16, 6], dur=1.6),
        A("trailglow", "draw", "rastro", dur=1.0, sfx="rotulador"),
        A("r0", "punch", "rastro", amount=0.4),
    ]},
})
# 1 · firma
scenes.append({"chapter": 0, "signature": True, "headline": "El truco es…", "narration": "El truco es…"})
# 2 · misterio
scenes.append({
    "chapter": 1, "number": "1",
    "headline": "Nadie las *veía*",
    "narration": "Durante décadas, nadie las vio moverse. Solo aparecían sus surcos, de cientos de metros.",
    "illustration": {"svg_file": "playa.svg", "caption": "Fig. 2 · Surcos en el barro", "anims": hide(*INSTR) + [
        A("clouds", "drift", amount=0.6),
        A("sun", "pulse", amount=0.4),
        zoom(560, 440, 1.3, "décadas", 1.0),
        A("r1", "punch", "moverse", amount=0.5),
        A("trailglow", "draw", "surcos", dur=1.0),
        A("lsurco", "pop", "surcos", sfx="pop"),
        zoom(500, 380, 1, "cientos", 0.8),
        A("tr2", "punch", "metros", amount=0.4),
        A("tr3", "punch", "metros", amount=0.4),
    ]},
    "elements": [{"type": "stamp", "text": "MISTERIO", "tone": "hot", "trigger": "nadie"}],
})
# 3 · GPS
scenes.append({
    "chapter": 1, "number": "1",
    "headline": "*Espías* con GPS",
    "narration": "Hasta que unos científicos les pusieron GPS y vigilaron el lago seco con cámaras y una estación meteorológica.",
    "illustration": {"svg_file": "playa.svg", "caption": "Fig. 3 · Piedras con GPS", "anims": hide("lsurco", "trailglow") + [
        A("clouds", "drift", amount=0.6),
        zoom(600, 440, 1.6, "científicos", 0.9),
        A("gps", "pop", "GPS", sfx="pop"),
        A("lgps", "pop", "GPS"),
        A("gw1", "fade", "GPS", dur=0.2),
        A("gw2", "fade", "GPS", dur=0.2),
        A("gw1", "ripple", "GPS", phase=0.0),
        A("gw2", "ripple", "GPS", phase=0.5),
        zoom(500, 380, 1, "lago", 0.8),
        A("camara", "slide-up", "cámaras", sfx="whoosh"),
        A("lcamara", "pop", "cámaras"),
        A("meteo", "slide-up", "estación"),
        A("cups", "pop", "estación"),
        A("cups", "spin", "meteorológica", amount=2.5),
        A("lmeteo", "pop", "meteorológica"),
    ]},
    "mascot": {"trigger": "vigilaron", "pose": "point", "note": "Vigilancia nivel espía", "side": "right"},
})
# 4 · charco helado
scenes.append({
    "chapter": 2, "number": "2",
    "headline": "Un charco *helado*",
    "narration": "En invierno, la lluvia deja un charco poco profundo. De noche, se congela en una placa finísima.",
    "illustration": {"svg_file": "hielo.svg", "caption": "Fig. 4 · Corte del charco", "anims": hide(
        "lbarro", "lviento", "lsurco", "viento", "empuje", "surconuevo", "grietas") + [
        A("lluvia", "fade", "lluvia", dur=0.3, sfx="chorro"),
        A("lluvia", "float", "lluvia", amount=0.5),
        A("agua", "grow", "charco", sfx="splash"),
        A("lagua", "pop", "profundo"),
        A("lluvia", "hide", "noche"),
        A("sol", "hide", "noche"),
        A("noche", "fade", "noche", dur=0.5),
        A("luna", "fade", "noche", dur=0.5),
        A("hielo", "fade", "congela", dur=0.4, sfx="brillo"),
        A("hielo2", "fade", "congela", dur=0.4),
        zoom(300, 430, 1.35, "placa", 0.8),
        A("lhielo", "pop", "placa"),
        A("hielo", "punch", "finísima", amount=0.4),
    ]},
    "elements": [{"type": "tag", "text": "Hielo de 3 a 6 mm", "tone": "accent", "trigger": "finísima"}],
})
# 5 · el sol la rompe
scenes.append({
    "chapter": 2, "number": "2",
    "headline": "El sol la *rompe*",
    "narration": "Por la mañana, el sol la calienta, la agrieta y la parte en grandes paneles flotantes.",
    "illustration": {"svg_file": "panel.svg", "caption": "Fig. 5 · Vista desde arriba", "anims": hide("nuevos", "viento", "lsurco") + [
        A("brillo", "fade", "sol", dur=0.6, sfx="brillo"),
        A("brillo", "pulse", "sol", amount=0.4),
        A("grietas", "draw", "agrieta", dur=0.8, sfx="chasquido"),
        A("lgrieta", "pop", "agrieta"),
        A("entero", "hide", "parte"),
        A("grietas", "hide", "parte"),
        A("p1", "drift", "parte", amount=0.35, phase=0.0),
        A("p2", "drift", "parte", amount=0.3, phase=0.3),
        A("p3", "drift", "parte", amount=0.35, phase=0.6),
        A("p4", "drift", "parte", amount=0.3, phase=0.15),
        A("p5", "drift", "parte", amount=0.35, phase=0.45),
        A("p6", "drift", "parte", amount=0.3, phase=0.75),
        A("p7", "drift", "parte", amount=0.35, phase=0.9),
        A("lgrieta", "hide", "paneles"),
        zoom(480, 460, 1.25, "paneles", 0.8),
        A("lpanel", "pop", "paneles", sfx="pop"),
    ]},
})
# 6 · el empujón
scenes.append({
    "chapter": 3, "number": "3",
    "headline": "Un *empujoncito*",
    "narration": "Basta una brisa floja: el viento empuja el hielo… y el hielo empuja las piedras.",
    "illustration": {"svg_file": "hielo_free.svg", "layout": "free", "height": 840, "caption": "Fig. 6 · El hielo empuja", "anims": hide(
        "grietas", "lagua", "lbarro", "lsurco", "lhielo") + [
        A("agua", "pulse", amount=0.1),
        A("viento", "draw", "brisa", dur=0.7, sfx="whoosh"),
        A("lviento", "pop", "brisa"),
        A("viento", "drift", "viento", amount=0.4),
        A("empuje", "draw", "empuja", dur=0.5),
        A("hielo", "punch", "hielo", amount=0.4),
        A("lhielo", "pop", "hielo empuja"),
        A("lviento", "hide", "piedras"),
        A("lhielo", "hide", "piedras"),
        A("piedra", "move", "piedras", to=[130, 0], dur=1.6, sfx="whoosh"),
        A("hielo", "move", "piedras", to=[130, 0], dur=1.6),
        A("hielo2", "move", "piedras", to=[130, 0], dur=1.6),
        A("empuje", "move", "piedras", to=[130, 0], dur=1.6),
        A("surconuevo", "draw", "piedras", dur=1.4),
    ]},
    "elements": [{"type": "stat", "label": "Brisa de unos", "value": 5, "from": 0, "unit": " m/s", "note": "unos 18 km/h", "trigger": "brisa"}],
})
# 7 · el surco
scenes.append({
    "chapter": 3, "number": "3",
    "headline": "Y dejan *surco*",
    "narration": "Las piedras resbalan sobre el barro blando del fondo y van dibujando su rastro, a veces en zigzag.",
    "illustration": {"svg_file": "panel.svg", "caption": "Fig. 7 · Así se forma el surco", "anims": hide("entero", "grietas", "brillo", "lgrieta", "lpanel") + [
        A("viento", "draw", "piedras", dur=0.6, sfx="whoosh"),
        A("viento", "drift", "piedras", amount=0.3),
        A("paneles", "move", "resbalan", to=[90, 0], dur=2.2),
        A("nuevos", "draw", "resbalan", dur=1.8),
        zoom(520, 400, 1.4, "barro", 0.8),
        A("rb", "punch", "blando", amount=0.5),
        zoom(500, 350, 1, "dibujando", 0.7),
        A("lsurco", "pop", "rastro", sfx="rotulador"),
    ]},
})
# 8 · velocidad
scenes.append({
    "chapter": 4, "number": "+",
    "headline": "Sin *prisa*",
    "narration": "Iban a entre 2 y 5 metros por minuto: más despacio que una persona paseando.",
    "illustration": {"svg_file": "playa.svg", "caption": "Fig. 8 · A paso lento", "anims": hide(*INSTR, "lsurco") + [
        A("clouds", "drift", amount=0.6),
        A("sun", "pulse", amount=0.4),
        zoom(560, 450, 1.5, "Iban", 1.0),
        A("r1", "move", "Iban", to=[30, 10], dur=4.5),
        A("trailglow", "draw", "metros", dur=1.2, sfx="rotulador"),
        A("r1", "punch", "despacio", amount=0.5),
        zoom(500, 380, 1, "persona", 0.8),
        A("r2", "punch", "paseando", amount=0.5),
        A("r3", "punch", "paseando", amount=0.5),
    ]},
    "elements": [{"type": "tag", "text": "2-5 metros por minuto", "tone": "accent", "trigger": "metros"}],
})
# 9 · récords
scenes.append({
    "chapter": 4, "number": "+",
    "headline": "*224 metros*",
    "narration": "Una llegó a recorrer 224 metros. Y un solo día se movieron más de 60 piedras.",
    "illustration": {"svg_file": "panel.svg", "caption": "Fig. 9 · Todas a la vez", "anims": hide("entero", "grietas", "brillo", "lgrieta", "lpanel", "lsurco") + [
        A("viento", "draw", "llegó", dur=0.6, sfx="whoosh"),
        A("rb", "punch", "224", amount=0.6),
        A("paneles", "move", "día", to=[90, 0], dur=2.4),
        A("nuevos", "draw", "día", dur=2.0),
        A("ra", "punch", "60", amount=0.5), A("rc", "punch", "60", amount=0.5),
        A("rd", "punch", "60", amount=0.5), A("re", "punch", "60", amount=0.5),
        zoom(500, 380, 1.2, "piedras", 0.8),
    ]},
    "elements": [{"type": "stat", "label": "Recorrido récord", "value": 224, "from": 0, "unit": " m", "trigger": "224"}],
})
# 10 · TÚ
scenes.append({
    "chapter": 5, "number": "TÚ",
    "headline": "*Confiesa*",
    "narration": "Síguenos para más trucos. ¿Cuántas horas aguantarías mirando una piedra?",
    "elements": [{"type": "follow", "trigger": "Síguenos"}, {"type": "ask", "text": "¿Cuántas horas aguantarías mirando una *piedra*?", "trigger": "Cuántas"}],
})

guion = {
    "topic": "Las piedras que se mueven solas en el Valle de la Muerte",
    "categoria": "tierra",
    "title": "Estas piedras se mueven solas por el desierto (y ya sabemos cómo) 🪨",
    "source": "Fuentes: Norris et al., PLOS ONE (2014), «Sliding Rocks on Racetrack Playa, Death Valley National Park: First Observation of Rocks in Motion»",
    "chapters": ["?", "1", "2", "3", "+", "TÚ"],
    "outro_cta": "Todo tiene un truco",
    "cover": {"text": "Piedras que *se mueven solas*", "badge": "¿CÓMO LO HACEN?", "scene": 0},
    "publish": {
        "caption": "En el Valle de la Muerte hay piedras que se mueven solas y dejan surcos de cientos de metros. Durante décadas nadie las vio moverse… hasta que les pusieron GPS. ¿Adivinas quién las empuja?",
        "description": "En Racetrack Playa, un lago seco del Valle de la Muerte (California), las piedras dejan surcos larguísimos en el barro. En 2014, un equipo de científicos las grabó por fin en movimiento con GPS, cámaras y una estación meteorológica. El truco: en invierno se forma un charco poco profundo que de noche se congela en una placa de hielo de 3 a 6 mm. Por la mañana el sol la rompe en paneles flotantes y una brisa floja (unos 4-5 m/s) los empuja contra las piedras, que resbalan sobre el barro a 2-5 metros por minuto. Una llegó a recorrer 224 metros y el 20 de diciembre de 2013 se movieron más de 60 a la vez. Fuente: Norris et al., PLOS ONE (2014).",
        "hashtags": ["valledelamuerte", "geologia", "piedras", "ciencia", "curiosidades", "naturaleza", "eltrucoes"],
    },
    "scenes": scenes,
}
assert len(guion["title"]) <= 70, len(guion["title"])
words = sum(len(s["narration"].split()) for s in scenes)
print("palabras:", words, "título:", len(guion["title"]))
(OUT / "guion.json").write_text(json.dumps(guion, ensure_ascii=False, indent=2), encoding="utf-8")
for n in ("playa", "playa_full", "hielo", "hielo_free", "panel"):
    shutil.copy(HERE / f"{n}.svg", OUT / f"{n}.svg")

import json, shutil, sys
from pathlib import Path

OUT = Path("/home/user/automatizacion-contenidos/content/lote3-04-piel-de-gallina")
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


scenes = []
# 0 · gancho
scenes.append({
    "chapter": 0,
    "headline": "Piel *de gallina*",
    "narration": "Frío, una canción… y se te pone la piel de gallina.",
    "illustration": {"svg_file": "brazo_full.svg", "layout": "full", "caption": "Fig. 1 · Piel de gallina", "anims": [
        A("snow1", "float", amount=0.6), A("snow2", "drift", amount=0.5),
        A("snowtop", "drift", amount=0.7), A("snowbot", "float", amount=0.6),
        A("notes", "bob", amount=0.4),
        A("snow1", "punch", "Frío", sfx="whoosh"),
        A("notes", "punch", "canción", amount=0.8),
        A("hairflat", "hide", "gallina"),
        A("hairup", "fade", "gallina", dur=0.3),
        A("bumps", "fade", "gallina", dur=0.3, sfx="brillo"),
        A("lupa", "pop", "piel", sfx="pop"),
        A("lgallina", "pop", "gallina"),
        A("lupa", "punch", "gallina", amount=0.5),
    ]},
})
# 1 · firma
scenes.append({"chapter": 0, "signature": True, "headline": "El truco es…", "narration": "El truco es…"})
# 2 · el músculo
base_hide = ["muscontract", "bump1", "bump2", "lpunta", "lsimpatico", "nervesc", "signalsc", "lbulto", "lcelulas", "lnervio", "lfoliculo", "signal"]
scenes.append({
    "chapter": 1, "number": "1",
    "headline": "Un *músculo* por pelo",
    "narration": "Cada pelo tiene pegado un músculo diminuto: el músculo erector del pelo.",
    "illustration": {"svg_file": "corte.svg", "caption": "Fig. 2 · Corte de la piel", "anims": hide(*base_hide) + [
        A("snow", "drift", amount=0.4),
        A("lpelo", "pop", "pelo", sfx="pop"),
        A("hair1", "punch", "pelo", amount=0.4),
        zoom(450, 340, 1.6, "músculo"),
        A("musr1", "punch", "diminuto", amount=1.2, sfx="boing"),
        A("musrelax", "pulse", "diminuto", amount=0.5),
        zoom(500, 350, 1, "erector", 0.7),
        A("lmusculo", "pop", "erector", sfx="rotulador"),
        A("lfoliculo", "pop", "erector"),
    ]},
})
# 3 · tira y levanta
scenes.append({
    "chapter": 1, "number": "1",
    "headline": "Tira y *levanta*",
    "narration": "Al contraerse, tira del pelo, lo pone de punta y levanta un bultito en la piel.",
    "illustration": {"svg_file": "corte.svg", "caption": "Fig. 3 · El músculo se contrae", "anims": hide(
        "lpunta", "lsimpatico", "nervesc", "signalsc", "lcelulas", "lnervio", "lfoliculo", "signal", "lmusculo") + [
        A("snow", "drift", amount=0.4),
        A("musrelax", "hide", "contraerse"),
        A("muscontract", "fade", "contraerse", dur=0.25, sfx="chasquido"),
        A("hair1", "move", "tira", rotate=-24, dur=0.8),
        A("hair2", "move", "tira", rotate=-24, dur=0.8),
        A("lpelo", "hide", "tira"),
        A("lpunta", "pop", "punta", sfx="pop"),
        A("bump1", "fade", "levanta", dur=0.35),
        A("bump2", "fade", "levanta", dur=0.35),
        zoom(450, 250, 1.4, "levanta"),
        A("lbulto", "pop", "bultito"),
        A("bump1", "punch", "bultito", amount=0.6),
    ]},
})
# 4 · sistema simpático
scenes.append({
    "chapter": 2, "number": "2",
    "headline": "*Piloto* automático",
    "narration": "La orden la da el sistema nervioso simpático, el de «lucha o huida». Tú no puedes controlarla.",
    "illustration": {"svg_file": "corte.svg", "caption": "Fig. 4 · Nervio simpático", "anims": hide(
        "lpelo", "lmusculo", "lnervio", "lcelulas", "lbulto", "lpunta", "nervesc", "signalsc", "lfoliculo", "bump1", "bump2", "muscontract") + [
        A("snow", "drift", amount=0.4),
        A("signal", "fade", "orden", dur=0.3, sfx="chasquido"),
        A("signal", "flow", "orden", amount=1.6),
        zoom(640, 440, 1.4, "sistema"),
        A("lsimpatico", "pop", "simpático", sfx="pop"),
        A("nerve", "punch", "simpático", amount=0.3),
        zoom(500, 350, 1, "lucha", 0.6),
        A("musrelax", "hide", "huida"),
        A("muscontract", "fade", "huida", dur=0.25),
        A("hair1", "move", "huida", rotate=-24, dur=0.7, sfx="boing"),
        A("hair2", "move", "huida", rotate=-24, dur=0.7),
        A("bump1", "fade", "huida", dur=0.3),
        A("bump2", "fade", "huida", dur=0.3),
    ]},
    "mascot": {"trigger": "controlarla", "pose": "think", "note": "Ni lo intentes: va por libre", "side": "right"},
})
# 5 · qué lo dispara
scenes.append({
    "chapter": 2, "number": "2",
    "headline": "Frío… y *emoción*",
    "narration": "Por eso salta con el frío, con un susto… o con una canción que te emociona.",
    "illustration": {"svg_file": "brazo.svg", "caption": "Fig. 5 · Lo dispara todo", "anims": hide("lupa") + [
        A("snow1", "float", amount=0.6), A("snow2", "drift", amount=0.5),
        A("notes", "bob", amount=0.4),
        A("snow1", "punch", "frío", amount=1.2, sfx="whoosh"),
        A("hairflat", "hide", "susto"),
        A("hairup", "fade", "susto", dur=0.2),
        A("bumps", "fade", "susto", dur=0.2, sfx="sorpresa"),
        A("bumps", "punch", "susto", amount=0.3),
        A("notes", "punch", "canción", amount=1.2),
        zoom(560, 360, 1.3, "canción", 0.8),
        A("lgallina", "pop", "emociona"),
    ]},
    "elements": [{"type": "tag", "text": "Un reflejo", "tone": "accent", "trigger": "salta"}],
})
# 6 · herencia
scenes.append({
    "chapter": 3, "number": "3",
    "headline": "Herencia *peluda*",
    "narration": "Es un reflejo heredado: nuestros antepasados tenían mucho más pelo, y erizarlo los abrigaba.",
    "illustration": {"svg_file": "abrigo.svg", "caption": "Fig. 5 · Un abrigo de pelo", "anims": hide("aireup", "furup", "laire", "frio2", "calor") + [
        A("snow", "drift", amount=0.6),
        A("frio", "float", amount=0.4),
        A("ltu", "pop", "reflejo", sfx="pop"),
        A("lpoco", "pop", "heredado"),
        A("lantes", "pop", "antepasados", sfx="pop"),
        A("lmucho", "pop", "mucho"),
        A("lpoco", "hide", "mucho"),
        zoom(735, 430, 1.3, "mucho"),
        A("furflat", "hide", "erizarlo"),
        A("furup", "fade", "erizarlo", dur=0.3, sfx="whoosh"),
        A("lmucho", "hide", "erizarlo"),
        A("aireflat", "hide", "erizarlo"),
        A("aireup", "grow", "erizarlo"),
        A("calor", "fade", "abrigaba", dur=0.4),
        A("calor", "float", "abrigaba", amount=0.5),
        A("laire", "pop", "abrigaba"),
        A("frio2", "draw", "abrigaba"),
    ]},
})
# 7 · gato
scenes.append({
    "chapter": 3, "number": "3",
    "headline": "Como un *gato*",
    "narration": "Lo mismo hace un gato: eriza el pelo para abrigarse… o para parecer más grande.",
    "illustration": {"svg_file": "gato_free.svg", "layout": "free", "height": 840, "caption": "Fig. 6 · Gato erizado", "anims": [
        A("cat", "breathe", amount=0.6),
        A("tailthin", "sway", origin="bottom-right", amount=0.6),
        A("headg", "wiggle", amount=0.15),
        A("cat", "punch", "gato", amount=0.4),
        A("tailthin", "hide", "eriza"),
        A("tailpuff", "fade", "eriza", dur=0.2, sfx="boing"),
        A("bristle", "fade", "eriza", dur=0.2),
        A("bristle", "punch", "eriza", amount=0.4),
        A("lerizado", "pop", "pelo"),
        A("tailpuff", "punch", "abrigarse", amount=0.5),
        A("grande", "draw", "grande", sfx="whoosh"),
        A("lgrande", "pop", "grande"),
        A("cat", "punch", "grande", amount=0.7),
    ]},
})
# 8 · Harvard
scenes.append({
    "chapter": 4, "number": "+",
    "headline": "Despierta *células madre*",
    "narration": "Y en 2020, en Harvard, descubrieron algo más: ese nervio también despierta a las células madre del pelo.",
    "illustration": {"svg_file": "corte.svg", "caption": "Fig. 7 · Nicho del folículo", "anims": hide(
        "muscontract", "bump1", "bump2", "lpunta", "lsimpatico", "lbulto", "lpelo", "lmusculo", "signal", "lfoliculo", "lnervio") + [
        A("snow", "drift", amount=0.4),
        A("nerve", "punch", "nervio", amount=0.3),
        A("nervesc", "fade", "nervio", dur=0.3),
        A("signalsc", "fade", "despierta", dur=0.3, sfx="brillo"),
        A("signalsc", "flow", "despierta", amount=1.6),
        zoom(420, 330, 1.35, "despierta"),
        A("stem1", "punch", "células", amount=1.4),
        A("stem1", "pulse", "células", amount=1.2),
        A("lcelulas", "pop", "células", sfx="pop"),
    ]},
    "elements": [{"type": "tag", "text": "Harvard · 2020", "tone": "ink", "trigger": "Harvard"}],
})
# 9 · más pelo
scenes.append({
    "chapter": 4, "number": "+",
    "headline": "Más *pelo*",
    "narration": "En ratones, el frío las activa y el pelo crece antes. Eso sí: aún no es un remedio contra la calvicie.",
    "illustration": {"svg_file": "abrigo.svg", "caption": "Fig. 8 · Pelaje de ratón", "anims": hide(
        "ltu", "lantes", "lpoco", "lmucho", "laire", "frio", "frio2", "aireflat", "aireup", "calor", "furflat") + [
        A("snow", "drift", amount=0.6),
        zoom(790, 430, 1.9),
        A("humano", "hide"),
        A("snow", "punch", "frío", amount=0.8, sfx="whoosh"),
        A("furup", "grow", "crece", dur=1.0, sfx="brillo"),
        A("furup", "sway", "crece", origin="bottom", amount=0.15),
    ]},
    "mascot": {"trigger": "calvicie", "pose": "surprise", "note": "Calvos del mundo: paciencia", "side": "right"},
})
# 10 · TÚ
scenes.append({
    "chapter": 5, "number": "TÚ",
    "headline": "*Confiesa*",
    "narration": "Síguenos para más trucos. ¿Qué canción te pone a ti la piel de gallina?",
    "elements": [{"type": "follow", "trigger": "Síguenos"}, {"type": "ask", "text": "¿Qué *canción* te pone la piel de gallina?", "trigger": "Qué"}],
})

guion = {
    "topic": "Por qué se nos pone la piel de gallina",
    "categoria": "cuerpo",
    "title": "Por qué se te pone la piel de gallina (y qué tiene que ver un gato) 🐈",
    "source": "Fuentes: Shwartz et al., Cell (2020), laboratorio de Ya-Chieh Hsu (Harvard) · Science News (2020)",
    "chapters": ["?", "1", "2", "3", "+", "TÚ"],
    "outro_cta": "Todo tiene un truco",
    "cover": {"text": "¿Por qué la *piel de gallina*?", "badge": "UN REFLEJO HEREDADO", "scene": 0},
    "publish": {
        "caption": "Frío, un susto o tu canción favorita… y se te pone la piel de gallina. Es un músculo diminuto que levanta cada pelo, un reflejo que heredamos de antepasados mucho más peludos. ¿Qué canción te la pone a ti?",
        "description": "Junto a cada pelo hay un músculo diminuto, el músculo erector del pelo. Cuando el sistema nervioso simpático (el de «lucha o huida») le da la orden, se contrae, pone el pelo de punta y levanta un bultito en la piel. Es un reflejo heredado: a los mamíferos con mucho pelo, erizarlo les ayuda a atrapar aire y abrigarse, o a parecer más grandes, como hace un gato. En 2020, el equipo de Ya-Chieh Hsu en Harvard descubrió que ese nervio y ese músculo también regulan las células madre del folículo: en ratones, el frío las activa y el pelo crece antes. Fuentes: Shwartz et al., Cell (2020); Science News (2020).",
        "hashtags": ["pieldegallina", "cuerpohumano", "biologia", "ciencia", "curiosidades", "evolucion", "eltrucoes"],
    },
    "scenes": scenes,
}
assert len(guion["title"]) <= 70, len(guion["title"])
words = sum(len(s["narration"].split()) for s in scenes)
print("palabras:", words, "título:", len(guion["title"]))
(OUT / "guion.json").write_text(json.dumps(guion, ensure_ascii=False, indent=2), encoding="utf-8")
for n in ("brazo", "brazo_full", "corte", "abrigo", "gato_free"):
    shutil.copy(HERE / f"{n}.svg", OUT / f"{n}.svg")

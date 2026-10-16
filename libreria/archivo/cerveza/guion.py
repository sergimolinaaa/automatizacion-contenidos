import json, re, shutil, subprocess
from pathlib import Path

OUT = Path("/home/user/automatizacion-contenidos/content/lote4-04-cerveza-golpe")
HERE = Path(__file__).parent
OUT.mkdir(parents=True, exist_ok=True)
for f, cmd in (("escena", "escena.py"), ("escena_full", "full.py"), ("corte", "corte.py"), ("burbuja", "burbuja.py"), ("hongo", "hongo.py"), ("lago", "lago.py")):
    subprocess.run(f"cd {HERE} && python3 {cmd} > {f}.svg", shell=True, check=True)
    shutil.copy(HERE / f"{f}.svg", OUT / f"{f}.svg")


def H(*ids):
    return [{"target": i, "effect": "hide"} for i in ids]


scenes = [
    {
        "chapter": 0,
        "headline": "Un golpe y… *¡erupción!*",
        "narration": "Un golpecito en la boca de la botella… y la cerveza entra en erupción.",
        "illustration": {"svg_file": "escena_full.svg", "layout": "full", "caption": "Fig. 1 · El golpe", "anims": [
            {"target": "camera", "effect": "zoom", "to": [540, 760], "amount": 1.1},
            {"target": "bota", "effect": "move", "to": [-70, -80], "dur": 0.05},
            {"target": "bota", "effect": "move", "to": [70, 80], "trigger": "golpecito", "dur": 0.25},
            {"target": "impact", "effect": "pop", "trigger": "golpecito", "sfx": "chasquido"},
            {"target": "lgolpe", "effect": "pop", "trigger": "boca"},
            {"target": "ring1", "effect": "pop", "trigger": "boca"},
            {"target": "ring2", "effect": "pop", "trigger": "boca"},
            {"target": "ring1", "effect": "ripple", "phase": 0, "trigger": "boca"},
            {"target": "ring2", "effect": "ripple", "phase": 0.5, "trigger": "boca"},
            {"target": "botb", "effect": "shake", "amount": 0.4, "trigger": "boca"},
            {"target": "bota", "effect": "move", "to": [-110, -70], "rotate": -8, "trigger": "botella", "dur": 0.6},
            {"target": "impact", "effect": "hide", "trigger": "cerveza"},
            {"target": "lgolpe", "effect": "hide", "trigger": "cerveza"},
            {"target": "ring1", "effect": "hide", "trigger": "cerveza"},
            {"target": "ring2", "effect": "hide", "trigger": "cerveza"},
            {"target": "foam", "effect": "grow", "trigger": "erupción", "sfx": "burbujas"},
            {"target": "foam", "effect": "pulse", "amount": 0.4, "trigger": "erupción"},
            {"target": "drops", "effect": "pop", "trigger": "erupción"},
            {"target": "drops", "effect": "float", "amount": 0.6, "trigger": "erupción"},
            {"target": "puddle", "effect": "fade", "trigger": "erupción", "dur": 0.8},
            {"target": "camera", "effect": "zoom", "to": [540, 850], "amount": 1.08, "trigger": "erupción", "dur": 0.8},
        ]},
    },
    {"chapter": 0, "signature": True, "headline": "El truco es…", "narration": "El truco es…"},
    {
        "chapter": 1, "number": "1",
        "headline": "Una *onda* de presión",
        "narration": "El golpe sacude el vidrio y lanza ondas de presión por el líquido, como un sonido.",
        "illustration": {"svg_file": "corte.svg", "layout": "free", "caption": "Fig. 2 · Corte de la botella", "anims": H("lbub") + [
            {"target": "camera", "effect": "zoom", "to": [500, 330], "amount": 1.2},
            {"target": "golpe", "effect": "slide-down", "trigger": "golpe", "sfx": "whoosh"},
            {"target": "impact", "effect": "pop", "trigger": "sacude", "sfx": "chasquido"},
            {"target": "ring1", "effect": "pop", "trigger": "sacude"},
            {"target": "ring2", "effect": "pop", "trigger": "sacude"},
            {"target": "ring1", "effect": "ripple", "phase": 0, "trigger": "sacude"},
            {"target": "ring2", "effect": "ripple", "phase": 0.5, "trigger": "sacude"},
            {"target": "botb", "effect": "shake", "amount": 0.35, "trigger": "vidrio"},
            {"target": "camera", "effect": "zoom", "to": [500, 430], "amount": 1, "trigger": "lanza", "dur": 0.8},
            {"target": "w1", "effect": "slide-down", "trigger": "ondas"},
            {"target": "londa", "effect": "pop", "trigger": "presión"},
            {"target": "w2", "effect": "slide-down", "trigger": "presión"},
            {"target": "w3", "effect": "slide-down", "trigger": "líquido"},
            {"target": "down", "effect": "draw", "trigger": "líquido", "dur": 0.6},
            {"target": "w1", "effect": "pulse", "amount": 0.8, "trigger": "sonido"},
            {"target": "w2", "effect": "pulse", "amount": 0.8, "trigger": "sonido"},
            {"target": "w3", "effect": "pulse", "amount": 0.8, "trigger": "sonido"},
        ]},
    },
    {
        "chapter": 1, "number": "1",
        "headline": "Estira y *aplasta*",
        "narration": "Esas ondas estiran y aplastan, una y otra vez, las burbujitas que ya había dentro.",
        "illustration": {"svg_file": "burbuja.svg", "caption": "Fig. 3 · Al microscopio", "anims": H("burst", "hijas", "grandes", "lcav", "lhijas", "co2arr", "lco2") + [
            {"target": "co2", "effect": "drift", "amount": 0.25},
            {"target": "camera", "effect": "zoom", "to": [500, 380], "amount": 1.3},
            {"target": "estira", "effect": "pop", "trigger": "estiran", "sfx": "boing"},
            {"target": "madre", "effect": "pulse", "amount": 2.6, "trigger": "estiran"},
            {"target": "estira", "effect": "hide", "trigger": "aplastan"},
            {"target": "aplasta", "effect": "pop", "trigger": "aplastan"},
            {"target": "aplasta", "effect": "hide", "trigger": "otra"},
            {"target": "estira", "effect": "pop", "trigger": "otra"},
            {"target": "camera", "effect": "zoom", "to": [500, 350], "amount": 1, "trigger": "burbujitas", "dur": 0.8},
            {"target": "lmadre", "effect": "pop", "trigger": "burbujitas"},
            {"target": "madre", "effect": "punch", "trigger": "dentro"},
        ]},
    },
    {
        "chapter": 2, "number": "2",
        "headline": "*Cavitación*",
        "narration": "Hasta que colapsan y se rompen en nubes de burbujas diminutas. Es la cavitación.",
        "illustration": {"svg_file": "burbuja.svg", "caption": "Fig. 4 · Cavitación", "anims": H("grandes", "estira", "aplasta", "lhijas", "co2arr", "lco2", "lmadre") + [
            {"target": "co2", "effect": "drift", "amount": 0.25},
            {"target": "madre", "effect": "pulse", "amount": 3},
            {"target": "madre", "effect": "hide", "trigger": "colapsan"},
            {"target": "burst", "effect": "pop", "trigger": "colapsan", "sfx": "sorpresa"},
            {"target": "burst", "effect": "hide", "trigger": "rompen"},
            {"target": "hijas", "effect": "pop", "trigger": "rompen", "sfx": "burbujas"},
            {"target": "hijas", "effect": "pulse", "amount": 0.6, "trigger": "nubes"},
            {"target": "camera", "effect": "zoom", "to": [560, 330], "amount": 1.4, "trigger": "diminutas", "dur": 0.8},
            {"target": "lhijas", "effect": "pop", "trigger": "diminutas"},
            {"target": "camera", "effect": "zoom", "to": [500, 350], "amount": 1, "trigger": "Es", "dur": 0.7},
            {"target": "lhijas", "effect": "hide", "trigger": "cavitación"},
            {"target": "lcav", "effect": "pop", "trigger": "cavitación", "sfx": "sello"},
        ]},
    },
    {
        "chapter": 2, "number": "2",
        "headline": "Se *hinchan* de gas",
        "narration": "Son tan pequeñas que el gas disuelto entra en ellas rapidísimo… y crecen.",
        "illustration": {"svg_file": "burbuja.svg", "caption": "Fig. 5 · Entra el CO₂", "anims": H("madre", "burst", "estira", "aplasta", "lmadre", "lcav", "lhijas") + [
            {"target": "co2", "effect": "drift", "amount": 0.3},
            {"target": "hijas", "effect": "pulse", "amount": 0.5},
            {"target": "camera", "effect": "zoom", "to": [300, 420], "amount": 1.35, "trigger": "gas", "dur": 0.8},
            {"target": "lco2", "effect": "pop", "trigger": "gas"},
            {"target": "co2", "effect": "punch", "trigger": "disuelto"},
            {"target": "co2arr", "effect": "draw", "trigger": "entra", "dur": 0.6, "sfx": "whoosh"},
            {"target": "camera", "effect": "zoom", "to": [500, 350], "amount": 1, "trigger": "rapidísimo", "dur": 0.8},
            {"target": "hijas", "effect": "hide", "trigger": "crecen"},
            {"target": "grandes", "effect": "pop", "trigger": "crecen", "sfx": "pop"},
            {"target": "grandes", "effect": "pulse", "amount": 0.6, "trigger": "crecen"},
        ]},
        "mascot": {"trigger": "crecen", "pose": "surprise", "note": "Engordan a lo bestia", "side": "right"},
    },
    {
        "chapter": 3, "number": "3",
        "headline": "Un *hongo* de burbujas",
        "narration": "Al crecer, flotan y suben juntas formando un hongo, como el de una explosión.",
        "illustration": {"svg_file": "hongo.svg", "layout": "free", "caption": "Fig. 6 · Hongo de burbujas", "anims": H("foamtop", "overflow", "lespuma", "lvortex") + [
            {"target": "loose", "effect": "float", "amount": 0.8},
            {"target": "stem", "effect": "grow", "trigger": "flotan", "dur": 0.9},
            {"target": "capm", "effect": "slide-up", "trigger": "suben", "sfx": "burbujas"},
            {"target": "capm", "effect": "breathe", "amount": 1.2, "trigger": "suben"},
            {"target": "camera", "effect": "zoom", "to": [500, 520], "amount": 1.3, "trigger": "formando", "dur": 0.8},
            {"target": "lhongo", "effect": "pop", "trigger": "hongo"},
            {"target": "vl", "effect": "pop", "trigger": "explosión"},
            {"target": "vr", "effect": "pop", "trigger": "explosión"},
            {"target": "vl", "effect": "spin", "amount": -0.8, "trigger": "explosión"},
            {"target": "vr", "effect": "spin", "amount": 0.8, "trigger": "explosión"},
            {"target": "camera", "effect": "zoom", "to": [500, 430], "amount": 1, "trigger": "explosión", "dur": 0.9},
        ]},
    },
    {
        "chapter": 3, "number": "3",
        "headline": "*Desborde* total",
        "narration": "En un segundo, gran parte de la cerveza se convierte en espuma… y se desborda.",
        "elements": [{"type": "tag", "text": "En 1 segundo", "tone": "accent", "trigger": "segundo"}],
        "illustration": {"svg_file": "escena.svg", "caption": "Fig. 7 · Rebose", "anims": H("impact", "ring1", "ring2", "lgolpe") + [
            {"target": "bota", "effect": "move", "to": [-110, -70], "rotate": -8, "dur": 0.05},
            {"target": "foam", "effect": "grow", "trigger": "cerveza", "dur": 1.2, "sfx": "burbujas"},
            {"target": "foam", "effect": "pulse", "amount": 0.5, "trigger": "espuma"},
            {"target": "foam", "effect": "punch", "trigger": "desborda"},
            {"target": "drops", "effect": "pop", "trigger": "desborda", "sfx": "splash"},
            {"target": "drops", "effect": "float", "amount": 0.6, "trigger": "desborda"},
            {"target": "puddle", "effect": "fade", "trigger": "desborda", "dur": 0.6},
        ]},
    },
    {
        "chapter": 4, "number": "+",
        "headline": "Pasa hasta en *lagos*",
        "narration": "Y el mismo fenómeno ayuda a entender erupciones de gas en lagos, como la del lago Nyos, en Camerún.",
        "illustration": {"svg_file": "lago.svg", "caption": "Fig. 8 · Lago Nyos", "anims": [
            {"target": "plume", "effect": "float", "amount": 0.5},
            {"target": "camera", "effect": "zoom", "to": [500, 450], "amount": 1.35},
            {"target": "plume", "effect": "punch", "trigger": "fenómeno"},
            {"target": "camera", "effect": "zoom", "to": [600, 350], "amount": 1, "trigger": "erupciones", "dur": 0.8},
            {"target": "cloud", "effect": "slide-up", "trigger": "gas", "sfx": "whoosh"},
            {"target": "cloud", "effect": "drift", "amount": 0.3, "trigger": "gas"},
            {"target": "lco2", "effect": "pop", "trigger": "gas"},
            {"target": "flow", "effect": "draw", "trigger": "lagos", "dur": 0.7},
            {"target": "lnyos", "effect": "pop", "trigger": "Nyos"},
            {"target": "lyear", "effect": "pop", "trigger": "Camerún"},
        ]},
    },
    {
        "chapter": 5, "number": "TÚ",
        "headline": "Te *toca*",
        "narration": "Síguenos para más trucos. ¿Te atreverías a probarlo con un refresco… encima del sofá?",
        "elements": [
            {"type": "follow", "trigger": "Síguenos"},
            {"type": "ask", "text": "¿Te atreverías con un *refresco* encima del sofá?", "trigger": "Te"},
        ],
    },
]

g = {
    "topic": "Por qué la cerveza se desborda si golpeas la boca de la botella",
    "categoria": "cocina",
    "title": "Un golpecito y la botella entra en erupción: esta es la física 🫧",
    "source": "Fuente: Rodríguez-Rodríguez, Casado-Chacón & Fuster, Physical Review Letters 113, 214501 (2014)",
    "chapters": ["?", "1", "2", "3", "+", "TÚ"],
    "outro_cta": "Todo tiene un truco",
    "cover": {"text": "Un golpe y… *¡erupción!*", "scene": 0},
    "publish": {
        "caption": "Un golpecito en la boca de la botella y la espuma sale disparada 🫧 No es magia: es cavitación, la misma física que estudian en lagos que «explotan». ¿Te atreverías con un refresco encima del sofá?",
        "description": "Al golpear la boca de una botella con gas, el impacto lanza ondas de presión por el líquido que estiran y aplastan las burbujitas que ya había. Colapsan y se rompen en nubes de burbujas diminutas (cavitación); como tienen mucha superficie para su tamaño, el CO2 disuelto entra en ellas muy rápido y crecen. Después flotan y suben juntas formando una columna con forma de hongo, y en un segundo buena parte del líquido se convierte en espuma. Los autores relacionan el fenómeno con las erupciones de gas en lagos como el Nyos (Camerún). Fuente: J. Rodríguez-Rodríguez, A. Casado-Chacón y D. Fuster, «Physics of Beer Tapping», Physical Review Letters 113, 214501 (2014).",
        "hashtags": ["fisica", "ciencia", "burbujas", "curiosidades", "experimentos", "cocina", "eltrucoes"],
    },
    "scenes": scenes,
}

words_total = 0
for i, sc in enumerate(scenes):
    words = re.findall(r"[\wáéíóúñü]+", sc["narration"], re.I)
    words_total += len(words)
    trigs = [a.get("trigger") for a in sc.get("illustration", {}).get("anims", [])] + [e.get("trigger") for e in sc.get("elements", [])]
    if sc.get("mascot"):
        trigs.append(sc["mascot"]["trigger"])
    for t in trigs:
        if t and t not in words:
            print("TRIGGER NO ENCONTRADO", i, t)
    svg = sc.get("illustration", {}).get("svg_file")
    if svg:
        ids = set(re.findall(r'id="([^"]+)"', (OUT / svg).read_text()))
        for a in sc["illustration"]["anims"]:
            if a["target"] != "camera" and a["target"] not in ids:
                print("ID NO EXISTE", i, a["target"])
print("palabras:", words_total, "escenas:", len(scenes), "título:", len(g["title"]))
(OUT / "guion.json").write_text(json.dumps(g, ensure_ascii=False, indent=2), encoding="utf-8")

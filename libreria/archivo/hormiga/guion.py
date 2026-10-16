import json, re, shutil, subprocess, sys
from pathlib import Path

OUT = Path("/home/user/automatizacion-contenidos/content/lote4-03-hormiga-leon")
HERE = Path(__file__).parent
OUT.mkdir(parents=True, exist_ok=True)
for f, cmd in (("escena", "escena.py"), ("arriba", "arriba.py"), ("larva", "larva.py"), ("adulto", "adulto.py"), ("escena_full", "full.py"), ("adulto_free", "adulto.py free")):
    subprocess.run(f"cd {HERE} && python3 {cmd} > {f}.svg", shell=True, check=True)
    shutil.copy(HERE / f"{f}.svg", OUT / f"{f}.svg")


def H(*ids):
    return [{"target": i, "effect": "hide"} for i in ids]


ESC_ALL = ["angulo", "langulo", "aval", "avarrow", "laval", "tossarc", "toss", "sweat", "lant", "llarva", "husk"]


def esc_hide(*keep):
    return H(*[i for i in ESC_ALL if i not in keep])


scenes = [
    {
        "chapter": 0,
        "headline": "Le *disparan* arena",
        "narration": "Esta hormiga no resbala por torpe: alguien le dispara arena desde abajo.",
        "illustration": {"svg_file": "escena_full.svg", "layout": "full", "caption": "Fig. 1 · Corte de la trampa", "anims":
            esc_hide("tossarc", "toss", "aval", "sweat") + [
            {"target": "grass", "effect": "sway", "origin": "bottom", "amount": 0.4},
            {"target": "larva", "effect": "breathe", "amount": 0.6},
            {"target": "camera", "effect": "zoom", "to": [420, 850], "amount": 1.12},
            {"target": "ant", "effect": "shake", "amount": 0.4, "trigger": "resbala"},
            {"target": "aval", "effect": "fade", "trigger": "resbala", "dur": 0.4},
            {"target": "sweat", "effect": "pop", "trigger": "torpe"},
            {"target": "tossarc", "effect": "draw", "trigger": "dispara", "dur": 0.5, "sfx": "whoosh"},
            {"target": "toss", "effect": "pop", "trigger": "arena"},
            {"target": "camera", "effect": "zoom", "to": [560, 880], "amount": 1.15, "trigger": "abajo", "dur": 0.8},
            {"target": "larva", "effect": "punch", "trigger": "abajo"},
        ]},
    },
    {"chapter": 0, "signature": True, "headline": "El truco es…", "narration": "El truco es…"},
    {
        "chapter": 1, "number": "1",
        "headline": "Un *embudo* trampa",
        "narration": "Es una hormiga león, la larva de un insecto. Cava un embudo en espiral y se entierra en el fondo.",
        "illustration": {"svg_file": "arriba.svg", "caption": "Fig. 2 · Vista desde arriba", "anims": [
            {"target": "ant", "effect": "drift", "amount": 0.6},
            {"target": "jaws", "effect": "breathe", "amount": 0.8},
            {"target": "jaws", "effect": "punch", "trigger": "larva", "amount": 1.4, "sfx": "pop"},
            {"target": "spiral", "effect": "draw", "trigger": "Cava", "dur": 1.8, "sfx": "rotulador"},
            {"target": "lembudo", "effect": "pop", "trigger": "embudo"},
            {"target": "lespiral", "effect": "pop", "trigger": "espiral"},
            {"target": "camera", "effect": "zoom", "to": [516, 400], "amount": 1.7, "trigger": "entierra", "dur": 0.9},
            {"target": "llarva", "effect": "hide", "trigger": "entierra"},
            {"target": "lembudo", "effect": "hide", "trigger": "entierra"},
            {"target": "lespiral", "effect": "hide", "trigger": "entierra"},
            {"target": "jaws", "effect": "punch", "trigger": "fondo", "amount": 1.4},
        ]},
    },
    {
        "chapter": 1, "number": "1",
        "headline": "Al *borde* del derrumbe",
        "narration": "Sus paredes quedan casi en el ángulo de reposo: lo más empinadas posible sin derrumbarse.",
        "illustration": {"svg_file": "escena.svg", "caption": "Fig. 3 · Ángulo de reposo", "anims":
            esc_hide("angulo", "langulo") + [
            {"target": "grass", "effect": "sway", "origin": "bottom", "amount": 0.4},
            {"target": "larva", "effect": "breathe", "amount": 0.6},
            {"target": "ant", "effect": "bob", "amount": 0.2},
            {"target": "camera", "effect": "zoom", "to": [650, 330], "amount": 1.15, "trigger": "paredes", "dur": 0.8},
            {"target": "angulo", "effect": "draw", "trigger": "ángulo", "dur": 0.8, "sfx": "rotulador"},
            {"target": "langulo", "effect": "pop", "trigger": "reposo"},
            {"target": "angulo", "effect": "punch", "trigger": "empinadas"},
            {"target": "camera", "effect": "zoom", "to": [500, 350], "amount": 1, "trigger": "sin", "dur": 0.8},
            {"target": "ant", "effect": "shake", "amount": 0.5, "trigger": "derrumbarse"},
        ]},
    },
    {
        "chapter": 2, "number": "2",
        "headline": "Cañonazos de *arena*",
        "narration": "Si la presa intenta escapar, la larva le lanza arena con la cabeza.",
        "illustration": {"svg_file": "escena.svg", "caption": "Fig. 4 · Lluvia de arena", "anims":
            esc_hide("tossarc", "toss", "sweat", "lant") + [
            {"target": "grass", "effect": "sway", "origin": "bottom", "amount": 0.4},
            {"target": "lant", "effect": "pop", "trigger": "presa"},
            {"target": "ant", "effect": "shake", "amount": 0.5, "trigger": "intenta"},
            {"target": "sweat", "effect": "pop", "trigger": "escapar"},
            {"target": "lant", "effect": "hide", "trigger": "larva"},
            {"target": "camera", "effect": "zoom", "to": [420, 360], "amount": 1.35, "trigger": "lanza", "dur": 0.8},
            {"target": "larva", "effect": "punch", "trigger": "larva"},
            {"target": "tossarc", "effect": "draw", "trigger": "lanza", "dur": 0.5, "sfx": "whoosh"},
            {"target": "toss", "effect": "pop", "trigger": "arena"},
            {"target": "toss", "effect": "float", "amount": 0.4, "trigger": "arena"},
            {"target": "larva", "effect": "punch", "trigger": "cabeza", "amount": 1.4},
        ]},
    },
    {
        "chapter": 2, "number": "2",
        "headline": "Avalancha *provocada*",
        "narration": "Cada lluvia de arena provoca una avalancha que arrastra a la hormiga hasta el fondo.",
        "illustration": {"svg_file": "escena.svg", "caption": "Fig. 5 · Avalancha", "anims":
            esc_hide("tossarc", "toss", "aval", "avarrow", "laval", "sweat") + [
            {"target": "grass", "effect": "sway", "origin": "bottom", "amount": 0.4},
            {"target": "larva", "effect": "breathe", "amount": 0.6},
            {"target": "toss", "effect": "float", "amount": 0.4},
            {"target": "aval", "effect": "pop", "trigger": "avalancha", "sfx": "whoosh"},
            {"target": "laval", "effect": "pop", "trigger": "avalancha"},
            {"target": "avarrow", "effect": "draw", "trigger": "arrastra", "dur": 0.5},
            {"target": "aval", "effect": "move", "to": [40, 26], "trigger": "arrastra", "dur": 1.2},
            {"target": "ant", "effect": "move", "to": [150, 98], "trigger": "arrastra", "dur": 1.4},
            {"target": "sweat", "effect": "move", "to": [150, 98], "trigger": "arrastra", "dur": 1.4},
            {"target": "tossarc", "effect": "hide", "trigger": "arrastra"},
            {"target": "toss", "effect": "hide", "trigger": "arrastra"},
            {"target": "laval", "effect": "hide", "trigger": "fondo"},
            {"target": "avarrow", "effect": "hide", "trigger": "fondo"},
            {"target": "camera", "effect": "zoom", "to": [470, 400], "amount": 1.5, "trigger": "fondo", "dur": 0.8},
            {"target": "larva", "effect": "punch", "trigger": "fondo"},
        ]},
        "mascot": {"trigger": "fondo", "pose": "surprise", "note": "Tobogán de ida, sin vuelta", "side": "right"},
    },
    {
        "chapter": 3, "number": "3",
        "headline": "Mandíbulas *jeringa*",
        "narration": "Allí la atrapa con sus mandíbulas: funcionan como jeringas huecas.",
        "elements": [{"type": "stamp", "text": "¡ZAS!", "tone": "hot", "trigger": "atrapa", "sfx": "chasquido"}],
        "illustration": {"svg_file": "larva.svg", "caption": "Fig. 6 · Mandíbulas-jeringa", "anims": H("antdry", "ljugo", "flowout", "enz", "lenz", "inset", "lx40", "lhueca") + [
            {"target": "larva", "effect": "breathe", "amount": 0.8},
            {"target": "ant", "effect": "shake", "amount": 0.35},
            {"target": "camera", "effect": "zoom", "to": [380, 400], "amount": 1.35},
            {"target": "larva", "effect": "punch", "trigger": "atrapa"},
            {"target": "camera", "effect": "zoom", "to": [500, 350], "amount": 1, "trigger": "mandíbulas", "dur": 0.8},
            {"target": "inset", "effect": "pop", "trigger": "jeringas", "sfx": "pop"},
            {"target": "lx40", "effect": "pop", "trigger": "jeringas"},
            {"target": "lhueca", "effect": "pop", "trigger": "huecas"},
            {"target": "flowin", "effect": "flow", "amount": 1.2, "trigger": "huecas"},
        ]},
    },
    {
        "chapter": 3, "number": "3",
        "headline": "Se la *bebe*",
        "narration": "Le inyecta veneno y enzimas que le deshacen las entrañas… y luego se la bebe.",
        "illustration": {"svg_file": "larva.svg", "caption": "Fig. 7 · Digestión por fuera", "anims": H("antdry", "ljugo", "flowout", "enz", "lenz", "lhueca") + [
            {"target": "larva", "effect": "breathe", "amount": 0.8},
            {"target": "ant", "effect": "shake", "amount": 0.25},
            {"target": "flowin", "effect": "flow", "amount": 1.4},
            {"target": "flowin", "effect": "punch", "trigger": "inyecta"},
            {"target": "enz", "effect": "pop", "trigger": "veneno", "sfx": "burbujas"},
            {"target": "lenz", "effect": "pop", "trigger": "enzimas"},
            {"target": "enz", "effect": "pulse", "amount": 1.5, "trigger": "deshacen"},
            {"target": "camera", "effect": "zoom", "to": [330, 420], "amount": 1.4, "trigger": "entrañas", "dur": 0.8},
            {"target": "camera", "effect": "zoom", "to": [500, 350], "amount": 1, "trigger": "luego", "dur": 0.8},
            {"target": "lenz", "effect": "hide", "trigger": "luego"},
            {"target": "flowin", "effect": "hide", "trigger": "luego"},
            {"target": "flowout", "effect": "pop", "trigger": "luego"},
            {"target": "flowout", "effect": "flow", "amount": 1.4, "trigger": "luego"},
            {"target": "antdry", "effect": "fade", "trigger": "bebe", "dur": 0.8},
            {"target": "enz", "effect": "hide", "trigger": "bebe"},
            {"target": "ljugo", "effect": "pop", "trigger": "bebe", "sfx": "chorro"},
        ]},
    },
    {
        "chapter": 3, "number": "3",
        "headline": "Y *fuera* la basura",
        "narration": "Después lanza el cadáver vacío fuera del embudo.",
        "illustration": {"svg_file": "escena.svg", "caption": "Fig. 8 · Limpieza", "anims":
            esc_hide("husk") + H("ant") + [
            {"target": "grass", "effect": "sway", "origin": "bottom", "amount": 0.4},
            {"target": "larva", "effect": "breathe", "amount": 0.6},
            {"target": "larva", "effect": "punch", "trigger": "lanza", "amount": 1.4},
            {"target": "husk", "effect": "slide-up", "trigger": "lanza", "sfx": "whoosh"},
            {"target": "husk", "effect": "move", "to": [70, -30], "rotate": 40, "trigger": "cadáver", "dur": 1.2},
            {"target": "camera", "effect": "zoom", "to": [560, 290], "amount": 1.3, "trigger": "vacío", "dur": 0.8},
            {"target": "husk", "effect": "punch", "trigger": "fuera"},
        ]},
        "mascot": {"trigger": "embudo", "pose": "point", "note": "Ni las gracias le da", "side": "right"},
    },
    {
        "chapter": 4, "number": "+",
        "headline": "Adulta, *con alas*",
        "narration": "Y de adulta se transforma en esto: un insecto alado que parece una libélula, pero con antenas en maza.",
        "illustration": {"svg_file": "adulto_free.svg", "layout": "free", "caption": "Fig. 9 · Hormiga león adulta", "anims": H("inset", "evo", "lanos", "lalas", "lmaza") + [
            {"target": "camera", "effect": "zoom", "to": [520, 360], "amount": 1.15},
            {"target": "wingl", "effect": "sway", "origin": "right", "amount": 0.5},
            {"target": "wingr", "effect": "sway", "origin": "left", "amount": -0.5},
            {"target": "camera", "effect": "zoom", "to": [500, 430], "amount": 1, "trigger": "esto", "dur": 0.9, "sfx": "sorpresa"},
            {"target": "body", "effect": "punch", "trigger": "insecto"},
            {"target": "lalas", "effect": "pop", "trigger": "alado"},
            {"target": "wingl", "effect": "punch", "trigger": "libélula"},
            {"target": "wingr", "effect": "punch", "trigger": "libélula"},
            {"target": "lmaza", "effect": "pop", "trigger": "antenas"},
            {"target": "antennae", "effect": "punch", "trigger": "maza", "amount": 1.4},
        ]},
    },
    {
        "chapter": 4, "number": "+",
        "headline": "Años de *espera*",
        "narration": "Aunque antes puede pasar varios años como larva, enterrada y esperando.",
        "illustration": {"svg_file": "adulto.svg", "caption": "Fig. 10 · Antes, larva", "anims": H("lalas", "lmaza", "evo", "lanos") + [
            {"target": "wingl", "effect": "sway", "origin": "right", "amount": 0.4},
            {"target": "wingr", "effect": "sway", "origin": "left", "amount": -0.4},
            {"target": "camera", "effect": "zoom", "to": [260, 480], "amount": 1.45, "trigger": "antes", "dur": 0.8},
            {"target": "inset", "effect": "punch", "trigger": "antes"},
            {"target": "lanos", "effect": "pop", "trigger": "años", "sfx": "ding"},
            {"target": "evo", "effect": "draw", "trigger": "larva", "dur": 0.6},
            {"target": "inset", "effect": "breathe", "amount": 0.8, "trigger": "esperando"},
        ]},
    },
    {
        "chapter": 5, "number": "TÚ",
        "headline": "Te *toca*",
        "narration": "Síguenos para más trucos. ¿Cuántos pasos aguantarías tú en ese embudo?",
        "elements": [
            {"type": "follow", "trigger": "Síguenos"},
            {"type": "ask", "text": "¿Cuántos pasos *aguantarías* tú en ese embudo?", "trigger": "Cuántos"},
        ],
    },
]

g = {
    "topic": "La trampa de arena de la hormiga león",
    "categoria": "animales",
    "title": "Esta larva caza hormigas provocando avalanchas de arena 🐜",
    "source": "Fuentes: Fertin & Casas, J. Exp. Biol. (2006) · Franks et al., Proc. R. Soc. B (2019) · Büsse et al., bioRxiv (2020)",
    "chapters": ["?", "1", "2", "3", "+", "TÚ"],
    "outro_cta": "Todo tiene un truco",
    "cover": {"text": "Caza con *avalanchas*", "scene": 0},
    "publish": {
        "caption": "Esta hormiga no resbala por torpe: alguien le dispara arena desde abajo 🐜 La hormiga león construye un embudo perfecto y provoca avalanchas para cazar. ¿Tú cuánto aguantarías ahí dentro?",
        "description": "La hormiga león es la larva de un insecto neuróptero (familia Myrmeleontidae). Cava en espiral un embudo en la arena con las paredes casi en el ángulo de reposo y se entierra en el fondo. Cuando una presa intenta escapar, le lanza arena con la cabeza y provoca pequeñas avalanchas que la arrastran hasta sus mandíbulas, con las que le inyecta veneno y enzimas digestivas y después sorbe su interior. De adulta es un insecto alado parecido a una libélula. Fuentes: Fertin & Casas, J. Exp. Biol. (2006); Franks et al., Proc. R. Soc. B (2019); Büsse et al., bioRxiv (2020).",
        "hashtags": ["hormigaleon", "insectos", "animales", "ciencia", "curiosidades", "naturaleza", "eltrucoes"],
    },
    "scenes": scenes,
}

# comprobaciones: triggers presentes en la narración
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

"""Genera content/lote10-07-cristal-empanado/guion.json (anims con recetas de persona viva)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "content" / "lote10-07-cristal-empanado" / "guion.json"


def viva(p, fase=0.2, d=0.0, brazo_izq="top-right", brazo_der="top-left", der=True, izq=True):
    a = [{"target": f"{p}_cabeza", "effect": "sway", "origin": "bottom", "amount": 0.32, "delay": round(d + 0.25, 2)},
         {"target": f"{p}_ojos", "effect": "blink", "delay": round(d + 0.6, 2)}]
    if izq:
        a.append({"target": f"{p}_brazo_izq", "effect": "sway", "origin": brazo_izq, "amount": 0.16, "delay": round(d + 1.1, 2)})
    if der:
        a.append({"target": f"{p}_brazo_der", "effect": "sway", "origin": brazo_der, "amount": 0.24, "delay": round(d + 0.45, 2)})
    return a


def cuerpo(t, fase=0.2, d=0.0):
    return [{"target": t, "effect": "breathe", "origin": "bottom", "amount": 0.7, "phase": fase, "delay": d},
            {"target": t, "effect": "sway", "origin": "bottom", "amount": 0.12, "delay": round(d + 0.1, 2)}]


def lluvia(n=10):
    a = []
    for i in range(n):
        a.append({"target": f"gl{i}", "effect": "fall", "amount": 0.25 + 0.04 * (i % 4), "phase": round((i * 0.37) % 1, 2), "to": [0, 260]})
        a.append({"target": f"gl{i}", "effect": "drift", "amount": 0.3, "phase": round((i * 0.21) % 1, 2)})
    return a


# ---------------------------------------------------------------- 0 gancho
s0 = [
    {"target": "camera", "effect": "zoom", "delay": 0, "to": [540, 860], "amount": 1.06, "dur": 1.6},
    {"target": "lejos", "effect": "pan", "delay": 0, "to": [-30, 0], "dur": 5},
    {"target": "mu", "effect": "squash", "delay": 0, "dur": 0.6, "sfx": "boing"},
    *cuerpo("mu", 0.2, 0.7), *viva("mu", d=0.7, der=False),
    {"target": "mu_brazo_der", "effect": "wiggle", "origin": "bottom-left", "amount": 0.45, "delay": 0.7},
    *lluvia(),
    {"target": "vaho_borde", "effect": "hide"}, *[{"target": f"vaho_b{i}", "effect": "hide"} for i in range(4)],
    {"target": "duda", "effect": "hide"},
    {"target": "volante", "effect": "punch", "trigger": "coche", "amount": 0.08},
    {"target": "vaho_borde", "effect": "fade", "trigger": "empaña", "dur": 0.6, "sfx": "brillo"},
    {"target": "vaho_b0", "effect": "fade", "trigger": "cristal", "dur": 0.5},
    {"target": "vaho_b1", "effect": "fade", "trigger": "coche", "dur": 0.5},
    {"target": "vaho_b2", "effect": "fade", "trigger": "dentro", "dur": 0.5},
    {"target": "vaho_b3", "effect": "fade", "trigger": "justo", "dur": 0.5},
    {"target": "duda", "effect": "pop", "trigger": "dentro", "sfx": "pop"},
    {"target": "duda", "effect": "float", "trigger": "justo", "amount": 0.3},
    {"target": "mu", "effect": "move", "trigger": "por dentro", "to": [0, -14], "dur": 0.4},
    {"target": "mu_cabeza", "effect": "move", "trigger": "justo", "rotate": -7, "origin": "bottom", "dur": 0.6},
    {"target": "camera", "effect": "zoom", "trigger": "llueve", "to": [560, 860], "amount": 1.1, "dur": 1.0},
    {"target": "lluvia", "effect": "punch", "trigger": "llueve", "amount": 0.08},
]

# ---------------------------------------------------------------- 1 humedad
s1 = [
    {"target": "mh", "effect": "slide-up", "delay": 0, "dur": 0.5, "sfx": "whoosh"},
    *cuerpo("mh", 0.65, 0.5), *viva("mh", d=0.5),
    {"target": "ventana", "effect": "slide-down", "delay": 0.1, "dur": 0.5},
    {"target": "aliento", "effect": "hide"}, {"target": "ropag", "effect": "hide"}, {"target": "par", "effect": "hide"},
    {"target": "et_temp", "effect": "hide"}, {"target": "et_hum", "effect": "hide"},
    *[{"target": f"vp{i}", "effect": "hide"} for i in range(6)],
    {"target": "et_temp", "effect": "pop", "trigger": "templado", "sfx": "pop"},
    {"target": "mh_brazo_der", "effect": "move", "trigger": "templado", "rotate": -10, "origin": "top-left", "dur": 0.6},
    *[{"target": f"vp{i}", "effect": "pop", "trigger": w, "sfx": "pop" if i % 2 == 0 else "none"}
      for i, w in enumerate(("lleno", "lleno", "de humedad", "de humedad", "humedad", "humedad"))],
    *[{"target": f"vp{i}", "effect": "float", "amount": 0.3 + 0.05 * i, "delay": 0.2 * i} for i in range(6)],
    *[{"target": f"vp{i}", "effect": "drift", "amount": 0.5, "phase": round(0.17 * i, 2)} for i in range(6)],
    {"target": "et_hum", "effect": "pop", "trigger": "humedad", "sfx": "pop"},
    {"target": "aliento", "effect": "fade", "trigger": "aliento", "dur": 0.2, "sfx": "whoosh"},
    *[{"target": f"vh{i}", "effect": "puff", "phase": round(i / 3, 2), "to": [70, -110]} for i in range(3)],
    {"target": "mh_boca", "effect": "pulse", "trigger": "aliento", "amount": 0.5},
    {"target": "ropag", "effect": "pop", "trigger": "ropa", "sfx": "pop"},
    *[{"target": f"rg{i}", "effect": "bob", "amount": 0.4, "delay": 0.3 * i} for i in range(4)],
    {"target": "mh", "effect": "shake", "trigger": "mojada", "amount": 0.25},
    {"target": "par", "effect": "squash", "trigger": "paraguas", "to": [0, -160], "dur": 0.5, "sfx": "boing"},
    {"target": "par_tela", "effect": "sway", "origin": "bottom", "amount": 0.12, "trigger": "paraguas"},
    *[{"target": f"par_g{i}", "effect": "bob", "amount": 0.4, "delay": 0.25 * i} for i in range(3)],
    {"target": "camera", "effect": "zoom", "trigger": "la ropa", "to": [500, 360], "amount": 1.08, "dur": 1.2},
]

# ---------------------------------------------------------------- 2 cristal frío
s2 = [
    {"target": "cristal", "effect": "slide-up", "delay": 0, "dur": 0.5, "sfx": "whoosh"},
    {"target": "ter", "effect": "slide-up", "delay": 0.1, "dur": 0.5},
    *[{"target": f"m{i}", "effect": "slide-left", "delay": 0.05 * i, "dur": 0.5} for i in range(5)],
    *[{"target": f"m{i}", "effect": "float", "amount": 0.35, "delay": 0.5 + 0.13 * i} for i in range(5)],
    *[{"target": f"cp{i}", "effect": "spin", "amount": 0.08 + 0.03 * i} for i in range(3)],
    *[{"target": f"cp{i}", "effect": "drift", "amount": 0.5, "phase": 0.3 * i} for i in range(3)],
    {"target": "et_frio", "effect": "hide"}, {"target": "et_vapor", "effect": "hide"}, {"target": "vaso", "effect": "hide"},
    *[{"target": f"d{i}", "effect": "hide"} for i in range(5)], *[{"target": f"gv{i}", "effect": "hide"} for i in range(6)],
    {"target": "cristal", "effect": "punch", "trigger": "cristal", "amount": 0.15},
    {"target": "et_frio", "effect": "pop", "trigger": "frío", "sfx": "pop"},
    {"target": "ter", "effect": "shake", "trigger": "frío", "amount": 0.3},
    *[{"target": f"m{i}", "effect": "move", "trigger": "tocarlo", "to": [400 - x + 36, 0], "dur": 0.5 + 0.06 * i, "sfx": "whoosh" if i == 0 else "none"}
      for i, (x, y) in enumerate(((600, 230), (660, 360), (560, 470), (650, 590), (590, 700)))],
    {"target": "et_vapor", "effect": "pop", "trigger": "aire", "sfx": "pop"},
    *[{"target": f"m{i}", "effect": "hide", "trigger": "agua"} for i in range(5)],
    *[{"target": f"d{i}", "effect": "pop", "trigger": w, "sfx": "pop" if i % 2 == 0 else "none"}
      for i, w in enumerate(("agua", "agua", "en gotitas", "gotitas", "gotitas"))],
    *[{"target": f"d{i}", "effect": "bob", "amount": 0.25, "trigger": "como", "delay": 0} for i in range(5)],
    {"target": "et_vapor", "effect": "hide", "trigger": "como"},
    {"target": "vaso", "effect": "squash", "trigger": "como", "to": [0, -200], "dur": 0.55, "sfx": "boing"},
    *[{"target": f"gv{i}", "effect": "pop", "trigger": w, "sfx": "pop" if i % 2 == 0 else "none"}
      for i, w in enumerate(("vaso", "vaso", "con", "con", "hielo", "hielo"))],
    {"target": "camera", "effect": "zoom", "trigger": "vaso", "to": [500, 480], "amount": 1.05, "dur": 1.0},
]

# ---------------------------------------------------------------- 3 punto de rocío
s3 = [
    {"target": "esp", "effect": "squash", "delay": 0, "dur": 0.6, "sfx": "boing"},
    {"target": "ter3", "effect": "slide-up", "delay": 0.1, "dur": 0.5, "sfx": "whoosh"},
    {"target": "esp", "effect": "breathe", "origin": "bottom", "amount": 0.5, "delay": 0.7},
    {"target": "esp_agua", "effect": "hide"}, {"target": "marca", "effect": "hide"},
    {"target": "et_rocio", "effect": "hide"}, {"target": "et_cabe", "effect": "hide"}, {"target": "charco", "effect": "hide"},
    *[{"target": f"gs{i}", "effect": "hide"} for i in range(3)],
    {"target": "et_rocio", "effect": "pop", "trigger": "rocío", "sfx": "pop"},
    {"target": "ter3_columna", "effect": "grow", "origin": "bottom", "trigger": "temperatura", "dur": 0.8},
    {"target": "marca", "effect": "pop", "trigger": "temperatura", "sfx": "ding"},
    {"target": "esp_agua", "effect": "fade", "trigger": "aire", "dur": 0.9, "sfx": "chorro"},
    {"target": "esp", "effect": "shake", "trigger": "no puede", "amount": 0.4},
    {"target": "esp", "effect": "punch", "trigger": "puede", "amount": 0.3},
    *[{"target": f"gs{i}", "effect": "pop", "trigger": w, "sfx": "pop" if i != 1 else "none"} for i, w in enumerate(("con", "más", "vapor"))],
    *[{"target": f"gs{i}", "effect": "bob", "amount": 0.5, "delay": 0.2 * i} for i in range(3)],
    {"target": "charco", "effect": "fade", "trigger": "vapor", "dur": 0.4},
    {"target": "et_cabe", "effect": "pop", "trigger": "más", "sfx": "sorpresa"},
    {"target": "camera", "effect": "zoom", "trigger": "ya", "to": [500, 370], "amount": 1.06, "dur": 1.0},
]

# ---------------------------------------------------------------- 4 recirculación
s4 = [
    {"target": "brec", "effect": "squash", "delay": 0, "dur": 0.6, "sfx": "boing"},
    {"target": "car", "effect": "slide-left", "delay": 0.1, "dur": 0.5, "sfx": "whoosh"},
    {"target": "car_rueda_del", "effect": "spin", "amount": 0.02},
    {"target": "brec_luz", "effect": "hide"}, {"target": "asp", "effect": "hide"}, {"target": "cvaho", "effect": "hide"},
    {"target": "giro", "effect": "hide"}, {"target": "et_mismo", "effect": "hide"}, {"target": "et_vaho", "effect": "hide"},
    {"target": "brec", "effect": "punch", "trigger": "pones", "amount": 0.25, "sfx": "chasquido"},
    {"target": "brec_luz", "effect": "pop", "trigger": "recirculación", "sfx": "ding"},
    {"target": "brec_luz", "effect": "pulse", "trigger": "recirculación", "amount": 0.5},
    {"target": "giro", "effect": "pop", "trigger": "mueves", "sfx": "whoosh"},
    {"target": "giro", "effect": "spin", "trigger": "mueves", "amount": 0.6},
    {"target": "et_mismo", "effect": "pop", "trigger": "mismo", "sfx": "pop"},
    {"target": "cvaho", "effect": "fade", "trigger": "húmedo", "dur": 0.8},
    {"target": "asp", "effect": "draw", "trigger": "una", "dur": 0.4, "sfx": "rotulador"},
    {"target": "et_vaho", "effect": "pop", "trigger": "otra", "sfx": "sorpresa"},
    {"target": "car", "effect": "shake", "trigger": "vez", "amount": 0.3},
    {"target": "camera", "effect": "zoom", "trigger": "aire", "to": [560, 380], "amount": 1.06, "dur": 1.0},
]

# ---------------------------------------------------------------- 5 aire acondicionado
s5 = [
    {"target": "camera", "effect": "zoom", "delay": 0, "to": [540, 900], "amount": 1.05, "dur": 2.0},
    {"target": "lejos", "effect": "pan", "delay": 0, "to": [-30, 0], "dur": 8},
    {"target": "mujer", "effect": "squash", "delay": 0, "dur": 0.6, "sfx": "boing"},
    *cuerpo("mujer", 0.4, 0.7), *viva("md", d=0.7), *viva("mr", d=0.7),
    {"target": "mr", "effect": "hide"},
    *lluvia(),
    *[{"target": f"m{i}", "effect": "slide-down", "delay": 0.05 * i, "dur": 0.5} for i in range(6)],
    *[{"target": f"m{i}", "effect": "float", "amount": 0.35, "delay": 0.55 + 0.11 * i} for i in range(6)],
    {"target": "bac_luz", "effect": "hide"}, {"target": "duda5", "effect": "hide"}, {"target": "cpf", "effect": "hide"},
    {"target": "et_inv", "effect": "hide"}, {"target": "dest", "effect": "hide"}, {"target": "calor", "effect": "hide"},
    *[{"target": f"gd{i}", "effect": "hide"} for i in range(3)],
    {"target": "md_brazo_der", "effect": "move", "trigger": "funciona", "rotate": -12, "origin": "top-left", "dur": 0.6},
    {"target": "mr_brazo_der", "effect": "move", "trigger": "funciona", "rotate": -12, "origin": "top-left", "dur": 0.6},
    {"target": "duda5", "effect": "pop", "trigger": "error", "sfx": "sorpresa"},
    {"target": "duda5", "effect": "wiggle", "trigger": "error", "amount": 0.4},
    {"target": "md_cabeza", "effect": "move", "trigger": "parece", "rotate": 7, "origin": "bottom", "dur": 0.6},
    {"target": "bac", "effect": "punch", "trigger": "acondicionado", "amount": 0.35, "sfx": "chasquido"},
    {"target": "bac_luz", "effect": "pop", "trigger": "acondicionado", "sfx": "ding"},
    {"target": "bac_luz", "effect": "pulse", "trigger": "acondicionado", "amount": 0.5},
    {"target": "camera", "effect": "zoom", "trigger": "acondicionado", "to": [560, 1000], "amount": 1.1, "dur": 1.0},
    {"target": "duda5", "effect": "hide", "trigger": "en invierno"},
    {"target": "et_inv", "effect": "pop", "trigger": "invierno", "sfx": "pop"},
    {"target": "cpf", "effect": "pop", "trigger": "invierno"},
    {"target": "cpf", "effect": "spin", "trigger": "invierno", "amount": 0.1},
    *[{"target": f"m{i}", "effect": "move", "trigger": "Seca", "to": [540 - x + (i - 2.5) * 20, 1080 - y], "dur": 0.7 + 0.08 * i,
       "sfx": "whoosh" if i == 0 else "none"} for i, (x, y) in enumerate(((200, 620), (420, 700), (640, 640), (860, 720), (330, 860), (760, 880)))],
    {"target": "rejilla", "effect": "punch", "trigger": "aire y", "amount": 0.15},
    *[{"target": f"m{i}", "effect": "hide", "trigger": "aire y"} for i in range(6)],
    *[{"target": f"gd{i}", "effect": "pop", "trigger": "aire y", "sfx": "pop" if i == 0 else "none"} for i in range(3)],
    *[{"target": f"gd{i}", "effect": "move", "trigger": "algo", "to": [0, 90], "dur": 0.5} for i in range(3)],
    *[{"target": f"gd{i}", "effect": "hide", "trigger": "calor"} for i in range(3)],
    {"target": "et_inv", "effect": "hide", "trigger": "algo"},
    {"target": "calor", "effect": "pop", "trigger": "calor", "sfx": "pop"},
    {"target": "calor", "effect": "float", "trigger": "calor", "amount": 0.5},
    {"target": "camera", "effect": "zoom", "trigger": "calor", "to": [540, 900], "amount": 1.04, "dur": 1.2},
    {"target": "vaho_b0", "effect": "hide", "trigger": "calor"},
    {"target": "vaho_b1", "effect": "hide", "trigger": "despeja"},
    {"target": "vaho_b2", "effect": "hide", "trigger": "el cristal"},
    {"target": "vaho_b3", "effect": "hide", "trigger": "cristal"},
    {"target": "vaho_borde", "effect": "hide", "trigger": "cristal"},
    {"target": "md", "effect": "hide", "trigger": "despeja"},
    {"target": "mr", "effect": "fade", "trigger": "despeja", "dur": 0.15},
    {"target": "mr_brazo_der", "effect": "move", "trigger": "cristal", "rotate": -18, "origin": "top-left", "dur": 0.5},
    {"target": "dest", "effect": "pop", "trigger": "cristal", "sfx": "brillo"},
    {"target": "dest", "effect": "spin", "trigger": "cristal", "amount": 0.1},
]

# ---------------------------------------------------------------- guion
guion = {
    "topic": "¿Por qué se empañan por dentro los cristales del coche? El aire del interior está templado y cargado de humedad (aliento, ropa mojada, paraguas); al tocar el cristal frío baja de su punto de rocío y suelta el agua en gotitas, como un vaso con hielo. La recirculación lo empeora; el aire acondicionado, incluso en invierno, seca el aire y con algo de calor, aire exterior y chorro al parabrisas lo despeja (km77, Motor.es, Carglass)",
    "categoria": "objetos",
    "estilo": "papel",
    "title": "¿Por qué se empañan por dentro los cristales del coche?",
    "source": "Fuentes: km77 · Motor.es · Carglass",
    "chapters": ["?", "1", "2", "3", "+", "TÚ"],
    "outro_cta": "Todo tiene un truco",
    "cover": {"text": "Por qué se empañan los *cristales* del coche", "scene": 0},
    "publish": {
        "at": "2026-11-10T14:00:00+01:00",
        "caption": "¿Por qué se empaña el coche por dentro? El aire húmedo de tu aliento y la ropa mojada toca el cristal frío y suelta el agua: punto de rocío. Quita la recirculación y enciende el aire acondicionado aunque sea invierno: seca el aire (km77, Motor.es). ¿Tú cómo lo desempañas?",
        "description": "¿Por qué se empañan por dentro los cristales del coche? El aire del interior está templado y cargado de humedad por tu aliento, la ropa mojada y el paraguas. Cuando toca el cristal frío, baja de su punto de rocío y suelta el agua en gotitas, igual que un vaso con hielo. La recirculación lo empeora; lo que funciona es el aire acondicionado, incluso en invierno, porque seca el aire, con algo de calor, aire exterior y chorro al parabrisas. Fuentes: km77, Motor.es, Carglass. ¿Tú cómo lo desempañas?",
        "hashtags": ["coche", "conducir", "lluvia", "trucos", "ciencia"],
    },
    "scenes": [
        {"chapter": 0, "headline": "¿Niebla *dentro*?",
         "narration": "¿Por qué se empaña el cristal del coche por dentro justo cuando llueve?",
         "illustration": {"svg_file": "gancho_full.svg", "layout": "full", "caption": "Fig. 1 · ¡No veo nada!", "anims": s0}},
        {"chapter": 1, "number": "1", "headline": "Aire *húmedo*",
         "narration": "Dentro, el aire está templado y lleno de humedad: tu aliento, la ropa mojada, el paraguas.",
         "illustration": {"svg_file": "humedad_panel.svg", "layout": "panel", "caption": "Fig. 2 · Humedad", "anims": s1}},
        {"chapter": 1, "number": "1", "headline": "Cristal *frío*",
         "narration": "El cristal está frío: al tocarlo, el aire suelta el agua en gotitas, como un vaso con hielo.",
         "illustration": {"svg_file": "cristal_free.svg", "layout": "free", "height": 880, "caption": "Fig. 3 · Condensación", "anims": s2}},
        {"chapter": 2, "number": "2", "headline": "Punto *de rocío*",
         "narration": "Es el punto de rocío: la temperatura a la que el aire ya no puede con más vapor.",
         "illustration": {"svg_file": "rocio_panel.svg", "layout": "panel", "caption": "Fig. 4 · Esponja llena", "anims": s3}},
        {"chapter": 2, "number": "2", "headline": "*Recircular*: peor",
         "narration": "Si pones la recirculación, mueves el mismo aire húmedo una y otra vez.",
         "illustration": {"svg_file": "recirc_panel.svg", "layout": "panel", "caption": "Fig. 5 · En bucle", "anims": s4}},
        {"chapter": 3, "number": "3", "headline": "Aire *seco*",
         "narration": "Lo que funciona parece un error: el aire acondicionado en invierno. Seca el aire y, con algo de calor, despeja el cristal.",
         "illustration": {"svg_file": "ac_full.svg", "layout": "full", "caption": "Fig. 6 · Aire seco", "anims": s5}},
        {"chapter": 4, "number": "+", "headline": "Aire de *fuera*",
         "narration": "Así que aire de fuera, aire acondicionado y chorro al parabrisas.",
         "mascot": {"trigger": "Así", "pose": "cheer", "note": "¡Adiós, vaho!", "side": "right"},
         "elements": [{"type": "tag", "text": "AIRE DE FUERA", "tone": "ink", "trigger": "fuera", "sfx": "pop"},
                      {"type": "tag", "text": "A/C ENCENDIDO", "tone": "hot", "trigger": "acondicionado", "sfx": "pop"},
                      {"type": "stamp", "text": "AL PARABRISAS", "tone": "accent", "trigger": "parabrisas", "sfx": "sello"}]},
        {"chapter": 5, "headline": "Dudas → *truco*", "narration": "Tú traes las dudas y nosotros te damos el truco.",
         "elements": [{"type": "trick", "trigger": "Tú", "reveal_trigger": "nosotros"}]},
        {"chapter": 5, "number": "TÚ", "headline": "*Confiesa*", "narration": "Síguenos y las resolvemos. ¿Tú cómo lo desempañas?",
         "elements": [{"type": "follow", "trigger": "Síguenos"}, {"type": "ask", "text": "¿Tú cómo lo *desempañas*?", "trigger": "¿Tú"}]},
    ],
}
OUT.write_text(json.dumps(guion, ensure_ascii=False, indent=1) + "\n")
print("ok", OUT, sum(len(s["narration"].split()) for s in guion["scenes"]), "palabras")

"""lote9-06-miedo-oscuridad: escribe content/lote9-06-miedo-oscuridad/guion.json (animaciones con el método rossark).
Uso: python3 libreria/archivo/miedo-oscuridad/guion.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "content" / "lote9-06-miedo-oscuridad" / "guion.json"


def A(target, effect, **k):
    d = {"target": target, "effect": effect}
    d.update(k)
    return d


def persona_viva(pid, phase=0.0, blink=0.5, cabeza=0.25, brazos=True, sway=0.15):
    """Respira, parpadea, balancea el cuerpo y la cabeza llega después; brazos con fases distintas (nunca en espejo)."""
    o = [A(pid, "breathe", origin="bottom", amount=0.6, phase=phase),
         A(f"{pid}_ojos", "blink", delay=blink),
         A(f"{pid}_cabeza", "sway", origin="bottom", amount=cabeza, delay=blink - 0.15)]
    if sway:
        o.append(A(pid, "sway", origin="bottom", amount=sway, delay=0.3 + phase))
    if brazos:
        o += [A(f"{pid}_brazo_izq", "sway", origin="top-right", amount=0.18, delay=0.5 + phase),
              A(f"{pid}_brazo_der", "sway", origin="top-left", amount=0.12, delay=0.85 + phase)]
    return o


# ---------------------------------------------------------------- 0. gancho: apagas la luz
s0 = [
    # la niña ya está en la cama, viva desde el primer fotograma
    A("nina", "breathe", origin="bottom", amount=0.5, phase=0.2),
    A("ninaN_ojos", "blink", delay=0.35),
    A("ninaN_cabeza", "sway", origin="bottom", amount=0.25, delay=0.2),
    A("ninaS", "hide"),
    A("perch_abrigo", "sway", origin="top", amount=0.08, delay=0.4),
    # la mano entra ya en movimiento y pulsa el interruptor
    A("sw_tecla", "move", delay=0.0, to=[0, 41], dur=0.05),
    A("mano", "slide-up", delay=0.0, dur=0.5, sfx="whoosh"),
    A("mano", "move", trigger="Apagas", to=[0, -26], dur=0.22),
    A("sw_tecla", "move", trigger="Apagas", to=[0, -41], dur=0.25, sfx="chasquido"),
    A("mano", "move", trigger="luz", to=[0, 300], dur=0.7),
    A("velo", "fade", trigger="luz", dur=0.4),
    # cualquier ruido
    A("ondas", "pop", trigger="cualquier", origin="left", sfx="pop"),
    A("ondas", "pulse", trigger="cualquier", amount=0.7),
    A("cric", "pop", trigger="ruido", sfx="boing"),
    A("cric", "wiggle", trigger="ruido", amount=0.4),
    A("ninaN_cabeza", "move", trigger="ruido", rotate=-7, origin="bottom", dur=0.45),
    # la sombra del abrigo se vuelve un monstruo
    A("monstruo", "fade", trigger="parece", dur=0.5),
    A("monstruo", "sway", trigger="parece", origin="bottom", amount=0.08),
    A("monstruo_ojos", "pop", trigger="monstruo", sfx="sorpresa"),
    A("monstruo_ojos", "pulse", trigger="monstruo", amount=0.8),
    A("ninaN", "hide", trigger="monstruo"),
    A("ninaS", "fade", trigger="monstruo", dur=0.15),
    A("ninaS_ojos", "blink", delay=3.0),
    A("cama_manta", "move", trigger="monstruo", to=[0, -48], dur=0.45),
    A("nina", "shake", trigger="monstruo", amount=0.3),
    A("temb", "pop", trigger="monstruo"),
    A("temb", "wiggle", trigger="monstruo", amount=0.8),
]

# ---------------------------------------------------------------- 1. vivimos de la vista
s1 = [
    A("ojo", "pop", delay=0.0, dur=0.5),
    A("ojo", "blink", delay=1.2),
    A("ojo_iris", "move", delay=0.5, to=[34, -6], dur=0.6),
    A("ojo_brillo", "pulse", amount=0.4, delay=0.6),
    A("ojo_iris", "move", trigger="vista", to=[-34, 6], dur=0.6),
    A("velo", "hide"),
    A("duda", "hide"),
    A("x", "hide"),
]
for i in range(5):
    s1 += [A(f"b{i}", "grow", delay=0.35 + 0.07 * i, origin="bottom", dur=0.6, **({"sfx": "pop"} if i == 0 else {})),
           A(f"i{i}", "pop", delay=0.45 + 0.07 * i)]
s1 += [
    A("b0", "punch", trigger="sobre", amount=0.3),
    A("i0", "pulse", trigger="todo", amount=0.6),
    A("velo", "fade", trigger="oscuras", dur=0.4, sfx="whoosh"),
    A("duda", "pop", trigger="perdemos", sfx="pop"),
    A("duda", "wiggle", trigger="perdemos", amount=0.4),
    A("x", "pop", trigger="mejor", sfx="chasquido"),
    A("b0", "shake", trigger="sentido", amount=0.3),
]

# ---------------------------------------------------------------- 2. la noche era peligrosa
s2 = [
    A("fuego_llama", "sway", origin="bottom", amount=0.6),
    A("fuego_llama", "pulse", amount=0.35, phase=0.3),
    A("fuego_llama_in", "sway", origin="bottom", amount=0.9, phase=0.55),
    A("fuego_brillo", "pulse", amount=0.25, phase=0.2),
    A("fuego_chispas", "float", amount=0.8),
    A("acacia_copa", "sway", origin="bottom", amount=0.08),
    A("hierba", "sway", origin="bottom", amount=0.12, delay=0.2),
    A("padreG", "slide-right", delay=0.0, dur=0.5, sfx="whoosh"),
    A("ninoG", "slide-up", delay=0.12, dur=0.5),
    A("madreG", "slide-left", delay=0.2, dur=0.5),
] + persona_viva("padre", 0.0, 0.6, 0.25) + persona_viva("nino", 0.35, 0.9, 0.3) + persona_viva("madre", 0.7, 1.3, 0.2)
s2 += [
    A("tant", "pop", trigger="antepasados", sfx="pop"),
    A("tant", "float", trigger="antepasados", amount=0.2),
    A("fuego", "punch", trigger="noche", amount=0.15),
    A("leona", "hide"),
    A("ojosh", "pop", trigger="peligrosa", sfx="brillo"),
    A("ojosh", "pulse", trigger="peligrosa", amount=0.8),
    A("ojosh", "hide", trigger="depredadores"),
    A("leona", "fade", trigger="depredadores", dur=0.5),
    A("leona_ojos", "pulse", trigger="depredadores", amount=0.8),
    A("leona_cuerpo", "breathe", trigger="depredadores", amount=0.5),
    A("leona_cola", "sway", trigger="depredadores", origin="left", amount=0.5),
    A("tdep", "pop", trigger="depredadores", sfx="pop"),
    A("leona", "move", trigger="como", to=[-36, 0], dur=1.2),
    A("leona_cabeza", "move", trigger="leones", rotate=-4, origin="right", dur=0.6),
    A("alerta", "pop", trigger="leones", sfx="sorpresa"),
    A("alerta", "pulse", trigger="leones", amount=0.7),
    A("madre_cabeza", "move", trigger="cazan", rotate=7, origin="bottom", dur=0.55),
    A("nino_cabeza", "move", trigger="leones", rotate=6, origin="bottom", dur=0.55),
]

# ---------------------------------------------------------------- 3. Tanzania y la luna
s3 = [
    A("mapa", "slide-up", delay=0.0, dur=0.5, sfx="whoosh"),
    A("mapa_tz", "hide"),
    A("mapa_tz", "pop", trigger="Tanzania", sfx="pop"),
    A("mapa_tz", "pulse", trigger="Tanzania", amount=0.4),
    A("ttz", "pop", trigger="Tanzania"),
    A("cnt_0", "pop", delay=0.15),
    A("tat", "slide-up", trigger="ataques", dur=0.4),
    A("leon", "pop", trigger="leones", sfx="pop"),
    A("leon", "wiggle", trigger="leones", amount=0.3),
]
cnt = ["cnt_0", "cnt_1", "cnt_2", "cnt_3", "cnt_4", "cnt"]
pasos = ["cientos", "de ataques", "ataques", "de leones", "vio"]
for k in range(1, 6):
    s3 += [A(cnt[k], "hide")]
for k, trig in enumerate(pasos):
    s3 += [A(cnt[k], "hide", trigger=trig), A(cnt[k + 1], "pop", trigger=trig, dur=0.2, **({"sfx": "ding"} if k == 4 else {}))]
s3 += [A("cnt", "pulse", trigger="vio", amount=0.3)]
for i, trig in enumerate(["un", "estudio", "cientos", "ataques", "leones"]):
    s3 += [A(f"luna{i}", "pop", trigger=trig), A(f"luna{i}", "float", trigger=trig, amount=0.15, phase=0.2 * i)]
for i, trig in enumerate(["vio", "que", "se", "disparaban", "tras"]):
    s3 += [A(f"bar{i}", "grow", trigger=trig, origin="bottom", dur=0.6, **({"sfx": "pop"} if i >= 3 else {}))]
s3 += [
    A("tdesp", "pop", trigger="disparaban", sfx="pop"),
    A("tllena", "pop", trigger="luna", sfx="pop"),
    A("luna2", "punch", trigger="llena", amount=0.3),
    A("bar4", "punch", trigger="cuando", amount=0.15),
    A("cielo", "fade", trigger="anochece", dur=0.4),
    A("rel", "pop", trigger="anochece", sfx="pop"),
    A("rel_minutero", "spin", trigger="más", origin="bottom", amount=0.4),
    A("cielo", "pulse", trigger="oscuro", amount=0.25),
]

# ---------------------------------------------------------------- 4. el cerebro rellena
s4 = [
    A("cabG", "slide-right", delay=0.0, dur=0.5, sfx="whoosh"),
    A("cabG", "sway", origin="bottom", amount=0.08, delay=0.5),
    A("bal0", "slide-up", delay=0.2, dur=0.5),
    A("bal1", "hide"),
    A("hueco", "pop", trigger="oscuras", sfx="pop"),
    A("hueco", "pulse", trigger="oscuras", amount=0.15),
    A("garras", "pop", trigger="rellena", sfx="chasquido"),
    A("garras", "wiggle", trigger="rellena", amount=0.3),
    A("thueco", "slide-up", trigger="rellena", dur=0.4),
    A("ojos0", "pop", trigger="huecos", sfx="pop"),
    A("ojos0", "blink", delay=3.2),
    A("ojos1", "pop", trigger="con"),
    A("ojos1", "blink", delay=3.9),
    A("colmillos", "pop", trigger="amenazas", sfx="pop"),
    A("colmillos", "bob", trigger="amenazas", amount=0.3),
    A("tmejor", "pop", trigger="mejor", sfx="pop"),
    A("bal0", "hide", trigger="asustarse"),
    A("bal1", "fade", trigger="asustarse", dur=0.25, sfx="boing"),
    A("bal1", "punch", trigger="más", amount=0.15),
]

# ---------------------------------------------------------------- 5. no es cosa de niños
s5 = [
    A("cama2G", "slide-up", delay=0.0, dur=0.5, sfx="whoosh"),
    A("uniG", "breathe", origin="bottom", amount=0.5, phase=0.3),
    A("uni_ojos", "blink", delay=0.6),
    A("uniG", "sway", origin="bottom", amount=0.1, delay=0.4),
    A("luna_c", "pop", trigger="cosa", sfx="pop"),
    A("luna_c", "float", trigger="cosa", amount=0.25),
    A("tpiloto", "pop", trigger="estudio", sfx="pop"),
    A("canada", "slide-right", trigger="canadiense", dur=0.5, sfx="whoosh"),
    A("canada", "sway", trigger="canadiense", origin="left", amount=0.4),
    A("tcan", "pop", trigger="canadiense"),
    A("arco", "draw", trigger="casi", dur=1.2, sfx="rotulador"),
    A("tmitad", "pop", trigger="mitad", sfx="pop"),
    A("tuni", "pop", trigger="universitarios", sfx="pop"),
    A("tmal", "slide-up", trigger="dormían", dur=0.4),
    A("uniG", "shake", trigger="miedo", amount=0.25),
    A("tmitad", "punch", trigger="admitió", amount=0.3),
]

# ---------------------------------------------------------------- 6. feliz Halloween
s6 = [
    A("cala", "slide-up", delay=0.0, dur=0.5, sfx="whoosh"),
    A("cala_luz", "pulse", amount=0.5, delay=0.3),
    A("cala_tallo", "sway", origin="bottom", amount=0.3, delay=0.5),
    A("luna", "float", amount=0.2),
    A("fanN", "slide-left", delay=0.1, dur=0.55),
    A("fanN_tela", "sway", origin="top", amount=0.2, delay=0.4),
    A("fanN_ojos", "blink", delay=0.9),
    A("fanN_cuerpo", "breathe", origin="bottom", amount=0.6, delay=0.2),
    A("fanS", "hide"),
    A("sombra", "grow", trigger="Halloween", origin="bottom", dur=0.8, sfx="whoosh"),
    A("sombra", "sway", trigger="Halloween", origin="bottom", amount=0.1),
    A("fanN", "hide", trigger="asustas"),
    A("fanS", "fade", trigger="asustas", dur=0.15),
    A("fanS", "shake", trigger="asustas", amount=0.4),
    A("fanS_tela", "sway", trigger="asustas", origin="top", amount=0.3),
    A("alerta", "pop", trigger="oscuras", sfx="sorpresa"),
    A("alerta", "pulse", trigger="oscuras", amount=0.6),
    A("tinst", "pop", trigger="instinto", sfx="ding"),
    A("tinst", "punch", trigger="instinto", amount=0.3),
]

closing = [
    {"chapter": 5, "headline": "Dudas → *truco*", "narration": "Tú traes las dudas y nosotros te damos el truco.",
     "elements": [{"type": "trick", "trigger": "Tú", "reveal_trigger": "nosotros"}]},
    {"chapter": 5, "number": "TÚ", "headline": "*Confiesa*",
     "narration": "Síguenos y las resolvemos. ¿Tú duermes con alguna luz encendida?",
     "elements": [{"type": "follow", "trigger": "Síguenos"},
                  {"type": "ask", "text": "¿Tú duermes con alguna *luz* encendida?", "trigger": "¿Tú"}]},
]


def ill(svg, layout, caption, anims, height=None):
    d = {"svg_file": svg, "layout": layout}
    if height:
        d["height"] = height
    d["caption"] = caption
    d["anims"] = anims
    return d


guion = {
    "topic": "¿Por qué te da miedo la oscuridad? Dependemos de la vista, la noche era de los depredadores (ataques de leones en Tanzania tras la luna llena, PLoS ONE 2011), el cerebro rellena con amenazas y casi la mitad de los universitarios que dormían mal lo admitió (Carney, SLEEP 2012)",
    "categoria": "psicologia",
    "title": "¿Por qué te da miedo la oscuridad? Culpa de tus antepasados",
    "source": "Fuentes: PLoS ONE · Live Science · National Geographic · ScienceAlert · AASM",
    "chapters": ["?", "1", "2", "3", "+", "TÚ"],
    "outro_cta": "Todo tiene un truco",
    "cover": {"text": "Por qué da miedo la *oscuridad*", "scene": 0},
    "publish": {
        "at": "2026-10-31T14:00:00+01:00",
        "caption": "¿Por qué te da miedo la oscuridad? Vivimos de la vista, y de noche cazaban los leones: en Tanzania sus ataques eran más frecuentes en las noches más oscuras (PLoS ONE 2011). Tu cerebro rellena lo que no ve con amenazas. Feliz Halloween. ¿Tú duermes con alguna luz encendida?",
        "description": "¿Por qué te da miedo la oscuridad? Los humanos dependemos sobre todo de la vista, y durante miles de años la noche fue el momento de los depredadores. Un estudio publicado en PLoS ONE (2011) con cientos de ataques de leones en Tanzania vio que eran de dos a cuatro veces más frecuentes en los días tras la luna llena, cuando el anochecer es más oscuro. Por eso, cuando no ve, el cerebro rellena los huecos con amenazas. Y no es cosa de niños: en un estudio piloto de la Universidad Ryerson (2012), casi la mitad de los universitarios que dormían mal admitió miedo a la oscuridad. Fuentes: ScienceAlert, Live Science, National Geographic, American Academy of Sleep Medicine. ¿Tú duermes con alguna luz encendida?",
        "hashtags": ["halloween", "miedo", "psicologia", "cerebro", "curiosidades"],
    },
    "scenes": [
        {"chapter": 0, "headline": "¿Un *monstruo*?",
         "narration": "¿Apagas la luz y cualquier ruido parece un monstruo?",
         "illustration": ill("gancho_full.svg", "full", "Fig. 1 · A oscuras", s0)},
        {"chapter": 1, "number": "1", "headline": "Vivimos de la *vista*",
         "narration": "Los humanos dependemos sobre todo de la vista. A oscuras, perdemos nuestro mejor sentido.",
         "illustration": ill("vista_free.svg", "free", "Fig. 2 · La vista", s1, 860)},
        {"chapter": 1, "number": "1", "headline": "La noche era *peligrosa*",
         "narration": "Para nuestros antepasados, la noche era peligrosa: es cuando cazan depredadores como los leones.",
         "illustration": ill("sabana_full.svg", "full", "Fig. 3 · La sabana de noche", s2)},
        {"chapter": 2, "number": "2", "headline": "Más ataques a *oscuras*",
         "narration": "En Tanzania, un estudio de cientos de ataques de leones vio que se disparaban tras la luna llena, cuando anochece más oscuro.",
         "illustration": ill("tanzania_free.svg", "free", "Fig. 4 · Leones y luna", s3, 880)},
        {"chapter": 2, "number": "2", "headline": "El cerebro *rellena*",
         "narration": "Por eso, a oscuras, tu cerebro rellena los huecos con amenazas: mejor asustarse de más.",
         "illustration": ill("rellena_free.svg", "free", "Fig. 5 · Mejor pasarse", s4, 860)},
        {"chapter": 3, "number": "3", "headline": "No es cosa de *niños*",
         "narration": "Y no es cosa de niños: en un estudio canadiense, casi la mitad de los universitarios que dormían mal admitió ese miedo.",
         "illustration": ill("adultos_free.svg", "free", "Fig. 6 · Estudio piloto", s5, 860)},
        {"chapter": 4, "number": "+", "headline": "Feliz *Halloween*",
         "narration": "Esta noche de Halloween, si te asustas a oscuras, no eres miedica: es instinto.",
         "mascot": {"trigger": "miedica", "pose": "cheer", "note": "¡Feliz Halloween!", "side": "right"},
         "illustration": ill("halloween_free.svg", "free", "Fig. 7 · Halloween", s6, 640)},
    ] + closing,
}
OUT.write_text(json.dumps(guion, ensure_ascii=False, indent=2) + "\n")
print("ok", OUT)

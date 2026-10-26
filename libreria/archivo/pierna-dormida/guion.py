"""lote9-02-pierna-dormida: escribe content/lote9-02-pierna-dormida/guion.json (animaciones con el método rossark).
Uso: python3 libreria/archivo/pierna-dormida/guion.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "content" / "lote9-02-pierna-dormida" / "guion.json"


def A(target, effect, **k):
    d = {"target": target, "effect": effect}
    d.update(k)
    return d


# ---------------------------------------------------------------- 0. gancho
s0 = [
    # sentada en el sofá: respira y se prepara para levantarse desde el primer fotograma
    A("luS", "breathe", origin="bottom", amount=0.7, phase=0.2),
    A("luS_ojos", "blink", delay=0.2),
    A("luS", "move", delay=0.0, to=[0, -26], dur=0.45),
    A("luS_cabeza", "move", delay=0.12, rotate=-5, origin="bottom", dur=0.45),
    A("luS", "hide", trigger="levantas"),
    # de pie: entra desde abajo (se levanta) y la cabeza llega después del cuerpo
    A("luG", "move", delay=0.0, to=[0, 70], dur=0.05),
    A("luG", "fade", trigger="levantas", dur=0.2, sfx="whoosh"),
    A("luG", "move", trigger="levantas", to=[0, -70], dur=0.55),
    A("lu", "breathe", origin="bottom", amount=0.6, phase=0.6),
    A("lu_cabeza", "move", trigger="sofá", rotate=-5, origin="bottom", dur=0.5),
    A("lu_cabeza", "sway", origin="bottom", amount=0.3, delay=1.5),
    A("lu_ojos", "blink", delay=1.1),
    A("lu_brazo_izq", "sway", origin="top-right", amount=0.22, delay=0.8),
    A("lu_brazo_der", "sway", origin="top-left", amount=0.16, delay=1.3),
    A("fpierna", "draw", trigger="pierna", dur=0.45, sfx="rotulador"),
    A("fpierna", "flow", trigger="parece", amount=0.5),
    # pierna de corcho: cojea (el peso pasa a la otra pierna) y la cabeza compensa un poco después
    A("corcho", "fade", trigger="corcho", dur=0.35, sfx="brillo"),
    A("luG", "move", trigger="parece", rotate=-4, origin="bottom", dur=0.55),
    A("lu_cabeza", "move", trigger="corcho", rotate=8, origin="bottom", dur=0.5),
    A("luG", "sway", trigger="corcho", origin="bottom", amount=0.18),
    A("duda", "pop", trigger="parece", origin="bottom-left", sfx="pop"),
    A("duda", "wiggle", trigger="parece", amount=0.4),
    A("ay", "pop", trigger="corcho", sfx="boing"),
    A("ay", "float", trigger="corcho", amount=0.35),
    # hormiguitas que suben por la pierna (cada una a su ritmo) y chispas
    A("hg0", "pop", trigger="llena", sfx="pop"),
    A("hg1", "pop", trigger="de hormiguitas"),
    A("hg2", "pop", trigger="hormiguitas"),
    A("hg3", "pop", delay=3.05),
    A("hg4", "pop", delay=3.3),
    A("hg0", "move", trigger="llena", to=[-6, -150], dur=2.6),
    A("hg1", "move", trigger="de hormiguitas", to=[4, -120], dur=2.2),
    A("hg2", "move", trigger="hormiguitas", to=[-4, -110], dur=2.4),
    A("hg3", "move", delay=3.05, to=[6, -140], dur=2.0),
    A("hg4", "move", delay=3.3, to=[-2, -90], dur=2.3),
    A("h0_patas", "wiggle", trigger="llena", amount=1.2),
    A("h1_patas", "wiggle", trigger="hormiguitas", amount=1.0),
    A("h2_patas", "wiggle", trigger="hormiguitas", amount=1.3),
    A("h3_patas", "wiggle", delay=3.1, amount=1.1),
    A("h4_patas", "wiggle", delay=3.35, amount=1.2),
    A("ch0", "pop", trigger="llena"),
    A("ch1", "pop", trigger="de hormiguitas"),
    A("ch2", "pop", trigger="hormiguitas", sfx="brillo"),
    A("ch3", "pop", delay=3.2),
    A("ch0", "pulse", trigger="llena", amount=1.4),
    A("ch1", "pulse", trigger="de hormiguitas", amount=1.6),
    A("ch2", "pulse", trigger="hormiguitas", amount=1.2),
    A("ch3", "pulse", delay=3.2, amount=1.5),
]

# ---------------------------------------------------------------- 1. cruzar las piernas
px = 150 + 740 * 0.30
xs = (px + 100, px + 145, px + 190)
stops = (px + 48, px + 78, px + 108)
s1 = [
    A("asientoG", "slide-up", delay=0.0, dur=0.5, sfx="whoosh"),
    A("pbG", "slide-up", delay=0.06, dur=0.5),
    A("espG", "slide-up", delay=0.06, dur=0.5),
    A("espG", "move", delay=0.0, to=[0, -80], dur=0.05),
    A("ptG", "move", delay=0.0, to=[0, -80], dur=0.05),
    A("ptG", "slide-down", delay=0.12, dur=0.5),
    # la pierna de arriba baja y se cruza; la espinilla llega un poco después y se queda balanceándose
    A("ptG", "move", trigger="cruzar", to=[0, 80], dur=0.6, sfx="whoosh"),
    A("espG", "move", trigger="cruzar", to=[0, 80], dur=0.75),
    A("espG", "sway", trigger="piernas", origin="top", amount=0.12),
    A("ptG", "sway", trigger="piernas", origin="left", amount=0.04),
    A("pbG", "sway", delay=0.7, origin="left", amount=0.02),
    A("asientoG", "punch", trigger="sentarte", amount=0.12, sfx="boing"),
    # aplastar: el peso aprieta, el nervio y el vaso se estrechan
    A("pb_nervio_apl", "hide"),
    A("pb_vaso_apl", "hide"),
    A("fpeso", "pop", trigger="aplastas", origin="bottom", sfx="pop"),
    A("fpeso", "float", trigger="aplastas", amount=0.35),
    A("ptG", "move", trigger="aplastas", to=[0, 10], dur=0.3),
    A("espG", "move", trigger="aplastas", to=[0, 10], dur=0.35),
    A("gol", "pop", trigger="aplastas", sfx="chasquido"),
    A("gol", "pulse", trigger="aplastas", amount=0.8),
    A("pb_nervio", "hide", trigger="un nervio"),
    A("pb_nervio_apl", "fade", trigger="un nervio", dur=0.18),
    A("pb_vaso", "hide", trigger="un nervio"),
    A("pb_vaso_apl", "fade", trigger="un nervio", dur=0.18),
    A("tnervio", "pop", trigger="nervio", sfx="pop"),
    A("tnervio", "float", trigger="nervio", amount=0.15),
    A("tcable", "slide-up", trigger="cable", dur=0.4),
    A("cable", "draw", trigger="cable", dur=0.7, sfx="rotulador"),
    # mensajes: viajan hacia el cerebro y se paran en el apretón
    A("m0", "pop", trigger="lleva", sfx="pop"),
    A("m1", "pop", trigger="mensajes"),
    A("m2", "pop", trigger="al cerebro"),
    A("m0", "move", trigger="lleva", to=[stops[0] - xs[0], 0], dur=0.9),
    A("m1", "move", trigger="mensajes", to=[stops[1] - xs[1], 0], dur=0.9),
    A("m2", "move", trigger="al cerebro", to=[stops[2] - xs[2], 0], dur=0.9),
    A("m0", "pulse", trigger="mensajes", amount=1.2),
    A("m1", "pulse", trigger="al cerebro", amount=1.0),
    A("m2", "pulse", trigger="cerebro", amount=1.3),
    A("cere", "pop", trigger="cerebro", sfx="pop"),
    A("cere", "float", trigger="cerebro", amount=0.25),
    A("cduda", "pop", trigger="cerebro", origin="bottom-left"),
    A("cduda", "wiggle", trigger="cerebro", amount=0.4),
]

# ---------------------------------------------------------------- 2. vasos apretados
oi = (110, 200, 290, 375)
oi_stop = (285, 330, 375, 420)
s2 = [
    A("tejG", "slide-up", delay=0.0, dur=0.5, sfx="whoosh"),
    A("rodilla", "slide-down", delay=0.05, dur=0.5),
    A("medG", "pop", delay=0.35),
    A("vaso_apl", "hide"),
    A("nerv_apl", "hide"),
    A("dif0", "flow", amount=0.8),
    A("dif1", "flow", amount=0.7),
    A("dif2", "flow", amount=0.9),
    A("rodilla", "move", trigger="aprietas", to=[0, 92], dur=0.45, sfx="boing"),
    A("rodilla", "sway", trigger="vasos", origin="bottom", amount=0.06),
    A("presion", "pop", trigger="aprietas"),
    A("presion", "pulse", trigger="aprietas", amount=0.7),
    A("vaso", "hide", trigger="los vasos"),
    A("vaso_apl", "fade", trigger="los vasos", dur=0.18),
    A("nerv", "hide", trigger="los vasos"),
    A("nerv_apl", "fade", trigger="los vasos", dur=0.2),
    A("tvaso", "pop", trigger="vasos", sfx="pop"),
    A("tnerv", "pop", trigger="nervio", sfx="pop"),
]
for i, (x, st) in enumerate(zip(oi, oi_stop)):
    s2.append(A(f"oi{i}", "drift", amount=0.25, delay=0.1 * i, phase=0.23 * i))
    s2.append(A(f"oi{i}", "move", trigger="aprietas" if i % 2 == 0 else "los vasos", to=[st - x, 0], dur=1.0 + 0.15 * i))
for i in range(3):
    s2.append(A(f"od{i}", "move", delay=0.0, to=[180, 0], dur=2.6 + 0.3 * i))
s2 += [
    A("od0", "hide", trigger="llega"),
    A("od1", "hide", trigger="menos"),
    A("od2", "hide", trigger="oxígeno"),
    A("dif0", "hide", trigger="llega"),
    A("dif1", "hide", trigger="menos"),
    A("dif2", "hide", trigger="oxígeno"),
    A("aguja", "move", trigger="menos", rotate=-125, origin="center", dur=0.9, sfx="whoosh"),
    A("aguja", "wiggle", trigger="oxígeno", origin="center", amount=0.25),
    A("medG", "punch", trigger="oxígeno", amount=0.25),
]

# ---------------------------------------------------------------- 3. el nervio se calla
s3 = [
    A("pcG", "slide-up", delay=0.0, dur=0.5, sfx="whoosh"),
    A("pc_nervio", "hide"),
    A("pc_vaso", "hide"),
    A("cere", "pop", delay=0.15),
    A("cere", "float", delay=0.3, amount=0.22),
    A("cable", "flow", amount=0.6),
    A("bon", "pulse", amount=0.5),
    A("boff", "hide"),
    A("pcG", "sway", delay=0.6, origin="left", amount=0.02),
    A("sob0", "pop", trigger="nervio", sfx="papel"),
    A("sob1", "pop", trigger="se"),
    A("sob2", "pop", trigger="calla"),
    A("bon", "hide", trigger="calla"),
    A("boff", "fade", trigger="calla", dur=0.2, sfx="chasquido"),
    A("cable", "hide", trigger="y casi"),
    A("sob0", "move", trigger="casi", to=[-22, -170], dur=0.9),
    A("sob1", "move", trigger="no", to=[-18, -140], dur=0.9),
    A("sob2", "move", trigger="sientes", to=[-14, -110], dur=0.9),
    A("x", "pop", trigger="sientes", sfx="pop"),
    A("x", "pulse", trigger="sientes", amount=0.6),
    A("gris", "fade", trigger="pierna", dur=0.5),
    A("tpar", "pop", trigger="Es", sfx="ding"),
    A("tpar", "float", trigger="Es", amount=0.15),
    A("tsub1", "slide-up", trigger="la parestesia", dur=0.4),
    A("tsub2", "slide-up", trigger="parestesia", dur=0.4),
]

# ---------------------------------------------------------------- 4. pinchazos
on_trig = {3: "fibras", 7: "del", 1: "nervio", 5: "despiertan", 8: "a destiempo", 0: "destiempo"}
s4 = [
    A("vasoG", "slide-left", delay=0.0, dur=0.5, sfx="whoosh"),
    A("hzG", "slide-up", delay=0.1, dur=0.55),
    A("vabierto", "hide"),
    A("vstrecho", "hide", trigger="moverte"),
    A("vabierto", "fade", trigger="moverte", dur=0.25),
    A("tsangre", "pop", trigger="sangre", sfx="pop"),
]
for i in range(5):
    s4.append(A(f"gl{i}", "drift", delay=0.15 * i, amount=0.15, phase=0.2 * i))
    s4.append(A(f"gl{i}", "move", trigger="sangre" if i < 3 else "vuelve", to=[620 - 40 * i, 0], dur=1.8 + 0.25 * i))
for i in range(10):
    s4.append(A(f"hz_on{i}", "hide"))
order_delay = {2: 4.1, 4: 4.35, 6: 4.6, 9: 4.8}
for i in range(10):
    if i in on_trig:
        s4.append(A(f"hz_on{i}", "fade", trigger=on_trig[i], dur=0.25))
        s4.append(A(f"hz_on{i}", "pulse", trigger=on_trig[i], amount=0.12))
    else:
        s4.append(A(f"hz_on{i}", "fade", delay=order_delay[i], dur=0.25))
        s4.append(A(f"hz_on{i}", "pulse", delay=order_delay[i], amount=0.12))
s4 += [A("tfib", "pop", trigger="fibras", sfx="pop"), A("tfib", "float", trigger="despiertan", amount=0.15)]
ag_trig = ["De ahí", "ahí", "los", "pinchazos", "los", "pinchazos"]
for i in range(6):
    t = ag_trig[i]
    kw = {"trigger": t} if t else {"delay": 4.9 + 0.15 * (i - 4)}
    s4.append(A(f"ag{i}", "slide-down", dur=0.3, **kw, **({"sfx": "chasquido"} if i == 0 else {})))
    s4.append(A(f"ag{i}", "wiggle", amount=0.35, **kw))
    s4.append(A(f"cz{i}", "pop", **kw))
    s4.append(A(f"cz{i}", "pulse", amount=1.3, **kw))
s4 += [
    A("zzt", "pop", trigger="pinchazos", sfx="boing"),
    A("zzt", "punch", trigger="pinchazos", amount=0.5),
    A("hzG", "shake", trigger="pinchazos", amount=0.35),
]

# ---------------------------------------------------------------- 5. peroneo
s5 = [
    A("rodG", "slide-up", delay=0.0, dur=0.5, sfx="whoosh"),
    A("rodG", "sway", delay=0.6, origin="bottom", amount=0.03),
    A("otra", "slide-right", trigger="cruzas", dur=0.5, sfx="whoosh"),
    A("otra", "move", trigger="rodilla", to=[34, 0], dur=0.4, sfx="boing"),
    A("otra", "sway", trigger="rodilla", origin="left", amount=0.06),
    A("gol", "pop", trigger="sufre", sfx="chasquido"),
    A("gol", "pulse", trigger="sufre", amount=0.8),
    A("lupa", "pop", trigger="sufre", sfx="pop"),
    A("lupa", "float", trigger="el nervio", amount=0.2),
    A("rod_nervio", "draw", trigger="nervio", dur=0.6, sfx="rotulador"),
    A("tper", "pop", trigger="peroneo", sfx="pop"),
    A("onda", "pop", trigger="pasa"),
    A("onda", "ripple", trigger="pasa", phase=0),
    A("rod_nervio", "flow", trigger="justo", amount=0.4),
    A("tlado", "slide-up", trigger="lado", dur=0.4),
]

closing = [
    {"chapter": 5, "headline": "Dudas → *truco*", "narration": "Tú traes las dudas y nosotros te damos el truco.",
     "elements": [{"type": "trick", "trigger": "Tú", "reveal_trigger": "nosotros"}]},
    {"chapter": 5, "number": "TÚ", "headline": "*Confiesa*",
     "narration": "Síguenos y las resolvemos. ¿Dónde se te duerme más a ti?",
     "elements": [{"type": "follow", "trigger": "Síguenos"},
                  {"type": "ask", "text": "¿Dónde se te *duerme* más a ti?", "trigger": "¿Dónde"}]},
]


def ill(svg, layout, caption, anims, height=None):
    d = {"svg_file": svg, "layout": layout}
    if height:
        d["height"] = height
    d["caption"] = caption
    d["anims"] = anims
    return d


guion = {
    "topic": "¿Por qué se te duerme la pierna? Nervio aplastado, menos oxígeno, parestesia, fibras que despiertan a destiempo y el nervio peroneo",
    "categoria": "cuerpo",
    "title": "¿Por qué se te duerme la pierna y luego te hace cosquillas?",
    "source": "Fuentes: Science Norway · NBC News · KidsHealth · Psicología y Mente · Cureus",
    "chapters": ["?", "1", "2", "3", "+", "TÚ"],
    "outro_cta": "Todo tiene un truco",
    "cover": {"text": "Por qué se *duerme* la pierna", "scene": 0},
    "publish": {
        "at": "2026-10-27T14:00:00+01:00",
        "caption": "¿Por qué se te duerme la pierna? Aplastas un nervio y los vasos que le dan oxígeno, y deja de mandar mensajes. Al moverte, sus fibras se despiertan a destiempo: pinchazos (Science Norway, KidsHealth). Cruzar por la rodilla castiga al nervio peroneo. ¿Dónde se te duerme más a ti?",
        "description": "¿Por qué se te duerme la pierna? Al cruzar las piernas o sentarte encima aprietas un nervio y los vasos que lo alimentan, así que le llega menos oxígeno y deja de mandar mensajes al cerebro: es la parestesia. Al moverte, la sangre vuelve y las fibras del nervio se despiertan a destiempo, y eso son los pinchazos. Al cruzar por la rodilla, el más castigado es el nervio peroneo, que pasa por el lado de la rodilla. Unos segundos no hacen daño; si dura mucho o se repite, consulta al médico. Fuentes: Science Norway, NBC News, KidsHealth, Psicología y Mente, Cureus. ¿Dónde se te duerme más a ti?",
        "hashtags": ["cuerpohumano", "nervios", "salud", "curiosidades", "ciencia"],
    },
    "scenes": [
        {"chapter": 0, "headline": "¿Pierna de *corcho*?",
         "narration": "¿Te levantas del sofá y tu pierna parece de corcho, llena de hormiguitas?",
         "illustration": ill("gancho_full.svg", "full", "Fig. 1 · La pierna dormida", s0)},
        {"chapter": 1, "number": "1", "headline": "Nervio *aplastado*",
         "narration": "Al cruzar las piernas o sentarte encima, aplastas un nervio, el cable que lleva mensajes al cerebro.",
         "illustration": ill("cruzar_free.svg", "free", "Fig. 2 · Piernas cruzadas", s1, 880)},
        {"chapter": 1, "number": "1", "headline": "Menos *oxígeno*",
         "narration": "Y aprietas los vasos: al nervio le llega menos oxígeno.",
         "illustration": ill("oxigeno_free.svg", "free", "Fig. 3 · Vasos apretados", s2, 860)},
        {"chapter": 2, "number": "2", "headline": "Señal *apagada*",
         "narration": "El nervio se calla y casi no sientes la pierna. Es la parestesia.",
         "illustration": ill("calla_free.svg", "free", "Fig. 4 · Parestesia", s3, 860)},
        {"chapter": 2, "number": "2", "headline": "Despiertan *a destiempo*",
         "narration": "Al moverte, la sangre vuelve y las fibras del nervio despiertan a destiempo. De ahí los pinchazos.",
         "illustration": ill("pinchazos_full.svg", "full", "Fig. 5 · Los pinchazos", s4)},
        {"chapter": 3, "number": "3", "headline": "El nervio *peroneo*",
         "narration": "Si la cruzas por la rodilla, sufre el nervio peroneo, que pasa justo por el lado.",
         "illustration": ill("peroneo_free.svg", "free", "Fig. 6 · El nervio peroneo", s5, 900)},
        {"chapter": 4, "number": "+", "headline": "Segundos, *sin daño*",
         "narration": "Unos segundos de hormigueo no hacen daño. Si dura mucho o se repite sin motivo, consulta al médico.",
         "mascot": {"trigger": "repite", "pose": "point", "note": "¡Si dura, al médico!", "side": "right"},
         "elements": [{"type": "tag", "text": "UNOS SEGUNDOS", "tone": "ink", "trigger": "segundos", "sfx": "pop"},
                      {"type": "stamp", "text": "SIN DAÑO", "tone": "accent", "trigger": "daño", "sfx": "sello"},
                      {"type": "tag", "text": "SI DURA O SE REPITE", "tone": "hot", "trigger": "dura", "sfx": "pop"},
                      {"type": "stamp", "text": "AL MÉDICO", "tone": "hot", "trigger": "médico", "sfx": "sello"}]},
    ] + closing,
}
OUT.write_text(json.dumps(guion, ensure_ascii=False, indent=2) + "\n")
print("ok", OUT)

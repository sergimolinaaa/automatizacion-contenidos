"""Genera content/lote9-07-tostada-mantequilla/guion.json (anims con método rossark). Uso: python3 libreria/archivo/tostada-mantequilla/guion.py"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "content" / "lote9-07-tostada-mantequilla" / "guion.json"


def H(t, e, tr=None, **k):
    d = dict(target=t, effect=e)
    if tr:
        d["trigger"] = tr
    d.update(k)
    return d


def cuenta(prefijo, n, triggers, sfx_final="ding"):
    ids = [f"{prefijo}_{i}" for i in range(n - 1)] + [prefijo]
    out = []
    for i, (cid, tr) in enumerate(zip(ids, triggers)):
        k = dict(dur=0.12)
        if i == n - 1:
            k["sfx"] = sfx_final
        out.append(H(cid, "fade", tr, **k))
        if i > 0:
            out.append(H(ids[i - 1], "hide", tr))
    return out


def persona_viva(pid, phase=0.0, blink_delay=0.6, cuerpo=True):
    """Respira y oscila desde los pies; la cabeza oscila sobre el cuello con retraso (llega después del cuerpo)."""
    out = [H(f"{pid}_ojos", "blink", delay=blink_delay),
           H(f"{pid}_cabeza", "sway", origin="bottom", amount=0.25, delay=0.35 + phase)]
    if cuerpo:
        out += [H(pid, "breathe", origin="bottom", amount=0.6, phase=phase),
                H(pid, "sway", origin="bottom", amount=0.15, delay=0.1 + phase)]
    return out


# ---------------------------------------------------------------- 0. gancho
s0 = [H("anaE", "hide"),
      H("anaG", "breathe", origin="bottom", amount=0.5, phase=0.2),
      H("taza", "slide-right", delay=0.0, dur=0.5, sfx="whoosh"),
      H("taza_vapor", "float", amount=0.5, delay=0.3),
      H("tostada", "slide-down", delay=0.05, dur=0.45),
      # se inclina, roza el plato con el codo y vuelve
      H("anaG", "move", "Se", rotate=4, origin="bottom", dur=0.35),
      H("platoG", "move", "te", to=[45, 0], dur=0.4, sfx="papel"),
      H("anaG", "move", "cae", rotate=-4, origin="bottom", dur=0.6),
      # la tostada salta y cae girando (trayectoria fuera, giro dentro)
      H("tostada", "move", "cae", to=[70, -70], dur=0.35, sfx="whoosh"),
      H("tostada_r", "move", "cae", rotate=50, origin="center", dur=0.4),
      H("tostada", "move", "tostada", to=[150, 275], dur=0.55),
      H("tostada_r", "move", "tostada", rotate=130, origin="center", dur=0.55),
      H("lineas", "fade", "tostada", dur=0.15), H("lineas", "hide", "cómo"),
      H("plaf", "pop", "cómo", sfx="boing"), H("plaf", "wiggle", "cómo", amount=0.4),
      H("mancha", "pop", "cómo"),
      H("tostada", "punch", "cómo", amount=0.3),
      H("ana", "hide", "no"), H("anaE", "fade", "no", dur=0.15),
      H("tabajo", "pop", "lado", sfx="pop"), H("tabajo", "punch", "mantequilla", amount=0.4),
      H("tabajo", "float", "mantequilla", amount=0.25)]
for i, c in enumerate(("ana", "anaE")):
    s0 += persona_viva(c, phase=0.1 * i, blink_delay=0.7, cuerpo=False)
    s0 += [H(f"{c}_cabeza", "move", "cae por", rotate=-6, origin="bottom", dur=0.5)]

# ---------------------------------------------------------------- 1. no es mala suerte
s1 = [H("espejo", "slide-down", delay=0.0, dur=0.5, sfx="whoosh"),
      H("espejo", "sway", origin="top", amount=0.12, delay=0.5),
      H("gato", "slide-right", delay=0.1, dur=0.55),
      H("gato_cola", "sway", origin="bottom-right", amount=0.5, delay=0.4),
      H("gato_ojos", "blink", delay=0.9),
      H("tsuerte", "pop", "mala", sfx="pop"),
      H("aspa", "pop", "suerte", sfx="sello"), H("aspa", "punch", "suerte", amount=0.4),
      H("rm", "slide-left", "físico", dur=0.55, sfx="whoosh"),
      H("piz", "slide-down", "físico", dur=0.5),
      H("dibtiza", "fade", "Robert", dur=0.4),
      H("tnombre", "pop", "Robert", sfx="pop"),
      H("rm_brazo_izq", "move", "Matthews", rotate=10, origin="top-right", dur=0.5),
      H("revista", "slide-up", "calculó", dur=0.5, sfx="papel"), H("revista", "float", "calculó", amount=0.15),
      H("t30", "pop", "treinta", sfx="ding"), H("t30", "punch", "años", amount=0.35),
      H("rm_cabeza", "move", "hace", rotate=-5, origin="bottom", dur=0.5)]
s1 += persona_viva("rm", phase=0.2, blink_delay=1.0)

# ---------------------------------------------------------------- 2. empieza a girar
s2 = [H("mesa", "slide-right", delay=0.0, dur=0.5, sfx="whoosh"),
      H("tost", "slide-down", delay=0.15, dur=0.45, sfx="pop"),
      H("tost", "move", "resbalar", to=[190, 0], dur=0.9),
      H("tost_r", "move", "borde", rotate=8, origin="center", dur=0.5),
      H("tborde", "pop", "borde", sfx="pop"),
      H("peso", "draw", "mesa", dur=0.4, sfx="rotulador"),
      H("tpeso", "pop", "mesa"),
      H("fant0", "pop", "tostada", sfx="pop"),
      H("fant1", "pop", "empieza"),
      H("fant2", "pop", "girar"),
      H("giro", "draw", "empieza", dur=0.6, sfx="whoosh"),
      H("tgira", "pop", "girar", sfx="ding"), H("tgira", "float", "girar", amount=0.3),
      H("tost_r", "wiggle", "empieza", origin="center", amount=0.25)]

# ---------------------------------------------------------------- 3. solo media vuelta
s3 = [H("mesa", "slide-right", delay=0.0, dur=0.5, sfx="whoosh"),
      H("f0", "slide-down", delay=0.1, dur=0.45),
      H("regla", "grow", "mesa", origin="bottom", dur=0.6, sfx="pop"),
      H("tnormal", "pop", "normal", sfx="pop"),
      H("regla", "punch", "baja", amount=0.3),
      H("f1", "pop", "solo", sfx="pop"),
      H("f2", "pop", "tiempo", sfx="pop"),
      H("f3", "pop", "dar", sfx="pop"),
      H("arco", "draw", "media", dur=0.5, sfx="rotulador"),
      H("f4", "pop", "media", sfx="boing"),
      H("s180", "pop", "vuelta", sfx="sello"), H("s180", "punch", "vuelta", amount=0.4),
      H("mancha", "pop", "vuelta es", sfx="pop"),
      H("f4", "punch", "vuelta es", amount=0.35),
      H("tabajo", "pop", "mantequilla", sfx="pop"), H("tabajo", "punch", "abajo", amount=0.35),
      H("arco", "flow", "abajo", amount=0.6)]

# ---------------------------------------------------------------- 4. mesa de tres metros
s4 = [H("escalera", "slide-up", delay=0.0, dur=0.5, sfx="whoosh"),
      H("senor", "slide-up", delay=0.15, dur=0.55),
      H("mesaG", "grow", "cayera", origin="bottom", dur=0.9, sfx="whoosh"),
      H("t0", "punch", "bueno", amount=0.35),
      H("v0", "pop", "tendría", sfx="pop"),
      H("giro", "draw", "tendría", dur=0.9, sfx="whoosh"),
      H("v1", "pop", "medir", sfx="pop"),
      H("altura", "draw", "medir", dur=0.5, sfx="rotulador"), H("altura2", "draw", "medir", dur=0.5),
      H("v2", "pop", "unos", sfx="pop"),
      H("t3m", "pop", "unos", sfx="ding"),
      H("v3", "pop", "tres", sfx="boing"),
      H("ok", "pop", "metros", sfx="ding"), H("ok", "pulse", "metros", amount=0.6),
      H("senor_brazo_der", "wiggle", "medir", origin="bottom-left", amount=0.6),
      H("senor_cabeza", "move", "tres", rotate=6, origin="bottom", dur=0.4)]
s4 += persona_viva("senor", phase=0.3, blink_delay=0.8)

# ---------------------------------------------------------------- 5. los escolares
s5 = [H("nino", "slide-right", delay=0.0, dur=0.55, sfx="whoosh"),
      H("mesaN", "slide-right", delay=0.05, dur=0.5),
      H("tn", "slide-down", delay=0.2, dur=0.45),
      H("ninos", "pop", "mil", sfx="pop"), H("ninos", "bob", "escolares", amount=0.25),
      H("nino_brazo_der", "move", "probaron", rotate=-12, origin="top-left", dur=0.4),
      H("tn", "move", "probaron", to=[10, 160], dur=0.55, sfx="whoosh"),
      H("tn_r", "move", "probaron", rotate=180, origin="center", dur=0.55),
      H("plafn", "pop", "cayó", sfx="boing"), H("plafn", "wiggle", "cayó", amount=0.35),
      H("c0", "pop", "casi", sfx="pop"),
      H("c1", "pop", "dos", sfx="pop"),
      H("c2", "pop", "cada", sfx="pop"),
      H("t23", "pop", "tres", sfx="ding"), H("t23", "punch", "veces", amount=0.35),
      H("nino_cabeza", "move", "casi", rotate=-6, origin="bottom", dur=0.5)]
s5 += cuenta("cmil", 4, ["Más", "de", "mil", "escolares"])
s5 += persona_viva("nino", phase=0.15, blink_delay=0.9)


def ill(svg, layout, cap, an, h=None):
    d = {"svg_file": svg, "layout": layout, "caption": cap, "anims": an}
    if h:
        d["height"] = h
    return d


guion = {
    "topic": "¿Por qué la tostada cae por el lado de la mantequilla? Robert Matthews (European Journal of Physics, 1995): gira al resbalar y desde una mesa normal solo da media vuelta; con una mesa de unos tres metros caería boca arriba; experimento de 2001 con más de mil escolares británicos",
    "categoria": "fisica",
    "title": "¿Por qué la tostada cae por el lado de la mantequilla?",
    "source": "Fuentes: European Journal of Physics · Institute of Physics · Science Focus · The Telegraph · NPR",
    "chapters": ["?", "1", "2", "3", "+", "TÚ"],
    "outro_cta": "Todo tiene un truco",
    "cover": {"text": "Por qué la tostada cae del lado de la *mantequilla*", "scene": 0},
    "publish": {
        "at": "2026-11-01T14:00:00+01:00",
        "caption": "¿Por qué la tostada cae por el lado de la mantequilla? No es mala suerte: desde una mesa normal solo le da tiempo a dar media vuelta (Matthews, European Journal of Physics 1995). Con una mesa de unos tres metros caería boca arriba. Más de mil escolares lo comprobaron: casi dos de cada tres veces, mantequilla abajo. ¿Cuántas tostadas has perdido tú así?",
        "description": "¿Por qué la tostada cae por el lado de la mantequilla? El físico Robert Matthews lo calculó en 1995 (European Journal of Physics): al resbalar del borde, la tostada empieza a girar, y desde una mesa normal solo le da tiempo a dar media vuelta, así que llega al suelo boca abajo. Para que cayera boca arriba, la mesa tendría que medir unos tres metros. En 2001, más de mil escolares británicos lo comprobaron: cayó del lado de la mantequilla casi dos de cada tres veces. La mantequilla apenas pesa: pasaría igual sin ella. Fuentes: European Journal of Physics, Institute of Physics, Science Focus, The Telegraph, NPR. ¿Cuántas tostadas has perdido tú así?",
        "hashtags": ["fisica", "tostada", "leydemurphy", "ciencia", "curiosidades"],
    },
    "scenes": [
        {"chapter": 0, "headline": "Siempre *boca abajo*",
         "narration": "¿Se te cae la tostada y, cómo no, cae por el lado de la mantequilla?",
         "illustration": ill("gancho_full.svg", "full", "Fig. 1 · Otra vez", s0)},
        {"chapter": 1, "number": "1", "headline": "No es *mala suerte*",
         "narration": "No es mala suerte: el físico Robert Matthews lo calculó hace más de treinta años.",
         "illustration": ill("matthews.svg", "panel", "Fig. 2 · Matthews, 1995", s1)},
        {"chapter": 1, "number": "1", "headline": "Empieza a *girar*",
         "narration": "Al resbalar del borde de la mesa, la tostada empieza a girar.",
         "illustration": ill("girar_free.svg", "free", "Fig. 3 · El borde", s2, 860)},
        {"chapter": 2, "number": "2", "headline": "Solo *media vuelta*",
         "narration": "Pero una mesa normal es baja: solo le da tiempo a dar media vuelta. Y media vuelta es mantequilla abajo.",
         "illustration": ill("media_full.svg", "full", "Fig. 4 · La caída", s3)},
        {"chapter": 2, "number": "2", "headline": "Mesa de *tres metros*",
         "narration": "Para que cayera del lado bueno, la mesa tendría que medir unos tres metros.",
         "illustration": ill("tres_free.svg", "free", "Fig. 5 · Vuelta entera", s4, 1000)},
        {"chapter": 3, "number": "3", "headline": "Lo comprobaron los *niños*",
         "narration": "Más de mil escolares británicos lo probaron: cayó del lado de la mantequilla casi dos de cada tres veces.",
         "illustration": ill("ninos.svg", "panel", "Fig. 6 · Experimento escolar", s5),
         "elements": [{"type": "tag", "text": "2001, REINO UNIDO", "tone": "ink", "trigger": "británicos", "sfx": "pop"}]},
        {"chapter": 4, "number": "+", "headline": "Dale un *manotazo*",
         "narration": "La mantequilla apenas pesa: pasaría igual sin ella. Su consejo: si cae, dale un manotazo.",
         "mascot": {"trigger": "si cae", "pose": "point", "note": "¡Dale un manotazo!", "side": "right"},
         "elements": [{"type": "tag", "text": "LA MANTEQUILLA APENAS PESA", "tone": "ink", "trigger": "apenas", "sfx": "pop"},
                      {"type": "stamp", "text": "IGUAL SIN ELLA", "tone": "hot", "trigger": "igual", "sfx": "sello"}]},
        {"chapter": 5, "headline": "Dudas → *truco*",
         "narration": "Tú traes las dudas y nosotros te damos el truco.",
         "elements": [{"type": "trick", "trigger": "Tú", "reveal_trigger": "nosotros"}]},
        {"chapter": 5, "number": "TÚ", "headline": "*Confiesa*",
         "narration": "Síguenos y las resolvemos. ¿Cuántas tostadas has perdido tú así?",
         "elements": [{"type": "follow", "trigger": "Síguenos"},
                      {"type": "ask", "text": "¿Cuántas *tostadas* has perdido tú así?", "trigger": "¿Cuántas"}]},
    ],
}
OUT.write_text(json.dumps(guion, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("ok", OUT, sum(len(s["narration"].split()) for s in guion["scenes"]), "palabras")

"""Genera content/lote10-02-empate-escano/guion.json (montaje rossark). Ejecuta antes dib.py."""
import json

OUT = "/home/user/automatizacion-contenidos/content/lote10-02-empate-escano/guion.json"


def A(target, effect, **kw):
    d = {"target": target, "effect": effect}
    d.update(kw)
    return d


# ---------------------------------------------------------------- 0. gancho
s0 = [A("mesa", "slide-up", delay=0, dur=0.5, sfx="whoosh")]
for k in range(8):  # las dos pilas crecen a la vez, hoja a hoja, desde la base
    s0 += [A(f"pilaE_s{k}", "slide-down", delay=round(0.12 + 0.08 * k, 2), dur=0.3),
           A(f"pilaC_s{k}", "slide-down", delay=round(0.12 + 0.08 * k, 2), dur=0.3)]
s0 += [
    A("pilaE", "breathe", origin="bottom", phase=0.1, amount=0.5, delay=0.9),
    A("pilaC", "breathe", origin="bottom", phase=0.6, amount=0.5, delay=1.0),
    A("pilaE_chip", "pop", trigger="dos", sfx="pop"),
    A("pilaC_chip", "pop", trigger="partidos"),
    A("marc_0", "pop", trigger="partidos", sfx="pop"),
    A("marc_0", "hide", trigger="empatan"),
    A("marc_1", "fade", trigger="empatan", dur=0.15),
    A("marc_1", "hide", trigger="votos"),
    A("marc", "fade", trigger="votos", dur=0.15, sfx="ding"),
    A("marc", "punch", trigger="votos", amount=0.3),
    A("marc", "float", trigger="Quién", amount=0.2),
    A("hemi", "slide-down", trigger="Quién", dur=0.5, sfx="whoosh"),
    A("duda", "pop", trigger="Quién", sfx="sorpresa", origin="bottom-left"),
    A("duda", "float", trigger="gana", amount=0.4),
    A("esc", "pop", trigger="escaño", sfx="ding"),
    A("esc", "pulse", trigger="escaño", amount=0.8),
    A("onda", "ripple", trigger="escaño"),
]

# ---------------------------------------------------------------- 1. sin posicionarnos
s1 = [
    A("doc", "slide-up", delay=0, dur=0.5, sfx="whoosh"),
    A("doc", "sway", origin="bottom", amount=0.12, delay=0.6),
    A("chisp", "pop", trigger="explicamos"),
    A("chisp", "pulse", trigger="explicamos", amount=0.6),
    A("sello", "pop", trigger="posicionarnos", sfx="sello"),
    A("sello", "punch", trigger="posicionarnos", amount=0.5),
    A("sello", "sway", trigger="simplemente", amount=0.1),
    A("doc", "punch", trigger="simplemente", amount=0.2),
    A("chisp", "punch", trigger="que", amount=0.4),
    A("tley", "pop", trigger="dice", sfx="pop"),
    A("doc", "punch", trigger="ley", amount=0.25),
    A("tley", "punch", trigger="la", amount=0.3),
    A("hemi", "slide-up", trigger="Se", dur=0.5, sfx="whoosh"),
    A("eg0", "pop", trigger="usa"),
    A("eg1", "pop", trigger="el"),
    A("eg2", "pop", trigger="método"),
    A("hemi", "breathe", origin="bottom", amount=0.3, trigger="método"),
    A("tdh", "pop", trigger="D'Hondt", sfx="pop"),
    A("tdh", "punch", trigger="D'Hondt", amount=0.3),
]

# ---------------------------------------------------------------- 2. la tabla D'Hondt
DEST = {"f0": [-115, 424], "f1": [55, 238], "f2": [31, 424]}  # de dib.py (casilla → escaño)
s2 = [
    A("tinv", "pop", delay=0, sfx="pop"),
    A("tab_r0", "slide-right", delay=0.05, dur=0.45, sfx="whoosh"),
    A("tab_r1", "slide-right", delay=0.18, dur=0.45),
    A("tab_h0", "pop", delay=0.3), A("tab_h1", "pop", delay=0.38), A("tab_h2", "pop", delay=0.46),
    A("arco", "slide-up", delay=0.35, dur=0.5),
    A("tab_r0", "float", amount=0.15, delay=0.7),
    A("tab_r1", "float", amount=0.2, delay=0.95),
    A("tab_r0", "punch", trigger="votos", amount=0.2),
    A("tab_r1", "punch", trigger="partido", amount=0.2),
    A("tab_c0_0", "pop", trigger="uno", sfx="pop"), A("tab_c1_0", "pop", trigger="uno"),
    A("tab_c0_1", "pop", trigger="dos", sfx="pop"), A("tab_c1_1", "pop", trigger="dos"),
    A("tab_c0_2", "pop", trigger="tres", sfx="pop"), A("tab_c1_2", "pop", trigger="tres"),
    A("tab_o0_0", "draw", trigger="los cocientes", dur=0.4, sfx="rotulador"),
    A("tab_o1_0", "draw", trigger="cocientes", dur=0.4),
    A("tab_o0_1", "draw", trigger="más", dur=0.4),
    A("tgana", "pop", trigger="ganan", sfx="pop"),
]
for f_, trig in (("f0", "altos"), ("f1", "ganan"), ("f2", "escaño")):
    s2 += [A(f_, "pop", trigger=trig, sfx="whoosh"), A(f_, "move", trigger=trig, to=DEST[f_], dur=0.6)]

# ---------------------------------------------------------------- 3. cocientes iguales: el más votado
s3 = [
    A("cas0", "slide-right", delay=0, dur=0.45, sfx="whoosh"),
    A("cas1", "slide-left", delay=0.12, dur=0.45),
    A("bal0", "slide-up", delay=0.2, dur=0.5),
    A("cas0", "float", amount=0.2, delay=0.6),
    A("cas1", "float", amount=0.25, delay=0.85),
    A("igual", "pop", trigger="coinciden", sfx="pop"),
    A("igual", "pulse", trigger="coinciden", amount=0.6),
    A("cas0", "punch", trigger="coinciden", amount=0.25),
    A("cas1", "punch", trigger="coinciden", amount=0.25),
    A("tart", "pop", trigger="artículo", sfx="pop"),
    A("tart", "punch", trigger="tres", amount=0.3),
    A("bal0", "punch", trigger="escaño", amount=0.12),
    # se inclina en 3 pasos encadenados (crossfade corto: sin saltos)
    A("bal1", "fade", trigger="más", dur=0.12), A("bal0", "hide", trigger="más"),
    A("bal2", "fade", trigger="votado", dur=0.12), A("bal1", "hide", trigger="votado"),
    A("bal3", "fade", trigger="total", dur=0.12), A("bal2", "hide", trigger="total"),
    A("ttot", "pop", trigger="votado", sfx="pop"),
    A("ok", "pop", trigger="total", sfx="ding"),
    A("ok", "pulse", trigger="total", amount=0.4),
]

# ---------------------------------------------------------------- 4. sorteo y luego por turnos
s4 = [
    A("bombo", "slide-up", delay=0, dur=0.5, sfx="whoosh"),
    A("bombo_jaula", "spin", origin="center", amount=0.6, delay=0.2),
    A("bombo_manivela", "spin", origin="bottom-left", amount=0.6, delay=0.2),
    A("filas", "slide-up", delay=0.15, dur=0.5),
    A("marc", "pop", trigger="empatan", sfx="pop"),
    A("marc", "punch", trigger="votos", amount=0.3),
    A("marc", "float", trigger="votos", amount=0.2),
    A("cita", "pop", trigger="Primer", sfx="papel"),
    A("cita", "float", trigger="empate", amount=0.12),
    A("bombo_bola", "move", trigger="sorteo", to=[40, 95], dur=0.6),
    A("tsort", "pop", trigger="sorteo", sfx="ding"),
    A("t0", "pop", trigger="los", sfx="pop"),
    A("t1", "pop", trigger="siguientes", sfx="pop"),
    A("giro", "draw", trigger="siguientes", dur=0.8, sfx="rotulador"),
    A("t2", "pop", trigger="turnos", sfx="pop"),
    A("tturno", "pop", trigger="turnos"),
    A("t0", "float", trigger="siguientes", amount=0.2),
    A("t1", "float", trigger="turnos", amount=0.25),
]

# ---------------------------------------------------------------- 5. Lújar
s5 = [
    A("mapa", "slide-up", delay=0, dur=0.5, sfx="whoosh"),
    A("mapa", "float", amount=0.15, delay=0.6),
    A("mapa_granada", "pop", trigger="Lújar", sfx="pop"),
    A("onda", "ripple", trigger="Lújar"),
    A("pueblo_g", "slide-up", trigger="Lújar", dur=0.5),
    A("tluj", "pop", trigger="Granada", sfx="pop"),
    A("t2011", "pop", trigger="once", sfx="pop"),
    A("t2011", "sway", trigger="once", amount=0.15),
    A("marc_0", "pop", trigger="candidaturas", sfx="pop"),
    A("marc_0", "hide", trigger="ciento"),
    A("marc_1", "fade", trigger="ciento", dur=0.15),
    A("marc_1", "hide", trigger="sesenta"),
    A("marc", "fade", trigger="sesenta", dur=0.15, sfx="ding"),
    A("marc", "punch", trigger="votos", amount=0.3),
    A("tvot", "pop", trigger="votos"),
    A("bombo", "pop", trigger="sorteo", sfx="pop"),
    A("bombo_jaula", "spin", origin="center", amount=0.8, trigger="sorteo"),
    A("talc", "pop", trigger="decidió", sfx="sello"),
    A("baston", "slide-down", trigger="alcaldía", dur=0.5, sfx="ding"),
    A("baston", "sway", origin="bottom", amount=0.15, trigger="alcaldía"),
    A("baston_borla", "sway", origin="top", amount=0.5, trigger="alcaldía"),
    A("dest", "pop", trigger="alcaldía"),
    A("dest", "pulse", trigger="alcaldía", amount=0.6),
]

# ---------------------------------------------------------------- 6. un voto evita el sorteo
s6 = [
    A("urna", "slide-up", delay=0, dur=0.5, sfx="whoosh"),
    A("bombo", "slide-up", delay=0.1, dur=0.5),
    A("bombo_jaula", "move", origin="center", rotate=720, delay=0.15, dur=2.6),  # gira y se frena solo
    A("tstc", "pop", trigger="Constitucional", sfx="sello"),
    A("tstc", "punch", trigger="avaló", amount=0.3),
    A("sobre", "slide-down", trigger="un", dur=0.4),
    A("sobre", "move", trigger="voto", to=[0, 150], dur=0.5),
    A("sobre", "hide", trigger="puede"),
    A("urna", "punch", trigger="puede", amount=0.15),
    A("tun", "pop", trigger="voto", sfx="pop"),
    A("tache", "draw", trigger="evitar", dur=0.4, sfx="rotulador"),
    A("bombo", "punch", trigger="sorteo", amount=0.15),
]

scenes = [
    {"chapter": 0, "headline": "¿*Empate* a votos?",
     "narration": "¿Y si dos partidos empatan a votos? ¿Quién gana el escaño?",
     "illustration": {"svg_file": "gancho_full.svg", "layout": "full", "caption": "Fig. 1 · Empate a votos", "anims": s0}},
    {"chapter": 1, "number": "1", "headline": "Sin *posicionarnos*",
     "narration": "Te lo explicamos sin posicionarnos, simplemente con lo que dice la ley. Se usa el método D'Hondt.",
     "illustration": {"svg_file": "ley.svg", "layout": "panel", "caption": "Fig. 2 · LOREG", "anims": s1}},
    {"chapter": 1, "number": "1", "headline": "Ganan los *cocientes*",
     "narration": "Divides los votos de cada partido entre uno, dos, tres, y los cocientes más altos ganan escaño.",
     "illustration": {"svg_file": "tabla_free.svg", "layout": "free", "height": 820, "caption": "Fig. 3 · Ejemplo inventado", "anims": s2}},
    {"chapter": 2, "number": "2", "headline": "Gana *el más votado*",
     "narration": "Si dos cocientes coinciden, el artículo ciento sesenta y tres da el escaño al más votado en total.",
     "illustration": {"svg_file": "balanza.svg", "layout": "panel", "caption": "Fig. 4 · LOREG, art. 163", "anims": s3}},
    {"chapter": 2, "number": "2", "headline": "Y si no: *sorteo*",
     "narration": "¿Y si empatan también en votos? Primer empate, por sorteo; los siguientes, por turnos.",
     "illustration": {"svg_file": "sorteo_full.svg", "layout": "full", "caption": "Fig. 5 · Texto literal de la ley", "anims": s4}},
    {"chapter": 3, "number": "3", "headline": "Pasó en *Lújar*",
     "narration": "Pasó en Lújar, Granada, en dos mil once: dos candidaturas empataron a ciento sesenta y un votos, y un sorteo decidió la alcaldía.",
     "illustration": {"svg_file": "lujar.svg", "layout": "panel", "caption": "Fig. 6 · Lújar, 2011", "anims": s5}},
    {"chapter": 4, "number": "+", "headline": "Un voto *cuenta*",
     "narration": "El Constitucional lo avaló: un solo voto puede evitar el sorteo.",
     "illustration": {"svg_file": "unvoto_free.svg", "layout": "free", "height": 720, "caption": "Fig. 7 · STC 125/2011", "anims": s6},
     "mascot": {"trigger": "avaló", "pose": "cheer", "note": "¡Un voto evita el sorteo!", "side": "right"}},
    {"chapter": 5, "headline": "Dudas → *truco*", "narration": "Tú traes las dudas y nosotros te damos el truco.",
     "elements": [{"type": "trick", "trigger": "Tú", "reveal_trigger": "nosotros"}]},
    {"chapter": 5, "number": "TÚ", "headline": "*Confiesa*", "narration": "Síguenos y las resolvemos. ¿Sabías que se decide así?",
     "elements": [{"type": "follow", "trigger": "Síguenos"},
                  {"type": "ask", "text": "¿Sabías que se *decide* así?", "trigger": "Sabías"}]},
]

doc = {
    "topic": "Empate a votos: ¿quién gana el escaño? Con D'Hondt, si dos cocientes coinciden el escaño va a la candidatura con más votos en total; si también empatan en votos, el primer empate se resuelve por sorteo y los siguientes de forma alternativa (LOREG art. 163.1 d). Caso de Lújar (Granada, 2011) y STC 125/2011",
    "categoria": "politica",
    "title": "Empate a votos: ¿quién se lleva el escaño? Lo dice la ley",
    "source": "Fuentes: BOE, LOREG art. 163 · Junta Electoral Central · STC 125/2011 · LegalToday · Público",
    "chapters": ["?", "1", "2", "3", "+", "TÚ"],
    "outro_cta": "Todo tiene un truco",
    "cover": {"text": "Empate a votos: quién gana el *escaño*", "scene": 0},
    "publish": {
        "at": "2026-11-03T14:00:00+01:00",
        "caption": "Empate a votos: ¿quién gana el escaño? Sin posicionarnos: la ley (art. 163 LOREG) se lo da al que tenga más votos en total. Si también empatan, el primer empate va a sorteo y los siguientes por turnos. En Lújar, en 2011, un sorteo decidió la alcaldía (BOE, Tribunal Constitucional). ¿Sabías que un empate se decide así?",
        "description": "Empate a votos: ¿quién se lleva el escaño? Te lo explicamos sin posicionarnos, con el texto de la ley. Con el método D'Hondt, si dos cocientes coinciden, el artículo 163 de la Ley Orgánica del Régimen Electoral General da el escaño a la candidatura con más votos en total; y si también empatan en votos, «el primer empate se resolverá por sorteo y los sucesivos de forma alternativa». Pasó en Lújar (Granada) en 2011: dos candidaturas empataron a 161 votos, un sorteo decidió la alcaldía y el Tribunal Constitucional lo avaló (STC 125/2011). Fuentes: BOE, Junta Electoral Central, Tribunal Constitucional, LegalToday. ¿Sabías que un empate se decide así?",
        "hashtags": ["elecciones", "leyelectoral", "dhondt", "votar", "politica"],
    },
    "scenes": scenes,
}
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(doc, fh, ensure_ascii=False, indent=2)
print("ok", OUT, sum(len(s["narration"].split()) for s in scenes), "palabras")

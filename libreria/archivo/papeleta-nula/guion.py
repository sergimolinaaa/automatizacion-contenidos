import json, shutil, re
DST = "/home/user/automatizacion-contenidos/content/lote6-08-papeleta-nula"
import os; os.makedirs(DST, exist_ok=True)

def A(target, effect, trigger=None, **kw):
    d = {"target": target, "effect": effect}
    if trigger: d["trigger"] = trigger
    d.update(kw); return d
H = lambda *ids: [A(i, "hide") for i in ids]

scenes = [
 {"chapter": 0, "headline": "Un tachón = *nulo*",
  "narration": "Un tachón y tu voto del 29-N no vale nada.",
  "illustration": {"svg_file": "gancho_full.svg", "layout": "full", "caption": "Fig. 1 · Papeleta del Congreso",
   "anims": H("nums", "candado", "torden", "tpartido") + [
     A("boli", "slide-left", "Un", dur=0.5, sfx="whoosh"),
     A("tachon", "draw", "tachón", dur=0.6, sfx="papel"),
     A("tunvoto", "pop", "tachón", sfx="pop"),
     A("boli", "move", "voto", to=[40, 60], dur=0.4),
     A("t29", "pop", "29-N", sfx="ding"),
     A("tcong", "pop", "29-N"),
     A("nulo", "pop", "vale", sfx="sello"),
     A("papeleta", "shake", "vale", amount=0.4),
     A("tcero", "pop", "nada", sfx="pop"),
     A("nulo", "pulse", amount=0.4)]}},
 {"chapter": 1, "number": "1", "headline": "Lista *cerrada*",
  "narration": "Sin posicionarnos: solo cómo funciona. El Congreso es de lista cerrada: nombres y orden los pone el partido.",
  "elements": [{"type": "tag", "text": "SIN POSICIONARNOS", "tone": "ink", "trigger": "posicionarnos"}],
  "illustration": {"svg_file": "gancho_full.svg", "layout": "full", "caption": "Fig. 2 · Lista cerrada",
   "anims": H("tachon", "nulo", "boli", "t29", "tunvoto", "tcero") + [
     A("tcong", "pop", "Congreso", sfx="pop"),
     A("papeleta", "punch", "lista", amount=0.12, sfx="ding"),
     A("candado", "pop", "cerrada", sfx="sello"),
     A("candado", "pulse", amount=0.4),
     A("papeleta", "punch", "nombres", amount=0.15),
     A("nums", "draw", "orden", dur=0.6),
     A("torden", "pop", "orden", sfx="pop"),
     A("tpartido", "slide-up", "partido", dur=0.5, sfx="whoosh")]}},
 {"chapter": 1, "number": "1", "headline": "Ni tachar ni *escribir*",
  "narration": "Si tachas un nombre, añades otro o escribes algo, es nulo: no cuenta.",
  "illustration": {"svg_file": "papeletas.svg", "caption": "Fig. 3 · LOREG, art. 96.2",
   "anims": [
     A("l1", "pop", "tachas", sfx="pop"), A("m1", "draw", "tachas", dur=0.5),
     A("x1", "pop", "nombre", sfx="pop"),
     A("l2", "pop", "añades", sfx="pop"), A("m2", "draw", "añades", dur=0.6),
     A("x2", "pop", "otro", sfx="pop"),
     A("l3", "pop", "escribes", sfx="pop"), A("m3", "pop", "escribes"),
     A("x3", "pop", "algo", sfx="pop"),
     A("nulo", "pop", "nulo", sfx="sello"),
     A("b2", "shake", "cuenta", amount=0.4)]}},
 {"chapter": 2, "number": "2", "headline": "Dos en un *sobre*",
  "narration": "Dos papeletas de partidos distintos en el mismo sobre: nulo. Pero dos iguales cuentan como un solo voto.",
  "illustration": {"svg_file": "sobres_free.svg", "layout": "free", "height": 900, "caption": "Fig. 4 · LOREG, art. 96.1",
   "anims": H("sv", "sf", "lvacio", "lfolio", "okb", "xf", "lblanco", "lnulo2") + [
     A("sd", "slide-up", "Dos", dur=0.5, sfx="papel"),
     A("ldist", "pop", "distintos", sfx="pop"),
     A("sd", "punch", "sobre", amount=0.15),
     A("xd", "pop", "nulo", sfx="sello"), A("lnulo", "pop", "nulo"),
     A("si", "slide-up", "Pero", dur=0.5, sfx="papel"),
     A("ligual", "pop", "iguales", sfx="pop"),
     A("okv", "pop", "solo", sfx="ding"),
     A("l1voto", "pop", "voto", sfx="pop"),
     A("okv", "pulse", amount=0.4)]}},
 {"chapter": 3, "number": "3", "headline": "Vacío no es *nulo*",
  "narration": "El sobre vacío no es nulo: es voto en blanco. Pero con un folio en blanco dentro, sí es nulo.",
  "illustration": {"svg_file": "sobres_free.svg", "layout": "free", "height": 900, "caption": "Fig. 5 · LOREG, art. 96.5",
   "anims": H("sd", "si", "ldist", "ligual", "xd", "okv", "lnulo", "l1voto") + [
     A("sv", "slide-up", "El", dur=0.5, sfx="whoosh"),
     A("lvacio", "pop", "vacío", sfx="pop"),
     A("sv", "shake", "nulo", amount=0.3),
     A("okb", "pop", "voto", sfx="ding"), A("lblanco", "pop", "voto"),
     A("sf", "slide-up", "Pero", dur=0.5, sfx="papel"),
     A("lfolio", "pop", "folio", sfx="pop"),
     A("sf", "punch", "dentro", amount=0.15),
     A("xf", "pop", "sí", sfx="sello"), A("lnulo2", "pop", "sí")]}},
 {"chapter": 4, "number": "+", "headline": "Y el *Senado*",
  "narration": "¿Y el Senado? Ahí sí se marcan cruces: hasta tres nombres. Más de tres, nulo.",
  "illustration": {"svg_file": "senado_full.svg", "layout": "full", "caption": "Fig. 6 · Papeleta sepia del Senado",
   "anims": [
     A("papeleta", "punch", "Senado", amount=0.15, sfx="whoosh"),
     A("c1", "draw", "marcan", dur=0.35, sfx="pop"),
     A("c2", "draw", "cruces", dur=0.35, sfx="pop"),
     A("c3", "draw", "hasta", dur=0.35, sfx="pop"),
     A("thasta", "pop", "tres", sfx="ding"),
     A("okv", "pop", "nombres", sfx="ding"), A("tok", "pop", "nombres"),
     A("boli", "slide-left", "Más", dur=0.4, sfx="whoosh"),
     A("c4", "draw", "Más", dur=0.35),
     A("okv", "hide", "nulo"), A("tok", "hide", "nulo"),
     A("nulo", "pop", "nulo", sfx="sello"),
     A("papeleta", "shake", "nulo", amount=0.4)]}},
 {"chapter": 5, "headline": "Dudas → *truco*", "narration": "Tú traes las dudas y nosotros te damos el truco.",
  "elements": [{"type": "trick", "trigger": "Tú", "reveal_trigger": "nosotros"}]},
 {"chapter": 5, "number": "TÚ", "headline": "*Confiesa*",
  "narration": "Síguenos y las resolvemos. ¿Tu abuela también plancha las papeletas?",
  "elements": [{"type": "follow", "trigger": "Síguenos"},
               {"type": "ask", "text": "¿Tu abuela también *plancha* las papeletas?", "trigger": "Tu"}]},
]

g = {
 "topic": "Qué anula tu papeleta (y qué no) en las elecciones generales del 29 de noviembre de 2026",
 "categoria": "politica",
 "title": "Un tachón y tu voto no vale 🗳️",
 "source": "Fuentes: LOREG (LO 5/1985), art. 96 (apartados 1, 2, 4 y 5) · Instrucción 1/2012 de la Junta Electoral Central (BOE 19/3/2012) sobre alteraciones en las papeletas · BOE 6/10/2026 (Real Decreto 806/2026) · Ejemplo con partidos ficticios",
 "chapters": ["?", "1", "2", "3", "+", "TÚ"],
 "outro_cta": "Todo tiene un truco",
 "cover": {"text": "Un tachón y *adiós* voto", "scene": 0},
 "publish": {
  "at": "2026-10-16T14:00:00+02:00",
  "caption": "¿Sabías que un simple tachón puede anular tu voto el 29-N? 🗳️ La papeleta del Congreso es de lista cerrada: si tachas un nombre, añades otro o escribes algo, el voto es nulo. Dos papeletas de partidos distintos en el mismo sobre: nulo. Dos iguales: cuentan como un solo voto. El sobre vacío no es nulo, es voto en blanco; pero un folio en blanco dentro sí lo anula. Y en el Senado sí se marcan cruces: hasta tres en tu provincia. Sin posicionarnos: solo explicamos cómo funciona. ¿Lo sabías?",
  "description": "Qué anula tu papeleta en las elecciones generales del 29 de noviembre de 2026 (Real Decreto 806/2026, BOE del 6 de octubre). 1) Al Congreso se vota una lista cerrada y bloqueada: los nombres y su orden los decide cada partido. Por eso es nulo el voto en una papeleta en la que se hayan tachado, añadido o modificado nombres, alterado su orden o hecho cualquier otra alteración (LOREG, art. 96.2). 2) Es nulo el voto en sobre o papeleta distintos del modelo oficial, y el sobre con papeletas de candidaturas distintas; si lleva varias papeletas de la misma candidatura, cuenta como un solo voto válido (art. 96.1). 3) El sobre sin papeleta es voto en blanco, que es válido, no nulo (art. 96.5); en cambio, meter un papel en blanco dentro lo anula, según la Junta Electoral Central. 4) En el Senado sí se marcan los candidatos con una cruz: hasta tres en las circunscripciones provinciales (menos en las islas, Ceuta y Melilla); si se marcan más, el voto es nulo. Partidos del ejemplo: ficticios. Sin posicionarnos: solo explicamos cómo funciona. Fuentes: LOREG, art. 96; Instrucción 1/2012 de la JEC; BOE (Real Decreto 806/2026).",
  "hashtags": ["eltrucoes"]},
 "scenes": scenes,
}
# comprobar triggers
for i, s in enumerate(scenes):
    words = re.findall(r"[\wÁÉÍÓÚÑáéíóúñü\-]+", s["narration"])
    trig = [a.get("trigger") for a in s.get("illustration", {}).get("anims", [])] + [e.get("trigger") for e in s.get("elements", [])] + [s.get("mascot", {}).get("trigger")]
    for t in trig:
        if t and t not in words: print("TRIGGER?", i, t)
n = sum(len(s["narration"].split()) for s in scenes); print("palabras", n)
json.dump(g, open(DST + "/guion.json", "w"), ensure_ascii=False, indent=2)
for f in ("gancho_full.svg", "papeletas.svg", "sobres_free.svg", "senado_full.svg"):
    shutil.copy(f, DST)
print("ok")

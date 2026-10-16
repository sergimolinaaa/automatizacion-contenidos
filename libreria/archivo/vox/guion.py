import json, shutil, os
D = "/home/user/automatizacion-contenidos/content/lote6-07-vox-propone"
os.makedirs(D, exist_ok=True)
for fn in ("gancho_full.svg", "carteles.svg", "competencias_free.svg", "calendario_full.svg"):
    shutil.copy(fn, D)


def A(target, effect, trigger=None, **kw):
    a = {"target": target, "effect": effect}
    if trigger:
        a["trigger"] = trigger
    a.update(kw)
    return a


H = lambda *ids: [A(i, "hide") for i in ids]
G0 = ("tque", "atril", "tcand", "nov", "t29", "prog26", "aun", "aun2")
G1 = ("prog23", "lupa", "tult", "t23j")
TAGS = ("tirpf", "tsuc", "tokupa", "t48", "tileg")

scenes = [
 {"chapter": 0, "headline": "¿Qué propone *Vox*?",
  "narration": "¿Qué propone Vox para el 29-N? Su programa nuevo aún no ha salido.",
  "illustration": {"svg_file": "gancho_full.svg", "layout": "full", "caption": "Fig. 1 · Generales del 29-N", "anims": H(*G1, "tcand", "nov", "t29", "prog26", "aun", "aun2") + [
     A("tque", "wiggle", amount=0.3), A("atril", "punch", "Vox", amount=0.2), A("tcand", "pop", "Vox", sfx="pop"),
     A("nov", "pop", "29-N", sfx="sello"), A("t29", "pop", "29-N"),
     A("prog26", "slide-up", "programa", dur=0.5, sfx="papel"), A("prog26", "bob", amount=0.3),
     A("aun", "pop", "aún", sfx="sello"), A("aun2", "pop", "salido", sfx="sello"), A("nov", "shake", "salido", amount=0.3)]}},
 {"chapter": 1, "number": "1", "headline": "Su *último* programa",
  "narration": "Sin posicionarnos: solo te contamos qué propone. Miramos su último programa, el de 2023.",
  "elements": [{"type": "tag", "text": "SIN POSICIONARNOS", "tone": "ink", "trigger": "posicionarnos"}],
  "illustration": {"svg_file": "gancho_full.svg", "layout": "full", "caption": "Fig. 2 · Programa electoral de 2023", "anims": H(*G0, *G1) + [
     A("prog23", "slide-up", "contamos", dur=0.5, sfx="papel"), A("prog23", "punch", "propone", amount=0.12),
     A("lupa", "pop", "Miramos", sfx="whoosh"), A("tult", "pop", "último", sfx="pop"),
     A("lupa", "move", "programa", to=[-260, -160], dur=0.7),
     A("t23j", "pop", "2023", sfx="ding"), A("lupa", "move", "2023", to=[180, 120], dur=0.6), A("t23j", "pulse", amount=0.3)]}},
 {"chapter": 2, "number": "2", "headline": "*Impuestos*",
  "narration": "Según ese programa: bajar el IRPF, el impuesto de lo que ganas, y quitar el de herencias.",
  "illustration": {"svg_file": "carteles.svg", "caption": "Fig. 3 · Programa de Vox, 23-J 2023", "anims": H("tsegun", "c1", "c2", "c3", *TAGS) + [
     A("nombre", "punch", "programa", amount=0.15), A("tsegun", "pop", "Según", sfx="sello"),
     A("c1", "pop", "bajar", sfx="pop"),
     A("tirpf", "pop", "IRPF", sfx="pop"), A("tirpf", "punch", "ganas", amount=0.15),
     A("c1", "wiggle", "quitar", amount=0.3), A("tsuc", "pop", "herencias", sfx="pop"), A("tsuc", "pulse", amount=0.25)]}},
 {"chapter": 2, "number": "2", "headline": "*Vivienda*",
  "narration": "En vivienda, desalojar en 48 horas una casa ocupada.",
  "illustration": {"svg_file": "carteles.svg", "caption": "Fig. 4 · Programa de Vox, 23-J 2023", "anims": H("c2", "c3", *TAGS) + [
     A("c2", "pop", "vivienda", sfx="pop"), A("c2", "punch", "desalojar", amount=0.2),
     A("t48", "pop", "48", sfx="ding"), A("t48", "pulse", amount=0.3),
     A("tokupa", "pop", "ocupada", sfx="pop"), A("c2", "wiggle", "casa", amount=0.2), A("c1", "breathe", amount=0.2)]}},
 {"chapter": 3, "number": "3", "headline": "*Inmigración*",
  "narration": "En inmigración, expulsar a quien entre ilegalmente.",
  "illustration": {"svg_file": "carteles.svg", "caption": "Fig. 5 · Programa de Vox, 23-J 2023", "anims": H("c3", *TAGS) + [
     A("c3", "pop", "inmigración", sfx="pop"), A("c3", "punch", "expulsar", amount=0.2),
     A("c3", "wiggle", "entre", amount=0.25), A("tileg", "pop", "ilegalmente", sfx="pop"), A("tileg", "pulse", amount=0.3),
     A("c1", "breathe", amount=0.2), A("c2", "breathe", amount=0.2), A("nombre", "punch", "quien", amount=0.12)]}},
 {"chapter": 3, "number": "3", "headline": "Del Estado o *regional*",
  "narration": "Y devolver al Estado sanidad y educación, que hoy llevan las comunidades.",
  "illustration": {"svg_file": "competencias_free.svg", "layout": "free", "height": 840, "caption": "Fig. 6 · Programa de Vox, 23-J 2023", "anims": H("fl", "tdev", "tdefca", "tmas") + [
     A("fl", "draw", "devolver", dur=0.5, sfx="whoosh"), A("tdev", "pop", "Estado", sfx="pop"),
     A("estado", "punch", "Estado", amount=0.15),
     A("fsan", "move", "sanidad", to=[90, -490], dur=0.6, sfx="whoosh"), A("fedu", "move", "educación", to=[30, -490], dur=0.6, sfx="whoosh"),
     A("fl", "hide", "hoy"), A("tdev", "hide", "hoy"), A("ccaa", "punch", "hoy", amount=0.15),
     A("tdefca", "pop", "llevan", sfx="pop"), A("tmas", "pop", "comunidades", sfx="pop"),
     A("fseg", "move", "comunidades", to=[-30, -490], dur=0.6), A("fjus", "move", "comunidades", to=[-90, -490], dur=0.6)]},
  "mascot": {"trigger": "comunidades", "pose": "cheer", "note": "¡Apuntado!", "side": "left"}},
 {"chapter": 4, "number": "+", "headline": "*Sin* firmas",
  "narration": "¿Y para presentarse? Ya tiene escaños, asientos del Congreso: no necesita firmas. Solo su lista, del 21 al 26 de octubre.",
  "illustration": {"svg_file": "calendario_full.svg", "layout": "full", "caption": "Fig. 7 · LOREG, arts. 45 y 169.3", "anims": H("hemi", "tesc", "tdefesc", "firmas", "cruz", "tnofirm", "rango", "tplazo") + [
     A("tpreg", "wiggle", amount=0.25),
     A("hemi", "pop", "escaños", sfx="pop"), A("tesc", "pop", "escaños"), A("tdefesc", "pop", "asientos", sfx="pop"),
     A("firmas", "slide-up", "necesita", dur=0.4, sfx="papel"), A("cruz", "pop", "firmas", sfx="sello"), A("tnofirm", "pop", "firmas"),
     A("rango", "pop", "21", sfx="ding"), A("rango", "pulse", amount=0.3), A("tplazo", "pop", "octubre", sfx="sello")]}},
 {"chapter": 5, "headline": "Dudas → *truco*", "narration": "Tú traes las dudas y nosotros te damos el truco.",
  "elements": [{"type": "trick", "trigger": "Tú", "reveal_trigger": "nosotros"}]},
 {"chapter": 5, "number": "TÚ", "headline": "*Confiesa*",
  "narration": "Síguenos y las resolvemos. ¿Qué propondrías en tu comunidad de vecinos?",
  "elements": [{"type": "follow", "trigger": "Síguenos"},
               {"type": "ask", "text": "¿Qué propondrías en tu *comunidad de vecinos*?", "trigger": "Qué"}]},
]

g = {
    "topic": "Qué propone Vox para las elecciones generales del 29-N de 2026 según su último programa electoral oficial (generales de 2023) y qué necesita para presentarse",
    "categoria": "politica",
    "title": "¿Qué propone Vox para el 29-N? 🗳️",
    "source": "Fuentes: Programa electoral de Vox para las elecciones generales del 23-J de 2023 (voxespana.es, 7/7/2023; recogido por The Objective, Público y El Debate) · Candidatura: declaraciones de Vox del 5/10/2026 (Diario de León) · LOREG (LO 5/1985), arts. 45 y 169.3 · BOE 6/10/2026 (Real Decreto 806/2026)",
    "chapters": ["?", "1", "2", "3", "+", "TÚ"],
    "outro_cta": "Todo tiene un truco",
    "cover": {"text": "¿Qué propone *Vox*?", "scene": 0},
    "publish": {
        "at": "2026-10-12T21:00:00+02:00",
        "caption": "¿Sabes qué propone Vox para el 29-N? 🗳️ Su programa para 2026 aún no se ha publicado, así que miramos el último oficial, el de las generales de 2023. Según ese programa, proponen bajar el IRPF y suprimir el impuesto de sucesiones (herencias), desalojar en 48 horas una vivienda ocupada ilegalmente, expulsar a quien entre en España de forma ilegal y devolver al Estado sanidad, educación, seguridad y justicia. Como ya tiene escaños, no necesita firmas: presenta sus listas del 21 al 26 de octubre. Sin posicionarnos: solo explicamos qué propone. ¿Qué propondrías tú en tu comunidad de vecinos?",
        "description": "Qué propone Vox para las elecciones generales del 29 de noviembre de 2026 (Real Decreto 806/2026, BOE del 6 de octubre). A fecha de este vídeo, Vox no ha publicado su programa para 2026, así que resumimos su último programa electoral oficial, el de las generales del 23 de julio de 2023. Su candidato a la Presidencia del Gobierno, según el partido, es Santiago Abascal. Según ese programa: 1) Impuestos: bajar el IRPF (el impuesto sobre la renta, lo que ganas) y suprimir el Impuesto sobre el Patrimonio, el de Sucesiones y Donaciones (herencias y regalos) y las plusvalías municipales. 2) Vivienda: más medios para desalojar viviendas ocupadas ilegalmente, con una medida cautelar que permita el desalojo en 48 horas. 3) Inmigración: la expulsión inmediata de quienes entren ilegalmente en España. 4) Organización territorial: devolver al Estado las competencias de educación, sanidad, seguridad y justicia, que hoy gestionan en gran parte las comunidades autónomas. 5) Para presentarse: los partidos que obtuvieron representación en las últimas elecciones no necesitan reunir firmas (LOREG, art. 169.3); Vox obtuvo 33 escaños en el Congreso en 2023. Las candidaturas se presentan del 21 al 26 de octubre. Sin posicionarnos: solo explicamos qué propone. Fuentes: programa electoral de Vox para el 23-J de 2023; LOREG, arts. 45 y 169.3; BOE (Real Decreto 806/2026).",
        "hashtags": ["eltrucoes"],
    },
    "scenes": scenes,
}
json.dump(g, open(os.path.join(D, "guion.json"), "w"), ensure_ascii=False, indent=2)
n = sum(len(s["narration"].split()) for s in scenes)
print("palabras", n)
for i, s in enumerate(scenes):
    print(i, len(s["narration"].split()), s["narration"])
# triggers en narración
import re
for i, s in enumerate(scenes):
    words = [w.strip("¿?¡!.,:;«»…").lower() for w in s["narration"].split()]
    trig = [a.get("trigger") for a in s.get("illustration", {}).get("anims", [])] + [e.get("trigger") for e in s.get("elements", [])] + [e.get("reveal_trigger") for e in s.get("elements", [])] + [s.get("mascot", {}).get("trigger")]
    for t in trig:
        if t and t.lower() not in words:
            print("TRIGGER NO ENCONTRADO", i, t)

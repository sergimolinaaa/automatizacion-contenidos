import json, shutil, os
D = "/home/user/automatizacion-contenidos/content/lote6-06-nuevo-partido"
os.makedirs(D, exist_ok=True)
for fn in ("gancho_full.svg", "carteles.svg", "registro_free.svg", "calendario_full.svg"):
    shutil.copy(fn, D)


def A(target, effect, trigger=None, **kw):
    a = {"target": target, "effect": effect}
    if trigger:
        a["trigger"] = trigger
    a.update(kw)
    return a


H = lambda *ids: [A(i, "hide") for i in ids]
REG_A = ("tinterior", "carnet", "tjunio", "sello", "chk", "tdni")
REG_B = ("tesc", "tdefesc", "firmas", "boli", "gente", "uno", "t1000", "t01", "tprov")
G_S1 = ("brillo", "ideas", "tideas", "papeles", "tpapeles")

scenes = [
 {"chapter": 0, "headline": "Nace un *partido*",
  "narration": "Nace un partido a 50 días del 29-N. ¿Qué propone? ¿Llega a tiempo?",
  "illustration": {"svg_file": "gancho_full.svg", "layout": "full", "caption": "Fig. 1 · Presentación del 10 de octubre", "anims": H(*G_S1) + [
     A("tnuevo", "pop", "Nace", sfx="ding"), A("confeti", "pop", "Nace"), A("confeti", "float", amount=0.5),
     A("atril", "punch", "partido", amount=0.2),
     A("hoy", "pop", "50", sfx="pop"), A("flecha", "draw", "días", dur=0.5, sfx="whoosh"), A("t50", "pop", "días", sfx="pop"),
     A("nov", "pop", "29-N", sfx="sello"),
     A("tque", "pop", "Qué", sfx="sorpresa"), A("tque", "wiggle", amount=0.4),
     A("ttiempo", "pop", "Llega", sfx="pop"), A("nov", "shake", "tiempo", amount=0.4)]}},
 {"chapter": 1, "number": "1", "headline": "Ideas y *papeles*",
  "narration": "El truco es… mirar ideas y papeles. Sin posicionarnos: solo te contamos qué propone.",
  "elements": [{"type": "tag", "text": "EL TRUCO ES…", "trigger": "truco"},
               {"type": "tag", "text": "SIN POSICIONARNOS", "tone": "ink", "trigger": "posicionarnos"}],
  "illustration": {"svg_file": "gancho_full.svg", "layout": "full", "caption": "Fig. 2 · Dos cosas que mirar", "anims": H("tque", "ttiempo", "hoy", "nov", "flecha", "t50", "tnuevo", "confeti", "atril", *G_S1) + [
     A("ideas", "pop", "ideas", sfx="pop"), A("tideas", "pop", "ideas"), A("brillo", "pop", "ideas"), A("brillo", "pulse", amount=0.5),
     A("papeles", "slide-up", "papeles", dur=0.5, sfx="papel"), A("tpapeles", "pop", "papeles"),
     A("papeles", "bob", amount=0.4),
     A("papeles", "punch", "posicionarnos", amount=0.2),
     A("ideas", "punch", "propone", amount=0.25)]}},
 {"chapter": 1, "number": "1", "headline": "*Democracia 21*",
  "narration": "Se llama Democracia 21. Según su presentación, es reformista y busca consensos: acuerdos entre distintos.",
  "illustration": {"svg_file": "carteles.svg", "caption": "Fig. 3 · Según su presentación", "anims": H("nombre", "tsegun", "c1", "c2", "c3", "c4") + [
     A("atril", "breathe", amount=0.2),
     A("nombre", "pop", "Democracia", sfx="ding"), A("nombre", "punch", "21", amount=0.15),
     A("tsegun", "pop", "Según", sfx="sello"),
     A("c1", "pop", "reformista", sfx="pop"), A("c1", "wiggle", amount=0.25),
     A("c2", "pop", "consensos", sfx="pop"), A("c2", "punch", "acuerdos", amount=0.2),
     A("c2", "punch", "distintos", amount=0.15)]}},
 {"chapter": 2, "number": "2", "headline": "Lo que *propone*",
  "narration": "Y propone modernizar la democracia y «situar al ciudadano en el centro».",
  "illustration": {"svg_file": "carteles.svg", "caption": "Fig. 4 · Presentación del 10-oct-2026", "anims": H("c3", "c4") + [
     A("atril", "breathe", amount=0.2),
     A("atril", "punch", "propone", amount=0.2),
     A("c3", "pop", "modernizar", sfx="pop"), A("c3", "punch", "democracia", amount=0.2),
     A("c4", "pop", "ciudadano", sfx="pop"), A("c4", "punch", "centro", amount=0.25), A("c4", "pulse", amount=0.4),
     A("nombre", "punch", "situar", amount=0.12)]}},
 {"chapter": 2, "number": "2", "headline": "Ya está *inscrito*",
  "narration": "¿Y los papeles? Ya está inscrito, desde junio, en el Registro de Partidos.",
  "illustration": {"svg_file": "registro_free.svg", "layout": "free", "height": 820, "caption": "Fig. 5 · Ley de Partidos (LO 6/2002)", "anims": H(*REG_B) + H("tinterior", "tjunio", "sello", "chk", "tdni") + [
     A("carnet", "slide-up", "papeles", dur=0.6, sfx="whoosh"), A("carnet", "bob", amount=0.3),
     A("sello", "pop", "inscrito", sfx="sello"),
     A("tjunio", "pop", "junio", sfx="ding"),
     A("tinterior", "pop", "Registro", sfx="pop"),
     A("tdni", "pop", "Partidos", sfx="pop"), A("chk", "pop", "Partidos", sfx="ding"), A("chk", "pulse", amount=0.5)]},
  "mascot": {"trigger": "inscrito", "pose": "cheer", "note": "¡Papeles en regla!", "side": "left"}},
 {"chapter": 3, "number": "3", "headline": "*21-26 oct*",
  "narration": "Para el 29-N, debe presentar candidatura, su lista por provincia, del 21 al 26 de octubre.",
  "illustration": {"svg_file": "calendario_full.svg", "layout": "full", "caption": "Fig. 6 · LOREG, art. 45 · RD 806/2026", "anims": H("nota", "rango", "tplazo", "lista", "tdef", "junta", "fl") + [
     A("hoy", "pulse", amount=0.5),
     A("nota", "pop", "29-N", sfx="pop"),
     A("junta", "pop", "presentar", sfx="pop"),
     A("lista", "slide-up", "candidatura", dur=0.5, sfx="papel"),
     A("tdef", "pop", "lista", sfx="pop"),
     A("fl", "draw", "provincia", dur=0.5, sfx="whoosh"),
     A("rango", "pop", "21", sfx="ding"), A("rango", "pulse", amount=0.3),
     A("tplazo", "pop", "26", sfx="sello"), A("junta", "punch", "octubre", amount=0.2)]}},
 {"chapter": 3, "number": "3", "headline": "Firmas: *1 de cada 1.000*",
  "narration": "Sin escaños previos, necesita firmas: una de cada mil votantes de la provincia.",
  "illustration": {"svg_file": "registro_free.svg", "layout": "free", "height": 820, "caption": "Fig. 7 · LOREG, art. 169.3", "anims": H(*REG_A) + H(*REG_B) + [
     A("tesc", "pop", "escaños", sfx="pop"), A("tdefesc", "pop", "previos"),
     A("firmas", "slide-right", "firmas", dur=0.5, sfx="papel"), A("boli", "pop", "firmas"), A("boli", "wiggle", amount=0.4),
     A("gente", "fade", "una", dur=0.4), A("uno", "pop", "cada", sfx="ding"), A("uno", "pulse", amount=0.5),
     A("t1000", "pop", "mil", sfx="pop"), A("t01", "pop", "votantes"),
     A("tprov", "pop", "provincia", sfx="sello")]}},
 {"chapter": 5, "headline": "Dudas → *truco*", "narration": "Tú traes las dudas y nosotros te damos el truco.",
  "elements": [{"type": "trick", "trigger": "Tú", "reveal_trigger": "nosotros"}]},
 {"chapter": 5, "number": "TÚ", "headline": "*Confiesa*",
  "narration": "Síguenos y las resolvemos. ¿Cómo se llamaría tu partido?",
  "elements": [{"type": "follow", "trigger": "Síguenos"},
               {"type": "ask", "text": "¿Cómo se llamaría *tu partido*?", "trigger": "Cómo"}]},
]

g = {
    "topic": "Democracia 21, el partido presentado el 10 de octubre de 2026: qué propone según su presentación y qué necesita para presentarse a las generales del 29-N",
    "categoria": "politica",
    "title": "Nace un partido a 50 días del 29-N: ¿llega a tiempo? 🗳️",
    "source": "Fuentes: LO 6/2002 de Partidos Políticos, arts. 3 y 4 · LOREG (LO 5/1985), arts. 44, 45 y 169.3 · BOE 6/10/2026 (Real Decreto 806/2026) · Presentación de Democracia 21 (10/10/2026, Antena 3) · Inscripción en el Registro de Partidos en junio de 2026 (Forbes, Ara)",
    "chapters": ["?", "1", "2", "3", "+", "TÚ"],
    "outro_cta": "Todo tiene un truco",
    "cover": {"text": "¿Llega al *29-N*?", "scene": 0},
    "publish": {
        "at": "2026-10-11T09:00:00+02:00",
        "caption": "¿Le da tiempo a un partido recién presentado a llegar al 29-N? 🗳️ Democracia 21 se presentó el 10 de octubre: según su presentación, es reformista, busca consensos, quiere modernizar la democracia y «situar al ciudadano en el centro». Para ir a las urnas ya está inscrito en el Registro de Partidos; ahora debe presentar candidaturas del 21 al 26 de octubre y, sin escaños previos, reunir firmas de 1 de cada 1.000 votantes de cada provincia. Sin posicionarnos: solo explicamos cómo funciona. ¿Cómo se llamaría tu partido?",
        "description": "Democracia 21, el partido presentado el 10 de octubre de 2026 por la abogada Miriam González, y qué necesita para concurrir a las elecciones generales del 29 de noviembre (Real Decreto 806/2026, BOE del 6 de octubre). 1) Según su presentación, se define como reformista y aboga por facilitar consensos, modernizar la democracia española y «situar al ciudadano en el centro». 2) Cómo nace un partido en España (Ley Orgánica 6/2002): sus promotores firman ante notario el acta fundacional, con los estatutos (sus normas internas), y la presentan en el Registro de Partidos Políticos del Ministerio del Interior, que tiene veinte días para inscribirlo; la inscripción le da personalidad jurídica. Democracia 21 figura inscrito desde junio de 2026. 3) Para el 29-N, cada partido presenta sus candidaturas (listas de candidatos por provincia) ante las juntas electorales del 21 al 26 de octubre. 4) Los partidos que no obtuvieron representación en ninguna de las Cámaras en las elecciones anteriores necesitan, además, las firmas del 0,1 % de los electores inscritos en el censo de cada circunscripción en la que se presenten (LOREG, art. 169.3). Sin posicionarnos: solo explicamos cómo funciona. Fuentes: LO 6/2002; LOREG, arts. 44, 45 y 169.3; BOE (Real Decreto 806/2026).",
        "hashtags": ["eltrucoes"],
    },
    "scenes": scenes,
}
json.dump(g, open(os.path.join(D, "guion.json"), "w"), ensure_ascii=False, indent=2)
n = sum(len(s["narration"].split()) for s in scenes)
print("palabras", n)
for i, s in enumerate(scenes):
    print(i, len(s["narration"].split()), s["narration"])

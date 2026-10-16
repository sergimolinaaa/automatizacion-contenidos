import json, shutil
D = "/home/user/automatizacion-contenidos/content/lote5-07-efecto-ikea"
def A(target, effect, trigger=None, **k):
    d = {"target": target, "effect": effect}
    if trigger: d["trigger"] = trigger
    d.update(k)
    return d
def hide(*ids):
    return [A(i, "hide") for i in ids]

scenes = []
scenes.append({"chapter": 0, "headline": "*Torcida*, pero tuya",
  "narration": "Esa estantería que montaste tú, torcida y con un tornillo de sobra… te parece preciosa.",
  "illustration": {"svg_file": "montaje_full.svg", "layout": "full", "caption": "Fig. 1 · Obra propia", "anims":
    hide("medalla", "plomada") + [
    A("luz", "pulse", amount=0.4),
    A("estanteria", "punch", "estantería", amount=0.25),
    A("carton", "punch", "montaste", amount=0.2),
    A("llave", "wiggle", "montaste", amount=0.6),
    A("nivel", "punch", "torcida", amount=0.4, sfx="chasquido"),
    A("burbuja", "move", "torcida", to=[34, 0], dur=0.6),
    A("plomada", "fade", "torcida", dur=0.4),
    A("tornillo", "punch", "tornillo", amount=0.8),
    A("lsobra", "pop", "sobra", sfx="pop"),
    A("tornillo", "wiggle", "sobra", amount=0.6),
    A("corazones", "pop", "preciosa", sfx="brillo"),
    A("corazones", "float", "preciosa", amount=0.6)]}})
scenes.append({"chapter": 0, "signature": True, "headline": "El truco es…", "narration": "El truco es…"})
scenes.append({"chapter": 1, "number": "1", "headline": "A *montar* cajas",
  "narration": "En 2012, Norton, Mochon y Ariely pusieron a voluntarios a montar cajas de IKEA.",
  "elements": [{"type": "tag", "text": "J. Consum. Psychol., 2012", "tone": "ink", "trigger": "Norton"}],
  "illustration": {"svg_file": "cajas.svg", "caption": "Fig. 2 · El experimento", "anims":
    hide("cajar", "lmontada", "pl", "pr", "badge", "pregunta") + [
    A("aguja", "spin", amount=0.5),
    A("llave", "wiggle", amount=0.5),
    A("camera", "zoom", "Norton", to=[400, 400], amount=1.3, dur=0.8),
    A("piezas", "punch", "voluntarios", amount=0.3),
    A("piezas", "hide", "montar"),
    A("cajal", "pop", "montar", sfx="pop"),
    A("lmontas", "pop", "cajas", sfx="rotulador"),
    A("camera", "zoom", "IKEA", amount=1, dur=0.7)]}})
scenes.append({"chapter": 1, "number": "1", "headline": "¿Cuánto *pagarías*?",
  "narration": "Luego les preguntaron cuánto pagarían. Otros veían la misma caja, ya montada.",
  "illustration": {"svg_file": "cajas.svg", "caption": "Fig. 3 · La subasta", "anims":
    hide("piezas", "pl", "pr", "badge") + [
    A("aguja", "spin", amount=0.5),
    A("pregunta", "pop", "preguntaron", sfx="pop"),
    A("pregunta", "wiggle", "preguntaron", amount=0.3),
    A("cajal", "punch", "pagarían", amount=0.3),
    A("cajar", "pop", "Otros", sfx="pop"),
    A("cajar", "punch", "misma", amount=0.25),
    A("lmontada", "pop", "montada", sfx="rotulador"),
    A("cajar", "punch", "montada", amount=0.25)]}})
scenes.append({"chapter": 2, "number": "2", "headline": "¡Un *63 %* más!",
  "narration": "Los que la montaron ofrecían 78 céntimos de dólar. Los demás, 48. ¡Un 63 % más!",
  "illustration": {"svg_file": "cajas.svg", "caption": "Fig. 4 · Pujas medias", "anims":
    hide("piezas", "pregunta") + [
    A("aguja", "spin", amount=0.5),
    A("cajal", "punch", "montaron", amount=0.3),
    A("camera", "zoom", "ofrecían", to=[400, 300], amount=1.35, dur=0.7),
    A("pl", "pop", "78", sfx="ding"),
    A("pl", "sway", "78", amount=0.4, origin="left"),
    A("camera", "zoom", "demás", to=[620, 300], amount=1.35, dur=0.7),
    A("pr", "pop", "48", sfx="ding"),
    A("pr", "sway", "48", amount=0.4, origin="left"),
    A("camera", "zoom", "Un", amount=1, dur=0.6),
    A("badge", "pop", "63", sfx="sello"),
    A("badge", "wiggle", "63", amount=0.4)]}})
scenes.append({"chapter": 2, "number": "2", "headline": "Origami *de autor*",
  "narration": "Con origami, igual: quien doblaba su rana pagaba casi cinco veces más que quien solo la miraba.",
  "illustration": {"svg_file": "origami_free.svg", "layout": "free", "height": 780, "caption": "Fig. 5 · Ranas de papel", "anims":
    hide("rana2", "grulla", "pila_exp", "l_exp", "igual") + [
    A("rana", "bob", amount=0.35),
    A("rana", "punch", "rana", amount=0.3, sfx="boing"),
    A("pila_tu", "pop", "pagaba", sfx="pop"),
    A("l_tu", "pop", "pagaba"),
    A("pila_otros", "pop", "veces", sfx="pop"),
    A("l_otros", "pop", "veces"),
    A("pila_tu", "punch", "más", amount=0.3),
    A("badge", "pop", "miraba", sfx="sello"),
    A("badge", "wiggle", "miraba", amount=0.4)]}})
scenes.append({"chapter": 2, "number": "2", "headline": "Casi *de experto*",
  "narration": "Y la valoraba casi como una de experto.",
  "illustration": {"svg_file": "origami_free.svg", "layout": "free", "height": 780, "caption": "Fig. 6 · Experto", "anims":
    hide("rana", "pila_otros", "l_otros", "badge") + [
    A("rana2", "bob", amount=0.3),
    A("grulla", "float", amount=0.5),
    A("pila_tu", "punch", "valoraba", amount=0.3),
    A("igual", "pop", "casi", sfx="pop"),
    A("pila_exp", "pop", "como", sfx="pop"),
    A("l_exp", "pop", "experto", sfx="rotulador"),
    A("grulla", "punch", "experto", amount=0.3)]}})
scenes.append({"chapter": 3, "number": "3", "headline": "Si no lo *acabas*…",
  "narration": "Eso sí: si la desmontaban después, o no la terminaban, el efecto desaparecía.",
  "illustration": {"svg_file": "inacabada.svg", "caption": "Fig. 7 · A medias", "anims": [
    A("corazon", "pulse", amount=0.7),
    A("caja", "punch", "Eso", amount=0.25),
    A("flecha", "draw", "desmontaban", dur=0.6, sfx="whoosh"),
    A("paneles", "shake", "desmontaban", amount=0.5),
    A("camera", "zoom", "terminaban", to=[460, 350], amount=1.2, dur=0.7),
    A("lsin", "pop", "terminaban", sfx="rotulador"),
    A("camera", "zoom", "efecto", amount=1, dur=0.6),
    A("corazon", "hide", "desaparecía"),
    A("roto", "pop", "desaparecía", sfx="chasquido"),
    A("roto", "shake", "desaparecía", amount=0.4)]},
  "mascot": {"trigger": "desaparecía", "pose": "think", "note": "La mía lleva a medias desde 2019", "side": "right"}})
scenes.append({"chapter": 3, "number": "3", "headline": "Te sientes *capaz*",
  "narration": "¿Por qué? Terminarlo te hace sentir capaz. Y ese orgullo se paga en cariño.",
  "illustration": {"svg_file": "montaje_full.svg", "layout": "full", "caption": "Fig. 8 · Orgullo", "anims":
    hide("plomada", "lsobra") + [
    A("luz", "pulse", amount=0.4),
    A("estanteria", "punch", "Terminarlo", amount=0.25),
    A("nivel", "punch", "sentir", amount=0.3),
    A("medalla", "pop", "capaz", sfx="ding"),
    A("medalla", "wiggle", "capaz", amount=0.4),
    A("estanteria", "punch", "orgullo", amount=0.2),
    A("corazones", "pop", "cariño", sfx="brillo"),
    A("corazones", "float", "cariño", amount=0.6),
    A("burbuja", "move", to=[34, 0], dur=0.1)]}})
scenes.append({"chapter": 4, "number": "+", "headline": "¿Y el *huevo*?",
  "narration": "Se cuenta que los bizcochos de sobre vendían más al pedir un huevo. Es una anécdota, no un experimento.",
  "elements": [{"type": "stamp", "text": "ANÉCDOTA", "tone": "hot", "trigger": "anécdota", "sfx": "sello"}],
  "illustration": {"svg_file": "bizcocho.svg", "caption": "Fig. 9 · La leyenda del huevo", "anims":
    hide("salpica") + [
    A("cascaras", "wiggle", amount=0.3),
    A("yema", "bob", amount=0.25),
    A("caja", "punch", "bizcochos", amount=0.25),
    A("camera", "zoom", "sobre", to=[420, 300], amount=1.25, dur=0.7),
    A("sello", "pop", "pedir", sfx="pop"),
    A("yema", "move", "huevo", to=[0, 168], dur=0.5),
    A("yema", "hide", "Es"),
    A("salpica", "pop", "Es", sfx="splash"),
    A("camera", "zoom", "anécdota", amount=1, dur=0.6)]}})
scenes.append({"chapter": 5, "number": "TÚ", "headline": "*Confiesa*",
  "narration": "Síguenos para más trucos. Confiesa: ¿qué chapuza tuya defiendes como obra maestra?",
  "elements": [{"type": "follow", "trigger": "Síguenos"},
               {"type": "ask", "text": "¿Qué *chapuza* tuya defiendes como obra maestra?", "trigger": "Confiesa"}]})

g = {
 "topic": "El efecto IKEA: valoramos más lo que montamos nosotros",
 "categoria": "psicologia",
 "title": "¿Por qué tu estantería torcida te parece preciosa? 🔩",
 "source": "Fuentes: Norton, Mochon & Ariely, Journal of Consumer Psychology, 22, 453-460 (2012) · Mochon, Norton & Ariely, Int. J. Research in Marketing, 29, 363-369 (2012)",
 "chapters": ["?", "1", "2", "3", "+", "TÚ"],
 "outro_cta": "Todo tiene un truco",
 "cover": {"text": "Tu mueble *torcido* vale más", "scene": 0},
 "publish": {
  "caption": "Tu estantería está torcida, le sobra un tornillo… y te parece preciosa 🔩 Es el efecto IKEA: valoramos más lo que montamos nosotros. ¿Qué chapuza tuya defiendes como obra maestra?",
  "description": "En 2012, Michael Norton, Daniel Mochon y Dan Ariely publicaron en el Journal of Consumer Psychology «The IKEA effect: When labor leads to love». Quienes montaban una caja de almacenaje de IKEA ofrecían de media 0,78 dólares por ella, frente a 0,48 de quienes la recibían ya montada (alrededor de un 63 % más). Con origami pasó lo mismo: los autores de ranas y grullas de papel pujaban casi cinco veces más que otros participantes por sus propias figuras, casi como por las de un experto. Pero el efecto desaparecía si no terminaban la tarea o si montaban y luego desmontaban. Un trabajo posterior de los mismos autores lo relaciona con sentirse capaz. La historia de los bizcochos de sobre a los que había que añadir un huevo es una anécdota popular, no un experimento. Fuentes: Norton, Mochon & Ariely (2012), J. Consum. Psychol. 22, 453-460; Mochon, Norton & Ariely (2012), Int. J. Res. Mark. 29, 363-369.",
  "hashtags": ["efectoikea", "psicologia", "sesgos", "cerebro", "bricolaje", "curiosidades", "ciencia", "eltrucoes"]},
 "scenes": scenes}
json.dump(g, open(D + "/guion.json", "w"), ensure_ascii=False, indent=2)
for f in ("montaje_full.svg", "cajas.svg", "origami_free.svg", "inacabada.svg", "bizcocho.svg"):
    shutil.copy(f, D + "/" + f)

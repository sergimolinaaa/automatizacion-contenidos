import json, shutil
D = "/home/user/automatizacion-contenidos/content/lote5-08-pulpo-color"
def A(target, effect, trigger=None, **k):
    d = {"target": target, "effect": effect}
    if trigger: d["trigger"] = trigger
    d.update(k)
    return d
def hide(*ids):
    return [A(i, "hide") for i in ids]
PIEL_ALL = ["cr_cerrados", "opsinas", "l_ops", "interroga", "crono", "pulsos", "l_cer", "luz_iri", "refl_iri", "luz_leu", "refl_leu", "l_iri", "l_leu", "l_cro"]
def piel_hide(*keep):
    return hide(*[i for i in PIEL_ALL if i not in keep])

scenes = []
scenes.append({"chapter": 0, "headline": "Era una *roca*",
  "narration": "Mira esta roca. Ahora… ¡es un pulpo! Ha cambiado de color en menos de un segundo.",
  "illustration": {"svg_file": "arrecife_full.svg", "layout": "full", "caption": "Fig. 1 · Pulpo común", "anims": [
    A("ojos", "blink"),
    A("burbujas", "float", amount=0.8),
    A("peces", "drift", amount=0.8),
    A("algas", "sway", origin="bottom", amount=0.5),
    A("coral", "sway", origin="bottom", amount=0.2),
    A("anemona", "pulse", amount=0.6),
    A("pulpo", "punch", "roca", amount=0.12),
    A("rojo", "fade", "pulpo", dur=0.3, sfx="sorpresa"),
    A("lpulpo", "pop", "pulpo"),
    A("pulpo", "punch", "cambiado", amount=0.2),
    A("crono", "pop", "menos", sfx="chasquido"),
    A("aguja", "pop", "menos"),
    A("eje", "pop", "menos"),
    A("aguja", "spin", "menos", amount=2.5, origin="bottom")]}})
scenes.append({"chapter": 0, "signature": True, "headline": "El truco es…", "narration": "El truco es…"})
scenes.append({"chapter": 1, "number": "1", "headline": "Saquitos de *pigmento*",
  "narration": "Su piel tiene miles de saquitos de pigmento: amarillo, rojo y marrón. Son los cromatóforos.",
  "illustration": {"svg_file": "cromatoforo_free.svg", "layout": "free", "height": 780, "caption": "Fig. 2 · Piel al microscopio", "anims":
    hide("relajado", "contraido", "nervio", "impulso", "l_pig", "l_mus", "l_ner") + [
    A("vista", "breathe", amount=0.6),
    A("vista", "punch", "piel", amount=0.12),
    A("vista", "punch", "pigmento", amount=0.12),
    A("l_am", "pop", "amarillo", sfx="pop"),
    A("l_ro", "pop", "rojo", sfx="pop"),
    A("l_ma", "pop", "marrón", sfx="pop"),
    A("l_cro", "pop", "cromatóforos", sfx="ding")]}})
scenes.append({"chapter": 1, "number": "1", "headline": "Músculos que *estiran*",
  "narration": "Cada saquito está rodeado de músculos. Si se contraen, lo estiran y el color se extiende.",
  "illustration": {"svg_file": "cromatoforo_free.svg", "layout": "free", "height": 780, "caption": "Fig. 3 · Un cromatóforo", "anims":
    hide("vista", "l_am", "l_ro", "l_ma", "l_cro", "l_ner") + [
    A("relajado", "breathe", amount=0.6),
    A("relajado", "punch", "saquito", amount=0.15),
    A("l_pig", "pop", "saquito", sfx="pop"),
    A("l_mus", "pop", "músculos", sfx="pop"),
    A("impulso", "move", "contraen", to=[160, -126], dur=0.4),
    A("impulso", "hide", "estiran"),
    A("relajado", "hide", "estiran"),
    A("contraido", "pop", "estiran", sfx="boing"),
    A("contraido", "punch", "color", amount=0.15),
    A("contraido", "breathe", "extiende", amount=0.6)]}})
scenes.append({"chapter": 2, "number": "2", "headline": "Nervios *directos*",
  "narration": "Esos músculos los manda el cerebro con nervios directos. Por eso basta menos de un segundo.",
  "illustration": {"svg_file": "piel.svg", "caption": "Fig. 4 · Corte de la piel", "anims":
    piel_hide("cr_cerrados", "crono", "pulsos", "l_cer", "l_cro") + [
    A("l_cro", "pop", "músculos", sfx="pop"),
    A("cr_cerrados", "punch", "músculos", amount=0.2),
    A("nervios", "draw", "cerebro", dur=0.8, sfx="whoosh"),
    A("l_cer", "pop", "cerebro"),
    A("pulsos", "move", "nervios", to=[560, -10], dur=0.8),
    A("pulsos", "hide", "Por"),
    A("cr_cerrados", "hide", "Por"),
    A("cr_abiertos", "pop", "Por", sfx="boing"),
    A("superficie", "punch", "basta", amount=0.15),
    A("crono", "pop", "segundo", sfx="chasquido")]}})
scenes.append({"chapter": 3, "number": "3", "headline": "Espejos *bajo la piel*",
  "narration": "Debajo hay más trucos: los iridóforos, capas que reflejan la luz en azules y verdes.",
  "illustration": {"svg_file": "piel.svg", "caption": "Fig. 5 · Iridóforos", "anims":
    piel_hide("luz_iri", "refl_iri", "l_iri") + [
    A("camera", "zoom", "Debajo", to=[400, 340], amount=1.25, dur=0.7),
    A("iridoforos", "punch", "iridóforos", amount=0.15),
    A("camera", "zoom", "capas", amount=1, dur=0.6),
    A("l_iri", "pop", "reflejan", sfx="pop"),
    A("luz_iri", "draw", "luz", dur=0.5, sfx="whoosh"),
    A("refl_iri", "draw", "azules", dur=0.6, sfx="brillo"),
    A("refl_iri", "pulse", "verdes", amount=0.5)]}})
scenes.append({"chapter": 3, "number": "3", "headline": "Blanco que *copia*",
  "narration": "Y los leucóforos, blancos, devuelven la luz que llega: toman el color del entorno.",
  "illustration": {"svg_file": "piel.svg", "caption": "Fig. 6 · Leucóforos", "anims":
    piel_hide("luz_leu", "refl_leu", "l_leu") + [
    A("leucoforos", "punch", "leucóforos", amount=0.15),
    A("l_leu", "pop", "leucóforos", sfx="pop"),
    A("luz_leu", "draw", "luz", dur=0.5, sfx="whoosh"),
    A("refl_leu", "draw", "llega", dur=0.6, sfx="brillo"),
    A("superficie", "punch", "color", amount=0.15),
    A("refl_leu", "pulse", "entorno", amount=0.5)]},
  "mascot": {"trigger": "entorno", "pose": "point", "note": "Camaleón, toma nota", "side": "right"}})
scenes.append({"chapter": 4, "number": "+", "headline": "¿Y si no ve *colores*?",
  "narration": "El misterio: sus ojos probablemente no distinguen colores. ¿Cómo los imita, entonces?",
  "illustration": {"svg_file": "ojo.svg", "caption": "Fig. 7 · Ojo de pulpo", "anims": [
    A("ojo", "blink"),
    A("cabeza", "breathe", amount=0.5),
    A("camera", "zoom", "ojos", to=[390, 380], amount=1.3, dur=0.7),
    A("ojo", "punch", "ojos", amount=0.15),
    A("camera", "zoom", "distinguen", amount=1, dur=0.6),
    A("vista_color", "hide", "distinguen"),
    A("l_bn", "pop", "colores", sfx="pop"),
    A("interroga", "pop", "imita", sfx="sorpresa"),
    A("interroga", "wiggle", "imita", amount=0.5)]},
  "mascot": {"trigger": "imita", "pose": "think", "note": "¿Daltónico y rey del disfraz?", "side": "right"}})
scenes.append({"chapter": 4, "number": "+", "headline": "Piel que *capta luz*",
  "narration": "Una pista: su piel tiene opsinas, las proteínas del ojo que captan la luz. Pero el enigma sigue abierto.",
  "illustration": {"svg_file": "piel.svg", "caption": "Fig. 8 · Opsinas en la piel", "anims":
    piel_hide("opsinas", "l_ops", "interroga", "luz_leu") + [
    A("camera", "zoom", "piel", to=[400, 290], amount=1.3, dur=0.7),
    A("opsinas", "pop", "opsinas", sfx="brillo"),
    A("opsinas", "pulse", "opsinas", amount=0.6),
    A("camera", "zoom", "proteínas", amount=1, dur=0.6),
    A("l_ops", "pop", "captan", sfx="pop"),
    A("luz_leu", "draw", "luz", dur=0.5, sfx="whoosh"),
    A("interroga", "pop", "enigma", sfx="sorpresa"),
    A("interroga", "wiggle", "enigma", amount=0.5)]}})
scenes.append({"chapter": 5, "number": "TÚ", "headline": "Te *toca*",
  "narration": "Síguenos para más trucos. Si fueras pulpo, ¿de qué color te pondrías ahora mismo?",
  "elements": [{"type": "follow", "trigger": "Síguenos"},
               {"type": "ask", "text": "Si fueras pulpo, ¿de qué *color* te pondrías ahora?", "trigger": "fueras"}]})
g = {
 "topic": "El pulpo cambia de color en un instante",
 "categoria": "animales",
 "title": "El pulpo cambia de color en menos de un segundo 🐙",
 "source": "Fuentes: Messenger, Biological Reviews 76 (2001) · Mäthger et al., J. R. Soc. Interface 6 (2009) · Ramirez & Oakley, J. Exp. Biol. 218 (2015)",
 "chapters": ["?", "1", "2", "3", "+", "TÚ"],
 "outro_cta": "Todo tiene un truco",
 "cover": {"text": "Cambia de color *en un instante*", "scene": 0},
 "publish": {
  "caption": "Hace un segundo era una roca… y ahora es un pulpo 🐙 Su piel está llena de saquitos de pigmento que unos músculos abren al instante. ¿De qué color te pondrías tú ahora mismo?",
  "description": "El pulpo cambia de color en menos de un segundo gracias a los cromatóforos: saquitos elásticos de pigmento amarillo, rojo o marrón rodeados de músculos radiales. Esos músculos los controla directamente el cerebro a través de nervios, y al contraerse estiran el saquito y el color se extiende por la piel. Debajo hay más capas: los iridóforos, pilas de placas que reflejan la luz y dan brillos azules y verdes, y los leucóforos, células blancas que devuelven la luz que les llega y toman el color del entorno. El gran misterio: los cefalópodos tienen un solo tipo de fotorreceptor y probablemente no distinguen colores. Se ha visto que su piel tiene opsinas, proteínas que captan la luz, pero cómo igualan los colores sigue sin resolverse. Fuentes: Messenger (2001), Biological Reviews 76; Mäthger et al. (2009), J. R. Soc. Interface 6; Ramirez & Oakley (2015), J. Exp. Biol. 218.",
  "hashtags": ["pulpo", "camuflaje", "animales", "biologia", "oceano", "curiosidades", "ciencia", "eltrucoes"]},
 "scenes": scenes}
json.dump(g, open(D + "/guion.json", "w"), ensure_ascii=False, indent=2)
for f in ("arrecife_full.svg", "cromatoforo_free.svg", "piel.svg", "ojo.svg"):
    shutil.copy(f, D + "/" + f)

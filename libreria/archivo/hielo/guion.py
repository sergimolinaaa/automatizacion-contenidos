import json
def A(target, effect, trigger=None, **k):
    d = {"target": target, "effect": effect}
    if trigger: d["trigger"] = trigger
    d.update(k); return d
def Z(x, y, amount, trigger=None, dur=0.8):
    d = {"target": "camera", "effect": "zoom", "to": [x, y], "amount": amount, "dur": dur}
    if trigger: d["trigger"] = trigger
    return d
vaso_loops = [A("ice", "bob", amount=0.3), A("flame", "wiggle", amount=0.6, origin="bottom"), A("bubs", "float", amount=0.5)]
mol_loops = [A("liq1", "shake", amount=1.0), A("liq2", "wiggle", amount=0.7), A("liq3", "drift", amount=0.25), A("jitter", "pulse", amount=1.2)]
lago_loops = [A("weed", "sway", origin="bottom", amount=0.6), A("snow", "drift", amount=0.5), A("fish3", "float", amount=0.6), A("bubs", "pulse", amount=0.6)]
g = {
 "topic": "Por qué el hielo flota",
 "categoria": "fisica",
 "title": "¿Por qué el hielo flota? 🧊",
 "source": "Fuentes: USGS Water Science School · NOAA (icebergs) · propiedades del agua",
 "chapters": ["?", "1", "2", "3", "+", "TÚ"],
 "outro_cta": "La naturaleza tiene trucos",
 "cover": {"text": "El hielo *no debería flotar*", "scene": 0},
 "publish": {
  "caption": "Casi todo lo sólido se hunde en su propio líquido… menos el hielo 🧊 Su truco son unos hexágonos con huecos. ¿Te imaginas tu refresco con los cubitos en el fondo?",
  "description": "Casi todas las sustancias son más densas en sólido que en líquido, pero el agua no: al congelarse, sus moléculas se ordenan en una red de hexágonos con huecos y el hielo ocupa un 9 % más de espacio. Por eso es menos denso y flota (un iceberg esconde casi el 90 % bajo el agua), los lagos se congelan por arriba y debajo el agua se queda a unos 4 °C. Fuentes: USGS Water Science School; NOAA.",
  "hashtags": ["hielo", "agua", "fisica", "ciencia", "curiosidades", "sabiasque", "eltrucoes"]
 },
 "scenes": [
  {"chapter": 0, "headline": "El hielo *no debería flotar*",
   "narration": "Casi todo lo sólido se hunde en su propio líquido… menos el hielo.",
   "illustration": {"svg_file": "vaso.svg", "caption": "Fig. 1 · Agua y cera", "anims": [
     A("lflota", "hide"), A("lhunde", "hide"), A("lb", "hide"), A("la", "hide"), *vaso_loops,
     A("lb", "pop", "sólido", sfx="pop"),
     A("wax", "move", "hunde", to=[0, 222], dur=1.1, sfx="whoosh"),
     A("splash", "ripple", "hunde", amount=0.8),
     A("lhunde", "pop", "propio"),
     A("la", "pop", "menos"),
     Z(270, 330, 1.5, "menos"),
     A("ice", "punch", "hielo"),
     A("lflota", "pop", "hielo", sfx="ding")]}},
  {"chapter": 0, "signature": True, "headline": "El truco es…", "narration": "El truco es…"},
  {"chapter": 1, "number": "1", "headline": "En líquido, *apretadas*",
   "narration": "En el agua líquida, las moléculas van apretujadas, chocando sin parar y desordenadas.",
   "illustration": {"svg_file": "moleculas.svg", "caption": "Fig. 2 · Agua por dentro", "anims": [
     *[A(x, "hide") for x in ["hexes", "gaps", "more", "lmas", "lc", "la", "lb"]], *mol_loops,
     A("la", "pop", "líquida", sfx="pop"),
     Z(240, 370, 1.3, "moléculas"),
     A("liq1", "punch", "apretujadas"),
     A("jitter", "pulse", "chocando", amount=3),
     A("liq3", "shake", "chocando", amount=1.4),
     A("liq2", "punch", "desordenadas")]}},
  {"chapter": 2, "number": "2", "headline": "En hielo, *con huecos*",
   "narration": "Al congelarse, se enganchan en hexágonos perfectos… que dejan huecos por dentro.",
   "illustration": {"svg_file": "moleculas.svg", "caption": "Fig. 3 · La red del hielo", "anims": [
     *[A(x, "hide") for x in ["hexes", "gaps", "more", "lmas", "lc", "lb"]], *mol_loops,
     A("lb", "pop", "congelarse", sfx="pop"),
     Z(720, 300, 1.35, "congelarse"),
     A("lattice", "punch", "enganchan", amount=0.5),
     A("hexes", "draw", "hexágonos", dur=0.8, sfx="brillo"),
     Z(500, 350, 1, "dejan"),
     A("gaps", "pop", "huecos", sfx="pop"),
     A("lc", "pop", "huecos"),
     A("gaps", "pulse", "dentro", amount=1.5)]}},
  {"chapter": 2, "number": "2", "headline": "Ocupa *más sitio*",
   "narration": "Mismas moléculas, más espacio: el hielo ocupa un 9 % más que el agua.",
   "illustration": {"svg_file": "moleculas.svg", "caption": "Fig. 4 · Se estira", "anims": [
     A("hexes", "hide"), A("lc", "hide"), A("more", "hide"), A("lmas", "hide"), *mol_loops,
     A("gaps", "pulse", amount=1.2),
     A("liq2", "punch", "Mismas"), A("lattice", "punch", "moléculas", amount=0.5),
     A("more", "slide-right", "espacio", sfx="whoosh"),
     A("lmas", "pop", "ocupa"),
     Z(760, 420, 1.3, "ocupa"),
     A("more", "pulse", "9", amount=1.2),
     Z(500, 350, 1, "agua")]}},
  {"chapter": 3, "number": "3", "headline": "Menos denso… *flota*",
   "narration": "Mismo peso en más espacio: el hielo es menos denso que el agua. Por eso flota.",
   "illustration": {"svg_file": "vaso.svg", "caption": "Fig. 5 · Flotando", "anims": [
     A("lflota", "hide"), *vaso_loops,
     A("wax", "move", to=[0, 222], dur=0.05),
     A("ice", "punch", "peso"),
     Z(270, 330, 1.5, "denso"),
     A("la", "punch", "agua"),
     A("lflota", "pop", "flota", sfx="ding"),
     A("ice", "bob", "flota", amount=0.8)]}},
  {"chapter": 3, "number": "3", "headline": "La *punta* del iceberg",
   "narration": "Y por eso asoma solo un poquito: un iceberg esconde casi el 90 % bajo el agua.",
   "illustration": {"svg_file": "iceberg.svg", "caption": "Fig. 6 · Iceberg", "anims": [
     *[A(x, "hide") for x in ["b10", "b90", "l10", "l90", "lbajo"]],
     A("rip1", "ripple", phase=0.0), A("rip2", "ripple", phase=0.5),
     A("fish1", "drift", amount=0.8), A("fish2", "drift", amount=0.6, phase=0.4), A("gulls", "float", amount=0.6), A("bubbles", "float", amount=0.6),
     Z(640, 220, 1.4, "asoma"),
     A("b10", "draw", "asoma", dur=0.6, sfx="rotulador"), A("l10", "pop", "poquito"),
     Z(500, 350, 1, "iceberg"),
     A("berg", "punch", "esconde", amount=0.4),
     A("b90", "draw", "90", dur=0.8, sfx="rotulador"), A("l90", "pop", "90"),
     A("lbajo", "pop", "bajo")]}},
  {"chapter": 4, "number": "+", "headline": "Lagos con *tapa*",
   "narration": "Gracias a eso, los lagos se congelan por arriba. El hielo hace de tapa y aísla.",
   "illustration": {"svg_file": "lago.svg", "caption": "Fig. 7 · Lago en invierno", "anims": [
     A("ltapa", "hide"), A("l0", "hide"), A("l4", "hide"), *lago_loops,
     A("fish1", "drift", amount=0.6), A("fish2", "drift", amount=0.5, phase=0.5),
     A("icesheet", "slide-down", "congelan", dur=0.8, sfx="whoosh"),
     Z(500, 300, 1.35, "hielo"),
     A("ltapa", "pop", "tapa", sfx="pop"),
     A("icesheet", "punch", "aísla", amount=0.3)]}},
  {"chapter": 4, "number": "+", "headline": "Abajo, *4 grados*",
   "narration": "Debajo, el agua del fondo se queda a unos 4 grados, y los peces siguen nadando tan tranquilos.",
   "illustration": {"svg_file": "lago.svg", "caption": "Fig. 8 · Bajo el hielo", "anims": [
     A("ltapa", "hide"), A("l0", "hide"), A("l4", "hide"), *lago_loops,
     A("l0", "pop", "Debajo"),
     Z(520, 480, 1.35, "fondo"),
     A("l4", "pop", "4", sfx="ding"),
     A("fish1", "move", "peces", to=[100, 20], dur=2.0),
     A("fish2", "move", "peces", to=[-140, 0], dur=2.2),
     Z(500, 350, 1, "nadando"),
     A("snowman", "punch", "tranquilos")]},
   "mascot": {"trigger": "tranquilos", "pose": "cheer", "note": "Un edredón de hielo", "side": "right"}},
  {"chapter": 5, "number": "TÚ", "headline": "*Confiesa*",
   "narration": "Síguenos para más trucos. ¿Te imaginas tu refresco con los cubitos en el fondo?",
   "elements": [{"type": "follow", "trigger": "Síguenos"},
                {"type": "ask", "text": "¿Te imaginas tu refresco con los cubitos *en el fondo*?", "trigger": "Te"}]}
 ]}
open("/home/user/automatizacion-contenidos/content/lote2-03-hielo-flota/guion.json", "w").write(json.dumps(g, ensure_ascii=False, indent=2))

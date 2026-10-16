import json, re
H = lambda t, e, tr=None, **k: dict(target=t, effect=e, **({"trigger": tr} if tr else {}), **k)
hide = lambda *ids: [H(i, "hide") for i in ids]
E, G, M = "etiqueta_full.svg", "grafica.svg", "movil_free.svg"
full = lambda svg, cap, an: {"svg_file": svg, "layout": "full", "caption": cap, "anims": an}
free = lambda svg, cap, an: {"svg_file": svg, "layout": "free", "height": 840, "caption": cap, "anims": an}
panel = lambda svg, cap, an: {"svg_file": svg, "caption": cap, "anims": an}
scenes = [
 {"chapter": 0, "headline": "¿Rebaja *de verdad*?",
  "narration": "Este Black Friday, muchas rebajas no son rebajas.",
  "illustration": full(E, "Fig. 1 · Un «chollo»", hide("viejo50", "t2sem", "tdef", "cero", "falsa") + [
     H("banner", "pulse", amount=0.35), H("badge", "punch", "Black", amount=0.25, sfx="pop"),
     H("duda", "pop", "muchas", sfx="sorpresa"), H("duda", "bob", amount=0.6),
     H("badge", "spin", amount=0.15), H("bolsas", "sway", amount=0.4),
     H("etiqueta", "shake", "no", amount=0.5), H("falsa", "pop", "no", sfx="sello"),
     H("falsa", "punch", "son", amount=0.2)])},
 {"chapter": 1, "number": "1", "headline": "Subir… y *rebajar*",
  "narration": "El truco es… subir el precio unas semanas antes, y luego «rebajarlo».",
  "elements": [{"type": "tag", "text": "EL TRUCO ES…", "trigger": "truco"}],
  "illustration": panel(G, "Fig. 2 · Precio día a día", hide("p50", "igual", "ventana", "t30", "minimo", "tmin", "tley") + [
     H("l1", "draw", dur=0.8), H("bf", "pop", "truco", sfx="pop"),
     H("l2", "draw", "subir", dur=0.6, sfx="whoosh"), H("p100", "pop", "precio", sfx="pop"),
     H("p100", "punch", "semanas", amount=0.2),
     H("l3", "draw", "rebajarlo", dur=0.6, sfx="whoosh"), H("m50", "pop", "rebajarlo", sfx="ding"),
     H("m50", "pulse", amount=0.5)])},
 {"chapter": 1, "number": "1", "headline": "Pagas *lo mismo*",
  "narration": "Costaba 50. Lo suben a 100… y vuelve a 50 con un «menos 50 %». Pagas lo mismo.",
  "illustration": panel(G, "Fig. 3 · Precios ficticios", hide("p50", "p100", "m50", "igual", "ventana", "t30", "minimo", "tmin", "tley") + [
     H("p50", "pop", "Costaba", sfx="pop"), H("l1", "punch", "Costaba", amount=0.15),
     H("l2", "punch", "suben", amount=0.15), H("p100", "pop", "100", sfx="pop"),
     H("l3", "punch", "vuelve", amount=0.15), H("m50", "pop", "menos", sfx="ding"),
     H("bf", "punch", "menos", amount=0.2), H("igual", "pop", "mismo", sfx="sello"),
     H("igual", "pulse", amount=0.4)]),
  "mascot": {"trigger": "Pagas", "pose": "surprise", "note": "¡Qué morro!", "side": "left"}},
 {"chapter": 2, "number": "2", "headline": "La regla de *30 días*",
  "narration": "En España hay una ley: el precio tachado debe ser el más bajo de los últimos 30 días.",
  "illustration": panel(G, "Fig. 4 · Ley 7/1996, art. 20", hide("igual", "ventana", "t30", "minimo", "tmin", "tley") + [
     H("tley", "pop", "ley", sfx="sello"), H("m50", "pulse", amount=0.4),
     H("p100", "shake", "tachado", amount=0.5), H("ventana", "fade", "últimos", dur=0.5, sfx="whoosh"),
     H("t30", "pop", "30", sfx="pop"), H("minimo", "pop", "bajo", sfx="ding"),
     H("tmin", "pop", "bajo"), H("minimo", "pulse", amount=0.6)])},
 {"chapter": 2, "number": "2", "headline": "Tachado = *50 €*",
  "narration": "Si hace dos semanas costaba 50, el tachado tiene que decir 50. Rebaja: cero.",
  "illustration": full(E, "Fig. 5 · Lo que exige la ley", hide("viejo50", "t2sem", "tdef", "cero", "falsa", "duda") + [
     H("bolsas", "sway", amount=0.4), H("t2sem", "pop", "hace", sfx="pop"),
     H("t2sem", "hide", "tachado"), H("tdef", "pop", "tachado", sfx="pop"),
     H("viejo", "hide", "decir"), H("viejo50", "pop", "decir", sfx="papel"),
     H("badge", "shake", "Rebaja", amount=0.6), H("badge", "hide", "cero"),
     H("cero", "pop", "cero", sfx="sello"), H("etiqueta", "punch", "cero", amount=0.15)])},
 {"chapter": 3, "number": "3", "headline": "Haz *captura*",
  "narration": "Tu truco: haz captura del precio semanas antes. O mira su historial: lo que costó cada día.",
  "illustration": free(M, "Fig. 6 · Tus pruebas", hide("hoja", "nocuadra", "this", "this2", "this3", "flash", "pico") + [
     H("telefono", "slide-up", dur=0.5), H("tcap", "pop", "captura", sfx="pop"),
     H("flash", "fade", "captura", dur=0.15), H("flash", "hide", "precio"),
     H("tfecha", "pop", "semanas", sfx="pop"), H("lupa", "pop", "mira", sfx="whoosh"), H("lupa", "sway", amount=0.5),
     H("curva", "draw", "historial", dur=0.8), H("this", "pop", "historial", sfx="ding"),
     H("this2", "pop", "costó"), H("pico", "pop", "costó", sfx="pop"), H("this3", "pop", "día"), H("pico", "pulse", amount=0.6)])},
 {"chapter": 4, "number": "+", "headline": "¿No *cuadra*?",
  "narration": "¿No cuadra? Pide la hoja de reclamaciones.",
  "illustration": free(M, "Fig. 7 · Tu derecho", hide("this", "this2", "this3", "flash", "tcap", "tfecha", "lupa", "hoja", "nocuadra") + [
     H("pico", "pulse", amount=0.7), H("telefono", "shake", "No", amount=0.4),
     H("nocuadra", "pop", "cuadra", sfx="sello"), H("hoja", "slide-left", "hoja", dur=0.5, sfx="papel"),
     H("hoja", "punch", "reclamaciones", amount=0.2), H("nocuadra", "punch", "reclamaciones", amount=0.15)])},
 {"chapter": 5, "headline": "Dudas → *truco*",
  "narration": "Tú traes las dudas y nosotros te damos el truco.",
  "elements": [{"type": "trick", "trigger": "Tú", "reveal_trigger": "nosotros"}]},
 {"chapter": 5, "number": "TÚ", "headline": "*Confiesa*",
  "narration": "Síguenos y las resolvemos. ¿Cuántas gangas has pagado a precio normal?",
  "elements": [{"type": "follow", "trigger": "Síguenos"},
               {"type": "ask", "text": "¿Cuántas *gangas* has pagado a precio normal?", "trigger": "Cuántas"}]},
]
g = {
 "topic": "Cómo saber si una oferta del Black Friday (27 de noviembre de 2026) es falsa: la regla del precio anterior más bajo de los últimos 30 días",
 "categoria": "consumo",
 "title": "¿Esa rebaja del Black Friday es de verdad? 🏷️",
 "source": "Fuentes: Ley 7/1996 de Ordenación del Comercio Minorista, art. 20.1 (redacción del Real Decreto-ley 24/2021, art. 85) · Directiva (UE) 2019/2161 · Ejemplo con precios ficticios",
 "chapters": ["?", "1", "2", "3", "+", "TÚ"],
 "outro_cta": "Todo tiene un truco",
 "cover": {"text": "Rebajas *de mentira*", "scene": 0},
 "publish": {
  "caption": "¿Y si tu «-50 %» del Black Friday cuesta lo mismo que hace un mes? 🏷️ El truco: subir el precio unas semanas antes y luego «rebajarlo». En España, el precio tachado debe ser el más bajo de los 30 días anteriores. Haz captura del precio o mira su historial. ¿Te la han colado alguna vez?",
  "description": "Cómo saber si una oferta del Black Friday (27 de noviembre de 2026) es falsa. 1) El truco: subir el precio unas semanas antes y después anunciar una gran «rebaja» que te deja en el precio de siempre (ejemplo con precios ficticios: de 50 a 100 € y vuelta a 50 € con un «-50 %»). 2) En España, cuando una tienda anuncia una reducción de precio, el precio anterior que muestra debe ser el más bajo que aplicó a ese mismo producto en los 30 días anteriores (Ley 7/1996 de Ordenación del Comercio Minorista, art. 20.1, en la redacción del Real Decreto-ley 24/2021, que aplica la Directiva europea 2019/2161). 3) Cómo comprobarlo: haz captura del precio (con fecha) unas semanas antes o consulta su historial de precios. 4) Si no cuadra, pide la hoja de reclamaciones o acude a consumo. Fuentes: Ley 7/1996, art. 20; Real Decreto-ley 24/2021 (BOE).",
  "hashtags": ["eltrucoes"]},
 "scenes": scenes,
}
# comprobaciones
norm = lambda w: re.sub(r"[^\wáéíóúñü%]", "", w.lower())
tot = 0
for i, s in enumerate(scenes):
    words = [norm(w) for w in s["narration"].split()]
    tot += len(s["narration"].split())
    trig = [a.get("trigger") for a in s.get("illustration", {}).get("anims", [])] + [e.get("trigger") for e in s.get("elements", [])] + [e.get("reveal_trigger") for e in s.get("elements", [])] + [s.get("mascot", {}).get("trigger")]
    for t in trig:
        if t and norm(t) not in words: print("TRIGGER?", i, t)
print("palabras", tot)
open("/home/user/automatizacion-contenidos/content/lote6-05-black-friday/guion.json", "w").write(json.dumps(g, ensure_ascii=False, indent=2))

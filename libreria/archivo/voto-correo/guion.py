import json, shutil, os, re
D = "/home/user/automatizacion-contenidos/content/lote6-01-voto-correo"
os.makedirs(D, exist_ok=True)
for fn in ("gancho_full.svg", "oficina.svg", "sobres_free.svg", "colegio_full.svg"):
    shutil.copy(fn, D)

def A(target, effect, trigger=None, **kw):
    a = {"target": target, "effect": effect}
    if trigger: a["trigger"] = trigger
    a.update(kw)
    return a
H = lambda *ids: [A(i, "hide") for i in ids]

scenes = [
 {"chapter": 0, "headline": "¿Tu voto *se pierde*?",
  "narration": "¿Votas por correo el 29-N? Mucha gente teme que su voto se pierda por el camino.",
  "illustration": {"svg_file": "gancho_full.svg", "layout": "full", "caption": "Fig. 1 · Del buzón a la urna", "anims": [
     A("nubes", "drift", amount=0.5), A("sobre", "bob", amount=0.7),
     A("buzon", "punch", "Votas", amount=0.3), A("sobre", "punch", "correo", amount=0.25),
     A("ruta", "draw", "Mucha", dur=1.0, sfx="whoosh"), A("punta", "pop", "gente"),
     A("dudas", "pop", "teme", sfx="sorpresa"), A("dudas", "pulse", amount=0.7),
     A("urna", "punch", "voto", amount=0.3), A("tpierde", "pop", "pierda", sfx="pop"),
     A("sobre", "shake", "camino", amount=0.5)]}},
 {"chapter": 0, "signature": True, "headline": "El truco es…", "narration": "El truco es…"},
 {"chapter": 1, "number": "1", "headline": "Pídelo en *Correos*",
  "narration": "Sin posicionarnos: solo cómo funciona. Primero, pides el voto en Correos, con tu DNI, hasta el 19 de noviembre.",
  "elements": [{"type": "tag", "text": "SIN POSICIONARNOS", "tone": "ink", "trigger": "posicionarnos"}],
  "illustration": {"svg_file": "oficina.svg", "caption": "Fig. 2 · LOREG, art. 72", "anims": H("l25", "lgratis", "sello", "lcust", "sobreE", "l19", "form", "dni") + [
     A("saca", "breathe", amount=0.3),
     A("rotulo", "punch", "Primero", amount=0.25),
     A("form", "pop", "pides", sfx="papel"), A("rotulo", "punch", "Correos", amount=0.3),
     A("dni", "pop", "DNI", sfx="pop"), A("dni", "wiggle", amount=0.3),
     A("l19", "pop", "19", sfx="ding"), A("l19", "punch", "noviembre", amount=0.2)]}},
 {"chapter": 1, "number": "1", "headline": "Te llega *certificado*",
  "narration": "Desde el 9 de noviembre, te llega a casa por correo certificado. Solo te lo dan a ti, con DNI.",
  "illustration": {"svg_file": "sobres_free.svg", "layout": "free", "height": 820, "caption": "Fig. 3 · LOREG, art. 73", "anims": H("papeleta", "lpap", "sobrev", "lvot", "a1", "cert", "sobremesa", "a2", "a3") + [
     A("l9", "pop", "9", sfx="ding"), A("paquete", "slide-right", "llega", dur=0.6, sfx="whoosh"),
     A("paquete", "bob", amount=0.5), A("paquete", "punch", "certificado", amount=0.2),
     A("lsolo", "pop", "Solo", sfx="pop"), A("dniB", "pop", "ti", sfx="pop"),
     A("chk", "pop", "DNI", sfx="ding"), A("chk", "pulse", amount=0.5)]}},
 {"chapter": 2, "number": "2", "headline": "Sobre dentro de *sobre*",
  "narration": "Dentro: la papeleta va al sobre de votación. Ese sobre, con tu certificado del censo, va a otro dirigido a tu mesa.",
  "illustration": {"svg_file": "sobres_free.svg", "layout": "free", "height": 820, "caption": "Fig. 4 · Dos sobres", "anims": H("paquete", "l9", "dniB", "chk", "lsolo") + [
     A("papeleta", "pop", "papeleta", sfx="papel"), A("lpap", "pop", "papeleta"),
     A("a1", "draw", "va", dur=0.5, sfx="whoosh"), A("sobrev", "pop", "votación", sfx="pop"), A("lvot", "pop", "votación"),
     A("cert", "pop", "certificado", sfx="papel"), A("a3", "draw", "censo", dur=0.4),
     A("sobremesa", "pop", "otro", sfx="pop"), A("a2", "draw", "dirigido", dur=0.5, sfx="whoosh"),
     A("sobremesa", "punch", "mesa", amount=0.2)]}},
 {"chapter": 2, "number": "2", "headline": "Entrégalo *gratis*",
  "narration": "Lo entregas en Correos, certificado y gratis, hasta el 25 de noviembre.",
  "illustration": {"svg_file": "oficina.svg", "caption": "Fig. 5 · Sin franqueo", "anims": H("l19", "lcust", "form", "dni", "sello", "lgratis", "l25") + [
     A("saca", "breathe", amount=0.3),
     A("sobreE", "slide-up", "entregas", dur=0.5, sfx="whoosh"), A("rotulo", "punch", "Correos", amount=0.3),
     A("sello", "pop", "certificado", sfx="sello"), A("lgratis", "pop", "gratis", sfx="ding"),
     A("l25", "pop", "25", sfx="pop"), A("l25", "pulse", amount=0.5)]}},
 {"chapter": 3, "number": "3", "headline": "Bajo *custodia*",
  "narration": "Correos lo guarda bajo custodia hasta el día de la votación.",
  "illustration": {"svg_file": "oficina.svg", "caption": "Fig. 6 · Custodia postal", "anims": H("l19", "l25", "lgratis", "sello", "form", "dni", "lcust") + [
     A("rueda", "wiggle", amount=0.3),
     A("sobreE", "move", "guarda", to=[330, -150], dur=0.8, sfx="whoosh"),
     A("sobreE", "hide", "bajo"), A("caja", "punch", "bajo", amount=0.15),
     A("rotulo", "hide", "custodia"),
     A("camera", "zoom", "custodia", to=[790, 300], amount=1.35, dur=0.7),
     A("lcust", "pop", "custodia", sfx="sello"),
     A("candado", "punch", "votación", amount=0.3)]},
  "mascot": {"trigger": "día", "pose": "think", "note": "Ni yo tengo la llave", "side": "left"}},
 {"chapter": 3, "number": "3", "headline": "Domingo, *9:00*",
  "narration": "El domingo 29, a las nueve, lo lleva a tu mesa electoral.",
  "illustration": {"svg_file": "colegio_full.svg", "layout": "full", "caption": "Fig. 7 · Colegio electoral", "anims": H("t20", "lsin", "voto", "chkc") + [
     A("urnas", "breathe", amount=0.2),
     A("t29", "pop", "domingo", sfx="pop"), A("reloj", "punch", "nueve", amount=0.2), A("thora", "pop", "nueve", sfx="ding"),
     A("saca", "slide-right", "lleva", dur=0.6, sfx="whoosh"), A("saca", "punch", "mesa", amount=0.25),
     A("cartel", "punch", "electoral", amount=0.25)]}},
 {"chapter": 4, "number": "+", "headline": "Sin *abrirlo*",
  "narration": "Al cerrar, el presidente comprueba el censo y mete tu sobre en la urna. Sin abrirlo.",
  "illustration": {"svg_file": "colegio_full.svg", "layout": "full", "caption": "Fig. 8 · LOREG, art. 88", "anims": H("t29", "thora", "voto", "chkc", "lsin", "t20") + [
     A("urnas", "breathe", amount=0.2),
     A("horaria", "move", "cerrar", rotate=330, origin="center", dur=1.0, sfx="chasquido"),
     A("t20", "pop", "presidente", sfx="ding"),
     A("censo", "punch", "comprueba", amount=0.25), A("chkc", "pop", "censo", sfx="ding"),
     A("voto", "pop", "mete", sfx="papel"), A("voto", "move", "urna", to=[0, 42], dur=0.5),
     A("lsin", "pop", "Sin", sfx="sello"), A("lsin", "pulse", amount=0.5)]}},
 {"chapter": 5, "number": "TÚ", "headline": "*Confiesa*",
  "narration": "Síguenos para más trucos. ¿Votarías en pijama desde el sofá?",
  "elements": [{"type": "follow", "trigger": "Síguenos"},
               {"type": "ask", "text": "¿Votarías en *pijama* desde el sofá?", "trigger": "Votarías"}]},
]

g = {
 "topic": "Cómo funciona el voto por correo en las generales del 29 de noviembre de 2026",
 "categoria": "politica",
 "title": "¿Votar por correo es seguro? Así viaja tu voto 🗳️✉️",
 "source": "Fuentes: LOREG (LO 5/1985), arts. 72, 73 y 88 · BOE 6/10/2026 (Real Decreto 806/2026) · Correos y Oficina del Censo Electoral (INE): plazos del voto por correo 29-N",
 "chapters": ["?", "1", "2", "3", "+", "TÚ"],
 "outro_cta": "Todo tiene un truco",
 "cover": {"text": "¿Tu voto *se pierde*?", "scene": 0},
 "publish": {
  "caption": "¿Votas por correo el 29-N? ✉️🗳️ Pídelo en Correos con tu DNI hasta el 19 de noviembre, te llega certificado desde el 9 y lo entregas gratis hasta el 25. El domingo va a tu mesa y entra en la urna sin abrir. Sin posicionarnos: solo explicamos cómo funciona. ¿Votarías en pijama desde el sofá?",
  "description": "Así viaja el voto por correo en las elecciones generales del 29 de noviembre de 2026 (Real Decreto 806/2026, BOE del 6 de octubre). 1) Se solicita en persona en cualquier oficina de Correos con DNI (o por internet con certificado digital o DNIe) hasta el jueves 19 de noviembre. 2) La Oficina del Censo Electoral envía la documentación por correo certificado a partir del 9 de noviembre y solo se entrega al interesado, acreditando su identidad. 3) La papeleta va en el sobre de votación; ese sobre, junto con el certificado de inscripción en el censo, va en un segundo sobre dirigido a la mesa. 4) Se entrega en Correos, por correo certificado y sin franqueo, hasta el 25 de noviembre. 5) Correos lo custodia hasta el día de la votación y lo lleva a la mesa a las nueve. 6) Al terminar la votación, el presidente comprueba que el elector está en el censo e introduce el sobre de votación en la urna, sin abrirlo. Sin posicionarnos: solo explicamos cómo funciona. Fuentes: LOREG, arts. 72, 73 y 88; BOE (Real Decreto 806/2026); Correos y Oficina del Censo Electoral.",
  "hashtags": ["votoporcorreo", "elecciones", "eleccionesgenerales", "29N", "leyelectoral", "politica", "aprendeentiktok", "eltrucoes"]
 },
 "scenes": scenes,
}
# comprobaciones: palabras y triggers
tot = 0
for i, s in enumerate(scenes):
    words = re.findall(r"[\wÁÉÍÓÚÑáéíóúñü0-9-]+", s["narration"])
    tot += len(words)
    low = [w.lower() for w in words]
    trigs = [a.get("trigger") for a in s.get("illustration", {}).get("anims", []) if a.get("trigger")] + [e.get("trigger") for e in s.get("elements", [])]
    if s.get("mascot"): trigs.append(s["mascot"]["trigger"])
    bad = [t for t in trigs if t.lower() not in low]
    print(i + 1, len(words), "BAD:" if bad else "", bad)
print("total", tot)
json.dump(g, open(D + "/guion.json", "w"), ensure_ascii=False, indent=2)

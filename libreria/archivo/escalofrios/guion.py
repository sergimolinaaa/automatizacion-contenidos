import json, re, unicodedata

D = "/home/user/automatizacion-contenidos/content/lote6-02-escalofrios"


def A(t, e, trig=None, **k):
    a = {"target": t, "effect": e}
    if trig:
        a["trigger"] = trig
    a.update(k)
    return a


def H(*ids):
    return [A(i, "hide") for i in ids]


def zoom(trig, to, amount, dur=0.8):
    a = {"target": "camera", "effect": "zoom", "to": to, "amount": amount, "dur": dur}
    if trig:
        a["trigger"] = trig
    return a


scenes = [
    {"chapter": 0, "headline": "¿Y los *escalofríos*?",
     "narration": "Nos preguntáis: ¿y los escalofríos? Te explicamos el truco.",
     "illustration": {"svg_file": "comentario_full.svg", "layout": "full", "caption": "Fig. 1 · Vuestra pregunta",
                      "anims": [A("snowtop", "drift", amount=0.6), A("snowbot", "float", amount=0.5),
                                A("corazon", "pulse", amount=0.6),
                                A("lpregunta", "pop", "preguntáis", sfx="pop"),
                                A("temblor", "fade", "escalofríos", dur=0.2, sfx="sorpresa"),
                                A("temblor", "shake", "escalofríos", amount=1.2),
                                A("card", "punch", "escalofríos", amount=0.25),
                                A("respuesta", "slide-left", "explicamos", sfx="whoosh"),
                                A("corazon", "punch", "truco", amount=0.8)]}},
    {"chapter": 0, "signature": True, "headline": "El truco es…", "narration": "El truco es…"},
    {"chapter": 1, "number": "1", "headline": "Un *termostato* en la cabeza",
     "narration": "En tu cerebro, el hipotálamo funciona como un termostato: quiere tenerte a unos 37 grados.",
     "illustration": {"svg_file": "cerebro.svg", "caption": "Fig. 2 · El hipotálamo",
                      "anims": H("cascos", "notas", "dopa", "ldopa", "virus", "l39", "orden") + [
                          A("hipo", "pulse", amount=0.8),
                          A("cerebro", "punch", "cerebro", amount=0.2, sfx="pop"),
                          zoom("hipotálamo", [480, 360], 1.5),
                          A("hipo", "punch", "hipotálamo", amount=1.2, sfx="brillo"),
                          zoom("funciona", [500, 350], 1, 0.6),
                          A("lhipo", "pop", "funciona", sfx="rotulador"),
                          A("guia", "draw", "termostato", dur=0.5),
                          A("termo", "punch", "termostato", amount=0.4, sfx="ding"),
                          A("aguja", "wiggle", "quiere", amount=0.4),
                          A("l37", "pop", "37", sfx="pop")]}},
    {"chapter": 1, "number": "1", "headline": "Músculos *a tope*",
     "narration": "Si te enfrías, da la orden: tus músculos se contraen y relajan sin parar, muy rápido.",
     "illustration": {"svg_file": "persona_free.svg", "layout": "free", "height": 860, "caption": "Fig. 3 · La orden de tiritar",
                      "anims": H("calor", "lcalor", "ltiritar") + [
                          A("nieve", "drift", amount=0.6), A("vaho", "float", amount=0.5),
                          A("temblor", "fade", "enfrías", dur=0.2, sfx="whoosh"),
                          A("persona", "shake", "orden", amount=0.8),
                          A("boca", "shake", "orden", amount=1.2),
                          A("lineas", "pop", "músculos", sfx="pop"),
                          A("lmusculo", "pop", "músculos"),
                          zoom("contraen", [800, 600], 1.5),
                          A("relajado", "hide", "contraen"),
                          A("contraido", "fade", "contraen", dur=0.15, sfx="chasquido"),
                          A("tira", "pop", "contraen"),
                          A("contraido", "shake", "parar", amount=1.6),
                          zoom("rápido", [500, 550], 1, 0.6)]}},
    {"chapter": 2, "number": "2", "headline": "Tiritar *calienta*",
     "narration": "Eso es tiritar: un movimiento que no te lleva a ningún sitio, pero fabrica calor.",
     "illustration": {"svg_file": "persona_free.svg", "layout": "free", "height": 860, "caption": "Fig. 4 · Calor de músculo",
                      "anims": H("relajado") + [
                          A("persona", "shake", amount=1.0), A("boca", "shake", amount=1.4),
                          A("temblor", "shake", amount=1.0), A("contraido", "shake", amount=1.6),
                          A("nieve", "drift", amount=0.6),
                          A("ltiritar", "pop", "tiritar", sfx="pop"),
                          A("vaho", "float", amount=0.5),
                          A("persona", "punch", "movimiento", amount=0.15),
                          A("calor", "draw", "calor", dur=0.6, sfx="brillo"),
                          A("calor", "float", "calor", amount=0.5),
                          A("lcalor", "pop", "calor")]},
},
    {"chapter": 2, "number": "2", "headline": "¿Y con *fiebre*?",
     "narration": "¿Y con fiebre? Tus defensas suben el termostato, por ejemplo a 39 grados.",
     "illustration": {"svg_file": "cerebro.svg", "caption": "Fig. 5 · Termostato con fiebre",
                      "anims": H("cascos", "notas", "dopa", "ldopa", "lhipo", "orden") + [
                          A("virus", "pop", "fiebre", sfx="pop"),
                          A("virus", "float", "fiebre", amount=0.6),
                          A("hipo", "pulse", "defensas", amount=1.2),
                          A("guia", "draw", "defensas", dur=0.5),
                          A("termo", "punch", "termostato", amount=0.4),
                          zoom("suben", [840, 300], 1.4),
                          A("aguja", "move", "suben", rotate=90, origin="center", dur=1.2, sfx="whoosh"),
                          A("l37", "hide", "39"),
                          A("l39", "pop", "39", sfx="ding")]},
     "elements": [{"type": "tag", "text": "Pirógenos", "tone": "hot", "trigger": "defensas"}]},
    {"chapter": 2, "number": "2", "headline": "Fiebre… y *tiritas*",
     "narration": "Tu cuerpo sigue a 37, así que el cerebro cree que tienes frío. Por eso tiritas hasta llegar a 39.",
     "illustration": {"svg_file": "fiebre_full.svg", "layout": "full", "caption": "Fig. 6 · Fiebre que sube",
                      "anims": [
                          A("lfiebre", "pop", "cuerpo", sfx="pop"),
                          zoom("37", [800, 860], 1.25),
                          A("t37", "punch", "37", amount=0.5, sfx="ding"),
                          zoom("cerebro", [540, 760], 1, 0.6),
                          A("bocadillo", "pop", "frío", sfx="sorpresa"),
                          A("bocadillo", "float", "frío", amount=0.4),
                          A("temblor", "fade", "tiritas", dur=0.2),
                          A("temblor", "shake", "tiritas", amount=1.2),
                          A("persona", "shake", "tiritas", amount=1.0),
                          A("t37", "hide", "39"),
                          A("t39", "fade", "39", dur=0.2, sfx="ding"),
                          A("termometro", "punch", "39", amount=0.4)]}},
    {"chapter": 3, "number": "3", "headline": "Primo de la *piel de gallina*",
     "narration": "Es el mismo modo frío de la piel de gallina: tu cuerpo intenta guardar calor.",
     "illustration": {"svg_file": "brazo.svg", "caption": "Fig. 7 · Mismo modo frío",
                      "anims": H("notes") + [
                          A("snow1", "float", amount=0.6), A("snow2", "drift", amount=0.5),
                          A("snow1", "punch", "frío", amount=1.2, sfx="whoosh"),
                          A("hairflat", "hide", "gallina"),
                          A("hairup", "fade", "gallina", dur=0.3),
                          A("bumps", "fade", "gallina", dur=0.3, sfx="brillo"),
                          A("lgallina", "pop", "gallina"),
                          A("lupa", "pop", "cuerpo", sfx="pop"),
                          zoom("guardar", [690, 230], 1.4),
                          A("bumps", "punch", "calor", amount=0.3)]},
     "mascot": {"trigger": "calor", "pose": "point", "note": "Mismo botón, otro efecto", "side": "right"}},
    {"chapter": 4, "number": "+", "headline": "Escalofrío *musical*",
     "narration": "¿Y el escalofrío con tu canción favorita? Eso es otra cosa: se llama frisson.",
     "illustration": {"svg_file": "brazo_full.svg", "layout": "full", "caption": "Fig. 8 · Frisson",
                      "anims": H("snow1", "snow2", "snowtop", "snowbot", "lgallina") + [
                          A("notes", "bob", amount=0.5),
                          A("notes", "punch", "canción", amount=1.0, sfx="ding"),
                          A("notes", "wiggle", "favorita", amount=0.6),
                          A("hairflat", "hide", "frisson"),
                          A("hairup", "fade", "frisson", dur=0.2),
                          A("bumps", "fade", "frisson", dur=0.2, sfx="brillo"),
                          A("lupa", "pop", "frisson")]},
     "elements": [{"type": "tag", "text": "Frisson", "tone": "accent", "trigger": "cosa"}]},
    {"chapter": 4, "number": "+", "headline": "Chute de *dopamina*",
     "narration": "En 2011, en Montreal, vieron que en ese momento el cerebro libera dopamina, la de la recompensa.",
     "illustration": {"svg_file": "cerebro.svg", "caption": "Fig. 9 · Música y dopamina",
                      "anims": H("virus", "l39", "l37", "termo", "aguja", "guia", "lhipo", "orden", "hipo") + [
                          A("notas", "bob", amount=0.5), A("cascos", "breathe", amount=0.6),
                          A("notas", "punch", "Montreal", amount=0.6),
                          A("cerebro", "punch", "cerebro", amount=0.2, sfx="pop"),
                          zoom("libera", [470, 290], 1.4),
                          A("dopa", "pop", "dopamina", sfx="brillo"),
                          A("dopa", "pulse", "dopamina", amount=1.2),
                          zoom("recompensa", [500, 350], 1, 0.6),
                          A("ldopa", "pop", "recompensa", sfx="rotulador")]},
     "elements": [{"type": "tag", "text": "McGill · 2011", "tone": "ink", "trigger": "Montreal"}]},
    {"chapter": 5, "number": "TÚ", "headline": "Te *toca*",
     "narration": "Síguenos para más trucos. ¿Qué rareza de tu cuerpo te explicamos ahora?",
     "elements": [{"type": "follow", "trigger": "Síguenos"},
                  {"type": "ask", "text": "¿Qué *rareza* de tu cuerpo te explicamos ahora?", "trigger": "Qué"}]},
]

g = {
    "topic": "Por qué tiritamos y qué son los escalofríos (frío, fiebre y música)",
    "categoria": "cuerpo",
    "title": "¿Y los escalofríos? Por qué tiritas, incluso con fiebre 🥶",
    "source": "Fuentes: fisiología de la termorregulación y la fiebre (hipotálamo, prostaglandina E2) · Salimpoor et al., Nature Neuroscience (2011), Universidad McGill",
    "chapters": ["?", "1", "2", "3", "+", "TÚ"],
    "outro_cta": "Todo tiene un truco",
    "cover": {"text": "¿Por qué *tiritamos*?", "badge": "RESPONDEMOS EN COMENTARIOS", "scene": 3},
    "publish": {
        "caption": "Respondemos a una pregunta de los comentarios del vídeo de la piel de gallina: ¿y los escalofríos? 🥶 Tu hipotálamo es un termostato: si te enfrías, tus músculos tiritan para fabricar calor. Con fiebre sube el termostato, y por eso tiritas aunque estés caliente. ¿Qué rareza de tu cuerpo te explicamos ahora? Déjala en comentarios.",
        "description": "Respondemos a una pregunta que nos dejasteis en los comentarios del vídeo de la piel de gallina: ¿y los escalofríos? El hipotálamo funciona como un termostato que intenta mantenerte a unos 37 °C. Cuando te enfrías, ordena a los músculos contraerse y relajarse muy rápido: eso es tiritar, y ese movimiento no hace trabajo útil, así que su energía sale como calor. Con fiebre, las sustancias que liberan tus defensas (pirógenos, a través de la prostaglandina E2) suben el punto de consigna del hipotálamo: el cuerpo, aún a 37, se siente frío y tirita hasta alcanzar la nueva temperatura. Es el mismo «modo frío» que pone la piel de gallina. El escalofrío con la música es otra cosa, el frisson: en 2011, un equipo de la Universidad McGill (Montreal) vio que en esos picos de emoción el cerebro libera dopamina en el estriado. Fuentes: fisiología de la termorregulación y la fiebre; Salimpoor et al., Nature Neuroscience (2011). ¿Qué rareza de tu cuerpo te explicamos ahora? Déjala en comentarios.",
        "hashtags": ["escalofrios", "fiebre", "cuerpohumano", "ciencia", "curiosidades", "biologia", "eltrucoes"]},
    "scenes": scenes,
}


def norm(w):
    w = unicodedata.normalize("NFD", w.lower())
    return re.sub(r"[^\w]", "", "".join(c for c in w if unicodedata.category(c) != "Mn"))


tot = 0
for i, s in enumerate(scenes):
    words = s["narration"].split()
    tot += len(words)
    keys = {norm(w) for w in words}
    trigs = [a.get("trigger") for a in s.get("illustration", {}).get("anims", [])] + [e.get("trigger") for e in s.get("elements", [])] + [s.get("mascot", {}).get("trigger")]
    for t in trigs:
        if t and norm(t) not in keys:
            print("TRIGGER MALO", i, t)
    if "illustration" in s:
        svg = open(f"{D}/{s['illustration']['svg_file']}").read()
        ids = set(re.findall(r'id="([^"]+)"', svg))
        for a in s["illustration"]["anims"]:
            if a["target"] != "camera" and a["target"] not in ids:
                print("ID MALO", i, a["target"])
        print(i, len(words), len(s["illustration"]["anims"]), s["illustration"].get("layout", "panel"))
print("palabras", tot)
json.dump(g, open(f"{D}/guion.json", "w"), ensure_ascii=False, indent=2)

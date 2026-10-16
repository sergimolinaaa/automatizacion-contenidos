import json, shutil, os, re
D = "/home/user/automatizacion-contenidos/content/lote7-01-hielo-cruje"
os.makedirs(D, exist_ok=True)
for fn in ("vaso_full.svg", "termos.svg", "corte_free.svg", "micro.svg"):
    shutil.copy(fn, D)


def A(target, effect, trigger=None, **kw):
    a = {"target": target, "effect": effect}
    if trigger:
        a["trigger"] = trigger
    a.update(kw)
    return a


H = lambda *ids: [A(i, "hide") for i in ids]
CORTE_ALL = ["gotas", "calor", "caracol", "lfuera", "ldentro", "crecer", "tension", "lcrecer", "lnodeja", "lchoque",
             "g1", "g2", "g3", "g4", "crac1", "crac2", "lfragil"]
H_CORTE = lambda *keep: H(*[i for i in CORTE_ALL if i not in keep])

scenes = [
 {"chapter": 0, "headline": "¿Y ese *crac*?",
  "narration": "¿Has oído cómo cruje el hielo al echarle la bebida? Tiene explicación.",
  "illustration": {"svg_file": "vaso_full.svg", "layout": "full", "caption": "Fig. 1 · Hielo y refresco", "anims":
     H("ondas", "ondasW", "oreja", "lflota", "crono", "aguja", "lseg") + [
     A("burbujas", "float", amount=0.6), A("botella", "wiggle", amount=0.2, origin="right"),
     A("chorro", "flow", amount=1.2),
     A("gotas", "pop", "oído", sfx="splash"), A("gotas", "bob", "oído", amount=0.5),
     A("grieta1", "draw", "cruje", dur=0.35), A("crac1", "pop", "cruje", sfx="chasquido"),
     A("cubo1", "shake", "hielo", amount=0.6),
     A("grieta2", "draw", "echarle", dur=0.35), A("crac2", "pop", "echarle", sfx="chasquido"),
     A("crac1", "wiggle", "bebida", amount=0.5),
     A("grieta1b", "draw", "Tiene", dur=0.3), A("crac3", "pop", "Tiene", sfx="chasquido"),
     A("grieta2b", "draw", "explicación", dur=0.3), A("crac2", "wiggle", "explicación", amount=0.5)]}},
 {"chapter": 1, "number": "1", "headline": "De *18 bajo cero*",
  "narration": "El hielo sale del congelador a unos 18 grados bajo cero. La bebida está mucho más templada.",
  "illustration": {"svg_file": "termos.svg", "caption": "Fig. 2 · Frío contra templado", "anims": [
     A("vaho", "float", amount=0.6),
     A("bandeja", "move", "sale", to=[40, 0], dur=0.6, sfx="whoosh"),
     A("congelador", "punch", "congelador", amount=0.15),
     A("fillF", "grow", "18", sfx="tic"), A("lfrio", "pop", "bajo", sfx="ding"),
     A("termoF", "shake", "cero", amount=0.4),
     A("bebida", "slide-left", "bebida", dur=0.5, sfx="whoosh"), A("termoC", "pop", "bebida"),
     A("fillC", "grow", "mucho", sfx="tic"), A("rayo", "pop", "más", sfx="chasquido"),
     A("lcalor", "pop", "templada", sfx="pop"), A("rayo", "pulse", "templada", amount=0.8)]}},
 {"chapter": 1, "number": "1", "headline": "Fuera templado, dentro *helado*",
  "narration": "Al caerle encima, la capa de fuera se calienta de golpe. Pero el centro sigue helado: el calor entra despacio.",
  "illustration": {"svg_file": "corte_free.svg", "layout": "free", "height": 860, "caption": "Fig. 3 · Cubito por dentro", "anims":
     H_CORTE("gotas", "calor", "caracol", "lfuera", "ldentro") + [
     A("gotas", "slide-down", "caerle", dur=0.5, sfx="splash"), A("gotas", "float", "encima", amount=0.5),
     A("capa", "fade", "capa", dur=0.6, sfx="brillo"), A("lfuera", "pop", "calienta", sfx="pop"),
     A("capa", "pulse", "golpe", amount=0.3),
     A("nucleo", "pulse", "centro", amount=0.6), A("ldentro", "pop", "helado", sfx="ding"),
     A("calor", "draw", "calor", dur=0.6, sfx="whoosh"),
     A("caracol", "slide-left", "despacio", dur=0.6, sfx="boing"), A("caracol", "bob", "despacio", amount=0.3)]}},
 {"chapter": 2, "number": "2", "headline": "El hielo *se estira*",
  "narration": "Y el hielo, al calentarse, se estira un poquito: sus moléculas se mueven más y se separan, como gente bailando.",
  "illustration": {"svg_file": "micro.svg", "caption": "Fig. 4 · Moléculas de agua en el hielo", "anims": [
     A("lfrio", "pop", "hielo", sfx="pop"),
     A("lupaC", "pop", "calentarse", sfx="pop"), A("ltemp", "pop", "calentarse"),
     A("separan", "pop", "estira", sfx="whoosh"), A("separan", "pulse", "estira", amount=0.8),
     A("lexag", "pop", "poquito"),
     A("molsC", "shake", "moléculas", amount=0.5), A("lquietas", "pop", "mueven", sfx="pop"),
     A("lseparan", "pop", "separan", sfx="pop"),
     A("notas", "pop", "gente", sfx="ding"), A("notas", "bob", "bailando", amount=0.6)]},
  "mascot": {"trigger": "bailando", "pose": "surprise", "note": "Fiesta en el hielo", "side": "right"}},
 {"chapter": 2, "number": "2", "headline": "Un *tira y afloja*",
  "narration": "La capa de fuera quiere crecer y el centro no la deja. Es un choque térmico: un tira y afloja.",
  "illustration": {"svg_file": "corte_free.svg", "layout": "free", "height": 860, "caption": "Fig. 5 · Choque térmico", "anims":
     H_CORTE("crecer", "tension", "lcrecer", "lnodeja", "lchoque") + [
     A("capa", "pulse", "capa", amount=0.4),
     A("crecer", "pop", "quiere", sfx="whoosh"), A("lcrecer", "pop", "crecer", sfx="pop"),
     A("crecer", "pulse", "crecer", amount=0.7),
     A("nucleo", "punch", "centro", amount=0.4),
     A("tension", "draw", "deja", dur=0.6), A("lnodeja", "pop", "deja", sfx="sello"),
     A("lcrecer", "hide", "choque"), A("lchoque", "pop", "choque", sfx="chasquido"),
     A("tension", "shake", "choque", amount=0.6), A("lnodeja", "punch", "tira", amount=0.3),
     A("lchoque", "punch", "afloja", amount=0.3)]}},
 {"chapter": 3, "number": "3", "headline": "Frágil: *¡crac!*",
  "narration": "Y el hielo es frágil, como el cristal: no se dobla, se rompe. Se abren grietas, y cada una suena: ¡crac!",
  "illustration": {"svg_file": "corte_free.svg", "layout": "free", "height": 860, "caption": "Fig. 6 · Grietas", "anims":
     H_CORTE("g1", "g2", "g3", "g4", "crac1", "crac2", "lfragil") + [
     A("lfragil", "pop", "frágil", sfx="pop"), A("nucleo", "pulse", "cristal", amount=0.4),
     A("lfragil", "punch", "dobla", amount=0.3),
     A("g1", "draw", "rompe", dur=0.4, sfx="chasquido"),
     A("g2", "draw", "abren", dur=0.4, sfx="chasquido"), A("g3", "draw", "grietas", dur=0.4),
     A("g4", "draw", "cada", dur=0.4, sfx="chasquido"),
     A("crac2", "pop", "suena", sfx="pop"), A("crac1", "pop", "crac", sfx="chasquido"),
     A("crac1", "wiggle", "crac", amount=0.6)]}},
 {"chapter": 4, "number": "+", "headline": "Flota y *suena*",
  "narration": "Y lo oyes porque el cubito flota arriba y se agrieta durante segundos.",
  "illustration": {"svg_file": "vaso_full.svg", "layout": "full", "caption": "Fig. 7 · Lo oyes", "anims":
     H("botella", "chorro", "gotas", "crac1", "crac2", "crac3", "grieta1b", "grieta2b") + [
     A("burbujas", "float", amount=0.6),
     A("oreja", "slide-left", "oyes", dur=0.5, sfx="whoosh"),
     A("ondasW", "pop", "porque"), A("ondas", "pop", "porque", sfx="pop"),
     A("ondas", "pulse", "porque", amount=0.6), A("ondasW", "pulse", "porque", amount=0.6),
     A("lflota", "pop", "flota", sfx="pop"), A("cubos", "bob", "flota", amount=0.3),
     A("grieta1b", "draw", "agrieta", dur=0.3, sfx="chasquido"), A("crac3", "pop", "agrieta"),
     A("crono", "pop", "durante", sfx="tic"), A("aguja", "pop", "durante"),
     A("aguja", "spin", "segundos", amount=1.5, origin="bottom"),
     A("lseg", "pop", "segundos", sfx="ding"), A("grieta2b", "draw", "segundos", dur=0.3)]}},
 {"chapter": 5, "headline": "Dudas → *truco*",
  "narration": "Tú traes las dudas y nosotros te damos el truco.",
  "elements": [{"type": "trick", "trigger": "Tú", "reveal_trigger": "nosotros"}]},
 {"chapter": 5, "number": "TÚ", "headline": "*Confiesa*",
  "narration": "Síguenos y las resolvemos. ¿Tu hielo también se queja con el refresco?",
  "elements": [{"type": "follow", "trigger": "Síguenos"},
               {"type": "ask", "text": "¿Tu hielo también se *queja* con el refresco?", "trigger": "Tu"}]},
]

SRC = ("Fuentes: The Conversation, serie Curious Kids (Daniel Southam, Universidad Curtin) · ScienceABC · Mental Floss "
       "· Engineering ToolBox y Wikipedia (dilatación térmica del hielo y del vidrio) · IDAE y fabricantes (congelador a 18 °C bajo cero)")
guion = {
    "topic": "Por qué cruje el hielo al echarle la bebida (choque térmico)",
    "categoria": "fisica",
    "title": "¿Por qué cruje el hielo al echarle la bebida? 🧊",
    "source": SRC,
    "chapters": ["?", "1", "2", "3", "+", "TÚ"],
    "outro_cta": "Todo tiene un truco",
    "cover": {"text": "Por qué *cruje* el hielo", "scene": 0},
    "publish": {
        "at": "2026-10-17T14:00:00+02:00",
        "caption": ("¿Por qué cruje el hielo al echarle la bebida? 🧊 El cubito sale del congelador a unos 18 °C bajo cero y, al mojarse, "
                    "su capa de fuera se calienta y se dilata mientras el centro sigue helado. Ese choque térmico lo agrieta, y cada grieta suena; "
                    "lo oyes tan bien porque el cubito flota arriba y se va rompiendo durante segundos (The Conversation, ScienceABC). "
                    "¿Qué otro ruido de tu cocina te explicamos?"),
        "description": ("¿Por qué cruje el hielo al echarle la bebida? El cubito sale del congelador a unos 18 °C bajo cero (IDAE) y, al caerle encima "
                        "la bebida, su capa de fuera se calienta y se dilata, mientras el centro sigue helado porque el calor avanza despacio dentro del hielo. "
                        "Ese choque térmico crea tensiones que el hielo, frágil como el cristal, no aguanta: se abren grietas y cada una suena, y como el cubito "
                        "flota arriba y se agrieta durante segundos, lo oyes perfectamente (The Conversation, Daniel Southam, Universidad Curtin; ScienceABC; Mental Floss). "
                        "Dato: por cada grado, el hielo se dilata más de cinco veces que el vidrio de una ventana (Engineering ToolBox; Wikipedia, dilatación térmica). "
                        "¿Qué otro ruido de tu cocina quieres que te expliquemos?"),
        "hashtags": ["hielo", "fisica", "cienciaencasa", "curiosidades"],
    },
    "scenes": scenes,
}
txt = json.dumps(guion, ensure_ascii=False, indent=2)
open(D + "/guion.json", "w").write(txt + "\n")

# comprobaciones
nw = sum(len(s["narration"].split()) for s in scenes)
print("palabras:", nw)
for k in ("title", "source", "caption", "description"):
    pass
allt = json.dumps(guion, ensure_ascii=False)
for ch in ("—", "–", " - "):
    if ch in allt:
        print("GUION encontrado:", repr(ch))
for s in scenes:
    texts = [s["headline"], s["narration"]] + [e.get("text", "") for e in s.get("elements", [])]
    if any("-" in t for t in texts):
        print("guion en escena", s["headline"])
import unicodedata
def norm(w):
    return re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFKD", w.lower()).encode("ascii", "ignore").decode())
for i, s in enumerate(scenes):
    keys = [norm(w) for w in s["narration"].split()]
    trigs = [a.get("trigger") for a in s.get("illustration", {}).get("anims", [])] + [e.get("trigger") for e in s.get("elements", [])] + [s.get("mascot", {}).get("trigger")]
    for t in trigs:
        if t and not any(k.startswith(norm(t)) for k in keys):
            print("trigger no encontrado", i, t)
print("ok")

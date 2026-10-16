import json
from pathlib import Path

OUT = Path("/home/user/automatizacion-contenidos/content/lote2-05-geiser/guion.json")
old = json.loads(OUT.read_text(encoding="utf-8"))


def A(target, effect, trigger=None, **kw):
    a = {"target": target, "effect": effect}
    if trigger:
        a["trigger"] = trigger
    a.update(kw)
    return a


def cam(x, y, amount, trigger=None, dur=0.8):
    a = {"target": "camera", "effect": "zoom", "to": [x, y], "amount": amount, "dur": dur}
    if trigger:
        a["trigger"] = trigger
    return a


land_loops = [A("poolfog", "drift", amount=0.6), A("bison", "breathe", amount=0.6), A("people", "bob", amount=0.15)]
corte_hide = ["jet", "boil", "vapor", "spill", "lvapor"]

scenes = [
    {"chapter": 0, "headline": "La Tierra *escupe agua*",
     "narration": "Hay sitios donde el suelo dispara agua hirviendo hacia el cielo.",
     "illustration": {"svg_file": "escena.svg", "caption": "Fig. 1 · Géiser", "anims": land_loops + [
         A("ruler", "hide"), A("lalt", "hide"), A("linterval", "hide"), A("lyellow", "hide"),
         A("puff", "float", amount=0.6),
         cam(520, 440, 1.6),
         A("bison", "punch", "suelo", amount=0.5),
         A("puff", "hide", "dispara"),
         A("jet", "grow", "dispara", sfx="chorro"), A("steam", "fade", "dispara", dur=0.9), A("steam", "drift", "dispara", amount=0.8),
         A("runoff", "flow", "dispara", amount=1.2),
         cam(500, 350, 1, "dispara", dur=0.9),
         A("lhot", "pop", "hirviendo", sfx="pop"),
         A("jet", "punch", "cielo", amount=0.5)]}},
    {"chapter": 0, "signature": True, "headline": "El truco es…", "narration": "El truco es…"},
    {"chapter": 1, "number": "1", "headline": "Una olla *bajo tierra*",
     "narration": "Bajo el géiser hay una cueva llena de agua, unida a la superficie por un tubo estrecho.",
     "illustration": {"svg_file": "corte.svg", "caption": "Fig. 2 · Por dentro", "anims": [A(t, "hide") for t in corte_hide] + [
         A("infil", "hide"), A("rain", "hide"), A("heat", "hide"), A("llluvia", "hide"), A("lmagma", "hide"),
         A("bubbles", "float", amount=0.4),
         cam(480, 460, 1.4, "cueva"), A("lcam", "pop", "cueva", sfx="pop"),
         A("chamber", "punch", "llena", amount=0.5),
         cam(520, 300, 1.3, "superficie"),
         A("ltubo", "pop", "tubo"), A("chamber", "punch", "estrecho", amount=0.3)]}},
    {"chapter": 1, "number": "1", "headline": "Lluvia *y fuego*",
     "narration": "La lluvia se filtra hasta allí… y el magma calienta la roca que la rodea.",
     "illustration": {"svg_file": "corte.svg", "caption": "Fig. 3 · Agua y calor", "anims": [A(t, "hide") for t in corte_hide] + [
         A("ltubo", "hide"), A("lcam", "hide"), A("heat", "hide"),
         A("bubbles", "float", amount=0.4),
         A("rain", "pop", "lluvia", sfx="burbujas"), A("rain", "float", "lluvia", amount=0.5), A("llluvia", "pop", "lluvia"),
         A("infil", "draw", "filtra", dur=1.1),
         cam(420, 560, 1.5, "magma"), A("lmagma", "pop", "magma"),
         A("heat", "pop", "calienta", sfx="whoosh"), A("heat", "pulse", "calienta", amount=1.0),
         cam(500, 350, 1, "rodea"), A("chamber", "punch", "rodea", amount=0.4)]}},
    {"chapter": 2, "number": "2", "headline": "Aplastada *por el peso*",
     "narration": "Pero el peso del agua de encima la aprieta tanto que no puede hervir.",
     "illustration": {"svg_file": "presion.svg", "caption": "Fig. 4 · Presión", "anims": [
         A("hotter", "hide"), A("lmas", "hide"),
         A("heat", "pulse", amount=0.8), A("parcel", "breathe", amount=0.8),
         A("press1", "pop", "peso", sfx="pop"), A("lpeso", "pop", "peso"),
         A("press2", "pop", "agua"), A("press3", "pop", "encima"),
         cam(420, 520, 1.5, "aprieta"), A("squeeze", "pop", "aprieta", sfx="whoosh"), A("squeeze", "pulse", "aprieta", amount=1.2),
         A("parcel", "punch", "tanto"),
         A("nobubble", "shake", "hervir", amount=0.6), A("lnohierve", "pop", "hervir")]},
     "mascot": {"trigger": "hervir", "pose": "explain", "note": "Como una olla exprés", "side": "right"}},
    {"chapter": 2, "number": "2", "headline": "Más de *100 °C*… y líquida",
     "narration": "Así supera los cien grados… y sigue siendo líquida.",
     "elements": [{"type": "tag", "text": "Agua sobrecalentada", "tone": "hot", "trigger": "líquida"}],
     "illustration": {"svg_file": "presion.svg", "caption": "Fig. 5 · Sobrecalentada", "anims": [
         A("lpeso", "hide"), A("lnohierve", "hide"),
         A("heat", "pulse", amount=0.8), A("parcel", "breathe", amount=0.8), A("squeeze", "pulse", amount=0.6),
         cam(760, 320, 1.4, "supera"), A("hotter", "grow", "supera", dur=1.2, sfx="magia"),
         A("mark100", "punch", "cien"), A("lmas", "pop", "grados"),
         cam(500, 350, 1, "líquida"), A("parcel", "punch", "líquida")]}},
    {"chapter": 3, "number": "3", "headline": "Una *burbuja* lo cambia todo",
     "narration": "Hasta que un poco se convierte en vapor, sube y derrama agua por arriba.",
     "illustration": {"svg_file": "corte.svg", "caption": "Fig. 6 · Rebosa", "anims": [
         A("jet", "hide"), A("boil", "hide"), A("ltubo", "hide"), A("lcam", "hide"), A("llluvia", "hide"), A("lmagma", "hide"),
         A("infil", "hide"), A("rain", "hide"), A("spill", "hide"), A("vapor", "hide"), A("lvapor", "hide"),
         A("heat", "pulse", amount=0.8), A("bubbles", "float", amount=0.4),
         cam(520, 330, 1.35),
         A("vapor", "pop", "vapor", sfx="burbujas"), A("lvapor", "pop", "vapor"),
         A("lvapor", "hide", "sube"), A("vapor", "move", "sube", to=[0, -196], dur=1.3),
         cam(520, 200, 1.6, "derrama"), A("spill", "pop", "derrama", sfx="splash"), A("spill", "flow", "arriba", amount=1.0)]}},
    {"chapter": 3, "number": "3", "headline": "Y de golpe… *¡fuuush!*",
     "narration": "Pesa menos, la presión baja… y toda el agua hierve de golpe. ¡Erupción!",
     "elements": [{"type": "stamp", "text": "¡Fuuush!", "tone": "hot", "trigger": "Erupción", "sfx": "sello"}],
     "illustration": {"svg_file": "corte.svg", "caption": "Fig. 7 · Erupción", "anims": [
         A("vapor", "hide"), A("lvapor", "hide"), A("ltubo", "hide"), A("lcam", "hide"), A("llluvia", "hide"), A("lmagma", "hide"),
         A("infil", "hide"), A("rain", "hide"),
         A("heat", "pulse", amount=1.0), A("bubbles", "float", amount=0.4), A("spill", "flow", amount=1.0),
         cam(520, 300, 1.3),
         A("spill", "punch", "Pesa", amount=0.8), A("chamber", "punch", "presión", amount=0.4),
         cam(520, 440, 1.3, "hierve", dur=0.6), A("boil", "pop", "hierve", sfx="burbujas"), A("boil", "shake", "hierve", amount=0.8),
         A("chamber", "shake", "golpe", amount=0.8),
         cam(500, 350, 1, "Erupción", dur=0.6), A("jet", "grow", "Erupción", sfx="chorro")]}},
    {"chapter": 4, "number": "+", "headline": "Puntual *como un reloj*",
     "narration": "Old Faithful, el más famoso, entra en erupción cada 60 a 110 minutos… y lanza agua hasta 55 metros.",
     "illustration": {"svg_file": "escena.svg", "caption": "Fig. 8 · Old Faithful", "anims": land_loops + [
         A("puff", "hide"), A("lhot", "hide"), A("ruler", "hide"), A("lalt", "hide"), A("linterval", "hide"), A("lyellow", "hide"),
         A("steam", "drift", amount=0.8), A("runoff", "flow", amount=1.2), A("jet", "pulse", amount=0.3),
         A("jet", "punch", "famoso", amount=0.5),
         cam(520, 330, 1.4, "Faithful"), A("jet", "punch", "erupción", amount=0.6), A("people", "punch", "erupción", amount=0.6),
         cam(500, 350, 1, "minutos"), A("linterval", "pop", "minutos", sfx="tic"),
         A("ruler", "draw", "lanza", dur=1.2, sfx="rotulador"),
         A("lalt", "pop", "metros", sfx="ding")]}},
    {"chapter": 4, "number": "+", "headline": "Son *rarísimos*",
     "narration": "Y son rarísimos: la mitad de los géiseres del planeta están en Yellowstone.",
     "elements": [{"type": "stat", "label": "Géiseres del planeta", "value": 50, "from": 0, "unit": " %", "note": "están en Yellowstone", "trigger": "mitad"}],
     "illustration": {"svg_file": "escena.svg", "caption": "Fig. 9 · Un parque único", "anims": land_loops + [
         A("puff", "hide"), A("lhot", "hide"), A("ruler", "hide"), A("lalt", "hide"), A("linterval", "hide"), A("lyellow", "hide"),
         A("steam", "drift", amount=0.8), A("runoff", "flow", amount=1.2), A("jet", "pulse", amount=0.3),
         cam(520, 300, 1.5),
         A("jet", "punch", "rarísimos", amount=0.5),
         cam(500, 350, 1, "planeta", dur=1.0),
         A("lyellow", "pop", "Yellowstone", sfx="ding"), A("bison", "punch", "Yellowstone", amount=0.6)]}},
    {"chapter": 5, "number": "TÚ", "headline": "*Confiesa*",
     "narration": "Síguenos para más trucos. Sinceramente: ¿esperarías hora y media para ver un chorro?",
     "elements": [{"type": "follow", "trigger": "Síguenos"}, {"type": "ask", "text": "¿Esperarías *hora y media* para ver un chorro?", "trigger": "Sinceramente"}]},
]

g = {
    "topic": old["topic"],
    "categoria": old.get("categoria", "tierra"),
    "title": old["title"],
    "source": "Fuentes: USGS · Servicio de Parques Nacionales de EE. UU. (Yellowstone, Old Faithful)",
    "chapters": ["?", "1", "2", "3", "+", "TÚ"],
    "outro_cta": old.get("outro_cta", "La Tierra también tiene trucos"),
    "cover": {"text": old["cover"]["text"], "scene": 0},
    "publish": {
        "caption": "Un chorro de agua hirviendo que sale del suelo como un reloj 💨 El truco: agua a más de 100 °C que no puede hervir… hasta que de golpe sí. ¿Esperarías hora y media para verlo?",
        "description": "Bajo un géiser hay una cueva llena de agua de lluvia, unida a la superficie por un tubo estrecho y calentada por la roca que rodea al magma. El peso del agua de encima sube su punto de ebullición, así que se calienta por encima de 100 °C sin hervir. Cuando un poco se convierte en vapor y derrama agua por arriba, la presión baja y todo hierve de golpe: ¡erupción! Old Faithful, en Yellowstone, entra en erupción cada 60 a 110 minutos y lanza agua hasta 55 metros. Fuentes: USGS; Servicio de Parques Nacionales de EE. UU. (Yellowstone).",
        "hashtags": old["publish"]["hashtags"]},
    "scenes": scenes,
}
OUT.write_text(json.dumps(g, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("palabras:", sum(len(s["narration"].split()) for s in scenes))

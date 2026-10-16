import json
from pathlib import Path

OUT = Path("/home/user/automatizacion-contenidos/examples/pez-arquero/guion.json")
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


escena_loops = [A("rip1", "ripple", phase=0.0), A("rip2", "ripple", phase=0.5), A("rays", "drift", amount=0.5),
                A("leaves", "sway", origin="top", amount=0.35), A("fishbody", "breathe", amount=0.5),
                A("tail", "wiggle", origin="right", amount=0.7), A("pec", "wiggle", origin="right", amount=0.8),
                A("school", "drift", amount=1.2), A("grass", "sway", origin="bottom", amount=0.5)]

scenes = [
    {"chapter": 0, "headline": "Caza *a escupitajos*",
     "narration": "Este pez caza insectos que están fuera del agua… ¡a escupitajos!",
     "illustration": {"svg_file": "escena.svg", "caption": "Fig. 1 · Pez arquero", "anims": escena_loops + [
         A("splash", "hide"), A("rs1", "hide"), A("rs2", "hide"),
         A("bubbles", "float", amount=0.8),
         A("fish", "punch", "pez", amount=0.6), A("lpez", "pop", "pez", sfx="pop"),
         A("lpresa", "pop", "insectos"), cam(760, 200, 1.6, "insectos"),
         A("bug", "punch", "fuera"),
         cam(500, 350, 1, "agua"),
         A("lpresa", "hide", "escupitajos"),
         A("jet", "draw", "escupitajos", dur=0.45, sfx="chorro"), A("drops", "pop", "escupitajos"),
         A("impact", "pop", "escupitajos"), A("bug", "shake", "escupitajos", amount=0.8)]}},
    {"chapter": 0, "signature": True, "headline": "El truco es…", "narration": "El truco es…"},
    {"chapter": 1, "number": "1", "headline": "Una *pistola* en la boca",
     "narration": "Pega la lengua a un surco del paladar y forma un tubo.",
     "illustration": {"svg_file": "boca.svg", "caption": "Fig. 2 · Corte de la cabeza", "anims": [
         A("press", "hide"), A("wflow", "hide"), A("jet", "hide"), A("jdrops", "hide"), A("lbranq", "hide"), A("tubeflow", "hide"),
         A("eye", "blink"), A("gills", "wiggle", amount=0.25), A("cavity", "breathe", amount=0.6),
         A("tongue", "punch", "lengua"), A("llengua", "pop", "lengua", sfx="pop"),
         cam(760, 280, 1.5, "surco"), A("lsurco", "pop", "surco"), A("groove", "pulse", "surco", amount=1.2),
         A("tube", "punch", "forma"),
         cam(500, 350, 1, "tubo"), A("inset", "pop", "tubo", sfx="pop"), A("ltubo", "pop", "tubo")]}},
    {"chapter": 1, "number": "1", "headline": "Aprieta *de golpe*",
     "narration": "Luego aprieta las tapas de las branquias de golpe… y el agua sale disparada.",
     "illustration": {"svg_file": "boca.svg", "caption": "Fig. 3 · Bomba de agua", "anims": [
         A("lsurco", "hide"), A("llengua", "hide"),
         A("eye", "blink"), A("gills", "wiggle", amount=0.25),
         A("press", "pop", "aprieta", sfx="whoosh"), A("press", "pulse", "aprieta", amount=1.2),
         A("gill", "punch", "tapas"), A("lbranq", "pop", "branquias"),
         A("wflow", "draw", "golpe", dur=0.6), A("cavity", "punch", "golpe"),
         cam(840, 270, 1.6, "agua"), A("press", "hide", "agua"), A("tubeflow", "fade", "agua", dur=0.3), A("tubeflow", "flow", "agua", amount=1.6),
         A("jet", "draw", "disparada", dur=0.35, sfx="chorro"), A("jdrops", "pop", "disparada")]},
     "mascot": {"trigger": "disparada", "pose": "explain", "note": "Como apretar una jeringuilla", "side": "right"}},
    {"chapter": 2, "number": "2", "headline": "La presa *no está ahí*",
     "narration": "Pero desde el agua, la presa no está donde parece: la luz se tuerce al cruzar la superficie.",
     "illustration": {"svg_file": "luz.svg", "caption": "Fig. 4 · Refracción", "anims": [
         A("aim", "hide"), A("reticle", "hide"), A("lreal", "hide"),
         A("fishbody", "breathe", amount=0.5), A("tail", "wiggle", origin="right", amount=0.6), A("rays", "drift", amount=0.5),
         A("bug", "punch", "presa"),
         A("ghost", "fade", "parece", dur=0.5, sfx="magia"), A("ghost", "float", "parece", amount=0.6), A("lparece", "pop", "parece"),
         A("ray", "draw", "luz", dur=0.9, sfx="brillo"),
         A("lparece", "hide", "tuerce"),
         cam(520, 300, 1.5, "tuerce"), A("bend", "pop", "tuerce"), A("ltuerce", "pop", "tuerce"),
         A("fake", "fade", "cruzar", dur=0.4), A("normal", "fade", "cruzar", dur=0.4),
         cam(500, 350, 1, "superficie")]}},
    {"chapter": 2, "number": "2", "headline": "Apunta *al sitio real*",
     "narration": "Su cerebro corrige el engaño… y apunta al sitio real.",
     "illustration": {"svg_file": "luz.svg", "caption": "Fig. 5 · Apunta bien", "anims": [
         A("ltuerce", "hide"), A("bend", "hide"), A("reticle", "hide"), A("lreal", "hide"), A("aim", "hide"),
         A("fishbody", "breathe", amount=0.5), A("tail", "wiggle", origin="right", amount=0.6), A("rays", "drift", amount=0.5),
         A("ghost", "float", amount=0.6),
         A("eye", "punch", "cerebro", amount=1.5),
         A("lparece", "hide", "engaño"), A("ghost", "hide", "engaño"), A("fake", "hide", "engaño"),
         A("aim", "fade", "apunta", dur=0.4, sfx="whoosh"),
         cam(760, 210, 1.4, "real"), A("reticle", "pop", "real", sfx="ding"), A("lreal", "pop", "real"), A("bug", "punch", "real")]}},
    {"chapter": 3, "number": "3", "headline": "Una *bala* de agua",
     "narration": "Además, dispara el agua cada vez más rápido: la cola alcanza a la punta y forma una gota gorda justo al llegar.",
     "illustration": {"svg_file": "chorro.svg", "caption": "Fig. 6 · Anatomía de un chorro", "anims": [
         A("impact", "hide"), A("fast", "hide"), A("slow", "hide"), A("lfast", "hide"), A("lslow", "hide"), A("blob", "hide"), A("lgota", "hide"),
         A("rip1", "ripple", phase=0.0), A("rip2", "ripple", phase=0.5), A("fishbody", "breathe", amount=0.5),
         A("stream", "punch", "dispara", amount=0.4),
         A("fast", "pop", "rápido", sfx="whoosh"),
         A("lfast", "pop", "cola"), A("slow", "pop", "punta"), A("lslow", "pop", "punta"),
         A("fast", "move", "alcanza", to=[118, -92], dur=1.0),
         cam(690, 220, 1.5, "gota"), A("blob", "pop", "gota", sfx="pop"), A("blob", "pulse", "gota", amount=0.8),
         A("lgota", "pop", "gorda"),
         A("impact", "pop", "llegar", sfx="splash"), A("bug", "shake", "llegar", amount=0.8)]}},
    {"chapter": 3, "number": "3", "headline": "Y luego… *¡plaf!*",
     "narration": "¡Plaf! El insecto cae… y el pez ya nada hacia donde va a caer.",
     "elements": [{"type": "stamp", "text": "¡Plaf!", "tone": "accent", "trigger": "Plaf", "sfx": "sello"}],
     "illustration": {"svg_file": "escena.svg", "caption": "Fig. 7 · A la cazuela", "anims": escena_loops + [
         A("lpresa", "hide"), A("lpez", "hide"),
         A("bubbles", "float", amount=0.8),
         A("impact", "pop", "Plaf"),
         A("jet", "hide", "cae"), A("drops", "hide", "cae"), A("impact", "hide", "cae"),
         A("bug", "move", "cae", to=[-25, 157], rotate=170, dur=0.8, sfx="whoosh"),
         A("splash", "pop", "pez", sfx="splash"), A("rs1", "fade", "pez", dur=0.2), A("rs1", "ripple", "pez", phase=0.0),
         A("rs2", "fade", "pez", dur=0.2), A("rs2", "ripple", "pez", phase=0.5),
         A("fish", "move", "nada", to=[200, -4], dur=1.1),
         A("bubbles", "move", "nada", to=[200, -4], dur=1.1),
         cam(700, 360, 1.35, "nada", dur=1.0)]}},
    {"chapter": 4, "number": "+", "headline": "Puntería *de 2 metros*",
     "narration": "Sus disparos llegan hasta unos 2 metros. Y aprenden a apuntar mirando a otros.",
     "elements": [
         {"type": "stat", "label": "Alcance del disparo", "value": 2, "from": 0, "unit": " m", "note": "hasta unos dos metros", "trigger": "disparos"},
         {"type": "fact", "label": "Dato", "text": "Aprenden a apuntar observando a otros peces arqueros", "tone": "accent", "trigger": "mirando"}]},
    {"chapter": 4, "number": "+", "headline": "Reconoce *caras*",
     "narration": "Y en un laboratorio aprendieron a reconocer caras humanas: escupían a la que conocían. Acertaban 8 de cada 10 veces.",
     "elements": [
         {"type": "icon", "icon": "eye", "label": "Caras humanas", "trigger": "caras"},
         {"type": "dots", "label": "Aciertos", "filled": 8, "total": 10, "caption": "eligiendo entre 44 caras nuevas", "trigger": "Acertaban"}],
     "mascot": {"trigger": "conocían", "pose": "surprise", "note": "Yo no reconozco ni a mi vecino", "side": "right"}},
    {"chapter": 5, "number": "TÚ", "headline": "*Confiesa*",
     "narration": "¿Tú acertarías a una mosca escupiendo? Te leo.",
     "elements": [{"type": "ask", "text": "¿Tú acertarías a una *mosca* escupiendo?", "trigger": "Tú"}]},
]

g = {
    "topic": old["topic"],
    "categoria": old.get("categoria", "animales"),
    "title": "Este pez caza a escupitajos 🎯",
    "source": "Fuentes: Schuster et al., Current Biology (2006) · Gerullis & Schuster, Current Biology (2014) · Newport et al., Scientific Reports (2016)",
    "chapters": ["?", "1", "2", "3", "+", "TÚ"],
    "outro_cta": old.get("outro_cta", "La naturaleza tiene trucos"),
    "cover": old["cover"],
    "publish": {
        "caption": "Este pez derriba insectos… escupiéndoles agua 💦 Forma una pistola con la lengua, corrige la refracción de la luz y hasta moldea el chorro. ¿Tú acertarías a una mosca escupiendo?",
        "description": "El pez arquero (Toxotes) caza insectos posados fuera del agua disparándoles chorros. Pega la lengua a un surco del paladar para formar un tubo y aprieta las tapas de las branquias de golpe. Corrige la refracción de la luz para apuntar al sitio real, y suelta el agua cada vez más rápido para que el chorro se junte en una gota justo antes del impacto. En el laboratorio incluso aprendieron a reconocer caras humanas. Fuentes: Schuster et al., Current Biology (2006); Gerullis & Schuster, Current Biology (2014); Newport et al., Scientific Reports (2016).",
        "hashtags": ["pezarquero", "peces", "animales", "naturaleza", "ciencia", "curiosidades", "eltrucoes"]},
    "scenes": scenes,
}
OUT.write_text(json.dumps(g, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("palabras:", sum(len(s["narration"].split()) for s in scenes))

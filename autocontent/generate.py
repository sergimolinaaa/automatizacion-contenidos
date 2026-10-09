"""Genera un vídeo nuevo de «El truco es…» de principio a fin con Claude, sin revisión manual.

1. Investigación: Claude busca en la web el tema y devuelve una ficha de datos verificados.
2. Guion: con esa ficha, escribe el guion en el formato del vídeo (escenas, ilustraciones SVG
   con sus animaciones, tarjetas, matraz, encuesta, portada y textos para publicar).
3. Validación: se comprueba todo (SVG bien formado, ids animados que existen, palabras
   disparadoras que aparecen en la narración, longitud...). Si algo falla, Claude lo corrige.
"""

import json
import re
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path

import anthropic

from .config import ROOT
from .timeline import norm

MODEL = "claude-opus-5-5"
FALLBACK_BETA = "server-side-fallback-2026-07-01"
CONTENT_DIR = ROOT / "content"
TOPICS = ROOT / "data" / "temas.json"

ELEMENT_TYPES = {"stat", "fact", "icon", "compare", "dots", "list", "scale", "tag", "stamp", "quiz", "ask", "follow"}
ICONS = {"atom", "earth", "moon", "sun", "paper", "dna", "brain", "drop", "bolt", "rocket", "clock", "eye", "bacteria",
         "star", "ruler", "heart", "fire", "snow", "magnet", "planet", "microscope", "leaf", "bone", "wave"}
EFFECTS = {"pop", "fade", "draw", "grow", "slide-left", "slide-right", "slide-up", "slide-down", "float", "bob", "sway",
           "spin", "pulse", "shake", "wiggle", "flow", "blink", "move", "hide", "punch",
           "ripple", "breathe", "drift"}
SFX = {"whoosh", "barrido", "pop", "papel", "ding", "sorpresa", "sello", "chasquido", "chorro", "burbujas", "splash",
       "tic", "magia", "boing", "rotulador", "brillo", "none"}
POSES = {"idle", "point", "wave", "think", "surprise", "explain", "cheer"}
SIGNATURE_LINE = "El truco es…"


def _client() -> anthropic.Anthropic:
    return anthropic.Anthropic()


def _text(msg) -> str:
    return "".join(b.text for b in msg.content if b.type == "text")


def _check_stop(msg) -> None:
    if msg.stop_reason == "refusal":
        raise RuntimeError(f"Claude rechazó la petición: {msg.stop_details}")
    if msg.stop_reason == "max_tokens":
        raise RuntimeError("La respuesta se cortó por max_tokens")


# ------------------------------------------------------------------ 1. tema

CATEGORY_ORDER = ["psicologia", "animales", "objetos", "fisica", "plantas", "cuerpo", "cocina", "tierra", "politica"]


def _last_category() -> str | None:
    scripts = sorted(CONTENT_DIR.glob("*/guion.json"), key=lambda p: p.stat().st_mtime) if CONTENT_DIR.exists() else []
    for p in reversed(scripts):
        cat = json.loads(p.read_text(encoding="utf-8")).get("categoria")
        if cat:
            return cat
    return None


def pick_topic() -> dict:
    """Siguiente tema pendiente, rotando de categoría respecto al último vídeo."""
    topics = json.loads(TOPICS.read_text(encoding="utf-8"))
    pending = [t for t in topics if not t.get("hecho")]
    urgent = [t for t in pending if t.get("prioridad")]
    if urgent:
        return urgent[0]
    if not pending:
        return new_topic(topics)
    last = _last_category()
    start = (CATEGORY_ORDER.index(last) + 1) if last in CATEGORY_ORDER else 0
    for k in range(len(CATEGORY_ORDER)):
        cat = CATEGORY_ORDER[(start + k) % len(CATEGORY_ORDER)]
        for t in pending:
            if t.get("categoria") == cat:
                return t
    return pending[0]


def new_topic(existing: list[dict]) -> dict:
    """Si se acaba el banco, Claude propone un tema nuevo que no se repita."""
    used = "\n".join(f"- {t['tema']}" for t in existing)
    msg = _client().beta.messages.create(
        model=MODEL,
        max_tokens=2000,
        output_config={"effort": "medium"},
        betas=[FALLBACK_BETA],
        fallbacks="default",
        messages=[{"role": "user", "content": (
            "Propón UN tema nuevo para «El truco es…», una cuenta de vídeos cortos que muestra algo que parece magia "
            "(ciencia, cuerpo, psicología, objetos, cocina o reglas de la política actual) y explica su truco. Debe ser visual, sorprendente, "
            "verificable y fácil de ilustrar. No repitas ninguno de estos:\n" + used +
            "\n\nResponde solo con una línea: el tema.")}],
    )
    _check_stop(msg)
    tema = _text(msg).strip().strip('"').splitlines()[0]
    existing.append({"tema": tema, "categoria": "nuevo"})
    TOPICS.write_text(json.dumps(existing, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return existing[-1]


def mark_done(topic: dict) -> None:
    topics = json.loads(TOPICS.read_text(encoding="utf-8"))
    for t in topics:
        if t["tema"] == topic["tema"]:
            t["hecho"] = True
    TOPICS.write_text(json.dumps(topics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# ------------------------------------------------------------------ 2. investigación

RESEARCH_PROMPT = """Investiga este tema para un vídeo corto de divulgación en español: «{tema}».
Pista inicial (puede estar incompleta o equivocada, compruébala): {pista}

Busca en fuentes fiables (artículos científicos, universidades, museos, enciclopedias) y devuelve una FICHA con:
1. Qué hace el protagonista (lo que parece magia), en 1-2 frases.
2. El truco: cómo funciona, paso a paso, con el mecanismo real.
3. 3-6 datos concretos y sorprendentes (cifras con unidades) que puedas respaldar, cada uno con su fuente.
4. 1-2 datos extra curiosos para un capítulo final.
5. Errores o mitos frecuentes sobre el tema que NO hay que repetir.
6. Fuente principal en formato corto (p. ej. «Fuente: Autor et al., Revista (año)»).
Si un dato no está bien respaldado, márcalo como dudoso. Escribe en español."""


def research(topic: dict) -> str:
    client = _client()
    messages = [{"role": "user", "content": RESEARCH_PROMPT.format(tema=topic["tema"], pista=topic.get("pista", "(ninguna)"))}]
    for _ in range(6):
        msg = client.beta.messages.create(
            model=MODEL,
            max_tokens=16000,
            output_config={"effort": "high"},
            tools=[{"type": "web_search_20260209", "name": "web_search", "max_uses": 8}],
            messages=messages,
            betas=[FALLBACK_BETA],
            fallbacks="default",
        )
        if msg.stop_reason != "pause_turn":
            break
        messages.append({"role": "assistant", "content": msg.content})
    _check_stop(msg)
    return _text(msg)


# ------------------------------------------------------------------ 3. guion

def _example() -> str:
    ex = ROOT / "content" / "lote3-01-zapatero"
    script = json.loads((ex / "guion.json").read_text(encoding="utf-8"))
    svgs = {p.stem: p.read_text(encoding="utf-8") for p in ex.glob("*.svg")}
    for sc in script["scenes"]:
        ill = sc.get("illustration")
        if ill and "svg_file" in ill:
            ill["svg"] = Path(ill.pop("svg_file")).stem
    script["svgs"] = svgs
    return json.dumps(script, ensure_ascii=False, indent=1)


SYSTEM = """Eres el guionista, ilustrador y animador de «El truco es…», una cuenta de vídeos verticales (TikTok, Reels, Shorts)
en español de España. Cada vídeo enseña algo que parece magia y luego cuenta su truco: naturaleza, animales, física, química de la cocina,
psicología y experimentos famosos, cuerpo humano u objetos cotidianos con un diseño ingenioso. El gancho es propio (nunca copiado).
POLÍTICA ACTUAL: también el truco de las reglas detrás de la noticia (cómo se reparten escaños, por qué la fecha de las elecciones,
qué es un decreto ley...). NEUTRALIDAD TOTAL: explica el mecanismo con fuentes oficiales (Constitución, LOREG, BOE), sin opinar,
sin favorecer ni ridiculizar a ningún partido o persona, sin caricaturas de políticos reales; en ejemplos numéricos usa partidos
ficticios de colores. Fechas y cifras de actualidad, comprobadas el mismo día.
Tono: cercano, con chispa y humor suave; frases cortas que se entienden a la primera; nada de relleno ni clickbait falso.
NUNCA inventes datos: usa solo los de la ficha de investigación; si un dato está marcado como dudoso, no lo uses.

ESTRUCTURA (unos 40-55 segundos, 130-175 palabras de narración en total, 9-12 escenas cortas de 1-2 frases: ritmo rápido):
- Escena 0, capítulo 0 "?": GANCHO. Lo increíble en una frase (máx. 12 palabras). Con ilustración.
- Escena 1, capítulo 0: FIRMA (rápida). {"chapter": 0, "signature": true, "headline": "El truco es…", "narration": "El truco es…"}
- Capítulos "1", "2", "3": el truco explicado paso a paso (1-2 escenas por capítulo). Usa ilustraciones de detalle.
- Capítulo "+": 1-2 datos extra sorprendentes.
- Capítulo "TÚ" (escena final, unos 4-5 s): primero la llamada a seguir y luego UNA pregunta corta (máx. 12 palabras) sobre
  el tema del vídeo, con gracia o un punto de humor, que den ganas de contestar (nada de encuestas genéricas).
  narration = "Síguenos para más trucos. <pregunta>"; headline de 1-2 palabras ("*Confiesa*", "Te *toca*"...);
  elements = [{"type":"follow","trigger":"Síguenos"}, {"type":"ask","text":"<pregunta con *palabra clave*>","trigger":<1ª palabra de la pregunta>}].
  Ejemplos de tono: "¿Qué superpoder animal te pedirías tú?", "Sinceramente: ¿tú te habrías hundido?".
chapters siempre = ["?", "1", "2", "3", "+", "TÚ"]. Las escenas de capítulos numerados llevan "number" igual al capítulo.

CADA ESCENA: headline (2-6 palabras, con *asteriscos* en la palabra clave), narration (1-3 frases), y según convenga:
- illustration: {"svg": "<nombre de un SVG de svgs>", "caption": "Fig. N · ...", "anims": [...]}
- elements: tarjetas (máx. 2 por escena; con ilustración, máx. 1 pequeña: tag, stamp o stat).
- mascot: el matraz (mascota de la cuenta) aparece SOLO de vez en cuando (2-3 veces por vídeo) para una nota corta y graciosa:
  {"trigger": "palabra", "pose": "point|think|surprise|explain|cheer|wave", "note": "máx. 8 palabras", "side": "right"}.
  No lo pongas en escenas con ilustración Y tarjetas a la vez.
- Ninguna nota ni texto en pantalla lleva emojis.

TARJETAS (elements). Todas aceptan "trigger" (palabra EXACTA de la narración de esa escena en la que aparecen) y "sfx":
- {"type":"stat","label","value":número,"from"?,"decimals"?,"unit"?,"prefix"?,"note"?}
- {"type":"fact","label"?,"text","tone":"paper|accent|ink"}
- {"type":"icon","icon":<atom|earth|moon|sun|paper|dna|brain|drop|bolt|rocket|clock|eye|bacteria|star|ruler|heart|fire|snow|magnet|planet|microscope|leaf|bone|wave>,"label"?}
- {"type":"compare","label"?,"rows":[{"label","value","display"?,"trigger"?}],"log"?}
- {"type":"dots","label"?,"filled","total"?,"caption"?}
- {"type":"list","label"?,"items":[{"text","trigger"?}]}
- {"type":"scale","label"?,"from","to","progress":0-1,"marker"?}
- {"type":"tag","text","tone":"accent|ink|hot"}
- {"type":"stamp","text","tone":"accent|hot"}  (golpe: ¡PLAF!, ¡BANG!, MITO, FALSO...)
- {"type":"follow"} y {"type":"ask","text":"pregunta final con *resaltado*"}  (solo en TÚ)

ILUSTRACIONES (svgs): estilo "pegatina realista": contornos de tinta #0B0B14 gruesos (6-9 px, stroke-linejoin round) en
el primer plano, pero con VOLUMEN y DETALLE de ilustración profesional:
- Anatomía y forma CORRECTAS y reconocibles (número de patas, articulaciones, proporciones, colores reales del ser u objeto).
  Las patas, antenas, tallos... salen del punto exacto del cuerpo donde nacen y terminan donde apoyan (calcula las coordenadas).
- Volumen: <linearGradient>/<radialGradient> en <defs> (claro arriba, oscuro abajo), una línea de brillo clara y fina en el
  borde superior de cada cuerpo, brillo blanco en ojos y gotas, sombras proyectadas suaves (elipse oscura con opacidad).
- Profundidad: fondo en capas (lejos: colores claros y desaturados SIN contorno; cerca: con contorno), luz coherente.
- Detalles que dan realismo: segmentos, texturas sencillas (escamas, venas, pelitos), reflejos en el agua, piedrecitas...
- Trazos finos (patas, antenas): doble trazo, uno de tinta ancho debajo y el color encima, para que tengan contorno.
- Paleta realista para el tema (agua #8FD3FF→#2F7FD6, vegetación #36B37E/#7BE07B, tierra #E7C487...) y marca solo para
  resaltar: lima #C8FF2E (flechas, etiquetas), coral #FF5A36 (peligro, calor, fuerza).
- Protagonista grande y centrado, nada importante a menos de 40 unidades del borde (el panel recorta un poco arriba y abajo),
  esquina superior izquierda (0-340 × 0-70) libre para el rótulo "Fig.". Sin filtros, sin imágenes, sin <script>, sin enlaces.
- Haz 3-4 SVG por vídeo: la escena general + vistas de detalle o esquemas del truco (cortes, vista al microscopio, vista
  desde arriba, moléculas...). Etiquetas: <g id="..."><rect rx="12" .../><text font-family="JetBrains Mono"
  font-weight="800" font-size="30" text-anchor="middle">TEXTO</text></g>, MAYÚSCULAS, cortas, con línea guía hasta lo que
  señalan; NUNCA tapan al protagonista ni se solapan entre sí ni con flechas.
- Todo lo que se anima va en un <g id="nombre"> propio (ids en minúscula, sin espacios). Los <defs>/<use> están permitidos.

ANIMACIONES (anims): {"target": id, "effect", "trigger"?, "dur"?, "to"?: [dx, dy], "rotate"?, "amount"?, "origin"?, "phase"?, "sfx"?}
- Entradas (empiezan ocultas hasta su trigger): pop, fade, draw (trazos que se dibujan: chorros, flechas, rayos), grow, slide-left/right/up/down.
- Bucles (sin trigger = desde el inicio de la escena): float, bob, sway (origin bottom para plantas), spin, pulse, shake, wiggle,
  flow (agua que corre en trazos), blink, ripple (onda que se expande y se desvanece: pon 2 por punto con phase 0 y 0.5),
  breathe (respiración sutil del cuerpo), drift (deriva lateral lenta).
- Acciones: move (to: desplazamiento en unidades del viewBox, rotate: grados, origin: center|bottom|top|left|right|bottom-left|bottom-right|top-left|top-right = punto de giro de la caja del grupo, útil para bisagras; los move se suman), hide (desaparece; sin trigger = oculto toda la escena),
  punch (golpe de énfasis: crece y vuelve, justo cuando la voz nombra esa parte).
- CÁMARA: {"target": "camera", "effect": "zoom", "to": [x, y] del viewBox, "amount": 1.3-2, "trigger"?} acerca la cámara a ese
  punto; con "amount": 1 vuelve al plano general. Úsala 1-2 veces por escena para enseñar el detalle del que se habla.
- Cuando reutilices un SVG en otra escena, oculta con "hide" lo que no toque mostrar.
- TODAS las escenas (salvo la firma y la final TÚ) llevan ilustración: nada de escenas solo con tarjetas. Si una escena es un
  dato o una cifra, ponla sobre un dibujo (puedes REUTILIZAR un SVG con otros zooms y otras anims, o hacer uno nuevo).
- VARIEDAD DE DISEÑO por escena (illustration.layout): alterna en cada vídeo los tres tipos, no siempre el recuadro:
  · "panel" (por defecto): recuadro con viewBox 0 0 1000 700.
  · "free": SIN recuadro, el dibujo flota sobre el fondo azul de la marca. SVG SIN rect de fondo (transparente), puede ser
    vertical (p. ej. viewBox 0 0 1000 1100) y con "height" en px (800-900). Ideal para el protagonista recortado.
  · "full": PANTALLA COMPLETA detrás del titular. SVG vertical viewBox 0 0 1080 1920 con fondo completo; lo importante entre
    y 450 y 1250 (arriba va el titular y abajo los subtítulos). Úsalo para el gancho o los momentos espectaculares.
  Usa al menos 2 escenas "free" o "full" por vídeo. El zoom de cámara usa las coordenadas del viewBox de cada SVG.
- La ilustración debe verse COMPLETA desde el primer instante de la escena (nunca un panel vacío): usa entradas solo para
  detalles que se añaden (chorros, flechas, etiquetas, burbujas), no para el protagonista ni el fondo.
- RITMO MUY DINÁMICO: cada escena con ilustración lleva 6-12 anims; algo nuevo pasa cada 1-1,5 s (zoom, punch, etiqueta,
  flecha, movimiento) siempre sincronizado con la palabra que lo dice, y siempre hay bucles de fondo (ondas, respiración, antenas).
- Cada escena debe enseñar lo que dice la narración: si hablas de la lava, se ve la lava; no reutilices un dibujo que no encaja.
- "sfx" opcional para el sonido del momento: whoosh, pop, papel, ding, sorpresa, sello, chasquido, chorro, burbujas, splash, boing, rotulador, brillo, none.

TRIGGERS: deben ser una palabra que aparezca TAL CUAL en la narración de ESA escena (sin signos).
Escribe los números de la narración con cifras (42, 5.000) solo si se leen bien; evita siglas raras.

ADEMÁS:
- "title": título para YouTube (máx. 70 caracteres, con gancho, sin mentir) que puede llevar 1 emoji al final.
- "publish": {"caption": texto para Instagram/TikTok (2-3 frases con gancho + pregunta), "description": descripción para YouTube
  (3-5 frases + fuente), "hashtags": 5-8 hashtags sin '#', en español, del tema y generales (ciencia, curiosidades...)}.
- "cover": {"text": gancho de portada de 3-6 palabras con *palabra clave*, "badge": "¿CÓMO LO HACE?" o similar, "scene": 0}.
- "source": línea corta de fuentes.

Responde SOLO con el objeto JSON (sin texto antes ni después, sin ```), con las claves: topic, title, source, chapters,
outro_cta (lema corto general, p. ej. "Todo tiene un truco"; nunca "la naturaleza tiene trucos"), svgs (objeto nombre → SVG completo), scenes, publish, cover."""


def _extract_json(text: str) -> dict:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text)
    start, end = text.find("{"), text.rfind("}")
    return json.loads(text[start : end + 1])


def write_script(topic: dict, facts: str, feedback: list[str] | None = None, previous: str | None = None) -> tuple[dict, str]:
    client = _client()
    system = [
        {"type": "text", "text": SYSTEM},
        {"type": "text", "text": "EJEMPLO COMPLETO DE UN VÍDEO BIEN HECHO (formato y nivel de detalle a imitar; el tema será otro):\n" + _example(),
         "cache_control": {"type": "ephemeral"}},
    ]
    content = f"TEMA: {topic['tema']}\n\nFICHA DE INVESTIGACIÓN (única fuente de datos):\n{facts}"
    messages = [{"role": "user", "content": content}]
    if feedback and previous:
        messages += [
            {"role": "assistant", "content": previous},
            {"role": "user", "content": "Corrige estos problemas y devuelve el JSON completo corregido:\n- " + "\n- ".join(feedback)},
        ]
    with client.beta.messages.stream(
        model=MODEL,
        max_tokens=64000,
        system=system,
        messages=messages,
        output_config={"effort": "high"},
        betas=[FALLBACK_BETA],
        fallbacks="default",
    ) as stream:
        msg = stream.get_final_message()
    _check_stop(msg)
    raw = _text(msg)
    return _extract_json(raw), raw


# ------------------------------------------------------------------ 4. validación

def _ids(svg: str) -> set[str]:
    return set(re.findall(r'\bid="([^"]+)"', svg))


def validate(script: dict) -> tuple[list[str], list[str]]:
    """Devuelve (errores graves, avisos). Arregla en el sitio lo que se puede arreglar solo."""
    errors, warnings = [], []
    for key in ("topic", "title", "svgs", "scenes", "publish", "cover"):
        if key not in script:
            errors.append(f"Falta la clave '{key}'.")
    if errors:
        return errors, warnings
    script["chapters"] = ["?", "1", "2", "3", "+", "TÚ"]
    script.setdefault("outro_cta", "Todo tiene un truco")

    svgs = script["svgs"]
    for name, svg in list(svgs.items()):
        try:
            root = ET.fromstring(svg)
        except ET.ParseError as e:
            errors.append(f"El SVG '{name}' no es XML válido: {e}.")
            continue
        if "viewBox" not in root.attrib:
            errors.append(f"El SVG '{name}' no tiene viewBox.")
        if re.search(r"<script|<foreignObject|href=\"http", svg, re.I):
            errors.append(f"El SVG '{name}' contiene scripts o enlaces externos.")

    scenes = script["scenes"]
    if not 7 <= len(scenes) <= 12:
        errors.append(f"Hay {len(scenes)} escenas; deben ser entre 7 y 12.")
    if len(scenes) > 1:
        sig = scenes[1].get("narration", "")
        sig = SIGNATURE_LINE
        scenes[1].update({"chapter": 0, "signature": True, "headline": "El truco es…", "narration": sig})
        scenes[1].pop("illustration", None), scenes[1].pop("elements", None), scenes[1].pop("mascot", None)
    for i, sc in enumerate(scenes[2:-1], start=2):
        if not sc.get("illustration"):
            errors.append(f"Escena {i}: todas las escenas (salvo firma y final) deben llevar ilustración.")
    if scenes and not scenes[0].get("illustration"):
        errors.append("La escena 0 (gancho) necesita ilustración.")
    words = sum(len(s.get("narration", "").split()) for s in scenes)
    if not 110 <= words <= 240:
        errors.append(f"La narración tiene {words} palabras; debe tener entre 150 y 210.")
    if scenes and scenes[-1].get("chapter") != 5:
        errors.append("La última escena debe ser el capítulo 5 (TÚ) con la pregunta final.")

    for i, sc in enumerate(scenes):
        if not isinstance(sc.get("chapter"), int) or not 0 <= sc["chapter"] <= 5:
            errors.append(f"Escena {i}: capítulo inválido.")
        keys = {norm(w) for w in sc.get("narration", "").split()}

        def fix_trigger(obj: dict, where: str):
            trig = obj.get("trigger")
            if trig and not any(norm(t) in keys for t in str(trig).split()):
                warnings.append(f"Escena {i} {where}: trigger '{trig}' no está en la narración (se quita).")
                obj.pop("trigger")
            if obj.get("sfx") and obj["sfx"] not in SFX:
                obj.pop("sfx")

        ill = sc.get("illustration")
        if ill:
            name = ill.get("svg")
            if name not in svgs:
                errors.append(f"Escena {i}: la ilustración usa el SVG '{name}', que no existe.")
            else:
                ids = _ids(svgs[name])
                good = []
                for a in ill.get("anims", []):
                    if a.get("target") == "camera":
                        if a.get("effect") != "zoom":
                            continue
                    elif a.get("target") not in ids or a.get("effect") not in EFFECTS:
                        warnings.append(f"Escena {i}: animación inválida {a.get('target')}/{a.get('effect')} (se quita).")
                        continue
                    fix_trigger(a, f"anim {a['target']}")
                    good.append(a)
                ill["anims"] = good
        good_el = []
        for el in sc.get("elements", []) or []:
            if el.get("type") not in ELEMENT_TYPES:
                warnings.append(f"Escena {i}: tarjeta '{el.get('type')}' desconocida (se quita).")
                continue
            if el["type"] == "icon" and el.get("icon") not in ICONS:
                el["icon"] = "star"
            fix_trigger(el, el["type"])
            for sub in ("rows", "items", "options"):
                for it in el.get(sub, []) or []:
                    fix_trigger(it, f"{el['type']}.{sub}")
            good_el.append(el)
        sc["elements"] = good_el
        cam = sc.get("mascot")
        if cam:
            if cam.get("pose") not in POSES:
                cam["pose"] = "point"
            fix_trigger(cam, "mascot")
    return errors, warnings


# ------------------------------------------------------------------ 5. guardar

def slugify(text: str) -> str:
    import unicodedata
    t = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:50] or "video"


def save(script: dict) -> Path:
    folder = CONTENT_DIR / f"{date.today():%Y-%m-%d}-{slugify(script['topic'])}"
    folder.mkdir(parents=True, exist_ok=True)
    for name, svg in script.pop("svgs").items():
        (folder / f"{name}.svg").write_text(svg, encoding="utf-8")
    for sc in script["scenes"]:
        ill = sc.get("illustration")
        if ill and "svg" in ill:
            ill["svg_file"] = f"{ill.pop('svg')}.svg"
    (folder / "guion.json").write_text(json.dumps(script, ensure_ascii=False, indent=2), encoding="utf-8")
    return folder


def generate(topic: dict | None = None, max_fixes: int = 2) -> Path:
    topic = topic or pick_topic()
    print(f"Tema: {topic['tema']}")
    facts = research(topic)
    print("Ficha de investigación lista.")
    script, raw = write_script(topic, facts)
    for attempt in range(max_fixes + 1):
        errors, warnings = validate(script)
        for w in warnings:
            print("  aviso:", w)
        if not errors:
            break
        print(f"  {len(errors)} errores, pidiendo corrección ({attempt + 1}/{max_fixes}): {errors}")
        if attempt == max_fixes:
            raise RuntimeError("El guion no pasó la validación: " + "; ".join(errors))
        script, raw = write_script(topic, facts, errors, raw)
    script["categoria"] = topic.get("categoria", script.get("categoria", "animales"))
    folder = save(script)
    (folder / "investigacion.md").write_text(facts, encoding="utf-8")
    mark_done(topic)
    try:
        from .visual_qa import review
        review(folder)
    except Exception as e:  # la revisión visual nunca debe parar la publicación
        print(f"  aviso: revisión visual no completada: {e}")
    print(f"→ {folder}")
    return folder

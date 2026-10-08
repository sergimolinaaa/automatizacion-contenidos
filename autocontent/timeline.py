"""Convierte un guion (escenas + elementos con palabra disparadora) y los tiempos de
cada palabra de la locución en las props que renderiza Remotion (video/src/types.ts)."""

import copy
import re
import unicodedata

NESTED = {"compare": "rows", "list": "items", "quiz": "options"}


def norm(word: str) -> str:
    w = unicodedata.normalize("NFKD", word.lower()).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]", "", w)


def estimate_words(text: str, start: float, wps_factor: float = 1.0) -> list[dict]:
    """Tiempos aproximados (para previsualizar sin TTS)."""
    words, t = [], start
    for raw in text.split():
        dur = (0.075 * len(norm(raw) or raw) + 0.13) / wps_factor
        words.append({"text": raw, "start": round(t, 3), "end": round(t + dur, 3)})
        t += dur + (0.28 if raw[-1] in ".,:;!?" else 0.03)
    return words


def find_trigger(trigger: str | None, words: list[dict], after: float) -> float | None:
    if not trigger:
        return None
    target = [norm(w) for w in trigger.split() if norm(w)]
    if not target:
        return None
    keys = [norm(w["text"]) for w in words]
    for i, w in enumerate(words):
        if w["start"] + 1e-6 < after:
            continue
        if keys[i : i + len(target)] == target or (len(target) == 1 and keys[i].startswith(target[0])):
            return w["start"]
    return None


def build_props(script: dict, scene_words: list[list[dict]], end_padding: float = 0.5) -> dict:
    """scene_words[i] son las palabras de la escena i con tiempos ABSOLUTOS."""
    scenes_in = script["scenes"]
    all_words = [w for ws in scene_words for w in ws]
    scenes = []
    for i, (sc, ws) in enumerate(zip(scenes_in, scene_words)):
        start = 0.0 if i == 0 else round(ws[0]["start"] - 0.12, 3)
        scenes.append({"start": start, "_words": ws, "src": sc})
    for i, s in enumerate(scenes):
        nxt = scenes[i + 1]["start"] if i + 1 < len(scenes) else s["_words"][-1]["end"] + end_padding
        s["end"] = round(nxt, 3)

    out_scenes = []
    for s in scenes:
        sc, ws = s["src"], s["_words"]
        elements, cursor = [], s["start"]
        for k, el in enumerate(copy.deepcopy(sc.get("elements", []))):
            at = find_trigger(el.pop("trigger", None), ws, cursor)
            if at is None:
                at = s["start"] + 0.25 + 0.6 * k
            el["at"] = round(max(s["start"], at - 0.1), 3)
            cursor = el["at"]
            sub = NESTED.get(el["type"])
            for j, item in enumerate(el.get(sub, []) if sub else []):
                t_item = find_trigger(item.pop("trigger", None), ws, cursor)
                if t_item is not None:
                    item["at"] = round(t_item - 0.1, 3)
                    cursor = item["at"]
            elements.append(el)
        ill = sc.get("illustration")
        if ill:
            ill = copy.deepcopy(ill)
            anims = []
            for a in ill.get("anims", []):
                trig = a.pop("trigger", None)
                if trig:
                    at = find_trigger(trig, ws, s["start"])
                    a["at"] = round((at if at is not None else s["start"] + 0.3) - 0.05, 3)
                elif "delay" in a:
                    a["at"] = round(s["start"] + a.pop("delay"), 3)
                anims.append(a)
            ill["anims"] = anims
        cameo = sc.get("mascot")
        if cameo:
            cameo = copy.deepcopy(cameo)
            at = find_trigger(cameo.pop("trigger", None), ws, s["start"])
            cameo["at"] = round(at - 0.1 if at is not None else s["start"] + 0.4, 3)
        out_scenes.append({
            "start": s["start"],
            "end": s["end"],
            "chapter": sc.get("chapter", 0),
            "number": sc.get("number"),
            "headline": sc["headline"],
            "signature": bool(sc.get("signature")),
            "illustration": ill,
            "mascot": cameo,
            "elements": elements,
        })

    last_end = out_scenes[-1]["end"]
    props = {
        "source": script.get("source"),
        "chapters": script["chapters"],
        "scenes": out_scenes,
        "words": all_words,
        "audio": script.get("audio"),
        "music": script.get("music"),
        "musicVolume": script.get("music_volume", 0.1),
        "outro": {"at": round(last_end, 3), "cta": script.get("outro_cta")} if script.get("outro", True) else None,
    }
    return props


COVER_SECONDS = 18 / 30  # fotogramas finales con la portada (video/src/Short.tsx: COVER_FRAMES)


def cover_offset_ms(props: dict) -> int:
    """Milisegundo del vídeo donde está la portada (para elegirla como miniatura)."""
    return int((duration_of(props) + COVER_SECONDS / 2) * 1000)


def duration_of(props: dict) -> float:
    end = max(s["end"] for s in props["scenes"])
    if props.get("outro"):
        end = max(end, props["outro"]["at"] + 2.6)
    return end

"""Efectos de sonido y música de fondo sintetizados por código (sin derechos de autor).

- Los efectos se colocan solos a partir de las props del vídeo: entrada de tarjetas, sellos,
  cambios de capítulo, animaciones de la ilustración, el cameo del matraz, la firma...
  Cualquier elemento o animación puede forzar su sonido con el campo "sfx" ("none" = silencio).
- La música es un bucle alegre de marimba, bajo y percusión suave; cambia de tonalidad,
  progresión y patrón según una semilla, así cada vídeo suena distinto.
- Si hay pistas en assets/music/ (con licencia libre), se usan en lugar de la música generada.
"""

import random
import wave
from pathlib import Path

import numpy as np

SR = 44100

GAIN = {
    "whoosh": 0.45, "barrido": 0.7, "pop": 0.55, "papel": 0.55, "ding": 0.4, "sorpresa": 0.45,
    "sello": 0.85, "chasquido": 0.85, "chorro": 0.5, "burbujas": 0.5, "splash": 0.6, "tic": 0.35,
    "magia": 0.6, "boing": 0.5, "rotulador": 0.35, "brillo": 0.4,
}


def _t(d: float) -> np.ndarray:
    return np.arange(int(SR * d)) / SR


def _lowpass(x: np.ndarray, cutoff) -> np.ndarray:
    """Filtro paso bajo de un polo con corte variable (vectorizado por tramos)."""
    cutoff = np.broadcast_to(np.asarray(cutoff, dtype=float), x.shape)
    a = 1 - np.exp(-2 * np.pi * cutoff / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i in range(len(x)):
        acc += a[i] * (x[i] - acc)
        y[i] = acc
    return y


def _norm(x: np.ndarray, peak: float = 0.9) -> np.ndarray:
    return x / (np.max(np.abs(x)) + 1e-9) * peak


def _note(f: float, dur: float, t0: float, out: np.ndarray, timbre: str = "marimba", vol: float = 1.0) -> None:
    t = _t(dur)
    if timbre == "marimba":
        x = (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 4 * f * t) * np.exp(-t * 18)
             + 0.12 * np.sin(2 * np.pi * 10 * f * t) * np.exp(-t * 40)) * np.exp(-t * 6)
    elif timbre == "campana":
        x = (np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * 2.76 * f * t) * np.exp(-t * 3)
             + 0.25 * np.sin(2 * np.pi * 5.4 * f * t) * np.exp(-t * 6)) * np.exp(-t * 2.4)
    elif timbre == "pluck":
        x = (np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 12)
             + 0.25 * np.sin(2 * np.pi * 3 * f * t) * np.exp(-t * 20)) * np.exp(-t * 9)
    else:  # bajo redondo
        x = (np.sin(2 * np.pi * f * t) + 0.2 * np.sin(2 * np.pi * 2 * f * t)) * np.exp(-t * 3.5) * (1 - np.exp(-t * 80))
    x *= 1 - np.exp(-t * 300)
    i = int(t0 * SR)
    end = min(len(out), i + len(x))
    if end > i:
        out[i:end] += vol * x[: end - i]


# ---------------------------------------------------------------- efectos

def synth_library() -> dict[str, np.ndarray]:
    rng = np.random.default_rng(7)
    s: dict[str, np.ndarray] = {}
    t = _t(0.38)
    env = np.sin(np.pi * t / t[-1]) ** 2
    s["whoosh"] = _norm(_lowpass(rng.normal(0, 1, len(t)), 400 + 3500 * np.sin(np.pi * t / t[-1])) * env)
    t = _t(0.55)
    env = np.sin(np.pi * t / t[-1]) ** 1.5
    noise = _lowpass(rng.normal(0, 1, len(t)), 250 + 2200 * np.sin(np.pi * t / t[-1]))
    s["barrido"] = _norm(noise * env + 0.3 * np.diff(noise, prepend=0) * 8 * env)
    t = _t(0.11)
    f = 720 * np.exp(-t * 18) + 240
    s["pop"] = _norm(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 30))
    t = _t(0.16)
    s["papel"] = _norm(0.7 * np.diff(rng.normal(0, 1, len(t)), prepend=0) * np.exp(-t * 45) + np.sin(2 * np.pi * 110 * t) * np.exp(-t * 28))
    t = _t(0.7)
    s["ding"] = _norm((np.sin(2 * np.pi * 1318 * t) + 0.35 * np.sin(2 * np.pi * 2637 * t) + 0.15 * np.sin(2 * np.pi * 3954 * t))
                      * np.exp(-t * 6) * (1 - np.exp(-t * 400)))
    t = _t(0.3)
    f = 330 + 900 * (t / t[-1]) ** 1.6 + 25 * np.sin(2 * np.pi * 28 * t)
    s["sorpresa"] = _norm(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / t[-1]) ** 0.6)
    t = _t(0.25)
    s["sello"] = _norm(np.sin(2 * np.pi * 70 * t) * np.exp(-t * 22) + 0.5 * _lowpass(rng.normal(0, 1, len(t)), 1800) * np.exp(-t * 35))
    t = _t(0.35)
    s["chasquido"] = _norm(np.diff(rng.normal(0, 1, len(t)), prepend=0) * np.exp(-t * 60) + 0.8 * np.sin(2 * np.pi * 95 * t) * np.exp(-t * 25))
    t = _t(0.4)
    s["chorro"] = _norm(_lowpass(rng.normal(0, 1, len(t)), 2500 + 2000 * t / t[-1]) * np.sin(np.pi * t / t[-1]))
    # burbujas: blips que suben de tono
    t = _t(0.6)
    out = np.zeros(len(t))
    for k in range(7):
        d = _t(0.07)
        f = rng.uniform(500, 1100) * (1 + 3 * d / d[-1])
        blip = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * d / d[-1])
        i = int(SR * rng.uniform(0, 0.5))
        out[i:i + len(blip)] += blip[: len(out) - i]
    s["burbujas"] = _norm(out)
    # splash: golpe de agua
    t = _t(0.6)
    s["splash"] = _norm(_lowpass(rng.normal(0, 1, len(t)), 3000 * np.exp(-t * 4) + 300) * np.exp(-t * 7) + 0.5 * np.sin(2 * np.pi * 120 * t) * np.exp(-t * 20))
    # tic: contador
    t = _t(0.03)
    s["tic"] = _norm(np.sin(2 * np.pi * 2400 * t) * np.exp(-t * 150))
    # boing: muelle (entrada del matraz)
    t = _t(0.45)
    f = 220 + 160 * np.sin(2 * np.pi * 9 * t) * np.exp(-t * 5)
    s["boing"] = _norm(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 5))
    # rotulador: trazo que se dibuja
    t = _t(0.5)
    ch = _lowpass(rng.normal(0, 1, len(t)), 5000) * (0.6 + 0.4 * np.sin(2 * np.pi * 9 * t))
    s["rotulador"] = _norm(np.diff(ch, prepend=0) * np.sin(np.pi * t / t[-1]) ** 0.5)
    # brillo: arpegio rápido de campanitas
    out = np.zeros(int(SR * 0.9))
    for k, fr in enumerate([1318.5, 1568, 1975.5, 2637]):
        _note(fr, 0.6, k * 0.05, out, "campana", 0.5)
    s["brillo"] = _norm(out)
    s["magia"] = jingle()
    return s


def jingle() -> np.ndarray:
    """Sintonía de «El truco es…» (~2,2 s): redoble corto + "¡tachán!" con brillo."""
    total = np.zeros(int(SR * 2.4))
    rng = np.random.default_rng(3)
    # redoble suave
    for k in range(10):
        d = _t(0.05)
        hit = _lowpass(rng.normal(0, 1, len(d)), 2500) * np.exp(-d * 60) * (0.3 + 0.07 * k)
        i = int(SR * k * 0.045)
        total[i:i + len(hit)] += hit
    # ¡ta-chán!
    do5, mi5, sol5, do6, mi6 = 523.25, 659.25, 783.99, 1046.5, 1318.5
    _note(sol5, 0.25, 0.48, total, "marimba", 0.8)
    for f, v in [(do5, 0.8), (mi5, 0.6), (sol5, 0.55), (do6, 0.5)]:
        _note(f, 1.6, 0.66, total, "marimba", v)
    _note(130.81, 1.4, 0.66, total, "bajo", 0.6)
    for k, f in enumerate([do6, mi6, 1568 * 2 / 2 * 1.0, 2093]):
        _note(f, 1.0, 0.72 + k * 0.06, total, "campana", 0.28)
    fade = np.ones_like(total)
    n = int(SR * 0.5)
    fade[-n:] = np.linspace(1, 0, n)
    return _norm(total * fade, 0.9)


# ---------------------------------------------------------------- música

SCALES = {
    "C": 261.63, "D": 293.66, "F": 349.23, "G": 392.0, "A": 220.0 * 2,
}
PROGRESSIONS = [
    [0, 5, 3, 4],  # I vi IV V
    [0, 4, 5, 3],  # I V vi IV
    [5, 3, 0, 4],  # vi IV I V
    [0, 3, 5, 4],  # I IV vi V
]
MAJOR = [0, 2, 4, 5, 7, 9, 11]


def _degree_freq(root: float, degree: int, octave: int = 0) -> float:
    semis = MAJOR[degree % 7] + 12 * (degree // 7 + octave)
    return root * 2 ** (semis / 12)


def music(duration: float, seed: int) -> np.ndarray:
    rnd = random.Random(seed)
    rng = np.random.default_rng(seed)
    bpm = rnd.choice([100, 104, 108, 112])
    beat = 60 / bpm
    root = rnd.choice(list(SCALES.values()))
    prog = rnd.choice(PROGRESSIONS)
    arp = rnd.choice([[0, 2, 4, 2], [0, 4, 2, 4], [0, 2, 4, 7], [4, 2, 0, 2]])
    total = np.zeros(int(SR * (duration + 2)))
    hat = _lowpass(rng.normal(0, 1, int(SR * 0.04)), 7000)
    hat = np.diff(hat, prepend=0) * np.exp(-_t(0.04) * 90)
    kick_t = _t(0.25)
    kick = np.sin(2 * np.pi * np.cumsum(110 * np.exp(-kick_t * 25) + 45) / SR) * np.exp(-kick_t * 14)
    t0, bar = 0.0, 0
    while t0 < duration + 1:
        chord = prog[bar % len(prog)]
        # bajo: negras en la tónica del acorde
        for b in range(4):
            _note(_degree_freq(root, chord, -2), beat * 0.9, t0 + b * beat, total, "bajo", 0.55)
        # marimba: arpegio en corcheas
        for k in range(8):
            deg = chord + arp[k % len(arp)]
            vol = 0.32 if k % 2 == 0 else 0.22
            _note(_degree_freq(root, deg, 0), beat * 0.9, t0 + k * beat / 2, total, "marimba", vol)
        # melodía sencilla cada dos compases
        if bar % 2 == 1:
            for k, step in enumerate(rnd.sample([0, 2, 4, 5, 7], 3)):
                _note(_degree_freq(root, chord + step, 1), beat * 1.2, t0 + (k * 1.25 + 0.5) * beat, total, "pluck", 0.16)
        # percusión suave
        for b in range(4):
            i = int((t0 + b * beat) * SR)
            if b in (0, 2) and i + len(kick) < len(total):
                total[i:i + len(kick)] += 0.45 * kick
            j = int((t0 + b * beat + beat / 2) * SR)
            if j + len(hat) < len(total):
                total[j:j + len(hat)] += 0.12 * hat
        t0 += 4 * beat
        bar += 1
    total = total[: int(SR * duration)]
    fade_in, fade_out = int(SR * 0.6), int(SR * 1.5)
    total[:fade_in] *= np.linspace(0, 1, fade_in)
    total[-fade_out:] *= np.linspace(1, 0, fade_out)
    return _norm(total, 0.8)


# ---------------------------------------------------------------- eventos

ANIM_SFX = {"pop": "pop", "draw": "rotulador", "move": "whoosh", "slide-left": "whoosh", "slide-right": "whoosh",
            "slide-up": "whoosh", "slide-down": "whoosh", "grow": "pop", "zoom": "whoosh", "punch": "tic"}
ELEMENT_SFX = {"stat": "pop", "fact": "papel", "icon": "pop", "compare": "papel", "dots": "papel", "list": "papel",
               "scale": "whoosh", "tag": "papel", "stamp": "sello", "quiz": "papel", "ask": "pop", "follow": "ding"}


def events_from_props(props: dict) -> list[dict]:
    ev: list[dict] = []

    def add(name: str | None, t: float | None, vol: float = 1.0):
        if name and name != "none" and t is not None and t >= 0:
            ev.append({"sfx": name, "t": t, "vol": vol})

    prev_chapter = None
    for i, sc in enumerate(props["scenes"]):
        if sc.get("signature"):
            add("magia", sc["start"])
        elif prev_chapter is not None and sc["chapter"] != prev_chapter:
            add("barrido", max(0, sc["start"] - 0.12))
        elif i > 0:
            add("whoosh", sc["start"], 0.6)
        prev_chapter = sc["chapter"]
        ill = sc.get("illustration") or {}
        if ill and i > 0 and not sc.get("signature"):
            add("pop", sc["start"] + 0.05, 0.5)
        for a in ill.get("anims", []):
            if "sfx" in a:
                add(a["sfx"], a.get("at"))
            elif a.get("at") is not None and a["at"] > sc["start"] + 0.1:
                add(ANIM_SFX.get(a["effect"]), a["at"], 0.7)
        for el in sc.get("elements", []):
            add(el.get("sfx", ELEMENT_SFX.get(el["type"])), el.get("at"))
            for sub in ("rows", "items", "options"):
                for it in el.get(sub, []) or []:
                    add("ding" if sub == "options" else "pop", it.get("at"), 0.6)
        cam = sc.get("mascot")
        if cam:
            add("boing", cam.get("at"))
    if props.get("outro"):
        add("brillo", props["outro"]["at"])
    # no apilar sonidos en el mismo instante
    ev.sort(key=lambda e: e["t"])
    out, last = [], -1.0
    for e in ev:
        if e["t"] - last >= 0.08 or e["sfx"] in ("magia", "sello", "barrido"):
            out.append(e)
            last = e["t"]
    return out


# ---------------------------------------------------------------- mezcla

def _save(path: Path, x: np.ndarray) -> Path:
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())
    return path


def sfx_track(events: list[dict], duration: float, out: Path) -> Path:
    lib = synth_library()
    total = np.zeros(int(SR * duration) + SR)
    for e in events:
        x = lib[e["sfx"]] * GAIN.get(e["sfx"], 0.5) * e.get("vol", 1.0)
        i = int(e["t"] * SR)
        if i >= len(total):
            continue
        end = min(len(total), i + len(x))
        total[i:end] += x[: end - i]
    total = total[: int(SR * duration)]
    peak = np.max(np.abs(total)) if len(total) else 0
    if peak > 0.95:
        total *= 0.95 / peak
    return _save(out, total)


def music_track(duration: float, seed: int, out: Path) -> Path:
    return _save(out, music(duration, seed))

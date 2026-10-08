"""Locución con Edge TTS y tiempos palabra a palabra para subtítulos y animaciones.

Todo el guion se sintetiza de una sola vez (la entonación fluye entre frases, como una
persona leyendo) y luego se reparte por escenas alineando las palabras devueltas por el TTS
con las del texto original. Después se masteriza el audio para redes (-14 LUFS).
"""

import asyncio
import subprocess
from pathlib import Path

import edge_tts

from .timeline import norm

TICKS_PER_SECOND = 10_000_000  # edge-tts da offsets en unidades de 100 ns


def probe_duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(out.stdout.strip())


async def _synthesize(text: str, voice: str, rate: str, pitch: str, out_path: Path) -> list[dict]:
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch, boundary="WordBoundary")
    words = []
    with open(out_path, "wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                start = chunk["offset"] / TICKS_PER_SECOND
                words.append({"text": chunk["text"], "start": start, "end": start + chunk["duration"] / TICKS_PER_SECOND})
    return words


def align(tokens: list[str], tts_words: list[dict]) -> list[dict]:
    """Asigna a cada palabra del guion (con su puntuación) los tiempos del TTS."""
    out: list[dict | None] = [None] * len(tokens)
    j = 0
    for w in tts_words:
        key = norm(w["text"])
        if not key:
            continue
        for k in range(j, min(j + 4, len(tokens))):
            tk = norm(tokens[k])
            if tk and (tk == key or tk.startswith(key) or key.startswith(tk)):
                if out[k] is None:
                    out[k] = {"text": tokens[k], "start": w["start"], "end": w["end"]}
                else:  # el TTS partió una palabra en dos: alargamos
                    out[k]["end"] = w["end"]
                j = k + 1 if tk == key or key.startswith(tk) else k
                break
    # palabras que el TTS no devolvió: reparten el hueco entre sus vecinas
    for k, item in enumerate(out):
        if item is None:
            prev_end = next((out[i]["end"] for i in range(k - 1, -1, -1) if out[i]), 0.0)
            nxt = next((out[i]["start"] for i in range(k + 1, len(out)) if out[i]), prev_end + 0.3)
            out[k] = {"text": tokens[k], "start": prev_end, "end": max(prev_end + 0.05, min(nxt, prev_end + 0.4))}
    return out  # type: ignore[return-value]


def master(src: Path, dst: Path) -> Path:
    """Limpieza y volumen de redes: quita graves sobrantes, comprime suave y normaliza."""
    af = "highpass=f=70,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120,loudnorm=I=-14:TP=-1.5:LRA=9"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-af", af, "-ar", "44100", "-b:a", "192k", str(dst)], check=True)
    return dst


def narrate(narrations: list[str], cfg: dict, workdir: Path) -> tuple[Path, list[list[dict]]]:
    """Devuelve el audio masterizado y, por escena, sus palabras con tiempos absolutos."""
    v = cfg["voice"]
    scene_tokens = [n.split() for n in narrations]
    flat = [t for toks in scene_tokens for t in toks]
    raw = workdir / "voice_raw.mp3"
    tts_words = asyncio.run(_synthesize(" ".join(narrations), v["name"], v.get("rate", "+0%"), v.get("pitch", "+0Hz"), raw))
    aligned = align(flat, tts_words)
    per_scene, i = [], 0
    for toks in scene_tokens:
        per_scene.append(aligned[i : i + len(toks)])
        i += len(toks)
    audio = master(raw, workdir / "voice.mp3")
    return audio, per_scene

"""Locución con Edge TTS (gratis) y tiempos palabra a palabra para los subtítulos."""

import asyncio
import subprocess
from pathlib import Path

import edge_tts

TICKS_PER_SECOND = 10_000_000  # edge-tts da offsets en unidades de 100 ns


def probe_duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(out.stdout.strip())


async def _synthesize(text: str, voice: str, rate: str, out_path: Path) -> list[dict]:
    communicate = edge_tts.Communicate(text, voice, rate=rate, boundary="WordBoundary")
    words = []
    with open(out_path, "wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                start = chunk["offset"] / TICKS_PER_SECOND
                words.append({"text": chunk["text"], "start": start, "end": start + chunk["duration"] / TICKS_PER_SECOND})
    return words


def narrate(segments: list[dict], cfg: dict, workdir: Path) -> list[dict]:
    """Genera un audio por segmento. Devuelve, por segmento: ruta, duración y palabras con tiempos absolutos."""
    voice, rate = cfg["voice"]["name"], cfg["voice"].get("rate", "+0%")
    result, cursor = [], 0.0
    for i, seg in enumerate(segments):
        audio = workdir / f"voice_{i:02d}.mp3"
        words = asyncio.run(_synthesize(seg["narration"], voice, rate, audio))
        duration = probe_duration(audio)
        for w in words:
            w["start"] += cursor
            w["end"] += cursor
        result.append({"audio": audio, "duration": duration, "words": words})
        cursor += duration
    return result

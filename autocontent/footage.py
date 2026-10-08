"""Descarga metraje de stock vertical de Pexels (gratis, uso comercial permitido)."""

import os
import random
from pathlib import Path

import requests

PEXELS_SEARCH = "https://api.pexels.com/videos/search"


def pick_file(video: dict, target_width: int = 1080) -> dict | None:
    """Elige el archivo vertical cuya anchura se acerque más a la deseada (sin pasarse demasiado)."""
    files = [f for f in video.get("video_files", []) if f.get("width") and f.get("height") and f["height"] > f["width"]]
    if not files:
        return None
    return min(files, key=lambda f: (abs(f["width"] - target_width), -f["width"]))


def search(query: str, min_duration: float, used_ids: set[int]) -> dict | None:
    resp = requests.get(
        PEXELS_SEARCH,
        headers={"Authorization": os.environ["PEXELS_API_KEY"]},
        params={"query": query, "orientation": "portrait", "per_page": 15, "size": "medium"},
        timeout=30,
    )
    resp.raise_for_status()
    videos = [v for v in resp.json().get("videos", []) if v["id"] not in used_ids]
    long_enough = [v for v in videos if v.get("duration", 0) >= min_duration]
    pool = long_enough or videos
    if not pool:
        return None
    return random.choice(pool[:6])


def fetch_clips(segments: list[dict], durations: list[float], workdir: Path, fallback_query: str) -> list[Path]:
    used: set[int] = set()
    clips = []
    for i, (seg, dur) in enumerate(zip(segments, durations)):
        video = None
        for query in (seg["visual_query"], " ".join(seg["visual_query"].split()[:2]), fallback_query):
            video = search(query, dur, used)
            if video:
                break
        if not video:
            raise RuntimeError(f"No hay metraje para el segmento {i}: {seg['visual_query']!r}")
        used.add(video["id"])
        file = pick_file(video)
        if not file:
            raise RuntimeError(f"El vídeo {video['id']} de Pexels no tiene versión vertical")
        path = workdir / f"clip_{i:02d}.mp4"
        with requests.get(file["link"], stream=True, timeout=120) as r:
            r.raise_for_status()
            with open(path, "wb") as f:
                for chunk in r.iter_content(1 << 20):
                    f.write(chunk)
        clips.append(path)
    return clips

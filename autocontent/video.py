"""Montaje final con ffmpeg: clips recortados a 9:16, voz, música opcional y subtítulos quemados."""

import random
import subprocess
from pathlib import Path

from .config import ROOT

MUSIC_DIR = ROOT / "assets" / "music"


def run(cmd: list[str], cwd: Path) -> None:
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg falló ({' '.join(cmd[:6])}...):\n{proc.stderr[-2000:]}")


def prepare_clip(src: Path, duration: float, cfg: dict, out: Path) -> Path:
    w, h, fps = cfg["video"]["width"], cfg["video"]["height"], cfg["video"]["fps"]
    vf = f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},fps={fps},setsar=1,format=yuv420p"
    run(["ffmpeg", "-y", "-stream_loop", "-1", "-i", str(src), "-t", f"{duration:.3f}", "-vf", vf, "-an",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", str(out)], cwd=out.parent)
    return out


def concat(paths: list[Path], out: Path, reencode_audio: bool = False) -> Path:
    listing = out.with_suffix(".txt")
    listing.write_text("".join(f"file '{p.name}'\n" for p in paths), encoding="utf-8")
    codec = ["-c:a", "aac", "-b:a", "192k"] if reencode_audio else ["-c", "copy"]
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listing.name, *codec, out.name], cwd=out.parent)
    return out


def pick_music() -> Path | None:
    tracks = [p for p in MUSIC_DIR.glob("*") if p.suffix.lower() in {".mp3", ".m4a", ".wav", ".ogg"}]
    return random.choice(tracks) if tracks else None


def assemble(clips: list[Path], voice_parts: list[dict], subs: Path, cfg: dict, out: Path) -> Path:
    workdir = out.parent
    prepared = [prepare_clip(c, vp["duration"], cfg, workdir / f"prep_{i:02d}.mp4")
                for i, (c, vp) in enumerate(zip(clips, voice_parts))]
    video = concat(prepared, workdir / "video_noaudio.mp4")
    voice = concat([vp["audio"] for vp in voice_parts], workdir / "voice.m4a", reencode_audio=True)

    inputs = ["-i", video.name, "-i", voice.name]
    music = pick_music()
    if music:
        inputs += ["-stream_loop", "-1", "-i", str(music)]
        vol = cfg["video"].get("music_volume", 0.12)
        audio_graph = f"[2:a]volume={vol}[m];[1:a][m]amix=inputs=2:duration=first:normalize=0[a]"
    else:
        audio_graph = "[1:a]anull[a]"
    graph = f"[0:v]ass={subs.name}[v];{audio_graph}"
    run(["ffmpeg", "-y", *inputs, "-filter_complex", graph, "-map", "[v]", "-map", "[a]",
         "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out.name], cwd=workdir)
    return out

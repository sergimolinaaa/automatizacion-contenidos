"""Renderiza un guion (carpeta con guion.json + SVG) a vídeo y portada con voz, efectos y música."""

import json
import shutil
import subprocess
import tempfile
import zlib
from pathlib import Path

from . import sfx
from .config import ROOT, load_config
from .timeline import build_props, cover_offset_ms, duration_of
from .voice import narrate

VIDEO_DIR = ROOT / "video"
PUBLIC_AUDIO = VIDEO_DIR / "public" / "audio"
COVER_FRAME_EXTRA = 0.0


def load_script(folder: Path) -> dict:
    script = json.loads((folder / "guion.json").read_text(encoding="utf-8"))
    for sc in script["scenes"]:
        ill = sc.get("illustration")
        if ill and "svg_file" in ill:
            ill["svg"] = (folder / ill.pop("svg_file")).read_text(encoding="utf-8")
    return script


def build(folder: Path) -> dict:
    """Voz + tiempos + efectos + música → props del vídeo (y audio en video/public/audio)."""
    cfg = load_config()
    script = load_script(folder)
    work = Path(tempfile.mkdtemp())
    audio, scene_words = narrate([sc["narration"] for sc in script["scenes"]], cfg, work)
    PUBLIC_AUDIO.mkdir(parents=True, exist_ok=True)
    shutil.copy(audio, PUBLIC_AUDIO / "voz.mp3")
    script["audio"] = "audio/voz.mp3"
    props = build_props(script, scene_words)
    dur = duration_of(props)
    sfx.sfx_track(sfx.events_from_props(props), dur, PUBLIC_AUDIO / "sfx.wav")
    props["sfx"] = "audio/sfx.wav"
    tracks = sorted((ROOT / "assets" / "music").glob("*.mp3"))
    seed = zlib.crc32(folder.name.encode())
    if tracks:
        shutil.copy(tracks[seed % len(tracks)], PUBLIC_AUDIO / "music.mp3")
        props["music"] = "audio/music.mp3"
    else:
        sfx.music_track(dur, seed, PUBLIC_AUDIO / "music.wav")
        props["music"] = "audio/music.wav"
    if "cover" in script:
        props["cover"] = script["cover"]
    return props


def _remotion(args: list[str]) -> None:
    subprocess.run(["npx", "remotion", *args], cwd=VIDEO_DIR, check=True)


def render(folder: Path, out_dir: Path | None = None) -> tuple[Path, Path]:
    out_dir = (out_dir or folder).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    props = build(folder)
    props_path = Path(tempfile.mkdtemp()) / "props.json"
    props_path.write_text(json.dumps(props, ensure_ascii=False), encoding="utf-8")
    video = out_dir / "video.mp4"
    cover = out_dir / "portada.png"
    print(f"Duración: {duration_of(props):.1f} s")
    _remotion(["render", "Short", str(video), f"--props={props_path}"])
    _remotion(["still", "Portada", str(cover), "--frame=0", f"--props={props_path}"])
    (out_dir / "props.json").write_text(json.dumps({k: v for k, v in props.items() if k != "scenes"} | {"duration": duration_of(props), "cover_offset_ms": cover_offset_ms(props)}, ensure_ascii=False, indent=1), encoding="utf-8")
    return video, cover

"""Renderiza un guion de ejemplo con voz real (Edge TTS) y Remotion.

Uso: python scripts/render_example.py examples/pez-arquero/guion.json previews/pez-arquero.mp4
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from autocontent.config import load_config  # noqa: E402
from autocontent.timeline import build_props, duration_of  # noqa: E402
from autocontent.voice import narrate  # noqa: E402


def main(src: Path, out: Path) -> None:
    cfg = load_config()
    script = json.loads(src.read_text(encoding="utf-8"))
    for sc in script["scenes"]:
        ill = sc.get("illustration")
        if ill and "svg_file" in ill:
            ill["svg"] = (src.parent / ill.pop("svg_file")).read_text(encoding="utf-8")

    work = Path(tempfile.mkdtemp())
    audio, scene_words = narrate([sc["narration"] for sc in script["scenes"]], cfg, work)
    public_audio = ROOT / "video" / "public" / "audio"
    public_audio.mkdir(parents=True, exist_ok=True)
    shutil.copy(audio, public_audio / "voz.mp3")
    script["audio"] = "audio/voz.mp3"

    props = build_props(script, scene_words)
    props_path = work / "props.json"
    props_path.write_text(json.dumps(props, ensure_ascii=False), encoding="utf-8")
    print(f"Duración: {duration_of(props):.1f} s")

    out = out.resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["npx", "remotion", "render", "Short", str(out), f"--props={props_path}"], cwd=ROOT / "video", check=True)
    print(f"→ {out}")


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))

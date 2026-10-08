"""Renderiza un guion de ejemplo (examples/<tema>/guion.json) con voz, efectos y música.

Uso: python scripts/render_example.py examples/pez-arquero/guion.json previews/pez-arquero.mp4
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from autocontent.render import render  # noqa: E402

if __name__ == "__main__":
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    video, cover = render(src.parent, out_dir=ROOT / "output" / src.parent.name)
    out.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(video, out)
    shutil.copy(cover, out.with_suffix(".png"))
    print(f"→ {out}")

"""Renderiza los guiones (examples/* y content/*) que no tienen vídeo o que han cambiado.

Uso: python scripts/render_queue.py [REF_ANTERIOR] [--todo]
"""
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from autocontent.render import render  # noqa: E402

OUT = ROOT / "previews"


def changed_dirs(before: str | None) -> set[str]:
    if not before or set(before) == {"0"}:
        return set()
    try:
        out = subprocess.run(["git", "diff", "--name-only", before, "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True).stdout
    except subprocess.CalledProcessError:
        return set()
    return {"/".join(p.split("/")[:2]) for p in out.splitlines() if p.startswith(("examples/", "content/"))}


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    everything = "--todo" in sys.argv
    changed = changed_dirs(args[0] if args else None)
    folders = sorted(p.parent for p in list(ROOT.glob("examples/*/guion.json")) + list(ROOT.glob("content/*/guion.json")))
    for folder in folders:
        rel = folder.relative_to(ROOT).as_posix()
        video = OUT / f"{folder.name}-con-voz.mp4"
        if everything or rel in changed or not video.exists():
            print(f"=== {rel}")
            v, c = render(folder, out_dir=ROOT / "output" / folder.name)
            OUT.mkdir(exist_ok=True)
            shutil.copy(v, video)
            shutil.copy(c, video.with_suffix(".png"))
            shutil.copy(ROOT / "output" / folder.name / "props.json", OUT / f"{folder.name}-con-voz.json")


if __name__ == "__main__":
    main()

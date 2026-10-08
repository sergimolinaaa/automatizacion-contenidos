"""Genera las props de previsualización (tiempos estimados, sin voz) a partir de un guion.

Uso: python scripts/preview_props.py examples/pez-arquero/guion.json
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from autocontent.timeline import build_props, duration_of, estimate_words  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

src = Path(sys.argv[1])
script = json.loads(src.read_text(encoding="utf-8"))
for sc in script["scenes"]:
    ill = sc.get("illustration")
    if ill and "svg_file" in ill:
        ill["svg"] = (src.parent / ill.pop("svg_file")).read_text(encoding="utf-8")

t, scene_words = 0.15, []
for sc in script["scenes"]:
    ws = estimate_words(sc["narration"], t, wps_factor=1.15)
    scene_words.append(ws)
    t = ws[-1]["end"] + 0.3
props = build_props(script, scene_words)
out = ROOT / "video" / "src" / "sample-props.json"
out.write_text(json.dumps(props, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"{out} · {duration_of(props):.1f} s")

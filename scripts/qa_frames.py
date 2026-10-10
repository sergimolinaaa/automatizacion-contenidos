"""Renderiza un guion a media resolución (sin voz, tiempos estimados) y saca fotogramas de cada escena + hojas de contacto.
Uso: python3 scripts/qa_frames.py content/<carpeta> <directorio_salida>
"""
import json, os, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault("REMOTION_BROWSER", "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell")
from autocontent.visual_qa import preview_props
from autocontent.render import load_script
folder, out = ROOT / sys.argv[1], Path(sys.argv[2]).resolve()
out.mkdir(parents=True, exist_ok=True)
props = preview_props(load_script(folder))
(out / "props.json").write_text(json.dumps(props, ensure_ascii=False))
video = out / "qa.mp4"
subprocess.run(["npx", "remotion", "render", "Short", str(video), f"--props={out/'props.json'}", "--scale=0.5", "--muted", "--concurrency=1", "--log=error"], cwd=ROOT / "video", check=True)
rows = []
for i, sc in enumerate(props["scenes"]):
    a, b = sc["start"], sc["end"]
    ts = [a + 0.35, a + 0.5 * (b - a), b - 0.2]
    names = []
    for k, t in enumerate(ts):
        f = out / f"s{i:02d}_{k}.png"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", str(video), "-frames:v", "1", str(f)], check=True)
        names.append(str(f))
    print(f"escena {i}: {a:.1f}-{b:.1f}s  {sc['headline']}")
    rows.append(names)
# hojas de contacto de 4 escenas (3 fotogramas cada una)
for n in range(0, len(rows), 4):
    chunk = rows[n:n + 4]
    lines = []
    for j, r in enumerate(chunk):
        line = out / f"_row{n + j}.png"
        subprocess.run(["convert", *r, "+append", "-resize", "x480", str(line)], check=True)
        lines.append(str(line))
    subprocess.run(["convert", *lines, "-append", str(out / f"hoja_{n // 4}.png")], check=True)
print("hojas:", sorted(str(p) for p in out.glob("hoja_*.png")))

"""Renderiza las muestras de estilo (sin voz, tiempos estimados) a entregas/estilos/{A,B,C}.mp4 + PNG + comparativa.
Uso: python3 muestras/estilos/render.py [A B C]
"""
import json, os, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
os.environ.setdefault("REMOTION_BROWSER", "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell")
from autocontent.visual_qa import preview_props
from autocontent.render import load_script

OUT = ROOT / "entregas" / "estilos"
OUT.mkdir(parents=True, exist_ok=True)
DUR = 6.0


def run(*cmd, **kw):
    subprocess.run(list(map(str, cmd)), check=True, **kw)


def render(estilo):
    folder = Path(__file__).resolve().parent / estilo
    props = preview_props(load_script(folder))
    props["scenes"][0]["end"] = DUR
    props.pop("outro", None)
    pp = folder / "_props.json"
    pp.write_text(json.dumps(props, ensure_ascii=False))
    mudo = OUT / f"_{estilo}_mudo.mp4"
    run("npx", "remotion", "render", "Short", mudo, f"--props={pp}", f"--frames=0-{int(DUR*30)-1}", "--muted", "--log=error",
        cwd=ROOT / "video")
    pp.unlink()
    mp4 = OUT / f"{estilo}.mp4"
    # pista de audio silenciosa para que las redes y los reproductores lo traten como vídeo normal
    run("ffmpeg", "-v", "error", "-y", "-i", mudo, "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-shortest",
        "-c:v", "copy", "-c:a", "aac", mp4)
    mudo.unlink()
    run("ffmpeg", "-v", "error", "-y", "-ss", "4.5", "-i", mp4, "-frames:v", "1", OUT / f"{estilo}.png")
    print("→", mp4)


if __name__ == "__main__":
    for e in sys.argv[1:] or ["A", "B", "C"]:
        render(e)
    if all((OUT / f"{e}.mp4").exists() for e in "ABC"):
        ins = sum((["-i", OUT / f"{e}.mp4"] for e in "ABC"), [])
        fl = ";".join(f"[{i}:v]scale=-2:1080,setsar=1[v{i}]" for i in range(3)) + ";[v0][v1][v2]hstack=inputs=3[v]"
        run("ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", fl, "-map", "[v]", "-map", "0:a", "-c:v", "libx264",
            "-pix_fmt", "yuv420p", "-crf", "20", "-c:a", "aac", "-shortest", OUT / "comparativa.mp4")
        print("→", OUT / "comparativa.mp4")

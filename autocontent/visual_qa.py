"""Revisión visual automática: renderiza fotogramas de cada escena y Claude los revisa como imágenes.

Busca líneas o piezas mal colocadas, partes que flotan o se separan del cuerpo, colores incoherentes,
solapes, paneles vacíos, textos cortados o ilegibles y animaciones que no encajan con lo que se dice.
Si encuentra problemas, devuelve los SVG y animaciones corregidos y se vuelve a revisar.
"""

import base64
import json
import re
import subprocess
import tempfile
from pathlib import Path

import anthropic

from .config import ROOT
from .render import load_script
from .timeline import build_props, estimate_words

MODEL = "claude-opus-5-5"
FALLBACK_BETA = "server-side-fallback-2026-07-01"
VIDEO_DIR = ROOT / "video"

QA_PROMPT = """Eres el director de arte de «El truco es…», una cuenta de vídeos científicos animados con un estilo de
ilustración plana tipo pegatina (contornos de tinta gruesos, colores planos, marca azul #2347FF + lima #C8FF2E).
Te paso fotogramas reales de cada escena del vídeo (a mitad y al final de la escena), el código SVG de las ilustraciones
y sus animaciones. Revisa con ojo MUY exigente, como si fuera a publicarse en una cuenta profesional:

- Geometría: líneas, patas, brazos, antenas, chorros o flechas que no salen de donde deberían, que quedan sueltos,
  que atraviesan el cuerpo o que apuntan a sitios sin sentido; piezas que flotan separadas; proporciones absurdas.
- Coherencia: el dibujo debe representar de forma reconocible y CORRECTA lo que dice la narración (anatomía real,
  dirección de los movimientos, qué empuja a qué). Si algo es científicamente incorrecto en el dibujo, corrígelo.
- Color: colores que no corresponden al objeto real, poco contraste, elementos que se pierden con el fondo.
- Composición: paneles vacíos o casi vacíos, protagonista demasiado pequeño, cosas cortadas por el borde,
  etiquetas que tapan lo importante o se salen, texto ilegible.
- Animación: elementos que aparecen en el sitio equivocado tras un "move", rotaciones con el punto de giro mal
  (p. ej. una bisagra que gira desde el centro), cosas que deberían verse y están ocultas, o al revés.

Devuelve SOLO un JSON (sin ```):
{"ok": true|false,
 "issues": ["descripción concreta de cada problema"],
 "svgs": {"nombre": "<svg ...>SVG COMPLETO CORREGIDO</svg>"},     // solo los SVG que cambies; mismos ids si siguen animándose
 "anims": {"<índice de escena>": [ ...lista COMPLETA de anims corregida para esa escena... ]}  // solo escenas que cambies
}
"ok" es true solo si no hay ningún problema visible. Mantén el viewBox 0 0 1000 700, el estilo y los ids que usan las
animaciones (o actualiza las animaciones si cambias ids). Las anims usan "trigger" (palabra de la narración), no "at"."""


def preview_props(script: dict) -> dict:
    t, scene_words = 0.15, []
    for sc in script["scenes"]:
        ws = estimate_words(sc["narration"], t, wps_factor=1.15)
        scene_words.append(ws)
        t = ws[-1]["end"] + 0.3
    props = build_props(script, scene_words)
    if "cover" in script:
        props["cover"] = script["cover"]
    return props


def render_frames(props: dict, work: Path) -> list[tuple[int, float, Path]]:
    """Renderiza el vídeo a media resolución (sin audio) y extrae 2 fotogramas por escena con ilustración."""
    props_path = work / "props.json"
    props_path.write_text(json.dumps(props, ensure_ascii=False), encoding="utf-8")
    video = work / "qa.mp4"
    subprocess.run(["npx", "remotion", "render", "Short", str(video), f"--props={props_path}", "--scale=0.5", "--muted",
                    "--log=error"], cwd=VIDEO_DIR, check=True)
    frames = []
    for i, sc in enumerate(props["scenes"]):
        if not sc.get("illustration") and not sc.get("elements"):
            continue
        for k, t in enumerate((sc["start"] + 0.45 * (sc["end"] - sc["start"]), sc["end"] - 0.25)):
            out = work / f"s{i:02d}_{k}.png"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", str(video), "-frames:v", "1", str(out)], check=True)
            frames.append((i, t, out))
    return frames


def _img(path: Path) -> dict:
    return {"type": "image", "source": {"type": "base64", "media_type": "image/png",
                                        "data": base64.standard_b64encode(path.read_bytes()).decode()}}


def review_once(folder: Path) -> dict:
    raw_script = json.loads((folder / "guion.json").read_text(encoding="utf-8"))
    script = load_script(folder)
    work = Path(tempfile.mkdtemp())
    frames = render_frames(preview_props(script), work)
    svgs = {p.stem: p.read_text(encoding="utf-8") for p in folder.glob("*.svg")}
    content: list[dict] = [{"type": "text", "text": QA_PROMPT}]
    for i, t, path in frames:
        sc = raw_script["scenes"][i]
        content.append({"type": "text", "text": f"Escena {i} · titular «{sc['headline']}» · narración: «{sc['narration']}» · fotograma a {t:.1f}s"})
        content.append(_img(path))
    content.append({"type": "text", "text": "SVG actuales:\n" + "\n\n".join(f"### {n}\n{s}" for n, s in svgs.items())})
    anims = {i: sc["illustration"].get("anims", []) for i, sc in enumerate(raw_script["scenes"]) if sc.get("illustration")}
    content.append({"type": "text", "text": "Animaciones actuales por escena:\n" + json.dumps(anims, ensure_ascii=False)})
    with anthropic.Anthropic().beta.messages.stream(
        model=MODEL, max_tokens=64000, output_config={"effort": "high"},
        messages=[{"role": "user", "content": content}],
        betas=[FALLBACK_BETA], fallbacks="default",
    ) as stream:
        msg = stream.get_final_message()
    if msg.stop_reason in ("refusal", "max_tokens"):
        raise RuntimeError(f"Revisión visual interrumpida: {msg.stop_reason}")
    text = "".join(b.text for b in msg.content if b.type == "text").strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text)
    return json.loads(text[text.find("{"): text.rfind("}") + 1])


def apply_fixes(folder: Path, result: dict) -> None:
    for name, svg in (result.get("svgs") or {}).items():
        (folder / f"{Path(name).stem}.svg").write_text(svg, encoding="utf-8")
    if result.get("anims"):
        g = json.loads((folder / "guion.json").read_text(encoding="utf-8"))
        for idx, anims in result["anims"].items():
            sc = g["scenes"][int(idx)]
            if sc.get("illustration"):
                sc["illustration"]["anims"] = anims
        (folder / "guion.json").write_text(json.dumps(g, ensure_ascii=False, indent=2), encoding="utf-8")


def review(folder: Path, rounds: int = 3) -> list[str]:
    """Revisa y corrige hasta que no haya problemas (o se agoten las rondas). Devuelve el historial de problemas."""
    history = []
    for r in range(rounds):
        result = review_once(folder)
        issues = result.get("issues", [])
        history += [f"ronda {r + 1}: {i}" for i in issues]
        print(f"Revisión visual {r + 1}: {'OK' if result.get('ok') else f'{len(issues)} problemas'}")
        for i in issues:
            print("  -", i)
        if result.get("ok") and not result.get("svgs") and not result.get("anims"):
            break
        apply_fixes(folder, result)
    (folder / "revision_visual.md").write_text("\n".join(f"- {h}" for h in history) or "- Sin problemas", encoding="utf-8")
    return history

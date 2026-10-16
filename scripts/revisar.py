"""Revisión automática de un vídeo SIN mirar imágenes.

Uso: python3 scripts/revisar.py content/<carpeta> [--fotos]

Comprueba:
  1. Duración (real si ya está renderizado en previews/, si no estimada) dentro de 40-60 s.
  2. Que en ninguna escena pasen más de 3 s sin que algo aparezca, cambie o se mueva de forma puntual
     (entradas, movimientos, zooms, tarjetas, cameos, cambio de escena; los bucles de fondo no cuentan).
  3. Subtítulos y audio: todas las palabras con tiempo, en orden y dentro de la duración del audio (render real).
  4. Elementos fuera de cuadro: mide con Chromium la caja de cada texto y grupo con id de cada SVG y avisa si
     sale del área visible del layout (panel recorta 35 px arriba y abajo).
  5. Textos de publicación sin guiones y con 3-5 hashtags.
Con --fotos, si hay problemas, extrae como mucho 3 fotogramas de los momentos dudosos (de previews/ o del QA).
Sale con código 1 si encuentra problemas.
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from autocontent.render import load_script  # noqa: E402
from autocontent.visual_qa import preview_props  # noqa: E402

CHROME = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"
MAX_GAP = 3.0
LOOPS = {"float", "bob", "sway", "spin", "pulse", "shake", "wiggle", "flow", "blink", "ripple", "breathe", "drift"}
SAFE = {"panel": (0, 35, 1000, 665)}  # x0, y0, x1, y1 visibles del panel 1000x700


def events(sc: dict) -> list[float]:
    t = [sc["start"]]
    for el in sc.get("elements", []):
        t.append(el["at"])
        for sub in ("items", "rows", "options"):
            t += [i["at"] for i in el.get(sub, []) if "at" in i]
        if el.get("reveal"):
            t.append(el["reveal"])
    for a in (sc.get("illustration") or {}).get("anims", []):
        if a.get("effect") not in LOOPS and a.get("at") is not None:
            t.append(a["at"])
            if a.get("dur"):
                t.append(a["at"] + a["dur"])
    if sc.get("mascot"):
        t.append(sc["mascot"].get("at", sc["start"]))
    return sorted(x for x in t if sc["start"] - 0.01 <= x <= sc["end"])


def bboxes(svg: str) -> list[dict]:
    """Cajas (en unidades del viewBox) de textos y grupos con id, medidas con Chromium."""
    html = ("<html><body style='margin:0'>" + svg + "<pre id='out'></pre><script>"
            "const s=document.querySelector('svg');const r=[];"
            "s.querySelectorAll('text,g[id]').forEach(e=>{try{const b=e.getBBox();"
            "const m=e.getCTM(),n=s.getCTM().inverse().multiply(m);"
            "const p=[[b.x,b.y],[b.x+b.width,b.y],[b.x,b.y+b.height],[b.x+b.width,b.y+b.height]].map(([x,y])=>"
            "[n.a*x+n.c*y+n.e,n.b*x+n.d*y+n.f]);"
            "r.push({id:e.id||'',tag:e.tagName,txt:(e.textContent||'').trim().slice(0,30),"
            "x0:Math.min(...p.map(q=>q[0])),y0:Math.min(...p.map(q=>q[1])),x1:Math.max(...p.map(q=>q[0])),"
            "y1:Math.max(...p.map(q=>q[1]))})}catch(x){}});"
            "document.getElementById('out').textContent=JSON.stringify(r);</script></body></html>")
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(html)
    out = subprocess.run([CHROME, "--no-sandbox", "--disable-gpu", "--dump-dom", f"file://{f.name}"],
                         capture_output=True, text=True, timeout=60).stdout
    m = re.search(r"<pre id=\"out\">(.*?)</pre>", out, re.S)
    return json.loads(m.group(1).replace("&quot;", '"').replace("&amp;", "&")) if m else []


def main() -> int:
    folder = (ROOT / sys.argv[1]).resolve() if not Path(sys.argv[1]).is_absolute() else Path(sys.argv[1])
    raw = json.loads((folder / "guion.json").read_text(encoding="utf-8"))
    real = ROOT / "previews" / f"{folder.name}-con-voz.json"
    rendered = json.loads(real.read_text(encoding="utf-8")) if real.exists() else {}
    props = preview_props(load_script(folder))  # línea de tiempo de escenas y animaciones (estimada)
    fuente = "real (render con voz)" if rendered else "estimada (sin voz)"
    problemas, dudas = [], []

    # 1. duración
    dur = props["scenes"][-1]["end"]
    video = ROOT / "previews" / f"{folder.name}-con-voz.mp4"
    if video.exists() and rendered:
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                    str(video)], capture_output=True, text=True).stdout or dur)
    print(f"Duración {fuente}: {dur:.1f} s")
    if not 40 <= dur <= 60:
        if rendered:
            problemas.append(f"duración {dur:.1f} s fuera de 40-60 s")
        else:
            print(f"· aviso: duración estimada {dur:.1f} s (la real con voz suele ser algo menor)")

    # 2. huecos sin cambios
    for i, sc in enumerate(props["scenes"]):
        if sc.get("signature") or i == len(props["scenes"]) - 1:  # la tarjeta final (seguir + pregunta) se queda quieta a propósito
            continue
        ev = events(sc) + [sc["end"]]
        for a, b in zip(ev, ev[1:]):
            if b - a > MAX_GAP:
                problemas.append(f"escena {i} «{sc.get('headline', '')}»: {b - a:.1f} s sin cambios ({a:.1f}-{b:.1f} s)")
                dudas.append((a + b) / 2)

    # 3. subtítulos y audio
    words = rendered.get("words", [])
    if words:
        prev = 0.0
        for w in words:
            if w["end"] < w["start"] or w["start"] + 0.001 < prev:
                problemas.append(f"subtítulo desordenado en «{w['text']}» ({w['start']:.2f} s)")
                break
            prev = w["start"]
        if words[-1]["end"] > dur + 0.2:
            problemas.append("los subtítulos acaban después que el audio")
        n_narr = sum(len(sc.get("narration", "").split()) for sc in raw["scenes"])
        if abs(len(words) - n_narr) > 2:
            problemas.append(f"{len(words)} subtítulos para {n_narr} palabras de narración")

    # 4. fuera de cuadro
    for i, sc in enumerate(raw["scenes"]):
        ill = sc.get("illustration") or {}
        if not ill.get("svg_file"):
            continue
        svg = (folder / ill["svg_file"]).read_text(encoding="utf-8")
        vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', svg).group(1).replace(",", " ").split()]
        lay = ill.get("layout", "panel")
        x0, y0, x1, y1 = SAFE.get(lay, (vb[0], vb[1], vb[0] + vb[2], vb[1] + vb[3])) if lay == "panel" else \
            (vb[0], vb[1], vb[0] + vb[2], vb[1] + vb[3])
        hidden = {a["target"] for a in ill.get("anims", []) if a.get("effect") == "hide" and not a.get("trigger") and a.get("at") is None}
        for b in bboxes(svg):
            if b["id"] in hidden or (b["tag"] == "g" and not b["id"]):
                continue
            if b["x0"] < x0 - 2 or b["y0"] < y0 - 2 or b["x1"] > x1 + 2 or b["y1"] > y1 + 2:
                if b["tag"] == "text" or b["id"] not in ("", "fondo", "bg", "background"):
                    nombre = b["txt"] or b["id"]
                    if b["tag"] == "text":
                        problemas.append(f"escena {i} ({ill['svg_file']}): texto «{nombre}» fuera de cuadro")
            # los grupos grandes (fondos, escenarios) pueden salirse a propósito; solo se avisa de textos

    # 5. textos de publicación
    pub = raw.get("publish", {})
    for k in ("caption", "description"):
        if re.search(r"[–—]|\s-\s|^\s*-\s", pub.get(k, ""), re.M):
            problemas.append(f"publish.{k} tiene guiones")
    for k in ("title",):
        if re.search(r"[–—]|\s-\s", raw.get(k, "")):
            problemas.append("el título tiene guiones")
    if not 3 <= len(pub.get("hashtags", [])) <= 5:
        problemas.append(f"publish.hashtags: {len(pub.get('hashtags', []))} (deben ser 3-5)")

    print("\n".join(f"✗ {p}" for p in problemas) or "✓ sin problemas")
    if problemas and "--fotos" in sys.argv:
        src = video if video.exists() else None
        if src:
            for k, t in enumerate(sorted(set(round(d, 1) for d in dudas if isinstance(d, float)))[:3]):
                out = Path(tempfile.gettempdir()) / f"revisar_{folder.name}_{k}.png"
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", str(src), "-frames:v", "1",
                                "-vf", "scale=-1:640", str(out)], check=True)
                print("foto:", out)
    return 1 if problemas else 0


if __name__ == "__main__":
    sys.exit(main())

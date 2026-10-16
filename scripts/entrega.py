"""Resumen de entrega de un vídeo: título de portada, guion, descripción y elementos visuales por tramo.
Uso: python3 scripts/entrega.py content/<carpeta>  (escribe entregas/<carpeta>.md; fuera de content/ para no re-renderizar)
"""
import json, sys
from pathlib import Path

folder = Path(sys.argv[1])
g = json.loads((folder / "guion.json").read_text(encoding="utf-8"))
pub = g.get("publish", {})
cover = g.get("cover", {}).get("text", g["title"]).replace("*", "")
out = [f"# {g['title']}", "", f"**Título de portada:** {cover}", f"**Fecha:** {pub.get('at', 'cola normal (14:00)')}", "", "## Guion"]
for i, sc in enumerate(g["scenes"]):
    out.append(f"{i + 1}. {sc.get('narration', '')}")
out += ["", "## Descripción (YouTube)", pub.get("description", ""), "", "## Texto (TikTok / Instagram)", pub.get("caption", ""),
        "", "Hashtags: " + " ".join("#" + h.lstrip("#") for h in pub.get("hashtags", [])) + " #eltrucoes", "", "## Elementos visuales por tramo"]
for i, sc in enumerate(g["scenes"]):
    ill = sc.get("illustration") or {}
    bits = []
    if ill:
        bits.append(f"dibujo {ill.get('svg_file', '')} ({ill.get('layout', 'panel')}), {len(ill.get('anims', []))} animaciones")
    bits += [e.get("type") + (": " + e["text"] if e.get("text") else "") for e in sc.get("elements", [])]
    if sc.get("mascot"):
        bits.append("mascota: " + sc["mascot"].get("note", ""))
    out.append(f"{i + 1}. **{sc.get('headline', '').replace('*', '')}**: " + "; ".join(bits))
dest = folder.parents[1] / "entregas" / f"{folder.name}.md"
dest.parent.mkdir(exist_ok=True)
dest.write_text("\n".join(out) + "\n", encoding="utf-8")
print(dest)

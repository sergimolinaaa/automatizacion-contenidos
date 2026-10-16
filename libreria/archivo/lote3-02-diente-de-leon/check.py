"""uso: check.py content/<carpeta>  → valida como el pipeline (sin modificar el guion)"""
import sys, json, copy
from pathlib import Path
sys.path.insert(0, "/home/user/automatizacion-contenidos")
from autocontent.generate import validate
folder = Path(sys.argv[1])
s = json.loads((folder / "guion.json").read_text())
s = copy.deepcopy(s)
s["svgs"] = {p.stem: p.read_text() for p in folder.glob("*.svg")}
for sc in s["scenes"]:
    ill = sc.get("illustration")
    if ill:
        ill["svg"] = Path(ill.pop("svg_file")).stem
err, warn = validate(s)
print("ERRORES:", err); print("AVISOS:", warn)
print("palabras:", sum(len(x["narration"].split()) for x in s["scenes"]))
for i, sc in enumerate(s["scenes"]):
    n = len(sc.get("illustration", {}).get("anims", [])) if sc.get("illustration") else 0
    print(i, sc["headline"], "anims:", n)

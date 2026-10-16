import json, sys, copy
from pathlib import Path
sys.path.insert(0, "/home/user/automatizacion-contenidos")
from autocontent.generate import validate
folder = Path(sys.argv[1])
g = json.loads((folder / "guion.json").read_text())
s = copy.deepcopy(g)
s["svgs"] = {p.stem: p.read_text() for p in folder.glob("*.svg")}
used = set()
for sc in s["scenes"]:
    ill = sc.get("illustration")
    if ill:
        ill["svg"] = Path(ill.pop("svg_file")).stem; used.add(ill["svg"])
before = json.dumps(s["scenes"], sort_keys=True)
err, warn = validate(s)
print("errores", err); print("avisos", warn)
print("svgs sin usar:", set(s["svgs"]) - used)
print("palabras", sum(len(x["narration"].split()) for x in g["scenes"]), "escenas", len(g["scenes"]))
for i, sc in enumerate(g["scenes"]):
    ill = sc.get("illustration")
    print(i, len(sc["narration"].split()), "anims", len(ill["anims"]) if ill else "-", "el", len(sc.get("elements", [])), "masc" if sc.get("mascot") else "")

import json, sys, copy
from pathlib import Path
sys.path.insert(0, "/home/user/automatizacion-contenidos")
from autocontent.generate import validate
f = Path(sys.argv[1])
s = json.loads((f / "guion.json").read_text())
s2 = copy.deepcopy(s); s2["svgs"] = {}
for sc in s2["scenes"]:
    ill = sc.get("illustration")
    if ill:
        n = ill.pop("svg_file"); ill["svg"] = Path(n).stem
        s2["svgs"][ill["svg"]] = (f / n).read_text()
e, w = validate(s2)
print("ERR", e); print("WARN", w)

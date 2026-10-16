import json, re, sys
sys.path.insert(0, "/home/user/automatizacion-contenidos")
from autocontent.timeline import norm
from pathlib import Path
folder = Path(sys.argv[1])
s = json.loads((folder / "guion.json").read_text())
words = 0
for i, sc in enumerate(s["scenes"]):
    keys = [norm(w) for w in sc["narration"].split()]
    words += len(sc["narration"].split())
    def chk(o, where):
        t = o.get("trigger")
        if not t: return
        tt = [norm(w) for w in t.split() if norm(w)]
        ok = any(keys[k:k+len(tt)] == tt or (len(tt) == 1 and keys[k].startswith(tt[0])) for k in range(len(keys)))
        if not ok: print(f"escena {i} {where}: trigger '{t}' no está")
    ill = sc.get("illustration")
    if ill:
        svg = (folder / ill["svg_file"]).read_text()
        ids = set(re.findall(r'\bid="([^"]+)"', svg))
        for a in ill["anims"]:
            if a["target"] != "camera" and a["target"] not in ids: print(f"escena {i}: target {a['target']} no existe")
            chk(a, a["target"])
        print(i, ill["svg_file"], len([a for a in ill["anims"] if a["effect"] != "hide"]), "anims")
    for e in sc.get("elements", []): chk(e, e["type"])
    if sc.get("mascot"): chk(sc["mascot"], "mascot")
print("palabras", words, "escenas", len(s["scenes"]), "title", len(s["title"]))

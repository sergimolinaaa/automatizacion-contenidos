"""uso: pv.py in.svg out.png [id_oculto ...]"""
import sys, subprocess, re
src, out, hide = sys.argv[1], sys.argv[2], sys.argv[3:]
s = open(src).read()
if hide:
    css = "<style>" + ",".join("#" + h for h in hide) + "{display:none}</style>"
    s = re.sub(r"(<svg[^>]*>)", r"\1" + css, s, count=1)
tmp = out + ".tmp.svg"
open(tmp, "w").write(s)
subprocess.run(["bash", "/tmp/claude-0/-home-user-automatizacion-contenidos/039df981-7a17-5355-b711-18510fb209db/scratchpad/ref/shot.sh", tmp, out])

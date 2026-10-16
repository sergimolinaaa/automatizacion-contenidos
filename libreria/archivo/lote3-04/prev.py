# uso: prev.py in.svg out.png "css..."   (inyecta CSS para simular estados)
import sys, subprocess, re, os
src, out, css = sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else ""
s = open(src).read()
s = re.sub(r'(<svg[^>]*>)', r'\1<style>g[id]{transform-box:fill-box;transform-origin:center} ' + css.replace('\\', '\\\\') + '</style>', s, count=1)
tmp = out + ".svg"; open(tmp, "w").write(s)
subprocess.run(["bash", "/tmp/claude-0/-home-user-automatizacion-contenidos/039df981-7a17-5355-b711-18510fb209db/scratchpad/ref/shot.sh", tmp, out])
os.remove(tmp)

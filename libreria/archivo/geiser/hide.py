import sys,re
src,out,ids=sys.argv[1],sys.argv[2],sys.argv[3].split(',')
s=open(src).read()
for i in ids:
    if i: s=s.replace(f'<g id="{i}"',f'<g id="{i}" display="none"',1)
open(out,'w').write(s)

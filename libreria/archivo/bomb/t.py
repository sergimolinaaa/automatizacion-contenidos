import sys; sys.path.insert(0,'.')
from beetle import *
print(svg_open(DEFS)+'<rect width="1000" height="700" fill="#FFF4E4"/><g transform="translate(560 360) scale(1.5)">'+shadow()+beetle()+'</g></svg>')

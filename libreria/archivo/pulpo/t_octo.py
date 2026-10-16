from lib import *
import octo
o = [header(octo.defs("rojo") + octo.defs("camu"), 1080, 1400)]
o.append('<rect width="1080" height="1400" fill="#7FC6E8"/>')
o.append('<g transform="translate(-300 0)">' + octo.body("rojo") + octo.eyes() + '</g>')
o.append('<g transform="translate(300 0)">' + octo.body("camu") + octo.eyes() + '</g>')
o.append('</svg>')
open("t_octo.svg", "w").write("\n".join(o))

import sys; sys.path.insert(0,'.')
from lib import *
from lib import _mandible
g=''.join(f'<g transform="translate({120+190*i} 300) scale(1.6)">{_mandible(-1,o)}{_mandible(1,o)}<ellipse cx="0" cy="0" rx="26" ry="18" fill="#C4A47C" stroke="#000" stroke-width="5"/></g>' for i,o in enumerate([0.4,0.62,0.9,1.15,1.4]))
print(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 700"><defs>{LARVA_DEFS}</defs><rect width="1000" height="700" fill="#F2E4C4"/>{g}</svg>')

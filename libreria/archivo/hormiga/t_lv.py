import sys; sys.path.insert(0,'.')
from lib import *
print(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 700"><defs>{LARVA_DEFS}</defs><rect width="1000" height="700" fill="#F2E4C4"/>'
 f'<g transform="translate(300 200) scale(1.8)">{larva()}</g><g transform="translate(750 200) scale(1.8)">{larva(0.4)}</g></svg>')

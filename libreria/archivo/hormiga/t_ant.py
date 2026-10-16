import sys; sys.path.insert(0,'.')
from lib import *
print(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 700"><defs>{ANT_DEFS}</defs><rect width="1000" height="700" fill="#F2E4C4"/>'
 f'<g transform="translate(300 300) scale(2.4)">{ant()}</g><g transform="translate(750 300) scale(2.4)">{ant("slip")}</g><g transform="translate(500 620) scale(2.4)">{ant(husk=True)}</g><line x1="0" y1="300" x2="1000" y2="300" stroke="red"/></svg>')

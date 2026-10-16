from lib import *; from parts import *
o=[svg_open(fish_defs()+FLY_DEFS),'<rect width="1000" height="700" fill="#BFE6FF"/>']
o.append(f'<g transform="translate(420 380) scale(1.5)">{fish()}</g>')
o.append(f'<g transform="translate(820 200) scale(2.5)">{fly()}</g><line x1="700" y1="200" x2="950" y2="200" stroke="green" stroke-width="4"/>')
o.append('</svg>'); open('t.svg','w').write("\n".join(o))

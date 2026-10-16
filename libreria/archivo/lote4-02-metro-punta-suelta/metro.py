from dib import INK, LIME, CORAL, cap, capd, arrow, tag
DEFS = '''
<linearGradient id="wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#EAF2F8"/><stop offset="1" stop-color="#D5E2EC"/></linearGradient>
<linearGradient id="bench" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E2B27A"/><stop offset="1" stop-color="#B9834E"/></linearGradient>
<linearGradient id="benchfront" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#A86F3D"/><stop offset="1" stop-color="#7E5029"/></linearGradient>
<linearGradient id="case" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFE15A"/><stop offset="0.55" stop-color="#F7BE16"/><stop offset="1" stop-color="#D49A06"/></linearGradient>
<linearGradient id="rub" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4A4E58"/><stop offset="1" stop-color="#1F2128"/></linearGradient>
<linearGradient id="blade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFF08A"/><stop offset="0.5" stop-color="#FFD83A"/><stop offset="1" stop-color="#E9B90F"/></linearGradient>
<linearGradient id="steel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F2F5F9"/><stop offset="0.5" stop-color="#BCC4D0"/><stop offset="1" stop-color="#7F8898"/></linearGradient>
<linearGradient id="steelh" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8E97A6"/><stop offset="0.4" stop-color="#E6EAF0"/><stop offset="1" stop-color="#9AA3B1"/></linearGradient>
<radialGradient id="rivet" cx="0.35" cy="0.35" r="0.7"><stop offset="0" stop-color="#FFFFFF"/><stop offset="0.5" stop-color="#C4CBD6"/><stop offset="1" stop-color="#6F7888"/></radialGradient>
<linearGradient id="wood" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F0C890"/><stop offset="1" stop-color="#C98F55"/></linearGradient>
'''

def blade_marks(x_end, y0, y1, px_cm, n, dirn=-1, fs=24, start=0, unit="cm"):
    """Marcas de la cinta. x_end = posición del cero; dirn=-1: los números crecen hacia la izquierda."""
    o = []
    h = y1 - y0
    for mm in range(start * 10, n * 10 + 1):
        x = x_end + dirn * mm * px_cm / 10
        if mm % 10 == 0:
            L = h * 0.45
        elif mm % 5 == 0:
            L = h * 0.3
        else:
            L = h * 0.18
        if mm == 0:
            continue
        o.append(f'<line x1="{x:.1f}" y1="{y0}" x2="{x:.1f}" y2="{y0+L:.1f}" stroke="{INK}" stroke-width="{2.4 if mm%10==0 else 1.5}"/>')
        o.append(f'<line x1="{x:.1f}" y1="{y1}" x2="{x:.1f}" y2="{y1-L*0.7:.1f}" stroke="{INK}" stroke-width="{2 if mm%10==0 else 1.2}"/>')
        if mm % 10 == 0 and mm > 0:
            c = mm // 10
            col = CORAL if c % 10 == 0 else INK
            o.append(f'<text x="{x - dirn*px_cm*0.16:.1f}" y="{y0+h*0.72:.1f}" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="{fs}" fill="{col}">{c}</text>')
    return "".join(o)

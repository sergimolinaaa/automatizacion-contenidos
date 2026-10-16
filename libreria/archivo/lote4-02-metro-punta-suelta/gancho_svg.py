from metro import *
import sys
FREE = len(sys.argv) > 1
T = 44; G = 44
BY0, BY1 = 380, 400          # cinta (corte)
TY0 = BY0 - T                # placa del gancho
PX = 820                     # cara interior de la pestaña
R = (470, 680)
o = [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 700">
<defs>{DEFS}
<radialGradient id="bg" cx="0.55" cy="0.5" r="0.8"><stop offset="0" stop-color="#F6FAFF"/><stop offset="1" stop-color="#D6E6F5"/></radialGradient>
</defs>
'''+ ("" if FREE else '<rect width="1000" height="700" fill="url(#bg)"/><g stroke="#C3D7EA" stroke-width="2">' + "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="700"/>' for x in range(0, 1001, 50)) + "".join(f'<line x1="0" y1="{y}" x2="1000" y2="{y}"/>' for y in range(0, 701, 50)) + '</g>')]
# cinta (fija) con remaches
o.append('<g id="cinta">')
o.append(f'<rect x="{60 if FREE else -20}" y="{BY0}" width="{PX-(60 if FREE else -20)}" height="{BY1-BY0}" fill="url(#blade)" stroke="{INK}" stroke-width="5"/>')
o.append(f'<text x="580" y="{BY1+44}" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="26" fill="{"#FFFFFF" if FREE else "#8A6A10"}">CINTA</text>')
o.append('</g>')
# gancho (se desliza)
o.append('<g id="hook">')
segs = [(300, R[0] - 16 - G), (R[0] + 16, R[1] - 16 - G), (R[1] + 16, PX)]
for a, b in segs:
    o.append(f'<rect x="{a}" y="{TY0}" width="{b-a}" height="{T}" fill="url(#steel)" stroke="{INK}" stroke-width="5"/>')
o.append(f'<path d="M {PX-4} {TY0} L {PX+T-12} {TY0} Q {PX+T} {TY0} {PX+T} {TY0+12} L {PX+T} 520 L {PX} 520 L {PX} {TY0+T} L {PX-4} {TY0+T} Z" fill="url(#steelh)" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
o.append(f'<line x1="304" y1="{TY0+6}" x2="{PX+6}" y2="{TY0+6}" stroke="#FFFFFF" stroke-width="3" opacity="0.8"/>')
o.append('</g>')
# remaches (fijos a la cinta)
o.append('<g id="remaches">')
for rx in R:
    o.append(f'<rect x="{rx-16}" y="{TY0-4}" width="32" height="{BY1-TY0+8}" fill="#9AA3B1" stroke="{INK}" stroke-width="4"/>')
    o.append(f'<path d="M {rx-44} {TY0} C {rx-40} {TY0-20} {rx+40} {TY0-20} {rx+44} {TY0} Z" fill="url(#rivet)" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    o.append(f'<path d="M {rx-40} {BY1} C {rx-36} {BY1+16} {rx+36} {BY1+16} {rx+40} {BY1} Z" fill="url(#rivet)" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
o.append('</g>')
# huecos de holgura resaltados
o.append(f'<g id="huecos">' + "".join(f'<rect x="{rx-16-G+3}" y="{TY0+3}" width="{G-6}" height="{T-6}" rx="4" fill="{LIME}" opacity="0.9"/>' for rx in R) + '</g>')
# cotas
def cota(id_, x1, x2, y, label, w, up=True, col=CORAL):
    ty = y - 74 if up else y + 18
    return (f'<g id="{id_}"><path d="M {x1} {y-14} L {x1} {y+14} M {x2} {y-14} L {x2} {y+14} M {x1} {y} L {x2} {y}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
            f'<rect x="{(x1+x2)/2-w/2}" y="{ty}" width="{w}" height="56" rx="12" fill="{col}" stroke="{INK}" stroke-width="4"/>'
            f'<text x="{(x1+x2)/2}" y="{ty+39}" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="28" fill="{INK}">{label}</text></g>')
o.append(cota("choL", R[1] - 16 - G, R[1] - 16, 290, "HOLGURA", 190, col=LIME))
o.append(cota("cgrosor", PX, PX + T, 556, "GROSOR", 150, up=False, col=LIME))
o.append(f'<g id="igual"><circle cx="930" cy="440" r="40" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/><text x="930" y="458" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="50" fill="{INK}">=</text></g>')
o.append(tag("lremache", 160, 480, 200, "REMACHE", 300, 480, R[0] - 20, BY1 + 12))
o.append(f'<g id="zoomtag"><rect x="860" y="40" width="110" height="50" rx="25" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/><text x="915" y="75" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="26" fill="{INK}">×10</text></g>')
# vista desde arriba (recuadro)
o.append('<g id="arriba">')
o.append(f'<rect x="40" y="90" width="380" height="200" rx="18" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/>')
o.append(f'<text x="230" y="126" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="22" fill="#5D6676">VISTA DE ARRIBA</text>')
o.append(f'<rect x="60" y="150" width="320" height="100" fill="url(#blade)" stroke="{INK}" stroke-width="4"/>')
o.append(blade_marks(380, 152, 248, 60, 5, fs=20).replace('font-size="20"', 'font-size="20" opacity="0"'))
o.append(f'<rect x="230" y="146" width="150" height="108" rx="8" fill="url(#steel)" stroke="{INK}" stroke-width="4"/>')
o.append(f'<rect x="380" y="146" width="16" height="108" rx="4" fill="#8E97A6" stroke="{INK}" stroke-width="4"/>')
for sx in (262, 332):
    o.append(f'<rect x="{sx-20}" y="{186}" width="40" height="28" rx="14" fill="#4A5160" stroke="{INK}" stroke-width="3"/>')
    o.append(f'<circle cx="{sx+6}" cy="200" r="12" fill="url(#rivet)" stroke="{INK}" stroke-width="3"/>')
o.append('</g>')
# martillo (no lo arregles)
o.append('<g id="martillo"><g transform="rotate(-35 640 160)">'
         f'<rect x="630" y="120" width="22" height="190" rx="8" fill="#C98F55" stroke="{INK}" stroke-width="6"/>'
         f'<rect x="590" y="88" width="110" height="46" rx="8" fill="url(#steel)" stroke="{INK}" stroke-width="6"/>'
         f'<rect x="690" y="96" width="24" height="30" rx="4" fill="#8E97A6" stroke="{INK}" stroke-width="5"/></g></g>')
o.append(f'<g id="prohibido"><circle cx="640" cy="200" r="120" fill="none" stroke="{INK}" stroke-width="30"/><circle cx="640" cy="200" r="120" fill="none" stroke="{CORAL}" stroke-width="18"/>'
         f'<path d="M 555 115 L 725 285" stroke="{INK}" stroke-width="30" stroke-linecap="round"/><path d="M 555 115 L 725 285" stroke="{CORAL}" stroke-width="18" stroke-linecap="round"/></g>')
o.append('</svg>')
open("gancho_free.svg" if FREE else "gancho.svg", "w").write("\n".join(o))

from vx import *

OUT = "competencias_free.svg"
defs = BASE_DEFS + VX_DEFS + lg("roofS", [(0, "#F7F4EE"), (1, "#CFC8B8")])
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000">\n<defs>{defs}</defs>']

# edificio ESTADO (genérico, columnas)
BX, BT, BW = 500, 90, 520
x0 = BX - BW / 2
e = f'<ellipse cx="{BX}" cy="402" rx="300" ry="22" fill="{INK}" opacity="0.25"/>'
e += f'<path d="M {x0-20} 170 L {BX} 90 L {x0+BW+20} 170 Z" fill="url(#roofS)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
e += f'<rect x="{x0-10}" y="166" width="{BW+20}" height="34" rx="4" fill="url(#stoneG)" stroke="{INK}" stroke-width="6"/>'
e += T(BX, 193, "ESTADO", 28, INK, font=DISP)
for k in range(6):
    cx = x0 + 40 + k * (BW - 80) / 5
    e += f'<rect x="{f(cx-18)}" y="200" width="36" height="160" fill="url(#stoneG)" stroke="{INK}" stroke-width="5"/>'
    e += f'<path d="M {f(cx-6)} 210 L {f(cx-6)} 350" stroke="#FFFFFF" stroke-width="5" opacity="0.8"/>'
e += f'<rect x="{x0-30}" y="358" width="{BW+60}" height="34" rx="4" fill="url(#stoneG)" stroke="{INK}" stroke-width="6"/>'
e += f'<path d="M {BX-60} 148 Q {BX} 118 {BX+60} 148" fill="none" stroke="#B9B09C" stroke-width="5"/>'
o.append(G("estado", e))

# caja de comunidades (abajo)
cb = f'<rect x="78" y="660" width="860" height="230" rx="26" fill="{INK}" opacity="0.25" transform="translate(8 10)"/>'
cb += f'<rect x="78" y="660" width="860" height="230" rx="26" fill="url(#cardG)" stroke="{INK}" stroke-width="7"/>'
cb += f'<rect x="78" y="660" width="860" height="56" rx="26" fill="url(#navyG)" stroke="{INK}" stroke-width="6"/>'
cb += T(508, 699, "COMUNIDADES AUTÓNOMAS", 28, "#FFFFFF", font=DISP)
o.append(G("ccaa", cb))

# fichas de competencias (en la caja) -> suben al Estado
def ficha(cx, cy, name, icon, col):
    return (f'<circle cx="{f(cx+5)}" cy="{f(cy+7)}" r="62" fill="{INK}" opacity="0.25"/>'
            f'<circle cx="{f(cx)}" cy="{f(cy)}" r="62" fill="{col}" stroke="{INK}" stroke-width="6"/>'
            f'<circle cx="{f(cx)}" cy="{f(cy)}" r="50" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/>' + icon
            + f'<rect x="{f(cx-text_w(name,18)/2)}" y="{f(cy+58)}" width="{f(text_w(name,18))}" height="34" rx="9" fill="{INK}"/>'
            + T(cx, cy + 82, name, 18, "#FFFFFF"))

def i_san(cx, cy):
    return f'<path d="M {f(cx-10)} {f(cy-30)} h 20 v 20 h 20 v 20 h -20 v 20 h -20 v -20 h -20 v -20 h 20 Z" fill="{CORAL}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
def i_edu(cx, cy):
    return (f'<path d="M {f(cx)} {f(cy-14)} Q {f(cx-18)} {f(cy-26)} {f(cx-36)} {f(cy-20)} L {f(cx-36)} {f(cy+22)} Q {f(cx-18)} {f(cy+16)} {f(cx)} {f(cy+26)} Z" fill="#5C78E8" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
            f'<path d="M {f(cx)} {f(cy-14)} Q {f(cx+18)} {f(cy-26)} {f(cx+36)} {f(cy-20)} L {f(cx+36)} {f(cy+22)} Q {f(cx+18)} {f(cy+16)} {f(cx)} {f(cy+26)} Z" fill="#7F96F2" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')
def i_seg(cx, cy):
    return f'<path d="M {f(cx)} {f(cy-32)} L {f(cx+28)} {f(cy-20)} Q {f(cx+28)} {f(cy+18)} {f(cx)} {f(cy+32)} Q {f(cx-28)} {f(cy+18)} {f(cx-28)} {f(cy-20)} Z" fill="url(#steelG)" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>' + f'<path d="M {f(cx)} {f(cy-20)} L {f(cx)} {f(cy+20)}" stroke="#FFFFFF" stroke-width="4" opacity="0.7"/>'
def i_jus(cx, cy):
    return (f'<path d="M {f(cx)} {f(cy-30)} L {f(cx)} {f(cy+24)} M {f(cx-16)} {f(cy+26)} L {f(cx+16)} {f(cy+26)} M {f(cx-30)} {f(cy-18)} L {f(cx+30)} {f(cy-18)}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
            f'<path d="M {f(cx-40)} {f(cy+4)} Q {f(cx-30)} {f(cy+16)} {f(cx-20)} {f(cy+4)} Z M {f(cx+20)} {f(cy+4)} Q {f(cx+30)} {f(cy+16)} {f(cx+40)} {f(cy+4)} Z" fill="{YEL}" stroke="{INK}" stroke-width="4"/>'
            f'<path d="M {f(cx-30)} {f(cy-18)} L {f(cx-38)} {f(cy+4)} M {f(cx-30)} {f(cy-18)} L {f(cx-22)} {f(cy+4)} M {f(cx+30)} {f(cy-18)} L {f(cx+22)} {f(cy+4)} M {f(cx+30)} {f(cy-18)} L {f(cx+38)} {f(cy+4)}" stroke="{INK}" stroke-width="3"/>')

FY = 780
fx = [200, 400, 600, 800]
for id_, x, n, ic, col in (("fsan", fx[0], "SANIDAD", i_san, CORAL), ("fedu", fx[1], "EDUCACIÓN", i_edu, "#5C78E8"),
                           ("fseg", fx[2], "SEGURIDAD", i_seg, "#9AA3B5"), ("fjus", fx[3], "JUSTICIA", i_jus, YEL)):
    o.append(G(id_, ficha(x, FY, n, ic(x, FY), col)))

# flecha de subida y etiquetas
o.append(arrow("fl", ((500, 640), (500, 440)), col=LIME, w=14, head=34))
s, _ = label("tdev", 500, 560, "DEVOLVER AL ESTADO", bg=INK, fg=LIME, size=28); o.append(s)
s, _ = label("tdefca", 500, 612, "= GOBIERNOS DE CADA REGIÓN", bg=CORAL, fg="#FFFFFF", size=26); o.append(s)
s, _ = label("tmas", 500, 470, "+ SEGURIDAD Y JUSTICIA", bg=CORAL, fg="#FFFFFF", size=26); o.append(s)
o.append("</svg>")
save(OUT, "\n".join(o))

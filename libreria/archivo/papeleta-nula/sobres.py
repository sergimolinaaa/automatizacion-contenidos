from pn import *

OUT = "sobres_free.svg"
o = [header(1000, 900, SEPIA)]
EW, EH, ECY = 400, 270, 400
L, R = 255, 745


def pap(cx, cy, sh, rot):
    b, _ = ballot(cx, cy, 220, 300, sh, rows=4, title=False)
    return f'<g transform="rotate({rot} {cx} {cy})">{b}</g>'


def folio(cx, cy, rot):
    return (f'<g transform="rotate({rot} {cx} {cy})"><rect x="{cx-110}" y="{cy-150}" width="220" height="300" rx="5" fill="#FFFFFF" stroke="{INK}" stroke-width="6"/>'
            f'<path d="M {cx-95} {cy-135} L {cx-95} {cy+70}" stroke="#E4E7EF" stroke-width="6" stroke-linecap="round"/></g>')


o.append(g("sd", envelope(L, ECY, EW, EH, pap(L - 45, ECY - 70, "star", -10) + pap(L + 45, ECY - 60, "circle", 9))))
o.append(g("si", envelope(R, ECY, EW, EH, pap(R - 40, ECY - 70, "star", -8) + pap(R + 40, ECY - 62, "star", 7))))
o.append(g("sv", envelope(L, ECY, EW, EH)))
o.append(g("sf", envelope(R, ECY, EW, EH, folio(R, ECY - 70, 4))))
# etiquetas
for id_, x, t, bg, fg in (("ldist", L, "DISTINTAS", INK, LIME), ("ligual", R, "IGUALES", INK, LIME),
                          ("lvacio", L, "SOBRE VACÍO", INK, LIME), ("lfolio", R, "FOLIO EN BLANCO", INK, LIME)):
    s, _ = label(id_, x, 48, t, bg=bg, fg=fg, size=38); o.append(s)
o.append(cross(L, 680, 70, id_="xd"))
o.append(check(R, 680, 70, id_="okv"))
o.append(check(L, 680, 70, id_="okb"))
o.append(cross(R, 680, 70, id_="xf"))
for id_, x, t, bg, fg in (("lnulo", L, "NULO", CORAL, "#FFFFFF"), ("l1voto", R, "= 1 VOTO", LIME, INK),
                          ("lblanco", L, "VOTO EN BLANCO", LIME, INK), ("lnulo2", R, "NULO", CORAL, "#FFFFFF")):
    s, _ = label(id_, x, 800, t, bg=bg, fg=fg, size=38); o.append(s)
o.append("</svg>")
save(OUT, "\n".join(o))

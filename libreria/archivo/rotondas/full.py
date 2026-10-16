from rot import *
import json

P = {}  # poses (x, y, hd) de cada coche para el guion


def C(id_, x, y, hd, col, **kw):
    P[id_] = (round(x, 1), round(y, 1), round(hd, 1))
    return car(id_, x, y, hd, col, **kw)


def pose(th, r):
    x, y = polar(th, r)
    return (x, y, -th)


# ---------------- rotonda_full.svg: gancho (S0), cedes el paso (S1), error clásico (S5) ----------------
o = [header(1080, 1920), base()]
EXIT_W = (110, CY - LANE)
mal = arc(95, 132, R_IN_L) + [(330, 800), (232, 815), EXIT_W]
o.append(route("ruta_mal", mal, CORAL, 14))
# S1: coche que entra (espera en el ramal este) y coche que ya circula
ex, ey = CX + R_OUT + 72, CY - LANE
o.append(C("espera", ex, ey, -90, "azul"))
o.append(C("dentro", *pose(-70, R_OUT_L), "blanco"))
o.append(ceda_sign("ceda", 980, 690, 1.0))
# S0 (estático) y S5 (animado)
o.append(C("blanco", 330, 691, -138, "blanco"))
o.append(C("rojo", 322, 806, -100, "rojo"))
o.append(C("blanco5", *pose(100, R_OUT_L), "blanco"))
o.append(C("rojo5", *pose(95, R_IN_L), "rojo"))
o.append(horn("piii", 190, 690, r=54))
# etiquetas
s, _ = label("tcorta", 210, 965, "EL QUE CORTA", target=(300, 830), bg=CORAL, fg="#FFFFFF", size=28, src=(240, 940)); o.append(s)
s, _ = label("tnodeja", 330, 600, "EL QUE NO LO DEJA", target=(330, 660), bg=INK, fg=LIME, size=28); o.append(s)
s, _ = label("tpref", CX, CY, "PREFERENCIA", bg=LIME, fg=INK, size=28); o.append(s)
s, _ = label("tdentro", CX, CY - 64, "DENTRO", bg=INK, fg="#FFFFFF", size=24); o.append(s)
s, _ = label("tcedes", 895, 1060, "CEDES EL PASO", target=(940, 845), bg="#FFFFFF", fg=INK, size=28, src=(940, 1040)); o.append(s)
o.append(crossmark("mal", 205, 875, 30))
o.append(checkmark("bien", 525, 600, 30))
o.append(gps("recalc", 64, 470, 540, None, "Recalculando…", None, col=CORAL, icon="recalc"))
o.append(g("duda", f'<circle cx="625" cy="640" r="52" fill="#FFE14D" stroke="{INK}" stroke-width="6"/>' + T(625, 666, "?", 70, INK, font=DISP)))
o.append("</svg>")
save(OUT + "rotonda_full.svg", "\n".join(o))

# ---------------- ruta_full.svg: GPS + carriles (S3, S4, S6) ----------------
o = [header(1080, 1920), base()]
ent = [(CX + LANE, 1260), (CX + LANE + 20, 1180), polar(-45, 228), polar(-20, R_IN_L)] + arc(-20, 112, R_IN_L)[1:]
o.append(route("ruta_in", ent, "#3DA5FF", 16))
sal = arc(110, 128, R_IN_L) + [polar(140, 255), polar(151, 283), polar(161, 303), (200, CY - LANE - 2), EXIT_W]
o.append(route("ruta_out", sal, LIME, 16))
vuelta = arc(195, 505, R_OUT_L) + [polar(153, 288), polar(161, 303), (200, CY - LANE - 2), EXIT_W]
o.append(route("ruta_vuelta", vuelta, "#36D17E", 16))
o.append(C("tu3", CX + LANE, 1240, 0, "amarillo", tag="TÚ", s=1.15))
o.append(C("tu4", *pose(110, R_IN_L), "amarillo", tag="TÚ", s=1.15, blink=True))
o.append(C("tu6", *pose(195, R_OUT_L), "amarillo", tag="TÚ", s=1.15))
o.append(badge("b1", 1000, 1060, "1"))
o.append(badge("b2", 800, 565, "2"))
o.append(badge("b3", 80, 715, "3"))
s, _ = label("ldentro", *polar(-128, R_IN_L), "DENTRO", bg=INK, fg="#FFFFFF", size=22); o.append(s)
s, _ = label("lfuera", *polar(-128, R_OUT_L + 8), "FUERA", bg=LIME, fg=INK, size=22); o.append(s)
s, _ = label("lint", 300, 628, "INTERMITENTE", target=polar(118, R_IN_L), bg="#FFB020", fg=INK, size=26, src=(330, 640)); o.append(s)
s, _ = label("lgratis", CX, CY, "GRATIS", bg=LIME, fg=INK, size=34); o.append(s)
o.append(gps("gps3", 24, 452, 720, "en 60 m", "Toma la 3.ª salida", None, badge="3.ª"))
o.append(gps("gpsv", 24, 452, 720, "Recalculando…", "Da otra vuelta", None, col="#36D17E", icon="loop"))
# bocina tachada
o.append(g("sinpiii", horn("_h", 870, 1180, r=50)[len('<g id="_h">'):-4]
           + f'<path d="M 800 1130 L 940 1230" stroke="{CORAL}" stroke-width="14" stroke-linecap="round"/>'))
o.append("</svg>")
save(OUT + "ruta_full.svg", "\n".join(o))
json.dump(P, open("poses.json", "w"), indent=1)

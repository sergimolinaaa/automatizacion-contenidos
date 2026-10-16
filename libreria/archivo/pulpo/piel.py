import math, random
from lib import *
X0, X1 = 40, 620          # cara frontal
YT, YB = 180, 560
DX, DY = 80, -80          # profundidad (cara superior/lateral)
L_EPI, L_CRO, L_IRI, L_LEU = 200, 300, 390, 470  # límites inferiores de capa
defs = (lg("bgw", [(0, "#BFE6FF"), (1, "#E9F6FF")]) +
        lg("epi", [(0, "#FFF4EE"), (1, "#F9E3D8")]) + lg("derm", [(0, "#F6D6C8"), (1, "#EEC4B4")]) +
        lg("iri", [(0, "#DDEBFF"), (1, "#C8DDF5")]) + lg("leu", [(0, "#F8FAFC"), (1, "#E6ECF2")]) +
        lg("musc", [(0, "#E79A92"), (1, "#C7665E")]) +
        lg("plate", [(0, "#4FD1C5"), (0.5, "#5B8CFF"), (1, "#A06BFF")], 0, 0, 1, 0) +
        lg("topskin", [(0, "#F7CDBE"), (1, "#E9A792")]) +
        rg("am", [(0, "#FFE070"), (1, "#E0A800")], 0.4, 0.35, 0.7) + rg("ro", [(0, "#FF7A5E"), (1, "#B8241A")], 0.4, 0.35, 0.7) +
        rg("ma", [(0, "#9A6A48"), (1, "#3E2414")], 0.4, 0.35, 0.7) + lg("crono", [(0, "#FFFFFF"), (1, "#DCE3EA")]))
o = [header(defs)]
o.append('<rect width="1000" height="700" fill="url(#bgw)"/>')
# agua: partículas
random.seed(2)
o.append('<g fill="#FFFFFF" opacity="0.6">' + "".join(f'<circle cx="{random.uniform(0, 1000):.0f}" cy="{random.uniform(0, 700):.0f}" r="{random.uniform(1.5, 4):.1f}"/>' for _ in range(40)) + '</g>')
# sombra del bloque
o.append(f'<path d="M {X0 + 20} {YB + 14} L {X1 + 30} {YB + 14} L {X1 + DX + 20} {YB + DY + 10} L {X1 + DX + 20} {YB + 30} L {X0 + 20} {YB + 30} Z" fill="#000" opacity="0.08"/>')
# ---- cara superior (superficie de la piel) ----
top = [(X0, YT), (X0 + DX, YT + DY), (X1 + DX, YT + DY), (X1, YT)]
o.append(f'<path d="{poly(top, True)}" fill="url(#topskin)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
random.seed(7)
spots = []
for _ in range(60):
    u, v = random.uniform(0.04, 0.96), random.uniform(0.12, 0.9)
    x = X0 + u * (X1 - X0) + v * DX
    y = YT + v * DY
    k = random.choice(["am", "ro", "ro", "ma"])
    r = random.uniform(6, 16)
    spots.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r:.1f}" ry="{r * 0.45:.1f}" fill="url(#{k})" stroke="{INK}" stroke-width="2"/>')
o.append('<g id="superficie">' + "".join(spots) + '</g>')
# ---- cara lateral ----
side = [(X1, YT), (X1 + DX, YT + DY), (X1 + DX, YB + DY), (X1, YB)]
o.append(f'<path d="{poly(side, True)}" fill="#E8B8A6" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
for yl, col in ((L_EPI, "#F3DCD2"), (L_CRO, "#E3B2A0"), (L_IRI, "#B9CDEB"), (L_LEU, "#E9EEF3")):
    pass
bands = [(YT, L_EPI, "#F6E2D8"), (L_EPI, L_CRO, "#E7BBA9"), (L_CRO, L_IRI, "#B4C8E8"), (L_IRI, L_LEU, "#E4EAF0"), (L_LEU, YB, "#D69C90")]
for a, b, col in bands:
    o.append(f'<path d="{poly([(X1, a), (X1 + DX, a + DY), (X1 + DX, b + DY), (X1, b)], True)}" fill="{col}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>')
o.append(f'<path d="{poly(side, True)}" fill="none" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
# ---- cara frontal: capas ----
o.append(f'<rect x="{X0}" y="{YT}" width="{X1 - X0}" height="{L_EPI - YT}" fill="url(#epi)"/>')
o.append(f'<rect x="{X0}" y="{L_EPI}" width="{X1 - X0}" height="{L_CRO - L_EPI}" fill="url(#derm)"/>')
o.append(f'<rect x="{X0}" y="{L_CRO}" width="{X1 - X0}" height="{L_IRI - L_CRO}" fill="url(#iri)"/>')
o.append(f'<rect x="{X0}" y="{L_IRI}" width="{X1 - X0}" height="{L_LEU - L_IRI}" fill="url(#leu)"/>')
o.append(f'<rect x="{X0}" y="{L_LEU}" width="{X1 - X0}" height="{YB - L_LEU}" fill="url(#derm)"/>')
# células de la epidermis
o.append('<g fill="none" stroke="#E2B9A8" stroke-width="2.5">' + "".join(f'<rect x="{x}" y="{YT + 3}" width="34" height="14" rx="6"/>' for x in range(X0 + 4, X1 - 30, 38)) + '</g>')
# cromatóforos: cerrados y abiertos (vistos de lado: lentejas aplanadas)
CR = [(110, 228, "am"), (230, 236, "ro"), (350, 226, "am"), (450, 262, "ma"), (540, 240, "ro"), (170, 270, "ma"), (300, 276, "ro"), (420, 232, "am"), (580, 280, "ma")]
ab, ce = ['<g id="cr_abiertos">'], ['<g id="cr_cerrados">']
for x, y, k in CR:
    ab.append(f'<path d="M {x - 62} {y} L {x - 40} {y}" stroke="#C7665E" stroke-width="5" stroke-linecap="round"/><path d="M {x + 40} {y} L {x + 62} {y}" stroke="#C7665E" stroke-width="5" stroke-linecap="round"/>')
    ab.append(f'<ellipse cx="{x}" cy="{y}" rx="46" ry="13" fill="url(#{k})" stroke="{INK}" stroke-width="3.5"/>')
    ce.append(f'<path d="M {x - 62} {y} Q {x - 40} {y - 6} {x - 14} {y}" stroke="#C7665E" stroke-width="3" fill="none" stroke-linecap="round"/><path d="M {x + 14} {y} Q {x + 40} {y - 6} {x + 62} {y}" stroke="#C7665E" stroke-width="3" fill="none" stroke-linecap="round"/>')
    ce.append(f'<ellipse cx="{x}" cy="{y}" rx="14" ry="12" fill="url(#{k})" stroke="{INK}" stroke-width="3.5"/>')
ab.append('</g>'); ce.append('</g>')
o.append("".join(ce)); o.append("".join(ab))
# iridóforos: pilas de placas
IR = ['<g id="iridoforos">']
for i, x in enumerate(range(X0 + 20, X1 - 60, 72)):
    y0 = L_CRO + 14 + (i % 2) * 10
    IR.append(f'<rect x="{x}" y="{y0}" width="62" height="62" rx="14" fill="#EAF2FF" stroke="#8FA6C8" stroke-width="3"/>')
    for k in range(6):
        IR.append(f'<rect x="{x + 8}" y="{y0 + 8 + k * 9}" width="46" height="5" rx="2.5" fill="url(#plate)"/>')
IR.append('</g>')
o.append("".join(IR))
# leucóforos: células blancas granulosas
LE = ['<g id="leucoforos">']
random.seed(5)
for x in range(X0 + 26, X1 - 20, 46):
    y = L_IRI + 40 + random.uniform(-8, 8)
    LE.append(f'<circle cx="{x}" cy="{y:.0f}" r="20" fill="#FFFFFF" stroke="#9AA8B8" stroke-width="3"/>')
    for _ in range(5):
        LE.append(f'<circle cx="{x + random.uniform(-10, 10):.0f}" cy="{y + random.uniform(-10, 10):.0f}" r="3" fill="#D5DEE8"/>')
LE.append('</g>')
o.append("".join(LE))
# músculo y dermis profunda
o.append('<g stroke="#C7665E" stroke-width="4" fill="none" opacity="0.7">' + "".join(f'<path d="M {X0 + 6} {y} C 200 {y - 8}, 400 {y + 8}, {X1 - 6} {y}"/>' for y in range(L_LEU + 18, YB - 8, 16)) + '</g>')
# nervios (del cerebro): suben hasta los músculos de los cromatóforos
NV = ['<g id="nervios">']
trunk = f"M {X0 - 30} 530 C 150 528, 300 520, 590 516"
NV.append(dbl(trunk, 8, "#FFD23F", 7))
for x, y, k in CR[:5]:
    NV.append(dbl(f"M {x + 30} 520 C {x + 36} 450, {x + 50} 360, {x + 52} {y + 6}", 4, "#FFD23F", 5))
NV.append('</g>')
o.append("".join(NV))
o.append(f'<g id="pulsos"><circle cx="{X0 - 10}" cy="530" r="11" fill="{LIME}" stroke="{INK}" stroke-width="4"/><circle cx="{X0 - 60}" cy="530" r="8" fill="{LIME}" stroke="{INK}" stroke-width="3"/></g>')
# opsinas en la piel
OP = ['<g id="opsinas">']
for x in range(X0 + 40, X1 - 20, 92):
    OP.append(f'<circle cx="{x}" cy="{YT + 10}" r="9" fill="#B06BFF" stroke="{INK}" stroke-width="3"/><path d="M {x} {YT + 1} L {x} {YT - 12}" stroke="{INK}" stroke-width="3"/><circle cx="{x}" cy="{YT - 14}" r="4" fill="#E9D5FF" stroke="{INK}" stroke-width="2"/>')
OP.append('</g>')
o.append("".join(OP))
# contorno de la cara frontal y líneas de capa
for yl in (L_EPI, L_CRO, L_IRI, L_LEU):
    o.append(f'<path d="M {X0} {yl} L {X1} {yl}" stroke="{INK}" stroke-width="2.5" opacity="0.5"/>')
o.append(f'<rect x="{X0}" y="{YT}" width="{X1 - X0}" height="{YB - YT}" fill="none" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
o.append(f'<path d="M {X0 + 4} {YT + 4} L {X0 + DX + 2} {YT + DY + 4}" stroke="#FFFFFF" stroke-width="3" opacity="0.7"/>')
# ---- luz ----
def ray(id_, pts, col, w=8):
    return arrow(id_, pts[0][0], pts[0][1], pts[1][0], pts[1][1], col, w, 24)
o.append(ray("luz_iri", [(170, 52), (260, 330)], "#FFF3A0"))
o.append('<g id="refl_iri">' + arrow(None, 280, 330, 380, 60, "#43C6B8", 8, 24) + arrow(None, 300, 335, 460, 70, "#5B8CFF", 8, 24) + '</g>')
o.append(ray("luz_leu", [(500, 52), (470, 415)], "#FFF3A0"))
o.append('<g id="refl_leu">' + arrow(None, 470, 420, 400, 120, "#FFFFFF", 7, 22) + arrow(None, 478, 420, 560, 110, "#FFFFFF", 7, 22) + arrow(None, 486, 420, 680, 170, "#FFFFFF", 7, 22) + '</g>')
# ---- etiquetas (columna derecha) ----
def lab(id_, cy, text, tx, ty, size=26):
    s, _ = tag(id_, 865, cy, text, size=size)
    w = text_w(text, size)
    return s.replace(f'<g id="{id_}">', f'<g id="{id_}"><line x1="{865 - w / 2:.0f}" y1="{cy}" x2="{tx}" y2="{ty}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/><circle cx="{tx}" cy="{ty}" r="8" fill="{LIME}" stroke="{INK}" stroke-width="4"/>')
o.append(lab("l_cro", 236, "CROMATÓFOROS", 582, 240))
o.append(lab("l_iri", 340, "IRIDÓFOROS", 560, 345))
o.append(lab("l_leu", 430, "LEUCÓFOROS", 560, 432))
o.append(lab("l_ops", 150, "OPSINAS", 592, 168))
s, _ = tag("l_cer", 175, 612, "DEL CEREBRO", size=26)
o.append(s.replace('<g id="l_cer">', f'<g id="l_cer"><line x1="110" y1="583" x2="60" y2="532" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'))
# cronómetro y signo de pregunta
cx, cy = 860, 560
C = [f'<g id="crono"><rect x="{cx - 11}" y="{cy - 78}" width="22" height="18" rx="4" fill="#C7CFD8" stroke="{INK}" stroke-width="4"/>',
     f'<circle cx="{cx}" cy="{cy}" r="64" fill="url(#crono)" stroke="{INK}" stroke-width="6"/>',
     f'<path d="M {cx} {cy} L {cx + 50 * math.sin(math.radians(80)):.0f} {cy - 50 * math.cos(math.radians(80)):.0f} A 50 50 0 0 0 {cx} {cy - 50} Z" fill="{LIME}"/>',
     f'<path d="M {cx} {cy} L {cx} {cy - 50}" stroke="{CORAL}" stroke-width="6" stroke-linecap="round"/><circle cx="{cx}" cy="{cy}" r="6" fill="{INK}"/>',
     txt(cx, cy + 36, "&lt;1 s", 22), '</g>']
o.append("".join(C))
o.append(f'<g id="interroga"><circle cx="{cx}" cy="{cy}" r="62" fill="{CORAL}" stroke="{INK}" stroke-width="6"/>' + txt(cx, cy + 30, "?", 86, "#FFFFFF") + '</g>')
o.append('</svg>')
open("piel.svg", "w").write("\n".join(o))

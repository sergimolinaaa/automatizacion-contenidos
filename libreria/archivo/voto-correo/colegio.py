import sys, math
from vc import *

OUT = sys.argv[1] if len(sys.argv) > 1 else "colegio_full.svg"
defs = BASE_DEFS + EXTRA_DEFS + lg("wallC", [(0, "#E3EEDF"), (1, "#C8DCC2")]) + lg("floorC", [(0, "#C9B79C"), (1, "#9C8665")]) \
    + lg("cloth", [(0, "#F7F8FB"), (1, "#D6DAE4")]) + rg("clockF", [(0, "#FFFFFF"), (1, "#E7EAF0")]) + lg("plaque", [(0, "#2F5BD3"), (1, "#1D3C99")]) \
    + lg("sleeve", [(0, "#7A8AA8"), (1, "#4E5D7A")]) + lg("skinH", [(0, "#F1C6A4"), (1, "#D9997A")])
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920">\n<defs>{defs}</defs>']
o.append('<rect width="1080" height="1920" fill="url(#wallC)"/>')
# zócalo y suelo
o.append(f'<rect x="0" y="1060" width="1080" height="200" fill="#A9C4A0"/><path d="M 0 1060 L 1080 1060" stroke="{INK}" stroke-width="6"/>')
o.append(f'<rect x="0" y="1260" width="1080" height="660" fill="url(#floorC)"/><path d="M 0 1260 L 1080 1260" stroke="{INK}" stroke-width="7"/>')
o.append('<g stroke="#8A7455" stroke-width="3" opacity="0.6">' + "".join(f'<line x1="{x}" y1="1262" x2="{x*1.6-324}" y2="1920"/>' for x in range(0, 1200, 120))
         + "".join(f'<line x1="0" y1="{y}" x2="1080" y2="{y}"/>' for y in (1340, 1460, 1620, 1820)) + "</g>")
# ventana al fondo (izquierda)
o.append(f'<rect x="70" y="600" width="250" height="330" rx="10" fill="#BFE4FF" stroke="{INK}" stroke-width="7"/>')
o.append(f'<path d="M 195 600 L 195 930 M 70 765 L 320 765" stroke="{INK}" stroke-width="7"/>')
o.append('<path d="M 100 640 L 160 640 L 100 720 Z" fill="#FFFFFF" opacity="0.6"/>')
o.append(f'<rect x="56" y="930" width="278" height="20" rx="6" fill="#F2F2F2" stroke="{INK}" stroke-width="6"/>')
# cartel COLEGIO ELECTORAL
o.append(f'<g id="cartel"><rect x="360" y="470" width="420" height="110" rx="16" fill="url(#plaque)" stroke="{INK}" stroke-width="7"/>'
         f'<rect x="374" y="484" width="392" height="82" rx="10" fill="none" stroke="#9DB6FF" stroke-width="3"/>'
         + T(570, 518, "COLEGIO", 32, "#FFFFFF", font=DISP) + T(570, 556, "ELECTORAL", 32, "#FFFFFF", font=DISP) + "</g>")
# reloj
CX, CY, R = 870, 700, 120
o.append(f'<g id="reloj"><circle cx="{CX+8}" cy="{CY+10}" r="{R+14}" fill="{INK}" opacity="0.22"/>'
         f'<circle cx="{CX}" cy="{CY}" r="{R+14}" fill="#3A445C" stroke="{INK}" stroke-width="7"/>'
         f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="url(#clockF)" stroke="{INK}" stroke-width="5"/>')
for h in range(12):
    a = math.radians(h * 30 - 90)
    r1, r2 = (R - 26, R - 8) if h % 3 else (R - 34, R - 8)
    o.append(f'<line x1="{f(CX+r1*math.cos(a))}" y1="{f(CY+r1*math.sin(a))}" x2="{f(CX+r2*math.cos(a))}" y2="{f(CY+r2*math.sin(a))}" stroke="{INK}" stroke-width="{7 if h % 3 == 0 else 4}" stroke-linecap="round"/>')
o.append("</g>")
# agujas (simétricas para girar desde el centro): horaria apunta a las 9
o.append(f'<g id="horaria"><line x1="{CX-70}" y1="{CY}" x2="{CX+70}" y2="{CY}" stroke="none"/>'
         f'<path d="M {CX} {CY} L {CX-66} {CY}" stroke="{INK}" stroke-width="15" stroke-linecap="round"/>'
         f'<path d="M {CX} {CY} L {CX-62} {CY}" stroke="{CORAL}" stroke-width="7" stroke-linecap="round"/></g>')
o.append(f'<g id="minutero"><line x1="{CX}" y1="{CY-96}" x2="{CX}" y2="{CY+96}" stroke="none"/>'
         f'<path d="M {CX} {CY+12} L {CX} {CY-92}" stroke="{INK}" stroke-width="9" stroke-linecap="round"/></g>')
o.append(f'<circle cx="{CX}" cy="{CY}" r="12" fill="{INK}"/><circle cx="{CX}" cy="{CY}" r="5" fill="{CORAL}"/>')
s, _ = label("thora", CX, CY + R + 56, "9:00", bg=LIME, fg=INK, size=30)
o.append(s)

# mesa electoral
TY = 1150
o.append(f'<ellipse cx="540" cy="1262" rx="470" ry="18" fill="{INK}" opacity="0.2"/>')
for x in (140, 920):
    o.append(f'<rect x="{x-14}" y="{TY}" width="28" height="200" fill="#6B4A2E" stroke="{INK}" stroke-width="6"/>')
o.append(f'<path d="M 90 {TY-18} L 990 {TY-18} L 1000 {TY+76} L 80 {TY+76} Z" fill="url(#cloth)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
o.append(f'<path d="M 90 {TY+40} L 990 {TY+40}" stroke="#C3C9D6" stroke-width="4"/>')
# papeletas apiladas
o.append(saca(185, TY - 10, 150, 180, id_="saca"))
# lista del censo (portapapeles) a la derecha
KX, KY, KW, KH = 900, TY - 120, 130, 170
o.append(f'<g id="censo"><g transform="rotate(6 {KX} {KY})"><rect x="{KX-KW/2+6}" y="{KY-KH/2+8}" width="{KW}" height="{KH}" rx="10" fill="{INK}" opacity="0.22"/>'
         f'<rect x="{KX-KW/2}" y="{KY-KH/2}" width="{KW}" height="{KH}" rx="10" fill="#B0814F" stroke="{INK}" stroke-width="6"/>'
         f'<rect x="{KX-KW/2+12}" y="{KY-KH/2+18}" width="{KW-24}" height="{KH-30}" rx="4" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/>'
         f'<rect x="{KX-26}" y="{KY-KH/2-10}" width="52" height="24" rx="6" fill="#9AA3B5" stroke="{INK}" stroke-width="4"/>'
         + T(KX, KY - KH / 2 + 44, "CENSO", 18, INK, font=DISP)
         + "".join(f'<path d="M {KX-KW/2+26} {KY-KH/2+68+i*22} L {KX+KW/2-(26 if i%2 else 40)} {KY-KH/2+68+i*22}" stroke="#9AA3B5" stroke-width="6" stroke-linecap="round"/>' for i in range(4))
         + "</g></g>")
o.append(check(KX + 52, KY + 62, 32, id_="chkc"))
# urnas
u1, slot1 = urna(400, TY - 14, 230, 240, "CONGRESO", n_sobres=7, seed=2)
u2, slot2 = urna(690, TY - 14, 200, 220, "SENADO", n_sobres=6, seed=9)
o.append(f'<g id="urnas">{u1}{u2}</g>')
print(slot1, slot2)
# sobre + mano que vota (el brazo entra por la izquierda)
sx, sy = slot1[0] - 10, slot1[1] - 84
arm = f"M -60 {sy-190} C 120 {sy-200}, 230 {sy-120}, {sx-66} {sy-40}"
fingers = "".join(dbl(f"M {sx-60} {sy-38+k*14} L {sx-14} {sy-44+k*16}", 16, "#E7AE8B", 10) for k in range(3))
o.append(f'<g id="voto">'
         + dbl(arm, 60, "url(#sleeve)", 14)
         + fingers + sobre(sx, sy, 120, 84, -8)
         + f'<ellipse cx="{sx-66}" cy="{sy-36}" rx="40" ry="30" transform="rotate(25 {sx-66} {sy-36})" fill="url(#skinH)" stroke="{INK}" stroke-width="6"/>'
         + dbl(f"M {sx-56} {sy-20} L {sx-22} {sy-8}", 16, "#F1C6A4", 10)
         + f'<path d="M {sx-92} {sy-66} C {sx-96} {sy-40}, {sx-90} {sy-14}, {sx-78} {sy-6}" fill="none" stroke="#5C6B89" stroke-width="16" stroke-linecap="round"/>'
         + "</g>")
# etiqueta 29N
s, _ = label("t29", 570, 640, "DOMINGO 29", size=30)
o.append(s)
s, _ = label("t20", CX, CY + R + 56, "20:00 CIERRE", bg=CORAL, fg="#FFFFFF", size=30)
o.append(s)
s, _ = label("lsin", 570, 640, "SIN ABRIR", bg=LIME, fg=INK, size=34)
o.append(s)
o.append("</svg>")
save(OUT, "\n".join(o))

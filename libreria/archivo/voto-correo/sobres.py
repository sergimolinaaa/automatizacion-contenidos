from vc import *

OUT = "sobres_free.svg"
defs = BASE_DEFS + EXTRA_DEFS + lg("papG", [(0, "#FFFFFF"), (1, "#ECEEF4")]) + lg("vioG", [(0, "#9B6BFF"), (1, "#6A3FD6")])
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000">\n<defs>{defs}</defs>']

# ---------- escena «te llega a casa» ----------
o.append(cert_envelope(500, 470, 540, 340, -4, id_="paquete"))
s, _ = label("l9", 500, 190, "DESDE EL 9 NOV", bg=INK, fg=LIME, size=34); o.append(s)
o.append(dni(740, 790, 260, 8, id_="dniB"))
o.append(check(890, 690, 46, id_="chk"))
s, _ = label("lsolo", 330, 800, "SOLO A TI", bg=CORAL, fg="#FFFFFF", size=34); o.append(s)

# ---------- escena «sobre dentro de sobre» ----------
# papeleta (candidatura ficticia: banda de color y líneas)
PX, PY, PW, PH = 230, 300, 220, 300
pap = (f'<rect x="{PX-PW/2+8}" y="{PY-PH/2+10}" width="{PW}" height="{PH}" rx="8" fill="{INK}" opacity="0.2"/>'
       f'<rect x="{PX-PW/2}" y="{PY-PH/2}" width="{PW}" height="{PH}" rx="8" fill="url(#papG)" stroke="{INK}" stroke-width="6"/>'
       f'<rect x="{PX-PW/2}" y="{PY-PH/2}" width="{PW}" height="60" rx="8" fill="url(#vioG)" stroke="{INK}" stroke-width="5"/>'
       f'<circle cx="{PX-PW/2+34}" cy="{PY-PH/2+30}" r="16" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/>'
       + "".join(f'<path d="M {PX-PW/2+64} {PY-PH/2+22+k*16} L {PX+PW/2-20-k*30} {PY-PH/2+22+k*16}" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round"/>' for k in range(2))
       + "".join(f'<circle cx="{PX-PW/2+30}" cy="{PY-PH/2+96+i*40}" r="7" fill="#9AA3B5"/><path d="M {PX-PW/2+50} {PY-PH/2+96+i*40} L {PX+PW/2-(26 if i%2 else 46)} {PY-PH/2+96+i*40}" stroke="#9AA3B5" stroke-width="7" stroke-linecap="round"/>' for i in range(5))
       + f'<path d="M {PX-PW/2+12} {PY-PH/2+74} L {PX-PW/2+12} {PY+PH/2-16}" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round"/>')
o.append(f'<g id="papeleta">{pap}</g>')
s, _ = label("lpap", PX, 110, "PAPELETA", bg=INK, fg=LIME, size=30); o.append(s)
# sobre de votación
VX, VY = 750, 300
o.append(f'<g id="sobrev"><ellipse cx="{VX+8}" cy="{VY+118}" rx="160" ry="14" fill="{INK}" opacity="0.2"/>{sobre(VX, VY, 300, 200, 0, sw=7)}'
         + T(VX, VY + 70, "CONGRESO", 24, "#5A6170", font=DISP) + "</g>")
s, _ = label("lvot", VX, 120, "SOBRE DE VOTACIÓN", bg=INK, fg=LIME, size=26); o.append(s)
o.append(arrow("a1", ((360, 300), (575, 300)), col=LIME, w=12, head=30))
# certificado del censo
CX, CY, CW, CH = 220, 730, 250, 180
o.append(f'<g id="cert"><g transform="rotate(-5 {CX} {CY})"><rect x="{CX-CW/2+8}" y="{CY-CH/2+10}" width="{CW}" height="{CH}" rx="8" fill="{INK}" opacity="0.2"/>'
         f'<rect x="{CX-CW/2}" y="{CY-CH/2}" width="{CW}" height="{CH}" rx="8" fill="url(#kraft)" stroke="{INK}" stroke-width="6"/>'
         + T(CX, CY - CH / 2 + 40, "CERTIFICADO", 22, INK, font=DISP) + T(CX, CY - CH / 2 + 70, "DEL CENSO", 20, "#5A6170")
         + "".join(f'<path d="M {CX-CW/2+24} {CY+i*26} L {CX+CW/2-(30 if i%2 else 70)} {CY+i*26}" stroke="#9AA3B5" stroke-width="6" stroke-linecap="round"/>' for i in range(3))
         + f'<circle cx="{CX+CW/2-40}" cy="{CY+48}" r="22" fill="none" stroke="{CORAL}" stroke-width="5"/>'
         + "</g></g>")
# sobre dirigido a la mesa
o.append(cert_envelope(670, 770, 440, 280, 3, id_="sobremesa", text="A LA MESA", franq=False))
o.append(arrow("a2", ((750, 430), (700, 600)), col=LIME, w=12, head=30, curve=(760, 530)))
o.append(arrow("a3", ((360, 730), (440, 750)), col=LIME, w=12, head=26))
o.append("</svg>")
save(OUT, "\n".join(o))

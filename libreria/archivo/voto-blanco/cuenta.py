from vb import *

OUT = "cuenta_full.svg"
extra = lg("bgC", [(0, "#EEF2FA"), (1, "#D3DCEB")])
o = [header(1080, 1920, extra)]
o.append('<rect width="1080" height="1920" fill="url(#bgC)"/>')
o.append('<g stroke="#DCE3EF" stroke-width="3">' + "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="1920"/>' for x in range(0, 1080, 54)) + "</g>")
s, _ = label("titulo", 540, 500, "¿CUENTA PARA EL 3 %?", bg=INK, fg=LIME, size=36); o.append(s)

CW, TOP, BOT = 318, 560, 1235
XS = [185, 540, 895]


def card(cx, title, art, verdict_ok, vtext, uid, ts=30):
    x = cx - CW / 2
    s = f'<rect x="{f(x+8)}" y="{TOP+12}" width="{CW}" height="{BOT-TOP}" rx="28" fill="{INK}" opacity="0.2"/>'
    s += f'<rect x="{f(x)}" y="{TOP}" width="{CW}" height="{BOT-TOP}" rx="28" fill="url(#cardG)" stroke="{INK}" stroke-width="7"/>'
    s += f'<rect x="{f(x)}" y="{TOP}" width="{CW}" height="86" rx="28" fill="{INK}"/>'
    s += f'<rect x="{f(x)}" y="{TOP+50}" width="{CW}" height="36" fill="{INK}"/>'
    s += T(cx, TOP + 56, title, ts, "#FFFFFF", font=DISP)
    s += art
    return f'<g id="{uid}">{s}</g>'


# arte de cada tarjeta (zona y 690-930)
art_b = envelope(XS[0], 840, 200, 130)
art_n = envelope(XS[1], 850, 200, 130, paper=papeleta(XS[1] + 6, 790, 140, 170, rot=6, scribble=True))
# abstención: sofá con «Zzz»
sx, sy = XS[2], 880
art_a = (f'<ellipse cx="{sx}" cy="{sy+62}" rx="140" ry="14" fill="{INK}" opacity="0.2"/>'
         f'<rect x="{sx-120}" y="{sy-70}" width="240" height="90" rx="26" fill="url(#sofaD)" stroke="{INK}" stroke-width="6"/>'
         f'<rect x="{sx-105}" y="{sy-8}" width="210" height="54" rx="16" fill="url(#sofaG)" stroke="{INK}" stroke-width="6"/>'
         f'<rect x="{sx-140}" y="{sy-30}" width="46" height="88" rx="20" fill="url(#sofaG)" stroke="{INK}" stroke-width="6"/>'
         f'<rect x="{sx+94}" y="{sy-30}" width="46" height="88" rx="20" fill="url(#sofaG)" stroke="{INK}" stroke-width="6"/>'
         f'<path d="M {sx-100} {sy+58} L {sx-100} {sy+74} M {sx+100} {sy+58} L {sx+100} {sy+74}" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>'
         f'<path d="M {sx-100} {sy-56} L {sx-100} {sy-20}" stroke="#A9C8FF" stroke-width="7" stroke-linecap="round"/>'
         f'<g id="zzz">' + T(sx + 20, sy - 105, "Z", 34, INK, font=DISP) + T(sx + 56, sy - 140, "Z", 44, INK, font=DISP) + T(sx + 100, sy - 182, "Z", 54, INK, font=DISP) + "</g>")
o.append(card(XS[0], "BLANCO", art_b, True, "", "cblanco"))
o.append(card(XS[1], "NULO", art_n, False, "", "cnulo"))
o.append(card(XS[2], "ABSTENCIÓN", art_a, False, "", "cabst", ts=24))
# subtítulos de las tarjetas
s, _ = label("sb", XS[0], 990, "SOBRE VACÍO", bg="#FFFFFF", fg=INK, size=22); o.append(s)
s, _ = label("sn", XS[1], 990, "TACHADO", bg="#FFFFFF", fg=INK, size=22); o.append(s)
s, _ = label("sa", XS[2], 990, "NO VOTAR", bg="#FFFFFF", fg=INK, size=22); o.append(s)
# veredictos
VY = 1100
o.append(check(XS[0], VY, 56, id_="okb"))
o.append(cross(XS[1], VY, 56, id_="kon"))
o.append(cross(XS[2], VY, 56, id_="koa"))
s, _ = label("vb", XS[0], 1190, "SÍ CUENTA", bg=LIME, fg=INK, size=24); o.append(s)
s, _ = label("vn", XS[1], 1190, "NO CUENTA", bg=CORAL, fg="#FFFFFF", size=24); o.append(s)
s, _ = label("va", XS[2], 1190, "NO CUENTA", bg=CORAL, fg="#FFFFFF", size=24); o.append(s)
# flecha «sube el listón» en la tarjeta del blanco
o.append(arrow("sube", ((XS[0] + 136, 955), (XS[0] + 136, 850)), col=LIME, w=12, head=28))
o.append("</svg>")
save(OUT, "\n".join(o))

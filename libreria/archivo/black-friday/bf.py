"""SVG del vídeo Black Friday (reutiliza voto-blanco/vb.py: label, T, stamp2, header, lg/rg...)."""
import sys
SP = "/tmp/claude-0/-home-user-automatizacion-contenidos/039df981-7a17-5355-b711-18510fb209db/scratchpad"
sys.path.insert(0, SP + "/voto-blanco")
from vb import *  # noqa
OUTD = "/home/user/automatizacion-contenidos/content/lote6-05-black-friday/"
GREEN = "#3E8E1E"


def price_tag(cx, cy, w, h, rot=-5):
    """Etiqueta de cartón con agujero y cordel; devuelve (fondo, (x0,y0))."""
    x0, y0 = cx - w / 2, cy - h / 2
    n = 70  # muesca
    path = (f"M {f(x0+n)} {f(y0)} L {f(x0+w-14)} {f(y0)} Q {f(x0+w)} {f(y0)} {f(x0+w)} {f(y0+14)} L {f(x0+w)} {f(y0+h-14)} "
            f"Q {f(x0+w)} {f(y0+h)} {f(x0+w-14)} {f(y0+h)} L {f(x0+n)} {f(y0+h)} L {f(x0)} {f(cy+h*0.2)} L {f(x0)} {f(cy-h*0.2)} Z")
    s = f'<g transform="rotate({rot} {f(cx)} {f(cy)})">'
    s += f'<path d="{path}" transform="translate(14 18)" fill="{INK}" opacity="0.28"/>'
    s += f'<path d="{path}" fill="url(#tagG)" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'
    s += f'<path d="M {f(x0+n+14)} {f(y0+14)} L {f(x0+w-24)} {f(y0+14)}" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round" opacity="0.7"/>'
    s += f'<circle cx="{f(x0+48)}" cy="{f(cy)}" r="18" fill="#1A1E2C" stroke="{INK}" stroke-width="6"/>'
    s += f'<circle cx="{f(x0+48)}" cy="{f(cy)}" r="7" fill="#3A4258"/>'
    s += "</g>"
    return s


def bag(cx, base, w, h, col1, col2, text=""):
    x0, y0 = cx - w / 2, base - h
    s = f'<ellipse cx="{f(cx+8)}" cy="{f(base+6)}" rx="{f(w*0.58)}" ry="14" fill="{INK}" opacity="0.25"/>'
    s += f'<path d="M {f(cx-w*0.22)} {f(y0+6)} Q {f(cx-w*0.22)} {f(y0-h*0.32)} {f(cx)} {f(y0-h*0.32)} Q {f(cx+w*0.22)} {f(y0-h*0.32)} {f(cx+w*0.22)} {f(y0+6)}" fill="none" stroke="{INK}" stroke-width="12" stroke-linecap="round"/>'
    s += f'<path d="M {f(cx-w*0.22)} {f(y0+6)} Q {f(cx-w*0.22)} {f(y0-h*0.32)} {f(cx)} {f(y0-h*0.32)} Q {f(cx+w*0.22)} {f(y0-h*0.32)} {f(cx+w*0.22)} {f(y0+6)}" fill="none" stroke="#E9D9B8" stroke-width="5" stroke-linecap="round"/>'
    s += f'<path d="M {f(x0)} {f(y0)} L {f(x0+w)} {f(y0)} L {f(x0+w-10)} {f(base)} L {f(x0+10)} {f(base)} Z" fill="url(#{col1})" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
    s += f'<path d="M {f(x0+w*0.7)} {f(y0+4)} L {f(x0+w-14)} {f(base-4)} L {f(x0+w-4)} {f(y0+4)} Z" fill="{col2}" opacity="0.5"/>'
    s += f'<path d="M {f(x0+16)} {f(y0+16)} L {f(x0+22)} {f(base-24)}" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round" opacity="0.5"/>'
    if text:
        s += T(cx, y0 + h * 0.58, text, 30, "#FFFFFF", font=DISP)
    return s


# ---------------------------------------------------------------- A. etiqueta (full)
def etiqueta():
    extra = (lg("wallBF", [(0, "#141826"), (1, "#252B40")]) + lg("tagG", [(0, "#FFF6DC"), (1, "#F2D9A2")])
             + lg("bagA", [(0, "#FF7A5C"), (1, "#D9432A")]) + lg("bagB", [(0, "#D9FF6A"), (1, "#9CCB12")])
             + lg("shelfG", [(0, "#4A5370"), (1, "#2C3248")]) + rg("glowBF", [(0, "#C8FF2E"), (1, "#141826")]))
    o = [header(1080, 1920, extra)]
    o.append('<rect width="1080" height="1920" fill="url(#wallBF)"/>')
    o.append('<circle cx="540" cy="900" r="520" fill="url(#glowBF)" opacity="0.22"/>')
    o.append('<g transform="translate(0 60)">')
    # baldas
    for y in (1290, 1560):
        o.append(f'<rect x="0" y="{y}" width="1080" height="34" fill="url(#shelfG)" stroke="{INK}" stroke-width="6"/>')
        o.append(f'<path d="M 0 {y+4} L 1080 {y+4}" stroke="#7B86A6" stroke-width="4"/>')
    # cajas en las baldas (decoración)
    for x, w, h, c in ((250, 120, 90, "#3B4566"), (40, 60, 140, "#465277"), (760, 100, 110, "#3B4566")):
        o.append(f'<rect x="{x}" y="{1290-h}" width="{w}" height="{h}" rx="8" fill="{c}" stroke="{INK}" stroke-width="6"/>')
    # banner BLACK FRIDAY
    ban = f'<rect x="150" y="452" width="780" height="104" rx="18" fill="{INK}" stroke="{LIME}" stroke-width="6"/>'
    ban += T(540, 524, "BLACK FRIDAY", 58, LIME, font=DISP)
    o.append(g("banner", ban))
    # cordel
    # etiqueta
    TX, TY = 560, 850
    import math
    a = math.radians(-5); hx0, hy0 = TX - 320 + 48 - TX, 0
    HX, HY = TX + hx0 * math.cos(a), TY + hx0 * math.sin(a)
    o.append(f'<path d="M {f(HX)} {f(HY)} C {f(HX-60)} {f(HY-120)} {f(HX-10)} {f(HY-230)} {f(HX+40)} 560" fill="none" stroke="{INK}" stroke-width="11" stroke-linecap="round"/>')
    o.append(f'<path d="M {f(HX)} {f(HY)} C {f(HX-60)} {f(HY-120)} {f(HX-10)} {f(HY-230)} {f(HX+40)} 560" fill="none" stroke="#E9D9B8" stroke-width="5" stroke-linecap="round"/>')
    tag_ = price_tag(TX, TY, 640, 400, rot=-5)
    inner = f'<g transform="rotate(-5 {TX} {TY})">'
    inner += g("viejo", T(TX + 30, TY - 70, "100 €", 76, "#7A6A4A", font=DISP)
               + f'<path id="tachon" d="M {TX-130} {TY-90} L {TX+190} {TY-108}" stroke="{CORAL}" stroke-width="14" stroke-linecap="round"/>')
    inner += g("viejo50", T(TX + 30, TY - 70, "50 €", 76, "#7A6A4A", font=DISP)
               + f'<path d="M {TX-90} {TY-90} L {TX+150} {TY-104}" stroke="{CORAL}" stroke-width="14" stroke-linecap="round"/>')
    inner += g("nuevo", T(TX + 30, TY + 100, "50 €", 150, INK, font=DISP))
    bars = "".join(f'<rect x="{TX+150+i*7}" y="{TY+140}" width="{(3 if i%3 else 5)}" height="34" fill="{INK}"/>' for i in range(14))
    inner += bars + T(TX - 160, TY + 168, "REF. 0427", 22, "#7A6A4A")
    inner += "</g>"
    o.append(g("etiqueta", tag_ + inner))
    # badge -50 %
    o.append(f'<g id="badge"><circle cx="850" cy="640" r="98" fill="{CORAL}" stroke="{INK}" stroke-width="8"/>'
             f'<circle cx="850" cy="640" r="80" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-dasharray="10 8"/>'
             + T(850, 658, "-50 %", 50, "#FFFFFF", font=DISP) + "</g>")
    # bolsas
    o.append(g("bolsas", bag(150, 1290, 170, 200, "bagA", "#A8301C", "¡YA!") + bag(950, 1290, 140, 170, "bagB", "#6E8F0A")))
    # interrogante
    o.append(f'<g id="duda"><circle cx="170" cy="700" r="70" fill="{YEL}" stroke="{INK}" stroke-width="7"/>' + T(170, 734, "?", 96, INK, font=DISP) + "</g>")
    # etiquetas de explicación
    s, _ = label("t2sem", 540, 1200, "HACE 2 SEMANAS: 50 €", bg=INK, fg=LIME, size=34); o.append(s)
    s, _ = label("tdef", 540, 1200, "TACHADO = PRECIO DE ANTES", bg="#FFFFFF", fg=INK, size=32); o.append(s)
    o.append(stamp2(600, 1030, "REBAJA: 0 %", 50, rot=-8, col=CORAL, id_="cero"))
    o.append(stamp2(600, 1030, "¿FALSA?", 58, rot=-8, col=CORAL, id_="falsa"))
    o.append("</g>")
    o.append("</svg>")
    save(OUTD + "etiqueta_full.svg", "\n".join(o))


# ---------------------------------------------------------------- B. gráfica (panel)
def grafica():
    extra = lg("bgG", [(0, "#F4F7FF"), (1, "#E3EAF8")]) + lg("winG", [(0, "#C8FF2E"), (1, "#C8FF2E")])
    o = [header(1000, 700, extra)]
    o.append('<rect width="1000" height="700" fill="url(#bgG)"/>')
    X0, X1, Y0 = 110, 950, 590          # ejes
    day = (X1 - 30 - X0) / 56           # 8 semanas
    xd = lambda d: X0 + d * day
    Y50, Y100 = 470, 210
    BF, JUMP = 48, 34
    # cuadrícula
    o.append('<g stroke="#C9D3E8" stroke-width="2">' + "".join(f'<line x1="{f(xd(w*7))}" y1="120" x2="{f(xd(w*7))}" y2="{Y0}"/>' for w in range(1, 9)) + "</g>")
    for yv in (Y50, Y100):
        o.append(f'<line x1="{X0}" y1="{yv}" x2="{X1-20}" y2="{yv}" stroke="#C9D3E8" stroke-width="2" stroke-dasharray="8 8"/>')
    # ventana de 30 días
    win = f'<rect x="{f(xd(BF-30))}" y="120" width="{f(xd(BF)-xd(BF-30))}" height="{Y0-120}" fill="{LIME}" opacity="0.35"/>'
    win += f'<path d="M {f(xd(BF-30))} 120 L {f(xd(BF-30))} {Y0} M {f(xd(BF))} 120 L {f(xd(BF))} {Y0}" stroke="#6E8F0A" stroke-width="4" stroke-dasharray="10 7"/>'
    o.append(g("ventana", win))
    s, _ = label("t30", (xd(BF - 30) + xd(BF)) / 2, 152, "ÚLTIMOS 30 DÍAS", bg=INK, fg=LIME, size=28); o.append(s)
    # ejes
    o.append(f'<path d="M {X0} 100 L {X0} {Y0} L {X1} {Y0}" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>')
    o.append(T(X0 - 14, Y50 + 10, "50", 28, INK, anchor="end"))
    o.append(T(X0 - 14, Y100 + 10, "100", 28, INK, anchor="end"))
    o.append(T(X0 - 14, 120, "€", 30, INK, anchor="end"))
    o.append(T((X0 + X1) / 2, Y0 + 52, "SEMANAS →", 26, "#5A6380"))
    # línea de precio en 3 tramos
    def seg(id_, pts_, col):
        d = "M " + " L ".join(f"{f(x)} {f(y)}" for x, y in pts_)
        return (f'<g id="{id_}"><path d="{d}" fill="none" stroke="{INK}" stroke-width="20" stroke-linecap="round" stroke-linejoin="round"/>'
                f'<path d="{d}" fill="none" stroke="{col}" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/></g>')
    o.append(seg("l1", [(xd(0), Y50), (xd(JUMP), Y50)], "#2EC4B6"))
    o.append(seg("l2", [(xd(JUMP), Y50), (xd(JUMP), Y100), (xd(BF), Y100)], CORAL))
    o.append(seg("l3", [(xd(BF), Y100), (xd(BF), Y50), (xd(56), Y50)], "#2EC4B6"))
    # etiquetas
    s, _ = label("p50", xd(14), Y50 - 60, "50 €", bg="#FFFFFF", fg=INK, size=32); o.append(s)
    s, _ = label("p100", xd(41), Y100 + 56, "100 €", bg=CORAL, fg="#FFFFFF", size=32); o.append(s)
    o.append(f'<g id="m50"><circle cx="{f(xd(BF)+70)}" cy="{f((Y50+Y100)/2)}" r="58" fill="{CORAL}" stroke="{INK}" stroke-width="6"/>'
             + T(xd(BF) + 70, (Y50 + Y100) / 2 + 12, "-50 %", 32, "#FFFFFF", font=DISP) + "</g>")
    o.append(f'<g id="bf"><rect x="{f(xd(BF)-60)}" y="{Y0+16}" width="120" height="44" rx="10" fill="{INK}"/>' + T(xd(BF), Y0 + 47, "BLACK F.", 22, LIME) + "</g>")
    s, _ = label("igual", xd(28), Y50 + 70, "¡EL MISMO PRECIO!", bg=LIME, fg=INK, size=30); o.append(s)
    # mínimo dentro de la ventana
    o.append(f'<g id="minimo"><circle cx="{f(xd(26))}" cy="{Y50}" r="30" fill="none" stroke="{GREEN}" stroke-width="9"/></g>')
    s, _ = label("tmin", xd(26), Y50 + 68, "EL MÁS BAJO: 50 €", bg=GREEN, fg="#FFFFFF", size=28); o.append(s)
    s, _ = label("tley", 285, 300, "ART. 20 · LEY 7/1996", bg="#FFFFFF", fg=INK, size=24); o.append(s)
    o.append("</svg>")
    save(OUTD + "grafica.svg", "\n".join(o))


# ---------------------------------------------------------------- C. móvil (free)
def movil():
    extra = (lg("phoneG", [(0, "#3A4258"), (1, "#151926")], 0, 0, 1, 1) + lg("scrG", [(0, "#FFFFFF"), (1, "#EEF2FA")])
             + lg("hojaG", [(0, "#FFFFFF"), (1, "#EEF0F5")]))
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 900">\n<defs>{DEFS}{extra}</defs>']
    PX, PY, PW, PH = 300, 60, 400, 780
    ph = f'<rect x="{PX+16}" y="{PY+20}" width="{PW}" height="{PH}" rx="56" fill="{INK}" opacity="0.25"/>'
    ph += f'<rect x="{PX}" y="{PY}" width="{PW}" height="{PH}" rx="56" fill="url(#phoneG)" stroke="{INK}" stroke-width="8"/>'
    SX, SY, SW, SH = PX + 22, PY + 26, PW - 44, PH - 52
    ph += f'<rect x="{SX}" y="{SY}" width="{SW}" height="{SH}" rx="38" fill="url(#scrG)"/>'
    ph += f'<rect x="{PX+PW/2-50}" y="{SY+12}" width="100" height="24" rx="12" fill="{INK}"/>'
    ph += f'<path d="M {PX+10} {PY+80} L {PX+10} {PY+250}" stroke="#7A86A6" stroke-width="5" stroke-linecap="round" opacity="0.6"/>'
    # app: producto + precio
    ph += f'<rect x="{SX+30}" y="{SY+70}" width="{SW-60}" height="190" rx="18" fill="#E3E9F6" stroke="#B9C4DC" stroke-width="3"/>'
    # producto (auriculares genéricos)
    hx, hy = SX + SW / 2, SY + 175
    ph += f'<path d="M {hx-62} {hy+10} Q {hx-62} {hy-80} {hx} {hy-80} Q {hx+62} {hy-80} {hx+62} {hy+10}" fill="none" stroke="{INK}" stroke-width="14" stroke-linecap="round"/>'
    for sx in (-1, 1):
        ph += f'<rect x="{hx+sx*62-22}" y="{hy-10}" width="44" height="70" rx="16" fill="{CORAL}" stroke="{INK}" stroke-width="6"/>'
    ph += T(SX + 30, SY + 310, "50 €", 44, INK, anchor="start", font=DISP)
    ph += T(SX + 30, SY + 360, "HISTORIAL", 24, "#5A6380", anchor="start")
    # mini gráfica
    gx0, gx1, gy50, gy100 = SX + 30, SX + SW - 30, SY + 560, SY + 430
    ph += f'<rect x="{gx0-10}" y="{gy100-30}" width="{gx1-gx0+20}" height="{gy50-gy100+70}" rx="14" fill="#FFFFFF" stroke="#B9C4DC" stroke-width="3"/>'
    gw = gx1 - gx0
    d = f"M {gx0} {gy50} L {f(gx0+gw*0.6)} {gy50} L {f(gx0+gw*0.6)} {gy100} L {f(gx0+gw*0.85)} {gy100} L {f(gx0+gw*0.85)} {gy50} L {gx1} {gy50}"
    o.append(g("telefono", ph))
    o.append(g("curva", f'<path d="{d}" fill="none" stroke="{CORAL}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>'))
    o.append(g("pico", f'<circle cx="{f(gx0+gw*0.725)}" cy="{gy100}" r="22" fill="none" stroke="{CORAL}" stroke-width="6"/>'))
    # botón captura
    o.append(g("boton", f'<circle cx="{PX+PW/2}" cy="{SY+SH-60}" r="34" fill="#FFFFFF" stroke="{INK}" stroke-width="6"/><circle cx="{PX+PW/2}" cy="{SY+SH-60}" r="22" fill="{CORAL}"/>'))
    # flash
    o.append(g("flash", f'<rect x="{SX}" y="{SY}" width="{SW}" height="{SH}" rx="38" fill="#FFFFFF" opacity="0.85"/>'))
    # etiquetas a los lados
    s, _ = label("tcap", 165, 200, "CAPTURA", bg=LIME, fg=INK, size=32); o.append(s)
    s, _ = label("tfecha", 165, 280, "+ FECHA", bg="#FFFFFF", fg=INK, size=28); o.append(s)
    s, _ = label("this", 870, 420, "HISTORIAL:", bg=INK, fg=LIME, size=28); o.append(s)
    s, _ = label("this2", 870, 485, "LO QUE COSTÓ", bg="#FFFFFF", fg=INK, size=24); o.append(s)
    s, _ = label("this3", 870, 540, "CADA DÍA", bg="#FFFFFF", fg=INK, size=24); o.append(s)
    # hoja de reclamaciones
    hj = f'<g transform="rotate(5 875 330)"><rect x="770" y="170" width="210" height="320" rx="10" fill="url(#hojaG)" stroke="{INK}" stroke-width="7"/>'
    hj += T(875, 225, "HOJA DE", 21, INK, font=DISP) + T(875, 257, "RECLAMA-", 21, INK, font=DISP) + T(875, 289, "CIONES", 21, INK, font=DISP)
    for i in range(5):
        hj += f'<path d="M 795 {330+i*30} L {955-(i%2)*40} {330+i*30}" stroke="#A3ABBD" stroke-width="7" stroke-linecap="round"/>'
    hj += "</g>"
    o.append(g("hoja", hj))
    o.append(g("lupa", f'<circle cx="170" cy="560" r="62" fill="#DDF3FF" fill-opacity="0.7" stroke="{INK}" stroke-width="10"/>'
               f'<path d="M 214 604 L 268 660" stroke="{INK}" stroke-width="22" stroke-linecap="round"/><path d="M 140 530 Q 150 515 168 512" stroke="#FFFFFF" stroke-width="7" fill="none" stroke-linecap="round"/>'))
    o.append(stamp2(500, 770, "¿NO CUADRA?", 40, rot=-6, col=CORAL, id_="nocuadra"))
    o.append("</svg>")
    save(OUTD + "movil_free.svg", "\n".join(o))


if __name__ == "__main__":
    import os
    os.makedirs(OUTD, exist_ok=True)
    etiqueta(); grafica(); movil()

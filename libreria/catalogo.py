"""Catálogo visual de la librería: TODAS las piezas en una sola imagen para revisarlas de un vistazo.

Uso:  python3 libreria/catalogo.py salida.png
Genera también salida.svg (el catálogo vectorial) y salida.html (con las fuentes de la marca), y hace la captura con
el Chromium headless de /opt/pw-browsers (el mismo que scripts/shot.sh).
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from libreria.svg import base as B  # noqa: E402
from libreria.svg.base import *  # noqa: E402,F401
from libreria.svg.personajes import persona, pictograma, multitud  # noqa: E402
from libreria.svg.objetos import politica as P, casa as C, cuerpo as CU, escenarios as E, animales as AN, tienda as TI  # noqa: E402

CHROME = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"
COLS = 6
CW = 400          # ancho de cada celda en el catálogo
TITLE_H = 34


def celdas():
    """Lista de (título, ancho_viewBox, alto_viewBox, contenido_svg, fondo_claro)."""
    out = []
    add = lambda t, w, h, c, claro=True: out.append((t, w, h, c, claro))

    # ---------------- base
    s = etiqueta("e1", 260, 90, "ETIQUETA", apunta=(150, 260))
    s += etiqueta("e2", 720, 90, "LIMA", bg=LIME, fg=INK, apunta=(820, 250))
    s += flecha("f1", (130, 420), (420, 300), curva=0.3)
    s += flecha("f2", (560, 330), (880, 470), col=CORAL, curva=-0.25)
    s += flecha_gorda("fg", (300, 580), (700, 580))
    add("etiqueta · flecha · flecha_gorda", 1000, 700, s)
    s = globo("g1", 300, 150, "¿EN SERIO?", cola=(220, 300), size=40)
    s += globo("g2", 720, 160, "MMM…", cola=(800, 320), tipo="piensa", size=40)
    s += globo("g3", 500, 480, "¡CRAC!", tipo="grito", size=56)
    add("globo: habla · piensa · grito", 1000, 700, s)
    s = sello("s1", 500, 200, "MITO", 90) + sello("s2", 500, 470, "VÁLIDO", 64, rot_=6, col="#1E8E5A")
    add("sello", 1000, 700, s)
    s = icono_duda("i1", 120, 170, 60) + icono_alerta("i2", 320, 170, 62) + icono_ok("i3", 520, 170, 60) + icono_no("i4", 720, 170, 60)
    s += corazon("i5", 900, 175, 1.3) + chispa("i6", 140, 470, 60) + destellos("i7", 360, 470, 70) + aspa("i8", 600, 470, 50)
    s += rayos("i9", 840, 520, 60, 110, n=7)
    add("iconos de reacción", 1000, 700, s)
    s = contador("c1", 280, 200, "3.270", "LISTÓN") + marcador("c2", 700, 200, "28", "30", txt_izq="ANTES", txt_der="DESPUÉS", w=440)
    s += barra("b1", 120, 640, 90, 160, CORAL, "A", "40") + barra("b2", 240, 640, 90, 250, LIME, "B", "70")
    s += medidor("m1", 700, 610, 170, 0.75, texto="TEMPERATURA")
    add("contador · marcador · barra · medidor", 1000, 700, s)
    s = copo(110, 120, 50) + ondas_calor(260, 220) + ondas_calor(300, 200) + temblor(390, 70) + nota_musical(520, 180, 80, doble=True)
    s += zzz(650, 190, 60) + gota(860, 150, 40) + vaho(80, 400, 1.3)
    s += onomatopeya("o1", 410, 420, "¡PLAF!", 120, 46) + ondas_sonido("os", 640, 430, 40, 3) + lineas_velocidad(900, 420, dir_=-1, col=CORAL)
    s += confeti("cf", (40, 560, 960, 680), 30)
    add("efectos y ambiente", 1000, 700, s)
    s = lupa("lp", 260, 300, 160, contenido=f'<rect x="80" y="120" width="400" height="400" fill="#FFE3D0"/>' + CU.piel_lupa(260, 300, 160))
    s += nube(700, 200, 1.2) + resplandor(700, 500, 120) + chispa(None, 700, 500, 50, YEL)
    add("lupa (con contenido recortado) · nube · resplandor", 1000, 700, s)
    s = tarjeta("t1", 280, 330, 360, 420, acento=TEAL, rot_=-4, body=T(280, 320, "TARJETA", 44, INK, font=DISP))
    s += cartel("ct", 720, 200, "¡NUEVO!", 50) + onda_expansiva("r1", 720, 500, 110)
    add("tarjeta · cartel · onda_expansiva", 1000, 700, s)

    # ---------------- personajes
    gente = ""
    gente += persona("p1", 120, 680, 0.95, "adulto", "media", "corto", "castano", "jersey")
    gente += persona("p2", 340, 680, 0.95, "joven", "clara", "largo", "rubio", "camiseta", CORAL, brazos=("cintura", "saluda"), expresion="risa", accesorios=("pendientes",))
    gente += persona("p3", 590, 680, 0.95, "mayor", "morena", "calvo", "canoso", "chaqueta", "#5A6B8C", accesorios=("gafas", "baston", "bigote"), expresion="duda", brazos=("barbilla", "abajo"))
    gente += persona("p4", 840, 680, 1.15, "nino", "oscura", "rizado", "negro", "camisa", VERDE, expresion="sorpresa", brazos=("arriba", "arriba"))
    add("persona: adulto · joven · mayor · niño", 1000, 700, gente)
    gente = persona("q1", 150, 680, 0.95, "adulto", "clara", "coleta", "pelirrojo", "vestido", VIOLETA, expresion="sueno", accesorios=("gafas",), brazos=("abajo", "senala"))
    gente += persona("q2", 430, 680, 0.95, "adulto", "media", "corto", "castano", "abrigo", PIZARRA, accesorios=("gorro", "bufanda"), expresion="frio", brazos="cruzados")
    gente += persona("q3", 700, 680, 0.95, "mayor", "clara", "mono", "blanco", "jersey", ROSA, pose="sentado", silla=True, expresion="triste", accesorios=("gafas",))
    gente += persona("q4", 900, 690, 0.75, "adulto", "oscura", "rapado", "negro", "camisa", "#FFFFFF", pose="busto", expresion="enfado", accesorios=("barba",))
    add("persona: vestido · abrigo+gorro+bufanda · sentado · busto", 1000, 700, gente)
    gente = ""
    for i, ex in enumerate(("neutral", "sorpresa", "risa", "duda", "frio", "sueno", "triste", "enfado")):
        gente += persona(f"x{i}", 70 + i * 123, 300, 0.95, "joven", ["clara", "media", "morena", "oscura"][i % 4],
                         ["corto", "largo", "rizado", "coleta", "mono", "rapado", "calvo", "corto"][i], ["negro", "castano", "rubio", "pelirrojo", "canoso", "negro", "castano", "rubio"][i],
                         pose="busto", expresion=ex)
        gente += T(70 + i * 123, 340, ex.upper(), 20, INK)
    gente += multitud("mt", 60, 940, 660, n=10, s=120)
    add("expresiones (busto) · pictograma/multitud", 1000, 700, gente)

    # ---------------- política
    s = P.urna("u", 230, 600, 280, 300, texto="CONGRESO").__str__()
    s += P.papeleta_congreso("pc", 600, 360, 260, 360, "circle", rot_=4)
    s += P.sobre_abierto("sa", 860, 520, 200, 150, dentro=P.papeleta(None, 860, 450, 120, 160, forma="tri"))
    add("urna · papeleta_congreso · sobre_abierto", 1000, 700, s)
    s = P.papeleta_senado("ps", 250, 360, 360, 420, cruces=(0, 2, 4)) + P.boli("bo", 330, 540, 200, rot_=-40)
    s += P.sobre_certificado("sc", 690, 220, 380, 230, rot_=-4) + P.dni("dn", 650, 520, 260, rot_=5) + P.saca("sk", 890, 660, 170, 200)
    add("papeleta_senado · boli · sobre_certificado · dni · saca", 1000, 700, s)
    reparto, _ = P.dhondt({"ESTRELLA": 38000, "CÍRCULO": 30000, "TRIÁNGULO": 17900, "CUADRADO": 10000, "ROMBO": 3100}, 30, validos=100000)
    s = P.hemiciclo("hm", 500, 520, 30, 3, 220, 380, P.colores_reparto(reparto), r_esc=24)
    s += "".join(P.chip_partido(None, 140 + i * 180, 640, forma, size=26) for i, (_, _, forma) in enumerate(P.PARTIDOS))
    add("hemiciclo (D'Hondt) · chip_partido", 1000, 700, s)
    s = P.calendario("cal", 180, 260, 220, 240, "NOV", "29", rot_=-5) + P.atril("at", 480, 640, 220, 260)
    s += P.atril("at2", 800, 640, 220, 260, mic=False, frontal=P.placa(800, 500, 150, 70, "ABC"))
    s += P.sin_posicionarnos("sp", 500, 90, 34)
    add("calendario · atril (logo/placa) · sello SIN POSICIONARNOS", 1000, 700, s)
    s = P.documento("doc", 230, 350, 280, 380, "PROGRAMA", "2026", rot_=-3) + P.carpeta("cp", 590, 380, 300, 230)
    s += P.garabato("gb", 760, 960, 160, 30) + P.candado("ck", 860, 420, 120)
    for i, (_, _, forma) in enumerate(P.PARTIDOS):
        s += P.icono_partido(forma, 760 + i * 50, 620, 20, sw=4)
    add("documento · carpeta · garabato · candado · iconos", 1000, 700, s)

    # ---------------- casa
    s = C.vaso("v1", 200, 640, 400, 280, 0.62, "agua", cubitos=2) + C.vaso("v2", 500, 640, 340, 220, 0.75, "refresco", burbujas=12)
    s += C.botella("bt", 730, 640, 420, texto="AGUA") + C.taza("tz", 900, 640, 150)
    add("vaso (agua+cubitos, refresco) · botella · taza", 1000, 700, s)
    s = C.mesa("ms", 300, 470, 500, 200) + C.reloj("rl", 300, 260, 110) + C.ventana("vn", 760, 300, 260, 300)
    add("mesa · reloj · ventana con cortinas", 1000, 700, s)
    pant = f'<rect x="0" y="0" width="1000" height="1000" fill="#EEF2FA"/>' + T(200, 300, "50 €", 54, INK, font=DISP) + T(200, 370, "HISTORIAL", 22, GRIS_OSC)
    s = C.movil("mv", 200, 350, 290, pantalla=pant) + C.bombilla("bb", 480, 300, 160) + rayos(None, 480, 240, 120, 170, n=7)
    s += C.casita("cs", 800, 300, 220) + C.etiqueta_precio("ep", 760, 520, 300, 150, "19 €", tachado="40 €")
    add("móvil · bombilla · casita · etiqueta_precio", 1000, 700, s)
    s = C.bolsa("bl", 160, 640, 200, 220, texto="REBAJAS") + C.caja_madera("cm", 330, 640, 240, 180)
    s += C.llave_allen("ll", 720, 640, 1.4, 20) + C.tornillo("tr", 860, 520, 1.6, 30) + C.cubito("cb", 820, 230, 150, 12)
    s += C.grieta("gr", (300, 120), (560, 300), amp=16)
    add("bolsa · caja_madera · llave_allen · tornillo · cubito · grieta", 1000, 700, s)

    # ---------------- cuerpo
    s = CU.cabeza_perfil("cp", 300, 690, 0.95) + CU.cerebro("cb", 780, 230, 0.9)
    s += etiqueta(None, 780, 560, "HIPOTÁLAMO", apunta=CU.cerebro(None, 780, 230, 0.9).puntos["hipotalamo"])
    add("cabeza_perfil · cerebro + hipotálamo", 1000, 700, s)
    s = CU.musculo("m1", 300, 180, 240, 80) + CU.musculo("m2", 300, 480, 240, 80, contraido=True)
    s += CU.termometro("tm", 760, 120, 380, 0.75, CORAL, texto="39 °C")
    add("músculo relajado/contraído · termómetro", 1000, 700, s)
    s = CU.antebrazo("ab", (-40, 520), (1040, 320), 110, gallina=True)
    s += f'<g opacity="1">{lupa(None, 700, 180, 120, contenido=CU.piel_lupa(700, 180, 120))}</g>'
    add("antebrazo con vello + piel de gallina · piel_lupa", 1000, 700, s)

    # ---------------- bostezo (lote7-03): expresión bostezo, mano a la boca, gafas de sol, perro, muebles
    s = persona("pb1", 190, 660, 0.95, "adulto", "clara", "largo", "castano", "chaqueta", "#8A93A6", expresion="bostezo", brazos=("boca", "abajo"))
    s += persona("pb2", 500, 660, 0.95, "joven", "morena", "corto", "negro", "jersey", "#2FA36B", expresion="bostezo", brazos=("arriba", "arriba"))
    s += persona("pb3", 810, 660, 0.95, "adulto", "media", "corto", "negro", "abrigo", "#C9A86A", accesorios=("gafas_sol", "bigote"))
    add("persona: expresion='bostezo' · brazos 'boca' · gafas_sol", 1000, 700, s)
    s = AN.perro("pe", 250, 660, 1.2) + "".join(AN.icono_perro(None, 560 + 80 * (i % 5), 140 + 80 * (i // 5), 54, "#FFC83D" if i < 7 else "#C9CED8") for i in range(15))
    s += C.portapapeles("pp", 760, 520, 170, 220) + bandera("bd", 560, 470, 130, 86)
    add("perro (bostezo) · icono_perro · portapapeles · bandera", 1000, 700, s)
    s = C.sofa("so", 260, 640, 440, 120, respaldo=170) + C.banco("bn", 740, 640, 380, 120)
    s += C.cronometro("cr", 260, 150, 70) + C.pizarra("pz", 740, 170, 260, 150)
    add("sofa · banco · cronometro · pizarra", 1000, 700, s)
    s = C.huella("hu", 300, 350, 1.5, espejo=True) + C.zapato_arriba("za", 520, 350, 1.5, CORAL) + C.zapato_arriba("zb", 720, 350, 1.5, TEAL, espejo=True)
    add("huella · zapato_arriba", 1000, 700, s)
    s = TI.cartel_precio("cp", 200, 130, 280, "9", "99") + TI.cartel_precio("cp10", 520, 130, 240, "10", None, col=LIME, cinta="OFERTA")
    s += "".join(TI.producto(t, 120 + i * 110, 420, 0.9, c) for i, (t, c) in enumerate(zip(("caja", "bote", "botella", "lata", "brick"), TI.COLS_PROD)))
    s += TI.carrito("car", 790, 470, 300) + TI.ticket("tk", 830, 480, 200, total="2,48", size=18)
    s += TI.recta_numerica("rn", 120, 560, 590, 9, 10, 0.1, {9: "9", 10: "10"}, size=26)
    add("tienda: cartel_precio · producto · carrito · ticket · recta_numerica", 1000, 700, s)
    add("tienda.supermercado() + estanteria", 1080, 1920, TI.supermercado(), False)

    # ---------------- escenarios (miniaturas de 1080x1920)
    for nombre, fondo in (("habitacion()", E.habitacion()), ("cocina()", E.cocina()), ("oficina()", E.oficina()),
                          ("escenario()", E.escenario()), ("cielo('dia')", E.cielo()), ("cielo('tarde')", E.cielo(hora="tarde")),
                          ("cielo('noche')", E.cielo(hora="noche"))):
        add(nombre, 1080, 1920, fondo, False)
    r = E.carriles_rotonda()
    coches = ""
    for i, (ang, col) in enumerate(((20, "rojo"), (130, "azul"), (250, "amarillo"))):
        x, y, rb = E.punto_en_anillo(540, 880, r["exterior"], ang)
        coches += E.coche_aereo(f"car{i}", x, y, rb, col, intermitente="der" if i == 0 else None)
    coches += E.coche_aereo("car9", 540 + 65, 1500, 0, "blanco")
    add("rotonda() + coche_aereo()", 1080, 1920, E.rotonda() + coches, False)
    return out


def construir():
    cells = celdas()
    rows, row = [], []
    for c in cells:
        # las miniaturas de escenarios ocupan una celda; todo lo demás también
        if row and (row[-1][4] != c[4]):  # los escenarios (fondo azul) empiezan fila nueva
            rows.append(row)
            row = []
        row.append(c)
        if len(row) == COLS:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    parts, y = [], 0
    for row in rows:
        hmax = max((CW - 16) * h / w for _, w, h, _, _ in row) + 16 + TITLE_H
        for i, (t, w, h, c, claro) in enumerate(row):
            x = i * CW
            ch = (CW - 16) * h / w
            parts.append(f'<rect x="{x+4}" y="{y+4}" width="{CW-8}" height="{hmax-8}" rx="10" fill="{"#F4F8FD" if claro else "#2347FF"}" stroke="#0B0B14" stroke-width="2"/>')
            parts.append(f'<svg x="{x+8}" y="{y+8}" width="{CW-16}" height="{ch}" viewBox="0 0 {w} {h}" overflow="hidden">{c}</svg>')
            parts.append(f'<text x="{x+CW/2}" y="{y+hmax-14}" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="12" fill="#0B0B14">{t}</text>')
        y += hmax
    W, H = CW * COLS, int(y)
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
           f'<defs>{B.defs_registradas()}</defs>\n<rect width="{W}" height="{H}" fill="#DDE3EE"/>\n' + "\n".join(parts) + "\n</svg>")
    return doc, W, H


def main():
    out = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "catalogo.png")
    doc, W, H = construir()
    validar(doc)
    base_ = os.path.splitext(out)[0]
    open(base_ + ".svg", "w", encoding="utf-8").write(doc)
    fonts = os.path.join(ROOT, "video", "public", "fonts")
    css = (f'@font-face{{font-family:"Unbounded";font-weight:900;src:url("file://{fonts}/unbounded-latin-900-normal.woff2")}}'
           f'@font-face{{font-family:"JetBrains Mono";font-weight:800;src:url("file://{fonts}/jetbrains-mono-latin-800-normal.woff2")}}'
           "html,body{margin:0;padding:0;background:#DDE3EE}")
    html = f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{doc}</body></html>'
    open(base_ + ".html", "w", encoding="utf-8").write(html)
    subprocess.run([CHROME, "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
                    "--virtual-time-budget=4000", f"--window-size={W},{H}", f"--screenshot={out}", "file://" + base_ + ".html"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
    print("catálogo:", out, f"({W}x{H})", "· svg:", base_ + ".svg")


if __name__ == "__main__":
    main()

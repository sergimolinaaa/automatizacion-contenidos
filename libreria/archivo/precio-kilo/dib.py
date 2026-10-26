"""lote9-03-precio-kilo: dibujos de «¿El pack ahorro sale más caro? Mira el precio por kilo».
Uso: python3 libreria/archivo/precio-kilo/dib.py

Método rossark: cada parte es su grupo con pivote propio (cuerpo en los pies, cabeza en el cuello, brazo en el hombro,
lupa en el mango), los repetidos llevan fase distinta y los números cuentan con capas que se relevan.
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from libreria.svg.base import *  # noqa
from libreria.svg.personajes import persona
from libreria.svg.objetos import casa as K, politica as P, tienda as TI, vuelo as V

OUT = ROOT / "content" / "lote9-03-precio-kilo"
OUT.mkdir(parents=True, exist_ok=True)
ARROZ_BANDA = "#2E7D4F"


def balda(x0, x1, y, alto=34):
    """Balda frontal del lineal (tabla con canto para colgar precios)."""
    return (sombra_caja(x0, y, x1 - x0, alto, 6, 0, 14, 0.25)
            + f'<rect x="{f(x0)}" y="{f(y)}" width="{f(x1-x0)}" height="{alto}" rx="6" fill="url(#baldaG)" stroke="{INK}" stroke-width="6"/>')


def caras(prefijo, x, y, s, exps, **kw):
    """Varias persona() idénticas en el mismo sitio con distinta cara (hide/fade para cambiarla)."""
    o = ""
    ps = []
    for e in exps:
        p = persona(f"{prefijo}_{e}", x, y, s, expresion=e, **kw)
        ps.append(p)
        o += p
    return o, ps[0]


def cuenta_cartel(prefijo, cx, cy, w, valores, col=YEL, moneda="€/kg"):
    """Cartel de precio que cuenta hacia arriba: una capa por valor; la última se llama `prefijo`."""
    o = ""
    for i, v in enumerate(valores):
        e, c = v.split(",")
        o += TI.cartel_precio(prefijo if i == len(valores) - 1 else f"{prefijo}_{i}", cx, cy, w, e, c, moneda, col=col)
    return o


# ---------------------------------------------------------------- 0. gancho: el pack ahorro al carro (full)
def gancho():
    fondo = TI.supermercado(rotulo="ARROZ Y LEGUMBRES")
    body = ""
    # balda de la derecha con el pack y su precio
    body += g("baldaG", balda(600, 1100, 790))
    body += TI.paquete("pack", 860, 790, 240, 300, texto="ARROZ", peso="5 kg", cinta="PACK AHORRO", banda=ARROZ_BANDA)
    # carrito (asa a la izquierda, en la mano del hombre)
    car = TI.carrito("carro", 666, 1300, 420, CORAL, lleno=False, espejo=True)
    # hombre de 45 con camisa de cuadros (tres caras para relevarlas)
    kw = dict(edad="adulto", piel="clara", pelo="corto", pelo_color="castano", ropa="camisa", ropa_color="#C0392B",
              pantalon_color="#3E5C93", accesorios=("barba",), brazos=("relajado", "coge"), mira=1)
    hom, p0 = caras("h", 330, 1300, 1.25, ("neutral", "risa", "sorpresa"), **kw)
    body += g("hombre", g("hombreB", hom))
    body += car
    # precio del pack: primero el grande y luego el que asusta (por kilo)
    body += TI.cartel_precio("precio1", 860, 885, 230, "4", "50", "€", col=YEL, cinta="AHORRO")
    body += TI.cartel_precio("precio2", 860, 885, 230, "1", "10", "€/kg", col=CORAL, cinta="MÁS CARO", fg="#FFFFFF")
    body += icono_alerta("alerta", 1010, 760, 46)
    body += destellos("brilla", 560, 640, 70, LIME)
    body += onomatopeya("ups", 590, 600, "¡OJO!", r=95, size=40, rot_=-10)
    guardar(f"{OUT}/gancho_full.svg", svg(body, "full", fondo=fondo))
    return p0


# ---------------------------------------------------------------- 1. dos precios (free)
def dos_precios():
    H = 860
    body = ""
    body += P.documento("boe", 205, 185, 290, 290, "BOE", "REAL DECRETO 3423/2000")
    body += sello("oblig", 220, 250, "OBLIGATORIO", size=40, rot_=-9)
    body += bandera("bandera", 820, 110, 170, 110, cols=("#C60B1E", "#FFC400", "#FFC400", "#C60B1E"), mastil=True)
    body += etiqueta("tesp", 820, 250, "ESPAÑA", bg=INK, fg=LIME, size=28)
    et = TI.etiqueta_lineal("et", 520, 565, 700, "ARROZ 500 g", "4,50 €", "9,00 €/kg")
    body += et
    px, py = et.puntos["precio"]
    ux, uy = et.puntos["unidad"]
    body += g("n1", _badge(px - 335, py - 10, "1", LIME))
    body += g("n2", _badge(ux + 245, uy - 4, "2", CORAL))
    body += etiqueta("tuni", 640, 828, "PRECIO POR UNIDAD DE MEDIDA", apunta=(ux + 60, uy + 52), desde=(500, 810), bg=LIME, fg=INK, size=27)
    guardar(f"{OUT}/precios_free.svg", svg(body, "free", h=H))


def _badge(cx, cy, n, col):
    return (f'<circle cx="{f(cx+4)}" cy="{f(cy+5)}" r="34" fill="{INK}" opacity="0.25"/>'
            f'<circle cx="{f(cx)}" cy="{f(cy)}" r="34" fill="{col}" stroke="{INK}" stroke-width="6"/>'
            + T(cx, cy + 15, n, 42, INK, font=DISP))


# ---------------------------------------------------------------- 2. el número pequeño (free)
def numero_pequeno():
    H = 860
    body = ""
    et = TI.etiqueta_lineal("et", 470, 215, 600, "ARROZ 500 g", "4,50 €", "9,00 €/kg")
    body += et
    ux, uy = et.puntos["unidad"]
    lx, ly = ux + 10, uy - 6
    zoom = (f'<rect x="{f(lx-140)}" y="{f(ly-140)}" width="280" height="280" fill="#F1F3F8"/>'
            + T(lx, ly - 18, "POR KG", 34, "#5A6170") + T(lx, ly + 44, "9,00 €", 54, INK, font=DISP))
    body += g("lupaG", lupa("lupa", lx, ly, 118, ang=40, contenido=zoom))
    body += etiqueta("tcuesta", 420, 470, "LO QUE CUESTA 1 KG", bg=INK, fg=LIME, size=26)
    base = 760
    iconos = [
        ("ikilo", V.pesa(None, 130, base, 170, "KG"), "€/KG"),
        ("ilitro", K.botella(None, 375, base, 230, "#F2C14E", etiqueta_col=TEAL, texto="ACEITE"), "€/LITRO"),
        ("ilavado", TI.producto("bote", 620, base, 1.55, VIO) + g(None, gota(668, base - 205, 30, "#8FD3FF")), "€/LAVADO"),
        ("irollo", TI.rollo_papel(None, 865, base, 1.0), "€/ROLLO"),
    ]
    for i, (iid, dib, txt) in enumerate(iconos):
        cx = (130, 375, 620, 865)[i]
        body += g(iid, dib)
        body += etiqueta(f"{iid}_t", cx, base + 55, txt, bg=LIME if i % 2 == 0 else "#FFFFFF", fg=INK, size=26)
    guardar(f"{OUT}/pequeno_free.svg", svg(body, "free", h=H))


# ---------------------------------------------------------------- 3. la misma regla: gana el pequeño (full)
def compara():
    fondo = TI.supermercado(rotulo="PASILLO 4", seed=8)
    body = g("baldaG", balda(-20, 1100, 1000, 40))
    body += TI.paquete("pq", 300, 1000, 170, 230, texto="ARROZ", peso="1 kg", banda=ARROZ_BANDA)
    body += TI.paquete("gr", 720, 1000, 330, 450, texto="ARROZ", peso="5 kg", cinta="AHORRO", banda=ARROZ_BANDA)
    gx, gy = TI.paquete(None, 720, 1000, 330, 450, cinta="AHORRO").puntos["cinta"]
    body += P.garabato("tacha", gx - 165, gx + 165, gy, 26, n=9, col=CORAL, sw=13)
    body += cuenta_cartel("cpq", 300, 1125, 230, ["0,50", "1,00", "1,50", "2,00"], col=LIME)
    body += cuenta_cartel("cgr", 720, 1125, 230, ["0,50", "1,00", "1,50", "2,00", "2,50"], col=YEL)
    body += K.trofeo("copa", 300, 760, 210, "GANA", "#FFC83D")
    body += confeti("conf", (130, 470, 480, 760), n=26, seed=4)
    body += etiqueta("tej", 540, 1262, "EJEMPLO INVENTADO", bg=INK, fg="#FFFFFF", size=26)
    body += etiqueta("tregla", 540, 505, "MISMA REGLA: € POR KILO", bg=LIME, fg=INK, size=30)
    guardar(f"{OUT}/compara_full.svg", svg(body, "full", fondo=fondo))


# ---------------------------------------------------------------- 4. la OCU: hasta un 82 % más (free)
def ocu():
    H = 880
    body = ""
    body += P.documento("doc", 195, 165, 290, 270, "OCU", "FORMATOS AHORRO")
    body += g("lupaO", lupa("lupao", 280, 230, 62, ang=45))
    base = 690
    body += g("eje", f'<path d="M 420 {base} L 960 {base}" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>')
    body += barra("bnor", 470, base, 170, 200, LIME)
    body += barra("bgra", 730, base, 170, 364, CORAL)
    body += TI.paquete("ppq", 555, base + 150, 100, 130, texto="ARROZ", peso="1 kg", banda=ARROZ_BANDA)
    body += TI.paquete("pgr", 815, base + 182, 150, 172, texto="ARROZ", peso="5 kg", banda=ARROZ_BANDA)
    body += etiqueta("tnor", 555, 455, "NORMAL", bg="#FFFFFF", fg=INK, size=26)
    for i, v in enumerate(("+0 %", "+20 %", "+41 %", "+62 %", "+82 %")):
        body += contador("c82" if i == 4 else f"c82_{i}", 815, 265, v, w=250, h=96, size=52)
    body += etiqueta("tuni", 195, 470, "POR KILO O LITRO", bg=LIME, fg=INK, size=27)
    body += etiqueta("text", 195, 560, "EN EL CASO", bg=INK, fg=LIME, size=27)
    body += etiqueta("text2", 195, 625, "MÁS EXTREMO", bg=INK, fg=LIME, size=27)
    guardar(f"{OUT}/ocu_free.svg", svg(body, "free", h=H))


# ---------------------------------------------------------------- 5. reclama (free)
def reclama():
    H = 880
    body = ""
    body += cartel("cartel", 330, 85, "PACK AHORRO", size=40, bg=YEL, fg=INK)
    body += sello("falso", 380, 150, "NO ES AHORRO", size=38, rot_=-6)
    body += TI.paquete("packR", 300, 800, 300, 420, texto="ARROZ", peso="5 kg", cinta="PACK AHORRO", banda=ARROZ_BANDA)
    body += P.formulario("hoja", 300, 545, 420, 560, "HOJA DE RECLAMACIONES", "CONSUMO", ("PACK AHORRO", "NO AHORRA"))
    fx, fy = 300 + 420 * 0.12, 545 + 560 * 0.4
    body += P.boli("boli", fx + 60, fy - 20, 170, 30)
    # mujer de 35 con el móvil en alto haciendo la foto a la etiqueta
    mu = persona("mu", 760, 870, 0.8, "adulto", "morena", "coleta", "negro", "jersey", TEAL, "#3E5C93",
                 expresion="neutral", brazos=("cintura", "sujeta"), mira=-1)
    hx, hy = mu.puntos["mano_der"]
    pant = TI.etiqueta_lineal(None, 0, 0, 150, "ARROZ", "4,50 €", "9,00 €/kg")
    mx, my = hx + 5, hy - 150
    px0, py0, px1, py1 = K.movil(None, mx, my, 120).puntos["pantalla"]
    foto = f'<g transform="translate({f((px0+px1)/2)} {f((py0+py1)/2)})">{pant}</g>'
    body += g("mujer", g("mujerB", mu))
    body += g("movilG", K.movil("movil", mx, my, 120, pantalla=g("foto", foto)))
    body += g("flash", f'<circle cx="{f(mx)}" cy="{f(my)}" r="120" fill="#FFFFFF" opacity="0.85"/>' + chispa(None, mx, my, 60, "#FFFFFF"))
    guardar(f"{OUT}/reclama_free.svg", svg(body, "free", h=H))
    return mu


if __name__ == "__main__":
    gancho()
    dos_precios()
    numero_pequeno()
    compara()
    ocu()
    reclama()
    print("ok")

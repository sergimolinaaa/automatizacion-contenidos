"""Catálogo del estilo PAPEL: piezas de la librería ya convertidas con a_papel(), personas con estilo="papel" y los fondos.

Uso:  python3 libreria/catalogo_papel.py entregas/estilos/catalogo_papel.png
Reutiliza la maquetación y la captura de catalogo.py (Chromium headless de /opt/pw-browsers).
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from libreria import catalogo as CAT  # noqa: E402
from libreria.svg.base import *  # noqa: E402,F401
from libreria.svg.personajes import persona  # noqa: E402
from libreria.svg.papel import a_papel, fondo_neutro, fondo_calle, fondo_casa, fondo_cielo, grano, PAPEL as PP  # noqa: E402
from libreria.svg.objetos import politica as P, casa as C, cuerpo as CU, animales as AN, tecnologia as TE, dinero as D  # noqa: E402


def celdas():
    out = []

    def add(t, c, w=1000, h=700, fondo=None):
        fondo = fondo if fondo is not None else fondo_neutro(w, h, motas=False)
        out.append((t, w, h, fondo + c + grano(w, h), True))

    # ---------------- personas
    s = persona("pa", 230, 660, 0.95, "adulto", "media", "largo", "castano", "jersey", CORAL, estilo="papel",
                expresion="duda", brazos=("relajado", "explica"))
    s += persona("pb", 520, 660, 0.95, "joven", "clara", "corto", "castano", "abrigo", "#2F6FD9", estilo="papel",
                 accesorios=("gorro", "bufanda"), expresion="frio", brazos=("cruzados", "cruzados"))
    s += persona("pc", 800, 660, 0.95, "mayor", "morena", "calvo", "canoso", "camisa", TEAL, estilo="papel",
                 accesorios=("gafas", "bigote"), expresion="risa", brazos=("cintura", "saluda"))
    add('persona(estilo="papel")', s)
    s = persona("pd", 260, 660, 0.95, "nino", "oscura", "rizado", "negro", "camiseta", AMARILLO, estilo="papel",
                expresion="sorpresa", brazos=("arriba", "arriba"))
    s += a_papel(persona("pe", 640, 660, 0.95, "adulto", "clara", "coleta", "rubio", "chaqueta", VIO,
                         expresion="neutral", brazos=("relajado", "senala")), 1)
    add('niño papel · a_papel(persona pegatina)', s)

    # ---------------- cuerpo
    s = a_papel(CU.cerebro("cb", 300, 300, 0.9), 2) + a_papel(CU.termometro("tm", 760, 120, 420, 0.75, CORAL, texto="39 °C"), 3)
    add("cuerpo: cerebro · termometro", s)
    s = a_papel(CU.mano("mn", 300, 360, 1.3), 4) + a_papel(CU.musculo("m1", 700, 300, 240, 80, contraido=True), 5)
    add("cuerpo: mano · musculo", s)

    # ---------------- tecnología
    pant = f'<rect x="0" y="0" width="1000" height="1000" fill="#EEF2FA"/>' + T(220, 330, "13 %", 54, CORAL, font=DISP)
    s = a_papel(C.movil("mv", 220, 350, 280, pantalla=pant), 6) + a_papel(TE.bateria("bt", 520, 350, 160, 300, nivel=0.25), 7)
    s += a_papel(TE.chip("ch", 820, 350, 200), 8)
    add("tecnologia: movil · bateria · chip", s)

    # ---------------- política
    s = a_papel(P.urna("u", 260, 620, 280, 300, texto="CONGRESO"), 9)
    s += a_papel(P.dni("dn", 700, 230, 300, rot_=5), 10, filtro="papelFino")
    s += a_papel(P.sobre(700, 520, 220, 150, id_="so"), 11)
    add("politica: urna · dni · sobre", s)
    reparto, _ = P.dhondt({"ESTRELLA": 38000, "CÍRCULO": 30000, "TRIÁNGULO": 17900, "CUADRADO": 10000}, 30, validos=100000)
    s = a_papel(P.hemiciclo("hm", 500, 560, 30, 3, 220, 380, P.colores_reparto(reparto), r_esc=24), 12, filtro="papelFino")
    add("politica: hemiciclo", s)

    # ---------------- casa
    s = a_papel(C.taza("tz", 200, 600, 200), 13) + a_papel(C.bombilla("bb", 480, 300, 170), 14)
    s += a_papel(C.reloj("rl", 800, 300, 130), 15) + a_papel(D.saco_dinero("sd", 780, 660, 220), 16)
    add("casa: taza · bombilla · reloj · saco_dinero", s)
    s = a_papel(C.sofa("sf", 300, 620, 460, 120, respaldo=170), 17) + a_papel(C.ventana("vn", 780, 330, 260, 320), 18)
    add("casa: sofa · ventana", s)

    # ---------------- animales
    s = a_papel(AN.perro("pr", 280, 660, 1.2), 19) + a_papel(AN.gato("ga", 740, 360, 1.0), 20)
    add("animales: perro · gato", s)

    # ---------------- fondos (miniaturas 1080x1920)
    for t, fnd in (("fondo_calle('dia')", fondo_calle("dia")), ("fondo_calle('noche')", fondo_calle("noche")),
                   ("fondo_casa()", fondo_casa()), ("fondo_cielo('tarde')", fondo_cielo("tarde")),
                   ("fondo_neutro()", fondo_neutro())):
        out.append((t, 1080, 1920, fnd + grano(), False))
    return out


def main():
    CAT.celdas = celdas
    CAT.COLS = 5
    if len(sys.argv) < 2:
        sys.argv.append(os.path.join(ROOT, "entregas", "estilos", "catalogo_papel.png"))
    CAT.main()


if __name__ == "__main__":
    main()

"""Dibujos de lote8-07-basilisco. Uso: python3 libreria/archivo/basilisco/dib.py"""
import sys
sys.path.insert(0, "/home/user/automatizacion-contenidos")
from libreria.svg.base import *
from libreria.svg.personajes import persona
from libreria.svg.objetos import reptiles as R

OUT = "/home/user/automatizacion-contenidos/content/lote8-07-basilisco/"


# ------------------------------------------------------------- 1. gancho (full)
def gancho():
    AY = 1000
    b_a = R.basilisco("ba", 560, 850, 1.05, "a")
    b_b = R.basilisco("bb", 560, 850, 1.05, "b")
    pie = b_a.puntos["pie"]
    estela = g("estela", "".join(f'<ellipse cx="{x}" cy="{AY + 18}" rx="{r}" ry="{r*0.28:.0f}" fill="none" stroke="#FFFFFF" stroke-width="6" opacity="0.85"/>'
                                 for x, r in ((420, 60), (300, 75), (170, 90))))
    spl = R.salpicadura("spl", pie[0] + 10, AY + 6, 0.7)
    vel = g("vel", lineas_velocidad(150, 760, 4, 110, 40))
    corre = g("corre", estela + vel + b_a + b_b + spl)
    duda = icono_duda("duda", 900, 560, 52)
    cart = cartel("cjesus", 540, 1180, "LAGARTO JESUCRISTO", 44)
    sh = sello("sagua", 820, 1090, "¡SIN HUNDIRSE!", 34, -6)
    body = corre + duda + sh + cart
    guardar(OUT + "gancho_full.svg", svg(body, "full", fondo=R.selva_rio(1080, 1920, AY)))


# ------------------------------------------------------------- 2. pata con flecos (panel)
def pata():
    pc = R.pata_basilisco("pc", 290, 520, 0.9, abiertos=False)
    po = R.pata_basilisco("po", 290, 520, 0.9, abiertos=True)
    tip = po.puntos["dedos"][3]
    lab = etiqueta("lflecos", 640, 120, "FLECOS DE ESCAMAS", apunta=(tip[0] - 10, tip[1] + 40), size=28)
    # huellas en el agua
    hp = g("hpeq", f'<ellipse cx="760" cy="300" rx="55" ry="22" fill="{degradado(AGUA, 0.2)}" stroke="{INK}" stroke-width="6"/>'
           + T(760, 360, "SIN FLECOS", 24, INK))
    hg = g("hgran", f'<ellipse cx="760" cy="510" rx="150" ry="56" fill="{degradado(AGUA, 0.2)}" stroke="{INK}" stroke-width="6"/>'
           + brillo("M 650 495 Q 700 470 760 468", 6, 0.7) + T(760, 610, "CON FLECOS", 24, INK))
    fl = flecha("fgrande", (760, 385), (760, 440), CORAL, 12, 26)
    tag = etiqueta("lpisada", 760, 220, "PISADA", size=28, bg=LIME, fg=INK)
    body = pc + po + hp + fl + hg + tag + lab
    guardar(OUT + "pata.svg", svg(body, "panel", fondo=fondo_suave()))


# ------------------------------------------------------------- 3. pisada en 3 fases (free)
def secuencia():
    H, SUP = 900, 380
    agua = R.agua_corte(0, 1000, SUP, 880)
    sep = "".join(f'<line x1="{x}" y1="40" x2="{x}" y2="870" stroke="#FFFFFF" stroke-width="4" stroke-dasharray="10 14" opacity="0.6"/>' for x in (335, 665))
    # fase 1: golpe
    p1 = R.pie_lateral("f1_pie", 140, SUP - 120, 0.9, pierna=220)
    f1 = g("f1", g("f1_pierna", p1)
           + R.salpicadura("f1_spl", 200, SUP + 4, 0.75)
           + g("f1_vel", lineas_velocidad(70, 140, 3, 60, 30, "#FFFFFF", 1).replace("rotate", "rotate"))
           + flecha("f1_flecha", (290, 90), (290, 300), CORAL, 12, 28)
           + onomatopeya("f1_plaf", 250, 560, "¡PLAF!", 90, 38)
           + etiqueta("f1_lab", 168, 840, "1 · GOLPE", size=28))
    # fase 2: bolsa de aire
    b2 = R.bolsa_aire("f2_bolsa", 500, SUP, 230, 290, 0)
    p2 = R.pie_lateral("f2_pie", 455, SUP + 250, 0.8, pierna=380)
    f2 = g("f2", b2 + p2
           + etiqueta("f2_aire", 595, 470, "AIRE", size=26, bg="#FFFFFF", fg=INK)
           + flecha("f2_ag1", (420, 700), (360, 760), "#BFE6FF", 9, 22)
           + flecha("f2_ag2", (580, 700), (640, 760), "#BFE6FF", 9, 22)
           + flecha("f2_up", (500, 800), (500, 700), LIME, 16, 34)
           + etiqueta("f2_lab", 500, 840, "2 · BOLSA DE AIRE", size=26))
    # fase 3: saca la pata antes de que se cierre
    b3a = R.bolsa_aire("f3_ab", 830, SUP, 230, 260, 0.45)
    b3c = R.bolsa_aire("f3_ce", 830, SUP, 230, 260, 1)
    p3 = R.pie_lateral("f3_pie", 790, SUP + 220, 0.8, pierna=360)
    gotas = g("f3_gotas", gota(860, SUP - 140, 22, "#BFE6FF") + gota(900, SUP - 90, 18, "#BFE6FF") + gota(820, SUP - 70, 16, "#BFE6FF"))
    f3 = g("f3", b3a + b3c + p3 + gotas
           + flecha("f3_up", (940, 330), (940, 120), LIME, 14, 30)
           + icono_ok("f3_ok", 940, 560, 44)
           + etiqueta("f3_lab", 832, 840, "3 · SACA LA PATA", size=26))
    body = agua + sep + f1 + f2 + f3
    guardar(OUT + "secuencia_free.svg", svg(body, "free", h=H))


# ------------------------------------------------------------- 4. Nature 1996 y 4,5 m (panel)
def nature():
    mini_portada = (R.agua_corte(12, 228, 230, 300, ondas=True)
                    + f'<g transform="translate(120 190) scale(0.2) translate(-560 -850)">{R.basilisco("rv_b", 560, 850, 1)}</g>')
    rv = R.revista("rv", 190, 340, 240, 320, "nature", "1996", mini_portada)
    nom = etiqueta("lnom", 190, 560, "GLASHEEN Y McMAHON", size=22)
    s96 = sello("s96", 330, 170, "1996", 40, 10)
    SUP = 470
    pista = R.agua_corte(400, 960, SUP, 650)
    mini = g("mini", R.basilisco("mb", 520, SUP - 0.3 * 152, 0.3, "a"))
    estela = g("estela", "".join(f'<ellipse cx="{x}" cy="{SUP+4}" rx="22" ry="7" fill="none" stroke="#FFFFFF" stroke-width="5"/>' for x in range(560, 900, 50)))
    regla = f'<rect x="460" y="575" width="440" height="40" rx="6" fill="{degradado(YEL, 0.2)}" stroke="{INK}" stroke-width="5"/>'
    regla += "".join(f'<line x1="{460 + i*44}" y1="575" x2="{460 + i*44}" y2="{597 if i % 2 else 607}" stroke="{INK}" stroke-width="4"/>' for i in range(1, 10))
    regla = g("regla", regla)
    l45 = etiqueta("l45", 700, 290, "UNOS 4,5 METROS", size=28, bg=LIME, fg=INK)
    hunde = R.salpicadura("hunde", 910, SUP + 2, 0.4)
    body = pista + estela + regla + mini + hunde + l45 + rv + nom + s96
    guardar(OUT + "nature.svg", svg(body, "panel", fondo=fondo_suave()))


# ------------------------------------------------------------- 5. ¿y una persona? (full)
def persona_agua():
    AY = 1000
    yo = persona("yo", 330, 1290, 1.2, "adulto", "media", "corto", "castano", "camiseta", CORAL,
                 expresion="sorpresa", brazos=("arriba", "saluda"))
    frente = (f'<rect x="0" y="1070" width="1080" height="850" fill="url(#rioG)"/>'
              f'<path d="M 0 1070 ' + " ".join("q 30 -12 60 0 t 60 0" for _ in range(9)) + f'" fill="none" stroke="{INK}" stroke-width="6"/>')
    ondas = g("ondas", f'<ellipse cx="330" cy="1080" rx="190" ry="40" fill="none" stroke="#FFFFFF" stroke-width="7"/>'
              f'<ellipse cx="330" cy="1080" rx="260" ry="58" fill="none" stroke="#FFFFFF" stroke-width="5" opacity="0.6"/>')
    no = icono_no("no", 520, 560, 50)
    med = medidor("vel", 800, 600, 160, 0.5)
    cnt = contador("c100", 800, 700, "+100 KM/H", None, w=330, h=96)
    b1 = barra("b1", 640, 1170, 120, 30, GRIS, None, "TÚ")
    b2 = barra("b2", 830, 1170, 120, 300, CORAL, None, "×15")
    lb = etiqueta("lpot", 800, 1225, "POTENCIA DE PIERNAS", size=24)
    body = g("yo_g", yo) + frente + ondas + no + med + cnt + b1 + b2 + lb
    guardar(OUT + "persona_full.svg", svg(body, "full", fondo=R.selva_rio(1080, 1920, AY)))


if __name__ == "__main__":
    gancho(); pata(); secuencia(); nature(); persona_agua()

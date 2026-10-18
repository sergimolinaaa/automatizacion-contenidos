"""SVG de content/lote7-05-picadura (¿Por qué te pica una picadura y rascarte lo empeora?).
Uso: python3 libreria/archivo/picadura/dib.py"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from libreria.svg.base import *  # noqa
from libreria.svg.personajes import persona, EDADES
from libreria.svg.objetos import cuerpo as C, piel as PI

OUT = ROOT / "content" / "lote7-05-picadura"
SEROT = "#4FB3FF"


# ---------------------------------------------------------------- 0. gancho (full): niño en la piscina
def gancho():
    esc = 1.75
    p = persona("nino_p", 540, 1310, esc, "nino", "clara", "corto", "castano", "camiseta", TEAL,
                pantalon_color=CORAL, zapato_color="#2F7FD6", expresion="triste", brazos=("cruzados", "sujeta"))
    hx, hy = p.puntos["cabeza"]
    cap = PI.gorra(None, hx, hy, EDADES["nino"]["rx"] * esc, col=YEL)
    body = g("nino", p + cap)
    sx, sy = p.puntos["hombro_der"]
    mx, my = p.puntos["mano_der"]
    bx, by = sx + (mx - sx) * 0.5 + 34, sy + (my - sy) * 0.5 + 40
    body += PI.habon("bulto", bx, by, 54, 24, arriba=True)
    body += PI.rayitas_picor("picor", bx, by, 52, 7, a0=-20)
    body += PI.mosquito("mosq", 820, 520, 1.15, ang=8)
    body += g("zumbido", ondas_sonido(None, 690, 500, 30, 2, 150, 220, 22, 6, INK))
    return svg(body, "full", fondo=PI.piscina(agua_y0=700, agua_y1=1060))


# ---------------------------------------------------------------- 1. saliva del mosquito (panel)
def saliva():
    sup = 330
    pc = PI.piel_corte("piel", 40, sup, 920, 320)
    body = pc
    m = PI.mosquito("mosq", 0, 0, 1.2, ang=-12)
    tx, ty = m.puntos["trompa"]
    ox, oy = 470 - tx, sup + 6 - ty
    body += f'<g id="mosq_g"><g transform="translate({f(ox)} {f(oy)})">{m}</g></g>'
    cx_, cy_ = m.puntos["cabeza"]
    dx, dy = tx - cx_, ty - cy_
    L = (dx * dx + dy * dy) ** 0.5
    ux, uy = dx / L, dy / L
    p0 = (470, sup + 6)
    p1 = (470 + ux * 95, sup + 6 + uy * 95)
    body += g("aguja", f'<path d="M {f(p0[0])} {f(p0[1])} L {f(p1[0])} {f(p1[1])}" fill="none" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>'
              f'<path d="M {f(p0[0])} {f(p0[1])} L {f(p1[0])} {f(p1[1])}" fill="none" stroke="#8A91A6" stroke-width="3.5" stroke-linecap="round"/>')
    for i, (gx, gy) in enumerate(((p1[0] - 20, p1[1] + 24), (p1[0] + 22, p1[1] + 14), (p1[0] - 2, p1[1] + 44), (p1[0] + 40, p1[1] + 40))):
        body += PI.gota_saliva(f"sal{i}", gx, gy, 13)
    body += etiqueta("lsal", 230, 230, "SALIVA", apunta=(p1[0] - 20, p1[1] + 24), size=30)
    body += etiqueta("lanti", 790, 215, "ANTICOAGULANTE", size=30, bg=LIME, fg=INK)
    body += g("lanti2", T(790, 280, "NO DEJA QUE LA SANGRE", 24, INK) + T(790, 310, "SE CUAJE", 24, INK))
    vx, vy = pc.puntos["vaso"]
    body += flecha("fsangre", (760, vy), (560, vy), col="#FFFFFF", w=10, punta=24)
    return svg(body, "panel", fondo=fondo_suave())


# ---------------------------------------------------------------- 2. histamina (panel)
def histamina():
    mt = PI.mastocito("mast", 290, 390, 150)
    body = mt
    body += etiqueta("ldef", 290, 165, "CÉLULA DE DEFENSA", size=28)
    prot = ""
    for i, (x, y) in enumerate(((560, 230), (610, 330), (555, 430))):
        prot += PI.gota_saliva(None, x, y, 20) + icono_duda(None, x + 34, y - 36, 20)
    body += g("prot", prot)
    body += PI.histamina("hist1", 470, 300, 70, 12, seed=2)
    body += PI.histamina("hist2", 470, 470, 70, 12, seed=8)
    s = PI.sirena("sirena", 830, 390, 1.15)
    body += s
    body += etiqueta("lhist", 560, 600, "HISTAMINA", size=32, bg=YEL, fg=INK)
    body += etiqueta("lalarma", 830, 470, "LA ALARMA", size=28)
    return svg(body, "panel", fondo=fondo_suave())


# ---------------------------------------------------------------- 3. el bulto (free)
def bulto():
    body = ""
    cer = C.cerebro("cer", 230, 150, 0.5, hipotalamo=False)
    body += cer
    pc = PI.piel_corte("piel", 50, 560, 470, 250, pelos=False, seed=7)
    body += pc
    body += PI.habon("bulto", 290, 562, 230, 86, halo=False, corte=True)
    d = "M 330 690 C 430 660, 470 560, 450 450 C 430 360, 300 360, 236 300"
    body += g("nervio", trazo(d, 14, "#FFD23F", 8))
    body += g("nervio_on", f'<path d="{d}" fill="none" stroke="#FFF7C2" stroke-width="7" stroke-linecap="round"/>')
    body += etiqueta("lnervio", 560, 420, "NERVIO", size=30, bg=YEL, fg=INK)
    body += PI.rayitas_picor("picor_cer", 230, 170, 120, 8, a0=10)
    a = C.antebrazo("brazo", (620, 800), (860, 400), ancho=92, piel="clara", vello=False, manga=TEAL)
    body += a
    ax, ay = a.puntos["centro"]
    body += PI.habon("bulto_ext", ax - 6, ay - 6, 80, arriba=True)
    body += etiqueta("lbulto", 760, 250, "BULTO ROJO", apunta=(ax - 6, ay - 40), size=32, bg=CORAL, fg="#FFFFFF")
    return svg(body, "free", h=840)


# ---------------------------------------------------------------- 4. rascar = dolor leve (panel)
def rascar():
    pa, pb, pc_, pl = ("#FCDCC3", "#F3BE98", "#E3A07A", "#C98763")
    body = (sombra_caja(60, 300, 880, 330, 40) + f'<rect x="60" y="300" width="880" height="330" rx="40" fill="url(#pielL_clara)" stroke="{INK}" stroke-width="7"/>'
            + '<g fill="#D9A07C" opacity="0.6">' + "".join(f'<circle cx="{x}" cy="{y}" r="4"/>' for x, y in
                                                         ((120, 360), (210, 560), (330, 340), (700, 580), (820, 380), (890, 520), (160, 470), (600, 360)))
            + "</g>" + brillo("M 110 330 L 880 330", 6, 0.5))
    hb = PI.habon("hab", 430, 470, 120, arriba=True)
    body += hb
    body += PI.rayitas_picor("picor", 430, 470, 100, 8)
    rayas = "".join(f'<path d="M {x} 420 C {x + 20} 460, {x + 10} 500, {x + 30} 540" fill="none" stroke="#F06A78" stroke-width="9" stroke-linecap="round"/>' for x in (520, 552, 584, 616))
    body += g("rayas", rayas)
    body += PI.mano_rasca("mano", 610, 520, 0.85, piel="clara", manga=TEAL)
    ch = chispa(None, 520, 380, 28, CORAL) + chispa(None, 660, 400, 22, CORAL) + chispa(None, 600, 600, 24, CORAL)
    body += g("chispas", ch)
    body += etiqueta("ldolor", 200, 200, "DOLOR LEVE", size=32, bg=CORAL, fg="#FFFFFF")
    body += etiqueta("lpicor", 230, 560, "PICOR", size=30, bg=YEL, fg=INK)
    body += PI.reloj_arena("reloj", 880, 170, 170)
    body += etiqueta("lmomento", 700, 140, "UN RATO", size=28)
    return svg(body, "panel", fondo=fondo_suave())


# ---------------------------------------------------------------- 5. serotonina (full)
def serotonina():
    body = ""
    cer = C.cerebro("cer", 600, 600, 0.85, hipotalamo=False)
    body += cer
    body += g("medula", trazo("M 600 820 L 600 1190", 44, "#E996A4", 8))
    rojo = "M 600 900 C 520 920, 470 980, 450 1210"
    amar = "M 600 960 C 680 980, 730 1040, 750 1210"
    body += g("c_rojo", trazo(rojo, 16, CORAL, 8))
    body += g("c_amar", trazo(amar, 16, "#FFD23F", 8))
    body += g("amar_on", f'<path d="{amar}" fill="none" stroke="#FFF36B" stroke-width="44" stroke-linecap="round" opacity="0.45"/>'
              f'<path d="{amar}" fill="none" stroke="#FFFBD0" stroke-width="10" stroke-linecap="round"/>')
    body += etiqueta("ldolor", 340, 1180, "DOLOR", size=30, bg=CORAL, fg="#FFFFFF")
    body += etiqueta("lpicor", 880, 1180, "PICOR", size=30, bg=YEL, fg=INK)
    bolas = ""
    for i, (x, y) in enumerate(((588, 836), (614, 850), (596, 868), (622, 878), (604, 892))):
        bolas += f'<circle cx="{x}" cy="{y}" r="15" fill="{degradado_brillo(SEROT)}" stroke="{INK}" stroke-width="4"/>'
    body += g("sero", bolas)
    body += etiqueta("lsero", 860, 860, "SEROTONINA", size=32, bg=SEROT, fg=INK, apunta=(630, 870))
    body += etiqueta("lmens", 860, 930, "MENSAJERO QUÍMICO", size=24, bg="#FFFFFF", fg=INK)
    r = PI.raton_lab("raton", 230, 1010, 0.85)
    body += r
    body += etiqueta("lraton", 230, 1060, "EN RATONES", size=28)
    return svg(body, "full", fondo=fondo_suave(1080, 1920, "#1B2C66", "#3554B8", seed=9))


# ---------------------------------------------------------------- 6. círculo vicioso (free)
def circulo():
    cx, cy, r = 250, 300, 165
    body = ""
    fl = flecha(None, (cx + 20, cy - r), (cx + 10, cy + r), col=LIME, w=16, punta=34, ctrl=(cx + r * 1.4, cy - r * 0.7), ctrl2=(cx + r * 1.4, cy + r * 0.7))
    fl += flecha(None, (cx - 20, cy + r), (cx - 10, cy - r), col=LIME, w=16, punta=34, ctrl=(cx - r * 1.4, cy + r * 0.7), ctrl2=(cx - r * 1.4, cy - r * 0.7))
    body += g("ciclo", fl)
    ic = PI.habon(None, cx, cy - 55, 60, arriba=True) + PI.rayitas_picor(None, cx, cy - 55, 44, 7)
    body += g("ic_picor", ic)
    body += g("ic_mano", PI.mano_rasca(None, cx - 20, cy + 110, 0.38, piel="clara", manga=TEAL))
    body += etiqueta("lmas1", cx, 85, "MÁS PICOR", size=28, bg=YEL, fg=INK)
    body += etiqueta("lmas2", cx, 520, "MÁS RASCAR", size=28)
    # piel con herida
    body += (sombra_caja(560, 110, 400, 240, 34) + f'<rect x="560" y="110" width="400" height="240" rx="34" fill="url(#pielL_clara)" stroke="{INK}" stroke-width="7"/>')
    h = PI.habon("hab", 760, 230, 130, arriba=True, herida=True)
    body += h
    for i, (x, y, a) in enumerate(((610, 70, 20), (930, 70, -30), (930, 410, 40))):
        body += g(f"bac{i}", PI.bacteria(None, x, y, 0.75, a))
    esc = 1.15
    ab = persona("abu", 800, 800, esc, "mayor", "clara", "mono", "canoso", "jersey", VIO, accesorios=("gafas",),
                 expresion="enfado", pose="busto", brazos=("relajado", "apunta_arriba"))
    body += g("abuela", ab + PI.delantal(None, 800, 800, esc, "mayor", col=ROSA, busto=True))
    body += globo("globo", 470, 660, "¡NO TE RASQUES!", cola=(640, 640), size=30)
    return svg(body, "free", h=800)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in (("gancho_full.svg", gancho), ("saliva.svg", saliva), ("histamina.svg", histamina),
                     ("bulto_free.svg", bulto), ("rascar.svg", rascar), ("serotonina_full.svg", serotonina),
                     ("circulo_free.svg", circulo)):
        guardar(str(OUT / name), fn())

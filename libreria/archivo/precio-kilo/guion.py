"""Genera content/lote9-03-precio-kilo/guion.json (anims con método rossark). Uso: python3 libreria/archivo/precio-kilo/guion.py"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "content" / "lote9-03-precio-kilo" / "guion.json"


def H(t, e, tr=None, **k):
    d = dict(target=t, effect=e)
    if tr:
        d["trigger"] = tr
    d.update(k)
    return d


def cuenta(prefijo, n, triggers, sfx_final="ding"):
    """Capas prefijo_0 … prefijo_{n-2}, prefijo: cada una entra (fade corto) y la anterior se oculta: el número sube."""
    ids = [f"{prefijo}_{i}" for i in range(n - 1)] + [prefijo]
    out = []
    for i, (cid, tr) in enumerate(zip(ids, triggers)):
        k = dict(dur=0.12)
        if i == n - 1:
            k["sfx"] = sfx_final
        out.append(H(cid, "fade", tr, **k))
        if i > 0:
            out.append(H(ids[i - 1], "hide", tr))
    return out


def persona_viva(pid, phase=0.0, blink_delay=0.6):
    """Persona natural: ojos que parpadean, cabeza que oscila sobre el cuello con retraso respecto al cuerpo."""
    return [H(f"{pid}_ojos", "blink", delay=blink_delay),
            H(f"{pid}_cabeza", "sway", origin="bottom", amount=0.28, delay=0.35 + phase)]


# ---------------------------------------------------------------- 0. gancho
caras = ("h_neutral", "h_risa", "h_sorpresa")
s0 = [H("h_risa", "hide"), H("h_sorpresa", "hide"),
      H("hombre", "sway", origin="bottom", amount=0.16, delay=0.1),
      H("hombreB", "breathe", origin="bottom", amount=0.6, phase=0.25),
      H("carro", "slide-right", delay=0.0, dur=0.6, sfx="whoosh"),
      H("carro_ruedas", "wiggle", amount=0.25, delay=0.6),
      H("baldaG", "slide-left", delay=0.05, dur=0.5),
      H("pack", "slide-left", delay=0.05, dur=0.5),
      H("precio1", "slide-left", delay=0.15, dur=0.5),
      H("pack_cinta", "pulse", amount=0.35, delay=0.6)]
for i, c in enumerate(caras):
    s0 += persona_viva(c, phase=0.0, blink_delay=0.5 + 0.1 * i)
    s0 += [H(f"{c}_brazo_der", "wiggle", origin="top-left", amount=0.12, delay=0.9),
           H(f"{c}_brazo_izq", "move", "barato", rotate=14, origin="top-right", dur=0.5),
           H(f"{c}_brazo_izq", "move", "Quizá", rotate=-14, origin="top-right", dur=0.6),
           H(f"{c}_cabeza", "move", "pack", rotate=5, origin="bottom", dur=0.5),
           H(f"{c}_cabeza", "move", "pagas", rotate=-9, origin="bottom", dur=0.4)]
s0 += [H("pack", "move", "Coges", to=[-90, -110], rotate=-8, dur=0.45, sfx="whoosh"),
       H("pack", "move", "ahorro", to=[-90, 470], rotate=8, dur=0.55, sfx="boing"),
       H("carro", "punch", "porque", amount=0.15),
       H("h_neutral", "hide", "barato"), H("h_risa", "fade", "barato", dur=0.15),
       H("brilla", "pop", "barato", sfx="brillo"), H("brilla", "spin", "barato", amount=0.2),
       H("precio1", "punch", "sale", amount=0.25),
       H("precio1", "shake", "Quizá", amount=0.5),
       H("precio1", "hide", "pagas"), H("precio2", "pop", "pagas", sfx="sorpresa"),
       H("h_risa", "hide", "pagas"), H("h_sorpresa", "fade", "pagas", dur=0.15),
       H("alerta", "pop", "pagas", origin="bottom"), H("alerta", "wiggle", "pagas", amount=0.5, origin="bottom"),
       H("ups", "pop", "más", sfx="pop"), H("ups", "hide", "Quizá"),
       H("brilla", "hide", "Quizá"),
       ]
# «¡OJO!» al final, en el segundo «más»
s0 = [a for a in s0 if a["target"] != "ups"] + [H("ups", "pop", "pagas", sfx="pop"), H("ups", "float", "pagas", amount=0.4)]

# ---------------------------------------------------------------- 1. dos precios
s1 = [H("et", "slide-up", delay=0.0, dur=0.55, sfx="whoosh"),
      H("et", "float", amount=0.12, delay=0.6),
      H("bandera", "slide-down", "España", dur=0.45), H("bandera", "sway", "España", origin="left", amount=0.35),
      H("tesp", "pop", "España"),
      H("boe", "slide-right", "ley", dur=0.5, sfx="papel"), H("boe", "float", "ley", amount=0.15),
      H("oblig", "pop", "obliga", sfx="sello"), H("oblig", "punch", "obliga", amount=0.4),
      H("et_precio", "pop", "precios", sfx="pop"), H("et_unidad", "hide"),
      H("n1", "pop", "paquete", sfx="pop"), H("n1", "bob", "paquete", amount=0.3),
      H("et_precio", "punch", "paquete", amount=0.25),
      H("et_unidad", "pop", "unidad", sfx="pop"),
      H("n2", "pop", "unidad", sfx="pop"), H("n2", "bob", "unidad", amount=0.3),
      H("tuni", "pop", "medida", sfx="ding"), H("et_unidad", "pulse", "medida", amount=0.5)]

# ---------------------------------------------------------------- 2. el número pequeño
s2 = [H("et", "slide-down", delay=0.0, dur=0.5, sfx="whoosh"), H("et", "float", amount=0.1, delay=0.5),
      H("lupaG", "slide-left", delay=0.25, dur=0.6, sfx="whoosh"),
      H("lupaG", "sway", origin="bottom-right", amount=0.25, delay=0.85),
      H("lupaG", "punch", "pequeño", amount=0.3, sfx="ding"),
      H("tcuesta", "pop", "cuesta", sfx="pop"),
      H("ikilo", "pop", "kilo", sfx="pop"), H("ikilo_t", "slide-up", "kilo", dur=0.35),
      H("ikilo", "sway", "kilo", origin="bottom", amount=0.15),
      H("ilitro", "pop", "litro", sfx="pop"), H("ilitro_t", "slide-up", "litro", dur=0.35),
      H("ilitro", "sway", "litro", origin="bottom", amount=0.18),
      H("ilavado", "pop", "lavado", sfx="pop"), H("ilavado_t", "slide-up", "lavado", dur=0.35),
      H("ilavado", "sway", "lavado", origin="bottom", amount=0.14),
      H("irollo", "pop", "rollo", sfx="pop"), H("irollo_t", "slide-up", "rollo", dur=0.35),
      H("irollo", "sway", "rollo", origin="bottom", amount=0.16)]

# ---------------------------------------------------------------- 3. compara con la misma regla
s3 = [H("baldaG", "slide-up", delay=0.0, dur=0.45),
      H("pq", "slide-up", delay=0.05, dur=0.5, sfx="whoosh"),
      H("gr", "slide-up", delay=0.2, dur=0.55),
      H("tej", "pop", delay=0.3), H("tregla", "pop", "Imagina", sfx="pop"), H("tregla", "float", "Imagina", amount=0.2),
      H("pq", "sway", origin="bottom", amount=0.08, delay=0.6),
      H("gr", "sway", origin="bottom", amount=0.06, delay=0.9),
      H("pq", "punch", "paquete", amount=0.3),
      H("gr_cinta", "pulse", "grande", amount=0.4),
      H("gr", "punch", "grande", amount=0.2),
      H("tacha", "draw", "cincuenta", dur=0.45, sfx="rotulador"),
      H("copa", "slide-down", "Gana", dur=0.5, sfx="ding"),
      H("copa", "float", "Gana", amount=0.25),
      H("copa_brillo", "pulse", "Gana", amount=0.8),
      H("conf", "pop", "pequeño Gana".split()[0], sfx="none")]
s3 = [a for a in s3 if a["target"] != "conf"] + [H("conf", "pop", "Gana el pequeño", sfx="brillo"),
                                                  H("conf", "drift", "Gana el pequeño", amount=0.5)]
s3 += cuenta("cpq", 4, ["dos", "euros", "el kilo", "kilo"])
s3 += cuenta("cgr", 5, ["El grande", "grande", "dos con", "con", "cincuenta"])
s3 += [H("cpq", "pulse", "Gana", amount=0.5), H("cgr", "shake", "cincuenta", amount=0.3)]

# ---------------------------------------------------------------- 4. la OCU
s4 = [H("eje", "draw", delay=0.0, dur=0.5),
      H("ppq", "slide-up", delay=0.1, dur=0.45, sfx="pop"), H("pgr", "slide-up", delay=0.3, dur=0.5),
      H("doc", "slide-right", delay=0.05, dur=0.5, sfx="papel"), H("doc", "float", amount=0.12, delay=0.6),
      H("lupaO", "pop", "encontró", sfx="pop"), H("lupaO", "sway", "encontró", origin="bottom-right", amount=0.4),
      H("bnor", "grow", "formatos", origin="bottom", dur=0.6, sfx="pop"),
      H("tnor", "pop", "formatos"),
      H("bgra", "grow", "grandes", origin="bottom", dur=0.8, sfx="whoosh"),
      H("pgr", "punch", "grandes", amount=0.3),
      H("pgr", "sway", "grandes", origin="bottom", amount=0.1), H("ppq", "sway", "grandes", origin="bottom", amount=0.12),
      H("bgra", "pulse", "caros", amount=0.25),
      H("tuni", "pop", "unidad", sfx="pop"),
      H("ppq", "punch", "pequeños", amount=0.35),
      H("text", "slide-right", "pequeños", dur=0.4), H("text2", "slide-right", "pequeños", dur=0.5)]
s4 += cuenta("c82", 5, ["hasta", "un", "ochenta", "dos", "por ciento"])
s4 += [H("c82", "punch", "más caros", amount=0.35)]

# ---------------------------------------------------------------- 5. reclama
s5 = [H("mujer", "slide-left", delay=0.0, dur=0.55, sfx="whoosh"),
      H("mujer", "sway", origin="bottom", amount=0.16, delay=0.6),
      H("mujerB", "breathe", origin="bottom", amount=0.6, phase=0.6),
      H("movilG", "slide-left", delay=0.1, dur=0.6),
      H("movilG", "sway", origin="bottom-left", amount=0.18, delay=0.75),
      H("mu_ojos", "blink", delay=0.7), H("mu_cabeza", "sway", origin="bottom", amount=0.3, delay=0.9),
      H("packR", "slide-up", delay=0.05, dur=0.5, sfx="pop"), H("packR", "sway", origin="bottom", amount=0.1, delay=0.6),
      H("packR_cinta", "pulse", amount=0.4, delay=0.6),
      H("cartel", "pop", delay=0.2), H("cartel", "punch", "venden", amount=0.3, sfx="pop"), H("cartel", "pulse", "ahorro", amount=0.6),
      H("packR", "shake", "no", amount=0.5), H("packR", "hide", "pide"),
      H("flash", "fade", "algo", dur=0.1, sfx="chasquido"), H("flash", "hide", "que"),
      H("foto", "pop", "no"),
      H("falso", "pop", "es", sfx="sello"), H("falso", "punch", "es", amount=0.4),
      H("mu_cabeza", "move", "pide", rotate=-7, origin="bottom", dur=0.5),
      H("hoja", "slide-up", "pide", dur=0.5, sfx="papel"),
      H("hoja_c0", "pop", "hoja", sfx="pop"), H("hoja_c1", "pop", "de"),
      H("boli", "slide-down", "hoja", dur=0.45),
      H("hoja_firma", "draw", "reclamaciones", dur=0.7, sfx="rotulador"),
      H("boli", "move", "reclamaciones", to=[95, -10], rotate=-6, dur=0.7),
      H("hoja", "float", "reclamaciones", amount=0.12)]


def full(svg, cap, an):
    return {"svg_file": svg, "layout": "full", "caption": cap, "anims": an}


def free(svg, h, cap, an):
    return {"svg_file": svg, "layout": "free", "height": h, "caption": cap, "anims": an}


guion = {
    "topic": "Pack ahorro que sale más caro: el precio por unidad de medida obligatorio en la etiqueta (kilo, litro, lavado, rollo) y el estudio de la OCU",
    "categoria": "consumo",
    "title": "¿El pack ahorro sale más caro? Mira el precio por kilo",
    "source": "Fuentes: BOE (RD 3423/2000) · OCU · Consumoteca · Deia",
    "chapters": ["?", "1", "2", "3", "+", "TÚ"],
    "outro_cta": "Todo tiene un truco",
    "cover": {"text": "Pack ahorro más caro: mira el *precio por kilo*", "scene": 0},
    "publish": {
        "at": "2026-10-28T14:00:00+01:00",
        "caption": "¿El pack ahorro sale más caro? Mira el número pequeño de la etiqueta: el precio por kilo o por litro, obligatorio en España (Real Decreto 3423/2000). La OCU vio formatos grandes hasta un 82 % más caros por unidad. ¿Qué pack ahorro te ha engañado a ti?",
        "description": "¿El pack ahorro sale más caro? En España la etiqueta debe mostrar dos precios: el del paquete y el precio por unidad de medida, normalmente por kilo o por litro (Real Decreto 3423/2000). Ese número pequeño es el que te dice qué sale más barato de verdad. La OCU encontró formatos grandes que, por unidad, costaban hasta un 82 % más que los pequeños, sobre todo en hipermercados. Si te venden como ahorro algo que no lo es, haz una foto y pide la hoja de reclamaciones. Fuentes: BOE, OCU, Consumoteca, Deia. ¿Qué pack ahorro te ha engañado a ti?",
        "hashtags": ["supermercado", "ahorro", "consumo", "compras", "ocu"],
    },
    "scenes": [
        {"chapter": 0, "headline": "¿Pack *ahorro?*",
         "narration": "¿Coges el pack ahorro porque sale más barato? Quizá pagas más.",
         "illustration": full("gancho_full.svg", "Fig. 1 · El pack ahorro", s0)},
        {"chapter": 1, "number": "1", "headline": "Dos *precios*",
         "narration": "En España la ley obliga a mostrar dos precios: el del paquete y el precio por unidad de medida.",
         "illustration": free("precios_free.svg", 860, "Fig. 2 · RD 3423/2000", s1)},
        {"chapter": 1, "number": "1", "headline": "El número *pequeño*",
         "narration": "Es el número pequeño: lo que cuesta el kilo, el litro, el lavado o el rollo.",
         "illustration": free("pequeno_free.svg", 860, "Fig. 3 · Precio por unidad", s2)},
        {"chapter": 2, "number": "2", "headline": "Compara con la *misma regla*",
         "narration": "Imagina: el paquete pequeño, a dos euros el kilo. El grande, a dos con cincuenta. Gana el pequeño.",
         "illustration": full("compara_full.svg", "Fig. 4 · Ejemplo inventado", s3)},
        {"chapter": 2, "number": "2", "headline": "Hasta un *82 %* más",
         "narration": "La OCU encontró formatos grandes hasta un ochenta y dos por ciento más caros por unidad que los pequeños.",
         "illustration": free("ocu_free.svg", 880, "Fig. 5 · OCU, formatos ahorro", s4)},
        {"chapter": 3, "number": "3", "headline": "Si no hay ahorro, *reclama*",
         "narration": "Si te venden como ahorro algo que no lo es, pide la hoja de reclamaciones.",
         "illustration": free("reclama_free.svg", 880, "Fig. 6 · Foto y reclamación", s5)},
        {"chapter": 4, "number": "+", "headline": "Mira el precio *pequeño*",
         "narration": "No te fíes del precio grande: mira siempre el pequeño.",
         "mascot": {"trigger": "No", "pose": "point", "note": "¡Mira el €/kg!", "side": "right"},
         "elements": [{"type": "tag", "text": "PRECIO POR KILO", "tone": "ink", "trigger": "mira", "sfx": "pop"}]},
        {"chapter": 5, "headline": "Dudas → *truco*",
         "narration": "Tú traes las dudas y nosotros te damos el truco.",
         "elements": [{"type": "trick", "trigger": "Tú", "reveal_trigger": "nosotros"}]},
        {"chapter": 5, "number": "TÚ", "headline": "*Confiesa*",
         "narration": "Síguenos y las resolvemos. ¿Qué pack ahorro te ha engañado a ti?",
         "elements": [{"type": "follow", "trigger": "Síguenos"},
                      {"type": "ask", "text": "¿Qué pack *ahorro* te ha engañado a ti?", "trigger": "¿Qué"}]},
    ],
}
OUT.write_text(json.dumps(guion, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("ok", OUT, sum(len(s["narration"].split()) for s in guion["scenes"]), "palabras")

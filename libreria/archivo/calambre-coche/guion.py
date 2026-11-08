"""Genera content/lote10-06-calambre-coche/guion.json (estilo papel). Uso: python3 libreria/archivo/calambre-coche/guion.py"""
import json
import random
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "content" / "lote10-06-calambre-coche" / "guion.json"


def A(target, effect, **kw):
    d = {"target": target, "effect": effect}
    d.update(kw)
    return d


def viva(p, grupo=None, phase=0.2, d0=0.0, brazo_izq=True, brazo_der=True, cuerpo=True):
    """Receta «persona viva»: respira, se balancea, cabeza con retraso, parpadeo y brazos con su fase."""
    grupo = grupo or p
    o = []
    if cuerpo:
        o += [A(grupo, "breathe", origin="bottom", amount=0.75, phase=phase, delay=round(d0 + 0.6, 2)),
              A(grupo, "sway", origin="bottom", amount=0.13, delay=round(d0 + 0.7, 2))]
    o += [A(f"{p}_cabeza", "sway", origin="bottom", amount=0.32, delay=round(d0 + 0.9, 2)),
          A(f"{p}_ojos", "blink", delay=round(d0 + 0.6, 2))]
    if brazo_izq:
        o.append(A(f"{p}_brazo_izq", "sway", origin="top-right", amount=0.16, delay=round(d0 + 1.0, 2)))
    if brazo_der:
        o.append(A(f"{p}_brazo_der", "sway", origin="top-left", amount=0.22, delay=round(d0 + 0.4, 2)))
    return o


def caras(a, b, trigger, grupo, phase=0.2, d0=0.0, **kw):
    o = [A(b, "hide")]
    o += viva(a, grupo, phase, d0, **kw) + viva(b, grupo, phase, d0, cuerpo=False, **kw)
    o += [A(a, "hide", trigger=trigger), A(b, "fade", trigger=trigger, dur=0.15)]
    return o


def pops(prefijo, n, triggers=None, d0=None, paso=0.18, sfx="pop"):
    o = []
    for i in range(n):
        kw = {"trigger": triggers[i]} if triggers else {"delay": round(d0 + i * paso, 2)}
        o.append(A(f"{prefijo}{i}", "pop", sfx=sfx if i == 0 or triggers else "none", **kw))
    return o


S = []
# ---------------------------------------------------------------- 0 gancho
a0 = [A("camera", "zoom", delay=0, to=[520, 860], amount=1.06, dur=1.6),
      A("lejos", "pan", delay=0, to=[-14, 0], dur=5), A("medio", "pan", delay=0, to=[-40, 0], dur=5),
      A("cerca", "pan", delay=0, to=[-110, 0], dur=5), A("astro", "hide"),
      A("hombre", "squash", delay=0, dur=0.6, sfx="boing")]
a0 += caras("hn", "hs", "calambre", "hombre", 0.2, 0.1)
a0 += [A("coche_rueda_del", "spin", amount=0.02),
       A("hn_brazo_der", "move", trigger="Por", rotate=6, origin="top-left", dur=0.5),
       A("hs_brazo_der", "move", trigger="Por", rotate=6, origin="top-left", dur=0.5),
       A("coche", "punch", trigger="da", amount=0.06),
       A("chis", "pop", trigger="calambre", sfx="chasquido"), A("chis", "pulse", trigger="calambre", amount=0.5),
       A("rays", "pop", trigger="calambre"), A("rays", "spin", trigger="calambre", amount=0.08),
       A("zas", "pop", trigger="al cerrar", sfx="sorpresa"), A("zas", "wiggle", trigger="al cerrar", amount=0.4),
       A("temb", "pop", trigger="calambre"),
       A("hn_brazo_der", "move", trigger="calambre", rotate=-26, origin="top-left", dur=0.25),
       A("hs_brazo_der", "move", trigger="calambre", rotate=-26, origin="top-left", dur=0.25),
       A("hombre", "move", trigger="calambre", to=[-26, -18], dur=0.25),
       A("hs_cabeza", "move", trigger="al cerrar", rotate=-6, origin="bottom", dur=0.5),
       A("hombre", "shake", trigger="cerrar", amount=0.3),
       A("camera", "zoom", trigger="calambre", to=[560, 860], amount=1.14, dur=0.9),
       A("coche_maneta", "punch", trigger="puerta", amount=0.4),
       A("coche", "punch", trigger="coche", amount=0.05)]
S.append({"chapter": 0, "headline": "¡*Calambre*!", "narration": "¿Por qué te da calambre al cerrar la puerta del coche?",
          "illustration": {"svg_file": "gancho_full.svg", "layout": "full", "caption": "Fig. 1 · ¡Zas!", "anims": a0}})

# ---------------------------------------------------------------- 1 asiento
a1 = [A("asi", "slide-up", delay=0, dur=0.5, sfx="whoosh"), A("conductor", "squash", delay=0.1, dur=0.6, sfx="boing")]
a1 += caras("cn", "cs", "cargas", "conductor", 0.65, 0.2)
a1 += [A(f"m1_{i}", "hide") for i in range(5)]
a1 += [A("coch", "pop", trigger="No", sfx="pop"), A("asp1", "draw", trigger="coche", dur=0.35, sfx="rotulador"),
       A("et_tu", "pop", trigger="eres", sfx="pop"), A("et_tu", "punch", trigger="tú", amount=0.3),
       A("cn_brazo_der", "move", trigger="eres", rotate=-12, origin="top-left", dur=0.6),
       A("cs_brazo_der", "move", trigger="eres", rotate=-12, origin="top-left", dur=0.6),
       A("coch", "hide", trigger="Al"), A("asp1", "hide", trigger="Al"),
       A("fl1", "draw", trigger="deslizarte", dur=0.45, sfx="rotulador"),
       A("conductor", "move", trigger="deslizarte", to=[140, 0], dur=1.4, sfx="whoosh"),
       A("asi_cojin", "punch", trigger="asiento", amount=0.15),
       A("roce", "pop", trigger="ropa", sfx="pop"), A("roce", "wiggle", trigger="roza", amount=0.5),
       A("asi_respaldo", "punch", trigger="tapicería", amount=0.12),
       A("m1_0", "pop", trigger="te cargas", sfx="pop"), A("m1_1", "pop", trigger="cargas"),
       A("m1_2", "pop", trigger="de electricidad"), A("m1_3", "pop", trigger="electricidad", sfx="pop"),
       A("m1_4", "pop", trigger="estática"),
       A("et_est", "pop", trigger="electricidad", sfx="pop"), A("et_est", "punch", trigger="estática", amount=0.3),
       A("camera", "zoom", trigger="cargas", to=[520, 500], amount=1.06, dur=1.2)]
a1 += [A(f"m1_{i}", "pulse", trigger="estática", amount=0.4) for i in range(5)]
S.append({"chapter": 1, "number": "1", "headline": "No es el coche: *eres tú*",
          "narration": "No es el coche: eres tú. Al deslizarte por el asiento, la ropa roza la tapicería y te cargas de electricidad estática.",
          "illustration": {"svg_file": "asiento_free.svg", "layout": "free", "height": 900, "caption": "Fig. 2 · El roce", "anims": a1}})

# ---------------------------------------------------------------- 2 goma
a2 = [A("zap", "slide-up", delay=0, dur=0.5, sfx="whoosh"), A("chico", "squash", delay=0.1, dur=0.6, sfx="boing"),
      A("globo", "hide"), A("pelos", "hide"), A("asp2", "hide"), A("fl2", "hide")]
a2 += viva("chi", "chico", 0.4, 0.2, brazo_izq=False)
a2 += pops("m2z", 3, d0=0.3) + pops("m2p", 3, d0=0.5)
a2 += [A("zap_suela", "punch", trigger="suelas", amount=0.3), A("et_goma", "pop", trigger="goma", sfx="pop"),
       A("fl2", "draw", trigger="dejan", dur=0.4, sfx="rotulador"), A("asp2", "pop", trigger="escapar", sfx="sorpresa"),
       A("asp2", "wiggle", trigger="esa", amount=0.4)]
a2 += [A(f"m2z{i}", "move", trigger="escapar", to=[0, 26], dur=0.3) for i in range(3)]
a2 += [A(f"m2z{i}", "move", trigger="carga", to=[0, -26], dur=0.45) for i in range(3)]
a2 += [A(f"m2p{i}", "punch", trigger="cargado", amount=0.4) for i in range(3)]
a2 += [A("chico", "punch", trigger="vas", amount=0.08),
       A("globo", "pop", trigger="globo", sfx="pop"), A("globo", "wiggle", trigger="globo", amount=0.45),
       A("globo_roce", "wiggle", trigger="frotado", amount=0.6),
       A("chi_brazo_izq", "wiggle", trigger="globo", amount=0.3, origin="top-right"),
       A("pelos", "grow", trigger="frotado", origin="bottom", dur=0.5, sfx="chasquido"),
       A("pelos", "wiggle", trigger="frotado", amount=0.2),
       A("camera", "zoom", trigger="como", to=[560, 450], amount=1.05, dur=1.0)]
S.append({"chapter": 1, "number": "1", "headline": "Suelas *de goma*",
          "narration": "Las suelas de goma no dejan escapar esa carga: vas cargado como un globo frotado.",
          "illustration": {"svg_file": "goma_free.svg", "layout": "free", "height": 860, "caption": "Fig. 3 · Aislado", "anims": a2}})

# ---------------------------------------------------------------- 3 chispa
a3 = [A("dedo", "slide-right", delay=0, dur=0.5, sfx="whoosh"), A("dedo", "float", amount=0.15, delay=0.5),
      A("cargas3", "slide-right", delay=0, dur=0.5), A("rayo3", "hide"), A("dest3", "hide"),
      A("camera", "zoom", delay=0, to=[540, 880], amount=1.05, dur=2.0)]
a3 += [A(f"m3_{i}", "pulse", amount=0.3, delay=0.5 + i * 0.2) for i in range(4)]
a3 += [A("et_metal", "pop", trigger="metal", sfx="pop"), A("puerta", "punch", trigger="metal", amount=0.05),
       A("dedo", "move", trigger="tocar", to=[60, 0], dur=1.2), A("cargas3", "move", trigger="tocar", to=[60, 0], dur=1.2),
       A("cargas3", "jitter", trigger="carga", amount=0.4),
       A("rayo3", "draw", trigger="salta", dur=0.2, sfx="chasquido"),
       A("dest3", "pop", trigger="golpe", sfx="brillo"), A("dest3", "spin", trigger="golpe", amount=0.1),
       A("ondas", "hide"), A("ondas", "pop", trigger="golpe"), A("on1", "ripple", trigger="golpe", phase=0), A("on2", "ripple", trigger="golpe", phase=0.5),
       A("cargas3", "hide", trigger="golpe"),
       A("et_chispa", "pop", trigger="chispa", sfx="pop"),
       A("camera", "zoom", trigger="chispa", to=[520, 880], amount=1.18, dur=0.9),
       A("zas3", "pop", trigger="calambre", sfx="sorpresa"), A("zas3", "wiggle", trigger="calambre", amount=0.4),
       A("dedo", "move", trigger="calambre", to=[-90, 10], dur=0.3), A("rayo3", "hide", trigger="calambre")]
S.append({"chapter": 2, "number": "2", "headline": "La *chispa*",
          "narration": "Al tocar el metal, la carga salta de golpe en una chispa: el calambre.",
          "illustration": {"svg_file": "chispa_full.svg", "layout": "full", "caption": "Fig. 4 · Descarga", "anims": a3}})

# ---------------------------------------------------------------- 4 aire
rnd = random.Random(4)
a4 = [A("bh", "slide-up", delay=0, dur=0.5, sfx="whoosh"), A("bs", "slide-up", delay=0.15, dur=0.5)]
a4 += viva("ph", "bh", 0.2, 0.2, brazo_izq=False, brazo_der=False) + viva("ps", "bs", 0.65, 0.5, brazo_izq=False, brazo_der=False)
a4 += pops("mh", 3, d0=0.4) + pops("ms", 4, d0=0.6)
a4 += [A(f"gt{i}", "hide") for i in range(6)] + [A("pelicula", "hide"), A("et_seco", "hide")]
a4 += [A("copo4", "pop", trigger="invierno", sfx="pop"), A("copo4", "spin", trigger="invierno", amount=0.1),
       A("termo4", "squash", trigger="pasa", to=[0, -160], dur=0.5, sfx="pop"),
       A("termo4", "shake", trigger="más", amount=0.3),
       A("et_hum", "pop", trigger="húmedo", sfx="pop")]
a4 += [A(f"gt{i}", "pop", trigger="húmedo" if i < 3 else "capa") for i in range(6)]
a4 += [A(f"gt{i}", "float", amount=round(rnd.uniform(0.2, 0.4), 2), trigger="invisible") for i in range(6)]
a4 += [A("pelicula", "fade", trigger="invisible", dur=0.5, sfx="brillo"), A("pelicula", "pulse", trigger="agua", amount=0.3)]
a4 += [A(f"mh{i}", "move", trigger="lleva", to=[(-1) ** i * 90, -240], dur=0.9) for i in range(3)]
a4 += [A(f"mh{i}", "hide", trigger="con aire seco") for i in range(3)]
a4 += [A("et_seco", "pop", trigger="seco", sfx="pop"), A("et_hum", "punch", trigger="carga", amount=0.25),
       A("bs", "shake", trigger="no", amount=0.3)]
a4 += [A(f"ms{i}", "pulse", trigger="no", amount=0.5) for i in range(4)]
a4 += [A(f"ms{i}", "punch", trigger="seco", amount=0.4) for i in range(4)]
S.append({"chapter": 2, "number": "2", "headline": "Aire *seco*",
          "narration": "En invierno pasa más: con aire húmedo, una capa invisible de agua se lleva la carga; con aire seco, no.",
          "illustration": {"svg_file": "aire_panel.svg", "layout": "panel", "caption": "Fig. 5 · Humedad", "anims": a4}})

# ---------------------------------------------------------------- 5 ropa
a5 = [A("jalg", "slide-down", delay=0, dur=0.5, sfx="whoosh"), A("jpol", "slide-down", delay=0.15, dur=0.5),
      A("jalg_jersey", "sway", origin="top", amount=0.1, delay=0.6), A("jpol_jersey", "sway", origin="top", amount=0.12, delay=0.9),
      A("et_pol", "hide")]
a5 += pops("ma", 2, d0=0.5)
a5 += [A(f"mp{i}", "hide") for i in range(7)]
a5 += [A("jalg_etiqueta", "punch", trigger="ropa", amount=0.3), A("jpol", "punch", trigger="sintética", amount=0.12),
       A("jpol_etiqueta", "punch", trigger="poliéster", amount=0.35)]
a5 += [A(f"mp{i}", "pop", trigger=["como", "como", "el", "poliéster", "poliéster", "acumula", "acumula"][i], sfx="pop" if i % 2 == 0 else "none") for i in range(7)]
a5 += [A(f"mp{i}", "shake", trigger="todavía", amount=0.5) for i in range(7)]
a5 += [A("et_pol", "pop", trigger="todavía", sfx="pop"), A("et_pol", "punch", trigger="más", amount=0.3),
       A("camera", "zoom", trigger="acumula", to=[640, 370], amount=1.12, dur=1.0)]
S.append({"chapter": 3, "number": "3", "headline": "Ropa *sintética*",
          "narration": "La ropa sintética, como el poliéster, acumula todavía más.",
          "illustration": {"svg_file": "ropa_panel.svg", "layout": "panel", "caption": "Fig. 6 · Tejidos", "anims": a5}})

# ---------------------------------------------------------------- 6 +, 7-8 cierre
S.append({"chapter": 4, "number": "+", "headline": "Agarra el *marco*",
          "narration": "Para evitarlo, agarra el marco metálico de la puerta antes de pisar el suelo.",
          "mascot": {"trigger": "evitarlo", "pose": "point", "note": "¡Primero la mano, luego el pie!", "side": "right"},
          "elements": [{"type": "tag", "text": "AGARRA EL MARCO", "tone": "ink", "trigger": "agarra", "sfx": "pop"},
                       {"type": "tag", "text": "ANTES DE PISAR", "tone": "hot", "trigger": "puerta", "sfx": "pop"},
                       {"type": "stamp", "text": "SIN CALAMBRE", "tone": "accent", "trigger": "suelo", "sfx": "sello"}]})
S.append({"chapter": 5, "headline": "Dudas → *truco*", "narration": "Tú traes las dudas y nosotros te damos el truco.",
          "elements": [{"type": "trick", "trigger": "Tú", "reveal_trigger": "nosotros"}]})
S.append({"chapter": 5, "number": "TÚ", "headline": "*Confiesa*", "narration": "Síguenos y las resolvemos. ¿A ti te da calambre el coche?",
          "elements": [{"type": "follow", "trigger": "Síguenos"}, {"type": "ask", "text": "¿A ti te da *calambre* el coche?", "trigger": "¿A"}]})

G = {
    "topic": "¿Por qué te da calambre al tocar el coche? Al deslizarte por el asiento la ropa roza la tapicería y te cargas de electricidad estática; las suelas de goma no dejan escapar la carga y al tocar el metal salta en una chispa. Con aire seco (invierno) pasa más y la ropa sintética acumula más. Truco: agarra el marco metálico antes de pisar el suelo (RACE, Mapfre, Universidad de Kentucky, The Naked Scientists, Motorpasión)",
    "categoria": "fisica",
    "estilo": "papel",
    "title": "¿Por qué te da calambre al tocar el coche?",
    "source": "Fuentes: RACE · Mapfre · Univ. de Kentucky · The Naked Scientists",
    "chapters": ["?", "1", "2", "3", "+", "TÚ"],
    "outro_cta": "Todo tiene un truco",
    "cover": {"text": "Por qué da *calambre* el coche", "scene": 0},
    "publish": {
        "at": "2026-11-09T14:00:00+01:00",
        "caption": "¿Por qué te da calambre el coche? No es el coche, eres tú: te cargas al rozar el asiento y las suelas de goma no dejan escapar la carga. Al tocar el metal, chispa. Con aire seco, peor. Agarra el marco de la puerta antes de pisar el suelo (RACE, Mapfre). ¿A ti te da calambre el coche?",
        "description": "¿Por qué te da calambre al tocar el coche? Al deslizarte por el asiento, la ropa y la tapicería se frotan y te cargas de electricidad estática; las suelas de goma no dejan que esa carga se vaya al suelo. Al tocar el metal, salta de golpe en una chispa diminuta. Pasa más en otoño e invierno porque el aire seco no se lleva la carga, y la ropa sintética acumula más. Truco práctico: agarra el marco metálico de la puerta antes de poner el pie en el suelo. Fuentes: RACE, Mapfre, Universidad de Kentucky, The Naked Scientists. ¿A ti te da calambre el coche?",
        "hashtags": ["coche", "electricidad", "fisica", "invierno", "curiosidades"]},
    "scenes": S,
}
OUT.write_text(json.dumps(G, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("ok", OUT, sum(len(s["narration"].split()) for s in S), "palabras")

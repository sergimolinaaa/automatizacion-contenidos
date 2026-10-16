import json, math, sys
sys.path.insert(0, ".")
from rot import polar, R_IN_L, R_OUT_L, CY, LANE

P = json.load(open("poses.json"))


def pose(th, r):
    x, y = polar(th, r)
    return (x, y, -th)


def moves(target, start, pts, triggers, dur=0.6):
    out, cur = [], start
    for p, trg in zip(pts, triggers):
        dr = p[2] - cur[2]
        while dr > 180: dr -= 360
        while dr < -180: dr += 360
        a = {"target": target, "effect": "move", "to": [round(p[0] - cur[0], 1), round(p[1] - cur[1], 1)], "rotate": round(dr, 1), "dur": dur}
        if isinstance(trg, str):
            a["trigger"] = trg
        else:
            a["delay"] = trg
        out.append(a)
        cur = p
    return out


def A(target, effect, trigger=None, **kw):
    a = {"target": target, "effect": effect}
    if trigger: a["trigger"] = trigger
    a.update(kw)
    return a


def hides(*ids):
    return [A(i, "hide") for i in ids]


S = []
# 0 · GANCHO
S.append({"chapter": 0, "headline": "¿Quién tiene *razón*?",
          "narration": "En la rotonda: ¿el que corta o el que no lo deja?",
          "illustration": {"svg_file": "rotonda_full.svg", "layout": "full", "caption": "Fig. 1 · Rotonda de dos carriles",
                           "anims": hides("espera", "dentro", "ceda", "blanco5", "rojo5", "tpref", "tdentro", "tcedes", "mal", "bien", "recalc") + [
                               A("ruta_mal", "draw", "rotonda", dur=0.9, sfx="whoosh"),
                               {"target": "camera", "effect": "zoom", "to": [400, 800], "amount": 1.45, "dur": 0.3},
                               A("duda", "pop", "rotonda", sfx="ding"), A("duda", "pulse", amount=0.6),
                               A("rojo", "punch", "corta", amount=0.3), A("tcorta", "pop", "corta", sfx="pop"),
                               A("rojo", "shake", amount=0.4),
                               A("blanco", "punch", "deja", amount=0.3), A("tnodeja", "pop", "deja", sfx="pop"),
                               A("piii", "pop", "deja", sfx="sorpresa"), A("piii", "wiggle", amount=0.8)]}})

# 1 · EL TRUCO ES… dentro manda
d0 = tuple(P["dentro"])
S.append({"chapter": 1, "number": "1", "headline": "Dentro *manda*",
          "narration": "El truco es… quien ya está dentro manda. Si vas a entrar, cedes el paso.",
          "elements": [{"type": "tag", "text": "EL TRUCO ES…", "trigger": "truco"}],
          "illustration": {"svg_file": "rotonda_full.svg", "layout": "full", "caption": "Fig. 2 · Quien circula dentro, primero",
                           "anims": hides("blanco", "rojo", "blanco5", "rojo5", "ruta_mal", "tcorta", "tnodeja", "piii", "mal", "bien", "recalc", "duda") + [
                               A("tdentro", "pop", "dentro", sfx="pop"),
                               {"target": "camera", "effect": "zoom", "to": [700, 880], "amount": 1.3, "dur": 0.5}]
                           + moves("dentro", d0, [pose(-25, R_OUT_L), pose(20, R_OUT_L), pose(70, R_OUT_L)], ["dentro", "manda", "vas"], dur=0.7) + [
                               A("tpref", "pop", "manda", sfx="ding"), A("tpref", "pulse", amount=0.5),
                               A("espera", "punch", "entrar", amount=0.25),
                               A("ceda", "pop", "cedes", sfx="sello"), A("tcedes", "pop", "cedes"),
                               A("ceda", "punch", "paso", amount=0.25)]}})

# 2 · la norma
S.append({"chapter": 1, "number": "1", "headline": "Lo dice la *norma*",
          "narration": "Lo dice el Reglamento de Circulación, el libro de normas del tráfico: artículo 57.",
          "illustration": {"svg_file": "norma.svg", "caption": "Fig. 3 · RGC, art. 57.1.c",
                           "anims": [A("ficha", "slide-left", "dice", dur=0.5, sfx="whoosh"),
                                     A("libro", "punch", "Reglamento", amount=0.25),
                                     A("libro", "float", amount=0.4),
                                     A("tlibro", "pop", "libro", sfx="pop"),
                                     A("hl_dentro", "draw", "normas", dur=0.4, sfx="rotulador"),
                                     A("hl_preferencia", "draw", "tráfico", dur=0.5, sfx="rotulador"),
                                     A("sello", "pop", "artículo", sfx="sello"),
                                     A("sello", "punch", "57", amount=0.3),
                                     A("camera", "zoom", "normas", to=[690, 300], amount=1.25),
                                     A("camera", "zoom", "artículo", to=[500, 350], amount=1)]}})

# 3 · carril de dentro
t3 = tuple(P["tu3"])
S.append({"chapter": 2, "number": "2", "headline": "Carril de *dentro*",
          "narration": "¿Vas a la tercera salida? Puedes ir por el carril de dentro.",
          "illustration": {"svg_file": "ruta_full.svg", "layout": "full", "caption": "Fig. 4 · Salidas 1, 2 y 3",
                           "anims": hides("tu4", "tu6", "ruta_out", "ruta_vuelta", "lint", "lgratis", "gpsv", "sinpiii") + [
                               A("gps3", "slide-down", "Vas", dur=0.5, sfx="ding"),
                               A("b1", "pop", delay=0.5, sfx="pop"), A("b2", "pop", delay=0.8, sfx="pop"),
                               A("b3", "pop", "tercera", sfx="ding"), A("b3", "pulse", amount=0.6),
                               A("ruta_in", "draw", "Puedes", dur=1.4, sfx="whoosh"),
                               A("lfuera", "pop", "carril", sfx="pop"), A("ldentro", "pop", "dentro", sfx="pop")]
                           + moves("tu3", t3, [pose(-45, 228), pose(5, R_IN_L), pose(55, R_IN_L), pose(105, R_IN_L)], ["Puedes", "ir", "carril", "dentro"], dur=0.7)}})

# 4 · sal por fuera
t4 = tuple(P["tu4"])
EXIT = (120, CY - LANE, 90 * -1)
S.append({"chapter": 2, "number": "2", "headline": "Sal por *fuera*",
          "narration": "Pero antes de salir, pon el intermitente y pásate con tiempo al carril de fuera.",
          "illustration": {"svg_file": "ruta_full.svg", "layout": "full", "caption": "Fig. 5 · Primero al carril exterior",
                           "anims": hides("tu3", "tu6", "ruta_in", "ruta_vuelta", "lgratis", "gpsv", "sinpiii", "b1", "b2", "lint") + [
                               A("b3", "punch", "salir", amount=0.3), A("gps3", "punch", "salir", amount=0.12),
                               A("tu4b", "pop", "intermitente", sfx="ding"), A("tu4b", "pulse", amount=1.6),
                               A("lint", "pop", "intermitente"), A("lint", "hide", "pásate"),
                               A("ruta_out", "draw", "pásate", dur=1.3, sfx="whoosh"),
                               A("lfuera", "punch", "fuera", amount=0.3)]
                           + moves("tu4", t4, [pose(140, 262), pose(158, 295), (200, CY - LANE - 2, -95), EXIT], ["pásate", "tiempo", "carril", "fuera"], dur=0.7)}})

# 5 · el error clásico
r5, b5 = tuple(P["rojo5"]), tuple(P["blanco5"])
S.append({"chapter": 3, "number": "3", "headline": "El error *clásico*",
          "narration": "Cortar desde dentro es el error clásico. El de fuera sigue su carril: tiene preferencia.",
          "illustration": {"svg_file": "rotonda_full.svg", "layout": "full", "caption": "Fig. 6 · El que corta y el que no lo deja",
                           "anims": hides("espera", "dentro", "ceda", "blanco", "rojo", "tpref", "tdentro", "tcedes", "duda") + [
                               A("ruta_mal", "draw", "Cortar", dur=1.0, sfx="whoosh"),
                               {"target": "camera", "effect": "zoom", "to": [400, 800], "amount": 1.45, "dur": 0.3},
                               A("tcorta", "pop", "dentro", sfx="pop"),
                               A("recalc", "slide-down", "error", dur=0.5, sfx="sorpresa"),
                               A("piii", "pop", "error"), A("piii", "wiggle", amount=0.8),
                               A("mal", "pop", "clásico", sfx="sello"),
                               A("tnodeja", "pop", "fuera", sfx="pop"), A("recalc", "hide", "fuera"),
                               A("blanco5", "punch", "carril", amount=0.25),
                               A("bien", "pop", "preferencia", sfx="ding")]
                           + moves("rojo5", r5, [pose(130, R_IN_L), (322, 806, -100)], ["Cortar", "dentro"], dur=0.7)
                           + moves("blanco5", b5, [(330, 691, -138)], ["Cortar"], dur=1.0)}})

# 6 · otra vuelta
t6 = tuple(P["tu6"])
loop = [pose(195 + 62 * k, R_OUT_L) for k in range(1, 6)] + [(200, CY - LANE - 2, -95)]
S.append({"chapter": 4, "number": "+", "headline": "Otra *vuelta*",
          "narration": "¿Se te pasó? Da otra vuelta. Gratis y sin bocinazos.",
          "illustration": {"svg_file": "ruta_full.svg", "layout": "full", "caption": "Fig. 7 · Vuelta extra",
                           "anims": hides("tu3", "tu4", "ruta_in", "ruta_out", "gps3", "lint", "ldentro", "lfuera", "b1", "b2") + [
                               A("gpsv", "slide-down", "pasó", dur=0.5, sfx="sorpresa"),
                               A("b3", "shake", amount=0.6),
                               A("tu6", "punch", "pasó", amount=0.25),
                               A("ruta_vuelta", "draw", "Da", dur=2.2, sfx="whoosh"),
                               A("lgratis", "pop", "Gratis", sfx="ding"),
                               A("sinpiii", "pop", "bocinazos", sfx="pop")]
                           + moves("tu6", t6, loop, ["Da", "otra", "vuelta", "Gratis", "sin", "bocinazos"], dur=0.6)},
          "mascot": {"trigger": "vuelta", "pose": "cheer", "note": "¡Vuelta de honor!", "side": "left"}})

S.append({"chapter": 5, "headline": "Dudas → *truco*", "narration": "Tú traes las dudas y nosotros te damos el truco.",
          "elements": [{"type": "trick", "trigger": "Tú", "reveal_trigger": "nosotros"}]})
S.append({"chapter": 5, "number": "TÚ", "headline": "*Confiesa*",
          "narration": "Síguenos y las resolvemos. ¿Tú eres de los que dan tres vueltas?",
          "elements": [{"type": "follow", "trigger": "Síguenos"},
                       {"type": "ask", "text": "¿Tú eres de los que dan *tres vueltas*?", "trigger": "Tú"}]})

G = {
    "topic": "Cómo se circula bien por una rotonda en España: prioridad, carriles y salida",
    "categoria": "objetos",
    "title": "Rotondas: ¿el que corta o el que no lo deja? 🚗",
    "source": "Fuentes: Reglamento General de Circulación (Real Decreto 1428/2003), art. 57.1.c (preferencia en las glorietas) · DGT, recomendaciones para circular por glorietas (salir siempre desde el carril exterior, intermitente al salir)",
    "chapters": ["?", "1", "2", "3", "+", "TÚ"],
    "outro_cta": "Todo tiene un truco",
    "cover": {"text": "Rotondas: *¿quién manda?*", "scene": 0},
    "publish": {
        "caption": "¿En la rotonda tiene razón el que corta o el que no lo deja? 🚗 Quien ya circula dentro tiene preferencia (Reglamento General de Circulación, art. 57.1.c). Puedes ir por el carril interior, pero antes de salir pon el intermitente y pásate con tiempo al exterior. ¿Se te pasó? Otra vuelta. ¿Tú cuántas das?",
        "description": "Cómo se circula bien por una rotonda (glorieta) en España. 1) Quien ya circula dentro de la rotonda tiene preferencia sobre quien quiere entrar: el que entra cede el paso (Reglamento General de Circulación, art. 57.1.c: «En las glorietas, los que se hallen dentro de la vía circular tendrán preferencia de paso sobre los que pretendan acceder a aquéllas»). 2) Si vas a una salida lejana puedes circular por el carril interior. 3) Antes de salir, pon el intermitente derecho y pásate con antelación al carril exterior: la DGT recuerda que se sale siempre desde el carril exterior. 4) Salir cortando desde el carril interior es el error clásico: el coche que va por el carril exterior sigue su carril y tiene preferencia. 5) Si no llegas a tiempo al carril exterior, da otra vuelta. Fuentes: Real Decreto 1428/2003 (Reglamento General de Circulación), art. 57.1.c; DGT.",
        "hashtags": ["eltrucoes"],
    },
    "scenes": S,
}
json.dump(G, open("/home/user/automatizacion-contenidos/content/lote6-04-rotondas/guion.json", "w"), ensure_ascii=False, indent=2)
words = sum(len(s["narration"].replace("…", " ").split()) for s in S)
print("palabras", words)

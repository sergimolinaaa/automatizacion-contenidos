# Montaje rápido de un vídeo «El truco es…»

Esta guía sustituye a la skill rossark, a los vídeos de referencia y a `Illustration.tsx` para montar. Nivel aprobado:
`content/lote8-09-gasto-campana`, `content/lote9-01-sacudida-dormir`, `content/lote10-01-frio-bateria`
(sus dibujos en `libreria/archivo/{gasto-campana,sacudida-dormir,frio-bateria}/dib.py`). Ábrelos solo si algo de aquí no basta.
Desde el 2-nov TODO va en **papel recortado** (§0): la referencia de estilo es `muestras/estilos/C` (`muestras/estilos/dib.py`, `estilo_c`).

## 0. Estilo papel (obligatorio desde el 2-nov)
Todo sale de `libreria/svg/papel.py` (catálogo: `entregas/estilos/catalogo_papel.png`, se regenera con
`python3 libreria/catalogo_papel.py`). No hay que dibujar nada nuevo: las piezas de siempre se convierten.
```python
from libreria.svg.base import *
from libreria.svg.personajes import persona
from libreria.svg.papel import a_papel, recorte, fondo_calle, fondo_casa, fondo_cielo, fondo_neutro, grano, hoja_transicion, fx, PAPEL as PP
from libreria.svg.objetos import tecnologia as TE, politica as P

body = fondo_calle("dia")                                    # capas lejos / medio / cerca ya agrupadas para el parallax
body += persona("ana", 400, 1290, 1.2, estilo="papel", expresion="duda", brazos=("relajado", "explica"))
body += a_papel(TE.bateria("bat", 760, 900, 150, 280, nivel=0.3), semilla=3)
body += a_papel(P.urna("urna", 300, 1240, 280, 300, texto="CONGRESO"), semilla=4)
body += recorte("M 700 600 L 860 600 L 780 480 Z", PP["mostaza"], semilla=5, id_="aviso")   # forma suelta de papel
body += hoja_transicion("salida", PP["mostaza"], "?")       # salida de escena (ver anims abajo)
body += grano()                                               # SIEMPRE lo último: grano de papel encima de todo
guardar(f"{OUT}/gancho_full.svg", svg(body, "full"))
```
- **`persona(..., estilo="papel")`**: mismos parámetros, ids (`_cabeza`, `_ojos`, `_brazo_izq/der`…) y `.puntos` que siempre;
  sin contorno, mejillas marcadas, cada parte recortada con su sombra y un giro leve. Las recetas de §3 valen tal cual.
- **`a_papel(pieza, semilla)`** sirve para CUALQUIER pieza (`objetos/*.py`, `persona()`, iconos y etiquetas de `base`): quita los
  contornos negros (deja un filo fino tono sobre tono), pasa degradados y colores a la paleta, quita brillos, añade borde roto,
  sombra y giro (±0,6-2° según `semilla`; `giro=0` lo quita). El id exterior se conserva: se anima igual. Usa una `semilla`
  distinta por pieza. Con texto dentro elige solo `filtro="papelFino"` (no rompe letras); úsalo también en piezas pequeñas.
  Convierten bien: personas, cerebro, termómetro, móvil, batería, chip, urna, dni, sobre, hemiciclo, taza, bombilla, reloj,
  saco de dinero, sofá, ventana. Regular (se entienden, pero mejor redibujar si son protagonistas): `cuerpo.mano` (dedos
  pegados), `animales.perro` (patas en líneas), `animales.gato` (conserva contorno oscuro propio).
- **Fondos** (1080×1920, suelo en y 1290, capas con 200 px de sobra a cada lado): `fondo_calle(hora)` (dia, tarde, noche),
  `fondo_casa(noche=False)`, `fondo_cielo(hora)` (sol o luna en `astro`, nubes `nube0..2`), `fondo_neutro(w, h, col)` (cartulina con
  fibras; vale para `panel` 1000×700). Pásalos como primer trozo de `body` (o en `fondo=`). En `free` no hay fondo: piezas sueltas.
- **Paleta** `PAPEL` (alias `PP`): crema `#FBF6EC`, hueso `#F3E6CF`, tinta `#3A2E2A` (en vez de negro), coral `#E86A4A`, mostaza
  `#F2C14E`, azul `#6FA8C8`, azul_osc `#4B5A7A`, cielo `#BFD9E2`, verde `#7FBF7A`, terracota `#D98E6A`, arena `#E9B872`,
  lavanda `#8FA7C4`, piel `#F1C7A1`, mejilla `#E99486`… `EQUIV` da la equivalencia de cada color de `base.py` y
  `color_papel(hex)` convierte cualquiera. Textos y cifras: `T(..., fill=PP["tinta"], font=DISP)`; nada de LIMA chillón ni negro.
- **Filtros** (atributo con `fx(nombre)`: `f'<g{fx("papelCapa")}>…</g>'`): `papelBorde` (pieza suelta), `papelCapa` (capa dentro de
  una pieza), `papelFino` (pequeñas o con texto), `papelPlano` (borde roto sin sombra: suelos, cosas pegadas al fondo).
  Nunca pongas el `filter` en el mismo `<g id>` que animas si además lleva `transform`: `a_papel`/`capa()` ya lo anidan bien.
- **Transiciones de papel**: la salida de escena es una hoja rasgada que sube (`hoja_transicion`); entradas con `squash` (cae
  aplastándose como un recorte) o `slide-up` + giro; los relevos de cifras con `fade` 0,1 y `jitter`. Anims:
```json
{"target": "salida", "effect": "pan", "delay": 5.15, "to": [0, -2020], "rotate": -3, "dur": 0.75, "sfx": "papel"},
{"target": "chico", "effect": "squash", "delay": 0, "dur": 0.6, "sfx": "boing"},
{"target": "aviso", "effect": "squash", "trigger": "batería", "dur": 0.5, "to": [0, -160], "sfx": "sorpresa"}
```
  `delay` de la hoja = duración de la escena − 0,8 s. `sfx` de papel: `papel` en entradas y salidas de hojas.

## 1. guion.json mínimo completo
Los SVG se generan con un `dib.py` (ver §6) en la misma carpeta y se citan con `svg_file`. Tiempos: `trigger` (palabra de la voz)
o `delay` (segundos desde que empieza la escena). Capítulos: índice en `chapters` (0 «?», 1-3, 4 «+», 5 «TÚ»).
```json
{
  "topic": "Resumen del tema con el dato clave", "categoria": "moviles",
  "title": "¿Por qué el frío se come la batería del móvil?",
  "source": "Fuentes: Battery University · Apple Soporte",
  "chapters": ["?", "1", "2", "3", "+", "TÚ"], "outro_cta": "Todo tiene un truco",
  "cover": {"text": "Por qué el frío gasta la *batería* del móvil", "scene": 0},
  "publish": {"at": "2026-11-02T14:00:00+01:00", "caption": "¿Pregunta? Resumen con datos y fuentes. ¿Pregunta final?",
              "description": "¿Pregunta? 3-4 frases con datos. Fuentes: … ¿Pregunta final?", "hashtags": ["movil", "bateria", "frio"]},
  "scenes": [
    {"chapter": 0, "headline": "¿Se *congela* la batería?",
     "narration": "¿Sales a la calle con frío y tu móvil se apaga con batería?",
     "illustration": {"svg_file": "gancho_full.svg", "layout": "full", "caption": "Fig. 1 · ¡Se apagó!", "anims": [
       {"target": "tel", "effect": "slide-up", "delay": 0, "dur": 0.5, "sfx": "whoosh"},
       {"target": "chico", "effect": "breathe", "origin": "bottom", "amount": 0.6, "phase": 0.2},
       {"target": "chico", "effect": "sway", "origin": "bottom", "amount": 0.12, "delay": 0.1},
       {"target": "chf_ojos", "effect": "blink", "delay": 0.6},
       {"target": "camera", "effect": "zoom", "trigger": "calle", "to": [470, 860], "amount": 1.08, "dur": 1.2},
       {"target": "temb", "effect": "pop", "trigger": "frío", "sfx": "pop"},
       {"target": "tel", "effect": "punch", "trigger": "móvil", "amount": 0.25},
       {"target": "plof", "effect": "pop", "trigger": "apaga", "sfx": "sorpresa"},
       {"target": "duda", "effect": "pop", "trigger": "con batería", "sfx": "pop"}]}},
    {"chapter": 4, "number": "+", "headline": "Es *temporal*",
     "narration": "Tranquilo: es temporal, al calentarse se recupera.",
     "mascot": {"trigger": "Tranquilo", "pose": "point", "note": "¡Al bolsillo y calentito!", "side": "right"},
     "elements": [{"type": "tag", "text": "ES TEMPORAL", "tone": "ink", "trigger": "temporal", "sfx": "pop"},
                  {"type": "stamp", "text": "SE RECUPERA", "tone": "accent", "trigger": "recupera", "sfx": "sello"}]},
    {"chapter": 5, "headline": "Dudas → *truco*", "narration": "Tú traes las dudas y nosotros te damos el truco.",
     "elements": [{"type": "trick", "trigger": "Tú", "reveal_trigger": "nosotros"}]},
    {"chapter": 5, "number": "TÚ", "headline": "*Confiesa*", "narration": "Síguenos y las resolvemos. ¿A ti se te ha apagado con frío?",
     "elements": [{"type": "follow", "trigger": "Síguenos"}, {"type": "ask", "text": "¿A ti se te ha *apagado* con frío?", "trigger": "¿A"}]}
  ]
}
```
- Escenas 1-3 llevan `"number": "1"|"2"|"3"`. `free` añade `"height": 820-900`. Titular 2-5 palabras con un `*resaltado*`.
- `mascot`: UN objeto por escena (`pose`: idle, point, wave, think, surprise, explain, cheer; `until` opcional). 1-2 cameos por vídeo,
  nunca en escenas con ilustración y tarjetas a la vez. Con ilustración, como mucho 1 tarjeta pequeña (tag, stamp o stat).
- `sfx`: whoosh, pop, papel, ding, sorpresa, sello, chasquido, chorro, burbujas, splash, boing, rotulador, brillo, none.

## 2. El DSL de animación (`illustration.anims`)
Cada `target` es el id de un `<g id>` SIN `transform` propio (usa `g()`/`gt()` de la librería). `origin` es una esquina o lado de la
caja del grupo (center, bottom, top, left, right, bottom-left, bottom-right, top-left, top-right). 30 fps.

| efecto | qué hace (motor) | valores que han funcionado |
|---|---|---|
| `pop` | entra escalando con muelle (≈0,35 s) | etiquetas, iconos, sellos; con `origin` sale de una esquina (bocadillos) |
| `fade` | entra con fundido (`dur`, por defecto 0,7) | 0,12-0,15 cambios de cara o cifra; 0,4-0,9 capas (líquido espeso) |
| `draw` | dibuja trazos (`dur` 0,7) | flechas, líneas tope, grietas: 0,35-0,6; franjas largas 1,5 |
| `grow` | estira en vertical desde `origin` (bottom por defecto) | barras, columnas 0,6; `origin: top` = baja/desenrolla, 1-1,2 |
| `slide-left/right/up/down` | entra desde 260 px a la izq./der., 220 px abajo/arriba | `dur` 0,4-0,6 + `whoosh`; la entrada del instante 0 |
| `hide` | sale con fundido de 6 fotogramas; sin trigger = oculto desde el inicio | relevos de capas, cosas que «caen dentro» |
| `move` | `to` [dx, dy] y/o `rotate` (grados), muelle en `dur`; SE SUMAN | gestos rotate ±5-15, 0,5-0,7; caídas 0,25-0,6; agujas −110, 1,5 |
| `punch` | golpe de escala +16 %·amount (0,47 s) | 0,15-0,5 en la palabra que nombra la cosa |
| `breathe` | respira: alto ±3 %, ancho ±1,2 %·amount, 2,6 s | personas 0,5-0,9 `origin: bottom`, `phase` distinta por persona |
| `sway` | balanceo ±6°·amount, 3,1 s (sin `phase`: desfasa con `delay`) | cuerpo 0,12-0,15; cabeza 0,22-0,4; brazos 0,1-0,3; plantas 0,1 |
| `float` | sube y baja ±10 px·amount, 2,9 s | 0,2-0,5 (iconos, iones, globos) |
| `bob` | botecitos 14 px·amount | 0,4 (sudor, cosas que rebotan) |
| `drift` | deriva lateral ±18 px·amount, 5,7 s (`phase`) | 0,3-1,1 (copos, nubes, frío de la nevera) |
| `pulse` | late ±7 %·amount, 1,3 s | 0,2-0,6 (luces, cifras finales, LED) |
| `shake` | tiembla en horizontal ±5 px·amount | 0,15-0,8 (frío, esfuerzo, golpe) |
| `wiggle` | vaivén rápido ±5°·amount, 0,7 s | 0,35-0,5 (manos, tijeras, alertas) |
| `spin` | gira 120°/s·amount | 0,05-0,15 (copos, minutero, sol) |
| `flow` | trazo discontinuo que corre | 0,5-0,6 tras un `draw` (flechas, agua) |
| `ripple` | anillo que crece y se apaga, 1,6 s | dos anillos con `phase` 0 y 0,5 |
| `blink` | parpadeo de 5 fotogramas cada 3 s (sin `phase`) | `delay` distinto por persona (0,4-1,7) |
| `zoom` (`target: "camera"`) | acerca a `to` [x, y] del viewBox; `amount: 1` vuelve | full 1,08-1,22, `dur` 0,9-1,6; panel 1,3-1,8; 1-2 por escena |
| `squash` (entrada) | cae estirado desde `to` (por defecto [0, −320]) y al tocar se aplasta y rebota (`amount` = rebote) | personas `dur` 0,6 + `boing`; avisos `to` [0, −160] 0,5; objetos `amount` 0,7 0,55 |
| `move` + `antic` | antes del gesto retrocede `antic` (fracción) y luego se lanza | cabeza que se encoge 0,4 (0,5 s); brazo que saca el móvil 0,18-0,5 (0,55-0,7 s) |
| `pan` | desplaza `to` [dx, dy] (y `rotate`) sin rebote, ease in-out en `dur` (6 por defecto) | parallax lejos −14, medio −40, cerca −110 en 6 s; niveles que bajan 2 s; hoja de salida [0, −2020] 0,75 |
| `jitter` | temblor nervioso en x, y y giro (bucle) | 0,9 en cifras que caen; 0,3-0,5 en objetos nerviosos |
| `flutter` | ondea con viento: dos senos desfasados (bucle) | bufanda, pelo, banderas 0,8 `origin: top`, `phase` 0,1 |
| `puff` | partícula que nace, sube creciendo y se apaga, 1,8 s (bucle); `to` = recorrido | vaho y humo: 3 copias, `phase` i/3, `to` [70, −110] |
| `fall` | cae en bucle recorriendo `to[1]` (900 por defecto) centrado en su sitio | copos: `amount` 0,7-1,3, `phase` al azar, `to` [0, 1500] + `drift` 0,4-1 + `spin` 0,05-0,15 |

Reglas del motor: una entrada deja el grupo oculto hasta su momento; lo último que pasa manda (entrada, `hide`, entrada…).
Los bucles empiezan en su `at` (sin trigger ni delay, al empezar la escena). Hay un avance de cámara automático ×1,045.

## 3. Recetas rossark en nuestro DSL
Principios: nunca teletransportar; amplitudes pequeñas; cada parte gira sobre su pivote; cada parte con su fase (nada en sincronía);
izquierda y derecha nunca en espejo; nada congelado mientras está en pantalla; cabeza y manos llegan después del cuerpo.

**Persona viva** (`persona("ana", …)` da `ana`, `ana_cabeza`, `ana_ojos`, `ana_brazo_izq/der`; izq/der = lado de la pantalla):
```json
{"target": "ana", "effect": "breathe", "origin": "bottom", "amount": 0.8, "phase": 0.2},
{"target": "ana", "effect": "sway", "origin": "bottom", "amount": 0.15},
{"target": "ana_cabeza", "effect": "sway", "origin": "bottom", "amount": 0.35, "delay": 0.18},
{"target": "ana_ojos", "effect": "blink", "delay": 0.6},
{"target": "ana_brazo_izq", "effect": "sway", "origin": "top-right", "amount": 0.18, "delay": 0.9},
{"target": "ana_brazo_der", "effect": "sway", "origin": "top-left", "amount": 0.3, "delay": 0.35},
{"target": "ana_brazo_der", "effect": "move", "trigger": "gastar", "rotate": -14, "origin": "top-left", "dur": 0.6},
{"target": "ana_brazo_der", "effect": "move", "trigger": "veintinueve", "rotate": 8, "origin": "top-left", "dur": 0.7}
```
Brazos distintos en cada lado (`("relajado", "explica")`, `("relajado", "sujeta")`, nunca `("abajo", "abajo")`). Segunda persona:
`phase` 0,65 y otros `delay` (1,1 · 1,3 · 1,7). Mano por encima del hombro: `bottom-left`/`bottom-right`.

**Cabeza con retraso** (el cuerpo actúa y la cabeza llega un poco después, a menos fuerza y en sentido contrario):
```json
{"target": "dani", "effect": "move", "trigger": "golpe", "to": [0, -40], "dur": 0.25},
{"target": "dani", "effect": "move", "trigger": "sientes", "to": [0, 40], "dur": 0.45},
{"target": "dani_cabeza", "effect": "move", "trigger": "que", "rotate": 6, "origin": "right", "dur": 0.5}
```
El trigger no admite retraso: usa la palabra SIGUIENTE o un `dur` mayor (cuerpo 0,4, cabeza 0,7). En bucles, `delay` de la cabeza
0,2-0,3 s mayor que el del cuerpo. Partes que están fuera del grupo (p. ej. `dani_brazo`) llevan el mismo `move` que el cuerpo.

**Cara que cambia con fundido**: dos `persona()` iguales en el mismo sitio, metidas en un grupo padre que lleva los bucles.
```python
body += g("chico", persona("chf", 380, 1300, 1.22, expresion="frio", **kw) + persona("chs", 380, 1300, 1.22, expresion="sorpresa", **kw))
```
```json
{"target": "chs", "effect": "hide"},
{"target": "chico", "effect": "breathe", "origin": "bottom", "amount": 0.6, "phase": 0.2},
{"target": "chf_ojos", "effect": "blink", "delay": 0.6}, {"target": "chs_ojos", "effect": "blink", "delay": 0.6},
{"target": "chf", "effect": "hide", "trigger": "apaga"},
{"target": "chs", "effect": "fade", "trigger": "apaga", "dur": 0.15}
```
Los bucles de cabeza y brazos se repiten IGUALES en las dos caras para que el relevo no salte. `sueno.durmiente` ya trae `_cara_<exp>`.

**Barras que crecen desde la base** (recorte + barra dibujada ya crecida pero bajada su altura; un `move` la saca con ease-out):
```python
clip = f'<clipPath id="clipB"><rect x="0" y="0" width="1000" height="{base}"/></clipPath>'
body += '<g clip-path="url(#clipB)">' + "".join(g(i, barra(None, x, base + h, w, h, col=c)) for i, x, h, w, c in datos) + "</g>"
guardar(f"{OUT}/datos_free.svg", svg(body, "free", h=820, defs=clip))
```
```json
{"target": "b33", "effect": "move", "trigger": "mil", "to": [0, -198], "dur": 0.7, "sfx": "pop"},
{"target": "b58", "effect": "move", "trigger": "justificaron", "to": [0, -348], "dur": 1.2, "sfx": "ding"},
{"target": "b33", "effect": "breathe", "trigger": "los", "origin": "bottom", "amount": 0.35},
{"target": "v33", "effect": "fade", "trigger": "los", "dur": 0.25}
```
Escalona 0,15-0,3 s entre barras. Versión simple: `{"effect": "grow", "origin": "bottom", "dur": 0.6}`. Valor encima al terminar.

**Contador que sube por capas** (una capa por valor; la última sin sufijo):
```python
def cuenta(prefijo, cx, cy, valores, w, h=110, size=None):
    return "".join(contador(prefijo if i == len(valores) - 1 else f"{prefijo}_{i}", cx, cy, v, w=w, h=h, size=size) for i, v in enumerate(valores))
body += cuenta("c37", 500, 285, ("0,12 €", "0,25 €", "0,37 €"), w=360, h=130)
```
```json
{"target": "c37_0", "effect": "fade", "trigger": "treinta", "dur": 0.15, "sfx": "ding"},
{"target": "c37_0", "effect": "hide", "trigger": "siete"}, {"target": "c37_1", "effect": "fade", "trigger": "siete", "dur": 0.15},
{"target": "c37_1", "effect": "hide", "trigger": "céntimos"}, {"target": "c37", "effect": "fade", "trigger": "céntimos", "dur": 0.15},
{"target": "c37", "effect": "punch", "trigger": "céntimos", "amount": 0.3}
```
3-6 capas, una por palabra seguida. Sin caja digital: `g("v58_0", T(...))` + `g("v58", T(...))`. Tarjeta del motor: `stat` con `from`.

**Objeto que entra ya en movimiento** (nunca aparece quieto: entra desde fuera y su bucle empieza cuando acaba la entrada):
```json
{"target": "tel", "effect": "slide-up", "delay": 0, "dur": 0.5, "sfx": "whoosh"},
{"target": "tel", "effect": "float", "amount": 0.3, "delay": 0.5},
{"target": "cp0", "effect": "slide-down", "delay": 0.0, "dur": 0.6}, {"target": "cp0", "effect": "float", "amount": 0.52, "delay": 0.74},
{"target": "cp0", "effect": "drift", "amount": 0.72, "phase": 0.6},
{"target": "mon0", "effect": "move", "trigger": "gastar", "to": [70, 270], "rotate": 40, "dur": 0.5, "sfx": "whoosh"},
{"target": "mon0", "effect": "hide", "trigger": "partido"}, {"target": "saco", "effect": "punch", "trigger": "partido", "amount": 0.15}
```
Repetidos (copos, iones, monedas): cada uno su `delay` (+0,05), `amount` y `phase` sacados de `random.Random(semilla)`.

**Pivote en hombro o base**: `origin` gira sobre una esquina de la caja del grupo (cabeza `bottom` = cuello; brazo der `top-left`
e izq `top-right` = hombro; pierna `top` = cadera; planta, cartel, persona `bottom`; bandera `left`; cabeza tumbada `right`).
Si el eje no cae en una esquina (aguja, rueda, codo), mete `mente.pivote(px, py, r)` en el grupo: con él, `center` = (px, py).
```python
body += g("med_aguja", pivote(cx, cy, r * 0.75) + trazo(f"M {cx} {cy} L {tx} {ty}", 9, INK, 5))
```
```json
{"target": "med_aguja", "effect": "move", "trigger": "entrega", "rotate": -110, "origin": "center", "dur": 1.5, "sfx": "whoosh"}
```

**Cámara con parallax en 3 planos** (el fondo de papel ya trae `lejos`, `medio` y `cerca`; personas y objetos van aparte, sin pan):
```json
{"target": "camera", "effect": "zoom", "delay": 0, "to": [500, 930], "amount": 1.08, "dur": 2.6},
{"target": "camera", "effect": "zoom", "delay": 2.9, "to": [520, 960], "amount": 1.03, "dur": 0.35},
{"target": "camera", "effect": "zoom", "delay": 3.2, "to": [600, 900], "amount": 1.2, "dur": 1.3},
{"target": "lejos", "effect": "pan", "delay": 0, "to": [-14, 0], "dur": 6},
{"target": "medio", "effect": "pan", "delay": 0, "to": [-40, 0], "dur": 6},
{"target": "cerca", "effect": "pan", "delay": 0, "to": [-110, 0], "dur": 6}
```
El zoom 1,03 entre los dos acercones es la anticipación de cámara (retrocede antes del golpe). Zoom final como mucho 1,2 en
`full` (con titular de 2 líneas, 1,06-1,1). Lejos poco, cerca mucho: nunca los tres planos a la misma velocidad.

**Copos, vaho y bufanda** (movimiento secundario de la muestra C):
```json
{"target": "bufanda", "effect": "flutter", "origin": "top", "amount": 0.8, "phase": 0.1, "delay": 0.25},
{"target": "vh0", "effect": "puff", "delay": 0.3, "phase": 0, "to": [70, -110]},
{"target": "cp0", "effect": "fall", "amount": 0.9, "phase": 0.37, "to": [0, 1500]},
{"target": "cp0", "effect": "drift", "amount": 0.6, "phase": 0.2}, {"target": "cp0", "effect": "spin", "amount": 0.1},
{"target": "pct_grp", "effect": "jitter", "delay": 2.5, "amount": 0.9}
```

## 4. Composición
- **Grandes**: al menos 2 escenas `free`/`full` (los aprobados usan casi solo free/full). `free` con `height` 820-900 y el
  protagonista ocupando más de media anchura; `full` para el gancho y lo espectacular; `panel` solo para esquemas con fondo propio.
- **Nada de paneles vacíos**: fondo y protagonista se ven desde el primer fotograma; las entradas por trigger son detalles
  (etiquetas, flechas, iconos, cifras). Si la escena reutiliza un SVG, oculta con `hide` lo que no toca.
- **Instante 0**: cada escena tiene una entrada con `"delay": 0` (`slide-up`/`slide-down` 0,5 s + `whoosh`) y sus bucles ya andando.
- **Cada 3 s pasa algo** (mejor cada 1-1,5 s): entrada, `move`, `punch`, `zoom` o tarjeta en la palabra que lo dice. Los bucles no
  cuentan para `revisar.py`; si la frase no tiene palabras clave, rellena con `delay`.
- **Titular libre**: el titular ocupa arriba (pantalla y 236-450). En `full` nada de texto ni etiquetas por encima de y 450 (y 520
  si el titular ocupa 2 líneas) y zoom como mucho 1,25. Titular corto (2-5 palabras) para que quepa en una línea.
- **Zonas seguras**: `panel` 1000×700, nada importante fuera de y 45-655 y esquina 0-340 × 0-70 libre para «Fig.»;
  `free` 1000×h transparente (sin rect de fondo); `full` 1080×1920, lo importante entre y 450 y 1250; por debajo de 1300 van los
  subtítulos (pantalla y 1350-1480), ahí solo suelo o fondo. Etiquetas a 40 unidades o más del borde, sin solaparse entre sí.

## 5. Errores que ya han salido y su arreglo
| error | arreglo |
|---|---|
| Titular pisado | En `full`, nada por encima de y 450; quita o baja el zoom; acorta el titular; oculta con `hide` antes del zoom las etiquetas altas. |
| Mascota con una sola pose por escena | El motor admite UN cameo con UNA pose por escena: no pongas listas ni dos `mascot`. Elige la pose de la palabra del trigger (surprise en el dato, cheer en el alivio, point hacia una tarjeta) y deja que las tarjetas aporten el cambio; la segunda reacción, en otra escena. |
| Triggers que no coinciden | Si la palabra no está en la narración de ESA escena, la anim cae en silencio a inicio + 0,3 s. Las anims buscan desde el inicio de la escena (primera aparición); una palabra sola casa por prefijo («la» casa con «lavar»): para la segunda aparición usa 2 palabras («un líquido»). Comprueba con el script de §6. |
| Cifras con unidades en la voz | La voz Edge desalinea «0 a 97 km/h», «20 °C», «50 %». En `narration` escribe con palabras («veinte grados bajo cero», «la mitad»); las cifras van en el dibujo («−20 °C», «50 %»); triggers = esas palabras. |
| Escena «+» vacía | Sin ilustración necesita mascota y 2-3 tarjetas `tag`/`stamp` con triggers repartidos (una cada 1-1,5 s), como en los aprobados; o reutiliza un SVG del vídeo con otros zooms. |
| Todo a la vez o cuerpos en sincronía | `phase`/`delay` distintos por parte y por persona; amplitudes de la tabla (§2). |
| Protagonista estatua | Receta «persona viva» completa + un gesto (`move` rotate) en cada palabra clave. |
| Zoom que corta etiquetas | Visible = viewBox / amount alrededor de `to`; oculta antes lo que quede fuera. |

## 6. Flujo de trabajo (8 pasos, con tope de control de calidad)
1. Lee `CLAUDE.md`, esta guía y SOLO tu bloque de guion (`grep -n <carpeta> guiones/semana-*.md`). No investigues ni reescribas.
2. Plan por escena: layout, protagonista, y 3-5 momentos con su palabra exacta. Busca en el índice (§7) las piezas y lee en
   `libreria/README.md` SOLO las firmas de las que vas a usar.
3. Dibuja en `libreria/archivo/<tema>/dib.py` (copia la cabecera de `libreria/archivo/frio-bateria/dib.py`: `ROOT`, imports, `OUT`) y
   ejecútalo: `python3 libreria/archivo/<tema>/dib.py` → `content/<carpeta>/*.svg`. Pieza nueva reutilizable: a `libreria/` sin romper nada.
4. Escribe `content/<carpeta>/guion.json` (§1) con las recetas (§3). `publish.at` exacto el del calendario.
5. Triggers: pega esto tal cual (no imprime nada si todo casa):
```bash
python3 - content/<carpeta> <<'EOF'
import json,sys; sys.path.insert(0,"."); from autocontent.timeline import norm
for i,s in enumerate(json.load(open(sys.argv[1]+"/guion.json"))["scenes"]):
    ws=[norm(w) for w in s["narration"].split()]
    for o in (s.get("illustration") or {}).get("anims",[])+s.get("elements",[])+[s.get("mascot") or {}]:
        for k in ("trigger","reveal_trigger"):
            t=[norm(x) for x in (o.get(k) or "").split() if norm(x)]
            if t and not any(ws[j:j+len(t)]==t or (len(t)==1 and ws[j].startswith(t[0])) for j in range(len(ws))): print(i,k,o[k])
EOF
```
6. `python3 scripts/revisar.py content/<carpeta>` (sin imágenes) hasta que pase: duración 40-60 s, huecos de 3 s, fuera de cuadro, textos.
7. UN SOLO render local sin voz: `python3 scripts/qa_frames.py content/<carpeta> <scratchpad>/qa-<carpeta>`. Mira COMO MUCHO 3
   imágenes (las hojas `hoja_0.png`, `hoja_1.png`… con 4 escenas × 3 instantes, o fotogramas `sNN_k.png` sueltos). Busca titular
   pisado, paneles vacíos, cortes. Arregla y vuelve a `revisar.py`; no hay segundo render.
8. Sube: `python3 scripts/entrega.py content/<carpeta>`, `git add content/<carpeta> entregas/<carpeta>.md` (+ `libreria/…` si
   hay piezas nuevas), commit, `git pull --rebase --autostash origin <rama> && git push -u origin <rama>`. NUNCA `git stash pop`.
   Reglas de subida de cada encargo en `docs/encargo-comun.md`.

## 7. Índice de la librería (`libreria/svg/`; firmas en `libreria/README.md`)
- **papel** (OBLIGATORIO, §0): `a_papel`, `recolorear`, `recorte`, `capa`, `grano`, `fx`, `PAPEL`/`EQUIV`/`color_papel`, fondos `fondo_calle`, `fondo_casa`, `fondo_cielo`, `fondo_neutro`, `hoja_transicion`.
- **base**: paleta (AZUL, LIME, CORAL, INK, AMARILLO, TEAL…), `svg`, `guardar`, `g`, `gt`, `T`, `degradado`, `trazo`, `sombra`, `brillo`; `etiqueta`, `flecha`, `flecha_gorda`, `globo`, `sello`, `onomatopeya`, `icono_duda/alerta/ok/no`, `contador`, `barra`, `medidor`, `copo`, `vaho`, `temblor`, `zzz`, `gota`, `nube`, `onda_expansiva`, `lupa`, `confeti`.
- **personajes**: `persona(id, x, y, escala, edad, piel, pelo, …, expresion, pose, brazos=(izq, der))` (ids `_cabeza`, `_ojos`, `_boca`, `_brazo_izq/der`; `.puntos` boca, mano_der, cima…), `manos_entrelazadas`, `multitud`, `pictograma`.
- **animales**: `perro` (bostezo), `icono_perro`, `gato` (caída en el aire), `mono` (en una rama, duerme o agarra).
- **aviones**: `jumbo`, `perfil_ala`, `lineas_corriente`, `signo_presion`, `cochecito`, `manzana`, `retrato_newton`, `pista_despegue`, fondo `aula`.
- **casa**: `vaso`, `botella`, `taza`, `mesa`, `ventana`, `movil(pantalla=)`, `reloj`, `bombilla`, `sofa`, `banco`, `cronometro`, `pizarra`, `portapapeles`, `trofeo`, `escoba`, `tambor`, `tubo_pasta`, `tostada`, `etiqueta_precio`, `escalera`, `espejo_roto`.
- **coches**: `deportivo_lateral` (corte, ruedas spin), `deportivo_cenital`, `motor_bloque`, `centro_gravedad`, `escudo_porsche`, `persona_cenital`, `flecha_giro`, `marcas_derrape`; fondos `sala_presentacion`, `carretera`, `pista_hielo`.
- **compra**: `brick_leche`, `nevera` de súper, `lista_compra`, `barra_pan`, `horno_pan`, `camion_frigorifico`, `carretilla`, `caja_carton`, `palet`, `galletas`, `chocolate`, `cana_pescar`.
- **cuerpo**: `cerebro`, `cabeza_perfil`, `musculo`, `antebrazo` (piel de gallina), `termometro`, `articulacion`, `mano`, `escaner_resonancia`, `oido_interno`, `aparato_digestivo`, `estomago_corte`, fondo `intestino_interior`.
- **dinero**: `banco`, `torre_bce`, `bandera_ue`, `moneda_euro`, `ficha`, `recibo_hipoteca`, `palanca`, `saco_dinero`, `linea_tope`.
- **escenarios** (fondos): `habitacion`, `cocina`, `oficina`, `escenario`, `cielo`, `sol`, `rotonda`, `coche_aereo`, `arbol_aereo`, `edificio_aereo`.
- **frio**: `congelador`, `cuenco`, `vapor_subiendo`, `escarcha`, `corrientes` (convección), `burbujas_gas`, `grafica_enfriamiento`.
- **memoria**: `puerta`, `tijeras`, `caja_colores`, `bocadillo_piensa` (dibujo dentro), `humo`, `gota_esfuerzo`, `mando_consola`, `sala_pixel`, `tele_antigua`, `tira_pelicula`, `archivador`, `birrete`.
- **mente**: `pivote`, `pluma`, `bola_cristal`, `engranaje`, `barra_volumen`, `cara_cerebro`.
- **nervios**: `pierna_nervio`, `pierna_encima`, `vaso_tubo`, `nervio_tubo`, `haz_fibras`, `rodilla_lateral`, `hormiga`, `aguja`, `nervio_lupa`.
- **noche**: `ojo`, `icono_sentido`, `interruptor`, `mano_indice`, `sombra_monstruo`, `hoguera`, `leona`, `acacia`, `matas`, fondo `sabana_noche`, `fase_luna`, `calabaza`, `fantasma`, `bandera_canada`.
- **piel**: `piel_corte`, `habon`, `mosquito`, `mastocito`, `histamina`, `bacteria`, `raton_lab`, `mano_rasca`, `reloj_arena`, `sirena`, `gorra`, `delantal`, fondo `piscina`.
- **politica**: `urna`, `sobre`, `papeleta*`, `dni`, `hemiciclo`, `capa_escanos`, `tabla_dhondt`, `calendario`, `atril`, `documento`, `sin_posicionarnos`, `carta_notificacion`, `formulario`, `bombo`, `mesa_electoral`, `colegio_electoral`, `corona`, `baston_mando` (sus PARTIDOS son ficticios: los reales van con su nombre y colores).
- **reptiles**: `basilisco`, `pata_basilisco`, `pie_lateral`, `bolsa_aire`, `salpicadura`, `agua_corte`, `revista`, fondo `selva_rio`.
- **sueno**: `cama_lateral`, `durmiente` (`_cara_<exp>`), `marioneta`, `arbol_rama`, `pierna_corte`, `musculo_ventana`.
- **tecnologia**: `pantalla_movil`, `bateria`, `chip`, `logo_apple`, `icono_app`, `barra_almacenamiento`, `pantalla_cargando/almacenamiento/salud`, `papelera`, `armario`, `brazo_robot`, `iones_bateria`, `caja_pesada`, `bateria_esfuerzo`.
- **territorio**: `mapa_espana`, `balanza`, `ciudad`, `pueblo`.
- **tiempo**: `cama` (detrás/delante), `mesilla`, `despertador`, `luna`, `flecha_atras`.
- **tienda**: `cartel_precio`, `producto`, `estanteria`, `carrito`, `ticket`, `recta_numerica`, `billete`, `etiqueta_lineal`, `paquete`, `rollo_papel`, fondo `supermercado`.
- **vuelo**: `roadster`, `chorro`, `deposito_aire`, `rampa`, `avion`, `globo_aire`, `extintor`, `pesa`, `logo_tesla`, fondo `pista_pruebas`.

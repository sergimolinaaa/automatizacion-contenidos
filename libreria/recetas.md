# Recetas de animación (DSL de `guion.json`)

Bloques listos para pegar dentro de `illustration.anims` (o `elements`). Motor: `video/src/components/Illustration.tsx`,
tipos: `video/src/types.ts`, conversión trigger→tiempo: `autocontent/timeline.py`.

## Reglas rápidas
- `trigger` = palabra EXACTA de la narración de **esa** escena (sin signos). El motor usa el inicio de esa palabra − 0,05 s.
- Sin trigger: los **bucles** empiezan con la escena; las **entradas** (pop, fade, draw, grow, slide-*) también.
  Alternativa a trigger: `"delay": 1.2` (segundos desde el inicio de la escena).
- Una entrada deja el grupo **oculto hasta su momento**. `hide` sin trigger = oculto toda la escena. Lo último que pasa manda.
- `move` es relativo (unidades del viewBox) y **se suman**; en grupos rotados van en coordenadas locales. `origin` = punto de giro de la caja del grupo.
- Los ids animados deben ser grupos `<g id>` **sin** `transform` propio (la librería ya lo hace así con `gt()`).
- Cámara: `{"target":"camera","effect":"zoom","to":[x,y],"amount":1.3-2}`; `amount: 1` vuelve al plano general. Hay además un avance lento automático (×1,045).
- `sfx`: whoosh, pop, papel, ding, sorpresa, sello, chasquido, chorro, burbujas, splash, boing, rotulador, brillo, none.

## Ritmo: nunca más de 3 s sin cambio
Una escena dura 2,5-6 s. Plan tipo (escena de 4 s, 10-12 palabras):
| t (s) | qué pasa | cómo |
|---|---|---|
| 0 | dibujo completo + bucle de fondo | `breathe` / `float` / `ripple` sin trigger |
| ~0,8 | 1.ª palabra clave | `pop` etiqueta o `punch` del protagonista |
| ~1,8 | 2.ª | `draw` flecha o `zoom` de cámara |
| ~2,8 | 3.ª | `pop` sello / `move` |
| ~3,6 | remate | `punch` / `pulse` |
Si la frase tiene pocas palabras clave, usa `delay` para rellenar huecos (p. ej. un `punch` con `"delay": 1.5`).
Cada 1-1,5 s algo nuevo; nunca un hueco de 3 s sin entrada, acción o zoom.

---

## 1. Algo que cae
```json
{"target": "manzana", "effect": "slide-down", "trigger": "cae", "dur": 0.5, "sfx": "whoosh"},
{"target": "manzana", "effect": "move", "trigger": "suelo", "to": [0, 260], "dur": 0.5, "sfx": "boing"},
{"target": "manzana", "effect": "punch", "trigger": "golpe", "amount": 0.4}
```
`slide-down` entra desde arriba (−220 px); el `move` posterior la deja en el suelo. Para un rebote, añade otro `move` `to:[0,-40]` y luego `to:[0,40]`.

## 2. Algo que crece
```json
{"target": "barra2", "effect": "grow", "trigger": "sube", "dur": 0.6, "origin": "bottom", "sfx": "pop"},
{"target": "barra2", "effect": "pulse", "amount": 0.4, "trigger": "doble"}
```
`grow` estira en vertical desde `origin` (por defecto abajo). Va perfecto con `base.barra()` y la columna de `cuerpo.termometro()` (`<id>_columna`).
Para que algo "se infle" en las dos direcciones usa `pop` (escala desde el centro).

## 3. Comparación antes / después (mismo sitio, dos dibujos)
```json
{"target": "despues", "effect": "hide"},
{"target": "antes", "effect": "punch", "trigger": "antes", "amount": 0.2},
{"target": "antes", "effect": "hide", "trigger": "ahora"},
{"target": "despues", "effect": "pop", "trigger": "ahora", "sfx": "pop"},
{"target": "tdespues", "effect": "pop", "trigger": "ahora"}
```
Ejemplos en la librería: `cuerpo.musculo(contraido=False/True)`, `antebrazo` (`_vello` → `_erizado` + `_bultos`), dos `persona()` con expresiones distintas en el mismo punto.
Variante en pantalla partida: dibuja izquierda/derecha y usa `slide-left` / `slide-right` con 1 s de diferencia. Como tarjeta: elemento `compare`.

## 4. Zoom a un detalle sin cortar etiquetas
```json
{"target": "tgeneral", "effect": "hide", "trigger": "dentro"},
{"target": "camera", "effect": "zoom", "trigger": "dentro", "to": [482, 352], "amount": 1.8, "dur": 0.7},
{"target": "tdetalle", "effect": "pop", "trigger": "termostato", "sfx": "ding"},
{"target": "camera", "effect": "zoom", "trigger": "resto", "amount": 1}
```
- Oculta con `hide` las etiquetas que quedarían cortadas fuera del encuadre ANTES del zoom.
- La etiqueta del detalle debe caer dentro del recuadro visible: ancho visible = viewBox / amount (1000/1.8 ≈ 555 px alrededor de `to`).
- Usa los anclajes de la librería: `cerebro(...).puntos["hipotalamo"]`, `persona(...).puntos["boca"]`, `urna(...).puntos["ranura"]`.
- Máximo 1-2 zooms por escena; nunca tapes el titular (en `full`, deja lo importante entre y 450 y 1250).

## 5. Contador animado
Con la tarjeta del motor (cuenta sola de `from` a `value`):
```json
"elements": [{"type": "stat", "label": "VOTOS VÁLIDOS", "from": 100000, "value": 109000, "unit": "", "trigger": "109.000", "sfx": "ding"}]
```
Dentro del dibujo (`base.contador()` dos veces en el mismo sitio, ids `v100` y `v109`):
```json
{"target": "v109", "effect": "hide"},
{"target": "v100", "effect": "pop", "trigger": "suma"},
{"target": "v100", "effect": "hide", "trigger": "109.000"},
{"target": "v109", "effect": "pop", "trigger": "109.000", "sfx": "ding"},
{"target": "v109", "effect": "pulse", "amount": 0.4}
```

## 6. Globo de texto / bocadillo
```json
{"target": "globo1", "effect": "pop", "trigger": "dice", "origin": "bottom-left", "sfx": "pop"},
{"target": "globo1", "effect": "float", "amount": 0.4},
{"target": "p1_boca", "effect": "pulse", "trigger": "dice", "amount": 1.5}
```
Coloca la cola del `base.globo()` en `persona(...).puntos["boca"]`. `origin` en la esquina de la cola: el globo "sale" de la boca.
Para el matraz (mascota) usa `"mascot": {"trigger": "…", "pose": "think", "note": "máx. 8 palabras", "side": "right"}` (no en escenas con ilustración + tarjetas).

## 7. Aparición en cascada
```json
{"target": "chip0", "effect": "slide-up", "trigger": "Estrella", "dur": 0.4, "sfx": "pop"},
{"target": "chip1", "effect": "slide-up", "trigger": "Círculo", "dur": 0.4},
{"target": "chip2", "effect": "slide-up", "trigger": "Triángulo", "dur": 0.4},
{"target": "chip3", "effect": "slide-up", "delay": 2.6, "dur": 0.4},
{"target": "chip4", "effect": "slide-up", "delay": 2.8, "dur": 0.4}
```
Sin palabras para cada pieza, escalona con `delay` cada 0,2-0,3 s. Hemiciclo escaño a escaño: `hemiciclo(..., ids=True)` → ids `<id>_e0…`.
En tarjetas: `list` con `items[].trigger`.

## 8. Señalar con flecha
```json
{"target": "flecha1", "effect": "draw", "trigger": "aquí", "dur": 0.5, "sfx": "rotulador"},
{"target": "tagua", "effect": "pop", "trigger": "agua"},
{"target": "flecha1", "effect": "flow", "amount": 0.6}
```
`draw` dibuja el trazo (las flechas de `base.flecha()` son trazos dobles: se dibujan con contorno). Para que "empuje", añade
`{"target":"flecha1","effect":"move","to":[20,0],"trigger":"…"}`. Persona que señala: `persona(..., brazos=("abajo","senala"))` + `wiggle` en `<id>_brazo_der` con `origin: "left"`.

## 9. Sello que golpea
```json
{"target": "sello", "effect": "pop", "trigger": "falso", "sfx": "sello"},
{"target": "sello", "effect": "punch", "trigger": "falso", "amount": 0.5},
{"target": "protagonista", "effect": "shake", "trigger": "falso", "amount": 0.6}
```
`base.sello()` / `politica.sin_posicionarnos()`. Como tarjeta: `{"type": "stamp", "text": "MITO", "tone": "hot", "trigger": "mito"}`.
Política (obligatorio, escena 1): `{"type": "tag", "text": "SIN POSICIONARNOS", "tone": "ink", "trigger": "posicionarnos"}` o el sello dibujado.

## 10. Latido / pulso de fondo (bucles, sin trigger)
```json
{"target": "corazon", "effect": "pulse", "amount": 1.2},
{"target": "anillo1", "effect": "ripple", "phase": 0},
{"target": "anillo2", "effect": "ripple", "phase": 0.5},
{"target": "p1", "effect": "breathe"},
{"target": "p1_ojos", "effect": "blink"},
{"target": "nubes", "effect": "drift", "amount": 0.6},
{"target": "sol_rayos", "effect": "spin", "amount": 0.15}
```
`ripple` va con `base.onda_expansiva()` (dos anillos, phase 0 y 0,5). `breathe` + `blink` dan vida a cualquier `persona()`.
Temblar de frío: `{"target":"p1","effect":"shake","amount":0.5}` + `{"target":"temblor","effect":"wiggle"}`.

## Extras útiles
- Saludo: `{"target":"p1_brazo_der","effect":"wiggle","origin":"bottom-left","amount":1.5}` con `brazos=("abajo","saluda")`.
- Asentir: `{"target":"p1_cabeza","effect":"sway","origin":"bottom","amount":0.6}`.
- Sobre que entra en la urna: `{"target":"sobre","effect":"move","trigger":"meter","to":[0,95],"dur":0.6,"sfx":"whoosh"}` y luego `hide`.
- Coche por la rotonda: varios `move` encadenados (los move se suman) o dibuja el coche en 2-3 posiciones y alterna `hide`/`pop`.
- Intermitente: `{"target":"car0_inter","effect":"pulse","amount":3}` (blink aplasta en vertical: úsalo solo para ojos).

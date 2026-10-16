# Librería de piezas de «El truco es…»

Monta cada vídeo **combinando piezas** y dibuja solo lo específico del tema. Python 3 sin dependencias; cada función
devuelve una cadena SVG (o `Pieza`: cadena con `.puntos` = anclajes en coordenadas finales y `.caja` = (x0, y0, x1, y1)).
Estilo pegatina realista: contorno tinta `#0B0B14` 6-9 px, degradados claro→oscuro, brillo blanco arriba, sombra suave.

- `svg/base.py` — paleta, documento, etiquetas, flechas, globos, sellos, iconos, contadores, efectos.
- `svg/personajes.py` — personaje paramétrico (edad, pelo, piel, ropa, accesorios, expresión, pose, brazos).
- `svg/objetos/politica.py · casa.py · cuerpo.py · escenarios.py · animales.py` — piezas por tema ya aprobadas.
- `recetas.md` — bloques JSON de animación listos para pegar (caída, crecer, antes/después, zoom, contador, globo, cascada, flecha, sello, pulso).
- `catalogo.py` — `python3 libreria/catalogo.py salida.png` → todas las piezas en una imagen (+ `.svg`, `.html`).

## Montar una escena (ejemplo mínimo)
```python
import sys; sys.path.insert(0, "/home/user/automatizacion-contenidos")
from libreria.svg.base import *
from libreria.svg.personajes import persona
from libreria.svg.objetos import politica as P, escenarios as E

ana = persona("ana", 300, 1250, 1.3, "adulto", "media", "largo", "castano", "jersey", CORAL,
              expresion="duda", brazos=("barbilla", "abajo"))
u = P.urna("urna", 720, 1240, 300, 320, texto="CONGRESO")
body = (ana + u
        + globo("globo", 360, 520, "¿Y SI VOTO\nEN BLANCO?", cola=ana.puntos["boca"], size=40)
        + etiqueta("tranura", 760, 820, "RANURA", apunta=u.puntos["ranura"])
        + P.sobre(720, 640, 140, 95, id_="sobre"))
guardar("content/lote7-01-ejemplo/gancho_full.svg", svg(body, "full", fondo=E.habitacion()))
```
En el guion: `{"svg_file": "gancho_full.svg", "layout": "full", "anims": [ {"target":"ana","effect":"breathe"},
{"target":"ana_ojos","effect":"blink"}, {"target":"globo","effect":"pop","trigger":"blanco"},
{"target":"sobre","effect":"move","trigger":"meter","to":[0,140]} … ]}` (más en `recetas.md`).
Revisa con `bash scripts/shot.sh in.svg out.png` (para `full` usa `--window-size=1080,1920` o el `.html` del catálogo).

## Layouts (`svg(body, layout, h=None, fondo=None)`)
| layout | viewBox | reglas |
|---|---|---|
| `panel` | 1000×700 | fondo propio (`fondo_suave()`), nada importante fuera de y 45-655, esquina 0-340×0-70 libre («Fig.») |
| `free` | 1000×h (800-1100) | transparente, sobre el azul de la marca; en el guion `"height": 800-900` |
| `full` | 1080×1920 | fondo completo (escenarios); lo importante entre y 450 y 1250 |
`LAYOUTS`, `ZONA_FIG`, `ZONA_SEGURA` tienen estos números. Mínimo 2 escenas free/full por vídeo.

## base.py
**Paleta**: `AZUL #2347FF`, `AZUL_OSC`, `LIMA/LIME #C8FF2E`, `CORAL #FF5A36`, `TINTA/INK #0B0B14`, `PAPEL`, `PAPEL_GRIS`, `AMARILLO/YEL`,
`NARANJA`, `TURQUESA/TEAL`, `VIOLETA`, `ROSA`, `CIELO`, `AGUA`, `VERDE`, `VERDE_CLARO`, `TIERRA`, `MADERA`, `GRIS`, `GRIS_OSC`, `PIZARRA`. Fuentes: `MONO`, `DISP`.

**Documento y utilidades**
- `svg(body, layout="panel", h=None, w=None, fondo=None, defs="")` · `guardar(path, doc)` (valida XML) · `validar(doc)`
- `g(id_, body, extra="")` · `gt(id_, transform, body)` (grupo animable con transform interior) · `T(x, y, s, size=30, fill, anchor, font=MONO)`
- `f(v)`, `pts(p)`, `poly(p, closed)`, `smooth(p, closed, t)` (Catmull-Rom), `rot(p, c, deg)`, `shade(hex, k)`, `text_w(text, size, font)`, `solapan(a, b)`
- Degradados (se registran solos en `<defs>`): `degradado(col, k=0.28, dir="v"|"h"|"d") → "url(#…)"`, `degradado_brillo(col)` (radial),
  `lg(id, stops)`, `rg(id, stops)`, `registrar_defs(...)`. Ya registrados: `papelG, papelCrema, cristalG, cristalLado, metalG, metalH, aceroG, maderaG,
  maderaOsc, limaG, coralG, amarilloG, tarjetaG, sombraR, resplandorY, resplandorC, fondoSuave` (+ los de cada módulo).
- Estilo: `trazo(d, w, col, borde=7)` (doble trazo tinta+color; alias `dbl`), `pegatina(d, fill, sw=7, blanco=0)`, `sombra(cx, cy, rx, ry)`,
  `sombra_caja(x, y, w, h)`, `brillo(d, w, op)`, `brillo_arco(cx, cy, r)`, `fondo_suave(w, h, col1, col2, bokeh)`

**Rótulos y señales**
- `etiqueta(id_, cx, cy, text, apunta=None, desde=None, bg=INK, fg=LIME, size=30)` → Pieza (.caja) · `etiqueta_caja(cx, cy, text, size)`
- `flecha(id_, p0, p1, col=LIME, w=12, punta=30, curva=0.0 | ctrl=(x,y) [+ ctrl2])` · `flecha_gorda(id_, p0, p1, ancho=56, col=CORAL)`
- `globo(id_, cx, cy, text, cola=(x,y), size=40, tipo="habla"|"piensa"|"grito")` (usa `\n` para 2 líneas)
- `sello(id_, cx, cy, text, size=60, rot_=-8, col=CORAL)` · `cartel(id_, cx, cy, text)` (pancarta) · `tarjeta(id_, cx, cy, w, h, acento, rot_, body)`
- `onomatopeya(id_, cx, cy, "¡CRAC!", r=110, size=48)` · `ondas_sonido(id_, cx, cy, r0, n, a0, a1)`

**Iconos de reacción**: `icono_duda` (?), `icono_alerta` (!), `icono_ok` (✓), `icono_no` (✗) — todos `(id_, cx, cy, r=40)`; `aspa(id_, cx, cy, r)`,
`corazon(id_, cx, cy, s)`, `chispa(id_, cx, cy, r, col, puntas=4)`, `bandera(id_, cx, cy, w, h, cols=Italia)` (mástil; `sway` origin left), `destellos(id_, cx, cy, r)`, `rayos(id_, cx, cy, r1, r2, n, col)`, `confeti(id_, caja, n)`

**Contadores y medidores**: `contador(id_, cx, cy, "3.270", etiqueta_txt)` (pantalla digital), `marcador(id_, cx, cy, izq, der, txt_izq, txt_der)`,
`barra(id_, x, base, w, h, col, texto, valor)` (para `grow`), `medidor(id_, cx, cy, r, nivel)` (aguja en `<id>_aguja`)

**Efectos y ambiente** (sin id; envuélvelos con `g()`): `copo(cx, cy, r)`, `ondas_calor(x, y)`, `temblor(x, y)`, `lineas_velocidad(x, y)`,
`nota_musical(cx, cy, s, doble)`, `zzz(cx, cy, s)`, `gota(cx, cy, s, col)`, `vaho(cx, cy)`, `nube(cx, cy, s, contorno)`, `resplandor(cx, cy, r, "Y"|"C")`,
`onda_expansiva(id_, cx, cy, r)` (para `ripple`), `lupa(id_, cx, cy, r, contenido=svg_recortado)`

## personajes.py
`persona(id_, x, y, escala=1, edad, piel, pelo, pelo_color, ropa, ropa_color, pantalon_color, zapato_color, camisa_color,
accesorios=(), bufanda_color, expresion, pose, brazos=(izq, der), mira=-1|0|1, silla=False, espejo=False)` → Pieza
- (x, y) = suelo entre los pies (busto: centro del corte inferior). Alto a escala 1: adulto 600, mayor 575, niño 400.
- `edad`: nino, joven, adulto, mayor · `piel`: clara, media, morena, oscura · `pelo`: corto, largo, rizado, coleta, mono, calvo, rapado, None
- `pelo_color`: castano, negro, rubio, pelirrojo, canoso, blanco o hex · `ropa`: camiseta, jersey, camisa, chaqueta, vestido, abrigo
- `accesorios`: gafas, gafas_sol, gorro, bufanda, pendientes, baston, barba, bigote · `expresion`: neutral, sorpresa, risa, duda, frio, sueno, triste, enfado,
  **bostezo** (ojos apretados, cejas arriba, bocaza con dientes, lengua y campanilla + lagrimilla `{id}_lagrima`; para «abrir la boca» usa `grow` origin top en `{id}_boca`)
- `pose`: de_pie, sentado (con `silla=True` dibuja la silla), busto · `brazos`: abajo, cintura, arriba, saluda, senala, barbilla, **boca** (mano tapando el bostezo, por delante de la cara), coge, cruzados
- Sentado: el asiento queda a `128*escala` (adulto) / `63*escala` (niño) sobre `y`; úsalo con `casa.sofa(asiento=...)` / `casa.banco(asiento=...)`.
- Cambiar solo la cara: dibuja dos `persona()` iguales con distinta `expresion` en el mismo sitio y alterna `hide` + `fade` (`dur` 0.15) con el mismo trigger.
- Ids: `{id}`, `{id}_cuerpo`, `{id}_piernas`, `{id}_cabeza`, `{id}_ojos`, `{id}_cejas`, `{id}_boca`, `{id}_brazo_izq`, `{id}_brazo_der`,
  `{id}_mano_izq/der`, `{id}_acc_<accesorio>` (izq/der = lado de la pantalla).
- `.puntos`: cabeza, boca, ojos, cima, pies, mano_izq, mano_der, hombro_izq, hombro_der, alto.
- También: `cabeza(id_, rx, ry, hy, …)` (solo la cabeza, coordenadas locales), `pictograma(id_, cx, cy, s, col)`, `multitud(id_, x0, x1, base, n, s)`.

## objetos/politica.py (solo partidos ficticios)
- `PARTIDOS` [(nombre, color, forma)]: ESTRELLA #FFC83D star · CÍRCULO #2EC4B6 circle · TRIÁNGULO #FF7EB6 tri · CUADRADO #C7894B square · ROMBO #9AA3B5 diamond; `COLOR`, `NOMBRE`, `FORMA`
- `icono_partido(forma, cx, cy, s)` · `chip_partido(id_, cx, cy, forma, texto)` · `dhondt(votos, escanos, umbral=0.03, validos)` · `miles(v)` · `colores_reparto(reparto)`
- `urna(id_, cx, base, w, h, texto)` (.puntos["ranura"]) · `sobre(cx, cy, w, h, rot_, id_=)` · `sobre_abierto(id_, cx, cy, w, h, dentro)`
- `papeleta(id_, cx, cy, w, h, forma, tachada)` · `papeleta_congreso(id_, cx, cy, w, h, forma, filas)` (.puntos["filas"]) ·
  `papeleta_senado(id_, cx, cy, w, h, formas, cruces=(0,2))` (cruces en `<id>_c1…`, .puntos["casillas"])
- `sobre_certificado(id_, cx, cy, w, h, rot_)` · `dni(id_, cx, cy, w, rot_)` · `saca(id_, cx, base, w, h)`
- `hemiciclo(id_, cx, cy, n, filas, r0, r1, colores, r_esc, ids=False)` (escaños `<id>_e<i>`, .puntos["escanos"]) · `posiciones_hemiciclo(...)`
- `calendario(id_, cx, cy, w, h, "NOV", "29")` · `atril(id_, cx, base, w, h, mic, frontal)` · `logo_generico(cx, cy, r, "D21")` · `placa(cx, cy, w, h, "ABC")`
- `documento(id_, cx, cy, w, h, titulo, sub)` · `carpeta(id_, cx, cy, w, h, texto)` · `boli(id_, cx, cy, L, rot_)` · `garabato(id_, x0, x1, yc, amp)` · `candado(id_, cx, cy, s)`
- `sin_posicionarnos(id_, cx, cy, size)` — sello obligatorio de la escena 1 de política.

## objetos/casa.py
`vaso(id_, cx, base, alto, ancho, nivel, liquido="agua|refresco|cola|leche|zumo|cafe", cubitos=0..3)` (ids `_liquido`, `_burbujas`, `_cubo<i>`) ·
`cubito(id_, cx, cy, s, ang)` · `grieta(id_, p0, p1, amp)` · `botella(id_, cx, base, alto, col, etiqueta_col, texto)` · `taza(id_, cx, base, w, liquido)` (`_vapor`) ·
`mesa(id_, cx, y_tablero, w, alto)` · `ventana(id_, cx, cy, w, h, cortinas, noche)` · `movil(id_, cx, cy, w, pantalla=svg)` (.puntos["pantalla"]) ·
`reloj(id_, cx, cy, r, hora, minuto)` (`_horaria`, `_minutero`; para girarlas dibújalas a las 12:00 y usa spin/move rotate) · `bombilla(id_, cx, cy, s, encendida)` ·
`casita(id_, cx, base, w)` · `etiqueta_precio(id_, cx, cy, w, h, "19 €", tachado="40 €")` · `bolsa(id_, cx, base, w, h, col, texto)` ·
`caja_madera(id_, x0, yb, w, h)` · `llave_allen(id_, x, y, s, ang)` · `tornillo(id_, x, y, s, ang)` ·
`sofa(id_, cx, base, w, asiento, col, respaldo)` (.puntos asiento/izq/der) · `banco(id_, cx, base, w, asiento)` (parque) ·
`cronometro(id_, cx, cy, r, col)` (aguja `_aguja` a las 12: `{"effect":"move","rotate":300,"origin":"bottom","dur":2}`) ·
`pizarra(id_, cx, cy, w, h, contenido)` · `zapato_arriba(id_, cx, cy, s, col, espejo)` + `huella(id_, cx, cy, s, espejo)` (ponerse en el lugar del otro) ·
`portapapeles(id_, cx, cy, w, h, filas, marcadas)` (✓ en `_c<i>`)

## objetos/cuerpo.py
`cerebro(id_, cx, cy, s, hipotalamo=True)` (`_hipotalamo`; .puntos hipotalamo/cerebelo/frente) · `cabeza_perfil(id_, x, y, s, piel, con_cerebro)` ·
`musculo(id_, cx, cy, largo, grosor, contraido)` · `antebrazo(id_, p0, p1, ancho, piel, vello, gallina, manga)` (`_vello`, `_erizado`, `_bultos`) ·
`piel_lupa(cx, cy, r, erizado)` (contenido para `lupa`) · `termometro(id_, cx, top, h, nivel, col, texto)` (`_columna`)

## objetos/animales.py
`perro(id_, cx, base, s, pelaje="labrador|chocolate|negro|blanco", collar, bostezo=True)` — sentado de frente, alto ≈ 430*s; ids `_cabeza`, `_cola` (sway origin bottom-left),
`_ojos` / `_ojos_cerrados`, `_boca` (bocaza con lengua enroscada: `grow` origin top), `_orejas` · `icono_perro(id_, cx, cy, s, col)` (cabeza para cuadrículas: gris/dorado)

## objetos/escenarios.py (fondos sin ids; W, H ajustables, por defecto 1080×1920)
`habitacion(pared, ventana_, cuadro, noche)` · `cocina()` · `oficina()` · `escenario(foco_x)` (cortinas + foco + tarima) ·
`cielo(hora="dia|tarde|noche", colinas, nubes)` · `sol(id_, cx, cy, r)` (`_rayos`) · `rotonda(cx=540, cy=880, r_isla, r_ext)` ·
`coche_aereo(id_, x, y, rumbo, color="rojo|blanco|amarillo|azul|verde", intermitente="der")` (`_inter`) · `carriles_rotonda()` ·
`punto_en_anillo(cx, cy, r, ang)` → (x, y, rumbo) · `arbol_aereo(x, y, r)` · `edificio_aereo(x, y, w, h)`

## Lo que ya hace el motor Remotion (no se dibuja)
- **Fondo**: azul `#2347FF` con cuadrícula milimetrada que se desplaza despacio + viñeteado (`Background.tsx`).
- **Titular**: `headline` con `*palabra*` en bloque lima, y `number` grande al lado (`Headline.tsx`). 2-6 palabras.
- **Barra de capítulos** arriba (`["?","1","2","3","+","TÚ"]`) y fuente (`source`) (`ProgressBar.tsx`); barrido lima diagonal al cambiar de capítulo.
- **Subtítulos** palabra a palabra en grupos de ≤4 (`Captions.tsx`), zona y 1350-1480.
- **Viñeta** de la ilustración: `panel` (recuadro blanco con borde y sombra, rótulo `caption` «Fig. N · …» arriba a la izquierda),
  `free` (sin recuadro), `full` (pantalla completa con velos oscuros arriba y abajo). Entrada: pop/escala; salida: fundido.
  Cámara: zooms (`target: camera`) + avance documental ×1,045 automático.
- **Animaciones** de ids: entradas pop, fade, draw, grow, slide-left/right/up/down; bucles float, bob, sway, spin, pulse, shake, wiggle, flow,
  blink, ripple, breathe, drift; acciones move, hide, punch; `origin`, `phase`, `amount`, `dur`, `trigger`/`delay`, `sfx`.
- **Mascota** (matraz): `"mascot": {"trigger", "pose": idle|point|wave|think|surprise|explain|cheer, "note", "side"}` — 1-2 cameos por vídeo.
- **Tarjetas** (`elements`, todas con `trigger` y `sfx`): `stat` (número que cuenta: value, from, decimals, unit, prefix, note), `fact` (texto, tone paper|accent|ink),
  `icon`, `compare` (barras con rows), `dots`, `list` (items con trigger), `scale` (from→to con progress), `tag` (accent|ink|hot), `stamp` (golpe: MITO, FALSO…),
  `quiz`, y las del cierre `trick`, `follow`, `ask`. Con ilustración, máx. 1 tarjeta pequeña (tag, stamp o stat).
- **Cierre** (capítulo 5 «TÚ», 2 escenas, sin dibujo): (1) «Tú traes las dudas y nosotros te damos el truco.», headline «Dudas → *truco*»,
  `{"type":"trick","trigger":"Tú","reveal_trigger":"nosotros"}` (4 variantes que rotan solas); (2) «Síguenos y las resolvemos. <pregunta>»,
  `follow` + `ask`. Luego el outro «Todo tiene un truco» y la portada (no tocar).
- **Sonido**: voz Edge TTS +25 %, música con ducking y efectos (`sfx`) automáticos por tipo de elemento.

## Procedencia (scripts temporales del scratchpad que se han rescatado)
lote5/pol.py, lote5/d/partidos.py, voto-correo/vc.py, voto-blanco/vb.py, papeleta-nula/pn.py y senado.py, nuevo-partido/np.py y gancho.py,
vox/vx.py, escalofrios/persona.py y cerebro.py, lote3-04/brazo.py, lote4-01-bebe-carrito/dib.py, hielo-cruje/hc.py y vaso.py,
black-friday/bf.py, ikea/lib.py, rotondas/rot.py, cielo/paisaje.py y atardecer.py, lib.py (utilidades).
lote7-03-bostezo (sistema nuevo): bostezo + mano a la boca + gafas de sol en personajes, animales.py, sofá, banco, cronómetro, pizarra, zapatos/huella, portapapeles y bandera.

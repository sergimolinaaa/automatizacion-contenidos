# Librería de piezas de «El truco es…»

Monta cada vídeo **combinando piezas** y dibuja solo lo específico del tema. Python 3 sin dependencias; cada función
devuelve una cadena SVG (o `Pieza`: cadena con `.puntos` = anclajes en coordenadas finales y `.caja` = (x0, y0, x1, y1)).
Estilo pegatina realista: contorno tinta `#0B0B14` 6-9 px, degradados claro→oscuro, brillo blanco arriba, sombra suave.

- `svg/base.py` — paleta, documento, etiquetas, flechas, globos, sellos, iconos, contadores, efectos.
- `svg/personajes.py` — personaje paramétrico (edad, pelo, piel, ropa, accesorios, expresión, pose, brazos).
- `svg/objetos/politica.py · casa.py · frio.py · compra.py · reptiles.py · cuerpo.py · escenarios.py · animales.py · tienda.py · coches.py · tecnologia.py · memoria.py` — piezas por tema ya aprobadas.
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
- `pose`: de_pie, sentado (con `silla=True` dibuja la silla), busto · `brazos`: abajo, cintura, arriba, saluda, senala, barbilla, **boca** (mano tapando el bostezo, por delante de la cara), coge, cruzados,
  **relajado** (codo algo doblado: mejor que «abajo», menos rígido), **explica** (antebrazo adelante, palma abierta), **apunta_arriba** (índice al cielo), **sujeta** (puño a la altura del hombro),
  **junta** (manos delante de la tripa; con `("junta", "junta")` dibuja los dedos entrelazados en `{id}_manos` y `.puntos["manos"]`: punch al crujirse los nudillos)
- Que no parezcan estatuas: mezcla poses distintas en cada brazo y usa la receta «Persona natural» de `recetas.md` (breathe + blink + sway suave del cuerpo + gesto con move/wiggle).
- Sentado: el asiento queda a `128*escala` (adulto) / `63*escala` (niño) sobre `y`; úsalo con `casa.sofa(asiento=...)` / `casa.banco(asiento=...)`.
- Cambiar solo la cara: dibuja dos `persona()` iguales con distinta `expresion` en el mismo sitio y alterna `hide` + `fade` (`dur` 0.15) con el mismo trigger.
- Ids: `{id}`, `{id}_cuerpo`, `{id}_piernas`, `{id}_cabeza`, `{id}_ojos`, `{id}_cejas`, `{id}_boca`, `{id}_brazo_izq`, `{id}_brazo_der`,
  `{id}_mano_izq/der`, `{id}_acc_<accesorio>` (izq/der = lado de la pantalla).
- `.puntos`: cabeza, boca, ojos, cima, pies, mano_izq, mano_der, hombro_izq, hombro_der, alto.
- También: `manos_entrelazadas(id_, cx, cy, s, piel)` (sueltas, ≈ 230×150; `_nudillos`), `cabeza(id_, rx, ry, hy, …)` (solo la cabeza, coordenadas locales), `pictograma(id_, cx, cy, s, col)`, `multitud(id_, x0, x1, base, n, s)`.

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
- Investidura: `corona(id_, cx, base, w)` (corona real genérica; `_joyas` pulse; ponla en `persona.puntos["cima"][1] + 0.16*w`) ·
  `capa_escanos(id_, puntos, n, col, r, grupos=4, desde=0)` (pinta n escaños de un `hemiciclo()` de izquierda a derecha en capas `id_0…` para que se llenen en cascada: 176 síes de 350)
- Mesas electorales: `carta_notificacion(id_, cx, cy, w, h, titulo, cargo, fecha, remite)` (sobre con hoja que sale: move `{id}_hoja` [0,-h*0.55]; `{id}_cargo`) ·
  `calendario_plazos(id_, cx, cy, n=7, cw, ch, titulo)` (casillas `_d<i>`, marca de día gastado `_m<i>` para pop en cascada) ·
  `formulario(id_, cx, cy, w, h, titulo, sub, filas)` (✓ en `_c<i>`, firma `_firma` para draw) · `bombo(id_, cx, cy, r, texto, bola_txt)` (`_jaula`/`_manivela` spin, `_bola` move) ·
  `mesa_electoral(id_, cx, y_tablero, w, alto, cartel, urna_dx)` (mantel, cartel, urna; personas `pose="busto"` antes para que la mesa las tape) ·
  `colegio_electoral(W, H, suelo_y, rotulo)` (fondo: aula con pizarra, ventanales, cabina con cortina y suelo de baldosas)

## objetos/territorio.py (mapa, balanza y ciudad frente a pueblo)
`mapa_espana(id_, cx, cy, w, puntos, ids, destacar=("Madrid","Soria"))` (Península, Portugal en gris, Baleares, Ceuta, Melilla y recuadro de Canarias; capitales en `_puntos`,
con `ids=True` cada una en `_p_<slug>`; las de `destacar` van aparte en `_<slug>` en coral; .puntos[nombre] = (x, y), `CAPITALES`) ·
`balanza(id_, cx, base, w, inclina, izq=svg, der=svg, txt_izq, txt_der)` (dos platillos; contenido en coordenadas del platillo; para inclinarla, dos balanzas + hide/fade;
.puntos plato_izq/plato_der/fiel) · `ciudad(id_, x0, x1, base, alto, n)` (rascacielos `_t<i>` para grow en cascada) · `pueblo(id_, cx, base, w)` (casas de piedra `_c<i>` y `_iglesia`)

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
`portapapeles(id_, cx, cy, w, h, filas, marcadas)` (✓ en `_c<i>`) · `trofeo(id_, cx, base, h, texto, col)` (copa dorada con placa; `_brillo`) ·
`nivel_burbuja(id_, cx, cy, w, h, col, inclinado)` (burbuja en `_burbuja`: move horizontal) · `red_ventana(id_, x, y, w, h, paso)` (malla protectora para ventanas y balcones; fade)

## objetos/cuerpo.py
`cerebro(id_, cx, cy, s, hipotalamo=True)` (`_hipotalamo`; .puntos hipotalamo/cerebelo/frente) · `cabeza_perfil(id_, x, y, s, piel, con_cerebro)` ·
`musculo(id_, cx, cy, largo, grosor, contraido)` · `antebrazo(id_, p0, p1, ancho, piel, vello, gallina, manga)` (`_vello`, `_erizado`, `_bultos`) ·
`piel_lupa(cx, cy, r, erizado)` (contenido para `lupa`) · `termometro(id_, cx, top, h, nivel, col, texto)` (`_columna`) ·
`articulacion(id_, cx, cy, s, abierta=0, burbuja=False, gas=True)` (nudillo en corte ≈ 780×350: `_hueso`, `_falange` (move [60,0] = separar, unidades locales),
`_liquido` (sinovial), `_capsula`, `_gas`, `_burbuja`; .puntos hueco/burbuja/hueso/falange/liquido) · `mano(id_, cx, cy, s, piel, espejo)` (mano abierta de frente,
dedos arriba ≈ 260×360: `_dedos`, `_pulgar`, `_nudillos`; .puntos nudillos/puntas/muneca) · `escaner_resonancia(id_, cx, cy, w, texto="RM")` (`_anillo`, `_pantalla`; .puntos hueco/camilla) ·
`oido_interno(id_, cx, cy, s)` (laberinto ≈ 380×330: canales semicirculares `_canales`, líquido `_liquido` (wiggle), `_caracol`, `_vestibulo`; cabe en una `lupa` con s≈0.6)

## objetos/animales.py
`perro(id_, cx, base, s, pelaje="labrador|chocolate|negro|blanco", collar, bostezo=True)` — sentado de frente, alto ≈ 430*s; ids `_cabeza`, `_cola` (sway origin bottom-left),
`_ojos` / `_ojos_cerrados`, `_boca` (bocaza con lengua enroscada: `grow` origin top), `_orejas` · `icono_perro(id_, cx, cy, s, col)` (cabeza para cuadrículas: gris/dorado)
`gato(id_, cx, cy, s, pelaje="naranja|gris|negro|blanco", giro_del, giro_tras, doblez, patas="normal|encogidas|estiradas", cola, rot_, expresion="normal|susto|feliz", cria, espejo)` — de perfil (morro a la derecha), (cx, cy) = cintura, suelo en cy+165*s;
cada mitad gira sobre la columna (0 = patas abajo, 180 = boca arriba) y `doblez` lo dobla en V: fotogramas de la caída en el aire. Ids `_cabeza`, `_ojos` (blink), `_cola` (sway origin bottom-right)

## objetos/vuelo.py (propulsión, «coches que vuelan», acción y reacción)
`roadster(id_, cx, base, s, col="rojo|blanco|negro", toberas=None|"abajo"|"atras", logo=True, rot_)` (deportivo de perfil, morro a la derecha; .puntos toberas/centro/morro/cola; `_ruedas`, `_faro`) ·
`chorro(id_, x, y, largo, ancho, ang)` (aire a presión; 90 = abajo, 180 = izquierda; `_lineas` para flow, `_soplos`) · `deposito_aire(id_, cx, cy, w, h, nivel)` (bombona con moléculas `_moleculas` y manómetro `_aguja`) ·
`rampa(id_, x0, x1, base, alto)` · `avion(id_, cx, cy, s)` (`_ala`) · `globo_aire(id_, cx, cy, r, ang)` (.puntos boquilla) · `extintor(id_, cx, base, h)` (.puntos boquilla) ·
`pesa(id_, cx, base, w, "KG")` · `logo_tesla(id_, cx, cy, r)` (pegatina simplificada) · `pista_pruebas(W, H, suelo_y)` (fondo: atardecer, mesetas, arena y asfalto)

## objetos/tienda.py (consumo, súper, precios)
`cartel_precio(id_, cx, cy, w, entero="9", cent="99", moneda="€", col, cinta=None)` (cartel del lineal: entero grande + céntimos pequeños; sub-ids `_entero`, `_cent`; `cent=None` → «10 €»; .puntos entero/cent) ·
`producto(tipo="caja|bote|botella|lata|brick", cx, base, s, col)` · `estanteria(id_, x0, x1, top, baldas, alto, seed, col)` (.puntos["baldas"] = y de cada balda para colgar precios) ·
`carrito(id_, cx, base, w, col, lleno, espejo)` (`_compra`, `_ruedas`; .puntos asa/cesta; con `espejo=True` el asa queda a la izquierda, junto a `persona(brazos=(…, "coge"))`) ·
`ticket(id_, cx, top, w, lineas=[(concepto, precio)], total, titulo)` (`_l<i>`, `_total` para cascada) ·
`recta_numerica(id_, x0, x1, y, a, b, paso, etiquetas)` · `billete(id_, cx, cy, w, valor="50", rot_)` (billete de euro estilizado, color por valor; `_cifra`) (.puntos["x"](valor) → x, para poner marcadores) · `supermercado(W, H, suelo_y, seed, rotulo)` (fondo: pasillo con estantería llena y suelo de baldosas)

## objetos/coches.py (coches, motor y física del giro)
`deportivo_lateral(id_, cx, base, s, col="rojo", motor="centro|delante|detras", corte=True, logo=False, piloto=True, aleron=True)` (superdeportivo genérico de perfil
mirando a la izquierda, ≈ 920×230 a s=1; `corte` = rayos X con piloto, asiento y motor; sub-ids `_carroceria`, `_motor`, `_piloto`, `_rueda_del`, `_rueda_tras` (spin), `_cg`;
.puntos eje_del/eje_tras/motor/cg/piloto/morro/cola/techo/maletero) · `deportivo_cenital(id_, cx, cy, s, col, motor, cg, rumbo)` (desde arriba, motor bajo tapa de cristal,
`_motor`, `_cg`; para girarlo `{"effect":"move","rotate":35}`) · `motor_bloque(id_, cx, cy, w, h)` · `centro_gravedad(id_, cx, cy, r)` (símbolo a cuartos) ·
`escudo_porsche(id_, cx, cy, s)` (escudo simplificado estilo pegatina, ≈ 200×240) · `persona_cenital(id_, cx, cy, s, brazos="estirados|pegados", bolsas)` (`_brazos`; spin para girar) ·
`flecha_giro(id_, cx, cy, r, a0, a1, col)` (flecha en arco) · `maleta(id_, cx, base, w, h)` · `marcas_derrape(id_, p0, p1, ctrl)` (draw) ·
fondos `sala_presentacion(W, H, suelo_y)`, `carretera(W, H, y0, y1)`, `pista_hielo(W, H, y0)`.

## objetos/tecnologia.py (móviles, batería, almacenamiento)
`pantalla_movil(cx, cy, w)` → caja de la pantalla de `casa.movil()` para preparar su contenido · `bateria(id_, cx, cy, w, h, nivel, col, rayo, gastada, texto)` (pila de litio vertical;
`gastada=True` hinchada y amarillenta; `_carga` grow, `_rayo` pulse; .puntos borne/centro/base) · `chip(id_, cx, cy, s, "CPU")` (procesador con patillas, `_nucleo` pulse) ·
`logo_apple(id_, cx, cy, s)` (manzana mordida, pegatina) · `icono_app(id_, cx, cy, s, col, glifo="play|chat|foto|mapa|nota|juego|camara|estrella")` ·
`barra_almacenamiento(id_, x, y, w, h, frac, col, texto)` (`_lleno`) · pantallas para `movil(pantalla=…)`: `pantalla_cargando` (icono + rueda `{id}_rueda` spin),
`pantalla_almacenamiento` (casi lleno: `{id}_barra`, `{id}_aviso`), `pantalla_salud` (salud de la batería, `{id}_pct`) · `papelera(id_, cx, base, w)` (`_tapa`) ·
`armario(id_, cx, base, w, h, lleno, abierto)` (a reventar, ropa asomando en `_ropa`: shake/wiggle)

## objetos/compra.py (la compra: leche, pan, caprichos, reparto en frío)
`brick_leche(id_, cx, base, s, col, texto="LECHE", rot_)` (brik de 1 L con techo a dos aguas, ≈ 110×235 a s=1; `_gota`; .puntos tapon/centro/base) ·
`nevera(id_, x0, top, w, h, puertas, baldas, rotulo="LÁCTEOS")` (nevera de súper con puertas de cristal y briks; `_luz` (pulse), `_briks`, `_rotulo`) ·
`ancla(id_, cx, cy, s, col)` · `cana_pescar(id_, mango, punta, sedal)` (.puntos anzuelo; `_sedal`) · `galletas(id_, cx, cy, s, col, texto, rot_)` ·
`chocolate(id_, cx, cy, s, rot_, col)` · `lista_compra(id_, cx, cy, w, h, items, tachadas, titulo)` (tachones `_t<i>` para draw, líneas `_i<i>`) ·
`barra_pan(id_, cx, cy, L, rot_)` · `horno_pan(id_, cx, base, w, h)` (`_vapor` float, `_fuego` pulse, `_barras`) ·
`camion_frigorifico(id_, cx, base, s, espejo)` (cabina a la izquierda; `_ruedas`, `_frio`; .puntos trasera/cabina; para que llegue marcha atrás: slide-right) ·
`carretilla(id_, x, base, s, cajas)` (diablo con cajas; .puntos asa: alto del asa = 286*s) · `caja_carton(cx, base, w, h, texto)` · `palet(id_, cx, base, w, filas)`.
Truco: regla o barra que se alarga en horizontal = grupo dibujado en vertical dentro de un `<g transform="rotate(-90)">` + `grow` con origin top (ver archivo/leche-fondo).

## objetos/piel.py (piel, picaduras y bichos)
`piel_corte(id_, x0, y0, w, h, vaso, pelos, grasa)` (epidermis, dermis, vaso con glóbulos `_globulos` para drift, grasa; .puntos sup/vaso/dermis) ·
`habon(id_, cx, base, w, h, corte, herida, arriba)` (bulto rojo: grow origin bottom; `arriba=True` mancha redonda; `_herida` para draw) · `rayitas_picor(id_, cx, cy, r, n)` ·
`mosquito(id_, cx, cy, s, ang)` (mosquito tigre, `_alas` pulse; .puntos trompa/cabeza) · `gota_saliva(id_, cx, cy, r)` · `mastocito(id_, cx, cy, r)` (célula de defensa, `_granulos`, `_ojos`) ·
`histamina(id_, cx, cy, r, n)` · `sirena(id_, cx, base, s)` (`_luz` spin) · `bacteria(id_, cx, cy, s, ang)` · `raton_lab(id_, cx, base, s)` (`_pata` wiggle) ·
`mano_rasca(id_, cx, cy, s, piel, manga)` (uñas rascando: shake) · `reloj_arena(id_, cx, cy, h)` (`_abajo` grow, `_chorro`) ·
`gorra(id_, cx, cy, r, col)` y `delantal(id_, x, y, escala, edad, col, busto)` (encima de persona(), en su mismo grupo) · fondo `piscina(W, H, agua_y0, agua_y1)`.

## objetos/frio.py (frío y calor en casa: congelador, helado, convección)
`congelador(id_, cx, base, w, h, baldas, puerta, escarcha, rotulo)` (vertical abierto con baldas de rejilla y escarcha; `_puerta`, `_frio` (drift), `_luz` (pulse);
.puntos baldas (y de cada balda)/interior/centro) · `cuenco(id_, cx, base, w, estado="liquido|helado", vapor)` (`_vapor`) · `vapor_subiendo(id_, cx, y, w, alto, n)` (float) ·
`escarcha(id_, x0, x1, y, grosor, derretida)` (picos blancos o charquito: hide + fade para «derretir») · `corrientes(id_, cx, cy, w, h)` (bucles de convección: draw + flow) ·
`burbujas_gas(id_, cx, y0, y1, w, n, texto)` · `grafica_enfriamiento(id_, x0, y0, w, h, curvas=[(id, [(t, °C)], col, rótulo)])` (curvas en su id para draw, rótulo `_r`, línea de 0 °C).

## objetos/aviones.py (aviones y aerodinámica)
`jumbo(id_, cx, cy, s, franja, rot_)` (747 de cuatro motores de perfil, morro a la derecha, ≈ 1000×450 a s=1; `_motores`, `_ventanillas`, `_ala`; .puntos morro/cola/ala/ventanilla/tren) ·
`perfil_ala(id_, cx, cy, L, ang, t, m, curva=True)` (corte NACA del ala; `ang` = ángulo de ataque, positivo morro arriba; `_curva` lima para draw; .puntos ataque/salida/arriba/abajo/sup/inf) ·
`lineas_corriente(id_, ala, x0, x1, arriba, abajo, bajada)` (aire que rodea el ala y sale desviado hacia abajo; `_l<i>` para draw escalonado, flow) ·
`signo_presion(id_, cx, cy, r, "+"|"-")` · `cochecito(id_, cx, base, s, col)` (turismo pequeño para pilas) · `manzana(id_, cx, cy, r)` ·
`retrato_newton(id_, cx, cy, s)` (marco ovalado con placa; persona en `{id}_p`) · `pista_despegue(id_, W, H, horizonte)` (pista en perspectiva, `_marcas`) · fondo `aula(W, H, suelo_y)`.
Truco: para que el ala «se incline», dibújala a 0° y anímala con `move` `rotate` (origin center); las líneas de corriente se calculan con otro `perfil_ala` ya inclinado.

## objetos/dinero.py (hipotecas, bancos, BCE)
`banco(id_, cx, base, w, rotulo, col_friso, euro, ue)` (fachada clásica con columnas y frontón con € o estrellas UE; `_puerta`; .puntos puerta/rotulo/cima/izq/der) · `torre_bce(id_, cx, base, h, rotulo)` (torres de cristal del BCE, `_luces` pulse) · `estrellas_ue(id_, cx, cy, r)` · `bandera_ue(id_, cx, cy, w, h)` · `moneda_euro(id_, cx, cy, r)` · `ficha(id_, cx, cy, w, h, titulo, sub, col, fg)` (bloque grueso para fórmulas: «EURÍBOR» + «DIFERENCIAL») · `recibo_hipoteca(id_, cx, cy, w, h, titulo, banco_txt, concepto)` (carta del banco con casilla vacía en .puntos["cifra"] para cifras con hide/pop) · `palanca(id_, cx, base, h, texto)` (mando con `_mango`: move rotate ±25 origin bottom).

## objetos/tiempo.py (horas, sueño, cambio de hora)
`cama(id_, cx, base, w, col)` → (detras, delante): cabecero y almohada / edredón (`{id}_manta`); entre medias una `persona(pose="busto")` en `detras.puntos["persona"]` (varias en el mismo sitio con distinta cara para hide/fade) ·
`mesilla(id_, cx, base, w, h)` (.puntos tablero) · `despertador(id_, cx, base, w, texto="3:00", col_txt)` (digital; dos en el mismo sitio + hide/pop para cambiar la hora; `_hora`) ·
`luna(id_, cx, cy, r)` · `flecha_atras(id_, cx, cy, r, a0, a1)` (arco antihorario alrededor de `casa.reloj`: «retrasar la hora», para draw; las agujas: `move rotate -360` origin bottom en `_minutero` y `-30` origin left en `_horaria` si está a las 3).

## objetos/escenarios.py (fondos sin ids; W, H ajustables, por defecto 1080×1920)
`habitacion(pared, ventana_, cuadro, noche)` · `cocina()` · `oficina()` · `escenario(foco_x)` (cortinas + foco + tarima) ·
`cielo(hora="dia|tarde|noche", colinas, nubes)` · `sol(id_, cx, cy, r)` (`_rayos`) · `rotonda(cx=540, cy=880, r_isla, r_ext)` ·
`coche_aereo(id_, x, y, rumbo, color="rojo|blanco|amarillo|azul|verde", intermitente="der")` (`_inter`) · `carriles_rotonda()` ·
`punto_en_anillo(cx, cy, r, ang)` → (x, y, rumbo) · `arbol_aereo(x, y, r)` · `edificio_aereo(x, y, w, h)`

## objetos/memoria.py (memoria, psicología cotidiana, «cambiar de habitación»)
`puerta(id_, cx, base, w, h, estado="abierta|cerrada|ambas", placa=None, luz=True, marco)` (puerta de madera de frente con luz de la otra habitación; `_hoja` abierta, `_cerrada` para «cerrar la puerta» con hide/pop, `_placa` dorada; .puntos hueco/pomo/placa/suelo) ·
`tijeras(id_, cx, cy, s, rot_, col)` · `caja_colores(id_, cx, cy, w, h, col, lazo, borrosa)` (borrosa = recuerdo desvaído) · `bocadillo_piensa(id_, cx, cy, w, h, contenido=svg, cola)` (nube de pensamiento con DIBUJO dentro; `_nube`, `_burbujas`) ·
`humo(id_, cx, cy, s)` («se deshace en humo») · `gota_esfuerzo(id_, cx, cy, s)` · `mando_consola(id_, cx, cy, s)` · `sala_pixel(x0, y0, w, h, px)` (fondo de videojuego) + `bloque_pixel(cx, base, w, h, col)` + `avatar_pixel(id_, cx, base, px)` ·
`tele_antigua(id_, cx, base, w, texto, patas)` (`_pantalla`) · `tira_pelicula(id_, x0, cy, [f(cx, cy, w, h)…], fw, fh, sep)` (fotogramas `_f<i>`, números `_n<i>`, cortes `_corte<i>` para draw; .puntos corte<i> = x) ·
`edificio_cupula(id_, cx, base, w)` (universidad clásica con cúpula dorada) · `archivador(id_, cx, base, w, h, etiqueta=(l1, l2))` (`_carpeta`; .puntos carpeta/asa) · `birrete(id_, cx, cy, s)` (graduado; cy = base del gorro, pon `persona.puntos["cima"]` + 38*s)

## objetos/reptiles.py (basilisco, pisada sobre el agua, revista científica, río en la selva)
`basilisco(id_, cx, cy, s, pose="a|b", espejo, rot_)` (lagarto Jesucristo corriendo a dos patas, morro a la derecha; (cx, cy) = cadera, pie apoyado en cy+150*s;
alterna pose a/b con hide/fade para que corra; `_cola`, `_cabeza`, `_ojos`, `_cresta`, `_brazos`, `_pata_apoyo`, `_pata_aire`; .puntos pie/cabeza/ojo/cola/agua) ·
`pata_basilisco(id_, cx, cy, s, abiertos)` (planta con dedos en abanico y flecos de escamas `_flecos`; abiertos/plegados para hide/pop; .puntos dedos) ·
`pie_lateral(id_, cx, cy, s, pierna, ang)` (pierna + pie de lado, (cx, cy) = planta) · `bolsa_aire(id_, cx, sup_y, w, h, cierre=0..1)` (cavidad de aire que se cierra) ·
`salpicadura(id_, cx, cy, s)` (corona con gotas) · `agua_corte(x0, x1, sup_y, fondo_y)` (agua en corte, sin id) ·
`revista(id_, cx, cy, w, h, titulo="nature", fecha, contenido)` (portada de revista científica) · fondo `selva_rio(W, H, agua_y)`.

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
lote7-10-tesla-vuela: vuelo.py y brazos relajado/explica/apunta_arriba/sujeta en personajes.
lote7-08-precios-99: tienda.py (cartel_precio, producto, estanteria, carrito, ticket, recta_numerica, supermercado).
lote7-11-nudillos (archivo/nudillos/dib.py): articulación en corte, mano, escáner de resonancia, trofeo, manos entrelazadas y brazos «junta».
lote7-12-mesa-electoral: carta de notificación, calendario de plazos, formulario, bombo, mesa y colegio electoral (politica.py) y billete (tienda.py).
lote7-09-motor-central: coches.py (deportivo en corte y cenital, motor, centro de gravedad, escudo Porsche, persona cenital, flecha de giro, maleta, derrape, sala, carretera, pista de hielo).
lote8-01-movil-lento (archivo/movil-lento/dib.py): tecnologia.py (batería nueva y gastada, chip, logo de Apple, iconos de app, pantallas de móvil, barra de almacenamiento, papelera y armario).
lote7-04-leche-fondo (archivo/leche-fondo/dib.py): compra.py (brik, nevera de lácteos, ancla, caña, galletas, chocolate, lista, pan, horno, camión frigorífico, carretilla, palé).
lote8-06-investidura (archivo/investidura/dib.py): corona y capa_escanos (politica.py).
lote8-02-voto-soria: territorio.py (mapa de España con capitales, balanza, ciudad y pueblo).
lote7-05-picadura (archivo/picadura/dib.py): piel.py (corte de piel, habón, mosquito, mastocito, histamina, sirena, bacteria, ratón, mano rascando, reloj de arena, gorra, delantal, piscina).
lote8-04-agua-caliente (archivo/agua-caliente/dib.py): frio.py (congelador, cuenco de helado, vapor, escarcha, corrientes de convección, burbujas de gas y gráfica de enfriamiento).
lote8-03-gatos-caen: gato de perfil con giro por mitades (animales.py), oído interno (cuerpo.py), nivel de burbuja y red de ventana (casa.py).
lote7-06-puerta-olvido (archivo/puerta-olvido/dib.py): memoria.py (puerta abierta/cerrada con placa, tijeras, caja, bocadillo con dibujo, humo, mando, sala pixelada, tele antigua, tira de película, universidad con cúpula, archivador y birrete).
lote7-07-avion (archivo/avion/dib.py): aviones.py (jumbo, perfil de ala, líneas de corriente, signos de presión, cochecito, manzana, retrato de Newton, pista, aula).
lote8-05-hipoteca (archivo/hipoteca/dib.py): dinero.py (banco, torres del BCE, bandera y estrellas UE, moneda, ficha de fórmula, recibo de hipoteca, palanca).
lote8-07-basilisco (archivo/basilisco/dib.py): reptiles.py (basilisco, pata con flecos, pie lateral, bolsa de aire, salpicadura, agua en corte, revista y río en la selva).
lote8-08-cambio-hora (archivo/cambio-hora/dib.py): tiempo.py (cama con persona dentro, mesilla, despertador digital, luna, flecha de retrasar la hora).

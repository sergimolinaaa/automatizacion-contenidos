# «El truco es…» (@eltrucoes): cómo producir vídeos

Cuenta automática de Shorts/Reels/TikTok en español de España: cada vídeo explica «el truco» detrás de algo (ciencia, cuerpo,
psicología, objetos, cocina, animales y reglas de la política actual). Lema: **«Todo tiene un truco»** (nunca «la naturaleza tiene trucos»).

## Reparto del trabajo
- **Claude (sesión)**: escribe `content/<loteN-NN-tema>/guion.json` + sus SVG, revisa y hace commit+push.
- **GitHub Actions**: `render-ejemplo.yml` (al hacer push de `content/**`) pone voz Edge TTS, efectos y renderiza con Remotion;
  `programar.yml` (cron :37) programa en Buffer (YouTube, Instagram, TikTok) **1 al día a las 14 h de Madrid**, máximo 1 por día (`SLOTS` en `autocontent/publish.py`).
  Estado de la cola: `data/publicaciones.json`. Banco de temas: `data/temas.json` (marca `"hecho": true` al subir).

## Qué funciona (datos de la cuenta, oct 2026)
- Lo que habla de «tú»: tu cuerpo, tu mente, tu voto, tu dinero, tu día a día (algo que el espectador ha vivido).
- Elecciones: SOLO cómo funciona el sistema (voto en blanco, escaños, fechas). NUNCA programas ni propuestas de partidos.
- Curiosidades visuales «¿cómo es posible?» (piedras que se mueven, palomitas…).
- Responder preguntas de comentarios (el de los escalofríos rindió muy por encima de la media).
- 1 vídeo al día a las 14:00, el mismo en las 3 redes. Nunca más de uno al día (`publish.py` lo impide).

## Calendario
`data/calendario.json` manda (fecha → tema). Cada vídeo lleva `"publish": {"at": "<fecha>T14:00:00+02:00"}` (+01:00 desde el 25-oct).
Al hacerlo, rellena su `"carpeta"` en el calendario. Si una noticia muy relevante encaja, AVISA al usuario antes de cambiar el calendario.
DOMINGOS («RESPUESTA A COMENTARIO»): el usuario pasa capturas de comentarios (no tenemos acceso a las redes); se elige la pregunta
con más likes que encaje y el vídeo empieza «Respondemos a la pregunta de @usuario…». Si no hay pregunta válida, avisar y proponer tema.

## Guion y textos
- 40-60 s (unas 110-150 palabras), 7-11 escenas. Voz Edge TTS a +25 % (`config.yaml`).
- GANCHO en los 2 primeros segundos: pregunta directa al espectador («¿Por qué…?», «¿Te ha pasado…?»).
- Explica el mecanismo de forma sencilla con un ejemplo cotidiano. Para todos, de 10 a 90 años: cada palabra técnica con
  definición corta o comparación cotidiana. NUNCA decir «El truco es…» en la narración.
- Cierre en 2 escenas (capítulo 5 «TÚ»): (1) "Tú traes las dudas y nosotros te damos el truco.", headline "Dudas → *truco*",
  elements `[{"type":"trick","trigger":"Tú","reveal_trigger":"nosotros"}]`; (2) "Síguenos y las resolvemos. <pregunta que invite a comentar>"
  con `[{"type":"follow","trigger":"Síguenos"},{"type":"ask",...}]`.
- Cada dato verificado con AL MENOS 2 fuentes fiables, citadas en la descripción y en "source".
- `cover.text`: título de portada corto, como búsqueda real («Por qué cruje el hielo»).
- `publish.description` (YouTube) y `publish.caption`: empiezan con la pregunta del título, resumen en 3-4 frases con datos concretos,
  citan las fuentes y acaban con una pregunta. `publish.hashtags`: 3-5 concretos (sin #); `publish.py` añade #eltrucoes.
- SIN GUIONES de ningún tipo en textos, títulos ni descripciones (ni -, ni –, ni —): comas, dos puntos o punto y seguido.
- Triggers = palabras EXACTAS de la narración de esa escena. Mascota: 1-2 cameos, nunca junto a ilustración + tarjetas.
- Política: neutral, escena 1 «Sin posicionarnos: solo cómo funciona.» + sello; partidos ficticios de colores.
- Entrega de cada vídeo: `python3 scripts/entrega.py content/<carpeta>` (genera `entregas/<carpeta>.md`).

## Estilo visual (estética azul: fondo azul con cuadrícula, título blanco con bloques lima, ilustración en viñeta)
- El nivel MÍNIMO es `content/lote3-01-zapatero`. Pegatina realista: degradados, brillos, sombras; 3-4 SVG por vídeo hechos con Python.
- NUNCA un momento vacío: cada frase tiene algo en pantalla que la ilustra. NUNCA más de 3 s sin que algo aparezca, se mueva o cambie.
- Todas las escenas (salvo las 2 del cierre) llevan dibujo; mitad inferior libre para subtítulos; nada solapado ni cortado.
- Layouts `panel` (1000x700), `free` (transparente, vertical) y `full` (1080x1920, lo importante entre y 450-1250). Mínimo 2 free/full.
- Motor: `video/src/components/Illustration.tsx`, tipos en `video/src/types.ts`, reglas de DSL en `SYSTEM` de `autocontent/generate.py`.

## Proceso
1. Toma el siguiente día del calendario (`data/calendario.json`) sin carpeta asignada.
2. Crea la carpeta `content/loteN-NN-tema/` (no renombres carpetas ya subidas: identifican vídeos programados).
3. Revisa un SVG: `bash scripts/shot.sh in.svg out.png`. Revisa el vídeo entero (sin voz, ~3-6 min):
   `python3 scripts/qa_frames.py content/<carpeta> <scratchpad>/qa_<tema>` y mira TODAS las `hoja_N.png`. Corrige y repite (≥2 rondas).
4. Marca el tema `"hecho": true` y sube SOLO esa carpeta:
   `git add content/<carpeta> data/temas.json && git commit -m "…" && git pull --rebase --autostash origin <rama> && git push -u origin <rama>`.
5. Comprueba `data/publicaciones.json`: avisa al usuario solo si hay fallos.

## Ahorro de créditos (límite semanal)
- 1 vídeo por subagente; sin volver a investigar lo que ya está en la pista. Máximo 2 renders de QA por vídeo (el 2º solo si el 1º tiene fallos).
- Reutiliza los scripts de dibujo de vídeos anteriores (urnas, hemiciclo, papeletas…) en vez de empezar de cero.
- El coordinador mira solo las hojas finales; no repite el QA del subagente.

## Errores a evitar
- Un commit en `content/**` dispara render + publicación: no subas borradores. No subas `lote2-03-hielo-flota`/`lote2-04-hipo` (ya publicados).
- NUNCA `git stash pop` a ciegas (hay stashes viejos que no deben aplicarse); usa `pull --rebase --autostash`.
- Zooms de cámara (`"camera"`) que tapan el titular o cortan etiquetas: oculta etiquetas con `hide` o quita el zoom.
- `hide` sin trigger oculta desde el principio de la escena; los `move` se suman; en grupos rotados van en coordenadas locales.
- Vídeos demasiado largos (>60 s): recorta palabras y la escena "+".
- **Secretos**: la clave de Buffer vive solo en el secreto `BUFFER_API_KEY` de GitHub. Nunca la escribas en archivos ni pidas claves por chat.

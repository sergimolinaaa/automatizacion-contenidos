# «El truco es…» (@eltrucoes): cómo producir vídeos

Cuenta automática de Shorts/Reels/TikTok en español de España: cada vídeo explica «el truco» detrás de algo (ciencia, cuerpo,
psicología, objetos, cocina, animales y reglas de la política actual). Lema: **«Todo tiene un truco»** (nunca «la naturaleza tiene trucos»).

## Reparto del trabajo
- **Claude (sesión)**: escribe `content/<loteN-NN-tema>/guion.json` + sus SVG, revisa y hace commit+push.
- **GitHub Actions**: `render-ejemplo.yml` (al hacer push de `content/**`) pone voz Edge TTS, efectos y renderiza con Remotion;
  `programar.yml` (cron :37) programa en Buffer (YouTube, Instagram, TikTok) **3 al día: 9, 14 y 21 h de Madrid** (`SLOTS` en `autocontent/publish.py`).
  Estado de la cola: `data/publicaciones.json`. Banco de temas: `data/temas.json` (marca `"hecho": true` al subir).

## Fórmula y estructura (el nivel MÍNIMO es `content/lote3-01-zapatero`; cópialo como plantilla)
- Reglas completas de guion, ilustración y DSL de animación: constante `SYSTEM` en `autocontent/generate.py`. Motor: `video/src/components/Illustration.tsx`, tipos en `video/src/types.ts`.
- guion.json: topic, categoria, title, source (fuentes reales), chapters `["?","1","2","3","+","TÚ"]`, outro_cta, cover, publish, scenes.
- 9-12 escenas, **135-150 palabras** (40-55 s), frases cortas. Escena 1 = firma `{"chapter":0,"signature":true,"headline":"El truco es…","narration":"El truco es…"}`.
- Final (capítulo 5 «TÚ», sin mascota): narración `"Síguenos para más trucos. <UNA pregunta corta y graciosa>"`,
  elements `[{"type":"follow","trigger":"Síguenos"},{"type":"ask","text":"¿… *clave* …?","trigger":"<1ª palabra de la pregunta>"}]`.
- Triggers = palabras EXACTAS de la narración de esa escena. Solo datos verdaderos y verificables (WebSearch si dudas).
- Mascota (matraz): 1-2 cameos graciosos, nunca junto a ilustración + tarjetas.

## Estilo visual
- Pegatina realista: degradados, brillos, sombras, anatomía/física correctas; 3-4 SVG por vídeo generados con un script Python que calcula coordenadas.
- TODAS las escenas (salvo firma y final) llevan dibujo; la mitad inferior queda libre para subtítulos; nada solapado ni cortado.
- Varía `illustration.layout`: `panel` (1000x700, nada importante fuera de y 45-655, esquina 0-340×0-70 reservada a «Fig.»),
  `free` (transparente, vertical, height 800-900) y `full` (1080x1920, lo importante entre y 450-1250). Mínimo 2 free/full por vídeo.
- 6-12 anims por escena (pop/fade/grow/slide/draw, move, hide con trigger, bucles): algo nuevo cada 1-1,5 s.
- Portada: no tocar (va al final, sin bocadillo).

## Política actual (categoría "politica")
Solo el mecanismo (D'Hondt, decreto ley, fechas…) con fuentes oficiales (Constitución, LOREG, BOE, INE); fechas y cifras comprobadas el mismo día.
Elecciones generales del **29-N** (RD 806/2026): 1 vídeo de política al día + 2 de otros temas. Gancho llamativo ligado al 29-N
(«Votar en blanco no hace lo que crees», «¿Votar por correo es seguro?»), adaptado al formato, nunca copiado.
Sin opinión, sin partidos ni políticos reales (nada de «si votas a X esto proponen»), sin caricaturas: partidos ficticios de colores. **Obligatorio**: tras la firma,
narración «Sin posicionarnos: solo cómo funciona.» + sello visible «SIN POSICIONARNOS»; y en cada texto de publicación
«Sin posicionarnos: solo explicamos cómo funciona.».

## Proceso
1. Elige el siguiente tema no hecho de `data/temas.json` (`prioridad` primero; cada día 1 de política y 2 de otras categorías).
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
- Vídeos demasiado largos (>55 s): recorta palabras, no escenas.
- **Secretos**: la clave de Buffer vive solo en el secreto `BUFFER_API_KEY` de GitHub. Nunca la escribas en archivos ni pidas claves por chat.

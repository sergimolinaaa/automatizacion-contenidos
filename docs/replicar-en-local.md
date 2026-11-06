# Cómo replicar «El truco es…» con Claude Code en local (para otra cuenta u otro estilo)

## Lo importante: NO se generan imágenes con IA
Todo es CÓDIGO. Claude no "pinta" imágenes: escribe dibujos vectoriales (SVG) con Python, los anima con
Remotion (React) y los graba a vídeo. Es como hacer un dibujo en Illustrator, pero escrito a mano en texto.

Piezas del sistema (todas en este repo):
| Pieza | Qué es | Dónde |
|---|---|---|
| Dibujos | SVG generados con Python (formas, degradados, personajes por partes con ids) | `libreria/svg/` (base.py, personajes.py, papel.py, objetos/*.py) |
| Animación | Motor Remotion que lee un `guion.json` y anima cada id del SVG (pop, move, sway, squash, pan…) | `video/src/` (Illustration.tsx) |
| Voz | Edge TTS (gratis, voz es-ES) con tiempos por palabra para subtítulos y triggers | `autocontent/voice.py` |
| Montaje | `guion.json` = escenas con narración + SVG + animaciones disparadas por palabras | `content/<carpeta>/` |
| Render | `python scripts/render_example.py content/<carpeta>` → MP4 1080×1920 | `scripts/` |
| Revisión | `python3 scripts/revisar.py content/<carpeta>` (huecos, textos fuera, triggers) | `scripts/revisar.py` |

## Requisitos en tu ordenador
- Node.js 20+ y npm (para Remotion), Python 3.11+, ffmpeg, Chrome/Chromium.
- `git clone` de este repo → `cd video && npm install` → `pip install edge-tts pyyaml requests`.
- Prueba: `python scripts/render_example.py content/lote10-01-frio-bateria` debe dar un MP4 en `output/`.

## Prompt para pegar en Claude Code (terminal)
Copia esto tal cual (cambia lo que está entre <>):

---
Vamos a crear vídeos verticales animados de 40-60 s para una cuenta nueva: <nombre de la cuenta y tema>.
IMPORTANTE: no necesitas generar imágenes con IA. Todo se hace con CÓDIGO, y tú sabes escribir código:
1. Los dibujos son SVG escritos con Python (formas, paths, degradados, grupos con id). Tú los escribes.
2. La animación la hace Remotion leyendo un guion.json que dice qué id del SVG se mueve, cómo y en qué palabra.
3. La voz es Edge TTS (gratis) y el vídeo final lo graba Remotion + ffmpeg.
Este repo ya tiene todo el sistema funcionando para otra cuenta. Úsalo como base:
- Lee primero docs/montaje-rapido.md (guía corta del motor y del DSL de animación) y docs/reglas-visuales.md.
- Mira un ejemplo completo: content/lote10-03-pelo-cancion/guion.json y libreria/archivo/pelo-cancion/dib.py
  (el script Python que genera sus SVG).
- Las piezas reutilizables están en libreria/svg/ (personajes.py, papel.py, objetos/*.py). Índice en libreria/README.md.
Tarea:
a) Crea una carpeta nueva content/<cuenta>-01-<tema>/ con un guion.json de 8-10 escenas (narración en español,
   120-130 palabras, gancho en los 2 primeros segundos) y sus SVG generados con un script dib.py en
   libreria/archivo/<tema>/. Estilo visual: <describe el estilo nuevo: colores, si lleva contorno, personajes…>.
b) Anima cada escena con el DSL (entradas pop/squash, move con antic, sway/breathe en personajes, pan de cámara),
   nunca más de 3 s sin que algo cambie.
c) Comprueba con python3 scripts/revisar.py content/<carpeta> y renderiza con
   python scripts/render_example.py content/<carpeta>. Mira 3 fotogramas del MP4 (ffmpeg) y corrige.
No me digas que no puedes generar imágenes: no hace falta, todo es SVG escrito en código.
---

## Para otra cuenta con OTRO estilo
- Copia el repo (o una rama) y cambia la marca en `video/src/brand.ts` (colores, tipografías, mascota) y
  `video/src/theme.ts` (modo de fondo). El estilo de dibujo se cambia en `libreria/svg/base.py` (paleta, contornos)
  o creando un conversor como `libreria/svg/papel.py` (`a_papel()` transforma cualquier pieza ya hecha).
- NO subas a `content/**` en este repo para la otra cuenta: aquí un push a content publica en Buffer.
  Usa un repo propio para la otra cuenta (o quita los workflows `.github/workflows/programar.yml` y `render-ejemplo.yml`).
- La publicación (Buffer) es opcional: en local puedes renderizar y subir los MP4 a mano.

## Por qué aquí "gasta" y en local no
Aquí cada vídeo lo hace un agente que lee guías, escribe ~10 SVG y revisa fotogramas (150-250k tokens).
En local con tu suscripción de Claude Code el coste es el mismo trabajo, pero contra tu plan del terminal.
Para gastar poco en cualquier sitio: guía corta (docs/montaje-rapido.md), reutilizar piezas de la librería,
1 solo render de prueba y máximo 3 fotogramas mirados.

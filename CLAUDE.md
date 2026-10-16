# «El truco es…» (@eltrucoes): reglas esenciales

Vídeos verticales de 40-60 s (TikTok, Reels, Shorts) que explican el truco de algo que el espectador ha vivido. Lema «Todo tiene un truco».
Empieza SIEMPRE leyendo `estado.md` (qué está guionizado, montado, programado y publicado). No arrastres conversaciones largas.

## Flujo en dos fases
1. **Guiones (1 vez por semana)**: investiga y escribe todos los de la semana en `guiones/semana-AAAA-MM-DD.md`
   (plantilla `guiones/PLANTILLA.md`): fuentes (2 por dato), título de portada, guion, descripción, hashtags y guion visual por frase.
   Reglas: `docs/reglas-guion.md`. Calendario: `data/calendario.json`.
2. **Montaje (por vídeo)**: lee SOLO su guion y `libreria/README.md`. Monta con piezas de `libreria/` y dibuja solo lo específico
   (si una pieza nueva sirve para otros vídeos, guárdala en `libreria/`). No investigues ni reescribas el guion.
   Revisa con `python3 scripts/revisar.py content/<carpeta>`: mira fotogramas SOLO si falla, máximo 3. Reglas: `docs/reglas-visuales.md`.
3. Sube SOLO esa carpeta (un push a `content/**` renderiza con voz en GitHub y programa en Buffer):
   `git add content/<carpeta> … && git commit && git pull --rebase --autostash origin <rama> && git push -u origin <rama>`.
   Genera la ficha `python3 scripts/entrega.py content/<carpeta>` y actualiza `estado.md`.

## Reglas que nunca se rompen
- Calidad de guion, ilustración y animación al nivel de `content/lote3-01-zapatero` y `content/lote6-03-voto-en-blanco`.
- Nunca un momento vacío; nunca más de 3 s sin que algo aparezca, se mueva o cambie.
- 2 vídeos al día, el mismo en las 3 redes: 14:00 el del calendario (`publish.at`) y 21:00 uno extra de `data/temas.json`
  (sin `publish.at`; va a la primera franja libre). `publish.py` impide más de 2 al día.
- Elecciones: solo cómo funciona el sistema, neutral («Sin posicionarnos»), nunca programas de partidos.
- Nunca decir «El truco es…» en la narración. Sin guiones (-, –, —) en ningún texto. Hashtags: 3-5 + #eltrucoes.
- Solo datos verificados con 2 fuentes fiables. Errores típicos: `docs/errores.md`.
- Secretos: la clave de Buffer vive solo en el secreto `BUFFER_API_KEY` de GitHub. Nunca en archivos ni en el chat.
- NUNCA `git stash pop` a ciegas (hay stashes viejos); usa `pull --rebase --autostash`.

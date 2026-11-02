# Encargo común: un vídeo de «El truco es…»

Repo: /home/user/automatizacion-contenidos · rama `claude/busy-cori-ldit11` (trabajas a la vez que otros agentes en otras carpetas).

## Antes de empezar
Lee CLAUDE.md, docs/reglas-guion.md, docs/reglas-visuales.md, docs/errores.md, libreria/README.md y libreria/recetas.md
(sobre todo «Persona natural»). Nivel mínimo: content/lote3-01-zapatero y content/lote6-03-voto-en-blanco.

## Si tu encargo dice «MONTAJE desde guion»
Lee SOLO tu bloque en guiones/semana-2026-10-19.md. No investigues ni reescribas el guion (si se pasa de 135 palabras, recorta lo mínimo).

## Si tu encargo dice «GUION + MONTAJE»
Investiga lo justo con WebSearch: cada dato con 2 fuentes fiables. Gancho en los 2 primeros segundos. Explica el mecanismo con un ejemplo cotidiano.

## Reglas
- 40-60 s reales: 120-135 palabras como máximo. Cifras con unidades dichas con palabras (la voz Edge desalinea «0 a 97 km/h»).
- Cierre fijo en 2 escenas (trick + follow/ask), ver docs/reglas-guion.md.
- Sin guiones (-, –, —) en NINGÚN texto. 3-5 hashtags + #eltrucoes. Nunca decir «El truco es…».
- Nunca más de 3 s sin que algo cambie. Triggers = palabras exactas de la narración de su escena.
- Personas naturales: respiración, balanceo sutil, gestos en palabras clave; nada de brazos rígidos ni mano en la boca.
- Marcas y logos reales permitidos. Estimaciones solo diciendo «no confirmado al 100 %». Política: neutral, solo cómo funciona,
  frase entera «Te lo explicamos sin posicionarnos, …» variada + sello SIN POSICIONARNOS; partidos con nombre y colores reales si salen.
- Usa piezas de libreria/. Piezas nuevas reutilizables: en libreria/ SIN romper lo existente (otros agentes también tocan libreria/).
- `publish.at` EXACTO el que te dan.

## Revisión
`python3 scripts/revisar.py content/<carpeta>` hasta que pase. Fotogramas SOLO si falla, máximo 3.

## Subida (autorizada: es el flujo normal del proyecto)
- `python3 scripts/entrega.py content/<carpeta>`
- NO toques estado.md, data/calendario.json ni data/temas.json (los actualiza el coordinador para evitar conflictos).
- `git add content/<carpeta> entregas/<carpeta>.md` (+ libreria/ si añadiste piezas) → commit cuyo mensaje termine con:
  ```
  Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
  Claude-Session: https://claude.ai/code/session_011MEEHPXUHdPfFa7K7npsRd
  ```
- `git pull --rebase --autostash origin claude/busy-cori-ldit11 && git push -u origin claude/busy-cori-ldit11`
  Si el rebase choca en libreria/ (README u otro), resuelve conservando AMBOS lados. NUNCA `git stash pop`.

## Respuesta final (corta)
Datos con fuentes, palabras, duración estimada, piezas nuevas de librería y hash del commit.

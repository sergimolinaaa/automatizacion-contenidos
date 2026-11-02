# Encargo: MONTAJE desde guion (método rossark, versión corta)

1. Lee SOLO estos tres textos: `CLAUDE.md`, `docs/montaje-rapido.md` y tu bloque de guion
   (`grep -n <carpeta> guiones/semana-*.md`; si no aparece, búscalo por la fecha en `data/calendario.json`).
   No leas la skill rossark, ni los vídeos de referencia, ni `video/src/components/Illustration.tsx`: la guía ya los resume.
2. Consulta `libreria/README.md` SOLO para las firmas de las piezas que vayas a usar (localízalas con el índice §7 de la guía
   y `grep -n "<pieza>" libreria/README.md`). No lo leas entero.
3. No investigues ni reescribas el guion; si pasa de 135 palabras, recorta lo mínimo. Cifras con unidades, dichas con palabras.
4. Monta siguiendo la guía: escenas free/full grandes, ningún panel vacío, algo entra en el instante 0 de cada escena,
   nunca 3 s sin cambio, personas vivas (respiración, balanceo, parpadeo, gesto en la palabra clave, cabeza con retraso).
5. Control de calidad con TOPE: `revisar.py` las veces que haga falta (no mira imágenes), pero como mucho 1 render local sin voz
   (`python3 scripts/qa_frames.py content/<carpeta> <scratchpad>/qa-<carpeta>`) y como mucho 3 imágenes miradas.
6. Reglas de subida, archivos que NO se tocan y formato del commit: `docs/encargo-comun.md` (apartados «Reglas», «Revisión» y «Subida»;
   ignora su «Antes de empezar»: lo sustituye este encargo).
7. Respuesta final corta: cambios respecto al guion, palabras, duración estimada, piezas nuevas de librería y hash del commit.

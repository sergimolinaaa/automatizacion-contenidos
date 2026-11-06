# Reglas visuales

## Estilo visual: PAPEL RECORTADO (estándar desde el 2-nov)
- Todos los vídeos nuevos van en papel recortado. Referencia de calidad: `muestras/estilos/C` (dibujos en `muestras/estilos/dib.py`,
  `estilo_c`) más las recetas de `docs/montaje-rapido.md` §0 y §3 (parallax en 3 planos, squash, antic, flutter, puff, fall, jitter).
- Cómo: `libreria/svg/papel.py`. Personas con `persona(..., estilo="papel")`; cualquier otra pieza con `a_papel(pieza, semilla)`;
  fondos `fondo_calle`, `fondo_casa`, `fondo_cielo`, `fondo_neutro`; `grano()` al final de cada SVG; salida con `hoja_transicion`.
  Catálogo de lo que ya convierte bien: `entregas/estilos/catalogo_papel.png`.
- Rasgos: sin contornos negros (tinta marrón `#3A2E2A` solo en detalles), paleta cálida apagada (`PAPEL`), bordes irregulares,
  sombra de papel levantado, grano y fibras, giros leves de collage, 3 planos con parallax. Nada de degradados ni brillos de pegatina.
- El estilo pegatina anterior (`content/lote3-01-zapatero`, `content/lote6-03-voto-en-blanco`) sigue siendo la referencia de
  calidad de guion, composición y animación, no de acabado. 3-4 SVG por vídeo hechos con Python.
- NUNCA un momento vacío: cada frase tiene algo en pantalla que la ilustra. NUNCA más de 3 s sin que algo aparezca, se mueva o cambie.
- Todas las escenas (salvo las 2 del cierre) llevan dibujo; mitad inferior libre para subtítulos; nada solapado ni cortado.
- Layouts `panel` (1000x700), `free` (transparente, vertical) y `full` (1080x1920, lo importante entre y 450-1250). Mínimo 2 free/full.
- Motor: `video/src/components/Illustration.tsx`, tipos en `video/src/types.ts`, reglas de DSL en `SYSTEM` de `autocontent/generate.py`.

Más detalle del DSL de animación: constante SYSTEM en autocontent/generate.py y libreria/recetas.md.

## Movimiento (skill rossark-motion-skill)
Para animar personas, animales y objetos usa el método de `.claude/skills/rossark-motion-skill/SKILL.md`
(secciones 1, 3, 4 y 5): nunca teletransportar, amplitudes pequeñas, rotar sobre su pivote (cuello, hombro, base),
cada parte con su fase (nada en sincronía), izquierda y derecha nunca en espejo, ninguna pose congelada mientras
está en pantalla (respiración, balanceo, parpadeo cada 3-4 s), y la cabeza y las manos llegan un poco después del cuerpo.
Nuestro motor es el DSL de animaciones de `video/src/components/Illustration.tsx` (no las plantillas de React Native ni SwiftUI).

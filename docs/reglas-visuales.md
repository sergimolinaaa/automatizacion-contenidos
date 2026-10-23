# Reglas visuales

## Estilo visual (estética azul: fondo azul con cuadrícula, título blanco con bloques lima, ilustración en viñeta)
- El nivel MÍNIMO es `content/lote3-01-zapatero`. Pegatina realista: degradados, brillos, sombras; 3-4 SVG por vídeo hechos con Python.
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

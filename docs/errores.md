# Errores a evitar

## Errores a evitar
- Un commit en `content/**` dispara render + publicación: no subas borradores. No subas `lote2-03-hielo-flota`/`lote2-04-hipo` (ya publicados).
- NUNCA `git stash pop` a ciegas (hay stashes viejos que no deben aplicarse); usa `pull --rebase --autostash`.
- Zooms de cámara (`"camera"`) que tapan el titular o cortan etiquetas: oculta etiquetas con `hide` o quita el zoom.
- `hide` sin trigger oculta desde el principio de la escena; los `move` se suman; en grupos rotados van en coordenadas locales.
- Vídeos demasiado largos (>60 s): recorta palabras y la escena "+".
- **Secretos**: la clave de Buffer vive solo en el secreto `BUFFER_API_KEY` de GitHub. Nunca la escribas en archivos ni pidas claves por chat.

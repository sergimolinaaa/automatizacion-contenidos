# Reglas de guion y textos

## Qué funciona (datos de la cuenta, oct 2026)
- Lo que habla de «tú»: tu cuerpo, tu mente, tu voto, tu dinero, tu día a día (algo que el espectador ha vivido).
- Elecciones: SOLO cómo funciona el sistema (voto en blanco, escaños, fechas). NUNCA programas ni propuestas de partidos.
- Curiosidades visuales «¿cómo es posible?» (piedras que se mueven, palomitas…).
- Responder preguntas de comentarios (el de los escalofríos rindió muy por encima de la media).
- 2 vídeos al día (14:00 calendario, 21:00 extra), el mismo en las 3 redes. `publish.py` impide más de 2 al día. (Prueba desde el 16-oct: comparar media y total con la semana de 1 al día.)

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
## Calendario
`data/calendario.json` manda (fecha → tema). Cada vídeo lleva `"publish": {"at": "<fecha>T14:00:00+02:00"}` (+01:00 desde el 25-oct).
Al hacerlo, rellena su `"carpeta"` en el calendario. Si una noticia muy relevante encaja, AVISA al usuario antes de cambiar el calendario.
DOMINGOS: de momento SIN respuestas a comentarios (decisión del usuario, 16-oct); se usa un tema de los pilares. Si se reactivan: el usuario pasa capturas de comentarios (no tenemos acceso a las redes); se elige la pregunta
con más likes que encaje y el vídeo empieza «Respondemos a la pregunta de @usuario…». Si no hay pregunta válida, avisar y proponer tema.

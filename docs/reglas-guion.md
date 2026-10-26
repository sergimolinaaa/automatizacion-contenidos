# Reglas de guion y textos

## Qué funciona (datos de la cuenta, oct 2026)
- Lo que habla de «tú»: tu cuerpo, tu mente, tu voto, tu dinero, tu día a día (algo que el espectador ha vivido).
- Elecciones: SOLO cómo funciona el sistema (voto en blanco, escaños, fechas). NUNCA programas ni propuestas de partidos.
- Curiosidades visuales «¿cómo es posible?» (piedras que se mueven, palomitas…).
- Responder preguntas de comentarios (el de los escalofríos rindió muy por encima de la media).
- 1 vídeo al día a las 14:00 (desde el 26-oct; la prueba de 2 al día del 16 al 27-oct se paró por coste). `publish.py` impide más de 1 al día.

### Datos de views (capturas del 25-oct, últimas 2 semanas)
- Éxitos en las 3 redes: voto en blanco (IG 16,6K, TikTok 8.152), D'Hondt «mismos votos, otro resultado» (TikTok 6.650, IG 2.684), piel de gallina (TikTok 5.363).
- Fórmula: PARADOJA o MITO que se rompe + algo que le toca al espectador (su voto, su cuerpo).
- TikTok premia cuerpo y tecnología cotidiana (picadura, móvil lento, tiritar, motor en medio ≈ 2.100-2.500).
  Instagram premia sistema electoral y fenómenos visuales (rotondas, «¿llega al 29 N?» ≈ 2.150).
- Flojean: dinero y consumo (rebajas, precios ,99), «tu voto se pierde», vídeos de partidos en IG. YouTube no sirve para decidir temas.
- Pedido del usuario: más «tecnología cotidiana + causa física sorprendente + estacional» (tipo el frío y la batería del móvil).

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
- Política: neutral. En la escena 1 una frase ENTERA que varíe de un vídeo a otro: «Te lo explicamos sin posicionarnos, simplemente
  con los datos publicados.», «Sin posicionarnos: solo con los datos que ya sabemos.»… + sello. Partidos con su NOMBRE y COLORES reales
  (decisión del usuario, 16-oct), tratados todos igual.
- Marcas: nombre y logotipo reales permitidos aunque parezca anuncio (dibujado en SVG estilo pegatina). Precios y cifras estimadas o
  dichas por alguien: valen, pero dilo claro en narración o tarjeta («estimado, no confirmado al 100 %») y cita quién lo dice.
- Entrega de cada vídeo: `python3 scripts/entrega.py content/<carpeta>` (genera `entregas/<carpeta>.md`).
## Calendario
`data/calendario.json` manda (fecha → tema). Cada vídeo lleva `"publish": {"at": "<fecha>T14:00:00+02:00"}` (+01:00 desde el 25-oct).
Al hacerlo, rellena su `"carpeta"` en el calendario. Si una noticia muy relevante encaja, AVISA al usuario antes de cambiar el calendario.
DOMINGOS: de momento SIN respuestas a comentarios (decisión del usuario, 16-oct); se usa un tema de los pilares. Si se reactivan: el usuario pasa capturas de comentarios (no tenemos acceso a las redes); se elige la pregunta
con más likes que encaje y el vídeo empieza «Respondemos a la pregunta de @usuario…». Si no hay pregunta válida, avisar y proponer tema.

"""Genera el guion completo de un vídeo corto con Claude (salida JSON estructurada)."""

import json

import anthropic

SCRIPT_SCHEMA = {
    "type": "object",
    "properties": {
        "topic": {"type": "string", "description": "Tema concreto del vídeo, en una frase"},
        "title": {"type": "string", "description": "Título para YouTube, máx. 90 caracteres"},
        "segments": {
            "type": "array",
            "description": "Narración dividida en bloques; el primero es el gancho",
            "items": {
                "type": "object",
                "properties": {
                    "narration": {"type": "string", "description": "Texto que lee la voz"},
                    "visual_query": {
                        "type": "string",
                        "description": "2-4 palabras EN INGLÉS para buscar metraje de stock",
                    },
                },
                "required": ["narration", "visual_query"],
                "additionalProperties": False,
            },
        },
        "description": {"type": "string", "description": "Descripción para YouTube (2-4 frases)"},
        "caption": {"type": "string", "description": "Texto para Instagram/TikTok, con emojis moderados"},
        "hashtags": {"type": "array", "items": {"type": "string"}, "description": "5-8 hashtags sin '#'"},
    },
    "required": ["topic", "title", "segments", "description", "caption", "hashtags"],
    "additionalProperties": False,
}

SYSTEM_PROMPT = """Eres el guionista de una cuenta de vídeos cortos verticales (YouTube Shorts, Instagram Reels y TikTok).
Escribes guiones que retienen al espectador hasta el final:
- El primer segmento es un gancho de menos de 3 segundos que crea curiosidad inmediata.
- Cada segmento es una o dos frases cortas, fáciles de leer como subtítulo.
- Ritmo alto, sin relleno, sin saludos ni "hola a todos".
- La información debe ser correcta y verificable. Nunca inventes datos, cifras ni citas.
- El cierre invita a comentar, seguir o ver otro vídeo, sin sonar desesperado.
Cada segmento lleva una búsqueda de metraje de stock en inglés que ilustre lo que se dice (cosas filmables, no conceptos abstractos)."""


def build_prompt(cfg: dict, recent_topics: list[str], idea: str | None) -> str:
    ch = cfg["channel"]
    words = int(cfg["video"]["target_seconds"] * 2.6)  # ~2.6 palabras/segundo
    rules = "\n".join(f"- {r}" for r in ch.get("extra_rules", []))
    avoid = "\n".join(f"- {t}" for t in recent_topics[-60:]) or "- (ninguno todavía)"
    topic_line = (
        f"Tema del vídeo de hoy: {idea}" if idea else "Elige tú un tema nuevo y con mucho potencial viral dentro del nicho."
    )
    return f"""Canal: {ch['name']}
Nicho: {ch['niche']}
Idioma de todo el texto (salvo visual_query): {ch['language']}
Audiencia: {ch['audience']}
Tono: {ch['tone']}
Reglas del canal:
{rules}

{topic_line}

Temas ya publicados (no los repitas ni hagas variaciones obvias):
{avoid}

Longitud: unas {words} palabras de narración en total, repartidas en 6-10 segmentos."""


def write_script(cfg: dict, recent_topics: list[str], idea: str | None = None) -> dict:
    client = anthropic.Anthropic()
    response = client.beta.messages.create(
        model=cfg["claude"]["model"],
        max_tokens=16000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": build_prompt(cfg, recent_topics, idea)}],
        output_config={
            "effort": cfg["claude"].get("effort", "medium"),
            "format": {"type": "json_schema", "schema": SCRIPT_SCHEMA},
        },
        # Si el modelo rechaza la petición, la API la reintenta en otro modelo recomendado.
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
    )
    if response.stop_reason == "refusal":
        raise RuntimeError(f"Claude rechazó generar el guion: {response.stop_details}")
    if response.stop_reason == "max_tokens":
        raise RuntimeError("El guion se cortó por max_tokens")
    text = next(b.text for b in response.content if b.type == "text")
    script = json.loads(text)
    script["hashtags"] = [h.lstrip("#").replace(" ", "") for h in script["hashtags"] if h.strip()]
    return script

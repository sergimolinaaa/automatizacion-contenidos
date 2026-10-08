"""Subtítulos dinámicos estilo TikTok (formato ASS) con la palabra activa resaltada."""

from pathlib import Path


def ass_time(seconds: float) -> str:
    cs = max(0, round(seconds * 100))
    h, cs = divmod(cs, 360000)
    m, cs = divmod(cs, 6000)
    s, cs = divmod(cs, 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("{", "(").replace("}", ")").replace("\n", " ")


def group_words(words: list[dict], per_line: int) -> list[list[dict]]:
    """Agrupa palabras en líneas cortas, cortando también tras signos de puntuación."""
    lines, current = [], []
    for w in words:
        current.append(w)
        if len(current) >= per_line or w["text"].rstrip()[-1:] in ".,!?;:":
            lines.append(current)
            current = []
    if current:
        lines.append(current)
    return lines


def build_ass(words: list[dict], cfg: dict, total_duration: float) -> str:
    v, c = cfg["video"], cfg["video"]["captions"]
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {v['width']}
PlayResY: {v['height']}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{c['font']},{c['font_size']},{c['primary_color']},&H000000FF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,{c['outline']},2,2,60,60,{c['margin_bottom']},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    lines = group_words(words, c["words_per_line"])
    for li, line in enumerate(lines):
        # Cada línea se mantiene en pantalla hasta que empieza la siguiente.
        line_end = lines[li + 1][0]["start"] if li + 1 < len(lines) else total_duration
        for wi, word in enumerate(line):
            start = word["start"]
            end = line[wi + 1]["start"] if wi + 1 < len(line) else line_end
            if end <= start:
                continue
            parts = []
            for k, other in enumerate(line):
                txt = escape(other["text"].upper())
                parts.append(f"{{\\c{c['highlight_color']}}}{txt}{{\\c{c['primary_color']}}}" if k == wi else txt)
            pop = "{\\fscx108\\fscy108\\t(0,80,\\fscx100\\fscy100)}" if wi == 0 else ""
            events.append(f"Dialogue: 0,{ass_time(start)},{ass_time(end)},Default,,0,0,0,,{pop}{' '.join(parts)}")
    return header + "\n".join(events) + "\n"


def write_ass(words: list[dict], cfg: dict, total_duration: float, path: Path) -> Path:
    path.write_text(build_ass(words, cfg, total_duration), encoding="utf-8")
    return path

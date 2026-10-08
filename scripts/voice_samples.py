"""Genera muestras de todas las voces en español de Edge TTS (y las multilingües)
con el mismo texto, para elegir la más realista de oído.

Uso:
  python scripts/voice_samples.py [carpeta_salida]            # todas las voces
  python scripts/voice_samples.py carpeta es-ES-XimenaNeural  # variantes de una voz
"""
import asyncio
import json
import subprocess
import sys
from pathlib import Path

import edge_tts

TEXT = (
    "Este pez caza insectos a escupitajos. ¿Cómo lo hace? El truco es su boca: "
    "pega la lengua al paladar, forma un tubo, y cierra las branquias de golpe. "
    "El agua sale disparada… y el insecto cae. ¡Plaf!"
)
LOCALES = ("es-ES", "es-MX", "es-US", "es-AR", "es-CO", "es-CL")


async def main(out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    voices = await edge_tts.list_voices()
    chosen = [v for v in voices if v["Locale"] in LOCALES or "Multilingual" in v["ShortName"]]
    index = []
    for v in sorted(chosen, key=lambda v: (v["Locale"] != "es-ES", v["ShortName"])):
        name = v["ShortName"]
        raw = out / f"{name}.raw.mp3"
        final = out / f"{name}.mp3"
        try:
            await edge_tts.Communicate(TEXT, name, rate="+5%").save(str(raw))
        except Exception as e:  # algunas voces multilingües pueden fallar
            print(f"✗ {name}: {e}")
            continue
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(raw), "-af", "loudnorm=I=-14:TP=-1.5", "-b:a", "128k", str(final)], check=True)
        raw.unlink()
        index.append({"voice": name, "gender": v["Gender"], "locale": v["Locale"], "file": final.name})
        print(f"✓ {name}")
    (out / "voces.json").write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")


# (velocidad, tono, nombre) para afinar una voz concreta
VARIANTS = [
    ("+0%", "+0Hz", "natural"),
    ("+8%", "+0Hz", "agil"),
    ("+14%", "+0Hz", "rapida"),
    ("+8%", "-4Hz", "agil-grave"),
    ("+8%", "+4Hz", "agil-aguda"),
    ("+12%", "+2Hz", "energica"),
    ("+4%", "-2Hz", "calmada"),
]


async def variants(out: Path, voice: str) -> None:
    out.mkdir(parents=True, exist_ok=True)
    index = []
    for rate, pitch, label in VARIANTS:
        raw = out / f"{label}.raw.mp3"
        final = out / f"{voice}_{label}_vel{rate}_tono{pitch}.mp3"
        await edge_tts.Communicate(TEXT, voice, rate=rate, pitch=pitch).save(str(raw))
        af = "highpass=f=70,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120,loudnorm=I=-14:TP=-1.5:LRA=9"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(raw), "-af", af, "-b:a", "160k", str(final)], check=True)
        raw.unlink()
        index.append({"voice": voice, "rate": rate, "pitch": pitch, "label": label, "file": final.name})
        print(f"✓ {final.name}")
    (out / "variantes.json").write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    dest = Path(sys.argv[1] if len(sys.argv) > 1 else "previews/voces")
    if len(sys.argv) > 2:
        asyncio.run(variants(dest, sys.argv[2]))
    else:
        asyncio.run(main(dest))

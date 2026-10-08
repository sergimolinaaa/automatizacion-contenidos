import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from autocontent.timeline import build_props, estimate_words, find_trigger  # noqa: E402
from autocontent.voice import align  # noqa: E402


def test_align_keeps_punctuation_and_handles_splits():
    tokens = ["¿Cómo", "lo", "hace?", "El", "truco", "es…"]
    tts = [
        {"text": "Cómo", "start": 0.0, "end": 0.3},
        {"text": "lo", "start": 0.3, "end": 0.4},
        {"text": "hace", "start": 0.4, "end": 0.7},
        {"text": "El", "start": 1.0, "end": 1.1},
        {"text": "truco", "start": 1.1, "end": 1.4},
        {"text": "es", "start": 1.4, "end": 1.6},
    ]
    out = align(tokens, tts)
    assert [w["text"] for w in out] == tokens
    assert out[2]["start"] == 0.4 and out[5]["end"] == 1.6


def test_align_fills_missing_words():
    out = align(["Hola", "mundo", "feliz"], [{"text": "Hola", "start": 0, "end": 0.3}, {"text": "feliz", "start": 0.8, "end": 1.1}])
    assert out[1]["start"] >= 0.3 and out[1]["end"] <= 0.8


def test_triggers_map_to_word_times():
    script = {
        "chapters": ["?", "1"],
        "scenes": [
            {"chapter": 0, "headline": "A", "narration": "Este pez caza a escupitajos.",
             "illustration": {"svg": "<svg/>", "anims": [{"target": "jet", "effect": "draw", "trigger": "escupitajos"}]},
             "elements": [{"type": "tag", "text": "x", "trigger": "pez"}]},
            {"chapter": 1, "headline": "B", "narration": "El truco es su boca.",
             "mascot": {"trigger": "boca", "note": "hola"}},
        ],
    }
    ws1 = estimate_words(script["scenes"][0]["narration"], 0.1)
    ws2 = estimate_words(script["scenes"][1]["narration"], ws1[-1]["end"] + 0.3)
    props = build_props(script, [ws1, ws2])
    s0, s1 = props["scenes"]
    assert abs(s0["illustration"]["anims"][0]["at"] - (find_trigger("escupitajos", ws1, 0) - 0.05)) < 1e-6
    assert s0["elements"][0]["at"] < s0["illustration"]["anims"][0]["at"]
    assert s1["mascot"]["at"] > s1["start"]
    assert props["outro"]["at"] == s1["end"]


def test_generator_validator_accepts_examples_and_fixes_bad_triggers():
    import json as _json

    from autocontent import generate

    script = _json.loads(generate._example())
    script["scenes"][0]["illustration"]["anims"].append({"target": "fish", "effect": "pop", "trigger": "inexistente"})
    script["scenes"][0]["illustration"]["anims"].append({"target": "no-existe", "effect": "pop"})
    errors, warnings = generate.validate(script)
    assert errors == []
    assert any("inexistente" in w for w in warnings) and any("no-existe" in w for w in warnings)
    assert script["scenes"][1]["signature"] is True

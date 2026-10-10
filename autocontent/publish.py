"""Programa los vídeos renderizados en Buffer (YouTube, Instagram y TikTok): 3 al día (mañana, mediodía y noche, hora de Madrid).

- Cada vídeo necesita una URL pública (la API de Buffer no admite subir archivos): se publica como
  asset de una release de GitHub en un repositorio PÚBLICO (MEDIA_REPO, p. ej. "usuario/eltrucoes-videos").
- El orden alterna categorías (plantas, animales, física, cuerpo, tierra...) para que el feed sea variado.
- El estado (qué se ha programado y cuándo) se guarda en data/publicaciones.json.

Variables: BUFFER_API_KEY, MEDIA_REPO, GH_TOKEN (con permiso de escritura en MEDIA_REPO).
"""

import json
import os
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

from .config import ROOT

API = "https://api.buffer.com"
STATE = ROOT / "data" / "publicaciones.json"
PREVIEWS = ROOT / "previews"
TZ = ZoneInfo("Europe/Madrid")
SLOTS = (9, 14, 21)  # horas locales de publicación: mañana, mediodía y tarde-noche
MIN_GAP = timedelta(hours=2)  # separación mínima con la publicación anterior
MAX_QUEUE = 8  # publicaciones futuras por canal (el plan de Buffer permite 10)
CATEGORY_ORDER = ["psicologia", "animales", "objetos", "fisica", "plantas", "cuerpo", "cocina", "tierra", "politica"]


# ------------------------------------------------------------------ Buffer GraphQL

def gql(query: str, variables: dict | None = None, partial: bool = False) -> dict:
    """partial=True devuelve los datos aunque Buffer añada errores (p. ej. una publicación creada con avisos)."""
    r = requests.post(
        API,
        json={"query": query, "variables": variables or {}},
        headers={"Authorization": f"Bearer {os.environ['BUFFER_API_KEY']}", "Content-Type": "application/json"},
        timeout=60,
    )
    r.raise_for_status()
    data = r.json()
    if data.get("errors"):
        if partial and data.get("data"):
            print(f"  aviso de Buffer: {data['errors']}")
            return data["data"]
        raise RuntimeError(f"Buffer: {data['errors']}")
    return data["data"]


def channels() -> list[dict]:
    """Canales conectados en Buffer: [{id, name, service}]."""
    orgs = gql("query { account { organizations { id name } } }")["account"]["organizations"]
    out = []
    for org in orgs:
        res = gql(
            "query($org: OrganizationId!) { channels(input: { organizationId: $org }) { id name service } }",
            {"org": org["id"]},
        )
        out += res["channels"]
    return out


def _metadata(service: str, meta: dict) -> dict | None:
    s = service.lower()
    if s == "youtube":
        return {"youtube": {"title": meta["title"][:100], "categoryId": "27"}}
    if s == "instagram":
        return {"instagram": {"type": "reel", "shouldShareToFeed": True}}
    if s == "tiktok":
        return {"tiktok": {"title": meta["title"][:90]}}
    return None


CREATE = """
mutation($input: CreatePostInput!) {
  createPost(input: $input) {
    ... on PostActionSuccess { post { id dueAt } }
    ... on MutationError { message }
  }
}"""


def create_post(channel: dict, text: str, video_url: str, due: datetime, meta: dict, thumb_ms: int) -> dict:
    base = {
        "channelId": channel["id"],
        "text": text,
        "schedulingType": "automatic",
        "mode": "customScheduled",
        "dueAt": due.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "assets": [{"video": {"url": video_url, "metadata": {"thumbnailOffset": thumb_ms}}}],
    }
    md = _metadata(channel["service"], meta)
    attempts = [dict(base, metadata=md)] if md else []
    attempts.append(base)  # sin metadatos específicos si el esquema no los acepta
    errors = []
    for inp in attempts:
        try:
            res = (gql(CREATE, {"input": inp}, partial=True) or {}).get("createPost") or {}
        except requests.RequestException as e:
            # sin respuesta no sabemos si se creó: NO reintentar (evita duplicados)
            raise RuntimeError(f"Sin respuesta de Buffer en {channel['service']} (no se reintenta): {e}") from e
        except RuntimeError as e:
            errors.append(str(e)[:600])
            continue
        if res.get("post"):
            return res["post"]
        errors.append(res.get("message"))
    raise RuntimeError(f"No se pudo programar en {channel['service']}: " + " || ".join(map(str, errors)))


# ------------------------------------------------------------------ alojamiento público

def host_video(slug: str, video: Path, cover: Path) -> str:
    repo = os.environ["MEDIA_REPO"]
    tag = f"v-{slug}"
    subprocess.run(["gh", "release", "create", tag, str(video), str(cover), "--repo", repo, "--title", slug, "--notes", slug],
                   check=False, capture_output=True)
    subprocess.run(["gh", "release", "upload", tag, str(video), str(cover), "--repo", repo, "--clobber"], check=True)
    return f"https://github.com/{repo}/releases/download/{tag}/{video.name}"


# ------------------------------------------------------------------ planificación

def load_state() -> dict:
    return json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {"posts": []}


def save_state(state: dict) -> None:
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def pending_videos(state: dict) -> list[dict]:
    done = {p["slug"] for p in state["posts"]}
    items = []
    for video in sorted(PREVIEWS.glob("*-con-voz.mp4")):
        slug = video.name.removesuffix("-con-voz.mp4")
        if slug in done:
            continue
        folder = next((p for p in [ROOT / "content" / slug, ROOT / "examples" / slug] if (p / "guion.json").exists()), None)
        if not folder:
            continue
        script = json.loads((folder / "guion.json").read_text(encoding="utf-8"))
        info = json.loads(video.with_suffix(".json").read_text(encoding="utf-8")) if video.with_suffix(".json").exists() else {}
        items.append({"slug": slug, "video": video, "cover": video.with_suffix(".png"), "script": script,
                      "category": script.get("categoria", "animales"), "thumb_ms": info.get("cover_offset_ms", 0)})
    return interleave(items)


def interleave(items: list[dict]) -> list[dict]:
    """Ordena alternando categorías: animal, planta, física, cuerpo, tierra, animal..."""
    buckets: dict[str, list[dict]] = {}
    for it in items:
        buckets.setdefault(it["category"], []).append(it)
    order = [c for c in CATEGORY_ORDER if c in buckets] + [c for c in buckets if c not in CATEGORY_ORDER]
    out = []
    while any(buckets.values()):
        for c in order:
            if buckets.get(c):
                out.append(buckets[c].pop(0))
    return out


def caption(script: dict, service: str) -> str:
    pub = script.get("publish", {})
    tags = " ".join(f"#{h}" for h in pub.get("hashtags", []))
    if service.lower() == "youtube":
        return f"{pub.get('description', script['title'])}\n\n{tags} #shorts"
    return f"{pub.get('caption', script['title'])}\n\n{tags}"


def refresh_hosted(state: dict) -> None:
    """Si un vídeo ya programado se ha vuelto a renderizar, sustituye el archivo en la misma URL.
    Buffer descarga el vídeo al publicar, así que sale la versión nueva sin tocar la publicación."""
    now = datetime.now(timezone.utc)
    repo = os.environ["MEDIA_REPO"]
    for p in state["posts"]:
        if datetime.fromisoformat(p["due"]) <= now + timedelta(minutes=10):
            continue
        video = PREVIEWS / f"{p['slug']}-con-voz.mp4"
        if not video.exists():
            continue
        tag = f"v-{p['slug']}"
        res = subprocess.run(["gh", "release", "view", tag, "--repo", repo, "--json", "assets"], capture_output=True, text=True)
        if res.returncode != 0:
            print(f"  aviso: no puedo leer la release {tag}: {res.stderr.strip()[:200]}")
            continue
        sizes = {a["name"]: a.get("size") for a in json.loads(res.stdout).get("assets", [])}
        print(f"  {p['slug']}: alojado {sizes.get(video.name)} bytes, render actual {video.stat().st_size} bytes")
        if sizes.get(video.name) != video.stat().st_size:
            subprocess.run(["gh", "release", "upload", tag, str(video), str(video.with_suffix(".png")), "--repo", repo, "--clobber"], check=True)
            print(f"  actualizado {p['slug']} (nuevo render)")


def next_slot(after: datetime) -> datetime:
    """Primera franja (SLOTS, hora de Madrid) estrictamente posterior a `after`."""
    local = after.astimezone(TZ)
    for day in range(3):
        d = (local + timedelta(days=day)).date()
        for h in SLOTS:
            slot = datetime(d.year, d.month, d.day, h, tzinfo=TZ)
            if slot > local:
                return slot.astimezone(timezone.utc)
    raise RuntimeError("sin franja")


def schedule_all(limit: int | None = None) -> list[dict]:
    state = load_state()
    refresh_hosted(state)
    chans = channels()
    print("Canales:", ", ".join(f"{c['service']} ({c['name']})" for c in chans))
    now = datetime.now(timezone.utc)
    last = max((datetime.fromisoformat(p["due"]) for p in state["posts"]), default=None)
    due = next_slot(max(now + timedelta(minutes=30), (last + MIN_GAP) if last else now))
    future = sum(1 for p in state["posts"] if datetime.fromisoformat(p["due"]) > now)
    room = max(0, MAX_QUEUE - future)
    limit = room if limit is None else min(limit, room)
    print(f"En cola: {future} · hueco para {room} · se programan {limit}")
    complete_missing(state, chans, now)
    scheduled = []
    for item in pending_videos(state)[:limit]:
        url = host_video(item["slug"], item["video"], item["cover"])
        entry = {"slug": item["slug"], "category": item["category"], "due": due.isoformat(), "url": url, "posts": {}}
        state["posts"].append(entry)  # se guarda ANTES de crear nada: un fallo nunca provoca duplicados
        save_state(state)
        full = fill_channels(state, entry, item["script"], chans, item["thumb_ms"])
        scheduled.append(entry)
        due = next_slot(due + MIN_GAP)
        if not full:
            print("  Buffer está lleno en algún canal; los canales que faltan se completarán en la próxima ejecución.")
            break
    return scheduled


def fill_channels(state: dict, entry: dict, script: dict, chans: list[dict], thumb_ms: int) -> bool:
    """Crea la publicación en los canales que aún no la tienen. Guarda el estado tras cada una."""
    due = datetime.fromisoformat(entry["due"])
    ok = True
    for ch in chans:
        if ch["service"] in entry["posts"]:
            continue
        try:
            post = create_post(ch, caption(script, ch["service"]), entry["url"], due, {"title": script["title"]}, thumb_ms)
        except RuntimeError as e:
            print(f"  {entry['slug']} → {ch['service']}: {e}")
            ok = False
            continue
        entry["posts"][ch["service"]] = post["id"]
        save_state(state)
        print(f"  {entry['slug']} → {ch['service']} a las {due:%d/%m %H:%M} UTC")
    return ok


def complete_missing(state: dict, chans: list[dict], now: datetime) -> None:
    """Publicaciones futuras a las que les falta algún canal (p. ej. por la cola llena): se completan."""
    for entry in state["posts"]:
        if datetime.fromisoformat(entry["due"]) <= now + timedelta(minutes=20):
            continue
        if all(c["service"] in entry["posts"] for c in chans):
            continue
        folder = next((p for p in [ROOT / "content" / entry["slug"], ROOT / "examples" / entry["slug"]] if (p / "guion.json").exists()), None)
        if not folder:
            continue
        script = json.loads((folder / "guion.json").read_text(encoding="utf-8"))
        info_p = PREVIEWS / f"{entry['slug']}-con-voz.json"
        thumb = json.loads(info_p.read_text(encoding="utf-8")).get("cover_offset_ms", 0) if info_p.exists() else 0
        fill_channels(state, entry, script, chans, thumb)

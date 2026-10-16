"""Uso:
  python -m autocontent generar            # Claude investiga un tema y escribe el guion (content/<fecha-tema>/)
  python -m autocontent render CARPETA     # vídeo + portada de un guion
  python -m autocontent diario             # generar + render
  python -m autocontent canales            # lista los canales de Buffer
  python -m autocontent programar [-n N]   # programa en Buffer los vídeos pendientes, uno cada 2 horas
  python -m autocontent mover SLUG ISO […] # cambia la hora de uno o varios vídeos ya programados
"""
import argparse
from pathlib import Path

from .config import load_dotenv


def main() -> None:
    load_dotenv()
    ap = argparse.ArgumentParser(prog="autocontent")
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("generar")
    g.add_argument("--tema", help="tema concreto (si no, el siguiente del banco data/temas.json)")
    r = sub.add_parser("render")
    r.add_argument("carpeta", type=Path)
    sub.add_parser("diario")
    sub.add_parser("canales")
    pr = sub.add_parser("programar")
    pr.add_argument("-n", type=int, default=None, help="máximo de vídeos a programar")
    mv = sub.add_parser("mover")
    mv.add_argument("pares", nargs="+", help="slug y nueva hora ISO, uno o varios pares: SLUG 2026-10-17T21:00:00+02:00 …")
    a = ap.parse_args()

    if a.cmd in ("canales", "programar", "mover"):
        from . import publish

        if a.cmd == "canales":
            for c in publish.channels():
                print(f"{c['service']:<10} {c['name']:<30} {c['id']}")
        elif a.cmd == "mover":
            for slug, cuando in zip(a.pares[::2], a.pares[1::2]):
                publish.move(slug, cuando)
        else:
            publish.schedule_all(a.n)
        return

    from . import generate, render

    if a.cmd == "generar":
        generate.generate({"tema": a.tema} if a.tema else None)
    elif a.cmd == "render":
        render.render(a.carpeta)
    elif a.cmd == "diario":
        folder = generate.generate()
        render.render(folder)


if __name__ == "__main__":
    main()

"""Uso:
  python -m autocontent generar            # Claude investiga un tema y escribe el guion (content/<fecha-tema>/)
  python -m autocontent render CARPETA     # vídeo + portada de un guion
  python -m autocontent diario             # generar + render (y publicar cuando esté configurado)
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
    a = ap.parse_args()

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

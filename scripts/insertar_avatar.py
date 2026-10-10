"""Pone foto y nombre en una tarjeta de comentario (con permiso de la persona).
Uso: python3 scripts/insertar_avatar.py <tarjeta.svg> <foto.png> <nombre>
La tarjeta debe tener <clipPath id="avclip"><circle cx cy r/></clipPath>, un grupo
<g clip-path="url(#avclip)">…</g> con el avatar genérico y el texto «Un seguidor».
"""
import base64, re, sys
from pathlib import Path

svg_path, img_path, nombre = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
s = svg_path.read_text(encoding="utf-8")
cx, cy, r = map(float, re.search(r'<clipPath id="avclip"><circle cx="([\d.]+)" cy="([\d.]+)" r="([\d.]+)"', s).groups())
b64 = base64.b64encode(img_path.read_bytes()).decode()
img = (f'<image href="data:image/png;base64,{b64}" x="{cx - r:g}" y="{cy - r:g}" '
       f'width="{2 * r:g}" height="{2 * r:g}" preserveAspectRatio="xMidYMid slice"/>')
s, n = re.subn(r'(<g clip-path="url\(#avclip\)">).*?(</g>)', lambda m: m.group(1) + img + m.group(2), s, count=1, flags=re.S)
s = s.replace(">Un seguidor</text>", f">{nombre}</text>")
svg_path.write_text(s, encoding="utf-8")
print("avatar:", n, "· nombre:", nombre)

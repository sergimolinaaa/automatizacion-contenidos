"""Arcos de arcoíris y piezas de paisaje compartidas."""
import math
from dl import *

SPEC = ["#FF3B30", "#FF9500", "#FFE11A", "#34C759", "#2D7BFF", "#8E44FF"]


def arc_above(cx, cy, r, hy):
    """Arco de la circunferencia (cx,cy,r) por encima de la recta y=hy (de izquierda a derecha por arriba)."""
    dy = cy - hy
    if dy >= r:
        return None
    dx = math.sqrt(r * r - dy * dy)
    large = 1 if dy < 0 else 0
    return f"M {cx - dx:.1f} {hy} A {r:.1f} {r:.1f} 0 {large} 1 {cx + dx:.1f} {hy}"


def arc_below(cx, cy, r, hy):
    dy = cy - hy
    dx = math.sqrt(r * r - dy * dy)
    large = 0 if dy < 0 else 1
    return f"M {cx + dx:.1f} {hy} A {r:.1f} {r:.1f} 0 {large} 1 {cx - dx:.1f} {hy}"


def band(cx, cy, r_out, w, hy, order=SPEC, op=1.0, glow=True):
    """Arcoíris: colores desde el radio exterior hacia dentro en el orden dado."""
    n = len(order)
    s = ""
    if glow:
        d = arc_above(cx, cy, r_out - w * n / 2, hy)
        s += f'<path d="{d}" fill="none" stroke="#FFFFFF" stroke-width="{w * n + 18}" opacity="{0.12 * op:.2f}"/>'
    for k, c in enumerate(order):
        r = r_out - w * (k + 0.5)
        d = arc_above(cx, cy, r, hy)
        s += f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w + 0.8}" opacity="{op:.2f}"/>'
    # brillo fino en el borde exterior
    d = arc_above(cx, cy, r_out - 1, hy)
    s += f'<path d="{d}" fill="none" stroke="#FFFFFF" stroke-width="2" opacity="{0.35 * op:.2f}"/>'
    return s


def annulus_above(cx, cy, r1, r2, hy):
    """Corona circular entre r1<r2 por encima de y=hy."""
    dy = cy - hy
    d1, d2 = math.sqrt(r1 * r1 - dy * dy), math.sqrt(r2 * r2 - dy * dy)
    return (f"M {cx - d2:.1f} {hy} A {r2} {r2} 0 0 1 {cx + d2:.1f} {hy} L {cx + d1:.1f} {hy} "
            f"A {r1} {r1} 0 0 0 {cx - d1:.1f} {hy} Z")


def disc_above(cx, cy, r, hy):
    dy = cy - hy
    d = math.sqrt(r * r - dy * dy)
    return f"M {cx - d:.1f} {hy} A {r} {r} 0 0 1 {cx + d:.1f} {hy} Z"


def tree(x, y, s=1.0, col="#2E8B57", far=False):
    """Árbol redondeado con tronco (y = base)."""
    if far:
        return (f'<rect x="{x - 3 * s:.1f}" y="{y - 24 * s:.1f}" width="{6 * s:.1f}" height="{24 * s:.1f}" fill="#6F8F7A"/>'
                f'<circle cx="{x}" cy="{y - 34 * s:.1f}" r="{20 * s:.1f}" fill="{col}"/>')
    return (f'<path d="M {x - 5 * s:.1f} {y} L {x - 4 * s:.1f} {y - 36 * s:.1f} L {x + 4 * s:.1f} {y - 36 * s:.1f} L {x + 5 * s:.1f} {y} Z" fill="#7A5236" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
            f'<circle cx="{x - 14 * s:.1f}" cy="{y - 46 * s:.1f}" r="{20 * s:.1f}" fill="{col}" stroke="{INK}" stroke-width="5"/>'
            f'<circle cx="{x + 14 * s:.1f}" cy="{y - 48 * s:.1f}" r="{19 * s:.1f}" fill="{col}" stroke="{INK}" stroke-width="5"/>'
            f'<circle cx="{x}" cy="{y - 64 * s:.1f}" r="{22 * s:.1f}" fill="{col}" stroke="{INK}" stroke-width="5"/>'
            f'<path d="M {x - 22 * s:.1f} {y - 52 * s:.1f} C {x - 20 * s:.1f} {y - 62 * s:.1f}, {x - 10 * s:.1f} {y - 70 * s:.1f}, {x - 4 * s:.1f} {y - 74 * s:.1f}" fill="none" stroke="#9BE08A" stroke-width="{4 * s:.1f}" stroke-linecap="round" opacity="0.8"/>')


def person_back(x, y, s=1.0, idn="persona"):
    """Persona de espaldas (y = pies). Chaqueta coral, gorro azul, mochila."""
    def P(dx, dy):
        return f"{x + dx * s:.1f} {y + dy * s:.1f}"
    o = f'<g id="{idn}">'
    # piernas
    o += f'<path d="M {P(-14, -70)} L {P(-16, -4)} L {P(-4, -4)} L {P(-2, -70)} Z" fill="url(#pants)" stroke="{INK}" stroke-width="{5 * s ** 0.5:.1f}" stroke-linejoin="round"/>'
    o += f'<path d="M {P(2, -70)} L {P(4, -4)} L {P(16, -4)} L {P(14, -70)} Z" fill="url(#pants)" stroke="{INK}" stroke-width="{5 * s ** 0.5:.1f}" stroke-linejoin="round"/>'
    o += f'<path d="M {P(-20, -6)} L {P(-2, -6)} L {P(-2, 2)} L {P(-20, 2)} Z M {P(2, -6)} L {P(20, -6)} L {P(20, 2)} L {P(2, 2)} Z" fill="#4A3426" stroke="{INK}" stroke-width="{4 * s ** 0.5:.1f}" stroke-linejoin="round"/>'
    # brazos
    o += f'<path d="M {P(-26, -128)} C {P(-36, -110)}, {P(-36, -88)}, {P(-32, -70)}" fill="none" stroke="{INK}" stroke-width="{18 * s:.1f}" stroke-linecap="round"/>'
    o += f'<path d="M {P(-26, -128)} C {P(-36, -110)}, {P(-36, -88)}, {P(-32, -70)}" fill="none" stroke="#E5532F" stroke-width="{11 * s:.1f}" stroke-linecap="round"/>'
    o += f'<path d="M {P(26, -128)} C {P(36, -110)}, {P(36, -88)}, {P(32, -70)}" fill="none" stroke="{INK}" stroke-width="{18 * s:.1f}" stroke-linecap="round"/>'
    o += f'<path d="M {P(26, -128)} C {P(36, -110)}, {P(36, -88)}, {P(32, -70)}" fill="none" stroke="#E5532F" stroke-width="{11 * s:.1f}" stroke-linecap="round"/>'
    # torso
    o += f'<path d="M {P(-28, -134)} C {P(-30, -146)}, {P(30, -146)}, {P(28, -134)} L {P(24, -66)} C {P(10, -60)}, {P(-10, -60)}, {P(-24, -66)} Z" fill="url(#jacket)" stroke="{INK}" stroke-width="{6 * s ** 0.5:.1f}" stroke-linejoin="round"/>'
    # mochila
    o += f'<rect x="{x - 19 * s:.1f}" y="{y - 132 * s:.1f}" width="{38 * s:.1f}" height="{52 * s:.1f}" rx="{10 * s:.1f}" fill="#3E8E6A" stroke="{INK}" stroke-width="{5 * s ** 0.5:.1f}"/>'
    o += f'<rect x="{x - 12 * s:.1f}" y="{y - 108 * s:.1f}" width="{24 * s:.1f}" height="{18 * s:.1f}" rx="{5 * s:.1f}" fill="#2F7454" stroke="{INK}" stroke-width="{3 * s ** 0.5:.1f}"/>'
    o += f'<path d="M {P(-12, -126)} L {P(-6, -126)}" stroke="#86D9AE" stroke-width="{4 * s:.1f}" stroke-linecap="round"/>'
    # cabeza con gorro
    o += f'<circle cx="{x:.1f}" cy="{y - 160 * s:.1f}" r="{20 * s:.1f}" fill="#6B4630" stroke="{INK}" stroke-width="{5 * s ** 0.5:.1f}"/>'
    o += f'<path d="M {P(-21, -162)} C {P(-21, -190)}, {P(21, -190)}, {P(21, -162)} Z" fill="#2F6FD6" stroke="{INK}" stroke-width="{5 * s ** 0.5:.1f}" stroke-linejoin="round"/>'
    o += f'<path d="M {P(-12, -176)} C {P(-6, -182)}, {P(4, -183)}, {P(10, -180)}" fill="none" stroke="#8FB8FF" stroke-width="{3 * s:.1f}" stroke-linecap="round"/>'
    o += f'<circle cx="{x - 20 * s:.1f}" cy="{y - 158 * s:.1f}" r="{5 * s:.1f}" fill="#E8A27A" stroke="{INK}" stroke-width="{3 * s ** 0.5:.1f}"/>'
    o += f'<circle cx="{x + 20 * s:.1f}" cy="{y - 158 * s:.1f}" r="{5 * s:.1f}" fill="#E8A27A" stroke="{INK}" stroke-width="{3 * s ** 0.5:.1f}"/>'
    o += '</g>'
    return o


DEFS_P = "\n".join([
    lg("jacket", [(0, "#FF7A57"), (1, "#D9431F")]),
    lg("pants", [(0, "#3C4A66"), (1, "#222B3D")]),
])

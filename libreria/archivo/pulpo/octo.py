"""Pulpo (vista lateral, sentado sobre una roca). Coordenadas base: cabeza en ~(540, 900)."""
import math, random
from lib import *

PAL = {
    "rojo": dict(top="#FF7A55", mid="#E2412A", bot="#8E1C12", far="#A82A1A", spot="#FFC2AE", blot="#B52A18", suck="#FFD9CC", sring="#E89A88", hi="#FFB59C"),
    "camu": dict(top="#B3A388", mid="#8A7A62", bot="#4E4334", far="#5E5241", spot="#D8CDB6", blot="#5B4E3C", suck="#CFC3AA", sring="#9C8F77", hi="#D6CAB2"),
}


def defs(k):
    p = PAL[k]
    return (rg(f"{k}_mant", [(0, p["top"]), (0.55, p["mid"]), (1, p["bot"])], 0.38, 0.3, 0.8) +
            lg(f"{k}_arm", [(0, p["top"]), (1, p["mid"])]) +
            lg(f"{k}_armfar", [(0, p["far"]), (1, p["bot"])]))


ARMS_BACK = [
    [(470, 950), (390, 930), (310, 905), (262, 868), (270, 838), (300, 842)],
    [(612, 948), (712, 930), (800, 896), (846, 852), (834, 826), (810, 834)],
]
ARMS_FRONT = [
    [(452, 962), (350, 1000), (250, 1046), (182, 1030), (176, 996), (204, 986)],
    [(478, 978), (400, 1066), (318, 1130), (286, 1176), (312, 1196), (338, 1180)],
    [(512, 990), (488, 1100), (452, 1178), (470, 1214), (500, 1204)],
    [(560, 992), (584, 1104), (626, 1176), (666, 1182), (674, 1158)],
    [(592, 984), (672, 1070), (756, 1128), (816, 1124), (820, 1096), (800, 1088)],
    [(618, 966), (730, 1004), (846, 1036), (912, 1012), (908, 980), (884, 978)],
]


def arm(pts, k, far=False, w0=58, seed=0):
    p = PAL[k]
    d, c, norms, ws = tentacle(pts, w0, 9)
    fill = f"url(#{k}_armfar)" if far else f"url(#{k}_arm)"
    s = f'<path d="{d}" fill="{fill}" stroke="{INK}" stroke-width="{5 if far else 6}" stroke-linejoin="round"/>'
    # ventosas en el lado inferior (desde la mitad del brazo)
    m = len(c)
    for i in range(int(m * 0.35), m - 3, 4):
        x, y = c[i]
        nx, ny = norms[i]
        # lado que mira hacia abajo/fuera
        sgn = 1 if ny > 0 else -1
        r = max(3.5, ws[i] * 0.42)
        sx, sy = x + nx * sgn * ws[i] * 0.95, y + ny * sgn * ws[i] * 0.95
        s += f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="{r:.1f}" fill="{p["suck"]}" stroke="{INK}" stroke-width="3"/><circle cx="{sx:.1f}" cy="{sy:.1f}" r="{r * 0.45:.1f}" fill="{p["sring"]}"/>'
    # brillo en el lomo
    hl = [(x - nx * w * 0.5, y - ny * w * 0.5) for (x, y), (nx, ny), w in zip(c[2:int(m * 0.6)], norms[2:int(m * 0.6)], ws[2:int(m * 0.6)])]
    if not far and len(hl) > 2:
        s += f'<path d="{poly(hl)}" fill="none" stroke="{p["hi"]}" stroke-width="4" stroke-linecap="round" opacity="0.7"/>'
    # motas
    random.seed(seed)
    for i in range(3, int(m * 0.7), 5):
        x, y = c[i]
        s += f'<ellipse cx="{x + random.uniform(-6, 6):.1f}" cy="{y + random.uniform(-6, 6):.1f}" rx="{ws[i] * 0.35:.1f}" ry="{ws[i] * 0.22:.1f}" fill="{p["blot"]}" opacity="0.55"/>'
    return s


def body(k):
    p = PAL[k]
    o = []
    for i, a in enumerate(ARMS_BACK):
        o.append(arm(a, k, far=True, w0=50, seed=10 + i))
    # manto (saco) inclinado hacia atrás
    mant = "M 470 900 C 380 860, 360 700, 420 600 C 480 500, 640 500, 690 600 C 740 700, 690 860, 610 900 Z"
    o.append(f'<path d="{mant}" fill="url(#{k}_mant)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
    o.append(f'<path d="M 430 640 C 450 580, 520 548, 580 552" fill="none" stroke="{p["hi"]}" stroke-width="7" stroke-linecap="round" opacity="0.85"/>')
    random.seed(3)
    for _ in range(26):
        x, y = random.uniform(420, 680), random.uniform(580, 880)
        if not inside_mant(x, y):
            continue
        r = random.uniform(5, 14)
        o.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r:.0f}" ry="{r * 0.7:.0f}" fill="{p["blot"]}" opacity="0.6"/>')
    for _ in range(30):
        x, y = random.uniform(420, 680), random.uniform(580, 880)
        if not inside_mant(x, y):
            continue
        o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.uniform(2.5, 5):.1f}" fill="{p["spot"]}" opacity="0.8"/>')
    # cabeza (bajo el manto) con relieve de los ojos
    head = "M 440 900 C 430 850, 470 830, 540 830 C 610 830, 650 850, 640 900 C 636 950, 600 980, 540 980 C 480 980, 444 950, 440 900 Z"
    o.append(f'<path d="{head}" fill="url(#{k}_mant)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
    # sifón
    o.append(f'<path d="M 626 920 C 660 916, 676 930, 680 948 C 668 956, 650 954, 632 946 Z" fill="url(#{k}_arm)" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    # membrana (umbrela) entre las bases de los brazos
    web = "M 446 930 C 400 980, 420 1030, 470 1040 C 520 1060, 570 1060, 620 1040 C 670 1028, 690 980, 640 930 Z"
    o.append(f'<path d="{web}" fill="url(#{k}_arm)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
    for i, a in enumerate(ARMS_FRONT):
        o.append(arm(a, k, w0=60, seed=20 + i))
    # papilas sobre los ojos
    for ex in (482, 598):
        o.append(f'<path d="M {ex - 8} 846 L {ex} 826 L {ex + 8} 846" fill="{p["mid"]}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')
    return "".join(o)


def inside_mant(x, y):
    # aproximación elíptica del manto
    return ((x - 548) / 140) ** 2 + ((y - 720) / 175) ** 2 < 0.8


def eyes():
    o = []
    for ex in (482, 598):
        o.append(f'<ellipse cx="{ex}" cy="872" rx="30" ry="25" fill="#F4E7B8" stroke="{INK}" stroke-width="6"/>')
        o.append(f'<ellipse cx="{ex}" cy="872" rx="24" ry="19" fill="#E9C86A"/>')
        o.append(f'<rect x="{ex - 17}" y="866" width="34" height="11" rx="5" fill="{INK}"/>')
        o.append(f'<circle cx="{ex - 9}" cy="864" r="4.5" fill="#FFFFFF"/>')
    return "".join(o)

import math, random
from lib import *
W, H = 1000, 820
CX, CY, R = 470, 400, 330
COL = {"am": ("#FFE070", "#F2B705", "#A87800"), "ro": ("#FF7A5E", "#D9362A", "#7E1810"), "ma": ("#9A6A48", "#5A3420", "#2A160C")}
defs = (rg("skin", [(0, "#FFF3EA"), (1, "#F2D2C2")]) +
        "".join(rg(f"pg_{k}", [(0, a), (0.6, b), (1, c)], 0.4, 0.38, 0.7) for k, (a, b, c) in COL.items()) +
        lg("musc", [(0, "#F7B5B0"), (1, "#D9726C")]) + lg("ring", [(0, "#4A4E5A"), (1, "#16181F")]) +
        f'<clipPath id="lens"><circle cx="{CX}" cy="{CY}" r="{R}"/></clipPath>')
o = [header(defs, W, H)]


def blob(cx, cy, r, seed, n=14, j=0.16):
    random.seed(seed)
    pts = []
    for k in range(n):
        a = 2 * math.pi * k / n
        rr = r * (1 + random.uniform(-j, j))
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return smooth(pts, closed=True)


def chromato(cx, cy, r, kind, seed, open_=True, muscles=True):
    s = ""
    if muscles and open_:
        for k in range(10):
            a = 2 * math.pi * k / 10 + seed
            x1, y1 = cx + r * 1.02 * math.cos(a), cy + r * 1.02 * math.sin(a)
            x2, y2 = cx + r * 1.55 * math.cos(a), cy + r * 1.55 * math.sin(a)
            s += f'<path d="M {x1:.1f} {y1:.1f} L {x2:.1f} {y2:.1f}" stroke="#D9726C" stroke-width="{max(2, r * 0.12):.1f}" stroke-linecap="round" opacity="0.8"/>'
    s += f'<path d="{blob(cx, cy, r, seed)}" fill="url(#pg_{kind})" stroke="{INK}" stroke-width="{min(7, max(2.5, r * 0.1)):.1f}" stroke-linejoin="round"/>'
    if open_ and r > 18:
        random.seed(seed + 1)
        for _ in range(int(r / 4)):
            a, d = random.uniform(0, 6.28), random.uniform(0, r * 0.75)
            s += f'<circle cx="{cx + d * math.cos(a):.1f}" cy="{cy + d * math.sin(a):.1f}" r="{random.uniform(1.5, 3.2):.1f}" fill="{COL[kind][2]}" opacity="0.55"/>'
        s += f'<path d="M {cx - r * 0.5:.1f} {cy - r * 0.35:.1f} Q {cx - r * 0.2:.1f} {cy - r * 0.62:.1f} {cx + r * 0.2:.1f} {cy - r * 0.55:.1f}" fill="none" stroke="#FFFFFF" stroke-width="{max(2, r * 0.1):.1f}" stroke-linecap="round" opacity="0.6"/>'
    return s


# sombra del visor
o.append(f'<circle cx="{CX + 14}" cy="{CY + 18}" r="{R + 22}" fill="#000" opacity="0.28"/>')
o.append(f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="url(#skin)"/>')
# ---------- vista general: muchos cromatóforos ----------
V = [f'<g id="vista"><g clip-path="url(#lens)">']
random.seed(11)
placed = []
SPECIAL = {"am": (640, 250), "ro": (660, 420), "ma": (600, 590)}
for kind, (x, y) in SPECIAL.items():
    placed.append((x, y, 40, kind, True))
tries = 0
while len(placed) < 70 and tries < 5000:
    tries += 1
    x, y = random.uniform(CX - R, CX + R), random.uniform(CY - R, CY + R)
    if (x - CX) ** 2 + (y - CY) ** 2 > (R + 20) ** 2:
        continue
    op = random.random() < 0.55
    r = random.uniform(24, 38) if op else random.uniform(7, 11)
    if any(math.hypot(x - a, y - b) < (r + rb) * (1.55 if (op or ob) else 1.3) for a, b, rb, _, ob in placed):
        continue
    kind = random.choice(["am", "am", "ro", "ro", "ma"])
    placed.append((x, y, r, kind, op))
# capilares tenues
V.append('<g stroke="#E7B3A6" stroke-width="3" fill="none" opacity="0.7"><path d="M 140 300 C 260 280, 360 340, 480 300 S 700 240, 820 280"/><path d="M 150 560 C 280 520, 400 600, 520 560 S 720 500, 800 540"/></g>')
for i, (x, y, r, kind, op) in enumerate(placed):
    V.append(chromato(x, y, r, kind, i * 0.7, op))
V.append('</g></g>')
o.append("".join(V))
# ---------- detalle: un cromatóforo ----------
DX, DY = CX, CY - 10
def muscles(r_in, r_out, w):
    s = ""
    for k in range(14):
        a = 2 * math.pi * k / 14 + 0.1
        ca, sa = math.cos(a), math.sin(a)
        x1, y1, x2, y2 = DX + r_in * ca, DY + r_in * sa, DX + r_out * ca, DY + r_out * sa
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        px, py = -sa * w / 2, ca * w / 2
        d = f"M {x1:.1f} {y1:.1f} Q {mx + px:.1f} {my + py:.1f} {x2:.1f} {y2:.1f} Q {mx - px:.1f} {my - py:.1f} {x1:.1f} {y1:.1f} Z"
        s += f'<path d="{d}" fill="url(#musc)" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
        s += f'<path d="M {x1 + (x2 - x1) * 0.2:.1f} {y1 + (y2 - y1) * 0.2:.1f} L {x1 + (x2 - x1) * 0.8:.1f} {y1 + (y2 - y1) * 0.8:.1f}" stroke="#FFFFFF" stroke-width="2" opacity="0.5"/>'
        s += f'<circle cx="{x2:.1f}" cy="{y2:.1f}" r="5" fill="#C9605A" stroke="{INK}" stroke-width="3"/>'
    return s
o.append(f'<g id="relajado">{muscles(50, 278, 40)}<path d="{blob(DX, DY, 52, 3, 16, 0.12)}" fill="url(#pg_ro)" stroke="{INK}" stroke-width="6"/>'
         f'<path d="M {DX - 26} {DY - 18} Q {DX - 8} {DY - 34} {DX + 14} {DY - 30}" stroke="#FFFFFF" stroke-width="5" fill="none" stroke-linecap="round" opacity="0.6"/>'
         f'<path d="M {DX - 30} {DY + 10} q 14 -8 26 0 M {DX + 4} {DY + 22} q 12 -6 22 2" stroke="{INK}" stroke-width="3" fill="none" opacity="0.5"/></g>')
o.append(f'<g id="contraido">{muscles(178, 278, 64)}' + chromato(DX, DY, 182, "ro", 5, True, False) + '</g>')
# nervio
NV = f"M 40 790 C 120 720, 170 680, 230 640"
br = [f"M 230 640 C 250 610, 262 590, {DX + 278 * math.cos(2 * math.pi * 6 / 14 + 0.1) + 8:.0f} {DY + 278 * math.sin(2 * math.pi * 6 / 14 + 0.1) - 4:.0f}",
      f"M 230 640 C 280 640, 320 650, {DX + 278 * math.cos(2 * math.pi * 4 / 14 + 0.1) - 6:.0f} {DY + 278 * math.sin(2 * math.pi * 4 / 14 + 0.1) + 6:.0f}"]
o.append('<g id="nervio">' + dbl(NV, 12, "#FFD23F", 8) + "".join(dbl(b, 7, "#FFD23F", 7) for b in br) + '</g>')
o.append(f'<g id="impulso"><circle cx="70" cy="766" r="13" fill="{LIME}" stroke="{INK}" stroke-width="4"/><circle cx="70" cy="766" r="22" fill="none" stroke="{LIME}" stroke-width="4" opacity="0.6"/></g>')
# aro del visor (encima)
o.append(f'<circle cx="{CX}" cy="{CY}" r="{R + 12}" fill="none" stroke="url(#ring)" stroke-width="26"/>')
o.append(f'<circle cx="{CX}" cy="{CY}" r="{R + 26}" fill="none" stroke="{INK}" stroke-width="6"/><circle cx="{CX}" cy="{CY}" r="{R - 1}" fill="none" stroke="{INK}" stroke-width="5"/>')
o.append(f'<path d="M {CX - R * 0.62:.0f} {CY - R * 0.72:.0f} A {R - 30} {R - 30} 0 0 1 {CX + R * 0.1:.0f} {CY - R + 28:.0f}" fill="none" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round" opacity="0.45"/>')
# etiquetas de colores (vista)
for gid, txt_, (x, y), ly in (("l_am", "AMARILLO", SPECIAL["am"], 170), ("l_ro", "ROJO", SPECIAL["ro"], 420), ("l_ma", "MARRÓN", SPECIAL["ma"], 670)):
    s, _ = tag(gid, 900, ly, txt_, size=28)
    s = s.replace(f'<g id="{gid}">', f'<g id="{gid}"><line x1="{900 - 70}" y1="{ly}" x2="{x + 30}" y2="{y}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/><circle cx="{x + 30}" cy="{y}" r="8" fill="{LIME}" stroke="{INK}" stroke-width="4"/>')
    o.append(s)
s, _ = tag("l_cro", CX, 780, "CROMATÓFOROS", size=30)
o.append(s)
# etiquetas del detalle
for gid, txt_, ly, tx, ty in (("l_pig", "PIGMENTO", 150, DX + 40, DY - 30), ("l_mus", "MÚSCULO", 470, DX + 228 * math.cos(0.1 + 2 * math.pi / 14), DY + 228 * math.sin(0.1 + 2 * math.pi / 14))):
    s, _ = tag(gid, 900, ly, txt_, size=28)
    s = s.replace(f'<g id="{gid}">', f'<g id="{gid}"><line x1="{900 - 80}" y1="{ly}" x2="{tx}" y2="{ty}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/><circle cx="{tx}" cy="{ty}" r="8" fill="{LIME}" stroke="{INK}" stroke-width="4"/>')
    o.append(s)
s, _ = tag("l_ner", 250, 790, "NERVIO", size=28)
s = s.replace('<g id="l_ner">', f'<g id="l_ner"><line x1="210" y1="761" x2="168" y2="716" stroke="{INK}" stroke-width="5" stroke-linecap="round"/><circle cx="168" cy="716" r="8" fill="{LIME}" stroke="{INK}" stroke-width="4"/>')
o.append(s)
o.append('</svg>')
open("cromatoforo_free.svg", "w").write("\n".join(o))

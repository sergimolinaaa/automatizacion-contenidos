import sys, math, random
sys.path.insert(0, sys.path[0])
from seeds import *

CX, CY = 610, 285          # centro de la cabezuela (reloj)
RA, RB, RP = 24, 100, 46    # radio del receptáculo, longitud hasta el ápice, largo de los pelos

defs = "\n".join([
    lg("sky", [(0, "#6FB6EA"), (0.55, "#A9D8F7"), (1, "#E4F4FF")]),
    lg("hill1", [(0, "#CFEBD2"), (1, "#B6DFBC")]),
    lg("hill2", [(0, "#A6DA9E"), (1, "#86C77E")]),
    lg("meadow", [(0, "#62C164"), (1, "#2F8C42")]),
    lg("stem", [(0, "#8FBF5A"), (0.45, "#C9E39A"), (1, "#7FAE4B")], 0, 0, 1, 0),
    lg("leaf", [(0, "#5DBB4F"), (1, "#2E8A3A")]),
    rg("recep", [(0, "#A7884F"), (0.7, "#6F5530"), (1, "#4C3A20")], 0.4, 0.35, 0.7),
    rg("sun", [(0, "#FFFFFF", 0.95), (0.35, "#FFF6C8", 0.6), (1, "#FFF6C8", 0)]),
    rg("glow", [(0, "#FFFFFF", 0.55), (1, "#FFFFFF", 0)]),
    rg("flower", [(0, "#FFE45C"), (0.7, "#FFC61A"), (1, "#E89B00")], 0.45, 0.4, 0.6),
    DEFS_SEED,
])
o = [header(defs)]
o.append('<rect width="1000" height="700" fill="url(#sky)"/>')
o.append('<circle cx="930" cy="70" r="190" fill="url(#sun)"/>')
# nubes lejanas (sin contorno)
o.append('<g id="clouds" fill="#FFFFFF" opacity="0.75">'
         '<g><ellipse cx="760" cy="150" rx="80" ry="22"/><ellipse cx="800" cy="134" rx="48" ry="26"/><ellipse cx="740" cy="140" rx="36" ry="20"/></g>'
         '<g><ellipse cx="160" cy="330" rx="70" ry="16"/><ellipse cx="190" cy="318" rx="40" ry="20"/></g>'
         '<g opacity="0.8"><ellipse cx="440" cy="370" rx="60" ry="12"/><ellipse cx="465" cy="361" rx="30" ry="14"/></g></g>')
# colinas en capas
o.append('<path d="M 0 440 C 120 410, 250 425, 380 415 C 520 404, 640 430, 780 418 C 880 410, 950 420, 1000 416 L 1000 700 L 0 700 Z" fill="url(#hill1)"/>')
o.append('<g fill="#9FCFA2" opacity="0.8"><ellipse cx="150" cy="430" rx="34" ry="20"/><ellipse cx="185" cy="425" rx="22" ry="16"/><ellipse cx="840" cy="422" rx="30" ry="18"/></g>')
o.append('<path d="M 0 490 C 160 470, 300 488, 470 478 C 640 468, 820 492, 1000 474 L 1000 700 L 0 700 Z" fill="url(#hill2)"/>')
# reloj lejano (desenfocado, sin contorno)
far = []
rnd = random.Random(9)
for k in range(60):
    a = rnd.uniform(0, 2 * math.pi)
    far.append(f'M 860 455 L {860 + math.cos(a) * 30:.1f} {455 + math.sin(a) * 30:.1f}')
o.append(f'<path d="M 862 520 C 860 495, 858 470, 860 455" stroke="#7FAF66" stroke-width="4" fill="none"/>'
         f'<path d="{" ".join(far)}" stroke="#FFFFFF" stroke-width="2" opacity="0.75"/><circle cx="860" cy="455" r="31" fill="#FFFFFF" opacity="0.25"/>')
# flores amarillas a media distancia
def flower(x, y, r, stem_to, idn):
    s = f'<g id="{idn}">'
    s += dbl(f"M {x} {y + r * 0.3:.1f} C {x - 4} {y + 40}, {x + 6} {stem_to - 30}, {x + 2} {stem_to}", 5, "#6FB24A", 6)
    pet = []
    for k in range(22):
        a = 2 * math.pi * k / 22
        pet.append(f'<ellipse cx="{x + math.cos(a) * r * 0.62:.1f}" cy="{y + math.sin(a) * r * 0.38:.1f}" rx="{r * 0.42:.1f}" ry="{r * 0.13:.1f}" transform="rotate({math.degrees(a):.0f} {x + math.cos(a) * r * 0.62:.1f} {y + math.sin(a) * r * 0.38:.1f})" fill="url(#flower)"/>')
    s += f'<ellipse cx="{x}" cy="{y}" rx="{r + 4}" ry="{r * 0.62 + 4:.1f}" fill="{INK}"/>' + "".join(pet)
    s += f'<ellipse cx="{x}" cy="{y - 2}" rx="{r * 0.42:.1f}" ry="{r * 0.24:.1f}" fill="#FFD21F" stroke="#E0A000" stroke-width="2"/>'
    s += f'<ellipse cx="{x - r * 0.25:.1f}" cy="{y - r * 0.2:.1f}" rx="{r * 0.2:.1f}" ry="{r * 0.07:.1f}" fill="#FFFFFF" opacity="0.6"/></g>'
    return s

# prado cercano
o.append(f'<path d="M 0 560 C 180 540, 340 556, 520 548 C 700 540, 860 560, 1000 548 L 1000 700 L 0 700 Z" fill="url(#meadow)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
o.append('<path d="M 30 566 C 180 548, 330 562, 500 556" fill="none" stroke="#9BE08A" stroke-width="4" stroke-linecap="round" opacity="0.7"/>')
o.append(flower(170, 528, 22, 562, "fl1"))
o.append(flower(905, 520, 18, 552, "fl2"))
# hojas de diente de león (rosetas dentadas)
def leaf(base, tip, width, teeth, flip=1):
    bx, by = base
    tx, ty = tip
    L = math.hypot(tx - bx, ty - by)
    ux, uy = (tx - bx) / L, (ty - by) / L
    nx, ny = -uy, ux
    left, right = [], []
    for i in range(0, 41):
        t = i / 40
        w = width * math.sin(math.pi * min(1, t * 1.02)) ** 0.7 * (0.35 + 0.65 * t ** 0.8)
        tooth = 1 - 0.55 * ((t * teeth) % 1) if t > 0.15 else 1   # dientes hacia la base (runcinada)
        cx_, cy_ = bx + ux * L * t, by + uy * L * t
        left.append((cx_ + nx * w * tooth, cy_ + ny * w * tooth))
        right.append((cx_ - nx * w * tooth, cy_ - ny * w * tooth))
    outline = left + list(reversed(right))
    s = f'<path d="{poly(outline, True)}" fill="url(#leaf)" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    s += f'<path d="M {bx} {by} L {bx + ux * L * 0.92:.1f} {by + uy * L * 0.92:.1f}" stroke="#B7E39A" stroke-width="4" stroke-linecap="round"/>'
    return s

o.append('<g id="leaves">')
o.append(leaf((600, 720), (360, 610), 44, 5))
o.append(leaf((600, 720), (850, 600), 46, 5))
o.append(leaf((600, 720), (470, 585), 36, 4))
o.append(leaf((600, 720), (740, 580), 38, 4))
o.append('</g>')

# ---- reloj del diente de león
o.append('<g id="clock">')
# tallo hueco, saliendo de la roseta hasta el receptáculo
stem = f"M 598 700 C 590 600, 616 440, {CX} {CY + RA - 4}"
o.append(dbl(stem, 13, "url(#stem)", 8))
o.append(f'<path d="M 594 690 C 588 600, 610 450, {CX - 4} {CY + 40}" stroke="#E6F4C4" stroke-width="3" fill="none" opacity="0.8"/>')
# brácteas reflejas (colgando bajo la cabezuela)
br = []
for k, ang in enumerate([-70, -40, -12, 14, 42, 68]):
    a = math.radians(ang)
    x0, y0 = CX + math.sin(a) * 12, CY + 18
    x1, y1 = x0 + math.sin(a) * 26, y0 + 52 - abs(ang) * 0.25
    br.append(dbl(f"M {x0:.1f} {y0:.1f} Q {x0 + math.sin(a) * 30:.1f} {y0 + 6:.1f} {x1:.1f} {y1:.1f}", 6, "#6FA548", 5))
o.append("".join(br))

o.append(f'<circle cx="{CX}" cy="{CY}" r="{RB + RP + 10}" fill="url(#glow)"/>')
# semillas sobre una esfera (Fibonacci), con un hueco arriba a la izquierda (ya volaron)
rnd = random.Random(5)
N = 104
gapdir = (-0.72, 0.62, 0.3)
gl = math.sqrt(sum(c * c for c in gapdir)); gapdir = tuple(c / gl for c in gapdir)
seeds = []
for i in range(N):
    yv = 1 - 2 * (i + 0.5) / N
    r = math.sqrt(1 - yv * yv)
    th = i * math.pi * (3 - math.sqrt(5))
    d = (math.cos(th) * r, yv, math.sin(th) * r)
    if sum(a * b for a, b in zip(d, gapdir)) > 0.62:
        continue
    if d[1] < -0.8:
        continue
    seeds.append(d)
seeds.sort(key=lambda d: d[2])

def basis(d):
    a = (0, 0, 1) if abs(d[2]) < 0.9 else (1, 0, 0)
    u = (d[1] * a[2] - d[2] * a[1], d[2] * a[0] - d[0] * a[2], d[0] * a[1] - d[1] * a[0])
    ul = math.sqrt(sum(c * c for c in u)); u = tuple(c / ul for c in u)
    v = (d[1] * u[2] - d[2] * u[1], d[2] * u[0] - d[0] * u[2], d[0] * u[1] - d[1] * u[0])
    return u, v

def S(p):  # proyección ortográfica
    return CX + p[0], CY - p[1]

back_fil, front_fil, beaks_b, beaks_f, ach = [], [], [], [], []
for d in seeds:
    apex = tuple(c * RB for c in d)
    base = tuple(c * (RA + 14) for c in d)
    root = tuple(c * RA for c in d)
    u, v = basis(d)
    fl = []
    for k in range(13):
        psi = 2 * math.pi * k / 13 + rnd.uniform(-0.15, 0.15)
        a = math.radians(rnd.uniform(70, 84))
        L = RP * rnd.uniform(0.85, 1.05)
        dirv = tuple(math.cos(a) * d[j] + math.sin(a) * (math.cos(psi) * u[j] + math.sin(psi) * v[j]) for j in range(3))
        tip = tuple(apex[j] + dirv[j] * L for j in range(3))
        p0, p1 = S(apex), S(tip)
        fl.append(f"M {p0[0]:.1f} {p0[1]:.1f} L {p1[0]:.1f} {p1[1]:.1f}")
    (front_fil if d[2] >= -0.15 else back_fil).append(" ".join(fl))
    b0, b1 = S(base), S(apex)
    (beaks_f if d[2] >= -0.15 else beaks_b).append(f"M {b0[0]:.1f} {b0[1]:.1f} L {b1[0]:.1f} {b1[1]:.1f}")
    r0, r1 = S(root), S(base)
    if d[2] > -0.2:
        ach.append((d[2], r0, r1))

o.append(f'<path d="{" ".join(back_fil)}" stroke="#7F9AB6" stroke-width="3" opacity="0.45" fill="none" stroke-linecap="round"/>')
o.append(f'<path d="{" ".join(back_fil)}" stroke="#F3F8FF" stroke-width="1.3" opacity="0.8" fill="none" stroke-linecap="round"/>')
o.append(f'<path d="{" ".join(beaks_b)}" stroke="#D8D2B8" stroke-width="1.8" opacity="0.8" fill="none"/>')
# receptáculo (se ve por el hueco)
o.append(f'<circle cx="{CX}" cy="{CY}" r="{RA + 2}" fill="url(#recep)" stroke="{INK}" stroke-width="5"/>')
pits = []
for k in range(26):
    a = rnd.uniform(0, 2 * math.pi); rr = rnd.uniform(4, RA - 6)
    pits.append(f'<circle cx="{CX + math.cos(a) * rr:.1f}" cy="{CY + math.sin(a) * rr:.1f}" r="1.8"/>')
o.append('<g fill="#3A2A14" opacity="0.7">' + "".join(pits) + "</g>")
o.append(f'<ellipse cx="{CX - 8}" cy="{CY - 10}" rx="9" ry="5" fill="#D8C08A" opacity="0.6"/>')
# aquenios pegados al receptáculo (los de delante)
for z, r0, r1 in sorted(ach):
    o.append(f'<path d="M {r0[0]:.1f} {r0[1]:.1f} L {r1[0]:.1f} {r1[1]:.1f}" stroke="{INK}" stroke-width="6.5" stroke-linecap="round"/>'
             f'<path d="M {r0[0]:.1f} {r0[1]:.1f} L {r1[0]:.1f} {r1[1]:.1f}" stroke="#8A6A3C" stroke-width="3.5" stroke-linecap="round"/>')
o.append(f'<path d="{" ".join(beaks_f)}" stroke="#6E7F90" stroke-width="3.6" opacity="0.6" fill="none" stroke-linecap="round"/>')
o.append(f'<path d="{" ".join(beaks_f)}" stroke="#F4EFDC" stroke-width="1.8" fill="none" stroke-linecap="round"/>')
o.append(f'<path d="{" ".join(front_fil)}" stroke="#5E7086" stroke-width="3.6" opacity="0.55" fill="none" stroke-linecap="round"/>')
o.append(f'<path d="{" ".join(front_fil)}" stroke="#FFFFFF" stroke-width="1.7" fill="none" stroke-linecap="round"/>')
o.append('</g>')

# brisa (líneas de viento hacia la izquierda)
o.append('<g id="wind" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" opacity="0.8">'
         '<path d="M 520 150 C 470 140, 420 160, 360 150"/><path d="M 470 460 C 400 450, 330 470, 260 455"/><path d="M 900 300 C 850 290, 820 305, 780 300"/></g>')
# semillas volando
o.append('<g id="fs1">' + side_seed(300, 225, 1.45, rot=-14, n=38, seed=11, barbs=0) + '</g>')
o.append('<g id="fs2">' + side_seed(150, 420, 1.0, rot=8, n=34, seed=12) + '</g>')
o.append('<g id="fs3">' + side_seed(470, 105, 0.78, rot=-22, n=30, seed=13) + '</g>')
o.append('<g id="fs4">' + side_seed(95, 275, 0.66, rot=16, n=28, seed=14) + '</g>')


# sensor sin batería inspirado en el vilano (Iyer et al., Nature 2022): paracaídas de tiras de poliimida + placa solar
SX0, SY0 = 860, 175
sl = pappus_lines(SX0, SY0, 62, n=28, theta=10, elev=22, rot=6, seed=40, curl=0.05, jitter=False)
sb, sf = fil_svg(sl, w=3.4, edge=6.4, col="#F2A93B", edgecol=INK, back_op=0.8)
hub2 = (SX0 + 9, SY0 + 70)
o.append('<g id="sensor">' + sb +
         f'<path d="M {SX0} {SY0} L {hub2[0]} {hub2[1]}" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
         f'<path d="M {SX0} {SY0} L {hub2[0]} {hub2[1]}" stroke="#F2A93B" stroke-width="3" stroke-linecap="round"/>'
         f'<g transform="rotate(6 {hub2[0]} {hub2[1]})"><rect x="{hub2[0] - 26}" y="{hub2[1]}" width="52" height="30" rx="4" fill="#2E8B57" stroke="{INK}" stroke-width="5"/>'
         f'<rect x="{hub2[0] - 18}" y="{hub2[1] + 6}" width="22" height="18" fill="#1F3A7A" stroke="{INK}" stroke-width="2"/>'
         f'<path d="M {hub2[0] - 18} {hub2[1] + 12} L {hub2[0] + 4} {hub2[1] + 12} M {hub2[0] - 18} {hub2[1] + 18} L {hub2[0] + 4} {hub2[1] + 18} M {hub2[0] - 7} {hub2[1] + 6} L {hub2[0] - 7} {hub2[1] + 24}" stroke="#7FA6FF" stroke-width="1.5"/>'
         f'<rect x="{hub2[0] + 9}" y="{hub2[1] + 8}" width="11" height="9" fill="#111" stroke="#C9A227" stroke-width="2"/>'
         f'<circle cx="{hub2[0] + 14}" cy="{hub2[1] + 23}" r="3" fill="#FFD34D"/></g>'
         + sf + f'<circle cx="{SX0}" cy="{SY0}" r="5" fill="#F2A93B" stroke="{INK}" stroke-width="3"/></g>')
t, box = tag("lsensor", 866, 362, "SIN BATERÍA", target=(hub2[0] - 4, hub2[1] + 32), anchor_from=(870, 333))
o.append(t)

t, box = tag("lpara", 215, 108, "PARACAÍDAS", target=(262, 182), anchor_from=(230, 130))
o.append(t)
o.append('</svg>')
open(sys.argv[1], "w").write("\n".join(o))

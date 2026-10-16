import sys; sys.path.insert(0, "../tools")
from tofull import tofull
back = ('<g opacity="0.9"><rect x="80" y="120" width="920" height="300" rx="10" fill="#C9D8E4"/>' +
        "".join(f'<circle cx="{x}" cy="{y}" r="6" fill="#AFC1D0"/>' for x in range(120, 980, 48) for y in range(150, 400, 48)) +
        '<g fill="#B7C7D4"><path d="M 160 170 L 380 170 L 380 230 L 200 250 Z"/><rect x="380" y="180" width="60" height="30" rx="8"/>'
        '<rect x="520" y="160" width="16" height="140" rx="7"/><circle cx="528" cy="152" r="20"/><rect x="640" y="200" width="160" height="26" rx="10"/><rect x="700" y="150" width="26" height="140" rx="6"/>'
        '<path d="M 860 160 L 930 160 L 915 320 L 875 320 Z"/></g></g>'
        '<g stroke="#5E3A1C" stroke-width="3" opacity="0.4">' + "".join(f'<line x1="0" y1="{y}" x2="1080" y2="{y}"/>' for y in (1300, 1420, 1560, 1720, 1860)) + '</g>')
tofull("metro.svg", "metro_full.svg", "#EAF2F8", "#7E5029", back)

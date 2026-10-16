from dib import *
o = [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 700">
<defs>{DEFS}
<linearGradient id="wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFF4E2"/><stop offset="1" stop-color="#FBE2C2"/></linearGradient>
<linearGradient id="floor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E2BE8C"/><stop offset="1" stop-color="#C99A62"/></linearGradient>
<linearGradient id="glass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#E4F4FF"/><stop offset="1" stop-color="#B5D6EE"/></linearGradient>
<linearGradient id="wood" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#C98B55"/><stop offset="0.5" stop-color="#E2AD74"/><stop offset="1" stop-color="#A86C3C"/></linearGradient>
<clipPath id="mc"><rect x="584" y="92" width="312" height="520" rx="14"/></clipPath>
</defs>
<rect width="1000" height="700" fill="url(#wall)"/>
<rect y="470" width="1000" height="230" fill="url(#floor)"/>
<g stroke="#B8895A" stroke-width="2.5" opacity="0.5"><line x1="0" y1="530" x2="1000" y2="530"/><line x1="0" y1="600" x2="1000" y2="600"/><line x1="150" y1="470" x2="150" y2="530"/><line x1="420" y1="530" x2="420" y2="600"/></g>
<rect x="0" y="456" width="1000" height="16" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/>
<ellipse cx="740" cy="642" rx="200" ry="14" fill="{INK}" opacity="0.18"/>
''']
# espejo de pie
o.append(f'<rect x="562" y="70" width="356" height="566" rx="26" fill="url(#wood)" stroke="{INK}" stroke-width="7"/>')
o.append(f'<rect x="584" y="92" width="312" height="520" rx="14" fill="url(#glass)" stroke="{INK}" stroke-width="5"/>')
o.append('<g clip-path="url(#mc)">')
o.append('<rect x="584" y="470" width="312" height="150" fill="#D9C3A0" opacity="0.7"/><rect x="584" y="458" width="312" height="12" fill="#F2F6FA"/>')
o.append(f'<g id="reflejo"><g transform="translate(760 600) scale(-0.86 0.86)">{baby(uid="r", arms="touch", hand=(90, -278), k=1/0.86)}'
         f'<circle cx="70" cy="-299" r="7" fill="{CORAL}" stroke="{INK}" stroke-width="3"/></g></g>')
o.append('<rect x="584" y="92" width="312" height="520" fill="#CFEAFF" opacity="0.22"/>')
o.append('<path d="M 600 300 L 720 110 L 760 110 L 640 300 Z M 820 610 L 890 480 L 890 530 L 850 610 Z" fill="#FFFFFF" opacity="0.45"/>')
o.append('</g>')
o.append(f'<rect x="590" y="636" width="22" height="16" fill="#8E5A30" stroke="{INK}" stroke-width="4"/><rect x="868" y="636" width="22" height="16" fill="#8E5A30" stroke="{INK}" stroke-width="4"/>')
# bebé real
o.append(f'<g id="bebe"><g transform="translate(330 616)">{baby(uid="e", arms="touch", hand=(90, -278))}'
         f'<g id="dot"><circle cx="70" cy="-299" r="7" fill="{CORAL}" stroke="{INK}" stroke-width="3"/></g></g></g>')
# etiquetas
o.append(tag("lmancha", 610, 0 + 120, 260, "MANCHA ROJA", 740, 178, 678, 322, bg=INK, fg=LIME))
o.append(f'<g id="yo"><path d="M 230 146 L 460 146 Q 480 146 480 166 L 480 214 Q 480 234 460 234 L 380 234 L 362 262 L 340 234 L 230 234 Q 210 234 210 214 L 210 166 Q 210 146 230 146 Z" fill="#FFFFFF" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
         f'<text x="345" y="204" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="40" fill="{INK}">¡SOY YO!</text></g>')
# mini carrito superado
o.append(f'<g id="minicarro"><rect x="20" y="300" width="180" height="140" rx="18" fill="#FFFFFF" stroke="{INK}" stroke-width="6"/>'
         f'<g transform="translate(14 270) scale(0.42)">{cart(60, 120, k=2.2, uid="mc", items=False)}</g>'
         f'<circle cx="172" cy="318" r="30" fill="{LIME}" stroke="{INK}" stroke-width="5"/><path d="M 158 318 L 168 330 L 186 306" fill="none" stroke="{INK}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/></g>')
o.append('</svg>')
open("espejo.svg", "w").write("\n".join(o))

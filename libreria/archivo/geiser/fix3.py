s=open('corte.py').read()
s=s.replace('''o.append('<g fill="url(#magma)" stroke="#0B0B14" stroke-width="5">''','''o.append('<g transform="translate(0 -34)"><g fill="url(#magma)" stroke="#0B0B14" stroke-width="5">''')
s=s.replace('''<ellipse cx="720" cy="676" rx="50" ry="9"/></g>')''','''<ellipse cx="720" cy="676" rx="50" ry="9"/></g></g>')''')
s=s.replace('label("lmagma", 200, 588, "MAGMA", line_to=(300, 646))','label("lmagma", 200, 560, "MAGMA", line_to=(300, 616))')
open('corte.py','w').write(s)
s=open('guion_geiser.py').read()
s=s.replace('''         cam(520, 380, 1.3),
         A("spill", "punch", "Pesa"''','''         cam(520, 300, 1.3),
         A("spill", "punch", "Pesa"''')
s=s.replace('''A("boil", "pop", "hierve", sfx="burbujas"),''','''cam(520, 440, 1.3, "hierve", dur=0.6), A("boil", "pop", "hierve", sfx="burbujas"),''')
s=s.replace('''cam(800, 590, 1.5, "Faithful"), A("people", "punch", "erupción", amount=0.6),''','''cam(520, 330, 1.4, "Faithful"), A("jet", "punch", "erupción", amount=0.6), A("people", "punch", "erupción", amount=0.6),''')
open('guion_geiser.py','w').write(s)

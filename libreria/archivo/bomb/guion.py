import json
D="/home/user/automatizacion-contenidos/content/lote2-01-escarabajo-bombardero/"
old=json.load(open("/tmp/claude-0/-home-user-automatizacion-contenidos/039df981-7a17-5355-b711-18510fb209db/scratchpad/bomb/old_guion.json"))
def A(t,e,**k):
    d={"target":t,"effect":e}; d.update(k); return d
scenes=[
 {"chapter":0,"headline":"Dispara *spray hirviendo*",
  "narration":"Si molestas a este escarabajo, te dispara un chorro a cien grados.",
  "illustration":{"svg_file":"escena.svg","caption":"Fig. 1 · Escarabajo bombardero","anims":[
   A("grassl","sway",origin="bottom",amount=0.5),A("grassr","sway",origin="bottom",amount=-0.4),
   A("antennae","wiggle",origin="right",amount=0.35),A("antant","wiggle",origin="bottom-right",amount=0.8),
   A("beetle","breathe",amount=0.3),
   A("ant","move",to=[-60,0],trigger="molestas",dur=0.8),
   A("beetle","punch",trigger="escarabajo"),
   A("abdtip","move",rotate=25,origin="left",trigger="dispara",dur=0.35),
   A("spray","fade",trigger="chorro",dur=0.15,sfx="chorro"),A("spray","pulse",trigger="chorro",amount=0.6),
   A("mist","pop",trigger="chorro",sfx="none"),
   A("camera","zoom",to=[690,450],amount=1.6,trigger="chorro",dur=0.6),
   A("steam","pop",trigger="cien",sfx="burbujas"),A("steam","float",amount=0.4),
   A("heat","draw",trigger="grados",dur=0.4),A("hot","pop",trigger="grados",sfx="sello"),
   A("alarm","pop",trigger="grados",sfx="none"),
   A("camera","zoom",to=[500,350],amount=1,trigger="grados",dur=0.7)]}},
 {"chapter":0,"signature":True,"headline":"El truco es…","narration":"El truco es…"},
 {"chapter":1,"number":"1","headline":"Un *depósito* químico",
  "narration":"Dentro del abdomen guarda un depósito de hidroquinonas y agua oxigenada. Juntas, pero tranquilas: sin ayuda, casi no reaccionan.",
  "illustration":{"svg_file":"corte.svg","caption":"Fig. 2 · Su arsenal","anims":[
   A("flow","hide"),A("lval","hide"),A("lcam","hide"),A("lenz","hide"),
   A("glands","pulse",amount=0.6),A("mols","shake",amount=0.15),A("reservoir","breathe",amount=0.6),
   A("antennae","wiggle",origin="right",amount=0.3),
   A("camera","zoom",to=[620,300],amount=1.35,trigger="abdomen",dur=0.8),
   A("lres","pop",trigger="depósito",sfx="pop"),A("reservoir","punch",trigger="depósito"),
   A("camera","zoom",to=[500,350],amount=1,trigger="hidroquinonas",dur=0.7),
   A("lhq","pop",trigger="hidroquinonas"),A("lh2o2","pop",trigger="oxigenada"),
   A("mols","punch",trigger="tranquilas",amount=0.8)]},
  "mascot":{"trigger":"tranquilas","pose":"think","note":"Tranquilas… de momento","side":"right"}},
 {"chapter":2,"number":"2","headline":"La cámara *de reacción*",
  "narration":"Cuando le atacan, abre una válvula y el líquido pasa a una cámara llena de enzimas.",
  "illustration":{"svg_file":"corte.svg","caption":"Fig. 3 · La válvula","anims":[
   A("lhq","hide"),A("lh2o2","hide"),
   A("glands","pulse",amount=0.6),A("mols","shake",amount=0.15),A("reservoir","breathe",amount=0.6),
   A("antennae","wiggle",origin="right",amount=0.3),
   A("camera","zoom",to=[760,300],amount=1.85,trigger="atacan",dur=0.8),A("lres","hide",trigger="atacan"),
   A("valvetop","move",to=[0,-5],trigger="abre",dur=0.3),A("valvebot","move",to=[0,5],trigger="abre",dur=0.3),
   A("lval","pop",trigger="válvula",sfx="pop"),
   A("flow","draw",trigger="líquido",dur=0.7,sfx="chorro"),
   A("lcam","pop",trigger="cámara"),A("chamber","punch",trigger="cámara"),
   A("enzymes","punch",trigger="enzimas",amount=1.2),A("lenz","pop",trigger="enzimas",sfx="ding")]}},
 {"chapter":2,"number":"2","headline":"*Hierve* de golpe",
  "narration":"Las enzimas disparan la reacción: el líquido se calienta hasta unos cien grados.",
  "illustration":{"svg_file":"camara.svg","caption":"Fig. 4 · Cámara de reacción","anims":[
   A("press","hide"),A("pulses","hide"),A("lval","hide"),A("ldep","hide"),
   A("flowlines","flow",amount=0.8),A("mols","shake",amount=0.2),A("reservoir","breathe",amount=0.5),
   A("camera","zoom",to=[628,370],amount=1.15),
   A("enzymes","punch",trigger="enzimas",amount=1.2),A("lenz","pop",trigger="enzimas",sfx="pop"),
   A("bubbles","pop",trigger="reacción",sfx="burbujas"),A("bubbles","float",amount=0.3),
   A("chamber","shake",trigger="reacción",amount=0.3),
   A("glow","fade",trigger="calienta",dur=0.8),A("mercury","grow",trigger="calienta"),
   A("camera","zoom",to=[760,260],amount=1.4,trigger="cien",dur=0.7),
   A("l100","pop",trigger="cien",sfx="ding"),A("lenz","hide",trigger="cien"),A("thermo","punch",trigger="grados")]}},
 {"chapter":3,"number":"3","headline":"Dispara *a ráfagas*",
  "narration":"La presión lo expulsa, la válvula se cierra… y vuelta a empezar: unas quinientas ráfagas por segundo.",
  "illustration":{"svg_file":"camara.svg","caption":"Fig. 5 · Ametralladora química","anims":[
   A("ldep","hide"),A("lenz","hide"),
   A("bubbles","float",amount=0.3),A("chamber","shake",amount=0.3),A("mols","shake",amount=0.2),
   A("press","pop",trigger="presión",sfx="whoosh"),A("press","pulse",trigger="presión",amount=1.2),
   A("pulses","pop",trigger="expulsa",sfx="chasquido"),
   A("p1","ripple",trigger="expulsa",phase=0.0),A("p2","ripple",trigger="expulsa",phase=0.33),A("p3","ripple",trigger="expulsa",phase=0.66),
   A("camera","zoom",to=[450,330],amount=1.3,trigger="válvula",dur=0.6),
   A("lval","pop",trigger="válvula"),
   A("valvetop","move",to=[0,16],trigger="cierra",dur=0.25,sfx="chasquido"),A("valvebot","move",to=[0,-16],trigger="cierra",dur=0.25),
   A("flow","hide",trigger="cierra"),
   A("valvetop","move",to=[0,-16],trigger="vuelta",dur=0.25),A("valvebot","move",to=[0,16],trigger="vuelta",dur=0.25),
   A("flow","fade",trigger="vuelta",dur=0.3),
   A("camera","zoom",to=[500,350],amount=1,trigger="quinientas",dur=0.6),
   A("pulses","punch",trigger="ráfagas")]},
  "elements":[{"type":"stat","label":"Ráfagas por segundo","value":500,"from":0,"trigger":"quinientas"}]},
 {"chapter":3,"number":"3","headline":"*Apunta* con el culo",
  "narration":"Y gira la punta del abdomen para apuntar donde quiera: delante, de lado o hacia atrás.",
  "illustration":{"svg_file":"apunta.svg","caption":"Fig. 6 · Vista desde arriba","anims":[
   A("antennae","wiggle",origin="left",amount=0.3),
   A("tip","punch",trigger="gira",amount=1.2,sfx="boing"),
   A("camera","zoom",to=[650,330],amount=1.4,trigger="punta",dur=0.7),
   A("camera","zoom",to=[500,350],amount=1,trigger="donde",dur=0.7),
   A("tip","hide",trigger="delante"),A("tipdel","pop",trigger="delante"),
   A("jfront","fade",trigger="delante",dur=0.25,sfx="chorro"),A("ldel","pop",trigger="delante",sfx="none"),
   A("tipdel","hide",trigger="lado"),A("ldel","hide",trigger="lado"),A("jfront","hide",trigger="lado"),
   A("tip","fade",trigger="lado",dur=0.2),A("tip","move",rotate=70,origin="left",trigger="lado",dur=0.3),
   A("jside","fade",trigger="lado",dur=0.25,sfx="chorro"),A("llado","pop",trigger="lado",sfx="none"),
   A("tip","move",rotate=-70,origin="left",trigger="atrás",dur=0.3),A("jside","hide",trigger="atrás"),A("llado","hide",trigger="atrás"),
   A("jback","fade",trigger="atrás",dur=0.25,sfx="chorro"),A("latras","pop",trigger="atrás",sfx="none")]}},
 {"chapter":4,"number":"+","headline":"Ni *tragado* se rinde",
  "narration":"Y si un sapo se lo traga, le dispara desde dentro… en pleno estómago.",
  "elements":[{"type":"list","label":"Mal plan para el sapo","trigger":"sapo","items":[
     {"text":"Se lo traga","trigger":"traga"},
     {"text":"Recibe un chorro hirviendo","trigger":"dispara"},
     {"text":"…en el estómago","trigger":"estómago"}]}],
  "mascot":{"trigger":"estómago","pose":"surprise","note":"Mala digestión","side":"right"}},
 {"chapter":4,"number":"+","headline":"*Vomitado*, pero vivo",
  "narration":"En un experimento, el 43 % de los sapos lo vomitó, y esos escarabajos salieron vivos. Alguno, tras más de hora y media dentro.",
  "elements":[
   {"type":"stat","label":"Sapos que lo vomitaron","value":43,"from":0,"unit":"%","note":"y todos esos escarabajos, vivos","trigger":"vomitó"},
   {"type":"fact","label":"Récord","text":"Hasta 107 minutos dentro del sapo","tone":"accent","trigger":"hora"}]},
 {"chapter":5,"number":"TÚ","headline":"*Confiesa*",
  "narration":"Sinceramente: ¿a quién apuntarías tú con el spray? Te leo.",
  "elements":[{"type":"ask","text":"¿A quién *apuntarías* tú con el spray?","trigger":"Sinceramente"}]}
]
g={k:old[k] for k in ("topic","categoria","title","source","chapters","outro_cta","cover","publish")}
g["publish"]["description"]=("El escarabajo bombardero guarda hidroquinonas y agua oxigenada en un depósito del abdomen. Cuando le atacan, "
 "abre una válvula y las pasa a una cámara de reacción llena de enzimas: la mezcla se calienta hasta unos 100 °C y sale disparada "
 "a ráfagas, unas 500 por segundo, hacia donde apunte la punta del abdomen. En un experimento, el 43 % de los sapos que se lo tragaron lo vomitaron, y esos escarabajos salieron vivos. "
 "Fuentes: Eisner; Arndt et al., Science (2015); Sugiura & Sato, Biology Letters (2018).")
g["scenes"]=scenes
# comprobación de triggers
import re
for i,s in enumerate(scenes):
    words=set(re.findall(r"[\wáéíóúñüÁÉÍÓÚÑ%]+",s["narration"]))
    trig=[a.get("trigger") for a in s.get("illustration",{}).get("anims",[])]
    for e in s.get("elements",[]):
        trig.append(e.get("trigger")); trig+= [it.get("trigger") for it in e.get("items",[])]
    if s.get("mascot"): trig.append(s["mascot"]["trigger"])
    for t in trig:
        if t and t not in words: print("TRIGGER MALO", i, t)
print("palabras:", sum(len(s["narration"].split()) for s in scenes))
json.dump(g,open(D+"guion.json","w"),ensure_ascii=False,indent=2)

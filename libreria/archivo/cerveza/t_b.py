import sys; sys.path.insert(0,'.')
from lib import *
b1=Bottle(300,650,560,170); b2=Bottle(700,650,400,120)
print(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 700"><defs>{BOTTLE_DEFS}</defs><rect width="1000" height="700" fill="#EFE6D6"/>{b1.draw(liquid=b1.yl+40)}{b2.draw(cap=False)}<g>{foam_blob([(700,240),(680,215),(720,212),(700,185),(690,160),(712,140)],22)}</g></svg>')

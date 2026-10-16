import sys, re
import xml.etree.ElementTree as ET
for fn in sys.argv[1:]:
    root = ET.parse(fn).getroot()
    for el in root.iter():
        i = el.get("id")
        if i and el.tag.endswith("}g") or (i and not el.tag.endswith(("Gradient", "clipPath", "stop"))):
            if el.get("opacity") or el.get("transform"):
                print(fn, i, "opacity" if el.get("opacity") else "", "transform" if el.get("transform") else "")

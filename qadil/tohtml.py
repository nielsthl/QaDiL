import ADT
from HTML import HTML
import sys
import io
import os

filename = sys.argv[1]


infile = io.open(filename, "r", encoding="utf-8")

firstname, extension = os.path.splitext(filename)

doc = HTML(infile.read(), firstname)
doc.translate()
#for v in doc.tokens:
#    print(v)
#doc.tokenize()
#for v in doc.tokens:
#    print(v)
#print(doc.HTML())
#print(doc.macros)
s = doc.HTML()
print(s)



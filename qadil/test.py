import ADT
#from HTML import HTML
from Parser import Parser
import sys
import io
import os

filename = sys.argv[1]


infile = io.open(filename, "r", encoding="utf-8")

firstname, extension = os.path.splitext(filename)

#doc = HTML(infile.read(), firstname)
doc = Parser(infile.read())
#doc.translate()
#print(doc.obj)
doc.tokenize()
for t in doc.tokenlist:
    print(t)


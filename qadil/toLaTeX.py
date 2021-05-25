import ADT
from LaTeX import LaTeX
import sys
import io
import os

filename = sys.argv[1]


infile = io.open(filename, "r", encoding="utf-8")

firstname, extension = os.path.splitext(filename)

txt = infile.read()
#
# Hack below is disgusting. It overwrites the html macro \youtube for LaTeX pdf
#
txt = txt.replace("\\chapterno", "\\newcommand{\\youtube}[1]{\\href{https://www.youtube.com/embed/#1?rel=0}{Link to video}}\\chapterno")
doc = LaTeX(txt, firstname)
doc.translate()
#for v in doc.tokens:
#    print(v)
#doc.tokenize()
#for v in doc.tokens:
#    print(v)
#print(doc.HTML())
#print(doc.macros)
s = doc.LaTeX()
print(s)



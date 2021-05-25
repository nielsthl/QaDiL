#!/usr/bin/python3

import sys
import os
import io 
from HTML import HTML

filename = sys.argv[1]
infile = io.open(filename, "r", encoding="utf8")
firstname, extension = os.path.splitext(filename)
outfile = io.open(firstname + ".html", "w", encoding="utf8")

doc = HTML(infile.read(), firstname)
doc.translate()
outfile.write(doc.HTML())

infile.close()
outfile.close()

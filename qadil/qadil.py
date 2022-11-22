#!/usr/bin/python3

import os
import io
import argparse
from HTML import HTML

arg_parser = argparse.ArgumentParser(description="QaDiL")
arg_parser.add_argument("filename")
arg_parser.add_argument("--language", help="Two letter abbreviation of language, e.g. EN for English.", default="DA")
args = arg_parser.parse_args()

filename = args.filename
infile = io.open(filename, "r", encoding="utf8")
firstname, extension = os.path.splitext(filename)
outfile = io.open(firstname + ".html", "w", encoding="utf8")

doc = HTML(infile.read(), firstname, language=args.language)
doc.translate()
outfile.write(doc.HTML())

infile.close()
outfile.close()

INIT = ../../qadil/init.py
COMPILER = ../../qadil/qadil.py
GENTOC = ../../qadil/gentoc.py
GENLABELS = ../../qadil/genlbls.py

all: book labels toc init
book: index.html intro.html bibliography.html
init:
	python3 $(INIT) .
labels:
	python3 $(GENLABELS) .
toc:
	python3 $(GENTOC) .
%.html: %.tex
	python3 $(COMPILER) $<
clean:
	rm -f *.html *.toc *.lbl *~
zip:
	zip -r Generic.zip *.html img/ js/ css/
 

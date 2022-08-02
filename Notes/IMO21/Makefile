INIT = ../../qadil/init.py
CHAPTERDIR = .
COMPILER = ../../qadil/qadil.py
GENTOC = ../../qadil/gentoc.py
GENLABELS = ../../qadil/genlbls.py

all: book labels toc init

book: $(CHAPTERDIR)/index.html $(CHAPTERDIR)/intro.html $(CHAPTERDIR)/lineqs.html $(CHAPTERDIR)/matrices.html $(CHAPTERDIR)/whatisopt.html $(CHAPTERDIR)/euclidean.html $(CHAPTERDIR)/convexfunctions.html $(CHAPTERDIR)/diffseveral.html $(CHAPTERDIR)/hessian.html $(CHAPTERDIR)/convexoptimization.html

init:
	python3 $(INIT) $(CHAPTERDIR) 

labels:
	python3 $(GENLABELS) $(CHAPTERDIR) 

toc:
	python3 $(GENTOC) $(CHAPTERDIR) 

%.html: %.tex
	python3 $(COMPILER) $<

clean:
	rm -f $(CHAPTERDIR)/*.html $(CHAPTERDIR)/*.toc $(CHAPTERDIR)/*.lbl $(CHAPTERDIR)/*~

zip:
	zip -r IMO21.zip *.html img/ js/ css/
 

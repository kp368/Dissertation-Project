# This is the Makefile for the demonstration dissertation
# written by Martin Richards
#
# Note that continuation lines require '\'
# and that TAB is used after ':' and before unix commands.

DISS = disser.tex refs.bib propbody.tex

PROP = proposal.tex propbody.tex

help:
	@echo
	@echo "USAGE:"
	@echo
	@echo "make          display help information"
	@echo "make prop     make the proposal and view it using xdvi"
	@echo "make disser.ps  make a postscript version of the dissertation"
	@echo "make disser.pdf make a .pdf version of the dissertation"
	@echo "make gv       view the dissertation with ghostview"
	@echo "make gs       view the dissertation with ghostscript"
	@echo "make all      construct proposal.dvi and diss.ps"
	@echo "make count    display an estimated word count"
	@echo "make pub      put demodiss.tar on my homepage"
	@echo "make clean    remove all remakeable files"
	@echo "make pr       print the dissertation"
	@echo

prop:	proposal.dvi
	xdvi proposal.dvi

disser.ps:	$(DISS)
	latex disser
	bibtex disser
	latex disser
	bibtex disser
	latex disser
	bibtex disser
	dvips -Ppdf -G0 -t a4 -pp 0-200 -o disser.ps disser.dvi

disser.pdf: $(DISS)	
	pdflatex disser.tex	

makefile.txt:	Makefile
	expand Makefile >makefile.txt
count:
	detex disser.tex | tr -cd '0-9A-Za-z \n' | wc -w

proposal.dvi: $(PROP)
	latex proposal

all:	proposal.dvi disser.ps

pub:	disser.pdf
	cp disser.pdf /homes/mr/public_html/demodiss.pdf
	make clean
	(cd ..; tar cfv /homes/mr/public_html/demodiss.tar demodiss)

clean:
	rm -f disser.ps *.dvi *.aux *.log *.err
	rm -f core *~ *.lof *.toc *.blg *.bbl
	rm -f makefile.txt

gv:	disser.ps
	ghostview disser.ps

gs:	disser.ps
	gs disser.ps

pr:	disser.ps
	lpr disser.ps

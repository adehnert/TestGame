SOURCES=$(wildcard *.tex)
OUTPUTS=$(subst json-PRINT.pdf,json-PRINT.json,$(SOURCES:.tex=.pdf))

GENERAL_DEPS = ../LaTeX/testgame.cls ../LaTeX/cards.sty  ../LaTeX/datatypes.sty  ../LaTeX/extraction.sty  ../LaTeX/gametex.sty  ../LaTeX/parsename.sty $(wildcard ../Lists/*.tex)
GENERAL_DEPS += $(wildcard ../Bluesheets/*.tex) $(wildcard ../Charsheets/*.tex) $(wildcard Greensheets/*.tex) $(wildcard Handouts/*.tex) $(wildcard Lists/*.tex) $(wildcard Notebooks/*.tex) $(wildcard Whitesheets/*.tex)

all : $(OUTPUTS)

clean :
	rm $(OUTPUTS) *.aux *.log

%.pdf : %.tex $(GENERAL_DEPS)
	pdflatex $<

json-PRINT.json : json-PRINT.tex $(GENERAL_DEPS)
	pdflatex $<

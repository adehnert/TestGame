SOURCES=$(wildcard *.tex)
OUTPUTS=$(subst json-PRINT.pdf,json-PRINT.json,$(SOURCES:.tex=.pdf)) rules-scenario.pdf

GENERAL_DEPS = ../LaTeX/testgame.cls ../LaTeX/cards.sty  ../LaTeX/datatypes.sty  ../LaTeX/extraction.sty  ../LaTeX/gametex.sty  ../LaTeX/parsename.sty $(wildcard ../Lists/*.tex)
GENERAL_DEPS += $(wildcard ../Bluesheets/*.tex) $(wildcard ../Charsheets/*.tex) $(wildcard Greensheets/*.tex) $(wildcard Handouts/*.tex) $(wildcard Lists/*.tex) $(wildcard Notebooks/*.tex) $(wildcard Whitesheets/*.tex)

all : $(OUTPUTS)

clean :
	rm $(OUTPUTS) *.aux *.log

%.pdf : %.tex $(GENERAL_DEPS)
	pdflatex -halt-on-error $<

rules-scenario.pdf : ../Handouts/rules-scenario.tex $(GENERAL_DEPS)
	pdflatex -halt-on-error $<

json-PRINT.json : json-PRINT.tex $(GENERAL_DEPS)
	pdflatex -halt-on-error $<

# Delete PDF's when they fail to compile
# See https://www.gnu.org/software/make/manual/html_node/Errors.html#Errors
.DELETE_ON_ERROR:

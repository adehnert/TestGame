SOURCES=$(wildcard *.tex)
OUTPUTS=$(SOURCES:.tex=.pdf)

GENERAL_DEPS = $(wildcard ../LaTeX/*.cls) ../LaTeX/cards.sty  ../LaTeX/datatypes.sty  ../LaTeX/extraction.sty  ../LaTeX/gametex.sty  ../LaTeX/parsename.sty $(wildcard ../Lists/*.tex)

INSTALL_DIR = /mit/adehnert/Public/assassin/docs/

all : $(OUTPUTS)

clean :
	rm $(OUTPUTS) *.aux *.log

%.pdf : %.tex $(GENERAL_DEPS)
	pdflatex -halt-on-error $<

install : ci.pdf guildcamp-git.pdf
	cp $^ $(INSTALL_DIR)

# Delete PDF's when they fail to compile
# See https://www.gnu.org/software/make/manual/html_node/Errors.html#Errors
.DELETE_ON_ERROR:

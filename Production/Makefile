SOURCES=$(wildcard *.tex)
OUTPUTS=$(subst json-PRINT.pdf,json-PRINT.json,$(SOURCES:.tex=.pdf)) rules-scenario.pdf

EPUB_SOURCES=$(filter-out json-PRINT.tex skilllist-PRINT.tex cheatsheet-PRINT.tex,$(SOURCES))
EPUBS=$(EPUB_SOURCES:.tex=.epub)

# LaTeX/gametex.cfg and Production/ebook-convert.sh are both needed to build
# epub files. Gate building an epub for charsheets on them being present.
# Also need the "htlatex" and "ebook-convert" binaries (from the "tex4ht" and
# "calibre" Ubuntu packages, respectively)
ifneq ("$(wildcard ../LaTeX/gametex.cfg)","")
    $(warning adding to epub ($(EPUBS)) and mobi entries to OUTPUTS)
    OUTPUTS+=$(EPUBS) $(EPUBS:.epub=.mobi)
else
endif

GENERAL_DEPS = $(wildcard ../LaTeX/*.cls) ../LaTeX/cards.sty  ../LaTeX/datatypes.sty  ../LaTeX/extraction.sty  ../LaTeX/gametex.sty  ../LaTeX/parsename.sty $(wildcard ../Lists/*.tex)
dirs = Bluesheets Charsheets Greensheets Handouts Lists Notebooks Whitesheets
GENERAL_DEPS += $(foreach dir,$(dirs),$(wildcard ../$(dir)/*.tex))

all : $(OUTPUTS)

clean :
	rm $(OUTPUTS) *.aux *.log

%.pdf : %.tex $(GENERAL_DEPS)
	pdflatex -halt-on-error $<

%.epub : %.tex $(GENERAL_DEPS) ebook-convert.sh ../LaTeX/gametex.cfg
	htlatex $< "gametex"
	./ebook-convert.sh $*

%.mobi : %.epub
	ebook-convert $< $@

rules-scenario.pdf : ../Handouts/rules-scenario.tex $(GENERAL_DEPS)
	pdflatex -halt-on-error $<

json-PRINT.json : json-PRINT.tex $(GENERAL_DEPS)
	pdflatex -halt-on-error $<

# Delete PDF's when they fail to compile
# See https://www.gnu.org/software/make/manual/html_node/Errors.html#Errors
.DELETE_ON_ERROR:

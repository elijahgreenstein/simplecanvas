SRC := source
BUILD := build
BLD := $(BUILD)/docs
PY := docbuilder.py
ST := static
CSS := styles.css

STATIC_SRC:= $(SRC)/$(ST)
STATIC_BLD := $(BLD)/$(ST)
MD := $(wildcard $(SRC)/*.md)
HTML := $(subst $(SRC),$(BLD),$(MD:.md=.html))

.PHONY : all
all : dirs static html

.PHONY : dirs
dirs : $(BLD) $(STATIC_BLD)

$(BLD) :
	mkdir -p $(BLD)

$(STATIC_BLD) :
	mkdir -p $(STATIC_BLD)

.PHONY : static
static : $(STATIC_BLD)/$(CSS)
$(STATIC_BLD)/$(CSS) : $(STATIC_SRC)/$(CSS)
	cp $< $@

.PHONY : html
html : $(HTML)

$(BLD)/%.html : $(SRC)/%.md
	python $(PY) $< $@ ./$(ST)/$(CSS)

.PHONY : clean
clean :
	rm -rf $(BUILD)

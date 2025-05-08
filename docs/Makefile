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

.PHONY : html
html : $(HTML)

$(BLD)/%.html : $(SRC)/%.md $(BLD) $(STATIC_BLD)/$(CSS)
	python $(PY) $< $@ ./$(ST)/$(CSS)

$(BLD) :
	mkdir -p $(BLD)

$(STATIC_BLD)/$(CSS) : $(STATIC_SRC)/$(CSS) $(STATIC_BLD)
	cp $< $@

$(STATIC_BLD) :
	mkdir -p $(STATIC_BLD)

.PHONY : prune
prune :
	for htmlfile in $(wildcard $(BLD)/*.html); do \
		if [ ! -e $(SRC)/$$(basename $${htmlfile} .html).md ]; then \
			rm $${htmlfile}; \
			echo "Removed '$${htmlfile}'"; \
			fi \
		done

.PHONY : clean
clean :
	rm -rf $(BUILD)

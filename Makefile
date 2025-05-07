# Use this Makefile to build the documentation in `docs` and commit the build to
# the `gh-pages` branch.
#
# To build the documentation locally, use the Makefile in `docs`.

DOC := docs
BLD := $(DOC)/build
BLD_DOCS := $(BLD)/docs
GHP := gh-pages

ADD := git add --all
COM := git commit -m "Update docs"
PUSH := git push origin $(GHP)

.PHONY : docs
docs :
	rm -rf $(BLD)
	mkdir $(BLD)
	git clone .git --branch $(GHP) $(BLD)
	rm -rf $(BLD_DOCS)
	cd $(DOC) && make
	cd $(BLD_DOCS) && $(ADD) && $(COM) && $(PUSH)

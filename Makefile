# Use this Makefile to build the documentation in `docs` and commit the build to
# the `gh-pages` branch. Use `make push` to push `gh-pages` branch to GitHub.
#
# To build the documentation locally, use the Makefile in `docs`.

DOC := docs
BLD := $(DOC)/build
OUT := docs
GHP := gh-pages
GIT := $(BLD)/.git

.PHONY : docs
docs : $(GIT)
	cd $(DOC) && make && make prune
	cd $(BLD)/$(OUT) && \
		git add --all && \
		git commit -m "Update docs" && \
		git push origin $(GHP)

$(GIT) :
	rm -rf $(BLD)
	mkdir $(BLD)
	git clone .git --branch $(GHP) $(BLD)

.PHONY : push
push :
	git checkout $(GHP)
	git push
	git checkout main

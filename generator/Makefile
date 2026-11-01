# Shortcuts for the model generator. Run from anywhere: make -C generator <target>
ROOT  := $(abspath $(dir $(lastword $(MAKEFILE_LIST)))/..)
GEN   := cd $(ROOT) && uv run python -m generator
# Extra flags for the model targets, e.g. `make -C generator sync-graph FLAGS=--verbose`
FLAGS ?=

.PHONY: help fetch-graph fetch-graph-beta fetch-sharepoint sync-graph sync-sharepoint sync \
        force-graph force-sharepoint force dry-run test

help:
	@echo "fetch-graph | fetch-graph-beta | fetch-sharepoint   download metadata (needs O365_* env or tests.settings)"
	@echo "sync-graph | sync-sharepoint | sync                 update the model from the saved metadata"
	@echo "force-graph | force-sharepoint | force              same, ignoring the up-to-date fast path"
	@echo "dry-run                                             plan both syncs without writing"
	@echo "test                                                run tests/tooling"
	@echo "any target: append FLAGS=... (e.g. FLAGS=--verbose, FLAGS=--check)"

fetch-graph:
	$(GEN) fetch graph $(FLAGS)

fetch-graph-beta:
	$(GEN) fetch graph --graph-version beta $(FLAGS)

fetch-sharepoint:
	$(GEN) fetch sharepoint $(FLAGS)

sync-graph:
	$(GEN) generate graph $(FLAGS)

sync-sharepoint:
	$(GEN) generate sharepoint $(FLAGS)

sync: sync-graph sync-sharepoint

force-graph:
	$(GEN) generate graph --force $(FLAGS)

force-sharepoint:
	$(GEN) generate sharepoint --force $(FLAGS)

force: force-graph force-sharepoint

dry-run:
	$(GEN) generate graph --dry-run $(FLAGS)
	$(GEN) generate sharepoint --dry-run $(FLAGS)

test:
	cd $(ROOT) && uv run pytest tests/tooling -q

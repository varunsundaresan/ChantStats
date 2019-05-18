PYTEST ?= pipenv run pytest
PYTEST_ARGS ?= --cov=chantstats --cov-report=term-missing -svx

all: test-fast

test-fast:
	$(PYTEST) $(PYTEST_ARGS) tests/

test-all:
	$(PYTEST) $(PYTEST_ARGS) --runslow tests/

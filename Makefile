PY					:= python
MAIN				:= src.main
CONFIG_FILE	:= config.txt

POETRY			:= poetry
FLAKE8				:= flake8
MYPY				:= mypy
MYPY_FLAGS			:=	--warn-return-any \
						--warn-unused-ignores \
						--ignore-missing-imports \
						--disallow-untyped-defs \
						--check-untyped-defs
MYPY_FLAGS_STRICT	:=	--strict

install:
	pip install $(POETRY)
	$(POETRY) install

run:
	$(POETRY) run $(PY) -m $(MAIN) $(CONFIG_FILE)

debug:
	$(POETRY) run $(PY) -m pdb $(MAIN) $(CONFIG_FILE)

clean:
	rm ./__pycache__
	rm ./.mypy_cache

lint: install 
	-$(PY) -m $(FLAKE8) .
	$(PY) -m $(MYPY) . $(MYPY_FLAGS)

lint-strict: install
	-$(PY) -m $(FLAKE8) .
	$(PY) -m $(MYPY) . $(MYPY_FLAGS_STRICT)

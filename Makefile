PY					:= python3

FLAKE8				:= flake8
MYPY				:= mypy
MYPY_FLAGS			:=	--warn-return-any \
						--warn-unused-ignores \
						--ignore-missing-imports \
						--disallow-untyped-defs \
						--check-untyped-defs
MYPY_FLAGS_STRICT	:=	--strict

install:
	pip install $(FLAKE8)
	pip install $(MYPY)

run:
	python3 -m src.main config.txt

debug:
	python3 -m pdb src/main.py config.txt

clean:
	rm ./__pycache__
	rm ./.mypy_cache

lint: install 
	-$(PY) -m $(FLAKE8) .
	$(PY) -m $(MYPY) . $(MYPY_FLAGS)

lint-strict: install
	-$(PY) -m $(FLAKE8) .
	$(PY) -m $(MYPY) . $(MYPY_FLAGS_STRICT)

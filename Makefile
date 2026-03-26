PY					:= python
CONFIG_FILE	:= config.txt
VENV_MOD	:= venv
VENV		:= .environment
PACKAGE			:= mazegen
ACTIVATE	:= $(VENV)/bin/activate
RUN_CMD			:= a-maze-ing

PIP					:= pip
POETRY			:= poetry
FLAKE8				:= flake8
MYPY				:= mypy
MYPY_FLAGS			:=	--warn-return-any \
						--warn-unused-ignores \
						--ignore-missing-imports \
						--disallow-untyped-defs \
						--check-untyped-defs
MYPY_FLAGS_STRICT	:=	--strict

build:
	$(POETRY) build -o .

venv: $(ACTIVATE)

$(ACTIVATE):
	@echo "Creating virtual environment..."
	@$(PY) -m $(VENV_MOD) $(VENV)
	@echo "Done !"

install: venv pyproject.toml
	@. $(ACTIVATE) && $(PIP) install .

run: install
	@. $(ACTIVATE) && $(RUN_CMD) $(CONFIG_FILE)

debug: install
	@. $(ACTIVATE) && $(PY) -m pdb $(RUN_CMD) $(CONFIG_FILE)

clean:
	@rm -rf */__pycache__
	@rm -rf .mypy_cache
	@echo "Cleared project !"

lint: install
	-. $(ACTIVATE) && $(PY) -m $(FLAKE8) $(PACKAGE)
	. $(ACTIVATE) && $(PY) -m $(MYPY) $(PACKAGE) $(MYPY_FLAGS)

lint-strict: install
	-. $(ACTIVATE) && $(PY) -m $(FLAKE8) $(PACKAGE)
	. $(ACTIVATE) && $(PY) -m $(MYPY) $(PACKAGE) $(MYPY_FLAGS_STRICT)

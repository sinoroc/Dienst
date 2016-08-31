# Makefile


workdir := .
requirements_txt := $(workdir)/requirements.txt


rm := rm --force --recursive


.PHONY: venv
venv:
	tox -e develop


.PHONY: develop
develop:
	pip install --requirement $(requirements_txt) --editable $(workdir)


.PHONY: lint
lint: pep8 pylint


.PHONY: pep8
pep8:
	pycodestyle


.PHONY: pylint
pylint:
	pytest --pylint -m pylint


.PHONY: test
test: pytest


.PHONY: pytest
pytest:
	pytest


.PHONY: clean
clean:
	@$(rm) $(workdir)/*.egg
	@$(rm) $(workdir)/*.egg-info/
	@$(rm) $(workdir)/.cache/
	@$(rm) $(workdir)/.eggs/
	@$(rm) $(workdir)/build/
	@$(rm) $(workdir)/dist/


# EOF

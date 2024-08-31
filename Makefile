codecheck:
	isort wordlemini
	ruff format wordlemini --line-length 79
	ruff check wordlemini
	mypy wordlemini
	pylint wordlemini

BABEL_CFG = wordlemini/babel.cfg
LOCALES = wordlemini/locales
BASE_POT = wordlemini/locales/base.pot

init: 
	pybabel init -l ru -i $(BASE_POT) -d $(LOCALES)

extract:
	pybabel extract -F $(BABEL_CFG) -o $(BASE_POT) .

update:
	pybabel update -i $(BASE_POT) -d $(LOCALES)

compile:
	pybabel compile -d $(LOCALES)
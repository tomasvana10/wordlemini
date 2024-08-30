codecheck:
	isort wordlemini
	ruff format wordlemini --line-length 79
	ruff check wordlemini
	mypy wordlemini
	pylint wordlemini

BABEL_CFG = wordlemini/babel.cfg
LOCALES = wordlemini/locales
BASE_POT = wordlemini/locales/base.pot
TRANSLATOR = wordlemini/__dev.py

# i18n
i18n: extract update translate compile

init: 
	pybabel init -l ru -i $(BASE_POT) -d $(LOCALES)

extract:
	pybabel extract -F $(BABEL_CFG) -o $(BASE_POT) .

update:
	pybabel update -i $(BASE_POT) -d $(LOCALES)

translate:
	python $(TRANSLATOR)

compile:
	pybabel compile -d $(LOCALES)
# Python makefile
WD := $(shell pwd)
PROJECT := ./infoset
MAX_LOCALS := 20

PYTHON := bin/python
PIP := bin/pip

PEP257 := bin/pep257

PEP8 := bin/pep8
PEP8FLAGS := --statistics --show-source

PYLINT := bin/pylint
PYLINTFLAGS := --max-locals=$(MAX_LOCALS)
PYLINT_DISABLE := 'W0702,W0703' 

PYCHECKER := bin/pychecker

NOSETESTS := bin/nosetests

PYTHONFILES := $(wildcard *.py)

# globaldeps: gvenv gpip  check if pip and virutal env are installed globally, if not install

dependencies: venv
	$(PIP) install pyyaml
	$(PIP) install pep8
	$(PIP) install pep257
	$(PIP) install pysnmp
	$(PIP) install pylint
	$(PIP) install nose
	$(PIP) install mock

.PHONY: setup
setup: venv dependencies

.PHONY: clean
clean: clean_dist clean_venv

.PHONY: clean_dist
clean_dist:
	rm -rf dist

##################### #####################
# virtual env
##################### #####################

venv: bin/python

bin/python:
	virtualenv .

.PHONY: clean_venv
clean_venv:
	rm -rf bin include lib local man share

##################### #####################
# linting :: run pep8 and pylint
##################### #####################

.PHONY: lint
lint: pep8 pep257 pylint

## Pep8

.PHONY: pep8
pep8: pep
	$(PEP8) $(PROJECT) $(PEP8FLAGS)

pep: venv bin/pep8
bin/pep8:
	$(PIP) install pep8

.PHONY: pep257
pep257: pep2
	$(PEP257) $(PROJECT)

pep2: venv bin/pep257
bin/pep257:
	$(PIP) install pep257

## PyLint

pylint: venv bin/pylint
	$(PYLINT) $(PROJECT) $(PYLINTFLAGS) --disable=$(PYLINT_DISABLE)

bin/pylint: 
	$(PIP) install pylint


##################### #####################
# test :: run nosetest pychecker then lint
##################### #####################

.PHONY: test
test: nosetests lint

## Nose

.PHONY: nosetests
nosetests: nose
	$(NOSETESTS) --exe --verbosity=2

nose: venv bin/nosetests

bin/nosetests:
	$(PIP) install nose

## PyChecker

.PHONY: pycheck
pycheck: pychecker
	$(PYCHECKER) hello_world/*.py

pychecker: venv bin/pychecker

##################### #####################
# build ::  create an executable 
##################### #####################

.PHONY: develop
develop: venv
	$(PYTHON) setup.py develop

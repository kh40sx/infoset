# Python makefile
WD := $(shell pwd)
PROJECT := ./infoset
MAX_LOCALS := 20
VENV_PREFIX := venv/bin
INFOSET:= venv/bin/infoset

LESSC:= node_modules/.bin/lessc
PYTHON := $(VENV_PREFIX)/python
PIP := $(VENV_PREFIX)/pip3

PEP257 := $(VENV_PREFIX)/pep257

PEP8 := $(VENV_PREFIX)/pep8
PEP8FLAGS := --statistics --show-source

PYLINT := $(VENV_PREFIX)/pylint
PYLINTFLAGS := --max-locals=$(MAX_LOCALS)
#PYLINTFLAGS := -rn --max-locals=$(MAX_LOCALS)
PYLINT_DISABLE := 'W0702,W0703,R0903,R0204,R0801'
#PYLINT_DISABLE := 'W0702,W0703'

NOSETESTS := $(VENV_PREFIX)/nosetests
VIRT := $(shell which virtualenv)
RRD_TOOL := $(shell which rrdtool)
PYTHONFILES := $(wildcard *.py)

# globaldeps, check if pip3 and virutal env are installed globally, if not install

##################### #####################
# virtual env
##################### #####################

venv: virtual-env

PIP_EXISTS:
	@which pip3 > /dev/null

virtual-env: PIP_EXISTS venv-installed
	virtualenv venv

venv-installed:
ifndef VIRT
	sudo pip3 install virtualenv
else
	$(echo "virtualenv installed")
endif

.PHONY: clean_venv
clean_venv:
	rm -rf venv
	rm -f ./bin/infoset

##################### #####################
# local dependencies
##################### #####################
install:
	$(PIP) install -r requirements.txt

.PHONY: setup
setup: venv

.PHONY: clean
clean: clean_dist clean_venv

.PHONY: clean_dist
clean_dist:
	rm -rf dist

##################### #####################
# linting :: run pep8 and pylint
##################### #####################

.PHONY: lint
lint: pep8 pep257 pylint

## Pep8

.PHONY: pep8
pep8: venv $(PEP8)
	$(PEP8) $(PROJECT) $(PEP8FLAGS)

$(PEP8):
	$(PIP) install pep8

## Pep257

.PHONY: pep257
pep257: venv $(PEP257)
	$(PEP257) $(PROJECT)

$(PEP257):
	$(PIP) install pep257

## PyLint

pylint: venv $(PYLINT)
	$(PYLINT) $(PROJECT) $(PYLINTFLAGS) --disable=$(PYLINT_DISABLE)

$(PYLINT):
	$(PIP) install pylint


##################### #####################
# test :: run nosetest pychecker then lint
##################### #####################

.PHONY: test
test: nosetests

## Nose

.PHONY: nosetests
nosetests: nose
	$(NOSETESTS) --exe --verbosity=2

nose: venv $(NOSETESTS)

$(NOSETESTS):
	$(PIP) install nose

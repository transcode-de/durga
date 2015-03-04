BUILDDIR ?= _build
PORT ?= 8000
SPHINXOPTS =

.PHONY: clean clean-build clean-docs clean-pyc clean-test coverage coverage-html develop docs \
	isort open-docs serve-docs test test-all test-upload upload

help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  clean          to remove all build, test, coverage and Python artifacts"
	@echo "  clean-build    to remove build artifacts"
	@echo "  clean-docs     to remove documentation artifacts"
	@echo "  clean-pyc      to remove Python file artifacts"
	@echo "  clean-test     to remove test and coverage artifacts"
	@echo "  coverage       to generate a coverage report with the default Python"
	@echo "  coverage-html  to generate and open a HTML coverage report with the default Python"
	@echo "  develop        to install (or update) all packages required for development"
	@echo "  dist           to package a release"
	@echo "  docs           to build the project documentation as HTML"
	@echo "  isort          to run isort on the whole project"
	@echo "  open-docs      to open the project documentation in the default browser"
	@echo "  serve-docs     to serve the project documentation in the default browser"
	@echo "  test           to run unit tests quickly with the default Python"
	@echo "  test-all       to run unit tests on every Python version with tox"
	@echo "  test-upload    to upload a release to test PyPI using twine"
	@echo "  upload         to upload a release using twine"

clean: clean-build clean-docs clean-pyc clean-test

clean-docs:
	$(MAKE) -C docs clean BUILDDIR=$(BUILDDIR)

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .cache/
	rm -fr .tox/
	coverage erase
	rm -fr htmlcov/

coverage:
	py.test --pep8 --flakes $(TEST_ARGS) --cov durga

coverage-html: coverage
	coverage html
	python -c "import os, webbrowser; webbrowser.open('file://%s/htmlcov/index.html' % os.getcwd())"

develop:
	pip install -U pip setuptools wheel
	pip install -U -e .[dev]
	pip install -U -e .[docs]
	pip install -U -e .[tests]

dist: clean
	python setup.py sdist bdist_wheel
	ls -l dist

docs:
	rm docs/durga.rst
	rm docs/modules.rst
	sphinx-apidoc -o docs/ durga
	$(MAKE) -C docs html BUILDDIR=$(BUILDDIR) SPHINXOPTS='$(SPHINXOPTS)'

isort:
	isort --recursive setup.py durga tests

open-docs:
	python -c "import os, webbrowser; webbrowser.open('file://{}/docs/{}/html/index.html'.format(os.getcwd(), '$(BUILDDIR)'))"

serve-docs:
	python -c "import webbrowser; webbrowser.open('http://127.0.0.1:$(PORT)')"
	cd docs/$(BUILDDIR)/html; python -m SimpleHTTPServer $(PORT)

test:
	py.test --pep8 --flakes $(TEST_ARGS)

test-all:
	tox

test-upload:
	twine upload -r test -s dist/*
	python -c "import webbrowser; webbrowser.open('https://testpypi.python.org/pypi/durga')"

upload:
	twine upload -s dist/*

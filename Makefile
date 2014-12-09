.PHONY: clean clean-build clean-pyc clean-test coverage coverage-html docs test test-all \
	test-integration upload

help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  clean             to remove all build, test, coverage and Python artifacts"
	@echo "  clean-build       to remove build artifacts"
	@echo "  clean-pyc         to remove Python file artifacts"
	@echo "  clean-test        to remove test and coverage artifacts"
	@echo "  coverage          to generate a coverage report with the default Python"
	@echo "  coverage-html     to generate and open a HTML coverage report with the default Python"
	@echo "  dist              to package a release"
	@echo "  docs              to build and open the project documentation as HTML"
	@echo "  test              to run unit tests quickly with the default Python"
	@echo "  test-all          to run unit tests and integration tests on every Python version with tox"
	@echo "  test-integration  to run unit tests and integration tests with the default Python"
	@echo "  upload            to upload a release using twine"

clean: clean-build clean-pyc clean-test
	$(MAKE) -C docs clean

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
	py.test --pep8 --flakes --run-integration-tests $(TEST_ARGS) --cov durga

coverage-html: coverage
	coverage html
	@python -c "import os, webbrowser; webbrowser.open('file://%s/htmlcov/index.html' % os.getcwd())"

dist: clean
	python setup.py sdist bdist_wheel
	ls -l dist

docs:
	sphinx-apidoc -o docs/ durga
	$(MAKE) -C docs clean html
	@python -c "import os, webbrowser; webbrowser.open('file://%s/docs/_build/html/index.html' % os.getcwd())"

test:
	py.test --pep8 --flakes $(TEST_ARGS)

test-integration:
	py.test --pep8 --flakes --run-integration-tests $(TEST_ARGS)

test-all:
	tox

upload:
	twine upload -s dist/*

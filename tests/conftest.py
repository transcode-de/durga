# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os

import pytest
import six

import durga

str = six.string_types[0]


class MoviesResource(durga.Resource):
    base_url = 'https://api.example.com'
    name = 'movies'
    results_path = ('objects',)
    schema = durga.schema.Schema({
        'id': durga.schema.Use(int, error='Invalid id'),
        'resource_uri': durga.schema.And(str, len, error='Invalid resource_uri'),
        'runtime': durga.schema.Use(int, error='Invalid runtime'),
        'title': durga.schema.And(str, len, error='Invalid title'),
        'director': durga.schema.And(str, len, error='Invalid director'),
        'year': durga.schema.Use(int, error='Invalid year'),
    })


@pytest.fixture
def resource(scope='module'):
    return MoviesResource()


@pytest.fixture
def fixture():
    def load(name):
        fixture = os.path.join(os.path.dirname(__file__), 'fixtures', name)
        with open(fixture) as f:
            return f.read()
    return load


def pytest_addoption(parser):
    """Adds --run-integration-tests option."""
    parser.addoption('--run-integration-tests', action='store_true', default=False,
        help='Runs the integration tests using external services.')


def pytest_runtest_setup(item):
    """Skips integration tests if --run-integration-tests option is False."""
    integration_marker = item.get_marker('integrationtest')
    if integration_marker and not item.config.getvalue('--run-integration-tests'):
        pytest.skip('Skipping integration tests using external services.')

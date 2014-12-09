# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

import durga


class MoviesResource(durga.Resource):
    base_url = 'https://api.example.com'
    name = 'movies'
    results_path = ('objects',)
    schema = 'schema'


@pytest.fixture
def resource(scope='module'):
    return MoviesResource()


def pytest_addoption(parser):
    """Adds --run-integration-tests option."""
    parser.addoption('--run-integration-tests', action='store_true', default=False,
        help='Runs the integration tests using external services.')


def pytest_runtest_setup(item):
    """Skips integration tests if --run-integration-tests option is False."""
    integration_marker = item.get_marker('integrationtest')
    if integration_marker and not item.config.getvalue('--run-integration-tests'):
        pytest.skip('Skipping integration tests using external services.')

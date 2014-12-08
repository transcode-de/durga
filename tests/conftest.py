# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

import durga


class MoviesResource(durga.Resource):
    base_url = 'https://api.example.com'
    name = 'movies'
    schema = 'schema'


@pytest.fixture
def resource(scope='module'):
    return MoviesResource()

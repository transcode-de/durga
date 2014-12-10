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
def resource_class(scope='session'):
    return MoviesResource


@pytest.fixture
def resource(resource_class, scope='module'):
    return resource_class()


@pytest.fixture
def fixture():
    def load(name):
        fixture = os.path.join(os.path.dirname(__file__), 'fixtures', name)
        with open(fixture) as f:
            return f.read()
    return load

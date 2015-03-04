# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

import pytest
import six

import durga

str = six.string_types[0]


class MoviesResource(durga.Resource):
    base_url = 'https://api.example.com'
    path = 'movies'
    objects_path = ('objects',)
    schema = durga.schema.Schema({
        'id': durga.schema.Use(int, error='Invalid id'),
        durga.schema.Optional('resource_uri'): durga.schema.And(str, len,
            error='Invalid resource_uri'),
        'runtime': durga.schema.Use(int, error='Invalid runtime'),
        'title': durga.schema.And(str, len, error='Invalid title'),
        'director': durga.schema.And(str, len, error='Invalid director'),
        'year': durga.schema.Use(int, error='Invalid year'),
    })


class ActorResource(durga.Resource):
    base_url = 'https://api.example.com'
    id_attribute = 'id'
    objects_path = ('objects',)
    path = 'movies/{movie_name}/{movie_year}/actors'
    path_params = ('movie_name', 'movie_year')


class MovieElement(durga.element.Element):
    def save(self):
        return True

    @property
    def full_title(self):
        return '{} ({})'.format(self.title, self.year)


@pytest.fixture
def resource_class(scope='session'):
    return MoviesResource


@pytest.fixture
def resource(resource_class, scope='module'):
    return resource_class()


@pytest.fixture
def actor_resource(scope='module'):
    return ActorResource()


@pytest.fixture
def fixture():
    def load(name):
        fixture = os.path.join(os.path.dirname(__file__), 'fixtures', name)
        with open(fixture) as f:
            return f.read()
    return load


@pytest.fixture
def api_key():
    return 'a33076a7ae214c0d12931ae8e38e846d'


@pytest.fixture
def return_payload():
    """Returns a callback to be used with httpretty.

    The callback function returns the payload sent to httpretty as response body.
    """
    def request_callback(method, uri, headers):
        return (200, headers, method.body)
    return request_callback


@pytest.fixture
def element_class():
    return MovieElement

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from durga import element, exceptions


def test_get_object_not_found(httpserver, resource):
    httpserver.serve_content('{"objects": []}')
    resource.base_url = httpserver.url
    with pytest.raises(exceptions.ObjectNotFound):
        resource.collection.get(id=1)


def test_get_multiple_objects_returned(httpserver, fixture, resource):
    httpserver.serve_content(fixture('movies.json'))
    resource.base_url = httpserver.url
    with pytest.raises(exceptions.MultipleObjectsReturned) as excinfo:
        resource.collection.get(id=1)
    assert str(excinfo.value) == 'Your query returned multiple results.'


def test_get(httpserver, fixture, resource, api_key):
    httpserver.serve_content(fixture('movie_1.json'))
    resource.base_url = httpserver.url
    movie = resource.collection.get(id=1, api_key=api_key)
    assert movie.id == 1
    assert 'id=1' in resource.collection.response.url
    assert api_key in resource.collection.response.url
    resource.id_attribute = 'id'
    movie = resource.collection.get(id=1, api_key=api_key)
    assert movie.id == 1
    assert 'id=1' not in resource.collection.response.url
    assert api_key in resource.collection.response.url


def test_all(httpserver, fixture, resource):
    httpserver.serve_content(fixture('movies.json'))
    resource.base_url = httpserver.url
    movies = resource.collection.all()
    assert movies.count() == 3
    for movie in movies:
        assert isinstance(movie, element.Element)


def test_slice(httpserver, fixture, resource):
    httpserver.serve_content(fixture('movies.json'))
    resource.base_url = httpserver.url
    movies = resource.collection.all()[:2]
    assert len(list(movies)) == 2
    for movie in movies:
        assert isinstance(movie, element.Element)

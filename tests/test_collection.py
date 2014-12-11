# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from durga import element, exceptions


@pytest.mark.parametrize('content', ['{}', '[]'])
def test_get_object_not_found(httpserver, content, resource):
    httpserver.serve_content(content)
    resource.base_url = httpserver.url
    with pytest.raises(exceptions.ObjectNotFound):
        resource.collection.get(year=1900)


def test_get_multiple_objects_returned(httpserver, fixture, resource):
    httpserver.serve_content(fixture('movies.json'))
    resource.base_url = httpserver.url
    with pytest.raises(exceptions.MultipleObjectsReturned) as excinfo:
        resource.collection.get(year=1994)
    assert str(excinfo.value) == 'Your query returned multiple results.'


def test_get(httpserver, fixture, resource, api_key):
    httpserver.serve_content(fixture('movie.json'))
    resource.base_url = httpserver.url
    movie = resource.collection.get(id=1, api_key=api_key)
    assert movie.id == 4
    assert movie.title == 'Léon: The Professional'
    assert 'id=1' in resource.collection.response.url
    assert api_key in resource.collection.response.url
    resource.id_attribute = 'id'
    movie = resource.collection.get(id=1, api_key=api_key)
    assert movie.id == 4
    assert 'id=1' not in resource.collection.response.url
    assert api_key in resource.collection.response.url


def test_all(httpserver, fixture, resource):
    httpserver.serve_content(fixture('movies.json'))
    resource.base_url = httpserver.url
    movies = resource.collection.all()
    assert movies.count() == 4
    for movie in movies:
        assert isinstance(movie, element.Element)


def test_slice(httpserver, fixture, resource):
    httpserver.serve_content(fixture('movies.json'))
    resource.base_url = httpserver.url
    movies = resource.collection.all()[:2]
    assert len(list(movies)) == 2
    for movie in movies:
        assert isinstance(movie, element.Element)

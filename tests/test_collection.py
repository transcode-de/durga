# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import httpretty
import pytest

from durga import element, exceptions


@pytest.mark.httpretty
@pytest.mark.parametrize('content', ['{}', '[]'])
def test_get_object_not_found(content, resource):
    httpretty.register_uri(httpretty.GET, resource.get_url(), body=content,
        content_type='application/json')
    with pytest.raises(exceptions.ObjectNotFound):
        resource.collection.get(year=1900)


@pytest.mark.httpretty
def test_get_multiple_objects_returned(fixture, resource):
    httpretty.register_uri(httpretty.GET, resource.get_url(), body=fixture('movies.json'),
        content_type='application/json')
    with pytest.raises(exceptions.MultipleObjectsReturned) as excinfo:
        resource.collection.get(year=1994)
    assert str(excinfo.value) == 'Your query returned multiple results.'


@pytest.mark.httpretty
def test_get(fixture, resource, api_key):
    httpretty.register_uri(httpretty.GET, resource.get_url(), body=fixture('movie.json'),
        content_type='application/json')
    movie = resource.collection.get(id=1, api_key=api_key)
    assert movie.id == 4
    assert movie.title == 'Léon: The Professional'
    assert 'id=1' in resource.collection.response.url
    assert api_key in resource.collection.response.url


@pytest.mark.httpretty
def test_get_without_filter(fixture, resource, api_key):
    resource.id_attribute = 'id'
    httpretty.register_uri(httpretty.GET, resource.collection.get_element_url(1),
        body=fixture('movie.json'), content_type='application/json')
    movie = resource.collection.get(id=1, api_key=api_key)
    assert movie.id == 4
    assert 'id=1' not in resource.collection.response.url
    assert api_key in resource.collection.response.url


@pytest.mark.httpretty
def test_all(fixture, resource):
    httpretty.register_uri(httpretty.GET, resource.get_url(), body=fixture('movies.json'),
        content_type='application/json')
    movies = resource.collection.all()
    assert movies.count() == 4
    for movie in movies:
        assert isinstance(movie, element.Element)


@pytest.mark.httpretty
def test_all_without_schema(fixture, resource):
    """Fetches all elements without using a schema which deactivates validation."""
    resource.schema = None
    httpretty.register_uri(httpretty.GET, resource.get_url(), body=fixture('movies_errors.json'),
        content_type='application/json')
    movies = resource.collection.all()
    assert movies.count() == 4
    for movie in movies:
        assert isinstance(movie, element.Element)


@pytest.mark.httpretty
def test_slice(fixture, resource):
    httpretty.register_uri(httpretty.GET, resource.get_url(), body=fixture('movies.json'),
        content_type='application/json')
    movies = resource.collection.all()[:2]
    assert len(list(movies)) == 2
    for movie in movies:
        assert isinstance(movie, element.Element)

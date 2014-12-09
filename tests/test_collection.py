# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from durga import exceptions


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


def test_get(httpserver, fixture, resource):
    httpserver.serve_content(fixture('movie_1.json'))
    resource.base_url = httpserver.url
    movie = resource.collection.get(id=1)
    assert movie.id == 1

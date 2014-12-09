# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import operator

import pytest

import durga


def test_base_url_required():
    with pytest.raises(AssertionError) as excinfo:
        durga.Resource()
    assert excinfo.value.msg == 'You must define a "base_url" attribute.'


def test_name_required():
    class TestResource(durga.Resource):
        base_url = 'https://api.example.com'

    with pytest.raises(AssertionError) as excinfo:
        TestResource()
    assert excinfo.value.msg == 'You must define a "name" attribute.'


def test_results_path_required():
    class TestResource(durga.Resource):
        base_url = 'https://api.example.com'
        name = 'test'

    with pytest.raises(AssertionError) as excinfo:
        TestResource()
    assert excinfo.value.msg == 'You must define a "results_path" attribute.'


def test_schema_required():
    class TestResource(durga.Resource):
        base_url = 'https://api.example.com'
        name = 'test'
        results_path = ('objects',)

    with pytest.raises(AssertionError) as excinfo:
        TestResource()
    assert excinfo.value.msg == 'You must define a "schema" attribute.'


def test_get_url(resource):
    assert resource.get_url() == 'https://api.example.com/movies'


@pytest.mark.parametrize('query,op', [
    ({}, operator.eq),
    ({'api_key': 42}, operator.gt),
])
def test_query_copy(query, op, resource_class, httpserver, fixture):
    TestResource = type(str('TestResource'), (resource_class,), {'query': query})
    r1 = TestResource()
    r2 = TestResource()
    assert id(r1) != id(r2)
    httpserver.serve_content(fixture('movies.json'))
    r1.base_url = r2.base_url = httpserver.url
    r1.collection.filter(id=1)
    r2.collection.filter(id=2)
    assert op(len(r1.collection.params), 1)
    assert op(len(r2.collection.params), 1)
    assert id(r1.collection.params) != id(r2.collection.params)

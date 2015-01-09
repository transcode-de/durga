# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import operator
try:
    from urlparse import urlsplit
except ImportError:
    from urllib.parse import urlsplit

import httpretty
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


def test_get_url(resource):
    assert resource.get_url() == 'https://api.example.com/movies'


@pytest.mark.httpretty
@pytest.mark.parametrize('query,op', [
    ({}, operator.eq),
    ({'api_key': 42}, operator.gt),
])
def test_query_copy(query, op, resource_class, fixture):
    TestResource = type(str('TestResource'), (resource_class,), {'query': query})
    r1 = TestResource()
    r2 = TestResource()
    assert id(r1) != id(r2)
    httpretty.register_uri(httpretty.GET, r1.get_url(), body=fixture('movies.json'),
        content_type='application/json')
    r1.collection.filter(id=1).count()
    url1 = r1.collection.response.request.url
    r2.collection.filter(id=2).count()
    url2 = r2.collection.response.request.url
    assert op(len(urlsplit(url1)[3]), 4)
    assert op(len(urlsplit(url2)[3]), 4)
    assert id(url1) != id(url2)

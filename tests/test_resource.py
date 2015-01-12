# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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
def test_headers_default(resource):
    httpretty.register_uri(httpretty.GET, resource.get_url(), body='[]',
        content_type='application/json')
    resource.collection.count()
    headers = resource.collection.response.request.headers
    assert headers['Accept'] == 'application/json'
    assert headers['Content-Type'] == 'application/json'
    assert headers['User-Agent'].startswith('durga')


@pytest.mark.httpretty
def test_headers_custom(resource_class):
    resource_class.headers = {
        'User-Agent': 'durga-test',
        'authorisation': 'Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ=='
    }
    resource = resource_class()
    httpretty.register_uri(httpretty.GET, resource.get_url(), body='[]',
        content_type='application/json')
    resource.collection.count()
    headers = resource.collection.response.request.headers
    assert headers['authorisation'] == resource.headers['authorisation']
    assert headers['User-Agent'] == resource.headers['User-Agent']

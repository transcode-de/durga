# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import httpretty
import pytest

import durga

try:
    from urlparse import urlsplit
except ImportError:
    from urllib.parse import urlsplit


def test_base_url_required():
    with pytest.raises(AssertionError) as excinfo:
        durga.Resource()
    assert excinfo.value.msg == 'You must define a "base_url" attribute.'


def test_path_required():
    class TestResource(durga.Resource):
        base_url = 'https://api.example.com'

    with pytest.raises(AssertionError) as excinfo:
        TestResource()
    assert excinfo.value.msg == 'You must define a "path" attribute.'


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


@pytest.mark.httpretty
def test_path_params_filter(actor_resource, fixture):
    params = {
        'format': 'json',
        'movie_year': 1994,
        'movie_name': 'Pulp Fiction',
    }
    httpretty.register_uri(httpretty.GET, actor_resource.get_url().format(**params),
        body=fixture('movies.json'), content_type='application/json')
    actor_resource.collection.filter(**params).count()
    url_parts = urlsplit(actor_resource.collection.response.request.url)
    assert url_parts[2] == '/movies/Pulp%20Fiction/1994/actors'
    assert url_parts[3] == 'format=json'


@pytest.mark.httpretty
def test_path_params_get(actor_resource, fixture):
    params = {
        'id': 23,
        'format': 'json',
        'movie_year': 1994,
        'movie_name': 'Pulp Fiction',
    }
    httpretty.register_uri(httpretty.GET,
        actor_resource.collection.get_element_url(params['id']).format(**params),
        body=fixture('movie.json'), content_type='application/json')
    actor_resource.collection.get(**params)
    url_parts = urlsplit(actor_resource.collection.response.request.url)
    assert url_parts[2] == '/movies/Pulp%20Fiction/1994/actors/23'
    assert url_parts[3] == 'format=json'


@pytest.mark.httpretty
def test_custom_element(resource, element_class, fixture):
    resource.element = element_class
    httpretty.register_uri(httpretty.GET, resource.get_url(), body=fixture('movies.json'),
        content_type='application/json')
    movie = resource.collection.all()[0]
    assert movie.save()
    assert movie.full_title == 'Pulp Fiction (1994)'

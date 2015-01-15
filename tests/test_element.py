# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import httpretty
import pytest
import schema

from durga import element


def test_get_default_url_attribute(resource):
    class DefaultURLElement(element.Element):
        url = 'https://api.example.com/movies/23'

    assert DefaultURLElement(resource, {}).get_url() == DefaultURLElement.url


def test_get_custom_url_attribute(resource):
    resource.url_attribute = 'resource_uri'

    class CustomURLElement(element.Element):
        resource_uri = 'https://api.example.com/movies/23'

    assert CustomURLElement(resource, {}).get_url() == CustomURLElement.resource_uri


def test_get_dynamic_url(resource):
    class DynamicURLElement(element.Element):
        id = '23'

    with pytest.raises(AssertionError) as excinfo:
        DynamicURLElement(resource, {}).get_url()
    assert excinfo.value.msg == 'You must define an id_attribute attribute at MoviesResource.'
    resource.id_attribute = 'id'
    element_obj = DynamicURLElement(resource, {})
    assert element_obj.get_url() == '/'.join([resource.get_url(), element_obj.id])


@pytest.mark.httpretty
def test_save(fixture, resource, return_payload):
    """Tests saving an ``Element`` in different ways."""
    resource.url_attribute = 'resource_uri'
    httpretty.register_uri(httpretty.GET, resource.get_url(), body=fixture('movie.json'),
        content_type='application/json')
    movie = resource.collection.get(id=1)
    httpretty.register_uri(httpretty.PUT, movie.get_url(), body=return_payload,
        content_type='application/json')
    movie.runtime = 120
    assert movie.save().runtime == movie.runtime
    data = {'runtime': 90}
    movie.update(data)
    movie.save()
    assert movie.runtime == data['runtime']
    assert movie.get_raw()['runtime'] == 110


@pytest.mark.httpretty
def test_save_validation(fixture, resource, return_payload):
    """Tests saving an ``Element`` including validation."""
    resource.url_attribute = 'resource_uri'
    httpretty.register_uri(httpretty.GET, resource.get_url(), body=fixture('movie.json'),
        content_type='application/json')
    movie = resource.collection.get(id=1)
    movie.runtime = 'NAN'
    with pytest.raises(schema.SchemaError) as excinfo:
        movie.save()
    assert str(excinfo.value) == 'Invalid runtime'
    resource.schema = None  # Deactivates validation
    httpretty.register_uri(httpretty.PUT, movie.get_url(), body=return_payload,
        content_type='application/json')
    movie.save().runtime = 'NAN'


@pytest.mark.httpretty
def test_delete(fixture, resource):
    resource.url_attribute = 'resource_uri'
    httpretty.register_uri(httpretty.GET, resource.get_url(), body=fixture('movie.json'),
        content_type='application/json')
    movie = resource.collection.get(id=1)
    httpretty.register_uri(httpretty.DELETE, movie.get_url(), status=204)
    response = movie.delete()
    assert response.status_code == 204

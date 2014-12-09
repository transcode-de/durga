# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

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
        DynamicURLElement(None, {}).get_url()
    assert excinfo.value.msg == 'You must define an id_attribute attribute at NoneType.'
    resource.id_attribute = 'id'
    element_obj = DynamicURLElement(resource, {})
    assert element_obj.get_url() == '/'.join([resource.get_url(), element_obj.id])

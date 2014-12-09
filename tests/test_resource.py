# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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

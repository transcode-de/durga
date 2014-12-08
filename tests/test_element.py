# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from durga import element


class TestElement(element.Element):
    url = 'https://api.example.com/movies/23'


def test_get_url_attribute():
    assert TestElement().get_url() == 'https://api.example.com/movies/23'

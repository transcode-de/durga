# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from durga import validators


def test_url_validator():
    with pytest.raises(ValueError):
        validators.url('not_a_url')
    validators.url('http://www.excample.com')

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

try:
    from urllib.parse import urlsplit
except ImportError:
    from urlparse import urlsplit


def url(url):
    split_result = urlsplit(url)
    if not all([split_result.scheme, split_result.netloc]):
        raise ValueError('Not a valid url.')
    return url

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest
import six

import durga
from durga.element import Element

basestring = six.string_types[0]


class FlickrPhotoSearchResource(durga.Resource):
    base_url = 'https://query.yahooapis.com/v1/public'
    name = 'yql'
    results_path = ('query', 'results', 'photo')
    schema = durga.schema.Schema({
        'farm': durga.schema.Use(int),
        'id': durga.schema.Use(int),
        'isfamily': durga.schema.Use(bool),
        'isfriend': durga.schema.Use(bool),
        'ispublic': durga.schema.Use(bool),
        'owner': durga.schema.And(basestring, len),
        'secret': durga.schema.And(basestring, len),
        'server': durga.schema.Use(int),
        'title': durga.schema.And(basestring, len),
    })


@pytest.mark.integrationtest
def test_flickr():
    flickr = FlickrPhotoSearchResource()
    query = {
        'q': 'select * from flickr.photos.search where text="Cat" and api_key="92bd0de55a63046155c09f1a06876875"',  # noqa
        'format': 'json'
    }
    images = flickr.collection.filter(**query)
    assert images.count() == 10
    image = images[0]
    assert image.__class__.__name__.lower().startswith(flickr.name)
    assert isinstance(image, Element)
    assert isinstance(image.id, int)
    assert isinstance(image.isfamily, bool)
    assert isinstance(image.owner, basestring)

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest
import six

import durga
from durga.element import Element

basestring = six.string_types[0]


class FlickrResource(durga.Resource):
    base_url = 'https://api.flickr.com/services'
    name = 'rest'
    results_path = ('photos', 'photo')
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
    query = {
        'method': 'flickr.photos.search',
        'api_key': 'a33076a7ae214c0d12931ae8e38e846d',
        'format': 'json',
        'nojsoncallback': 1,
    }


@pytest.mark.integrationtest
def test_flickr():
    images = FlickrResource().collection.filter(text='Cat', per_page=10)
    assert images.count() == 10
    image = images[0]
    assert image.__class__.__name__.lower().startswith(FlickrResource.name)
    assert isinstance(image, Element)
    assert isinstance(image.id, int)
    assert isinstance(image.isfamily, bool)
    assert isinstance(image.owner, basestring)
    assert isinstance(image.get_raw(), dict)
    assert sorted(image.get_raw().keys()) == sorted(image.get_resource().schema._schema.keys())

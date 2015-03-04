# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from uuid import UUID

import httpretty
import pytest
import six
from dateutil import parser

import durga
from durga.element import Element

str = six.string_types[0]


class MusicBrainzResource(durga.Resource):
    base_url = 'http://musicbrainz.org/ws/2'
    id_attribute = 'id'
    path = 'artist'
    schema = durga.schema.Schema({
        'country': durga.schema.And(str, len, error='Invalid country'),
        'ipis': [durga.schema.Optional(str)],
        'area': {
            'disambiguation': durga.schema.Optional(str),
            'iso_3166_3_codes': [durga.schema.Optional(str)],
            'sort-name': str,
            'name': str,
            'id': durga.schema.And(str, len, lambda n: UUID(n, version=4)),
            'iso_3166_2_codes': [durga.schema.Optional(str)],
            'iso_3166_1_codes': [durga.schema.Optional(str)],
        },
        'sort-name': str,
        'name': str,
        'disambiguation': durga.schema.Optional(str),
        'life-span': {
            'ended': bool,
            'begin': durga.schema.And(str, len, parser.parse, error='Invalid begin'),
            'end': durga.schema.Or(
                None,
                durga.schema.And(str, len, parser.parse, error='Invalid end')),
        },
        'end_area': durga.schema.Or(None, {
            'disambiguation': durga.schema.Optional(str),
            'iso_3166_3_codes': [durga.schema.Optional(str)],
            'sort-name': str,
            'name': str,
            'id': durga.schema.And(str, len, lambda n: UUID(n, version=4)),
            'iso_3166_2_codes': [durga.schema.Optional(str)],
            'iso_3166_1_codes': [durga.schema.Optional(str)],
        }),
        'id': durga.schema.And(str, len, lambda n: UUID(n, version=4), error='Invalid id'),
        'type': str,
        'begin_area': {
            'disambiguation': durga.schema.Optional(str),
            'iso_3166_3_codes': [durga.schema.Optional(str)],
            'sort-name': str,
            'name': str,
            'id': durga.schema.And(str, len, lambda n: UUID(n, version=4)),
            'iso_3166_2_codes': [durga.schema.Optional(str)],
            'iso_3166_1_codes': [durga.schema.Optional(str)],
        },
        'gender': durga.schema.Or(None, str),
    })
    query = {
        'method': '',
        'fmt': 'json',
        'nojsoncallback': 1,
    }


@pytest.mark.xfail(reason='resource has no objects_path = ('',)')
@pytest.mark.httpretty
def test_artist_resource(fixture):
    artist_resource = MusicBrainzResource()
    uuid = '05cbaf37-6dc2-4f71-a0ce-d633447d90c3'
    params = {'id': uuid}
    httpretty.register_uri(httpretty.GET,
        artist_resource.get_url(),
        body=fixture('musicbrainz_artist.json'), content_type='application/json')
    artist = artist_resource.collection.filter(**params)[0]
    assert isinstance(artist, Element)
    assert artist.id == uuid
    assert artist.name == '東方神起'
    assert artist.country == 'KR'

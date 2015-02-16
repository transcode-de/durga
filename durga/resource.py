# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests

from .collection import Collection


class Resource(object):
    headers = {}
    object_path = tuple()
    objects_path = tuple()
    schema = None

    def __init__(self):
        """Checks if the required attributes are set and sets default HTTP headers."""
        assert hasattr(self, 'base_url'), 'You must define a "base_url" attribute.'
        assert hasattr(self, 'path'), 'You must define a "path" attribute.'
        self.session = requests.Session()
        self.headers.setdefault('Accept', 'application/json')
        self.headers.setdefault('Content-Type', 'application/json')
        self.headers.setdefault('User-Agent', requests.utils.default_user_agent('durga'))
        self.session.headers.update(self.headers)
        self.session.params = getattr(self, 'query', {})

    @property
    def collection(self):
        if not hasattr(self, '_collection'):
            self._collection = Collection(self.get_url(), self)
        return self._collection

    def get_url(self):
        return '{0}/{1}'.format(self.base_url, self.path)

    def get_id_attribute(self):
        id_attribute = getattr(self, 'id_attribute', None)
        assert id_attribute, (
            'You must define an id_attribute attribute at {0}.'.format(self.__class__.__name__)
        )
        return id_attribute

    def dispatch(self, request):
        """Dispatches the Request instance and returns an Response instance."""
        if hasattr(self, 'path_params'):
            request.url = request.url.format(**request.params)
            for key in self.path_params:
                del request.params[key]
        return self.session.send(self.session.prepare_request(request))

    def extract(self, response):
        """Returns a list of JSON data extracted from the response."""
        try:
            data = response.json()
            if len(data):
                for key in self.objects_path:
                    data = data[key]
        except KeyError:
            data = response.json()
            for key in self.object_path:
                data = data[key]
            data = [data]
        return data

    def validate(self, data):
        """Validates the passed data.

        If data is empty or no schema is defined the data is not
        validated and returned as it is.
        """
        if not len(data) or self.schema is None:
            return data
        return [self.schema.validate(item) for item in data]

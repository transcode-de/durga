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
        """Check if the required attributes are set and set default HTTP headers."""
        if not hasattr(self, 'base_url'):
            raise AttributeError('You must define a "base_url" attribute.')
        if not hasattr(self, 'path'):
            raise AttributeError('You must define a "path" attribute.')
        self.session = requests.Session()
        self.headers.setdefault('Accept', 'application/json')
        self.headers.setdefault('Content-Type', 'application/json')
        self.headers.setdefault('User-Agent', requests.utils.default_user_agent('durga'))
        self.session.headers.update(self.headers)
        self.session.params = getattr(self, 'query', {})

    @property
    def collection(self):
        if not hasattr(self, '_collection'):
            self._collection = Collection(self.url, self)
        return self._collection

    @property
    def url(self):
        """Full URL of the resource."""
        return '{0}/{1}'.format(self.base_url, self.path)

    @property
    def id_attribute(self):
        """``Element`` attribute name to be used as primary id."""
        id_attribute = getattr(self, '_id_attribute', None)
        if not id_attribute:
            raise AttributeError(
                'You must define an id_attribute attribute at {0}.'.format(self.__class__.__name__)
            )
        return id_attribute

    @id_attribute.setter
    def id_attribute(self, value):
        self._id_attribute = value

    def dispatch(self, request):
        """Dispatch the Request instance and return an Response instance."""
        if hasattr(self, 'path_params'):
            request.url = request.url.format(**request.params)
            for key in self.path_params:
                del request.params[key]
        return self.session.send(self.session.prepare_request(request))

    def extract(self, response):
        """Return a list of JSON data extracted from the response."""
        try:
            data = response.json()
            if data:
                for key in self.objects_path:
                    data = data[key]
        except KeyError:
            data = response.json()
            for key in self.object_path:
                data = data[key]
            data = [data]
        return data

    def validate(self, data):
        """Validate the passed data.

        If data is empty or no schema is defined the data is not
        validated and returned as it is.
        """
        if not data or self.schema is None:
            return data
        return [self.schema.validate(item) for item in data]

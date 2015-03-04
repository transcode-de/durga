# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

import requests


class Element(object):
    def __init__(self, resource, data):
        self._resource = resource
        self._data = data

    def update(self, data):
        """Updates the attributes with items from the data dictionary."""
        for key, value in data.items():
            setattr(self, key, value)

    def save(self):
        """Updates the remote resource.

        There are two ways to provide data to be saved:

        1. Pass it as a dictionary to the ``update()`` method.
        2. Modify the Element's attributes.

        The data will be validated before the PUT request is made. After
        a successful update an updated Element instance is returned.
        """
        self.validate()
        resource = self.get_resource()
        request = requests.Request('PUT', self.get_url(), data=json.dumps(self.get_data()))
        response = resource.dispatch(request)
        return resource.collection.get_element(resource.validate(resource.extract(response))[0])

    def delete(self):
        return self.get_resource().dispatch(requests.Request('DELETE', self.get_url()))

    def get_url(self):
        resource = self.get_resource()
        url_attribute = getattr(resource, 'url_attribute', 'url')
        try:
            url = getattr(self, url_attribute)
        except AttributeError:
            id_attribute = resource.get_id_attribute()
            return resource.collection.get_element_url(getattr(self, id_attribute))
        return url

    def get_resource(self):
        return self._resource

    def get_raw(self):
        return self._data.copy()

    def get_data(self):
        """Returns the Element's data as dictionary."""
        return dict([(key, getattr(self, key)) for key in self.get_raw()])

    def validate(self):
        """Validates the Element's data.

        If validation fails a schema.SchemaError is raised.
        """
        self.get_resource().validate([self.get_data()])

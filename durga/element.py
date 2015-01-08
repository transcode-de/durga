# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

import requests


class Element(object):
    def __init__(self, resource, data):
        self._resource = resource
        self._data = data

    def update(self, data):
        self._data.update(data)
        response = requests.put(self.get_url(), data=json.dumps(self._data))
        collection = self._resource.collection
        return collection.get_element(collection.validate(collection.extract(response))[0])

    def delete(self):
        return requests.delete(self.get_url())

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
        return self._data

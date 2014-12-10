# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class Element(object):
    def __init__(self, resource, data):
        self._resource = resource
        self._data = data

    def update(self, data):
        pass

    def delete(self):
        pass

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

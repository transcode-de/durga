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
            id_attribute = getattr(resource, 'id_attribute', None)
            assert id_attribute, (
                'You must define an id_attribute attribute at {0}.'.format(resource.__class__.__name__)  # noqa
            )
            url = '{0}/{1}'.format(resource.get_url(), getattr(self, id_attribute))
        return url

    def get_resource(self):
        return self._resource

    def get_raw(self):
        return self._data

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .collection import Collection


class Resource(object):
    schema = None

    def __init__(self):
        assert getattr(self, 'base_url', None), 'You must define a "base_url" attribute.'
        assert getattr(self, 'name', None), 'You must define a "name" attribute.'
        assert getattr(self, 'objects_path', None), 'You must define a "objects_path" attribute.'

    @property
    def collection(self):
        if not hasattr(self, '_collection'):
            self._collection = Collection(self.get_url(), self)
        return self._collection

    def get_url(self):
        return '{0}/{1}'.format(self.base_url, self.name)

    def get_id_attribute(self):
        id_attribute = getattr(self, 'id_attribute', None)
        assert id_attribute, (
            'You must define an id_attribute attribute at {0}.'.format(self.__class__.__name__)
        )
        return id_attribute

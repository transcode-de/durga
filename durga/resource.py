# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class Resource(object):
    def __init__(self):
        assert getattr(self, 'base_url', None), 'You must define a base_url attribute.'
        assert getattr(self, 'name', None), 'You must define a name attribute.'
        assert getattr(self, 'schema', None), 'You must define a schema attribute.'

    def get_url(self):
        return '{0}/{1}'.format(self.base_url, self.name)

    def all(self):
        pass

    def filter(self, **kwargs):
        pass

    def get(self, **kwargs):
        pass

    def create(self, data):
        pass

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .collection import Collection


class Resource(object):
    def __init__(self):
        assert getattr(self, 'base_url', None), 'You must define a "base_url" attribute.'
        assert getattr(self, 'name', None), 'You must define a "name" attribute.'
        assert getattr(self, 'results_path', None), 'You must define a "results_path" attribute.'
        assert getattr(self, 'schema', None), 'You must define a "schema" attribute.'
        self.collection = Collection(self.get_url(), self)

    def get_url(self):
        return '{0}/{1}'.format(self.base_url, self.name)

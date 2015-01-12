# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import itertools

import requests

from . import exceptions
from .element import Element


class Collection(object):
    response = None

    def __init__(self, url, resource):
        self.url = url
        self.resource = resource
        self._reset_request()

    def all(self):
        self._reset_request()
        return self

    def filter(self, *args, **kwargs):
        self._reset_data()
        self.request.params.update(kwargs)
        return self

    def order_by(self):
        raise NotImplementedError
        return self

    def count(self):
        return len(self)

    def get(self, *args, **kwargs):
        try:
            id_attribute = self.resource.get_id_attribute()
            self.request.url = self.get_element_url(kwargs.pop(id_attribute))
        except AssertionError:
            pass
        self.filter(**kwargs)
        count = self.count()
        if count > 1:
            raise exceptions.MultipleObjectsReturned
        elif count == 0:
            raise exceptions.ObjectNotFound
        element = self.elements[0]
        self._reset_request()
        return element

    def create(self, data):
        pass

    def update(self, data):
        pass

    def delete(self):
        pass

    def _reset_data(self):
        self.data = self.validated_data = self._elements = None

    def _reset_request(self):
        self._reset_data()
        self.request = requests.Request('GET', self.url)

    @property
    def elements(self):
        if not self._elements:
            self.response = self.resource.dispatch(self.request)
            self.data = self.resource.extract(self.response)
            self.validated_data = self.resource.validate(self.data)
            self._elements = [self.get_element(data) for data in self.validated_data]
        return self._elements

    def get_element(self, data):
        if not hasattr(self, 'element_class'):
            prefix = self.resource.path.title().replace('/', '')
            self.element_class = str('{0}Element'.format(prefix))
        if not hasattr(self, 'element_base'):
            self.element_base = getattr(self.resource, 'Element', Element)
        try:
            element = type(self.element_class, (self.element_base,), data)(self.resource, data)
        except TypeError:
            error = 'Failed to create Element. Data from request: {}'.format(data)
            raise exceptions.DurgaError(error)
        return element

    def get_element_url(self, id):
        if self.resource.schema:
            self.resource.schema._schema[self.resource.get_id_attribute()].validate(id)
        return '{0}/{1}'.format(self.url, id)

    def __getitem__(self, key):
        """Returns a single Element or a slice of Elements."""
        if isinstance(key, slice):
            return itertools.islice(self.elements, *key.indices(self.count()))
        else:
            return self.elements[key]

    def __iter__(self):
        return iter(self.elements)

    def __len__(self):
        return len(self.elements)

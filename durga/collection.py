# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import itertools
import json

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

    def values(self, *fields):
        """Returns a list of dictionaries instead of Element instances.

        The optional positional arguments, \*fields, can be used to limit
        the fields that are returned.
        """
        self._reset_data()
        self.fields = fields
        self.as_dict = True
        self.as_list = False
        return self

    def values_list(self, *fields, **kwargs):
        """Returns a list of tuples instead of Element instances.

        The optional positional arguments, \*fields, can be used to limit
        the fields that are returned.

        If only a single field is passed in, the flat parameter can be
        passed in too. If True, this will mean the returned results are
        single values, rather than one-tuples.
        """
        self._reset_data()
        self.flat = kwargs.pop('flat', False)
        if kwargs:
            raise TypeError('Unexpected keyword arguments to values_list: {}'.format(list(kwargs)))
        if self.flat and len(fields) != 1:
            raise TypeError((" If 'flat' is used values_list must be called "
                "with exactly one field."))
        self.fields = fields
        self.as_dict = False
        self.as_list = True
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
        """Creates a new remote resource from a dictionary.

        At first the data will be validated. After successful validation
        the data is converted to JSON. The response of the POST request
        is returned afterwards.
        """
        self.resource.validate([data])
        request = requests.Request('POST', self.url, data=json.dumps(data))
        return self.resource.dispatch(request)

    def update(self, data):
        """Updates all Elements of this Collection with data from a dictionary.

        The data dictionary is used to update the data of all Elements
        of this Collection. The updated Elements are validated and their
        data is converted to JSON. A PUT request is made for each
        Element. Finally a list of all responses is returned.
        """
        responses = []
        for element in self.elements:
            element.update(data)
            element.validate()
            request = requests.Request('PUT', self.url, data=json.dumps(element.get_data()))
            responses.append(self.resource.dispatch(request))
        return responses

    def delete(self):
        """Deletes all Elements of this Collection.

        Returns the response for each deleted Element as a list.
        """
        return [element.delete() for element in self.elements]

    def _reset_data(self):
        self.data = self.validated_data = self._elements = None

    def _reset_fields(self):
        self.as_dict = self.as_list = self.flat = False
        self.fields = None

    def _reset_request(self):
        self._reset_data()
        self._reset_fields()
        self.request = requests.Request('GET', self.url)

    @property
    def elements(self):
        if not self._elements:
            self.response = self.resource.dispatch(self.request)
            self.data = self.resource.extract(self.response)
            self.validated_data = self.resource.validate(self.data)
            if self.as_dict or self.as_list:
                self._elements = [self.get_values(data) for data in self.validated_data]
            else:
                self._elements = [self.get_element(data) for data in self.validated_data]
        return self._elements

    def get_element(self, data):
        """Returns an Element instance holding the passed data dictionary."""
        if not hasattr(self, 'element_class'):
            prefix = self.resource.path.title().replace('/', '')
            self.element_class = str('{0}Element'.format(prefix))
        if not hasattr(self, 'element_base'):
            self.element_base = getattr(self.resource, 'element', Element)
        try:
            element = type(self.element_class, (self.element_base,), data)(self.resource, data)
        except TypeError:
            error = 'Failed to create Element. Data from request: {}'.format(data)
            raise exceptions.DurgaError(error)
        return element

    def get_values(self, data):
        """Returns either a dictionary, a tuple or a single field.

        The data type and the fields returned are defined by using
        values() or values_list().
        """
        if self.as_dict:
            if self.fields:
                values = dict(tuple([(field, data[field]) for field in self.fields]))
            else:
                values = data
        elif self.flat:
            values = data[self.fields[0]]
        else:
            if self.fields:
                values = [data[field] for field in self.fields]
            else:
                values = data.values()
            values = tuple(values)
        return values

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

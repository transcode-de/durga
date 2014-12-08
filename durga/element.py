# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class Element(object):
    def update(self, data):
        pass

    def delete(self):
        pass

    def get_url(self):
        if hasattr(self, 'url'):
            url = self.url
        else:
            resource = self.get_resource()
            url = '{0}/{1}'.format(resource.get_url(), getattr(self, resource.id_attribute))
        return url

    def get_resource(self):
        return self._resource

    def get_raw(self):
        return self._raw

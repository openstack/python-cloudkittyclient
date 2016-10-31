# Copyright 2012 OpenStack Foundation
# Copyright 2015 Objectif Libre
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
Base utilities to build API operation managers and objects on top of.
"""

import copy

from six.moves.urllib import parse

from cloudkittyclient.apiclient import base
from cloudkittyclient import exc
from cloudkittyclient.i18n import _


def getid(obj):
    """Extracts object ID.

    Abstracts the common pattern of allowing both an object or an
    object's ID (UUID) as a parameter when dealing with relationships.
    """
    try:
        return obj.id
    except AttributeError:
        return obj


class Manager(object):
    """Managers interact with a particular type of API.

    It works with samples, meters, alarms, etc. and provide CRUD operations for
    them.
    """
    resource_class = None

    def __init__(self, api):
        self.api = api

    @property
    def client(self):
        """Compatible with latest oslo-incubator.apiclient code."""
        return self.api

    def _create(self, url, body):
        body = self.api.post(url, json=body).json()
        if body:
            return self.resource_class(self, body)

    def _list(self, url, response_key=None, obj_class=None, body=None,
              expect_single=False):
        resp = self.api.get(url)
        if not resp.content:
            raise exc.HTTPNotFound
        body = resp.json()

        if obj_class is None:
            obj_class = self.resource_class

        if response_key:
            try:
                data = body[response_key]
            except KeyError:
                return []
        else:
            data = body
        if expect_single:
            data = [data]
        return [obj_class(self, res, loaded=True) for res in data if res]

    def _update(self, url, item, response_key=None):
        if not item.dirty_fields:
            return item
        item = self.api.put(url, json=item.dirty_fields).json()
        # PUT requests may not return a item
        if item:
            return self.resource_class(self, item)

    def _delete(self, url):
        self.api.delete(url)


class CrudManager(base.CrudManager):
    """A CrudManager that automatically gets its base URL."""

    base_url = None

    def build_url(self, base_url=None, **kwargs):
        base_url = base_url or self.base_url
        return super(CrudManager, self).build_url(base_url, **kwargs)

    def get(self, **kwargs):
        kwargs = self._filter_kwargs(kwargs)
        return self._get(
            self.build_url(**kwargs))

    def create(self, **kwargs):
        kwargs = self._filter_kwargs(kwargs)
        return self._post(
            self.build_url(**kwargs), kwargs)

    def update(self, **kwargs):
        kwargs = self._filter_kwargs(kwargs)
        params = kwargs.copy()

        return self._put(
            self.build_url(**kwargs), params)

    def findall(self, base_url=None, **kwargs):
        """Find multiple items with attributes matching ``**kwargs``.

        :param base_url: if provided, the generated URL will be appended to it
        """
        kwargs = self._filter_kwargs(kwargs)

        rl = self._list(
            '%(base_url)s%(query)s' % {
                'base_url': self.build_url(base_url=base_url, **kwargs),
                'query': '?%s' % parse.urlencode(kwargs) if kwargs else '',
            },
            self.collection_key)
        num = len(rl)

        if num == 0:
            msg = _("No %(name)s matching %(args)s.") % {
                'name': self.resource_class.__name__,
                'args': kwargs
            }
            raise exc.HTTPNotFound(msg)
        return rl


class Resource(base.Resource):
    """A resource represents a particular instance of an object.

    Resource might be tenant, user, etc.
    This is pretty much just a bag for attributes.

    :param manager: Manager object
    :param info: dictionary representing resource attributes
    :param loaded: prevent lazy-loading if set to True
    """

    key = None

    def to_dict(self):
        return copy.deepcopy(self._info)

    @property
    def dirty_fields(self):
        out = self.to_dict()
        for k, v in self._info.items():
            if self.__dict__[k] != v:
                out[k] = self.__dict__[k]
        return out

    def update(self):
        try:
            return self.manager.update(**self.dirty_fields)
        except AttributeError:
            raise exc.NotUpdatableError(self)

# -*- coding: utf-8 -*-
# Copyright 2014 Objectif Libre
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# @author: François Magimel (linkid)

"""
Quote resource and manager.
"""

from cloudkittyclient.openstack.common.apiclient import base


class Quote(base.Resource):
    """A resource represents a particular instance of an object (tenant, user,
    etc). This is pretty much just a bag for attributes.

    :param manager: Manager object
    :param info: dictionary representing resource attributes
    :param loaded: prevent lazy-loading if set to True
    """

    def _add_details(self, info):
        try:
            setattr(self, 'price', info)
        except AttributeError:
            # In this case we already defined the attribute on the class
            pass


class QuoteManager(base.CrudManager):
    """Managers interact with a particular type of API and provide CRUD
    operations for them.
    """

    resource_class = Quote
    collection_key = 'billing/quote'
    key = 'quote'

    def _post(self, url, json, response_key=None, return_raw=False):
        """Create an object."""
        body = self.client.post(url, json=json).json()
        if return_raw:
            return body
        return self.resource_class(self, body)

    def post(self, **kwargs):
        """Get the price corresponding to resources attributes."""
        kwargs = self._filter_kwargs(kwargs)
        return self._post(
            url=self.build_url(base_url='/v1', **kwargs),
            json=kwargs.get('json'),
            return_raw=kwargs.get('return_raw'))

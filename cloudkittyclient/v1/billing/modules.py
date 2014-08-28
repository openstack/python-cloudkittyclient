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
Modules resource and manager.
"""

from cloudkittyclient.openstack.common.apiclient import base


class ExtensionSummary(base.Resource):
    """A billing extension summary."""

    def __repr__(self):
        return "<ExtensionSummary %s>" % self.name

    @property
    def id(self):
        return self.name


class Module(base.Resource):
    def __repr__(self):
        name = self._info
        if hasattr(self.manager, 'module_id'):
            name = self.manager.module_id
        return "<Module %s>" % name

    def _add_details(self, info):
        pass

    @property
    def id(self):
        name = self._info
        return name


class ModulesManager(base.CrudManager):
    resource_class = Module
    collection_key = 'billing/modules'
    key = 'module'

    def _list(self, url, response_key, obj_class=None, json=None):
        if json:
            body = self.client.post(url, json=json).json()
        else:
            body = self.client.get(url).json()

        if obj_class is None:
            obj_class = self.resource_class

        # hack
        if type(body) == dict:
            data = body[response_key]
        else:
            data = body

        # NOTE(ja): keystone returns values as list as {'values': [ ... ]}
        #           unlike other services which just return the list...
        try:
            data = data['values']
        except (KeyError, TypeError):
            pass

        return [obj_class(self, res, loaded=True) for res in data if res]

    def list(self, base_url=None, **kwargs):
        """Get module list in the billing pipeline.
        /v1/billing/modules
        """
        return super(ModulesManager, self).list(base_url='/v1', **kwargs)

    def _get(self, url, response_key=None, obj_class=None):
        body = self.client.get(url).json()

        if obj_class is None:
            obj_class = self.resource_class

        # hack
        if response_key is None:
            return obj_class(self, body, loaded=True)
        else:
            return obj_class(self, body[response_key], loaded=True)

    def get(self, **kwargs):
        """Get a module.
        /v1/billing/module/<module>
        """
        kwargs = self._filter_kwargs(kwargs)
        self.module_id = kwargs.get('module_id')

        return self._get(
            url=self.build_url(base_url='/v1', **kwargs),
            response_key=None,
            obj_class=ExtensionSummary)

    def get_status(self, **kwargs):
        """Get the status of a module.
        /v1/billing/module/<module>/enabled
        """
        kwargs = self._filter_kwargs(kwargs)
        self.module_id = kwargs.get('module_id')

        return self._get(
            url='%(base_url)s/enabled' % {
                'base_url': self.build_url(base_url='/v1', **kwargs),
            },
            response_key=None)

    def update(self, **kwargs):
        """Update the status of a module.
        /v1/billing/modules/<module>/enabled
        """
        kwargs = self._filter_kwargs(kwargs)
        self.module_id = kwargs.get('module_id')

        return self._put(
            url='%(base_url)s/enabled' % {  # hack
                'base_url': self.build_url(base_url='/v1', **kwargs),
            },
            json=kwargs.get('enabled'),
            response_key=None)

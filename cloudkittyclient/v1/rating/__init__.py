# -*- coding: utf-8 -*-
# Copyright 2018 Objectif Libre
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
#
from cliff import lister

from cloudkittyclient.common import base
from cloudkittyclient import exc
from cloudkittyclient import utils
from cloudkittyclient.v1.rating import hashmap
from cloudkittyclient.v1.rating import pyscripts


class RatingManager(base.BaseManager):
    """Class used to handle /v1/rating endpoint"""

    url = '/v1/rating/{endpoint}/{module_id}'

    def __init__(self, api_client):
        super(RatingManager, self).__init__(api_client)
        self.hashmap = hashmap.HashmapManager(api_client)
        self.pyscripts = pyscripts.PyscriptManager(api_client)

    def get_module(self, **kwargs):
        """Returns the given module.

        If module_id is not specified, returns the list of loaded modules.

        :param module_id: ID of the module on which you want information.
        :type module_id: str
        """
        authorized_args = ['module_id']
        url = self.get_url('modules', kwargs, authorized_args)
        return self.api_client.get(url).json()

    def update_module(self, **kwargs):
        """Update the given module.

        :param module_id: Id of the module to update.
        :type module_id: str
        :param enabled: Set to True to enable the module, False to disable it.
        :type enabled: bool
        :param priority: New priority of the module.
        :type priority: int
        """
        if not kwargs.get('module_id', None):
            raise exc.ArgumentRequired("'module_id' argument is required.")
        url = self.get_url('modules', kwargs)
        module = self.get_module(**kwargs)
        for key in module.keys():
            value = kwargs.get(key, None)
            if value is not None and module[key] != value:
                module[key] = value
        self.api_client.put(url, json=module)
        return self.get_module(**kwargs)

    def reload_modules(self, **kwargs):
        """Triggers a reload of all rating modules."""
        url = self.get_url('reload_modules', kwargs)
        self.api_client.get(url)

    def get_quotation(self, **kwargs):
        """Returns a quote base on multiple resource descriptions.

        :param res_data: A list of resource descriptions.
        :type res_data: list
        """
        if not kwargs.get('res_data', None):
            raise exc.ArgumentRequired("'res_data' argument is required.")
        url = self.get_url('quote', {})

        body = {'resources': kwargs['res_data']}
        return self.api_client.post(url, json=body).json()


class CliModuleGet(lister.Lister):
    """Get a rating module or list loaded rating modules.

    If module_id is not specified, returns a list of all loaded
    rating modules.
    """
    columns = [
        ('module_id', 'Module'),
        ('enabled', 'Enabled'),
        ('priority', 'Priority'),
    ]

    def take_action(self, parsed_args):
        resp = utils.get_client_from_osc(self).rating.get_module(
            module_id=parsed_args.module_id,
        )
        values = utils.list_to_cols([resp], self.columns)
        return [col[1] for col in self.columns], values

    def get_parser(self, prog_name):
        parser = super(CliModuleGet, self).get_parser(prog_name)
        parser.add_argument('module_id', type=str, help='Module name')
        return parser


class CliModuleList(lister.Lister):
    """List loaded rating modules."""

    columns = [
        ('module_id', 'Module'),
        ('enabled', 'Enabled'),
        ('priority', 'Priority'),
    ]

    def take_action(self, parsed_args):
        resp = utils.get_client_from_osc(self).rating.get_module()
        values = utils.list_to_cols(resp['modules'], self.columns)
        return [col[1] for col in self.columns], values


class CliModuleSet(lister.Lister):
    columns = [
        ('module_id', 'Module'),
        ('enabled', 'Enabled'),
        ('priority', 'Priority'),
    ]

    def _take_action(self, **kwargs):
        resp = utils.get_client_from_osc(self).rating.update_module(**kwargs)
        values = [resp.get(col[0]) for col in self.columns]
        return [col[1] for col in self.columns], [values]

    def get_parser(self, prog_name):
        parser = super(CliModuleSet, self).get_parser(prog_name)
        parser.add_argument('module_id', type=str, help='Module name')
        return parser


class CliModuleEnable(CliModuleSet):
    """Enable a rating module."""

    def take_action(self, parsed_args):
        kwargs = vars(parsed_args)
        kwargs['enabled'] = True
        return self._take_action(**kwargs)


class CliModuleDisable(CliModuleEnable):
    """Disable a rating module."""

    def take_action(self, parsed_args):
        kwargs = vars(parsed_args)
        kwargs['enabled'] = False
        return self._take_action(**kwargs)


class CliModuleSetPriority(CliModuleSet):
    """Set the priority of a rating module."""

    def get_parser(self, prog_name):
        parser = super(CliModuleSetPriority, self).get_parser(prog_name)
        parser.add_argument('priority', type=int, help='Priority (int)')
        return parser

    def take_action(self, parsed_args):
        return self._take_action(**vars(parsed_args))

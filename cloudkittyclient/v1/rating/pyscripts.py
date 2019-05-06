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
from cloudkittyclient.common import base
from cloudkittyclient import exc


class PyscriptManager(base.BaseManager):
    """Class used to manage the Pyscript rating module"""

    url = '/v1/rating/module_config/pyscripts/{endpoint}/{script_id}'

    def list_scripts(self, **kwargs):
        """Get a list of all pyscripts.

        :param no_data: Set to True to remove script data from output.
        :type no_data: bool
        """
        authorized_args = ['no_data']
        url = self.get_url('scripts', kwargs, authorized_args)
        return self.api_client.get(url).json()

    def get_script(self, **kwargs):
        """Get the script corresponding to the given ID.

        :param script_id: ID of the script.
        :type script_id: str
        """
        if not kwargs.get('script_id'):
            raise exc.ArgumentRequired("Argument 'script_id' is required.")
        url = self.get_url('scripts', kwargs)
        return self.api_client.get(url).json()

    def create_script(self, **kwargs):
        """Create a new script.

        :param name: Name of the script to create
        :type name: str
        :param data: Content of the script
        :type data: str
        """
        for arg in ('name', 'data'):
            if not kwargs.get(arg):
                raise exc.ArgumentRequired(
                    "'Argument {} is required.'".format(arg))
        url = self.get_url('scripts', kwargs)
        body = dict(name=kwargs['name'], data=kwargs['data'])
        return self.api_client.post(url, json=body).json()

    def update_script(self, **kwargs):
        """Update an existing script.

        :param script_id: ID of the script to update
        :type script_id: str
        :param name: Name of the script to create
        :type name: str
        :param data: Content of the script
        :type data: str
        """
        if not kwargs.get('script_id'):
            raise exc.ArgumentRequired("Argument 'script_id' is required.")
        script = self.get_script(script_id=kwargs['script_id'])
        for key in ('name', 'data'):
            if kwargs.get(key):
                script[key] = kwargs[key]
        script.pop('checksum', None)
        url = self.get_url('scripts', kwargs)
        return self.api_client.put(url, json=script).json()

    def delete_script(self, **kwargs):
        """Delete a script.

        :param script_id: ID of the script to update
        :type script_id: str
        """
        if not kwargs.get('script_id'):
            raise exc.ArgumentRequired("Argument 'script_id' is required.")
        url = self.get_url('scripts', kwargs)
        self.api_client.delete(url)


# Copyright 2019 Objectif Libre
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
from cloudkittyclient import exc
from cloudkittyclient.v1.client import rating


class RatingManager(rating.RatingManager):
    """Class used to handle /v2/rating/modules endpoint"""

    url = '/v2/rating/modules'

    def get_module(self, **kwargs):
        """Returns the given module.

        If module_id is not specified, returns the list of loaded modules.

        :param module_id: ID of the module on which you want information.
        :type module_id: str
        """
        module_id = kwargs.get('module_id', None)
        if module_id is not None:
            url = "{}/{}".format(self.url, module_id)
        else:
            url = self.url
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
        mutable_fields = ['enabled', 'priority']
        changes = {}
        for key, value in kwargs.items():
            if value is not None and key in mutable_fields:
                changes[key] = value
        self.api_client.put("{}/{}".format(self.url, kwargs['module_id']),
                            json=changes)
        return self.get_module(**kwargs)

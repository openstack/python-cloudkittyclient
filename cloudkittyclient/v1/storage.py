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


class StorageManager(base.BaseManager):
    """Class used to handle /v1/storage endpoint"""

    url = '/v1/storage/dataframes'

    def get_dataframes(self, **kwargs):
        """Returns a list of rated dataframes.

        :param begin: Begin timestamp
        :type begin: datetime
        :param end: End timestamp
        :type end: datetime
        :param tenant_id: ID of the tenant to filter on
        :type tenant_id: str
        :param resource_type: Resource type to filter on
        :type resource_type: str
        """
        authorized_args = ['begin', 'end', 'tenant_id', 'resource_type']
        url = self.get_url('', kwargs, authorized_args)
        return self.api_client.get(url).json()

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


class InfoManager(base.BaseManager):
    """Class used to handle /v1/info endpoint"""
    url = '/v1/info/{endpoint}/{metric_name}'

    def get_metric(self, **kwargs):
        """Returns info for the given service.

        If metric_name is not specified, returns info for all services.

        :param metric_name: Name of the service on which you want information
        :type metric_name: str
        """
        url = self.get_url('metrics', kwargs)
        return self.api_client.get(url).json()

    def get_config(self, **kwargs):
        """Returns the current configuration."""
        url = self.get_url('config', kwargs)
        return self.api_client.get(url).json()

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

from stevedore import extension

from cloudkittyclient import client as ckclient
from cloudkittyclient.openstack.common.apiclient import client
from cloudkittyclient.v1 import collector
from cloudkittyclient.v1 import core
from cloudkittyclient.v1 import report
from cloudkittyclient.v1 import storage

SUBMODULES_NAMESPACE = 'cloudkitty.client.modules'


class Client(object):
    """Client for the Cloudkitty v1 API.

    :param string endpoint: A user-supplied endpoint URL for the cloudkitty
                            service.
    :param function token: Provides token for authentication.
    :param integer timeout: Allows customization of the timeout for client
                            http requests. (optional)
    """

    def __init__(self, *args, **kwargs):
        """Initialize a new client for the Cloudkitty v1 API."""
        self.auth_plugin = (kwargs.get('auth_plugin')
                            or ckclient.get_auth_plugin(*args, **kwargs))
        self.client = client.HTTPClient(
            auth_plugin=self.auth_plugin,
            region_name=kwargs.get('region_name'),
            endpoint_type=kwargs.get('endpoint_type'),
            original_ip=kwargs.get('original_ip'),
            verify=kwargs.get('verify'),
            cert=kwargs.get('cert'),
            timeout=kwargs.get('timeout'),
            timings=kwargs.get('timings'),
            keyring_saver=kwargs.get('keyring_saver'),
            debug=kwargs.get('debug'),
            user_agent=kwargs.get('user_agent'),
            http=kwargs.get('http')
        )

        self.http_client = client.BaseClient(self.client)
        self.modules = core.CloudkittyModuleManager(self.http_client)
        self.collector = collector.CollectorManager(self.http_client)
        self.reports = report.ReportManager(self.http_client)
        self.quotations = core.QuotationManager(self.http_client)
        self.storage = storage.StorageManager(self.http_client)
        self._expose_submodules()

    def _expose_submodules(self):
        extensions = extension.ExtensionManager(
            SUBMODULES_NAMESPACE,
        )
        for ext in extensions:
            client = ext.plugin.get_client(self.http_client)
            setattr(self, ext.name, client)

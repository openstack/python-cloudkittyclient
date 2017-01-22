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
from cloudkittyclient.v1 import collector
from cloudkittyclient.v1 import core
from cloudkittyclient.v1 import report
from cloudkittyclient.v1 import storage

SUBMODULES_NAMESPACE = 'cloudkitty.client.modules'


class Client(object):
    """Client for the Cloudkitty v1 API.

    :param session: a keystoneauth/keystoneclient session object
    :type session: keystoneclient.session.Session
    :param str service_type: The default service_type for URL discovery
    :param str service_name: The default service_name for URL discovery
    :param str interface: The default interface for URL discovery
                          (Default: public)
    :param str region_name: The default region_name for URL discovery
    :param str endpoint_override: Always use this endpoint URL for requests
                                  for this cloudkittyclient
    :param auth: An auth plugin to use instead of the session one
    :type auth: keystoneclient.auth.base.BaseAuthPlugin
    :param str user_agent: The User-Agent string to set
                           (Default is python-cloudkittyclient)
    :param int connect_retries: the maximum number of retries that should be
                                attempted for connection errors
    :param logger: A logging object
    :type logger: logging.Logger
    """

    def __init__(self, *args, **kwargs):
        """Initialize a new client for the Cloudkitty v1 API."""

        if not kwargs.get('auth_plugin'):
            kwargs['auth_plugin'] = ckclient.get_auth_plugin(*args, **kwargs)
        self.auth_plugin = kwargs.get('auth_plugin')

        self.http_client = ckclient.construct_http_client(**kwargs)
        self.modules = core.CloudkittyModuleManager(self.http_client)
        self.collector = collector.CollectorManager(self.http_client)
        self.reports = report.ReportManager(self.http_client)
        self.reportsummary = report.ReportSummaryManager(self.http_client)
        self.quotations = core.QuotationManager(self.http_client)
        self.storage = storage.StorageManager(self.http_client)
        self.config = core.ConfigInfoManager(self.http_client)
        self.service_info = core.ServiceInfoManager(self.http_client)
        self._expose_submodules()

    def _expose_submodules(self):
        extensions = extension.ExtensionManager(
            SUBMODULES_NAMESPACE,
        )
        for ext in extensions:
            client = ext.plugin.get_client(self.http_client)
            setattr(self, ext.name, client)

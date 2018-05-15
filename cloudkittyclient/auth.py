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
from keystoneauth1 import loading
from keystoneauth1 import plugin


class CloudKittyNoAuthPlugin(plugin.BaseAuthPlugin):
    """No authentication plugin for CloudKitty

    """
    def __init__(self, endpoint='http://localhost:8889', *args, **kwargs):
        super(CloudKittyNoAuthPlugin, self).__init__()
        self._endpoint = endpoint

    def get_auth_ref(self, session, **kwargs):
        return None

    def get_endpoint(self, session, **kwargs):
        return self._endpoint

    def get_headers(self, session, **kwargs):
        return {}


class CloudKittyNoAuthLoader(loading.BaseLoader):
    plugin_class = CloudKittyNoAuthPlugin

    def get_options(self):
        options = super(CloudKittyNoAuthLoader, self).get_options()
        options.extend([
            loading.Opt('endpoint', help='CloudKitty Endpoint',
                        required=True, default='http://localhost:8889'),
        ])
        return options

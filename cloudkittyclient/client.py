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
OpenStack Client interface. Handles the REST calls and responses.
"""

from cloudkittyclient.common import auth as ks_auth
from cloudkittyclient.common import client
from cloudkittyclient.openstack.common import importutils


def get_client(api_version, **kwargs):
    """Get an authenticated client.

    This is based on the credentials in the keyword args.

    :param api_version: the API version to use
    :param kwargs: keyword args containing credentials, either:
            * os_auth_token: pre-existing token to re-use
            * endpoint: CloudKitty API endpoint
            or:
            * os_username: name of user
            * os_password: user's password
            * os_auth_url: endpoint to authenticate against
            * os_tenant_name: name of tenant
    """
    cli_kwargs = {
        'username': kwargs.get('os_username'),
        'password': kwargs.get('os_password'),
        'tenant_name': kwargs.get('os_tenant_name'),
        'token': kwargs.get('os_auth_token'),
        'auth_url': kwargs.get('os_auth_url'),
        'endpoint': kwargs.get('cloudkitty_url')
    }
    return Client(api_version, **cli_kwargs)


def Client(version, **kwargs):
    module = importutils.import_versioned_module(version, 'client')
    client_class = getattr(module, 'Client')

    keystone_auth = ks_auth.KeystoneAuthPlugin(
        username=kwargs.get('username'),
        password=kwargs.get('password'),
        tenant_name=kwargs.get('tenant_name'),
        token=kwargs.get('token'),
        auth_url=kwargs.get('auth_url'),
        endpoint=kwargs.get('endpoint'))
    http_client = client.HTTPClient(keystone_auth)

    return client_class(http_client)

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

"""
Tests for the Keystone auth plugin
`cloudkittyclient.common.KeystoneAuthPluginTest`.
"""

from keystoneclient.v2_0 import client as ksclient
import mock

from cloudkittyclient.common import auth
from cloudkittyclient.openstack.common.apiclient import client
from cloudkittyclient.openstack.common.apiclient import exceptions
from cloudkittyclient.tests import base


@mock.patch.object(ksclient, 'Client')
class KeystoneAuthPluginTest(base.TestCase):
    def setUp(self):
        super(KeystoneAuthPluginTest, self).setUp()
        plugin = auth.KeystoneAuthPlugin(
            username="fake-username",
            password="fake-password",
            tenant_name="fake-tenant-name",
            auth_url="http://auth:5000",
            endpoint="http://cloudkitty:8888")
        self.cs = client.HTTPClient(auth_plugin=plugin)

    def test_authenticate(self, mock_ksclient):
        self.cs.authenticate()
        mock_ksclient.assert_called_with(
            username="fake-username",
            password="fake-password",
            tenant_name="fake-tenant-name",
            auth_url="http://auth:5000")

    def test_token_and_endpoint(self, mock_ksclient):
        self.cs.authenticate()
        (token, endpoint) = self.cs.auth_plugin.token_and_endpoint(
            "fake-endpoint-type", "fake-service-type")
        self.assertIsInstance(token, mock.MagicMock)
        self.assertEqual("http://cloudkitty:8888", endpoint)

    def test_token_and_endpoint_before_auth(self, mock_ksclient):
        (token, endpoint) = self.cs.auth_plugin.token_and_endpoint(
            "fake-endpoint-type", "fake-service-type")
        self.assertIsNone(token, None)
        self.assertIsNone(endpoint, None)

    def test_sufficient_options_missing_tenant_name(self, mock_ksclient):
        plugin = auth.KeystoneAuthPlugin(
            username="fake-username",
            password="fake-password",
            auth_url="http://auth:5000",
            endpoint="http://cloudkitty:8888")
        cs = client.HTTPClient(auth_plugin=plugin)
        self.assertRaises(exceptions.AuthPluginOptionsMissing,
                          cs.authenticate)


@mock.patch.object(ksclient, 'Client')
class KeystoneAuthPluginTokenTest(base.TestCase):
    def test_token_and_endpoint(self, mock_ksclient):
        plugin = auth.KeystoneAuthPlugin(
            token="fake-token",
            endpoint="http://cloudkitty:8888")
        cs = client.HTTPClient(auth_plugin=plugin)

        cs.authenticate()
        (token, endpoint) = cs.auth_plugin.token_and_endpoint(
            "fake-endpoint-type", "fake-service-type")
        self.assertEqual('fake-token', token)
        self.assertEqual('http://cloudkitty:8888', endpoint)

    def test_sufficient_options_missing_endpoint(self, mock_ksclient):
        plugin = auth.KeystoneAuthPlugin(
            token="fake-token")
        cs = client.HTTPClient(auth_plugin=plugin)

        self.assertRaises(exceptions.AuthPluginOptionsMissing,
                          cs.authenticate)

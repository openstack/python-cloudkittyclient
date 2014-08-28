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
Tests for the manager billing.modules `cloudkittyclient.v1.billing.modules`.
"""

import json

from cloudkittyclient.openstack.common.apiclient import fake_client
from cloudkittyclient.tests import base
from cloudkittyclient.v1.billing import modules
from cloudkittyclient.v1 import client


modules_test = ["noop", "test"]
info_module = {
    "enabled": True,
    "name": "test",
    "hot-config": True,
    "description": "Test description"
}

fixtures_list_modules = {
    '/v1/billing/modules': {
        'GET': (
            {},
            json.dumps(modules_test)
        ),
    }
}
fixtures_get_one_module = {
    '/v1/billing/modules/test': {
        'GET': (
            {},
            json.dumps(info_module)
        ),
    }
}
fixtures_get_status_module = {
    '/v1/billing/modules/test/enabled': {
        'GET': (
            {},
            json.dumps(str(info_module['enabled']))
        ),
    }
}
fixtures_put_status_module = {
    '/v1/billing/modules/test/enabled': {
        'PUT': (
            {},
            json.dumps(str(False))
        ),
    }
}


class ModulesManagerTest(base.TestCase):
    def connect_client(self, fixtures):
        """Returns the manager."""
        fake_http_client = fake_client.FakeHTTPClient(fixtures=fixtures)
        api_client = client.Client(fake_http_client)
        return modules.ModulesManager(api_client)

    def test_list_modules(self):
        mgr = self.connect_client(fixtures_list_modules)
        modules_expected = [
            modules.Module(modules.ModulesManager, module)
            for module in modules_test
        ]

        self.assertEqual(modules_expected, mgr.list())

    def test_get_one_module(self):
        mgr = self.connect_client(fixtures_get_one_module)
        module_expected = modules.ExtensionSummary(
            modules.ModulesManager, info_module)
        module_get = mgr.get(module_id='test')

        self.assertIn('ExtensionSummary', repr(module_get))
        self.assertEqual(module_expected, module_get)
        self.assertEqual(module_expected.enabled, module_get.enabled)
        self.assertEqual('test', module_get.name)
        self.assertEqual(getattr(module_expected, 'hot-config'),
                         getattr(module_get, 'hot-config'))
        self.assertEqual(module_expected.description, module_get.description)

    def test_get_status_module(self):
        mgr = self.connect_client(fixtures_get_status_module)
        module_status_expected = info_module['enabled']
        module_status_get = mgr.get_status(module_id='test')

        self.assertIn('Module', repr(module_status_get))
        self.assertIn('test', repr(module_status_get))
        self.assertEqual(str(module_status_expected), module_status_get.id)

    def test_update_status_module(self):
        mgr = self.connect_client(fixtures_put_status_module)
        module_status_put = mgr.update(module_id='test', enabled=False)

        self.assertEqual('False', module_status_put.id)

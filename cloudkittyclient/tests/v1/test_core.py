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
from cloudkittyclient.apiclient import client
from cloudkittyclient.apiclient import fake_client
from cloudkittyclient.tests import utils
import cloudkittyclient.v1.core


fixtures = {
    '/v1/rating/modules': {
        'GET': (
            {},
            {'modules': [
                {
                    'module_id': 'hashmap',
                    'enabled': True,
                    'priority': 1,
                },
                {
                    'module_id': 'noop',
                    'enabled': False,
                    'priority': 1,
                },
            ]},
        ),
    },
    '/v1/rating/modules/hashmap': {
        'GET': (
            {},
            {
                'module_id': 'hashmap',
                'enabled': True,
                'priority': 1,
            }
        ),
        'PUT': (
            {},
            {
                'module_id': 'hashmap',
                'enabled': False,
                'priority': 1,
            }
        ),
    },
    '/v1/rating/modules/noop': {
        'GET': (
            {},
            {
                'module_id': 'noop',
                'enabled': False,
                'priority': 1,
            }
        ),
        'PUT': (
            {},
            {
                'module_id': 'noop',
                'enabled': True,
                'priority': 1,
            }
        ),
    },
    '/v1/collectors': {
        'GET': (
            {},
            {'collectors': [
                {
                    'module_id': 'ceilo',
                    'enabled': True,
                },
            ]},
        ),
    },
}


class CloudkittyModuleManagerTest(utils.BaseTestCase):

    def setUp(self):
        super(CloudkittyModuleManagerTest, self).setUp()
        self.http_client = fake_client.FakeHTTPClient(fixtures=fixtures)
        self.api = client.BaseClient(self.http_client)
        self.mgr = cloudkittyclient.v1.core.CloudkittyModuleManager(self.api)

    def test_list_all(self):
        resources = list(self.mgr.list())
        expect = [
            'GET', '/v1/rating/modules'
        ]
        self.http_client.assert_called(*expect)
        self.assertEqual(2, len(resources))
        self.assertEqual('hashmap', resources[0].module_id)
        self.assertEqual('noop', resources[1].module_id)

    def test_get_module_status(self):
        resource = self.mgr.get(module_id='hashmap')
        expect = [
            'GET', '/v1/rating/modules/hashmap'
        ]
        self.http_client.assert_called(*expect)
        self.assertEqual('hashmap', resource.module_id)
        self.assertTrue(resource.enabled)


class CloudkittyModuleTest(utils.BaseTestCase):

    def setUp(self):
        super(CloudkittyModuleTest, self).setUp()
        self.http_client = fake_client.FakeHTTPClient(fixtures=fixtures)
        self.api = client.BaseClient(self.http_client)
        self.mgr = cloudkittyclient.v1.core.CloudkittyModuleManager(self.api)

    def test_enable(self):
        self.ck_module = self.mgr.get(module_id='noop')
        self.ck_module.enable()
        # PUT /v1/rating/modules/noop
        # body : {'enabled': True}
        expect = [
            'PUT', '/v1/rating/modules/noop', {'module_id': 'noop',
                                               'enabled': True,
                                               'priority': 1},
        ]
        self.http_client.assert_called(*expect)

    def test_disable(self):
        self.ck_module = self.mgr.get(module_id='hashmap')
        self.ck_module.disable()
        # PUT /v1/rating/modules/hashmap
        # body : {'enabled': False}
        expect = [
            'PUT', '/v1/rating/modules/hashmap', {'module_id': 'hashmap',
                                                  'enabled': False,
                                                  'priority': 1},
        ]
        self.http_client.assert_called(*expect)

    def test_set_priority(self):
        self.ck_module = self.mgr.get(module_id='hashmap')
        self.ck_module.set_priority(100)
        # PUT /v1/rating/modules/hashmap
        # body : {'priority': 100}
        expect = [
            'PUT', '/v1/rating/modules/hashmap', {'module_id': 'hashmap',
                                                  'enabled': True,
                                                  'priority': 100},
        ]
        self.http_client.assert_called(*expect)

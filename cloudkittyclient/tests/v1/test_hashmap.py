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
from cloudkittyclient.openstack.common.apiclient import client
from cloudkittyclient.openstack.common.apiclient import fake_client
from cloudkittyclient.tests import utils
from cloudkittyclient.v1.rating import hashmap


fixtures = {
    # services
    '/v1/rating/module_config/hashmap/services': {
        'GET': (
            {},
            {'services':
                [
                    {
                        'service_id': '2451c2e0-2c6b-4e75-987f-93661eef0fd5',
                        'name': 'compute'
                    },
                    {
                        'service_id': '2451c2e0-2c6b-4e75-987f-93661eef0fd6',
                        'name': 'volume'
                    },
                    {
                        'service_id': '2451c2e0-2c6b-4e75-987f-93661eef0fd7',
                        'name': 'network'
                    },
                ],
             }
        ),
    },
    # a service
    ('/v1/rating/module_config/hashmap/services/'
     '2451c2e0-2c6b-4e75-987f-93661eef0fd5'): {
        'GET': (
            {},
            {
                'service_id': '2451c2e0-2c6b-4e75-987f-93661eef0fd5',
                'name': 'compute',
            }
        ),
        'DELETE': (
            {},
            {},
        ),
    },
    # a field
    ('/v1/rating/module_config/hashmap/fields/'
     'a53db546-bac0-472c-be4b-5bf9f6117581'): {
        'GET': (
            {},
            {
                'field_id': 'a53db546-bac0-472c-be4b-5bf9f6117581',
                'service_id': '2451c2e0-2c6b-4e75-987f-93661eef0fd5',
                'name': 'flavor',
            },
        ),
        'PUT': (
            {},
            {},
        ),
    },
    ('/v1/rating/module_config/hashmap/fields'
     '?service_id=2451c2e0-2c6b-4e75-987f-93661eef0fd5'): {
        'GET': (
            {},
            {'fields': [
                {
                    'field_id': 'a53db546-bac0-472c-be4b-5bf9f6117581',
                    'service_id': '2451c2e0-2c6b-4e75-987f-93661eef0fd5',
                    'name': 'flavor',
                },
                {
                    'field_id': 'a53db546-bac0-472c-be4b-5bf9f6117582',
                    'service_id': '2451c2e0-2c6b-4e75-987f-93661eef0fd5',
                    'name': 'LOLOL',
                },
            ]
            },
        ),
        'PUT': (
            {},
            {},
        ),
    },
    # a mapping
    ('/v1/rating/module_config/hashmap/mappings/'
     'bff0d209-a8e4-46f8-8c1a-f231db375dcb'): {
        'GET': (
            {},
            {
                'mapping_id': 'bff0d209-a8e4-46f8-8c1a-f231db375dcb',
                'service_id': '2451c2e0-2c6b-4e75-987f-93661eef0fd5',
                'field_id': 'a53db546-bac0-472c-be4b-5bf9f6117581',
                'group_id': None,
                'value': 'm1.small',
                'cost': 0.50,
                'type': 'flat',
            },
        ),
        'PUT': (
            {},
            {
                'mapping_id': 'bff0d209-a8e4-46f8-8c1a-f231db375dcb',
                'service_id': '2451c2e0-2c6b-4e75-987f-93661eef0fd5',
                'field_id': 'a53db546-bac0-472c-be4b-5bf9f6117581',
                'group_id': None,
                'value': 'm1.small',
                'cost': 0.20,
                'type': 'flat',
            },
        ),
    },
    # some mappings
    ('/v1/rating/module_config/hashmap/mappings'
     '?service_id=2451c2e0-2c6b-4e75-987f-93661eef0fd5'): {
        'GET': (
            {},
            {'mappings':
                [
                    {
                        'mapping_id': 'bff0d209-a8e4-46f8-8c1a-f231db375dcb',
                        'service_id': '2451c2e0-2c6b-4e75-987f-93661eef0fd5',
                        'field_id': None,
                        'group_id': None,
                        'value': 'm1.small',
                        'cost': 0.50,
                        'type': 'flat',
                    },
                    {
                        'mapping_id': 'bff0d209-a8e4-46f8-8c1a-f231db375dcc',
                        'service_id': '2451c2e0-2c6b-4e75-987f-93661eef0fd5',
                        'field_id': None,
                        'group_id': None,
                        'value': 'm1.tiny',
                        'cost': 1.10,
                        'type': 'flat',
                    },
                    {
                        'mapping_id': 'bff0d209-a8e4-46f8-8c1a-f231db375dcd',
                        'service_id': '2451c2e0-2c6b-4e75-987f-93661eef0fd5',
                        'field_id': None,
                        'group_id': None,
                        'value': 'm1.big',
                        'cost': 1.50,
                        'type': 'flat',
                    },
                ],
             }
        ),
        'PUT': (
            {},
            {},
        ),
    },
    '/v1/rating/module_config/hashmap/groups': {
        'GET': (
            {},
            {'groups':
                [
                    {
                        'group_id': 'aaa1c2e0-2c6b-4e75-987f-93661eef0fd5',
                        'name': 'object_consumption'
                    },
                    {
                        'group_id': 'aaa1c2e0-2c6b-4e75-987f-93661eef0fd6',
                        'name': 'compute_instance'
                    },
                    {
                        'group_id': 'aaa1c2e0-2c6b-4e75-987f-93661eef0fd7',
                        'name': 'netowrking'
                    },
                ],
             }
        ),
    },
    ('/v1/rating/module_config/hashmap/groups/'
     'aaa1c2e0-2c6b-4e75-987f-93661eef0fd5'): {
        'GET': (
            {},
            {
                'group_id': 'aaa1c2e0-2c6b-4e75-987f-93661eef0fd5',
                'name': 'object_consumption'
            },
        ),
        'DELETE': (
            {},
            {},
        ),
    },
    ('/v1/rating/module_config/hashmap/groups/'
     'aaa1c2e0-2c6b-4e75-987f-93661eef0fd5?recursive=True'): {
        'DELETE': (
            {},
            {},
        ),
    },
    # a threshold
    ('/v1/rating/module_config/hashmap/thresholds/'
     '1f136864-be73-481f-b9be-4fbda2496f72'): {
        'GET': (
            {},
            {
                'threshold_id': '1f136864-be73-481f-b9be-4fbda2496f72',
                'service_id': '1329d62f-bd1c-4a88-a75a-07545e41e8d7',
                'field_id': 'c7c28d87-5103-4a05-af7f-e4d0891cb7fc',
                'group_id': None,
                'level': 30,
                'cost': 5.98,
                'map_type': 'flat',
            },
        ),
        'PUT': (
            {},
            {
                'threshold_id': '1f136864-be73-481f-b9be-4fbda2496f72',
                'service_id': '1329d62f-bd1c-4a88-a75a-07545e41e8d7',
                'field_id': 'c7c28d87-5103-4a05-af7f-e4d0891cb7fc',
                'group_id': None,
                'level': 30,
                'cost': 5.99,
                'type': 'flat',
            },
        ),
        'DELETE': (
            {},
            {},
        ),
    },
}


class ServiceManagerTest(utils.BaseTestCase):

    def setUp(self):
        super(ServiceManagerTest, self).setUp()
        self.http_client = fake_client.FakeHTTPClient(fixtures=fixtures)
        self.api = client.BaseClient(self.http_client)
        self.mgr = hashmap.ServiceManager(self.api)

    def test_list_services(self):
        resources = list(self.mgr.list())
        expect = [
            'GET', '/v1/rating/module_config/hashmap/services'
        ]
        self.http_client.assert_called(*expect)
        self.assertEqual(len(resources), 3)
        self.assertEqual(
            resources[0].service_id,
            '2451c2e0-2c6b-4e75-987f-93661eef0fd5'
        )
        self.assertEqual(resources[0].name, 'compute')
        self.assertEqual(resources[1].name, 'volume')
        self.assertEqual(resources[2].name, 'network')

    def test_get_a_service(self):
        resource = self.mgr.get(
            service_id='2451c2e0-2c6b-4e75-987f-93661eef0fd5'
        )
        expect = [
            'GET', ('/v1/rating/module_config/hashmap/services/'
                    '2451c2e0-2c6b-4e75-987f-93661eef0fd5')
        ]
        self.http_client.assert_called(*expect)
        self.assertEqual(resource.service_id,
                         '2451c2e0-2c6b-4e75-987f-93661eef0fd5')
        self.assertEqual(resource.name, 'compute')


class ServiceTest(utils.BaseTestCase):

    def setUp(self):
        super(ServiceTest, self).setUp()
        self.http_client = fake_client.FakeHTTPClient(fixtures=fixtures)
        self.api = client.BaseClient(self.http_client)
        self.mgr = hashmap.ServiceManager(self.api)
        self.resource = self.mgr.get(
            service_id='2451c2e0-2c6b-4e75-987f-93661eef0fd5'
        )

    def test_get_fields(self):
        fields = self.resource.fields[:]
        expect = [
            'GET', ('/v1/rating/module_config/hashmap/fields'
                    '?service_id=2451c2e0-2c6b-4e75-987f-93661eef0fd5'),
        ]
        self.http_client.assert_called(*expect)
        self.assertEqual(len(fields), 2)

    def test_get_mappings(self):
        mappings = self.resource.mappings[:]
        expect = [
            'GET', ('/v1/rating/module_config/hashmap/mappings'
                    '?service_id=2451c2e0-2c6b-4e75-987f-93661eef0fd5'),
        ]
        self.http_client.assert_called(*expect)
        self.assertEqual(len(mappings), 3)


class FieldManagerTest(utils.BaseTestCase):

    def setUp(self):
        super(FieldManagerTest, self).setUp()
        self.http_client = fake_client.FakeHTTPClient(fixtures=fixtures)
        self.api = client.BaseClient(self.http_client)
        self.mgr = hashmap.FieldManager(self.api)

    def test_get_a_field(self):
        resource = self.mgr.get(
            field_id='a53db546-bac0-472c-be4b-5bf9f6117581'
        )
        expect = [
            'GET', ('/v1/rating/module_config/hashmap/fields/'
                    'a53db546-bac0-472c-be4b-5bf9f6117581')
        ]
        self.http_client.assert_called(*expect)
        self.assertEqual(resource.field_id,
                         'a53db546-bac0-472c-be4b-5bf9f6117581')
        self.assertEqual(
            resource.service_id,
            '2451c2e0-2c6b-4e75-987f-93661eef0fd5'
        )
        self.assertEqual(resource.name, 'flavor')


class MappingManagerTest(utils.BaseTestCase):

    def setUp(self):
        super(MappingManagerTest, self).setUp()
        self.http_client = fake_client.FakeHTTPClient(fixtures=fixtures)
        self.api = client.BaseClient(self.http_client)
        self.mgr = hashmap.MappingManager(self.api)

    def test_get_a_mapping(self):
        resource = self.mgr.get(
            mapping_id='bff0d209-a8e4-46f8-8c1a-f231db375dcb'
        )
        expect = [
            'GET', ('/v1/rating/module_config/hashmap/mappings/'
                    'bff0d209-a8e4-46f8-8c1a-f231db375dcb')
        ]
        self.http_client.assert_called(*expect)
        self.assertEqual(resource.mapping_id,
                         'bff0d209-a8e4-46f8-8c1a-f231db375dcb')
        self.assertEqual(
            resource.service_id,
            '2451c2e0-2c6b-4e75-987f-93661eef0fd5'
        )
        self.assertEqual(
            resource.field_id,
            'a53db546-bac0-472c-be4b-5bf9f6117581'
        )
        self.assertEqual(resource.value, 'm1.small')
        self.assertEqual(resource.cost, 0.5)

    def test_update_a_mapping(self):
        resource = self.mgr.get(
            mapping_id='bff0d209-a8e4-46f8-8c1a-f231db375dcb'
        )
        resource.cost = 0.2
        self.mgr.update(**resource.dirty_fields)
        expect = [
            'PUT', ('/v1/rating/module_config/hashmap/mappings/'
                    'bff0d209-a8e4-46f8-8c1a-f231db375dcb'),
            {u'mapping_id': u'bff0d209-a8e4-46f8-8c1a-f231db375dcb',
             u'cost': 0.2, u'type': u'flat',
             u'service_id': u'2451c2e0-2c6b-4e75-987f-93661eef0fd5',
             u'field_id': u'a53db546-bac0-472c-be4b-5bf9f6117581',
             u'value': u'm1.small'}
        ]
        self.http_client.assert_called(*expect)


class GroupManagerTest(utils.BaseTestCase):

    def setUp(self):
        super(GroupManagerTest, self).setUp()
        self.http_client = fake_client.FakeHTTPClient(fixtures=fixtures)
        self.api = client.BaseClient(self.http_client)
        self.mgr = hashmap.GroupManager(self.api)

    def test_get_a_group(self):
        resource = self.mgr.get(
            group_id='aaa1c2e0-2c6b-4e75-987f-93661eef0fd5'
        )
        expect = [
            'GET', ('/v1/rating/module_config/hashmap/groups/'
                    'aaa1c2e0-2c6b-4e75-987f-93661eef0fd5')
        ]
        self.http_client.assert_called(*expect)
        self.assertEqual(resource.group_id,
                         'aaa1c2e0-2c6b-4e75-987f-93661eef0fd5')
        self.assertEqual(resource.name, 'object_consumption')

    def test_delete_a_group(self):
        self.mgr.delete(group_id='aaa1c2e0-2c6b-4e75-987f-93661eef0fd5')
        expect = [
            'DELETE', ('/v1/rating/module_config/hashmap/groups/'
                       'aaa1c2e0-2c6b-4e75-987f-93661eef0fd5')
        ]
        self.http_client.assert_called(*expect)

    def test_delete_a_group_recursively(self):
        self.mgr.delete(group_id='aaa1c2e0-2c6b-4e75-987f-93661eef0fd5',
                        recursive=True)
        expect = [
            'DELETE', ('/v1/rating/module_config/hashmap/groups/'
                       'aaa1c2e0-2c6b-4e75-987f-93661eef0fd5?recursive=True')
        ]
        self.http_client.assert_called(*expect)


class GroupTest(utils.BaseTestCase):

    def setUp(self):
        super(GroupTest, self).setUp()
        self.http_client = fake_client.FakeHTTPClient(fixtures=fixtures)
        self.api = client.BaseClient(self.http_client)
        self.mgr = hashmap.GroupManager(self.api)

    def test_delete(self):
        self.group = self.mgr.get(
            group_id='aaa1c2e0-2c6b-4e75-987f-93661eef0fd5'
        )
        self.group.delete()
        # DELETE /v1/rating/groups/aaa1c2e0-2c6b-4e75-987f-93661eef0fd5
        expect = [
            'DELETE', ('/v1/rating/module_config/hashmap/groups/'
                       'aaa1c2e0-2c6b-4e75-987f-93661eef0fd5')
        ]
        self.http_client.assert_called(*expect)

    def test_delete_recursive(self):
        self.group = self.mgr.get(
            group_id='aaa1c2e0-2c6b-4e75-987f-93661eef0fd5'
        )
        self.group.delete(recursive=True)
        # DELETE
        # /v1/rating/groups/aaa1c2e0-2c6b-4e75-987f-93661eef0fd5?recusrive=True
        expect = [
            'DELETE', ('/v1/rating/module_config/hashmap/groups/'
                       'aaa1c2e0-2c6b-4e75-987f-93661eef0fd5'
                       '?recursive=True')
        ]
        self.http_client.assert_called(*expect)


class ThresholdManagerTest(utils.BaseTestCase):

    def setUp(self):
        super(ThresholdManagerTest, self).setUp()
        self.http_client = fake_client.FakeHTTPClient(fixtures=fixtures)
        self.api = client.BaseClient(self.http_client)
        self.mgr = hashmap.ThresholdManager(self.api)

    def test_get_a_threshold(self):
        resource = self.mgr.get(
            threshold_id='1f136864-be73-481f-b9be-4fbda2496f72'
        )
        expect = [
            'GET', ('/v1/rating/module_config/hashmap/thresholds/'
                    '1f136864-be73-481f-b9be-4fbda2496f72')
        ]
        self.http_client.assert_called(*expect)
        self.assertEqual(resource.threshold_id,
                         '1f136864-be73-481f-b9be-4fbda2496f72')
        self.assertEqual(
            resource.service_id,
            '1329d62f-bd1c-4a88-a75a-07545e41e8d7'
        )
        self.assertEqual(
            resource.field_id,
            'c7c28d87-5103-4a05-af7f-e4d0891cb7fc'
        )
        self.assertEqual(resource.level, 30)
        self.assertEqual(resource.cost, 5.98)

    def test_update_a_threshold(self):
        resource = self.mgr.get(
            threshold_id='1f136864-be73-481f-b9be-4fbda2496f72'
        )
        resource.cost = 5.99
        self.mgr.update(**resource.dirty_fields)
        expect = [
            'PUT', ('/v1/rating/module_config/hashmap/thresholds/'
                    '1f136864-be73-481f-b9be-4fbda2496f72'),
            {u'threshold_id': u'1f136864-be73-481f-b9be-4fbda2496f72',
             u'cost': 5.99, u'map_type': u'flat',
             u'service_id': u'1329d62f-bd1c-4a88-a75a-07545e41e8d7',
             u'field_id': u'c7c28d87-5103-4a05-af7f-e4d0891cb7fc',
             u'level': 30}
        ]
        self.http_client.assert_called(*expect)

    def test_delete_a_threshold(self):
        self.mgr.delete(threshold_id='1f136864-be73-481f-b9be-4fbda2496f72')
        expect = [
            'DELETE', ('/v1/rating/module_config/hashmap/thresholds/'
                       '1f136864-be73-481f-b9be-4fbda2496f72')
        ]
        self.http_client.assert_called(*expect)

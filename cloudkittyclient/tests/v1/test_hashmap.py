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
from cloudkittyclient.v1.rating import hashmap

GROUP1 = {
    'group_id': 'aaa1c2e0-2c6b-4e75-987f-93661eef0fd5',
    'name': 'object_consumption'}

GROUP2 = {
    'group_id': '36171313-9813-4456-bf40-0195b2c98d1e',
    'name': 'compute_instance'}

GROUP3 = {
    'group_id': '1dc7d980-e80a-4449-888f-26686392f4cc',
    'name': 'networking'}

SERVICE1 = {
    'service_id': '2451c2e0-2c6b-4e75-987f-93661eef0fd5',
    'name': 'compute'}

SERVICE2 = {
    'service_id': '338dd381-2c25-4347-b14d-239194c6068c',
    'name': 'volume'}

SERVICE3 = {
    'service_id': '2f5bc5be-3753-450f-9492-37a6dba2fa8a',
    'name': 'network'}

SERVICE_MAPPING1 = {
    'mapping_id': 'ae6145c3-6b00-4954-b698-cbc36a3d6c4b',
    'service_id': SERVICE3['service_id'],
    'field_id': None,
    'group_id': None,
    'value': None,
    'cost': 0.50,
    'type': 'flat'}

SERVICE_MAPPING1_PUT = {
    'mapping_id': SERVICE_MAPPING1['mapping_id'],
    'service_id': SERVICE3['service_id'],
    'field_id': None,
    'group_id': None,
    'value': None,
    'cost': 0.20,
    'type': SERVICE_MAPPING1['type']}

SERVICE_THRESHOLD1 = {
    'threshold_id': '22e3ae52-a863-47c6-8994-6acdec200346',
    'service_id': SERVICE3['service_id'],
    'field_id': None,
    'group_id': GROUP3['group_id'],
    'level': 30,
    'cost': 5.98,
    'map_type': 'flat'}

SERVICE_THRESHOLD1_PUT = {
    'threshold_id': SERVICE_THRESHOLD1['threshold_id'],
    'service_id': SERVICE3['service_id'],
    'group_id': SERVICE_THRESHOLD1['group_id'],
    'level': SERVICE_THRESHOLD1['level'],
    'cost': 5.99,
    'map_type': SERVICE_THRESHOLD1['map_type']}

FIELD1 = {
    'field_id': 'a53db546-bac0-472c-be4b-5bf9f6117581',
    'service_id': SERVICE1['service_id'],
    'name': 'flavor'}

FIELD2 = {
    'field_id': 'f818a5a6-da88-474c-bd33-184ed769be63',
    'service_id': SERVICE1['service_id'],
    'name': 'image_id'}

FIELD3 = {
    'field_id': 'b9861ba3-26d8-4c39-bb66-c607d48ccfce',
    'service_id': SERVICE1['service_id'],
    'name': 'vcpus'}

FIELD_MAPPING1 = {
    'mapping_id': 'bff0d209-a8e4-46f8-8c1a-f231db375dcb',
    'service_id': None,
    'field_id': FIELD1['field_id'],
    'group_id': GROUP2['group_id'],
    'value': 'm1.small',
    'cost': 0.50,
    'type': 'flat'}

FIELD_MAPPING1_PUT = {
    'mapping_id': FIELD_MAPPING1['mapping_id'],
    'field_id': FIELD_MAPPING1['field_id'],
    'group_id': FIELD_MAPPING1['group_id'],
    'value': FIELD_MAPPING1['value'],
    'cost': 0.20,
    'type': FIELD_MAPPING1['type']}

FIELD_MAPPING2 = {
    'mapping_id': '1f1a05f2-1549-4623-b70a-9ab5c69fcd91',
    'service_id': None,
    'field_id': FIELD1['field_id'],
    'group_id': None,
    'value': 'm1.tiny',
    'cost': 1.10,
    'type': 'flat'}

FIELD_MAPPING3 = {
    'mapping_id': 'deb4efe8-77c4-40ca-b8ca-27ec4892fa5f',
    'service_id': None,
    'field_id': FIELD1['field_id'],
    'group_id': None,
    'value': 'm1.big',
    'cost': 1.50,
    'type': 'flat'}

FIELD_THRESHOLD1 = {
    'threshold_id': 'a33aca4b-3c12-41c5-a153-134c705fdbe2',
    'service_id': None,
    'field_id': FIELD3['field_id'],
    'group_id': None,
    'level': 2,
    'cost': 1.2,
    'map_type': 'flat'}

FIELD_THRESHOLD1_PUT = {
    'threshold_id': FIELD_THRESHOLD1['threshold_id'],
    'service_id': None,
    'field_id': FIELD3['field_id'],
    'group_id': None,
    'level': FIELD_THRESHOLD1['level'],
    'cost': 1.5,
    'map_type': FIELD_THRESHOLD1['map_type']}

fixtures = {
    # services
    '/v1/rating/module_config/hashmap/services': {
        'GET': (
            {},
            {'services':
                [
                    SERVICE1,
                    SERVICE2,
                    SERVICE3
                ],
             }
        ),
    },
    # a service
    ('/v1/rating/module_config/hashmap/services/' +
     SERVICE1['service_id']): {
        'GET': (
            {},
            SERVICE1
        ),
        'DELETE': (
            {},
            {},
        ),
    },
    # a service
    ('/v1/rating/module_config/hashmap/services/' +
     SERVICE3['service_id']): {
        'GET': (
            {},
            SERVICE3
        ),
        'DELETE': (
            {},
            {},
        ),
    },
    # a service mapping
    ('/v1/rating/module_config/hashmap/mappings/' +
     SERVICE_MAPPING1['mapping_id']): {
        'GET': (
            {},
            SERVICE_MAPPING1
        ),
        'PUT': (
            {},
            SERVICE_MAPPING1_PUT
        ),
    },
    # some service mappings
    ('/v1/rating/module_config/hashmap/mappings?service_id=' +
     SERVICE3['service_id']): {
        'GET': (
            {},
            {'mappings':
                [
                    SERVICE_MAPPING1
                ],
             }
        ),
        'PUT': (
            {},
            {},
        ),
    },
    # a service threshold
    ('/v1/rating/module_config/hashmap/thresholds/' +
     SERVICE_THRESHOLD1['threshold_id']): {
        'GET': (
            {},
            SERVICE_THRESHOLD1
        ),
        'PUT': (
            {},
            SERVICE_THRESHOLD1_PUT
        ),
        'DELETE': (
            {},
            {},
        ),
    },
    # service thresholds
    ('/v1/rating/module_config/hashmap/thresholds?service_id=' +
     SERVICE3['service_id']): {
        'GET': (
            {},
            {'thresholds':
                [
                    SERVICE_THRESHOLD1
                ]
             },
        ),
    },
    # service thresholds in a group
    ('/v1/rating/module_config/hashmap/thresholds?group_id=' +
     GROUP3['group_id']): {
        'GET': (
            {},
            {'thresholds':
                [
                    SERVICE_THRESHOLD1
                ]
             },
        ),
    },
    # a field
    ('/v1/rating/module_config/hashmap/fields/' +
     FIELD1['field_id']): {
        'GET': (
            {},
            FIELD1
        ),
        'PUT': (
            {},
            {},
        ),
        'DELETE': (
            {},
            {},
        ),
    },
    # a field
    ('/v1/rating/module_config/hashmap/fields/' +
     FIELD3['field_id']): {
        'GET': (
            {},
            FIELD3
        ),
        'PUT': (
            {},
            {},
        ),
    },
    # some fields
    ('/v1/rating/module_config/hashmap/fields?service_id=' +
     SERVICE1['service_id']): {
        'GET': (
            {},
            {'fields': [
                FIELD1,
                FIELD2,
                FIELD3
            ]
            },
        ),
        'PUT': (
            {},
            {},
        ),
    },
    # a field mapping
    ('/v1/rating/module_config/hashmap/mappings/' +
     FIELD_MAPPING1['mapping_id']): {
        'GET': (
            {},
            FIELD_MAPPING1
        ),
        'PUT': (
            {},
            FIELD_MAPPING1_PUT
        ),
        'DELETE': (
            {},
            {},
        ),
    },
    # some mappings
    ('/v1/rating/module_config/hashmap/mappings?field_id=' +
     FIELD1['field_id']): {
        'GET': (
            {},
            {'mappings':
                [
                    FIELD_MAPPING1,
                    FIELD_MAPPING2,
                    FIELD_MAPPING3
                ],
             }
        ),
        'PUT': (
            {},
            {},
        ),
    },
    # some mappings in a group
    ('/v1/rating/module_config/hashmap/mappings?group_id=' +
     GROUP2['group_id']): {
        'GET': (
            {},
            {'mappings':
                [
                    FIELD_MAPPING1,
                ],
             }
        ),
        'PUT': (
            {},
            {},
        ),
    },
    # a field threshold
    ('/v1/rating/module_config/hashmap/thresholds/' +
     FIELD_THRESHOLD1['threshold_id']): {
        'GET': (
            {},
            FIELD_THRESHOLD1
        ),
        'PUT': (
            {},
            FIELD_THRESHOLD1_PUT
        ),
        'DELETE': (
            {},
            {},
        ),
    },
    # field thresholds
    ('/v1/rating/module_config/hashmap/thresholds?field_id=' +
     FIELD3['field_id']): {
        'GET': (
            {},
            {'thresholds':
                [
                    FIELD_THRESHOLD1
                ]
             },
        ),
    },
    # some groups
    '/v1/rating/module_config/hashmap/groups': {
        'GET': (
            {},
            {'groups':
                [
                    GROUP1,
                    GROUP2,
                    GROUP3
                ],
             }
        ),
    },
    # a group
    ('/v1/rating/module_config/hashmap/groups/' +
     GROUP2['group_id']): {
        'GET': (
            {},
            GROUP2
        ),
        'DELETE': (
            {},
            {},
        ),
    },
    # another group
    ('/v1/rating/module_config/hashmap/groups/' +
     GROUP3['group_id']): {
        'GET': (
            {},
            GROUP3
        ),
        'DELETE': (
            {},
            {},
        ),
    },
    # recursive delete group
    ('/v1/rating/module_config/hashmap/groups/' +
     GROUP2['group_id'] +
     '?recursive=True'): {
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
            'GET', '/v1/rating/module_config/hashmap/services']
        self.http_client.assert_called(*expect)
        self.assertEqual(3, len(resources))
        self.assertEqual(
            SERVICE1['service_id'],
            resources[0].service_id)
        self.assertEqual(SERVICE1['name'], resources[0].name)
        self.assertEqual(SERVICE2['name'], resources[1].name)
        self.assertEqual(SERVICE3['name'], resources[2].name)

    def test_get_a_service(self):
        resource = self.mgr.get(
            service_id=SERVICE1['service_id'])
        expect = [
            'GET', ('/v1/rating/module_config/hashmap/services/' +
                    SERVICE1['service_id'])]
        self.http_client.assert_called(*expect)
        self.assertEqual(SERVICE1['service_id'],
                         resource.service_id)
        self.assertEqual(SERVICE1['name'],
                         resource.name)

    def test_delete_a_service(self):
        self.mgr.delete(service_id=SERVICE1['service_id'])
        expect = [
            'DELETE', ('/v1/rating/module_config/hashmap/services/' +
                       SERVICE1['service_id'])]
        self.http_client.assert_called(*expect)


class ServiceTest(utils.BaseTestCase):

    def setUp(self):
        super(ServiceTest, self).setUp()
        self.http_client = fake_client.FakeHTTPClient(fixtures=fixtures)
        self.api = client.BaseClient(self.http_client)
        self.mgr = hashmap.ServiceManager(self.api)
        self.resource = self.mgr.get(service_id=SERVICE3['service_id'])

    def test_get_fields(self):
        self.resource = self.mgr.get(
            service_id=SERVICE1['service_id'])
        fields = self.resource.fields[:]
        expect = [
            'GET', ('/v1/rating/module_config/hashmap/fields?service_id=' +
                    SERVICE1['service_id'])]
        self.http_client.assert_called(*expect)
        self.assertEqual(3, len(fields))
        field = fields[0]
        self.assertEqual(SERVICE1['service_id'],
                         field.service_id)
        self.assertEqual(FIELD1['field_id'],
                         field.field_id)
        self.assertEqual(FIELD1['name'],
                         field.name)

    def test_get_mappings(self):
        mappings = self.resource.mappings[:]
        expect = [
            'GET', ('/v1/rating/module_config/hashmap/mappings?service_id=' +
                    SERVICE3['service_id'])]
        self.http_client.assert_called(*expect)
        self.assertEqual(1, len(mappings))
        mapping = mappings[0]
        self.assertEqual(SERVICE3['service_id'],
                         mapping.service_id)
        self.assertEqual(SERVICE_MAPPING1['mapping_id'],
                         mapping.mapping_id)
        self.assertEqual(SERVICE_MAPPING1['value'], mapping.value)
        self.assertEqual(SERVICE_MAPPING1['cost'], mapping.cost)
        self.assertEqual(SERVICE_MAPPING1['type'], mapping.type)

    def test_get_thresholds(self):
        thresholds = self.resource.thresholds[:]
        expect = [
            'GET', ('/v1/rating/module_config/hashmap/thresholds?service_id=' +
                    SERVICE3['service_id'])]
        self.http_client.assert_called(*expect)
        self.assertEqual(1, len(thresholds))
        threshold = thresholds[0]
        self.assertEqual(SERVICE_THRESHOLD1['service_id'],
                         threshold.service_id)
        self.assertEqual(SERVICE_THRESHOLD1['threshold_id'],
                         threshold.threshold_id)
        self.assertEqual(SERVICE_THRESHOLD1['level'], threshold.level)
        self.assertEqual(SERVICE_THRESHOLD1['cost'], threshold.cost)
        self.assertEqual(SERVICE_THRESHOLD1['map_type'], threshold.map_type)


class FieldManagerTest(utils.BaseTestCase):

    def setUp(self):
        super(FieldManagerTest, self).setUp()
        self.http_client = fake_client.FakeHTTPClient(fixtures=fixtures)
        self.api = client.BaseClient(self.http_client)
        self.mgr = hashmap.FieldManager(self.api)

    def test_list_fields(self):
        resources = list(self.mgr.list(service_id=SERVICE1['service_id']))
        expect = [
            'GET', ('/v1/rating/module_config/hashmap/fields?service_id=' +
                    SERVICE1['service_id'])]
        self.http_client.assert_called(*expect)
        self.assertEqual(3, len(resources))
        self.assertEqual(SERVICE1['service_id'],
                         resources[0].service_id)
        self.assertEqual(FIELD1['name'], resources[0].name)
        self.assertEqual(FIELD2['name'], resources[1].name)
        self.assertEqual(FIELD3['name'], resources[2].name)

    def test_get_a_field(self):
        resource = self.mgr.get(
            field_id=FIELD1['field_id'])
        expect = [
            'GET', ('/v1/rating/module_config/hashmap/fields/' +
                    FIELD1['field_id'])]
        self.http_client.assert_called(*expect)
        self.assertEqual(FIELD1['field_id'], resource.field_id)
        self.assertEqual(SERVICE1['service_id'], resource.service_id)
        self.assertEqual(FIELD1['name'], resource.name)

    def test_delete_a_field(self):
        self.mgr.delete(field_id=FIELD1['field_id'])
        expect = [
            'DELETE', ('/v1/rating/module_config/hashmap/fields/' +
                       FIELD1['field_id'])]
        self.http_client.assert_called(*expect)


class FieldTest(utils.BaseTestCase):

    def setUp(self):
        super(FieldTest, self).setUp()
        self.http_client = fake_client.FakeHTTPClient(fixtures=fixtures)
        self.api = client.BaseClient(self.http_client)
        self.mgr = hashmap.FieldManager(self.api)
        self.resource = self.mgr.get(field_id=FIELD1['field_id'])

    def test_get_service(self):
        service = self.resource.service
        expect = [
            'GET', ('/v1/rating/module_config/hashmap/services/' +
                    SERVICE1['service_id'])]
        self.http_client.assert_called(*expect)
        self.assertEqual(SERVICE1['service_id'], service.service_id)
        self.assertEqual(SERVICE1['name'], service.name)

    def test_get_mappings(self):
        mappings = self.resource.mappings[:]
        expect = [
            'GET', ('/v1/rating/module_config/hashmap/mappings?field_id=' +
                    FIELD1['field_id'])]
        self.http_client.assert_called(*expect)
        self.assertEqual(3, len(mappings))
        mapping = mappings[0]
        self.assertEqual(FIELD1['field_id'], mapping.field_id)
        self.assertEqual(FIELD_MAPPING1['mapping_id'], mapping.mapping_id)
        self.assertEqual(FIELD_MAPPING1['value'], mapping.value)
        self.assertEqual(FIELD_MAPPING1['cost'], mapping.cost)
        self.assertEqual(FIELD_MAPPING1['type'], mapping.type)

    def test_get_thresholds(self):
        resource = self.mgr.get(field_id=FIELD3['field_id'])
        thresholds = resource.thresholds[:]
        expect = [
            'GET', ('/v1/rating/module_config/hashmap/thresholds?field_id=' +
                    FIELD3['field_id'])]
        self.http_client.assert_called(*expect)
        self.assertEqual(1, len(thresholds))
        threshold = thresholds[0]
        self.assertEqual(FIELD3['field_id'], threshold.field_id)
        self.assertEqual(FIELD_THRESHOLD1['threshold_id'],
                         threshold.threshold_id)
        self.assertEqual(FIELD_THRESHOLD1['level'],
                         threshold.level)
        self.assertEqual(FIELD_THRESHOLD1['cost'],
                         threshold.cost)
        self.assertEqual(FIELD_THRESHOLD1['map_type'],
                         threshold.map_type)


class MappingManagerTest(utils.BaseTestCase):

    def setUp(self):
        super(MappingManagerTest, self).setUp()
        self.http_client = fake_client.FakeHTTPClient(fixtures=fixtures)
        self.api = client.BaseClient(self.http_client)
        self.mgr = hashmap.MappingManager(self.api)

    def test_get_mappings_by_group(self):
        mappings = self.mgr.findall(group_id=GROUP2['group_id'])
        expect = [
            'GET', ('/v1/rating/module_config/hashmap/mappings?group_id=' +
                    GROUP2['group_id'])]
        self.http_client.assert_called(*expect)
        self.assertEqual(1, len(mappings))
        mapping = mappings[0]
        self.assertEqual(FIELD1['field_id'], mapping.field_id)
        self.assertEqual(FIELD_MAPPING1['group_id'], mapping.group_id)
        self.assertEqual(FIELD_MAPPING1['mapping_id'], mapping.mapping_id)
        self.assertEqual(FIELD_MAPPING1['value'], mapping.value)
        self.assertEqual(FIELD_MAPPING1['cost'], mapping.cost)
        self.assertEqual(FIELD_MAPPING1['type'], mapping.type)

    def test_get_a_mapping(self):
        resource = self.mgr.get(mapping_id=FIELD_MAPPING1['mapping_id'])
        expect = [
            'GET', ('/v1/rating/module_config/hashmap/mappings/' +
                    FIELD_MAPPING1['mapping_id'])]
        self.http_client.assert_called(*expect)
        self.assertEqual(FIELD_MAPPING1['mapping_id'], resource.mapping_id)
        self.assertEqual(FIELD1['field_id'], resource.field_id)
        self.assertEqual(FIELD_MAPPING1['value'], resource.value)
        self.assertEqual(FIELD_MAPPING1['cost'], resource.cost)
        self.assertEqual(FIELD_MAPPING1['type'], resource.type)

    def test_update_a_mapping(self):
        resource = self.mgr.get(mapping_id=FIELD_MAPPING1['mapping_id'])
        resource.cost = 0.2
        self.mgr.update(**resource.dirty_fields)
        expect = [
            'PUT', ('/v1/rating/module_config/hashmap/mappings/' +
                    FIELD_MAPPING1['mapping_id']),
            FIELD_MAPPING1_PUT]
        self.http_client.assert_called(*expect)

    def test_delete_a_mapping(self):
        self.mgr.delete(mapping_id=FIELD_MAPPING1['mapping_id'])
        expect = [
            'DELETE', ('/v1/rating/module_config/hashmap/mappings/' +
                       FIELD_MAPPING1['mapping_id'])]
        self.http_client.assert_called(*expect)


class MappingTest(utils.BaseTestCase):

    def setUp(self):
        super(MappingTest, self).setUp()
        self.http_client = fake_client.FakeHTTPClient(fixtures=fixtures)
        self.api = client.BaseClient(self.http_client)
        self.mgr = hashmap.MappingManager(self.api)
        self.resource = self.mgr.get(mapping_id=FIELD_MAPPING1['mapping_id'])

    def test_get_service_mapping_parent(self):
        resource = self.mgr.get(mapping_id=SERVICE_MAPPING1['mapping_id'])
        service = resource.service
        expect = [
            'GET', ('/v1/rating/module_config/hashmap/services/' +
                    SERVICE3['service_id'])]
        self.http_client.assert_called(*expect)
        self.assertEqual(SERVICE3['service_id'], service.service_id)
        field = resource.field
        self.assertIsNone(field)

    def test_get_field_mapping_parent(self):
        service = self.resource.service
        self.assertIsNone(service)
        field = self.resource.field
        expect = [
            'GET', ('/v1/rating/module_config/hashmap/fields/' +
                    FIELD1['field_id'])]
        self.http_client.assert_called(*expect)
        self.assertEqual(FIELD1['field_id'], field.field_id)

    def test_get_group(self):
        group = self.resource.group
        expect = [
            'GET', ('/v1/rating/module_config/hashmap/groups/' +
                    GROUP2['group_id'])]
        self.http_client.assert_called(*expect)
        self.assertEqual(GROUP2['group_id'], group.group_id)
        self.assertEqual(GROUP2['name'], group.name)


class ThresholdManagerTest(utils.BaseTestCase):

    def setUp(self):
        super(ThresholdManagerTest, self).setUp()
        self.http_client = fake_client.FakeHTTPClient(fixtures=fixtures)
        self.api = client.BaseClient(self.http_client)
        self.mgr = hashmap.ThresholdManager(self.api)

    def test_get_thresholds_by_group(self):
        mappings = self.mgr.findall(group_id=GROUP3['group_id'])
        expect = [
            'GET', ('/v1/rating/module_config/hashmap/thresholds?group_id=' +
                    GROUP3['group_id'])]
        self.http_client.assert_called(*expect)
        self.assertEqual(1, len(mappings))
        mapping = mappings[0]
        self.assertEqual(SERVICE_THRESHOLD1['threshold_id'],
                         mapping.threshold_id)
        self.assertEqual(SERVICE_THRESHOLD1['service_id'],
                         mapping.service_id)
        self.assertEqual(SERVICE_THRESHOLD1['group_id'],
                         mapping.group_id)
        self.assertEqual(SERVICE_THRESHOLD1['level'],
                         mapping.level)
        self.assertEqual(SERVICE_THRESHOLD1['cost'],
                         mapping.cost)
        self.assertEqual(SERVICE_THRESHOLD1['map_type'],
                         mapping.map_type)

    def test_get_a_threshold(self):
        resource = self.mgr.get(
            threshold_id=SERVICE_THRESHOLD1['threshold_id'])
        expect = [
            'GET', ('/v1/rating/module_config/hashmap/thresholds/' +
                    SERVICE_THRESHOLD1['threshold_id'])]
        self.http_client.assert_called(*expect)
        self.assertEqual(SERVICE_THRESHOLD1['threshold_id'],
                         resource.threshold_id)
        self.assertEqual(SERVICE_THRESHOLD1['service_id'],
                         resource.service_id)
        self.assertEqual(SERVICE_THRESHOLD1['level'],
                         resource.level)
        self.assertEqual(SERVICE_THRESHOLD1['cost'],
                         resource.cost)
        self.assertEqual(SERVICE_THRESHOLD1['map_type'],
                         resource.map_type)

    def test_update_a_threshold(self):
        resource = self.mgr.get(
            threshold_id=SERVICE_THRESHOLD1['threshold_id'])
        resource.cost = 5.99
        self.mgr.update(**resource.dirty_fields)
        expect = [
            'PUT', ('/v1/rating/module_config/hashmap/thresholds/' +
                    SERVICE_THRESHOLD1['threshold_id']),
            SERVICE_THRESHOLD1_PUT]
        self.http_client.assert_called(*expect)

    def test_delete_a_threshold(self):
        self.mgr.delete(threshold_id=SERVICE_THRESHOLD1['threshold_id'])
        expect = [
            'DELETE', ('/v1/rating/module_config/hashmap/thresholds/' +
                       SERVICE_THRESHOLD1['threshold_id'])]
        self.http_client.assert_called(*expect)


class ThresholdTest(utils.BaseTestCase):

    def setUp(self):
        super(ThresholdTest, self).setUp()
        self.http_client = fake_client.FakeHTTPClient(fixtures=fixtures)
        self.api = client.BaseClient(self.http_client)
        self.mgr = hashmap.ThresholdManager(self.api)
        self.resource = self.mgr.get(
            threshold_id=SERVICE_THRESHOLD1['threshold_id'])

    def test_get_service_threshold_parent(self):
        service = self.resource.service
        expect = [
            'GET', ('/v1/rating/module_config/hashmap/services/' +
                    SERVICE3['service_id'])]
        self.http_client.assert_called(*expect)
        self.assertEqual(SERVICE3['service_id'], service.service_id)
        field = self.resource.field
        self.assertIsNone(field)

    def test_get_field_mapping_parent(self):
        resource = self.mgr.get(
            threshold_id=FIELD_THRESHOLD1['threshold_id'])
        service = resource.service
        self.assertIsNone(service)
        field = resource.field
        expect = [
            'GET', ('/v1/rating/module_config/hashmap/fields/' +
                    FIELD3['field_id'])]
        self.http_client.assert_called(*expect)
        self.assertEqual(FIELD3['field_id'], field.field_id)

    def test_get_group(self):
        group = self.resource.group
        expect = [
            'GET', ('/v1/rating/module_config/hashmap/groups/' +
                    GROUP3['group_id'])]
        self.http_client.assert_called(*expect)
        self.assertEqual(GROUP3['group_id'], group.group_id)
        self.assertEqual(GROUP3['name'], group.name)


class GroupManagerTest(utils.BaseTestCase):

    def setUp(self):
        super(GroupManagerTest, self).setUp()
        self.http_client = fake_client.FakeHTTPClient(fixtures=fixtures)
        self.api = client.BaseClient(self.http_client)
        self.mgr = hashmap.GroupManager(self.api)

    def test_get_a_group(self):
        resource = self.mgr.get(group_id=GROUP2['group_id'])
        expect = [
            'GET', ('/v1/rating/module_config/hashmap/groups/' +
                    GROUP2['group_id'])]
        self.http_client.assert_called(*expect)
        self.assertEqual(GROUP2['group_id'], resource.group_id)
        self.assertEqual(GROUP2['name'], resource.name)

    def test_list_groups(self):
        resources = list(self.mgr.list())
        expect = [
            'GET', '/v1/rating/module_config/hashmap/groups']
        self.http_client.assert_called(*expect)
        self.assertEqual(3, len(resources))
        self.assertEqual(
            resources[0].group_id,
            GROUP1['group_id'])
        self.assertEqual(GROUP1['name'], resources[0].name)
        self.assertEqual(GROUP2['name'], resources[1].name)
        self.assertEqual(GROUP3['name'], resources[2].name)

    def test_delete_a_group(self):
        self.mgr.delete(group_id=GROUP2['group_id'])
        expect = [
            'DELETE', ('/v1/rating/module_config/hashmap/groups/' +
                       GROUP2['group_id'])]
        self.http_client.assert_called(*expect)

    def test_delete_a_group_recursively(self):
        self.mgr.delete(group_id=GROUP2['group_id'],
                        recursive=True)
        expect = [
            'DELETE', ('/v1/rating/module_config/hashmap/groups/' +
                       GROUP2['group_id'] +
                       '?recursive=True')]
        self.http_client.assert_called(*expect)


class GroupTest(utils.BaseTestCase):

    def setUp(self):
        super(GroupTest, self).setUp()
        self.http_client = fake_client.FakeHTTPClient(fixtures=fixtures)
        self.api = client.BaseClient(self.http_client)
        self.mgr = hashmap.GroupManager(self.api)
        self.resource = self.mgr.get(group_id=GROUP2['group_id'])

    def test_delete(self):
        self.resource.delete()
        expect = [
            'DELETE', ('/v1/rating/module_config/hashmap/groups/' +
                       GROUP2['group_id'])]
        self.http_client.assert_called(*expect)

    def test_delete_recursive(self):
        self.resource.delete(recursive=True)
        expect = [
            'DELETE', ('/v1/rating/module_config/hashmap/groups/' +
                       GROUP2['group_id'] +
                       '?recursive=True')]
        self.http_client.assert_called(*expect)

    def test_get_mappings(self):
        mappings = self.resource.mappings[:]
        expect = [
            'GET', ('/v1/rating/module_config/hashmap/mappings?group_id=' +
                    GROUP2['group_id'])]
        self.http_client.assert_called(*expect)
        self.assertEqual(1, len(mappings))
        mapping = mappings[0]
        self.assertEqual(FIELD1['field_id'], mapping.field_id)
        self.assertEqual(FIELD_MAPPING1['mapping_id'], mapping.mapping_id)
        self.assertEqual(FIELD_MAPPING1['value'], mapping.value)
        self.assertEqual(FIELD_MAPPING1['cost'], mapping.cost)
        self.assertEqual(FIELD_MAPPING1['type'], mapping.type)

    def test_get_thresholds(self):
        resource = self.mgr.get(group_id=GROUP3['group_id'])
        thresholds = resource.thresholds[:]
        expect = [
            'GET', ('/v1/rating/module_config/hashmap/thresholds?group_id=' +
                    GROUP3['group_id'])]
        self.http_client.assert_called(*expect)
        self.assertEqual(1, len(thresholds))
        threshold = thresholds[0]
        self.assertEqual(SERVICE3['service_id'], threshold.service_id)
        self.assertEqual(SERVICE_THRESHOLD1['threshold_id'],
                         threshold.threshold_id)
        self.assertEqual(SERVICE_THRESHOLD1['level'],
                         threshold.level)
        self.assertEqual(SERVICE_THRESHOLD1['cost'],
                         threshold.cost)
        self.assertEqual(SERVICE_THRESHOLD1['map_type'],
                         threshold.map_type)

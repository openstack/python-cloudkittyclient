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
from cloudkittyclient.tests.functional import base


class CkHashmapTest(base.BaseFunctionalTest):

    def __init__(self, *args, **kwargs):
        super(CkHashmapTest, self).__init__(*args, **kwargs)
        self.runner = self.cloudkitty

    def setUp(self):
        super(CkHashmapTest, self).setUp()
        self._fields = list()
        self._services = list()
        self._mappings = list()
        self._groups = list()
        self._thresholds = list()

    def tearDown(self):
        super(CkHashmapTest, self).tearDown()
        for field in self._fields:
            try:
                self.runner(
                    'hashmap field delete', params=field, has_output=False)
            except RuntimeError:
                pass
        for service in self._services:
            try:
                self.runner(
                    'hashmap service delete', params=service, has_output=False)
            except RuntimeError:
                pass
        for group in self._groups:
            try:
                self.runner(
                    'hashmap group delete', params=group, has_output=False)
            except RuntimeError:
                pass
        for mapping in self._mappings:
            try:
                self.runner(
                    'hashmap mapping delete', params=mapping, has_output=False)
            except RuntimeError:
                pass
        for threshold in self._thresholds:
            try:
                self.runner('hashmap threshold delete',
                            params=threshold, has_output=False)
            except RuntimeError:
                pass

    def test_list_mapping_types(self):
        resp = self.runner('hashmap mapping-types list')
        found_types = [elem['Mapping types'] for elem in resp]
        self.assertIn('flat', found_types)
        self.assertIn('rate', found_types)

    def test_create_get_delete_service(self):
        # Create service
        resp = self.runner('hashmap service create', params='testservice')[0]
        self.assertEqual(resp['Name'], 'testservice')
        service_id = resp['Service ID']
        self._services.append(service_id)

        # Check that resp is the same with service get and list
        resp_with_sid = self.runner(
            'hashmap service get', params=service_id)
        resp_without_sid = self.runner('hashmap service list')
        self.assertEqual(resp_with_sid, resp_without_sid)
        self.assertEqual(len(resp_with_sid), 1)

        # Check that deletion works
        self.runner('hashmap service delete',
                    params=resp['Service ID'],
                    has_output=False)
        resp = self.runner('hashmap service list')
        self.assertEqual(len(resp), 0)

    def test_group_get_create_delete(self):
        # Create group
        resp = self.runner('hashmap group create', params='testgroup')[0]
        self.assertEqual(resp['Name'], 'testgroup')
        group_id = resp['Group ID']
        self._groups.append(group_id)

        resp = self.runner('hashmap group list')
        self.assertEqual(len(resp), 1)

        # Check that deletion works
        self.runner('hashmap group delete',
                    params=group_id, has_output=False)
        resp = self.runner('hashmap group list')
        self.assertEqual(len(resp), 0)

    def test_create_get_delete_field(self):
        # Create service
        resp = self.runner('hashmap service create', params='testservice')[0]
        service_id = resp['Service ID']
        self._services.append(service_id)

        # Create field
        resp = self.runner('hashmap field create',
                           params='{} testfield'.format(service_id))[0]
        self.assertEqual(resp['Name'], 'testfield')
        self.assertEqual(resp['Service ID'], service_id)
        field_id = resp['Field ID']
        self._fields.append(field_id)

        # Check that resp is the same with field get and list
        resp_with_fid = self.runner('hashmap field get', params=field_id)
        resp_with_sid = self.runner('hashmap field list', params=service_id)
        self.assertEqual(resp_with_fid, resp_with_sid)
        self.assertEqual(len(resp_with_fid), 1)

        # Check that deletion works
        self.runner(
            'hashmap field delete', params=field_id, has_output=False)
        # resp = self.runner(
        #     'hashmap field list', params='-s {}'.format(service_id))
        resp = self.runner(
            'hashmap field list', params=service_id)
        self.assertEqual(len(resp), 0)

    def test_create_get_update_delete_mapping_service(self):
        resp = self.runner('hashmap service create', params='testservice')[0]
        service_id = resp['Service ID']
        self._services.append(service_id)

        # Create mapping
        resp = self.runner('hashmap mapping create',
                           params='-s {} 12'.format(service_id))[0]
        mapping_id = resp['Mapping ID']
        self._mappings.append(mapping_id)
        self.assertEqual(resp['Service ID'], service_id)
        self.assertEqual(float(resp['Cost']), float(12))

        # Get mapping
        resp_with_sid = self.runner(
            'hashmap mapping list', params='-s {}'.format(service_id))[0]
        resp_with_mid = self.runner(
            'hashmap mapping get', params=mapping_id)[0]
        self.assertEqual(resp_with_sid, resp_with_mid)
        self.assertEqual(resp_with_sid['Mapping ID'], mapping_id)
        self.assertEqual(resp_with_sid['Service ID'], service_id)
        self.assertEqual(float(resp_with_sid['Cost']), float(12))

        # Update mapping
        resp = self.runner('hashmap mapping update',
                           params='--cost 10 {}'.format(mapping_id))[0]
        self.assertEqual(float(resp['Cost']), float(10))

        # Check that deletion works
        self.runner(
            'hashmap mapping delete', params=mapping_id, has_output=False)
        resp = self.runner(
            'hashmap mapping list', params='-s {}'.format(service_id))
        self.assertEqual(len(resp), 0)
        self.runner(
            'hashmap service delete', params=service_id, has_output=False)

    def test_create_get_update_delete_mapping_field(self):
        resp = self.runner('hashmap service create', params='testservice')[0]
        service_id = resp['Service ID']
        self._services.append(service_id)

        resp = self.runner('hashmap field create',
                           params='{} testfield'.format(service_id))[0]
        field_id = resp['Field ID']
        self._fields.append(field_id)

        # Create mapping
        resp = self.runner(
            'hashmap mapping create',
            params='--field-id {} 12 --value testvalue'.format(field_id))[0]
        mapping_id = resp['Mapping ID']
        self._mappings.append(service_id)
        self.assertEqual(resp['Field ID'], field_id)
        self.assertEqual(float(resp['Cost']), float(12))
        self.assertEqual(resp['Value'], 'testvalue')

        # Get mapping
        resp = self.runner(
            'hashmap mapping get', params=mapping_id)[0]
        self.assertEqual(resp['Mapping ID'], mapping_id)
        self.assertEqual(float(resp['Cost']), float(12))

        # Update mapping
        resp = self.runner('hashmap mapping update',
                           params='--cost 10 {}'.format(mapping_id))[0]
        self.assertEqual(float(resp['Cost']), float(10))

    def test_group_mappings_get(self):
        # Service and group
        resp = self.runner('hashmap service create', params='testservice')[0]
        service_id = resp['Service ID']
        self._services.append(service_id)
        resp = self.runner('hashmap group create', params='testgroup')[0]
        group_id = resp['Group ID']
        self._groups.append(group_id)

        # Create service mapping bleonging to testgroup
        resp = self.runner(
            'hashmap mapping create',
            params='-s {} -g {} 12'.format(service_id, group_id))[0]
        mapping_id = resp['Mapping ID']
        self._mappings.append(mapping_id)

        resp = self.runner('hashmap group mappings get', params=group_id)[0]
        self.assertEqual(resp['Group ID'], group_id)
        self.assertEqual(float(resp['Cost']), float(12))

    def test_create_get_update_delete_threshold_service(self):
        resp = self.runner('hashmap service create', params='testservice')[0]
        service_id = resp['Service ID']
        self._services.append(service_id)

        # Create threshold
        resp = self.runner('hashmap threshold create',
                           params='-s {} 12 0.9'.format(service_id))[0]
        threshold_id = resp['Threshold ID']
        self._thresholds.append(threshold_id)
        self.assertEqual(resp['Service ID'], service_id)
        self.assertEqual(float(resp['Level']), float(12))
        self.assertEqual(float(resp['Cost']), float(0.9))

        # Get threshold
        resp_with_sid = self.runner(
            'hashmap threshold list', params='-s {}'.format(service_id))[0]
        resp_with_tid = self.runner(
            'hashmap threshold get', params=threshold_id)[0]
        self.assertEqual(resp_with_sid, resp_with_tid)
        self.assertEqual(resp_with_sid['Threshold ID'], threshold_id)
        self.assertEqual(resp_with_sid['Service ID'], service_id)
        self.assertEqual(float(resp_with_sid['Level']), float(12))
        self.assertEqual(float(resp_with_sid['Cost']), float(0.9))

        # Update threshold
        resp = self.runner('hashmap threshold update',
                           params='--cost 10 {}'.format(threshold_id))[0]
        self.assertEqual(float(resp['Cost']), float(10))

        # Check that deletion works
        self.runner(
            'hashmap threshold delete', params=threshold_id, has_output=False)
        resp = self.runner(
            'hashmap threshold list', params='-s {}'.format(service_id))
        self.assertEqual(len(resp), 0)

    def test_create_get_update_delete_threshold_field(self):
        resp = self.runner('hashmap service create', params='testservice')[0]
        service_id = resp['Service ID']
        self._services.append(service_id)

        resp = self.runner('hashmap field create',
                           params='{} testfield'.format(service_id))[0]
        field_id = resp['Field ID']
        self._fields.append(field_id)

        # Create threshold
        resp = self.runner(
            'hashmap threshold create',
            params='--field-id {} 12 0.9'.format(field_id))[0]
        threshold_id = resp['Threshold ID']
        self._thresholds.append(service_id)
        self.assertEqual(resp['Field ID'], field_id)
        self.assertEqual(float(resp['Level']), float(12))
        self.assertEqual(float(resp['Cost']), float(0.9))

        # Get threshold
        resp = self.runner('hashmap threshold get', params=threshold_id)[0]
        self.assertEqual(resp['Threshold ID'], threshold_id)
        self.assertEqual(float(resp['Level']), float(12))
        self.assertEqual(float(resp['Cost']), float(0.9))

        # Update threshold
        resp = self.runner('hashmap threshold update',
                           params='--cost 10 {}'.format(threshold_id))[0]
        self.assertEqual(float(resp['Cost']), float(10))

    def test_group_thresholds_get(self):
        # Service and group
        resp = self.runner('hashmap service create', params='testservice')[0]
        service_id = resp['Service ID']
        self._services.append(service_id)
        resp = self.runner('hashmap group create', params='testgroup')[0]
        group_id = resp['Group ID']
        self._groups.append(group_id)

        # Create service threshold bleonging to testgroup
        resp = self.runner(
            'hashmap threshold create',
            params='-s {} -g {} 12 0.9'.format(service_id, group_id))[0]
        threshold_id = resp['Threshold ID']
        self._thresholds.append(threshold_id)
        resp = self.runner('hashmap group thresholds get', params=group_id)[0]
        self.assertEqual(resp['Group ID'], group_id)
        self.assertEqual(float(resp['Level']), float(12))
        self.assertEqual(float(resp['Cost']), float(0.9))


class OSCHashmapTest(CkHashmapTest):

    def __init__(self, *args, **kwargs):
        super(OSCHashmapTest, self).__init__(*args, **kwargs)
        self.runner = self.openstack

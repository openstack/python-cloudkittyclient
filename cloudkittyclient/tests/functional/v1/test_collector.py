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


class CkCollectorTest(base.BaseFunctionalTest):

    def __init__(self, *args, **kwargs):
        super(CkCollectorTest, self).__init__(*args, **kwargs)
        self.runner = self.cloudkitty

    def test_create_get_delete_collector_mapping(self):
        # Create Mapping
        resp = self.runner(
            'collector-mapping create', params='compute gnocchi')[0]
        self.assertEqual(resp['Collector'], 'gnocchi')
        self.assertEqual(resp['Service'], 'compute')

        # Check that mapping is queryable
        resp = self.runner('collector-mapping list')
        self.assertEqual(len(resp), 1)
        resp = resp[0]
        self.assertEqual(resp['Collector'], 'gnocchi')
        self.assertEqual(resp['Service'], 'compute')

        # Delete mapping
        self.runner('collector-mapping delete',
                    params='compute', has_output=False)

        # Check that mapping was deleted
        resp = self.runner('collector-mapping list')
        self.assertEqual(len(resp), 0)

    def test_collector_enable_disable(self):
        # Enable collector
        resp = self.runner('collector enable gnocchi')
        self.assertEqual(len(resp), 1)
        resp = resp[0]
        self.assertEqual(resp['Collector'], 'gnocchi')
        self.assertEqual(resp['State'], True)

        # Disable collector
        resp = self.runner('collector disable gnocchi')
        self.assertEqual(len(resp), 1)
        resp = resp[0]
        self.assertEqual(resp['Collector'], 'gnocchi')
        self.assertEqual(resp['State'], False)


class OSCCollectorTest(CkCollectorTest):

    def __init__(self, *args, **kwargs):
        super(OSCCollectorTest, self).__init__(*args, **kwargs)
        self.runner = self.openstack

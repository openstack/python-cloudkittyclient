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


class CkRatingTest(base.BaseFunctionalTest):

    def __init__(self, *args, **kwargs):
        super(CkRatingTest, self).__init__(*args, **kwargs)
        self.runner = self.cloudkitty

    def test_module_enable_get_disable(self):
        # enable
        resp = self.runner('module enable', params='hashmap')[0]
        self.assertTrue(resp['Enabled'])

        # get
        resp = self.runner('module get', params='hashmap')[0]
        self.assertTrue(resp['Enabled'])
        self.assertEqual(resp['Module'], 'hashmap')

        # disable
        resp = self.runner('module disable', params='hashmap')[0]
        self.assertFalse(resp['Enabled'])

    def test_module_set_priority(self):
        resp = self.runner('module set priority', params='hashmap 100')[0]
        self.assertEqual(resp['Priority'], 100)


class OSCRatingTest(CkRatingTest):

    def __init__(self, *args, **kwargs):
        super(CkRatingTest, self).__init__(*args, **kwargs)
        self.runner = self.openstack

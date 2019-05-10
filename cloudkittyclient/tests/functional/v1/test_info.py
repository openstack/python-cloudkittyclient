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
import jsonpath_rw_ext as jp

from cloudkittyclient.tests.functional import base


class CkInfoTest(base.BaseFunctionalTest):

    def __init__(self, *args, **kwargs):
        super(CkInfoTest, self).__init__(*args, **kwargs)
        self.runner = self.cloudkitty

    def test_info_config_get(self):
        resp = self.runner('info config get')
        for elem in resp:
            if elem.get('Section') == 'name':
                self.assertEqual(elem['Value'], 'OpenStack')

    def test_info_metric_list(self):
        resp = self.runner('info metric list')
        res = jp.match1('$.[*].Metric', resp)
        self.assertIsNotNone(res)

    def test_info_service_get_image_size(self):
        resp = self.runner('info metric get', params='image.size')[0]
        self.assertEqual(resp['Metric'], 'image.size')


class OSCInfoTest(CkInfoTest):

    def __init__(self, *args, **kwargs):
        super(OSCInfoTest, self).__init__(*args, **kwargs)
        self.runner = self.openstack

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
from cloudkittyclient.tests.functional.v1 import base


class CkReportTest(base.BaseFunctionalTest):
    def __init__(self, *args, **kwargs):
        super(CkReportTest, self).__init__(*args, **kwargs)
        self.runner = self.cloudkitty

    def test_get_summary(self):
        resp = self.runner('summary get')[0]
        self.assertEqual(resp['Resource Type'], 'ALL')

    def test_get_summary_with_groupby(self):
        resp = self.runner('summary get', params='-g res_type tenant_id')
        self.assertEqual(len(resp), 0)

    def test_get_total(self):
        resp = self.runner('total get')
        self.assertIn('Total', resp.keys())

    def test_get_tenants(self):
        self.runner('report tenant list')


class OSCReportTest(CkReportTest):

    def __init__(self, *args, **kwargs):
        super(OSCReportTest, self).__init__(*args, **kwargs)
        self.runner = self.openstack

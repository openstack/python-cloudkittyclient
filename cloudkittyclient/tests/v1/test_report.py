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
Tests for the manager report `cloudkittyclient.v1.report`.
"""

from cloudkittyclient.openstack.common.apiclient import fake_client
from cloudkittyclient.tests import base
from cloudkittyclient.v1 import client
from cloudkittyclient.v1 import report


fixtures = {
    '/v1/report/total': {
        'GET': (
            {},
            '10.0'
        ),
    }
}


class ReportManagerTest(base.TestCase):
    def setUp(self):
        super(ReportManagerTest, self).setUp()
        fake_http_client = fake_client.FakeHTTPClient(fixtures=fixtures)
        api_client = client.Client(fake_http_client)
        self.mgr = report.ReportManager(api_client)

    def test_get(self):
        _report = self.mgr.get()
        self.assertIn('Report', repr(_report))
        self.assertEqual(10.0, _report.total)

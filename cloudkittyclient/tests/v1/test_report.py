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
import cloudkittyclient.v1.report


fixtures = {
    '/v1/report/summary': {
        'GET': (
            {},
            {'summary': [
                {
                    'tenant_id': 'ALL',
                    'res_type': 'ALL',
                    'begin': '2017-01-01T00:00:00',
                    'end': '2017-02-01T00:00:00',
                    'rate': '2325.29992'
                },
            ]},
        ),
    },
    '/v1/report/summary?tenant_id=649de47ad78a44bd8562b0aa84389b2b': {
        'GET': (
            {},
            {'summary': [
                {
                    'tenant_id': '649de47ad78a44bd8562b0aa84389b2b',
                    'res_type': 'ALL',
                    'begin': '2017-01-01T00:00:00',
                    'end': '2017-02-01T00:00:00',
                    'rate': '990.14996'
                },
            ]},
        ),
    },
    '/v1/report/summary?service=compute': {
        'GET': (
            {},
            {'summary': [
                {
                    'tenant_id': 'ALL',
                    'res_type': 'compute',
                    'begin': '2017-01-01T00:00:00',
                    'end': '2017-02-01T00:00:00',
                    'rate': '690.0'
                },
            ]},
        ),
    },
    '/v1/report/summary?groupby=res_type%2Ctenant_id': {
        'GET': (
            {},
            {'summary': [
                {
                    'tenant_id': '3747afc360b64702a53bdd64dc1b8976',
                    'res_type': 'compute',
                    'begin': '2017-01-01T00:00:00',
                    'end': '2017-02-01T00:00:00',
                    'rate': '517.5'
                },
                {
                    'tenant_id': '3747afc360b64702a53bdd64dc1b8976',
                    'res_type': 'volume',
                    'begin': '2017-01-01T00:00:00',
                    'end': '2017-02-01T00:00:00',
                    'rate': '817.64996'
                },
                {
                    'tenant_id': '649de47ad78a44bd8562b0aa84389b2b',
                    'res_type': 'compute',
                    'begin': '2017-01-01T00:00:00',
                    'end': '2017-02-01T00:00:00',
                    'rate': '172.5'
                },
                {
                    'tenant_id': '649de47ad78a44bd8562b0aa84389b2b',
                    'res_type': 'volume',
                    'begin': '2017-01-01T00:00:00',
                    'end': '2017-02-01T00:00:00',
                    'rate': '817.64996'
                },
            ]},
        ),
    },
}


class ReportSummaryManagerTest(utils.BaseTestCase):

    def setUp(self):
        super(ReportSummaryManagerTest, self).setUp()
        self.http_client = fake_client.FakeHTTPClient(fixtures=fixtures)
        self.api = client.BaseClient(self.http_client)
        self.mgr = cloudkittyclient.v1.report.ReportSummaryManager(self.api)

    def test_get_summary(self):
        self.mgr.get_summary()
        expect = [
            'GET', '/v1/report/summary'
        ]
        self.http_client.assert_called(*expect)

    def test_get_summary_with_tenant(self):
        self.mgr.get_summary(tenant_id='649de47ad78a44bd8562b0aa84389b2b')
        expect = [
            'GET',
            '/v1/report/summary?tenant_id=649de47ad78a44bd8562b0aa84389b2b'
        ]
        self.http_client.assert_called(*expect)

    def test_get_summary_with_service(self):
        self.mgr.get_summary(service='compute')
        expect = [
            'GET',
            '/v1/report/summary?service=compute'
        ]
        self.http_client.assert_called(*expect)

    def test_get_summary_with_groupby(self):
        self.mgr.get_summary(groupby='res_type,tenant_id')
        expect = [
            'GET',
            '/v1/report/summary?groupby=res_type%2Ctenant_id'
        ]
        self.http_client.assert_called(*expect)

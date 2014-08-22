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
Tests for the manager billing.quote `cloudkittyclient.v1.billing.quote`.
"""

from cloudkittyclient.openstack.common.apiclient import fake_client
from cloudkittyclient.tests import base
from cloudkittyclient.v1.billing import quote
from cloudkittyclient.v1 import client


compute = {
    'desc': {
        'image_id': "a41fba37-2429-4f15-aa00-b5bc4bf557bf",
    },
    'service': "compute",
    'volume': 1
}

fixtures = {
    '/v1/billing/quote': {
        'POST': (
            {},
            '4.2'
        ),
    }
}


class QuoteManagerTest(base.TestCase):
    def setUp(self):
        super(QuoteManagerTest, self).setUp()
        fake_http_client = fake_client.FakeHTTPClient(fixtures=fixtures)
        api_client = client.Client(fake_http_client)
        self.mgr = quote.QuoteManager(api_client)

    def test_post(self):
        _quote = self.mgr.post(json=compute)
        self.assertIn('Quote', repr(_quote))
        self.assertEqual(4.2, _quote.price)

    def test_post_raw(self):
        _quote = self.mgr.post(json=compute, return_raw=True)
        self.assertEqual(4.2, _quote)

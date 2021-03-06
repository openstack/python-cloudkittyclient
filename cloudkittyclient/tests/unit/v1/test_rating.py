# Copyright 2019 Objectif Libre
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
import decimal

from cloudkittyclient import exc
from cloudkittyclient.tests.unit.v1 import base


class TestRating(base.BaseAPIEndpointTestCase):

    def test_quote_request(self):
        res_data = [{'usage': {
            'instance': [{
                'vol': {'unit': 'undef', 'qty': '1'},
                'rating': {'price': decimal.Decimal(1)},
                'desc': {
                    'disk_total_display': 1,
                    'image_id': 'c43a3e7d-c4e6-45d6-8c8d-e2832a45bc0a',
                    'ram': 64,
                    'ephemeral': 0,
                    'vcpus': 1,
                    'source_type': 'image',
                    'disk_total': 1,
                    'flavor_id': '42',
                    'flavor': 'm1.nano',
                    'disk': 1,
                    'source_val': 'c43a3e7d-c4e6-45d6-8c8d-e2832a45bc0a'}
            }]
        }}]

        self.rating.get_quotation(res_data=res_data)
        self.api_client.post.assert_called_once_with(
            '/v1/rating/quote/', json={'resources': res_data})

    def test_get_quotation_no_res_data(self):
        self.assertRaises(exc.ArgumentRequired, self.rating.get_quotation)

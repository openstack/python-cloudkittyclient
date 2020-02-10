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

from cloudkittyclient.tests.unit.v2 import base


class TestRating(base.BaseAPIEndpointTestCase):

    def test_get_modules(self):
        self.rating.get_module()
        self.api_client.get.assert_called_once_with('/v2/rating/modules')

    def test_get_one_module(self):
        self.rating.get_module(module_id="moduleidtest")
        self.api_client.get.assert_called_once_with(
            '/v2/rating/modules/moduleidtest')

    def test_update_one_module(self):
        self.rating.update_module(module_id="moduleidtest",
                                  enabled=False, priority=42)
        self.api_client.put.assert_called_once_with(
            '/v2/rating/modules/moduleidtest',
            json={
                'enabled': False,
                'priority': 42,
            })

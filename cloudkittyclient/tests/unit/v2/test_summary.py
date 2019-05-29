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
from collections import OrderedDict

from cloudkittyclient.tests.unit.v2 import base


class TestSummary(base.BaseAPIEndpointTestCase):

    def test_get_summary(self):
        self.summary.get_summary()
        self.api_client.get.assert_called_once_with('/v2/summary')

    def test_get_summary_with_pagination_args(self):
        self.summary.get_summary(offset=10, limit=10)
        try:
            self.api_client.get.assert_called_once_with(
                '/v2/summary?limit=10&offset=10')
        except AssertionError:
            self.api_client.get.assert_called_once_with(
                '/v2/summary?offset=10&limit=10')

    def test_get_summary_filters(self):
        self.summary.get_summary(
            filters=OrderedDict([('one', 'two'), ('three', 'four')]))
        self.api_client.get.assert_called_once_with(
            '/v2/summary?filters=one%3Atwo%2Cthree%3Afour')

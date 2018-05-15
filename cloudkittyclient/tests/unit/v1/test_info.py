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
from cloudkittyclient.tests.unit.v1 import base


class TestInfo(base.BaseAPIEndpointTestCase):

    def test_get_metric(self):
        self.info.get_metric()
        self.api_client.get.assert_called_once_with('/v1/info/metrics/')

    def test_get_metric_with_arg(self):
        self.info.get_metric(metric_name='testmetric')
        self.api_client.get.assert_called_once_with(
            '/v1/info/metrics/testmetric')

    def test_get_config(self):
        self.info.get_config()
        self.api_client.get.assert_called_once_with('/v1/info/config/')

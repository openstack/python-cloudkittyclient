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
from cloudkittyclient import exc
from cloudkittyclient.tests.unit.v1 import base


class TestCollector(base.BaseAPIEndpointTestCase):

    def test_get_mapping_no_args(self):
        self.collector.get_mapping()
        self.api_client.get.assert_called_once_with('/v1/collector/mappings/')

    def test_get_mapping_service_id(self):
        self.collector.get_mapping(service='testservice')
        self.api_client.get.assert_called_once_with(
            '/v1/collector/mappings/testservice')

    def test_get_mapping_collector(self):
        self.collector.get_mapping(collector='testcollector')
        self.api_client.get.assert_called_once_with(
            '/v1/collector/mappings/?collector=testcollector')

    def test_get_mapping_collector_service_id(self):
        self.collector.get_mapping(
            service='testservice', collector='testcollector')
        self.api_client.get.assert_called_once_with(
            '/v1/collector/mappings/testservice?collector=testcollector')

    def test_create_mapping(self):
        kwargs = dict(service='testservice', collector='testcollector')
        self.collector.create_mapping(**kwargs)
        self.api_client.post.assert_called_once_with(
            '/v1/collector/mappings/', json=kwargs)

    def test_create_mapping_no_name(self):
        self.assertRaises(exc.ArgumentRequired,
                          self.collector.create_mapping,
                          collector='testcollector')

    def test_delete_mapping(self):
        kwargs = dict(service='testservice')
        self.collector.delete_mapping(**kwargs)
        self.api_client.delete.assert_called_once_with(
            '/v1/collector/mappings/', json=kwargs)

    def test_delete_mapping_no_service(self):
        self.assertRaises(exc.ArgumentRequired,
                          self.collector.create_mapping)

    def test_get_state(self):
        self.collector.get_state(name='testcollector')
        self.api_client.get.assert_called_once_with(
            '/v1/collector/states/?name=testcollector')

    def test_set_state(self):
        kwargs = dict(name='testcollector', enabled=True)
        self.collector.set_state(**kwargs)
        self.api_client.put.assert_called_once_with(
            '/v1/collector/states/', json=kwargs)

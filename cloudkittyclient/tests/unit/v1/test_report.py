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


class TestReport(base.BaseAPIEndpointTestCase):

    def test_get_summary(self):
        self.report.get_summary()
        self.api_client.get.assert_called_once_with('/v1/report/summary')

    def test_get_summary_with_groupby(self):
        self.report.get_summary(groupby=['res_type', 'tenant_id'])
        self.api_client.get.assert_called_once_with(
            '/v1/report/summary?groupby=res_type%2Ctenant_id')

    def test_get_summary_with_begin_end(self):
        self.report.get_summary(begin='begin', end='end')
        try:
            self.api_client.get.assert_called_once_with(
                '/v1/report/summary?begin=begin&end=end')
        # Passing a dict to urlencode can change arg order
        except AssertionError:
            self.api_client.get.assert_called_once_with(
                '/v1/report/summary?end=end&begin=begin')

    def test_get_total(self):
        self.report.get_total()
        self.api_client.get.assert_called_once_with('/v1/report/total')

    def test_get_total_with_begin_end(self):
        self.report.get_total(begin='begin', end='end')
        try:
            self.api_client.get.assert_called_once_with(
                '/v1/report/total?begin=begin&end=end')
        # Passing a dict to urlencode can change arg order
        except AssertionError:
            self.api_client.get.assert_called_once_with(
                '/v1/report/total?end=end&begin=begin')

    def test_get_tenants(self):
        self.report.get_tenants()
        self.api_client.get.assert_called_once_with('/v1/report/tenants')

    def test_get_tenants_with_begin_end(self):
        self.report.get_tenants(begin='begin', end='end')
        try:
            self.api_client.get.assert_called_once_with(
                '/v1/report/tenants?begin=begin&end=end')
        # Passing a dict to urlencode can change arg order
        except AssertionError:
            self.api_client.get.assert_called_once_with(
                '/v1/report/tenants?end=end&begin=begin')

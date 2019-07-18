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
from cloudkittyclient import exc
from cloudkittyclient.tests.unit.v2 import base
import datetime


class TestScope(base.BaseAPIEndpointTestCase):

    def test_get_scope(self):
        self.scope.get_scope_state()
        self.api_client.get.assert_called_once_with('/v2/scope')

    def test_get_scope_with_args(self):
        self.scope.get_scope_state(offset=10, limit=10)
        try:
            self.api_client.get.assert_called_once_with(
                '/v2/scope?limit=10&offset=10')
        except AssertionError:
            self.api_client.get.assert_called_once_with(
                '/v2/scope?offset=10&limit=10')

    def test_reset_scope_with_args(self):
        self.scope.reset_scope_state(
            state=datetime.datetime(2019, 5, 7),
            all_scopes=True)
        self.api_client.put.assert_called_once_with(
            '/v2/scope',
            json={
                'state': datetime.datetime(2019, 5, 7),
                'all_scopes': True,
            })

    def test_reset_scope_with_list_args(self):
        self.scope.reset_scope_state(
            state=datetime.datetime(2019, 5, 7),
            scope_id=['id1', 'id2'],
            all_scopes=False)
        self.api_client.put.assert_called_once_with(
            '/v2/scope',
            json={
                'state': datetime.datetime(2019, 5, 7),
                'scope_id': 'id1,id2',
            })

    def test_reset_scope_strips_none_and_false_args(self):
        self.scope.reset_scope_state(
            state=datetime.datetime(2019, 5, 7),
            all_scopes=False,
            scope_key=None,
            scope_id=['id1', 'id2'])
        self.api_client.put.assert_called_once_with(
            '/v2/scope',
            json={
                'state': datetime.datetime(2019, 5, 7),
                'scope_id': 'id1,id2',
            })

    def test_reset_scope_with_no_args_raises_exc(self):
        self.assertRaises(
            exc.ArgumentRequired,
            self.scope.reset_scope_state)

    def test_reset_scope_with_lacking_args_raises_exc(self):
        self.assertRaises(
            exc.ArgumentRequired,
            self.scope.reset_scope_state,
            state=datetime.datetime(2019, 5, 7))

    def test_reset_scope_with_both_args_raises_exc(self):
        self.assertRaises(
            exc.InvalidArgumentError,
            self.scope.reset_scope_state,
            state=datetime.datetime(2019, 5, 7),
            scope_id=['id1', 'id2'],
            all_scopes=True)

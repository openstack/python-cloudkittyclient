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


class TestPyscripts(base.BaseAPIEndpointTestCase):

    def test_list_scripts(self):
        self.pyscripts.list_scripts()
        self.api_client.get.assert_called_once_with(
            '/v1/rating/module_config/pyscripts/scripts/')

    def test_list_scripts_no_data(self):
        self.pyscripts.list_scripts(no_data=True)
        self.api_client.get.assert_called_once_with(
            '/v1/rating/module_config/pyscripts/scripts/?no_data=True')

    def test_get_script(self):
        self.pyscripts.get_script(script_id='testscript')
        self.api_client.get.assert_called_once_with(
            '/v1/rating/module_config/pyscripts/scripts/testscript')

    def test_get_script_no_arg(self):
        self.assertRaises(exc.ArgumentRequired, self.pyscripts.get_script)

    def test_create_script(self):
        kwargs = dict(name='name', data='data')
        self.pyscripts.create_script(**kwargs)
        self.api_client.post.assert_called_once_with(
            '/v1/rating/module_config/pyscripts/scripts/', json=kwargs)

    def test_create_script_no_data(self):
        self.assertRaises(
            exc.ArgumentRequired, self.pyscripts.create_script, name='name')

    def test_create_script_no_name(self):
        self.assertRaises(
            exc.ArgumentRequired, self.pyscripts.create_script, data='data')

    def test_update_script(self):
        args = dict(script_id='script_id', name='name', data='data')
        self.pyscripts.update_script(**args)
        self.api_client.get.assert_called_once_with(
            '/v1/rating/module_config/pyscripts/scripts/script_id')
        args.pop('script_id', None)
        self.api_client.put.assert_called_once_with(
            '/v1/rating/module_config/pyscripts/scripts/script_id', json=args)

    def test_update_script_no_script_id(self):
        self.assertRaises(
            exc.ArgumentRequired, self.pyscripts.update_script, name='name')

    def test_delete_script(self):
        kwargs = dict(script_id='script_id')
        self.pyscripts.delete_script(**kwargs)
        self.api_client.delete.assert_called_once_with(
            '/v1/rating/module_config/pyscripts/scripts/script_id')

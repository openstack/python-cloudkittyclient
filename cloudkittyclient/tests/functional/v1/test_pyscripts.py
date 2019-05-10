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
from cloudkittyclient.tests.functional import base


class CkPyscriptTest(base.BaseFunctionalTest):

    def __init__(self, *args, **kwargs):
        super(CkPyscriptTest, self).__init__(*args, **kwargs)
        self.runner = self.cloudkitty

    def test_create_get_update_list_delete(self):
        # Create
        resp = self.runner(
            'pyscript create', params="testscript 'return 0'")[0]
        script_id = resp['Script ID']
        self.assertEqual(resp['Name'], 'testscript')

        # Get
        resp = self.runner('pyscript get', params=script_id)[0]
        self.assertEqual(resp['Name'], 'testscript')
        self.assertEqual(resp['Script ID'], script_id)

        # Update
        resp = self.runner(
            'pyscript update',
            params="-n newname -d 'return 1' {}".format(script_id))[0]
        self.assertEqual(resp['Name'], 'newname')
        self.assertEqual(resp['Script ID'], script_id)
        self.assertEqual(resp['Data'], 'return 1')

        # List
        resp = self.runner('pyscript list')
        self.assertEqual(len(resp), 1)
        resp = resp[0]
        self.assertEqual(resp['Name'], 'newname')
        self.assertEqual(resp['Script ID'], script_id)
        self.assertEqual(resp['Data'], 'return 1')

        # Delete
        self.runner('pyscript delete', params=script_id, has_output=False)


class OSCPyscriptTest(CkPyscriptTest):

    def __init__(self, *args, **kwargs):
        super(CkPyscriptTest, self).__init__(*args, **kwargs)
        self.runner = self.openstack

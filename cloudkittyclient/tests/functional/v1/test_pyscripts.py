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
from datetime import datetime
from datetime import timedelta

from cloudkittyclient.tests.functional import base


class CkPyscriptTest(base.BaseFunctionalTest):

    def __init__(self, *args, **kwargs):
        super(CkPyscriptTest, self).__init__(*args, **kwargs)
        self.runner = self.cloudkitty

    def test_create_get_update_list_delete(self):
        future_date = datetime.now() + timedelta(days=1)
        date_iso = future_date.isoformat()
        # Create
        resp = self.runner(
            'pyscript create', params=f"testscript "
                                      f"'return 0' --start {date_iso}")[0]
        script_id = resp['Script ID']
        self.assertEqual(resp['Name'], 'testscript')

        # Get
        resp = self.runner('pyscript get', params=script_id)[0]
        self.assertEqual(resp['Name'], 'testscript')
        self.assertEqual(resp['Script ID'], script_id)

        # Update
        resp = self.runner(
            'pyscript update',
            params="-d 'return 1' {} --description "
                   "desc".format(script_id))[0]
        self.assertEqual(resp['Script Description'], 'desc')
        self.assertEqual(resp['Script ID'], script_id)
        self.assertEqual(resp['Data'], 'return 1')

        # List
        resp = self.runner('pyscript list')
        self.assertEqual(len(resp), 1)
        resp = resp[0]
        self.assertEqual(resp['Script Description'], 'desc')
        self.assertEqual(resp['Script ID'], script_id)
        self.assertEqual(resp['Data'], 'return 1')

        # Delete
        self.runner('pyscript delete', params=script_id, has_output=False)

    def test_create_get_update_list_delete_started(self):
        # Create
        resp = self.runner(
            'pyscript create', params="testscript_started "
                                      "'return 0'")[0]
        script_id = resp['Script ID']
        self.assertEqual(resp['Name'], 'testscript_started')

        # Get
        resp = self.runner('pyscript get', params=script_id)[0]
        self.assertEqual(resp['Name'], 'testscript_started')
        self.assertEqual(resp['Script ID'], script_id)

        # Should not be able to update a rule that is running (start < now)
        try:
            self.runner(
                'pyscript update',
                params="-d 'return 1' {} --description "
                       "desc".format(script_id))[0]
        except RuntimeError as e:
            expected_error = ("You are allowed to update only the attribute "
                              "[end] as this rule is already running as it "
                              "started on ")
            self.assertIn(expected_error, str(e))

        # List
        resp = self.runner('pyscript list')
        self.assertEqual(len(resp), 1)
        resp = resp[0]
        self.assertEqual(resp['Script Description'], None)
        self.assertEqual(resp['Script ID'], script_id)
        self.assertEqual(resp['Data'], 'return 0')

        # Delete
        self.runner('pyscript delete', params=script_id, has_output=False)


class OSCPyscriptTest(CkPyscriptTest):

    def __init__(self, *args, **kwargs):
        super(CkPyscriptTest, self).__init__(*args, **kwargs)
        self.runner = self.openstack

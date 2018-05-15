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
from cloudkittyclient.tests.functional.v1 import base


class CkStorageTest(base.BaseFunctionalTest):

    def __init__(self, *args, **kwargs):
        super(CkStorageTest, self).__init__(*args, **kwargs)
        self.runner = self.cloudkitty

    def test_dataframes_get(self):
        self.runner('dataframes get')


class OSCStorageTest(CkStorageTest):

    def __init__(self, *args, **kwargs):
        super(CkStorageTest, self).__init__(*args, **kwargs)
        self.runner = self.openstack

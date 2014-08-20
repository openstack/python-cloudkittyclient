# -*- coding: utf-8 -*-
# Copyright 2014 Objectif Libre
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# @author: François Magimel (linkid)

"""
Tests for the main Client interface `cloudkittyclient.client`.
"""

import mock
import six

from cloudkittyclient import client
from cloudkittyclient.common import auth
from cloudkittyclient.tests import base
from cloudkittyclient.v1 import client as v1client


VERSIONS = {
    '1': v1client,
}


class ClientTest(base.TestCase):
    def test_client_unsupported_version(self):
        self.assertRaises(ImportError, client.Client,
                          '111.11', **{})

    def test_client(self):
        for (version, instance) in six.iteritems(VERSIONS):
            with mock.patch.object(auth, 'KeystoneAuthPlugin'):
                c = client.Client(version, **{})
                self.assertIsInstance(c, instance.Client)

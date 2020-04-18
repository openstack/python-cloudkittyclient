# Copyright 2012 OpenStack Foundation
# All Rights Reserved.
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
from unittest import mock

import fixtures
import testtools

from keystoneauth1 import adapter
from keystoneauth1 import session


class BaseTestCase(testtools.TestCase):

    def setUp(self):
        super(BaseTestCase, self).setUp()
        self.useFixture(fixtures.FakeLogger())


class FakeRequest(dict):
    """Fake requests.Request object."""

    def json(self):
        return self


class FakeHTTPClient(adapter.Adapter):
    """Keystone HTTP adapter with request methods being mocks"""

    def __init__(self):
        super(FakeHTTPClient, self).__init__(session=session.Session())
        for attr in ('get', 'put', 'post', 'delete'):
            setattr(self, attr, mock.Mock(return_value=FakeRequest()))

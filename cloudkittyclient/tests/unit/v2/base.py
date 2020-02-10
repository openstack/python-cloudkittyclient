# Copyright 2019 objectif Libre
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


from cloudkittyclient.tests import utils
from cloudkittyclient.v2 import dataframes
from cloudkittyclient.v2.rating import modules
from cloudkittyclient.v2 import scope
from cloudkittyclient.v2 import summary


class BaseAPIEndpointTestCase(utils.BaseTestCase):

    def setUp(self):
        super(BaseAPIEndpointTestCase, self).setUp()
        self.api_client = utils.FakeHTTPClient()
        self.dataframes = dataframes.DataframesManager(self.api_client)
        self.scope = scope.ScopeManager(self.api_client)
        self.summary = summary.SummaryManager(self.api_client)
        self.rating = modules.RatingManager(self.api_client)

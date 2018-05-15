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

from cloudkittyclient.tests import utils
from cloudkittyclient.v1 import collector
from cloudkittyclient.v1 import info
from cloudkittyclient.v1 import rating
from cloudkittyclient.v1.rating import hashmap
from cloudkittyclient.v1.rating import pyscripts
from cloudkittyclient.v1 import report
from cloudkittyclient.v1 import storage


class BaseAPIEndpointTestCase(utils.BaseTestCase):

    def setUp(self):
        super(BaseAPIEndpointTestCase, self).setUp()
        self.api_client = utils.FakeHTTPClient()
        self.storage = storage.StorageManager(self.api_client)
        self.rating = rating.RatingManager(self.api_client)
        self.collector = collector.CollectorManager(self.api_client)
        self.info = info.InfoManager(self.api_client)
        self.report = report.ReportManager(self.api_client)
        self.pyscripts = pyscripts.PyscriptManager(self.api_client)
        self.hashmap = hashmap.HashmapManager(self.api_client)

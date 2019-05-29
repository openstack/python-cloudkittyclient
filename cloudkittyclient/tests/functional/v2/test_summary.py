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
from cloudkittyclient.tests.functional import base


class CkSummaryTest(base.BaseFunctionalTest):

    def __init__(self, *args, **kwargs):
        super(CkSummaryTest, self).__init__(*args, **kwargs)
        self.runner = self.cloudkitty

    def test_summary_get(self):
        return True
        # FIXME(peschk_l): Uncomment and update this once there is a way to set
        # the state of a summary through the client
        # resp = self.runner('summary get')


class OSCSummaryTest(CkSummaryTest):

    def __init__(self, *args, **kwargs):
        super(OSCSummaryTest, self).__init__(*args, **kwargs)
        self.runner = self.openstack

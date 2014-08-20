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
OpenStack Client interface. Handles the REST calls and responses.
"""

from cloudkittyclient.openstack.common.apiclient import client
from cloudkittyclient.v1 import report


class Client(client.BaseClient):
    """Client for the Cloudkitty v1 API."""

    def __init__(self, http_client, extensions=None):
        """Initialize a new client for the Cloudkitty v1 API."""
        super(Client, self).__init__(http_client, extensions)

        self.report = report.ReportManager(self)

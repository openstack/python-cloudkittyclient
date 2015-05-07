# Copyright 2015 Objectif Libre
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

from cloudkittyclient.v1.rating import hashmap


class Client(object):
    """Client for the Hashmap v1 API.

    :param http_client: A http client.
    """

    def __init__(self, http_client):
        """Initialize a new client for the Hashmap v1 API."""
        self.http_client = http_client
        self.services = hashmap.ServiceManager(self.http_client)
        self.fields = hashmap.FieldManager(self.http_client)
        self.mappings = hashmap.MappingManager(self.http_client)
        self.groups = hashmap.GroupManager(self.http_client)
        self.thresholds = hashmap.ThresholdManager(self.http_client)

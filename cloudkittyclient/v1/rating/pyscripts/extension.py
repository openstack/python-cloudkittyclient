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

from cloudkittyclient.v1.rating.pyscripts import client
from cloudkittyclient.v1.rating.pyscripts import shell


class Extension(object):
    """PyScripts extension.

    """

    @staticmethod
    def get_client(http_client):
        return client.Client(http_client)

    @staticmethod
    def get_shell():
        return shell

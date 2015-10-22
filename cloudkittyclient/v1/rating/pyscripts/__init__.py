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

from cloudkittyclient.common import base


class Script(base.Resource):
    key = 'script'

    def __repr__(self):
        return "<pyscripts.Script %s>" % self._info


class ScriptManager(base.CrudManager):
    resource_class = Script
    base_url = '/v1/rating/module_config/pyscripts'
    key = 'script'
    collection_key = 'scripts'

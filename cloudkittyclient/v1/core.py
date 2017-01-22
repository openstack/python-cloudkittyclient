# Copyright 2015 Objectif Libre
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


class CloudkittyModule(base.Resource):

    key = 'module'

    def __repr__(self):
        return "<CloudkittyModule %s>" % self._info

    def enable(self):
        self.enabled = True
        self.update()

    def disable(self):
        self.enabled = False
        self.update()

    def set_priority(self, value):
        self.priority = value
        self.update()


class CloudkittyModuleManager(base.CrudManager):
    resource_class = CloudkittyModule
    base_url = "/v1/rating"
    key = 'module'
    collection_key = "modules"


class Collector(base.Resource):

    key = 'collector'

    def __repr__(self):
        return "<Collector %s>" % self._info


class CollectorManager(base.Manager):
    resource_class = Collector
    base_url = "/v1/rating"
    key = "collector"
    collection_key = "collectors"


class QuotationManager(base.Manager):
    base_url = "/v1/rating/quote"

    def quote(self, resources):
        out = self.api.post(self.base_url,
                            json={'resources': resources}).json()
        return out


class ServiceInfo(base.Resource):

    key = "service"

    def __repr__(self):
        return "<Service %s>" % self._info


class ServiceInfoManager(base.CrudManager):
    resource_class = ServiceInfo
    base_url = "/v1/info"
    key = "service"
    collection_key = "services"


class ConfigInfoManager(base.Manager):
    base_url = "/v1/info/config"

    def get_config(self):
        out = self.api.get(self.base_url).json()
        return out

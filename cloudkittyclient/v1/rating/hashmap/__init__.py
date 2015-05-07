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


class Service(base.Resource):
    key = 'service'

    def __repr__(self):
        return "<hashmap.Service %s>" % self._info

    @property
    def fields(self):
        return FieldManager(client=self.manager.client).findall(
            service_id=self.service_id
        )

    @property
    def mappings(self):
        return MappingManager(client=self.manager.client).findall(
            service_id=self.service_id
        )


class ServiceManager(base.CrudManager):
    resource_class = Service
    base_url = '/v1/rating/module_config/hashmap'
    key = 'service'
    collection_key = 'services'


class Field(base.Resource):
    key = 'field'

    def __repr__(self):
        return "<hashmap.Field %s>" % self._info

    @property
    def service(self):
        return ServiceManager(client=self.manager.client).get(
            service_id=self.service_id
        )


class FieldManager(base.CrudManager):
    resource_class = Field
    base_url = '/v1/rating/module_config/hashmap'
    key = 'field'
    collection_key = 'fields'


class Mapping(base.Resource):
    key = 'mapping'

    def __repr__(self):
        return "<hashmap.Mapping %s>" % self._info

    @property
    def service(self):
        return ServiceManager(client=self.manager.client).get(
            service_id=self.service_id
        )

    @property
    def field(self):
        if self.field_id is None:
            return None
        return FieldManager(client=self.manager.client).get(
            service_id=self.service_id
        )


class MappingManager(base.CrudManager):
    resource_class = Mapping
    base_url = '/v1/rating/module_config/hashmap'
    key = 'mapping'
    collection_key = 'mappings'


class Group(base.Resource):
    key = 'group'

    def __repr__(self):
        return "<hashmap.Group %s>" % self._info

    def delete(self, recursive=False):
        return self.manager.delete(group_id=self.group_id, recursive=recursive)


class GroupManager(base.CrudManager):
    resource_class = Group
    base_url = '/v1/rating/module_config/hashmap'
    key = 'group'
    collection_key = 'groups'

    def delete(self, group_id, recursive=False):
        url = self.build_url(group_id=group_id)
        if recursive:
            url += "?recursive=True"
        return self._delete(url)


class Threshold(base.Resource):
    key = 'threshold'

    def __repr__(self):
        return "<hashmap.Threshold %s>" % self._info


class ThresholdManager(base.CrudManager):
    resource_class = Threshold
    base_url = '/v1/rating/module_config/hashmap'
    key = 'threshold'
    collection_key = 'thresholds'

    def group(self, threshold_id):
        url = ('%(base_url)s/thresholds/%(threshold_id)s/group' %
               {'base_url': self.base_url, 'threshold_id': threshold_id})
        out = self._get(url)
        return out

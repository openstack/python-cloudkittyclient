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


class BaseAttributeMixin(object):
    def _validate_attribute(self, attribute):
        attr = getattr(self, attribute)
        if attr:
            kwargs = {attribute: attr}
            return kwargs

    def _get_resource(self, mgr, attribute):
        kwargs = self._validate_attribute(attribute)
        if kwargs:
            return mgr(client=self.manager.client).get(**kwargs)

    def _get_resources(self, mgr, attribute):
        kwargs = self._validate_attribute(attribute)
        if kwargs:
            try:
                return mgr(client=self.manager.client).findall(**kwargs)
            except Exception:
                pass
        return []


class ServiceMixin(BaseAttributeMixin):
    @property
    def service(self):
        return self._get_resource(ServiceManager, 'service_id')


class FieldMixin(BaseAttributeMixin):
    @property
    def field(self):
        return self._get_resource(FieldManager, 'field_id')


class GroupMixin(BaseAttributeMixin):
    @property
    def group(self):
        return self._get_resource(GroupManager, 'group_id')


class FieldsMixin(BaseAttributeMixin):
    attribute = ''

    @property
    def fields(self):
        return self._get_resources(FieldManager, self.attribute)


class MappingsMixin(BaseAttributeMixin):
    attribute = ''

    @property
    def mappings(self):
        return self._get_resources(MappingManager, self.attribute)


class ThresholdsMixin(BaseAttributeMixin):
    attribute = ''

    @property
    def thresholds(self):
        return self._get_resources(ThresholdManager, self.attribute)


class Service(base.Resource, FieldsMixin, MappingsMixin, ThresholdsMixin):
    key = 'service'
    attribute = 'service_id'

    def __repr__(self):
        return "<hashmap.Service %s>" % self._info


class ServiceManager(base.CrudManager):
    resource_class = Service
    base_url = '/v1/rating/module_config/hashmap'
    key = 'service'
    collection_key = 'services'


class Field(base.Resource, ServiceMixin, MappingsMixin, ThresholdsMixin):
    key = 'field'
    attribute = 'field_id'

    def __repr__(self):
        return "<hashmap.Field %s>" % self._info


class FieldManager(base.CrudManager):
    resource_class = Field
    base_url = '/v1/rating/module_config/hashmap'
    key = 'field'
    collection_key = 'fields'


class Mapping(base.Resource, ServiceMixin, FieldMixin, GroupMixin):
    key = 'mapping'

    def __repr__(self):
        return "<hashmap.Mapping %s>" % self._info


class MappingManager(base.CrudManager):
    resource_class = Mapping
    base_url = '/v1/rating/module_config/hashmap'
    key = 'mapping'
    collection_key = 'mappings'


class Group(base.Resource, MappingsMixin, ThresholdsMixin):
    key = 'group'
    attribute = 'group_id'

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


class Threshold(base.Resource, ServiceMixin, FieldMixin, GroupMixin):
    key = 'threshold'

    def __repr__(self):
        return "<hashmap.Threshold %s>" % self._info


class ThresholdManager(base.CrudManager):
    resource_class = Threshold
    base_url = '/v1/rating/module_config/hashmap'
    key = 'threshold'
    collection_key = 'thresholds'

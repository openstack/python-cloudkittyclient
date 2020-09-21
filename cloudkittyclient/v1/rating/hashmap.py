# -*- coding: utf-8 -*-
# Copyright 2018 Objectif Libre
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
from cloudkittyclient.common import base
from cloudkittyclient import exc


class HashmapManager(base.BaseManager):
    """Class used to manage the Hashmap rating module"""

    url = '/v1/rating/module_config/hashmap/{endpoint}/{resource_id}'

    def get_mapping_types(self, **kwargs):
        """Returns a list of all available mapping types."""
        url = self.get_url('types', kwargs)
        return self.api_client.get(url).json()

    def get_service(self, **kwargs):
        """Returns the service corresponding to the provided ID.

        If no ID is provided, returns a list of all hashmap services.

        :param service_id: ID of the service
        :type service_id: str
        """
        if kwargs.get('service_id'):
            kwargs['resource_id'] = kwargs['service_id']
        url = self.get_url('services', kwargs)
        return self.api_client.get(url).json()

    def create_service(self, **kwargs):
        """Creates a hashmap service.

        :param name: Name of the service
        :type name: str
        """
        if not kwargs.get('name'):
            raise exc.ArgumentRequired("Argument 'service_name' is mandatory.")
        url = self.get_url('services', kwargs)
        body = dict(name=kwargs['name'])
        return self.api_client.post(url, json=body).json()

    def delete_service(self, **kwargs):
        """Deletes a hashmap service

        :param service_id: ID of the service to delete
        :type service_id: uuid
        """
        if not kwargs.get('service_id'):
            raise exc.ArgumentRequired("Argument 'service_id' is mandatory.")
        url = self.get_url('services', kwargs)
        body = dict(service_id=kwargs['service_id'])
        self.api_client.delete(url, json=body)

    def get_field(self, **kwargs):
        """Returns a hashmap field.

        Either service_id or field_id must be specified. If service_id is
        provided, all fields of the given service are returned. If field_id
        is specified, only this field is returned.

        :param service_id: ID of the service of which you want fields
        :type service_id: str
        :param field_id: ID of the field you want
        :type field_id: str
        """
        if not kwargs.get('service_id') and not kwargs.get('field_id'):
            raise exc.ArgumentRequired("Either 'service_id' or 'field_id' "
                                       "must be specified.")
        elif kwargs.get('service_id') and kwargs.get('field_id'):
            raise exc.InvalidArgumentError(
                "You can't specify both 'service_id' and 'field_id'")
        elif kwargs.get('field_id'):
            kwargs['resource_id'] = kwargs['field_id']
            kwargs.pop('service_id', None)
        else:
            kwargs.pop('resource_id', None)
        authorized_args = ['service_id']
        url = self.get_url('fields', kwargs, authorized_args)
        return self.api_client.get(url).json()

    def create_field(self, **kwargs):
        """Creates a hashmap field.

        :param name: Field name
        :type name: str
        :param service_id: ID of the service the field belongs to
        :type service_id: uuid
        """
        if not kwargs.get('name'):
            raise exc.ArgumentRequired("'name' argument is required")
        if not kwargs.get('service_id'):
            raise exc.ArgumentRequired("'service_id' argument is required")
        body = dict(name=kwargs['name'], service_id=kwargs['service_id'])
        url = self.get_url('fields', kwargs)
        return self.api_client.post(url, json=body).json()

    def delete_field(self, **kwargs):
        """Deletes the given field.

        :param field_id: ID of the field to delete.
        :type field_id: uuid
        """
        if not kwargs.get('field_id'):
            raise exc.ArgumentRequired("'field_id' argument is required")
        url = self.get_url('fields', kwargs)
        body = dict(field_id=kwargs['field_id'])
        self.api_client.delete(url, json=body)

    def get_mapping(self, **kwargs):
        """Get hashmap mappings.

        If mapping_id is not provided, you need to specify either service_id,
        field_id or group_id.

        :param mapping_id: ID of the mapping
        :type mapping_id: uuid
        :param service_id: ID of the service to filter on
        :type service_id: uuid
        :param group_id: ID of the group to filter on
        :type group_id: uuid
        :param field_id: ID of the field to filter on
        :type field_id: uuid
        :param tenant_id: ID of the tenant to filter on
        :type tenant_id: uuid
        :param filter_tenant: Explicitly filter on given tenant (allows to
                              filter on tenant being None). Defaults to false.
        :type filter_tenant: bool
        :param no_group: Filter on orphaned mappings.
        :type no_group: bool
        """
        if not kwargs.get('mapping_id'):
            if not kwargs.get('service_id') and not kwargs.get('field_id') \
               and not kwargs.get('group_id'):
                raise exc.ArgumentRequired("You must provide either 'field_id'"
                                           ", 'service_id' or 'group_id'.")
            allowed_args = ['service_id', 'group_id', 'field_id', 'tenant_id',
                            'filter_tenant', 'no_group']
        else:
            allowed_args = []
            kwargs['resource_id'] = kwargs['mapping_id']
        url = self.get_url('mappings', kwargs, allowed_args)
        return self.api_client.get(url).json()

    def create_mapping(self, **kwargs):
        """Create a hashmap mapping.

        :param cost: Cost of the mapping
        :type cost: decimal.Decimal
        :param field_id: ID of the field the mapping belongs to
        :type field_id: uuid
        :param service_id: ID of the service the mapping belongs to
        :type service_id: uuid
        :param tenant_id: ID of the tenant the mapping belongs to
        :type tenant_id: uuid
        :param group_id: ID of the group the mapping belongs to
        :type group_id: uuid
        :param type: Type of the mapping (flat or rate)
        :type type: str
        :param value: Value of the mapping
        :type value: str
        """
        if not kwargs.get('cost'):
            raise exc.ArgumentRequired("'cost' argument is required")
        if not kwargs.get('value'):
            if not kwargs.get('service_id'):
                raise exc.ArgumentRequired(
                    "'service_id' must be specified if no value is provided")
        if kwargs.get('value') and kwargs.get('service_id'):
            raise exc.InvalidArgumentError(
                "You can't specify a value when 'service_id' is specified.")
        if not kwargs.get('service_id') and not kwargs.get('field_id'):
            raise exc.ArgumentRequired("You must specify either 'service_id'"
                                       " or 'field_id'")
        elif kwargs.get('service_id') and kwargs.get('field_id'):
            raise exc.InvalidArgumentError(
                "You can't specify both 'service_id'and 'field_id'")
        body = dict(
            cost=kwargs.get('cost'),
            value=kwargs.get('value'),
            service_id=kwargs.get('service_id'),
            group_id=kwargs.get('group_id'),
            field_id=kwargs.get('field_id'),
            tenant_id=kwargs.get('tenant_id'),
            type=kwargs.get('type') or 'flat',
        )
        url = self.get_url('mappings', kwargs)
        return self.api_client.post(url, json=body).json()

    def delete_mapping(self, **kwargs):
        """Delete a hashmap mapping.

        :param mapping_id: ID of the mapping to delete.
        :type mapping_id: uuid
        """
        if not kwargs.get('mapping_id'):
            raise exc.ArgumentRequired("'mapping_id' argument is required")
        url = self.get_url('mappings', kwargs)
        body = dict(mapping_id=kwargs['mapping_id'])
        self.api_client.delete(url, json=body)

    def update_mapping(self, **kwargs):
        """Update a hashmap mapping.

        :param mapping_id: ID of the mapping to update
        :type mapping_id: uuid
        :param cost: Cost of the mapping
        :type cost: decimal.Decimal
        :param field_id: ID of the field the mapping belongs to
        :type field_id: uuid
        :param service_id: ID of the field the mapping belongs to
        :type service_id: uuid
        :param tenant_id: ID of the field the mapping belongs to
        :type tenant_id: uuid
        :param type: Type of the mapping (flat or rate)
        :type type: str
        :param value: Value of the mapping
        :type value: str
        """
        if not kwargs.get('mapping_id'):
            raise exc.ArgumentRequired("'mapping_id' argument is required")
        mapping = self.get_mapping(**kwargs)
        for key in mapping.keys():
            value = kwargs.get(key, None)
            if value is not None and mapping[key] != value:
                mapping[key] = value
        url = self.get_url('mappings', kwargs)
        self.api_client.put(url, json=mapping)
        return self.get_mapping(**kwargs)

    def get_mapping_group(self, **kwargs):
        """Get the group attached to a mapping.

        :param mapping_id: ID of the mapping to update
        :type mapping_id: uuid
        """
        if not kwargs.get('mapping_id'):
            raise exc.ArgumentRequired("'mapping_id' argument is required")
        kwargs['resource_id'] = 'group'
        allowed_args = ['mapping_id']
        url = self.get_url('mappings', kwargs, allowed_args)
        return self.api_client.get(url).json()

    def get_group(self, **kwargs):
        """Get the hashmap group corresponding to the given ID.

        If group_id is not specified, returns a list of all hashmap groups.

        :param group_id: Group ID
        :type group_id: uuid
        """
        kwargs['resource_id'] = kwargs.get('group_id') or ''
        url = self.get_url('groups', kwargs)
        return self.api_client.get(url).json()

    def create_group(self, **kwargs):
        """Create a hashmap group.

        :param name: Name of the group
        :type name: str
        """
        if not kwargs.get('name'):
            raise exc.ArgumentRequired("'name' argument is required")
        body = dict(name=kwargs['name'])
        url = self.get_url('groups', kwargs)
        return self.api_client.post(url, json=body).json()

    def delete_group(self, **kwargs):
        """Delete a hashmap group.

        :param group_id: ID of the group to delete
        :type group_id: uuid
        :param recursive: Delete mappings recursively
        :type recursive: bool
        """
        if not kwargs.get('group_id'):
            raise exc.ArgumentRequired("'group_id' argument is required")
        body = dict(
            group_id=kwargs['group_id'],
            recursive=kwargs.get('recursive', False))
        url = self.get_url('groups', kwargs)
        self.api_client.delete(url, json=body)

    def get_group_mappings(self, **kwargs):
        """Get the mappings attached to the given group.

        :param group_id: ID of the group
        :type group_id: uuid
        """
        if not kwargs.get('group_id'):
            raise exc.ArgumentRequired("'group_id' argument is required")
        authorized_args = ['group_id']
        kwargs['resource_id'] = 'mappings'
        url = self.get_url('groups', kwargs, authorized_args)
        return self.api_client.get(url).json()

    def get_group_thresholds(self, **kwargs):
        """Get the thresholds attached to the given group.

        :param group_id: ID of the group
        :type group_id: uuid
        """
        if not kwargs.get('group_id'):
            raise exc.ArgumentRequired("'group_id' argument is required")
        authorized_args = ['group_id']
        kwargs['resource_id'] = 'thresholds'
        url = self.get_url('groups', kwargs, authorized_args)
        return self.api_client.get(url).json()

    def get_threshold(self, **kwargs):
        """Get hashmap thresholds.

        If threshold_id is not provided, you need to specify either service_id,
        field_id or group_id.

        :param threshold_id: ID of the threshold
        :type threshold_id: uuid
        :param service_id: ID of the service to filter on
        :type service_id: uuid
        :param group_id: ID of the group to filter on
        :type group_id: uuid
        :param field_id: ID of the field to filter on
        :type field_id: uuid
        :param tenant_id: ID of the tenant to filter on
        :type tenant_id: uuid
        :param filter_tenant: Explicitly filter on given tenant (allows to
                              filter on tenant being None). Defaults to false.
        :type filter_tenant: bool
        :param no_group: Filter on orphaned thresholds.
        :type no_group: bool
        """
        if not kwargs.get('threshold_id'):
            if not kwargs.get('service_id') and not kwargs.get('field_id') \
               and not kwargs.get('group_id'):
                raise exc.ArgumentRequired("You must provide either 'field_id'"
                                           ", 'service_id' or 'group_id'.")
            allowed_args = ['service_id', 'group_id', 'field_id', 'tenant_id',
                            'filter_tenant', 'no_group']
        else:
            allowed_args = []
            kwargs['resource_id'] = kwargs['threshold_id']
        url = self.get_url('thresholds', kwargs, allowed_args)
        return self.api_client.get(url).json()

    def create_threshold(self, **kwargs):
        """Create a hashmap threshold.

        :param cost: Cost of the threshold
        :type cost: decimal.Decimal
        :param field_id: ID of the field the threshold belongs to
        :type field_id: uuid
        :param service_id: ID of the service the threshold belongs to
        :type service_id: uuid
        :param tenant_id: ID of the tenant the threshold belongs to
        :type tenant_id: uuid
        :param group_id: ID of the group the threshold belongs to
        :type group_id: uuid
        :param type: Type of the threshold (flat or rate)
        :type type: str
        :param level: Level of the threshold
        :type level: str
        """
        for arg in ['cost', 'level']:
            if kwargs.get(arg) is None:
                raise exc.ArgumentRequired(
                    "'{}' argument is required".format(arg))
        if not kwargs.get('service_id') and not kwargs.get('field_id'):
            raise exc.ArgumentRequired("You must specify either 'service_id'"
                                       " or 'field_id'")
        body = dict(
            cost=kwargs.get('cost'),
            level=kwargs.get('level'),
            service_id=kwargs.get('service_id'),
            field_id=kwargs.get('field_id'),
            group_id=kwargs.get('group_id'),
            tenant_id=kwargs.get('tenant_id'),
            type=kwargs.get('type') or 'flat',
        )
        url = self.get_url('thresholds', kwargs)
        return self.api_client.post(url, json=body).json()

    def delete_threshold(self, **kwargs):
        """Delete a hashmap threshold.

        :param threshold_id: ID of the threshold to delete.
        :type threshold_id: uuid
        """
        if not kwargs.get('threshold_id'):
            raise exc.ArgumentRequired("'threshold_id' argument is required")
        url = self.get_url('thresholds', kwargs)
        body = dict(threshold_id=kwargs['threshold_id'])
        self.api_client.delete(url, json=body)

    def update_threshold(self, **kwargs):
        """Update a hashmap threshold.

        :param threshold_id: ID of the threshold to update
        :type threshold_id: uuid
        :param cost: Cost of the threshold
        :type cost: decimal.Decimal
        :param field_id: ID of the field the threshold belongs to
        :type field_id: uuid
        :param service_id: ID of the field the threshold belongs to
        :type service_id: uuid
        :param tenant_id: ID of the field the threshold belongs to
        :type tenant_id: uuid
        :param type: Type of the threshold (flat or rate)
        :type type: str
        :param level: Level of the threshold
        :type level: str
        """
        if not kwargs.get('threshold_id'):
            raise exc.ArgumentRequired("'threshold_id' argument is required")
        threshold = self.get_threshold(**kwargs)
        for key in threshold.keys():
            value = kwargs.get(key, None)
            if value is not None and threshold[key] != value:
                threshold[key] = value
        url = self.get_url('thresholds', kwargs)
        self.api_client.put(url, json=threshold)
        return self.get_threshold(**kwargs)

    def get_threshold_group(self, **kwargs):
        """Get the group attached to a threshold.

        :param threshold_id: ID of the threshold to update
        :type threshold_id: uuid
        """
        if not kwargs.get('threshold_id'):
            raise exc.ArgumentRequired("'threshold_id' argument is required")
        kwargs['resource_id'] = 'group'
        allowed_args = ['threshold_id']
        url = self.get_url('thresholds', kwargs, allowed_args)
        return self.api_client.get(url).json()

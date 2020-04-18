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
from unittest import mock

from cloudkittyclient import exc
from cloudkittyclient.tests.unit.v1 import base
from cloudkittyclient.tests import utils


class TestHashmap(base.BaseAPIEndpointTestCase):

    def test_get_mapping_types(self):
        self.hashmap.get_mapping_types()
        self.api_client.get.assert_called_once_with(
            '/v1/rating/module_config/hashmap/types/')

    def test_get_service(self):
        self.hashmap.get_service()
        self.api_client.get.assert_called_once_with(
            '/v1/rating/module_config/hashmap/services/')

    def test_get_service_service_id(self):
        self.hashmap.get_service(service_id='service_id')
        self.api_client.get.assert_called_once_with(
            '/v1/rating/module_config/hashmap/services/service_id')

    def test_create_service(self):
        kwargs = dict(name='service')
        self.hashmap.create_service(**kwargs)
        self.api_client.post.assert_called_once_with(
            '/v1/rating/module_config/hashmap/services/', json=kwargs)

    def test_create_service_no_name(self):
        self.assertRaises(exc.ArgumentRequired, self.hashmap.create_service)

    def test_delete_service(self):
        self.hashmap.delete_service(service_id='service_id')
        self.api_client.delete.assert_called_once_with(
            '/v1/rating/module_config/hashmap/services/',
            json={'service_id': 'service_id'})

    def test_delete_service_no_id(self):
        self.assertRaises(exc.ArgumentRequired, self.hashmap.delete_service)

    def test_get_fields_of_service(self):
        self.hashmap.get_field(service_id='service_id')
        self.api_client.get.assert_called_once_with(
            '/v1/rating/module_config/hashmap/fields/?service_id=service_id')

    def test_get_field(self):
        self.hashmap.get_field(field_id='field_id')
        self.api_client.get.assert_called_once_with(
            '/v1/rating/module_config/hashmap/fields/field_id')

    def test_get_field_no_args(self):
        self.assertRaises(exc.ArgumentRequired, self.hashmap.get_field)

    def test_get_field_with_service_id_and_field_id(self):
        self.assertRaises(exc.InvalidArgumentError, self.hashmap.get_field,
                          service_id='service_id', field_id='field_id')

    def test_create_field(self):
        kwargs = dict(name='name', service_id='service_id')
        self.hashmap.create_field(**kwargs)
        self.api_client.post.assert_called_once_with(
            '/v1/rating/module_config/hashmap/fields/', json=kwargs)

    def test_create_field_no_name(self):
        self.assertRaises(exc.ArgumentRequired,
                          self.hashmap.create_field,
                          service_id='service_id')

    def test_create_field_no_service_id(self):
        self.assertRaises(
            exc.ArgumentRequired, self.hashmap.create_field, name='name')

    def test_delete_field(self):
        kwargs = dict(field_id='field_id')
        self.hashmap.delete_field(**kwargs)
        self.api_client.delete.assert_called_once_with(
            '/v1/rating/module_config/hashmap/fields/', json=kwargs)

    def test_delete_field_no_arg(self):
        self.assertRaises(exc.ArgumentRequired, self.hashmap.delete_field)

    def test_get_mapping_with_id(self):
        self.hashmap.get_mapping(mapping_id='mapping_id')
        self.api_client.get.assert_called_once_with(
            '/v1/rating/module_config/hashmap/mappings/mapping_id')

    def test_get_mapping_service_id(self):
        self.hashmap.get_mapping(service_id='service_id')
        self.api_client.get.assert_called_once_with(
            '/v1/rating/module_config/hashmap/mappings/?service_id=service_id')

    def test_get_mapping_no_args(self):
        self.assertRaises(exc.ArgumentRequired, self.hashmap.get_mapping)

    def test_create_mapping(self):
        kwargs = dict(cost=2, value='value', field_id='field_id')
        body = dict(
            cost=kwargs.get('cost'),
            value=kwargs.get('value'),
            service_id=kwargs.get('service_id'),
            field_id=kwargs.get('field_id'),
            group_id=kwargs.get('group_id'),
            tenant_id=kwargs.get('tenant_id'),
            type=kwargs.get('type') or 'flat',
        )
        self.hashmap.create_mapping(**kwargs)
        self.api_client.post.assert_called_once_with(
            '/v1/rating/module_config/hashmap/mappings/', json=body)

    def test_create_mapping_no_cost(self):
        self.assertRaises(exc.ArgumentRequired, self.hashmap.create_mapping,
                          value='value', field_id='field_id')

    def test_create_mapping_no_id(self):
        self.assertRaises(exc.ArgumentRequired, self.hashmap.create_mapping,
                          value='value', cost=12)

    def test_create_mapping_field_and_service_id(self):
        self.assertRaises(
            exc.InvalidArgumentError, self.hashmap.create_mapping, cost=12,
            field_id='field_id', service_id='service_id')

    def test_create_mapping_value_and_service_id(self):
        self.assertRaises(
            exc.InvalidArgumentError, self.hashmap.create_mapping,
            value='value', service_id='service_id', cost=0.8)

    def test_update_mapping(self):
        kwargs = dict(
            cost=12,
            value='value',
            service_id='service_id',
            field_id='field_id',
            tenant_id='tenant_id',
            type='type',
            mapping_id='mapping_id',
        )
        fake_get = mock.Mock(return_value=utils.FakeRequest(
            cost='Bad value',
            value='Bad value',
            service_id='Bad value',
            field_id='Bad value',
            tenant_id='Bad value',
            type='Bad value',
            mapping_id='mapping_id',
        ))
        self.api_client.get = fake_get
        self.hashmap.update_mapping(**kwargs)
        self.api_client.get.assert_called_with(
            '/v1/rating/module_config/hashmap/mappings/mapping_id')
        self.api_client.put.assert_called_once_with(
            '/v1/rating/module_config/hashmap/mappings/', json=kwargs)

    def test_update_mapping_no_arg(self):
        self.assertRaises(exc.ArgumentRequired, self.hashmap.update_mapping)

    def test_get_mapping_group(self):
        self.hashmap.get_mapping_group(mapping_id='mapping_id')
        self.api_client.get.assert_called_once_with(
            '/v1/rating/module_config/'
            'hashmap/mappings/group?mapping_id=mapping_id')

    def test_delete_mapping(self):
        kwargs = dict(mapping_id='mapping_id')
        self.hashmap.delete_mapping(**kwargs)
        self.api_client.delete.assert_called_once_with(
            '/v1/rating/module_config/hashmap/mappings/', json=kwargs)

    def test_delete_mapping_no_arg(self):
        self.assertRaises(exc.ArgumentRequired, self.hashmap.delete_mapping)

    def test_get_mapping_group_no_arg(self):
        self.assertRaises(exc.ArgumentRequired, self.hashmap.get_mapping_group)

    def test_get_group_no_arg(self):
        self.hashmap.get_group()
        self.api_client.get.assert_called_once_with(
            '/v1/rating/module_config/hashmap/groups/')

    def test_get_group(self):
        self.hashmap.get_group(group_id='group_id')
        self.api_client.get.assert_called_once_with(
            '/v1/rating/module_config/hashmap/groups/group_id')

    def test_create_group(self):
        kwargs = dict(name='group')
        self.hashmap.create_group(**kwargs)
        self.api_client.post.assert_called_once_with(
            '/v1/rating/module_config/hashmap/groups/',
            json=kwargs)

    def test_create_group_no_name(self):
        self.assertRaises(exc.ArgumentRequired, self.hashmap.create_group)

    def test_delete_group(self):
        kwargs = dict(group_id='group_id')
        self.hashmap.delete_group(**kwargs)
        kwargs['recursive'] = False
        self.api_client.delete.assert_called_once_with(
            '/v1/rating/module_config/hashmap/groups/',
            json=kwargs)

    def test_delete_group_recursive(self):
        kwargs = dict(group_id='group_id', recursive=True)
        self.hashmap.delete_group(**kwargs)
        self.api_client.delete.assert_called_once_with(
            '/v1/rating/module_config/hashmap/groups/',
            json=kwargs)

    def test_delete_group_no_id(self):
        self.assertRaises(exc.ArgumentRequired, self.hashmap.create_group)

    def test_get_group_mappings(self):
        self.hashmap.get_group_mappings(group_id='group_id')
        self.api_client.get.assert_called_once_with(
            '/v1/rating/module_config/hashmap/groups/mappings'
            '?group_id=group_id')

    def test_get_group_mappings_no_args(self):
        self.assertRaises(
            exc.ArgumentRequired, self.hashmap.get_group_mappings)

    def test_get_group_thresholds(self):
        self.hashmap.get_group_thresholds(group_id='group_id')
        self.api_client.get.assert_called_once_with(
            '/v1/rating/module_config/hashmap/groups/thresholds'
            '?group_id=group_id')

    def test_get_group_thresholds_no_args(self):
        self.assertRaises(
            exc.ArgumentRequired, self.hashmap.get_group_thresholds)

    def test_get_threshold_with_id(self):
        self.hashmap.get_threshold(threshold_id='threshold_id')
        self.api_client.get.assert_called_once_with(
            '/v1/rating/module_config/hashmap/thresholds/threshold_id')

    def test_get_threshold_service_id(self):
        self.hashmap.get_threshold(service_id='service_id')
        self.api_client.get.assert_called_once_with(
            '/v1/rating/module_config/hashmap/thresholds/'
            '?service_id=service_id')

    def test_get_threshold_no_args(self):
        self.assertRaises(exc.ArgumentRequired, self.hashmap.get_threshold)

    def test_create_threshold(self):
        kwargs = dict(cost=2, level=123, field_id='field_id')
        body = dict(
            cost=kwargs.get('cost'),
            level=kwargs.get('level'),
            service_id=kwargs.get('service_id'),
            field_id=kwargs.get('field_id'),
            group_id=kwargs.get('group_id'),
            tenant_id=kwargs.get('tenant_id'),
            type=kwargs.get('type') or 'flat',
        )
        self.hashmap.create_threshold(**kwargs)
        self.api_client.post.assert_called_once_with(
            '/v1/rating/module_config/hashmap/thresholds/', json=body)

    def test_create_threshold_no_cost(self):
        self.assertRaises(exc.ArgumentRequired, self.hashmap.create_threshold,
                          level=123, field_id='field_id')

    def test_create_threshold_no_id(self):
        self.assertRaises(exc.ArgumentRequired, self.hashmap.create_threshold,
                          level=123, cost=12)

    def test_create_threshold_field_and_service_id(self):
        self.assertRaises(
            exc.ArgumentRequired, self.hashmap.create_threshold, cost=12,
            field_id='field_id', service_id='service_id')

    def test_delete_threshold(self):
        kwargs = dict(threshold_id='threshold_id')
        self.hashmap.delete_threshold(**kwargs)
        self.api_client.delete.assert_called_once_with(
            '/v1/rating/module_config/hashmap/thresholds/', json=kwargs)

    def test_delete_threshold_no_arg(self):
        self.assertRaises(exc.ArgumentRequired, self.hashmap.delete_threshold)

    def test_update_threshold(self):
        kwargs = dict(
            cost=12,
            level=123,
            service_id='service_id',
            field_id='field_id',
            tenant_id='tenant_id',
            type='type',
            threshold_id='threshold_id'
        )
        fake_get = mock.Mock(return_value=utils.FakeRequest(
            cost='Bad value',
            level='Bad value',
            service_id='Bad value',
            field_id='Bad value',
            tenant_id='Bad value',
            type='Bad value',
            threshold_id='threshold_id'
        ))
        self.api_client.get = fake_get
        self.hashmap.update_threshold(**kwargs)
        self.api_client.get.assert_called_with(
            '/v1/rating/module_config/hashmap/thresholds/threshold_id')
        self.api_client.put.assert_called_once_with(
            '/v1/rating/module_config/hashmap/thresholds/', json=kwargs)

    def test_update_threshold_no_arg(self):
        self.assertRaises(exc.ArgumentRequired, self.hashmap.update_threshold)

    def test_get_threshold_group(self):
        self.hashmap.get_threshold_group(threshold_id='threshold_id')
        self.api_client.get.assert_called_once_with(
            '/v1/rating/module_config/'
            'hashmap/thresholds/group?threshold_id=threshold_id')

    def test_get_threshold_group_no_arg(self):
        self.assertRaises(
            exc.ArgumentRequired, self.hashmap.get_threshold_group)

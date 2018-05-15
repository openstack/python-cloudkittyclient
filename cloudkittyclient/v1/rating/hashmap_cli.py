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
from cliff import command
from cliff import lister

from cloudkittyclient import utils


class CliGetMappingTypes(lister.Lister):
    """Get hashmap mapping types/"""
    def take_action(self, parsed_args):
        client = utils.get_client_from_osc(self)
        resp = client.rating.hashmap.get_mapping_types()
        return ['Mapping types'], [[item] for item in resp]


class CliGetService(lister.Lister):
    """Get a hashmap service"""

    columns = [
        ('name', 'Name'),
        ('service_id', 'Service ID'),
    ]

    def take_action(self, parsed_args):
        resp = utils.get_client_from_osc(self).rating.hashmap.get_service(
            service_id=parsed_args.service_id,
        )
        # NOTE(lukapeschke): This can't be done with 'or', because it would
        # lead to resp being [[]] if resp['services'] is an empty list. Having
        # a list in a list causes cliff to display a row of 'None' instead of
        # nothing
        values = utils.list_to_cols([resp], self.columns)
        return [col[1] for col in self.columns], values

    def get_parser(self, prog_name):
        parser = super(CliGetService, self).get_parser(prog_name)
        parser.add_argument('service_id', type=str, help='Service ID')
        return parser


class CliListService(lister.Lister):
    """List hashmap services."""

    columns = [
        ('name', 'Name'),
        ('service_id', 'Service ID'),
    ]

    def take_action(self, parsed_args):
        resp = utils.get_client_from_osc(self).rating.hashmap.get_service()
        # NOTE(lukapeschke): This can't be done with 'or', because it would
        # lead to resp being [[]] if resp['services'] is an empty list. Having
        # a list in a list causes cliff to display a row of 'None' instead of
        # nothing
        values = utils.list_to_cols(resp['services'], self.columns)
        return [col[1] for col in self.columns], values


class CliCreateService(lister.Lister):
    """Create a hashmap service."""

    columns = [
        ('name', 'Name'),
        ('service_id', 'Service ID'),
    ]

    def take_action(self, parsed_args):
        resp = utils.get_client_from_osc(self).rating.hashmap.create_service(
            **vars(parsed_args))
        values = utils.list_to_cols(resp, self.columns)
        return [col[1] for col in self.columns], values

    def get_parser(self, prog_name):
        parser = super(CliCreateService, self).get_parser(prog_name)
        parser.add_argument('name', type=str, help='Service Name')
        return parser


class CliDeleteService(command.Command):
    """Delete a hashmap service"""

    def take_action(self, parsed_args):
        utils.get_client_from_osc(self).rating.hashmap.delete_service(
            **vars(parsed_args))

    def get_parser(self, prog_name):
        parser = super(CliDeleteService, self).get_parser(prog_name)
        parser.add_argument('service_id', type=str, help='Service ID')
        return parser


class CliGetField(lister.Lister):
    """Get a Hashmap field."""
    columns = [
        ('name', 'Name'),
        ('field_id', 'Field ID'),
        ('service_id', 'Service ID'),
    ]

    def take_action(self, parsed_args):
        resp = utils.get_client_from_osc(self).rating.hashmap.get_field(
            field_id=parsed_args.field_id,
        )
        values = utils.list_to_cols([resp], self.columns)
        return [col[1] for col in self.columns], values

    def get_parser(self, prog_name):
        parser = super(CliGetField, self).get_parser(prog_name)
        parser.add_argument('field_id', type=str, help='Field ID')
        return parser


class CliListField(lister.Lister):
    """List hashmap fields for the given service."""

    columns = [
        ('name', 'Name'),
        ('field_id', 'Field ID'),
        ('service_id', 'Service ID'),
    ]

    def take_action(self, parsed_args):
        resp = utils.get_client_from_osc(self).rating.hashmap.get_field(
            service_id=parsed_args.service_id,
        )
        values = utils.list_to_cols(resp['fields'], self.columns)
        return [col[1] for col in self.columns], values

    def get_parser(self, prog_name):
        parser = super(CliListField, self).get_parser(prog_name)
        parser.add_argument('service_id', type=str, help='Service ID')
        return parser


class CliCreateField(lister.Lister):
    """Create a hashmap field."""
    columns = [
        ('name', 'Name'),
        ('field_id', 'Field ID'),
        ('service_id', 'Service ID'),
    ]

    def take_action(self, parsed_args):
        resp = utils.get_client_from_osc(self).rating.hashmap.create_field(
            **vars(parsed_args))
        resp = [resp] if resp.get('fields') is None else resp['fields']
        values = utils.list_to_cols(resp, self.columns)
        return [col[1] for col in self.columns], values

    def get_parser(self, prog_name):
        parser = super(CliCreateField, self).get_parser(prog_name)
        parser.add_argument('service_id', type=str, help='Service ID')
        parser.add_argument('name', type=str, help='Field name')
        return parser


class CliDeleteField(command.Command):
    """Delete a hashmap field."""

    def take_action(self, parsed_args):
        utils.get_client_from_osc(self).rating.hashmap.delete_field(
            **vars(parsed_args))

    def get_parser(self, prog_name):
        parser = super(CliDeleteField, self).get_parser(prog_name)
        parser.add_argument('field_id', type=str, help='Field ID')
        return parser


class CliGetMapping(lister.Lister):
    """Get a hashmap mapping."""

    columns = [
        ('mapping_id', 'Mapping ID'),
        ('value', 'Value'),
        ('cost', 'Cost'),
        ('type', 'Type'),
        ('field_id', 'Field ID'),
        ('service_id', 'Service ID'),
        ('group_id', 'Group ID'),
        ('tenant_id', 'Project ID'),
    ]

    def take_action(self, parsed_args):
        resp = utils.get_client_from_osc(self).rating.hashmap.get_mapping(
            mapping_id=parsed_args.mapping_id)
        values = utils.list_to_cols([resp], self.columns)
        return [col[1] for col in self.columns], values

    def get_parser(self, prog_name):
        parser = super(CliGetMapping, self).get_parser(prog_name)
        parser.add_argument('mapping_id', type=str,
                            help='Mapping ID to filter on')
        return parser


class CliListMapping(lister.Lister):
    """List hashmap mappings."""

    columns = [
        ('mapping_id', 'Mapping ID'),
        ('value', 'Value'),
        ('cost', 'Cost'),
        ('type', 'Type'),
        ('field_id', 'Field ID'),
        ('service_id', 'Service ID'),
        ('group_id', 'Group ID'),
        ('tenant_id', 'Project ID'),
    ]

    def take_action(self, parsed_args):
        resp = utils.get_client_from_osc(self).rating.hashmap.get_mapping(
            **vars(parsed_args))
        values = utils.list_to_cols(resp['mappings'], self.columns)
        return [col[1] for col in self.columns], values

    def get_parser(self, prog_name):
        parser = super(CliListMapping, self).get_parser(prog_name)
        parser.add_argument('-s', '--service-id', type=str,
                            help='Service ID to filter on')
        parser.add_argument('-g', '--group-id', type=str,
                            help='Group ID to filter on')
        parser.add_argument('--field-id', type=str,
                            help='Field ID to filter on')
        parser.add_argument('-p', '--project-id', type=str, dest='tenant_id',
                            help='Project ID to filter on')
        parser.add_argument('--filter-tenant', action='store_true',
                            help='Explicitly filter on given tenant (allows '
                            'to filter on tenant being None)')
        parser.add_argument('--no-group', action='store_true',
                            help='Filter on orphaned mappings')
        return parser


class CliCreateMapping(lister.Lister):
    """Create a Hashmap mapping."""
    columns = [
        ('mapping_id', 'Mapping ID'),
        ('value', 'Value'),
        ('cost', 'Cost'),
        ('type', 'Type'),
        ('field_id', 'Field ID'),
        ('service_id', 'Service ID'),
        ('group_id', 'Group ID'),
        ('tenant_id', 'Project ID'),
    ]

    def take_action(self, parsed_args):
        resp = utils.get_client_from_osc(self).rating.hashmap.create_mapping(
            **vars(parsed_args))
        values = utils.list_to_cols([resp], self.columns)
        return [col[1] for col in self.columns], values

    def get_parser(self, prog_name):
        parser = super(CliCreateMapping, self).get_parser(prog_name)
        parser.add_argument('-s', '--service-id', type=str, help='Service ID')
        parser.add_argument('-g', '--group-id', type=str, help='Group ID')
        parser.add_argument('--field-id', type=str, help='Field ID')
        parser.add_argument('-p', '--project-id', type=str, dest='tenant_id',
                            help='Project ID')
        parser.add_argument('-t', '--type', type=str, help='Mapping type')
        parser.add_argument('--value', type=str, help='Value')
        parser.add_argument('cost', type=float, help='Cost')
        return parser


class CliDeleteMapping(command.Command):
    """Delete a Hashmap mapping."""

    def take_action(self, parsed_args):
        utils.get_client_from_osc(self).rating.hashmap.delete_mapping(
            **vars(parsed_args))

    def get_parser(self, prog_name):
        parser = super(CliDeleteMapping, self).get_parser(prog_name)
        parser.add_argument('mapping_id', type=str, help='Mapping ID')
        return parser


class CliUpdateMapping(lister.Lister):
    """Update a Hashmap mapping."""

    columns = [
        ('mapping_id', 'Mapping ID'),
        ('value', 'Value'),
        ('cost', 'Cost'),
        ('type', 'Type'),
        ('field_id', 'Field ID'),
        ('service_id', 'Service ID'),
        ('group_id', 'Group ID'),
        ('tenant_id', 'Project ID'),
    ]

    def take_action(self, parsed_args):
        resp = utils.get_client_from_osc(self).rating.hashmap.update_mapping(
            **vars(parsed_args))
        values = utils.list_to_cols([resp], self.columns)
        return [col[1] for col in self.columns], values

    def get_parser(self, prog_name):
        parser = super(CliUpdateMapping, self).get_parser(prog_name)
        parser.add_argument('-s', '--service-id', type=str, help='Service ID')
        parser.add_argument('-g', '--group-id', type=str, help='Group ID')
        parser.add_argument('--field-id', type=str, help='Field ID')
        parser.add_argument('-p', '--project-id', type=str, dest='tenant_id',
                            help='Project ID')
        parser.add_argument('--value', type=str, help='Value')
        parser.add_argument('--cost', type=str, help='Cost')
        parser.add_argument('mapping_id', type=str, help='Mapping ID')
        return parser


class CliListGroup(lister.Lister):
    """List existing hashmap groups."""

    columns = [
        ('name', 'Name'),
        ('group_id', 'Group ID'),
    ]

    def take_action(self, parsed_args):
        resp = utils.get_client_from_osc(self).rating.hashmap.get_group()
        values = utils.list_to_cols(resp['groups'], self.columns)
        return [col[1] for col in self.columns], values


class CliCreateGroup(lister.Lister):
    """Create a Hashmap group."""
    columns = [
        ('name', 'Name'),
        ('group_id', 'Group ID'),
    ]

    def take_action(self, parsed_args):
        resp = utils.get_client_from_osc(self).rating.hashmap.create_group(
            **vars(parsed_args))
        values = utils.list_to_cols([resp], self.columns)
        return [col[1] for col in self.columns], values

    def get_parser(self, prog_name):
        parser = super(CliCreateGroup, self).get_parser(prog_name)
        parser.add_argument('name', type=str, help='Group Name')
        return parser


class CliDeleteGroup(command.Command):
    """Create a Hashmap group."""

    def take_action(self, parsed_args):
        utils.get_client_from_osc(self).rating.hashmap.delete_group(
            **vars(parsed_args))

    def get_parser(self, prog_name):
        parser = super(CliDeleteGroup, self).get_parser(prog_name)
        parser.add_argument('--recursive', action='store_true',
                            help='Delete mappings recursively')
        parser.add_argument('group_id', type=str, help='Group ID')
        return parser


class CliGetGroupMappings(lister.Lister):
    """Get all Hashmap mappings for the given group."""

    columns = [
        ('mapping_id', 'Mapping ID'),
        ('value', 'Value'),
        ('cost', 'Cost'),
        ('type', 'Type'),
        ('field_id', 'Field ID'),
        ('service_id', 'Service ID'),
        ('group_id', 'Group ID'),
        ('tenant_id', 'Project ID'),
    ]

    def take_action(self, parsed_args):
        client = utils.get_client_from_osc(self)
        resp = client.rating.hashmap.get_group_mappings(**vars(parsed_args))
        return ([col[1] for col in self.columns],
                utils.list_to_cols(resp.get('mappings', []), self.columns))

    def get_parser(self, prog_name):
        parser = super(CliGetGroupMappings, self).get_parser(prog_name)
        parser.add_argument('group_id', type=str, help='Group ID')
        return parser


class CliGetGroupThresholds(lister.Lister):
    """Get all thresholds for the given group."""

    columns = [
        ('threshold_id', 'Threshold ID'),
        ('level', 'Level'),
        ('cost', 'Cost'),
        ('type', 'Type'),
        ('field_id', 'Field ID'),
        ('service_id', 'Service ID'),
        ('group_id', 'Group ID'),
        ('tenant_id', 'Project ID'),
    ]

    def take_action(self, parsed_args):
        client = utils.get_client_from_osc(self)
        resp = client.rating.hashmap.get_group_thresholds(**vars(parsed_args))
        return ([col[1] for col in self.columns],
                utils.list_to_cols(resp.get('thresholds', []), self.columns))

    def get_parser(self, prog_name):
        parser = super(CliGetGroupThresholds, self).get_parser(prog_name)
        parser.add_argument('group_id', type=str, help='Group ID')
        return parser


class CliGetThreshold(lister.Lister):
    """Get a Hashmap threshold."""

    columns = [
        ('threshold_id', 'Threshold ID'),
        ('level', 'Level'),
        ('cost', 'Cost'),
        ('type', 'Type'),
        ('field_id', 'Field ID'),
        ('service_id', 'Service ID'),
        ('group_id', 'Group ID'),
        ('tenant_id', 'Project ID'),
    ]

    def take_action(self, parsed_args):
        resp = utils.get_client_from_osc(self).rating.hashmap.get_threshold(
            threshold_id=parsed_args.threshold_id,
        )
        values = utils.list_to_cols([resp], self.columns)
        return [col[1] for col in self.columns], values

    def get_parser(self, prog_name):
        parser = super(CliGetThreshold, self).get_parser(prog_name)
        parser.add_argument('threshold_id', type=str,
                            help='Threshold ID to filter on')
        return parser


class CliListThreshold(lister.Lister):
    """List Hashmap thresholds"""
    columns = [
        ('threshold_id', 'Threshold ID'),
        ('level', 'Level'),
        ('cost', 'Cost'),
        ('type', 'Type'),
        ('field_id', 'Field ID'),
        ('service_id', 'Service ID'),
        ('group_id', 'Group ID'),
        ('tenant_id', 'Project ID'),
    ]

    def take_action(self, parsed_args):
        resp = utils.get_client_from_osc(self).rating.hashmap.get_threshold(
            **vars(parsed_args))
        values = utils.list_to_cols(resp['thresholds'], self.columns)
        return [col[1] for col in self.columns], values

    def get_parser(self, prog_name):
        parser = super(CliListThreshold, self).get_parser(prog_name)
        parser.add_argument('-s', '--service-id', type=str,
                            help='Service ID to filter on')
        parser.add_argument('-g', '--group-id', type=str,
                            help='Group ID to filter on')
        parser.add_argument('--field-id', type=str,
                            help='Field ID to filter on')
        parser.add_argument('-p', '--project-id', type=str, dest='tenant_id',
                            help='Project ID to filter on')
        parser.add_argument('--filter-tenant', action='store_true',
                            help='Explicitly filter on given tenant (allows '
                            'to filter on tenant being None)')
        parser.add_argument('--no-group', action='store_true',
                            help='Filter on orphaned thresholds')
        return parser


class CliCreateThreshold(lister.Lister):
    """Create a Hashmap threshold."""
    columns = [
        ('threshold_id', 'Threshold ID'),
        ('level', 'Level'),
        ('cost', 'Cost'),
        ('type', 'Type'),
        ('field_id', 'Field ID'),
        ('service_id', 'Service ID'),
        ('group_id', 'Group ID'),
        ('tenant_id', 'Project ID'),
    ]

    def take_action(self, parsed_args):
        resp = utils.get_client_from_osc(self).rating.hashmap.create_threshold(
            **vars(parsed_args))
        values = utils.list_to_cols([resp], self.columns)
        return [col[1] for col in self.columns], values

    def get_parser(self, prog_name):
        parser = super(CliCreateThreshold, self).get_parser(prog_name)
        parser.add_argument('-s', '--service-id', type=str, help='Service ID')
        parser.add_argument('-g', '--group-id', type=str, help='Group ID')
        parser.add_argument('--field-id', type=str, help='Field ID')
        parser.add_argument('-p', '--project-id', type=str, dest='tenant_id',
                            help='Project ID')
        parser.add_argument('-t', '--type', type=str, help='Threshold type')
        parser.add_argument('level', type=str, help='Threshold level')
        parser.add_argument('cost', type=float, help='Cost')
        return parser


class CliDeleteThreshold(command.Command):
    """Delete a Hashmap threshold."""

    def take_action(self, parsed_args):
        utils.get_client_from_osc(self).rating.hashmap.delete_threshold(
            **vars(parsed_args))

    def get_parser(self, prog_name):
        parser = super(CliDeleteThreshold, self).get_parser(prog_name)
        parser.add_argument('threshold_id', type=str, help='Threshold ID')
        return parser


class CliUpdateThreshold(lister.Lister):
    """Update a Hashmap threshold."""

    columns = [
        ('threshold_id', 'Threshold ID'),
        ('level', 'Level'),
        ('cost', 'Cost'),
        ('type', 'Type'),
        ('field_id', 'Field ID'),
        ('service_id', 'Service ID'),
        ('group_id', 'Group ID'),
        ('tenant_id', 'Project ID'),
    ]

    def take_action(self, parsed_args):
        resp = utils.get_client_from_osc(self).rating.hashmap.update_threshold(
            **vars(parsed_args))
        values = utils.list_to_cols([resp], self.columns)
        return [col[1] for col in self.columns], values

    def get_parser(self, prog_name):
        parser = super(CliUpdateThreshold, self).get_parser(prog_name)
        parser.add_argument('-s', '--service-id', type=str, help='Service ID')
        parser.add_argument('-g', '--group-id', type=str, help='Group ID')
        parser.add_argument('--field-id', type=str, help='Field ID')
        parser.add_argument('-p', '--project-id', type=str, dest='tenant_id',
                            help='Project ID')
        parser.add_argument('-l', '--level', type=str, help='Threshold level')
        parser.add_argument('--cost', type=str, help='Cost')
        parser.add_argument('threshold_id', type=str, help='Threshold ID')
        return parser

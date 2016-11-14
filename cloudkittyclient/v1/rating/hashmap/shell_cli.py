# Copyright 2016 Objectif Libre
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

import functools

from osc_lib.command import command
from oslo_utils import strutils

from cloudkittyclient.v1.rating.hashmap import shell


_bool_strict = functools.partial(strutils.bool_from_string, strict=True)


class CliHashmapServiceCreate(command.Command):
    """Create a service."""
    def get_parser(self, prog_name):
        parser = super(CliHashmapServiceCreate, self).get_parser(prog_name)
        parser.add_argument('-n', '--name',
                            help='Service name',
                            required=True)
        return parser

    def take_action(self, parsed_args):
        ckclient = self.app.client_manager.rating
        shell.do_hashmap_service_create(ckclient, parsed_args)


class CliHashmapServiceList(command.Command):
    """List services."""
    def take_action(self, parsed_args):
        ckclient = self.app.client_manager.rating
        shell.do_hashmap_service_list(ckclient, parsed_args)


class CliHashmapServiceDelete(command.Command):
    """Delete a service."""
    def get_parser(self, prog_name):
        parser = super(CliHashmapServiceDelete, self).get_parser(prog_name)
        parser.add_argument('-s', '--service-id',
                            help='Service id',
                            required=True)
        return parser

    def take_action(self, parsed_args):
        ckclient = self.app.client_manager.rating
        shell.do_hashmap_service_delete(ckclient, parsed_args)


class CliHashmapFieldCreate(command.Command):
    """Create a field."""
    def get_parser(self, prog_name):
        parser = super(CliHashmapFieldCreate, self).get_parser(prog_name)
        parser.add_argument('-s', '--service-id',
                            help='Service id',
                            required=True)
        parser.add_argument('-n', '--name',
                            help='Field name',
                            required=True)
        return parser

    def take_action(self, parsed_args):
        ckclient = self.app.client_manager.rating
        shell.do_hashmap_field_create(ckclient, parsed_args)


class CliHashmapFieldList(command.Command):
    """List fields."""
    def get_parser(self, prog_name):
        parser = super(CliHashmapFieldList, self).get_parser(prog_name)
        parser.add_argument('-s', '--service-id',
                            help='Service id',
                            required=True)
        return parser

    def take_action(self, parsed_args):
        ckclient = self.app.client_manager.rating
        shell.do_hashmap_field_list(ckclient, parsed_args)


class CliHashmapFieldDelete(command.Command):
    """Delete a field."""
    def get_parser(self, prog_name):
        parser = super(CliHashmapFieldDelete, self).get_parser(prog_name)
        parser.add_argument('-f', '--field-id',
                            help='Field id',
                            required=True)
        return parser

    def take_action(self, parsed_args):
        ckclient = self.app.client_manager.rating
        shell.do_hashmap_field_delete(ckclient, parsed_args)


class CliHashmapMappingCommon(command.Command):
    def get_parser(self, prog_name, cost=False):
        parser = super(CliHashmapMappingCommon, self).get_parser(prog_name)
        parser.add_argument('-c', '--cost',
                            help='Mapping Cost',
                            required=cost)
        parser.add_argument('-v', '--value',
                            help='Mapping Value',
                            required=False)
        parser.add_argument('-t', '--type',
                            help='Mapping type (flat, rate)',
                            required=False)
        parser.add_argument('-g', '--group-id',
                            help='Group id',
                            required=False)
        parser.add_argument('-p', '--project-id',
                            help='Project/Tenant id',
                            required=False)
        return parser


class CliHashmapMappingCreate(CliHashmapMappingCommon):
    """Create a mapping."""
    def get_parser(self, prog_name):
        parser = super(CliHashmapMappingCreate, self).get_parser(prog_name,
                                                                 cost=True)
        parser.add_argument('-s', '--service-id',
                            help='Service id',
                            required=False)
        parser.add_argument('-f', '--field-id',
                            help='Service id',
                            required=False)
        return parser

    def take_action(self, parsed_args):
        ckclient = self.app.client_manager.rating
        shell.do_hashmap_mapping_create(ckclient, parsed_args)


class CliHashmapMappingUpdate(CliHashmapMappingCommon):
    """Update a mapping."""
    def get_parser(self, prog_name):
        parser = super(CliHashmapMappingUpdate, self).get_parser(prog_name)
        parser.add_argument('-m', '--mapping-id',
                            help='Mapping id',
                            required=True)
        return parser

    def take_action(self, parsed_args):
        ckclient = self.app.client_manager.rating
        shell.do_hashmap_mapping_update(ckclient, parsed_args)


class CliHashmapMappingList(command.Command):
    """List mappings."""
    def get_parser(self, prog_name):
        parser = super(CliHashmapMappingList, self).get_parser(prog_name)
        parser.add_argument('-s', '--service-id',
                            help='Service id',
                            required=False)
        parser.add_argument('-f', '--field-id',
                            help='Field id',
                            required=False)
        parser.add_argument('-g', '--group-id',
                            help='Group id',
                            required=False)
        parser.add_argument('-p', '--project-id',
                            help='Project id',
                            required=False)
        return parser

    def take_action(self, parsed_args):
        ckclient = self.app.client_manager.rating
        shell.do_hashmap_mapping_list(ckclient, parsed_args)


class CliHashmapMappingDelete(command.Command):
    """Delete a mapping."""
    def get_parser(self, prog_name):
        parser = super(CliHashmapMappingDelete, self).get_parser(prog_name)
        parser.add_argument('-m', '--mapping-id',
                            help='Mapping id',
                            required=True)
        return parser

    def take_action(self, parsed_args):
        ckclient = self.app.client_manager.rating
        shell.do_hashmap_mapping_delete(ckclient, parsed_args)


class CliHashmapGroupCreate(command.Command):
    """Create a group."""
    def get_parser(self, prog_name):
        parser = super(CliHashmapGroupCreate, self).get_parser(prog_name)
        parser.add_argument('-n', '--name',
                            help='Group name.',
                            required=True)
        return parser

    def take_action(self, parsed_args):
        ckclient = self.app.client_manager.rating
        shell.do_hashmap_group_create(ckclient, parsed_args)


class CliHashmapGroupList(command.Command):
    """List groups."""
    def take_action(self, parsed_args):
        ckclient = self.app.client_manager.rating
        shell.do_hashmap_group_list(ckclient, parsed_args)


class CliHashmapGroupDelete(command.Command):
    """Delete a group."""
    def get_parser(self, prog_name):
        parser = super(CliHashmapGroupDelete, self).get_parser(prog_name)
        parser.add_argument('-g', '--group-id',
                            help='Group uuid',
                            required=True)
        parser.add_argument('-r', '--recursive',
                            help="""Delete the group's mappings.""",
                            required=False,
                            default=False)
        return parser

    def take_action(self, parsed_args):
        ckclient = self.app.client_manager.rating
        shell.do_hashmap_group_delete(ckclient, parsed_args)


class CliHashmapThresholdCommon(command.Command):
    def get_parser(self, prog_name, create=False):
        parser = super(CliHashmapThresholdCommon, self).get_parser(prog_name)
        parser.add_argument('-l', '--level',
                            help='Threshold level',
                            required=create)
        parser.add_argument('-c', '--cost',
                            help='Threshold cost',
                            required=create)
        parser.add_argument('-t', '--type',
                            help='Threshold type',
                            required=False)
        parser.add_argument('-g', '--group-id',
                            help='Group id',
                            required=False)
        parser.add_argument('-p', '--project-id',
                            help='Project/tenant id',
                            required=False)
        return parser


class CliHashmapThresholdCreate(CliHashmapThresholdCommon):
    """Create a threshold."""
    def get_parser(self, prog_name):
        parser = super(CliHashmapThresholdCreate, self).get_parser(prog_name,
                                                                   create=True)
        parser.add_argument('-s', '--service-id',
                            help='Service id',
                            required=False)
        parser.add_argument('-f', '--field-id',
                            help='Field id',
                            required=False)
        return parser

    def take_action(self, parsed_args):
        ckclient = self.app.client_manager.rating
        shell.do_hashmap_threshold_create(ckclient, parsed_args)


class CliHashmapThresholdUpdate(CliHashmapThresholdCommon):
    """Update a threshold."""
    def get_parser(self, prog_name):
        parser = super(CliHashmapThresholdUpdate, self).get_parser(prog_name)
        parser.add_argument('-i', '--threshold-id',
                            help='Threshold id',
                            required=True)
        return parser

    def take_action(self, parsed_args):
        ckclient = self.app.client_manager.rating
        shell.do_hashmap_threshold_update(ckclient, parsed_args)


class CliHashmapThresholdList(command.Command):
    """List thresholds."""
    def get_parser(self, prog_name):
        parser = super(CliHashmapThresholdList, self).get_parser(prog_name)
        parser.add_argument('-s', '--service-id',
                            help='Service id',
                            required=False)
        parser.add_argument('-f', '--field-id',
                            help='Field id',
                            required=False)
        parser.add_argument('-g', '--group-id',
                            help='Group id',
                            required=False)
        parser.add_argument('--no-group',
                            type=_bool_strict, metavar='{True,False}',
                            help='If True, list only orphaned thresholds',
                            required=False)
        parser.add_argument('-p', '--project-id',
                            help='Project/tenant id',
                            required=False)
        return parser

    def take_action(self, parsed_args):
        ckclient = self.app.client_manager.rating
        shell.do_hashmap_threshold_list(ckclient, parsed_args)


class CliHashmapThresholdDelete(command.Command):
    """Delete a threshold."""
    def get_parser(self, prog_name):
        parser = super(CliHashmapThresholdDelete, self).get_parser(prog_name)
        parser.add_argument('-i', '--threshold-id',
                            help='Threshold uuid',
                            required=True)
        return parser

    def take_action(self, parsed_args):
        ckclient = self.app.client_manager.rating
        shell.do_hashmap_threshold_delete(ckclient, parsed_args)


class CliHashmapThresholdGet(command.Command):
    """Get a threshold."""
    def get_parser(self, prog_name):
        parser = super(CliHashmapThresholdGet, self).get_parser(prog_name)
        parser.add_argument('-i', '--threshold-id',
                            help='Threshold uuid',
                            required=True)
        return parser

    def take_action(self, parsed_args):
        ckclient = self.app.client_manager.rating
        shell.do_hashmap_threshold_get(ckclient, parsed_args)


class CliHashmapThresholdGroup(command.Command):
    """Get a threshold group."""
    def get_parser(self, prog_name):
        parser = super(CliHashmapThresholdGroup, self).get_parser(prog_name)
        parser.add_argument('-i', '--threshold-id',
                            help='Threshold uuid',
                            required=True)
        return parser

    def take_action(self, parsed_args):
        ckclient = self.app.client_manager.rating
        shell.do_hashmap_threshold_group(ckclient, parsed_args)

# Copyright 2016 Objectif Libre
#
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

from osc_lib.command import command

from cloudkittyclient.v1.collector import shell


class CliCollectorMappingList(command.Command):
    """List collector mappings."""
    def get_parser(self, prog_name):
        parser = super(CliCollectorMappingList, self).get_parser(prog_name)
        parser.add_argument('-c', '--collector',
                            help='Collector name to filter on.',
                            required=False,
                            default=None)
        return parser

    def take_action(self, parsed_args):
        ckclient = self.app.client_manager.rating
        shell.do_collector_mapping_list(ckclient, parsed_args)


class CliCollectorMappingGet(command.Command):
    """Show collector mapping detail."""
    def get_parser(self, prog_name):
        parser = super(CliCollectorMappingGet, self).get_parser(prog_name)
        parser.add_argument('-s', '--service',
                            help='Which service to get the mapping for.',
                            required=True)
        return parser

    def take_action(self, parsed_args):
        ckclient = self.app.client_manager.rating
        shell.do_collector_mapping_get(ckclient, parsed_args)


class CliCollectorMappingCreate(command.Command):
    """Create collector mappings."""
    def get_parser(self, prog_name):
        parser = super(CliCollectorMappingCreate, self).get_parser(prog_name)
        parser.add_argument('-c', '--collector',
                            help='Map a service to this collector.',
                            required=True)
        parser.add_argument('-s', '--service',
                            help='Map a collector to this service.',
                            required=True)
        return parser

    def take_action(self, parsed_args):
        ckclient = self.app.client_manager.rating
        shell.do_collector_mapping_create(ckclient, parsed_args)


class CliCollectorMappingDelete(command.Command):
    """Delete collector mappings."""
    def get_parser(self, prog_name):
        parser = super(CliCollectorMappingDelete, self).get_parser(prog_name)
        parser.add_argument('-s', '--service',
                            help='Filter on this service',
                            required=True)
        return parser

    def take_action(self, parsed_args):
        ckclient = self.app.client_manager.rating
        shell.do_collector_mapping_delete(ckclient, parsed_args)


class BaseCliCollectorState(command.Command):
    def get_parser(self, prog_name):
        parser = super(BaseCliCollectorState, self).get_parser(prog_name)
        parser.add_argument('-n', '--name',
                            help='Name of the collector',
                            required=True)
        return parser


class CliCollectorStateGet(BaseCliCollectorState):
    """Show collector state."""
    def take_action(self, parsed_args):
        ckclient = self.app.client_manager.rating
        shell.do_collector_state_get(ckclient, parsed_args)


class CliCollectorStateEnable(BaseCliCollectorState):
    """Enable collector state."""
    def take_action(self, parsed_args):
        ckclient = self.app.client_manager.rating
        shell.do_collector_state_enable(ckclient, parsed_args)


class CliCollectorStateDisable(BaseCliCollectorState):
    """Disable collector state."""
    def take_action(self, parsed_args):
        ckclient = self.app.client_manager.rating
        shell.do_collector_state_disable(ckclient, parsed_args)

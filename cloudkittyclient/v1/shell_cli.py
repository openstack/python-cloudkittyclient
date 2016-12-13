# Copyright 2016 Objectif Libre

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

from cloudkittyclient.v1 import shell


class CliModuleList(command.Command):
    """List modules."""
    def take_action(self, parsed_args):
        ckclient = self.app.client_manager.rating
        shell.do_module_list(ckclient, parsed_args)


class CliModuleEnable(command.Command):
    """Enable a module."""
    def get_parser(self, prog_name):
        parser = super(CliModuleEnable, self).get_parser(prog_name)
        parser.add_argument('-n', '--name',
                            help='Module name',
                            required=True)
        return parser

    def take_action(self, parsed_args):
        ckclient = self.app.client_manager.rating
        shell.do_module_enable(ckclient, parsed_args)


class CliModuleDisable(command.Command):
    """Disable a module."""
    def get_parser(self, prog_name):
        parser = super(CliModuleDisable, self).get_parser(prog_name)
        parser.add_argument('-n', '--name',
                            help='Module name',
                            required=True)
        return parser

    def take_action(self, parsed_args):
        ckclient = self.app.client_manager.rating
        shell.do_module_disable(ckclient, parsed_args)


class CliModuleSetPriority(command.Command):
    def get_parser(self, prog_name):
        parser = super(CliModuleSetPriority, self).get_parser(prog_name)
        parser.add_argument('-n', '--name',
                            help='Module name',
                            required=True)
        parser.add_argument('-p', '--priority',
                            help='Module priority',
                            required=True)
        return parser

    def take_action(self, parsed_args):
        ckclient = self.app.client_manager.rating
        shell.do_module_set_priority(ckclient, parsed_args)


class CliInfoGetConfig(command.Command):
    def get_parser(self, prog_name):
        parser = super(CliInfoGetConfig, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        ckclient = self.app.client_manager.rating
        shell.do_info_config_get(ckclient, parsed_args)


class CliInfoGetService(command.Command):
    def get_parser(self, prog_name):
        parser = super(CliInfoGetService, self).get_parser(prog_name)
        parser.add_argument('-n', '--name',
                            help='Service name',
                            required=False)
        return parser

    def take_action(self, parsed_args):
        ckclient = self.app.client_manager.rating
        shell.do_info_service_get(ckclient, parsed_args)

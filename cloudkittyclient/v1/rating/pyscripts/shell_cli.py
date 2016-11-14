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

from cloudkittyclient.v1.rating.pyscripts import shell


_bool_strict = functools.partial(strutils.bool_from_string, strict=True)


class CliPyScriptCreate(command.Command):
    """Create a script."""
    def get_parser(self, prog_name):
        parser = super(CliPyScriptCreate, self).get_parser(prog_name)
        parser.add_argument('-n', '--name',
                            help='Script name',
                            required=True)
        parser.add_argument('-f', '--file',
                            help='Script file',
                            required=False)
        return parser

    def take_action(self, parsed_args):
        ckclient = self.app.client_manager.rating
        shell.do_pyscripts_script_create(ckclient, parsed_args)


class CliPyScriptList(command.Command):
    """List scripts."""
    def get_parser(self, prog_name):
        parser = super(CliPyScriptList, self).get_parser(prog_name)
        parser.add_argument('-d', '--show-data',
                            help='Show data in the listing',
                            required=False,
                            default=False)
        return parser

    def take_action(self, parsed_args):
        ckclient = self.app.client_manager.rating
        shell.do_pyscripts_script_list(ckclient, parsed_args)


class CliPyScriptGet(command.Command):
    """Get script."""
    def get_parser(self, prog_name):
        parser = super(CliPyScriptGet, self).get_parser(prog_name)
        parser.add_argument('-s', '--script-id',
                            help='Script uuid',
                            required=True)
        return parser

    def take_action(self, parsed_args):
        ckclient = self.app.client_manager.rating
        shell.do_pyscripts_script_get(ckclient, parsed_args)


class CliPyScriptGetData(command.Command):
    """Get script data."""
    def get_parser(self, prog_name):
        parser = super(CliPyScriptGetData, self).get_parser(prog_name)
        parser.add_argument('-s', '--script-id',
                            help='Script uuid',
                            required=True)
        return parser

    def take_action(self, parsed_args):
        ckclient = self.app.client_manager.rating
        shell.do_pyscripts_script_get_data(ckclient, parsed_args)


class CliPyScriptDelete(command.Command):
    """Get script data."""
    def get_parser(self, prog_name):
        parser = super(CliPyScriptDelete, self).get_parser(prog_name)
        parser.add_argument('-s', '--script-id',
                            help='Script uuid',
                            required=True)
        return parser

    def take_action(self, parsed_args):
        ckclient = self.app.client_manager.rating
        shell.do_pyscripts_script_delete(ckclient, parsed_args)


class CliPyScriptUpdate(command.Command):
    """Update a script."""
    def get_parser(self, prog_name):
        parser = super(CliPyScriptUpdate, self).get_parser(prog_name)
        parser.add_argument('-s', '--script-id',
                            help='Script uuid',
                            required=True)
        parser.add_argument('-f', '--file',
                            help='Script file',
                            required=True)
        return parser

    def take_action(self, parsed_args):
        ckclient = self.app.client_manager.rating
        shell.do_pyscripts_script_update(ckclient, parsed_args)

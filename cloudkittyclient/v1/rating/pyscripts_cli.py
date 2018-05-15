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


class BaseScriptCli(lister.Lister):

    columns = [
        ('name', 'Name'),
        ('script_id', 'Script ID'),
        ('checksum', 'Checksum'),
        ('data', 'Data'),
    ]


class CliGetScript(BaseScriptCli):
    """Get a PyScript."""

    def take_action(self, parsed_args):
        resp = utils.get_client_from_osc(self).rating.pyscripts.get_script(
            **vars(parsed_args))
        resp = [resp]
        values = utils.list_to_cols(resp, self.columns)
        return [col[1] for col in self.columns], values

    def get_parser(self, prog_name):
        parser = super(CliGetScript, self).get_parser(prog_name)
        parser.add_argument('script_id', type=str, help='Script ID')
        return parser


class CliListScripts(BaseScriptCli):
    """List existing PyScripts."""

    def take_action(self, parsed_args):
        resp = utils.get_client_from_osc(self).rating.pyscripts.list_scripts(
            **vars(parsed_args))
        resp = resp.get('scripts') or []
        values = utils.list_to_cols(resp, self.columns)
        return [col[1] for col in self.columns], values

    def get_parser(self, prog_name):
        parser = super(CliListScripts, self).get_parser(prog_name)
        parser.add_argument(
            '-n', '--no-data', action='store_true',
            help='Set to true to remove script data from output')
        return parser


class CliCreateScript(BaseScriptCli):
    """Create a PyScript."""

    def take_action(self, parsed_args):
        try:
            with open(parsed_args.data, 'r') as fd:
                parsed_args.data = fd.read()
        except IOError:
            pass
        resp = utils.get_client_from_osc(self).rating.pyscripts.create_script(
            **vars(parsed_args))
        resp = [resp]
        values = utils.list_to_cols(resp, self.columns)
        return [col[1] for col in self.columns], values

    def get_parser(self, prog_name):
        parser = super(CliCreateScript, self).get_parser(prog_name)
        parser.add_argument('name', type=str, help='Script Name')
        parser.add_argument('data', type=str, help='Script Data or data file')
        return parser


class CliUpdateScript(BaseScriptCli):
    """Update a PyScript."""

    def take_action(self, parsed_args):
        if parsed_args.data:
            try:
                with open(parsed_args.data, 'r') as fd:
                    parsed_args.data = fd.read()
            except IOError:
                pass
        resp = utils.get_client_from_osc(self).rating.pyscripts.update_script(
            **vars(parsed_args))
        resp = [resp]
        values = utils.list_to_cols(resp, self.columns)
        return [col[1] for col in self.columns], values

    def get_parser(self, prog_name):
        parser = super(CliUpdateScript, self).get_parser(prog_name)
        parser.add_argument('script_id', type=str, help='Script ID')
        parser.add_argument('-n', '--name', type=str, help='Script Name')
        parser.add_argument('-d', '--data', type=str,
                            help='Script Data or data file')
        return parser


class CliDeleteScript(command.Command):
    """Delete a PyScript."""

    def take_action(self, parsed_args):
        utils.get_client_from_osc(self).rating.pyscripts.delete_script(
            **vars(parsed_args))

    def get_parser(self, prog_name):
        parser = super(CliDeleteScript, self).get_parser(prog_name)
        parser.add_argument('script_id', type=str, help='Script ID')
        return parser

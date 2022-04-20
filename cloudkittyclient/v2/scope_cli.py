# Copyright 2019 Objectif Libre
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
from oslo_utils import timeutils

from cloudkittyclient import utils


class CliScopeStateGet(lister.Lister):
    """Get information about current state of several scopes."""
    info_columns = [
        ('scope_id', 'Scope ID'),
        ('scope_key', 'Scope Key'),
        ('collector', 'Collector'),
        ('fetcher', 'Fetcher'),
        ('state', 'State')
    ]

    def get_parser(self, prog_name):
        parser = super(CliScopeStateGet, self).get_parser(prog_name)

        for col in self.info_columns[:-1]:
            parser.add_argument(
                '--' + col[0].replace('_', '-'), type=str,
                action='append', help='Optional filter on ' + col[1])

        parser.add_argument('--offset', type=int, default=0,
                            help='Index of the first scope')
        parser.add_argument('--limit', type=int, default=100,
                            help='Maximal number of scopes')

        return parser

    def take_action(self, parsed_args):
        resp = utils.get_client_from_osc(self).scope.get_scope_state(
            offset=parsed_args.offset,
            limit=parsed_args.limit,
            collector=parsed_args.collector,
            fetcher=parsed_args.fetcher,
            scope_id=parsed_args.scope_id,
            scope_key=parsed_args.scope_key,
        )
        values = utils.list_to_cols(resp['results'], self.info_columns)
        return [col[1] for col in self.info_columns], values


class CliScopeStateReset(command.Command):
    """Reset the state of several scopes."""
    info_columns = [
        ('scope_id', 'Scope ID'),
        ('scope_key', 'Scope Key'),
        ('collector', 'Collector'),
        ('fetcher', 'Fetcher'),
    ]

    def get_parser(self, prog_name):
        parser = super(CliScopeStateReset, self).get_parser(prog_name)

        for col in self.info_columns:
            parser.add_argument(
                '--' + col[0].replace('_', '-'), type=str,
                action='append', help='Optional filter on ' + col[1])

        parser.add_argument(
            '-a', '--all-scopes',
            action='store_true',
            help="Target all scopes at once")

        parser.add_argument(
            'state',
            type=timeutils.parse_isotime,
            help="State iso8601 datetime to which the state should be set. "
            "Example: 2019-06-01T00:00:00Z.")

        return parser

    def take_action(self, parsed_args):
        utils.get_client_from_osc(self).scope.reset_scope_state(
            collector=parsed_args.collector,
            fetcher=parsed_args.fetcher,
            scope_id=parsed_args.scope_id,
            scope_key=parsed_args.scope_key,
            all_scopes=parsed_args.all_scopes,
            state=parsed_args.state,
        )


class CliPatchScope(command.Command):
    """Update scope attributes."""

    info_columns = [
        ('scope_key', 'Scope Key'),
        ('collector', 'Collector'),
        ('fetcher', 'Fetcher'),
        ('active', 'Active'),
    ]

    def get_parser(self, prog_name):
        parser = super(CliPatchScope, self).get_parser(prog_name)

        for col in self.info_columns:
            parser.add_argument(
                '--' + col[0].replace('_', '-'), type=str,
                help='Optional filter on ' + col[1])

        parser.add_argument(
            '-id', '--scope-id', required=True, type=str,
            help="The scope ID to be updated")

        return parser

    def take_action(self, parsed_args):
        return utils.get_client_from_osc(self).scope.update_scope(
            collector=parsed_args.collector,
            fetcher=parsed_args.fetcher,
            scope_id=parsed_args.scope_id,
            scope_key=parsed_args.scope_key,
            active=parsed_args.active)

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
from cliff import lister
from oslo_utils import timeutils

from cloudkittyclient import utils


class CliSummaryGet(lister.Lister):
    """Get a summary for a given period."""

    def get_parser(self, prog_name):
        parser = super(CliSummaryGet, self).get_parser(prog_name)

        def filter_(elem):
            if len(elem.split(':')) != 2:
                raise TypeError
            return str(elem)

        parser.add_argument('--offset', type=int, default=0,
                            help='Index of the first element')
        parser.add_argument('--limit', type=int, default=100,
                            help='Maximal number of elements')
        parser.add_argument('-g', '--groupby', type=str, action='append',
                            help='Attribute to group the summary by. Can be '
                            'specified several times')
        parser.add_argument('--filter', type=filter_, action='append',
                            help="Optional filter, in 'key:value' format. Can "
                            "be specified several times.")
        parser.add_argument('-b', '--begin', type=timeutils.parse_isotime,
                            help="Start of the period to query, in iso8601 "
                            "format. Example: 2019-05-01T00:00:00Z.")
        parser.add_argument('-e', '--end', type=timeutils.parse_isotime,
                            help="End of the period to query, in iso8601 "
                            "format. Example: 2019-06-01T00:00:00Z.")

        return parser

    def take_action(self, parsed_args):
        filters = dict(elem.split(':') for elem in (parsed_args.filter or []))
        resp = utils.get_client_from_osc(self).summary.get_summary(
            offset=parsed_args.offset,
            limit=parsed_args.limit,
            begin=parsed_args.begin,
            end=parsed_args.end,
            filters=filters,
            groupby=parsed_args.groupby,
        )
        columns = [c.replace('_', ' ').capitalize() for c in resp['columns']]
        return columns, resp['results']

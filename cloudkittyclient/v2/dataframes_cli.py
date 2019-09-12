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
import argparse

from cliff import command
from cliff import lister
from oslo_utils import timeutils

from cloudkittyclient import utils


class CliDataframesAdd(command.Command):
    """Add one or several DataFrame objects to the storage backend."""
    def get_parser(self, prog_name):
        parser = super(CliDataframesAdd, self).get_parser(prog_name)

        parser.add_argument(
            'datafile',
            type=argparse.FileType('r'),
            help="File formatted as a JSON object having a DataFrame list"
                 "under a 'dataframes' key."
                 "'-' (hyphen) can be specified for using stdin.",
            )

        return parser

    def take_action(self, parsed_args):
        with parsed_args.datafile as dfile:
            dataframes = dfile.read()
            utils.get_client_from_osc(self).dataframes.add_dataframes(
                dataframes=dataframes,
            )


class CliDataframesGet(lister.Lister):
    """Get dataframes from the storage backend."""
    columns = [
        ('begin', 'Begin'),
        ('end', 'End'),
        ('metric', 'Metric Type'),
        ('unit', 'Unit'),
        ('qty', 'Quantity'),
        ('price', 'Price'),
        ('groupby', 'Group By'),
        ('metadata', 'Metadata'),
    ]

    def get_parser(self, prog_name):
        parser = super(CliDataframesGet, self).get_parser(prog_name)

        def filter_(elem):
            if len(elem.split(':')) != 2:
                raise TypeError
            return str(elem)

        parser.add_argument('--offset', type=int, default=0,
                            help='Index of the first dataframe')
        parser.add_argument('--limit', type=int, default=100,
                            help='Maximal number of dataframes')
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

        dataframes = utils.get_client_from_osc(self).dataframes.get_dataframes(
            offset=parsed_args.offset,
            limit=parsed_args.limit,
            begin=parsed_args.begin,
            end=parsed_args.end,
            filters=filters,
        ).get('dataframes', [])

        def format_(d):
            return ' '.join([
                '{}="{}"'.format(k, v) for k, v in (d or {}).items()])

        values = []
        for df in dataframes:
            period = df['period']
            usage = df['usage']
            for metric_type, points in usage.items():
                for point in points:
                    values.append([
                        period['begin'],
                        period['end'],
                        metric_type,
                        point['vol']['unit'],
                        point['vol']['qty'],
                        point['rating']['price'],
                        format_(point.get('groupby', {})),
                        format_(point.get('metadata', {})),
                    ])

        return [col[1] for col in self.columns], values

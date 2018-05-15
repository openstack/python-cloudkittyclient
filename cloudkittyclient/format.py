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
import csv

from cliff.formatters import base
import jsonpath_rw_ext as jp
from oslo_log import log
import yaml


LOG = log.getLogger(__name__)


class DataframeToCsvFormatter(base.ListFormatter):
    """Cliff formatter allowing to customize CSV report content."""

    default_config = [
        ('Begin', '$.begin'),
        ('End', '$.end'),
        ('Metric Type', '$.service'),
        ('Qty', '$.volume'),
        ('Cost', '$.rating'),
        ('Project ID', '$.desc.project_id'),
        ('Resource ID', '$.desc.resource_id'),
        ('User ID', '$.desc.user_id'),
    ]

    def _load_config(self, filename):
        config = self.default_config
        if filename:
            try:
                with open(filename, 'r') as fd:
                    yml_config = yaml.safe_load(fd.read())
                if len(yml_config):
                    config = [(list(item.keys())[0], list(item.values())[0])
                              for item in yml_config]
                else:
                    LOG.warning('Invalid config file {file}. Using default '
                                'configuration'.format(file=filename))
            except (IOError, yaml.scanner.ScannerError) as err:
                LOG.warning('Error: {err}. Using default '
                            'configuration'.format(err=err))
        self.parsers = {}
        for col, path in config:
            self.parsers[col] = jp.parse(path)
        return config

    def add_argument_group(self, parser):
        group = parser.add_argument_group('dataframe-to-csv formatter')
        group.add_argument('--format-config-file',
                           type=str, dest='format_config',
                           help='Config file for the dict-to-csv formatter')

    def _get_csv_row(self, config, json_item):
        row = {}
        for col, parser in self.parsers.items():
            items = parser.find(json_item)
            row[col] = items[0].value if items else ''
        return row

    def emit_list(self, column_names, data, stdout, parsed_args):
        config = self._load_config(vars(parsed_args).get('format_config'))
        self.writer = csv.DictWriter(stdout,
                                     fieldnames=[elem[0] for elem in config])
        self.writer.writeheader()
        for dataframe in data:
            rating_data = dataframe[3]
            for item in rating_data:
                item['begin'] = dataframe[0]
                item['end'] = dataframe[1]
                row = self._get_csv_row(config, item)
                self.writer.writerow(row)
